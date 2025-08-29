import React from 'react';
import HeroSection from '../components/home/HeroSection';
import ProblemSolutionSection from '../components/home/ProblemSolutionSection';

const Home = () => {
  return (
    <div className="min-h-screen bg-humo-500">

      {/* Sección de Hero */}
      <HeroSection />

      {/* Sección de Problema/Solución */}
      <ProblemSolutionSection />
  
    </div>
  );
};

export default Home;