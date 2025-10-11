FROM python:3.11-slim

WORKDIR /app

# Install Flask
RUN pip install --no-cache-dir flask==3.0.0

# Copy app
COPY todo-app.py .

# Create non-root user
RUN useradd -m -u 1000 todouser && chown -R todouser:todouser /app

USER todouser

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "todo-app.py"]
