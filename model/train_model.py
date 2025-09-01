#!/usr/bin/env python3
"""
Script para entrenar YOLO11s con logos de marcas deportivas
Autor: Copilot
Fecha: Agosto 2025
"""

import os
import sys
import shutil
import random
from pathlib import Path
import yaml
from ultralytics import YOLO
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime
import re

class YOLOTrainer:
    def __init__(self, data_path="by_class", dataset_path="dataset", version_type="timestamp", model_path="yolo11n.pt"):
        """
        Inicializar el entrenador YOLO
        
        Args:
            data_path: Ruta a los datos organizados por clase
            dataset_path: Ruta donde se creará el dataset YOLO
            version_type: Tipo de versionado ('timestamp' o 'incremental')
            model_path: Ruta al modelo base (ej: 'yolo11n.pt', 'yolov8n-logo.pt', etc.)
        """
        self.data_path = Path(data_path)
        self.dataset_path = Path(dataset_path)
        self.classes = []
        self.class_mapping = {}
        self.version_type = version_type
        self.run_name = self.generate_run_name()
        self.model = model_path  # Ahora configurable
        
        # Crear directorios del dataset
        self.setup_directories()
        
        print(f"🤖 Modelo seleccionado: {self.model}")
        if "logo" in self.model.lower():
            print("✨ Detectado modelo especializado en logos - Usando configuración optimizada")
        
    def setup_directories(self):
        """Crear estructura de directorios para YOLO"""
        dirs = [
            self.dataset_path / "images" / "train",
            self.dataset_path / "images" / "val",
            self.dataset_path / "images" / "test",
            self.dataset_path / "labels" / "train",
            self.dataset_path / "labels" / "val",
            self.dataset_path / "labels" / "test"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio creado: {dir_path}")
    
    def generate_run_name(self, base_name="modelo_entreno"):
        """
        Generar nombre único para el run basado en el tipo de versionado
        
        Args:
            base_name: Nombre base para el run
            
        Returns:
            str: Nombre único del run
        """
        if self.version_type == "timestamp":
            # Formato: modelo_entreno_2025-08-27_14-30-15-123456
            import time
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            microseconds = str(int(time.time() * 1000000) % 1000000).zfill(6)
            return f"{base_name}_{timestamp}-{microseconds}"
        
        elif self.version_type == "incremental":
            # Formato: modelo_entreno_v1, modelo_entreno_v2, etc.
            runs_dir = Path("runs/detect")
            if not runs_dir.exists():
                return f"{base_name}_v1"
            
            # Buscar versiones existentes
            existing_versions = []
            pattern = re.compile(rf"{base_name}_v(\d+)")
            
            for run_dir in runs_dir.iterdir():
                if run_dir.is_dir():
                    match = pattern.match(run_dir.name)
                    if match:
                        existing_versions.append(int(match.group(1)))
            
            # Determinar siguiente versión
            if existing_versions:
                next_version = max(existing_versions) + 1
            else:
                next_version = 1
                
            return f"{base_name}_v{next_version}"
        
        else:
            # Fallback al nombre base
            return base_name
    
    def get_model_paths(self):
        """
        Obtener rutas del modelo basadas en el nombre del run
        
        Returns:
            dict: Diccionario con las rutas del modelo
        """
        base_path = Path("runs/detect") / self.run_name
        return {
            'best': base_path / "weights" / "best.pt",
            'last': base_path / "weights" / "last.pt",
            'results_dir': base_path,
            'weights_dir': base_path / "weights"
        }
    
    def load_class_mapping(self):
        """Cargar el mapeo de clases desde label_map.txt"""
        label_map_path = self.data_path / "label_map.txt"
        
        if not label_map_path.exists():
            print(f"❌ No se encontró {label_map_path}")
            return False
            
        with open(label_map_path, 'r', encoding='utf-8') as f:
            self.classes = [line.strip() for line in f if line.strip()]
        
        # Crear mapeo de clase a índice
        self.class_mapping = {cls: idx for idx, cls in enumerate(self.classes)}
        
        print(f"✅ Clases cargadas: {len(self.classes)}")
        for idx, cls in enumerate(self.classes):
            print(f"   {idx}: {cls}")
        
        return True
    
    def clean_labels(self):
        """Limpiar y corregir etiquetas con índices de clase incorrectos"""
        print("\n🧹 Limpiando etiquetas incorrectas...")
        
        corrected_count = 0
        total_files = 0
        
        for class_name in self.classes:
            labels_dir = self.data_path / class_name / "labels"
            if not labels_dir.exists():
                continue
                
            class_index = self.class_mapping[class_name]
            label_files = list(labels_dir.glob("*.txt"))
            
            for label_file in label_files:
                total_files += 1
                try:
                    # Leer contenido del archivo
                    with open(label_file, 'r') as f:
                        lines = f.readlines()
                    
                    corrected_lines = []
                    file_corrected = False
                    
                    for line in lines:
                        if line.strip():
                            parts = line.strip().split()
                            if len(parts) >= 5:
                                old_class = int(parts[0])
                                if old_class != class_index:
                                    # Corregir el índice de clase
                                    parts[0] = str(class_index)
                                    file_corrected = True
                                corrected_lines.append(' '.join(parts) + '\n')
                            else:
                                corrected_lines.append(line)
                    
                    # Escribir archivo corregido si hubo cambios
                    if file_corrected:
                        with open(label_file, 'w') as f:
                            f.writelines(corrected_lines)
                        corrected_count += 1
                        
                except Exception as e:
                    print(f"⚠️ Error procesando {label_file}: {e}")
        
        print(f"✅ Etiquetas corregidas: {corrected_count}/{total_files} archivos")
        return corrected_count > 0
    
    def copy_and_organize_data(self, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
        """
        Copiar y organizar imágenes y etiquetas en train/val/test
        
        Args:
            train_ratio: Proporción de datos para entrenamiento
            val_ratio: Proporción de datos para validación
            test_ratio: Proporción de datos para prueba
        """
        print(f"📊 Organizando datos: {train_ratio*100}% train, {val_ratio*100}% val, {test_ratio*100}% test")
        
        for class_name in self.classes:
            class_dir = self.data_path / class_name
            images_dir = class_dir / "images"
            labels_dir = class_dir / "labels"
            
            if not images_dir.exists() or not labels_dir.exists():
                print(f"⚠️ Saltando {class_name}: faltan carpetas images o labels")
                continue
            
            # Obtener lista de imágenes
            image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
            
            if len(image_files) == 0:
                print(f"⚠️ No se encontraron imágenes en {class_name}")
                continue
            
            print(f"📸 Procesando {class_name}: {len(image_files)} imágenes")
            
            # Dividir en train/val/test
            train_files, temp_files = train_test_split(image_files, train_size=train_ratio, random_state=42)
            val_files, test_files = train_test_split(temp_files, train_size=val_ratio/(val_ratio+test_ratio), random_state=42)
            
            # Copiar archivos
            self._copy_files(train_files, "train", class_name, labels_dir)
            self._copy_files(val_files, "val", class_name, labels_dir)
            self._copy_files(test_files, "test", class_name, labels_dir)
    
    def _copy_files(self, files, split, class_name, labels_dir):
        """Copiar archivos de imagen y etiqueta al directorio correspondiente"""
        for img_file in files:
            # Copiar imagen
            dst_img = self.dataset_path / "images" / split / img_file.name
            shutil.copy2(img_file, dst_img)
            
            # Copiar etiqueta correspondiente
            label_file = labels_dir / (img_file.stem + ".txt")
            if label_file.exists():
                dst_label = self.dataset_path / "labels" / split / label_file.name
                shutil.copy2(label_file, dst_label)
            else:
                print(f"⚠️ No se encontró etiqueta para {img_file.name}")
    
    def create_yaml_config(self):
        """Crear archivo de configuración YAML para YOLO"""
        config = {
            'path': str(self.dataset_path.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'nc': len(self.classes),
            'names': self.classes
        }
        
        yaml_path = self.dataset_path / "config.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Configuración YAML creada: {yaml_path}")
        return yaml_path
    
    def verify_dataset(self):
        """Verificar la integridad del dataset"""
        print("\n🔍 Verificando dataset...")
        
        splits = ['train', 'val', 'test']
        total_images = 0
        total_labels = 0
        
        for split in splits:
            img_dir = self.dataset_path / "images" / split
            lbl_dir = self.dataset_path / "labels" / split
            
            img_count = len(list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")))
            lbl_count = len(list(lbl_dir.glob("*.txt")))
            
            total_images += img_count
            total_labels += lbl_count
            
            print(f"   {split}: {img_count} imágenes, {lbl_count} etiquetas")
        
        print(f"📊 Total: {total_images} imágenes, {total_labels} etiquetas")
        
        if total_images == total_labels:
            print("✅ Dataset verificado correctamente")
            return True
        else:
            print("❌ Inconsistencia en el dataset")
            return False
    
    def train_model(self, epochs=200, batch_size=4, img_size=416, patience=20, lr_custom=None):
        """
        Entrenar el modelo YOLO11s
        
        Args:
            epochs: Número de épocas
            batch_size: Tamaño del lote (ajustado para GTX 960M)
            img_size: Tamaño de imagen
            patience: Paciencia para early stopping
        """
        import torch
        
        # Verificar disponibilidad de GPU
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"\n🚀 Iniciando entrenamiento...")
        print(f"   📱 Dispositivo: {device}")
        print(f"   📂 Nombre del run: {self.run_name}")
        if torch.cuda.is_available():
            print(f"   🎮 GPU: {torch.cuda.get_device_name(0)}")
            print(f"   💾 Memoria GPU: {torch.cuda.get_device_properties(0).total_memory // (1024**3)} GB")
        print(f"   📊 Épocas: {epochs}")
        print(f"   📦 Batch size: {batch_size}")
        print(f"   🖼️ Tamaño imagen: {img_size}")
        
        # Cargar modelo YOLO11s (versión 11 Small)
        model = YOLO(self.model)
        
        # Configurar parámetros de entrenamiento
        yaml_config = self.dataset_path / "config.yaml"
        
        # Entrenar modelo con configuración optimizada para GTX 960M y anti-timeout
        results = model.train(
            data=str(yaml_config),
            epochs=epochs,
            batch=batch_size,
            imgsz=img_size,
            patience=patience,
            device=device,  # Usar GPU automáticamente
            save=True,
            save_period=5,  # Guardar cada 5 épocas (más frecuente para evitar pérdidas)
            project='runs/detect',
            name=self.run_name,  # Usar el nombre versionado
            exist_ok=True,
            pretrained=True,
            optimizer='AdamW',  # Optimizador más eficiente para data set pequeños
            verbose=True,
            seed=42,
            deterministic=True,
            single_cls=False,
            rect=False,
            cos_lr=True,  # Cosine LR scheduler
            close_mosaic=10,
            resume=False,
            amp=False,  # Desactivar AMP para evitar problemas GPU antiguos
            fraction=1.0,
            profile=False,
            freeze=None,
            multi_scale=True,  # Activar para permitir múltiples escalas
            overlap_mask=True,
            mask_ratio=4,
            dropout=0.0,
            val=True,
            split='val',
            save_json=False,
            conf=None,
            iou=0.7,
            max_det=300,
            half=False,  # Desactivado para GTX 960M
            dnn=False,
            plots=True,
            source=None,
            show=False,
            save_txt=False,
            save_conf=False,
            save_crop=False,
            show_labels=True,
            show_conf=True,
            vid_stride=1,
            stream_buffer=False,
            line_width=None,
            visualize=False,
            augment=False,
            agnostic_nms=False,
            classes=None,
            retina_masks=False,
            show_boxes=True,
            lr0=lr_custom if lr_custom is not None else 0.001,  # LR personalizable o por defecto
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3.0,
            warmup_momentum=0.8,
            warmup_bias_lr=0.1,
            box=7.5,
            cls=0.5,
            dfl=1.5,
            pose=12.0,
            kobj=1.0,
            nbs=64,
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=0.0,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.0,
            fliplr=0.5,
            bgr=0.0,
            mosaic=0.3,  # Reducir intensidad de mosaic
            mixup=0.0, # Desactivar para reducir carga computacional
            copy_paste=0.0, # Desactivar para estabilidad
            auto_augment='randaugment', # perfecto para usar distintos argumentos (aleatorio), inclinación, foco, etc...
            erasing=0.2,  # Reducir intensidad
            # Parámetros adicionales para optimización GPU
            workers=0,  # Desactivar multiprocessing en Windows
            cache=False,  # No cache en memoria para conservar RAM
        )
        
        print("✅ Entrenamiento completado!")
        return results
    
    def evaluate_model(self):
        """Evaluar el modelo entrenado"""
        print("\n📊 Evaluando modelo...")
        
        # Obtener ruta del mejor modelo usando el sistema de versionado
        model_paths = self.get_model_paths()
        best_model_path = model_paths['best']
        
        if not best_model_path.exists():
            print(f"❌ No se encontró el modelo entrenado en: {best_model_path}")
            return None
        
        # Cargar modelo
        model = YOLO(str(best_model_path))
        
        # Evaluar en el conjunto de validación
        results = model.val(data=str(self.dataset_path / "config.yaml"))
        
        print(f"✅ mAP50: {results.box.map50:.3f}")
        print(f"✅ mAP50-95: {results.box.map:.3f}")
        
        return results
    
    def predict_sample(self, sample_images=5):
        """Hacer predicciones en imágenes de muestra"""
        print(f"\n🔮 Prediciendo en {sample_images} imágenes de muestra...")
        
        # Obtener ruta del mejor modelo usando el sistema de versionado
        model_paths = self.get_model_paths()
        best_model_path = model_paths['best']
        
        if not best_model_path.exists():
            print(f"❌ No se encontró el modelo entrenado en: {best_model_path}")
            return
        
        # Cargar modelo
        model = YOLO(str(best_model_path))
        
        # Obtener imágenes de prueba
        test_images = list((self.dataset_path / "images" / "test").glob("*.jpg"))[:sample_images]
        
        if not test_images:
            test_images = list((self.dataset_path / "images" / "val").glob("*.jpg"))[:sample_images]
        
        # Generar nombre para las predicciones basado en el run
        prediction_name = f"prediction_{self.run_name}"
        
        # Hacer predicciones
        for img_path in test_images:
            results = model.predict(str(img_path), save=True, project="runs/predict", name=prediction_name)
            print(f"   Predicción guardada para: {img_path.name}")
        
        print(f"📁 Predicciones guardadas en: runs/predict/{prediction_name}/")
    
    def export_model(self, formats=['onnx', 'torchscript']):
        """Exportar modelo a diferentes formatos"""
        print(f"\n📦 Exportando modelo a formatos: {formats}")
        
        # Obtener ruta del mejor modelo usando el sistema de versionado
        model_paths = self.get_model_paths()
        best_model_path = model_paths['best']
        
        if not best_model_path.exists():
            print(f"❌ No se encontró el modelo entrenado en: {best_model_path}")
            return
        
        model = YOLO(str(best_model_path))
        
        for format_type in formats:
            try:
                model.export(format=format_type)
                print(f"✅ Modelo exportado a {format_type}")
            except Exception as e:
                print(f"❌ Error exportando a {format_type}: {e}")


def main(version_type="incremental", model_path="yolov8n-logo.pt"):
    """
    Función principal
    
    Args:
        version_type: Tipo de versionado ('timestamp' o 'incremental')
        model_path: Ruta al modelo base (ej: 'yolo11n.pt', 'yolov8n-logo.pt', etc.)
    """
    print("🏃‍♂️ Iniciando entrenamiento de YOLO para detección de logos deportivos")
    print("=" * 70)
    
    # Crear instancia del entrenador con versionado y modelo personalizable
    trainer = YOLOTrainer(version_type=version_type, model_path=model_path)
    
    print(f"🏷️ Tipo de versionado: {version_type}")
    print(f"🤖 Modelo base: {model_path}")
    print(f"📂 Nombre del run: {trainer.run_name}")
    
    # Detectar si es modelo especializado y ajustar configuración
    is_logo_model = "logo" in model_path.lower()
    if is_logo_model:
        print("🎯 Modelo especializado detectado - Aplicando configuración de fine-tuning")
        epochs = 50  # Menos épocas para fine-tuning
        lr = 0.0001  # Learning rate más bajo
    else:
        print("🔄 Modelo general detectado - Aplicando configuración estándar")
        epochs = 100
        lr = 0.001
    print("=" * 70)
    
    try:
        # 1. Cargar mapeo de clases
        if not trainer.load_class_mapping():
            print("❌ Error al cargar las clases")
            return
        
        # 2. Limpiar etiquetas incorrectas
        trainer.clean_labels()
        
        # 3. Organizar datos
        trainer.copy_and_organize_data()
        
        # 4. Crear configuración YAML
        trainer.create_yaml_config()
        
        # 5. Verificar dataset
        if not trainer.verify_dataset():
            print("❌ Error en la verificación del dataset")
            return
        
        # 6. Entrenar modelo con configuración dinámica
        if is_logo_model:
            print("🎯 Entrenando con configuración de fine-tuning (modelo especializado)")
            results = trainer.train_model(epochs=epochs, batch_size=4, lr_custom=lr)
        else:
            print("🔄 Entrenando con configuración estándar")
            results = trainer.train_model(epochs=epochs, batch_size=4)
        
        # 7. Evaluar modelo
        trainer.evaluate_model()
        
        # 8. Hacer predicciones de muestra
        trainer.predict_sample()
        
        # 9. Exportar modelo
        trainer.export_model(['onnx'])
        
        # Obtener rutas finales
        model_paths = trainer.get_model_paths()
        
        print("\n🎉 Proceso completado exitosamente!")
        print(f"📁 Resultados guardados en: {model_paths['results_dir']}")
        print(f"🤖 Modelo mejor en: {model_paths['best']}")
        print(f"📊 Predicciones en: runs/predict/prediction_{trainer.run_name}/")
        
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Configuración por defecto
    version_type = "timestamp"  # "timestamp" o "incremental"
    model_path = "yolov8m.pt"   # Modelo por defecto
    
    # También se pueden pasar como argumentos de línea de comandos
    # Ejemplo: python main.py timestamp yolov8n-logo.pt
    if len(sys.argv) > 1:
        if sys.argv[1] in ["timestamp", "incremental"]:
            version_type = sys.argv[1]
        else:
            # Si el primer argumento no es un tipo de versión, asumimos que es un modelo
            model_path = sys.argv[1]
            
    if len(sys.argv) > 2:
        # Segundo argumento es el modelo
        model_path = sys.argv[2]
    
    print(f"🚀 Configuración de arranque:")
    print(f"   📅 Tipo de versionado: {version_type}")
    print(f"   🤖 Modelo seleccionado: {model_path}")
    print(f"   📝 Uso: python main.py [timestamp|incremental] [modelo.pt]")
    print()
    
    main(version_type=version_type, model_path=model_path)
