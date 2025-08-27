import cv2
import os
import sys


def get_complete_video_info(video_path):
    """
    Extrae información detallada del video usando OpenCV
    """
    if not os.path.exists(video_path):
        print(f"Error: El archivo {video_path} no existe")
        return None
    
    capture = cv2.VideoCapture(video_path)
    
    if not capture.isOpened():
        print(f"Error: No se pudo abrir el video {video_path}")
        return None
    
    # Obtener todas las propiedades disponibles
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    # Codec información
    fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
    codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    
    # Tamaño del archivo
    file_size_bytes = os.path.getsize(video_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    file_size_kb = file_size_bytes / 1024
    
    # Bitrate aproximado
    bitrate_kbps = (file_size_kb * 8) / duration if duration > 0 else 0
    
    # Leer el primer frame para análisis adicional
    ret, first_frame = capture.read()
    channels = first_frame.shape[2] if ret and len(first_frame.shape) == 3 else 1
    
    video_info = {
        'path': video_path,
        'filename': os.path.basename(video_path),
        'width': width,
        'height': height,
        'fps': fps,
        'total_frames': frame_count,
        'duration_seconds': duration,
        'duration_minutes': duration / 60,
        'duration_hours': duration / 3600,
        'codec': codec.strip(),
        'size_bytes': file_size_bytes,
        'size_kb': round(file_size_kb, 2),
        'size_mb': round(file_size_mb, 2),
        'size_gb': round(file_size_mb / 1024, 3),
        'resolution': f"{width}x{height}",
        'aspect_ratio': round(width/height, 2) if height > 0 else 0,
        'bitrate_kbps': round(bitrate_kbps, 2),
        'color_channels': channels,
        'color_type': 'RGB' if channels == 3 else 'Grayscale' if channels == 1 else f'{channels} channels'
    }
    
    capture.release()
    return video_info


def show_complete_info(video_info):
    """
    Muestra la información completa del video
    """
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETO DEL VIDEO")
    print("="*60)
    
    print(f"📁 Archivo: {video_info['filename']}")
    print(f"📂 Ruta completa: {video_info['path']}")
    print()
    
    print("📐 DIMENSIONES Y RESOLUCIÓN:")
    print(f"   • Resolución: {video_info['resolution']} píxeles")
    print(f"   • Ancho: {video_info['width']} px")
    print(f"   • Alto: {video_info['height']} px")
    print(f"   • Relación de aspecto: {video_info['aspect_ratio']}:1")
    print()
    
    print("⏱️ DURACIÓN Y FRAMES:")
    print(f"   • Duración total: {video_info['duration_seconds']:.2f} segundos")
    print(f"   • En minutos: {video_info['duration_minutes']:.2f} min")
    if video_info['duration_hours'] >= 1:
        print(f"   • En horas: {video_info['duration_hours']:.2f} hrs")
    print(f"   • Total de frames: {video_info['total_frames']:,}")
    print(f"   • FPS: {video_info['fps']:.2f} frames por segundo")
    print()
    
    print("💾 TAMAÑO DEL ARCHIVO:")
    print(f"   • Bytes: {video_info['size_bytes']:,}")
    print(f"   • KB: {video_info['size_kb']:,}")
    print(f"   • MB: {video_info['size_mb']}")
    if video_info['size_gb'] > 0.1:
        print(f"   • GB: {video_info['size_gb']}")
    print()
    
    print("🎥 INFORMACIÓN TÉCNICA:")
    print(f"   • Codec: {video_info['codec']}")
    print(f"   • Bitrate aproximado: {video_info['bitrate_kbps']:.2f} kbps")
    print(f"   • Canales de color: {video_info['color_channels']}")
    print(f"   • Tipo de color: {video_info['color_type']}")
    print()
    
    # Clasificación de calidad
    if video_info['height'] >= 2160:
        quality = "4K Ultra HD"
    elif video_info['height'] >= 1440:
        quality = "2K/QHD"
    elif video_info['height'] >= 1080:
        quality = "Full HD"
    elif video_info['height'] >= 720:
        quality = "HD"
    elif video_info['height'] >= 480:
        quality = "SD"
    else:
        quality = "Baja resolución"
    
    print(f"📊 CLASIFICACIÓN DE CALIDAD: {quality}")
    print("="*60)


def calculate_scaled_dimensions(original_width, original_height, scale_factor=0.5, min_height=640):
    """
    Calcula las nuevas dimensiones basándose en un factor de escala
    Solo redimensiona si la altura original es mayor a min_height
    
    Args:
        original_width (int): Ancho original del video
        original_height (int): Alto original del video
        scale_factor (float): Factor de escala (0.5 = mitad, 0.25 = cuarto, etc.)
        min_height (int): Altura mínima para aplicar redimensionamiento
    
    Returns:
        tuple: (new_width, new_height, resized)
    """
    if original_height <= min_height:
        # No redimensionar videos pequeños
        return original_width, original_height, False
    
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    # Asegurar que las dimensiones sean pares (mejor para codecs de video)
    if new_width % 2 != 0:
        new_width += 1
    if new_height % 2 != 0:
        new_height += 1
    
    return new_width, new_height, True


def analyze_multiple_videos(directory):
    """
    Analiza todos los videos en un directorio
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    
    video_files = []
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(os.path.join(directory, file))
    
    if not video_files:
        print(f"No se encontraron videos en el directorio: {directory}")
        return
    
    print(f"Se encontraron {len(video_files)} videos para analizar:")
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\n🎬 ANALIZANDO VIDEO {i}/{len(video_files)}")
        video_info = get_complete_video_info(video_path)
        if video_info:
            show_complete_info(video_info)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  For specific video: python analyze_video.py video_path.mp4")
        print("  For directory: python analyze_video.py directory/")
        print("  For current directory: python analyze_video.py .")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        # Analizar un video específico
        video_info = get_complete_video_info(path)
        if video_info:
            show_complete_info(video_info)
    elif os.path.isdir(path):
        # Analizar todos los videos en el directorio
        analyze_multiple_videos(path)
    else:
        print(f"Error: La ruta '{path}' no existe")
