# Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Dockerfile

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install gitleaks (Linux x64 static binary)
# Pinning a specific version is safer for reproducibility
ARG GITLEAKS_VERSION="8.18.2"

RUN curl -sSL \
      -o /usr/local/bin/gitleaks \
      "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64" \
    && chmod +x /usr/local/bin/gitleaks \
    && gitleaks version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test scripts and report templates
COPY tests/ /tests/
COPY report_templates/ /report_templates/

WORKDIR /tests

ENTRYPOINT ["python", "run_tests.py"]
