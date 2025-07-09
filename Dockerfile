# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies required for WeasyPrint and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install mkdocs and plugins in builder
RUN pip install --no-cache-dir mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin

# Copy docs and mkdocs.yml, build the documentation
COPY ../docs ./docs
COPY ../mkdocs.yml .
RUN mkdocs build

# Copy requirements first for better caching
COPY workshop_certificates/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY workshop_certificates /app
# In the production stage, copy the built site
COPY --from=builder /app/site /app/site

# Create uploads directory
RUN mkdir -p uploads

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
    