import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const solutions = [
    { name: 'Brand Detection', path: '#' },
    { name: 'Campaign Analytics', path: '#' },
    { name: 'Reports', path: '#' },
    { name: 'API Access', path: '#' }
  ];

  const legal = [
    { name: 'Privacy Policy', path: '#' },
    { name: 'Terms of Service', path: '#' },
    { name: 'Copyright', path: '#' },
    { name: 'Data Protection', path: '#' }
  ];

  const enterprise = [
    { name: 'For Agencies', path: '#' },
    { name: 'Enterprise Plan', path: '#' },
    { name: 'White Label', path: '#' },
    { name: 'Contact Sales', path: '#' }
  ];

  const supportedLogos = ['Nike', 'Adidas'];

  return (
    <footer className="mt-auto text-white bg-petroleo-500">
      <div className="px-6 py-16 mx-auto max-w-7xl lg:px-8">
        
        {/* Contenedor principal footer  */}
        <div className="flex flex-col mb-12 lg:flex-row lg:justify-between">
          
          {/* Sección izquierda  */}
          <div className="mb-8 lg:mb-0 lg:mr-16"> 
            <Link to="/" className="flex items-center mb-6">
              <h2 className="text-3xl font-bold text-white font-montserrat">
                LogoTracker
                <span className="ml-1 text-coral-500">Pro</span>
              </h2>
            </Link>
            
            <p className="max-w-md mb-8 text-lg leading-relaxed text-petroleo-200 font-source">
              AI-powered logo detection for influencer marketing campaigns. Measure brand exposure with 93% recall in minutes, not hours
            </p>

            {/* Logos soportados */}
            <div className="pt-6 border-t border-petroleo-400">
              <p className="mb-3 text-sm font-source text-petroleo-200">Currently detecting:</p>
              <div className="flex flex-wrap gap-2">
                {supportedLogos.map((logo, index) => (
                  <span key={index} className="px-3 py-1 text-xs font-medium text-white rounded-full bg-petroleo-400">
                    {logo}
                  </span>
                ))}
                <span className="px-3 py-1 text-xs font-medium text-white rounded-full bg-lila-500">
                  More brands soon
                </span>
              </div>
            </div>
          </div>

          {/* Contenedor de las tres columnas */}
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-3 lg:justify-end md:gap-32">
            
            {/* Columna de soluciones */}
            <div className="text-left">
              <h3 className="mb-6 text-lg font-semibold text-white font-montserrat">
                Solutions
              </h3>
              <ul className="space-y-4">
                {solutions.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.path}
                      className="text-base transition-colors duration-300 font-source text-petroleo-200 hover:text-coral-500"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Columna de legal */}
            <div className="text-left">
              <h3 className="mb-6 text-lg font-semibold text-white font-montserrat">
                Legal
              </h3>
              <ul className="space-y-4">
                {legal.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.path}
                      className="text-base transition-colors duration-300 font-source text-petroleo-200 hover:text-coral-500"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Columna de empresas */}
            <div className="text-left">
              <h3 className="mb-6 text-lg font-semibold text-white font-montserrat">
                Enterprise
              </h3>
              <ul className="space-y-4">
                {enterprise.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.path}
                      className="text-base transition-colors duration-300 font-source text-petroleo-200 hover:text-coral-500"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>

        {/* Sección bottom */}
        <div className="pt-8 border-t border-petroleo-400">
          <div className="flex flex-col items-center justify-between gap-6 text-center lg:flex-row lg:text-left">
            <div className="flex flex-col lg:flex-row lg:items-center lg:space-x-8">
              <p className="mb-4 text-sm font-source text-petroleo-200 lg:mb-0">
                © {currentYear} LogoTracker Pro. Built for agencies who demand precision
              </p>
              <div className="flex items-center justify-center space-x-6 text-xs lg:justify-start text-petroleo-300">
                <Link to="#" className="transition-colors duration-300 hover:text-coral-500">Privacy</Link>
                <Link to="#" className="transition-colors duration-300 hover:text-coral-500">Terms</Link>
                <Link to="#" className="transition-colors duration-300 hover:text-coral-500">Security</Link>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-mostaza-500 animate-pulse"></div>
                <span className="text-sm font-source text-mostaza-500">AI System Online</span>
              </div>
              <span className="text-xs font-source text-petroleo-300">Powered by Computer Vision</span>
            </div>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;