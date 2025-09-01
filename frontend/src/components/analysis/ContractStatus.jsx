import React from 'react';

const ContractStatus = ({ metrics, formData }) => {
  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <h3 className="mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
        Contract Performance
      </h3>
      <div className="space-y-5">
        <div className="flex items-center justify-between p-4 rounded-button bg-humo-600">
          <span className="font-medium font-source text-petroleo-500">Contract Status</span>
          <span className={`px-3 py-1 text-sm font-bold text-white rounded-full font-montserrat ${
            metrics?.contract_compliant ? 'bg-green-500' : 'bg-coral-500'
          }`}>
            {metrics?.contract_compliant ? 'Compliant' : 'Non-compliant'}
          </span>
        </div>
        
        {formData.contract_price && (
          <div className="flex items-center justify-between p-4 rounded-button bg-coral-500/10">
            <span className="font-medium font-source text-petroleo-500">Contract Value</span>
            <span className="text-xl font-bold font-montserrat text-coral-500">
              €{formData.contract_price}
            </span>
          </div>
        )}
        
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 text-center rounded-button bg-lila-500/10">
            <div className="text-lg font-bold font-montserrat text-lila-500">
              {formData.min_brand_time || 0}s / {metrics?.total_time_seconds || 0}s
            </div>
            <div className="text-xs font-source text-petroleo-400">Required / Actual</div>
          </div>
          
          <div className="p-4 text-center rounded-button bg-mostaza-500/10">
            <div className="text-lg font-bold font-montserrat text-mostaza-500">
              {formData.min_logo_area || 0}% / {metrics?.average_area_percentage || 0}%
            </div>
            <div className="text-xs font-source text-petroleo-400">Required / Actual</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContractStatus;