import React from 'react';
import ContractStatus from './ContractStatus';
import VideoDetails from './VideoDetails';
import QuickActions from './QuickActions';

const MetricsPanel = ({ metrics, formData, videoData }) => {
  return (
    <>
      {/* Estado del contrato */}
      <ContractStatus metrics={metrics} formData={formData} />
      
      {/* Información del video */}
      <VideoDetails videoData={videoData} formData={formData} />
      
      {/* Acciones rápidas */}
      <QuickActions />
    </>
  );
};

export default MetricsPanel;