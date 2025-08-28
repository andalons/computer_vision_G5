const API_BASE_URL = "http://localhost:8000";

/**
 * Servicio para interactuar con la API de análisis
 */
class AnalysisService {
  
  /**
   * Obtiene la información del proyecto desde la API
   * @returns {Promise<Object>} Información del proyecto
   */
  async getProjectInfo() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      if (!response.ok) {
        throw new Error('No se pudo recuperar la información del proyecto');
      }
      return await response.json();
    } catch (error) {
      console.error('Error al obtener información del proyecto:', error);
      throw error;
    }
  }

  /**
   * Prepara un video para análisis
   * @param {Object} videoConfig - Configuración del video
   * @param {string} videoConfig.url - URL del video
   * @param {number} [videoConfig.scale_factor=0.6] - Factor de escala
   * @param {number} [videoConfig.fps_limit=15] - Límite de FPS
   * @param {number} [videoConfig.delay_frames] - Delay entre frames (calculado automáticamente)
   * @param {boolean} [videoConfig.delete_after_processing=true] - Eliminar después del procesamiento
   * @returns {Promise<Object>} Respuesta de la preparación
   */
  async prepareVideo(videoConfig) {
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
      const response = await fetch(`${API_BASE_URL}/prepare-video`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error preparando video');
      }

      return await response.json();
    } catch (error) {
      console.error('Error al preparar video:', error);
      throw error;
    }
  }

  /**
   * Obtiene la URL del stream de video
   * @returns {string} URL del stream
   */
  getStreamUrl() {
    const timestamp = new Date().getTime();
    return `${API_BASE_URL}/stream?t=${timestamp}`;
  }

  /**
   * Verifica si la API está disponible
   * @returns {Promise<boolean>} True si la API responde
   */
  async isApiAvailable() {
    try {
      const response = await fetch(`${API_BASE_URL}/`, {
        method: 'HEAD'
      });
      return response.ok;
    } catch (error) {
      console.error('API no disponible:', error);
      return false;
    }
  }
}

// Exportar una instancia del servicio
const analysisService = new AnalysisService();

export default analysisService;