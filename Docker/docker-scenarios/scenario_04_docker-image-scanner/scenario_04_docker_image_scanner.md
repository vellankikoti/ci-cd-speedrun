# Scenario 04: Docker Image Scanner - Production-Grade Hands-On Guide

## 🎯 **Learning Objective**
Master Docker security analysis using real vulnerability scanning with Trivy. Learn to identify security issues, apply best practices, and create secure Docker images through hands-on experience.

---

## 📋 **Prerequisites**
- Docker installed and running (no need to install Trivy locally)
- Web browser
- Basic understanding of Docker concepts

---

## 🚀 **Quick Start**

### **Step 1: No Trivy Installation Needed!**
You do **not** need to install Trivy locally. The application will automatically use the official Trivy Docker image (`aquasec/trivy:latest`) for all scanning operations. Just make sure Docker is running and the Docker socket is available.

### **Step 2: Start the Docker Image Analyzer**
```bash
# From the scenario_04_docker-image-scanner directory:
python app.py
```

### **Step 3: Open the Application**
- Open your browser and go to: http://localhost:8000

---

## ✅ **Pre-Flight Checklist**
- [ ] Docker is running (`docker ps`)
- [ ] Port 8000 is available
- [ ] You have internet access (for pulling images and Trivy Docker image)

---

## 🐳 **Curated Docker Image Examples for Demo**

Use these production-grade images for demonstration:

- `nginx:1.25-alpine` (secure, minimal)
- `python:3.11-slim` (modern, secure)
- `python:3.8` (older, more vulnerabilities)
- `node:18-alpine` (modern Node.js)
- `ubuntu:22.04` (large, more vulnerabilities)

---

## 🛠️ **How to Demonstrate**

### **A. Image Analysis**
1. Enter an image name (e.g., `nginx:1.25-alpine`, `python:3.11-slim`)
2. Click "Analyze Image"
3. Review:
   - Security score and vulnerability breakdown
   - Best practices and educational insights
   - Industry comparison

### **B. Image Comparison**
1. Click the "Compare Images" tab
2. Enter two image names (e.g., `python:3.8` vs `python:3.11-slim`)
3. Compare security metrics and best practices

---

## 🔍 **What You'll Learn**
- CVE understanding and severity
- Attack surface minimization
- Secure base image selection
- Non-root user best practices
- Multi-stage builds and layer optimization
- Secret management and image scanning
- Real-world CI/CD integration

---

## 🧪 **Recommended Images for Analysis**
- `nginx:1.25-alpine` (secure, minimal)
- `python:3.11-slim` (modern, secure)
- `python:3.8` (older, more vulnerabilities)
- `node:18-alpine` (modern Node.js)
- `ubuntu:22.04` (large, more vulnerabilities)

---

## 🔧 **Troubleshooting**
- **Trivy not found:** Ensure Docker is running and the Docker socket is available. The app will pull and use the Trivy Docker image automatically.
- **Docker connection failed:** Ensure Docker is running
- **Build failed:** Check Dockerfile syntax and base image availability
- **Port in use:** Stop other apps on port 8000 or change the port in `app.py`

---

## 🧹 **Clean Up**
```bash
# Stop the app (if running in foreground, Ctrl+C)
# Remove any test images if needed
# Optionally, clean up the uploads/ directory
rm -rf uploads/*
```

---

## 🎯 **Next Steps**
- Integrate scanning into your CI/CD pipeline
- Apply best practices to your own Dockerfiles
- Educate your team on container security
- Stay updated with the latest security tools

---

**Built for real-world, production-grade Docker security education.** 