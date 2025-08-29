#!/usr/bin/env python3
"""
Script para hacer predicciones con el modelo YOLOv8n entrenado para logos deportivos
Soporta:
- Predicciones en imágenes individuales
- Predicciones en carpetas de imágenes
- Predicciones en archivos de video
- Predicciones en tiempo real con webcam

Autor: Juan Carlos Macías / Copilot
Fecha: Agosto 2025
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import argparse

class LogoPredictor:
    def __init__(self, model_path="runs/detect/modelo_entreno_2025-08-28_10-40-53-602689/weights/best.onnx"):
        """
        Inicializar el predictor de logos
        
        Args:
            model_path: Ruta al modelo entrenado (.pt o .onnx)
        """
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"No se encontró el modelo en: {model_path}")
        
        print(f"🤖 Cargando modelo desde: {self.model_path}")
        self.model = YOLO(str(self.model_path))
        
        # Nombres de las clases
        self.class_names = {
            1: 'adidas', 
            7: 'nike',
            8: 'puma',
        }
        
        print(f"✅ Modelo cargado correctamente")
        print(f"📋 Clases disponibles: {list(self.class_names.values())}")
    
    def predict_image(self, image_path, conf_threshold=1, save_results=True):
        """
        Hacer predicción en una imagen específica
        
        Args:
            image_path: Ruta a la imagen
            conf_threshold: Umbral de confianza (0.0 - 1.0)
            save_results: Si guardar los resultados
        
        Returns:
            results: Resultados de la predicción
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")
        
        print(f"\n🔍 Analizando imagen: {image_path.name}")
        
        # Hacer predicción
        results = self.model.predict(
            source=str(image_path),
            conf=conf_threshold,
            save=save_results,
            project="runs/predict",
            name="logo_prediction",
            exist_ok=True
        )
        
        # Procesar resultados
        self.process_results(results[0], image_path)
        
        return results[0]
    
    def process_results(self, result, image_path):
        """
        Procesar y mostrar los resultados de la predicción
        
        Args:
            result: Resultado de YOLO
            image_path: Ruta de la imagen original
        """
        # Obtener detecciones
        boxes = result.boxes
        
        if boxes is None or len(boxes) == 0:
            print("❌ No se detectaron logos en la imagen")
            return
        
        print(f"✅ Se detectaron {len(boxes)} logo(s):")
        print("-" * 50)
        
        for i, box in enumerate(boxes):
            # Obtener información de la detección
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = self.class_names.get(class_id, f"Clase_{class_id}")
            
            # Coordenadas de la caja
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            print(f"📍 Logo {i+1}:")
            print(f"   🏷️ Marca: {class_name}")
            print(f"   🎯 Confianza: {confidence:.2%}")
            print(f"   📦 Coordenadas: ({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)})")
            print()
    
    def predict_multiple_images(self, folder_path, conf_threshold=0.5):
        """
        Hacer predicciones en múltiples imágenes de una carpeta
        
        Args:
            folder_path: Ruta a la carpeta con imágenes
            conf_threshold: Umbral de confianza
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"No se encontró la carpeta: {folder_path}")
        
        # Extensiones de imagen soportadas
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        # Encontrar todas las imágenes
        image_files = []
        for ext in image_extensions:
            image_files.extend(folder_path.glob(f"*{ext}"))
            image_files.extend(folder_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"❌ No se encontraron imágenes en: {folder_path}")
            return
        
        print(f"🔍 Procesando {len(image_files)} imágenes...")
        
        results_summary = {name: 0 for name in self.class_names.values()}
        
        for img_path in image_files:
            print(f"\n{'='*60}")
            result = self.predict_image(img_path, conf_threshold, save_results=True)
            
            # Contar detecciones por clase
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.class_names.get(class_id, f"Clase_{class_id}")
                    results_summary[class_name] += 1
        
        # Mostrar resumen
        print(f"\n{'='*60}")
        print("📊 RESUMEN DE DETECCIONES:")
        print("-" * 30)
        total_detections = sum(results_summary.values())
        
        for brand, count in results_summary.items():
            if count > 0:
                percentage = (count / total_detections) * 100
                print(f"🏷️  {brand}: {count} detecciones ({percentage:.1f}%)")
        
        print(f"\n🎯 Total de logos detectados: {total_detections}")
        print(f"📁 Resultados guardados en: runs/predict/logo_prediction/")
    
    def predict_video(self, video_path, conf_threshold=0.5, save_video=True):
        """
        Hacer predicciones en un archivo de video
        
        Args:
            video_path: Ruta al archivo de video
            conf_threshold: Umbral de confianza
            save_video: Si guardar el video con detecciones
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"No se encontró el video: {video_path}")
        
        print(f"🎥 Analizando video: {video_path.name}")
        print("Presiona 'q' para salir durante la reproducción")
        
        # Hacer predicción en video
        results = self.model.predict(
            source=str(video_path),
            conf=conf_threshold,
            show=True,
            save=save_video,
            project="runs/predict",
            name="video_prediction",
            exist_ok=True
        )
        
        if save_video:
            print(f"✅ Video procesado guardado en: runs/predict/video_prediction/")
    
    def predict_webcam(self, conf_threshold=0.5):
        """
        Hacer predicciones en tiempo real desde la webcam
        
        Args:
            conf_threshold: Umbral de confianza
        """
        print("🎥 Iniciando detección en tiempo real desde webcam...")
        print("Presiona 'q' para salir")
        
        # Hacer predicción en tiempo real
        results = self.model.predict(
            source=0,  # Webcam
            conf=conf_threshold,
            show=True,
            save=False
        )
    
    def show_model_info(self):
        """
        Mostrar información del modelo
        """
        print("\n🤖 INFORMACIÓN DEL MODELO:")
        print("-" * 40)
        print(f"📁 Archivo: {self.model_path}")
        print(f"📊 Clases: {len(self.class_names)}")
        print(f"🏷️  Marcas detectables:")
        for i, name in self.class_names.items():
            print(f"   {i}: {name}")
        print()


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Predictor de logos deportivos con YOLOv8")
    parser.add_argument("--image", "-i", type=str, help="Ruta a la imagen para analizar")
    parser.add_argument("--folder", "-f", type=str, help="Ruta a carpeta con imágenes")
    parser.add_argument("--video", "-v", type=str, help="Ruta al archivo de video para analizar")
    parser.add_argument("--webcam", "-w", action="store_true", help="Usar webcam en tiempo real")
    parser.add_argument("--model", "-m", type=str, default="runs/detect/modelo_entreno_2025-08-28_10-40-53-602689/weights/best.onnx", 
                       help="Ruta al modelo entrenado")
    parser.add_argument("--conf", "-c", type=float, default=0.5, 
                       help="Umbral de confianza (0.0-1.0)")
    parser.add_argument("--info", action="store_true", help="Mostrar información del modelo")
    parser.add_argument("--no-save", action="store_true", help="No guardar el video procesado")
    
    args = parser.parse_args()
    
    try:
        # Crear predictor
        predictor = LogoPredictor(args.model)
        
        if args.info:
            predictor.show_model_info()
            return
        
        if args.image:
            # Predicción en imagen única
            predictor.predict_image(args.image, args.conf)
            print(f"\n✅ Resultado guardado en: runs/predict/logo_prediction/")
            
        elif args.folder:
            # Predicción en múltiples imágenes
            predictor.predict_multiple_images(args.folder, args.conf)
            
        elif args.video:
            # Predicción en video
            save_video = not args.no_save
            predictor.predict_video(args.video, args.conf, save_video)
            
        elif args.webcam:
            # Predicción en tiempo real
            predictor.predict_webcam(args.conf)
            
        else:
            # Modo interactivo
            print("\n🎯 PREDICTOR DE LOGOS DEPORTIVOS")
            print("=" * 40)
            predictor.show_model_info()
            
            while True:
                print("\n📋 OPCIONES:")
                print("1. Analizar una imagen")
                print("2. Analizar carpeta de imágenes")
                print("3. Analizar un video")
                print("4. Webcam en tiempo real")
                print("5. Información del modelo")
                print("0. Salir")
                
                choice = input("\n🔸 Selecciona una opción (0-5): ").strip()
                
                if choice == "0":
                    print("👋 ¡Hasta luego!")
                    break
                    
                elif choice == "1":
                    img_path = input("📁 Ruta de la imagen: ").strip()
                    if img_path:
                        try:
                            predictor.predict_image(img_path, args.conf)
                            print(f"\n✅ Resultado guardado en: runs/predict/logo_prediction/")
                        except Exception as e:
                            print(f"❌ Error: {e}")
                
                elif choice == "2":
                    folder_path = input("📁 Ruta de la carpeta: ").strip()
                    if folder_path:
                        try:
                            predictor.predict_multiple_images(folder_path, args.conf)
                        except Exception as e:
                            print(f"❌ Error: {e}")
                
                elif choice == "3":
                    video_path = input("📁 Ruta del video: ").strip()
                    if video_path:
                        try:
                            save_video = input("💾 ¿Guardar video procesado? (s/N): ").strip().lower() == 's'
                            predictor.predict_video(video_path, args.conf, save_video)
                        except Exception as e:
                            print(f"❌ Error: {e}")
                
                elif choice == "4":
                    try:
                        predictor.predict_webcam(args.conf)
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif choice == "5":
                    predictor.show_model_info()
                
                else:
                    print("❌ Opción no válida")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
