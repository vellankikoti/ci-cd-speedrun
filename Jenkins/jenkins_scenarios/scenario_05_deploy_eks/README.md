## ✅ Success Criteria

You've successfully completed Scenario 5 when:

✅ **Authentication Works**: Jenkins can authenticate to AWS and access EKS cluster  
✅ **Container Builds**: Docker image builds successfully with AWS CLI and kubectl  
✅ **Pass Scenario**: Successful deployment completes without errors  
✅ **Fail Scenario**: Chaos deployment demonstrates proper failure handling  
✅ **Live Monitoring**: Real-time kubectl commands show cluster status  
✅ **Troubleshooting**: You can interpret kubectl output and debug issues  
✅ **Cleanup**: Resources are properly cleaned up after tests  

### 🎯 Workshop Learning Outcomes

After completing this scenario, attendees understand:

- **Containerized CI/CD**: How to use Docker containers for consistent deployments
- **EKS Integration**: Real-world Kubernetes deployment patterns
- **Chaos Engineering**: Intentional failure testing and recovery
- **kubectl Mastery**: Essential commands for Kubernetes troubleshooting
- **Security**: AWS credential management in CI/CD pipelines
- **Monitoring**: Live deployment monitoring and event analysis

---

## 🎉 Advanced Extensions

Ready for more challenges? Try these extensions:

### 🔄 Blue/Green Deployments
```bash
# Modify manifests to support blue/green deployments
# Add service selector switching
# Implement zero-downtime deployments
```

### 📊 Monitoring Integration
```bash
# Add Prometheus metrics collection
# Create Grafana dashboards
# Set up AlertManager rules
```

### 🔐 Security Enhancements
```bash
# Implement RBAC policies
# Add Pod Security Standards
# Configure Network Policies
```

### 🌐 Multi-Cluster Deployments
```bash
# Extend to deploy across multiple clusters
# Add region failover scenarios
# Implement cross-cluster networking
```

---

## 📚 Additional Resources

### Documentation Links
- [AWS EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/dockerfile_best-practices/)

### Sample Commands Reference

```bash
# EKS Cluster Management
aws eks list-clusters --region us-east-1
aws eks describe-cluster --name cluster-name --region us-east-1
aws eks update-kubeconfig --region us-east-1 --name cluster-name

# Kubernetes Deployment Commands
kubectl apply -f deployment.yaml
kubectl get deployments -o wide
kubectl describe deployment app-name
kubectl rollout status deployment/app-name
kubectl rollout history deployment/app-name

# Pod Management
kubectl get pods -l app=app-name -o wide
kubectl describe pod pod-name
kubectl logs pod-name --follow
kubectl exec -it pod-name -- /bin/bash

# Service and Networking
kubectl get services -o wide
kubectl describe service service-name
kubectl get endpoints
kubectl port-forward service/app-service 8080:80

# Troubleshooting Commands
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get events --field-selector type=Warning
kubectl top nodes
kubectl top pods

# Container and Image Management
docker build -t app:tag .
docker run --rm -it app:tag /bin/bash
docker logs container-id
docker exec -it container-id /bin/bash
```

---

## 🎯 Workshop Facilitation Tips

### For Instructors

**Timing Recommendations:**
- **Setup & Authentication**: 10-15 minutes
- **Pass Scenario Walkthrough**: 15-20 minutes  
- **Fail Scenario Deep Dive**: 20-25 minutes
- **Troubleshooting Practice**: 15-20 minutes
- **Q&A and Wrap-up**: 10-15 minutes

**Key Teaching Moments:**
1. **Authentication Flow**: Explain AWS IAM → EKS → kubectl chain
2. **Container Benefits**: Show how containerized tools ensure consistency
3. **Failure Analysis**: Walk through kubectl commands during fail scenario
4. **Real-world Parallels**: Connect chaos testing to production scenarios

### For Attendees

**Focus Areas:**
- Understand the kubectl command patterns
- Learn to read Kubernetes events and pod descriptions
- Practice troubleshooting failed deployments
- Recognize common deployment failure modes

**Hands-on Practice:**
- Run the authentication pipeline first
- Watch the console output carefully during both scenarios
- Try modifying the deployment manifests
- Experiment with kubectl commands

---

## 🔧 Customization Options

### Environment Variables

You can customize the scenario by modifying these environment variables in the Jenkinsfile:

```groovy
environment {
    SCENARIO_5_PATH = "Jenkins/jenkins_scenarios/scenario_05_deploy_eks"
    SCENARIO_5_IMAGE = "chaos-workshop-scenario-5:${BUILD_NUMBER}"
    AWS_PAGER = ""
    AWS_CLI_AUTO_PROMPT = "off"
}
```

### Parameter Modifications

Adjust default values in the parameters section:

```groovy
parameters {
    string(
        name: 'CLUSTER_NAME',
        defaultValue: 'your-cluster-name',  // Customize this
        description: 'EKS cluster name to deploy to'
    )
    choice(
        name: 'AWS_REGION',
        choices: ['us-east-1', 'your-region'],  // Add your regions
        description: 'AWS region for EKS cluster'
    )
}
```

### Custom Deployment Manifests

Create additional failure scenarios by modifying `deployment-fail.yaml`:

```yaml
# Example: Memory limit chaos
resources:
  limits:
    memory: "1Mi"  # Impossibly low limit
  requests:
    memory: "100Mi"

# Example: Invalid probe chaos
livenessProbe:
  httpGet:
    path: /nonexistent-endpoint
    port: 9999  # Wrong port
```

---

## 🚨 Important Notes

### Security Considerations

⚠️ **Credential Management**
- Never hardcode AWS credentials in Jenkinsfiles
- Use Jenkins credential store for secure credential handling
- Rotate credentials regularly

⚠️ **Container Security**
- The Dockerfile uses non-root user for running applications
- AWS CLI and kubectl run with appropriate permissions
- Consider using IAM roles for production deployments

⚠️ **Cluster Access**
- Test pipelines should use dedicated test clusters
- Implement proper RBAC for production environments
- Monitor and audit kubectl access

### Production Considerations

🏭 **Scaling for Production**
- Use dedicated Jenkins agents for Kubernetes deployments
- Implement proper resource quotas and limits
- Add monitoring and alerting for deployment failures
- Consider using GitOps tools like ArgoCD or Flux

🏭 **Multi-Environment Support**
- Extend parameters to support dev/staging/prod environments
- Implement environment-specific configuration management
- Add approval gates for production deployments

---

## 🐛 Known Issues and Workarounds

### Issue 1: aws-auth ConfigMap Access

**Problem:** New AWS users may not have kubectl access initially

**Workaround:** The JenkinsAuth pipeline will show your ARN - add it to the cluster's aws-auth ConfigMap

### Issue 2: Docker Layer Caching

**Problem:** Docker builds may be slow on first run

**Workaround:** The multi-stage Dockerfile is optimized for layer caching on subsequent builds

### Issue 3: EKS Cluster Warmup

**Problem:** Cold EKS clusters may take longer for first deployment

**Workaround:** Allow extra time for the first scenario run after cluster creation

---

**🔥 Chaos Agent Status: COMPLETELY DEFEATED! 🔥**

**Your EKS deployment pipeline is now bulletproof against chaos! You've mastered:**

✅ Containerized CI/CD pipelines  
✅ AWS and Kubernetes authentication  
✅ Real-time deployment monitoring  
✅ Chaos engineering principles  
✅ Production-ready troubleshooting skills  

---

*Ready to deploy with confidence! 🚀⚡*

---

## 📞 Support and Troubleshooting

If you encounter issues not covered in this guide:

1. **Check the console output** - Most issues are visible in the Jenkins build logs
2. **Verify prerequisites** - Ensure all required tools and permissions are configured
3. **Test authentication first** - Use the JenkinsAuth pipeline to validate setup
4. **Review the Dockerfile** - Understand what tools are available in the container
5. **Check cluster status** - Verify your EKS cluster is healthy and accessible

**Happy chaos engineering! May your deployments be resilient and your troubleshooting swift! 🎯🔧**# 🚀 Scenario 5: Deploy to EKS - Complete Guide

> **"Chaos Agent's Final Stand: Can your pipeline survive EKS deployment chaos?"**

Welcome to **Scenario 5** of the CI/CD Chaos Workshop! This scenario demonstrates real-world EKS deployment chaos testing with both **successful** and **failing** deployments to help you master Kubernetes troubleshooting.

---

## 🎯 What You'll Learn

✅ Deploy Python apps to AWS EKS clusters using containerized pipelines  
✅ Handle deployment failures with chaos engineering principles  
✅ Authenticate Jenkins with AWS and Kubernetes securely  
✅ Monitor live Kubernetes deployments in real-time  
✅ Troubleshoot common EKS deployment issues  
✅ Master pass/fail scenario testing with kubectl  

---

## 📋 Prerequisites

### 🔧 Required Tools

Your workshop environment needs:

- **Jenkins** (with Docker support)
- **Docker** (for containerized deployments)
- **AWS EKS Cluster** (already provisioned)
- **AWS CLI** v2.x (installed in container)
- **kubectl** (installed in container)

### 🔌 Required Jenkins Plugins

Install these plugins in Jenkins:

```bash
# Essential plugins
- Pipeline
- Docker Pipeline
- AWS Credentials
- Credentials Binding
```

**Installation via Jenkins CLI:**
```bash
jenkins-cli.jar install-plugin pipeline-stage-view docker-workflow aws-credentials-plugin credentials-binding
```

### 🔐 AWS Permissions Required

Your AWS user/role needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:DescribeCluster",
                "eks:ListClusters",
                "eks:AccessKubernetesApi"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

### ⚙️ EKS Cluster Requirements

- **EKS Cluster**: Pre-provisioned (default: `eks-cf-stack-eks-cluster`)
- **Node Groups**: At least 1 node group with capacity for test workloads
- **aws-auth ConfigMap**: Your AWS user/role must be configured for kubectl access

---

## 🛠️ Setup Instructions

### Step 1: Configure AWS Credentials in Jenkins

1. Go to **Jenkins Dashboard** → **Manage Jenkins** → **Credentials**
2. Click **Global** → **Add Credentials**
3. Select **Username with password** and configure:
   - **ID**: `aws-credentials`
   - **Username**: Your AWS Access Key ID
   - **Password**: Your AWS Secret Access Key

### Step 2: Configure Pipeline Parameters

Create a Jenkins Pipeline job with these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `CLUSTER_NAME` | String | `eks-cf-stack-eks-cluster` | EKS cluster name |
| `AWS_REGION` | Choice | `us-east-1, us-west-2, us-east-2, eu-west-1` | AWS region |
| `RUN_SCENARIO_5` | Boolean | `true` | Enable Scenario 5 execution |
| `SCENARIO_5_PASS` | Boolean | `true` | Run successful deployment test |
| `SCENARIO_5_FAIL` | Boolean | `true` | Run chaos/failure deployment test |
| `CLEANUP_AFTER_TESTS` | Boolean | `true` | Clean up resources after tests |

---

## 🏗️ Project Structure

Your scenario directory should look like this:

```
Jenkins/jenkins_scenarios/scenario_05_deploy_eks/
├── Dockerfile                    # Multi-stage container with AWS CLI & kubectl
├── requirements.txt              # Python dependencies
├── run_tests.py                 # Main test execution script
├── tests/
│   └── deploy/
│       ├── deployment-pass.yaml  # Working deployment manifest
│       ├── deployment-fail.yaml  # Intentionally broken deployment
│       ├── service.yaml          # Kubernetes service
│       └── configmap.yaml        # Application configuration
├── JenkinsAuth                   # Authentication validation pipeline
└── Jenkinsfile                   # Main scenario pipeline
```

---

## 🐳 Docker Container Details

### Multi-Stage Build Features

The `Dockerfile` creates a production-ready container with:

✅ **AWS CLI v2** (architecture-aware installation)  
✅ **kubectl** (latest stable version)  
✅ **Python 3.11** runtime  
✅ **Security**: Non-root user execution  
✅ **Optimization**: Multi-stage build for minimal size  

### Container Capabilities

```bash
# The container can execute:
- AWS CLI commands (sts, eks operations)
- kubectl commands (deployments, services, monitoring)
- Python test scripts with pytest
- JSON/YAML processing with jq
```

---

## 🔧 Jenkins Pipeline Execution

### Main Pipeline Stages

The `Jenkinsfile` executes these stages:

1. **Checkout & Preparation**
   - Verifies scenario directory structure
   - Validates required files (Dockerfile, tests, manifests)
   - Creates reports directory

2. **Build Docker Image**
   - Builds the multi-stage container: `chaos-workshop-scenario-5:${BUILD_NUMBER}`
   - Verifies successful build

3. **Setup AWS & Kubernetes**
   - Authenticates with AWS using stored credentials
   - Generates kubeconfig using containerized AWS CLI
   - Creates kubeconfig file for kubectl access

4. **Live Kubernetes Monitoring**
   - Displays cluster overview and node status
   - Lists existing namespaces, deployments, and pods
   - Shows services and configmaps

5. **Deploy & Monitor PASS Test** (if `SCENARIO_5_PASS=true`)
   - Deploys successful application using `deployment-pass.yaml`
   - Monitors deployment progress in real-time
   - Validates pod and service status

6. **Deploy & Monitor FAIL Test** (if `SCENARIO_5_FAIL=true`)
   - Cleans up previous deployments
   - Deploys broken application using `deployment-fail.yaml`
   - Demonstrates troubleshooting commands
   - Shows failure scenarios and error events

7. **Cleanup** (if `CLEANUP_AFTER_TESTS=true`)
   - Removes test deployments, services, and configmaps
   - Cleans up cluster resources

### Authentication Test Pipeline

The `JenkinsAuth` pipeline validates your setup:

```groovy
// Use this to test your AWS and EKS authentication
pipeline {
    agent {
        docker {
            image 'amazon/aws-cli:latest'
            args '-u root:root --entrypoint=""'
        }
    }
    
    stages {
        stage('AWS Authentication') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        # Test AWS connection
                        aws sts get-caller-identity
                        
                        # Check EKS cluster access
                        aws eks describe-cluster --name ${CLUSTER_NAME} --region ${AWS_REGION}
                        
                        # Generate kubeconfig
                        aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
                        
                        # Test kubectl (may fail if aws-auth not configured)
                        kubectl cluster-info || echo "kubectl access requires aws-auth configuration"
                    '''
                }
            }
        }
    }
}
```

---

## 📊 Deployment Scenarios

### ✅ Pass Scenario (`SCENARIO_5_PASS=true`)

Uses `deployment-pass.yaml` with:
- ✅ **Valid container image**: `nginx:latest`
- ✅ **Proper resource limits**: CPU and memory configured
- ✅ **Health checks**: Readiness and liveness probes
- ✅ **Correct environment variables**: All required env vars set
- ✅ **Service integration**: Proper label selectors

**Expected Outcome:**
- Deployment succeeds within 30 seconds
- Pods reach `Running` state
- Service endpoints are accessible
- No error events in Kubernetes

### ❌ Fail Scenario (`SCENARIO_5_FAIL=false`)

Uses `deployment-fail.yaml` with intentional chaos:
- ❌ **Invalid image**: `nonexistent-image:broken`
- ❌ **Resource conflicts**: Insufficient memory limits
- ❌ **Missing environment variables**: Required env vars undefined
- ❌ **Broken health checks**: Invalid probe endpoints

**Expected Chaos:**
- ImagePullBackOff errors
- Pod crashes and restarts
- Service endpoints unreachable
- Warning events in Kubernetes logs

### 🔍 Real-Time Monitoring

Both scenarios include live monitoring:

```bash
# Monitoring commands executed in pipeline:
kubectl get deployments -o wide
kubectl get pods -l app=chaos-workshop-app -o wide
kubectl describe deployment chaos-workshop-app
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl rollout status deployment/chaos-workshop-app
```

---

## 📈 Reports and Artifacts

### Archived Artifacts

After each pipeline run, Jenkins archives:

1. **kubeconfig** - Generated EKS cluster configuration
2. **environment-summary.json** - Build metadata and configuration
3. **reports/** directory - All generated reports (if any)

### Accessing Artifacts

1. **In Jenkins UI:**
   - Go to your build → **Build Artifacts** section
   - Download individual files or browse directories

2. **Via Jenkins API:**
```bash
# Get build artifacts
curl -X GET "http://jenkins-url/job/scenario-5-eks/${BUILD_NUMBER}/api/json?tree=artifacts[*]"

# Download specific artifact
curl -X GET "http://jenkins-url/job/scenario-5-eks/${BUILD_NUMBER}/artifact/kubeconfig"
```

### Live Console Output

The pipeline provides real-time monitoring output including:

- 🔍 **Cluster Overview**: Nodes, namespaces, existing resources
- 📊 **Deployment Status**: Real-time deployment progress
- 🐳 **Pod Monitoring**: Pod status, restarts, and events
- 🌐 **Service Status**: Service endpoints and connectivity
- 📜 **Event Logs**: Kubernetes events and error messages
- 🔧 **Troubleshooting Commands**: kubectl commands for debugging

---

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

#### 1. AWS Authentication Failed

**Error:** `Unable to locate credentials` or `InvalidUserID.NotFound`

**Solution:**
```bash
# Verify Jenkins credentials
# In Jenkins: Manage Jenkins → Credentials → Check 'aws-credentials'

# Test authentication in JenkinsAuth pipeline
# Expected output: Your AWS ARN and account ID
```

#### 2. EKS Cluster Access Denied

**Error:** `error: You must be logged in to the server (Unauthorized)`

**Root Cause:** Your AWS user/role is not in the EKS cluster's `aws-auth` ConfigMap

**Solution:**
```bash
# Your pipeline shows your ARN - add it to aws-auth ConfigMap
# Example ARN: arn:aws:iam::123456789012:user/jenkins-user

# Add to aws-auth ConfigMap in EKS cluster:
kubectl edit configmap aws-auth -n kube-system

# Add your user to mapUsers section:
mapUsers: |
  - userarn: arn:aws:iam::123456789012:user/jenkins-user
    username: jenkins-user
    groups:
      - system:masters
```

#### 3. Docker Build Fails

**Error:** `docker: command not found` or `permission denied`

**Solution:**
```bash
# Ensure Docker is available in Jenkins
# Check Jenkins Docker configuration
# Verify Jenkins user has Docker permissions:
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### 4. EKS Cluster Not Found

**Error:** `ResourceNotFoundException: No cluster found for name: xyz`

**Solution:**
```bash
# Verify cluster name and region parameters
# Check if cluster exists:
aws eks list-clusters --region us-east-1

# Update CLUSTER_NAME parameter in Jenkins job
```

#### 5. kubectl Commands Fail in Container

**Error:** `kubectl: command not found` or `connection refused`

**Solution:**
```bash
# The Dockerfile installs kubectl automatically
# Check if kubeconfig is properly generated
# Verify AWS credentials are passed to container
```

#### 6. ImagePullBackOff in Fail Scenario

**Expected Behavior:** This is intentional chaos!

**What It Demonstrates:**
- How to identify image pull failures
- Reading pod events and descriptions
- Understanding Kubernetes failure modes
- Using kubectl for troubleshooting

#### 7. Pass Scenario Deployment Timeout

**Error:** `deployment "chaos-workshop-app" exceeded its progress deadline`

**Solution:**
```bash
# Check node capacity
kubectl get nodes -o wide

# Check pod events
kubectl describe pods -l app=chaos-workshop-app

# Verify image availability
docker pull nginx:latest
```

### Debug Commands Reference

Use these commands to troubleshoot issues:

```bash
# AWS connectivity
aws sts get-caller-identity
aws eks describe-cluster --name your-cluster

# Kubernetes cluster info
kubectl cluster-info
kubectl get nodes -o wide

# Pod debugging
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Deployment status
kubectl get deployments
kubectl describe deployment <deployment-name>
kubectl rollout status deployment/<deployment-name>

# Service debugging
kubectl get services
kubectl describe service <service-name>
kubectl get endpoints

# Event monitoring
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get events --field-selector type=Warning
```

---

## 🚀 Quick Start Guide

### Step 1: Verify Prerequisites
```bash
# Check your EKS cluster exists
aws eks list-clusters --region us-east-1

# Verify cluster details
aws eks describe-cluster --name eks-cf-stack-eks-cluster --region us-east-1
```

### Step 2: Setup Jenkins Job

1. **Create New Pipeline Job**
   - Jenkins Dashboard → New Item → Pipeline

2. **Configure Parameters** (copy from section above)

3. **Add Pipeline Script**
   - Choose "Pipeline script from SCM"
   - Point to your repository
   - Specify path: `Jenkins/jenkins_scenarios/scenario_05_deploy_eks/Jenkinsfile`

### Step 3: Test Authentication

1. **Create JenkinsAuth Pipeline**
   - Use the `JenkinsAuth` file as pipeline script
   - Run to verify AWS and EKS access

2. **Expected Success Output:**
```bash
✅ AWS authentication successful!
👤 Your AWS ARN: arn:aws:iam::123456789012:user/your-user
✅ kubectl access successful! (or expected auth warning)
```

### Step 4: Run Full Scenario

1. **Execute Main Pipeline**
   - Set parameters as needed
   - Run with both PASS and FAIL tests enabled

2. **Monitor Progress**
   - Watch console output for real-time monitoring
   - Observe chaos engineering in action

### Step 5: Review Results

1. **Check Build Artifacts**
   - Download kubeconfig
   - Review environment summary

2. **Analyze Console Output**
   - Study pass vs. fail deployment differences
   - Learn troubleshooting commands

---

## 📚 Additional Resources

### Useful Links

- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Jenkins Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

### Sample Commands Reference

```bash
# AWS EKS Commands
aws eks list-clusters
aws eks describe-cluster --name cluster-name
aws eks update-kubeconfig --name cluster-name

# Kubernetes Commands
kubectl get deployments
kubectl get services
kubectl get pods
kubectl logs deployment/app
kubectl describe deployment app

# Docker Commands
docker build -t app:latest .
docker run --rm app:latest
docker images
docker ps
```

---

## ✅ Success Criteria

You've successfully completed Scenario 5 when:

✅ Jenkins can authenticate to AWS and EKS  
✅ Docker images build successfully  
✅ Pass scenario deploys without errors  
✅ Fail scenario demonstrates proper error handling  
✅ HTML and JSON reports are generated  
✅ You can troubleshoot common deployment issues  

---

## 🎉 Next Steps

After mastering Scenario 5:

1. **Explore Advanced Features:**
   - Blue/green deployments
   - Canary releases
   - Multi-cluster deployments

2. **Security Enhancements:**
   - RBAC configuration
   - Pod security policies
   - Network policies

3. **Monitoring Integration:**
   - Prometheus metrics
   - Grafana dashboards
   - AlertManager rules

---

**🔥 Chaos Agent Status: DEFEATED! Your EKS deployment pipeline is bulletproof! 🔥**

---

*Happy deploying! 🚀*