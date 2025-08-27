"""
Utilidades comunes para el sistema de análisis de video
"""
import os
import uuid
import time
from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any
from .config import VIDEO_CONFIG, QUALITY_THRESHOLDS, SYSTEM_MESSAGES

def generate_unique_video_id() -> str:
    """Generar ID único para video"""
    return str(uuid.uuid4())[:8]

def generate_video_path(base_dir: str = None, prefix: str = "video") -> str:
    """Generar ruta única para video"""
    if base_dir is None:
        base_dir = VIDEO_CONFIG['output_directory']
    
    os.makedirs(base_dir, exist_ok=True)
    video_id = generate_unique_video_id()
    return os.path.join(base_dir, f"{prefix}_{video_id}.mp4")

def validate_video_file(file_path: str) -> bool:
    """Validar que el archivo de video existe y es válido"""
    if not os.path.exists(file_path):
        return False
    
    # Verificar extensión
    _, ext = os.path.splitext(file_path)
    return ext.lower() in VIDEO_CONFIG['supported_extensions']

def get_video_quality_from_height(height: int) -> str:
    """Determinar calidad del video basado en la altura"""
    if height >= QUALITY_THRESHOLDS['4K_ULTRA_HD']:
        return "4K Ultra HD"
    elif height >= QUALITY_THRESHOLDS['2K_QHD']:
        return "2K/QHD"
    elif height >= QUALITY_THRESHOLDS['FULL_HD']:
        return "Full HD"
    elif height >= QUALITY_THRESHOLDS['HD']:
        return "HD"
    elif height >= QUALITY_THRESHOLDS['SD']:
        return "SD"
    else:
        return "Baja resolución"

def calculate_scaled_dimensions(
    original_width: int, 
    original_height: int, 
    scale_factor: float = 0.5, 
    min_height: int = 640
) -> Tuple[int, int, bool]:
    """
    Calcular dimensiones escaladas para un video
    
    Args:
        original_width: Ancho original
        original_height: Alto original
        scale_factor: Factor de escala (0.1-1.0)
        min_height: Altura mínima para aplicar escalado
    
    Returns:
        Tupla con (nuevo_ancho, nuevo_alto, fue_redimensionado)
    """
    if original_height <= min_height:
        return original_width, original_height, False
    
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    # Asegurar dimensiones pares para compatibilidad con codecs
    if new_width % 2 != 0:
        new_width += 1
    if new_height % 2 != 0:
        new_height += 1
    
    return new_width, new_height, True

def format_duration(seconds: float) -> str:
    """Formatear duración en formato legible"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def format_file_size(bytes_size: int) -> str:
    """Formatear tamaño de archivo en formato legible"""
    if bytes_size < 1024:
        return f"{bytes_size}B"
    elif bytes_size < 1024**2:
        return f"{bytes_size/1024:.1f}KB"
    elif bytes_size < 1024**3:
        return f"{bytes_size/(1024**2):.1f}MB"
    else:
        return f"{bytes_size/(1024**3):.2f}GB"

def get_system_message(key: str, default: str = "") -> str:
    """Obtener mensaje del sistema por clave"""
    return SYSTEM_MESSAGES.get(key, default)

def create_processing_log_entry(
    video_path: str,
    success: bool,
    processing_time: float = 0.0,
    error_message: str = None,
    additional_info: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Crear entrada de log para procesamiento"""
    entry = {
        'timestamp': datetime.now().isoformat(),
        'video_path': video_path,
        'video_name': os.path.basename(video_path),
        'success': success,
        'processing_time': processing_time,
        'processing_time_formatted': format_duration(processing_time)
    }
    
    if error_message:
        entry['error_message'] = error_message
    
    if additional_info:
        entry.update(additional_info)
    
    return entry

def validate_fps(fps: float) -> bool:
    """Validar que el FPS sea válido"""
    return 1.0 <= fps <= 60.0

def validate_scale_factor(factor: float) -> bool:
    """Validar que el factor de escala sea válido"""
    return 0.1 <= factor <= 1.0

def validate_url(url: str) -> bool:
    """Validación básica de URL"""
    return url.startswith(('http://', 'https://')) and len(url.strip()) > 10

def cleanup_old_videos(directory: str, max_age_hours: int = 24) -> int:
    """
    Limpiar videos antiguos del directorio
    
    Args:
        directory: Directorio a limpiar
        max_age_hours: Edad máxima en horas
    
    Returns:
        Número de archivos eliminados
    """
    if not os.path.exists(directory):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except OSError:
                    continue
    
    return deleted_count

def get_available_videos(directory: str) -> List[str]:
    """Obtener lista de videos disponibles en directorio"""
    if not os.path.exists(directory):
        return []
    
    videos = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if validate_video_file(file_path):
            videos.append(file_path)
    
    return sorted(videos)

class Timer:
    """Utilidad para medir tiempo de ejecución"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Iniciar cronómetro"""
        self.start_time = time.time()
        return self
    
    def stop(self) -> float:
        """Detener cronómetro y retornar tiempo transcurrido"""
        self.end_time = time.time()
        return self.elapsed_time()
    
    def elapsed_time(self) -> float:
        """Obtener tiempo transcurrido"""
        if self.start_time is None:
            return 0.0
        
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

def performance_monitor(func_name: str = "operation"):
    """Decorator para monitorear rendimiento de funciones"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with Timer() as timer:
                result = func(*args, **kwargs)
            
            print(f"⏱️  {func_name} completado en {timer.elapsed_time():.2f}s")
            return result
        return wrapper
    return decorator
