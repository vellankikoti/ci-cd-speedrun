#!/usr/bin/env python3
"""
Live CI/CD Deployment Simulator
Real-time, Interactive, Dynamic Learning Platform
"""
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import os
import time
import threading
import random
from datetime import datetime
from collections import deque

app = Flask(__name__)
CORS(app)

# Configuration
DEPLOYMENT_STRATEGY = os.environ.get('DEPLOYMENT_STRATEGY', 'Blue-Green')
APP_COMPLEXITY = os.environ.get('APP_COMPLEXITY', 'Simple')
INITIAL_VERSION = os.environ.get('INITIAL_VERSION', '1.0.0')
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', '1')

# Live application state (changes in real-time)
class DeploymentState:
    def __init__(self):
        self.environments = {
            'blue': {'version': '0.9.0', 'status': 'running', 'traffic': 100, 'health': 100, 'requests': 0},
            'green': {'version': INITIAL_VERSION, 'status': 'deploying', 'traffic': 0, 'health': 0, 'requests': 0}
        }
        self.deployment_progress = 0
        self.deployment_status = 'ready'
        self.deployment_logs = deque(maxlen=50)
        self.metrics = {
            'total_requests': 0,
            'successful_deploys': 0,
            'failed_deploys': 0,
            'rollbacks': 0,
            'avg_response_time': 45,
            'error_rate': 0.1
        }
        self.canary_stage = 0
        self.rolling_instance = 0
        self.last_action_time = datetime.now()

        # Start background tasks
        self.running = True
        threading.Thread(target=self._simulate_traffic, daemon=True).start()
        threading.Thread(target=self._health_monitor, daemon=True).start()

    def _simulate_traffic(self):
        """Simulate incoming traffic to environments"""
        while self.running:
            time.sleep(0.5)
            for env in ['blue', 'green']:
                if self.environments[env]['status'] == 'running' and self.environments[env]['traffic'] > 0:
                    # Simulate requests based on traffic percentage
                    requests = int(random.randint(5, 15) * (self.environments[env]['traffic'] / 100))
                    self.environments[env]['requests'] += requests
                    self.metrics['total_requests'] += requests

                    # Random response time variation
                    self.metrics['avg_response_time'] = random.randint(40, 60)

                    # Simulate occasional errors
                    if random.random() < 0.02:
                        self.metrics['error_rate'] = min(5.0, self.metrics['error_rate'] + 0.1)
                    else:
                        self.metrics['error_rate'] = max(0.1, self.metrics['error_rate'] - 0.05)

    def _health_monitor(self):
        """Monitor and update health status"""
        while self.running:
            time.sleep(1)
            for env in ['blue', 'green']:
                if self.environments[env]['status'] == 'running':
                    # Healthy environments stay healthy
                    target_health = 100
                elif self.environments[env]['status'] == 'deploying':
                    # Deploying environments gradually become healthy
                    target_health = min(100, self.environments[env]['health'] + 10)
                elif self.environments[env]['status'] == 'stopped':
                    # Stopped environments lose health
                    target_health = 0
                else:
                    target_health = self.environments[env]['health']

                # Gradually adjust health
                current = self.environments[env]['health']
                if current < target_health:
                    self.environments[env]['health'] = min(100, current + 5)
                elif current > target_health:
                    self.environments[env]['health'] = max(0, current - 10)

    def add_log(self, message):
        """Add timestamped log entry"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.deployment_logs.append(f"[{timestamp}] {message}")

state = DeploymentState()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
        deployment_strategy=DEPLOYMENT_STRATEGY,
        app_complexity=APP_COMPLEXITY,
        build_number=BUILD_NUMBER)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/state')
def get_state():
    """Get current deployment state"""
    return jsonify({
        'environments': state.environments,
        'deployment_progress': state.deployment_progress,
        'deployment_status': state.deployment_status,
        'metrics': state.metrics,
        'canary_stage': state.canary_stage,
        'rolling_instance': state.rolling_instance,
        'logs': list(state.deployment_logs),
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/deploy', methods=['POST'])
def deploy():
    """Trigger deployment based on strategy"""
    data = request.json
    version = data.get('version', '2.0.0')

    if state.deployment_status == 'deploying':
        return jsonify({'error': 'Deployment already in progress'}), 400

    strategy = DEPLOYMENT_STRATEGY
    state.deployment_status = 'deploying'
    state.deployment_progress = 0
    state.add_log(f"🚀 Starting {strategy} deployment to version {version}")

    # Start deployment in background
    threading.Thread(target=_execute_deployment, args=(version, strategy), daemon=True).start()

    return jsonify({'status': 'started', 'strategy': strategy, 'version': version})

@app.route('/api/rollback', methods=['POST'])
def rollback():
    """Rollback to previous version"""
    state.add_log("🔄 Initiating rollback...")

    # Instant rollback for Blue-Green
    if DEPLOYMENT_STRATEGY == 'Blue-Green':
        blue_traffic = state.environments['blue']['traffic']
        green_traffic = state.environments['green']['traffic']

        state.environments['blue']['traffic'] = green_traffic
        state.environments['green']['traffic'] = blue_traffic

        state.add_log("✅ Rollback complete! Traffic switched back instantly")
        state.metrics['rollbacks'] += 1
    else:
        state.add_log("⚠️ Rollback in progress...")
        # For other strategies, do gradual rollback
        threading.Thread(target=_execute_rollback, daemon=True).start()

    return jsonify({'status': 'rollback_initiated'})

@app.route('/api/simulate-failure', methods=['POST'])
def simulate_failure():
    """Simulate deployment failure for learning"""
    data = request.json
    env = data.get('environment', 'green')

    state.environments[env]['status'] = 'unhealthy'
    state.environments[env]['health'] = 20
    state.add_log(f"⚠️ Health check failed for {env} environment!")
    state.metrics['error_rate'] = 5.0

    return jsonify({'status': 'failure_simulated', 'environment': env})

@app.route('/api/recover', methods=['POST'])
def recover():
    """Recover from failure"""
    data = request.json
    env = data.get('environment', 'green')

    state.environments[env]['status'] = 'running'
    state.add_log(f"✅ {env} environment recovered!")

    return jsonify({'status': 'recovered', 'environment': env})

def _execute_deployment(version, strategy):
    """Execute deployment based on strategy"""
    try:
        if strategy == 'Blue-Green':
            _deploy_blue_green(version)
        elif strategy == 'Canary':
            _deploy_canary(version)
        elif strategy == 'Rolling':
            _deploy_rolling(version)
        elif strategy == 'Recreate':
            _deploy_recreate(version)

        state.deployment_status = 'completed'
        state.metrics['successful_deploys'] += 1
        state.add_log(f"✅ Deployment to version {version} completed successfully!")
    except Exception as e:
        state.deployment_status = 'failed'
        state.metrics['failed_deploys'] += 1
        state.add_log(f"❌ Deployment failed: {str(e)}")

def _deploy_blue_green(version):
    """Blue-Green deployment simulation"""
    state.add_log("📦 Deploying to Green environment...")
    state.environments['green']['version'] = version
    state.environments['green']['status'] = 'deploying'

    # Simulate deployment
    for i in range(0, 101, 10):
        state.deployment_progress = i
        time.sleep(0.3)

    state.environments['green']['status'] = 'running'
    state.add_log("✅ Green environment ready")

    # Wait for health checks
    state.add_log("🏥 Running health checks...")
    time.sleep(1)

    # Switch traffic
    state.add_log("🔄 Switching traffic from Blue to Green...")
    for traffic in range(0, 101, 20):
        state.environments['blue']['traffic'] = 100 - traffic
        state.environments['green']['traffic'] = traffic
        state.add_log(f"   Traffic: Blue {100-traffic}% → Green {traffic}%")
        time.sleep(0.5)

    state.environments['blue']['status'] = 'standby'
    state.add_log("✅ Traffic switched! Blue environment on standby for rollback")

def _deploy_canary(version):
    """Canary deployment simulation"""
    state.add_log("📦 Deploying Canary version...")
    state.environments['green']['version'] = version
    state.environments['green']['status'] = 'deploying'

    # Deploy canary
    for i in range(0, 101, 10):
        state.deployment_progress = i
        time.sleep(0.3)

    state.environments['green']['status'] = 'running'

    # Gradual traffic shift: 10% -> 25% -> 50% -> 75% -> 100%
    stages = [10, 25, 50, 75, 100]
    for stage_traffic in stages:
        state.canary_stage = stages.index(stage_traffic)
        state.add_log(f"📊 Canary stage {state.canary_stage + 1}: Routing {stage_traffic}% traffic...")

        state.environments['green']['traffic'] = stage_traffic
        state.environments['blue']['traffic'] = 100 - stage_traffic

        state.add_log(f"   Monitoring metrics at {stage_traffic}% traffic...")
        time.sleep(1.5)

        # Check if health is good
        if state.environments['green']['health'] < 50:
            state.add_log(f"⚠️ Health degraded! Stopping canary rollout")
            raise Exception("Canary health check failed")

    state.environments['blue']['status'] = 'stopped'
    state.add_log("✅ Canary deployment successful! Old version stopped")

def _deploy_rolling(version):
    """Rolling deployment simulation"""
    instances = 4
    state.add_log(f"📦 Rolling deployment across {instances} instances...")

    for instance in range(instances):
        state.rolling_instance = instance
        state.deployment_progress = int((instance / instances) * 100)

        state.add_log(f"🔄 Updating instance {instance + 1}/{instances}...")
        state.add_log(f"   Stopping instance {instance + 1}...")
        time.sleep(0.5)

        state.add_log(f"   Starting instance {instance + 1} with version {version}...")
        time.sleep(0.5)

        state.add_log(f"   Health check for instance {instance + 1}...")
        time.sleep(0.5)

        state.add_log(f"✅ Instance {instance + 1} updated successfully")

    state.deployment_progress = 100
    state.environments['green']['version'] = version
    state.environments['green']['traffic'] = 100
    state.environments['blue']['traffic'] = 0
    state.environments['blue']['status'] = 'stopped'
    state.add_log("✅ Rolling deployment complete!")

def _deploy_recreate(version):
    """Recreate deployment simulation"""
    state.add_log("⚠️ Stopping all instances (downtime expected)...")
    state.environments['blue']['status'] = 'stopped'
    state.environments['blue']['traffic'] = 0
    state.environments['green']['traffic'] = 0
    time.sleep(1)

    state.add_log("📦 Deploying new version...")
    state.environments['green']['version'] = version
    state.environments['green']['status'] = 'deploying'

    for i in range(0, 101, 20):
        state.deployment_progress = i
        time.sleep(0.4)

    state.add_log("🚀 Starting new instances...")
    time.sleep(1)

    state.environments['green']['status'] = 'running'
    state.environments['green']['traffic'] = 100
    state.deployment_progress = 100
    state.add_log("✅ New version deployed and serving traffic")

def _execute_rollback():
    """Execute rollback"""
    state.add_log("🔄 Rolling back deployment...")

    # Reverse traffic
    for traffic in range(0, 101, 20):
        state.environments['blue']['traffic'] = traffic
        state.environments['green']['traffic'] = 100 - traffic
        time.sleep(0.3)

    state.environments['green']['status'] = 'stopped'
    state.environments['blue']['status'] = 'running'
    state.add_log("✅ Rollback complete!")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Mastery - Live Deployment Simulator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #fff;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .subtitle { font-size: 1.2em; opacity: 0.9; }
        .config {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
        }
        .config-item { display: flex; flex-direction: column; align-items: center; }
        .config-label { font-size: 0.9em; opacity: 0.8; margin-bottom: 5px; }
        .config-value { font-size: 1.3em; font-weight: bold; }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        @media (max-width: 1024px) { .main-grid { grid-template-columns: 1fr; } }
        .card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .card-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .environments { display: flex; gap: 15px; margin-bottom: 20px; }
        .environment {
            flex: 1;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
            position: relative;
            overflow: hidden;
        }
        .environment.blue { border: 2px solid #3b82f6; }
        .environment.green { border: 2px solid #10b981; }
        .env-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .env-name { font-size: 1.3em; font-weight: bold; }
        .env-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .env-status.running { background: #10b981; }
        .env-status.deploying { background: #f59e0b; animation: pulse 1s infinite; }
        .env-status.stopped { background: #6b7280; }
        .env-status.standby { background: #3b82f6; }
        .env-status.unhealthy { background: #ef4444; animation: flash 0.5s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        @keyframes flash { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .env-details { margin-top: 10px; }
        .env-detail {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 0.95em;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #3b82f6);
            transition: width 0.3s ease;
        }
        .traffic-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: rgba(59, 130, 246, 0.5);
            transition: width 0.5s ease;
        }
        .controls { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .btn-primary { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
        .btn-danger { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
        .btn-warning { background: linear-gradient(135deg, #ffecd2, #fcb69f); color: #333; }
        .metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        @media (max-width: 768px) { .metrics-grid { grid-template-columns: 1fr; } }
        .metric {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-label { font-size: 0.9em; opacity: 0.8; margin-bottom: 5px; }
        .metric-value { font-size: 2em; font-weight: bold; }
        .logs {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            padding: 15px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #3b82f6;
            padding-left: 10px;
        }
        .log-entry:nth-child(even) { background: rgba(255, 255, 255, 0.05); }
        .deployment-progress { margin: 20px 0; }
        .version-input {
            padding: 10px;
            border-radius: 6px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(0, 0, 0, 0.2);
            color: white;
            font-size: 1em;
            margin-right: 10px;
        }
        .strategy-info {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 CI/CD Mastery</h1>
            <div class="subtitle">
                <span class="live-indicator"></span>
                Live Deployment Simulator - {{ deployment_strategy }} Strategy
            </div>
        </div>
        <div class="config">
            <div class="config-item">
                <div class="config-label">Strategy</div>
                <div class="config-value">{{ deployment_strategy }}</div>
            </div>
            <div class="config-item">
                <div class="config-label">Complexity</div>
                <div class="config-value">{{ app_complexity }}</div>
            </div>
            <div class="config-item">
                <div class="config-label">Build</div>
                <div class="config-value">#{{ build_number }}</div>
            </div>
            <div class="config-item">
                <div class="config-label">Status</div>
                <div class="config-value" id="deployment-status">Ready</div>
            </div>
        </div>
        <div class="main-grid">
            <div class="card">
                <div class="card-title">🏭 Live Environments</div>
                <div class="environments" id="environments"></div>
                <div class="strategy-info">
                    <strong>{{ deployment_strategy }} Strategy:</strong>
                    <div id="strategy-description"></div>
                </div>
                <div class="deployment-progress">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>Deployment Progress</span>
                        <span id="progress-percent">0%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                    </div>
                </div>
                <div class="controls">
                    <input type="text" class="version-input" id="version-input" placeholder="Version (e.g., 2.0.0)" value="2.0.0">
                    <button class="btn btn-primary" onclick="deploy()">🚀 Deploy</button>
                    <button class="btn btn-danger" onclick="rollback()">🔄 Rollback</button>
                    <button class="btn btn-warning" onclick="simulateFailure()">⚠️ Simulate Failure</button>
                </div>
            </div>
            <div class="card">
                <div class="card-title">📊 Live Metrics</div>
                <div class="metrics-grid" id="metrics"></div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">📝 Deployment Logs</div>
            <div class="logs" id="logs">
                <div class="log-entry">[Ready] Waiting for deployment action...</div>
            </div>
        </div>
    </div>
    <script>
        const strategyDescriptions = {
            'Blue-Green': 'Deploy to Green, switch traffic instantly, Blue on standby for instant rollback',
            'Canary': 'Gradually route traffic: 10% → 25% → 50% → 75% → 100%, monitor at each stage',
            'Rolling': 'Update instances one by one, zero downtime, resource efficient',
            'Recreate': 'Stop all instances, deploy new version, brief downtime expected'
        };
        document.getElementById('strategy-description').textContent = strategyDescriptions['{{ deployment_strategy }}'] || '';
        let isDeploying = false;
        function updateState() {
            fetch('/api/state')
                .then(res => res.json())
                .then(data => {
                    const envsHtml = Object.entries(data.environments).map(([name, env]) => `
                        <div class="environment ${name}">
                            <div class="env-header">
                                <div class="env-name">${name.toUpperCase()}</div>
                                <div class="env-status ${env.status}">${env.status.toUpperCase()}</div>
                            </div>
                            <div class="env-details">
                                <div class="env-detail"><span>Version:</span><strong>${env.version}</strong></div>
                                <div class="env-detail"><span>Health:</span><strong>${env.health}%</strong></div>
                                <div class="env-detail"><span>Traffic:</span><strong>${env.traffic}%</strong></div>
                                <div class="progress-bar"><div class="progress-fill" style="width: ${env.traffic}%"></div></div>
                                <div class="env-detail"><span>Requests:</span><strong>${env.requests.toLocaleString()}</strong></div>
                            </div>
                            <div class="traffic-bar" style="width: ${env.traffic}%"></div>
                        </div>
                    `).join('');
                    document.getElementById('environments').innerHTML = envsHtml;
                    document.getElementById('progress-fill').style.width = data.deployment_progress + '%';
                    document.getElementById('progress-percent').textContent = data.deployment_progress + '%';
                    document.getElementById('deployment-status').textContent = data.deployment_status.toUpperCase();
                    isDeploying = data.deployment_status === 'deploying';
                    const metricsHtml = `
                        <div class="metric"><div class="metric-label">Total Requests</div><div class="metric-value">${data.metrics.total_requests.toLocaleString()}</div></div>
                        <div class="metric"><div class="metric-label">Successful Deploys</div><div class="metric-value">${data.metrics.successful_deploys}</div></div>
                        <div class="metric"><div class="metric-label">Failed Deploys</div><div class="metric-value">${data.metrics.failed_deploys}</div></div>
                        <div class="metric"><div class="metric-label">Rollbacks</div><div class="metric-value">${data.metrics.rollbacks}</div></div>
                        <div class="metric"><div class="metric-label">Avg Response Time</div><div class="metric-value">${data.metrics.avg_response_time}ms</div></div>
                        <div class="metric"><div class="metric-label">Error Rate</div><div class="metric-value">${data.metrics.error_rate.toFixed(2)}%</div></div>
                    `;
                    document.getElementById('metrics').innerHTML = metricsHtml;
                    const logsHtml = data.logs.map(log => `<div class="log-entry">${log}</div>`).join('');
                    const logsContainer = document.getElementById('logs');
                    logsContainer.innerHTML = logsHtml;
                    logsContainer.scrollTop = logsContainer.scrollHeight;
                })
                .catch(err => console.error('Error fetching state:', err));
        }
        function deploy() {
            if (isDeploying) { alert('Deployment already in progress!'); return; }
            const version = document.getElementById('version-input').value || '2.0.0';
            fetch('/api/deploy', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({version}) })
                .then(res => res.json())
                .then(data => console.log('Deployment started:', data))
                .catch(err => alert('Deployment failed: ' + err));
        }
        function rollback() {
            if (!confirm('Are you sure you want to rollback?')) return;
            fetch('/api/rollback', {method: 'POST'})
                .then(res => res.json())
                .then(data => console.log('Rollback initiated:', data))
                .catch(err => alert('Rollback failed: ' + err));
        }
        function simulateFailure() {
            const env = prompt('Which environment to fail? (blue/green)', 'green');
            if (!env) return;
            fetch('/api/simulate-failure', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({environment: env}) })
                .then(res => res.json())
                .then(data => console.log('Failure simulated:', data))
                .catch(err => alert('Failed to simulate failure: ' + err));
        }
        setInterval(updateState, 500);
        updateState();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    state.add_log(f"🎯 CI/CD Simulator started with {DEPLOYMENT_STRATEGY} strategy")
    state.add_log(f"📊 Complexity level: {APP_COMPLEXITY}")
    state.add_log(f"📦 Initial version: {INITIAL_VERSION}")
    state.add_log("✨ Ready for interactive deployments!")

    app.run(host='0.0.0.0', port=8080, threaded=True)
