"""
API routes for database interaction (videos + metrics + model analysis).
"""

import os
import cv2
from fastapi import APIRouter, HTTPException

from backend.app.db.models import VideoMetricCreate, VideoCreate
from backend.app.db.services import (
    insert_video,
    get_all_videos,
    insert_video_metric,
    get_metrics_for_video,
)
from backend.app.db.utils import extract_video_metadata
from backend.app.analyze_video import get_complete_video_info
from backend.app.download_video import download_video
from backend.app.core.utils import generate_video_path
from backend.app.model.inference import LogoDetector
from backend.app.db.supabase_client import supabase

router = APIRouter(prefix="/db", tags=["database"])


# -------------------------------
# Save video metadata + contract info
# -------------------------------
@router.post("/save-video-info")
def save_video_info(video: VideoCreate):
    """
    Extract video metadata from URL, analyze technical info,
    and save it to Supabase with contract requirements.
    """
    try:
        # 1. Extract metadata from URL (yt-dlp)
        metadata = extract_video_metadata(video.url)

        # 2. Download video temporarily to analyze technical info
        video_path = generate_video_path(prefix="video")
        download_video(video.url, video_path)
        video_info = get_complete_video_info(video_path)

        # 3. Merge metadata + technical info + contract info
        video_record = {
            "url": metadata["url"],
            "platform": metadata["platform"],
            "influencer": metadata.get("influencer"),
            "title": metadata.get("title"),
            "description": metadata.get("description"),
            "duration_seconds": metadata.get("duration_seconds") or int(video_info["duration_seconds"]),
            "likes": metadata.get("likes"),
            "comments": metadata.get("comments"),
            "views": metadata.get("views"),
            "brand": video.brand,
            "contract_price": video.contract_price,
            "min_brand_time": video.min_brand_time,
            "min_logo_area": video.min_logo_area,
            "path": video_path,  # importante para localizar el archivo local
        }

        # 4. Save to Supabase
        result = insert_video(video_record)

        return {
            "message": "✅ Video metadata + contract info saved successfully",
            "supabase_record": result,
            "technical_info": video_info,
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving video info: {str(e)}")


# -------------------------------
# Video listing
# -------------------------------
@router.get("/videos")
def list_videos():
    """
    Retrieve all stored videos from Supabase.
    """
    return get_all_videos()


# -------------------------------
# Metrics endpoints
# -------------------------------
@router.post("/metrics")
def create_metric(metric: VideoMetricCreate):
    result = insert_video_metric(metric.model_dump())
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert metric")
    return result


@router.get("/metrics/{video_id}")
def list_metrics(video_id: str):
    return get_metrics_for_video(video_id)


# -------------------------------
# Analyze video with YOLO and save metrics
# -------------------------------
@router.post("/analyze-video/{video_id}")
def analyze_video_and_save_metrics(video_id: str):
    """
    Analyze a stored video with YOLO, calculate metrics,
    save them into Supabase, and export 4 frames with detections.
    """
    # 1. Fetch video from Supabase
    video = supabase.table("videos").select("*").eq("id", video_id).execute().data
    if not video:
        raise HTTPException(status_code=404, detail="Video not found in DB")
    video = video[0]

    video_path = video.get("path")
    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Local video file not available")

    # 2. Prepare YOLO detector
    detector = LogoDetector()
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count, detections_total = 0, []
    saved_frames = 0
    output_dir = "runs/debug_frames"
    os.makedirs(output_dir, exist_ok=True)
    screenshot_paths = []

    frame_height, frame_width = None, None # Inicializar dimensiones del frame

    # 3. Loop through frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # guardar dimensiones del primer frame válido
        if frame_height is None or frame_width is None:
            frame_height, frame_width = frame.shape[:2]

        detections = detector.predict_frame(frame, conf=0.25, iou=0.6)
        if detections:
            detections_total.extend(detections)

            if saved_frames < 4:
                for det in detections:
                    x1, y1, x2, y2 = det["bbox"]
                    label = f"{det['class']} {det['confidence']:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                    )
                out_path = os.path.join(output_dir, f"{video_id}_frame{frame_count}.jpg")
                cv2.imwrite(out_path, frame)
                screenshot_paths.append(out_path)
                saved_frames += 1

    cap.release()

    if not detections_total:
        return {"message": "⚠️ No logos detected in video"}

    # 4. Calculate metrics
    video_duration = frame_count / fps if fps > 0 else 1
    frames_with_logo = len(detections_total)
    total_time = frames_with_logo / fps if fps > 0 else 0
    avg_area = sum(
        ((det["bbox"][2] - det["bbox"][0]) * (det["bbox"][3] - det["bbox"][1]))
        for det in detections_total
    ) / (frame_count * (frame_height * frame_width))

    metric_record = {
        "video_id": video_id,
        "brand": detections_total[0]["class"],  # simplificación: primera marca detectada
        "total_time_seconds": total_time,
        "percentage_time": total_time / video_duration * 100,
        "average_area_percentage": avg_area * 100,
        "confidence_score": sum(det["confidence"] for det in detections_total)
        / len(detections_total),
    }

    result = insert_video_metric(metric_record)
    return {
        "message": "✅ Metrics saved",
        "metrics": result,
        "screenshots": screenshot_paths,
    }


# -------------------------------
# Get detections for visualization (frontend)
# -------------------------------
@router.get("/detections/{video_id}")
def get_detections(video_id: str):
    """
    Return raw detections frame by frame for a video (JSON format).
    Useful for frontend overlays.
    """
    video = supabase.table("videos").select("*").eq("id", video_id).execute().data
    if not video:
        raise HTTPException(status_code=404, detail="Video not found in DB")
    video = video[0]

    video_path = video.get("path")
    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Local video file not available")

    detector = LogoDetector()
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    detections_json = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        detections = detector.predict_frame(frame, conf=0.25, iou=0.6)
        for det in detections:
            detections_json.append(
                {
                    "frame": frame_idx,
                    "class": det["class"],
                    "confidence": det["confidence"],
                    "bbox": det["bbox"],
                }
            )
    cap.release()

    return {"video_id": video_id, "detections": detections_json}
