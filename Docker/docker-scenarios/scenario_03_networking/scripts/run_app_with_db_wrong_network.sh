#!/bin/bash
set -e

# Remove any previous containers
docker rm -f vote-app redis-server 2>/dev/null || true

# Run Redis (default bridge network)
docker run -d --name redis-server redis:alpine

# Run Flask app, try to connect to redis-server by name (will fail)
docker run -d --name vote-app -p 5000:5000 -e REDIS_HOST=redis-server vote-app

echo "Open http://localhost:5000 and try voting. The app will crash (cannot resolve redis-server)!" 