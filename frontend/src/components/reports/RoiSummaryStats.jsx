import React from 'react';
import { BarChart3, DollarSign, Award, Clock } from 'lucide-react';

const RoiSummaryStats = ({ filteredData }) => {
  // Calcular estadísticas de resumen internamente
  const summaryStats = {
    totalCampaigns: filteredData.length,
    totalInvestment: filteredData.reduce((sum, item) => sum + (item.contract_price || 0), 0),
    avgCompliance: filteredData.length > 0 ? 
      (filteredData.filter(item => item.compliance).length / filteredData.length * 100) : 0,
    totalExposureTime: filteredData.reduce((sum, item) => 
      sum + (item.metrics?.total_time_seconds || 0), 0)
  };

  return (
    <div className="grid grid-cols-1 gap-6 mb-12 md:grid-cols-2 lg:grid-cols-4">
      <div className="p-6 bg-white rounded-card shadow-strong">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-card bg-coral-500/10">
            <BarChart3 className="w-6 h-6 text-coral-500" />
          </div>
          <span className="text-3xl font-bold font-montserrat text-coral-500">
            {summaryStats.totalCampaigns}
          </span>
        </div>
        <p className="font-medium font-source text-petroleo-500">Total Campaigns</p>
        <p className="text-sm font-source text-petroleo-300">Analyzed collaborations</p>
      </div>

      <div className="p-6 bg-white rounded-card shadow-strong">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-card bg-mostaza-500/10">
            <DollarSign className="w-6 h-6 text-mostaza-500" />
          </div>
          <span className="text-3xl font-bold font-montserrat text-mostaza-500">
            €{summaryStats.totalInvestment.toLocaleString()}
          </span>
        </div>
        <p className="font-medium font-source text-petroleo-500">Total Investment</p>
        <p className="text-sm font-source text-petroleo-300">Contract values sum</p>
      </div>

      <div className="p-6 bg-white rounded-card shadow-strong">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-card bg-lila-500/10">
            <Award className="w-6 h-6 text-lila-500" />
          </div>
          <span className="text-3xl font-bold font-montserrat text-lila-500">
            {summaryStats.avgCompliance.toFixed(1)}%
          </span>
        </div>
        <p className="font-medium font-source text-petroleo-500">Compliance Rate</p>
        <p className="text-sm font-source text-petroleo-300">Contract requirements met</p>
      </div>

      <div className="p-6 bg-white rounded-card shadow-strong">
        <div className="flex items-center justify-between mb-4">
          <div className="p-3 rounded-card bg-petroleo-500/10">
            <Clock className="w-6 h-6 text-petroleo-500" />
          </div>
          <span className="text-3xl font-bold font-montserrat text-petroleo-500">
            {Math.round(summaryStats.totalExposureTime)}s
          </span>
        </div>
        <p className="font-medium font-source text-petroleo-500">Total Exposure</p>
        <p className="text-sm font-source text-petroleo-300">Brand visibility time</p>
      </div>
    </div>
  );
};

export default RoiSummaryStats;