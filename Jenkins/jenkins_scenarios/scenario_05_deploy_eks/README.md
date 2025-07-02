# 🚀 Scenario 5: EKS Deployment Testing

## Overview

Scenario 5 simulates real-world AWS EKS deployment chaos by testing both successful deployments and intentional failures. This enterprise-grade testing framework provides comprehensive reporting and integrates seamlessly with Jenkins CI/CD pipelines.

## 📁 File Structure

```
Jenkins/jenkins_scenarios/scenario_05_deploy_eks/
├── Dockerfile                          # Container for isolated testing
├── requirements.txt                    # Python dependencies
├── run_tests.py                       # Main test orchestrator
├── tests/
│   ├── test_deploy_eks_pass.py       # Successful deployment test
│   ├── test_deploy_eks_fail.py       # Chaos failure testing
│   └── deploy/
│       ├── deployment-pass.yaml      # Working Kubernetes manifests
│       ├── deployment-fail.yaml      # Intentionally broken manifests
│       ├── service.yaml              # Service configuration
│       └── configmap.yaml            # Application configuration
└── reports/                          # Generated test reports
    ├── eks_deployment_report.html    # Beautiful HTML report
    ├── eks_deployment_report.json    # Machine-readable results
    └── pytest_*.html                 # Individual test reports
```

## 🎯 Chaos Testing Scenarios

### PASS Test (`test_deploy_eks_pass.py`)
- ✅ Deploys working nginx application to EKS
- ✅ Validates pod readiness and health checks
- ✅ Tests service endpoint connectivity
- ✅ Captures deployment timeline and logs
- ✅ Verifies resource limits and configuration

### FAIL Test (`test_deploy_eks_fail.py`)
- 💥 Uses non-existent container image
- 💥 References missing ConfigMaps
- 💥 Implements aggressive health checks that fail
- 💥 Creates RBAC permission conflicts
- 💥 Captures failure events and remediation suggestions

## 🛠️ Prerequisites

### AWS EKS Cluster
```bash
# Ensure you have an EKS cluster running
aws eks describe-cluster --name your-cluster-name --region us-west-2

# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name your-cluster-name
```

### Required Tools
- `kubectl` (Kubernetes CLI)
- `aws` CLI v2
- Docker
- Python 3.11+

### AWS Permissions
Your AWS credentials need the following permissions:
- `eks:DescribeCluster`
- `eks:ListClusters`
- `eks:AccessKubernetesApi`
- Kubernetes RBAC permissions for the target namespace

### Jenkins Credentials
Set up these Jenkins credentials:
- `aws-credentials`: AWS Access Key ID and Secret
- `eks-kubeconfig`: Kubeconfig file for your EKS cluster

## 🚀 Quick Start

### 1. Local Testing

```bash
# Navigate to scenario directory
cd Jenkins/jenkins_scenarios/scenario_05_deploy_eks

# Install dependencies
pip install -r requirements.txt

# Run all tests
python run_tests.py

# Run only pass tests
python run_tests.py --pass-only

# Run only fail tests
python run_tests.py --fail-only
```

### 2. Docker Testing

```bash
# Build the container
docker build -t chaos-workshop-scenario-5 .

# Run tests with kubeconfig mounted
docker run --rm \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  -v $(pwd)/reports:/app/reports \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e AWS_DEFAULT_REGION=us-west-2 \
  chaos-workshop-scenario-5
```

### 3. Jenkins Integration

Add the Jenkinsfile snippet to your main pipeline and configure these parameters:
- `RUN_SCENARIO_5`: Enable/disable scenario
- `SCENARIO_5_PASS`: Run successful deployment test
- `SCENARIO_5_FAIL`: Run failure simulation test
- `EKS_CLUSTER_NAME`: Your EKS cluster name
- `AWS_REGION`: AWS region

## 📊 Report Features

### HTML Report Highlights
- **Executive Summary**: Pass/fail counts with visual indicators
- **Interactive Timeline**: Expandable deployment steps
- **Pod Status Table**: Real-time container health
- **Kubernetes Events**: Filtered warning and error events
- **Failure Analysis**: Automated root cause detection
- **Remediation Suggestions**: Actionable fix recommendations
- **Logs Integration**: Container and kubectl output

### JSON Report Structure
```json
{
  "scenario": "scenario_05_deploy_eks",
  "test_type": "PASS|FAIL",
  "status": "SUCCESS|FAILED|ERROR",
  "summary": {
    "total": 2,
    "passed": 1,
    "failed": 1,
    "errors": 0
  },
  "tests": [...],
  "deployment_timeline": [...],
  "pods": [...],
  "events": [...],
  "remediation_suggestions": [...]
}
```

## 🎭 Chaos Engineering Patterns

### Image Pull Failures
```yaml
# deployment-fail.yaml
image: nonexistent-registry.com/chaos-workshop/nonexistent-image:v1.0.0-broken
```

### Missing Dependencies
```yaml
# References non-existent ConfigMap
env:
- name: MISSING_CONFIG
  valueFrom:
    configMapKeyRef:
      name: nonexistent-configmap
      key: missing-key
```

### Aggressive Health Checks
```yaml
# Unrealistic probe settings
livenessProbe:
  httpGet:
    path: /health
    port: 8080  # Wrong port
  initialDelaySeconds: 1  # Too short
  periodSeconds: 1        # Too frequent
  failureThreshold: 1     # Too strict
```

### RBAC Issues
```yaml
# Non-existent service account
serviceAccountName: nonexistent-service-account
```

## 🔧 Configuration Options

### Environment Variables
- `AWS_ACCESS_KEY_ID`: AWS authentication
- `AWS_SECRET_ACCESS_KEY`: AWS authentication  
- `AWS_DEFAULT_REGION`: Target AWS region
- `KUBECONFIG`: Path to kubeconfig file
- `PYTHONPATH`: Python module search path

### Test Parameters
- `--pass-only`: Run only successful deployment tests
- `--fail-only`: Run only failure simulation tests
- `--skip-pass`: Skip successful deployment tests
- `--skip-fail`: Skip failure simulation tests

## 🛡️ Security Best Practices

### Container Security
- Non-root user execution
- Minimal base image (python:3.11-slim)
- Multi-stage build for smaller attack surface
- Health checks for container monitoring

### Credential Handling
- Credentials passed as environment variables
- No hardcoded secrets in code or containers
- Kubeconfig mounted read-only
- Automatic cleanup of temporary files

### Network Security
- Container runs with minimal network access
- kubectl communication over HTTPS
- AWS API calls use IAM credentials

## 🐛 Troubleshooting

### Common Issues

#### Cannot Connect to EKS Cluster
```bash
# Verify kubeconfig
kubectl cluster-info

# Check AWS credentials
aws sts get-caller-identity

# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name your-cluster
```

#### Permission Denied Errors
```bash
# Check RBAC permissions
kubectl auth can-i create deployments
kubectl auth can-i create services
kubectl auth can-i create configmaps
```

#### Container Build Failures
```bash
# Clean Docker cache
docker system prune -f

# Build with verbose output
docker build --no-cache --progress=plain -t chaos-workshop-scenario-5 .
```

#### Test Timeout Issues
```bash
# Increase timeout in run_tests.py
timeout=600  # 10 minutes

# Check cluster resources
kubectl top nodes
kubectl get events --sort-by='.lastTimestamp'
```

### Debug Mode
Enable detailed logging:
```python
# In test files
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Integration with Other Scenarios

Scenario 5 is designed to be completely isolated but integrates with the main workshop through:

### `run_all_scenarios.py` Integration
```python
# The main orchestrator can call scenario 5
if config.get('scenario_05_enabled'):
    result = run_scenario_05(config)
    results['scenario_05'] = result
```

### Report Aggregation
```json
{
  "workshop_summary": {
    "scenarios": {
      "scenario_05_deploy_eks": {
        "status": "PASSED",
        "duration": 120.5,
        "reports": ["eks_deployment_report.html"]
      }
    }
  }
}
```

## 📈 Metrics and Monitoring

### Key Performance Indicators
- **Deployment Time**: Time to successful rollout
- **Recovery Time**: Time to detect and report failures
- **Error Detection Rate**: Percentage of intentional failures caught
- **False Positive Rate**: Healthy deployments marked as failed

### Alerting Triggers
- Test execution duration > 10 minutes
- Cluster connectivity failures
- Unexpected test failures (PASS test failing)
- Missing expected failures (FAIL test passing)

## 🚀 Advanced Usage

### Custom Failure Scenarios
Create additional failure modes by modifying `deployment-fail.yaml`:
```yaml
# Resource exhaustion
resources:
  requests:
    memory: "16Gi"  # More than node capacity
    cpu: "8000m"    # More than node capacity

# Anti-affinity conflicts
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: chaos-workshop-app
      topologyKey: kubernetes.io/hostname
```

### Extended Monitoring
```python
# Add custom metrics collection
def collect_cluster_metrics(self):
    # Node resource usage
    # Pod distribution
    # Network latency
    # Storage performance
```

### Multi-Cluster Testing
```bash
# Test across multiple EKS clusters
export KUBECONFIG=cluster1.config:cluster2.config:cluster3.config
kubectl config get-contexts
```

## 📚 Educational Objectives

This scenario teaches participants:

### Kubernetes Fundamentals
- Deployment lifecycle management
- Service networking and exposure
- ConfigMap and secret handling
- Resource limits and requests
- Health checks and probes

### DevOps Practices
- Infrastructure as Code with YAML
- Automated testing strategies
- Failure simulation and chaos engineering
- Monitoring and observability
- Incident response procedures

### AWS EKS Specifics
- Cluster authentication and authorization
- Integration with AWS services
- Networking and security groups
- Auto-scaling and node management
- Cost optimization strategies

## 🤝 Contributing

To extend Scenario 5:

1. Add new failure modes in `deploy/` directory
2. Extend test classes with additional validations
3. Enhance HTML reporting with new visualizations
4. Add integration tests for different Kubernetes versions
5. Implement multi-region testing capabilities

## 📄 License

This scenario is part of the CI/CD Chaos Workshop and follows the same licensing terms as the main project.

---

**Ready to chaos test your EKS deployments? 🚀**

Start with `python run_tests.py` and watch the beautiful reports unfold!