/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Fuentes personalizadas
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'archivo': ['Archivo', 'sans-serif'],
      },
      // Paleta de colores
      colors: {
        // Steel Gray - Para textos y elementos principales
        'steel': {
          100: '#f1eff2',    // Fondos muy suaves
          700: '#665466',    // Textos secundarios
          900: '#2E293D',    // Textos principales, navbar
        },
        // Curious Blue - Para botones y elementos interactivos
        'curious': {
          500: '#27A3D4',    // Color principal - botones, links
          600: '#1e8bb8',    // Hover states
        },
        // Geraldine - Para CTAs importantes y alertas
        'geraldine': {
          500: '#F89183',    // Color principal - CTAs, alertas
          600: '#f5735f',    // Hover states
        },
        // Wafer - Para fondos neutros
        'wafer': {
          500: '#E5D7D7',    // Fondos neutros, cards
        },
      },
    },
  },
  plugins: [],
}