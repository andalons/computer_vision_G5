import React, { useState } from 'react';
import { Download, ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';

const RecentCampaignsTable = ({ filteredData }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  // Normalizar marcas
  const normalizeBrand = (brand) => {
    if (!brand) return 'Adidas';
    const lowerBrand = brand.toLowerCase();
    if (lowerBrand.includes('adidas')) return 'Adidas';
    if (lowerBrand.includes('nike')) return 'Nike';
    return brand;
  };

  // Calculo de paginas
  const totalItems = filteredData.length;
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredData.slice(startIndex, endIndex);

  // Manejo de paginación
  const handlePreviousPage = () => {
    setCurrentPage(prev => Math.max(prev - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage(prev => Math.min(prev + 1, totalPages));
  };

  const handleItemsPerPageChange = (newItemsPerPage) => {
    setItemsPerPage(newItemsPerPage);
    setCurrentPage(1);
  };

  // Funcionalidad de exportación de datos
  const handleExportData = () => {
    const csvContent = [
      // Headers
      ['Influencer', 'Platform', 'Video URL', 'Brand', 'Investment', 'Engagement Rate', 'Exposure Time', 'Cost per Second', 'Compliance'].join(','),
      // Columnas de datos
      ...filteredData.map(campaign => {
        const costPerSecond = campaign.metrics && campaign.metrics.total_time_seconds > 0 ? 
          (campaign.contract_price || 0) / campaign.metrics.total_time_seconds : 0;
        
        const engagementRate = campaign.views && campaign.views > 0 ?
          (((campaign.likes || 0) + (campaign.comments || 0)) / campaign.views) * 100 : 0;
        
        return [
          campaign.influencer || 'Unknown',
          campaign.platform || '',
          campaign.url || 'N/A',
          normalizeBrand(campaign.metrics?.brand || campaign.brand),
          campaign.contract_price || 0,
          engagementRate.toFixed(1) + '%',
          campaign.metrics?.total_time_seconds?.toFixed(1) || '0',
          costPerSecond.toFixed(3),
          campaign.compliance ? 'Compliant' : 'Non-compliant'
        ].join(',');
      })
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `campaigns-report-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="mt-12">
      <div className="p-8 bg-white rounded-card shadow-strong">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold font-montserrat text-petroleo-500">
            Recent Campaigns
          </h2>
          <button 
            onClick={handleExportData}
            disabled={filteredData.length === 0}
            className="flex items-center px-4 py-2 text-white transition-all duration-300 rounded-button bg-coral-gradient hover:shadow-coral disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Download className="w-4 h-4 mr-2" />
            Export Data
          </button>
        </div>
        
        {filteredData.length > 0 ? (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-humo-600">
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Influencer</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Platform</th>
                    <th className="hidden py-3 text-left font-montserrat text-petroleo-500 sm:table-cell">Video</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Brand</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Investment</th>
                    <th className="hidden py-3 text-left font-montserrat text-petroleo-500 md:table-cell">Engagement Rate</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Exposure Time</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Cost/Second</th>
                    <th className="py-3 text-left font-montserrat text-petroleo-500">Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  {currentData.map((campaign) => {
                    const costPerSecond = campaign.metrics && campaign.metrics.total_time_seconds > 0 ? 
                      (campaign.contract_price || 0) / campaign.metrics.total_time_seconds : 0;
                    
                    const engagementRate = campaign.views && campaign.views > 0 ?
                      (((campaign.likes || 0) + (campaign.comments || 0)) / campaign.views) * 100 : 0;
                    
                    return (
                      <tr key={campaign.id} className="border-b border-humo-200 hover:bg-humo-600">
                        <td className="py-4 font-medium font-source text-petroleo-500">
                          {campaign.influencer || 'Unknown'}
                        </td>
                        <td className="py-4 capitalize font-source text-petroleo-400">
                          {campaign.platform}
                        </td>
                        <td className="hidden py-4 sm:table-cell">
                          {campaign.url ? (
                            <button
                              onClick={() => window.open(campaign.url, '_blank', 'noopener,noreferrer')}
                              className="flex items-center px-2 py-1 text-xs transition-all duration-300 border rounded font-montserrat text-petroleo-500 border-petroleo-200 hover:bg-petroleo-500 hover:text-white"
                            >
                              <ExternalLink className="w-3 h-3 mr-1" />
                              View
                            </button>
                          ) : (
                            <span className="text-xs font-source text-petroleo-300">N/A</span>
                          )}
                        </td>
                        <td className="py-4 font-source text-petroleo-400">
                          {normalizeBrand(campaign.metrics?.brand || campaign.brand)}
                        </td>
                        <td className="py-4 font-source text-petroleo-400">
                          €{campaign.contract_price?.toLocaleString() || '0'}
                        </td>
                        <td className="hidden py-4 font-source text-petroleo-400 md:table-cell">
                          {engagementRate.toFixed(1)}%
                        </td>
                        <td className="py-4 font-source text-petroleo-400">
                          {campaign.metrics?.total_time_seconds?.toFixed(1) || '0'}s
                        </td>
                        <td className="py-4 font-source text-petroleo-400">
                          €{costPerSecond.toFixed(3)}/s
                        </td>
                        <td className="py-4">
                          <span className={`px-2 py-1 text-xs font-bold rounded-full font-montserrat ${
                            campaign.compliance ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {campaign.compliance ? 'Compliant' : 'Non-compliant'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Controles de paginación */}
            <div className="flex flex-col items-center justify-between mt-6 space-y-4 sm:flex-row sm:space-y-0">
              
              {/* Items info y selector de paginación */}
              <div className="flex items-center space-x-4">
                <span className="text-sm font-source text-petroleo-400">
                  Showing {startIndex + 1}-{Math.min(endIndex, totalItems)} of {totalItems} campaigns
                </span>
                
                <select
                  value={itemsPerPage}
                  onChange={(e) => handleItemsPerPageChange(parseInt(e.target.value))}
                  className="px-3 py-1 text-sm border rounded-button border-petroleo-200 font-source text-petroleo-500 focus:outline-none focus:border-coral-500"
                >
                  <option value={10}>10 per page</option>
                  <option value={25}>25 per page</option>
                  <option value={50}>50 per page</option>
                </select>
              </div>

              {/* Botones de paginación */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handlePreviousPage}
                  disabled={currentPage === 1}
                  className="flex items-center px-3 py-2 text-sm transition-all duration-300 border rounded-button border-petroleo-200 font-source text-petroleo-500 hover:bg-petroleo-500 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-petroleo-500"
                >
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Previous
                </button>
                
                <span className="px-4 py-2 text-sm font-medium font-source text-petroleo-500">
                  Page {currentPage} of {totalPages}
                </span>
                
                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className="flex items-center px-3 py-2 text-sm transition-all duration-300 border rounded-button border-petroleo-200 font-source text-petroleo-500 hover:bg-petroleo-500 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-petroleo-500"
                >
                  Next
                  <ChevronRight className="w-4 h-4 ml-1" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <h3 className="mb-2 text-lg font-bold font-montserrat text-petroleo-500">
              No Campaigns Found
            </h3>
            <p className="max-w-sm text-sm font-source text-petroleo-300">
              No campaigns match your current filters. Try adjusting your filter criteria to see more results.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecentCampaignsTable;