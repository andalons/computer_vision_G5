"""
Database service layer for videos and metrics
"""

from .supabase_client import supabase
from .models import VideoCreate, VideoMetricCreate
from typing import List, Optional

def insert_video(video: VideoCreate) -> Optional[dict]:
    response = supabase.table("videos").insert(video.dict()).execute()
    if response.data:
        return response.data[0]
    return None

def get_all_videos() -> List[dict]:
    response = supabase.table("videos").select("*").execute()
    return response.data or []

def insert_video_metric(metric: VideoMetricCreate) -> Optional[dict]:
    response = supabase.table("video_metrics").insert(metric.dict()).execute()
    if response.data:
        return response.data[0]
    return None

def get_metrics_for_video(video_id: str) -> List[dict]:
    response = supabase.table("video_metrics").select("*").eq("video_id", video_id).execute()
    return response.data or []
