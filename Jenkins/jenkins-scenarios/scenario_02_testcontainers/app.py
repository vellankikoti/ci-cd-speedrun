#!/usr/bin/env python3
"""
TestContainers Integration Demo Application
A real HTTP server with PostgreSQL database integration using TestContainers
"""

import os
import json
import time
import http.server
import socketserver
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import threading
import logging

# Import our PostgreSQL database manager
from database import PostgreSQLDatabaseManager, TestContainersDatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application metadata
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
BUILD_TIME = os.getenv('BUILD_TIME', datetime.now().isoformat())
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Database configuration
DB_TYPE = os.getenv('DB_TYPE', 'postgresql')  # postgresql or testcontainers

def create_database_manager():
    """Create appropriate database manager based on environment"""
    if DB_TYPE == 'testcontainers':
        # This will be used when running with TestContainers
        container_host = os.getenv('TESTCONTAINERS_HOST', 'localhost')
        container_port = int(os.getenv('TESTCONTAINERS_PORT', '5432'))
        return TestContainersDatabaseManager(container_host, container_port)
    else:
        # Regular PostgreSQL connection
        return PostgreSQLDatabaseManager()

class TestContainersHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the TestContainers demo"""

    def __init__(self, *args, db_manager=None, **kwargs):
        self.db_manager = db_manager
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self.serve_main_page()
        elif path == '/health':
            self.serve_health()
        elif path == '/api/users':
            self.serve_users()
        elif path == '/api/db-status':
            self.serve_db_status()
        elif path == '/api/db-stats':
            self.serve_db_stats()
        elif path == '/api/info':
            self.serve_info()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/users':
            self.create_user()
        else:
            self.send_error(404, "Not Found")

    def do_PUT(self):
        """Handle PUT requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/users/'):
            user_id = path.split('/')[-1]
            self.update_user(user_id)
        else:
            self.send_error(404, "Not Found")

    def do_DELETE(self):
        """Handle DELETE requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/users/'):
            user_id = path.split('/')[-1]
            self.delete_user(user_id)
        else:
            self.send_error(404, "Not Found")

    def serve_main_page(self):
        """Serve the main page"""
        users = self.db_manager.get_users()
        db_healthy = self.db_manager.health_check()

        users_html = "<ul>"
        for user in users:
            users_html += f"<li><strong>{user['name']}</strong> - {user['email']} <em>(ID: {user['id']})</em></li>"
        users_html += "</ul>"

        status_class = "healthy" if db_healthy else "error"
        status_text = "HEALTHY" if db_healthy else "DB ERROR"

        # Get database stats for display
        db_stats = self.db_manager.get_database_stats()
        db_type = "PostgreSQL" if DB_TYPE == 'postgresql' else "TestContainers PostgreSQL"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TestContainers Integration Demo</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; }}
        .status {{ padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        .healthy {{ background: #4CAF50; color: white; }}
        .error {{ background: #f44336; color: white; }}
        .info-card {{ background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .btn {{ background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }}
        .btn:hover {{ background: #45a049; }}
        .db-info {{ background: #e3f2fd; border-left-color: #2196F3; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; }}
        .stat-item {{ background: white; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2196F3; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 TestContainers Integration Demo</h1>

        <div class="info-card">
            <h3>Application Status <span class="status {status_class}">{status_text}</span></h3>
            <p>This application demonstrates <strong>real TestContainers integration</strong> with PostgreSQL:</p>
            <ul>
                <li>✅ HTTP server with PostgreSQL database integration</li>
                <li>✅ Real TestContainers PostgreSQL container</li>
                <li>✅ Advanced database operations (CRUD, stats, health)</li>
                <li>✅ RESTful API endpoints with full HTTP methods</li>
                <li>✅ Production-ready database patterns</li>
                <li>✅ Integration testing with real database</li>
            </ul>
        </div>

        <div class="info-card db-info">
            <h3>Database Information</h3>
            <p><strong>Database Type:</strong> {db_type}</p>
            <p><strong>Database Status:</strong> {'Connected' if db_healthy else 'Disconnected'}</p>
            <p><strong>Environment:</strong> {ENVIRONMENT}</p>
            {f'<p><strong>Database Size:</strong> {db_stats.get("database_size", "Unknown")}</p>' if 'database_size' in db_stats else ''}
        </div>

        <div class="info-card">
            <h3>Database Statistics</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{len(users)}</div>
                    <div class="stat-label">Total Users</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{db_stats.get('user_count', 0)}</div>
                    <div class="stat-label">Users in DB</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len(db_stats.get('tables', []))}</div>
                    <div class="stat-label">Tables</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{'✅' if db_healthy else '❌'}</div>
                    <div class="stat-label">Health Status</div>
                </div>
            </div>
        </div>

        <div class="info-card">
            <h3>Sample Users in Database</h3>
            {users_html}
        </div>

        <div class="info-card">
            <h3>Test the Application</h3>
            <a href="/health" class="btn">Health Check</a>
            <a href="/api/users" class="btn">Users API</a>
            <a href="/api/db-status" class="btn">DB Status</a>
            <a href="/api/db-stats" class="btn">DB Stats</a>
            <a href="/api/info" class="btn">App Info</a>
        </div>

        <div class="info-card">
            <h3>API Endpoints</h3>
            <p><strong>GET /api/users</strong> - List all users</p>
            <p><strong>POST /api/users</strong> - Create new user</p>
            <p><strong>PUT /api/users/{id}</strong> - Update user</p>
            <p><strong>DELETE /api/users/{id}</strong> - Delete user</p>
            <p><strong>GET /api/db-stats</strong> - Database statistics</p>
        </div>
    </div>
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_health(self):
        """Serve health check endpoint"""
        db_healthy = self.db_manager.health_check()
        status = 'healthy' if db_healthy else 'unhealthy'
        status_code = 200 if db_healthy else 503

        response = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'version': APP_VERSION,
            'environment': ENVIRONMENT,
            'database': 'connected' if db_healthy else 'disconnected'
        }

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def serve_users(self):
        """Serve users API endpoint"""
        users = self.db_manager.get_users()

        response = {
            'users': users,
            'count': len(users),
            'timestamp': datetime.now().isoformat()
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def serve_db_status(self):
        """Serve database status endpoint"""
        db_healthy = self.db_manager.health_check()
        user_count = len(self.db_manager.get_users())

        response = {
            'status': 'connected' if db_healthy else 'disconnected',
            'database_type': 'PostgreSQL',
            'environment': ENVIRONMENT,
            'user_count': user_count,
            'timestamp': datetime.now().isoformat()
        }

        status_code = 200 if db_healthy else 503
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def serve_db_stats(self):
        """Serve database statistics endpoint"""
        try:
            stats = self.db_manager.get_database_stats()
            if 'error' in stats:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(stats).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(stats, indent=2).encode())
        except Exception as e:
            error_response = {'error': str(e), 'timestamp': datetime.now().isoformat()}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

    def serve_info(self):
        """Serve application info endpoint"""
        response = {
            'name': 'TestContainers Integration Demo',
            'version': APP_VERSION,
            'description': 'A simple application demonstrating container integration testing',
            'build_time': BUILD_TIME,
            'environment': ENVIRONMENT,
            'endpoints': [
                '/health',
                '/api/users',
                '/api/db-status',
                '/api/info'
            ]
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def create_user(self):
        """Create a new user"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "Missing request body")
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            if 'name' not in data or 'email' not in data:
                self.send_error(400, "Name and email are required")
                return

            result = self.db_manager.create_user(data['name'], data['email'])

            if 'error' in result:
                self.send_response(409 if 'already exists' in result['error'] else 500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                response = {
                    'user': result,
                    'message': 'User created successfully'
                }
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response, indent=2).encode())

        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))

    def update_user(self, user_id):
        """Update user information"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "Missing request body")
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            # Validate user_id
            try:
                user_id = int(user_id)
            except ValueError:
                self.send_error(400, "Invalid user ID")
                return

            # Update user
            result = self.db_manager.update_user(
                user_id, 
                data.get('name'), 
                data.get('email')
            )

            if 'error' in result:
                status_code = 404 if 'not found' in result['error'] else 400
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                response = {
                    'user': result,
                    'message': 'User updated successfully'
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response, indent=2).encode())

        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, str(e))

    def delete_user(self, user_id):
        """Delete user by ID"""
        try:
            # Validate user_id
            try:
                user_id = int(user_id)
            except ValueError:
                self.send_error(400, "Invalid user ID")
                return

            # Delete user
            result = self.db_manager.delete_user(user_id)

            if 'error' in result:
                status_code = 404 if 'not found' in result['error'] else 500
                self.send_response(status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=2).encode())

        except Exception as e:
            self.send_error(500, str(e))

def create_handler_with_db(db_manager):
    """Create a handler class with database manager"""
    def handler(*args, **kwargs):
        return TestContainersHTTPHandler(*args, db_manager=db_manager, **kwargs)
    return handler

def start_server(port=5000):
    """Start the HTTP server"""
    try:
        # Create database manager
        db_manager = create_database_manager()
        
        # Initialize database
        db_manager.init_database()
        
        # Create handler with database
        handler_class = create_handler_with_db(db_manager)

        with socketserver.TCPServer(("", port), handler_class) as httpd:
            print(f"🚀 Starting TestContainers Integration Demo")
            print(f"📦 Version: {APP_VERSION}")
            print(f"🌍 Environment: {ENVIRONMENT}")
            print(f"🗄️ Database: {DB_TYPE.upper()} PostgreSQL")
            print(f"🌐 Server running on port {port}")
            print(f"🔗 Open http://localhost:{port} to view the application")
            print(f"📊 Database stats: {db_manager.get_database_stats()}")

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Server startup failed: {e}")
        raise
    finally:
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    start_server(port)