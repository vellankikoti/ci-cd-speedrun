#!/bin/bash
set -e

# Remove any previous container
docker rm -f vote-app 2>/dev/null || true

# Run Flask app with port publishing
# This demonstrates how -p 5000:5000 makes the app accessible from your host

docker run -d --name vote-app -p 5000:5000 vote-app

echo "The app is running and accessible from your host at http://localhost:5000. Try voting!"
echo "This demonstrates Docker's port publishing (-p) feature." 