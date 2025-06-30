# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Accept build argument
ARG APP_VERSION

# Copy requirements first
COPY Jenkins/jenkins_scenarios/scenario_01_docker_build/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Dynamically copy the right app file as app.py
COPY app/main_v${APP_VERSION}.py /app/app.py

EXPOSE 3000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
