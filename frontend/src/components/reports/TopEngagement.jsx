import React from 'react';
import { TrendingUp } from 'lucide-react';

const TopEngagement = ({ filteredData }) => {
  // Calcular top engagement internamente
  const topEngagement = (() => {
    const influencerMap = new Map();
    
    filteredData.filter(item => item.views && item.views > 0).forEach(item => {
      const influencerName = item.influencer || 'Unknown Creator';
      
      if (!influencerMap.has(influencerName)) {
        influencerMap.set(influencerName, {
          name: influencerName,
          totalViews: 0,
          totalLikes: 0,
          totalComments: 0,
          campaigns: 0
        });
      }
      
      const influencerData = influencerMap.get(influencerName);
      influencerData.totalViews += item.views || 0;
      influencerData.totalLikes += item.likes || 0;
      influencerData.totalComments += item.comments || 0;
      influencerData.campaigns += 1;
    });
    
    return Array.from(influencerMap.values())
      .map(influencer => ({
        ...influencer,
        totalEngagement: influencer.totalLikes + influencer.totalComments,
        avgEngagementRate: influencer.totalViews > 0 ? 
          ((influencer.totalLikes + influencer.totalComments) / influencer.totalViews) * 100 : 0
      }))
      .sort((a, b) => b.avgEngagementRate - a.avgEngagementRate)
      .slice(0, 5);
  })();

  return (
    <div className="p-8 bg-white rounded-card shadow-strong">
      <div className="flex items-center mb-6">
        <TrendingUp className="w-6 h-6 mr-3 text-coral-500" />
        <h2 className="text-2xl font-bold font-montserrat text-petroleo-500">
          Top Engagement
        </h2>
      </div>
      
      <div className="space-y-4">
        {topEngagement.length > 0 ? (
          topEngagement.map((influencer, index) => (
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
                  <p className="text-sm font-source text-petroleo-300">
                    {influencer.campaigns} campaign{influencer.campaigns > 1 ? 's' : ''}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold font-montserrat text-lila-500">
                  {influencer.avgEngagementRate.toFixed(1)}%
                </p>
                <p className="text-xs font-source text-petroleo-300">Engagement Rate</p>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <h3 className="mb-2 text-lg font-bold font-montserrat text-petroleo-500">
              No Engagement Data Available
            </h3>
            <p className="max-w-xs text-sm font-source text-petroleo-300">
              Add campaigns with view and engagement metrics to see top performers
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TopEngagement;