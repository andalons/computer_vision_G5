import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import DetectionCarousel from './DetectionCarousel';
import MetricsPanel from './MetricsPanel';

const AnalysisResults = ({ videoData, metrics, formData, onReset }) => {
  const [currentFrame, setCurrentFrame] = useState(0);
  
  // Placeholder frames data - reemplazar con datos reales de BD
  const detectionFrames = [
    { id: 1, timestamp: '0:23', confidence: 97, brand: 'Nike' },
    { id: 2, timestamp: '1:15', confidence: 94, brand: 'Nike' },
    { id: 3, timestamp: '2:08', confidence: 96, brand: 'Nike' },
    { id: 4, timestamp: '2:45', confidence: 93, brand: 'Nike' }
  ];

  const nextFrame = () => {
    setCurrentFrame(prev => (prev + 1) % detectionFrames.length);
  };

  const prevFrame = () => {
    setCurrentFrame(prev => prev === 0 ? detectionFrames.length - 1 : prev - 1);
  };

  return (
    <div className="min-h-screen pt-32 pb-20 bg-humo-500">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        
        {/* Header */}
        <div className="flex flex-col items-start justify-between mb-12 lg:flex-row lg:items-center">
          <div className="mb-6 lg:mb-0">
            <h1 className="mb-4 text-5xl font-bold font-montserrat text-petroleo-500">
              Analysis Complete
            </h1>
            <div className="grid grid-cols-1 gap-4 text-base md:grid-cols-2 font-source text-petroleo-300">
              <div className="flex items-center">
                <div className="flex-shrink-0 w-2 h-2 mr-3 rounded-full bg-coral-500"></div>
                <span className="mr-2 font-medium">Brand:</span>
                <span className="truncate">{formData.brand}</span>
              </div>
              <div className="flex items-center">
                <div className="flex-shrink-0 w-2 h-2 mr-3 rounded-full bg-lila-500"></div>
                <span className="mr-2 font-medium">Platform:</span>
                <span className="truncate">{videoData?.platform || 'Detecting...'}</span>
              </div>
              <div className="flex items-center">
                <div className="flex-shrink-0 w-2 h-2 mr-3 rounded-full bg-mostaza-500"></div>
                <span className="mr-2 font-medium">Influencer:</span>
                <span className="truncate">{videoData?.influencer || 'Not available'}</span>
              </div>
              {videoData?.duration_seconds && (
                <div className="flex items-center">
                  <div className="flex-shrink-0 w-2 h-2 mr-3 rounded-full bg-petroleo-400"></div>
                  <span className="mr-2 font-medium">Duration:</span>
                  <span className="truncate">{Math.floor(videoData.duration_seconds / 60)}:{(videoData.duration_seconds % 60).toString().padStart(2, '0')}</span>
                </div>
              )}
            </div>
          </div>
          <button
            onClick={onReset}
            className="px-6 py-3 font-medium transition-all duration-300 border-2 whitespace-nowrap font-montserrat rounded-button border-lila-500 text-lila-500 hover:bg-lila-500 hover:text-white hover:shadow-lila"
          >
            New Analysis
          </button>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          
          {/* Deslizador de fotogramas */}
          <div className="lg:col-span-2">
            <DetectionCarousel 
              detectionFrames={detectionFrames}
              currentFrame={currentFrame}
              setCurrentFrame={setCurrentFrame}
              nextFrame={nextFrame}
              prevFrame={prevFrame}
            />
          </div>

          {/* Panel de estadísticas */}
          <div className="space-y-8">
            <MetricsPanel 
              metrics={metrics}
              formData={formData}
              videoData={videoData}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;