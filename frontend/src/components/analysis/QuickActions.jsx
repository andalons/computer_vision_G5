import React from 'react';

const QuickActions = () => {
  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h3 className="mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
        Actions
      </h3>
      <div className="space-y-4">
        <button className="w-full px-6 py-4 font-semibold text-white transition-all duration-300 font-montserrat rounded-button bg-coral-gradient hover:shadow-coral">
          Download Report
        </button>
        <button className="w-full px-6 py-4 font-semibold transition-all duration-300 border-2 font-montserrat rounded-button border-lila-500 text-lila-500 hover:bg-lila-500 hover:text-white hover:shadow-lila">
          View ROI Analysis
        </button>
      </div>
    </div>
  );
};

export default QuickActions;