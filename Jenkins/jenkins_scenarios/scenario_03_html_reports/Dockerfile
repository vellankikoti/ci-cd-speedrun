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

# Copy requirements file if you wish to maintain one
# (Optional — included for clarity)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    pytest \
    pytest-html \
    pytest-json-report \
    requests \
    psycopg2-binary \
    redis \
    testcontainers

# By default, print pytest version
CMD ["pytest", "--version"]
