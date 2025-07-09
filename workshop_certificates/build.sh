#!/bin/bash

# Build script for Render deployment
# This script installs system dependencies needed for WeasyPrint and other packages

echo "🔧 Installing system dependencies..."

# Update package list
apt-get update

# Install system dependencies for WeasyPrint and other packages
apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

echo "✅ System dependencies installed successfully"

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "🎉 Build completed successfully!" 