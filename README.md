# LogoTracker Pro

Plataforma que detecta automáticamente logos en videos y fotos de influencers.

Resumen rápido
- Analiza videos e imágenes para localizar marcas y medir tiempo de exposición del logo.
- Genera informes que permiten verificar el cumplimiento de acuerdos publicitarios.

¿Qué problema resolvemos?
---------------------------------
Imagínate que una marca como Nike paga a un influencer para mostrar un producto y exige que el logo aparezca claramente durante X segundos. Hoy esa verificación es manual, lenta y propensa a errores. LogoTracker Pro automatiza esa tarea y entrega resultados en minutos.

Nuestra solución
---------------------------------
- Procesado automático de videos e imágenes.
- Detección de logos específicos (Nike y Adidas).
- Medición precisa del tiempo de aparición del logo.
- Informes exportables para auditoría y facturación.

Cómo funciona (resumen técnico)
---------------------------------
- Modelos de computer vision entrenados para detección de logos.
- Pipeline que extrae frames, ejecuta la inferencia y calcula métricas temporales.
- Componentes principales:
  - `backend/`: API, lógica del modelo, manejo de videos y almacenamiento temporal.
  - `frontend/`: interfaz (React) para visualizar resultados y lanzar análisis.

Marcas iniciales soportadas
---------------------------------
- Nike (swoosh)
- Adidas (tres rayas)
- (Se pueden añadir más marcas entrenando/añadiendo nuevos modelos)

Notas técnicas y cambios importantes (rutas de arranque)
---------------------------------
1) Dockerfile del Backend
	- Crea automáticamente el directorio `runs/debug_frames` para guardar capturas de debug.
	- Configura el directorio de configuración de Ultralytics en `/root/.config/Ultralytics`.
	- Ajusta permisos para evitar warnings al iniciar.

2) docker-compose.yml
	- Servicio `backend` expuesto en el puerto `8000`.
	- Servicio `frontend` expuesto en el puerto `3000`.
	- Variable de entorno añadida: `YOLO_CONFIG_DIR=/root/.config/Ultralytics`.
	- Volúmenes persistentes configurados:
	  - `debug_frames` (frames generados durante análisis)
	  - `downloads` (archivos temporales/descargas)
	- Red interna `app-network` para la comunicación entre servicios.

3) Código del Backend (`backend/app/main.py`)
	- Se crea el directorio `runs/debug_frames` antes de montar `StaticFiles`.
	- Evita el error de "directorio inexistente" al iniciar la aplicación.

# 🚀 LogoTracker Pro

Plataforma inteligente para la detección automática de logos en videos y fotos de influencers.


## 1. 🌐 Demo en Vivo

🚀  **Aplicación desplegada**: [Próximamente - En desarrollo]

_Nota: El proyecto se encuentra actualmente en desarrollo activo. La demo estará disponible próximamente._

---

## 2. 📚 Descripción del Proyecto

LogoTracker Pro resuelve el problema de verificar la presencia de logos en contenido de influencers, automatizando el análisis de videos e imágenes para marcas como Nike y Adidas. El sistema detecta logos, mide el tiempo de exposición y genera informes en minutos, eliminando el trabajo manual y los errores humanos.

**¿Qué problema resolvemos?**
- Verificación automática de contratos publicitarios (ej: "El logo debe aparecer 15 segundos").
- Ahorro de tiempo: de 2-4 horas manuales a minutos automáticos.
- Informes precisos y exportables para auditoría y facturación.

**Nuestra solución**
- Detección automática de logos en videos e imágenes.
- Medición exacta del tiempo de aparición.
- Soporte inicial para Nike y Adidas (fácilmente ampliable).

---

## 3. 🏗️ Estructura del Proyecto
```bash
computer_vision_G5/
│
├── 🐍 backend/               # Backend FastAPI, lógica de análisis y API
│   └── app/
│       ├── core/            # Configuración y utilidades
│       ├── db/              # Servicios y rutas de base de datos
│       ├── model/           # Descarga y ejecución de modelos
│       └── main.py          # API principal
│
├── 🖥️ frontend/              # Frontend React
│   ├── src/                 # Componentes, páginas y servicios
│   └── public/              # Recursos estáticos
│
├── 🤖 model/                 # Modelos de IA y scripts de inferencia           
└── README.md
```
---

## 4. 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.10+
- FastAPI
- Ultralytics (YOLO)
- Supabase (opcional)

### Frontend
- React
- Vite
- Tailwind CSS

### Machine Learning
- YOLOv8 (detección de logos)
- OpenCV

### DevOps
- Docker
- Docker Compose

---

## 5. 📋 Requisitos Previos

- Docker y Docker Compose instalados
- 8GB RAM mínimo recomendado
- GPU opcional para acelerar inferencia

---

## 6. 🚀 Instalación y Uso

### 6.1. Clonar el repositorio
```powershell
git clone https://github.com/andalons/computer_vision_G5.git
cd computer_vision_G5
```

### 6.2. Configurar variables de entorno
Edita `.env.example` y renómbralo a `.env` si necesitas personalizar credenciales.

### 6.3. Construir y levantar los servicios con Docker Compose
```powershell
# Navegar al directorio del proyecto
cd C:\Users\admin\Desktop\proyecto_12\trabajo\computer_vision_G5

# Construir e iniciar todos los servicios
docker-compose up --build

# Para ejecutar en segundo plano (detached)
docker-compose up --build -d

# Para detener los servicios
docker-compose down
```

### 6.4. (Opcional) Instalar dependencias manualmente
```powershell
# Crear y activar un entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias del backend
pip install -r backend/requirements.txt
pip install -r backend/app/requirements.txt
```

---

## 7. 📡 URLs disponibles

- Frontend (React): http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API (Swagger): http://localhost:8000/docs
- API Schema: http://localhost:8000/openapi.json
- Documentación alternativa (Redoc): http://localhost:8000/redoc

---

## 8. 🎯 Características Principales

- Detección automática de logos en videos e imágenes
- Medición precisa del tiempo de exposición
- Informes exportables
- Soporte inicial para Nike y Adidas
- Arquitectura escalable y modular


---

## 9. 📝 Licencia

Este proyecto está distribuido bajo la Licencia Factoria F5.

---

**Desarrollado con ❤️ por el equipo LogoTracker Pro**

_Aplicando inteligencia artificial para optimizar la verificación de campañas de marketing y contratos publicitarios._

