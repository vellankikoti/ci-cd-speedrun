#!/bin/bash
# Test script to verify port detection logic

echo "🔍 Testing port detection logic..."
echo ""

# Function to check if port is available
check_port() {
    local port=$1
    local available=true
    
    # Check netstat
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo "   • Port $port in use by netstat"
        available=false
    fi
    
    # Check ss
    if ss -tuln 2>/dev/null | grep -q ":$port "; then
        echo "   • Port $port in use by ss"
        available=false
    fi
    
    # Check lsof
    if lsof -i :$port 2>/dev/null | grep -q LISTEN; then
        echo "   • Port $port in use by lsof"
        available=false
    fi
    
    # Check Docker
    if docker ps --format "{{.Ports}}" 2>/dev/null | grep -q ":$port->"; then
        echo "   • Port $port in use by Docker"
        available=false
    fi
    
    if [ "$available" = true ]; then
        echo "   ✅ Port $port is available"
        return 0
    else
        echo "   ❌ Port $port is not available"
        return 1
    fi
}

# Test the port finding logic from the Jenkinsfile
echo "Testing port finding logic (like in Jenkinsfile):"
WEBAPP_PORT=8081
MAX_ATTEMPTS=10
ATTEMPTS=0

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    echo "Checking port $WEBAPP_PORT..."
    
    # Check if port is in use by netstat
    if netstat -tuln 2>/dev/null | grep -q ":$WEBAPP_PORT "; then
        echo "   • Port $WEBAPP_PORT in use by netstat, trying next..."
        WEBAPP_PORT=$((WEBAPP_PORT + 1))
        ATTEMPTS=$((ATTEMPTS + 1))
        continue
    fi
    
    # Check if port is in use by ss command
    if ss -tuln 2>/dev/null | grep -q ":$WEBAPP_PORT "; then
        echo "   • Port $WEBAPP_PORT in use by ss, trying next..."
        WEBAPP_PORT=$((WEBAPP_PORT + 1))
        ATTEMPTS=$((ATTEMPTS + 1))
        continue
    fi
    
    # Check if port is in use by lsof
    if lsof -i :$WEBAPP_PORT 2>/dev/null | grep -q LISTEN; then
        echo "   • Port $WEBAPP_PORT in use by lsof, trying next..."
        WEBAPP_PORT=$((WEBAPP_PORT + 1))
        ATTEMPTS=$((ATTEMPTS + 1))
        continue
    fi
    
    # Check if port is in use by Docker containers
    if docker ps --format "{{.Ports}}" 2>/dev/null | grep -q ":$WEBAPP_PORT->"; then
        echo "   • Port $WEBAPP_PORT in use by Docker, trying next..."
        WEBAPP_PORT=$((WEBAPP_PORT + 1))
        ATTEMPTS=$((ATTEMPTS + 1))
        continue
    fi
    
    # Port is available
    echo "   ✅ Found available port: $WEBAPP_PORT"
    break
done

if [ $ATTEMPTS -ge $MAX_ATTEMPTS ]; then
    echo "   ❌ Could not find available port after $MAX_ATTEMPTS attempts"
    exit 1
fi

echo ""
echo "Current port usage:"
echo "netstat:"
netstat -tuln 2>/dev/null | grep ":808" || echo "  No ports 808x in use"
echo ""
echo "ss:"
ss -tuln 2>/dev/null | grep ":808" || echo "  No ports 808x in use"
echo ""
echo "lsof:"
lsof -i :8081-8085 2>/dev/null || echo "  No processes on ports 8081-8085"
echo ""
echo "Docker:"
docker ps --format "{{.Ports}}" 2>/dev/null | grep ":808" || echo "  No Docker containers using ports 808x"
