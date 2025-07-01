# Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Dockerfile

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*

# Install gitleaks
RUN curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_$(uname -s)_$(uname -m).tar.gz | \
    tar -xz -C /usr/local/bin gitleaks

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test scripts and report templates
COPY tests/ /tests/
COPY report_templates/ /report_templates/

WORKDIR /tests

ENTRYPOINT ["python", "run_tests.py"]