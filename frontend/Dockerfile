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
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]