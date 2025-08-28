import React, { useState } from 'react';
import analysisService from '../services/AnalysisService';

const LinkAnalysis = () => {
  const [url, setUrl] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleStartAnalysis = async () => {
    if (!url.trim()) {
      setError('Por favor, ingresa una URL válida');
      return;
    }

    setError('');
    setIsLoading(true);
    setStatus('Preparando y analizando video...');

    try {
      // Preparar el video
      const result = await analysisService.prepareVideo({ url });
      
      // Iniciar el stream automáticamente
      setIsStreaming(true);
      setStatus(`Análisis iniciado: ${result.message}`);
    } catch (err) {
      setError(err.message);
      setStatus('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopStream = () => {
    setIsStreaming(false);
    setStatus('Análisis detenido');
  };

  return (
    <div className="container px-4 py-8 mx-auto">
      <h1 className="mb-6 text-4xl font-bold">Link Analysis</h1>
      
      <div className="p-6 mb-6 rounded-lg bg-blue-50">
        <div className="mb-4">
          <label htmlFor="videoUrl" className="block mb-2 text-sm font-medium text-gray-700">
            URL del video:
          </label>
          <input
            type="url"
            id="videoUrl"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.instagram.com/..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div className="space-x-2">
          <button
            onClick={handleStartAnalysis}
            disabled={isLoading}
            className="px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isLoading ? 'Procesando...' : 'Analizar Video'}
          </button>
          
          <button
            onClick={handleStopStream}
            disabled={!isStreaming}
            className="px-4 py-2 text-white bg-red-600 rounded hover:bg-red-700 disabled:bg-gray-400"
          >
            Detener
          </button>
        </div>
      </div>

      {status && (
        <div className="px-4 py-3 mb-4 text-green-700 bg-green-100 border border-green-400 rounded">
          {status}
        </div>
      )}

      {error && (
        <div className="px-4 py-3 mb-4 text-red-700 bg-red-100 border border-red-400 rounded">
          {error}
        </div>
      )}

      {isStreaming && (
        <div className="mt-6">
          <img
            src={analysisService.getStreamUrl()}
            alt="Video análisis"
            className="max-w-full border-2 border-gray-300 rounded"
          />
        </div>
      )}
    </div>
  );
};

export default LinkAnalysis;