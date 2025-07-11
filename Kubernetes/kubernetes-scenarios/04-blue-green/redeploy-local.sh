#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

NAMESPACE="scaling-challenge"

echo -e "${BLUE}🔵🟢 Kubernetes Blue-Green Demo - Local Redeploy${NC}"
echo "======================================================"

# Function to check if command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed or not in PATH${NC}"
        exit 1
    fi
}

# Function to check if we're in the right directory
check_directory() {
    if [ ! -f "backend/app.py" ] || [ ! -f "frontend/package.json" ]; then
        echo -e "${RED}❌ Please run this script from the 04-blue-green directory${NC}"
        exit 1
    fi
}

# Check prerequisites
check_command "docker"
check_command "kubectl"
check_directory

cd $(dirname "$0")

echo -e "${YELLOW}[1/7] Building backend Docker image...${NC}"
cd backend
if docker build -t bluegreen-backend:latest .; then
    echo -e "${GREEN}✅ Backend image built successfully${NC}"
else
    echo -e "${RED}❌ Backend image build failed${NC}"
    exit 1
fi

cd ../frontend

echo -e "${YELLOW}[2/7] Building frontend Docker image...${NC}"
if docker build -t bluegreen-frontend:latest .; then
    echo -e "${GREEN}✅ Frontend image built successfully${NC}"
else
    echo -e "${RED}❌ Frontend image build failed${NC}"
    exit 1
fi

cd ../k8s

echo -e "${YELLOW}[3/7] Re-applying backend and frontend deployments...${NC}"
kubectl apply -f backend-deployment.yaml -n $NAMESPACE
kubectl apply -f frontend-deployment.yaml -n $NAMESPACE

# Wait for deployments to be ready
echo -e "${YELLOW}[4/7] Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n $NAMESPACE

cd ..

# Kill any process using ports 3000 or 5000
echo -e "${YELLOW}[5/7] Cleaning up existing port forwards...${NC}"
for port in 3000 5000; do
    pid=$(lsof -ti tcp:$port 2>/dev/null || true)
    if [ -n "$pid" ]; then
        echo -e "${BLUE}Killing process on port $port (PID $pid)${NC}"
        kill -9 $pid 2>/dev/null || true
    fi
done

# Port-forward services
echo -e "${YELLOW}[6/7] Starting port-forwarding for backend and frontend...${NC}"
kubectl port-forward svc/backend-service 5000:5000 -n $NAMESPACE &
BACKEND_PID=$!
kubectl port-forward svc/frontend-service 3000:80 -n $NAMESPACE &
FRONTEND_PID=$!

sleep 5

# Check backend API
echo -e "${YELLOW}[7/7] Checking backend API for pods...${NC}"
if curl -s http://localhost:5000/api/pods > /dev/null; then
    echo -e "${GREEN}✅ Backend API is responding${NC}"
    echo -e "${BLUE}📊 Pod data:${NC}"
    curl -s http://localhost:5000/api/pods | jq . 2>/dev/null || echo "Raw response: $(curl -s http://localhost:5000/api/pods)"
else
    echo -e "${RED}❌ Backend API is not responding. Check backend logs:${NC}"
    kubectl logs deployment/backend-deployment -n $NAMESPACE --tail=20
fi

# Show status
echo -e "${BLUE}📊 Current Status:${NC}"
echo "----------------------------------------"
kubectl get pods -n $NAMESPACE
echo ""
kubectl get services -n $NAMESPACE

# Open frontend in browser
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo ""
echo -e "${BLUE}📋 Access Information:${NC}"
echo "----------------------------------------"
echo -e "${YELLOW}Frontend:${NC} http://localhost:3000"
echo -e "${YELLOW}Backend API:${NC} http://localhost:5000"
echo ""
echo -e "${BLUE}🔧 Management Commands:${NC}"
echo "----------------------------------------"
echo -e "${YELLOW}Show status:${NC} ./deploy-strategies.sh status"
echo -e "${YELLOW}Switch to green:${NC} ./deploy-strategies.sh green"
echo -e "${YELLOW}Progressive rollout:${NC} ./deploy-strategies.sh rollout"
echo -e "${YELLOW}Canary deployment:${NC} ./deploy-strategies.sh canary"
echo -e "${YELLOW}Kill random pod:${NC} ./deploy-strategies.sh kill"
echo ""

# Open browser
echo -e "${BLUE}🌐 Opening frontend in browser...${NC}"
if which xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif which open > /dev/null; then
    open http://localhost:3000
else
    echo -e "${YELLOW}Please open http://localhost:3000 in your browser${NC}"
fi

echo -e "${PURPLE}💡 Tip: Use the web UI to interactively manage deployments!${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop port-forwarding${NC}"

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID 