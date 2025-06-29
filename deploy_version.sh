#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "❌ Please provide a version number. Example:"
    echo "    ./deploy_version.sh 2"
    exit 1
fi

echo "👉 Switching to version $VERSION"

# Replace main.py
cp app/main_v${VERSION}.py app/main.py

# Check if container exists
CONTAINER_NAME="chaos-app-v${VERSION}"

# Find running container on port 3000
PORT_IN_USE=$(docker ps --filter "publish=3000" --format "{{.ID}}")

if [ ! -z "$PORT_IN_USE" ]; then
    echo "⚠️  A container is running on port 3000. Stopping and removing it..."
    docker stop $PORT_IN_USE
    docker rm $PORT_IN_USE
fi

# Remove previous same-named container if any
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "🔨 Building Docker image..."
docker build -t ci-cd-chaos-app:v${VERSION} .

echo "🚀 Running container chaos-app-v${VERSION}..."
docker run -d -p 3000:3000 --name $CONTAINER_NAME ci-cd-chaos-app:v${VERSION}

# Run Docker analysis script automatically
echo "📊 Generating Docker analysis report..."
python3 workshop_tools/docker_analysis.py $VERSION

echo "✅ Deployment complete for version $VERSION!"
echo "👉 View the Docker report here: reports/version_${VERSION}/docker_report.html"
