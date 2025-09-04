# Dockerfile para Frontend (React/Vite)
FROM node:18-alpine as builder

# Build argument para la URL del backend
ARG VITE_API_BASE_URL=https://deportlogo.onrender.com

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar todas las dependencias
RUN npm install

# Copiar el código fuente
COPY . .

# Configurar variable de entorno para el build
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Construir la aplicación para producción
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:alpine

# Copiar la build de React al directorio de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx (opcional)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Comando por defecto de Nginx
CMD ["nginx", "-g", "daemon off;"]
