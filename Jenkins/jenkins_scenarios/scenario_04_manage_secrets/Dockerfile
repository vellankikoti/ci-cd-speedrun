# Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Dockerfile

FROM python:3.12-slim

FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*

# Install gitleaks (Linux x64 static binary)
RUN set -eux; \
    GITLEAKS_VERSION=$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | grep tag_name | cut -d '"' -f4); \
    curl -sSL -o /usr/local/bin/gitleaks "https://github.com/gitleaks/gitleaks/releases/download/${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION#v}_linux_x64"; \
    chmod +x /usr/local/bin/gitleaks

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test scripts and report templates
COPY tests/ /tests/
COPY report_templates/ /report_templates/

WORKDIR /tests

ENTRYPOINT ["python", "run_tests.py"]