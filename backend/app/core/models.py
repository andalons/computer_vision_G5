"""
Modelos de datos usando Pydantic para validación
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum

class VideoQuality(str, Enum):
    """Enum para calidades de video"""
    ULTRA_HD_4K = "4K Ultra HD"
    QHD_2K = "2K/QHD"
    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LOW_RES = "Baja resolución"

class VideoRequest(BaseModel):
    """Modelo para peticiones de procesamiento de video"""
    url: str = Field(..., description="URL del video a procesar")
    scale_factor: float = Field(
        default=0.5, 
        ge=0.1, 
        le=1.0,
        description="Factor de escala para redimensionar (0.1-1.0)"
    )
    min_height: int = Field(
        default=640,
        ge=240,
        le=2160,
        description="Altura mínima para aplicar redimensionamiento"
    )
    fps_limit: float = Field(
        default=30.0,
        ge=1.0,
        le=60.0,
        description="FPS máximo para el streaming"
    )
    delay_frames: float = Field(
        default=0.033,
        ge=0.01,
        le=1.0,
        description="Delay en segundos entre frames"
    )
    delete_after_processing: bool = Field(
        default=True,
        description="Si True, elimina el video después del procesamiento"
    )

    @validator('fps_limit')
    def validate_fps(cls, v):
        """Validar que el FPS sea un valor razonable"""
        if v <= 0:
            raise ValueError('FPS debe ser mayor que 0')
        return v

    @validator('delay_frames', pre=True, always=True)
    def calculate_delay_from_fps(cls, v, values):
        """Calcular delay automáticamente basado en FPS si no se proporciona"""
        if 'fps_limit' in values and values['fps_limit'] > 0:
            return 1.0 / values['fps_limit']
        return v

class VideoInfo(BaseModel):
    """Modelo para información detallada del video"""
    path: str
    filename: str
    width: int
    height: int
    fps: float
    total_frames: int
    duration_seconds: float
    duration_minutes: float
    duration_hours: float
    codec: str
    size_bytes: int
    size_kb: float
    size_mb: float
    size_gb: float
    resolution: str
    aspect_ratio: float
    bitrate_kbps: float
    color_channels: int
    color_type: str
    quality: Optional[VideoQuality] = None

    @validator('quality', pre=True, always=True)
    def determine_quality(cls, v, values):
        """Determinar la calidad basada en la altura"""
        if 'height' not in values:
            return v
        
        height = values['height']
        if height >= 2160:
            return VideoQuality.ULTRA_HD_4K
        elif height >= 1440:
            return VideoQuality.QHD_2K
        elif height >= 1080:
            return VideoQuality.FULL_HD
        elif height >= 720:
            return VideoQuality.HD
        elif height >= 480:
            return VideoQuality.SD
        else:
            return VideoQuality.LOW_RES

class StreamConfig(BaseModel):
    """Configuración para streaming"""
    fps_limit: float = Field(default=15.0, ge=1.0, le=60.0)
    scale_factor: float = Field(default=0.6, ge=0.1, le=1.0)
    min_height: int = Field(default=640, ge=240, le=2160)
    delay_frames: float = Field(default=0.067, ge=0.01, le=1.0)

class ProcessingResponse(BaseModel):
    """Respuesta del procesamiento de video"""
    message: str
    video_path: str
    video_info: Optional[Dict[str, Any]] = None
    stream_config: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    success: bool = True

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: bool = True
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None

class HealthResponse(BaseModel):
    """Respuesta del health check"""
    status: str = "healthy"
    version: str = "1.0.0"
    uptime: Optional[float] = None
    active_streams: int = 0

class StatisticsResponse(BaseModel):
    """Respuesta con estadísticas del sistema"""
    total_videos_processed: int = 0
    active_streams: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    supported_formats: list = []
    system_info: Optional[Dict[str, Any]] = None
