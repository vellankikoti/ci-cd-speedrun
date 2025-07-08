# Multi-stage build for minimal image size
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Detect architecture and install kubectl
RUN ARCH=$(dpkg --print-architecture) && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/${ARCH}/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Detect architecture and install AWS CLI v2
RUN ARCH=$(uname -m) && \
    if [ "${ARCH}" = "x86_64" ]; then \
        AWS_CLI_ARCH="x86_64"; \
    elif [ "${ARCH}" = "aarch64" ]; then \
        AWS_CLI_ARCH="aarch64"; \
    else \
        echo "Unsupported architecture: ${ARCH}" && exit 1; \
    fi && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_CLI_ARCH}.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install --bin-dir /aws-cli-bin/

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy binaries from builder stage
COPY --from=builder /usr/local/bin/kubectl /usr/local/bin/kubectl
COPY --from=builder /aws-cli-bin/ /usr/local/bin/
COPY --from=builder /usr/local/aws-cli/ /usr/local/aws-cli/

# Create application directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN groupadd -r chaos && useradd -r -g chaos -d /app -s /bin/bash chaos

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/reports /app/tests/deploy \
    && chown -R chaos:chaos /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV KUBECONFIG=/root/.kube/config

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD kubectl version --client || exit 1

# Switch to non-root user for running tests
USER chaos

# Default command
CMD ["python", "run_tests.py"]

# Labels for metadata
LABEL maintainer="CI/CD Chaos Workshop"
LABEL description="EKS Deployment Testing Container for Scenario 5"
LABEL version="1.0.0"
LABEL scenario="scenario_05_deploy_eks"