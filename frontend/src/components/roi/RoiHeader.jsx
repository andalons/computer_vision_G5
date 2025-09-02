import React from 'react';

const RoiHeader = ({ filters, metrics, onFilteredDataChange }) => {
  // Normalización de marcas
  const normalizeBrand = (brand) => {
    if (!brand) return 'Adidas';
    const lowerBrand = brand.toLowerCase();
    if (lowerBrand.includes('adidas')) return 'Adidas';
    if (lowerBrand.includes('nike')) return 'Nike';
    return brand;
  };

  const applyFilters = (newFilters) => {
    let filtered = [...metrics];

    if (newFilters.platform !== 'all') {
      filtered = filtered.filter(item => item.platform === newFilters.platform);
    }

    if (newFilters.compliance !== 'all') {
      const isCompliant = newFilters.compliance === 'compliant';
      filtered = filtered.filter(item => item.compliance === isCompliant);
    }

    if (newFilters.brand !== 'all') {
      filtered = filtered.filter(item => {
        const itemBrand = normalizeBrand(item.metrics?.brand || item.brand);
        return itemBrand === newFilters.brand;
      });
    }

    // Notificar al padre con los datos filtrados
    onFilteredDataChange(filtered, newFilters);
  };

  return (
    <div className="flex flex-col items-start justify-between mb-12 lg:flex-row lg:items-center">
      <div className="mb-6 lg:mb-0">
        <h1 className="mb-4 text-5xl font-bold font-montserrat text-petroleo-500">
          ROI Dashboard
        </h1>
        <p className="text-xl font-source text-petroleo-300">
          Comprehensive analysis of brand collaboration performance and return on investment
        </p>
      </div>
      
      {/* Filtros */}
      <div className="flex flex-wrap gap-4">
        <select
          value={filters.platform}
          onChange={(e) => applyFilters({...filters, platform: e.target.value})}
          className="px-4 py-2 border-2 rounded-button border-petroleo-200 font-source text-petroleo-500 focus:outline-none focus:border-coral-500"
        >
          <option value="all">All Platforms</option>
          <option value="youtube">YouTube</option>
          <option value="tiktok">TikTok</option>
        </select>
        
        <select
          value={filters.compliance}
          onChange={(e) => applyFilters({...filters, compliance: e.target.value})}
          className="px-4 py-2 border-2 rounded-button border-petroleo-200 font-source text-petroleo-500 focus:outline-none focus:border-coral-500"
        >
          <option value="all">All Status</option>
          <option value="compliant">Compliant</option>
          <option value="non-compliant">Non-Compliant</option>
        </select>

        <select
          value={filters.brand}
          onChange={(e) => applyFilters({...filters, brand: e.target.value})}
          className="px-4 py-2 border-2 rounded-button border-petroleo-200 font-source text-petroleo-500 focus:outline-none focus:border-coral-500"
        >
          <option value="all">All Brands</option>
          <option value="Adidas">Adidas</option>
          <option value="Nike">Nike</option>
        </select>
      </div>
    </div>
  );
};

export default RoiHeader;