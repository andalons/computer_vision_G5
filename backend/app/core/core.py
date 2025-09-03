"""
Core principal del sistema de análisis de video
Punto de entrada centralizado para todas las funcionalidades core
"""

import os
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from core.config import *
from core.models import *
from core.state import *
from core.utils import *

class VideoAnalysisCore:
    """
    Clase principal del core del sistema de análisis de video
    Proporciona una interfaz unificada para todas las funcionalidades
    """
    
    def __init__(self):
        """Inicializar el core del sistema"""
        from . import __version__
        self.version = __version__
        self.initialized = True
        self._setup_directories()
    
    def _setup_directories(self):
        """Configurar directorios necesarios"""
        os.makedirs(VIDEO_CONFIG['output_directory'], exist_ok=True)
    
    def get_app_config(self) -> dict:
        """Obtener configuración de la aplicación FastAPI"""
        return API_CONFIG
    
    def get_cors_config(self) -> dict:
        """Obtener configuración de CORS"""
        return CORS_CONFIG
    
    def get_default_stream_config(self) -> dict:
        """Obtener configuración de streaming por defecto"""
        return DEFAULT_STREAM_CONFIG.copy()
    
    def create_video_request(self, url: str, **kwargs) -> VideoRequest:
        """Crear una instancia de VideoRequest con validación"""
        return VideoRequest(url=url, **kwargs)
    
    def generate_unique_video_path(self, prefix: str = "video") -> str:
        """Generar ruta única para video"""
        return generate_video_path(prefix=prefix)
    
    def validate_video_request(self, request_data: dict) -> tuple[bool, str]:
        """
        Validar datos de petición de video
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        try:
            # Validar URL
            if not request_data.get('url') or not validate_url(request_data['url']):
                return False, "URL inválida o vacía"
            
            # Validar FPS si se proporciona
            if 'fps_limit' in request_data:
                if not validate_fps(request_data['fps_limit']):
                    return False, "FPS debe estar entre 1 y 60"
            
            # Validar factor de escala si se proporciona
            if 'scale_factor' in request_data:
                if not validate_scale_factor(request_data['scale_factor']):
                    return False, "Factor de escala debe estar entre 0.1 y 1.0"
            
            # Intentar crear el modelo para validación completa
            VideoRequest(**request_data)
            return True, "Válido"
            
        except Exception as e:
            return False, f"Error de validación: {str(e)}"
    
    def update_global_stream_config(self, new_config: dict):
        """Actualizar configuración global de streaming"""
        update_stream_config(new_config)
    
    def get_current_stats(self) -> dict:
        """Obtener estadísticas actuales del sistema"""
        return get_system_stats()
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> int:
        """Limpiar archivos antiguos"""
        return cleanup_old_videos(
            VIDEO_CONFIG['output_directory'], 
            max_age_hours
        )
    
    def get_available_video_list(self) -> list:
        """Obtener lista de videos disponibles"""
        return get_available_videos(VIDEO_CONFIG['output_directory'])
    
    def create_processing_response(
        self, 
        message: str,
        video_path: str,
        video_info: dict = None,
        stream_config: dict = None,
        processing_time: float = None
    ) -> ProcessingResponse:
        """Crear respuesta de procesamiento estándar"""
        return ProcessingResponse(
            message=message,
            video_path=video_path,
            video_info=video_info,
            stream_config=stream_config,
            processing_time=processing_time
        )
    
    def create_error_response(
        self,
        message: str,
        detail: str = None,
        error_code: str = None
    ) -> ErrorResponse:
        """Crear respuesta de error estándar"""
        return ErrorResponse(
            message=message,
            detail=detail,
            error_code=error_code
        )
    
    def get_system_info(self) -> dict:
        """Obtener información completa del sistema"""
        return {
            'version': self.version,
            'initialized': self.initialized,
            'video_config': VIDEO_CONFIG,
            'processing_config': PROCESSING_CONFIG,
            'quality_thresholds': QUALITY_THRESHOLDS,
            'supported_extensions': VIDEO_CONFIG['supported_extensions'],
            'stats': self.get_current_stats(),
            'available_videos': len(self.get_available_video_list())
        }
    
    def start_processing_timer(self) -> Timer:
        """Iniciar cronómetro para procesamiento"""
        return Timer().start()
    
    def log_processing_result(
        self,
        video_path: str,
        success: bool,
        processing_time: float = 0.0,
        error_message: str = None
    ):
        """Registrar resultado de procesamiento"""
        add_processing_history(video_path, success, processing_time, error_message)
        
        if success:
            increment_processed_videos(processing_time)

# Instancia global del core
core = VideoAnalysisCore()

def get_core() -> VideoAnalysisCore:
    """Obtener instancia global del core"""
    return core

def initialize_core() -> VideoAnalysisCore:
    """Inicializar el core del sistema"""
    return get_core()

# Funciones de conveniencia que usan el core global
def validate_request(request_data: dict) -> tuple[bool, str]:
    """Validar petición usando el core global"""
    return core.validate_video_request(request_data)

def get_unique_video_path(prefix: str = "video") -> str:
    """Obtener ruta única para video usando el core global"""
    return core.generate_unique_video_path(prefix)

def log_processing(video_path: str, success: bool, processing_time: float = 0.0, error: str = None):
    """Registrar procesamiento usando el core global"""
    core.log_processing_result(video_path, success, processing_time, error)

# Información del módulo
def print_core_info():
    """Imprimir información del core"""
    from . import __version__
    print(f"""
🔧 Video Analysis Core v{__version__}
{'='*50}
📁 Output Directory: {VIDEO_CONFIG['output_directory']}
🎬 Supported Formats: {', '.join(VIDEO_CONFIG['supported_extensions'])}
⚙️ Processing Config: {PROCESSING_CONFIG['thread_pool_size']} threads
📊 Stats: {core.get_current_stats()['total_videos_processed']} videos processed
🚀 Status: {'Initialized' if core.initialized else 'Not Initialized'}
{'='*50}
    """)

if __name__ == "__main__":
    # Mostrar información cuando se ejecuta directamente
    print_core_info()
