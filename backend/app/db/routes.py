"""
API routes for database interaction
"""

from fastapi import APIRouter, HTTPException
from .models import VideoCreate, VideoMetricCreate
from .services import insert_video, get_all_videos, insert_video_metric, get_metrics_for_video

router = APIRouter(prefix="/db", tags=["database"])

@router.post("/videos")
def create_video(video: VideoCreate):
    result = insert_video(video)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert video")
    return result

@router.get("/videos")
def list_videos():
    return get_all_videos()

@router.post("/metrics")
def create_metric(metric: VideoMetricCreate):
    result = insert_video_metric(metric)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert metric")
    return result

@router.get("/metrics/{video_id}")
def list_metrics(video_id: str):
    return get_metrics_for_video(video_id)
