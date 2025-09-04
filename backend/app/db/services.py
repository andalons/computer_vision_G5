"""
Database service layer for videos and metrics
"""

from app.db.supabase_client import supabase
from app.db.models import VideoCreate, VideoMetricCreate
from typing import List, Optional

def insert_video(video_data: dict):
    """Insert video record into Supabase"""
    response = supabase.table("videos").insert(video_data).execute()
    return response.data[0] if response.data else None

def get_all_videos() -> List[dict]:
    response = supabase.table("videos").select("*").execute()
    return response.data or []

def insert_video_metric(metric: VideoMetricCreate) -> Optional[dict]:
    response = supabase.table("video_metrics").insert(metric).execute()
    if response.data:
        return response.data[0]
    return None

def get_metrics_for_video(video_id: str) -> List[dict]:
    response = supabase.table("video_metrics").select("*").eq("video_id", video_id).execute()
    return response.data or []
