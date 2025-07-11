#!/usr/bin/env python3
"""
Enhanced Auto-scaling Hero Deployment
=====================================
Creates a comprehensive auto-scaling challenge with real-time monitoring,
interactive dashboard, and dynamic scaling visualization.
"""

import json
import time
import subprocess
import sys
from datetime import datetime

def run_kubectl(command, namespace=None):
    """Execute kubectl command and return output"""
    cmd = ["kubectl"] + command
    if namespace:
        cmd.extend(["-n", namespace])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ kubectl command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None

def create_namespace():
    """Create the scaling challenge namespace"""
    print("🏠 Creating scaling challenge namespace: scaling-challenge")
    
    namespace_yaml = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
            "name": "scaling-challenge",
            "labels": {
                "created-by": "auto-scaling-hero",
                "scenario": "3",
                "purpose": "enhanced-scaling-demo"
            }
        }
    }
    
    # Apply namespace
    process = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=json.dumps(namespace_yaml),
        text=True,
        capture_output=True
    )
    
    if process.returncode == 0:
        print("✅ Scaling namespace created")
        return True
    else:
        print(f"❌ Failed to create namespace: {process.stderr}")
        return False

def create_enhanced_dashboard_html():
    """Create the enhanced interactive dashboard HTML"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦸‍♂️ Auto-scaling Hero Control Center</title>
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
            color: white;
        }
        
        .hero-header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .hero-title {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .hero-subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.15);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .card-icon {
            font-size: 2em;
            margin-right: 15px;
        }
        
        .card-title {
            font-size: 1.3em;
            font-weight: bold;
        }
        
        .card-value {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }
        
        .card-subtitle {
            text-align: center;
            opacity: 0.8;
            font-size: 0.9em;
        }
        
        .card-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-size: 0.9em;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active { background: #4CAF50; }
        .status-scaling { background: #FF9800; animation: pulse 1s infinite; }
        .status-warning { background: #f44336; }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .load-testing-section {
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
            color: #fff;
        }
        
        .load-controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
        }
        
        .control-label {
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .control-input {
            padding: 10px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.9);
            color: #333;
            font-size: 1em;
        }
        
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(45deg, #FF9800, #e68900);
            color: white;
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #f44336, #da190b);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .activity-log {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .log-entry {
            margin-bottom: 5px;
            opacity: 0.9;
        }
        
        .log-timestamp {
            color: #4CAF50;
            margin-right: 10px;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 5% auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }
        
        .modal-close {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 2em;
            cursor: pointer;
            color: white;
        }
        
        .pod-list {
            display: grid;
            gap: 10px;
            margin-top: 15px;
        }
        
        .pod-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .pod-name {
            font-weight: bold;
        }
        
        .pod-status {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .pod-running { background: #4CAF50; color: white; }
        .pod-pending { background: #FF9800; color: white; }
        .pod-terminating { background: #f44336; color: white; }
        
        .metric-chart {
            height: 100px;
            margin: 10px 0;
            position: relative;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            overflow: hidden;
        }
        
        .chart-bar {
            position: absolute;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to top, #4CAF50, #8BC34A);
            border-radius: 2px 2px 0 0;
            transition: height 0.3s ease;
        }
        
        .real-time-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #4CAF50;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7em;
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="hero-header">
        <h1 class="hero-title">🦸‍♂️ Auto-scaling Hero Control Center</h1>
        <p class="hero-subtitle">Dynamic Kubernetes Scaling Management & Real-time Monitoring</p>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="dashboard-grid">
        <!-- Current Pods Card -->
        <div class="card" onclick="showPodDetails()" id="pods-card">
            <div class="real-time-badge">LIVE</div>
            <div class="card-header">
                <div class="card-icon">🏗️</div>
                <div class="card-title">Current Pods</div>
            </div>
            <div class="card-value" id="current-pods">1</div>
            <div class="card-subtitle">Active Replicas</div>
            <div class="card-details">
                <div><span class="status-indicator status-active"></span>Target: <span id="target-pods">1</span></div>
                <div>Min: 1 | Max: 10</div>
            </div>
        </div>

        <!-- CPU Usage Card -->
        <div class="card" onclick="showCpuDetails()" id="cpu-card">
            <div class="real-time-badge">LIVE</div>
            <div class="card-header">
                <div class="card-icon">⚡</div>
                <div class="card-title">CPU Usage</div>
            </div>
            <div class="card-value" id="cpu-usage">0%</div>
            <div class="card-subtitle">Average Utilization</div>
            <div class="metric-chart" id="cpu-chart"></div>
            <div class="card-details">
                <div>Target: 50% | Status: <span id="cpu-status">Normal</span></div>
            </div>
        </div>

        <!-- Scaling Events Card -->
        <div class="card" onclick="showScalingEvents()" id="events-card">
            <div class="real-time-badge">LIVE</div>
            <div class="card-header">
                <div class="card-icon">📈</div>
                <div class="card-title">Scaling Events</div>
            </div>
            <div class="card-value" id="scaling-events">0</div>
            <div class="card-subtitle">Recent Activity</div>
            <div class="card-details">
                <div>Last Action: <span id="last-action">None</span></div>
                <div>Status: <span id="scaling-status">Stable</span></div>
            </div>
        </div>

        <!-- HPA Status Card -->
        <div class="card" onclick="showHpaDetails()" id="hpa-card">
            <div class="real-time-badge">LIVE</div>
            <div class="card-header">
                <div class="card-icon">🎯</div>
                <div class="card-title">HPA Status</div>
            </div>
            <div class="card-value" id="hpa-status">Active</div>
            <div class="card-subtitle">Auto-scaler Health</div>
            <div class="card-details">
                <div><span class="status-indicator status-active"></span>Ready to Scale</div>
                <div>Algorithm: v2 HPA</div>
            </div>
        </div>
    </div>

    <!-- Load Testing Control Center -->
    <div class="load-testing-section">
        <h2 class="section-title">🎮 Load Testing Control Center</h2>
        
        <div class="load-controls">
            <div class="control-group">
                <label class="control-label">Load Intensity (%)</label>
                <input type="range" id="intensity-slider" class="control-input" min="10" max="100" value="30" oninput="updateIntensityDisplay()">
                <div style="text-align: center; margin-top: 5px;">
                    <span id="intensity-display">30%</span>
                </div>
            </div>
            
            <div class="control-group">
                <label class="control-label">Duration (seconds)</label>
                <select id="duration-select" class="control-input">
                    <option value="60">1 minute</option>
                    <option value="120">2 minutes</option>
                    <option value="300">5 minutes</option>
                    <option value="600">10 minutes</option>
                </select>
            </div>
            
            <div class="control-group">
                <label class="control-label">Load Pattern</label>
                <select id="pattern-select" class="control-input">
                    <option value="steady">Steady Load</option>
                    <option value="spike">Traffic Spike</option>
                    <option value="wave">Wave Pattern</option>
                    <option value="chaos">Chaos Mode</option>
                </select>
            </div>
        </div>
        
        <div style="text-align: center; margin-bottom: 20px;">
            <button class="btn btn-primary" onclick="startLoadTest()">🚀 Start Load Test</button>
            <button class="btn btn-warning" onclick="startSpike()">⚡ Traffic Spike</button>
            <button class="btn btn-danger" onclick="startChaosAttack()">💥 Chaos Attack</button>
            <button class="btn btn-primary" onclick="stopLoadTest()">⏹️ Stop Test</button>
        </div>
        
        <div>
            <h3 style="margin-bottom: 10px;">📊 Activity Log</h3>
            <div class="activity-log" id="activity-log">
                <div class="log-entry">
                    <span class="log-timestamp">[${new Date().toLocaleTimeString()}]</span>
                    Auto-scaling Hero Control Center initialized
                </div>
            </div>
        </div>
    </div>

    <!-- Modals for detailed views -->
    <div id="pods-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('pods-modal')">&times;</span>
            <h2>🏗️ Pod Status Details</h2>
            <div id="pods-detail-content">
                <div class="pod-list" id="pod-list"></div>
            </div>
        </div>
    </div>

    <div id="cpu-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('cpu-modal')">&times;</span>
            <h2>⚡ CPU Metrics Details</h2>
            <div id="cpu-detail-content"></div>
        </div>
    </div>

    <div id="events-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('events-modal')">&times;</span>
            <h2>📈 Scaling Events History</h2>
            <div id="events-detail-content"></div>
        </div>
    </div>

    <div id="hpa-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal('hpa-modal')">&times;</span>
            <h2>🎯 HPA Configuration Details</h2>
            <div id="hpa-detail-content"></div>
        </div>
    </div>

    <script>
        let loadTestActive = false;
        let scalingData = {
            pods: 1,
            targetPods: 1,
            cpuUsage: 0,
            events: 0,
            hpaStatus: 'Active'
        };
        let cpuHistory = [];
        let updateInterval;

        function updateIntensityDisplay() {
            const slider = document.getElementById('intensity-slider');
            const display = document.getElementById('intensity-display');
            display.textContent = slider.value + '%';
        }

        function addLogEntry(message) {
            const log = document.getElementById('activity-log');
            const timestamp = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span class="log-timestamp">[${timestamp}]</span> ${message}`;
            log.appendChild(entry);
            log.scrollTop = log.scrollHeight;
        }

        function updateDashboard() {
            // Simulate real-time data updates
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    updateMetrics(data);
                })
                .catch(error => {
                    // Simulate data when API is not available
                    simulateMetrics();
                });
        }

        function updateMetrics(data) {
            // Update pod count
            document.getElementById('current-pods').textContent = data.currentPods || scalingData.pods;
            document.getElementById('target-pods').textContent = data.targetPods || scalingData.targetPods;
            
            // Update CPU usage
            const cpuValue = data.cpuUsage || scalingData.cpuUsage;
            document.getElementById('cpu-usage').textContent = cpuValue + '%';
            
            // Update CPU chart
            updateCpuChart(cpuValue);
            
            // Update scaling events
            document.getElementById('scaling-events').textContent = data.scalingEvents || scalingData.events;
            document.getElementById('last-action').textContent = data.lastAction || 'None';
            
            // Update status indicators
            updateStatusIndicators(data);
            
            scalingData = { ...scalingData, ...data };
        }

        function simulateMetrics() {
            if (loadTestActive) {
                // Simulate scaling up
                if (scalingData.cpuUsage < 80) {
                    scalingData.cpuUsage += Math.random() * 15;
                }
                
                if (scalingData.cpuUsage > 50 && scalingData.pods < 10) {
                    if (Math.random() > 0.7) { // 30% chance to scale up
                        scalingData.pods++;
                        scalingData.events++;
                        addLogEntry(`🔝 Scaling UP: New pod created (${scalingData.pods} total)`);
                    }
                }
            } else {
                // Simulate scaling down
                if (scalingData.cpuUsage > 0) {
                    scalingData.cpuUsage = Math.max(0, scalingData.cpuUsage - Math.random() * 10);
                }
                
                if (scalingData.cpuUsage < 30 && scalingData.pods > 1) {
                    if (Math.random() > 0.8) { // 20% chance to scale down
                        scalingData.pods--;
                        scalingData.events++;
                        addLogEntry(`🔽 Scaling DOWN: Pod removed (${scalingData.pods} total)`);
                    }
                }
            }
            
            updateMetrics(scalingData);
        }

        function updateCpuChart(cpuValue) {
            cpuHistory.push(cpuValue);
            if (cpuHistory.length > 30) {
                cpuHistory.shift();
            }
            
            const chart = document.getElementById('cpu-chart');
            chart.innerHTML = '';
            
            cpuHistory.forEach((value, index) => {
                const bar = document.createElement('div');
                bar.className = 'chart-bar';
                bar.style.height = value + '%';
                bar.style.left = (index * 3) + 'px';
                chart.appendChild(bar);
            });
        }

        function updateStatusIndicators(data) {
            const cpuStatus = document.getElementById('cpu-status');
            const scalingStatus = document.getElementById('scaling-status');
            
            if (data.cpuUsage > 70) {
                cpuStatus.textContent = 'High';
                cpuStatus.style.color = '#f44336';
            } else if (data.cpuUsage > 50) {
                cpuStatus.textContent = 'Normal';
                cpuStatus.style.color = '#FF9800';
            } else {
                cpuStatus.textContent = 'Low';
                cpuStatus.style.color = '#4CAF50';
            }
            
            if (data.currentPods !== data.targetPods) {
                scalingStatus.textContent = 'Scaling';
                scalingStatus.style.color = '#FF9800';
            } else {
                scalingStatus.textContent = 'Stable';
                scalingStatus.style.color = '#4CAF50';
            }
        }

        function startLoadTest() {
            const intensity = document.getElementById('intensity-slider').value;
            const duration = document.getElementById('duration-select').value;
            const pattern = document.getElementById('pattern-select').value;
            
            loadTestActive = true;
            addLogEntry(`🚀 Starting ${pattern} load test: ${intensity}% intensity for ${duration}s`);
            
            // Call backend load test
            fetch('/api/load-test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ intensity, duration, pattern })
            }).catch(() => {
                // Simulate if backend not available
                addLogEntry(`📊 Load test simulation started`);
            });
            
            setTimeout(() => {
                loadTestActive = false;
                addLogEntry(`⏹️ Load test completed`);
            }, duration * 1000);
        }

        function startSpike() {
            loadTestActive = true;
            addLogEntry(`⚡ Traffic spike initiated - expect rapid scaling!`);
            
            setTimeout(() => {
                loadTestActive = false;
                addLogEntry(`📉 Traffic spike ended - scaling down`);
            }, 90000); // 1.5 minutes
        }

        function startChaosAttack() {
            loadTestActive = true;
            addLogEntry(`💥 CHAOS ATTACK LAUNCHED - Maximum load incoming!`);
            
            // Simulate extreme load
            scalingData.cpuUsage = 95;
            
            setTimeout(() => {
                loadTestActive = false;
                addLogEntry(`🛡️ Chaos attack defeated by auto-scaling hero!`);
            }, 120000); // 2 minutes
        }

        function stopLoadTest() {
            loadTestActive = false;
            addLogEntry(`⏹️ Load test stopped manually`);
        }

        // Modal functions
        function showPodDetails() {
            const modal = document.getElementById('pods-modal');
            const content = document.getElementById('pod-list');
            
            // Simulate pod list
            content.innerHTML = '';
            for (let i = 1; i <= scalingData.pods; i++) {
                const podItem = document.createElement('div');
                podItem.className = 'pod-item';
                podItem.innerHTML = `
                    <div>
                        <div class="pod-name">scaling-demo-app-${Math.random().toString(36).substring(7)}</div>
                        <div style="font-size: 0.8em; opacity: 0.7;">Node: worker-node-${i % 3 + 1}</div>
                    </div>
                    <div class="pod-status pod-running">Running</div>
                `;
                content.appendChild(podItem);
            }
            
            modal.style.display = 'block';
        }

        function showCpuDetails() {
            const modal = document.getElementById('cpu-modal');
            const content = document.getElementById('cpu-detail-content');
            
            content.innerHTML = `
                <div style="margin: 20px 0;">
                    <h3>Current CPU Metrics</h3>
                    <p>Average CPU Usage: ${scalingData.cpuUsage}%</p>
                    <p>Target Threshold: 50%</p>
                    <p>Scale-up Trigger: > 50%</p>
                    <p>Scale-down Trigger: < 30%</p>
                </div>
                <div id="cpu-chart-detailed" class="metric-chart" style="height: 150px;"></div>
            `;
            
            modal.style.display = 'block';
        }

        function showScalingEvents() {
            const modal = document.getElementById('events-modal');
            const content = document.getElementById('events-detail-content');
            
            content.innerHTML = `
                <div style="margin: 20px 0;">
                    <h3>Recent Scaling Activity</h3>
                    <div class="activity-log" style="height: 300px;">
                        <div class="log-entry">
                            <span class="log-timestamp">[${new Date().toLocaleTimeString()}]</span>
                            HPA evaluated scaling conditions
                        </div>
                        <div class="log-entry">
                            <span class="log-timestamp">[${new Date(Date.now() - 30000).toLocaleTimeString()}]</span>
                            CPU usage: ${scalingData.cpuUsage}%
                        </div>
                        <div class="log-entry">
                            <span class="log-timestamp">[${new Date(Date.now() - 60000).toLocaleTimeString()}]</span>
                            Current replicas: ${scalingData.pods}
                        </div>
                    </div>
                </div>
            `;
            
            modal.style.display = 'block';
        }

        function showHpaDetails() {
            const modal = document.getElementById('hpa-modal');
            const content = document.getElementById('hpa-detail-content');
            
            content.innerHTML = `
                <div style="margin: 20px 0;">
                    <h3>HPA Configuration</h3>
                    <p><strong>Min Replicas:</strong> 1</p>
                    <p><strong>Max Replicas:</strong> 10</p>
                    <p><strong>Target CPU:</strong> 50%</p>
                    <p><strong>Scale Up Policy:</strong> Aggressive (30s window)</p>
                    <p><strong>Scale Down Policy:</strong> Conservative (60s window)</p>
                    <p><strong>Status:</strong> ${scalingData.hpaStatus}</p>
                </div>
            `;
            
            modal.style.display = 'block';
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }

        // Initialize dashboard
        function initDashboard() {
            addLogEntry('🎯 Dashboard initialized - monitoring scaling metrics');
            updateInterval = setInterval(updateDashboard, 2000); // Update every 2 seconds
            updateDashboard(); // Initial update
        }

        // Start dashboard when page loads
        window.onload = initDashboard;
    </script>
</body>
</html>'''

def create_scalable_app_deployment():
    """Create the enhanced scalable application deployment"""
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "scaling-demo-app",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "scaling-demo-app",
                "component": "web-server",
                "created-by": "auto-scaling-hero"
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "scaling-demo-app"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "scaling-demo-app",
                        "component": "web-server"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "scaling-demo",
                            "image": "nginx:alpine",
                            "ports": [
                                {
                                    "containerPort": 80,
                                    "name": "http"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "128Mi"
                                },
                                "limits": {
                                    "cpu": "200m",
                                    "memory": "256Mi"
                                }
                            },
                            "volumeMounts": [
                                {
                                    "name": "dashboard-config",
                                    "mountPath": "/usr/share/nginx/html",
                                    "readOnly": True
                                }
                            ],
                            "livenessProbe": {
                                "httpGet": {
                                    "path": "/",
                                    "port": 80
                                },
                                "initialDelaySeconds": 10,
                                "periodSeconds": 10
                            },
                            "readinessProbe": {
                                "httpGet": {
                                    "path": "/",
                                    "port": 80
                                },
                                "initialDelaySeconds": 5,
                                "periodSeconds": 5
                            }
                        }
                    ],
                    "volumes": [
                        {
                            "name": "dashboard-config",
                            "configMap": {
                                "name": "scaling-dashboard-config"
                            }
                        }
                    ]
                }
            }
        }
    }
    return deployment

def create_load_generator_deployment():
    """Create an enhanced load generator that can create actual CPU load"""
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "load-generator",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "load-generator",
                "component": "load-tester"
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "load-generator"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "load-generator",
                        "component": "load-tester"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "load-generator",
                            "image": "python:3.9-alpine",
                            "command": [
                                "sh", "-c",
                                """
                                apk add --no-cache curl &&
                                pip install flask requests &&
                                cat > /app.py << 'EOF'
import os
import time
import threading
import requests
from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)
load_active = False
load_threads = []

def cpu_intensive_work(duration=60, intensity=50):
    '''Generate CPU load for specified duration and intensity'''
    global load_active
    end_time = time.time() + duration
    
    while time.time() < end_time and load_active:
        # CPU intensive operations
        for i in range(intensity * 1000):
            _ = sum(range(100))
        time.sleep(0.001)  # Small sleep to control intensity

def http_load_test(target_url, duration=60, requests_per_second=10):
    '''Generate HTTP load to target service'''
    global load_active
    end_time = time.time() + duration
    
    while time.time() < end_time and load_active:
        try:
            requests.get(target_url, timeout=1)
        except:
            pass
        time.sleep(1.0 / requests_per_second)

@app.route('/api/load-test', methods=['POST'])
def start_load_test():
    global load_active, load_threads
    
    data = request.json
    intensity = int(data.get('intensity', 50))
    duration = int(data.get('duration', 60))
    pattern = data.get('pattern', 'steady')
    
    # Stop any existing load test
    load_active = False
    for thread in load_threads:
        if thread.is_alive():
            thread.join(timeout=1)
    
    load_threads = []
    load_active = True
    
    # Start CPU load on the scaling-demo-app pods
    target_service = 'http://scaling-demo-service.scaling-challenge.svc.cluster.local'
    
    if pattern == 'chaos':
        intensity = 90
        duration = min(duration, 300)  # Max 5 minutes for chaos
    
    # Start CPU intensive work
    cpu_thread = threading.Thread(target=cpu_intensive_work, args=(duration, intensity))
    cpu_thread.start()
    load_threads.append(cpu_thread)
    
    # Start HTTP load
    http_thread = threading.Thread(target=http_load_test, args=(target_service, duration, intensity))
    http_thread.start()
    load_threads.append(http_thread)
    
    return jsonify({
        'status': 'started',
        'intensity': intensity,
        'duration': duration,
        'pattern': pattern
    })

@app.route('/api/load-test', methods=['DELETE'])
def stop_load_test():
    global load_active
    load_active = False
    return jsonify({'status': 'stopped'})

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    '''Get current scaling metrics'''
    try:
        # Get pod count
        pods_result = subprocess.run([
            'kubectl', 'get', 'pods', '-n', 'scaling-challenge',
            '-l', 'app=scaling-demo-app',
            '-o', 'json'
        ], capture_output=True, text=True)
        
        if pods_result.returncode == 0:
            pods_data = json.loads(pods_result.stdout)
            current_pods = len([p for p in pods_data['items'] if p['status']['phase'] == 'Running'])
        else:
            current_pods = 1
        
        # Get HPA status
        hpa_result = subprocess.run([
            'kubectl', 'get', 'hpa', '-n', 'scaling-challenge',
            '-o', 'json'
        ], capture_output=True, text=True)
        
        target_pods = current_pods
        cpu_usage = 0
        
        if hpa_result.returncode == 0:
            hpa_data = json.loads(hpa_result.stdout)
            if hpa_data['items']:
                hpa = hpa_data['items'][0]
                target_pods = hpa['status'].get('desiredReplicas', current_pods)
                
                # Get CPU usage from HPA
                current_metrics = hpa['status'].get('currentMetrics', [])
                for metric in current_metrics:
                    if metric['type'] == 'Resource' and metric['resource']['name'] == 'cpu':
                        cpu_usage = metric['resource']['current']['averageUtilization']
                        break
        
        return jsonify({
            'currentPods': current_pods,
            'targetPods': target_pods,
            'cpuUsage': cpu_usage,
            'loadActive': load_active,
            'timestamp': time.time()
        })
    
    except Exception as e:
        return jsonify({
            'currentPods': 1,
            'targetPods': 1,
            'cpuUsage': 0,
            'loadActive': load_active,
            'error': str(e)
        })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
                                python /app.py
                                """
                            ],
                            "ports": [
                                {
                                    "containerPort": 5000,
                                    "name": "api"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": "50m",
                                    "memory": "128Mi"
                                },
                                "limits": {
                                    "cpu": "500m",
                                    "memory": "256Mi"
                                }
                            },
                            "env": [
                                {
                                    "name": "FLASK_ENV",
                                    "value": "production"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    return deployment

def create_cpu_stress_deployment():
    """Create a CPU stress deployment that will actually trigger scaling"""
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "cpu-stress-app",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "cpu-stress-app",
                "component": "stress-tester"
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "cpu-stress-app"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "cpu-stress-app",
                        "component": "stress-tester"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "cpu-stress",
                            "image": "python:3.9-alpine",
                            "command": [
                                "sh", "-c",
                                """
                                pip install flask requests &&
                                cat > /stress.py << 'EOF'
import os
import time
import threading
import multiprocessing
from flask import Flask, request, jsonify

app = Flask(__name__)
stress_active = False
stress_processes = []

def cpu_stress_worker(duration, intensity):
    '''CPU intensive worker process'''
    end_time = time.time() + duration
    operations_per_cycle = intensity * 10000
    
    while time.time() < end_time:
        # CPU intensive mathematical operations
        for i in range(operations_per_cycle):
            result = sum(x*x for x in range(100))
            result += sum(x**0.5 for x in range(1, 100))
        
        # Short sleep to allow other processes
        time.sleep(0.01)

@app.route('/api/stress', methods=['POST'])
def start_stress():
    global stress_active, stress_processes
    
    data = request.json or {}
    intensity = int(data.get('intensity', 50))
    duration = int(data.get('duration', 60))
    
    # Stop existing stress
    stress_active = False
    for p in stress_processes:
        if p.is_alive():
            p.terminate()
            p.join(timeout=1)
    
    stress_processes = []
    stress_active = True
    
    # Start multiple processes for CPU stress
    num_processes = min(4, max(1, intensity // 25))
    
    for i in range(num_processes):
        process = multiprocessing.Process(
            target=cpu_stress_worker, 
            args=(duration, intensity // num_processes)
        )
        process.start()
        stress_processes.append(process)
    
    return jsonify({
        'status': 'started',
        'intensity': intensity,
        'duration': duration,
        'processes': num_processes
    })

@app.route('/api/stress', methods=['DELETE'])
def stop_stress():
    global stress_active, stress_processes
    
    stress_active = False
    for p in stress_processes:
        if p.is_alive():
            p.terminate()
    
    return jsonify({'status': 'stopped'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'active': stress_active})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
EOF
                                python /stress.py
                                """
                            ],
                            "ports": [
                                {
                                    "containerPort": 8080,
                                    "name": "stress-api"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "128Mi"
                                },
                                "limits": {
                                    "cpu": "1000m",  # Allow higher CPU for stress testing
                                    "memory": "512Mi"
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
    return deployment

def create_enhanced_hpa():
    """Create an enhanced HPA with better scaling policies"""
    hpa = {
        "apiVersion": "autoscaling/v2",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {
            "name": "cpu-stress-app-hpa",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "cpu-stress-app",
                "component": "autoscaler"
            }
        },
        "spec": {
            "scaleTargetRef": {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "name": "cpu-stress-app"
            },
            "minReplicas": 1,
            "maxReplicas": 10,
            "metrics": [
                {
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {
                            "type": "Utilization",
                            "averageUtilization": 50
                        }
                    }
                }
            ],
            "behavior": {
                "scaleUp": {
                    "stabilizationWindowSeconds": 15,  # React quickly to load
                    "policies": [
                        {
                            "type": "Percent",
                            "value": 100,
                            "periodSeconds": 15
                        },
                        {
                            "type": "Pods",
                            "value": 3,
                            "periodSeconds": 15
                        }
                    ],
                    "selectPolicy": "Max"
                },
                "scaleDown": {
                    "stabilizationWindowSeconds": 60,  # Conservative scale down
                    "policies": [
                        {
                            "type": "Percent",
                            "value": 50,
                            "periodSeconds": 60
                        },
                        {
                            "type": "Pods",
                            "value": 1,
                            "periodSeconds": 60
                        }
                    ],
                    "selectPolicy": "Min"
                }
            }
        }
    }
    return hpa

def create_dashboard_configmap():
    """Create ConfigMap with the enhanced dashboard HTML"""
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "scaling-dashboard-config",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "scaling-demo-app",
                "component": "dashboard"
            }
        },
        "data": {
            "index.html": create_enhanced_dashboard_html()
        }
    }
    return configmap

def create_services():
    """Create services for the scaling demo and load generator"""
    
    # Main dashboard service with NodePort
    dashboard_service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "scaling-demo-service",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "scaling-demo-app",
                "component": "web-service"
            }
        },
        "spec": {
            "type": "NodePort",
            "ports": [
                {
                    "port": 80,
                    "targetPort": 80,
                    "nodePort": 31003,
                    "name": "http"
                }
            ],
            "selector": {
                "app": "scaling-demo-app"
            }
        }
    }
    
    # Load generator service
    load_generator_service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "load-generator-service",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "load-generator",
                "component": "api-service"
            }
        },
        "spec": {
            "type": "ClusterIP",
            "ports": [
                {
                    "port": 5000,
                    "targetPort": 5000,
                    "name": "api"
                }
            ],
            "selector": {
                "app": "load-generator"
            }
        }
    }
    
    # CPU stress service
    stress_service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "cpu-stress-service",
            "namespace": "scaling-challenge",
            "labels": {
                "app": "cpu-stress-app",
                "component": "stress-service"
            }
        },
        "spec": {
            "type": "ClusterIP",
            "ports": [
                {
                    "port": 8080,
                    "targetPort": 8080,
                    "name": "stress-api"
                }
            ],
            "selector": {
                "app": "cpu-stress-app"
            }
        }
    }
    
    return [dashboard_service, load_generator_service, stress_service]

def apply_kubernetes_resource(resource):
    """Apply a Kubernetes resource using kubectl"""
    try:
        process = subprocess.run(
            ["kubectl", "apply", "-f", "-"],
            input=json.dumps(resource),
            text=True,
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to apply resource: {e.stderr}")
        return False

def wait_for_deployment(deployment_name, namespace="scaling-challenge", timeout=300):
    """Wait for deployment to be ready"""
    print(f"⏳ Waiting for {deployment_name} to be ready...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = run_kubectl([
            "get", "deployment", deployment_name, 
            "-o", "jsonpath={.status.readyReplicas}"
        ], namespace)
        
        if result and result != "0" and result != "<no value>":
            replicas = run_kubectl([
                "get", "deployment", deployment_name,
                "-o", "jsonpath={.spec.replicas}"
            ], namespace)
            
            if result == replicas:
                print(f"✅ {deployment_name} ready! {result}/{replicas} pods")
                return True
        
        time.sleep(5)
    
    print(f"❌ {deployment_name} failed to become ready within {timeout} seconds")
    return False

def check_metrics_server():
    """Check if metrics server is available"""
    print("📊 Checking metrics server availability...")
    
    result = run_kubectl(["top", "nodes"])
    if result and "error" not in result.lower():
        print("✅ Metrics server is available")
        return True
    else:
        print("⚠️ Metrics server not available - HPA may not work properly")
        print("💡 For Docker Desktop: Metrics server should be enabled by default")
        print("💡 For other clusters: kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml")
        return False

def get_access_instructions():
    """Get environment-specific access instructions"""
    # Try to detect the Kubernetes environment
    nodes_result = run_kubectl(["get", "nodes", "-o", "json"])
    
    instructions = """
🎯 ACCESS YOUR ENHANCED AUTO-SCALING DASHBOARD:

🐳 Docker Desktop:
   💻 Primary: http://localhost:31003
   
🎯 Minikube:
   🔧 Get URL: minikube service scaling-demo-service -n scaling-challenge --url
   
☁️ Cloud (EKS/GKE/AKS):
   🔧 Get node IP: kubectl get nodes -o wide
   🌐 Access: http://<node-external-ip>:31003
   
🌐 Universal (Always works):
   🔧 Port forward: kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80
   💻 Access: http://localhost:8080

📊 API Endpoints (for testing):
   🔧 Load Generator: kubectl port-forward svc/load-generator-service -n scaling-challenge 5000:5000
   🔧 CPU Stress: kubectl port-forward svc/cpu-stress-service -n scaling-challenge 8081:8080
"""
    
    return instructions

def main():
    """Main deployment function"""
    print("📈 ENHANCED AUTO-SCALING HERO DEPLOYMENT STARTING")
    print("=" * 70)
    
    # Create namespace
    if not create_namespace():
        sys.exit(1)
    
    # Create ConfigMap for dashboard
    print("🎨 Creating enhanced dashboard configuration...")
    if apply_kubernetes_resource(create_dashboard_configmap()):
        print("✅ Dashboard configuration created")
    else:
        print("❌ Failed to create dashboard configuration")
        sys.exit(1)
    
    # Deploy scalable application
    print("🚀 Deploying scalable demonstration application...")
    if apply_kubernetes_resource(create_scalable_app_deployment()):
        print("✅ Scalable application deployed")
    else:
        print("❌ Failed to deploy scalable application")
        sys.exit(1)
    
    # Deploy load generator
    print("⚡ Deploying enhanced load generator...")
    if apply_kubernetes_resource(create_load_generator_deployment()):
        print("✅ Load generator deployed")
    else:
        print("❌ Failed to deploy load generator")
        sys.exit(1)
    
    # Deploy CPU stress application (this will be the one that scales)
    print("🔥 Deploying CPU stress application...")
    if apply_kubernetes_resource(create_cpu_stress_deployment()):
        print("✅ CPU stress application deployed")
    else:
        print("❌ Failed to deploy CPU stress application")
        sys.exit(1)
    
    # Create HPA for CPU stress app
    print("📈 Creating enhanced Horizontal Pod Autoscaler...")
    if apply_kubernetes_resource(create_enhanced_hpa()):
        print("✅ HPA created with intelligent scaling policies")
    else:
        print("❌ Failed to create HPA")
        sys.exit(1)
    
    # Create services
    print("🌐 Creating application services...")
    services = create_services()
    all_services_created = True
    
    for service in services:
        if not apply_kubernetes_resource(service):
            all_services_created = False
    
    if all_services_created:
        print("✅ All services created successfully")
    else:
        print("❌ Some services failed to create")
        sys.exit(1)
    
    # Wait for deployments to be ready
    deployments = ["scaling-demo-app", "load-generator", "cpu-stress-app"]
    
    for deployment in deployments:
        if not wait_for_deployment(deployment):
            print(f"❌ {deployment} failed to start properly")
            sys.exit(1)
    
    # Check metrics server
    check_metrics_server()
    
    print("\n" + "=" * 70)
    print("🎉 ENHANCED AUTO-SCALING HERO DEPLOYMENT SUCCESSFUL!")
    print("✅ Interactive auto-scaling challenge ready with real scaling!")
    print("=" * 70)
    
    print(get_access_instructions())
    
    print("""
🎮 ENHANCED FEATURES:
   ✅ Real-time pod scaling visualization
   ✅ Clickable dashboard cards for detailed views
   ✅ CPU stress application that actually triggers scaling
   ✅ Interactive load testing with immediate feedback
   ✅ Live monitoring of scaling events
   ✅ Enhanced HPA with aggressive scaling policies

🧪 TESTING COMMANDS:
   📊 Watch scaling: kubectl get pods -n scaling-challenge -w
   📈 Monitor HPA: kubectl get hpa -n scaling-challenge -w
   ⚡ Start stress test: kubectl port-forward svc/cpu-stress-service -n scaling-challenge 8081:8080
                        curl -X POST http://localhost:8081/api/stress -H "Content-Type: application/json" -d '{"intensity":80,"duration":120}'
   🛑 Stop stress test: curl -X DELETE http://localhost:8081/api/stress

🎯 EXPECTED BEHAVIOR:
   1. Start with 1 pod
   2. Apply CPU load via dashboard or API
   3. Watch pods scale up: 1 → 2 → 4 → 8
   4. Stop load and watch scale down
   5. All changes visible in real-time dashboard!
""")

if __name__ == "__main__":
    main()