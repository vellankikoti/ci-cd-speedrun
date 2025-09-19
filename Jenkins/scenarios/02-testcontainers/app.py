#!/usr/bin/env python3
"""
TestContainers Integration Demo Application
A simple HTTP server that demonstrates container integration testing patterns
"""

import os
import json
import time
import http.server
import socketserver
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import sqlite3
import threading

# Application metadata
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
BUILD_TIME = os.getenv('BUILD_TIME', datetime.now().isoformat())
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Database configuration (simulated with SQLite for demo)
DB_PATH = os.getenv('DB_PATH', '/tmp/testcontainers_demo.db')

class DatabaseManager:
    """Simple database manager using SQLite for demonstration"""

    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()

    def init_database(self):
        """Initialize database with test table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create sample data if table is empty
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                sample_users = [
                    ('John Doe', 'john@example.com'),
                    ('Jane Smith', 'jane@example.com'),
                    ('Bob Johnson', 'bob@example.com')
                ]
                for name, email in sample_users:
                    cursor.execute(
                        "INSERT INTO users (name, email) VALUES (?, ?)",
                        (name, email)
                    )

            conn.commit()
            conn.close()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")

    def get_connection(self):
        """Get database connection"""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None

    def get_users(self):
        """Get all users"""
        conn = self.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at")
            users = [
                {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'created_at': row[3]
                }
                for row in cursor.fetchall()
            ]
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            conn.close()

    def create_user(self, name, email):
        """Create a new user"""
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            user_id = cursor.lastrowid
            conn.commit()

            # Return the created user
            cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3]
            }
        except sqlite3.IntegrityError:
            return {'error': 'Email already exists'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()

    def health_check(self):
        """Check database health"""
        conn = self.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception:
            return False
        finally:
            conn.close()

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

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TestContainers Integration Demo</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; }}
        .status {{ padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        .healthy {{ background: #4CAF50; color: white; }}
        .error {{ background: #f44336; color: white; }}
        .info-card {{ background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .btn {{ background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }}
        .btn:hover {{ background: #45a049; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 TestContainers Integration Demo</h1>

        <div class="info-card">
            <h3>Application Status <span class="status {status_class}">{status_text}</span></h3>
            <p>This application demonstrates TestContainers integration concepts:</p>
            <ul>
                <li>✅ HTTP server with database integration</li>
                <li>✅ SQLite database simulation</li>
                <li>✅ Health checks and monitoring</li>
                <li>✅ RESTful API endpoints</li>
                <li>✅ Integration testing patterns</li>
            </ul>
        </div>

        <div class="info-card">
            <h3>Build Information</h3>
            <p><strong>Version:</strong> {APP_VERSION}</p>
            <p><strong>Build Time:</strong> {BUILD_TIME}</p>
            <p><strong>Environment:</strong> {ENVIRONMENT}</p>
            <p><strong>Database Status:</strong> {'Connected' if db_healthy else 'Disconnected'}</p>
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
            <a href="/api/info" class="btn">App Info</a>
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
            'database_type': 'SQLite',
            'database_path': DB_PATH,
            'user_count': user_count,
            'timestamp': datetime.now().isoformat()
        }

        status_code = 200 if db_healthy else 503
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

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

def create_handler_with_db(db_manager):
    """Create a handler class with database manager"""
    def handler(*args, **kwargs):
        return TestContainersHTTPHandler(*args, db_manager=db_manager, **kwargs)
    return handler

def start_server(port=5000):
    """Start the HTTP server"""
    db_manager = DatabaseManager()
    handler_class = create_handler_with_db(db_manager)

    with socketserver.TCPServer(("", port), handler_class) as httpd:
        print(f"🚀 Starting TestContainers Integration Demo")
        print(f"📦 Version: {APP_VERSION}")
        print(f"🌍 Environment: {ENVIRONMENT}")
        print(f"🗄️ Database: SQLite at {DB_PATH}")
        print(f"🌐 Server running on port {port}")
        print(f"🔗 Open http://localhost:{port} to view the application")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    start_server(port)