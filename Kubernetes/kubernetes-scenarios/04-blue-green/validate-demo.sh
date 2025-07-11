#!/bin/bash

# Kubernetes Blue-Green Demo - Validation Script
# This script validates that all components are working correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

NAMESPACE="scaling-challenge"
BACKEND_IMAGE="bluegreen-backend"
FRONTEND_IMAGE="bluegreen-frontend"

echo -e "${BLUE}🔵🟢 Kubernetes Blue-Green Demo - Validation${NC}"
echo "================================================"

# Function to check if command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed or not in PATH${NC}"
        return 1
    fi
    return 0
}

# Function to check if we're in the right directory
check_directory() {
    if [ ! -f "backend/app.py" ] || [ ! -f "frontend/package.json" ]; then
        echo -e "${RED}❌ Please run this script from the 04-blue-green directory${NC}"
        return 1
    fi
    return 0
}

# Function to validate Docker images
validate_docker_images() {
    echo -e "${YELLOW}🔍 Validating Docker images...${NC}"
    
    local backend_exists=false
    local frontend_exists=false
    
    if docker images | grep -q "$BACKEND_IMAGE"; then
        echo -e "${GREEN}✅ Backend image exists${NC}"
        backend_exists=true
    else
        echo -e "${RED}❌ Backend image not found${NC}"
    fi
    
    if docker images | grep -q "$FRONTEND_IMAGE"; then
        echo -e "${GREEN}✅ Frontend image exists${NC}"
        frontend_exists=true
    else
        echo -e "${RED}❌ Frontend image not found${NC}"
    fi
    
    if [ "$backend_exists" = true ] && [ "$frontend_exists" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to validate Kubernetes namespace
validate_namespace() {
    echo -e "${YELLOW}🔍 Validating Kubernetes namespace...${NC}"
    
    if kubectl get namespace $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Namespace $NAMESPACE exists${NC}"
        return 0
    else
        echo -e "${RED}❌ Namespace $NAMESPACE not found${NC}"
        return 1
    fi
}

# Function to validate Kubernetes deployments
validate_deployments() {
    echo -e "${YELLOW}🔍 Validating Kubernetes deployments...${NC}"
    
    local backend_ready=false
    local frontend_ready=false
    local blue_ready=false
    local green_ready=false
    
    # Check backend deployment
    if kubectl get deployment backend-deployment -n $NAMESPACE &> /dev/null; then
        if kubectl get deployment backend-deployment -n $NAMESPACE -o jsonpath='{.status.readyReplicas}' | grep -q "1"; then
            echo -e "${GREEN}✅ Backend deployment is ready${NC}"
            backend_ready=true
        else
            echo -e "${YELLOW}⚠️  Backend deployment not ready${NC}"
        fi
    else
        echo -e "${RED}❌ Backend deployment not found${NC}"
    fi
    
    # Check frontend deployment
    if kubectl get deployment frontend-deployment -n $NAMESPACE &> /dev/null; then
        if kubectl get deployment frontend-deployment -n $NAMESPACE -o jsonpath='{.status.readyReplicas}' | grep -q "1"; then
            echo -e "${GREEN}✅ Frontend deployment is ready${NC}"
            frontend_ready=true
        else
            echo -e "${YELLOW}⚠️  Frontend deployment not ready${NC}"
        fi
    else
        echo -e "${RED}❌ Frontend deployment not found${NC}"
    fi
    
    # Check blue deployment
    if kubectl get deployment blue-deployment -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Blue deployment exists${NC}"
        blue_ready=true
    else
        echo -e "${RED}❌ Blue deployment not found${NC}"
    fi
    
    # Check green deployment
    if kubectl get deployment green-deployment -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Green deployment exists${NC}"
        green_ready=true
    else
        echo -e "${RED}❌ Green deployment not found${NC}"
    fi
    
    if [ "$backend_ready" = true ] && [ "$frontend_ready" = true ] && [ "$blue_ready" = true ] && [ "$green_ready" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to validate Kubernetes services
validate_services() {
    echo -e "${YELLOW}🔍 Validating Kubernetes services...${NC}"
    
    local backend_service=false
    local frontend_service=false
    local demo_service=false
    
    # Check backend service
    if kubectl get service backend-service -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Backend service exists${NC}"
        backend_service=true
    else
        echo -e "${RED}❌ Backend service not found${NC}"
    fi
    
    # Check frontend service
    if kubectl get service frontend-service -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Frontend service exists${NC}"
        frontend_service=true
    else
        echo -e "${RED}❌ Frontend service not found${NC}"
    fi
    
    # Check demo app service
    if kubectl get service demo-app-service -n $NAMESPACE &> /dev/null; then
        echo -e "${GREEN}✅ Demo app service exists${NC}"
        demo_service=true
    else
        echo -e "${RED}❌ Demo app service not found${NC}"
    fi
    
    if [ "$backend_service" = true ] && [ "$frontend_service" = true ] && [ "$demo_service" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to validate pods
validate_pods() {
    echo -e "${YELLOW}🔍 Validating Kubernetes pods...${NC}"
    
    local total_pods=$(kubectl get pods -n $NAMESPACE --no-headers | wc -l)
    local running_pods=$(kubectl get pods -n $NAMESPACE --no-headers | grep -c "Running")
    
    echo -e "${BLUE}📊 Pod Status:${NC}"
    kubectl get pods -n $NAMESPACE
    
    if [ "$total_pods" -gt 0 ] && [ "$running_pods" -eq "$total_pods" ]; then
        echo -e "${GREEN}✅ All pods are running ($running_pods/$total_pods)${NC}"
        return 0
    else
        echo -e "${RED}❌ Not all pods are running ($running_pods/$total_pods)${NC}"
        return 1
    fi
}

# Function to validate API endpoints
validate_api() {
    echo -e "${YELLOW}🔍 Validating API endpoints...${NC}"
    
    # Start port forwarding for backend
    echo -e "${BLUE}Starting port forwarding for backend...${NC}"
    kubectl port-forward svc/backend-service 5000:5000 -n $NAMESPACE &
    PF_PID=$!
    
    # Wait for port forwarding to be ready
    sleep 5
    
    # Test API endpoints
    local api_working=false
    
    if curl -s http://localhost:5000/api/pods > /dev/null; then
        echo -e "${GREEN}✅ Backend API is responding${NC}"
        echo -e "${BLUE}📊 Sample pod data:${NC}"
        curl -s http://localhost:5000/api/pods | jq '.[0:2]' 2>/dev/null || echo "Raw response available"
        api_working=true
    else
        echo -e "${RED}❌ Backend API is not responding${NC}"
    fi
    
    # Stop port forwarding
    kill $PF_PID 2>/dev/null || true
    
    if [ "$api_working" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to show summary
show_summary() {
    echo -e "${BLUE}📊 Validation Summary:${NC}"
    echo "----------------------------------------"
    
    echo -e "${YELLOW}Deployments:${NC}"
    kubectl get deployments -n $NAMESPACE
    
    echo -e "${YELLOW}Services:${NC}"
    kubectl get services -n $NAMESPACE
    
    echo -e "${YELLOW}Pods:${NC}"
    kubectl get pods -n $NAMESPACE
    
    echo -e "${YELLOW}Images:${NC}"
    docker images | grep -E "($BACKEND_IMAGE|$FRONTEND_IMAGE)" || echo "No demo images found"
}

# Function to show next steps
show_next_steps() {
    echo -e "${GREEN}🎉 Validation completed!${NC}"
    echo ""
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "----------------------------------------"
    echo -e "${YELLOW}1. Start the demo:${NC} ./redeploy-local.sh"
    echo -e "${YELLOW}2. Rebuild everything:${NC} ./rebuild-and-deploy.sh"
    echo -e "${YELLOW}3. Manage deployments:${NC} ./deploy-strategies.sh help"
    echo ""
    echo -e "${PURPLE}💡 Tip: Use the web UI at http://localhost:3000 to interact with the demo!${NC}"
}

# Main validation function
main() {
    local all_valid=true
    
    # Check prerequisites
    if ! check_command "docker"; then all_valid=false; fi
    if ! check_command "kubectl"; then all_valid=false; fi
    if ! check_directory; then all_valid=false; fi
    
    if [ "$all_valid" = false ]; then
        echo -e "${RED}❌ Prerequisites check failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
    
    # Validate components
    if ! validate_docker_images; then all_valid=false; fi
    if ! validate_namespace; then all_valid=false; fi
    if ! validate_deployments; then all_valid=false; fi
    if ! validate_services; then all_valid=false; fi
    if ! validate_pods; then all_valid=false; fi
    if ! validate_api; then all_valid=false; fi
    
    # Show summary
    show_summary
    
    if [ "$all_valid" = true ]; then
        echo -e "${GREEN}🎉 All validations passed!${NC}"
        show_next_steps
    else
        echo -e "${RED}❌ Some validations failed${NC}"
        echo -e "${YELLOW}💡 Try running: ./rebuild-and-deploy.sh${NC}"
        exit 1
    fi
}

# Run main function
main "$@" 