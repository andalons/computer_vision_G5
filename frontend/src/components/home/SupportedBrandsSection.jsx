import React from 'react';
import nikelogo from '../../assets/logos/nike.png';
import adidaslogo from '../../assets/logos/adidas.png';
import asicslogo from '../../assets/logos/asics.png';
import newbalancelogo from '../../assets/logos/new-balance.png';

const SupportedBrandsSection = () => {
  const supportedBrands = [
    { name: 'Nike', logo: nikelogo },
    { name: 'Adidas', logo: adidaslogo },
    { name: 'Asics', logo: asicslogo },
    { name: 'New Balance', logo: newbalancelogo }
  ];

  return (
    <div className="w-full py-16 overflow-hidden bg-humo-600">
      <div className="px-6 mx-auto mb-8 text-center max-w-7xl lg:px-8">
        <h2 className="mb-4 text-2xl font-bold font-montserrat text-petroleo-500">
          Currently Detecting
        </h2>
        <p className="font-source text-petroleo-300">
          Specialized AI models trained for these major athletic brands
        </p>
      </div>
      
      {/* Full widht para movimiento infinito */}
      <div className="relative w-screen left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] overflow-hidden">
        <div className="flex animate-slide-infinite">
          {/*  Búcle de logos infinitos */}
          {Array(4).fill(supportedBrands).flat().map((brand, index) => (
            <div key={index} className="flex items-center justify-center flex-shrink-0 h-32 p-6 mx-3 bg-white sm:h-40 w-72 sm:w-96 sm:mx-6 rounded-card shadow-soft">
              <img
                src={brand.logo}
                alt={`${brand.name} logo`}
                className="object-contain w-24 h-24 max-w-full max-h-full sm:w-32 sm:h-32"
              />
            </div>
          ))}
        </div>
      </div>
      
      <div className="mt-8 text-center">
        <span className="inline-flex items-center px-6 py-3 text-sm font-medium text-white rounded-full bg-lila-500 font-source">
          More brands coming soon
        </span>
      </div>

      {/* Animaciones CSS */}
      <style jsx>{`
        @keyframes slide-infinite {
          0% {
            transform: translateX(0);
          }
          100% {
            transform: translateX(-25%);
          }
        }
        
        .animate-slide-infinite {
          animation: slide-infinite 25s linear infinite;
          width: 400%;
        }

        .animate-slide-infinite:hover {
          animation-play-state: paused;
        }
      `}</style>
    </div>
  );
};

export default SupportedBrandsSection;