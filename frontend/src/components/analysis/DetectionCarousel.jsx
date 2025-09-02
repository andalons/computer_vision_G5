import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const DetectionCarousel = ({ detectionFrames, currentFrame, setCurrentFrame, nextFrame, prevFrame, hasRealImages = false, metrics }) => {
  const [imageAspectRatio, setImageAspectRatio] = useState(null);

  const handleImageLoad = (e) => {
    const { naturalWidth, naturalHeight } = e.target;
    const aspectRatio = naturalWidth / naturalHeight;
    setImageAspectRatio(aspectRatio);
  };

  const isVerticalVideo = imageAspectRatio !== null && imageAspectRatio < 1;

  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h2 className="mb-8 text-3xl font-bold font-montserrat text-petroleo-500">
        Logo Detections
      </h2>
      
      {/* Carrusel */}
      <div className="relative">
        <div className="mb-6 overflow-hidden aspect-video bg-gradient-to-br from-petroleo-500 to-petroleo-600 rounded-card shadow-strong">
          {hasRealImages && detectionFrames[currentFrame].imageUrl ? (
            isVerticalVideo ? (
              // Estructura para videos verticales con backdrop difuminado
              <div className="relative w-full h-full">
                {/* Imagen de fondo difuminada */}
                <img 
                  src={detectionFrames[currentFrame].imageUrl}
                  alt=""
                  className="absolute inset-0 object-cover w-full h-full scale-110 blur-lg opacity-60"
                  aria-hidden="true"
                />
                {/* Imagen principal centrada */}
                <img 
                  src={detectionFrames[currentFrame].imageUrl}
                  alt={`Frame ${currentFrame + 1} - Logo detection`}
                  className="relative z-10 object-contain w-full h-full"
                  onLoad={handleImageLoad}
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.parentNode.nextSibling.style.display = 'flex';
                  }}
                />
              </div>
            ) : (
              // Imagen normal para videos horizontales
              <img 
                src={detectionFrames[currentFrame].imageUrl}
                alt={`Frame ${currentFrame + 1} - Logo detection`}
                className="object-cover w-full h-full"
                onLoad={handleImageLoad}
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
            )
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
        <div className="grid grid-cols-3 gap-4 p-6 bg-gradient-to-r from-humo-600 to-humo-400 rounded-card">
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
              Adidas
            </div>
            <div className="text-sm font-source text-petroleo-400">Brand</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetectionCarousel;