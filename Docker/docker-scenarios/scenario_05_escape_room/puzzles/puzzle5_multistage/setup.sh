#!/bin/bash

# Puzzle 5: The Image Sleuth
# Dr. NullPointer has created a suspicious image with a specific size

echo "🖼️  Setting up Puzzle 5: The Image Sleuth"
echo "Dr. NullPointer is creating a suspicious image..."

# Clean up any existing image
docker rmi suspicious-image 2>/dev/null || true

# Create a suspicious image with a specific size
docker build -t suspicious-image - << 'EOF'
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
    python3 \
    && rm -rf /var/lib/apt/lists/*
RUN echo "This is a suspicious image with a specific size..." > /suspicious.txt
CMD ["sleep", "infinity"]
EOF

echo "✅ Puzzle 5 setup complete!"
echo "📝 Image 'suspicious-image' has been created with a specific size"
echo "💡 Use: docker images suspicious-image"
echo "💡 Find the exact size in MB and submit it" 