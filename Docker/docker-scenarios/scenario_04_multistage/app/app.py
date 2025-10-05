from flask import Flask, render_template_string, request, jsonify
import subprocess
import json
import os
import time
import logging
import docker
from datetime import datetime

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

def get_image_info(image_name):
    """Get detailed information about a Docker image"""
    try:
        if not docker_available:
            # Return fallback data for demo
            if image_name == "bloated-app":
                return {
                    'name': image_name,
                    'size': 4537598976,  # 4.2GB in bytes
                    'size_str': '4.24GB',
                    'size_mb': 4324,
                    'layers': 30,
                    'created': '2024-01-01 12:00:00',
                    'history': [
                        {'CreatedBy': 'RUN apt-get update && apt-get install', 'Size': 524288000},
                        {'CreatedBy': 'RUN pip install flask django fastapi', 'Size': 314572800},
                        {'CreatedBy': 'RUN npm install -g create-react-app', 'Size': 209715200},
                        {'CreatedBy': 'COPY . /app', 'Size': 1048576},
                        {'CreatedBy': 'RUN mkdir -p /app/logs', 'Size': 4096}
                    ]
                }
            elif image_name == "optimized-app":
                return {
                    'name': image_name,
                    'size': 279969792,  # 267MB in bytes
                    'size_str': '267MB',
                    'size_mb': 267,
                    'layers': 8,
                    'created': '2024-01-01 12:30:00',
                    'history': [
                        {'CreatedBy': 'COPY --from=builder /opt/venv', 'Size': 104857600},
                        {'CreatedBy': 'RUN groupadd -r appuser', 'Size': 4096},
                        {'CreatedBy': 'COPY optimized_app.py ./app.py', 'Size': 8192},
                        {'CreatedBy': 'USER appuser', 'Size': 0},
                        {'CreatedBy': 'WORKDIR /app', 'Size': 0}
                    ]
                }
            return None
        
        image = docker_client.images.get(image_name)
        history = docker_client.api.history(image_name)
        
        # Calculate total size and layer count
        total_size = image.attrs.get('Size', 0)
        layer_count = len(history)
        
        # Get created date
        created = image.attrs.get('Created', '')
        if created:
            created = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get size in human readable format
        size_mb = total_size / (1024 * 1024)
        if size_mb > 1024:
            size_str = f"{size_mb / 1024:.1f}GB"
        else:
            size_str = f"{size_mb:.0f}MB"
        
        return {
            'name': image_name,
            'size': total_size,
            'size_str': size_str,
            'size_mb': size_mb,
            'layers': layer_count,
            'created': created,
            'history': history[:10]  # Top 10 layers
        }
    except Exception as e:
        logger.error(f"Error getting image info for {image_name}: {e}")
        return None

def get_container_stats():
    """Get statistics about running containers with resource usage"""
    try:
        if not docker_available:
            return {}
        
        containers = docker_client.containers.list(all=True)
        stats = {}
        
        for container in containers:
            if any(name in container.name for name in ['bloated-app', 'optimized-app', 'comparison']):
                try:
                    # Get real-time stats if container is running
                    live_stats = None
                    if container.status == 'running':
                        stats_stream = container.stats(stream=False)
                        cpu_usage = stats_stream.get('cpu_stats', {}).get('cpu_usage', {}).get('total_usage', 0)
                        memory_usage = stats_stream.get('memory_stats', {}).get('usage', 0)
                        memory_limit = stats_stream.get('memory_stats', {}).get('limit', 0)
                        
                        live_stats = {
                            'cpu_usage': cpu_usage,
                            'memory_usage': memory_usage / (1024 * 1024) if memory_usage else 0,  # MB
                            'memory_limit': memory_limit / (1024 * 1024) if memory_limit else 0   # MB
                        }
                    
                    stats[container.name] = {
                        'name': container.name,
                        'status': container.status,
                        'image': container.image.tags[0] if container.image.tags else 'unknown',
                        'ports': container.attrs.get('NetworkSettings', {}).get('Ports', {}),
                        'created': container.attrs.get('Created', ''),
                        'started': container.attrs.get('State', {}).get('StartedAt', ''),
                        'live_stats': live_stats
                    }
                except Exception as container_error:
                    logger.warning(f"Error getting stats for {container.name}: {container_error}")
        
        return stats
    except Exception as e:
        logger.error(f"Error getting container stats: {e}")
        return {}

def get_build_progress():
    """Get current Docker build progress if any builds are happening"""
    try:
        if not docker_available:
            return None
        
        # Check for recent builds by looking at images with very recent timestamps
        images = docker_client.images.list()
        recent_builds = []
        
        current_time = datetime.now()
        for image in images:
            if image.tags:
                created = image.attrs.get('Created', '')
                if created:
                    try:
                        image_time = datetime.fromisoformat(created.replace('Z', '+00:00').replace('+00:00', ''))
                        age_minutes = (current_time - image_time).total_seconds() / 60
                        
                        if age_minutes < 5:  # Built in last 5 minutes
                            recent_builds.append({
                                'tag': image.tags[0],
                                'age_minutes': age_minutes,
                                'size': image.attrs.get('Size', 0)
                            })
                    except Exception:
                        pass
        
        return recent_builds if recent_builds else None
    except Exception as e:
        logger.error(f"Error getting build progress: {e}")
        return None

def get_system_info():
    """Get Docker system information for enhanced insights"""
    try:
        if not docker_available:
            return {
                'total_images': 'N/A',
                'total_containers': 'N/A',
                'disk_usage': 'N/A'
            }
        
        system_info = docker_client.info()
        
        # Get disk usage
        try:
            df_result = docker_client.df()
            total_size = 0
            if 'Images' in df_result:
                total_size += sum(img.get('Size', 0) for img in df_result['Images'])
            if 'Containers' in df_result:
                total_size += sum(container.get('SizeRw', 0) for container in df_result['Containers'])
                
            disk_usage_gb = total_size / (1024 * 1024 * 1024) if total_size else 0
        except Exception:
            disk_usage_gb = 0
        
        return {
            'total_images': system_info.get('Images', 0),
            'total_containers': system_info.get('Containers', 0),
            'running_containers': system_info.get('ContainersRunning', 0),
            'disk_usage_gb': round(disk_usage_gb, 2),
            'docker_version': system_info.get('ServerVersion', 'Unknown')
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {'total_images': 'Error', 'total_containers': 'Error', 'disk_usage': 'Error'}

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🏗️ Docker Multi-Stage Build Comparison</title>
    <meta http-equiv="refresh" content="10">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
        }
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        .comparison-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.2);
            position: relative;
            overflow: hidden;
        }
        .comparison-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
        }
        .bloated::before {
            background: linear-gradient(90deg, #ff6b6b, #ee5a52);
        }
        .optimized::before {
            background: linear-gradient(90deg, #4ecdc4, #44a08d);
        }
        .card-title {
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .bloated .card-title {
            color: #ee5a52;
        }
        .optimized .card-title {
            color: #44a08d;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric {
            text-align: center;
            background: rgba(0,0,0,0.03);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.05);
        }
        .metric-value {
            font-size: 2.2em;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .metric-label {
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        .status-running {
            background: #d4edda;
            color: #155724;
        }
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        .status-unknown {
            background: #fff3cd;
            color: #856404;
        }
        .layer-preview {
            background: rgba(0,0,0,0.03);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
        }
        .layer-preview h4 {
            margin-bottom: 10px;
            color: #666;
        }
        .layer-item {
            padding: 4px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
        }
        .layer-item:last-child {
            border-bottom: none;
        }
        .summary-section {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.2);
            max-width: 1400px;
            margin: 0 auto;
        }
        .summary-title {
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .benefit {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .benefit-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .benefit-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .benefit-desc {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .live-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8em;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: pulse 2s infinite;
        }
        .system-info {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 0.75em;
            font-family: 'Courier New', monospace;
        }
        .container-status {
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9em;
        }
        .memory-bar {
            background: rgba(255,255,255,0.3);
            height: 4px;
            border-radius: 2px;
            margin: 5px 0;
            overflow: hidden;
        }
        .memory-fill {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            height: 100%;
            transition: width 0.5s ease;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
        }
        .quick-links {
            text-align: center;
            margin-top: 30px;
        }
        .quick-links a {
            display: inline-block;
            margin: 0 15px;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .quick-links a:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="live-indicator">
        <div class="pulse-dot"></div>
        Live Dashboard - Updates every 10s
    </div>
    
    {% if system_info %}
    <div class="system-info">
        <div><strong>🐳 Docker System</strong></div>
        <div>Version: {{ system_info.docker_version }}</div>
        <div>Images: {{ system_info.total_images }}</div>
        <div>Containers: {{ system_info.running_containers }}/{{ system_info.total_containers }}</div>
        <div>Disk Usage: {{ system_info.disk_usage_gb }}GB</div>
    </div>
    {% endif %}
    
    <div class="header">
        <h1>🏗️ Docker Multi-Stage Build Comparison</h1>
        <div class="subtitle">Real-time comparison of bloated vs optimized containers</div>
    </div>
    
    <div class="dashboard">
        <!-- Bloated Image Card -->
        <div class="comparison-card bloated">
            <div class="card-title">
                <span>🔴</span>
                <span>Bloated Image</span>
                {% if bloated_info %}
                <span class="status-indicator status-running">● RUNNING</span>
                {% else %}
                <span class="status-indicator status-unknown">● UNKNOWN</span>
                {% endif %}
            </div>
            
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-value">{{ bloated_info.size_str if bloated_info else 'N/A' }}</div>
                    <div class="metric-label">Size</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ bloated_info.layers if bloated_info else 'N/A' }}</div>
                    <div class="metric-label">Layers</div>
                </div>
                <div class="metric">
                    <div class="metric-value">❌</div>
                    <div class="metric-label">Security</div>
                </div>
                <div class="metric">
                    <div class="metric-value">SLOW</div>
                    <div class="metric-label">Performance</div>
                </div>
            </div>
            
            {% if container_stats and 'bloated-app-demo' in container_stats %}
            {% set container = container_stats['bloated-app-demo'] %}
            <div class="container-status">
                <h4>📊 Live Container Stats:</h4>
                <div>Status: {{ container.status|title }}</div>
                {% if container.live_stats %}
                <div>Memory: {{ '%.1f'|format(container.live_stats.memory_usage) }}MB</div>
                <div class="memory-bar">
                    <div class="memory-fill" style="width: {{ (container.live_stats.memory_usage / container.live_stats.memory_limit * 100) if container.live_stats.memory_limit else 0 }}%"></div>
                </div>
                {% endif %}
            </div>
            {% endif %}
            
            {% if bloated_info and bloated_info.history %}
            <div class="layer-preview">
                <h4>Top Layers (Size Impact):</h4>
                {% for layer in bloated_info.history[:5] %}
                <div class="layer-item">
                    <span>{{ layer.get('CreatedBy', 'Unknown')[:50] }}...</span>
                    <span>{{ '%.1f'|format(layer.get('Size', 0) / 1048576) }}MB</span>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <!-- Optimized Image Card -->
        <div class="comparison-card optimized">
            <div class="card-title">
                <span>🟢</span>
                <span>Optimized Multi-Stage</span>
                {% if optimized_info %}
                <span class="status-indicator status-running">● RUNNING</span>
                {% else %}
                <span class="status-indicator status-unknown">● UNKNOWN</span>
                {% endif %}
            </div>
            
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-value">{{ optimized_info.size_str if optimized_info else 'N/A' }}</div>
                    <div class="metric-label">Size</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ optimized_info.layers if optimized_info else 'N/A' }}</div>
                    <div class="metric-label">Layers</div>
                </div>
                <div class="metric">
                    <div class="metric-value">✅</div>
                    <div class="metric-label">Security</div>
                </div>
                <div class="metric">
                    <div class="metric-value">FAST</div>
                    <div class="metric-label">Performance</div>
                </div>
            </div>
            
            {% if container_stats and 'optimized-app-demo' in container_stats %}
            {% set container = container_stats['optimized-app-demo'] %}
            <div class="container-status">
                <h4>📊 Live Container Stats:</h4>
                <div>Status: {{ container.status|title }}</div>
                {% if container.live_stats %}
                <div>Memory: {{ '%.1f'|format(container.live_stats.memory_usage) }}MB</div>
                <div class="memory-bar">
                    <div class="memory-fill" style="width: {{ (container.live_stats.memory_usage / container.live_stats.memory_limit * 100) if container.live_stats.memory_limit else 0 }}%"></div>
                </div>
                {% endif %}
            </div>
            {% endif %}
            
            {% if optimized_info and optimized_info.history %}
            <div class="layer-preview">
                <h4>Top Layers (Multi-Stage):</h4>
                {% for layer in optimized_info.history[:5] %}
                <div class="layer-item">
                    <span>{{ layer.get('CreatedBy', 'Unknown')[:50] }}...</span>
                    <span>{{ '%.1f'|format(layer.get('Size', 0) / 1048576) }}MB</span>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <div class="summary-section">
        <h2 class="summary-title">📈 Optimization Benefits</h2>
        
        {% if bloated_info and optimized_info %}
        <div style="text-align: center; margin-bottom: 30px; font-size: 1.5em;">
            <strong style="color: #4ecdc4;">Size Reduction: {{ '%.1f'|format((1 - optimized_info.size_mb / bloated_info.size_mb) * 100) }}%</strong>
            <br>
            <span style="color: #666; font-size: 0.8em;">From {{ bloated_info.size_str }} to {{ optimized_info.size_str }}</span>
        </div>
        {% endif %}
        
        <div class="benefits-grid">
            <div class="benefit">
                <div class="benefit-icon">📦</div>
                <div class="benefit-title">Smaller Images</div>
                <div class="benefit-desc">Up to 94% size reduction using multi-stage builds</div>
            </div>
            <div class="benefit">
                <div class="benefit-icon">🚀</div>
                <div class="benefit-title">Faster Deploys</div>
                <div class="benefit-desc">Reduced image size means faster push/pull operations</div>
            </div>
            <div class="benefit">
                <div class="benefit-icon">🔒</div>
                <div class="benefit-title">Better Security</div>
                <div class="benefit-desc">Fewer packages means smaller attack surface</div>
            </div>
            <div class="benefit">
                <div class="benefit-icon">💰</div>
                <div class="benefit-title">Cost Savings</div>
                <div class="benefit-desc">Lower storage and bandwidth costs</div>
            </div>
        </div>
        
        <div class="quick-links">
            <a href="http://localhost:8001" target="_blank">🔴 View Bloated App</a>
            <a href="http://localhost:8002" target="_blank">🟢 View Optimized App</a>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Interactive multi-stage build comparison dashboard with enhanced real-time features"""
    # Get live data about both images
    bloated_info = get_image_info("bloated-app")
    optimized_info = get_image_info("optimized-app")
    
    # Get enhanced container statistics with resource usage
    container_stats = get_container_stats()
    
    # Get build progress information
    build_progress = get_build_progress()
    
    # Get system information
    system_info = get_system_info()
    
    logger.info(f"Dashboard loaded - Bloated: {'✅' if bloated_info else '❌'}, Optimized: {'✅' if optimized_info else '❌'}, Containers: {len(container_stats)}, Recent builds: {len(build_progress) if build_progress else 0}")
    
    return render_template_string(TEMPLATE, 
                                bloated_info=bloated_info,
                                optimized_info=optimized_info,
                                container_stats=container_stats,
                                build_progress=build_progress,
                                system_info=system_info)

@app.route("/api/stats")
def api_stats():
    """Enhanced API endpoint for real-time statistics and insights"""
    bloated_info = get_image_info("bloated-app")
    optimized_info = get_image_info("optimized-app")
    container_stats = get_container_stats()
    build_progress = get_build_progress()
    system_info = get_system_info()
    
    # Calculate additional insights
    insights = {}
    if bloated_info and optimized_info:
        size_reduction = (1 - optimized_info['size_mb'] / bloated_info['size_mb']) * 100
        layer_reduction = (1 - optimized_info['layers'] / bloated_info['layers']) * 100 if bloated_info['layers'] > 0 else 0
        
        insights = {
            'size_reduction_percent': round(size_reduction, 1),
            'layer_reduction_percent': round(layer_reduction, 1),
            'size_saved_mb': round(bloated_info['size_mb'] - optimized_info['size_mb'], 1),
            'deployment_time_improvement': '3x faster' if size_reduction > 80 else '2x faster',
            'security_improvement': 'Significant' if size_reduction > 90 else 'Moderate'
        }
    
    return jsonify({
        "bloated_info": bloated_info,
        "optimized_info": optimized_info,
        "container_stats": container_stats,
        "build_progress": build_progress,
        "system_info": system_info,
        "insights": insights,
        "timestamp": time.time(),
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route("/health")
def health():
    """Health check endpoint for Docker health check"""
    return jsonify({"status": "healthy", "timestamp": time.time()}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
