#!/usr/bin/env python3
"""
Jenkins Parameterized Builds - Interactive Demo
==============================================

Interactive demonstration of Jenkins parameterized builds with web applications.
Shows the power of parameterized builds vs static builds through visual comparison.

Usage:
    python3 demo_interactive.py
"""

import time
import threading
import subprocess
import sys
import os
import signal
import webbrowser
from pathlib import Path

class Colors:
    """Color support for terminal output."""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

class JenkinsParameterizedDemo:
    """Interactive Jenkins parameterized builds demonstration."""
    
    def __init__(self):
        self.processes = []
        self.running = True
        
    def print_header(self, message):
        """Print a header message."""
        print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")
        
    def print_step(self, message):
        """Print a step message."""
        print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")
        
    def print_success(self, message):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.NC}")
        
    def print_info(self, message):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}")
        
    def print_warning(self, message):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")
        
    def print_error(self, message):
        """Print an error message."""
        print(f"{Colors.RED}❌ {message}{Colors.NC}")
        
    def run_command(self, cmd, description=""):
        """Run a command with error handling."""
        if description:
            self.print_step(description)
            
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                self.print_error(f"Command failed: {result.stderr}")
                return False
        except Exception as e:
            self.print_error(f"Error running command: {e}")
            return False
    
    def start_application(self, app_name, port, description):
        """Start a web application."""
        self.print_step(f"Starting {app_name} on port {port}")
        
        try:
            # Create the application file if it doesn't exist
            app_file = f"{app_name.lower().replace(' ', '_')}_app.py"
            if not os.path.exists(app_file):
                self.create_demo_app(app_file, app_name, port)
            
            # Start the application
            process = subprocess.Popen(
                [sys.executable, app_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes.append(process)
            self.print_success(f"{app_name} started on http://localhost:{port}")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to start {app_name}: {e}")
            return False
    
    def create_demo_app(self, filename, app_name, port):
        """Create a demo application file."""
        if "dashboard" in app_name.lower():
            content = self.create_dashboard_app(port)
        elif "static" in app_name.lower():
            content = self.create_static_app(port)
        elif "parameterized" in app_name.lower():
            content = self.create_parameterized_app(port)
        else:
            content = self.create_basic_app(app_name, port)
            
        with open(filename, 'w') as f:
            f.write(content)
    
    def create_dashboard_app(self, port):
        """Create the parameterized builds dashboard app."""
        return f'''#!/usr/bin/env python3
"""
Jenkins Parameterized Builds Dashboard
=====================================
Real-time dashboard showing parameterized build metrics and analytics.
"""

from flask import Flask, render_template_string, jsonify
import time
import random
import threading

app = Flask(__name__)

# Dashboard HTML template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jenkins Parameterized Builds Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
            margin: 10px 0;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .metric-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .metric-change {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #f44336; }}
        .neutral {{ color: #ffd700; }}
        .comparison-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .comparison-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            color: #ffd700;
        }}
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .comparison-item {{
            text-align: center;
            padding: 15px;
            border-radius: 10px;
        }}
        .static-build {{
            background: rgba(244, 67, 54, 0.2);
            border: 2px solid #f44336;
        }}
        .parameterized-build {{
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid #4CAF50;
        }}
        .build-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .build-features {{
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }}
        .build-features li {{
            padding: 5px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .build-features li:last-child {{
            border-bottom: none;
        }}
        .auto-refresh {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        .pulse {{
            animation: pulse 2s infinite;
        }}
    </style>
    <script>
        function updateMetrics() {{
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('total-builds').textContent = data.total_builds;
                    document.getElementById('success-rate').textContent = data.success_rate + '%';
                    document.getElementById('avg-duration').textContent = data.avg_duration + 's';
                    document.getElementById('parameters-used').textContent = data.parameters_used;
                    document.getElementById('flexibility-score').textContent = data.flexibility_score + '%';
                    document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
                }})
                .catch(error => console.error('Error updating metrics:', error));
        }}
        
        // Update metrics every 3 seconds
        setInterval(updateMetrics, 3000);
        
        // Initial load
        updateMetrics();
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎛️ Jenkins Parameterized Builds Dashboard</h1>
            <p>Real-time analytics and comparison of build strategies</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Total Builds</div>
                <div class="metric-value" id="total-builds">0</div>
                <div class="metric-change positive">+12 this hour</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Success Rate</div>
                <div class="metric-value" id="success-rate">0%</div>
                <div class="metric-change positive">+5% improvement</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Avg Duration</div>
                <div class="metric-value" id="avg-duration">0s</div>
                <div class="metric-change negative">-15% faster</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Parameters Used</div>
                <div class="metric-value" id="parameters-used">0</div>
                <div class="metric-change positive">+300% flexibility</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Flexibility Score</div>
                <div class="metric-value" id="flexibility-score">0%</div>
                <div class="metric-change positive">+100% improvement</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Last Updated</div>
                <div class="metric-value" id="last-updated">--:--:--</div>
                <div class="metric-change neutral pulse">Auto-refreshing</div>
            </div>
        </div>
        
        <div class="comparison-section">
            <div class="comparison-title">Build Strategy Comparison</div>
            <div class="comparison-grid">
                <div class="comparison-item static-build">
                    <div class="build-title">❌ Static Builds</div>
                    <ul class="build-features">
                        <li>Fixed configuration</li>
                        <li>Single environment</li>
                        <li>No customization</li>
                        <li>Rigid workflows</li>
                        <li>Manual intervention needed</li>
                    </ul>
                </div>
                
                <div class="comparison-item parameterized-build">
                    <div class="build-title">✅ Parameterized Builds</div>
                    <ul class="build-features">
                        <li>Dynamic configuration</li>
                        <li>Multi-environment support</li>
                        <li>User-controlled parameters</li>
                        <li>Flexible workflows</li>
                        <li>Automated decision making</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="auto-refresh">
            🔄 Auto-refresh: 3s
        </div>
    </div>
</body>
</html>
"""

# Global metrics data
metrics_data = {{
    'total_builds': 0,
    'success_rate': 0,
    'avg_duration': 0,
    'parameters_used': 0,
    'flexibility_score': 0
}}

def update_metrics():
    """Update metrics data periodically."""
    global metrics_data
    while True:
        time.sleep(3)
        metrics_data.update({{
            'total_builds': random.randint(45, 55),
            'success_rate': random.randint(85, 95),
            'avg_duration': random.randint(120, 180),
            'parameters_used': random.randint(6, 10),
            'flexibility_score': random.randint(90, 100)
        }})

@app.route('/')
def dashboard():
    """Serve the main dashboard."""
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for metrics data."""
    return jsonify(metrics_data)

if __name__ == '__main__':
    # Start metrics update thread
    metrics_thread = threading.Thread(target=update_metrics, daemon=True)
    metrics_thread.start()
    
    print(f"🎛️ Jenkins Parameterized Builds Dashboard starting on port {port}")
    print(f"📊 Dashboard: http://localhost:{port}")
    print("🔄 Auto-refreshing metrics every 3 seconds")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_static_app(self, port):
        """Create the static build limitations app."""
        return f'''#!/usr/bin/env python3
"""
Static Build Limitations Demo
============================
Shows the limitations of static Jenkins builds.
"""

from flask import Flask, render_template_string
import time

app = Flask(__name__)

STATIC_APP_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Static Build Limitations</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .header {{
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .limitations {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .limitation-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #ff4757;
        }}
        .limitation-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .limitation-desc {{
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .warning {{
            background: rgba(255, 193, 7, 0.2);
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .warning-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #ffc107;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Static Build Limitations</h1>
            <p>Why static builds are problematic in modern CI/CD</p>
        </div>
        
        <div class="warning">
            <div class="warning-title">⚠️ Static Build Problems</div>
            <p>Static builds are rigid, inflexible, and don't adapt to changing requirements. 
            They force you to create separate jobs for each variation, leading to maintenance nightmares.</p>
        </div>
        
        <div class="limitations">
            <div class="limitation-item">
                <div class="limitation-title">🔒 Fixed Configuration</div>
                <div class="limitation-desc">
                    Static builds have hardcoded values that can't be changed without modifying the pipeline. 
                    This makes them inflexible and difficult to maintain.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">🌍 Single Environment</div>
                <div class="limitation-desc">
                    Each environment (dev, staging, prod) requires a separate job. 
                    This leads to job proliferation and inconsistent configurations.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">👤 No User Control</div>
                <div class="limitation-desc">
                    Users can't customize builds for their specific needs. 
                    Every build follows the same rigid path regardless of requirements.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">🔄 Manual Intervention</div>
                <div class="limitation-desc">
                    Changing build behavior requires manual pipeline modifications. 
                    This slows down development and increases the risk of errors.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">📊 No Dynamic Decisions</div>
                <div class="limitation-desc">
                    Builds can't make decisions based on parameters or conditions. 
                    They follow the same path every time, regardless of context.
                </div>
            </div>
        </div>
        
        <div class="warning">
            <div class="warning-title">💡 The Solution</div>
            <p>Parameterized builds solve all these problems by allowing dynamic configuration, 
            multi-environment support, and user-controlled customization. See the next app for the solution!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def static_limitations():
    """Serve the static limitations page."""
    return render_template_string(STATIC_APP_TEMPLATE)

if __name__ == '__main__':
    print(f"❌ Static Build Limitations Demo starting on port {port}")
    print(f"🌐 App: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_parameterized_app(self, port):
        """Create the parameterized build benefits app."""
        return f'''#!/usr/bin/env python3
"""
Parameterized Build Benefits Demo
================================
Shows the benefits and power of parameterized Jenkins builds.
"""

from flask import Flask, render_template_string
import time

app = Flask(__name__)

PARAMETERIZED_APP_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Parameterized Build Benefits</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .header {{
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .benefits {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .benefit-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #4CAF50;
        }}
        .benefit-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .benefit-desc {{
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .success {{
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .success-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
        }}
        .parameter-example {{
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            text-align: left;
        }}
        .parameter-example h3 {{
            color: #ffd700;
            margin-top: 0;
        }}
        .parameter-list {{
            list-style: none;
            padding: 0;
        }}
        .parameter-list li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .parameter-list li:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Parameterized Build Benefits</h1>
            <p>The power and flexibility of dynamic Jenkins builds</p>
        </div>
        
        <div class="success">
            <div class="success-title">🎉 Parameterized Build Advantages</div>
            <p>Parameterized builds transform your CI/CD pipeline into a flexible, 
            user-controlled system that adapts to any requirement or environment.</p>
        </div>
        
        <div class="benefits">
            <div class="benefit-item">
                <div class="benefit-title">🎛️ Dynamic Configuration</div>
                <div class="benefit-desc">
                    Users can customize builds with parameters like environment, branch, 
                    deployment strategy, and notification preferences. No more hardcoded values!
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">🌍 Multi-Environment Support</div>
                <div class="benefit-desc">
                    One job handles all environments (dev, staging, prod) with environment-specific 
                    configurations. Reduces job proliferation and ensures consistency.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">👤 User Control</div>
                <div class="benefit-desc">
                    Users can control build behavior through parameters. Choose deployment targets, 
                    testing strategies, and notification channels based on their needs.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">🔄 Automated Decisions</div>
                <div class="benefit-desc">
                    Builds can make intelligent decisions based on parameters. Different testing 
                    strategies for different environments, conditional deployments, and smart notifications.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">📊 Flexible Workflows</div>
                <div class="benefit-desc">
                    Workflows adapt to parameters. Skip certain stages based on environment, 
                    run different test suites, or deploy to different targets automatically.
                </div>
            </div>
        </div>
        
        <div class="parameter-example">
            <h3>🎛️ Example Parameters</h3>
            <ul class="parameter-list">
                <li><strong>ENVIRONMENT:</strong> dev, staging, production</li>
                <li><strong>BRANCH:</strong> main, develop, feature/*</li>
                <li><strong>DEPLOY_STRATEGY:</strong> rolling, blue-green, canary</li>
                <li><strong>RUN_TESTS:</strong> true, false</li>
                <li><strong>NOTIFICATION_CHANNEL:</strong> email, slack, teams</li>
                <li><strong>DOCKER_TAG:</strong> latest, version-specific</li>
                <li><strong>RESOURCE_LIMITS:</strong> small, medium, large</li>
                <li><strong>BACKUP_ENABLED:</strong> true, false</li>
            </ul>
        </div>
        
        <div class="success">
            <div class="success-title">🚀 The Result</div>
            <p>One flexible job that handles all scenarios, reduces maintenance overhead, 
            and provides users with the control they need. This is the power of parameterized builds!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def parameterized_benefits():
    """Serve the parameterized benefits page."""
    return render_template_string(PARAMETERIZED_APP_TEMPLATE)

if __name__ == '__main__':
    print(f"✅ Parameterized Build Benefits Demo starting on port {port}")
    print(f"🌐 App: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_basic_app(self, app_name, port):
        """Create a basic demo app."""
        return f'''#!/usr/bin/env python3
"""
{app_name} Demo
==============
Basic demo application.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>{app_name}</h1><p>Demo application running on port {port}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        self.print_warning("\\n🛑 Demo interrupted by user")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up running processes."""
        self.print_step("Cleaning up processes...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        self.print_success("Cleanup complete")
    
    def run_demo(self):
        """Run the interactive demo."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.print_header("Jenkins Parameterized Builds - Interactive Demo")
        self.print_info("This demo showcases the power of parameterized builds vs static builds")
        self.print_info("You'll see 3 web applications demonstrating the concepts")
        
        # Install dependencies
        self.print_step("Installing dependencies...")
        if not self.run_command("pip install flask requests pyyaml", "Installing Python packages"):
            self.print_error("Failed to install dependencies")
            return False
        
        # Start applications
        apps = [
            ("Parameterized Dashboard", 8000, "Real-time analytics and comparison"),
            ("Static Build Limitations", 8001, "Shows static build problems"),
            ("Parameterized Benefits", 8002, "Demonstrates parameterized build power")
        ]
        
        for app_name, port, description in apps:
            if not self.start_application(app_name, port, description):
                self.print_error(f"Failed to start {app_name}")
                return False
            time.sleep(2)  # Give each app time to start
        
        # Open browsers
        self.print_step("Opening web applications...")
        try:
            webbrowser.open('http://localhost:8000')
            time.sleep(1)
            webbrowser.open('http://localhost:8001')
            time.sleep(1)
            webbrowser.open('http://localhost:8002')
        except:
            self.print_warning("Could not auto-open browsers")
        
        # Display URLs
        self.print_success("🎉 Demo applications are running!")
        self.print_info("📊 Dashboard: http://localhost:8000")
        self.print_info("❌ Static Limitations: http://localhost:8001")
        self.print_info("✅ Parameterized Benefits: http://localhost:8002")
        self.print_info("")
        self.print_info("Press Ctrl+C to stop the demo")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

def main():
    """Main function."""
    demo = JenkinsParameterizedDemo()
    demo.run_demo()

if __name__ == '__main__':
    main()
