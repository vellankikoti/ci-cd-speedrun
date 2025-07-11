# Multi-stage build for production deployment
# Stage 1: Build MkDocs docs
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install mkdocs and plugins in builder
RUN pip install --no-cache-dir mkdocs mkdocs-material mkdocs-minify-plugin

# Copy docs and mkdocs.yml, build the documentation
COPY mkdocs-prod.yml ./mkdocs.yml
COPY docs/ ./docs/
RUN mkdocs build

# The static site is now in /site
# Use a static site host (like Render Static Site) to serve /site
