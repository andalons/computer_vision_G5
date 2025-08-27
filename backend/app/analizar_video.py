import cv2
import os
import sys


def obtener_info_completa_video(video_path):
    """
    Extrae información detallada del video usando OpenCV
    """
    if not os.path.exists(video_path):
        print(f"Error: El archivo {video_path} no existe")
        return None
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video {video_path}")
        return None
    
    # Obtener todas las propiedades disponibles
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    # Codec información
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    
    # Tamaño del archivo
    file_size_bytes = os.path.getsize(video_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    file_size_kb = file_size_bytes / 1024
    
    # Bitrate aproximado
    bitrate_kbps = (file_size_kb * 8) / duration if duration > 0 else 0
    
    # Leer el primer frame para análisis adicional
    ret, first_frame = cap.read()
    channels = first_frame.shape[2] if ret and len(first_frame.shape) == 3 else 1
    
    info = {
        'ruta': video_path,
        'nombre_archivo': os.path.basename(video_path),
        'ancho': width,
        'alto': height,
        'fps': fps,
        'total_frames': frame_count,
        'duracion_segundos': duration,
        'duracion_minutos': duration / 60,
        'duracion_horas': duration / 3600,
        'codec': codec.strip(),
        'tamaño_bytes': file_size_bytes,
        'tamaño_kb': round(file_size_kb, 2),
        'tamaño_mb': round(file_size_mb, 2),
        'tamaño_gb': round(file_size_mb / 1024, 3),
        'resolucion': f"{width}x{height}",
        'aspecto_ratio': round(width/height, 2) if height > 0 else 0,
        'bitrate_kbps': round(bitrate_kbps, 2),
        'canales_color': channels,
        'tipo_color': 'RGB' if channels == 3 else 'Escala de grises' if channels == 1 else f'{channels} canales'
    }
    
    cap.release()
    return info


def mostrar_info_completa(info):
    """
    Muestra la información completa del video
    """
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETO DEL VIDEO")
    print("="*60)
    
    print(f"📁 Archivo: {info['nombre_archivo']}")
    print(f"📂 Ruta completa: {info['ruta']}")
    print()
    
    print("📐 DIMENSIONES Y RESOLUCIÓN:")
    print(f"   • Resolución: {info['resolucion']} píxeles")
    print(f"   • Ancho: {info['ancho']} px")
    print(f"   • Alto: {info['alto']} px")
    print(f"   • Relación de aspecto: {info['aspecto_ratio']}:1")
    print()
    
    print("⏱️ DURACIÓN Y FRAMES:")
    print(f"   • Duración total: {info['duracion_segundos']:.2f} segundos")
    print(f"   • En minutos: {info['duracion_minutos']:.2f} min")
    if info['duracion_horas'] >= 1:
        print(f"   • En horas: {info['duracion_horas']:.2f} hrs")
    print(f"   • Total de frames: {info['total_frames']:,}")
    print(f"   • FPS: {info['fps']:.2f} frames por segundo")
    print()
    
    print("💾 TAMAÑO DEL ARCHIVO:")
    print(f"   • Bytes: {info['tamaño_bytes']:,}")
    print(f"   • KB: {info['tamaño_kb']:,}")
    print(f"   • MB: {info['tamaño_mb']}")
    if info['tamaño_gb'] > 0.1:
        print(f"   • GB: {info['tamaño_gb']}")
    print()
    
    print("🎥 INFORMACIÓN TÉCNICA:")
    print(f"   • Codec: {info['codec']}")
    print(f"   • Bitrate aproximado: {info['bitrate_kbps']:.2f} kbps")
    print(f"   • Canales de color: {info['canales_color']}")
    print(f"   • Tipo de color: {info['tipo_color']}")
    print()
    
    # Clasificación de calidad
    if info['alto'] >= 2160:
        calidad = "4K Ultra HD"
    elif info['alto'] >= 1440:
        calidad = "2K/QHD"
    elif info['alto'] >= 1080:
        calidad = "Full HD"
    elif info['alto'] >= 720:
        calidad = "HD"
    elif info['alto'] >= 480:
        calidad = "SD"
    else:
        calidad = "Baja resolución"
    
    print(f"📊 CLASIFICACIÓN DE CALIDAD: {calidad}")
    print("="*60)


def calcular_dimensiones_escaladas(ancho_original, alto_original, factor_escala=0.5, altura_minima=640):
    """
    Calcula las nuevas dimensiones basándose en un factor de escala
    Solo redimensiona si la altura original es mayor a altura_minima
    
    Args:
        ancho_original (int): Ancho original del video
        alto_original (int): Alto original del video
        factor_escala (float): Factor de escala (0.5 = mitad, 0.25 = cuarto, etc.)
        altura_minima (int): Altura mínima para aplicar redimensionamiento
    
    Returns:
        tuple: (nuevo_ancho, nuevo_alto, redimensionado)
    """
    if alto_original <= altura_minima:
        # No redimensionar videos pequeños
        return ancho_original, alto_original, False
    
    nuevo_ancho = int(ancho_original * factor_escala)
    nuevo_alto = int(alto_original * factor_escala)
    
    # Asegurar que las dimensiones sean pares (mejor para codecs de video)
    if nuevo_ancho % 2 != 0:
        nuevo_ancho += 1
    if nuevo_alto % 2 != 0:
        nuevo_alto += 1
    
    return nuevo_ancho, nuevo_alto, True


def analizar_multiples_videos(directorio):
    """
    Analiza todos los videos en un directorio
    """
    extensiones_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    
    archivos_video = []
    for archivo in os.listdir(directorio):
        if any(archivo.lower().endswith(ext) for ext in extensiones_video):
            archivos_video.append(os.path.join(directorio, archivo))
    
    if not archivos_video:
        print(f"No se encontraron videos en el directorio: {directorio}")
        return
    
    print(f"Se encontraron {len(archivos_video)} videos para analizar:")
    
    for i, video_path in enumerate(archivos_video, 1):
        print(f"\n🎬 ANALIZANDO VIDEO {i}/{len(archivos_video)}")
        info = obtener_info_completa_video(video_path)
        if info:
            mostrar_info_completa(info)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  Para un video específico: python analizar_video.py ruta_del_video.mp4")
        print("  Para un directorio: python analizar_video.py directorio/")
        print("  Para el directorio actual: python analizar_video.py .")
        sys.exit(1)
    
    ruta = sys.argv[1]
    
    if os.path.isfile(ruta):
        # Analizar un video específico
        info = obtener_info_completa_video(ruta)
        if info:
            mostrar_info_completa(info)
    elif os.path.isdir(ruta):
        # Analizar todos los videos en el directorio
        analizar_multiples_videos(ruta)
    else:
        print(f"Error: La ruta '{ruta}' no existe")
