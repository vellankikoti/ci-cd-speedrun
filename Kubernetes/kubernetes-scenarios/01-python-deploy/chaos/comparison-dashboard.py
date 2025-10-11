#!/usr/bin/env python3
"""
🎨 KUBERNETES DEPLOYMENT COMPARISON DASHBOARD
Visual comparison: Chaos (Manual YAML) vs Hero (Python Automation)
"""

from flask import Flask, render_template_string, jsonify
import subprocess
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Global state
deployment_state = {
    'chaos': {
        'status': 'unknown',
        'pods_running': 0,
        'pods_desired': 2,
        'services': 0,
        'errors': [],
        'deployment_time': 0,
        'uptime_percent': 0,
    },
    'hero': {
        'status': 'unknown',
        'pods_running': 0,
        'pods_desired': 2,
        'services': 0,
        'errors': [],
        'deployment_time': 0,
        'uptime_percent': 0,
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧨 Kubernetes Deployment Comparison</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #fff;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            padding: 30px 0;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }

        .comparison-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }

        .deployment-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }

        .deployment-card:hover {
            transform: translateY(-5px);
        }

        .chaos-card {
            border-left: 5px solid #ef4444;
        }

        .hero-card {
            border-left: 5px solid #10b981;
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
        }

        .card-title {
            font-size: 2em;
            font-weight: bold;
        }

        .status-badge {
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-healthy {
            background: #10b981;
            color: white;
        }

        .status-degraded {
            background: #f59e0b;
            color: white;
        }

        .status-failed {
            background: #ef4444;
            color: white;
        }

        .status-unknown {
            background: #6b7280;
            color: white;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }

        .metric {
            background: rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .metric-value.good {
            color: #10b981;
        }

        .metric-value.bad {
            color: #ef4444;
        }

        .metric-value.warning {
            color: #f59e0b;
        }

        .metric-label {
            font-size: 0.9em;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .progress-bar {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin-bottom: 25px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            transition: width 0.5s ease;
        }

        .progress-fill.chaos-progress {
            background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        }

        .error-list {
            background: rgba(239, 68, 68, 0.2);
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 10px;
            max-height: 200px;
            overflow-y: auto;
        }

        .error-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .error-item:last-child {
            border-bottom: none;
        }

        .comparison-table {
            width: 100%;
            margin-top: 30px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .comparison-table table {
            width: 100%;
            border-collapse: collapse;
        }

        .comparison-table th {
            padding: 15px;
            text-align: left;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            font-size: 1.1em;
        }

        .comparison-table td {
            padding: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: .5;
            }
        }

        .refresh-indicator {
            text-align: center;
            margin-top: 20px;
            opacity: 0.7;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧨 vs 🦸 Kubernetes Deployment Battle</h1>
            <p>Manual YAML Chaos vs Python Automation Hero</p>
        </div>

        <div class="comparison-grid">
            <!-- Chaos Card -->
            <div class="deployment-card chaos-card">
                <div class="card-header">
                    <div class="card-title">🧨 Chaos Deploy</div>
                    <div class="status-badge" id="chaos-status">
                        <span class="pulse">●</span> Checking...
                    </div>
                </div>

                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value bad" id="chaos-pods">0/2</div>
                        <div class="metric-label">Pods Ready</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value bad" id="chaos-uptime">0%</div>
                        <div class="metric-label">Uptime</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value bad" id="chaos-services">0</div>
                        <div class="metric-label">Services</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value bad" id="chaos-time">N/A</div>
                        <div class="metric-label">Deploy Time</div>
                    </div>
                </div>

                <div class="progress-bar">
                    <div class="progress-fill chaos-progress" id="chaos-progress" style="width: 0%">
                        0% Healthy
                    </div>
                </div>

                <div id="chaos-errors" class="error-list" style="display: none;">
                    <strong>⚠️ Errors Detected:</strong>
                    <div id="chaos-error-content"></div>
                </div>
            </div>

            <!-- Hero Card -->
            <div class="deployment-card hero-card">
                <div class="card-header">
                    <div class="card-title">🦸 Hero Deploy</div>
                    <div class="status-badge" id="hero-status">
                        <span class="pulse">●</span> Checking...
                    </div>
                </div>

                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value good" id="hero-pods">0/2</div>
                        <div class="metric-label">Pods Ready</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value good" id="hero-uptime">0%</div>
                        <div class="metric-label">Uptime</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value good" id="hero-services">0</div>
                        <div class="metric-label">Services</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value good" id="hero-time">N/A</div>
                        <div class="metric-label">Deploy Time</div>
                    </div>
                </div>

                <div class="progress-bar">
                    <div class="progress-fill" id="hero-progress" style="width: 0%">
                        0% Healthy
                    </div>
                </div>

                <div id="hero-errors" class="error-list" style="display: none;">
                    <strong>⚠️ Errors Detected:</strong>
                    <div id="hero-error-content"></div>
                </div>
            </div>
        </div>

        <div class="comparison-table">
            <h2 style="margin-bottom: 20px;">📊 Feature Comparison</h2>
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>🧨 Manual YAML (Chaos)</th>
                        <th>🦸 Python Automation (Hero)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Deployment Method</strong></td>
                        <td>❌ Manual kubectl apply</td>
                        <td>✅ One Python command</td>
                    </tr>
                    <tr>
                        <td><strong>Validation</strong></td>
                        <td>❌ No pre-flight checks</td>
                        <td>✅ Automatic validation</td>
                    </tr>
                    <tr>
                        <td><strong>Port Management</strong></td>
                        <td>❌ Manual, error-prone</td>
                        <td>✅ Auto-detect conflicts</td>
                    </tr>
                    <tr>
                        <td><strong>Error Handling</strong></td>
                        <td>❌ Cryptic messages</td>
                        <td>✅ Clear, actionable errors</td>
                    </tr>
                    <tr>
                        <td><strong>Cross-Platform</strong></td>
                        <td>⚠️ Platform-specific issues</td>
                        <td>✅ Works everywhere</td>
                    </tr>
                    <tr>
                        <td><strong>Health Monitoring</strong></td>
                        <td>❌ Manual checking</td>
                        <td>✅ Real-time dashboard</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="refresh-indicator">
            <p>🔄 Dashboard refreshes every 5 seconds | Last update: <span id="last-update">Never</span></p>
        </div>
    </div>

    <script>
        function updateDashboard() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Update chaos metrics
                    updateCard('chaos', data.chaos);
                    updateCard('hero', data.hero);

                    // Update timestamp
                    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
                })
                .catch(error => console.error('Error fetching status:', error));
        }

        function updateCard(type, data) {
            const prefix = type;

            // Update status badge
            const statusBadge = document.getElementById(`${prefix}-status`);
            statusBadge.className = `status-badge status-${data.status}`;
            statusBadge.innerHTML = `<span class="pulse">●</span> ${data.status.toUpperCase()}`;

            // Update metrics
            document.getElementById(`${prefix}-pods`).textContent = `${data.pods_running}/${data.pods_desired}`;
            document.getElementById(`${prefix}-uptime`).textContent = `${data.uptime_percent}%`;
            document.getElementById(`${prefix}-services`).textContent = data.services;
            document.getElementById(`${prefix}-time`).textContent = data.deployment_time > 0 ? `${data.deployment_time}s` : 'N/A';

            // Update progress bar
            const progress = document.getElementById(`${prefix}-progress`);
            const healthPercent = (data.pods_running / data.pods_desired) * 100;
            progress.style.width = `${healthPercent}%`;
            progress.textContent = `${Math.round(healthPercent)}% Healthy`;

            // Update errors
            const errorDiv = document.getElementById(`${prefix}-errors`);
            const errorContent = document.getElementById(`${prefix}-error-content`);

            if (data.errors && data.errors.length > 0) {
                errorDiv.style.display = 'block';
                errorContent.innerHTML = data.errors.map(e =>
                    `<div class="error-item">❌ ${e}</div>`
                ).join('');
            } else {
                errorDiv.style.display = 'none';
            }

            // Update metric value colors
            const podsEl = document.getElementById(`${prefix}-pods`);
            podsEl.className = `metric-value ${data.pods_running === data.pods_desired ? 'good' : 'bad'}`;

            const uptimeEl = document.getElementById(`${prefix}-uptime`);
            uptimeEl.className = `metric-value ${data.uptime_percent > 80 ? 'good' : (data.uptime_percent > 0 ? 'warning' : 'bad')}`;
        }

        // Initial load
        updateDashboard();

        // Auto-refresh every 5 seconds
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
"""

def check_deployment_status(namespace):
    """Check the status of a deployment"""
    status = {
        'status': 'unknown',
        'pods_running': 0,
        'pods_desired': 2,
        'services': 0,
        'errors': [],
        'deployment_time': 0,
        'uptime_percent': 0,
    }

    try:
        # Check pods
        cmd = f"kubectl get pods -n {namespace} -o json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            pods_data = json.loads(result.stdout)
            items = pods_data.get('items', [])

            running = sum(1 for item in items if item.get('status', {}).get('phase') == 'Running')
            status['pods_running'] = running
            status['pods_desired'] = len(items) if len(items) > 0 else 2

            # Check for errors in pod status
            for item in items:
                pod_name = item['metadata']['name']
                pod_status = item.get('status', {})
                container_statuses = pod_status.get('containerStatuses', [])

                for cs in container_statuses:
                    waiting = cs.get('state', {}).get('waiting', {})
                    if waiting:
                        reason = waiting.get('reason', 'Unknown')
                        status['errors'].append(f"{pod_name}: {reason}")

            # Calculate uptime percentage
            if status['pods_desired'] > 0:
                status['uptime_percent'] = int((running / status['pods_desired']) * 100)

        # Check services
        cmd = f"kubectl get svc -n {namespace} -o json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            svc_data = json.loads(result.stdout)
            status['services'] = len(svc_data.get('items', []))

        # Determine overall status
        if status['pods_running'] == status['pods_desired'] and status['services'] > 0:
            status['status'] = 'healthy'
        elif status['pods_running'] > 0:
            status['status'] = 'degraded'
        else:
            status['status'] = 'failed'

    except Exception as e:
        status['errors'].append(str(e))
        status['status'] = 'unknown'

    return status

@app.route('/')
def index():
    """Serve the dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Get current deployment status"""
    chaos_status = check_deployment_status('vote-app-chaos')
    hero_status = check_deployment_status('vote-app')

    return jsonify({
        'chaos': chaos_status,
        'hero': hero_status,
        'timestamp': datetime.now().isoformat()
    })

def find_free_port(start_port=5000, max_attempts=100):
    """Find a free port starting from start_port"""
    import socket

    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue

    # Fallback to random port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🎨 Kubernetes Deployment Comparison Dashboard")
    print("="*70 + "\n")

    # Find available port
    port = find_free_port(5000)

    print("📊 Starting dashboard server...")
    print(f"   🌐 URL: http://localhost:{port}")
    if port != 5000:
        print(f"   ℹ️  Port 5000 was busy, using port {port} instead")
    print("   🔄 Auto-refreshes every 5 seconds")
    print("\n💡 This dashboard compares:")
    print("   🧨 Chaos: Manual YAML deployment (broken)")
    print("   🦸 Hero: Python automated deployment (working)")
    print("\n⌨️  Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()
