import React from 'react';
import { Upload, Play, BarChart3 } from 'lucide-react';
import { Link } from 'react-router-dom';

const HeroSection = () => {
  const handleVideoDemo = () => {
    const videoSection = document.getElementById('video-demo');
    if (videoSection) {
      videoSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative px-6 pt-32 pb-20 overflow-hidden lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="grid items-center grid-cols-1 gap-16 lg:grid-cols-3">
          
          {/* Contenido izquierdo -  2/3 del espacio */}
          <div className="lg:col-span-2">
            <h1 className="mb-6 text-5xl font-bold leading-tight font-montserrat lg:text-6xl text-petroleo-500">
              Measure Brand Exposure with 
              <span className="text-coral-500"> AI Precision</span>
            </h1>
            
            <p className="max-w-2xl mb-8 text-xl leading-relaxed font-source text-petroleo-300">
              Transform manual logo verification from hours to minutes. AI detection for Nike, Adidas, Asics & New Balance with 95%+ accuracy
            </p>
            
            {/* Botones móviles  */}
            <div className="flex flex-col gap-4 sm:flex-row">
              <Link to="/link-analysis" className="w-full sm:w-auto">
                <button className="flex items-center justify-center w-full px-8 py-4 text-lg font-semibold text-white transition-all duration-300 font-montserrat rounded-button bg-coral-500 hover:bg-coral-400 hover:shadow-coral">
                  <Upload className="w-5 h-5 mr-2" />
                  Try Beta Version
                </button>
              </Link>
              <button 
                onClick={handleVideoDemo}
                className="flex items-center justify-center w-full px-8 py-4 text-lg font-medium transition-all duration-300 border-2 sm:w-auto font-montserrat rounded-button border-lila-500 text-lila-500 hover:bg-lila-500 hover:text-white"
              >
                <Play className="w-5 h-5 mr-2" />
                See How It Works
              </button>
            </div>
          </div>
          
          {/* Contenido derecho - Captura de pantalla análisis */}
          <div className="relative">
            <div className="overflow-hidden bg-white border rounded-card shadow-strong border-petroleo-200">
              <div className="aspect-[4/4] bg-humo-600 flex items-center justify-center">
                <div className="text-center">
                  <div className="flex items-center justify-center w-24 h-24 mx-auto mb-4 bg-petroleo-200 rounded-card">
                    <BarChart3 className="w-12 h-12 text-petroleo-400" />
                  </div>
                  <p className="text-sm font-source text-petroleo-400">Frame logo detection</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;