# Base Python image
FROM python:3.12-slim

# Install dependencies:
# - git: to clone repositories
# - docker CLI: to manage containers from inside pipeline
# - curl: useful for health checks
# - pip already included in python base image

RUN apt-get update \
    && apt-get install -y \
        git \
        docker.io \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Pre-install Python packages for TestContainers if you want:
# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace

# For debugging:
RUN python3 --version \
    && pip --version \
    && git --version \
    && docker --version

ENTRYPOINT ["/bin/bash"]
