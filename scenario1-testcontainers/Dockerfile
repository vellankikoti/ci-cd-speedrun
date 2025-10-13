# Scenario 1: TestContainers Magic
# Real database testing that catches bugs mocks miss

FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser -D -s /bin/sh appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5001/api/health')" || exit 1

# Run the application
CMD ["python", "app.py"]
