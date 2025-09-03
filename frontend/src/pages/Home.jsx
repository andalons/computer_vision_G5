import React from 'react';
import HeroSection from '../components/home/HeroSection';
import ProblemSolutionSection from '../components/home/ProblemSolutionSection';
import SupportedBrandsSection from '../components/home/SupportedBrandsSection';
import VideoDemoSection from '../components/home/VideoDemoSection';
import KeyFeaturesSection from '../components/home/KeyFeaturesSection';
import PricingSection from '../components/home/PricingSection';
import CtaSection from '../components/home/CtaSection';

const Home = () => {
  return (
    <div className="min-h-screen md:mt-16 bg-humo-500">

      {/* Sección de Hero */}
      <HeroSection />

      {/* Sección de Problema/Solución */}
      <ProblemSolutionSection />

      {/* Sección de Logos Soportados con búcle infinito*/}
      <SupportedBrandsSection />

      {/* Sección vídeo demo */}
      <VideoDemoSection />

      {/* Sección de características */}
      <KeyFeaturesSection />

      {/* Sección de precios */}
      <PricingSection />

      {/* Sección de CTA */}
      <CtaSection />
  
    </div>
  );
};

export default Home;