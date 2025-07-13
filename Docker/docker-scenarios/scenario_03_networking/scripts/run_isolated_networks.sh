#!/bin/bash
set -e

# Clean up any previous containers and networks
docker rm -f vote-app redis-server 2>/dev/null || true
docker network rm vote-net1 vote-net2 2>/dev/null || true

# Create two isolated networks
docker network create vote-net1
docker network create vote-net2

# Run Redis in vote-net1
docker run -d --name redis-server --network vote-net1 redis:alpine

# Build the Flask app image (if not already built)
docker build -t vote-app ./app

# Run the app in vote-net2, publish the port for demonstration
docker run -d --name vote-app --network vote-net2 -p 5000:5000 -e REDIS_HOST=redis-server vote-app

echo "App and Redis are running on different Docker networks (vote-net1 and vote-net2)."
echo "The app will fail to connect to Redis, demonstrating Docker network isolation." 