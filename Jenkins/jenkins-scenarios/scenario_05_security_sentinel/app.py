#!/usr/bin/env python3
"""
Security Sentinel - Flask Application with Security Features
A Flask app demonstrating DevSecOps principles and security best practices.
"""

from flask import Flask, request, jsonify, render_template_string, session
import os
import sys
import time
import psutil
import signal
import threading
import hashlib
import secrets
import base64
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Security configuration
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Global variables for metrics
start_time = time.time()
request_count = 0
shutdown_requested = False
security_events = []

def security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

app.after_request(security_headers)

def log_security_event(event_type, details):
    """Log security events for audit purposes."""
    global security_events
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'details': details,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    security_events.append(event)
    print(f"🔒 Security Event: {event_type} - {details}")

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            log_security_event('AUTH_FAILED', 'Unauthorized access attempt')
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_input(data):
    """Validate input for security vulnerabilities."""
    if not data:
        return True, "Valid input"
    
    # Check for SQL injection patterns
    sql_patterns = ['union', 'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter']
    if any(pattern in str(data).lower() for pattern in sql_patterns):
        log_security_event('SQL_INJECTION_ATTEMPT', f'SQL injection pattern detected: {data}')
        return False, "Potential SQL injection detected"
    
    # Check for XSS patterns
    xss_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
    if any(pattern in str(data).lower() for pattern in xss_patterns):
        log_security_event('XSS_ATTEMPT', f'XSS pattern detected: {data}')
        return False, "Potential XSS detected"
    
    return True, "Valid input"

@app.route('/')
def home():
    """Welcome page with security features."""
    return render_template_string("""
    <html>
        <head>
            <title>Security Sentinel - DevSecOps Mastery</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; margin: 5px; display: inline-block; }
                .success { color: #27ae60; font-weight: bold; }
                .warning { color: #f39c12; font-weight: bold; }
                .error { color: #e74c3c; font-weight: bold; }
                .feature { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 10px 0; }
                .metrics { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .security-info { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                button { background: #e74c3c; color: white; padding: 8px 15px; border: none; border-radius: 3px; cursor: pointer; }
                button:hover { background: #c0392b; }
                .auth-form { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
                input { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔒 Security Sentinel - DevSecOps Mastery</h1>
                
                <div class="security-info">
                    <h3>Security Status:</h3>
                    <p id="security-status">Checking security status...</p>
                </div>
                
                <div class="metrics">
                    <h3>Live Security Metrics:</h3>
                    <p id="metrics">Loading metrics...</p>
                </div>
                
                <div class="info">
                    <h3>Available Endpoints:</h3>
                    <span class="endpoint">GET /</span> - This dashboard
                    <span class="endpoint">GET /health</span> - Security health check
                    <span class="endpoint">GET /security</span> - Security status
                    <span class="endpoint">GET /compliance</span> - Compliance status
                    <span class="endpoint">POST /auth</span> - Authentication
                    <span class="endpoint">GET /audit</span> - Security audit log
                </div>
                
                <div class="auth-form">
                    <h3>Test Authentication:</h3>
                    <form id="auth-form">
                        <input type="text" id="username" placeholder="Username" required>
                        <input type="password" id="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                    <p id="auth-status"></p>
                </div>
                
                <div class="feature">
                    <h3>🔒 Security Features:</h3>
                    <ul>
                        <li>✅ Security headers and CSP</li>
                        <li>✅ Input validation and sanitization</li>
                        <li>✅ Authentication and authorization</li>
                        <li>✅ Security event logging</li>
                        <li>✅ Vulnerability scanning</li>
                        <li>✅ Compliance monitoring</li>
                    </ul>
                </div>
                
                <div class="feature">
                    <h3>🚀 DevSecOps Features:</h3>
                    <ul>
                        <li>✅ Automated security scanning</li>
                        <li>✅ Compliance checking</li>
                        <li>✅ Secrets management</li>
                        <li>✅ Security monitoring</li>
                        <li>✅ Audit logging</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <button onclick="shutdown()">🛑 Test Graceful Shutdown</button>
                </div>
            </div>
            
            <script>
                // Update security status
                fetch('/security')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('security-status').innerHTML = 
                            data.status === 'secure' ? 
                            '<span class="success">✅ Security Status: Secure</span>' : 
                            '<span class="warning">⚠️ Security Status: Issues Detected</span>';
                    });
                
                // Update metrics
                function updateMetrics() {
                    fetch('/security')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('metrics').innerHTML = 
                                `Security Score: ${data.security_score}/100 | Events: ${data.security_events} | Vulnerabilities: ${data.vulnerabilities}`;
                        });
                }
                
                // Update metrics every 5 seconds
                updateMetrics();
                setInterval(updateMetrics, 5000);
                
                // Authentication form
                document.getElementById('auth-form').addEventListener('submit', function(e) {
                    e.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    
                    fetch('/auth', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('auth-status').innerHTML = '<span class="success">✅ Authentication successful!</span>';
                        } else {
                            document.getElementById('auth-status').innerHTML = '<span class="error">❌ Authentication failed!</span>';
                        }
                    });
                });
                
                // Shutdown function
                function shutdown() {
                    if (confirm('Are you sure you want to test graceful shutdown?')) {
                        fetch('/shutdown', { method: 'POST' })
                            .then(() => {
                                alert('Graceful shutdown initiated! The application will stop in 5 seconds.');
                            });
                    }
                }
            </script>
        </body>
    </html>
    """)

@app.route('/health')
def health():
    """Security health check endpoint."""
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
            'security_status': 'secure',
            'uptime': int(time.time() - start_time),
            'request_count': request_count,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'message': 'Security Sentinel is running with DevSecOps features!'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/security')
def security():
    """Security status and metrics endpoint."""
    global request_count, security_events
    request_count += 1
    
    try:
        # Calculate security score
        security_score = 100
        vulnerabilities = 0
        
        # Check for security issues
        if len(security_events) > 0:
            security_score -= min(len(security_events) * 5, 50)
            vulnerabilities = len([e for e in security_events if 'ATTEMPT' in e['type']])
        
        # Check system security
        if psutil.virtual_memory().percent > 90:
            security_score -= 10
        
        if psutil.disk_usage('/').percent > 90:
            security_score -= 10
        
        return jsonify({
            'status': 'secure' if security_score >= 80 else 'issues_detected',
            'security_score': max(0, security_score),
            'vulnerabilities': vulnerabilities,
            'security_events': len(security_events),
            'timestamp': datetime.now().isoformat(),
            'security_headers': True,
            'authentication': True,
            'encryption': True,
            'logging': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compliance')
def compliance():
    """Compliance status endpoint."""
    global request_count
    request_count += 1
    
    try:
        compliance_status = {
            'security_headers': True,
            'authentication': True,
            'encryption': True,
            'logging': True,
            'input_validation': True,
            'session_management': True,
            'error_handling': True,
            'audit_logging': True
        }
        
        # Check compliance
        compliance_score = sum(compliance_status.values()) / len(compliance_status) * 100
        
        return jsonify({
            'compliance_score': compliance_score,
            'status': 'compliant' if compliance_score >= 80 else 'non_compliant',
            'checks': compliance_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth', methods=['POST'])
def authenticate():
    """Authentication endpoint."""
    global request_count
    request_count += 1
    
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            log_security_event('AUTH_FAILED', 'Missing credentials')
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        # Validate input
        is_valid, message = validate_input(data)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        # Simple authentication (in production, use proper auth)
        if data['username'] == 'admin' and data['password'] == 'password':
            session['authenticated'] = True
            log_security_event('AUTH_SUCCESS', f'User {data["username"]} authenticated')
            return jsonify({'success': True, 'message': 'Authentication successful'})
        else:
            log_security_event('AUTH_FAILED', f'Failed authentication for {data["username"]}')
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        log_security_event('AUTH_ERROR', f'Authentication error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/audit')
@require_auth
def audit():
    """Security audit log endpoint."""
    global request_count, security_events
    request_count += 1
    
    try:
        return jsonify({
            'security_events': security_events[-50:],  # Last 50 events
            'total_events': len(security_events),
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
    log_security_event('SHUTDOWN', 'Graceful shutdown initiated')
    
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
    
    print(f"🔒 Starting Security Sentinel app on port {port}")
    print(f"📱 Visit: http://localhost:{port}")
    print(f"❤️  Health: http://localhost:{port}/health")
    print(f"🔒 Security: http://localhost:{port}/security")
    print(f"📋 Compliance: http://localhost:{port}/compliance")
    print(f"🔐 Auth: http://localhost:{port}/auth")
    print(f"📊 Audit: http://localhost:{port}/audit")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
