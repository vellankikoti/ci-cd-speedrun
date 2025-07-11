#!/bin/bash

echo "🚀 Setting up Chaos Engineering Workshop - Scenario 02"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Function to find an available port
find_available_port() {
    local port=8080
    local max_attempts=50
    
    echo "🔍 Looking for available port..."
    
    for i in $(seq 8080 8129); do
        if ! lsof -i :$i > /dev/null 2>&1; then
            echo "✅ Found available port: $i"
            return $i
        fi
    done
    
    echo "❌ No available ports found in range 8080-8129"
    exit 1
}

# Find available port
find_available_port
JENKINS_PORT=$?

echo "🌐 Jenkins will be exposed on port: $JENKINS_PORT"

# Build Jenkins image
echo "🔨 Building Jenkins Docker image..."
docker build -t jenkins-docker ./jenkins-docker

if [ $? -eq 0 ]; then
    echo "✅ Jenkins image built successfully"
else
    echo "❌ Failed to build Jenkins image"
    exit 1
fi

# Stop and remove existing Jenkins container if it exists
echo "🧹 Cleaning up existing Jenkins container..."
docker stop jenkins 2>/dev/null
docker rm jenkins 2>/dev/null

# Run Jenkins container with dynamic port
echo "🚀 Starting Jenkins container on port $JENKINS_PORT..."
docker run -d --name jenkins -p $JENKINS_PORT:8080 -v /var/run/docker.sock:/var/run/docker.sock jenkins-docker

if [ $? -eq 0 ]; then
    echo "✅ Jenkins container started successfully"
else
    echo "❌ Failed to start Jenkins container"
    exit 1
fi

# Wait for Jenkins to start
echo "⏳ Waiting for Jenkins to start..."
sleep 15

# Get the initial admin password
echo "🔑 Getting Jenkins initial admin password..."
PASSWORD=$(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null)

if [ -n "$PASSWORD" ]; then
    echo "✅ Jenkins is ready!"
    echo ""
    echo "🎯 NEXT STEPS:"
    echo "1. Open Jenkins: http://localhost:$JENKINS_PORT"
    echo "2. Initial admin password: $PASSWORD"
    echo "3. Install recommended plugins"
    echo "4. Create your user account"
    echo "5. Create a new Pipeline job named 'chaos-ci-pipeline'"
    echo "6. Copy the Jenkinsfile from pipeline/Jenkinsfile"
    echo "7. Select a chaos scenario and click 'Build Now'!"
    echo ""
    echo "🎭 Available Chaos Scenarios:"
    echo "   - chaos-full: Everything is broken!"
    echo "   - chaos-1: Network fixed, other issues remain"
    echo "   - chaos-2: Resources fixed, services broken"
    echo "   - chaos-3: Services fixed, database broken"
    echo "   - chaos-free: Perfect pipeline!"
    echo ""
    echo "🧹 To cleanup: ./cleanup.sh"
    echo ""
    echo "💡 Pro Tip: If you want to run multiple scenarios simultaneously,"
    echo "   each will automatically get its own port!"
else
    echo "❌ Could not get Jenkins password. Jenkins might still be starting..."
    echo "Please wait a moment and try: docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
fi 