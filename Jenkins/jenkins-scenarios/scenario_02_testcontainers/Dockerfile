# Simplified Dockerfile for TestContainers Integration Demo
FROM python:3.11-slim

# Set build arguments
ARG APP_VERSION=1.0.0
ARG BUILD_TIME
ARG ENVIRONMENT=production

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_VERSION=${APP_VERSION}
ENV BUILD_TIME=${BUILD_TIME}
ENV ENVIRONMENT=${ENVIRONMENT}
ENV PORT=5000

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory
WORKDIR /app

# Copy application code
COPY app.py .
COPY tests/ tests/
COPY requirements.txt .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["python", "app.py"]

# Labels for metadata
LABEL maintainer="Jenkins Workshop"
LABEL version=${APP_VERSION}
LABEL description="TestContainers Integration Demo Application"
LABEL environment=${ENVIRONMENT}
