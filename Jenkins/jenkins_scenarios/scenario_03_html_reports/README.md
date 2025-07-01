# 📊 Scenario 03: HTML Reports Chaos - Complete Setup Guide

## 🎯 Overview

**Scenario 03** focuses on **HTML test reporting under chaotic conditions**. This scenario teaches attendees how to generate beautiful, robust test reports even when systems are failing, connections are dropping, and chaos is everywhere.

## 🗂️ Project Structure

```
Jenkins/jenkins_scenarios/scenario_03_html_reports/
├── Dockerfile                              # Container for isolated test execution
├── requirements.txt                        # Python dependencies
├── Jenkinsfile                            # Jenkins pipeline configuration
├── tests/                                 # Test files directory
│   ├── test_config_validation_pass.py     # Configuration validation (success)
│   ├── test_config_validation_fail.py     # Configuration validation (failure)
│   ├── test_api_health_pass.py           # API health checks (success)
│   ├── test_api_health_fail.py           # API health checks (failure)
│   ├── test_postgres_pass.py             # PostgreSQL tests (success)
│   ├── test_postgres_fail.py             # PostgreSQL tests (failure)
│   ├── test_redis_pass.py                # Redis cache tests (success)
│   ├── test_redis_fail.py                # Redis cache tests (failure)
│   ├── test_secret_scan_pass.py          # Secret scanning (success)
│   └── test_secret_scan_fail.py          # Secret scanning (failure)
└── SCENARIO_03_SETUP.md                  # This file
```

## 🔧 Prerequisites

### Required Software
- **Docker** 20.10+ with Docker Compose
- **Jenkins** 2.400+ with required plugins
- **Python** 3.11+
- **Git**

### Jenkins Plugins Required
- HTML Publisher Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- Workspace Cleanup Plugin

### System Requirements
- 8GB RAM (minimum 4GB)
- 15GB free disk space
- Internet connectivity for container pulls

## 🚀 Quick Setup

### 1. **Copy Files to Your Repository**

Place all the scenario files in your repository structure:

```bash
# Create the scenario directory
mkdir -p Jenkins/jenkins_scenarios/scenario_03_html_reports/tests

# Copy all files to the correct locations
# (Copy the Jenkinsfile, Dockerfile, requirements.txt, and all test files)
```

### 2. **Build and Test Locally (Optional)**

```bash
# Navigate to scenario directory
cd Jenkins/jenkins_scenarios/scenario_03_html_reports

# Build Docker image
docker build -t scenario-03-test .

# Test a simple passing scenario
docker run --rm \
  -v $(pwd)/test-reports:/app/reports \
  scenario-03-test \
  pytest tests/test_config_validation_pass.py \
    --html=reports/local_test.html \
    --self-contained-html \
    -v

# Check the generated report
open test-reports/local_test.html
```

### 3. **Setup Jenkins Pipeline**

1. **Create New Pipeline Job** in Jenkins
2. **Configure Pipeline**:
   - Pipeline script from SCM
   - Repository URL: `<your-repository-url>`
   - Script Path: `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile`
3. **Save Configuration**

### 4. **Run Your First Test**

1. Click **"Build with Parameters"**
2. **Start Simple**: Enable all mini-scenarios, set all to "pass" mode
3. **Execute Build** and watch the beautiful output!

## 🎪 Mini-Scenarios Explained

### ⚙️ **Config Validation**
- **Purpose**: Test configuration file parsing and validation
- **Pass Mode**: Valid YAML/JSON configs, proper environment variables
- **Fail Mode**: Malformed configs, missing variables, security violations

### 🏥 **API Health Checks**
- **Purpose**: Test API endpoint health monitoring
- **Pass Mode**: Healthy APIs, proper response formats, good performance
- **Fail Mode**: Service unavailable, timeouts, malformed responses

### 🐘 **PostgreSQL Database**
- **Purpose**: Test database connectivity using testcontainers
- **Pass Mode**: Successful CRUD operations, transactions, connection pooling
- **Fail Mode**: Connection failures, constraint violations, deadlocks

### 📦 **Redis Cache**
- **Purpose**: Test caching mechanisms and Redis operations
- **Pass Mode**: Successful cache operations, data persistence, pub/sub
- **Fail Mode**: Connection timeouts, memory exhaustion, data corruption

### 🔐 **Secret Scanning**
- **Purpose**: Test security scanning and secret management
- **Pass Mode**: Proper secret handling, secure storage, masked logging
- **Fail Mode**: Exposed secrets, weak encryption, plaintext passwords

## 🎛️ Pipeline Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `RUN_CONFIG_VALIDATION` | Enable/disable config validation tests | `true` |
| `RUN_API_HEALTH` | Enable/disable API health check tests | `true` |
| `RUN_POSTGRES` | Enable/disable PostgreSQL tests | `true` |
| `RUN_REDIS` | Enable/disable Redis cache tests | `true` |
| `RUN_SECRET_SCAN` | Enable/disable secret scanning tests | `true` |
| `CONFIG_VALIDATION_PASS` | Config validation: pass (true) or fail (false) | `true` |
| `API_HEALTH_PASS` | API health: pass (true) or fail (false) | `true` |
| `POSTGRES_PASS` | PostgreSQL: pass (true) or fail (false) | `true` |
| `REDIS_PASS` | Redis: pass (true) or fail (false) | `true` |
| `SECRET_SCAN_PASS` | Secret scan: pass (true) or fail (false) | `true` |

## 📊 Understanding the Reports

### **HTML Reports**
Each mini-scenario generates a beautiful HTML report with:
- ✅ **Test execution summary** with pass/fail counts
- 📈 **Detailed test results** with stack traces for failures
- 🕒 **Execution timeline** showing performance metrics
- 📸 **Screenshots and logs** where applicable
- 🎨 **Responsive design** that works on mobile and desktop

### **JSON Reports**
Machine-readable reports containing:
- 📊 **Structured test data** for automated analysis
- 🔍 **Detailed error information** for debugging
- ⏱️ **Performance metrics** and timing information
- 🏷️ **Test metadata** and tags

### **Consolidated Report**
A beautiful index page that:
- 🎯 **Summarizes all mini-scenarios** in one view
- 🔗 **Links to detailed reports** for each scenario
- 📋 **Shows overall health** of the testing pipeline
- 🎪 **Provides workshop progress** tracking

## 🔧 Customization Guide

### **Adding New Test Cases**

1. **Create new test file**:
```python
# tests/test_my_feature_pass.py
import pytest

def test_my_feature_works():
    """Test that my feature works correctly"""
    assert True, "My feature should work"
```

2. **Update Jenkinsfile** to include your new mini-scenario
3. **Add parameters** for enable/disable and pass/fail control

### **Modifying Existing Tests**

Each test file follows this pattern:
```python
class TestFeaturePass:  # or TestFeatureFail
    """Test feature scenarios that should pass/fail"""
    
    def test_specific_functionality(self):
        """Test description for learning purposes"""
        # Test implementation
        assert condition, "Helpful error message"
```

### **Customizing Reports**

The pipeline generates reports using:
```bash
pytest tests/test_*.py \
    --html=reports/report.html \
    --self-contained-html \
    --json-report \
    --json-report-file=reports/report.json \
    -v --tb=short --color=yes
```

You can modify report generation by:
- Adding custom pytest plugins
- Modifying HTML templates
- Adding additional report formats

## 🎓 Learning Paths

### 🔰 **Beginner Path**
1. **Run all scenarios in PASS mode** - understand the baseline
2. **Enable individual FAIL scenarios** - see what chaos looks like
3. **Study the HTML reports** - learn to read test results
4. **Fix simple issues** - modify tests to understand behavior

### 🏅 **Intermediate Path**
1. **Mix pass/fail scenarios** - simulate real-world conditions
2. **Analyze report patterns** - understand failure correlation
3. **Modify test parameters** - experiment with different configurations
4. **Create custom scenarios** - add your own mini-scenarios

### 🚀 **Advanced Path**
1. **Run full chaos mode** - all scenarios in FAIL mode
2. **Implement monitoring** - track report metrics over time
3. **Integrate with CI/CD** - use in your real pipelines
4. **Teach others** - become a chaos engineering mentor

## 🔍 Troubleshooting

### **Common Issues**

#### **Docker Build Failures**
```bash
# Check Docker daemon
docker info

# Clean up Docker resources
docker system prune -f

# Rebuild with no cache
docker build --no-cache -t scenario-03-test .
```

#### **Testcontainer Issues**
```bash
# Ensure Docker socket is accessible
ls -la /var/run/docker.sock

# Check Docker permissions
docker run hello-world

# Clean up testcontainer resources
docker container prune -f
```

#### **Report Generation Issues**
```bash
# Install pytest dependencies manually
pip install pytest-html pytest-json-report

# Test report generation locally
pytest tests/test_config_validation_pass.py \
  --html=test_report.html \
  --self-contained-html

# Check file permissions
chmod 755 reports/
```

#### **Jenkins Permission Issues**
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins service
sudo systemctl restart jenkins

# Check Jenkins can access Docker
sudo -u jenkins docker ps
```

### **Environment Variables**

The scenario uses these environment variables:
```bash
# Required for secret scanning tests
export SECRET_API_KEY="demo-secret-key-12345"
export DATABASE_PASSWORD="super-secret-password"

# Optional for extended testing
export ENVIRONMENT="test"
export DEBUG_MODE="false"
```

## 🎉 Success Metrics

Track your learning progress:

- **📊 Report Quality**: Can you interpret test results effectively?
- **🔧 Problem Resolution**: How quickly can you identify and fix issues?
- **🎯 Scenario Mastery**: Can you explain each failure mode's root cause?
- **🔄 Pipeline Improvement**: Can you enhance the reporting pipeline?
- **👥 Knowledge Transfer**: Can you teach others what you've learned?

## 🔗 Additional Resources

### **Documentation Links**
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-html Plugin](https://pytest-html.readthedocs.io/)
- [Testcontainers Python](https://testcontainers-python.readthedocs.io/)
- [Jenkins HTML Publisher](https://plugins.jenkins.io/htmlpublisher/)

### **Best Practices**
- Always use testcontainers for database/cache testing
- Generate self-contained HTML reports for portability
- Include both positive and negative test cases
- Use descriptive test names and error messages
- Archive reports for historical analysis

### **Next Steps**
1. Master this scenario completely
2. Move to Scenario 04 (Secrets Management)
3. Integrate learnings into your production pipelines
4. Share your experience with the community

---

**🚀 Ready to master HTML reporting under chaos? Let's build some resilient test pipelines!**