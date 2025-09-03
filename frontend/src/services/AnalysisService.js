import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Configuración base de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Obtener información básica del proyecto
export const getProjectInfo = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.error('Error al obtener información del proyecto:', error);
    throw error;
  }
};

// Preparar video para análisis
export const prepareVideo = async (videoConfig) => {
  const {
    url,
    scale_factor = 0.6,
    fps_limit = 15,
    delete_after_processing = true
  } = videoConfig;

  if (!url) {
    throw new Error('La URL del video es requerida');
  }

  const requestData = {
    url,
    scale_factor,
    fps_limit,
    delay_frames: 1.0 / fps_limit,
    delete_after_processing
  };

  try {
    const response = await api.post('/prepare-video', requestData);
    return response.data;
  } catch (error) {
    console.error('Error al preparar video:', error);
    throw error;
  }
};

// NUEVA FUNCIÓN: Analizar video con YOLO y generar métricas
export const analyzeVideo = async (videoId) => {
  if (!videoId) {
    throw new Error('Video ID es requerido para el análisis');
  }

  try {
    const response = await api.post(`/db/analyze-video/${videoId}`);
    return response.data;
  } catch (error) {
    console.error('Error al analizar video:', error);
    if (error.response?.status === 404) {
      throw new Error('Video no encontrado o archivo local no disponible');
    } else if (error.response?.status === 500) {
      throw new Error('Error interno del servidor durante el análisis');
    }
    throw error;
  }
};

// Obtener información del video cargado
export const getVideoInfo = async () => {
  try {
    const response = await api.get('/video-info');
    return response.data;
  } catch (error) {
    console.error('Error al obtener información del video:', error);
    throw error;
  }
};

// Obtener estadísticas del sistema
export const getSystemStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error al obtener estadísticas:', error);
    throw error;
  }
};

// Verificar estado de salud de la API
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error en health check:', error);
    throw error;
  }
};

// Obtener URL del stream de video
export const getStreamUrl = () => {
  const timestamp = new Date().getTime();
  return `${API_BASE_URL}/stream?t=${timestamp}`;
};

// Verificar si la API está disponible
export const isApiAvailable = async () => {
  try {
    const response = await api.head('/health');
    return response.status === 200;
  } catch (error) {
    console.error('API no disponible:', error);
    return false;
  }
};