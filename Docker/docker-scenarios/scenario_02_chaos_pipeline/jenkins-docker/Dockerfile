FROM jenkins/jenkins:lts

USER root

# Install Docker CLI and Python dependencies inside Jenkins container
RUN apt-get update && \
    apt-get install -y docker.io python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (using --break-system-packages for newer Python)
RUN pip3 install --break-system-packages pytest sqlalchemy testcontainers[mysql] docker requests

# Keep running as root for Docker access
# This is the simplest solution for workshop environments 