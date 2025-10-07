#!/usr/bin/env python3
"""
Docker Ninja - Advanced Flask Application
A Flask app demonstrating advanced Docker techniques and container orchestration.
"""

from flask import Flask, request, jsonify, render_template_string
import os
import sys
import time
import psutil
import signal
from datetime import datetime
import threading

app = Flask(__name__)

# Global variables for metrics
start_time = time.time()
request_count = 0
shutdown_requested = False

@app.route('/')
def home():
    """Welcome page with Docker ninja features."""
    return render_template_string("""
    <html>
        <head>
            <title>Docker Ninja - Advanced Container Orchestration</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; margin: 5px; display: inline-block; }
                .success { color: #27ae60; font-weight: bold; }
                .warning { color: #f39c12; font-weight: bold; }
                .feature { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 10px 0; }
                .metrics { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
                button { background: #e74c3c; color: white; padding: 8px 15px; border: none; border-radius: 3px; cursor: pointer; }
                button:hover { background: #c0392b; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐳 Docker Ninja - Advanced Container Orchestration</h1>
                
                <div class="info">
                    <h3>Container Status:</h3>
                    <p id="container-status">Checking container status...</p>
                </div>
                
                <div class="metrics">
                    <h3>Live Metrics:</h3>
                    <p id="metrics">Loading metrics...</p>
                </div>
                
                <div class="info">
                    <h3>Available Endpoints:</h3>
                    <span class="endpoint">GET /</span> - This dashboard
                    <span class="endpoint">GET /health</span> - Health check
                    <span class="endpoint">GET /metrics</span> - Performance metrics
                    <span class="endpoint">GET /info</span> - System information
                    <span class="endpoint">POST /shutdown</span> - Graceful shutdown
                </div>
                
                <div class="feature">
                    <h3>🐳 Docker Ninja Features:</h3>
                    <ul>
                        <li>✅ Multi-stage Docker builds</li>
                        <li>✅ Security scanning and hardening</li>
                        <li>✅ Blue-green deployment strategy</li>
                        <li>✅ Container orchestration with Docker Compose</li>
                        <li>✅ Non-root user security</li>
                        <li>✅ Health checks and monitoring</li>
                    </ul>
                </div>
                
                <div class="feature">
                    <h3>🚀 Advanced Techniques:</h3>
                    <ul>
                        <li>✅ Image optimization (90% size reduction)</li>
                        <li>✅ Vulnerability scanning</li>
                        <li>✅ Zero-downtime deployments</li>
                        <li>✅ Container resource monitoring</li>
                        <li>✅ Graceful shutdown handling</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <button onclick="shutdown()">🛑 Test Graceful Shutdown</button>
                </div>
            </div>
            
            <script>
                // Update container status
                fetch('/health')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('container-status').innerHTML = 
                            data.status === 'healthy' ? 
                            '<span class="success">✅ Container Healthy</span>' : 
                            '<span class="warning">⚠️ Container Issues</span>';
                    });
                
                // Update metrics
                function updateMetrics() {
                    fetch('/metrics')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('metrics').innerHTML = 
                                `Uptime: ${data.uptime}s | Requests: ${data.request_count} | CPU: ${data.cpu_percent}% | Memory: ${data.memory_percent}%`;
                        });
                }
                
                // Update metrics every 5 seconds
                updateMetrics();
                setInterval(updateMetrics, 5000);
                
                // Shutdown function
                function shutdown() {
                    if (confirm('Are you sure you want to test graceful shutdown?')) {
                        fetch('/shutdown', { method: 'POST' })
                            .then(() => {
                                alert('Graceful shutdown initiated! The container will stop in 5 seconds.');
                            });
                    }
                }
            </script>
        </body>
    </html>
    """)

@app.route('/health')
def health():
    """Health check endpoint with container status."""
    global request_count
    request_count += 1
    
    try:
        # Check system health
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Determine health status
        health_status = "healthy"
        if cpu_percent > 80 or memory_percent > 80 or disk_percent > 90:
            health_status = "degraded"
        
        return jsonify({
            'status': health_status,
            'timestamp': datetime.now().isoformat(),
            'container_id': os.environ.get('HOSTNAME', 'unknown'),
            'uptime': int(time.time() - start_time),
            'request_count': request_count,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'message': 'Docker Ninja container is running with advanced features!'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/metrics')
def metrics():
    """Performance metrics endpoint."""
    global request_count
    request_count += 1
    
    try:
        uptime = int(time.time() - start_time)
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'uptime': uptime,
            'request_count': request_count,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_mb': memory.used // (1024 * 1024),
            'memory_total_mb': memory.total // (1024 * 1024),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used // (1024 * 1024 * 1024),
            'disk_total_gb': disk.total // (1024 * 1024 * 1024),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/info')
def info():
    """System information endpoint."""
    global request_count
    request_count += 1
    
    try:
        return jsonify({
            'app_name': 'Docker Ninja',
            'version': '1.0.0',
            'python_version': sys.version,
            'platform': sys.platform,
            'container_id': os.environ.get('HOSTNAME', 'unknown'),
            'working_directory': os.getcwd(),
            'environment': os.environ.get('ENVIRONMENT', 'production'),
            'user': os.environ.get('USER', 'unknown'),
            'pid': os.getpid(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Graceful shutdown endpoint for testing."""
    global shutdown_requested
    
    if shutdown_requested:
        return jsonify({'message': 'Shutdown already in progress'}), 400
    
    shutdown_requested = True
    
    def delayed_shutdown():
        time.sleep(5)  # Give time for response
        os.kill(os.getpid(), signal.SIGTERM)
    
    # Start shutdown in background
    threading.Thread(target=delayed_shutdown, daemon=True).start()
    
    return jsonify({
        'message': 'Graceful shutdown initiated',
        'shutdown_in': '5 seconds',
        'timestamp': datetime.now().isoformat()
    })

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

if __name__ == '__main__':
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('ENVIRONMENT', 'production') == 'development'
    
    print(f"🐳 Starting Docker Ninja app on port {port}")
    print(f"📱 Visit: http://localhost:{port}")
    print(f"❤️  Health: http://localhost:{port}/health")
    print(f"📊 Metrics: http://localhost:{port}/metrics")
    print(f"ℹ️  Info: http://localhost:{port}/info")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
