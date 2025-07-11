# 🔧 Jenkins: Pipeline Mastery & Chaos Engineering

Welcome to **Phase 3** of the CI/CD Chaos Workshop — where you'll transform from a Jenkins user into a **pipeline architect** who can build, test, secure, and deploy with confidence!

## 🎯 What You'll Master

- **Docker Integration**: Build and test containers in Jenkins with real-world chaos scenarios
- **Testcontainers Pipeline**: Run database tests with intentional failures and recovery
- **Enterprise Reporting**: Generate stunning HTML reports that stakeholders love
- **Security Scanning**: Detect secrets and vulnerabilities before they reach production
- **Kubernetes Deployment**: Deploy to AWS EKS with proper monitoring and rollback

---

## 🚀 Why Jenkins Mastery Matters

**The Problem:** Your CI/CD pipeline is fragile. One small change breaks everything. Chaos Agent loves this!

**The Solution:** Build bulletproof pipelines that handle failures gracefully, provide clear feedback, and deploy with confidence.

**The Chaos Angle:** What happens when your Docker build fails? When tests are flaky? When secrets leak? Your Jenkins pipeline will be ready for anything!

---

## 🧪 Progressive Learning Scenarios

### 1. **Docker Build Chaos** 🐳
**What You'll Experience:**
- Build 5 different Python app versions with intentional sabotage
- Parameterize Jenkins pipelines with user inputs
- Handle Docker socket permissions and container lifecycle
- Detect and report build failures with clear error messages

**Real Pipeline You'll Write:**
```groovy
pipeline {
    parameters {
        string(name: 'APP_VERSION', defaultValue: '1', description: 'Which app version (1-5)?')
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ci-cd-chaos-app:v${params.APP_VERSION} ."
            }
        }
        stage('Test Container') {
            steps {
                sh "docker run -d --name chaos-app-v${params.APP_VERSION} -p 3000:3000 ci-cd-chaos-app:v${params.APP_VERSION}"
                sh "curl -f http://localhost:3000 || exit 1"
            }
        }
    }
}
```

**Chaos Lessons:** Version mismatches, container startup failures, network connectivity issues

---

### 2. **Testcontainers Integration** 🧪
**What You'll Experience:**
- Run PostgreSQL and Redis tests in Jenkins containers
- Simulate database connection failures and recovery
- Use Docker-in-Docker for isolated test environments
- Handle test flakiness with proper retry logic

**Real Pipeline You'll Write:**
```groovy
pipeline {
    agent {
        docker {
            image 'ci-cd-chaos-python:latest'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    parameters {
        choice(name: 'TEST_MODE', choices: ['pass', 'fail'], description: 'Run passing or failing tests?')
    }
    
    stages {
        stage('Run Database Tests') {
            steps {
                sh "pytest tests/test_postgres_${params.TEST_MODE}.py tests/test_redis_${params.TEST_MODE}.py"
            }
        }
    }
}
```

**Chaos Lessons:** Database connection failures, test isolation, resource constraints

---

### 3. **Enterprise HTML Reports** 📊
**What You'll Experience:**
- Generate stunning, interactive HTML reports with charts and animations
- Archive reports as Jenkins artifacts with proper retention
- Create mobile-responsive dashboards that stakeholders love
- Implement dark/light theme toggles and professional styling

**Real Pipeline You'll Write:**
```groovy
stage('Generate Reports') {
    steps {
        sh "python report_generator.py --scenarios config,api,database,secrets"
        archiveArtifacts artifacts: 'reports/**/*.html', fingerprint: true
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'index.html',
                reportName: 'Test Results Dashboard'
            ])
        }
    }
}
```

**Chaos Lessons:** Report generation failures, artifact storage issues, visualization challenges

---

### 4. **Secrets Management** 🔐
**What You'll Experience:**
- Scan code for leaked credentials using Gitleaks
- Use Jenkins credentials store for secure secret management
- Generate security reports with severity levels and remediation steps
- Implement secret rotation and access controls

**Real Pipeline You'll Write:**
```groovy
stage('Security Scan') {
    steps {
        withCredentials([string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID')]) {
            sh "gitleaks detect --source . --report-format json --report-path reports/secrets.json"
        }
    }
    post {
        always {
            script {
                if (fileExists('reports/secrets.json')) {
                    def secrets = readJSON file: 'reports/secrets.json'
                    if (secrets.size() > 0) {
                        error "Found ${secrets.size()} secrets in code!"
                    }
                }
            }
        }
    }
}
```

**Chaos Lessons:** Secret leaks, credential exposure, security compliance failures

---

### 5. **AWS EKS Deployment** ☁️
**What You'll Experience:**
- Deploy Python applications to Kubernetes clusters
- Handle authentication with AWS IAM and EKS
- Monitor deployments with real-time kubectl commands
- Implement proper rollback procedures and health checks

**Real Pipeline You'll Write:**
```groovy
stage('Deploy to EKS') {
    steps {
        withCredentials([string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID')]) {
            sh "aws eks update-kubeconfig --name ${params.CLUSTER_NAME} --region ${params.AWS_REGION}"
            sh "kubectl apply -f k8s/deployment.yaml"
            sh "kubectl rollout status deployment/chaos-app --timeout=300s"
        }
    }
    post {
        failure {
            sh "kubectl rollout undo deployment/chaos-app"
            sh "kubectl get events --sort-by=.metadata.creationTimestamp"
        }
    }
}
```

**Chaos Lessons:** Authentication failures, resource constraints, network connectivity issues, deployment timeouts

---

## 🎭 Built-In Chaos Engineering

Every scenario includes **intentional chaos** to build resilience:

### **Parameterized Chaos**
```groovy
parameters {
    choice(name: 'CHAOS_MODE', choices: ['pass', 'fail'], description: 'Run normal or chaos mode?')
}
```

### **Conditional Failures**
```groovy
stage('Chaos Test') {
    steps {
        script {
            if (params.CHAOS_MODE == 'fail') {
                error "Chaos Agent strikes! Simulated failure triggered."
            }
        }
    }
}
```

### **Resource Constraints**
```groovy
stage('Resource Test') {
    steps {
        sh "docker run --memory=100m --cpus=0.1 chaos-app"
    }
}
```

---

## 🏗️ Production Patterns You'll Learn

### **Pipeline Structure**
```groovy
pipeline {
    agent any
    
    parameters {
        // User inputs
    }
    
    environment {
        // Shared variables
    }
    
    stages {
        // Build, test, deploy stages
    }
    
    post {
        always {
            // Cleanup and reporting
        }
        success {
            // Success notifications
        }
        failure {
            // Failure handling and rollback
        }
    }
}
```

### **Docker Integration**
```groovy
agent {
    docker {
        image 'python:3.12-slim'
        args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
    }
}
```

### **Error Handling**
```groovy
post {
    failure {
        sh "docker logs ${container_name} || true"
        archiveArtifacts artifacts: 'logs/**/*', allowEmptyArchive: true
        emailext subject: "Build Failed: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_NUMBER} failed. Check console output.",
                 to: 'team@company.com'
    }
}
```

---

## 📊 Monitoring & Reporting

### **Pipeline Metrics**
- Build success/failure rates
- Average build duration
- Test execution times
- Deployment success rates
- Security scan results

### **Chaos Metrics**
- Number of simulated failures
- Recovery time from failures
- System resilience scores
- Rollback success rates

### **Enterprise Reports**
- Interactive HTML dashboards
- Color-coded status indicators
- Performance analytics
- Security compliance reports

---

## 🚀 How to Run

### **Quick Start**
```bash
# Start Jenkins with Docker
docker run -d \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Access Jenkins UI
open http://localhost:8080
```

### **Run All Scenarios**
```bash
# Execute the scenario runner
python Jenkins/jenkins_scenarios/run_all_scenarios.py
```

### **Expected Progression**
1. **Scenario 1**: Docker builds with chaos testing
2. **Scenario 2**: Testcontainers integration with database failures
3. **Scenario 3**: Beautiful HTML reports with interactive charts
4. **Scenario 4**: Security scanning and secrets management
5. **Scenario 5**: AWS EKS deployment with monitoring

---

## 🎯 Learning Outcomes

By the end of Phase 3, you'll be able to:

✅ **Build bulletproof Jenkins pipelines** that handle any failure gracefully  
✅ **Integrate Docker and Testcontainers** seamlessly into CI/CD workflows  
✅ **Generate professional reports** that stakeholders actually want to read  
✅ **Implement security scanning** that prevents credential leaks  
✅ **Deploy to Kubernetes** with proper monitoring and rollback procedures  
✅ **Apply chaos engineering** to make your pipelines more resilient  

---

## 🎭 The Chaos Agent's Challenge

**Chaos Agent:** *"Let's just use a simple pipeline. What could go wrong?"*

**Your Response:** *"Everything! Without proper error handling, security scanning, and monitoring, your pipeline becomes a liability. Jenkins mastery means building pipelines that survive chaos and provide clear feedback when things go wrong."*

---

## 🏁 Next Steps

✅ **Phase 3 Complete:** You now have Jenkins pipeline mastery!  
✅ **Ready for Phase 4:** [Kubernetes Chaos & Scalability](k8s.md) — where you'll orchestrate chaos at scale.  
✅ **Chaos Agent Status:** Defeated in pipeline automation! 🕶️  

---

**Remember:** Jenkins pipelines are your automation backbone. When chaos strikes, your pipeline will be your shield! 🔥

> 💡 **Pro Tip:** The chaos scenarios in these pipelines aren't just for fun — they're teaching you to build resilient systems that can handle real-world failures gracefully.
