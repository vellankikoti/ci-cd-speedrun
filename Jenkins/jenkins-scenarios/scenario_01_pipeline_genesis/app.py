#!/usr/bin/env python3
"""
Pipeline Genesis - Simple Flask Application
A clean, simple Flask app for learning Jenkins pipeline basics.
"""

from flask import Flask, jsonify
import sys
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Welcome page with basic information."""
    return """
    <html>
        <head>
            <title>Pipeline Genesis - Jenkins Learning App</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; margin: 5px; display: inline-block; }
                .success { color: #27ae60; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Pipeline Genesis</h1>
                <p class="success">Your first Jenkins pipeline is working!</p>
                
                <div class="info">
                    <h3>Available Endpoints:</h3>
                    <span class="endpoint">GET /</span> - This welcome page
                    <span class="endpoint">GET /health</span> - Health check
                    <span class="endpoint">GET /info</span> - System information
                </div>
                
                <div class="info">
                    <h3>What You've Learned:</h3>
                    <ul>
                        <li>✅ Jenkins pipeline basics</li>
                        <li>✅ Stage and step concepts</li>
                        <li>✅ Simple automation workflow</li>
                        <li>✅ Build triggers and execution</li>
                    </ul>
                </div>
                
                <p><strong>Next:</strong> Try the other endpoints to explore more!</p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Pipeline Genesis app is running perfectly!'
    })

@app.route('/info')
def info():
    """System information endpoint."""
    return jsonify({
        'app_name': 'Pipeline Genesis',
        'python_version': sys.version,
        'platform': sys.platform,
        'working_directory': os.getcwd(),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('ENVIRONMENT', 'development') == 'development'
    
    print(f"🚀 Starting Pipeline Genesis app on port {port}")
    print(f"📱 Visit: http://localhost:{port}")
    print(f"❤️  Health: http://localhost:{port}/health")
    print(f"ℹ️  Info: http://localhost:{port}/info")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
