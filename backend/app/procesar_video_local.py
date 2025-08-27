#!/usr/bin/env python3
"""
Script para procesar un video local (ya descargado) y funciones de streaming
"""
import cv2
import os
import time
from .analizar_video import obtener_info_completa_video, mostrar_info_completa, calcular_dimensiones_escaladas

def generate_video_stream(video_path, factor_escala=0.5, altura_minima=640, fps_limite=30.0, delay_frames=0.033):
    """
    Generador de frames para streaming con control de velocidad
    
    Args:
        video_path: Ruta del video
        factor_escala: Factor de escala para redimensionar
        altura_minima: Altura mínima para redimensionar
        fps_limite: FPS máximo para el streaming
        delay_frames: Delay en segundos entre frames
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error al abrir el video: {video_path}")
        return
    
    # Obtener información del video
    info_video = obtener_info_completa_video(video_path)
    
    # Calcular dimensiones
    if info_video:
        nuevo_ancho, nuevo_alto, sera_redimensionado = calcular_dimensiones_escaladas(
            info_video['ancho'], 
            info_video['alto'], 
            factor_escala,
            altura_minima
        )
        print(f"📐 Dimensiones: {info_video['ancho']}x{info_video['alto']} -> {nuevo_ancho}x{nuevo_alto}")
        fps_original = info_video.get('fps', 30.0)
        print(f"🎞️ FPS original: {fps_original:.2f}, FPS límite streaming: {fps_limite:.2f}")
    else:
        nuevo_ancho, nuevo_alto = 640, 480
        sera_redimensionado = True
        fps_original = 30.0
        print("⚠️ Usando dimensiones por defecto")
    
    frame_count = 0
    start_time = time.time()
    
    # Calcular delay basado en FPS deseado
    target_delay = 1.0 / fps_limite if fps_limite > 0 else delay_frames
    
    try:
        while cap.isOpened():
            frame_start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                print("📺 Fin del video alcanzado")
                break
            
            frame_count += 1
            
            # Redimensionar si es necesario
            if sera_redimensionado:
                frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
            
            # Calcular estadísticas de tiempo
            elapsed_time = time.time() - start_time
            current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            # Añadir información al frame
            cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f'Size: {nuevo_ancho}x{nuevo_alto}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(frame, f'FPS: {current_fps:.1f}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
            cv2.putText(frame, f'Target FPS: {fps_limite:.1f}', (10, 120), 
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
                print(f"📸 Frame {frame_count} | FPS actual: {current_fps:.2f} | Target: {fps_limite:.2f}")
    
    except Exception as e:
        print(f"❌ Error en generate_video_stream: {e}")
    finally:
        cap.release()
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time if total_time > 0 else 0
        print(f"✅ Análisis completado. Frames: {frame_count}, Tiempo: {total_time:.2f}s, FPS promedio: {avg_fps:.2f}")

def procesar_video_local(video_path, factor_escala=0.5, altura_minima=640, idx=0):
    """
    Procesa un video local que ya existe en el sistema
    
    Args:
        video_path (str): Ruta del video local
        factor_escala (float): Factor de escala para redimensionar
        altura_minima (int): Altura mínima para aplicar redimensionamiento
        idx (int): Índice del video (para mostrar en ventana)
    
    Returns:
        bool: True si el procesamiento fue exitoso, False en caso contrario
    """
    if not os.path.exists(video_path):
        print(f'❌ El archivo {video_path} no existe')
        return False
    
    print(f'📁 Procesando video local: {video_path}')
    
    # Obtener y mostrar información del video
    info_video = obtener_info_completa_video(video_path)
    if info_video:
        mostrar_info_completa(info_video)
    
    print(f'🎬 Reproduciendo {video_path} con OpenCV...')
    cap = cv2.VideoCapture(video_path)
    
    # Determinar si necesita redimensionamiento basándose en la resolución del video
    if info_video:
        nuevo_ancho, nuevo_alto, sera_redimensionado = calcular_dimensiones_escaladas(
            info_video['ancho'], 
            info_video['alto'], 
            factor_escala,
            altura_minima
        )
        
        if sera_redimensionado:
            print(f'📐 Redimensionando de {info_video["resolucion"]} a {nuevo_ancho}x{nuevo_alto}')
            print(f'🔄 Factor de escala: {int(factor_escala * 100)}% del tamaño original')
            titulo_ventana = f'Video Local {idx} - Escalado {int(factor_escala * 100)}%'
        else:
            print(f'📐 Video de baja resolución ({info_video["resolucion"]})')
            print(f'✨ Manteniendo tamaño original sin redimensionar')
            titulo_ventana = f'Video Local {idx} - Tamaño original'
    else:
        # Valores por defecto si no se pudo obtener la info
        nuevo_ancho, nuevo_alto = 640, 480
        sera_redimensionado = True
        titulo_ventana = f'Video Local {idx} - Dimensiones por defecto'
        print('⚠️  Usando dimensiones por defecto: 640x480')
    
    frame_count = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Solo redimensionar si es necesario
            if sera_redimensionado:
                frame_procesado = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
            else:
                frame_procesado = frame
            
            # Mostrar información en la ventana
            cv2.putText(frame_procesado, f'Frame: {frame_count}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame_procesado, f'Resolucion: {nuevo_ancho}x{nuevo_alto}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame_procesado, f'Archivo: {os.path.basename(video_path)}', (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            cv2.imshow(titulo_ventana, frame_procesado)
            
            # Presiona 'q' para salir, 'p' para pausar, 'r' para reiniciar
            key = cv2.waitKey(25) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                print("⏸️  Video pausado. Presiona cualquier tecla para continuar...")
                cv2.waitKey(0)  # Pausar hasta que se presione cualquier tecla
            elif key == ord('r'):
                print("🔄 Reiniciando video...")
                cap.set(cv2.CAP_PROP_POS_FRAME, 0)  # Volver al inicio
                frame_count = 0
        
        cap.release()
        cv2.destroyAllWindows()
        print(f'✅ Procesamiento completado. Total de frames mostrados: {frame_count}')
        return True
        
    except Exception as e:
        print(f'❌ Error durante el procesamiento: {e}')
        cap.release()
        cv2.destroyAllWindows()
        return False

def main():
    """Función principal"""
    
    # Buscar videos en la carpeta de descargas
    videos_dir = "videos_descargados"
    
    if not os.path.exists(videos_dir):
        print(f"❌ La carpeta {videos_dir} no existe")
        return
    
    # Encontrar videos disponibles
    extensiones_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    videos_disponibles = []
    
    for archivo in os.listdir(videos_dir):
        if any(archivo.lower().endswith(ext) for ext in extensiones_video):
            videos_disponibles.append(os.path.join(videos_dir, archivo))
    
    if not videos_disponibles:
        print(f"❌ No se encontraron videos en la carpeta {videos_dir}")
        print("💡 Primero ejecuta 'python main.py' para descargar algunos videos")
        return
    
    print(f"📁 Videos disponibles en {videos_dir}:")
    for i, video in enumerate(videos_disponibles):
        print(f"  {i + 1}. {os.path.basename(video)}")
    
    # Procesar el primer video disponible
    video_seleccionado = videos_disponibles[0]
    print(f"\n🎬 Procesando: {os.path.basename(video_seleccionado)}")
    print("🎮 Controles: 'q' = salir, 'p' = pausar, 'r' = reiniciar")
    print("-" * 60)
    
    procesar_video_local(
        video_path=video_seleccionado,
        factor_escala=0.6,      # Escalar al 60%
        altura_minima=720,      # Solo redimensionar si altura > 720px
        idx=1
    )

if __name__ == "__main__":
    main()
