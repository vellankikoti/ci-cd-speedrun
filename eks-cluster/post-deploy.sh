#!/bin/bash

# EKS Post-Deployment Setup Script
# This script completes the EKS cluster setup after CloudFormation deployment
# It creates IAM roles that depend on the OIDC provider and installs essential add-ons

set -e

# Configuration
STACK_NAME="${1:-workshop-eks-cluster}"
REGION="${2:-us-west-2}"

echo "🚀 Starting EKS post-deployment setup..."
echo "Stack: $STACK_NAME"
echo "Region: $REGION"

# Get cluster information from CloudFormation outputs
echo "📋 Retrieving cluster information..."
CLUSTER_NAME=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks[0].Outputs[?OutputKey==`ClusterName`].OutputValue' \
  --output text)

VPC_ID=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks[0].Outputs[?OutputKey==`VPCId`].OutputValue' \
  --output text)

OIDC_ISSUER=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks[0].Outputs[?OutputKey==`OIDCIssuerURL`].OutputValue' \
  --output text)

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "✅ Cluster Name: $CLUSTER_NAME"
echo "✅ VPC ID: $VPC_ID"
echo "✅ OIDC Issuer: $OIDC_ISSUER"
echo "✅ Account ID: $ACCOUNT_ID"

# Configure kubectl
echo "🔧 Configuring kubectl..."
aws eks update-kubeconfig --region $REGION --name $CLUSTER_NAME

# Verify cluster connectivity
echo "🔍 Verifying cluster connectivity..."
kubectl get nodes

# Create OIDC Identity Provider if it doesn't exist
echo "🔑 Setting up OIDC Identity Provider..."
OIDC_ID=$(echo $OIDC_ISSUER | cut -d '/' -f 5)

# Check if OIDC provider already exists
if aws iam get-open-id-connect-provider --open-id-connect-provider-arn "arn:aws:iam::$ACCOUNT_ID:oidc-provider/$OIDC_ID" 2>/dev/null; then
    echo "✅ OIDC provider already exists"
else
    echo "📝 Creating OIDC provider..."
    eksctl utils associate-iam-oidc-provider --region=$REGION --cluster=$CLUSTER_NAME --approve
fi

# Create AWS Load Balancer Controller IAM Role
echo "🔧 Creating AWS Load Balancer Controller IAM Role..."

cat > /tmp/alb-controller-trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::$ACCOUNT_ID:oidc-provider/$OIDC_ID"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "$OIDC_ID:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller",
                    "$OIDC_ID:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
EOF

# Create ALB Controller role if it doesn't exist
ALB_ROLE_NAME="${CLUSTER_NAME}-alb-controller-role"
if aws iam get-role --role-name $ALB_ROLE_NAME 2>/dev/null; then
    echo "✅ ALB Controller role already exists"
else
    echo "📝 Creating ALB Controller role..."
    aws iam create-role \
        --role-name $ALB_ROLE_NAME \
        --assume-role-policy-document file:///tmp/alb-controller-trust-policy.json \
        --description "IAM role for AWS Load Balancer Controller"
    
    # Download and attach the ALB Controller policy
    curl -s -o /tmp/iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.6.0/docs/install/iam_policy.json
    
    aws iam put-role-policy \
        --role-name $ALB_ROLE_NAME \
        --policy-name AWSLoadBalancerControllerIAMPolicy \
        --policy-document file:///tmp/iam_policy.json
fi

# Create EBS CSI Driver IAM Role
echo "🔧 Creating EBS CSI Driver IAM Role..."

cat > /tmp/ebs-csi-trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::$ACCOUNT_ID:oidc-provider/$OIDC_ID"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "$OIDC_ID:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa",
                    "$OIDC_ID:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
EOF

# Create EBS CSI role if it doesn't exist
EBS_ROLE_NAME="${CLUSTER_NAME}-ebs-csi-driver-role"
if aws iam get-role --role-name $EBS_ROLE_NAME 2>/dev/null; then
    echo "✅ EBS CSI Driver role already exists"
else
    echo "📝 Creating EBS CSI Driver role..."
    aws iam create-role \
        --role-name $EBS_ROLE_NAME \
        --assume-role-policy-document file:///tmp/ebs-csi-trust-policy.json \
        --description "IAM role for EBS CSI Driver"
    
    # Attach the managed policy
    aws iam attach-role-policy \
        --role-name $EBS_ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy
fi

# Update EBS CSI Driver add-on with the IAM role
echo "🔧 Updating EBS CSI Driver add-on..."
aws eks update-addon \
    --cluster-name $CLUSTER_NAME \
    --addon-name aws-ebs-csi-driver \
    --service-account-role-arn "arn:aws:iam::$ACCOUNT_ID:role/$EBS_ROLE_NAME" \
    --region $REGION \
    --resolve-conflicts OVERWRITE

# Wait for EBS CSI addon to be active
echo "⏳ Waiting for EBS CSI addon to be active..."
aws eks wait addon-active --cluster-name $CLUSTER_NAME --addon-name aws-ebs-csi-driver --region $REGION

# Install AWS Load Balancer Controller
echo "🔧 Installing AWS Load Balancer Controller..."

# Add Helm repository
helm repo add eks https://aws.github.io/eks-charts
helm repo update

# Create service account for ALB Controller
kubectl create serviceaccount aws-load-balancer-controller \
    --namespace kube-system \
    --dry-run=client -o yaml | kubectl apply -f -

# Annotate service account with IAM role
kubectl annotate serviceaccount aws-load-balancer-controller \
    --namespace kube-system \
    "eks.amazonaws.com/role-arn=arn:aws:iam::$ACCOUNT_ID:role/$ALB_ROLE_NAME" \
    --overwrite

# Install or upgrade AWS Load Balancer Controller
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
    --namespace kube-system \
    --set clusterName=$CLUSTER_NAME \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller \
    --set region=$REGION \
    --set vpcId=$VPC_ID

# Wait for ALB Controller to be ready
echo "⏳ Waiting for AWS Load Balancer Controller to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/aws-load-balancer-controller -n kube-system

# Install Metrics Server
echo "🔧 Installing Metrics Server..."
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for Metrics Server to be ready
echo "⏳ Waiting for Metrics Server to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/metrics-server -n kube-system

# Create default storage class
echo "🔧 Creating default storage class..."
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF

# Create cluster admin role binding for current user
echo "🔧 Creating cluster admin access..."
CURRENT_USER_ARN=$(aws sts get-caller-identity --query Arn --output text)
kubectl create clusterrolebinding workshop-admin \
    --clusterrole=cluster-admin \
    --user="$CURRENT_USER_ARN" \
    --dry-run=client -o yaml | kubectl apply -f -

# Verify cluster status
echo "🔍 Verifying cluster status..."
echo ""
echo "=== CLUSTER STATUS ==="
kubectl get nodes -o wide
echo ""
echo "=== SYSTEM PODS ==="
kubectl get pods -n kube-system
echo ""
echo "=== STORAGE CLASSES ==="
kubectl get storageclass
echo ""
echo "=== ADD-ONS STATUS ==="
aws eks describe-addon --cluster-name $CLUSTER_NAME --addon-name vpc-cni --region $REGION --query 'addon.status'
aws eks describe-addon --cluster-name $CLUSTER_NAME --addon-name coredns --region $REGION --query 'addon.status'
aws eks describe-addon --cluster-name $CLUSTER_NAME --addon-name kube-proxy --region $REGION --query 'addon.status'
aws eks describe-addon --cluster-name $CLUSTER_NAME --addon-name aws-ebs-csi-driver --region $REGION --query 'addon.status'

# Test cluster functionality
echo "🧪 Testing cluster functionality..."

# Test DNS resolution
echo "📡 Testing DNS resolution..."
kubectl run test-dns --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes.default || true

# Test storage provisioning
echo "💾 Testing storage provisioning..."
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 1Gi
EOF

# Wait a moment for PVC to be bound
sleep 10
kubectl get pvc test-pvc
kubectl delete pvc test-pvc

# Clean up temporary files
rm -f /tmp/alb-controller-trust-policy.json /tmp/ebs-csi-trust-policy.json /tmp/iam_policy.json

echo ""
echo "🎉 ================================="
echo "🎉 POST-DEPLOYMENT SETUP COMPLETE!"
echo "🎉 ================================="
echo ""
echo "✅ Cluster Name: $CLUSTER_NAME"
echo "✅ Region: $REGION"
echo "✅ VPC ID: $VPC_ID"
echo "✅ OIDC Provider: Created and configured"
echo "✅ AWS Load Balancer Controller: Installed and ready"
echo "✅ EBS CSI Driver: Configured with IAM role"
echo "✅ Metrics Server: Installed and ready"
echo "✅ Default Storage Class: gp3 (encrypted)"
echo "✅ Cluster Admin Access: Configured for current user"
echo ""
echo "🚀 Your EKS cluster is now ready for workshop demonstrations!"
echo ""
echo "📋 Quick verification commands:"
echo "   kubectl get nodes"
echo "   kubectl get pods --all-namespaces"
echo "   kubectl top nodes"
echo ""
echo "📋 To deploy a sample application:"
echo "   kubectl create deployment nginx --image=nginx"
echo "   kubectl expose deployment nginx --port=80 --type=LoadBalancer"
echo "   kubectl get services"
echo ""