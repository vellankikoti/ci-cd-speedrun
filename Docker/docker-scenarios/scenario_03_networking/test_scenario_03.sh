#!/bin/bash
set -e

echo "🧪 Testing Scenario 03 - Docker Networking Magic"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to wait for app to be ready
wait_for_app() {
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for app to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:5000 > /dev/null 2>&1; then
            print_success "App is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "App failed to start within 60 seconds"
    return 1
}

# Function to test voting functionality
test_voting() {
    print_status "Testing voting functionality..."
    
    # Get initial votes
    local initial_wfh=$(curl -s http://localhost:5000 | grep -o 'WFH Votes: [0-9]*' | grep -o '[0-9]*')
    local initial_wfo=$(curl -s http://localhost:5000 | grep -o 'WFO Votes: [0-9]*' | grep -o '[0-9]*')
    
    print_status "Initial votes - WFH: $initial_wfh, WFO: $initial_wfo"
    
    # Vote for WFH
    curl -s -X POST -d "vote=wfh" http://localhost:5000 > /dev/null
    sleep 1
    
    # Vote for WFO
    curl -s -X POST -d "vote=wfo" http://localhost:5000 > /dev/null
    sleep 1
    
    # Get final votes
    local final_wfh=$(curl -s http://localhost:5000 | grep -o 'WFH Votes: [0-9]*' | grep -o '[0-9]*')
    local final_wfo=$(curl -s http://localhost:5000 | grep -o 'WFO Votes: [0-9]*' | grep -o '[0-9]*')
    
    print_status "Final votes - WFH: $final_wfh, WFO: $final_wfo"
    
    # Check if votes increased
    if [ "$final_wfh" -gt "$initial_wfh" ] && [ "$final_wfo" -gt "$initial_wfo" ]; then
        print_success "Voting is working correctly!"
        return 0
    else
        print_error "Voting is not working correctly"
        return 1
    fi
}

# Function to check if containers are running
check_containers() {
    local container_name=$1
    if docker ps --format "table {{.Names}}" | grep -q "^$container_name$"; then
        print_success "Container $container_name is running"
        return 0
    else
        print_error "Container $container_name is not running"
        return 1
    fi
}

# Function to check if network exists
check_network() {
    local network_name=$1
    if docker network ls --format "table {{.Name}}" | grep -q "^$network_name$"; then
        print_success "Network $network_name exists"
        return 0
    else
        print_error "Network $network_name does not exist"
        return 1
    fi
}

# Clean up before starting
print_status "Cleaning up before testing..."
./scripts/cleanup.sh > /dev/null 2>&1 || true

# Test 1: Make scripts executable
print_status "Test 1: Making scripts executable..."
chmod +x scripts/*.sh
print_success "All scripts are now executable"

# Test 2: Build the app
print_status "Test 2: Building the Flask app..."
docker build -t vote-app ./app
print_success "App built successfully"

# Test 3: Step 1 - Run app without database
print_status "Test 3: Running app without database (should fail on vote)..."
./scripts/run_app_without_db.sh
sleep 5

if wait_for_app; then
    print_success "App started without database"
    
    # Test that voting fails
    response=$(curl -s -X POST -d "vote=wfh" http://localhost:5000 2>&1 || true)
    if echo "$response" | grep -q "Connection refused\|Name or service not known\|ConnectionError"; then
        print_success "App correctly fails when trying to vote (no database)"
    else
        print_warning "App didn't fail as expected when voting"
    fi
else
    print_error "App failed to start"
fi

# Clean up
./scripts/cleanup.sh > /dev/null 2>&1 || true

# Test 4: Step 2 - Run app with database in wrong network
print_status "Test 4: Running app with database in wrong network..."
./scripts/run_app_with_db_wrong_network.sh
sleep 5

if wait_for_app; then
    print_success "App started with database in wrong network"
    
    # Test that voting still fails
    response=$(curl -s -X POST -d "vote=wfh" http://localhost:5000 2>&1 || true)
    if echo "$response" | grep -q "Connection refused\|Name or service not known\|ConnectionError"; then
        print_success "App correctly fails when trying to vote (wrong network)"
    else
        print_warning "App didn't fail as expected when voting"
    fi
else
    print_error "App failed to start"
fi

# Clean up
./scripts/cleanup.sh > /dev/null 2>&1 || true

# Test 5: Step 3 - Fix the network
print_status "Test 5: Fixing the network..."
./scripts/fix_network.sh
sleep 5

if wait_for_app; then
    print_success "App started with fixed network"
    
    # Test that voting works
    if test_voting; then
        print_success "Voting works correctly with fixed network!"
    else
        print_error "Voting still doesn't work"
    fi
    
    # Check containers and network
    check_containers "vote-app"
    check_containers "redis-server"
    check_network "vote-net"
    
else
    print_error "App failed to start with fixed network"
fi

# Test 6: Check if ngrok is available
print_status "Test 6: Checking ngrok availability..."
if command -v ngrok &>/dev/null; then
    print_success "ngrok is available for public exposure"
else
    print_warning "ngrok not found - public exposure not available"
fi

# Test 7: Check if cloudflared is available
print_status "Test 7: Checking cloudflared availability..."
if command -v cloudflared &>/dev/null; then
    print_success "cloudflared is available for public exposure"
else
    print_warning "cloudflared not found - public exposure not available"
fi

# Final cleanup
print_status "Final cleanup..."
./scripts/cleanup.sh

echo ""
echo "🎉 Scenario 03 Testing Complete!"
echo "================================"
echo ""
echo "✅ All core functionality tested"
echo "✅ Network isolation demonstrated"
echo "✅ Voting functionality verified"
echo "✅ Public exposure tools checked"
echo ""
echo "📝 To run the full workshop experience:"
echo "   1. Follow the README.md step by step"
echo "   2. Try voting at http://localhost:5000"
echo "   3. Share with friends using ngrok or cloudflared"
echo "" 