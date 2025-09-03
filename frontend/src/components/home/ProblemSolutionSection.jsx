import React from 'react';
import { Clock, Zap } from 'lucide-react';

const ProblemSolutionSection = () => {
  return (
    <section className="py-20 bg-white">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        <div className="grid grid-cols-1 gap-16 lg:grid-cols-2">
          
          {/* Problema */}
          <div className="text-left">
            <div className="flex items-center mb-4">
              <div className="inline-flex items-center justify-center w-16 h-16 mr-4 bg-coral-500/10 rounded-card">
                <Clock className="w-8 h-8 text-coral-500" />
              </div>
              <h2 className="text-3xl font-bold font-montserrat text-petroleo-500">
                Manual Verification Takes Forever
              </h2>
            </div>
            <p className="mb-6 text-lg text-left font-source text-petroleo-300">
              Agencies spend 200+ hours monthly manually checking if influencer content meets brand exposure requirements. Human error rates reach 20%
            </p>
            <div className="space-y-3">
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-coral-500"></div>
                <span className="text-left font-source text-petroleo-400">4+ hours per video analysis</span>
              </div>
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-coral-500"></div>
                <span className="text-left font-source text-petroleo-400">High error rates</span>
              </div>
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-coral-500"></div>
                <span className="text-left font-source text-petroleo-400">Expensive manual labor</span>
              </div>
            </div>
          </div>

          {/* Solución */}
          <div className="text-left">
            <div className="flex items-center mb-4">
              <div className="inline-flex items-center justify-center w-16 h-16 mr-4 bg-mostaza-500/10 rounded-card">
                <Zap className="w-8 h-8 text-mostaza-500" />
              </div>
              <h2 className="text-3xl font-bold font-montserrat text-petroleo-500">
                AI Automation in Minutes
              </h2>
            </div>
            <p className="mb-6 text-lg text-left font-source text-petroleo-300">
              LogoTracker Pro analyzes entire campaigns automatically with precision that surpasses human capability and speed that transforms workflows
            </p>
            <div className="space-y-3">
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-mostaza-500"></div>
                <span className="text-left font-source text-petroleo-400">15 minutes per analysis</span>
              </div>
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-mostaza-500"></div>
                <span className="text-left font-source text-petroleo-400">98% precision rate</span>
              </div>
              <div className="flex items-center justify-start">
                <div className="w-3 h-3 mr-3 rounded-full bg-mostaza-500"></div>
                <span className="text-left font-source text-petroleo-400">10x cost reduction</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ProblemSolutionSection;