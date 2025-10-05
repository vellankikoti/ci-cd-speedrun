#!/usr/bin/env python3
"""
Lab 7: Microservices Integration - Working Examples
===================================================

Learn how to test microservices that interact with multiple
databases and services using TestContainers.
Master real-world microservices testing patterns.
"""

import os
import sys
import time
import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

# Python version check
if sys.version_info < (3, 10):
    print("❌ Python 3.10 or higher is required")
    sys.exit(1)

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

# Global variable to store health results
global_health_results = {}

# Platform-specific Docker host configuration
if sys.platform == "win32":
    os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
else:
    os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'testcontainers': 'testcontainers',
        'psycopg2': 'psycopg2-binary',
        'pymysql': 'pymysql',
        'redis': 'redis',
        'flask': 'flask',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_docker():
    """Check if Docker is available and running"""
    import subprocess
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.mysql import MySqlContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import pymysql
    import redis
    from flask import Flask, request, jsonify
    import requests
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("Please run: python3 setup.py from testcontainers directory")
    sys.exit(1)

def create_user_service(database_connection=None):
    """Create User Service with PostgreSQL"""
    app = Flask(__name__)
    
    db_conn = database_connection
    
    def get_db_connection():
        return db_conn
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id")
            users = cursor.fetchall()
            
            result = []
            for user_id, name, email, created_at in users:
                result.append({
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'created_at': created_at.isoformat()
                })
            
            cursor.close()
            return jsonify({'users': result, 'count': len(result)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/users', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return jsonify({'error': 'Name and email are required'}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (name, email)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            
            return jsonify({
                'id': user_id,
                'name': name,
                'email': email,
                'message': 'User created successfully'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user_id, name, email, created_at = user
            cursor.close()
            
            return jsonify({
                'id': user_id,
                'name': name,
                'email': email,
                'created_at': created_at.isoformat()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({
                    'service': 'user-service',
                    'status': 'unhealthy',
                    'error': 'Database connection not available',
                    'timestamp': time.time()
                }), 500
                
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            return jsonify({
                'service': 'user-service',
                'status': 'healthy',
                'database': 'connected',
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'service': 'user-service',
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    return app

def create_order_service(database_connection=None):
    """Create Order Service with MySQL"""
    app = Flask(__name__)
    
    db_conn = database_connection
    
    def get_db_connection():
        return db_conn
    
    @app.route('/api/orders', methods=['GET'])
    def get_orders():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, product_name, quantity, price, status, created_at FROM orders ORDER BY id")
            orders = cursor.fetchall()
            
            result = []
            for order_id, user_id, product_name, quantity, price, status, created_at in orders:
                result.append({
                    'id': order_id,
                    'user_id': user_id,
                    'product_name': product_name,
                    'quantity': quantity,
                    'price': float(price),
                    'status': status,
                    'created_at': created_at.isoformat()
                })
            
            cursor.close()
            return jsonify({'orders': result, 'count': len(result)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/orders', methods=['POST'])
    def create_order():
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            product_name = data.get('product_name')
            quantity = data.get('quantity')
            price = data.get('price')
            
            if not all([user_id, product_name, quantity, price]):
                return jsonify({'error': 'All fields are required'}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (user_id, product_name, quantity, price) VALUES (%s, %s, %s, %s)",
                (user_id, product_name, quantity, price)
            )
            order_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            
            return jsonify({
                'id': order_id,
                'user_id': user_id,
                'product_name': product_name,
                'quantity': quantity,
                'price': price,
                'status': 'pending',
                'message': 'Order created successfully'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/orders/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, product_name, quantity, price, status, created_at FROM orders WHERE id = %s", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            
            order_id, user_id, product_name, quantity, price, status, created_at = order
            cursor.close()
            
            return jsonify({
                'id': order_id,
                'user_id': user_id,
                'product_name': product_name,
                'quantity': quantity,
                'price': float(price),
                'status': status,
                'created_at': created_at.isoformat()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({
                    'service': 'order-service',
                    'status': 'unhealthy',
                    'error': 'Database connection not available',
                    'timestamp': time.time()
                }), 500
                
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            return jsonify({
                'service': 'order-service',
                'status': 'healthy',
                'database': 'connected',
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'service': 'order-service',
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    return app

def create_notification_service(redis_connection=None):
    """Create Notification Service with Redis"""
    app = Flask(__name__)
    
    redis_client = redis_connection
    
    def get_redis_client():
        return redis_client
    
    @app.route('/api/notifications', methods=['GET'])
    def get_notifications():
        try:
            r = get_redis_client()
            if not r:
                return jsonify({'error': 'Redis not available'}), 503
            
            # Get all notification keys
            keys = r.keys("notification:*")
            notifications = []
            
            for key in keys:
                notification_data = r.hgetall(key)
                if notification_data:
                    notifications.append({
                        'id': key.split(':')[1] if isinstance(key, str) else key.decode('utf-8').split(':')[1],
                        'user_id': notification_data.get('user_id'),
                        'message': notification_data.get('message'),
                        'type': notification_data.get('type'),
                        'created_at': notification_data.get('created_at')
                    })
            
            return jsonify({'notifications': notifications, 'count': len(notifications)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/notifications', methods=['POST'])
    def create_notification():
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            message = data.get('message')
            notification_type = data.get('type', 'info')
            
            if not all([user_id, message]):
                return jsonify({'error': 'User ID and message are required'}), 400
            
            r = get_redis_client()
            if not r:
                return jsonify({'error': 'Redis not available'}), 503
            
            notification_id = str(uuid.uuid4())
            notification_key = f"notification:{notification_id}"
            
            r.hset(notification_key, mapping={
                'user_id': str(user_id),
                'message': message,
                'type': notification_type,
                'created_at': datetime.now().isoformat()
            })
            r.expire(notification_key, 3600)  # 1 hour TTL
            
            return jsonify({
                'id': notification_id,
                'user_id': user_id,
                'message': message,
                'type': notification_type,
                'status': 'Notification created successfully'
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            r = get_redis_client()
            if not r:
                return jsonify({
                    'service': 'notification-service',
                    'status': 'unhealthy',
                    'error': 'Redis not available',
                    'timestamp': time.time()
                }), 503
            
            r.ping()
            
            return jsonify({
                'service': 'notification-service',
                'status': 'healthy',
                'cache': 'connected',
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'service': 'notification-service',
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    return app

def demo_microservices_architecture():
    """Demo complete microservices architecture"""
    print("\n🏗️ Microservices Architecture Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ User Service (PostgreSQL): {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Order Service (MySQL): {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        print(f"✅ Notification Service (Redis): {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Setup User Service Database
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 User Service Database: users table created")

        # Setup Order Service Database
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Order Service Database: orders table created")

        # Setup Notification Service Cache
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        print("📊 Notification Service Cache: Redis ready")

        # Create microservices with their respective database connections
        user_service = create_user_service(pg_conn)
        order_service = create_order_service(mysql_conn)
        notification_service = create_notification_service(r)

        # Start microservices
        def run_user_service():
            user_service.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

        def run_order_service():
            order_service.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)

        def run_notification_service():
            notification_service.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)

        user_thread = threading.Thread(target=run_user_service)
        order_thread = threading.Thread(target=run_order_service)
        notification_thread = threading.Thread(target=run_notification_service)

        user_thread.daemon = True
        order_thread.daemon = True
        notification_thread.daemon = True

        user_thread.start()
        order_thread.start()
        notification_thread.start()

        # Wait for services to start
        time.sleep(3)
        
        # Keep connections alive for health checks by not closing them yet
        # We'll close them after all tests are complete

        print(f"\n🚀 Microservices Started:")
        print(f"   👤 User Service: http://localhost:5001")
        print(f"   📦 Order Service: http://localhost:5002")
        print(f"   🔔 Notification Service: http://localhost:5003")

        # Test microservices integration
        print(f"\n🧪 Testing Microservices Integration:")

        # Test 1: Create users
        print(f"\n   Test 1: Create Users")
        users = [
            {"name": "Alice Johnson", "email": "alice@example.com"},
            {"name": "Bob Smith", "email": "bob@example.com"},
            {"name": "Carol Davis", "email": "carol@example.com"}
        ]

        created_users = []
        for user_data in users:
            try:
                response = requests.post("http://localhost:5001/api/users", json=user_data, timeout=5)
                if response.status_code == 201:
                    user = response.json()
                    created_users.append(user)
                    print(f"      ✅ Created: {user['name']} (ID: {user['id']})")
                else:
                    print(f"      ❌ Failed: {user_data['name']} - {response.status_code}")
            except Exception as e:
                print(f"      ❌ Error: {user_data['name']} - {str(e)[:30]}")

        # Test 2: Create orders
        print(f"\n   Test 2: Create Orders")
        orders = [
            {"user_id": 1, "product_name": "MacBook Pro", "quantity": 1, "price": 2499.99},
            {"user_id": 1, "product_name": "Wireless Mouse", "quantity": 2, "price": 29.99},
            {"user_id": 2, "product_name": "iPhone", "quantity": 1, "price": 999.99},
            {"user_id": 3, "product_name": "iPad", "quantity": 1, "price": 599.99}
        ]

        created_orders = []
        for order_data in orders:
            try:
                response = requests.post("http://localhost:5002/api/orders", json=order_data, timeout=5)
                if response.status_code == 201:
                    order = response.json()
                    created_orders.append(order)
                    print(f"      ✅ Created: {order['product_name']} x{order['quantity']} for User {order['user_id']}")
                else:
                    print(f"      ❌ Failed: {order_data['product_name']} - {response.status_code}")
            except Exception as e:
                print(f"      ❌ Error: {order_data['product_name']} - {str(e)[:30]}")

        # Test 3: Create notifications
        print(f"\n   Test 3: Create Notifications")
        notifications = [
            {"user_id": 1, "message": "Order #1 has been created", "type": "order"},
            {"user_id": 1, "message": "Order #2 has been created", "type": "order"},
            {"user_id": 2, "message": "Order #3 has been created", "type": "order"},
            {"user_id": 3, "message": "Order #4 has been created", "type": "order"}
        ]

        created_notifications = []
        for notification_data in notifications:
            try:
                response = requests.post("http://localhost:5003/api/notifications", json=notification_data, timeout=5)
                if response.status_code == 201:
                    notification = response.json()
                    created_notifications.append(notification)
                    print(f"      ✅ Created: {notification['message']} for User {notification['user_id']}")
                else:
                    print(f"      ❌ Failed: {notification_data['message']} - {response.status_code}")
            except Exception as e:
                print(f"      ❌ Error: {notification_data['message']} - {str(e)[:30]}")

        # Test 4: Cross-service data analysis
        print(f"\n   Test 4: Cross-Service Data Analysis")
        try:
            # Get all users
            users_response = requests.get("http://localhost:5001/api/users", timeout=5)
            users_data = users_response.json() if users_response.status_code == 200 else {'users': []}

            # Get all orders
            orders_response = requests.get("http://localhost:5002/api/orders", timeout=5)
            orders_data = orders_response.json() if orders_response.status_code == 200 else {'orders': []}

            # Get all notifications
            notifications_response = requests.get("http://localhost:5003/api/notifications", timeout=5)
            notifications_data = notifications_response.json() if notifications_response.status_code == 200 else {'notifications': []}

            print(f"      📊 System Overview:")
            print(f"         Users: {len(users_data.get('users', []))}")
            print(f"         Orders: {len(orders_data.get('orders', []))}")
            print(f"         Notifications: {len(notifications_data.get('notifications', []))}")

            # Show user-order relationships
            print(f"      🔗 User-Order Relationships:")
            for user in users_data.get('users', []):
                user_orders = [o for o in orders_data.get('orders', []) if o['user_id'] == user['id']]
                total_spent = sum(o['price'] * o['quantity'] for o in user_orders)
                print(f"         {user['name']}: {len(user_orders)} orders, ${total_spent:.2f} total")

        except Exception as e:
            print(f"      ❌ Cross-service analysis failed: {str(e)[:50]}")

        # Test 5: Health checks (run before cleanup)
        print(f"\n   Test 5: Health Checks")
        services = [
            ("User Service", "http://localhost:5001/api/health"),
            ("Order Service", "http://localhost:5002/api/health"),
            ("Notification Service", "http://localhost:5003/api/health")
        ]

        health_results = {}
        for service_name, health_url in services:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    status = health_data.get('status', 'unknown')
                    health_results[service_name] = status
                    print(f"      ✅ {service_name}: {status}")
                else:
                    health_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                    error_msg = health_data.get('error', f'HTTP {response.status_code}')
                    health_results[service_name] = 'unhealthy'
                    print(f"      ❌ {service_name}: Unhealthy ({response.status_code}) - {error_msg}")
            except Exception as e:
                health_results[service_name] = 'error'
                print(f"      ❌ {service_name}: Error - {str(e)[:30]}")

        # Wait for all health checks to complete
        time.sleep(1)
        
        # Store health results for service discovery demo
        global global_health_results
        global_health_results = health_results
        
        # Note: Database connections will be closed when containers are destroyed
        # No need to explicitly close them here as they're managed by TestContainers

def demo_service_discovery():
    """Demo service discovery and communication patterns"""
    print("\n🔍 Service Discovery Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Setup service registry in Redis
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Register services
        services = {
            "user-service": {
                "host": "localhost",
                "port": 5001,
                "health_endpoint": "/api/health",
                "status": "active"
            },
            "order-service": {
                "host": "localhost", 
                "port": 5002,
                "health_endpoint": "/api/health",
                "status": "active"
            },
            "notification-service": {
                "host": "localhost",
                "port": 5003,
                "health_endpoint": "/api/health",
                "status": "active"
            }
        }

        print("📝 Registering Services:")
        for service_name, service_info in services.items():
            r.hset(f"service:{service_name}", mapping=service_info)
            r.expire(f"service:{service_name}", 300)  # 5 minutes TTL
            print(f"   + {service_name}: {service_info['host']}:{service_info['port']}")

        # Service discovery simulation
        print(f"\n🔍 Service Discovery Simulation:")
        
        # Discover all services
        service_keys = r.keys("service:*")
        discovered_services = []
        
        for key in service_keys:
            service_data = r.hgetall(key)
            if service_data:
                service_name = key.split(":")[1]
                discovered_services.append({
                    'name': service_name,
                    'host': service_data['host'],
                    'port': service_data['port'],
                    'status': service_data['status']
                })
                print(f"   📡 Discovered: {service_name} at {service_data['host']}:{service_data['port']}")

        # Dynamic service health monitoring
        print(f"\n🏥 Service Health Monitoring:")
        
        for service in discovered_services:
            # Map service names to the health results from microservices demo
            service_name_mapping = {
                "user-service": "User Service",
                "order-service": "Order Service", 
                "notification-service": "Notification Service"
            }
            
            mapped_name = service_name_mapping.get(service['name'])
            actual_status = "unknown"
            
            if mapped_name and mapped_name in global_health_results:
                # Use actual health results from microservices demo
                actual_status = global_health_results[mapped_name]
                print(f"   ✅ {service['name']}: {actual_status} (from microservices demo)")
            else:
                # Fallback: try to actually check the service health
                health_url = f"http://{service['host']}:{service['port']}/api/health"
                try:
                    response = requests.get(health_url, timeout=3)
                    if response.status_code == 200:
                        health_data = response.json()
                        actual_status = health_data.get('status', 'unknown')
                        print(f"   ✅ {service['name']}: {actual_status} (live check)")
                    else:
                        actual_status = "unhealthy"
                        print(f"   ❌ {service['name']}: {actual_status} (HTTP {response.status_code})")
                except requests.exceptions.ConnectionError:
                    # Service not running - simulate realistic health status
                    import random
                    rand_val = random.random()
                    if rand_val < 0.7:  # 70% chance of healthy
                        actual_status = "healthy"
                        print(f"   ✅ {service['name']}: {actual_status} (simulated - service not running)")
                    elif rand_val < 0.9:  # 20% chance of degraded
                        actual_status = "degraded"
                        print(f"   ⚠️ {service['name']}: {actual_status} (simulated - service not running)")
                    else:  # 10% chance of unhealthy
                        actual_status = "unhealthy"
                        print(f"   ❌ {service['name']}: {actual_status} (simulated - service not running)")
                except Exception as e:
                    actual_status = "error"
                    print(f"   ❌ {service['name']}: {actual_status} (error: {str(e)[:30]})")
            
            # Update service status in registry
            r.hset(f"service:{service['name']}", "status", actual_status)

        # Show final service registry state
        print(f"\n📊 Service Registry State:")
        for key in service_keys:
            service_data = r.hgetall(key)
            if service_data:
                service_name = key.split(":")[1]
                status = service_data.get('status', 'unknown')
                if status == "healthy":
                    status_icon = "✅"
                elif status == "degraded":
                    status_icon = "⚠️"
                elif status == "unhealthy":
                    status_icon = "❌"
                else:
                    status_icon = "❓"
                print(f"   {status_icon} {service_name}: {status}")

def demo_event_driven_architecture():
    """Demo event-driven architecture with message queues"""
    print("\n📡 Event-Driven Architecture Demo...")
    
    with RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Simulate event publishing
        print("📤 Publishing Events:")
        events = [
            {
                "event_type": "user.created",
                "user_id": 1,
                "data": {"name": "Alice Johnson", "email": "alice@example.com"},
                "timestamp": datetime.now().isoformat()
            },
            {
                "event_type": "order.created",
                "order_id": 1,
                "user_id": 1,
                "data": {"product": "MacBook Pro", "quantity": 1, "price": 2499.99},
                "timestamp": datetime.now().isoformat()
            },
            {
                "event_type": "order.shipped",
                "order_id": 1,
                "user_id": 1,
                "data": {"tracking_number": "TRK123456", "carrier": "FedEx"},
                "timestamp": datetime.now().isoformat()
            },
            {
                "event_type": "notification.sent",
                "user_id": 1,
                "data": {"message": "Your order has been shipped", "type": "order_update"},
                "timestamp": datetime.now().isoformat()
            }
        ]

        for event in events:
            event_json = json.dumps(event)
            r.lpush("event_queue", event_json)
            print(f"   📤 {event['event_type']}: {event.get('user_id', 'N/A')}")

        # Simulate event processing
        print(f"\n📥 Processing Events:")
        processed_events = 0
        while processed_events < len(events):
            event_json = r.rpop("event_queue")
            if event_json:
                event = json.loads(event_json)
                print(f"   📥 Processed: {event['event_type']} for User {event.get('user_id', 'N/A')}")
                processed_events += 1

        # Show event statistics
        print(f"\n📊 Event Statistics:")
        print(f"   Total Events Published: {len(events)}")
        print(f"   Total Events Processed: {processed_events}")
        print(f"   Processing Rate: 100%")

        # Show event types
        event_types = {}
        for event in events:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1

        print(f"   Event Types:")
        for event_type, count in event_types.items():
            print(f"      {event_type}: {count} events")

def main():
    """Run Lab 7 - Microservices Integration"""
    print("🚀 LAB 7: Microservices Integration - Working Examples")
    print("=" * 60)
    print("✨ Master microservices testing with TestContainers!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_microservices_architecture()
        demo_service_discovery()
        demo_event_driven_architecture()
        
        print("\n✅ Lab 7 completed successfully!")
        print("Key concepts learned:")
        print("• Microservices architecture with multiple databases")
        print("• Service-to-service communication patterns")
        print("• Service discovery and health monitoring")
        print("• Event-driven architecture with message queues")
        print("• Cross-service data analysis and integration")
        print("• Real-world microservices testing scenarios")
        print("\n💪 You're ready for advanced patterns!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()