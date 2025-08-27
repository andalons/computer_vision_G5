"""
Estado global del sistema de análisis de video
"""
import threading
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GlobalState:
    """Clase para mantener el estado global del sistema"""
    
    # Video actual
    current_video_path: Optional[str] = None
    video_info_global: Optional[Dict[str, Any]] = None
    
    # Configuración de streaming
    stream_config: Dict[str, Any] = field(default_factory=lambda: {
        'fps_limite': 15.0,
        'factor_escala': 0.6,
        'altura_minima': 640,
        'delay_frames': 0.067
    })
    
    # Estadísticas del sistema
    start_time: float = field(default_factory=time.time)
    total_videos_processed: int = 0
    active_streams: int = 0
    total_processing_time: float = 0.0
    
    # Historial de procesamiento
    processing_history: list = field(default_factory=list)
    
    # Lock para thread safety
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def get_uptime(self) -> float:
        """Obtener tiempo de actividad en segundos"""
        return time.time() - self.start_time
    
    def increment_processed_videos(self, processing_time: float = 0.0):
        """Incrementar contador de videos procesados"""
        with self._lock:
            self.total_videos_processed += 1
            self.total_processing_time += processing_time
    
    def get_average_processing_time(self) -> float:
        """Obtener tiempo promedio de procesamiento"""
        with self._lock:
            if self.total_videos_processed == 0:
                return 0.0
            return self.total_processing_time / self.total_videos_processed
    
    def add_to_history(self, entry: Dict[str, Any]):
        """Agregar entrada al historial"""
        with self._lock:
            entry['timestamp'] = datetime.now().isoformat()
            self.processing_history.append(entry)
            
            # Mantener solo los últimos 100 registros
            if len(self.processing_history) > 100:
                self.processing_history = self.processing_history[-100:]
    
    def increment_active_streams(self):
        """Incrementar contador de streams activos"""
        with self._lock:
            self.active_streams += 1
    
    def decrement_active_streams(self):
        """Decrementar contador de streams activos"""
        with self._lock:
            self.active_streams = max(0, self.active_streams - 1)
    
    def update_stream_config(self, new_config: Dict[str, Any]):
        """Actualizar configuración de streaming"""
        with self._lock:
            self.stream_config.update(new_config)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas completas del sistema"""
        with self._lock:
            return {
                'uptime_seconds': self.get_uptime(),
                'total_videos_processed': self.total_videos_processed,
                'active_streams': self.active_streams,
                'total_processing_time': self.total_processing_time,
                'average_processing_time': self.get_average_processing_time(),
                'current_video_path': self.current_video_path,
                'stream_config': self.stream_config.copy(),
                'history_count': len(self.processing_history)
            }
    
    def reset_stats(self):
        """Reiniciar estadísticas (mantiene configuración)"""
        with self._lock:
            self.start_time = time.time()
            self.total_videos_processed = 0
            self.active_streams = 0
            self.total_processing_time = 0.0
            self.processing_history.clear()

# Instancia global del estado
global_state = GlobalState()

# Funciones de conveniencia para acceder al estado global
def get_current_video_path() -> Optional[str]:
    """Obtener la ruta del video actual"""
    return global_state.current_video_path

def set_current_video_path(path: str):
    """Establecer la ruta del video actual"""
    global_state.current_video_path = path

def get_video_info() -> Optional[Dict[str, Any]]:
    """Obtener información del video actual"""
    return global_state.video_info_global

def set_video_info(info: Dict[str, Any]):
    """Establecer información del video actual"""
    global_state.video_info_global = info

def get_stream_config() -> Dict[str, Any]:
    """Obtener configuración de streaming"""
    return global_state.stream_config.copy()

def update_stream_config(config: Dict[str, Any]):
    """Actualizar configuración de streaming"""
    global_state.update_stream_config(config)

def get_system_stats() -> Dict[str, Any]:
    """Obtener estadísticas del sistema"""
    return global_state.get_stats()

def increment_processed_videos(processing_time: float = 0.0):
    """Incrementar contador de videos procesados"""
    global_state.increment_processed_videos(processing_time)

def add_processing_history(video_path: str, success: bool, processing_time: float = 0.0, error: str = None):
    """Agregar entrada al historial de procesamiento"""
    entry = {
        'video_path': video_path,
        'success': success,
        'processing_time': processing_time,
        'error': error
    }
    global_state.add_to_history(entry)

# Context managers para manejo de streams activos
class ActiveStreamContext:
    """Context manager para manejar streams activos"""
    
    def __enter__(self):
        global_state.increment_active_streams()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        global_state.decrement_active_streams()

def active_stream():
    """Obtener context manager para stream activo"""
    return ActiveStreamContext()
