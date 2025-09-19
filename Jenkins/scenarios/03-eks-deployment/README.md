# EKS Cluster Deployment - Jenkins Workshop

Deploy and manage AWS EKS clusters with cost optimization for workshop demonstrations.

## Overview

This scenario demonstrates how to deploy a cost-optimized EKS cluster using Jenkins with the following features:

- **Parameterized deployment** with customizable cluster name, node type, and region
- **Cost optimization** with t3.small instances and single NAT Gateway
- **Automated setup** including kubectl configuration and essential add-ons
- **Connection management** with generated kubeconfig and AWS CLI commands
- **Workshop-ready** with comprehensive documentation and test suite

## Features

### 🚀 **Parameterized Deployment**
- **Cluster Name**: Customizable (default: `eks-demo-cluster`)
- **Node Instance Type**: t3.small, t3.medium, t3.large (t3.small for cost optimization)
- **Node Count**: 1-10 nodes (default: 3)
- **AWS Region**: Any supported region (default: us-west-2)
- **Logging**: Optional EKS control plane logging
- **ALB Controller**: Optional AWS Load Balancer Controller installation

### 💰 **Cost Optimization**
- **Single NAT Gateway** instead of multiple (saves ~$45/month)
- **t3.small instances** as default (cost-effective for workshops)
- **Minimal resource allocation** while maintaining functionality
- **Estimated cost**: ~$50-80/month for 3-node cluster

### 🔧 **Automated Setup**
- **EKS Cluster** with managed node groups
- **kubectl configuration** with automatic kubeconfig generation
- **Essential add-ons**: EBS CSI Driver, Metrics Server
- **Storage classes**: Default gp3 encrypted storage
- **Security**: Proper IAM roles and security groups

### 📋 **Connection Management**
- **Generated connection info** with all necessary commands
- **AWS CLI commands** for cluster access
- **kubectl commands** for cluster management
- **Test commands** for validation

## Files

- `Jenkinsfile` - Parameterized Jenkins pipeline with EKS deployment stages
- `eks-cluster-cost-optimized.yaml` - Cost-optimized CloudFormation template
- `eks_manager.py` - Python script for cluster management and configuration
- `Dockerfile` - Container definition for the pipeline
- `requirements.txt` - Python dependencies
- `tests/` - Comprehensive test suite

## Prerequisites

### AWS Requirements
- **AWS CLI** configured with appropriate credentials
- **kubectl** installed and configured
- **eksctl** installed (for OIDC provider setup)
- **Helm** installed (for add-on installation)
- **IAM permissions** for EKS, EC2, IAM, and CloudFormation

### Required IAM Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:*",
                "ec2:*",
                "iam:*",
                "cloudformation:*",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

### Local Tools
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Usage

### 🏭 **Production Jenkins Job Setup**

#### Quick Setup (Workshop Mode)
```bash
# 1. Clone the repository
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop

# 2. Start Jenkins (one command!)
cd Jenkins
python3 setup-jenkins-complete.py setup

# 3. Access Jenkins
# Open http://localhost:8080
# Complete the setup wizard

# 4. Run the pre-configured workshop job
# Click "🎓 Workshop - 03 EKS Deployment" → "Build with Parameters"
```

#### Manual Jenkins Job Creation (Production Mode)

##### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `03 EKS Deployment - Production`
4. **Select "Pipeline"** and click "OK"

##### Step 2: Configure Pipeline
1. **Description**: "Cost-optimized EKS cluster deployment with parameterized configuration"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/03-eks-deployment/Jenkinsfile`

##### Step 3: Configure Build Triggers (Optional)
- **GitHub hook trigger for GITScm polling** (if using webhooks)
- **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

##### Step 4: Configure Build Environment (Optional)
- **Delete workspace before build starts**
- **Add timestamps to the Console Output**

##### Step 5: Save and Run
1. **Click "Save"**
2. **Click "Build with Parameters"**
3. **Configure parameters**:
   - **CLUSTER_NAME**: `my-workshop-cluster` (or leave default)
   - **NODE_INSTANCE_TYPE**: `t3.small` (for cost optimization)
   - **AWS_REGION**: `us-west-2` (or your preferred region)
   - **NODE_COUNT**: `3` (or adjust as needed)
   - **ENABLE_LOGGING**: `true` (recommended)
   - **ENABLE_ALB_CONTROLLER**: `true` (recommended)
4. **Click "Build"**
5. **Monitor the pipeline execution**

### 🖥️ **Local Development and Testing**

#### Run Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_eks_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=eks_manager --cov-report=html
```

#### Manual EKS Deployment
```bash
# Deploy cluster
python eks_manager.py deploy \
    --cluster-name my-test-cluster \
    --stack-name my-test-stack \
    --region us-west-2 \
    --node-instance-type t3.small \
    --node-count 3 \
    --enable-logging \
    --enable-alb-controller

# Configure kubectl
python eks_manager.py configure-kubectl \
    --cluster-name my-test-cluster \
    --region us-west-2

# Run post-deployment setup
python eks_manager.py post-deploy \
    --cluster-name my-test-cluster \
    --stack-name my-test-stack \
    --region us-west-2

# Generate connection info
python eks_manager.py generate-connection-info \
    --cluster-name my-test-cluster \
    --region us-west-2 \
    --output-file connection-info.txt
```

### 🐳 **Docker Usage**

#### Build and Run Locally
```bash
# Build Docker image
docker build -t jenkins-eks-workshop .

# Run with AWS credentials
docker run -it --rm \
    -v ~/.aws:/root/.aws:ro \
    -e AWS_PROFILE=default \
    jenkins-eks-workshop

# Run specific command
docker run -it --rm \
    -v ~/.aws:/root/.aws:ro \
    -e AWS_PROFILE=default \
    jenkins-eks-workshop \
    python eks_manager.py deploy --cluster-name test-cluster --stack-name test-stack
```

## Pipeline Stages Overview

The Jenkinsfile includes these production-ready stages:

1. **Checkout Code** - Fetches source code from GitHub
2. **Validate Prerequisites** - Checks AWS CLI, kubectl, eksctl, and Helm installation
3. **Build Docker Image** - Creates containerized environment
4. **Run Tests** - Executes comprehensive test suite
5. **Deploy EKS Cluster** - Creates cost-optimized EKS cluster using CloudFormation
6. **Configure kubectl** - Sets up kubectl access and verifies connectivity
7. **Post-Deployment Setup** - Installs essential add-ons and configures storage
8. **Generate Connection Info** - Creates detailed connection instructions

## Configuration Parameters

### Jenkins Pipeline Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `CLUSTER_NAME` | String | `eks-demo-cluster` | Name of the EKS cluster |
| `NODE_INSTANCE_TYPE` | Choice | `t3.small` | EC2 instance type for worker nodes |
| `AWS_REGION` | String | `us-west-2` | AWS region for deployment |
| `NODE_COUNT` | String | `3` | Number of worker nodes |
| `ENABLE_LOGGING` | Boolean | `true` | Enable EKS control plane logging |
| `ENABLE_ALB_CONTROLLER` | Boolean | `true` | Install AWS Load Balancer Controller |

### Cost Optimization Features

- **Single NAT Gateway**: Reduces costs by ~$45/month compared to multi-AZ NAT
- **t3.small instances**: Cost-effective for workshop environments
- **Minimal resource allocation**: Only essential resources created
- **Spot instance support**: Can be configured for additional savings

## Monitoring and Debugging

### View Pipeline Progress
- Go to the job page
- Click on the build number
- View "Pipeline Steps" for detailed execution

### Check Logs
- Click on any stage to see detailed logs
- Use "Console Output" for full build log

### View Reports
- **Test Results**: JUnit test reports
- **Coverage Report**: Code coverage metrics
- **Connection Info**: Detailed cluster access instructions

### Troubleshooting
```bash
# Check Jenkins container logs
docker logs jenkins-workshop

# Check AWS credentials
aws sts get-caller-identity

# Verify kubectl configuration
kubectl config current-context

# Check EKS cluster status
aws eks describe-cluster --name <cluster-name> --region <region>

# View CloudFormation stack status
aws cloudformation describe-stacks --stack-name <stack-name> --region <region>
```

## Advanced Configuration

### Environment Variables
Configure these in Jenkins → Manage Jenkins → Configure System → Global Properties:

- `AWS_DEFAULT_REGION`: Default AWS region
- `AWS_PROFILE`: AWS profile to use
- `KUBECONFIG`: Path to kubeconfig file
- `HELM_HOME`: Helm configuration directory

### Credentials Setup
1. **Jenkins → Manage Jenkins → Manage Credentials**
2. **Add credentials for**:
   - AWS access keys or IAM roles
   - Docker registry access (if using private registry)
   - GitHub access (if using private repositories)

### Webhook Configuration (Optional)
1. **GitHub Repository → Settings → Webhooks**
2. **Add webhook**: `http://your-jenkins-url/github-webhook/`
3. **Select events**: "Just the push event"
4. **Test webhook** to ensure connectivity

## Cost Management

### Estimated Monthly Costs (us-west-2)
- **EKS Control Plane**: ~$73/month
- **3x t3.small nodes**: ~$30/month
- **NAT Gateway**: ~$45/month
- **EBS Storage**: ~$10/month
- **Total**: ~$158/month

### Cost Optimization Tips
1. **Use Spot instances** for non-critical workloads
2. **Scale down nodes** when not in use
3. **Use smaller instance types** for development
4. **Enable cluster autoscaler** for dynamic scaling
5. **Monitor costs** with AWS Cost Explorer

### Cleanup Commands
```bash
# Delete EKS cluster (via CloudFormation)
aws cloudformation delete-stack --stack-name <stack-name> --region <region>

# Delete cluster directly (if CloudFormation fails)
aws eks delete-cluster --name <cluster-name> --region <region>

# Clean up IAM roles
aws iam delete-role --role-name <cluster-name>-alb-controller-role
aws iam delete-role --role-name <cluster-name>-ebs-csi-driver-role
```

## Security Considerations

### IAM Roles and Policies
- **Least privilege access** for all IAM roles
- **Service-linked roles** for AWS services
- **OIDC provider** for pod-level permissions
- **Encrypted storage** with gp3 volumes

### Network Security
- **Private subnets** for worker nodes
- **Public subnets** for load balancers
- **Security groups** with minimal required access
- **NAT Gateway** for outbound internet access

### Cluster Security
- **RBAC** enabled with proper role bindings
- **Pod Security Standards** (if supported)
- **Network policies** for micro-segmentation
- **Image scanning** (if using ECR)

## Workshop Integration

### Demo Scripts
```bash
# Quick cluster deployment
python eks_manager.py deploy --cluster-name workshop-demo --stack-name workshop-demo-stack

# Generate demo connection info
python eks_manager.py generate-connection-info --cluster-name workshop-demo --output-file demo-connection.txt

# Deploy sample application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services
```

### Workshop Scenarios
1. **Basic Deployment**: Deploy cluster with default parameters
2. **Cost Optimization**: Compare different instance types
3. **Scaling**: Demonstrate node scaling capabilities
4. **Add-ons**: Show essential add-on installation
5. **Troubleshooting**: Common issues and solutions

## Support and Resources

### Documentation
- [EKS User Guide](https://docs.aws.amazon.com/eks/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/)

### Community
- [Kubernetes Slack](https://kubernetes.slack.com/)
- [AWS EKS Community](https://github.com/aws/containers-roadmap)
- [Jenkins Community](https://community.jenkins.io/)

### Issues and Contributions
- **Report issues**: Create GitHub issues for bugs or feature requests
- **Contribute**: Submit pull requests for improvements
- **Documentation**: Help improve documentation and examples
