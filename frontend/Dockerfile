# Build stage
FROM node:20-alpine

# Set working directory
WORKDIR /usr/src/app

# Working directory is already set

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy project files
COPY . .

# Add development command with host flag for container access
ENV VITE_API_HOST=http://api:8000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173", "--strictPort"]