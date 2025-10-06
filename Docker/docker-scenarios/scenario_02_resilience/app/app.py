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

def get_resilience_score(container_name):
    """Calculate resilience score for a container"""
    try:
        if not docker_available:
            # Return fallback data for demo
            if "fragile" in container_name:
                return {
                    'score': 0,
                    'uptime': 0,
                    'health_checks': 0,
                    'auto_restarts': 0,
                    'recovery_rate': 0
                }
            elif "resilient" in container_name:
                return {
                    'score': 100,
                    'uptime': 100,
                    'health_checks': 50,
                    'auto_restarts': 5,
                    'recovery_rate': 100
                }
            return None
        
        container = docker_client.containers.get(container_name)
        
        # Analyze container resilience
        score = 0
        uptime = 0
        health_checks = 0
        auto_restarts = 0
        
        # Check restart policy
        restart_policy = container.attrs.get('HostConfig', {}).get('RestartPolicy', {})
        if restart_policy.get('Name') != 'no':
            score += 30
        else:
            score -= 20
        
        # Check health check
        health_config = container.attrs.get('Config', {}).get('Health', {})
        if health_config:
            score += 25
            health_checks = 50  # Simulate health checks
        else:
            score -= 15
        
        # Check resource limits
        memory_limit = container.attrs.get('HostConfig', {}).get('Memory', 0)
        if memory_limit > 0:
            score += 20
        else:
            score -= 10
        
        # Check if container is running
        if container.status == 'running':
            score += 25
            uptime = 100
        else:
            score -= 30
            uptime = 0
        
        # Calculate final score
        score = max(0, min(100, score))
        recovery_rate = 100 if score >= 80 else 50 if score >= 50 else 0
        
        return {
            'score': score,
            'uptime': uptime,
            'health_checks': health_checks,
            'auto_restarts': auto_restarts,
            'recovery_rate': recovery_rate
        }
    except Exception as e:
        logger.error(f"Error calculating resilience score for {container_name}: {e}")
        return None

def get_container_info(container_name):
    """Get detailed information about a container"""
    try:
        if not docker_available:
            # Return fallback data for demo
            if "fragile" in container_name:
                return {
                    'name': container_name,
                    'status': 'running',
                    'image': 'fragile-app',
                    'created': '2024-01-01 12:00:00',
                    'resilience_score': 0,
                    'uptime': 0,
                    'health_checks': 0
                }
            elif "resilient" in container_name:
                return {
                    'name': container_name,
                    'status': 'running',
                    'image': 'resilient-app',
                    'created': '2024-01-01 12:30:00',
                    'resilience_score': 100,
                    'uptime': 100,
                    'health_checks': 50
                }
            return None
        
        container = docker_client.containers.get(container_name)
        created = container.attrs.get('Created', '')
        if created:
            created = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        
        resilience_info = get_resilience_score(container_name)
        
        return {
            'name': container_name,
            'status': container.status,
            'image': container.image.tags[0] if container.image.tags else 'unknown',
            'created': created,
            'resilience_score': resilience_info['score'] if resilience_info else 0,
            'uptime': resilience_info['uptime'] if resilience_info else 0,
            'health_checks': resilience_info['health_checks'] if resilience_info else 0
        }
    except Exception as e:
        logger.error(f"Error getting container info for {container_name}: {e}")
        return None

def get_resilience_metrics():
    """Get overall resilience metrics"""
    try:
        if not docker_available:
            return {
                'total_containers': 2,
                'resilient_containers': 1,
                'fragile_containers': 1,
                'average_resilience_score': 50,
                'total_uptime': 50,
                'health_checks_active': 1
            }
        
        containers = docker_client.containers.list()
        total_containers = len(containers)
        resilient_containers = 0
        fragile_containers = 0
        total_score = 0
        total_uptime = 0
        health_checks_active = 0
        
        for container in containers:
            resilience_info = get_resilience_score(container.name)
            if resilience_info:
                total_score += resilience_info['score']
                total_uptime += resilience_info['uptime']
                
                if resilience_info['score'] >= 80:
                    resilient_containers += 1
                else:
                    fragile_containers += 1
                
                if resilience_info['health_checks'] > 0:
                    health_checks_active += 1
        
        average_score = total_score / total_containers if total_containers > 0 else 0
        average_uptime = total_uptime / total_containers if total_containers > 0 else 0
        
        return {
            'total_containers': total_containers,
            'resilient_containers': resilient_containers,
            'fragile_containers': fragile_containers,
            'average_resilience_score': round(average_score, 1),
            'total_uptime': round(average_uptime, 1),
            'health_checks_active': health_checks_active
        }
    except Exception as e:
        logger.error(f"Error getting resilience metrics: {e}")
        return None

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🛡️ Docker Resilience Dashboard</title>
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
        .resilience-score {
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
        .fragile-card {
            background: rgba(255,0,0,0.1);
            border-left: 5px solid #f44336;
        }
        .resilient-card {
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
            <h1>🛡️ Docker Resilience Dashboard</h1>
            <div class="subtitle">Real-time resilience analysis and monitoring</div>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>📊 Overall Resilience Metrics</h3>
                <div class="metric">
                    <span class="metric-label">Total Containers:</span>
                    <span class="metric-value">{{ metrics.total_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Resilient Containers:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ metrics.resilient_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Fragile Containers:</span>
                    <span class="metric-value" style="color: #f44336;">{{ metrics.fragile_containers }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Average Resilience Score:</span>
                    <span class="metric-value">{{ metrics.average_resilience_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Average Uptime:</span>
                    <span class="metric-value">{{ metrics.total_uptime }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Health Checks Active:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ metrics.health_checks_active }}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🔍 Resilience Analysis</h3>
                <div class="resilience-score {{ 'score-high' if metrics.average_resilience_score >= 80 else 'score-medium' if metrics.average_resilience_score >= 50 else 'score-low' }}">
                    {{ metrics.average_resilience_score }}%
                </div>
                <div class="metric">
                    <span class="metric-label">Resilience Status:</span>
                    <span class="metric-value">
                        {% if metrics.average_resilience_score >= 80 %}
                            🟢 Resilient
                        {% elif metrics.average_resilience_score >= 50 %}
                            🟡 Needs Improvement
                        {% else %}
                            🔴 Fragile
                        {% endif %}
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Risk Level:</span>
                    <span class="metric-value">
                        {% if metrics.fragile_containers == 0 %}
                            🟢 Low Risk
                        {% elif metrics.fragile_containers < 2 %}
                            🟡 Medium Risk
                        {% else %}
                            🔴 High Risk
                        {% endif %}
                    </span>
                </div>
            </div>
        </div>
        
        <div class="comparison">
            <div class="card fragile-card">
                <h3>💥 Fragile Container</h3>
                <div class="metric">
                    <span class="metric-label">Resilience Score:</span>
                    <span class="metric-value" style="color: #f44336;">{{ fragile_info.resilience_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uptime:</span>
                    <span class="metric-value" style="color: #f44336;">{{ fragile_info.uptime }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Health Checks:</span>
                    <span class="metric-value" style="color: #f44336;">{{ fragile_info.health_checks }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value" style="color: #f44336;">{{ fragile_info.status }}</span>
                </div>
            </div>
            
            <div class="card resilient-card">
                <h3>🛡️ Resilient Container</h3>
                <div class="metric">
                    <span class="metric-label">Resilience Score:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ resilient_info.resilience_score }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uptime:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ resilient_info.uptime }}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Health Checks:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ resilient_info.health_checks }}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status:</span>
                    <span class="metric-value" style="color: #4CAF50;">{{ resilient_info.status }}</span>
                </div>
            </div>
        </div>
        
        <div class="auto-refresh">
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            <p>Auto-refreshes every 30 seconds</p>
        </div>
        
        <div class="links">
            <a href="http://localhost:8001" target="_blank">💥 Fragile App</a>
            <a href="http://localhost:8002" target="_blank">🛡️ Resilient App</a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Resilience dashboard main page"""
    logger.info("Resilience dashboard accessed")
    
    # Get resilience metrics
    metrics = get_resilience_metrics()
    if not metrics:
        metrics = {
            'total_containers': 2,
            'resilient_containers': 1,
            'fragile_containers': 1,
            'average_resilience_score': 50,
            'total_uptime': 50,
            'health_checks_active': 1
        }
    
    # Get container information
    fragile_info = get_container_info('fragile-app-demo')
    if not fragile_info:
        fragile_info = {
            'resilience_score': 0,
            'uptime': 0,
            'health_checks': 0,
            'status': 'running'
        }
    
    resilient_info = get_container_info('resilient-app-demo')
    if not resilient_info:
        resilient_info = {
            'resilience_score': 100,
            'uptime': 100,
            'health_checks': 50,
            'status': 'running'
        }
    
    return render_template_string(TEMPLATE, 
        metrics=metrics,
        fragile_info=fragile_info,
        resilient_info=resilient_info
    )

@app.route("/api/metrics")
def api_metrics():
    """API endpoint for resilience metrics"""
    metrics = get_resilience_metrics()
    return jsonify(metrics)

@app.route("/api/containers")
def api_containers():
    """API endpoint for container information"""
    fragile_info = get_container_info('fragile-app-demo')
    resilient_info = get_container_info('resilient-app-demo')
    
    return jsonify({
        'fragile': fragile_info,
        'resilient': resilient_info
    })

@app.route("/api/scan")
def api_scan():
    """API endpoint for resilience scan results"""
    try:
        # Simulate resilience scan
        scan_results = {
            'timestamp': time.time(),
            'fragile_containers': 1,
            'resilient_containers': 1,
            'resilience_recommendations': [
                'Implement health checks for all containers',
                'Configure auto-restart policies',
                'Set resource limits to prevent crashes',
                'Enable graceful shutdown handling',
                'Add monitoring and alerting'
            ],
            'resilience_score': 50
        }
        return jsonify(scan_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info("🛡️ Starting Docker Resilience Dashboard")
    app.run(host="0.0.0.0", port=5000)
