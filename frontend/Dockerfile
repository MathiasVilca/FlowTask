#Primera etapa: Build de angular (usamos imagen node)
FROM node:22-alpine AS build 

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

#Segunda Etapa: Servidor web usando nginx
FROM nginx:alpine

#Copia la salida compilada de Angular
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]