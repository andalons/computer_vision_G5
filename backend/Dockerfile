# Dockerfile para Backend (Python/FastAPI)
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para OpenCV y otras librerías
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos y instalar dependencias
COPY requirements.txt ./
COPY backend/app/requirements.txt ./backend/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r backend/app/requirements.txt

# Copiar el código de la aplicación
COPY backend/ ./backend/

# Crear directorio para archivos temporales si no existe
RUN mkdir -p /tmp/downloads

# Crear directorios necesarios para la aplicación
RUN mkdir -p /app/runs/debug_frames

# Crear directorio para configuración de Ultralytics y dar permisos
RUN mkdir -p /root/.config/Ultralytics && chmod 755 /root/.config/Ultralytics

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "backend/start_api.py"]
