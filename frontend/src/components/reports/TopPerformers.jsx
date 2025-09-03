import React from 'react';
import { Users } from 'lucide-react';

const TopPerformers = ({ filteredData }) => {
  // Calcular top performers internamente
  const topInfluencers = (() => {
    const influencerMap = new Map();
    
    filteredData.filter(item => item.metrics).forEach(item => {
      const influencerName = item.influencer || 'Unknown Creator';
      
      if (!influencerMap.has(influencerName)) {
        influencerMap.set(influencerName, {
          name: influencerName,
          campaigns: [],
          platforms: new Set()
        });
      }
      
      const influencerData = influencerMap.get(influencerName);
      influencerData.campaigns.push(item);
      influencerData.platforms.add(item.platform);
    });
    
    return Array.from(influencerMap.values())
      .map(influencer => ({
        ...influencer,
        complianceRate: (influencer.campaigns.filter(c => c.compliance).length / influencer.campaigns.length) * 100,
        platformsText: Array.from(influencer.platforms).join(', ')
      }))
      .sort((a, b) => b.complianceRate - a.complianceRate)
      .slice(0, 5);
  })();

  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <div className="flex items-center mb-6">
        <Users className="w-6 h-6 mr-3 text-lila-500" />
        <h2 className="text-2xl font-bold font-montserrat text-petroleo-500">
          Top Performers
        </h2>
      </div>
      
      <div className="space-y-4">
        {topInfluencers.length > 0 ? (
          topInfluencers.map((influencer, index) => (
            <div key={influencer.name} className="flex items-center justify-between p-4 rounded-button bg-humo-600">
              <div className="flex items-center">
                <div className={`flex items-center justify-center w-8 h-8 mr-4 text-white rounded-full font-bold text-sm ${
                  index === 0 ? 'bg-yellow-500' : index === 1 ? 'bg-gray-400' : index === 2 ? 'bg-yellow-600' : 'bg-petroleo-400'
                }`}>
                  {index + 1}
                </div>
                <div>
                  <p className="font-medium font-source text-petroleo-500">
                    {influencer.name}
                  </p>
                  <p className="text-sm capitalize font-source text-petroleo-300">
                    {influencer.campaigns.length} campaign{influencer.campaigns.length > 1 ? 's' : ''} • {influencer.platformsText}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className={`text-lg font-bold font-montserrat ${
                  influencer.complianceRate === 100 ? 'text-green-500' : influencer.complianceRate >= 50 ? 'text-mostaza-500' : 'text-coral-500'
                }`}>
                  {influencer.complianceRate.toFixed(1)}%
                </p>
                <p className="text-xs font-source text-petroleo-300">Compliance Rate</p>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <h3 className="mb-2 text-lg font-bold font-montserrat text-petroleo-500">
              No Performance Data Available
            </h3>
            <p className="max-w-xs text-sm font-source text-petroleo-300">
              Add campaigns with metrics to see top performing influencers
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TopPerformers;