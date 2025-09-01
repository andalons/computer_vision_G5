import React, { useRef, useState } from 'react';
import FormInput from '../components/analysis/FormInput';
import StartAnalysisButton from '../components/analysis/StartAnalysisButton';
import AnalysisResults from '../components/analysis/AnalysisResults';

const LinkAnalysis = () => {
  const formRef = useRef();
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const [videoData, setVideoData] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [formData, setFormData] = useState(null);
  const [screenshots, setScreenshots] = useState(null);

  const handleAnalysisComplete = (data) => {
    setVideoData(data.videoData);
    setMetrics(data.metrics);
    setFormData(data.formData);
    setScreenshots(data.screenshots);
    setAnalysisComplete(true);
  };

  const resetAnalysis = () => {
    setAnalysisComplete(false);
    setVideoData(null);
    setMetrics(null);
    setFormData(null);
    setScreenshots(null);
    if (formRef.current) {
      formRef.current.resetForm();
    }
  };

  if (analysisComplete) {
    return (
      <AnalysisResults 
        videoData={videoData}
        metrics={metrics}
        formData={formData}
        screenshots={screenshots}
        onReset={resetAnalysis}
      />
    );
  }

  return (
    <div className="min-h-screen pt-32 pb-20 bg-humo-500">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        
        {/* Header */}
        <div className="relative mb-16 text-center">
          <h1 className="mb-6 text-6xl font-bold font-montserrat text-petroleo-500">
            Automate Logo Verification
          </h1>
          <p className="max-w-4xl mx-auto text-2xl leading-relaxed font-source text-petroleo-300">
            Transform manual campaign verification from hours to minutes. Get precise brand exposure metrics and contract compliance reports with AI-powered detection
          </p>
        </div>

        {/* Contenedor principal formulario */}
        <div className="relative p-12 mb-12 bg-white rounded-card shadow-strong">
          <div className="relative max-w-6xl mx-auto">
            
            {/* Formulario */}
            <FormInput ref={formRef} />

            {/* Botón de iniciar análisis */}
            <StartAnalysisButton 
              formRef={formRef}
              onAnalysisComplete={handleAnalysisComplete}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LinkAnalysis;