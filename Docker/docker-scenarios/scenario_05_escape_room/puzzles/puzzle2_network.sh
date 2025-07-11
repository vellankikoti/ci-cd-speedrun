#!/bin/bash

# Puzzle 2: The Network Detective
# Dr. NullPointer has created a mysterious container with a specific IP

echo "🌐 Setting up Puzzle 2: The Network Detective"
echo "Dr. NullPointer is creating a mysterious container..."

# Clean up any existing container
docker rm -f network-spy 2>/dev/null || true

# Create a container with a specific name that will get a predictable IP
docker run -d --name network-spy \
  --network bridge \
  busybox sh -c "
echo 'I am a spy container with a secret IP address...'
echo 'Use docker inspect to find my IP!'
sleep infinity
"

echo "✅ Puzzle 2 setup complete!"
echo "📝 Container 'network-spy' is running with a specific IP address"
echo "💡 Use: docker inspect network-spy | grep IPAddress"
echo "💡 Find the IP address and submit it" 