import React from 'react';
import { Upload } from 'lucide-react';
import { Link } from 'react-router-dom';

const FinalCtaSection = () => {
  return (
    <section className="py-20 bg-petroleo-500">
      <div className="max-w-4xl px-6 mx-auto text-center lg:px-8">
        <h2 className="mb-6 text-4xl font-bold text-white font-montserrat">
          Transform Your Campaign Analysis Today
        </h2>
        <p className="mb-8 text-xl font-source text-petroleo-200">
          Join forward-thinking agencies who've already automated their logo verification process
        </p>
        
        <div className="flex flex-col justify-center gap-4 sm:flex-row">
          <Link to="/link-analysis" className="w-full sm:w-auto">
            <button className="flex items-center justify-center w-full px-8 py-4 text-lg font-semibold text-white transition-all duration-300 sm:w-auto font-montserrat rounded-button bg-coral-500 hover:bg-coral-400 hover:shadow-coral">
              <Upload className="w-5 h-5 mr-2" />
              Start Free Analysis
            </button>
          </Link>
          <button className="w-full px-8 py-4 text-lg font-medium text-white transition-all duration-300 border-2 border-white sm:w-auto font-montserrat rounded-button hover:bg-white hover:text-petroleo-500">
            Schedule Demo Call
          </button>
        </div>
      </div>
    </section>
  );
};

export default FinalCtaSection;