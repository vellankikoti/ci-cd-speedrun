#!/usr/bin/env python3
"""
Interactive Demo for Scenario 2: Parameterized Builds
Demonstrates the power of Jenkins parameterized builds with a visual interface
"""

import os
import sys
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json
from datetime import datetime

class ParameterizedBuildsDemo:
    def __init__(self):
        self.port = 8081
        self.server = None
        self.demo_data = {
            "scenarios": [
                {
                    "name": "Development Deployment",
                    "environment": "Development",
                    "version": "1.2.3",
                    "features": "Basic",
                    "run_tests": True,
                    "description": "Quick development deployment with basic features"
                },
                {
                    "name": "Staging Deployment",
                    "environment": "Staging",
                    "version": "1.2.3",
                    "features": "Advanced",
                    "run_tests": True,
                    "description": "Pre-production testing with advanced features"
                },
                {
                    "name": "Production Deployment",
                    "environment": "Production",
                    "version": "1.2.3",
                    "features": "Enterprise",
                    "run_tests": True,
                    "description": "Full production deployment with enterprise features"
                }
            ],
            "current_scenario": 0
        }
    
    def create_demo_html(self):
        """Create the interactive demo HTML page"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins Parameterized Builds Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .demo-section {{
            margin-bottom: 40px;
        }}
        
        .demo-section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .parameter-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .parameter-card {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        
        .parameter-card:hover {{
            border-color: #007bff;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.1);
        }}
        
        .parameter-card h3 {{
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .parameter-options {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .option-btn {{
            padding: 8px 16px;
            border: 2px solid #dee2e6;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }}
        
        .option-btn:hover {{
            border-color: #007bff;
            color: #007bff;
        }}
        
        .option-btn.active {{
            background: #007bff;
            color: white;
            border-color: #007bff;
        }}
        
        .checkbox-container {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .checkbox-container input[type="checkbox"] {{
            width: 20px;
            height: 20px;
            cursor: pointer;
        }}
        
        .scenario-buttons {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .scenario-btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .scenario-btn.development {{
            background: #28a745;
            color: white;
        }}
        
        .scenario-btn.staging {{
            background: #ffc107;
            color: #212529;
        }}
        
        .scenario-btn.production {{
            background: #dc3545;
            color: white;
        }}
        
        .scenario-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .jenkins-link {{
            display: inline-block;
            background: #2c3e50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-top: 20px;
        }}
        
        .jenkins-link:hover {{
            background: #34495e;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
        }}
        
        .info-box h4 {{
            color: #1976d2;
            margin-bottom: 10px;
        }}
        
        .current-selection {{
            background: #f8f9fa;
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .current-selection h3 {{
            color: #28a745;
            margin-bottom: 15px;
        }}
        
        .selection-item {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 5px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .selection-item:last-child {{
            border-bottom: none;
        }}
        
        .selection-label {{
            font-weight: 600;
            color: #495057;
        }}
        
        .selection-value {{
            color: #007bff;
            font-weight: 500;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Jenkins Parameterized Builds Demo</h1>
            <p>Experience the power of dynamic Jenkins pipelines with user input parameters</p>
        </div>
        
        <div class="content">
            <div class="demo-section">
                <h2>🎯 Quick Start Scenarios</h2>
                <p>Click on a scenario to see how parameterized builds work in different environments:</p>
                
                <div class="scenario-buttons">
                    <button class="scenario-btn development" onclick="loadScenario(0)">
                        🛠️ Development
                    </button>
                    <button class="scenario-btn staging" onclick="loadScenario(1)">
                        🧪 Staging
                    </button>
                    <button class="scenario-btn production" onclick="loadScenario(2)">
                        🚀 Production
                    </button>
                </div>
            </div>
            
            <div class="demo-section">
                <h2>⚙️ Parameter Configuration</h2>
                <p>Configure your deployment parameters and see how Jenkins responds:</p>
                
                <div class="parameter-grid">
                    <div class="parameter-card">
                        <h3>🌍 Environment</h3>
                        <div class="parameter-options">
                            <button class="option-btn active" onclick="selectOption('environment', 'Development')">Development</button>
                            <button class="option-btn" onclick="selectOption('environment', 'Staging')">Staging</button>
                            <button class="option-btn" onclick="selectOption('environment', 'Production')">Production</button>
                        </div>
                    </div>
                    
                    <div class="parameter-card">
                        <h3>📦 Version</h3>
                        <input type="text" id="version" value="1.0.0" style="width: 100%; padding: 10px; border: 2px solid #dee2e6; border-radius: 5px; font-size: 1em;">
                    </div>
                    
                    <div class="parameter-card">
                        <h3>🎛️ Features</h3>
                        <div class="parameter-options">
                            <button class="option-btn active" onclick="selectOption('features', 'Basic')">Basic</button>
                            <button class="option-btn" onclick="selectOption('features', 'Advanced')">Advanced</button>
                            <button class="option-btn" onclick="selectOption('features', 'Enterprise')">Enterprise</button>
                        </div>
                    </div>
                    
                    <div class="parameter-card">
                        <h3>🧪 Run Tests</h3>
                        <div class="checkbox-container">
                            <input type="checkbox" id="run_tests" checked>
                            <label for="run_tests">Execute automated tests before deployment</label>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="current-selection">
                <h3>📋 Current Selection</h3>
                <div class="selection-item">
                    <span class="selection-label">Environment:</span>
                    <span class="selection-value" id="current-environment">Development</span>
                </div>
                <div class="selection-item">
                    <span class="selection-label">Version:</span>
                    <span class="selection-value" id="current-version">1.0.0</span>
                </div>
                <div class="selection-item">
                    <span class="selection-label">Features:</span>
                    <span class="selection-value" id="current-features">Basic</span>
                </div>
                <div class="selection-item">
                    <span class="selection-label">Run Tests:</span>
                    <span class="selection-value" id="current-tests">Yes</span>
                </div>
            </div>
            
            <div class="info-box">
                <h4>💡 What You'll Learn</h4>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>Parameter Types:</strong> Choice, String, Boolean parameters</li>
                    <li><strong>Conditional Logic:</strong> Different actions based on user input</li>
                    <li><strong>Environment Management:</strong> Deploy to different environments</li>
                    <li><strong>Feature Flags:</strong> Enable/disable features per deployment</li>
                    <li><strong>Real-time Feedback:</strong> See how Jenkins responds to parameters</li>
                </ul>
            </div>
            
            <div style="text-align: center;">
                <a href="http://localhost:8080" class="jenkins-link" target="_blank">
                    🚀 Open Jenkins to Run Parameterized Build
                </a>
            </div>
        </div>
        
        <div class="footer">
            <p>Scenario 2: Parameterized Builds - Interactive Jenkins Demo</p>
        </div>
    </div>
    
    <script>
        const demoData = {json.dumps(self.demo_data)};
        let currentParams = {{
            environment: 'Development',
            version: '1.0.0',
            features: 'Basic',
            run_tests: true
        }};
        
        function selectOption(type, value) {{
            // Update button states
            document.querySelectorAll(`[onclick*="${{type}}"]`).forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Update current parameters
            currentParams[type] = value;
            updateCurrentSelection();
        }}
        
        function loadScenario(index) {{
            const scenario = demoData.scenarios[index];
            currentParams = {{
                environment: scenario.environment,
                version: scenario.version,
                features: scenario.features,
                run_tests: scenario.run_tests
            }};
            
            // Update UI
            updateParameterUI();
            updateCurrentSelection();
        }}
        
        function updateParameterUI() {{
            // Update environment buttons
            document.querySelectorAll('[onclick*="environment"]').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === currentParams.environment) {{
                    btn.classList.add('active');
                }}
            }});
            
            // Update features buttons
            document.querySelectorAll('[onclick*="features"]').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === currentParams.features) {{
                    btn.classList.add('active');
                }}
            }});
            
            // Update version input
            document.getElementById('version').value = currentParams.version;
            
            // Update tests checkbox
            document.getElementById('run_tests').checked = currentParams.run_tests;
        }}
        
        function updateCurrentSelection() {{
            document.getElementById('current-environment').textContent = currentParams.environment;
            document.getElementById('current-version').textContent = currentParams.version;
            document.getElementById('current-features').textContent = currentParams.features;
            document.getElementById('current-tests').textContent = currentParams.run_tests ? 'Yes' : 'No';
        }}
        
        // Update version when input changes
        document.getElementById('version').addEventListener('input', function() {{
            currentParams.version = this.value;
            updateCurrentSelection();
        }});
        
        // Update tests when checkbox changes
        document.getElementById('run_tests').addEventListener('change', function() {{
            currentParams.run_tests = this.checked;
            updateCurrentSelection();
        }});
        
        // Initialize
        updateCurrentSelection();
    </script>
</body>
</html>
        """
        
        with open('demo.html', 'w') as f:
            f.write(html_content)
    
    def start_server(self):
        """Start the demo web server"""
        class DemoHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=os.getcwd(), **kwargs)
            
            def log_message(self, format, *args):
                # Suppress default logging
                pass
        
        self.server = HTTPServer(('localhost', self.port), DemoHandler)
        print(f"🌐 Demo server starting on http://localhost:{self.port}")
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server_thread
    
    def run_demo(self):
        """Run the interactive demo"""
        print("🚀 Starting Jenkins Parameterized Builds Demo")
        print("=" * 60)
        
        # Create demo HTML
        self.create_demo_html()
        print("✅ Demo HTML created")
        
        # Start web server
        self.start_server()
        print("✅ Demo server started")
        
        # Open browser
        try:
            webbrowser.open(f'http://localhost:{self.port}')
            print("✅ Browser opened")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"   Please open http://localhost:{self.port} manually")
        
        print("\n🎯 Demo Instructions:")
        print("1. Use the interactive interface to configure parameters")
        print("2. Try different scenarios (Development, Staging, Production)")
        print("3. Click 'Open Jenkins' to run the actual parameterized build")
        print("4. Compare the demo interface with Jenkins parameterized build UI")
        
        print("\n📋 Jenkins Setup Instructions:")
        print("1. Go to Jenkins: http://localhost:8080")
        print("2. Create new Pipeline job")
        print("3. Enable 'This project is parameterized'")
        print("4. Add the parameters from the demo")
        print("5. Point to scenario_02_parameterized_builds/Jenkinsfile")
        
        print("\n🎓 Learning Objectives:")
        print("• Understand different parameter types")
        print("• See how conditional logic works")
        print("• Experience environment-specific deployments")
        print("• Learn feature flag implementation")
        print("• See real-time parameter feedback")
        
        print(f"\n🌐 Demo running at: http://localhost:{self.port}")
        print("Press Ctrl+C to stop the demo")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Demo stopped. Thanks for learning about parameterized builds!")
            if self.server:
                self.server.shutdown()

def main():
    """Main function"""
    demo = ParameterizedBuildsDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()