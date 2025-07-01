# Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Dockerfile

FROM python:3.12-slim

# Install system dependencies
# Install gitleaks (Linux x86_64)
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/* && \
    GITLEAKS_VERSION=$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | grep tag_name | cut -d '\"' -f4) && \
    curl -sSL https://github.com/gitleaks/gitleaks/releases/download/${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION#v}_linux_x64.tar.gz | \
    tar -xz -C /usr/local/bin gitleaks

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test scripts and report templates
COPY tests/ /tests/
COPY report_templates/ /report_templates/

WORKDIR /tests

ENTRYPOINT ["python", "run_tests.py"]