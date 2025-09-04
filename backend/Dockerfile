# Dockerfile para Backend (Python/FastAPI) - Versión Simplificada
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para OpenCV (versión optimizada)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt ./
# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /tmp/downloads
RUN mkdir -p /app/runs/debug_frames
RUN mkdir -p /root/.config/Ultralytics && chmod 755 /root/.config/Ultralytics

# Variables de entorno
ENV PYTHONPATH="/app"
ENV YOLO_CONFIG_DIR="/tmp"

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "start_api.py"]
