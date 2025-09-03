#!/usr/bin/env python3
"""
Script para procesar un video local (ya descargado) y funciones de streaming
"""
import cv2
import os
import time
from .analyze_video import get_complete_video_info, show_complete_info, calculate_scaled_dimensions

def generate_video_stream(video_path, scale_factor=0.5, min_height=640, fps_limit=30.0, delay_frames=0.033, delete_after_processing=False):
    """
    Generador de frames para streaming con control de velocidad
    
    Args:
        video_path: Ruta del video
        scale_factor: Factor de escala para redimensionar
        min_height: Altura mínima para redimensionar
        fps_limit: FPS máximo para el streaming
        delay_frames: Delay en segundos entre frames
        delete_after_processing: Si True, elimina el video después del procesamiento
    """
    capture = cv2.VideoCapture(video_path)
    
    if not capture.isOpened():
        print(f"❌ Error al abrir el video: {video_path}")
        return
    
    # Obtener información del video
    video_info = get_complete_video_info(video_path)
    
    # Calcular dimensiones
    if video_info:
        new_width, new_height, will_be_resized = calculate_scaled_dimensions(
            video_info['width'], 
            video_info['height'], 
            scale_factor,
            min_height
        )
        print(f"📐 Dimensiones: {video_info['width']}x{video_info['height']} -> {new_width}x{new_height}")
        original_fps = video_info.get('fps', 30.0)
        print(f"🎞️ FPS original: {original_fps:.2f}, FPS límite streaming: {fps_limit:.2f}")
    else:
        new_width, new_height = 640, 480
        will_be_resized = True
        original_fps = 30.0
        print("⚠️ Usando dimensiones por defecto")
    
    frame_count = 0
    start_time = time.time()
    
    # Calcular delay basado en FPS deseado
    target_delay = 1.0 / fps_limit if fps_limit > 0 else delay_frames
    
    try:
        while capture.isOpened():
            frame_start_time = time.time()
            
            ret, frame = capture.read()
            if not ret:
                print("📺 Fin del video alcanzado")
                
                break
            
            frame_count += 1
            
            # Redimensionar si es necesario
            if will_be_resized:
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Calcular estadísticas de tiempo
            elapsed_time = time.time() - start_time
            current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            # Añadir información al frame
            cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Size: {new_width}x{new_height}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(frame, f'FPS: {current_fps:.1f}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(frame, f'Target FPS: {fps_limit:.1f}', (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Codificar frame a JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
                )
            
            # Control de velocidad
            frame_process_time = time.time() - frame_start_time
            sleep_time = max(0, target_delay - frame_process_time)
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            # Log cada 100 frames
            if frame_count % 100 == 0:
                print(f"📸 Frame {frame_count} | FPS actual: {current_fps:.2f} | Target: {fps_limit:.2f}")
    
    except Exception as e:
        print(f"❌ Error en generate_video_stream: {e}")
    finally:
        capture.release()
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time if total_time > 0 else 0
        print(f"✅ Análisis completado. Frames: {frame_count}, Tiempo: {total_time:.2f}s, FPS promedio: {avg_fps:.2f}")
        
        # Eliminar video si se especificó
        if delete_after_processing and os.path.exists(video_path):
            try:
                file_size = os.path.getsize(video_path)
                file_size_mb = file_size / (1024 * 1024)
                os.remove(video_path)
                print(f"🗑️ Video eliminado automáticamente: {os.path.basename(video_path)} ({file_size_mb:.2f} MB liberados)")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar el video {video_path}: {e}")

def process_local_video(video_path, scale_factor=0.5, min_height=640, idx=0, delete_after_processing=False):
    """
    Procesa un video local que ya existe en el sistema
    
    Args:
        video_path (str): Ruta del video local
        scale_factor (float): Factor de escala para redimensionar
        min_height (int): Altura mínima para aplicar redimensionamiento
        idx (int): Índice del video (para mostrar en ventana)
        delete_after_processing (bool): Si True, elimina el video después del procesamiento
    
    Returns:
        bool: True si el procesamiento fue exitoso, False en caso contrario
    """
    if not os.path.exists(video_path):
        print(f'❌ El archivo {video_path} no existe')
        return False
    
    print(f'📁 Procesando video local: {video_path}')
    
    # Obtener y mostrar información del video
    video_info = get_complete_video_info(video_path)
    if video_info:
        show_complete_info(video_info)
    
    print(f'🎬 Reproduciendo {video_path} con OpenCV...')
    capture = cv2.VideoCapture(video_path)
    
    # Determinar si necesita redimensionamiento basándose en la resolución del video
    if video_info:
        new_width, new_height, will_be_resized = calculate_scaled_dimensions(
            video_info['width'], 
            video_info['height'], 
            scale_factor,
            min_height
        )
        
        if will_be_resized:
            print(f'📐 Redimensionando de {video_info["resolution"]} a {new_width}x{new_height}')
            print(f'🔄 Factor de escala: {int(scale_factor * 100)}% del tamaño original')
            window_title = f'Video Local {idx} - Escalado {int(scale_factor * 100)}%'
        else:
            print(f'📐 Video de baja resolución ({video_info["resolution"]})')
            print(f'✨ Manteniendo tamaño original sin redimensionar')
            window_title = f'Video Local {idx} - Tamaño original'
    else:
        # Valores por defecto si no se pudo obtener la info
        new_width, new_height = 640, 480
        will_be_resized = True
        window_title = f'Video Local {idx} - Dimensiones por defecto'
        print('⚠️  Usando dimensiones por defecto: 640x480')
    
    frame_count = 0
    try:
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Solo redimensionar si es necesario
            if will_be_resized:
                processed_frame = cv2.resize(frame, (new_width, new_height))
            else:
                processed_frame = frame
            
            # Mostrar información en la ventana
            cv2.putText(processed_frame, f'Frame: {frame_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(processed_frame, f'Resolucion: {new_width}x{new_height}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(processed_frame, f'Archivo: {os.path.basename(video_path)}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            cv2.imshow(window_title, processed_frame)
            
            # Presiona 'q' para salir, 'p' para pausar, 'r' para reiniciar
            key = cv2.waitKey(25) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                print("⏸️  Video pausado. Presiona cualquier tecla para continuar...")
                cv2.waitKey(0)  # Pausar hasta que se presione cualquier tecla
            elif key == ord('r'):
                print("🔄 Reiniciando video...")
                capture.set(cv2.CAP_PROP_POS_FRAME, 0)  # Volver al inicio
                frame_count = 0
        
        capture.release()
        cv2.destroyAllWindows()
        print(f'✅ Procesamiento completado. Total de frames mostrados: {frame_count}')
        
        # Eliminar video si se especificó
        if delete_after_processing and os.path.exists(video_path):
            try:
                file_size = os.path.getsize(video_path)
                file_size_mb = file_size / (1024 * 1024)
                os.remove(video_path)
                print(f"🗑️ Video eliminado automáticamente: {os.path.basename(video_path)} ({file_size_mb:.2f} MB liberados)")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar el video {video_path}: {e}")
        
        return True
        
    except Exception as e:
        print(f'❌ Error durante el procesamiento: {e}')
        capture.release()
        cv2.destroyAllWindows()
        
        # También intentar eliminar en caso de error si se especificó
        if delete_after_processing and os.path.exists(video_path):
            try:
                file_size = os.path.getsize(video_path)
                file_size_mb = file_size / (1024 * 1024)
                os.remove(video_path)
                print(f"🗑️ Video eliminado automáticamente tras error: {os.path.basename(video_path)} ({file_size_mb:.2f} MB liberados)")
            except Exception as delete_error:
                print(f"⚠️ No se pudo eliminar el video {video_path}: {delete_error}")
        
        return False

def main():
    """Función principal"""
    
    # Buscar videos en la carpeta de descargas
    videos_directory = "videos_descargados"
    
    if not os.path.exists(videos_directory):
        print(f"❌ La carpeta {videos_directory} no existe")
        return
    
    # Encontrar videos disponibles
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    available_videos = []
    
    for file in os.listdir(videos_directory):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            available_videos.append(os.path.join(videos_directory, file))
    
    if not available_videos:
        print(f"❌ No se encontraron videos en la carpeta {videos_directory}")
        print("💡 Primero ejecuta 'python main.py' para descargar algunos videos")
        return
    
    print(f"📁 Videos disponibles en {videos_directory}:")
    for i, video in enumerate(available_videos):
        print(f"  {i + 1}. {os.path.basename(video)}")
    
    # Procesar el primer video disponible
    selected_video = available_videos[0]
    print(f"\n🎬 Procesando: {os.path.basename(selected_video)}")
    print("🎮 Controles: 'q' = salir, 'p' = pausar, 'r' = reiniciar")
    print("-" * 60)
    
    process_local_video(
        video_path=selected_video,
        scale_factor=0.6,      # Escalar al 60%
        min_height=720,      # Solo redimensionar si altura > 720px
        idx=1
    )

if __name__ == "__main__":
    main()
