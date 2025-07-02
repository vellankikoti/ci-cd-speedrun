# Complete EKS Workshop Deployment Guide

## 🎯 Overview

This guide provides a complete, enterprise-grade solution for deploying EKS clusters for workshop environments. The solution consists of:

1. **CloudFormation Template** - Creates core infrastructure
2. **Post-Deployment Script** - Configures OIDC-dependent components
3. **Comprehensive Documentation** - Setup, usage, and troubleshooting

## 🏗️ Architecture Components

### Core Infrastructure (CloudFormation)
- ✅ **VPC with public/private subnets** across 2 AZs
- ✅ **EKS Cluster** with public API endpoint
- ✅ **Managed Node Group** with 3 t3.medium instances
- ✅ **Security Groups** with minimal required access
- ✅ **IAM Roles** for cluster and node groups
- ✅ **Core Add-ons**: VPC CNI, CoreDNS, kube-proxy, EBS CSI

### Post-Deployment Components (Script)
- ✅ **OIDC Identity Provider** configuration
- ✅ **AWS Load Balancer Controller** with IAM role
- ✅ **EBS CSI Driver** IAM role configuration
- ✅ **Metrics Server** installation
- ✅ **Default Storage Class** (gp3, encrypted)
- ✅ **Cluster admin access** for current user

## 🚀 Quick Start Deployment

### Prerequisites

```bash
# Required tools
aws --version          # AWS CLI v2
kubectl version        # Kubernetes CLI
helm version           # Helm v3
eksctl version         # eksctl (for OIDC setup)

# Verify AWS credentials
aws sts get-caller-identity
```

### Step 1: Deploy CloudFormation Template

```bash
# Download the template (save the CloudFormation YAML as eks-cluster.yaml)

# Deploy the stack
aws cloudformation create-stack \
  --stack-name workshop-eks-cluster \
  --template-body file://eks-cluster.yaml \
  --parameters \
    ParameterKey=ClusterName,ParameterValue=workshop-demo \
    ParameterKey=Environment,ParameterValue=workshop \
    ParameterKey=NodeInstanceType,ParameterValue=t3.medium \
    ParameterKey=NodeGroupDesiredCapacity,ParameterValue=3 \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-west-2

# Wait for completion (15-20 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name workshop-eks-cluster \
  --region us-west-2

# Verify deployment
aws cloudformation describe-stacks \
  --stack-name workshop-eks-cluster \
  --region us-west-2 \
  --query 'Stacks[0].StackStatus'
```

### Step 2: Run Post-Deployment Setup

```bash
# Make the script executable
chmod +x post-deployment-setup.sh

# Run the setup script
./post-deployment-setup.sh workshop-eks-cluster us-west-2

# The script will:
# - Configure kubectl
# - Set up OIDC provider
# - Create IAM roles for controllers
# - Install AWS Load Balancer Controller
# - Install Metrics Server
# - Configure storage classes
# - Verify cluster functionality
```

### Step 3: Verify Deployment

```bash
# Check cluster status
kubectl get nodes -o wide
kubectl get pods --all-namespaces
kubectl top nodes

# Check add-ons
kubectl get deployment -n kube-system
kubectl get storageclass

# Test with sample application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services

# Get LoadBalancer URL (wait a few minutes for provisioning)
kubectl get service nginx -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

## 💰 Cost Analysis & Optimization

### Estimated Costs (us-west-2)

| Component | Quantity | Unit Cost | Monthly Cost |
|-----------|----------|-----------|--------------|
| EKS Control Plane | 1 | $0.10/hour | $73 |
| EC2 Instances (t3.medium) | 3 | $0.0416/hour | $90 |
| NAT Gateway | 1 | $0.045/hour | $33 |
| EBS Storage (20GB × 3) | 60GB | $0.10/GB/month | $6 |
| Data Transfer | ~10GB | $0.09/GB | $1 |
| **Total Estimated** | | | **$203/month** |

### Cost Optimization Strategies

**1. Use Smaller Instances:**
```yaml
# In CloudFormation parameters
NodeInstanceType: t3.small  # Saves ~$45/month
```

**2. Use Spot Instances:**
```yaml
# Add to NodeGroup in template
CapacityType: SPOT
InstanceTypes:
  - t3.medium
  - t3a.medium
  - t3.large
```

**3. Workshop-Specific Optimization:**
- Deploy clusters only during workshop hours
- Use cluster autoscaler to scale down when idle
- Delete clusters immediately after workshops

## 🔧 Customization Options

### CloudFormation Parameters

```bash
# Minimum cost configuration
aws cloudformation create-stack \
  --parameters \
    ParameterKey=NodeInstanceType,ParameterValue=t3.small \
    ParameterKey=NodeGroupDesiredCapacity,ParameterValue=2 \
    ParameterKey=NodeGroupMinSize,ParameterValue=1 \
    ParameterKey=NodeGroupMaxSize,ParameterValue=4

# High availability configuration
aws cloudformation create-stack \
  --parameters \
    ParameterKey=NodeInstanceType,ParameterValue=t3.large \
    ParameterKey=NodeGroupDesiredCapacity,ParameterValue=6 \
    ParameterKey=NodeGroupMinSize,ParameterValue=3 \
    ParameterKey=NodeGroupMaxSize,ParameterValue=10
```

### Regional Deployment

```bash
# Deploy in different regions
REGIONS=("us-east-1" "us-west-2" "eu-west-1" "ap-southeast-1")

for region in "${REGIONS[@]}"; do
  aws cloudformation create-stack \
    --stack-name "workshop-eks-${region}" \
    --template-body file://eks-cluster.yaml \
    --region $region \
    --capabilities CAPABILITY_NAMED_IAM
done
```

## 🛡️ Security Best Practices

### Network Security
- **Private worker nodes** in private subnets
- **Public subnets** only for load balancers
- **Security groups** with minimal required ports
- **VPC Flow Logs** (optional, add to template)

### IAM Security
- **Least privilege** IAM roles and policies
- **IRSA (IAM Roles for Service Accounts)** for workloads
- **RBAC** configured for cluster access
- **No long-term credentials** in pods

### Cluster Security
```bash
# Enable envelope encryption (add to template)
EncryptionConfig:
  - Resources: ['secrets']
    Provider:
      KeyId: !Ref KMSKey

# Network policies (deploy post-setup)
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/master/calico-operator.yaml
```

## 📊 Monitoring & Observability

### Built-in Monitoring

```bash
# CloudWatch Container Insights
aws eks update-cluster-config \
  --name workshop-demo \
  --logging '{"enable":["api","audit","authenticator","controllerManager","scheduler"]}'

# View logs
aws logs describe-log-groups --log-group-name-prefix /aws/eks
```

### Additional Monitoring Tools

```bash
# Prometheus and Grafana (optional)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# AWS X-Ray (for distributed tracing)
kubectl apply -f https://github.com/aws/aws-xray-daemon/raw/master/kubernetes/xray-k8s-daemonset.yaml
```

## 🚨 Troubleshooting Guide

### Common Issues

**1. CloudFormation Stack Creation Fails**
```bash
# Check stack events
aws cloudformation describe-stack-events --stack-name workshop-eks-cluster

# Common causes:
# - Insufficient IAM permissions
# - Resource limits exceeded
# - Invalid parameter values
```

**2. Node Group Not Ready**
```bash
# Check node group status
aws eks describe-nodegroup --cluster-name workshop-demo --nodegroup-name workshop-demo-nodegroup

# Check EC2 instances
aws ec2 describe-instances --filters "Name=tag:eks:cluster-name,Values=workshop-demo"

# Common causes:
# - Subnet capacity issues
# - Security group misconfiguration
# - IAM role issues
```

**3. Pods Not Starting**
```bash
# Check pod status
kubectl describe pod POD_NAME

# Check node resources
kubectl describe nodes
kubectl top nodes

# Common causes:
# - Insufficient resources
# - Image pull errors
# - Security context issues
```

**4. LoadBalancer Not Getting External IP**
```bash
# Check AWS Load Balancer Controller
kubectl logs -n kube-system deployment/aws-load-balancer-controller

# Check service events
kubectl describe service SERVICE_NAME

# Common causes:
# - ALB Controller not installed/configured
# - Subnet tags missing
# - Security group issues
```

### Debug Commands

```bash
# Cluster connectivity
kubectl cluster-info
kubectl get componentstatuses

# Node status
kubectl get nodes -o wide
kubectl describe nodes

# Pod status
kubectl get pods --all-namespaces -o wide
kubectl get events --sort-by=.metadata.creationTimestamp

# Add-on status
aws eks list-addons --cluster-name workshop-demo
aws eks describe-addon --cluster-name workshop-demo --addon-name vpc-cni
```

## 🔄 CI/CD Integration Examples

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'ACTION', choices: ['deploy', 'destroy'], description: 'Action to perform')
        string(name: 'CLUSTER_NAME', defaultValue: 'workshop-demo', description: 'Cluster name')
        choice(name: 'REGION', choices: ['us-west-2', 'us-east-1'], description: 'AWS region')
    }
    
    environment {
        STACK_NAME = "eks-${params.CLUSTER_NAME}"
    }
    
    stages {
        stage('Deploy Infrastructure') {
            when { params.ACTION == 'deploy' }
            steps {
                sh '''
                    aws cloudformation create-stack \
                      --stack-name ${STACK_NAME} \
                      --template-body file://eks-cluster.yaml \
                      --parameters ParameterKey=ClusterName,ParameterValue=${CLUSTER_NAME} \
                      --capabilities CAPABILITY_NAMED_IAM \
                      --region ${REGION}
                    
                    aws cloudformation wait stack-create-complete \
                      --stack-name ${STACK_NAME} \
                      --region ${REGION}
                '''
            }
        }
        
        stage('Post-Deployment Setup') {
            when { params.ACTION == 'deploy' }
            steps {
                sh './post-deployment-setup.sh ${STACK_NAME} ${REGION}'
            }
        }
        
        stage('Verify Deployment') {
            when { params.ACTION == 'deploy' }
            steps {
                sh '''
                    kubectl get nodes
                    kubectl get pods --all-namespaces
                    kubectl top nodes
                '''
            }
        }
        
        stage('Destroy Infrastructure') {
            when { params.ACTION == 'destroy' }
            steps {
                sh '''
                    aws cloudformation delete-stack --stack-name ${STACK_NAME} --region ${REGION}
                    aws cloudformation wait stack-delete-complete --stack-name ${STACK_NAME} --region ${REGION}
                '''
            }
        }
    }
}
```

### Python Automation

```python
import boto3
import subprocess
import time
from typing import Dict, Any

class EKSWorkshopManager:
    def __init__(self, region: str = 'us-west-2'):
        self.region = region
        self.cf_client = boto3.client('cloudformation', region_name=region)
        self.eks_client = boto3.client('eks', region_name=region)
    
    def deploy_cluster(self, cluster_name: str) -> Dict[str, Any]:
        """Deploy EKS cluster using CloudFormation."""
        stack_name = f'eks-{cluster_name}'
        
        with open('eks-cluster.yaml', 'r') as f:
            template_body = f.read()
        
        # Create stack
        self.cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {'ParameterKey': 'ClusterName', 'ParameterValue': cluster_name},
                {'ParameterKey': 'Environment', 'ParameterValue': 'workshop'}
            ],
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
        
        # Wait for completion
        waiter = self.cf_client.get_waiter('stack_create_complete')
        waiter.wait(StackName=stack_name)
        
        # Run post-deployment setup
        subprocess.run(['./post-deployment-setup.sh', stack_name, self.region], check=True)
        
        # Get outputs
        outputs = self.cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs']
        return {output['OutputKey']: output['OutputValue'] for output in outputs}
    
    def destroy_cluster(self, cluster_name: str) -> None:
        """Destroy EKS cluster and all resources."""
        stack_name = f'eks-{cluster_name}'
        
        self.cf_client.delete_stack(StackName=stack_name)
        
        # Wait for deletion
        waiter = self.cf_client.get_waiter('stack_delete_complete')
        waiter.wait(StackName=stack_name)
    
    def get_cluster_status(self, cluster_name: str) -> str:
        """Get cluster status."""
        try:
            response = self.eks_client.describe_cluster(name=cluster_name)
            return response['cluster']['status']
        except self.eks_client.exceptions.ResourceNotFoundException:
            return 'NOT_FOUND'

# Usage example
if __name__ == "__main__":
    manager = EKSWorkshopManager()
    
    # Deploy cluster
    outputs = manager.deploy_cluster('workshop-demo')
    print(f"Cluster endpoint: {outputs['ClusterEndpoint']}")
    
    # Check status
    status = manager.get_cluster_status('workshop-demo')
    print(f"Cluster status: {status}")
    
    # Clean up (uncomment when ready)
    # manager.destroy_cluster('workshop-demo')
```

## 🧹 Complete Cleanup

### Destroy Everything

```bash
# Delete any remaining services with LoadBalancers
kubectl get services --all-namespaces -o wide | grep LoadBalancer
kubectl delete service SERVICE_NAME

# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name workshop-eks-cluster

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name workshop-eks-cluster

# Verify cleanup
aws eks list-clusters
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=*workshop*"
```

### Manual Cleanup (if needed)

```bash
# Clean up any orphaned resources
aws elbv2 describe-load-balancers --query 'LoadBalancers[?contains(LoadBalancerName, `k8s`)]'
aws ec2 describe-security-groups --filters "Name=group-name,Values=*k8s*"

# Remove kubectl context
kubectl config delete-context $(kubectl config current-context)
```

---

## 🎉 Workshop Success Checklist

When deployment is complete, verify:

✅ **CloudFormation stack** status is CREATE_COMPLETE  
✅ **EKS cluster** status is ACTIVE  
✅ **kubectl get nodes** shows 3 ready nodes  
✅ **kubectl get pods -n kube-system** shows all pods running  
✅ **AWS Load Balancer Controller** is deployed and ready  
✅ **Metrics Server** is running  
✅ **Sample application** can be deployed with LoadBalancer  
✅ **External URL** is accessible from browser  

Your enterprise-grade EKS cluster is ready for workshop demonstrations! 🚀

## 📋 Quick Reference Commands

```bash
# Deploy
aws cloudformation create-stack --stack-name workshop-eks-cluster --template-body file://eks-cluster.yaml --capabilities CAPABILITY_NAMED_IAM
./post-deployment-setup.sh workshop-eks-cluster us-west-2

# Test
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get service nginx

# Cleanup
kubectl delete service nginx
kubectl delete deployment nginx
aws cloudformation delete-stack --stack-name workshop-eks-cluster
```