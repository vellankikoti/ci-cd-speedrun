#!/usr/bin/env python3
"""
Docker Build Pipeline Demo Application
A simple Flask web application for demonstrating Docker build pipelines
"""

import os
import json
import time
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Application metadata
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
BUILD_TIME = os.getenv('BUILD_TIME', datetime.now().isoformat())
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Build Pipeline Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .info-card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 10px;
        }
        .status.healthy {
            background: #4CAF50;
            color: white;
        }
        .endpoint {
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            margin: 5px 0;
        }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        .btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Docker Build Pipeline Demo</h1>
        
        <div class="info-card">
            <h3>Application Status <span class="status healthy">HEALTHY</span></h3>
            <p>This application demonstrates a complete Docker build pipeline with:</p>
            <ul>
                <li>✅ Flask web application</li>
                <li>✅ Health checks and monitoring</li>
                <li>✅ API endpoints for testing</li>
                <li>✅ Docker containerization</li>
                <li>✅ Automated testing</li>
            </ul>
        </div>

        <div class="info-card">
            <h3>Build Information</h3>
            <p><strong>Version:</strong> {{ version }}</p>
            <p><strong>Build Time:</strong> {{ build_time }}</p>
            <p><strong>Environment:</strong> {{ environment }}</p>
            <p><strong>Container ID:</strong> {{ container_id }}</p>
        </div>

        <div class="info-card">
            <h3>Available Endpoints</h3>
            <div class="endpoint">GET /health - Health check endpoint</div>
            <div class="endpoint">GET /api/info - Application information</div>
            <div class="endpoint">GET /api/status - Detailed status</div>
            <div class="endpoint">POST /api/echo - Echo test endpoint</div>
        </div>

        <div class="info-card">
            <h3>Test the Application</h3>
            <a href="/health" class="btn">Health Check</a>
            <a href="/api/info" class="btn">API Info</a>
            <a href="/api/status" class="btn">Status</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with application information"""
    container_id = os.getenv('HOSTNAME', 'unknown')
    return render_template_string(HTML_TEMPLATE, 
                                version=APP_VERSION,
                                build_time=BUILD_TIME,
                                environment=ENVIRONMENT,
                                container_id=container_id)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': APP_VERSION,
        'environment': ENVIRONMENT
    }), 200

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'Docker Build Pipeline Demo',
        'version': APP_VERSION,
        'description': 'A Flask application demonstrating Docker build pipelines',
        'build_time': BUILD_TIME,
        'environment': ENVIRONMENT,
        'endpoints': [
            '/health',
            '/api/info',
            '/api/status',
            '/api/echo'
        ]
    })

@app.route('/api/status')
def api_status():
    """Detailed status endpoint"""
    return jsonify({
        'application': {
            'name': 'Docker Build Pipeline Demo',
            'version': APP_VERSION,
            'status': 'running',
            'uptime': time.time() - app.start_time if hasattr(app, 'start_time') else 0
        },
        'system': {
            'environment': ENVIRONMENT,
            'build_time': BUILD_TIME,
            'container_id': os.getenv('HOSTNAME', 'unknown'),
            'python_version': os.sys.version
        },
        'health': {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'database': 'not_configured',
                'external_apis': 'not_configured',
                'memory': 'ok',
                'disk': 'ok'
            }
        }
    })

@app.route('/api/echo', methods=['POST'])
def api_echo():
    """Echo test endpoint"""
    data = request.get_json() or {}
    return jsonify({
        'echo': data,
        'timestamp': datetime.now().isoformat(),
        'received_at': time.time()
    })

@app.route('/api/load-test')
def load_test():
    """Simple load test endpoint"""
    start_time = time.time()
    
    # Simulate some work
    result = 0
    for i in range(1000):
        result += i ** 2
    
    end_time = time.time()
    
    return jsonify({
        'result': result,
        'execution_time': end_time - start_time,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.start_time = time.time()
    port = int(os.getenv('PORT', 5000))
    debug = ENVIRONMENT == 'development'
    
    print(f"🚀 Starting Docker Build Pipeline Demo")
    print(f"📦 Version: {APP_VERSION}")
    print(f"🌍 Environment: {ENVIRONMENT}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌐 Server running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
