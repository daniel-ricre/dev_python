# Usar una imagen ligera de Node.js
FROM node:20-alpine

# Crear el directorio de trabajo
WORKDIR /app

# Instalar git para clonar el repositorio
RUN apk add --no-cache git

# Clonar el repositorio de X402 Facilitator
RUN git clone https://github.com/coinbase/x402-facilitator.git .

# Instalar las dependencias del proyecto
RUN npm install

# Construir la aplicación (si es necesario, como con TypeScript)
RUN npm run build

# Exponer el puerto que usa la aplicación (5555 por defecto)
EXPOSE 5555

# Comando para iniciar la aplicación
CMD ["npm", "start"]
