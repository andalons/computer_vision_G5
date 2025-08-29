"""
Pydantic models for database entities
"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class VideoCreate(BaseModel):
    url: str
    brand: str  # obligatorio, siempre debe estar
    platform: Optional[str] = None  # detectada automáticamente, no requerida
    influencer: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    duration_seconds: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    views: Optional[int] = None
    contract_price: Optional[float] = None
    min_brand_time: Optional[int] = None  # en segundos
    min_logo_area: Optional[float] = None  # en porcentaje de pantalla

class VideoDB(VideoCreate):
    id: UUID
    created_at: datetime

class VideoMetricCreate(BaseModel):
    video_id: UUID
    brand: str
    total_time_seconds: float
    percentage_time: float
    average_area_percentage: float
    confidence_score: float

class VideoMetricDB(VideoMetricCreate):
    id: UUID
    created_at: datetime
