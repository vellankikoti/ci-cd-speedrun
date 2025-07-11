#!/usr/bin/env python3
"""
Production-Grade Auto-scaling Dashboard & API
Serves the dashboard at / and provides real /api/metrics and /api/load-test endpoints.
"""

import os
import time
import threading
import requests
from flask import Flask, request, jsonify, send_file, make_response
import subprocess
import json

app = Flask(__name__)
load_active = False
load_threads = []

# --- Dashboard HTML (paste the full HTML here, with simulation logic removed) ---
DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦸‍♂️ Auto-scaling Hero Control Center</title>
    <style>
        /* ... (all CSS as before) ... */
    </style>
</head>
<body>
    <!-- ... (all HTML as before) ... -->
    <script>
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
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    updateMetrics(data);
                })
                .catch(error => {
                    addLogEntry('❌ Failed to fetch real metrics: ' + error);
                });
        }

        function updateMetrics(data) {
            document.getElementById('current-pods').textContent = data.currentPods;
            document.getElementById('target-pods').textContent = data.targetPods;
            document.getElementById('cpu-usage').textContent = data.cpuUsage + '%';
            updateCpuChart(data.cpuUsage);
            // ... (update other dashboard elements as needed) ...
        }

        // ... (rest of the JS, but remove simulateMetrics and all simulation logic) ...

        window.onload = function() {
            addLogEntry('🎯 Dashboard initialized - monitoring scaling metrics');
            setInterval(updateDashboard, 2000);
            updateDashboard();
        };
    </script>
</body>
</html>'''

# --- Flask routes ---
@app.route("/")
def dashboard():
    resp = make_response(DASHBOARD_HTML)
    resp.headers['Content-Type'] = 'text/html'
    return resp

@app.route('/api/load-test', methods=['POST'])
def start_load_test():
    global load_active, load_threads
    data = request.json
    intensity = int(data.get('intensity', 50))
    duration = int(data.get('duration', 60))
    pattern = data.get('pattern', 'steady')
    # ... (same logic as before for starting load) ...
    return jsonify({'status': 'started', 'intensity': intensity, 'duration': duration, 'pattern': pattern})

@app.route('/api/load-test', methods=['DELETE'])
def stop_load_test():
    global load_active
    load_active = False
    return jsonify({'status': 'stopped'})

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    try:
        pods_result = subprocess.run([
            'kubectl', 'get', 'pods', '-n', 'scaling-challenge',
            '-l', 'app=cpu-stress-app',
            '-o', 'json'
        ], capture_output=True, text=True)
        if pods_result.returncode == 0:
            pods_data = json.loads(pods_result.stdout)
            current_pods = len([p for p in pods_data['items'] if p['status']['phase'] == 'Running'])
        else:
            current_pods = 1
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
                current_metrics = hpa['status'].get('currentMetrics', [])
                for metric in current_metrics:
                    if metric['type'] == 'Resource' and metric['resource']['name'] == 'cpu':
                        cpu_usage = metric['resource']['current']['averageUtilization']
                        break
        return jsonify({
            'currentPods': current_pods,
            'targetPods': target_pods,
            'cpuUsage': cpu_usage,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'currentPods': 1,
            'targetPods': 1,
            'cpuUsage': 0,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 