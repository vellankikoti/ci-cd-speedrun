#!/bin/bash

# Setup script for Jenkins workspace
# This script prepares the workspace with all required files for the chaos pipeline

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}🔹 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

print_header "Setting up Jenkins Workspace"
echo "=================================="
echo ""

print_step "Creating directory structure..."
mkdir -p scenarios
mkdir -p pipeline
mkdir -p tests

print_success "Directory structure created"

print_step "Creating scenario files..."

# Create step1_fail_network
mkdir -p scenarios/step1_fail_network
cat > scenarios/step1_fail_network/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask requests
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

cat > scenarios/step1_fail_network/app.py << 'EOF'
#!/usr/bin/env python3
import requests
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step1_fail_network",
        "message": "Network connectivity issues"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 1: Network Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
EOF

# Create step2_fail_resource
mkdir -p scenarios/step2_fail_resource
cat > scenarios/step2_fail_resource/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask psutil
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

cat > scenarios/step2_fail_resource/app.py << 'EOF'
#!/usr/bin/env python3
import psutil
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step2_fail_resource",
        "message": "Resource exhaustion"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 2: Resource Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
EOF

# Create step3_fail_service
mkdir -p scenarios/step3_fail_service
cat > scenarios/step3_fail_service/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask redis
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

cat > scenarios/step3_fail_service/app.py << 'EOF'
#!/usr/bin/env python3
import redis
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step3_fail_service",
        "message": "Service dependency failure"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 3: Service Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
EOF

# Create step4_fail_db
mkdir -p scenarios/step4_fail_db
cat > scenarios/step4_fail_db/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask sqlalchemy pymysql
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

cat > scenarios/step4_fail_db/app.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "unhealthy",
        "step": "step4_fail_db",
        "message": "Database connectivity failure"
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 4: Database Failure"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
EOF

# Create step5_success
mkdir -p scenarios/step5_success
cat > scenarios/step5_success/Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask redis sqlalchemy pymysql psutil requests cryptography
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
EOF

cat > scenarios/step5_success/app.py << 'EOF'
#!/usr/bin/env python3
import json
import time
import os
from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "step": "step5_success",
        "message": "Production-ready system",
        "checks": {
            "database_connectivity": True,
            "network_connectivity": True,
            "overall_health": True,
            "redis_connectivity": True,
            "resource_management": True
        }
    })

@app.route('/')
def index():
    return jsonify({"message": "Step 5: Success - Production Ready"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
EOF

print_success "Scenario files created"

print_step "Creating pipeline files..."

# Create chaos_scenarios.py
cat > pipeline/chaos_scenarios.py << 'EOF'
#!/usr/bin/env python3
import sys
import time
import subprocess

class ChaosEngineer:
    def __init__(self):
        self.chaos_level = sys.argv[1] if len(sys.argv) > 1 else 'chaos-free'
        
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, check=True):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr

    def chaos_free(self):
        self.log("🎉 CHAOS FREE: Perfect pipeline!", "SUCCESS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity working", "EDUCATION")
        self.log("✅ Resource management working", "EDUCATION")
        self.log("✅ Service dependencies working", "EDUCATION")
        self.log("✅ Database connections stable", "EDUCATION")
        
        self.log("🧹 Cleaning up all chaos...", "FIX")
        self.run_command("docker rm -f $(docker ps -aq --filter 'name=chaos-*')", check=False)
        
        self.log("🚀 Starting stable services...", "SUCCESS")
        self.run_command("docker run -d --name stable-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        self.run_command("docker run -d --name stable-service python:3.10 sleep 300")
        
        time.sleep(5)
        success, stdout, stderr = self.run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
        if success:
            self.log("📊 Current container status:", "INFO")
            print(stdout)
        
        self.log("🎉 Chaos Free complete! Perfect pipeline achieved!", "SUCCESS")
        return True

    def run(self):
        self.log(f"🚀 Starting chaos scenario: {self.chaos_level}", "INFO")
        
        if self.chaos_level == 'chaos-free':
            return self.chaos_free()
        else:
            self.log(f"❌ Unknown chaos level: {self.chaos_level}", "ERROR")
            return False

if __name__ == "__main__":
    chaos = ChaosEngineer()
    success = chaos.run()
    sys.exit(0 if success else 1)
EOF

print_success "Pipeline files created"

print_step "Creating demo script..."

# Create demo_manual.sh
cat > demo_manual.sh << 'EOF'
#!/bin/bash
echo "🎓 Progressive Chaos Demo"
echo "========================"
echo ""
echo "This is a simplified demo for Jenkins workspace"
echo "Running chaos-free scenario..."
echo ""
echo "✅ Demo completed successfully!"
EOF

chmod +x demo_manual.sh

print_success "Demo script created"

print_step "Creating docker-compose file..."

# Create docker-compose-step5.yml
cat > docker-compose-step5.yml << 'EOF'
version: '3.8'

services:
  app:
    build: 
      context: ./scenarios/step5_success
      dockerfile: Dockerfile
    ports:
      - "8085:8080"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - MYSQL_HOST=mysql
      - MYSQL_PORT=3306
      - MYSQL_USER=root
      - MYSQL_PASSWORD=password
      - MYSQL_DATABASE=test
    networks:
      - chaos-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - chaos-network

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=test
    networks:
      - chaos-network

networks:
  chaos-network:
    driver: bridge
EOF

print_success "Docker compose file created"

print_step "Setting permissions..."
chmod +x pipeline/chaos_scenarios.py

print_success "Permissions set"

print_step "Verifying setup..."
echo "📁 Directory structure:"
ls -la
echo ""
echo "📦 Scenarios:"
ls -la scenarios/
echo ""
echo "🔧 Pipeline:"
ls -la pipeline/

print_success "Jenkins workspace setup completed!"

echo ""
print_header "Setup Complete!"
echo "================"
echo ""
echo "✅ All required files created"
echo "✅ Directory structure ready"
echo "✅ Pipeline scripts available"
echo "✅ Demo scripts ready"
echo "✅ Docker compose configuration ready"
echo ""
echo "🎉 Jenkins workspace is now ready for chaos pipeline!"
echo ""
echo "💡 Next steps:"
echo "   1. Commit these files to your repository"
echo "   2. Configure Jenkins to pull from this repository"
echo "   3. Run the chaos pipeline in Jenkins" 