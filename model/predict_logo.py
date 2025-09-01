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
import yaml

class LogoPredictor:
    def __init__(self, model_path="runs/detect/modelo_entreno_2025-08-30_19-19-42-687094/weights/best.pt"):
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

        # Obtener nombres de clases dinámicamente del modelo
        self.class_names = self.get_model_classes()
        
        print(f"✅ Modelo cargado correctamente")
        print(f"📋 Clases detectadas en el modelo: {len(self.class_names)}")
        print(f"🏷️  Marcas disponibles: {list(self.class_names.values())}")

    def get_model_classes(self):
        """
        Obtener las clases del modelo de forma dinámica
        
        Returns:
            dict: Diccionario con {id: nombre_clase}
        """
        try:
            # Método 1: Desde model.names (más directo)
            if hasattr(self.model, 'names') and self.model.names:
                print("📋 Clases obtenidas desde model.names")
                return self.model.names
            
            # Método 2: Desde model.model.names
            elif hasattr(self.model.model, 'names') and self.model.model.names:
                print("📋 Clases obtenidas desde model.model.names")
                return self.model.model.names
            
            # Método 3: Hacer una predicción dummy para cargar las clases
            elif hasattr(self.model, 'predict'):
                print("📋 Cargando clases mediante predicción dummy...")
                # Crear imagen dummy de 1x1 pixel
                dummy_img = np.zeros((1, 1, 3), dtype=np.uint8)
                temp_results = self.model.predict(dummy_img, verbose=False)
                if temp_results and hasattr(temp_results[0], 'names'):
                    return temp_results[0].names
            
            # Método 4: Desde el archivo de configuración del dataset
            config_path = Path("dataset/config.yaml")
            if config_path.exists():
                print("📋 Cargando clases desde dataset/config.yaml")
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if 'names' in config:
                        # Convertir lista a diccionario con índices
                        if isinstance(config['names'], list):
                            return {i: name for i, name in enumerate(config['names'])}
                        elif isinstance(config['names'], dict):
                            return config['names']
            
            # Fallback: Clases por defecto basadas en el proyecto
            print("⚠️  Usando clases por defecto del proyecto")
            return {
                0: 'adidas',
                1: 'adidas_1',
                2: 'adidas_2',
                3: 'nike', 
                4: 'puma'
            }
            
        except Exception as e:
            print(f"⚠️  Error obteniendo clases del modelo: {e}")
            print("📋 Usando clases por defecto")
            return {
                0: 'adidas',
                1: 'adidas_1',
                2: 'adidas_2',
                3: 'nike', 
                4: 'puma'
            }

    def predict_image(self, image_path, conf_threshold=0.5, save_results=True):
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
            conf=0.35,          # más recall
            iou=0.6,            # mejor filtrado
            max_det=300,
            save=save_results,
            project="runs/predict",
            name="logo_prediction",
            exist_ok=True,
            verbose=False
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
            class_name = self.get_class_name(class_id)
            
            # Coordenadas de la caja
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            print(f"📍 Logo {i+1}:")
            print(f"   🏷️  Marca: {class_name}")
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
            conf=0.25,          # más recall
            iou=0.6,            # mejor filtrado
            max_det=300,
            show=True,
            save=save_video,
            project="runs/predict",
            name="logo_prediction",
            exist_ok=True,
            verbose=False
        )
        #print(f" Resultados: {results}")
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

    def list_classes(self):
        """
        Listar todas las clases disponibles en el modelo
        
        Returns:
            dict: Diccionario con las clases {id: nombre}
        """
        print("\n📋 CLASES DISPONIBLES EN EL MODELO:")
        print("=" * 45)
        
        for class_id, class_name in self.class_names.items():
            print(f"🏷️  ID: {class_id:2d} → Nombre: '{class_name}'")
        
        print(f"\n📊 Total de clases: {len(self.class_names)}")
        print("=" * 45)
        
        return self.class_names

    def get_class_name(self, class_id):
        """
        Obtener el nombre de una clase por su ID
        
        Args:
            class_id: ID de la clase
            
        Returns:
            str: Nombre de la clase
        """
        return self.class_names.get(class_id, f"Clase_desconocida_{class_id}")

    def get_class_id(self, class_name):
        """
        Obtener el ID de una clase por su nombre
        
        Args:
            class_name: Nombre de la clase
            
        Returns:
            int: ID de la clase (None si no se encuentra)
        """
        for class_id, name in self.class_names.items():
            if name.lower() == class_name.lower():
                return class_id
        return None


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Predictor de logos deportivos con YOLOv8")
    parser.add_argument("--image", "-i", type=str, help="Ruta a la imagen para analizar")
    parser.add_argument("--folder", "-f", type=str, help="Ruta a carpeta con imágenes")
    parser.add_argument("--video", "-v", type=str, help="Ruta al archivo de video para analizar")
    parser.add_argument("--webcam", "-w", action="store_true", help="Usar webcam en tiempo real")
    parser.add_argument("--model", "-m", type=str, default="runs/detect/modelo_entrenado_v4/weights/best.pt", 
                       help="Ruta al modelo entrenado")
    parser.add_argument("--conf", "-c", type=float, default=0.5, 
                       help="Umbral de confianza (0.0-1.0)")
    parser.add_argument("--info", action="store_true", help="Mostrar información del modelo")
    parser.add_argument("--classes", action="store_true", help="Listar todas las clases disponibles")
    parser.add_argument("--no-save", action="store_true", help="No guardar el video procesado")
    
    args = parser.parse_args()
    
    try:
        # Crear predictor
        predictor = LogoPredictor(args.model)
        
        if args.info:
            predictor.show_model_info()
            return
        
        if args.classes:
            predictor.list_classes()
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
                print("6. Listar clases disponibles")
                print("0. Salir")
                
                choice = input("\n🔸 Selecciona una opción (0-6): ").strip()
                
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
                
                elif choice == "6":
                    predictor.list_classes()
                
                else:
                    print("❌ Opción no válida")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
