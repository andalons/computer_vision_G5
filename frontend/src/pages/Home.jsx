import React from 'react';
import HeroSection from '../components/home/HeroSection';
import ProblemSolutionSection from '../components/home/ProblemSolutionSection';
import SupportedBrandsSection from '../components/home/SupportedBrandsSection';
import VideoDemoSection from '../components/home/VideoDemoSection';

const Home = () => {
  return (
    <div className="min-h-screen bg-humo-500">

      {/* Sección de Hero */}
      <HeroSection />

      {/* Sección de Problema/Solución */}
      <ProblemSolutionSection />

      {/* Sección de Logos Soportados con búcle infinito*/}
      <SupportedBrandsSection />

      {/* Video Demo Section */}
      <VideoDemoSection />
  
    </div>
  );
};

export default Home;