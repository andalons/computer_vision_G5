"""
Configuraciones globales del sistema de análisis de video
"""

# Configuración de la aplicación FastAPI
API_CONFIG = {
    "title": "API de Streaming de Video Simple",
    "version": "1.0.0",
    "description": "Sistema de análisis de video con streaming en tiempo real",
    "host": "0.0.0.0",
    "port": 8000
}

# Configuración de CORS
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

# Configuración de streaming por defecto
DEFAULT_STREAM_CONFIG = {
    'fps_limite': 15.0,
    'factor_escala': 0.6,
    'altura_minima': 640,
    'delay_frames': 0.067  # ~15 FPS por defecto
}

# Configuración de video
VIDEO_CONFIG = {
    'output_directory': 'videos_descargados',
    'supported_extensions': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'],
    'default_quality': 85,  # JPEG quality para streaming
    'max_file_size_mb': 500,  # Tamaño máximo de archivo en MB
}

# Configuración de descarga
DOWNLOAD_CONFIG = {
    'format': 'mp4/bestaudio/best',
    'quiet': True,
    'timeout': 300,  # 5 minutos timeout
    'max_retries': 3
}

# Configuración de procesamiento
PROCESSING_CONFIG = {
    'max_concurrent_downloads': 3,
    'thread_pool_size': 4,
    'frame_log_interval': 100,  # Log cada X frames
    'default_fps': 30.0
}

# Configuración de calidad de video
QUALITY_THRESHOLDS = {
    '4K_ULTRA_HD': 2160,
    '2K_QHD': 1440,
    'FULL_HD': 1080,
    'HD': 720,
    'SD': 480,
    'LOW_RES': 240
}

# Mensajes del sistema
SYSTEM_MESSAGES = {
    'downloading': '📥 Descargando',
    'downloaded': '✅ Video descargado',
    'processing': '🎬 Iniciando análisis de',
    'completed': '✅ Análisis completado',
    'error': '❌ Error',
    'preparing': '⏳ Preparando video...',
    'streaming': '🎬 Análisis iniciado',
    'stopped': '⏹️ Análisis detenido'
}

# Configuración de logging
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# Configuración de headers HTTP para streaming
STREAMING_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0"
}

# URLs de ejemplo para testing
EXAMPLE_URLS = {
    'sample_video': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
    'instagram_reel': 'https://www.instagram.com/dulceida/reel/C2pBKGKiDSR/',
    'youtube_short': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
}
