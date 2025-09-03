import React from 'react';
import { TrendingUp, Euro } from 'lucide-react';

const CostEfficiency = ({ filteredData }) => {
  // Calculate best cost per second internally
  const bestCostPerSecond = (() => {
    const influencerMap = new Map();
    
    filteredData.filter(item => item.metrics && item.contract_price > 0).forEach(item => {
      const influencerName = item.influencer || 'Unknown Creator';
      
      if (!influencerMap.has(influencerName)) {
        influencerMap.set(influencerName, {
          name: influencerName,
          totalExposure: 0,
          totalInvestment: 0,
          campaigns: 0
        });
      }
      
      const influencerData = influencerMap.get(influencerName);
      influencerData.totalExposure += item.metrics.total_time_seconds;
      influencerData.totalInvestment += item.contract_price;
      influencerData.campaigns += 1;
    });
    
    return Array.from(influencerMap.values())
      .map(influencer => ({
        ...influencer,
        costPerSecond: influencer.totalExposure > 0 ? influencer.totalInvestment / influencer.totalExposure : Infinity
      }))
      .sort((a, b) => a.costPerSecond - b.costPerSecond) // Menor costo = mejor
      .slice(0, 5);
  })();

  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <div className="flex items-center mb-6">
        <Euro className="w-6 h-6 mr-3 text-mostaza-300" />
        <h2 className="text-2xl font-bold font-montserrat text-petroleo-500">
          Best Cost Efficiency
        </h2>
      </div>
      
      <div className="space-y-4">
        {bestCostPerSecond.length > 0 ? (
          bestCostPerSecond.map((campaign, index) => (
            <div key={campaign.name} className="flex items-center justify-between p-4 rounded-button bg-humo-600">
              <div className="flex items-center">
                <div className={`flex items-center justify-center w-8 h-8 mr-4 text-white rounded-full font-bold text-sm ${
                  index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : index === 2 ? 'bg-yellow-600' : 'bg-petroleo-400'
                }`}>
                  {index + 1}
                </div>
                <div>
                  <p className="font-medium font-source text-petroleo-500">
                    {campaign.name}
                  </p>
                  <p className="text-sm font-source text-petroleo-300">
                    €{campaign.totalInvestment.toLocaleString()} • {campaign.campaigns} campaign{campaign.campaigns > 1 ? 's' : ''}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold font-montserrat text-mostaza-500">
                  €{campaign.costPerSecond.toFixed(2)}/s
                </p>
                <p className="text-xs font-source text-petroleo-300">Cost per Second</p>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <h3 className="mb-2 text-lg font-bold font-montserrat text-petroleo-500">
              No Cost Data Available
            </h3>
            <p className="max-w-xs text-sm font-source text-petroleo-300">
              Add campaigns with contract prices and metrics to calculate cost efficiency
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CostEfficiency;