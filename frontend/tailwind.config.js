/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Fuentes 
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'], // Headers, CTA, KPIs
        'source': ['Source Sans Pro', 'sans-serif'], // Cuerpo, dashboards, párrafos
      },
      // Paleta de colores 
      colors: {
        // Coral intenso - CTA principal y acento
        'coral': {
          500: '#FF6F61', // Color principal - botones CTA, alertas
          600: '#E55A4C', // Hover states (10% más oscuro)
          400: '#FF8577', // Hover states más claro
          300: '#FF9B92', // Variante suave
        },
        // Lila futurista
        'lila': {
          500: '#6C63FF', // Color principal - botones secundarios, líneas
          600: '#5951E6', // Hover states
          400: '#8379FF', // Variante más clara
          300: '#A09CFF', // Para estados disabled
        },
        // Amarillo mostaza - Calidez y métricas positivas
        'mostaza': {
          500: '#F9A826', // Color principal - KPIs, barras positivas
          600: '#E0971F', // Hover states
          400: '#FAB647', // Variante más clara
          300: '#FCC668', // Para backgrounds suaves
        },
        // Azul petróleo - Fondo oscuro
        'petroleo': {
          500: '#264653', // Color principal - texto, fondos oscuros
          600: '#1E3A44', // Variante más oscura
          400: '#2F5562', // Variante más clara
          300: '#4A6B78', // Para texto secundario (70% opacity equivalent)
          200: '#7A9CAA', // Para bordes y elementos sutiles
        },
        // Blanco humo - Base clara
        'humo': {
          500: '#F1F1F1', // Fondo principal
          400: '#F4F4F4', // Variante más clara para cards
          600: '#EEEEEE', // Variante más oscura para contraste sutil
          300: '#F7F7F7', // Para highlights muy suaves
        },
      },
      // Espaciado y dimensiones
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      // Shadows 
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(38, 70, 83, 0.1), 0 4px 6px -2px rgba(38, 70, 83, 0.05)',
        'medium': '0 10px 25px -5px rgba(38, 70, 83, 0.15), 0 4px 6px -2px rgba(38, 70, 83, 0.05)',
        'strong': '0 20px 40px -12px rgba(38, 70, 83, 0.25)',
        'coral': '0 10px 25px -5px rgba(255, 111, 97, 0.25)',
        'lila': '0 10px 25px -5px rgba(108, 99, 255, 0.25)',
      },
      // Border radius 
      borderRadius: {
        'card': '12px',
        'button': '8px',
      },
      // Gradientes
      backgroundImage: {
        'coral-gradient': 'linear-gradient(135deg, #FF6F61 0%, #FF8577 100%)',
        'lila-gradient': 'linear-gradient(135deg, #6C63FF 0%, #8379FF 100%)',
        'mostaza-gradient': 'linear-gradient(135deg, #F9A826 0%, #FAB647 100%)',
        'petroleo-gradient': 'linear-gradient(135deg, #264653 0%, #2F5562 100%)',
      },
    },
  },
  plugins: [],
}