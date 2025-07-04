#!/bin/bash

# Set image and container names
IMAGE_NAME=prstats-backend
CONTAINER_NAME=prstats-backend-container

# Build the Docker image
echo "🔧 Building Docker image..."
docker build -t $IMAGE_NAME .

# Stop and remove existing container if it exists
echo "🧹 Cleaning up old container (if any)..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Run the Docker container
echo "Running Docker container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  $IMAGE_NAME
