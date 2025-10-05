from flask import Flask, render_template_string, request, jsonify
import subprocess
import json
import os
import time
import logging
import docker
from datetime import datetime
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize Docker client
try:
    docker_client = docker.from_env()
    # Test connection
    docker_client.ping()
    docker_available = True
    logger.info("✅ Docker client connected successfully!")
except Exception as e:
    docker_available = False
    docker_client = None
    logger.warning(f"⚠️ Docker client connection failed (running in fallback mode): {e}")

def get_security_score(container_name):
    """Calculate security score for a container"""
    try:
        if not docker_available:
            # Return fallback data for demo
            if "vulnerable" in container_name:
                return {
                    'score': 0,
                    'vulnerabilities': 15,
                    'secrets_exposed': 8,
                    'user_privileges': 'root',
                    'network_isolation': False,
                    'resource_limits': False
                }
            elif "secure" in container_name:
                return {
                    'score': 100,
                    'vulnerabilities': 0,
                    'secrets_exposed': 0,
                    'user_privileges': 'appuser',
                    'network_isolation': True,
                    'resource_limits': True
                }
            return None
        
        container = docker_client.containers.get(container_name)
        
        # Analyze container security
        score = 0
        vulnerabilities = 0
        secrets_exposed = 0
        
        # Check if running as root
        try:
            result = container.exec_run('whoami')
            if result.output.decode().strip() == 'root':
                vulnerabilities += 5
            else:
                score += 20
        except:
            vulnerabilities += 2
        
        # Check environment variables for secrets
        env_vars = container.attrs.get('Config', {}).get('Env', [])
        for env_var in env_vars:
            if any(secret in env_var.lower() for secret in ['password', 'secret', 'key', 'token']):
                if '=' in env_var and len(env_var.split('=')[1]) > 0:
                    secrets_exposed += 1
        
        # Check network configuration
        network_mode = container.attrs.get('HostConfig', {}).get('NetworkMode', 'default')
        if network_mode == 'host':
            vulnerabilities += 3
        else:
            score += 15
        
        # Check resource limits
        memory_limit = container.attrs.get('HostConfig', {}).get('Memory', 0)
        if memory_limit > 0:
            score += 15
        else:
            vulnerabilities += 2
        
        # Calculate final score
        score = min(100, score + (100 - vulnerabilities * 5))
        
        return {
            'score': max(0, score),
            'vulnerabilities': vulnerabilities,
            'secrets_exposed': secrets_exposed,
            'user_privileges': 'root' if vulnerabilities > 10 else 'limited',
            'network_isolation': network_mode != 'host',
            'resource_limits': memory_limit > 0
        }
    except Exception as e:
        logger.error(f"Error calculating security score for {container_name}: {e}")
        return None

def get_container_info(container_name):
    """Get detailed information about a container"""
    try:
        if not docker_available:
            # Return fallback data for demo
            if "vulnerable" in container_name:
                return {
                    'name': container_name,
                    'status': 'running',
                    'image': 'vulnerable-app',
                    'created': '2024-01-01 12:00:00',
                    'security_score': 0,
                    'vulnerabilities': 15,
                    'secrets_exposed': 8
                }
            elif "secure" in container_name:
                return {
                    'name': container_name,
                    'status': 'running',
                    'image': 'secure-app',
                    'created': '2024-01-01 12:30:00',
                    'security_score': 100,
                    'vulnerabilities': 0,
                    'secrets_exposed': 0
                }
            return None
        
        container = docker_client.containers.get(container_name)
        created = container.attrs.get('Created', '')
        if created:
            created = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        
        security_info = get_security_score(container_name)
        
        return {
            'name': container_name,
            'status': container.status,
            'image': container.image.tags[0] if container.image.tags else 'unknown',
            'created': created,
            'security_score': security_info['score'] if security_info else 0,
            'vulnerabilities': security_info['vulnerabilities'] if security_info else 0,
            'secrets_exposed': security_info['secrets_exposed'] if security_info else 0
        }
    except Exception as e:
        logger.error(f"Error getting container info for {container_name}: {e}")
        return None

def get_security_metrics():
    """Get overall security metrics"""
    try:
        if not docker_available:
            return {
                'total_containers': 2,
                'secure_containers': 1,
                'vulnerable_containers': 1,
                'average_security_score': 50,
                'total_vulnerabilities': 15,
                'secrets_exposed': 8
            }
        
        containers = docker_client.containers.list()
        total_containers = len(containers)
        secure_containers = 0
        vulnerable_containers = 0
        total_score = 0
        total_vulnerabilities = 0
        total_secrets_exposed = 0
        
        for container in containers:
            security_info = get_security_score(container.name)
            if security_info:
                total_score += security_info['score']
                total_vulnerabilities += security_info['vulnerabilities']
                total_secrets_exposed += security_info['secrets_exposed']
                
                if security_info['score'] >= 80:
                    secure_containers += 1
                else:
                    vulnerable_containers += 1
        
        average_score = total_score / total_containers if total_containers > 0 else 0
        
        return {
            'total_containers': total_containers,
            'secure_containers': secure_containers,
            'vulnerable_containers': vulnerable_containers,
            'average_security_score': round(average_score, 1),
            'total_vulnerabilities': total_vulnerabilities,
            'secrets_exposed': total_secrets_exposed
        }
    except Exception as e:
        logger.error(f"Error getting security metrics: {e}")
        return None

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🛡️ Docker Security Dashboard</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 0.2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card h3 {
            margin-top: 0;
            color: #4CAF50;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-label {
            font-weight: bold;
        }
        .metric-value {
            color: #4CAF50;
        }
        .security-score {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
        }
        .score-high {
            color: #4CAF50;
        }
        .score-medium {
            color: #ffeb3b;
        }
        .score-low {
            color: #f44336;
        }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        .vulnerable-card {
            background: rgba(255,0,0,0.1);
            border-left: 5px solid #f44336;
        }
        .secure-card {
            background: rgba(76, 175, 80, 0.1);
            border-left: 5px solid #4CAF50;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px 0;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
        .auto-refresh {
            text-align: center;
            margin: 20px 0;
            color: rgba(255,255,255,0.7);
        }
        .links {
            text-align: center;
            margin-top: 30px;
        }
        .links a {
            color: #4CAF50;
            text-decoration: none;
            margin: 0 15px;
            font-size: 1.1em;
        }
        .links a:hover {
            text-decoration: underline;
        }
    </style>
    <script>
        function refreshData() {
            location.reload();
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Docker Security Dashboard</h1>
            <div class="subtitle">Real-time security analysis and monitoring</div>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>📊 Overall Security Metrics</h3>
                <div class="metric">
                    <span class="metric-label">Total Containers:</span>
                    <span class="metric-value">{{ metrics.total_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Secure Containers:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ metrics.secure_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Vulnerable Containers:</span>
                    <span class="metric-value" style="color: #f44336;">{{ metrics.vulnerable_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Average Security Score:</span>
                    <span class="metric-value">{{ metrics.average_security_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Vulnerabilities:</span>
                    <span class="metric-value" style="color: #f44336;">{{ metrics.total_vulnerabilities }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Secrets Exposed:</span>
                    <span class="metric-value" style="color: #f44336;">{{ metrics.secrets_exposed }}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🔍 Security Analysis</h3>
                <div class="security-score {{ 'score-high' if metrics.average_security_score >= 80 else 'score-medium' if metrics.average_security_score >= 50 else 'score-low' }}">
                    {{ metrics.average_security_score }}%
                </div>
                <div class="metric">
                    <span class="metric-label">Security Status:</span>
                    <span class="metric-value">
                        {% if metrics.average_security_score >= 80 %}
                            🟢 Secure
                        {% elif metrics.average_security_score >= 50 %}
                            🟡 Needs Improvement
                        {% else %}
                            🔴 Critical
                        {% endif %}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Risk Level:</span>
                    <span class="metric-value">
                        {% if metrics.total_vulnerabilities == 0 %}
                            🟢 Low Risk
                        {% elif metrics.total_vulnerabilities < 5 %}
                            🟡 Medium Risk
                        {% else %}
                            🔴 High Risk
                        {% endif %}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="comparison">
            <div class="card vulnerable-card">
                <h3>🚨 Vulnerable Container</h3>
                <div class="metric">
                    <span class="metric-label">Security Score:</span>
                    <span class="metric-value" style="color: #f44336;">{{ vulnerable_info.security_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Vulnerabilities:</span>
                    <span class="metric-value" style="color: #f44336;">{{ vulnerable_info.vulnerabilities }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Secrets Exposed:</span>
                    <span class="metric-value" style="color: #f44336;">{{ vulnerable_info.secrets_exposed }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value" style="color: #f44336;">{{ vulnerable_info.status }}</span>
                </div>
            </div>
            
            <div class="card secure-card">
                <h3>🔒 Secure Container</h3>
                <div class="metric">
                    <span class="metric-label">Security Score:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ secure_info.security_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Vulnerabilities:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ secure_info.vulnerabilities }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Secrets Exposed:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ secure_info.secrets_exposed }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ secure_info.status }}</span>
                </div>
            </div>
        </div>
        
        <div class="auto-refresh">
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            <p>Auto-refreshes every 30 seconds</p>
        </div>
        
        <div class="links">
            <a href="http://localhost:8001" target="_blank">🚨 Vulnerable App</a>
            <a href="http://localhost:8002" target="_blank">🔒 Secure App</a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Security dashboard main page"""
    logger.info("Security dashboard accessed")
    
    # Get security metrics
    metrics = get_security_metrics()
    if not metrics:
        metrics = {
            'total_containers': 2,
            'secure_containers': 1,
            'vulnerable_containers': 1,
            'average_security_score': 50,
            'total_vulnerabilities': 15,
            'secrets_exposed': 8
        }
    
    # Get container information
    vulnerable_info = get_container_info('vulnerable-app-demo')
    if not vulnerable_info:
        vulnerable_info = {
            'security_score': 0,
            'vulnerabilities': 15,
            'secrets_exposed': 8,
            'status': 'running'
        }
    
    secure_info = get_container_info('secure-app-demo')
    if not secure_info:
        secure_info = {
            'security_score': 100,
            'vulnerabilities': 0,
            'secrets_exposed': 0,
            'status': 'running'
        }
    
    return render_template_string(TEMPLATE, 
        metrics=metrics,
        vulnerable_info=vulnerable_info,
        secure_info=secure_info
    )

@app.route("/api/metrics")
def api_metrics():
    """API endpoint for security metrics"""
    metrics = get_security_metrics()
    return jsonify(metrics)

@app.route("/api/containers")
def api_containers():
    """API endpoint for container information"""
    vulnerable_info = get_container_info('vulnerable-app-demo')
    secure_info = get_container_info('secure-app-demo')
    
    return jsonify({
        'vulnerable': vulnerable_info,
        'secure': secure_info
    })

@app.route("/api/scan")
def api_scan():
    """API endpoint for security scan results"""
    try:
        # Simulate security scan
        scan_results = {
            'timestamp': time.time(),
            'vulnerabilities_found': 15,
            'secrets_exposed': 8,
            'security_recommendations': [
                'Use Docker secrets for sensitive data',
                'Run containers as non-root user',
                'Implement network isolation',
                'Set resource limits',
                'Enable security scanning'
            ],
            'compliance_score': 50
        }
        return jsonify(scan_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info("🛡️ Starting Docker Security Dashboard")
    app.run(host="0.0.0.0", port=5000)
