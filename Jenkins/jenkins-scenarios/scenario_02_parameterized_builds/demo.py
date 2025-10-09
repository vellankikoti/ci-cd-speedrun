#!/usr/bin/env python3
"""
Perfect Demo for Scenario 2: Parameterized Builds
Simple, clean demonstration of Jenkins parameterized builds with web application
"""

import os
import sys
import time
import webbrowser
import subprocess
import threading
from datetime import datetime

class ParameterizedBuildsDemo:
    def __init__(self):
        self.port = 8080
        self.webapp_process = None
        
    def print_header(self, title):
        """Print a beautiful header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    def print_section(self, title):
        """Print a section header"""
        print(f"\n🔹 {title}")
        print("-" * 60)
    
    def generate_webapp(self, environment, version, features, run_tests, deployment_notes):
        """Generate a simple web application based on parameters"""
        print(f"🌐 Generating web application for {environment} + {features}...")
        
        # Environment-specific configurations
        env_configs = {
            "Development": {"color": "#28a745", "icon": "🛠️", "desc": "Development Environment"},
            "Staging": {"color": "#ffc107", "icon": "🧪", "desc": "Staging Environment"},
            "Production": {"color": "#dc3545", "icon": "🚀", "desc": "Production Environment"}
        }
        
        # Feature-specific configurations
        feature_configs = {
            "Basic": {"capabilities": ["User Auth", "Basic CRUD", "Simple Dashboard"], "price": "Free"},
            "Advanced": {"capabilities": ["Analytics", "API Integration", "Custom Dashboards"], "price": "$99/month"},
            "Enterprise": {"capabilities": ["AI/ML", "Multi-tenant", "Custom Workflows"], "price": "Custom"}
        }
        
        env_config = env_configs[environment]
        feature_config = feature_configs[features]
        
        # Generate HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins Parameterized Build Demo - {environment}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, {env_config['color']}20 0%, #f8f9fa 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, {env_config['color']} 0%, #2c3e50 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .info-card {{
            background: #f8f9fa;
            border: 2px solid {env_config['color']}30;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        .info-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        .info-card h3 {{ color: {env_config['color']}; margin-bottom: 15px; font-size: 1.3em; }}
        .feature-list {{ list-style: none; padding: 0; }}
        .feature-list li {{ padding: 8px 0; border-bottom: 1px solid #e9ecef; }}
        .feature-list li:before {{ content: '✅'; margin-right: 10px; }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .metric {{ text-align: center; padding: 15px; background: white; border-radius: 8px; border: 2px solid {env_config['color']}20; }}
        .metric-value {{ font-size: 1.5em; font-weight: bold; color: {env_config['color']}; }}
        .metric-label {{ font-size: 0.9em; color: #6c757d; margin-top: 5px; }}
        .demo-section {{
            background: linear-gradient(135deg, {env_config['color']}10 0%, #f8f9fa 100%);
            border: 2px solid {env_config['color']}30;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }}
        .demo-button {{
            background: linear-gradient(135deg, {env_config['color']} 0%, #2c3e50 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
        }}
        .demo-button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        .demo-output {{
            background: white;
            border: 2px solid {env_config['color']}30;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            min-height: 100px;
            display: none;
        }}
        .demo-output.active {{ display: block; animation: fadeIn 0.5s ease-in; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{env_config['icon']} {env_config['desc']}</h1>
            <p>Version {version} - Generated by Jenkins Parameterized Build</p>
        </div>
        
        <div class="content">
            <div class="info-grid">
                <div class="info-card">
                    <h3>🌍 Environment: {environment}</h3>
                    <ul class="feature-list">
                        <li>Environment: {environment}</li>
                        <li>Version: {version}</li>
                        <li>Features: {features}</li>
                        <li>Tests: {'Enabled' if run_tests else 'Disabled'}</li>
                        <li>Notes: {deployment_notes}</li>
                    </ul>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">{'1 Core' if features == 'Basic' else '2 Cores' if features == 'Advanced' else '4 Cores'}</div>
                            <div class="metric-label">CPU</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{'512MB' if features == 'Basic' else '1GB' if features == 'Advanced' else '4GB'}</div>
                            <div class="metric-label">Memory</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{feature_config['price']}</div>
                            <div class="metric-label">Pricing</div>
                        </div>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3>🎛️ Features: {features}</h3>
                    <ul class="feature-list">
                        {''.join([f'<li>{capability}</li>' for capability in feature_config['capabilities']])}
                    </ul>
                </div>
            </div>
            
            <div class="demo-section">
                <h3>🎮 Interactive Demo</h3>
                <p>Click the buttons below to see Jenkins parameterized build features:</p>
                
                <button class="demo-button" onclick="showFeatureDemo()">Show Features</button>
                <button class="demo-button" onclick="showEnvironmentDemo()">Show Environment</button>
                <button class="demo-button" onclick="showMonitoringDemo()">Show Monitoring</button>
                
                <div id="demo-output" class="demo-output">
                    <h4>Demo Output</h4>
                    <div id="demo-content"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Jenkins Parameterized Build - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <script>
        function showFeatureDemo() {{
            const content = `
                <h4>🎛️ Feature Demo: {features}</h4>
                <p><strong>Capabilities:</strong></p>
                <ul>
                    {''.join([f'<li>{capability}</li>' for capability in feature_config['capabilities']])}
                </ul>
                <p><strong>Pricing:</strong> {feature_config['price']}</p>
                <div style="background: {env_config['color']}20; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>Jenkins Action:</strong> Deployed {features} features to {environment} environment
                </div>
            `;
            showDemo(content);
        }}
        
        function showEnvironmentDemo() {{
            const content = `
                <h4>🌍 Environment Demo: {environment}</h4>
                <p><strong>Configuration:</strong></p>
                <ul>
                    <li>Environment: {environment}</li>
                    <li>Color Scheme: {env_config['color']}</li>
                    <li>Icon: {env_config['icon']}</li>
                    <li>Description: {env_config['desc']}</li>
                </ul>
                <div style="background: {env_config['color']}20; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>Jenkins Action:</strong> Configured {environment} environment with {features} features
                </div>
            `;
            showDemo(content);
        }}
        
        function showMonitoringDemo() {{
            const content = `
                <h4>📊 Monitoring Demo</h4>
                <p><strong>Real-time Metrics:</strong></p>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0;">
                    <div style="background: #e3f2fd; padding: 10px; border-radius: 5px; text-align: center;">
                        <div style="font-size: 1.5em; font-weight: bold; color: #1976d2;">95%</div>
                        <div style="font-size: 0.9em; color: #666;">CPU Usage</div>
                    </div>
                    <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; text-align: center;">
                        <div style="font-size: 1.5em; font-weight: bold; color: #2e7d32;">2.1GB</div>
                        <div style="font-size: 0.9em; color: #666;">Memory Used</div>
                    </div>
                    <div style="background: #fff3e0; padding: 10px; border-radius: 5px; text-align: center;">
                        <div style="font-size: 1.5em; font-weight: bold; color: #f57c00;">42ms</div>
                        <div style="font-size: 0.9em; color: #666;">Response Time</div>
                    </div>
                </div>
                <div style="background: {env_config['color']}20; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>Jenkins Action:</strong> Set up monitoring for {environment} environment
                </div>
            `;
            showDemo(content);
        }}
        
        function showDemo(content) {{
            const output = document.getElementById('demo-output');
            const demoContent = document.getElementById('demo-content');
            demoContent.innerHTML = content;
            output.classList.add('active');
        }}
    </script>
</body>
</html>
        """
        
        # Save HTML file
        os.makedirs("webapp", exist_ok=True)
        with open("webapp/index.html", "w") as f:
            f.write(html_content)
        
        print(f"✅ Web application generated: webapp/index.html")
        return True
    
    def start_webapp_server(self):
        """Start the web application server"""
        try:
            # Start web application server
            cmd = ["python3", "-m", "http.server", str(self.port)]
            self.webapp_process = subprocess.Popen(
                cmd, 
                cwd=os.path.join(os.getcwd(), "webapp"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Test if server is running
            import urllib.request
            try:
                response = urllib.request.urlopen(f"http://localhost:{self.port}", timeout=5)
                if response.getcode() == 200:
                    print(f"✅ Web application server started on port {self.port}")
                    return True
            except:
                pass
            
            print(f"⚠️  Web application server may not be ready yet")
            return True
            
        except Exception as e:
            print(f"❌ Error starting web application server: {e}")
            return False
    
    def run_demo(self):
        """Run the perfect demo"""
        self.print_header("🚀 Jenkins Parameterized Builds Demo")
        
        print("""
This demo shows the power of Jenkins parameterized builds with:

✅ Interactive Web Applications:
   • Real-time web app generation based on parameters
   • Visual demonstration of parameter effects
   • Environment-specific styling and features
   • Feature-specific capabilities and resources

✅ Simple & Clean:
   • One perfect script
   • Clean directory structure
   • Easy to understand and use
   • Professional output

✅ Educational Value:
   • See how parameters affect the final application
   • Understand environment-specific configurations
   • Learn feature flag implementation
   • Experience real-time parameter feedback
""")
        
        # Generate demo web applications
        self.print_section("Generating Demo Web Applications")
        
        scenarios = [
            ("Development", "1.0.0", "Basic", True, "Development testing"),
            ("Staging", "1.2.0", "Advanced", True, "Pre-production testing"),
            ("Production", "2.0.0", "Enterprise", True, "Production release")
        ]
        
        for i, (env, version, features, run_tests, notes) in enumerate(scenarios):
            print(f"\n🧪 Generating scenario {i+1}: {env} + {features}")
            
            if self.generate_webapp(env, version, features, run_tests, notes):
                print(f"   ✅ Web application generated for {env} + {features}")
            else:
                print(f"   ❌ Failed to generate web application for {env} + {features}")
        
        # Start web application server
        self.print_section("Starting Web Application Server")
        if self.start_webapp_server():
            print("✅ Web application server started")
        else:
            print("❌ Failed to start web application server")
        
        # Open browser
        try:
            webbrowser.open(f'http://localhost:{self.port}')
            print("✅ Browser opened")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"   Please open http://localhost:{self.port} manually")
        
        print("\n🎯 Demo Instructions:")
        print("1. View the generated web application in your browser")
        print("2. Click the interactive buttons to see different features")
        print("3. Notice how the app changes based on parameters")
        print("4. Compare different environment and feature combinations")
        
        print("\n📋 Jenkins Setup Instructions:")
        print("1. Go to Jenkins: http://localhost:8080")
        print("2. Create new Pipeline job")
        print("3. Enable 'This project is parameterized'")
        print("4. Add the parameters from the guide")
        print("5. Point to scenario_02_parameterized_builds/Jenkinsfile")
        print("6. Run the pipeline to see web application generation!")
        
        print("\n🎓 Learning Outcomes:")
        print("• Understand how parameters affect application generation")
        print("• See environment-specific configurations in action")
        print("• Learn feature flag implementation")
        print("• Experience real-time parameter feedback")
        print("• See the power of Jenkins parameterized builds")
        
        print(f"\n🌐 Demo running at: http://localhost:{self.port}")
        print("Press Ctrl+C to stop the demo")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Demo stopped. Thanks for learning about parameterized builds!")
            if self.webapp_process:
                self.webapp_process.terminate()

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-webapp":
        # Command-line mode for Jenkins
        if len(sys.argv) < 7:
            print("Usage: python3 demo.py --generate-webapp <environment> <version> <features> <run_tests> <deployment_notes>")
            sys.exit(1)
        
        environment = sys.argv[2]
        version = sys.argv[3]
        features = sys.argv[4]
        run_tests = sys.argv[5].lower() == 'true'
        deployment_notes = sys.argv[6]
        
        print(f"🌐 Generating web application for {environment} + {features}...")
        
        demo = ParameterizedBuildsDemo()
        if demo.generate_webapp(environment, version, features, run_tests, deployment_notes):
            print("✅ Web application generated successfully!")
        else:
            print("❌ Failed to generate web application")
            sys.exit(1)
    else:
        # Interactive demo mode
        demo = ParameterizedBuildsDemo()
        demo.run_demo()

if __name__ == "__main__":
    main()
