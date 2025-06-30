FROM python:3.12-slim

# Metadata
LABEL maintainer="CI/CD Chaos Workshop"
LABEL scenario="Scenario 03 - HTML Reports"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libssl-dev \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Create working dir
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-html \
    pytest-json-report \
    requests \
    psycopg2-binary \
    redis \
    testcontainers

# COPY your entire repo into the image
COPY . /app

# Create reports dir to avoid copy errors later
RUN mkdir -p /app/reports

# Default command prints pytest version
CMD ["pytest", "--version"]
