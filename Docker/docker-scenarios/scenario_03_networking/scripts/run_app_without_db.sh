#!/bin/bash
set -e

# Build the Flask app image
docker build -t vote-app ./app

# Remove any previous container
docker rm -f vote-app 2>/dev/null || true

# Run Flask app (no Redis)
docker run -d --name vote-app -p 5000:5000 vote-app

echo "Open http://localhost:5000 and try voting. The app will crash on vote (no Redis)!" 