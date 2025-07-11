# Scenario 04: Docker Image Scanner - Hands-On Guide

## Objective
Learn how to use the Docker Image Scanner to analyze Dockerfiles for security, best practices, and educational insights. This guide will walk you through setup, running the scanner, and testing with your own Dockerfiles.

---

## Prerequisites
- Docker installed and running
- (Optional) Python 3.8+ and pip if you want to run locally
- A web browser

---

## 1. Build and Run the Docker Image Scanner

### **A. Build the Docker Image**
```bash
docker build -t docker-analyser Docker/docker-scenarios/docker-image-scanner
```

### **B. Run the Scanner Container**
```bash
docker run -d --rm \
  -p 8899:8899 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name docker-analyser \
  docker-analyser
```

- The web UI will be available at: [http://localhost:8899](http://localhost:8899)

---

## 2. Using the Web Interface

1. **Open your browser and go to:** [http://localhost:8899](http://localhost:8899)
2. **Click the "Analyze Dockerfile" tab.**
3. **Upload any Dockerfile** (the file name does not matter, e.g., `Dockerfile`, `Dockerfile1`, etc.).
4. **Wait for the analysis to complete.**
5. **Review the results:**
   - Security score and vulnerabilities
   - Best practices and recommendations
   - Educational insights
   - Industry comparison

---

## 3. Testing with Example Dockerfiles

You can generate simple test Dockerfiles using the following script:

```bash
#!/bin/bash
mkdir -p simple_dockerfiles
cd simple_dockerfiles
cat > Dockerfile1 <<EOF
FROM alpine:3.18
CMD ["echo", "Hello from Alpine!"]
EOF
cat > Dockerfile2 <<EOF
FROM ubuntu:22.04
CMD ["bash", "-c", "echo Hello from Ubuntu! && cat /etc/os-release"]
EOF
cat > Dockerfile3 <<EOF
FROM nginx:alpine
EXPOSE 80
EOF
cat > Dockerfile4 <<EOF
FROM busybox
CMD ["sleep", "10"]
EOF
cat > Dockerfile5 <<EOF
FROM debian:stable-slim
CMD ["date"]
EOF
```

- Upload any of these files to the web UI for instant analysis.

---

## 4. Troubleshooting

- **If the build fails:**
  - Check the error message in the UI for details (e.g., syntax errors, missing base images).
  - Make sure your Dockerfile is valid and does not require extra files.
- **If the UI does not load:**
  - Ensure the container is running (`docker ps`)
  - Ensure nothing else is using port 8899
- **To stop the scanner:**
  ```bash
  docker stop docker-analyser
  ```

---

## 5. Clean Up
- To remove the container:
  ```bash
  docker stop docker-analyser
  ```
- To remove the image:
  ```bash
  docker rmi docker-analyser
  ```

---

## 6. Advanced: Run Locally (Optional)
If you want to run the scanner without Docker:

1. Install dependencies:
   ```bash
   cd Docker/docker-scenarios/docker-image-scanner
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open [http://localhost:8899](http://localhost:8899)

---

## 7. Additional Tips
- You can use any Dockerfile, with any name.
- The scanner provides real Trivy vulnerability data and actionable recommendations.
- Try modifying a Dockerfile (e.g., add `USER root` or expose a port) and see how the analysis changes.

---

**Congratulations!** You have successfully used the Docker Image Scanner to analyze Dockerfiles for security and best practices. 