import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

// Configuración base de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Guardar información del video en la base de datos
export const saveVideoInfo = async (videoData) => {
  try {
    const response = await api.post('/db/save-video-info', videoData);
    return response.data;
  } catch (error) {
    console.error('Error al guardar video:', error);
    throw error;
  }
};

// Obtener todos los videos guardados
export const listVideos = async () => {
  try {
    const response = await api.get('/db/videos');
    return response.data;
  } catch (error) {
    console.error('Error al obtener videos:', error);
    throw error;
  }
};

// Obtener métricas de un video específico
export const getVideoMetrics = async (videoId) => {
  if (!videoId) {
    throw new Error('ID del video requerido');
  }

  try {
    const response = await api.get(`/db/metrics/${videoId}`);
    return response.data;
  } catch (error) {
    console.error('Error al obtener métricas:', error);
    throw error;
  }
};