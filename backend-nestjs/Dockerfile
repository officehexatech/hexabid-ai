FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production=false

# Copy full project
COPY . .

# Build NestJS for production
RUN npm run build

EXPOSE 3000

# Start production build
CMD ["npm", "run", "start:prod"]
