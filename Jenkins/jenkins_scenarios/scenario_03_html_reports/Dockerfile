# Base Dockerfile for CI/CD Chaos Workshop
# This serves as a template for all scenario-specific Dockerfiles

FROM python:3.12-slim

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
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install common Python packages
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install additional testing packages that are commonly needed
RUN pip install \
    pytest-html \
    pytest-json-report \
    pytest-cov \
    pytest-xdist \
    pytest-mock \
    requests \
    docker \
    kubernetes \
    boto3 \
    pytest-testcontainers

# Create reports directory
RUN mkdir -p /app/reports

# Copy test runner script
COPY run_scenario_tests.py /usr/local/bin/run_scenario_tests.py
RUN chmod +x /usr/local/bin/run_scenario_tests.py

# Copy tests directory
COPY tests/ /app/tests/

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-m", "pytest", "--help"]