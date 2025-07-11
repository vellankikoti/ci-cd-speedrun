#!/bin/bash
set -e

# Cleanup
docker rm -f vote-app redis-server 2>/dev/null || true
docker network rm vote-net 2>/dev/null || true

# Create custom network
docker network create vote-net

# Run Redis in custom network
docker run -d --name redis-server --network vote-net redis:alpine

# Build Flask app image
docker build -t vote-app ./app

# Run Flask app in same network
docker run -d --name vote-app --network vote-net -p 5000:5000 -e REDIS_HOST=redis-server vote-app

echo "Vote app is live at http://localhost:5000 (votes will work now!)" 