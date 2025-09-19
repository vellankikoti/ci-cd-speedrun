#!/bin/bash

# EKS Workshop Demo Script
# This script demonstrates the EKS cluster deployment functionality

set -e

echo "🎓 EKS Workshop Demo Script"
echo "=========================="
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI v2"
    exit 1
fi

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl"
    exit 1
fi

# Check eksctl
if ! command -v eksctl &> /dev/null; then
    echo "❌ eksctl not found. Please install eksctl"
    exit 1
fi

# Check Helm
if ! command -v helm &> /dev/null; then
    echo "❌ Helm not found. Please install Helm"
    exit 1
fi

echo "✅ All prerequisites found"
echo ""

# Check AWS credentials
echo "🔍 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure'"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region || echo "us-west-2")
echo "✅ AWS credentials configured (Account: $ACCOUNT_ID, Region: $REGION)"
echo ""

# Set demo parameters
CLUSTER_NAME="workshop-demo-$(date +%s)"
STACK_NAME="workshop-demo-stack-$(date +%s)"

echo "🚀 Starting EKS cluster deployment demo..."
echo "   Cluster Name: $CLUSTER_NAME"
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo ""

# Run tests first
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short
echo ""

# Deploy cluster
echo "🚀 Deploying EKS cluster..."
python eks_manager.py deploy \
    --cluster-name "$CLUSTER_NAME" \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --node-instance-type t3.small \
    --node-count 3 \
    --enable-logging \
    --enable-alb-controller

if [ $? -eq 0 ]; then
    echo "✅ EKS cluster deployed successfully!"
else
    echo "❌ EKS cluster deployment failed!"
    exit 1
fi
echo ""

# Configure kubectl
echo "🔧 Configuring kubectl..."
python eks_manager.py configure-kubectl \
    --cluster-name "$CLUSTER_NAME" \
    --region "$REGION"

if [ $? -eq 0 ]; then
    echo "✅ kubectl configured successfully!"
else
    echo "❌ kubectl configuration failed!"
    exit 1
fi
echo ""

# Run post-deployment setup
echo "🔧 Running post-deployment setup..."
python eks_manager.py post-deploy \
    --cluster-name "$CLUSTER_NAME" \
    --stack-name "$STACK_NAME" \
    --region "$REGION"

if [ $? -eq 0 ]; then
    echo "✅ Post-deployment setup completed!"
else
    echo "❌ Post-deployment setup failed!"
    exit 1
fi
echo ""

# Generate connection info
echo "📋 Generating connection information..."
python eks_manager.py generate-connection-info \
    --cluster-name "$CLUSTER_NAME" \
    --region "$REGION" \
    --output-file "connection-info-$CLUSTER_NAME.txt"

if [ $? -eq 0 ]; then
    echo "✅ Connection information generated!"
else
    echo "❌ Connection information generation failed!"
    exit 1
fi
echo ""

# Show cluster status
echo "📊 Cluster Status:"
echo "=================="
kubectl get nodes -o wide
echo ""
kubectl get pods --all-namespaces
echo ""

# Deploy sample application
echo "🚀 Deploying sample application..."
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services
echo ""

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/nginx
echo ""

# Show final status
echo "🎉 Demo completed successfully!"
echo "==============================="
echo ""
echo "📋 Cluster Details:"
echo "   Cluster Name: $CLUSTER_NAME"
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo "   Account ID: $ACCOUNT_ID"
echo ""
echo "🔗 Connection Commands:"
echo "   aws eks update-kubeconfig --region $REGION --name $CLUSTER_NAME"
echo "   kubectl get nodes"
echo "   kubectl get pods --all-namespaces"
echo ""
echo "📄 Check connection-info-$CLUSTER_NAME.txt for detailed instructions"
echo ""
echo "🧹 To clean up resources:"
echo "   aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION"
echo "   kubectl delete deployment nginx"
echo "   kubectl delete service nginx"
echo ""
echo "💰 Estimated monthly cost: ~$50-80 (3x t3.small nodes + EKS control plane)"
echo ""
