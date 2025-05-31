# Build stage
FROM node:18-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy project files
COPY . .

# Add development command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]