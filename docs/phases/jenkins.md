
# 🔧 Phase 3 – Pipeline Showdown (Jenkins)

Welcome to **Phase 3** of the CI/CD Chaos Workshop!

This is where we turn chaos into control by building a **production-grade Jenkins pipeline** that:

✅ Builds Docker images  
✅ Runs Testcontainers tests  
✅ Archives HTML reports  
✅ Deploys safely to AWS EKS  
✅ Handles secrets securely

> **Mission:** “Chaos Agent sabotaged our pipelines. Let’s rebuild stronger!”

---

## 🐳 Running Jenkins with Docker

We’ll run Jenkins inside Docker.

Start Jenkins:

```bash
docker run -d   -p 8080:8080   -v jenkins_home:/var/jenkins_home   -v /var/run/docker.sock:/var/run/docker.sock   jenkins/jenkins:lts
```

✅ **Best Practices:**

- Mount the Docker socket
- Prefer using Docker agents for builds rather than the Jenkins master node

---

# 🚀 Scenario 1 – Building Docker Images in Jenkins

### ✅ Why It Matters

Building Docker images in Jenkins ensures **consistent environments** and reliable builds for all deployments.

> **Chaos Event:** “Docker build fails with ‘Cannot connect to the Docker daemon!’”

---

### ✅ What We’ll Do

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
✅ Don’t run Docker builds on Jenkins master node

---

### ✅ What Could Go Wrong?

- Docker socket permission issues  
- Image tags overwritten accidentally  
- Disk space filling up on Jenkins nodes

---

# 🚀 Scenario 2 – Running Testcontainers Tests

### ✅ Why It Matters

Testcontainers enables **true integration testing** by spinning up real databases and services in containers.

> **Chaos Event:** “Testcontainers can’t connect to Docker. Tests fail.”

---

### ✅ What We’ll Do

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

# 🚀 Scenario 3 – Archiving HTML Reports

### ✅ Why It Matters

HTML reports help teams **visually inspect results** and keep a paper trail for compliance or troubleshooting.

> **Chaos Event:** “Reports not found. Pipeline fails.”

---

### ✅ What We’ll Do

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

# 🚀 Scenario 4 – Managing Secrets for AWS

### ✅ Why It Matters

CI/CD pipelines **must handle secrets safely** to avoid catastrophic data leaks.

> **Chaos Event:** “Secrets printed in Jenkins logs!”

---

### ✅ What We’ll Do

✅ Store AWS credentials in Jenkins  
✅ Inject credentials without printing them in logs

---

### ✅ How to Fix It

✅ Use Jenkins credentials binding  
✅ Mask secrets in console output

---

### ✅ Pipeline Snippet

```groovy
withCredentials([
    [
        $class: 'AmazonWebServicesCredentialsBinding',
        credentialsId: 'aws-credentials'
    ]
]) {
    sh '''
        aws sts get-caller-identity
    '''
}
```

---

### ✅ Best Practices

✅ Never echo secrets  
✅ Rotate credentials regularly  
✅ Use IAM roles if running Jenkins on EC2

---

### ✅ What Could Go Wrong?

- Accidental logging of secrets  
- Expired credentials  
- Misconfigured credentials IDs

---

# 🚀 Scenario 5 – Deploying to AWS EKS

### ✅ Why It Matters

Kubernetes deployments are critical in modern CI/CD. Jenkins must **handle YAML validation, rollouts, and error handling.**

> **Chaos Event:** “Bad YAML causes deployment failures in EKS.”

---

### ✅ What We’ll Do

✅ Deploy app to AWS EKS  
✅ Run dry-run and YAML validation  
✅ Monitor deployment rollout status

---

### ✅ How to Fix It

✅ Validate YAML before applying  
✅ Roll back deployments if pods fail

---

### ✅ Pipeline Snippet

```groovy
stage('Deploy to EKS') {
    steps {
        withCredentials([
            [
                $class: 'AmazonWebServicesCredentialsBinding',
                credentialsId: 'aws-credentials'
            ]
        ]) {
            sh '''
                aws eks update-kubeconfig --name my-cluster
                kubectl apply -f k8s/deployment.yaml --dry-run=client
                kubeval k8s/deployment.yaml
                kubectl apply -f k8s/deployment.yaml
                kubectl rollout status deployment my-deployment
            '''
        }
    }
}
```

---

### ✅ Best Practices

✅ Always dry-run deployments  
✅ Use tools like `kubeval`  
✅ Monitor rollout status carefully

---

### ✅ What Could Go Wrong?

- Incorrect kubeconfig  
- YAML syntax errors  
- Pods stuck in CrashLoopBackOff

---

## 🎬 Complete Jenkinsfile Example

Here’s a **complete working Jenkinsfile** for our workshop:

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'APP_VERSION', defaultValue: '3', description: 'Which version to deploy?')
    }

    environment {
        DOCKER_IMAGE = "ci-cd-chaos-app:v${params.APP_VERSION}"
    }

    stages {
        stage('Hello Chaos') {
            steps {
                echo "Building pipeline for version ${params.APP_VERSION}"
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Run Testcontainers Tests') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Publish Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**', fingerprint: true
            }
        }
        stage('Deploy to EKS') {
            steps {
                withCredentials([
                    [
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-credentials'
                    ]
                ]) {
                    sh '''
                        aws eks update-kubeconfig --name my-cluster
                        kubectl apply -f k8s/deployment.yaml --dry-run=client
                        kubeval k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl rollout status deployment my-deployment
                    '''
                }
            }
        }
    }
}
```

---

## ✅ What You’ll Learn

By the end of Phase 3, you’ll:

✅ Build Docker images safely in Jenkins  
✅ Run Python Testcontainers tests in CI  
✅ Securely manage AWS secrets  
✅ Deploy confidently to AWS EKS  
✅ Know how to troubleshoot pipeline chaos

---

## ✅ Ready for Advanced Scenarios

Up next, we’ll tackle:

- Kubernetes-specific scenarios (Probes, ConfigMaps, Rollbacks)  
- Advanced GitOps pipelines with Argo CD  
- Progressive delivery with Argo Rollouts  
- Monitoring pipeline health with Prometheus & Grafana

Stay tuned for **Phase 4: Kubernetes Warzone!**

---

[⬅️ Previous Phase: Docker Mastery](./docker.md) | [Next Phase: Kubernetes Warzone ➡️](./k8s.md)
