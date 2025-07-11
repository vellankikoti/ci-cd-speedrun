# Use Python 3.11 for best compatibility with dependencies
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Trivy
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    lsb-release \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Trivy
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - \
    && echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list \
    && apt-get update \
    && apt-get install -y trivy \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port 8899 (random port to avoid conflicts)
EXPOSE 8899

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8899

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8899/api/v1/test || exit 1

# Run the application
CMD ["python", "app.py"] 