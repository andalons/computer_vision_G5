"""
API routes for database interaction (videos + metrics).
"""

from fastapi import APIRouter, HTTPException
from .models import VideoMetricCreate, VideoCreate
from .services import insert_video, get_all_videos, insert_video_metric, get_metrics_for_video
from .utils import extract_video_metadata

from ..analyze_video import get_complete_video_info
from ..download_video import download_video
from ..core.utils import generate_video_path  # para crear ruta temporal

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
        }

        # 4. Save to Supabase
        result = insert_video(video_record)

        return {
            "message": "✅ Video metadata + contract info saved successfully",
            "supabase_record": result,
            "technical_info": video_info
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
