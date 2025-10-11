FROM python:3.11-slim

WORKDIR /app

# Install Flask
RUN pip install --no-cache-dir flask==3.0.0

# Copy app
COPY app.py .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]
