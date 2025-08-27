# 🎥 Sistema de Análisis de Video - Grupo 5

## 📋 Descripción del Proyecto

Sistema de análisis de video desarrollado por el **Grupo 5** que permite descargar videos desde URLs (Instagram, YouTube, TikTok.) y procesarlos en tiempo real con streaming visual. La aplicación utiliza FastAPI como backend y una interfaz web HTML para la interacción del usuario.

### 🎯 Características Principales

- ✅ Descarga de videos desde múltiples plataformas (Instagram, YouTube, TikTok.)
- ✅ Análisis de video en tiempo real con streaming
- ✅ Interfaz web intuitiva con controles de FPS y escala
- ✅ API REST con documentación automática
- ✅ Configuración flexible de parámetros de procesamiento
- ✅ Arquitectura modular con sistema core centralizado

---

## 🛠️ Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10/11, macOS, Linux
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espacio en disco**: 2GB libres para videos temporales

### Dependencias Principales
- `yt-dlp`: Para descarga de videos
- `opencv-python`: Para procesamiento de video
- `fastapi`: Framework web
- `uvicorn`: Servidor ASGI
- `pydantic`: Validación de datos

---

## 📥 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/andalons/computer_vision_G5.git
cd computer_vision_G5
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# En macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
# Desde el directorio raíz del proyecto
pip install -r requirements.txt

# O desde el directorio backend
pip install -r backend/app/requirements.txt
```

### 4. Verificar Instalación
```bash
python -c "import cv2, fastapi, yt_dlp; print('✅ Todas las dependencias instaladas correctamente')"
```

---

## 🚀 Puesta en Marcha

### Método 1: Inicio Rápido con Script
```bash
# Navegar al directorio backend
cd backend

# Ejecutar el servidor API
python start_api.py
```

### Método 2: Inicio Manual
```bash
# Desde el directorio backend
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Acceder a la Interfaz Web
Una vez iniciado el servidor, abrir en el navegador:
- **Interfaz Principal**: http://localhost:8000
- **Interfaz de Usuario**: `frontend/text_api.html` (servir con servidor HTTP local)

### 4. Servir Frontend (Opción A - Python)
```bash
# En nueva terminal, navegar a frontend
cd frontend
python -m http.server 8080
```
Luego acceder a: http://localhost:8080/text_api.html

### 5. Servir Frontend (Opción B - Abrir directamente)
Abrir directamente el archivo `frontend/text_api.html` en el navegador.

---

## 📖 Uso del Sistema

### 1. Preparar Video
1. Ingresar URL del video (Instagram, YouTube, etc.)
2. Ajustar configuración:
   - **FPS**: Frames por segundo del streaming (1-60)
   - **Factor de Escala**: Reducir resolución para mejor rendimiento (0.1-1.0)
3. Hacer clic en **"Preparar vídeo"**

### 2. Iniciar Análisis
1. Una vez preparado, hacer clic en **"Iniciar análisis"**
2. El video se mostrará con procesamiento en tiempo real
3. Usar **"Detener"** para parar el análisis

### 3. Configuración Avanzada

#### Parámetros de Streaming
```json
{
  "fps_limite": 15.0,          // FPS del streaming
  "factor_escala": 0.6,        // Factor de redimensionado
  "altura_minima": 640,        // Altura mínima en píxeles
  "delay_frames": 0.067        // Delay entre frames (calculado)
}
```

#### URLs de Ejemplo
- Instagram: `https://www.instagram.com/dulceida/reel/C2pBKGKiDSR/`
- YouTube: `https://www.youtube.com/watch?v=VIDEO_ID`
- TikTok: `https://www.tiktok.com/@angelacrochett/video/7541491998251830544`

---

## 🔧 Estructura del Proyecto

```
computer_vision_G5/
├── backend/                    # Código del servidor
│   ├── start_api.py           # Script de inicio del servidor
│   └── app/                   # Aplicación principal
│       ├── main.py            # API FastAPI principal
│       ├── descargar_video.py # Módulo de descarga
│       ├── analizar_video.py  # Módulo de análisis
│       ├── procesar_video_local.py # Procesamiento local
│       ├── enlaces.json       # Enlaces de prueba
│       └── core/              # Sistema core centralizado
│           ├── config.py      # Configuraciones
│           ├── core.py        # Funcionalidades core
│           ├── models.py      # Modelos de datos
│           ├── state.py       # Gestión de estado
│           └── utils.py       # Utilidades
├── frontend/                  # Interfaz web
│   └── text_api.html         # Interfaz HTML principal
├── videos_descargados/       # Videos temporales descargados
├── notebooks/                # Notebooks de desarrollo
├── reports/                  # Informes y resultados
├── tests/                    # Tests unitarios
└── requirements.txt          # Dependencias del proyecto
```

---

## 🌐 Endpoints de la API

### Información del Proyecto
- **GET** `/` - Información básica del proyecto
- **GET** `/health` - Estado de salud del sistema
- **GET** `/stats` - Estadísticas del sistema

### Procesamiento de Video
- **POST** `/prepare-video` - Preparar video para análisis
- **GET** `/stream` - Iniciar streaming del análisis
- **GET** `/video-info` - Obtener información del video actual

### Documentación Automática
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## ⚙️ Configuración Avanzada

### Variables de Entorno
```bash
# Opcional: Configurar puerto personalizado
export API_PORT=8000
export API_HOST=0.0.0.0
```

### Configuración de Descarga
En `backend/app/core/config.py`:
```python
DOWNLOAD_CONFIG = {
    'format': 'mp4/bestaudio/best',
    'timeout': 300,  # 5 minutos
    'max_retries': 3
}
```

### Optimización de Rendimiento
```python
# Configuración recomendada para mejor rendimiento
DEFAULT_STREAM_CONFIG = {
    'fps_limite': 15.0,      # Reducir para mejor rendimiento
    'factor_escala': 0.6,    # Escalar para reducir carga
    'altura_minima': 640     # Resolución mínima
}
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegurarse de estar en el directorio backend
cd backend
python start_api.py
```

### Error: "Port already in use"
```bash
# Cambiar puerto en start_api.py o terminar proceso existente
netstat -ano | findstr :8000  # Windows
lsof -ti:8000 | xargs kill    # macOS/Linux
```

### Error de descarga de video
1. Verificar que la URL sea válida y accesible
2. Comprobar conexión a internet
3. Algunos sitios pueden requerir autenticación

### Problemas de rendimiento
1. Reducir FPS límite (5-15 recomendado)
2. Aumentar factor de escala (0.3-0.6)
3. Verificar recursos del sistema (CPU, RAM)

---

## 📝 Logs y Depuración

### Logs del Sistema
Los logs se muestran en la consola donde se ejecuta el servidor:
```
🚀 Iniciando server API de Análisis de Video...
📡 La API estará disponible en:
   • Interfaz web: http://localhost:8000
   • Documentación automática: http://localhost:8000/docs
✅ Core importado exitosamente
🔧 CORS configurado correctamente
```

### Monitoreo en Tiempo Real
- Acceder a `/health` para estado del sistema
- Usar `/stats` para estadísticas detalladas
- Los logs muestran cada frame procesado

---

## 🔄 Actualización del Sistema

```bash
# Actualizar repositorio
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Reiniciar servidor
# Ctrl+C para detener, luego python start_api.py
```

---

## 👥 Equipo de Desarrollo

**Grupo 5** - Proyecto de Visión Artificial  
Versión: 1.0.0

### Contacto y Soporte
- Repositorio: https://github.com/andalons/computer_vision_G5
- Issues: https://github.com/andalons/computer_vision_G5/issues

---

## 📄 Licencia

Este proyecto es parte de un curso académico de Inteligencia Artificial. Consultar con los instructores para términos de uso específicos.

---

## 🆘 Comandos de Referencia Rápida

```bash
# Instalación completa
git clone https://github.com/andalons/computer_vision_G5.git
cd computer_vision_G5
pip install -r requirements.txt

# Inicio del sistema
cd backend
python start_api.py

# Frontend (en nueva terminal)
cd frontend
python -m http.server 8080

# URLs importantes
# API: http://localhost:8000
# Frontend: http://localhost:8080/text_api.html
# Docs: http://localhost:8000/docs
```

