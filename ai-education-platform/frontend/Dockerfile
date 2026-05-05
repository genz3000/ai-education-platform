# syntax=docker/dockerfile:1

# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# No build needed for placeholder

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]