import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Upload, Check } from 'lucide-react';
import { prepareVideo, getStreamUrl, analyzeVideo } from '../../services/AnalysisService';
import { saveVideoInfo, getVideoMetrics } from '../../services/DatabaseService';

const StartAnalysisButton = forwardRef(({ formRef, onAnalysisComplete }, ref) => {
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState('');

  const analysisSteps = [
    { name: 'Uploading', description: 'Validating video source' },
    { name: 'Processing', description: 'Preparing video for analysis' },
    { name: 'Analyzing', description: 'AI detecting brand logos' },
    { name: 'Complete', description: 'Analysis ready' }
  ];

  const handleStartAnalysis = async () => {
    setError('');
    
    if (!formRef.current || !formRef.current.validateForm()) {
      return;
    }

    const formData = formRef.current.getFormData();
    console.log('Form data:', formData);

    setIsLoading(true);
    setCurrentStep(0);

    try {
      // Paso 1: Uploading
      setCurrentStep(0);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Guardar información del video en BD y obtener metadatos
      const videoResponse = await saveVideoInfo({
        url: formData.url.trim(),
        brand: formData.brand,
        contract_price: parseFloat(formData.contract_price),
        min_brand_time: parseInt(formData.min_brand_time),
        min_logo_area: parseFloat(formData.min_logo_area)
      });

      console.log('Video guardado:', videoResponse);

      // Verificar que tenemos videoId válido
      if (!videoResponse?.supabase_record?.id) {
        throw new Error('No se pudo obtener el ID del video guardado');
      }

      const videoId = videoResponse.supabase_record.id;
      
      // Paso 2: Processing
      setCurrentStep(1);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Preparar el video para procesamiento (opcional, depende de tu flujo)
      try {
        await prepareVideo({ url: formData.url });
      } catch (prepareError) {
        console.warn('Prepare video failed, continuing:', prepareError);
        // No fallar aquí, continuar con el análisis
      }
      
      // Paso 3: Analyzing 
      setCurrentStep(2);
      console.log('Iniciando análisis con YOLO para video ID:', videoId);
      
      // Llamar al endpoint que REALMENTE hace el análisis con YOLO
      const analysisResult = await analyzeVideo(videoId);
      console.log('Análisis completado:', analysisResult);
      
      // Verificar que el análisis fue exitoso
      if (!analysisResult?.metrics) {
        throw new Error('El análisis no generó métricas válidas');
      }

      // Ahora obtener las métricas que fueron generadas por el análisis
      const realMetrics = await getVideoMetrics(videoId);
      console.log('Métricas obtenidas:', realMetrics);
      
      let metricsData;
      if (realMetrics && realMetrics.length > 0) {
        metricsData = realMetrics[0];
      } else {
        // Usar las métricas del resultado del análisis como fallback
        metricsData = analysisResult.metrics;
      }

      // Verificar compliance del contrato
      const minBrandTime = parseInt(formData.min_brand_time);
      const minLogoArea = parseFloat(formData.min_logo_area);
      const contractCompliant = (
        (metricsData.total_time_seconds >= minBrandTime) && 
        (metricsData.average_area_percentage >= minLogoArea)
      );

      // Agregar información de compliance a las métricas
      metricsData.contract_compliant = contractCompliant;
      
      // Paso 4: Complete
      setCurrentStep(3);
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Notificar al componente padre que el análisis está completo
      if (onAnalysisComplete) {
        onAnalysisComplete({
          videoData: {
            ...videoResponse.supabase_record,
            technical_info: videoResponse.technical_info
          },
          metrics: metricsData,
          formData: formData,
          screenshots: analysisResult.screenshots ? { screenshots: analysisResult.screenshots } : null
        });
      }
      
    } catch (err) {
      console.error('Error durante el análisis:', err);
      setError(err.message || 'Error durante el análisis. Por favor, inténtalo de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  useImperativeHandle(ref, () => ({
    startAnalysis: handleStartAnalysis
  }));

  return (
    <>
      {/* Botón iniciar análisis */}
      <div className="text-center">
        <button
          onClick={handleStartAnalysis}
          disabled={isLoading}
          className="px-16 py-6 text-2xl font-bold text-white transition-all duration-300 font-montserrat rounded-card bg-coral-gradient hover:shadow-coral hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          <div className="flex items-center">
            <Upload className="w-8 h-8 mr-4" />
            Start Analysis
          </div>
        </button>
      </div>

      {/* Mensajes de error */}
      {error && (
        <div className="px-8 py-6 mt-8 border-2 rounded-card text-coral-600 bg-coral-500/10 border-coral-500/30 shadow-medium">
          <p className="text-lg font-medium font-source">{error}</p>
        </div>
      )}

      {/* Cargando Modal */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm">
          <div className="max-w-md p-8 mx-4 bg-white rounded-card shadow-strong">
            <div className="text-center">
              <h3 className="mb-8 text-2xl font-bold font-montserrat text-petroleo-500">
                Analyzing Your Video
              </h3>
              
              {/* Progreso pasos */}
              <div className="mb-8 space-y-4">
                {analysisSteps.map((step, index) => (
                  <div key={index} className="flex items-center">
                    <div className={`flex items-center justify-center w-8 h-8 rounded-full mr-4 transition-all duration-300 ${
                      index < currentStep 
                        ? 'bg-green-500 text-white' 
                        : index === currentStep 
                        ? 'bg-coral-500 text-white' 
                        : 'bg-petroleo-200 text-petroleo-400'
                    }`}>
                      {index < currentStep ? (
                        <Check className="w-4 h-4" />
                      ) : index === currentStep ? (
                        <div className="w-3 h-3 border-2 border-white rounded-full border-t-transparent animate-spin"></div>
                      ) : (
                        <span className="text-sm font-bold">{index + 1}</span>
                      )}
                    </div>
                    <div className="text-left">
                      <div className={`font-semibold font-montserrat ${
                        index <= currentStep ? 'text-petroleo-500' : 'text-petroleo-400'
                      }`}>
                        {step.name}
                      </div>
                      <div className="text-sm font-source text-petroleo-300">
                        {step.description}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Barra de progreso */}
              <div className="w-full h-3 mb-6 rounded-full bg-petroleo-200">
                <div 
                  className="h-3 transition-all duration-500 ease-out rounded-full bg-coral-gradient"
                  style={{ width: `${((currentStep + 1) / analysisSteps.length) * 100}%` }}
                ></div>
              </div>
              
              <p className="text-lg font-source text-petroleo-400">
                This process typically takes 2-3 minutes
              </p>
            </div>
          </div>
        </div>
      )}
     </>
  );  
});

export default StartAnalysisButton;