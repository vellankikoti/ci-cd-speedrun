#!/bin/bash
set -e

# Clean up any previous containers and network
docker rm -f vote-app redis-server 2>/dev/null || true
docker network rm vote-net 2>/dev/null || true

# Create a custom network
docker network create vote-net

# Run Redis in the custom network
docker run -d --name redis-server --network vote-net redis:alpine

# Build the Flask app image (if not already built)
docker build -t vote-app ./app

# Run the app in the same network, but DO NOT publish the port
docker run -d --name vote-app --network vote-net -e REDIS_HOST=redis-server vote-app

echo "App and Redis are running on the same Docker network, but the app's port is NOT published to the host."
echo "You cannot access http://localhost:5000 from your browser, but the app and Redis can communicate internally." 