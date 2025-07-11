#!/bin/bash

# Puzzle 3: The Memory Detective
# Dr. NullPointer has created a container with a specific memory limit

echo "💾 Setting up Puzzle 3: The Memory Detective"
echo "Dr. NullPointer is creating a memory-limited container..."

# Clean up any existing container
docker rm -f memory-victim 2>/dev/null || true

# Create a container with a specific memory limit
docker run -d --name memory-victim \
  --memory=10m \
  busybox sh -c "
echo 'I am a memory-limited container...'
echo 'My memory limit is set to 10MB'
echo 'Use docker inspect to find my exact memory limit!'
sleep infinity
"

echo "✅ Puzzle 3 setup complete!"
echo "📝 Container 'memory-victim' is running with a specific memory limit"
echo "💡 Use: docker inspect memory-victim | grep -i memory"
echo "💡 Find the memory limit in MB and submit it" 