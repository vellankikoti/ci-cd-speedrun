#!/bin/bash

# Verification script for scenario 04 port binding fix
# This script helps verify the fix is working correctly

set -e

echo "🔍 Scenario 04 K8s Commander - Port Binding Fix Verification"
echo "============================================================="
echo ""

# Check if running in Jenkins workspace
if [ -z "$WORKSPACE" ]; then
    echo "⚠️  Warning: Not running in Jenkins workspace"
    echo "   This script is designed to run after a Jenkins build"
    echo ""
fi

# Function to check container status
check_container() {
    local build_number=$1
    local container_name="k8s-commander-${build_number}"

    echo "🔍 Checking container: $container_name"

    # Check if container exists and is running
    if docker ps --filter "name=$container_name" --format "{{.Names}}" | grep -q "$container_name"; then
        echo "✅ Container is running"

        # Get port mapping
        local port_mapping=$(docker port $container_name 2>/dev/null | head -1)
        if [ -n "$port_mapping" ]; then
            local external_port=$(echo "$port_mapping" | cut -d: -f2)
            echo "✅ Port mapping: $port_mapping"
            echo "   → External port: $external_port"
            echo "   → Internal port: 8080 (fixed)"

            # Test API endpoints
            echo ""
            echo "🧪 Testing API endpoints..."

            if curl -s "http://localhost:$external_port/api/status" > /dev/null 2>&1; then
                echo "✅ Status API: Working"
                curl -s "http://localhost:$external_port/api/status" | jq . 2>/dev/null || true
            else
                echo "❌ Status API: Failed"
                return 1
            fi

            if curl -s "http://localhost:$external_port/api/concept" > /dev/null 2>&1; then
                echo "✅ Concept API: Working"
            else
                echo "❌ Concept API: Failed"
            fi

            if curl -s "http://localhost:$external_port/api/learning-path" > /dev/null 2>&1; then
                echo "✅ Learning Path API: Working"
            else
                echo "❌ Learning Path API: Failed"
            fi

            echo ""
            echo "🌐 Access URLs:"
            echo "   • Main App: http://localhost:$external_port"
            echo "   • API Status: http://localhost:$external_port/api/status"
            echo "   • Concept Info: http://localhost:$external_port/api/concept"
            echo "   • Learning Path: http://localhost:$external_port/api/learning-path"

            return 0
        else
            echo "❌ Could not get port mapping"
            return 1
        fi
    else
        echo "❌ Container is not running"

        # Check if container exists but is stopped
        if docker ps -a --filter "name=$container_name" --format "{{.Names}}" | grep -q "$container_name"; then
            echo "⚠️  Container exists but is stopped"
            echo "   Showing last 20 lines of logs:"
            docker logs --tail 20 "$container_name" 2>&1 || true
        else
            echo "❌ Container does not exist"
        fi
        return 1
    fi
}

# Function to show all k8s-commander containers
show_all_containers() {
    echo ""
    echo "📊 All K8s Commander Containers"
    echo "================================"

    local containers=$(docker ps -a --filter "name=k8s-commander" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")

    if [ -n "$containers" ]; then
        echo "$containers"
    else
        echo "No k8s-commander containers found"
    fi
}

# Function to check port conflicts
check_port_conflicts() {
    echo ""
    echo "🔍 Port Conflict Analysis"
    echo "========================="

    local start_port=8080
    local end_port=8100

    echo "Checking ports $start_port-$end_port..."
    echo ""

    for port in $(seq $start_port $end_port); do
        local in_use=false
        local used_by=""

        # Check netstat
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            in_use=true
            used_by="$used_by netstat"
        fi

        # Check lsof
        if lsof -i :$port 2>/dev/null | grep -q LISTEN; then
            in_use=true
            local process=$(lsof -i :$port 2>/dev/null | grep LISTEN | awk '{print $1}' | head -1)
            used_by="$used_by lsof($process)"
        fi

        # Check Docker
        if docker ps --format "{{.Ports}}" 2>/dev/null | grep -q ":$port->"; then
            in_use=true
            local container=$(docker ps --format "{{.Names}}: {{.Ports}}" 2>/dev/null | grep ":$port->" | cut -d: -f1)
            used_by="$used_by docker($container)"
        fi

        if [ "$in_use" = true ]; then
            echo "⚠️  Port $port: IN USE by $used_by"
        fi
    done

    echo ""
    echo "✅ Port conflict check complete"
}

# Main execution
main() {
    echo "📋 Verification Steps:"
    echo ""

    # Step 1: Show all containers
    show_all_containers

    # Step 2: Check port conflicts
    check_port_conflicts

    # Step 3: Check specific build if BUILD_NUMBER is set
    if [ -n "$BUILD_NUMBER" ]; then
        echo ""
        echo "🎯 Checking current build: $BUILD_NUMBER"
        echo "========================================="
        check_container "$BUILD_NUMBER"
    else
        echo ""
        echo "ℹ️  No BUILD_NUMBER set. To check a specific build, run:"
        echo "   BUILD_NUMBER=<number> ./verify-fix.sh"
    fi

    echo ""
    echo "✅ Verification complete!"
}

# Run main
main "$@"
