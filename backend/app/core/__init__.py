"""
Core package para el sistema de análisis de video
Contiene configuraciones, modelos y utilidades globales
"""

from .config import *
from .models import *
from .state import *
from .utils import *

__version__ = "1.0.0"
__author__ = "Sistema de Análisis de Video"
__description__ = "Core components for video analysis system"

# Exportaciones principales
__all__ = [
    # Config
    'API_CONFIG',
    'CORS_CONFIG', 
    'DEFAULT_STREAM_CONFIG',
    'VIDEO_CONFIG',
    'DOWNLOAD_CONFIG',
    'PROCESSING_CONFIG',
    'QUALITY_THRESHOLDS',
    'SYSTEM_MESSAGES',
    'STREAMING_HEADERS',
    'EXAMPLE_URLS',
    
    # Models
    'VideoRequest',
    'VideoInfo',
    'StreamConfig',
    'ProcessingResponse',
    'ErrorResponse',
    'HealthResponse',
    'StatisticsResponse',
    'VideoQuality',
    
    # State
    'global_state',
    'get_current_video_path',
    'set_current_video_path',
    'get_video_info',
    'set_video_info',
    'get_stream_config',
    'update_stream_config',
    'get_system_stats',
    'increment_processed_videos',
    'add_processing_history',
    'active_stream',
    
    # Utils
    'generate_unique_video_id',
    'generate_video_path',
    'validate_video_file',
    'get_video_quality_from_height',
    'calculate_scaled_dimensions',
    'format_duration',
    'format_file_size',
    'get_system_message',
    'create_processing_log_entry',
    'validate_fps',
    'validate_scale_factor',
    'validate_url',
    'cleanup_old_videos',
    'get_available_videos',
    'Timer',
    'performance_monitor'
]
