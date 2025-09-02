# 📊 Hugging Face Assets

Esta carpeta contiene todas las imágenes y gráficos utilizados en el documento `HUGGINGFACE_MODEL_COMPARISON.md` para la comparativa entre los modelos YOLOv8 Medium y Small.

## 📁 Contenido de la Carpeta

### 📈 Gráficos de Entrenamiento
- `medium_results.png` - Curvas de entrenamiento del modelo Medium (mAP, pérdidas, etc.)
- `small_results.png` - Curvas de entrenamiento del modelo Small (mAP, pérdidas, etc.)

### 🎯 Matrices de Confusión
- `medium_confusion_matrix.png` - Matriz de confusión del modelo Medium
- `small_confusion_matrix.png` - Matriz de confusión del modelo Small

### 📊 Curvas de Rendimiento
- `medium_pr_curve.png` - Curva Precision-Recall del modelo Medium
- `small_pr_curve.png` - Curva Precision-Recall del modelo Small
- `medium_f1_curve.png` - Curva F1-Score del modelo Medium
- `small_f1_curve.png` - Curva F1-Score del modelo Small

### 🏷️ Análisis del Dataset
- `medium_labels.jpg` - Distribución de labels utilizada en el entrenamiento del modelo Medium
- `small_labels.jpg` - Distribución de labels utilizada en el entrenamiento del modelo Small

### 🔍 Ejemplos de Validación
- `medium_val_batch0_labels.jpg` - Ground truth del batch 0 de validación (Medium)
- `small_val_batch0_labels.jpg` - Ground truth del batch 0 de validación (Small)
- `medium_val_batch0_pred.jpg` - Predicciones del batch 0 de validación (Medium)
- `small_val_batch0_pred.jpg` - Predicciones del batch 0 de validación (Small)
- `medium_val_batch1_pred.jpg` - Predicciones del batch 1 de validación (Medium)
- `small_val_batch1_pred.jpg` - Predicciones del batch 1 de validación (Small)

## 🎯 Propósito

Estas imágenes son utilizadas en el documento de comparativa de Hugging Face para:

1. **Visualizar el rendimiento** de ambos modelos
2. **Comparar métricas** de forma gráfica
3. **Mostrar ejemplos reales** de detección
4. **Documentar la calidad** de los entrenamientos
5. **Facilitar la comprensión** de las diferencias entre modelos

## 📋 Uso

Los enlaces en `HUGGINGFACE_MODEL_COMPARISON.md` apuntan a esta carpeta usando rutas relativas:
```markdown
![Imagen](./huggingface_assets/nombre_imagen.png)
```

## 📅 Última Actualización

**Fecha**: 2 de septiembre de 2025  
**Modelos**: YOLOv8 Medium vs Small  
**Dataset**: Sports Logos (4 clases: adidas, adidas_1, adidas_2, nike)
