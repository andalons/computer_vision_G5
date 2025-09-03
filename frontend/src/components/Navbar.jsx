import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const location = useLocation();

  // Ocultar/mostrar navbar al desplazarse
  useEffect(() => {
    const controlNavbar = () => {
      if (typeof window !== 'undefined') {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
          setIsVisible(false);
        } else {
          setIsVisible(true);
        }
        setLastScrollY(window.scrollY);
      }
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', controlNavbar);
      return () => {
        window.removeEventListener('scroll', controlNavbar);
      };
    }
  }, [lastScrollY]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const navItems = [
    {
      name: 'Home',
      path: '/'
    },
    {
      name: 'Analysis',
      path: '/link-analysis'
    },
    {
      name: 'Reports',
      path: '/reports'
    }
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-transform duration-500 ease-out ${
        isVisible ? 'translate-y-0' : '-translate-y-full'
      }`}
    >
      {/* Contenedor de Navbar */}
      <div className="relative w-full overflow-hidden bg-humo-500/30 backdrop-blur-md">
        <div className="relative z-10 flex items-center justify-between h-24 px-6 mx-auto max-w-7xl lg:px-8">
          
          {/* Logotipo y navegación  */}
          <div className="flex items-center space-x-12">
            <Link to="/" className="flex items-center">
              <h1 className="text-3xl font-bold tracking-tight font-montserrat text-petroleo-500">
                LogoTracker
                <span className="ml-1 text-coral-500">Pro</span>
              </h1>
            </Link>

            {/* Enlaces de Navegación - Desktop */}
            <div className="items-center hidden space-x-2 lg:flex">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`font-source px-4 py-2 rounded-button transition-all duration-300 ${
                    location.pathname === item.path 
                      ? 'text-coral-500 font-semibold' 
                      : 'text-petroleo-300 hover:text-coral-500 font-medium'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>

          {/* Botones derecha - Desktop */}
          <div className="items-center hidden space-x-4 lg:flex">
            {/* Botón Login - Secundario */}
            <button className="px-5 py-2 text-base font-medium transition-all duration-300 border font-montserrat rounded-button text-petroleo-400 hover:text-lila-500 border-petroleo-200 hover:border-lila-400">
              Login
            </button>
            
            {/* Botón CTA - Principal */}
            <button className="px-5 py-2 text-base font-semibold text-white transition-all duration-300 font-montserrat rounded-button bg-coral-500 hover:bg-coral-400 hover:shadow-coral">
              Start Now
            </button>
          </div>

          {/* Controles de navegación móvil*/}
          <div className="flex items-center lg:hidden">
            {/* Menu toggle button */}
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-3 transition-colors duration-300 text-petroleo-300 rounded-button focus:outline-none"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <div className="relative flex items-center justify-center w-6 h-6">
                <span 
                  className={`absolute h-0.5 w-5 bg-current transition-all duration-400 ${
                    isMenuOpen ? 'rotate-45' : '-translate-y-1.5'
                  }`}
                ></span>
                <span 
                  className={`absolute h-0.5 w-5 bg-current transition-all duration-400 ${
                    isMenuOpen ? 'opacity-0' : 'opacity-100'
                  }`}
                ></span>
                <span 
                  className={`absolute h-0.5 w-5 bg-current transition-all duration-400 ${
                    isMenuOpen ? '-rotate-45' : 'translate-y-1.5'
                  }`}
                ></span>
              </div>
            </button>
          </div>
        </div>

        {/* Menú desplegable móvil */}
        <div className={`transition-all duration-500 ease-out overflow-hidden lg:hidden ${
          isMenuOpen 
            ? 'max-h-screen opacity-100' 
            : 'max-h-0 opacity-0'
        }`}>
          <div className="flex flex-col px-6 py-6 border-t bg-humo-400/95 backdrop-blur-xl border-petroleo-200/20">
            {navItems.map((item, index) => (
              <div key={item.name}>
                <Link
                  to={item.path}
                  onClick={closeMenu}
                  className={`flex items-center justify-center h-12 font-source px-6 rounded-button transition-all duration-300 ${
                    location.pathname === item.path 
                      ? 'text-coral-500 font-semibold' 
                      : 'text-petroleo-300 hover:text-coral-500 font-medium'
                  }`}
                >
                  {item.name}
                </Link>
                {index < navItems.length - 1 && (
                  <div className="w-full h-px my-2 bg-petroleo-200/20"></div>
                )}
              </div>
            ))}
            
            {/* Botones móvil */}
            <div className="flex flex-col pt-6 mt-6 space-y-3 border-t border-petroleo-200/20">
              <button 
                onClick={closeMenu}
                className="px-5 py-3 text-base font-medium transition-all duration-300 border font-montserrat rounded-button text-petroleo-400 hover:text-lila-500 border-petroleo-200 hover:border-lila-400"
              >
                Login
              </button>
              <button 
                onClick={closeMenu}
                className="px-5 py-3 text-base font-semibold text-white transition-all duration-300 font-montserrat rounded-button bg-coral-500 hover:bg-coral-400"
              >
                Start Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;