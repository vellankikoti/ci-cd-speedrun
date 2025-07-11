# Multi-stage build for production deployment
# Stage 1: Build Flask app and MkDocs docs
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
RUN pip install --no-cache-dir mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin

# Copy docs and mkdocs.yml, build the documentation
COPY mkdocs-prod.yml ./mkdocs.yml
COPY docs/ ./docs/
RUN mkdocs build

# Stage 2: Nginx for static docs
FROM nginx:alpine AS nginx-docs
COPY --from=builder /site /usr/share/nginx/html
COPY workshop_certificates/nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Stage 3: (Optional) Flask app as separate image
# FROM python:3.11-slim AS flask-app
# ... (Flask app setup here if needed) ...

# To build and push:
