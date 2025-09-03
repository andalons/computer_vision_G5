import React from 'react';
import { Eye, Clock, BarChart3 } from 'lucide-react';

const KeyFeaturesSection = () => {
  const features = [
    {
      icon: Eye,
      title: 'AI Logo Detection',
      description: 'Advanced computer vision trained specifically for brand logo recognition with 95%+ accuracy rate'
    },
    {
      icon: Clock,
      title: 'Real-Time Analysis',
      description: 'Process videos in minutes, not hours. Get precise timestamp data for every logo appearance'
    },
    {
      icon: BarChart3,
      title: 'Detailed Reports',
      description: 'Comprehensive analytics with exposure time, contract compliance, and ROI calculations'
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        <div className="mb-16 text-center">
          <h2 className="mb-6 text-4xl font-bold font-montserrat text-petroleo-500">
            Built for Modern Marketing Teams
          </h2>
          <p className="max-w-2xl mx-auto text-xl font-source text-petroleo-300">
            Everything you need to transform manual campaign verification into automated, precise, and scalable analysis
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {features.map((feature, index) => (
            <div key={index} className="text-center lg:text-left">
              <div className="flex items-center justify-center mb-6 lg:justify-start">
                <div className="inline-flex items-center justify-center w-16 h-16 mr-4 bg-coral-500/10 rounded-card">
                  <feature.icon className="w-8 h-8 text-coral-500" />
                </div>
                <h3 className="text-xl font-semibold font-montserrat text-petroleo-500">
                  {feature.title}
                </h3>
              </div>
              <p className="leading-relaxed font-source text-petroleo-300">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default KeyFeaturesSection;