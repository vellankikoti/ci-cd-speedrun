# 🔧 Phase 3 – Pipeline Showdown (Jenkins)

Welcome to **Phase 3** of the CI/CD Chaos Workshop!

This is where we turn chaos into control by building a **production-grade Jenkins pipeline** that:

✅ Builds Docker images  
✅ Runs Testcontainers tests  
✅ Archives HTML reports  
✅ Deploys safely to AWS EKS  
✅ Handles secrets securely

> **Mission:** "Chaos Agent sabotaged our pipelines. Let's rebuild stronger!"

---

## 🐳 Running Jenkins with Docker

We'll run Jenkins inside Docker.

Start Jenkins:

```bash
docker run -d \
  -p 8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

✅ **Best Practices:**

- Mount the Docker socket
- Prefer using Docker agents for builds rather than the Jenkins master node

---

## 🚀 Scenario 1 – Building Docker Images in Jenkins

### ✅ Why It Matters

Building Docker images in Jenkins ensures **consistent environments** and reliable builds for all deployments.

> **Chaos Event:** "Docker build fails with 'Cannot connect to the Docker daemon!'"

---

### ✅ What We'll Do

✅ Build Python Docker images  
✅ Learn multi-stage Docker builds  
✅ Understand Docker socket mounting in Jenkins-in-Docker

---

### ✅ How to Fix It

✅ Mount the Docker socket into Jenkins  
✅ Install Docker plugin in Jenkins  
✅ Prefer Docker agents for builds

---

### ✅ Pipeline Snippet

```groovy
stage('Build Docker Image') {
    steps {
        script {
            dockerImage = docker.build("ci-cd-chaos-app:v${params.APP_VERSION}")
        }
    }
}
```

---

### ✅ Best Practices

✅ Keep images minimal  
✅ Always tag images with unique versions  
✅ Don't run Docker builds on Jenkins master node

---

### ✅ What Could Go Wrong?

- Docker socket permission issues  
- Image tags overwritten accidentally  
- Disk space filling up on Jenkins nodes

---

## 🚀 Scenario 2 – Running Testcontainers Tests

### ✅ Why It Matters

Testcontainers enables **true integration testing** by spinning up real databases and services in containers.

> **Chaos Event:** "Testcontainers can't connect to Docker. Tests fail."

---

### ✅ What We'll Do

✅ Run pytest Testcontainers tests  
✅ Learn how to ensure Docker connectivity for tests

---

### ✅ How to Fix It

✅ Use Docker-enabled Jenkins agents  
✅ Check Docker socket permissions

---

### ✅ Pipeline Snippet

```groovy
stage('Run Testcontainers Tests') {
    steps {
        sh 'pytest tests/'
    }
}
```

---

### ✅ Best Practices

✅ Always clean up containers after tests  
✅ Use minimal images for speed  
✅ Avoid running on shared network ports

---

### ✅ What Could Go Wrong?

- Docker API errors  
- Port collisions between test containers  
- Resource starvation on Jenkins agents

---

## 🚀 Scenario 3 – Archiving HTML Reports

### ✅ Why It Matters

HTML reports help teams **visually inspect results** and keep a paper trail for compliance or troubleshooting.

> **Chaos Event:** "Reports not found. Pipeline fails."

---

### ✅ What We'll Do

✅ Archive Docker analysis HTML reports from Phase 2  
✅ Display reports in Jenkins UI

---

### ✅ How to Fix It

✅ Check archive paths  
✅ Validate workspace usage

---

### ✅ Pipeline Snippet

```groovy
stage('Publish Reports') {
    steps {
        archiveArtifacts artifacts: 'reports/**', fingerprint: true
    }
}
```

---

### ✅ Best Practices

✅ Keep report paths consistent  
✅ Fingerprint reports for traceability  
✅ Use retention policies for old artifacts

---

### ✅ What Could Go Wrong?

- Wrong file paths  
- Workspace wiped by cleanup plugins

---

## 🚀 Scenario 4 – Managing Secrets for AWS

### ✅ Why It Matters

CI/CD pipelines **must handle secrets safely** to avoid catastrophic data leaks.

> **Chaos Event:** "Secrets printed in Jenkins logs!"

---

### ✅ What We'll Do

✅ Use Jenkins credentials for AWS access  
✅ Scan for secrets in code  
✅ Generate security reports

---

### ✅ How to Fix It

✅ Store secrets in Jenkins credentials  
✅ Use secret scanning tools  
✅ Never log sensitive data

---

### ✅ Pipeline Snippet

```groovy
stage('Deploy to AWS') {
    steps {
        withCredentials([string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID')]) {
            sh 'aws eks update-kubeconfig --name my-cluster'
        }
    }
}
```

---

### ✅ Best Practices

✅ Use Jenkins credentials store  
✅ Rotate secrets regularly  
✅ Scan for hardcoded secrets

---

### ✅ What Could Go Wrong?

- Secrets in logs  
- Hardcoded credentials  
- Expired AWS tokens

---

## 🚀 Scenario 5 – Deploying to AWS EKS

### ✅ Why It Matters

Kubernetes deployments need **proper validation** and **rollback capabilities**.

> **Chaos Event:** "Deployment stuck in pending. Pods won't start!"

---

### ✅ What We'll Do

✅ Deploy Python apps to EKS  
✅ Monitor rollout status  
✅ Handle deployment failures

---

### ✅ How to Fix It

✅ Validate YAML manifests  
✅ Check resource limits  
✅ Monitor pod events

---

### ✅ Pipeline Snippet

```groovy
stage('Deploy to EKS') {
    steps {
        sh 'kubectl apply -f k8s/'
        sh 'kubectl rollout status deployment/chaos-app'
    }
}
```

---

### ✅ Best Practices

✅ Always validate manifests  
✅ Use health checks  
✅ Have rollback procedures

---

### ✅ What Could Go Wrong?

- Invalid YAML syntax  
- Resource constraints  
- Network connectivity issues

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Pipeline Failures

```groovy
// Simulate pipeline failures
stage('Chaos Test') {
    steps {
        script {
            // Randomly fail builds
            if (Math.random() < 0.2) {
                error "Simulated pipeline failure"
            }
        }
    }
}
```

### ✅ Scenario 2: Slow Builds

```groovy
// Simulate slow builds
stage('Slow Build') {
    steps {
        script {
            // Add artificial delay
            sleep 30
            
            // Continue with build
            sh 'docker build -t chaos-app .'
        }
    }
}
```

### ✅ Scenario 3: Resource Exhaustion

```groovy
// Simulate resource issues
stage('Resource Test') {
    steps {
        script {
            // Try to use excessive resources
            sh 'docker run --memory=10g chaos-app'
        }
    }
}
```

---

## 📊 Monitoring & Reporting

### ✅ Pipeline Metrics

- Build success rate
- Average build time
- Test execution time
- Deployment success rate

### ✅ Chaos Metrics

- Number of simulated failures
- Recovery time from failures
- System resilience score

---

## 🎯 Next Steps

✅ **Phase 3 Complete:** You now have Jenkins pipeline mastery!  
✅ **Ready for Phase 4:** [Kubernetes Chaos & Scalability](k8s.md)  
✅ **Chaos Agent Status:** Defeated in pipeline automation! 🕶️

---

**Remember:** Jenkins pipelines are your automation backbone. When chaos strikes, your pipeline will be your shield! 🔥
