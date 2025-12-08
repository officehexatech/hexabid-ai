# ===============================
#  FRONTEND DOCKERFILE (FIXED)
# ===============================

FROM node:16-alpine AS build
WORKDIR /app

# Fast registry
RUN npm config set registry https://registry.npmmirror.com

# Copy package files
COPY package.json package-lock.json* ./

# FIX AJV ISSUES (FOR CRA + CRACO)
RUN npm install ajv@6 ajv-keywords@3 --legacy-peer-deps

# Install app dependencies
RUN npm install --legacy-peer-deps

# Copy everything
COPY . .

# Inject API URL
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Build React app
RUN npm run build

# ===============================
#  NGINX STATIC SERVER
# ===============================
FROM nginx:1.25-alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
