# Entrenamiento YOLO11n para Detección de Logos Deportivos

Este proyecto entrena un modelo YOLO11n para detectar logos de marcas deportivas en imágenes y videos con **sistema de versionado automático**.

## 🏷️ Sistema de Versionado

El proyecto incluye un **sistema automático de versionado** que organiza los entrenamientos de manera sistemática:

### Tipos de Versionado

1. **Timestamp** (por defecto): `modelo_entreno_2025-08-27_14-30-15`
2. **Incremental**: `modelo_entreno_v1`, `modelo_entreno_v2`, `modelo_entreno_v3`
3. **Por fecha**: `modelo_entreno_2025-08-27`, `modelo_entreno_2025-08-27_1`

### Uso Básico

```bash
# Versionado con timestamp (por defecto)
python train_model.py

# Versionado incremental
python train_model.py incremental

# Versionado con timestamp explícito
python train_model.py timestamp
```



## 📋 Marcas Detectadas

El modelo puede detectar los siguientes logos deportivos:
- **Adidas**: Marca alemana icónica
- **Nike**: Marca estadounidense líder
- **Puma**: Marca alemana deportiva


## 🚀 Instalación

### Prerequisitos
- Python 3.8 o superior
- Git
- CUDA (opcional, para entrenamiento con GPU)


### Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Para GPU con CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📊 Estructura del Dataset

```
by_class/
├── label_map.txt          # Mapeo de clases
├── report.csv            # Reporte del dataset
├── adidas/
│   ├── images/
│   └── labels/
├── nike/
│   ├── images/
│   └── labels/
└── ... (otras marcas)
```

## 🏃‍♂️ Uso

### Entrenamiento Completo
```python
python train_model.py
```

El script realizará automáticamente:
1. ✅ Carga del mapeo de clases
2. 📁 Organización de datos (train/val/test: 70%/20%/10%)
3. ⚙️ Creación de configuración YAML
4. 🔍 Verificación de integridad del dataset
5. 🚀 Entrenamiento del modelo YOLO11n
6. 📊 Evaluación del modelo
7. 🔮 Predicciones de muestra
8. 📦 Exportación del modelo

### Configuración Personalizada

Puedes modificar los parámetros en la función `main()`:

```python
# Entrenar con más épocas y batch size mayor
results = trainer.train_model(epochs=100, batch_size=16)

# Cambiar proporción train/val/test
trainer.copy_and_organize_data(train_ratio=0.8, val_ratio=0.15, test_ratio=0.05)
```

## 📁 Resultados con Versionado

Después del entrenamiento, encontrarás los resultados organizados por versión:

```
runs/detect/
├── modelo_entreno_2025-08-27_14-30-15/    # Versionado timestamp
│   ├── weights/
│   │   ├── best.pt                         # Mejor modelo
│   │   └── last.pt                         # Último checkpoint
│   ├── results.csv                         # Métricas de entrenamiento
│   ├── results.png                         # Gráficos de entrenamiento  
│   ├── confusion_matrix.png                # Matriz de confusión
│   └── args.yaml                           # Configuración utilizada
├── modelo_entreno_v1/                      # Versionado incremental
├── modelo_entreno_v2/
└── prediction_modelo_entreno_2025-08-27_14-30-15/  # Predicciones

runs/predict/
├── prediction_modelo_entreno_v1/           # Predicciones del modelo v1
├── prediction_modelo_entreno_v2/           # Predicciones del modelo v2
└── ...
```

### Acceso Programático a Resultados

```python
from version_manager import VersionManager

# Obtener rutas del modelo más reciente
latest_run = VersionManager.get_latest_run("modelo_entreno")
paths = VersionManager.get_model_paths(latest_run)

# Cargar el mejor modelo
from ultralytics import YOLO
model = YOLO(paths['best'])

# Hacer predicciones
results = model.predict("imagen.jpg")
```
│   ├── last.pt           # Último modelo
│   └── ...
├── train_batch*.jpg      # Batches de entrenamiento visualizados
├── val_batch*.jpg        # Batches de validación visualizados
├── results.png           # Gráficas de métricas
├── confusion_matrix.png  # Matriz de confusión
├── F1_curve.png          # Curva F1
├── P_curve.png           # Curva de Precisión
├── R_curve.png           # Curva de Recall
└── PR_curve.png          # Curva Precisión-Recall
```

## 🔮 Predicción en Imágenes/Videos

### Predicción en una imagen
```python
from ultralytics import YOLO

# Cargar modelo entrenado
model = YOLO('runs/detect/logo_detection/weights/best.pt')

# Predecir en imagen
results = model.predict('ruta/a/imagen.jpg', save=True)
```

### Predicción en video
```python
# Predecir en video
results = model.predict('ruta/a/video.mp4', save=True)
```

### Predicción en tiempo real (webcam)
```python
# Predecir desde webcam
results = model.predict(source=0, show=True, save=True)
```

## ⚙️ Parámetros de Entrenamiento

| Parámetro | Valor por Defecto | Descripción |
|-----------|-------------------|-------------|
| `epochs` | 50 | Número de épocas de entrenamiento |
| `batch_size` | 8 | Tamaño del lote |
| `img_size` | 640 | Tamaño de imagen de entrada |
| `patience` | 20 | Épocas de paciencia para early stopping |
| `lr0` | 0.01 | Tasa de aprendizaje inicial |
| `momentum` | 0.937 | Momentum del optimizador |

## 📊 Métricas de Evaluación

El modelo reporta las siguientes métricas:
- **mAP50**: Mean Average Precision a IoU 0.5
- **mAP50-95**: Mean Average Precision promedio de IoU 0.5 a 0.95
- **Precision**: Precisión por clase
- **Recall**: Sensibilidad por clase
- **F1-Score**: Puntuación F1 por clase

## 🔧 Solución de Problemas

### Error de CUDA
```bash
# Si tienes problemas con CUDA, usar CPU
pip install torch torchvision torchaudio
```

### Error de memoria
```python
# Reducir batch size
trainer.train_model(batch_size=4)
```

### Dataset corrupto
```bash
# Verificar integridad del dataset
python -c "from train_model import YOLOTrainer; t = YOLOTrainer(); t.load_class_mapping(); t.verify_dataset()"
```

## 📈 Mejoras Futuras

- [ ] Aumentar dataset con más imágenes
- [ ] Implementar data augmentation avanzado
- [ ] Probar con YOLO11s/m/l para mejor precisión
- [ ] Agregar detección de logos en contexto deportivo
- [ ] Implementar seguimiento de logos en video
- [ ] Crear API REST para predicciones

## 📝 Licencia

Este proyecto es para fines educativos y de investigación.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de solución de problemas
2. Consulta la documentación de [Ultralytics](https://docs.ultralytics.com/)
3. Abre un issue en el repositorio
