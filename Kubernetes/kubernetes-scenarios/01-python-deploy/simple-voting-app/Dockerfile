FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY vote-app.py .

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "vote-app.py"]
