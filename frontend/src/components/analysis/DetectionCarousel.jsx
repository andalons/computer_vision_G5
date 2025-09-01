import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const DetectionCarousel = ({ detectionFrames, currentFrame, setCurrentFrame, nextFrame, prevFrame, hasRealImages = false, metrics }) => {
  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h2 className="mb-8 text-3xl font-bold font-montserrat text-petroleo-500">
        Logo Detections
      </h2>
      
      {/* Carrusel */}
      <div className="relative">
        <div className="mb-6 overflow-hidden aspect-video bg-gradient-to-br from-petroleo-500 to-petroleo-600 rounded-card shadow-strong">
          {hasRealImages && detectionFrames[currentFrame].imageUrl ? (
            // Mostrar imagen real del screenshot
            <img 
              src={detectionFrames[currentFrame].imageUrl}
              alt={`Frame ${currentFrame + 1} - Logo detection`}
              className="object-cover w-full h-full"
              onError={(e) => {
                // Si falla cargar la imagen, mostrar placeholder
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
          ) : null}
          
          {/* Placeholder (se muestra si no hay imagen real o si falla cargar) */}
          <div 
            className={`flex items-center justify-center w-full h-full text-white ${hasRealImages && detectionFrames[currentFrame].imageUrl ? 'hidden' : 'flex'}`}
          >
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-6 border-4 border-white rounded-full opacity-80"></div>
              <p className="text-lg font-source opacity-80">
                Frame {currentFrame + 1}
              </p>
              <p className="mt-2 text-sm font-source opacity-60">
                Logo detected with {Math.round(metrics?.confidence_score * 100 || 0)}% confidence
              </p>
              {!hasRealImages && (
                <p className="mt-2 text-xs font-source opacity-40">
                  (Screenshot preview will be available soon)
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Navegación */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={prevFrame}
            className="p-3 text-white transition-all duration-300 rounded-button bg-petroleo-500 hover:bg-petroleo-600 hover:shadow-medium"
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
          
          <div className="flex space-x-3">
            {detectionFrames.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentFrame(index)}
                className={`w-4 h-4 rounded-full transition-all duration-300 ${
                  index === currentFrame 
                    ? 'bg-coral-500 shadow-coral scale-110' 
                    : 'bg-petroleo-300 hover:bg-petroleo-400'
                }`}
              />
            ))}
          </div>
          
          <button
            onClick={nextFrame}
            className="p-3 text-white transition-all duration-300 rounded-button bg-petroleo-500 hover:bg-petroleo-600 hover:shadow-medium"
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>

        {/* DATOS FIJOS DE LA BASE DE DATOS */}
        <div className="grid grid-cols-4 gap-4 p-6 bg-gradient-to-r from-humo-600 to-humo-400 rounded-card">
          <div className="text-center">
            <div className="text-2xl font-bold font-montserrat text-coral-500">
              {Math.round(metrics?.confidence_score * 100 || 0)}%
            </div>
            <div className="text-sm font-source text-petroleo-400">Confidence</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold font-montserrat text-mostaza-500">
              {Math.round(metrics?.total_time_seconds || 0)}s
            </div>
            <div className="text-sm font-source text-petroleo-400">Total Time</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold font-montserrat text-lila-500">
              {metrics?.brand || 'N/A'}
            </div>
            <div className="text-sm font-source text-petroleo-400">Brand</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold font-montserrat text-petroleo-500">
              {Math.round(metrics?.average_area_percentage || 0)}%
            </div>
            <div className="text-sm font-source text-petroleo-400">Screen</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetectionCarousel;