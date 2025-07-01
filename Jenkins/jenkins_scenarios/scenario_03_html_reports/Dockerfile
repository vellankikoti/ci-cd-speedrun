# Dockerfile for Scenario 03: HTML Reports Chaos
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    jq \
    unzip \
    vim \
    netcat-openbsd \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (for testcontainers)
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh --dry-run && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm get-docker.sh && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install additional testing and security packages
RUN pip install \
    pytest-html \
    pytest-json-report \
    pytest-cov \
    pytest-xdist \
    pytest-mock \
    requests \
    psycopg2-binary \
    redis \
    testcontainers \
    docker \
    pyyaml \
    cryptography \
    bandit \
    safety \
    truffleHog \
    gitpython

# Create reports directory
RUN mkdir -p /app/reports

# Copy test files
COPY tests/ /app/tests/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DOCKER_HOST=unix:///var/run/docker.sock

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pytest; print('OK')" || exit 1

# Default command
CMD ["pytest", "--help"]