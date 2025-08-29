import React, { useRef } from 'react';
import { Check } from 'lucide-react';

const VideoDemoSection = () => {
  const videoRef = useRef(null);

  return (
    <section id="video-demo" className="py-20 bg-petroleo-500">
      <div className="px-6 mx-auto text-center max-w-7xl lg:px-8">
        <h2 className="mb-6 text-4xl font-bold text-white font-montserrat">
          See LogoTracker in Action
        </h2>
        <p className="max-w-2xl mx-auto mb-12 text-xl font-source text-petroleo-200">
          Watch our AI detect and track brand logos in real-time with precise timestamp data and confidence scores
        </p>
        
        {/* Video Container */}
        <div className="relative max-w-4xl mx-auto">
          <div className="overflow-hidden aspect-video bg-petroleo-400 rounded-card shadow-strong">
            <video
              ref={videoRef}
              className="object-cover w-full h-full"
              poster="/api/placeholder/800/450"
              controls
            >
              <source src="/assets/videos/demo-detection.mp4" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
          
          {/*  Responsive móviles */}
          <div className="absolute p-3 sm:p-4 bottom-2 sm:bottom-4 left-2 sm:left-4 right-2 sm:right-4 bg-white/95 backdrop-blur-sm rounded-button">
            <div className="grid grid-cols-3 gap-2 text-center sm:gap-4">
              <div>
                <div className="text-lg font-bold sm:text-xl font-montserrat text-coral-500">97%</div>
                <div className="text-xs font-source text-petroleo-400">Detection</div>
              </div>
              <div>
                <div className="text-lg font-bold sm:text-xl font-montserrat text-mostaza-500">34s</div>
                <div className="text-xs font-source text-petroleo-400">Visible</div>
              </div>
              <div>
                <div className="flex items-center justify-center text-lg font-bold sm:text-xl">
                  <Check className="w-5 h-5 text-green-500 sm:w-6 sm:h-6" />
                </div>
                <div className="text-xs font-source text-petroleo-400">Contract</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default VideoDemoSection;