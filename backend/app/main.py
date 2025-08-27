#!/usr/bin/env python3
"""
Procesado de video para su análisis con un modelo de visión artificial
Ahora usando el sistema core centralizado
"""
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Intentar importar del core, si falla usar configuración de respaldo
try:
    from .core import (
        core, API_CONFIG, CORS_CONFIG, VideoRequest, 
        get_current_video_path, set_current_video_path,
        get_video_info, set_video_info,
        get_stream_config, update_stream_config,
        active_stream, Timer, get_system_message,
        generate_video_path
    )
    USE_CORE = True
    print("✅ Core importado exitosamente")
except ImportError as e:
    print(f"⚠️  Error importando core: {e}")
    print("🔄 Usando configuración de respaldo...")
    USE_CORE = False
    
    # Configuración de respaldo
    API_CONFIG = {
        "title": "API de Streaming de Video Simple",
        "version": "1.0.0"
    }
    
    CORS_CONFIG = {
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"]
    }
    
    # Variables de estado global de respaldo
    current_video_path = None
    video_info_global = None
    stream_config = {
        'fps_limite': 15.0,
        'factor_escala': 0.6,
        'altura_minima': 640,
        'delay_frames': 0.067
    }
    
    class VideoRequest(BaseModel):
        url: str
        factor_escala: float = 0.5
        altura_minima: int = 640
        fps_limite: float = 30.0
        delay_frames: float = 0.033

from .descargar_video import descargar_video
from .analizar_video import obtener_info_completa_video
from .procesar_video_local import generate_video_stream
import uuid

# Funciones de respaldo cuando no se usa el core
def generate_video_path_fallback(prefix="video"):
    """Generar ruta de video como respaldo"""
    os.makedirs('videos_descargados', exist_ok=True)
    video_id = str(uuid.uuid4())[:8]
    return f"videos_descargados/{prefix}_{video_id}.mp4"

def get_system_message_fallback(key, default=""):
    """Obtener mensajes del sistema como respaldo"""
    messages = {
        'downloading': '📥 Descargando',
        'downloaded': '✅ Video descargado',
        'processing': '🎬 Iniciando análisis de',
        'error': '❌ Error'
    }
    return messages.get(key, default)

app = FastAPI(**API_CONFIG)

# Configurar CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

print("🔧 CORS configurado correctamente")

# El estado ahora se maneja a través del core
# Variables globales movidas a core/state.py
# VideoRequest importado desde core

@app.get("/")
async def root():
    """Información básica del proyecto"""
    info = {
        "titulo": "API de Análisis de Video",
        "equipo": "Grupo 5",
        "version": "1.0.0",
        "descripcion": "Proyecto de vision artificial para analisis de video."
    }
    return info

@app.post("/prepare-video")
async def prepare_video(video_request: VideoRequest):
    """Preparar video para streaming (compatible con y sin core)"""
    global current_video_path, video_info_global, stream_config
    
    try:
        # Generar ruta de video
        if USE_CORE:
            video_path = generate_video_path(prefix="video")
            print(f'{get_system_message("downloading")}: {video_request.url}')
        else:
            video_path = generate_video_path_fallback(prefix="video")
            print(f'{get_system_message_fallback("downloading")}: {video_request.url}')
        
        print(f'⚙️ Configuración: FPS={video_request.fps_limite}, Escala={video_request.factor_escala}')
        
        # Descargar video
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            success = await loop.run_in_executor(
                executor, descargar_video, video_request.url, video_path
            )
        
        if not success:
            raise HTTPException(status_code=400, detail="Error descargando video")
        
        if USE_CORE:
            print(f'{get_system_message("downloaded")}: {video_path}')
        else:
            print(f'{get_system_message_fallback("downloaded")}: {video_path}')
        
        # Obtener información
        with ThreadPoolExecutor() as executor:
            video_info = await loop.run_in_executor(
                executor, obtener_info_completa_video, video_path
            )
        
        # Actualizar estado
        if USE_CORE:
            set_current_video_path(video_path)
            set_video_info(video_info)
            new_config = {
                'fps_limite': video_request.fps_limite,
                'factor_escala': video_request.factor_escala,
                'altura_minima': video_request.altura_minima,
                'delay_frames': video_request.delay_frames
            }
            update_stream_config(new_config)
            current_config = get_stream_config()
        else:
            # Modo de respaldo
            current_video_path = video_path
            video_info_global = video_info
            stream_config.update({
                'fps_limite': video_request.fps_limite,
                'factor_escala': video_request.factor_escala,
                'altura_minima': video_request.altura_minima,
                'delay_frames': video_request.delay_frames
            })
            current_config = stream_config.copy()
        
        return {
            "message": "Video preparado",
            "video_path": video_path,
            "video_info": video_info,
            "stream_config": current_config
        }
        
    except Exception as e:
        error_msg = str(e)
        if USE_CORE:
            print(f'{get_system_message("error")}: {error_msg}')
        else:
            print(f'{get_system_message_fallback("error")}: {error_msg}')
        
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/stream")
async def get_stream():
    """Obtener análisis del vídeo (compatible con y sin core)"""
    global current_video_path, stream_config
    
    # Obtener valores según el modo
    if USE_CORE:
        video_path = get_current_video_path()
        config = get_stream_config()
    else:
        video_path = current_video_path
        config = stream_config
    
    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="No hay vídeo preparado")
    
    if USE_CORE:
        print(f'{get_system_message("processing")}: {video_path}')
    else:
        print(f'{get_system_message_fallback("processing")}: {video_path}')
    
    print(f"⚙️ Config vídeo: {config}")
    
    return StreamingResponse(
        generate_video_stream(
            video_path=video_path,
            factor_escala=config.get('factor_escala', 0.5),
            altura_minima=config.get('altura_minima', 640),
            fps_limite=config.get('fps_limite', 30.0),
            delay_frames=config.get('delay_frames', 0.033)
        ),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/video-info")
async def get_video_info_endpoint():
    """Obtener información del vídeo (compatible con y sin core)"""
    global video_info_global
    
    if USE_CORE:
        video_info = get_video_info()
    else:
        video_info = video_info_global
    
    if not video_info:
        raise HTTPException(status_code=404, detail="No hay información disponible")
    
    return {"video_info": video_info}

@app.get("/stats")
async def get_system_stats():
    """Obtener estadísticas del sistema"""
    if USE_CORE:
        return core.get_system_info()
    else:
        return {
            "message": "Core no disponible - usando modo de respaldo",
            "mode": "fallback",
            "current_video": current_video_path is not None,
            "stream_config": stream_config
        }

@app.get("/health")
async def health_check():
    """Health check del sistema"""
    if USE_CORE:
        stats = core.get_current_stats()
        return {
            "status": "healthy",
            "version": core.version,
            "uptime": stats.get("uptime_seconds", 0),
            "active_streams": stats.get("active_streams", 0),
            "mode": "core"
        }
    else:
        return {
            "status": "healthy",
            "version": "1.0.0",
            "mode": "fallback",
            "message": "Funcionando en modo de respaldo"
        }
