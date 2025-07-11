#!/bin/bash

# Kubernetes Blue-Green Demo - Rebuild and Deploy Script
# This script ensures fresh builds and deployments with latest code changes

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="scaling-challenge"
BACKEND_IMAGE="bluegreen-backend"
FRONTEND_IMAGE="bluegreen-frontend"
BACKEND_TAG="latest"
FRONTEND_TAG="latest"

echo -e "${BLUE}🔵🟢 Kubernetes Blue-Green Demo - Rebuild and Deploy${NC}"
echo "=========================================================="

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

# Function to stop and remove containers
cleanup_containers() {
    echo -e "${YELLOW}🧹 Cleaning up existing containers...${NC}"
    
    # Stop and remove backend containers
    if docker ps -q --filter "ancestor=$BACKEND_IMAGE:$BACKEND_TAG" | grep -q .; then
        echo -e "${BLUE}Stopping backend containers...${NC}"
        docker ps -q --filter "ancestor=$BACKEND_IMAGE:$BACKEND_TAG" | xargs -r docker stop
        docker ps -aq --filter "ancestor=$BACKEND_IMAGE:$BACKEND_TAG" | xargs -r docker rm
    fi
    
    # Stop and remove frontend containers
    if docker ps -q --filter "ancestor=$FRONTEND_IMAGE:$FRONTEND_TAG" | grep -q .; then
        echo -e "${BLUE}Stopping frontend containers...${NC}"
        docker ps -q --filter "ancestor=$FRONTEND_IMAGE:$FRONTEND_TAG" | xargs -r docker stop
        docker ps -aq --filter "ancestor=$FRONTEND_IMAGE:$FRONTEND_TAG" | xargs -r docker rm
    fi
    
    # Remove Kubernetes deployments
    if kubectl get deployment -n $NAMESPACE &> /dev/null; then
        echo -e "${BLUE}Removing Kubernetes deployments...${NC}"
        kubectl delete deployment backend-deployment -n $NAMESPACE --ignore-not-found=true
        kubectl delete deployment frontend-deployment -n $NAMESPACE --ignore-not-found=true
    fi
    
    echo -e "${GREEN}✅ Container cleanup completed${NC}"
}

# Function to remove old images
cleanup_images() {
    echo -e "${YELLOW}🗑️  Removing old images...${NC}"
    
    # Remove backend images
    if docker images | grep -q "$BACKEND_IMAGE"; then
        echo -e "${BLUE}Removing backend images...${NC}"
        docker rmi $(docker images | grep "$BACKEND_IMAGE" | awk '{print $3}') --force 2>/dev/null || true
    fi
    
    # Remove frontend images
    if docker images | grep -q "$FRONTEND_IMAGE"; then
        echo -e "${BLUE}Removing frontend images...${NC}"
        docker rmi $(docker images | grep "$FRONTEND_IMAGE" | awk '{print $3}') --force 2>/dev/null || true
    fi
    
    # Clean up dangling images
    echo -e "${BLUE}Cleaning up dangling images...${NC}"
    docker image prune -f
    
    echo -e "${GREEN}✅ Image cleanup completed${NC}"
}

# Function to build backend
build_backend() {
    echo -e "${YELLOW}🔨 Building backend image...${NC}"
    
    cd backend
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}❌ requirements.txt not found in backend directory${NC}"
        exit 1
    fi
    
    # Build the image
    docker build -t $BACKEND_IMAGE:$BACKEND_TAG .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backend image built successfully${NC}"
    else
        echo -e "${RED}❌ Backend image build failed${NC}"
        exit 1
    fi
    
    cd ..
}

# Function to build frontend
build_frontend() {
    echo -e "${YELLOW}🔨 Building frontend image...${NC}"
    
    cd frontend
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        echo -e "${RED}❌ package.json not found in frontend directory${NC}"
        exit 1
    fi
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo -e "${BLUE}Installing frontend dependencies...${NC}"
        npm install
    fi
    
    # Build the image
    docker build -t $FRONTEND_IMAGE:$FRONTEND_TAG .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend image built successfully${NC}"
    else
        echo -e "${RED}❌ Frontend image build failed${NC}"
        exit 1
    fi
    
    cd ..
}

# Function to create namespace
create_namespace() {
    echo -e "${YELLOW}📦 Creating namespace if it doesn't exist...${NC}"
    
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        kubectl create namespace $NAMESPACE
        echo -e "${GREEN}✅ Namespace $NAMESPACE created${NC}"
    else
        echo -e "${BLUE}ℹ️  Namespace $NAMESPACE already exists${NC}"
    fi
}

# Function to apply Kubernetes manifests
apply_manifests() {
    echo -e "${YELLOW}📦 Applying Kubernetes manifests...${NC}"
    
    # Apply all manifests in the k8s directory
    kubectl apply -f k8s/ -n $NAMESPACE
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Kubernetes manifests applied successfully${NC}"
    else
        echo -e "${RED}❌ Failed to apply Kubernetes manifests${NC}"
        exit 1
    fi
}

# Function to wait for deployments to be ready
wait_for_deployments() {
    echo -e "${YELLOW}⏳ Waiting for deployments to be ready...${NC}"
    
    # Wait for backend deployment
    echo -e "${BLUE}Waiting for backend deployment...${NC}"
    kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n $NAMESPACE
    
    # Wait for frontend deployment
    echo -e "${BLUE}Waiting for frontend deployment...${NC}"
    kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n $NAMESPACE
    
    echo -e "${GREEN}✅ All deployments are ready${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 Current Status:${NC}"
    echo "----------------------------------------"
    
    echo -e "${YELLOW}Deployments:${NC}"
    kubectl get deployments -n $NAMESPACE
    
    echo -e "${YELLOW}Pods:${NC}"
    kubectl get pods -n $NAMESPACE
    
    echo -e "${YELLOW}Services:${NC}"
    kubectl get services -n $NAMESPACE
    
    echo -e "${YELLOW}Images:${NC}"
    docker images | grep -E "($BACKEND_IMAGE|$FRONTEND_IMAGE)" || echo "No demo images found"
}

# Function to setup initial deployment strategy
setup_initial_strategy() {
    echo -e "${YELLOW}🔄 Setting up initial blue-green strategy...${NC}"
    
    # Scale to 5 blue, 5 green
    kubectl scale deployment blue-deployment --replicas=5 -n $NAMESPACE
    kubectl scale deployment green-deployment --replicas=5 -n $NAMESPACE
    
    echo -e "${GREEN}✅ Initial strategy applied (5 blue, 5 green)${NC}"
}

# Function to show access information
show_access_info() {
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
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
    echo -e "${PURPLE}💡 Tip: Use the web UI to interactively manage deployments!${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}🚀 Starting rebuild and deploy process...${NC}"
    
    # Check prerequisites
    check_command "docker"
    check_command "kubectl"
    check_directory
    
    # Cleanup phase
    cleanup_containers
    cleanup_images
    
    # Build phase
    build_backend
    build_frontend
    
    # Deploy phase
    create_namespace
    apply_manifests
    wait_for_deployments
    setup_initial_strategy
    
    # Show results
    show_status
    show_access_info
}

# Run main function
main "$@" 