# 1) Build React app
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Fix Ajv versions for CRA
RUN npm install ajv@^6 ajv-keywords@^3 --legacy-peer-deps

COPY . .

# Build React app
RUN npm run build

# 2) Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
