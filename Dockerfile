# -------- BUILDER STAGE --------
    FROM python:3.12-slim AS builder

    WORKDIR /app
    
    # Install deps
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    # -------- FINAL STAGE --------
    FROM python:3.12-slim
    
    WORKDIR /app
    
    # Copy installed packages from builder
    COPY --from=builder /install /usr/local
    
    # Copy app source
    COPY ./app ./app
    
    # Expose app port
    EXPOSE 3000
    
    # Define default environment variable (v3+)
    ENV GREETING="Hello from the CI/CD Chaos Workshop!"
    
    # Healthcheck (added in v4)
    # HEALTHCHECK CMD curl --fail http://localhost:3000/health || exit 1
    
    # Run the app
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
    