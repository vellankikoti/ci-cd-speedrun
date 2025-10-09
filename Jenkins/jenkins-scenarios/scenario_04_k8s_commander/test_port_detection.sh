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

echo "Testing ports 8081-8085:"
for port in {8081..8085}; do
    echo "Checking port $port:"
    check_port $port
    echo ""
done

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
