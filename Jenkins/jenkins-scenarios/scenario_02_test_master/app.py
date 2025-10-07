#!/usr/bin/env python3
"""
Test Master - Flask Application with Database Integration
A Flask app that demonstrates TestContainers integration with real databases.
"""

from flask import Flask, request, jsonify, render_template_string
import os
import sys
from datetime import datetime
import json

# Import database module
from database import DatabaseManager, User

app = Flask(__name__)

# Initialize database manager
db_manager = DatabaseManager()

@app.route('/')
def home():
    """Welcome page with database status and user management."""
    return render_template_string("""
    <html>
        <head>
            <title>Test Master - Database Integration Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #3498db; color: white; padding: 5px 10px; border-radius: 3px; margin: 5px; display: inline-block; }
                .success { color: #27ae60; font-weight: bold; }
                .error { color: #e74c3c; font-weight: bold; }
                .user-form { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .user-list { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }
                input, button { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; }
                button { background: #3498db; color: white; cursor: pointer; }
                button:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧪 Test Master - Database Integration Demo</h1>
                
                <div class="info">
                    <h3>Database Status:</h3>
                    <p id="db-status">Checking database connection...</p>
                </div>
                
                <div class="info">
                    <h3>Available Endpoints:</h3>
                    <span class="endpoint">GET /</span> - This dashboard
                    <span class="endpoint">GET /health</span> - Health check
                    <span class="endpoint">GET /users</span> - List users
                    <span class="endpoint">POST /users</span> - Create user
                    <span class="endpoint">GET /users/{id}</span> - Get user
                    <span class="endpoint">PUT /users/{id}</span> - Update user
                    <span class="endpoint">DELETE /users/{id}</span> - Delete user
                </div>
                
                <div class="user-form">
                    <h3>Add New User:</h3>
                    <form id="user-form">
                        <input type="text" id="name" placeholder="Name" required>
                        <input type="email" id="email" placeholder="Email" required>
                        <button type="submit">Add User</button>
                    </form>
                </div>
                
                <div class="user-list">
                    <h3>Users:</h3>
                    <div id="users-list">Loading users...</div>
                </div>
                
                <div class="info">
                    <h3>What You've Learned:</h3>
                    <ul>
                        <li>✅ TestContainers integration</li>
                        <li>✅ Real database testing</li>
                        <li>✅ Parallel test execution</li>
                        <li>✅ Integration testing patterns</li>
                    </ul>
                </div>
            </div>
            
            <script>
                // Check database status
                fetch('/health')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('db-status').innerHTML = 
                            data.database_status === 'connected' ? 
                            '<span class="success">✅ Database Connected</span>' : 
                            '<span class="error">❌ Database Disconnected</span>';
                    });
                
                // Load users
                function loadUsers() {
                    fetch('/users')
                        .then(response => response.json())
                        .then(data => {
                            const usersList = document.getElementById('users-list');
                            if (data.users && data.users.length > 0) {
                                usersList.innerHTML = data.users.map(user => 
                                    `<div>${user.name} (${user.email}) - <button onclick="deleteUser(${user.id})">Delete</button></div>`
                                ).join('');
                            } else {
                                usersList.innerHTML = 'No users found. Add some users above!';
                            }
                        });
                }
                
                // Add user
                document.getElementById('user-form').addEventListener('submit', function(e) {
                    e.preventDefault();
                    const name = document.getElementById('name').value;
                    const email = document.getElementById('email').value;
                    
                    fetch('/users', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, email })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('name').value = '';
                            document.getElementById('email').value = '';
                            loadUsers();
                        }
                    });
                });
                
                // Delete user
                function deleteUser(id) {
                    fetch(`/users/${id}`, { method: 'DELETE' })
                        .then(() => loadUsers());
                }
                
                // Load users on page load
                loadUsers();
            </script>
        </body>
    </html>
    """)

@app.route('/health')
def health():
    """Health check endpoint with database status."""
    try:
        # Test database connection
        db_status = "connected" if db_manager.test_connection() else "disconnected"
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database_status': db_status,
            'message': 'Test Master app is running with database integration!'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'database_status': 'error',
            'error': str(e)
        }), 500

@app.route('/users', methods=['GET', 'POST'])
def users():
    """Handle user operations."""
    if request.method == 'GET':
        try:
            users = db_manager.get_all_users()
            return jsonify({
                'success': True,
                'users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in users],
                'count': len(users)
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'name' not in data or 'email' not in data:
                return jsonify({'success': False, 'error': 'Name and email are required'}), 400
            
            user = db_manager.create_user(data['name'], data['email'])
            return jsonify({
                'success': True,
                'user': {'id': user.id, 'name': user.name, 'email': user.email}
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_operations(user_id):
    """Handle individual user operations."""
    try:
        if request.method == 'GET':
            user = db_manager.get_user(user_id)
            if user:
                return jsonify({
                    'success': True,
                    'user': {'id': user.id, 'name': user.name, 'email': user.email}
                })
            else:
                return jsonify({'success': False, 'error': 'User not found'}), 404
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            user = db_manager.update_user(user_id, data.get('name'), data.get('email'))
            if user:
                return jsonify({
                    'success': True,
                    'user': {'id': user.id, 'name': user.name, 'email': user.email}
                })
            else:
                return jsonify({'success': False, 'error': 'User not found'}), 404
        
        elif request.method == 'DELETE':
            success = db_manager.delete_user(user_id)
            if success:
                return jsonify({'success': True, 'message': 'User deleted'})
            else:
                return jsonify({'success': False, 'error': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('ENVIRONMENT', 'development') == 'development'
    
    print(f"🧪 Starting Test Master app on port {port}")
    print(f"📱 Visit: http://localhost:{port}")
    print(f"❤️  Health: http://localhost:{port}/health")
    print(f"👥 Users: http://localhost:{port}/users")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
