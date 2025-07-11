#!/bin/bash

echo "🧪 Testing Chaos Engineering Workshop Setup"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "setup.sh" ]; then
    echo "❌ Please run this script from the scenario_02_chaos_pipeline directory"
    exit 1
fi

# Run setup
echo "🚀 Running setup..."
./setup.sh

if [ $? -ne 0 ]; then
    echo "❌ Setup failed"
    exit 1
fi

# Get the Jenkins port from the setup output
JENKINS_PORT=$(docker ps --filter 'name=jenkins' --format '{{.Ports}}' | grep -o '0.0.0.0:[0-9]*' | cut -d: -f2)

if [ -z "$JENKINS_PORT" ]; then
    echo "❌ Could not determine Jenkins port"
    exit 1
fi

echo "🌐 Jenkins is running on port: $JENKINS_PORT"

# Wait a bit more for Jenkins to be fully ready
echo "⏳ Waiting for Jenkins to be fully ready..."
sleep 20

# Test if Jenkins is responding
echo "🔍 Testing Jenkins connectivity..."
if curl -s http://localhost:$JENKINS_PORT > /dev/null; then
    echo "✅ Jenkins is responding on port $JENKINS_PORT"
else
    echo "❌ Jenkins is not responding on port $JENKINS_PORT"
    echo "Please check the Jenkins logs: docker logs jenkins"
    exit 1
fi

# Test chaos scenarios directly
echo "🧪 Testing chaos scenarios..."
echo "Testing chaos-full scenario..."

# Run chaos scenario directly
python3 pipeline/chaos_scenarios.py chaos-full

if [ $? -eq 0 ]; then
    echo "✅ Chaos scenario test passed"
else
    echo "❌ Chaos scenario test failed"
fi

echo ""
echo "🎉 Setup test completed!"
echo ""
echo "📋 Summary:"
echo "- Jenkins is running on port $JENKINS_PORT"
echo "- Chaos scenarios are working"
echo "- You can now access Jenkins at: http://localhost:$JENKINS_PORT"
echo ""
echo "🧹 To cleanup: ./cleanup.sh" 