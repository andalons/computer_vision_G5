import React, { useState, useEffect } from 'react';
import { listVideos, getVideoMetrics } from '../services/DatabaseService';
import RoiHeader from '../components/reports/RoiHeader';
import RoiSummaryStats from '../components/reports/RoiSummaryStats';
import TopPerformers from '../components/reports/TopPerformers';
import TopEngagement from '../components/reports/TopEngagement';
import CostEfficiency from '../components/reports/CostEfficiency';
import RecentCampaignsTable from '../components/reports/RecentCampaignsTable';

const Report = () => {
  const [videos, setVideos] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filteredData, setFilteredData] = useState([]);
  const [filters, setFilters] = useState({
    platform: 'all',
    compliance: 'all',
    brand: 'all',
    dateRange: '30'
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const videosData = await listVideos();
      setVideos(videosData);
      
      const metricsPromises = videosData.map(async (video) => {
        try {
          const videoMetrics = await getVideoMetrics(video.id);
          return {
            ...video,
            metrics: videoMetrics[0] || null,
            compliance: calculateCompliance(video, videoMetrics[0])
          };
        } catch (error) {
          return {
            ...video,
            metrics: null,
            compliance: false
          };
        }
      });
      
      const combinedData = await Promise.all(metricsPromises);
      setMetrics(combinedData);
      setFilteredData(combinedData);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateCompliance = (video, metric) => {
    if (!metric) return false;
    return metric.total_time_seconds >= (video.min_brand_time || 0);
  };

  const handleFilteredDataChange = (filteredResults, newFilters) => {
    setFilteredData(filteredResults);
    setFilters(newFilters);
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-32 pb-20 bg-humo-500">
        <div className="px-6 mx-auto max-w-7xl lg:px-8">
          <div className="flex items-center justify-center h-64">
            <div className="w-8 h-8 border-4 rounded-full border-coral-500 border-t-transparent animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-32 pb-20 md:mt-16 bg-humo-500">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        
        {/* Header con filtros */}
        <RoiHeader 
          filters={filters} 
          metrics={metrics}
          onFilteredDataChange={handleFilteredDataChange} 
        />

        {/* Sumario de datos filtrados */}
        <RoiSummaryStats filteredData={filteredData} />

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          
          {/* Top Influencers por rendimiento */}
          <TopPerformers filteredData={filteredData} />

          {/* Top Engagement */}
          <TopEngagement filteredData={filteredData} />

          {/* Mejor costo por segundo */}
          <CostEfficiency filteredData={filteredData} />

        </div>

          {/* Tabla de campañas recientes */}
          <RecentCampaignsTable filteredData={filteredData} />

      </div>
    </div>
  );
};

export default Report;