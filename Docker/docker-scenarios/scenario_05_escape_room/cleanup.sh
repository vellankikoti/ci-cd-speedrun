#!/bin/bash

# Docker Escape Room Challenge - Cleanup Script
# Removes all Docker resources created during the game

echo "🧹 Cleaning up Docker Escape Room Challenge resources..."

# Stop and remove containers
echo "📦 Removing containers..."
docker rm -f redis-server flask-app memory-test container123 network-spy memory-victim secret-keeper 2>/dev/null || true

# Remove networks
echo "🌐 Removing networks..."
docker network rm networkA networkB 2>/dev/null || true

# Remove volumes
echo "💾 Removing volumes..."
docker volume rm vault-volume 2>/dev/null || true

# Remove images
echo "🖼️  Removing images..."
docker rmi escape-final suspicious-image 2>/dev/null || true

# Remove any other containers that might have been created
echo "🔍 Cleaning up any remaining containers..."
docker ps -a --filter "name=memory-test" --filter "name=redis-server" --filter "name=flask-app" --filter "name=container123" --filter "name=network-spy" --filter "name=memory-victim" --filter "name=secret-keeper" -q | xargs -r docker rm -f

# Clean up any dangling resources
echo "🧽 Cleaning up dangling resources..."
docker system prune -f

echo "✅ Cleanup complete!"
echo "🎉 All Docker Escape Room Challenge resources have been removed" 