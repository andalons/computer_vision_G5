import React, { useState, useImperativeHandle, forwardRef } from 'react';
import { Upload } from 'lucide-react';

const FormInput = forwardRef((props, ref) => {
  const [formData, setFormData] = useState({
    url: '',
    brand: '',
    contract_price: '',
    min_brand_time: ''
  });
  
  const [fieldErrors, setFieldErrors] = useState({});

  const validateField = (name, value) => {
    const errors = {};
    
    switch (name) {
      case 'url':
        if (!value.trim()) {
          errors.url = 'Video URL is required';
        } else if (!value.match(/^https?:\/\/.+/)) {
          errors.url = 'Please enter a valid URL';
        }
        break;
      case 'brand':
        if (!value.trim()) {
          errors.brand = 'Please select a brand to detect';
        }
        break;
      case 'contract_price':
        if (!value.trim()) {
          errors.contract_price = 'Contract price is required';
        } else if (isNaN(value) || parseFloat(value) <= 0) {
          errors.contract_price = 'Please enter a valid amount';
        }
        break;
      case 'min_brand_time':
        if (!value.trim()) {
          errors.min_brand_time = 'Minimum time is required';
        } else if (isNaN(value) || parseInt(value) <= 0) {
          errors.min_brand_time = 'Please enter a valid duration';
        }
        break;
    }
    
    return errors;
  };

  const validateForm = () => {
    const requiredFields = ['url', 'brand', 'contract_price', 'min_brand_time'];
    let errors = {};
    
    requiredFields.forEach(field => {
      const fieldErrors = validateField(field, formData[field]);
      errors = { ...errors, ...fieldErrors };
    });
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  useImperativeHandle(ref, () => ({
    validateForm,
    getFormData: () => formData,
    resetForm: () => {
      setFormData({
        url: '',
        brand: '',
        contract_price: '',
        min_brand_time: ''
      });
      setFieldErrors({});
    }
  }));

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (fieldErrors[name]) {
      setFieldErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  return (
    <>
      {/* Input para la URL del video */}
      <div className="mb-12">
        <div className="flex items-center mb-6">
          <div className="flex items-center justify-center w-12 h-12 mr-4 rounded-card bg-coral-500/10">
            <Upload className="w-6 h-6 text-coral-500" />
          </div>
          <label className="text-2xl font-bold font-montserrat text-petroleo-500">
            Collaboration Video Link
          </label>
        </div>
        <input
          type="url"
          name="url"
          value={formData.url}
          onChange={handleInputChange}
          placeholder="Insert the link to your brand collaboration video"
          className={`w-full px-8 py-6 text-xl transition-all duration-300 border-2 rounded-card font-source text-petroleo-500 placeholder-petroleo-300 focus:outline-none focus:ring-0 ${
            fieldErrors.url 
              ? 'border-coral-500 focus:border-coral-600' 
              : 'border-petroleo-200 focus:border-coral-500 focus:shadow-coral'
          }`}
        />
        {fieldErrors.url && (
          <p className="mt-2 text-sm font-medium font-source text-coral-500">{fieldErrors.url}</p>
        )}
        <div className="flex items-center mt-4">
          <div className="w-2 h-2 mr-3 rounded-full bg-mostaza-500"></div>
          <p className="text-lg font-source text-petroleo-300">
            We support videos from YouTube and TikTok
          </p>
        </div>
      </div>

      {/* Sección de marca, contrato y requisitos */}
      <div className="grid grid-cols-1 gap-12 mb-12 lg:grid-cols-3">
        
        {/* Selección de marca */}
        <div className="p-8 rounded-card bg-gradient-to-br from-humo-600 to-humo-400">
          <label className="block mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
            Brand to Detect 
          </label>
          <select
            name="brand"
            value={formData.brand}
            onChange={handleInputChange}
            className={`w-full px-6 py-4 text-xl transition-all duration-300 border-2 rounded-card font-source text-petroleo-500 focus:outline-none focus:ring-0 ${
              fieldErrors.brand 
                ? 'border-coral-500 focus:border-coral-600' 
                : 'border-transparent focus:border-lila-500 focus:shadow-lila'
            }`}
          >
            <option value="">Select a brand to detect</option>
            <option value="Nike">Nike</option>
            <option value="Adidas">Adidas</option>
          </select>
          {fieldErrors.brand && (
            <p className="mt-2 text-sm font-medium font-source text-coral-500">{fieldErrors.brand}</p>
          )}
        </div>

        {/* Precio del contrato */}
        <div className="p-8 rounded-card bg-gradient-to-br from-humo-600 to-humo-400">
          <label className="block mb-6 text-2xl font-bold font-montserrat text-petroleo-500">
            Contract Value 
          </label>
          <div className="relative">
            <span className="absolute text-xl transform -translate-y-1/2 left-6 top-1/2 font-source text-petroleo-400">€</span>
            <input
              type="number"
              name="contract_price"
              value={formData.contract_price}
              onChange={handleInputChange}
              placeholder="Enter contract amount"
              className={`w-full py-4 pl-12 pr-6 text-xl transition-all duration-300 border-2 rounded-card font-source text-petroleo-500 placeholder-petroleo-300 focus:outline-none focus:ring-0 ${
                fieldErrors.contract_price 
                  ? 'border-coral-500 focus:border-coral-600' 
                  : 'border-transparent focus:border-mostaza-500 focus:shadow-medium'
              }`}
            />
          </div>
          {fieldErrors.contract_price && (
            <p className="mt-2 text-sm font-medium font-source text-coral-500">{fieldErrors.contract_price}</p>
          )}
        </div>

        {/* Tiempo mínimo de exposición del logo */}
        <div className="p-8 rounded-card bg-gradient-to-br from-petroleo-500 to-petroleo-600 shadow-strong">
          <label className="block mb-6 text-2xl font-bold text-white font-montserrat">
            Minimum Brand Time 
          </label>
          <div className="relative">
            <input
              type="number"
              name="min_brand_time"
              value={formData.min_brand_time}
              onChange={handleInputChange}
              placeholder="Enter min. seconds"
              className={`w-full px-6 py-4 pr-14 text-xl transition-all duration-300 bg-white border-2 rounded-card font-source text-petroleo-500 placeholder-petroleo-300 focus:outline-none focus:ring-0 ${
                fieldErrors.min_brand_time 
                  ? 'border-coral-500 focus:border-coral-600' 
                  : 'border-transparent focus:border-coral-500 focus:shadow-coral'
              }`}
            />
            <span className="absolute text-xl transform -translate-y-1/2 right-4 top-1/2 font-source text-petroleo-500">sec</span>
          </div>
          {fieldErrors.min_brand_time && (
            <p className="mt-2 text-sm font-medium text-coral-300">{fieldErrors.min_brand_time}</p>
          )}
        </div>
      </div>
    </>
  );  
});

export default FormInput;