#!/bin/bash

# Kubernetes Deployment Strategy Demo Script
# This script helps manage different deployment strategies for the demo

NAMESPACE="scaling-challenge"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔵🟢 Kubernetes Deployment Strategy Demo${NC}"
echo "=========================================="

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}❌ kubectl is not installed or not in PATH${NC}"
        exit 1
    fi
}

# Function to check namespace
check_namespace() {
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        echo -e "${YELLOW}⚠️  Creating namespace $NAMESPACE...${NC}"
        kubectl create namespace $NAMESPACE
    fi
}

# Function to apply manifests
apply_manifests() {
    echo -e "${BLUE}📦 Applying Kubernetes manifests...${NC}"
    kubectl apply -f k8s/ -n $NAMESPACE
    echo -e "${GREEN}✅ Manifests applied successfully${NC}"
}

# Function to show current deployment status
show_status() {
    echo -e "${BLUE}📊 Current Deployment Status:${NC}"
    echo "----------------------------------------"
    
    echo -e "${YELLOW}Blue Deployment:${NC}"
    kubectl get deployment blue-deployment -n $NAMESPACE -o wide
    
    echo -e "${GREEN}Green Deployment:${NC}"
    kubectl get deployment green-deployment -n $NAMESPACE -o wide
    
    echo -e "${BLUE}Pods:${NC}"
    kubectl get pods -n $NAMESPACE -l app=demo-app --show-labels
}

# Function to switch to blue-green strategy
switch_to_blue_green() {
    echo -e "${BLUE}🔄 Switching to Blue-Green Strategy...${NC}"
    
    # Scale blue to 5, green to 5
    kubectl scale deployment blue-deployment --replicas=5 -n $NAMESPACE
    kubectl scale deployment green-deployment --replicas=5 -n $NAMESPACE
    
    echo -e "${GREEN}✅ Blue-Green strategy applied (5 blue, 5 green)${NC}"
    show_status
}

# Function to switch to green (all green)
switch_to_green() {
    echo -e "${GREEN}🟢 Switching to Green Strategy...${NC}"
    
    # Scale blue to 0, green to 10
    kubectl scale deployment blue-deployment --replicas=0 -n $NAMESPACE
    kubectl scale deployment green-deployment --replicas=10 -n $NAMESPACE
    
    echo -e "${GREEN}✅ Green strategy applied (0 blue, 10 green)${NC}"
    show_status
}

# Function to switch to rollout strategy
switch_to_rollout() {
    echo -e "${BLUE}📈 Switching to Rollout Strategy...${NC}"
    
    # Scale blue to 3, green to 7 (progressive rollout)
    kubectl scale deployment blue-deployment --replicas=3 -n $NAMESPACE
    kubectl scale deployment green-deployment --replicas=7 -n $NAMESPACE
    
    echo -e "${GREEN}✅ Rollout strategy applied (3 blue, 7 green)${NC}"
    show_status
}

# Function to switch to canary strategy
switch_to_canary() {
    echo -e "${YELLOW}🐦 Switching to Canary Strategy...${NC}"
    
    # Scale blue to 8, green to 2 (canary)
    kubectl scale deployment blue-deployment --replicas=8 -n $NAMESPACE
    kubectl scale deployment green-deployment --replicas=2 -n $NAMESPACE
    
    echo -e "${GREEN}✅ Canary strategy applied (8 blue, 2 green)${NC}"
    show_status
}

# Function to kill a random pod
kill_random_pod() {
    echo -e "${RED}🗡️  Killing a random pod...${NC}"
    
    # Get a random pod
    POD_NAME=$(kubectl get pods -n $NAMESPACE -l app=demo-app -o jsonpath='{.items[0].metadata.name}')
    
    if [ ! -z "$POD_NAME" ]; then
        echo -e "${YELLOW}Killing pod: $POD_NAME${NC}"
        kubectl delete pod $POD_NAME -n $NAMESPACE
        echo -e "${GREEN}✅ Pod killed. Watch it self-heal!${NC}"
    else
        echo -e "${RED}❌ No pods found${NC}"
    fi
}

# Function to show help
show_help() {
    echo -e "${BLUE}Usage: $0 [COMMAND]${NC}"
    echo ""
    echo "Commands:"
    echo "  setup          - Apply all manifests and setup initial state"
    echo "  status         - Show current deployment status"
    echo "  blue-green     - Switch to blue-green strategy (5 blue, 5 green)"
    echo "  green          - Switch to green strategy (0 blue, 10 green)"
    echo "  rollout        - Switch to rollout strategy (3 blue, 7 green)"
    echo "  canary         - Switch to canary strategy (8 blue, 2 green)"
    echo "  kill           - Kill a random pod to test self-healing"
    echo "  help           - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup       # Initial setup"
    echo "  $0 green       # Switch all traffic to green"
    echo "  $0 kill        # Test self-healing"
}

# Main script logic
case "${1:-help}" in
    "setup")
        check_kubectl
        check_namespace
        apply_manifests
        switch_to_blue_green
        echo -e "${GREEN}🎉 Demo setup complete!${NC}"
        echo -e "${BLUE}Access the demo at: http://localhost:3000${NC}"
        ;;
    "status")
        check_kubectl
        show_status
        ;;
    "blue-green")
        check_kubectl
        switch_to_blue_green
        ;;
    "green")
        check_kubectl
        switch_to_green
        ;;
    "rollout")
        check_kubectl
        switch_to_rollout
        ;;
    "canary")
        check_kubectl
        switch_to_canary
        ;;
    "kill")
        check_kubectl
        kill_random_pod
        ;;
    "help"|*)
        show_help
        ;;
esac 