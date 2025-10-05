#!/usr/bin/env python3
"""
Lab 6: API Testing - Chaos Scenarios
====================================

Experience API chaos in production environments.
Learn how to handle API failures, timeouts, and real-world issues.
"""

import os
import sys
import json
import time
import random
import threading
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
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
    from flask import Flask, request, jsonify
    import requests
    import uuid
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis flask requests")
    sys.exit(1)

def create_chaos_api():
    """Create an API that simulates real-world chaos"""
    app = Flask(__name__)
    
    # Global variables for chaos simulation
    db_conn = None
    redis_client = None
    chaos_mode = False
    failure_rate = 0.0
    response_delay = 0.0
    
    def get_db_connection():
        return db_conn
    
    def get_redis_client():
        return redis_client
    
    def simulate_chaos():
        """Simulate various chaos scenarios"""
        if not chaos_mode:
            return False
        
        # Simulate random failures
        if random.random() < failure_rate:
            return True
        
        # Simulate response delays
        if response_delay > 0:
            time.sleep(response_delay)
        
        return False
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Get all users with chaos simulation"""
        try:
            if simulate_chaos():
                return jsonify({'error': 'Simulated database timeout'}), 500
            
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
        """Create a new user with chaos simulation"""
        try:
            if simulate_chaos():
                return jsonify({'error': 'Simulated processing failure'}), 500
            
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
    
    @app.route('/api/chaos/configure', methods=['POST'])
    def configure_chaos():
        """Configure chaos parameters"""
        global chaos_mode, failure_rate, response_delay
        
        data = request.get_json()
        chaos_mode = data.get('enabled', False)
        failure_rate = data.get('failure_rate', 0.0)
        response_delay = data.get('response_delay', 0.0)
        
        return jsonify({
            'chaos_mode': chaos_mode,
            'failure_rate': failure_rate,
            'response_delay': response_delay,
            'message': 'Chaos configuration updated'
        })
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check with chaos simulation"""
        try:
            if simulate_chaos():
                return jsonify({
                    'status': 'unhealthy',
                    'error': 'Simulated health check failure',
                    'timestamp': time.time()
                }), 500
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            redis_client = get_redis_client()
            if redis_client:
                redis_client.ping()
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'cache': 'connected' if redis_client else 'not_available',
                'chaos_mode': chaos_mode,
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    return app

def chaos_api_timeouts():
    """API timeout chaos - what happens when APIs are slow?"""
    print("\n💥 API Timeout Chaos...")
    print("🚨 What happens when APIs respond slowly or timeout?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup database
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            cursor = pg_conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Database Table Created: users")

            # Insert test data
            test_users = [
                ("Alice Johnson", "alice@example.com"),
                ("Bob Smith", "bob@example.com"),
                ("Carol Davis", "carol@example.com")
            ]

            print("📝 Creating Test Users:")
            for name, email in test_users:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (name, email)
                )
                print(f"   + {name} ({email})")

            pg_conn.commit()

            # Create chaos API
            app = create_chaos_api()
            app.config['db_conn'] = pg_conn
            app.config['redis_client'] = r
            
            # Set global variables
            import sys
            sys.modules[__name__].db_conn = pg_conn
            sys.modules[__name__].redis_client = r

            # Start API server
            def run_api():
                app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)

            api_thread = threading.Thread(target=run_api)
            api_thread.daemon = True
            api_thread.start()

            # Wait for API to start
            time.sleep(2)

            base_url = "http://localhost:5003"

            # Test timeout scenarios
            print(f"\n🧪 Testing API Timeout Scenarios:")

            # Scenario 1: Normal response
            print(f"\n   Scenario 1: Normal Response")
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}/api/users", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                print(f"      Status: {response.status_code}")
                print(f"      Response Time: {response_time:.2f}ms")
                print(f"      Users Returned: {len(response.json().get('users', []))}")
            except Exception as e:
                print(f"      ❌ Request failed: {str(e)[:50]}")

            # Scenario 2: Simulated slow response
            print(f"\n   Scenario 2: Simulated Slow Response")
            try:
                # Configure chaos for slow response
                chaos_config = {
                    "enabled": True,
                    "failure_rate": 0.0,
                    "response_delay": 2.0  # 2 second delay
                }
                requests.post(f"{base_url}/api/chaos/configure", json=chaos_config, timeout=5)
                
                start_time = time.time()
                response = requests.get(f"{base_url}/api/users", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                print(f"      Status: {response.status_code}")
                print(f"      Response Time: {response_time:.2f}ms (expected ~2000ms)")
            except Exception as e:
                print(f"      ❌ Request failed: {str(e)[:50]}")

            # Scenario 3: Client timeout
            print(f"\n   Scenario 3: Client Timeout")
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}/api/users", timeout=1)  # 1 second timeout
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                print(f"      Status: {response.status_code}")
                print(f"      Response Time: {response_time:.2f}ms")
            except requests.exceptions.Timeout:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                print(f"      ❌ Request timed out after {response_time:.2f}ms")
            except Exception as e:
                print(f"      ❌ Request failed: {str(e)[:50]}")

            # Scenario 4: Disable chaos and test normal response
            print(f"\n   Scenario 4: Disable Chaos")
            try:
                chaos_config = {
                    "enabled": False,
                    "failure_rate": 0.0,
                    "response_delay": 0.0
                }
                requests.post(f"{base_url}/api/chaos/configure", json=chaos_config, timeout=5)
                
                start_time = time.time()
                response = requests.get(f"{base_url}/api/users", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                print(f"      Status: {response.status_code}")
                print(f"      Response Time: {response_time:.2f}ms")
                print(f"      Users Returned: {len(response.json().get('users', []))}")
            except Exception as e:
                print(f"      ❌ Request failed: {str(e)[:50]}")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 API timeout test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Always implement proper timeout handling and retry logic!")

def chaos_api_failures():
    """API failure chaos - what happens when APIs fail?"""
    print("\n💥 API Failure Chaos...")
    print("🚨 What happens when APIs fail randomly or consistently?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup database
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            cursor = pg_conn.cursor()
            cursor.execute("""
                CREATE TABLE products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0
                )
            """)
            print("📊 Database Table Created: products")

            # Insert test products
            products = [
                ("MacBook Pro", 2499.99, 10),
                ("iPhone", 999.99, 25),
                ("iPad", 599.99, 15)
            ]

            print("📝 Creating Test Products:")
            for name, price, stock in products:
                cursor.execute(
                    "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                    (name, price, stock)
                )
                print(f"   + {name}: ${price} (Stock: {stock})")

            pg_conn.commit()

            # Create chaos API
            app = create_chaos_api()
            app.config['db_conn'] = pg_conn
            app.config['redis_client'] = r
            
            # Set global variables
            import sys
            sys.modules[__name__].db_conn = pg_conn
            sys.modules[__name__].redis_client = r

            # Start API server
            def run_api():
                app.run(host='0.0.0.0', port=5004, debug=False, use_reloader=False)

            api_thread = threading.Thread(target=run_api)
            api_thread.daemon = True
            api_thread.start()

            # Wait for API to start
            time.sleep(2)

            base_url = "http://localhost:5004"

            # Test failure scenarios
            print(f"\n🧪 Testing API Failure Scenarios:")

            # Scenario 1: Low failure rate
            print(f"\n   Scenario 1: Low Failure Rate (10%)")
            try:
                chaos_config = {
                    "enabled": True,
                    "failure_rate": 0.1,  # 10% failure rate
                    "response_delay": 0.0
                }
                requests.post(f"{base_url}/api/chaos/configure", json=chaos_config, timeout=5)
                
                success_count = 0
                failure_count = 0
                
                for i in range(10):
                    try:
                        response = requests.get(f"{base_url}/api/users", timeout=5)
                        if response.status_code == 200:
                            success_count += 1
                            print(f"      Request {i+1}: ✅ Success")
                        else:
                            failure_count += 1
                            print(f"      Request {i+1}: ❌ Failed ({response.status_code})")
                    except Exception as e:
                        failure_count += 1
                        print(f"      Request {i+1}: ❌ Exception ({str(e)[:30]})")
                
                print(f"      Results: {success_count} success, {failure_count} failures")
                print(f"      Success Rate: {(success_count/10)*100:.1f}%")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 2: High failure rate
            print(f"\n   Scenario 2: High Failure Rate (50%)")
            try:
                chaos_config = {
                    "enabled": True,
                    "failure_rate": 0.5,  # 50% failure rate
                    "response_delay": 0.0
                }
                requests.post(f"{base_url}/api/chaos/configure", json=chaos_config, timeout=5)
                
                success_count = 0
                failure_count = 0
                
                for i in range(10):
                    try:
                        response = requests.get(f"{base_url}/api/users", timeout=5)
                        if response.status_code == 200:
                            success_count += 1
                            print(f"      Request {i+1}: ✅ Success")
                        else:
                            failure_count += 1
                            print(f"      Request {i+1}: ❌ Failed ({response.status_code})")
                    except Exception as e:
                        failure_count += 1
                        print(f"      Request {i+1}: ❌ Exception ({str(e)[:30]})")
                
                print(f"      Results: {success_count} success, {failure_count} failures")
                print(f"      Success Rate: {(success_count/10)*100:.1f}%")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 3: Database connection failure simulation
            print(f"\n   Scenario 3: Database Connection Failure")
            try:
                # Close database connection to simulate failure
                cursor.close()
                pg_conn.close()
                
                # Try to make requests
                for i in range(3):
                    try:
                        response = requests.get(f"{base_url}/api/users", timeout=5)
                        print(f"      Request {i+1}: Status {response.status_code}")
                        if response.status_code != 200:
                            error_data = response.json()
                            print(f"         Error: {error_data.get('error', 'Unknown error')[:50]}")
                    except Exception as e:
                        print(f"      Request {i+1}: Exception - {str(e)[:50]}")
                
                print(f"      ⚠️  Database connection lost - API should handle gracefully")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 API failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement circuit breakers and graceful degradation!")

def chaos_api_load_issues():
    """API load chaos - what happens under high load?"""
    print("\n💥 API Load Chaos...")
    print("🚨 What happens when APIs are under high load?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup database
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            cursor = pg_conn.cursor()
            cursor.execute("""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    quantity INTEGER NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            print("📊 Database Table Created: orders")

            # Create chaos API
            app = create_chaos_api()
            app.config['db_conn'] = pg_conn
            app.config['redis_client'] = r
            
            # Set global variables
            import sys
            sys.modules[__name__].db_conn = pg_conn
            sys.modules[__name__].redis_client = r

            # Start API server
            def run_api():
                app.run(host='0.0.0.0', port=5005, debug=False, use_reloader=False)

            api_thread = threading.Thread(target=run_api)
            api_thread.daemon = True
            api_thread.start()

            # Wait for API to start
            time.sleep(2)

            base_url = "http://localhost:5005"

            # Test load scenarios
            print(f"\n🧪 Testing API Load Scenarios:")

            # Scenario 1: Normal load
            print(f"\n   Scenario 1: Normal Load (5 concurrent requests)")
            try:
                import concurrent.futures
                
                def make_request(request_id):
                    try:
                        start_time = time.time()
                        response = requests.get(f"{base_url}/api/users", timeout=10)
                        end_time = time.time()
                        return {
                            'id': request_id,
                            'status': response.status_code,
                            'time': (end_time - start_time) * 1000,
                            'success': response.status_code == 200
                        }
                    except Exception as e:
                        return {
                            'id': request_id,
                            'status': 0,
                            'time': 0,
                            'success': False,
                            'error': str(e)[:30]
                        }

                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [executor.submit(make_request, i) for i in range(5)]
                    results = [future.result() for future in concurrent.futures.as_completed(futures)]

                successful_requests = [r for r in results if r['success']]
                failed_requests = [r for r in results if not r['success']]

                print(f"      Successful: {len(successful_requests)}")
                print(f"      Failed: {len(failed_requests)}")
                
                if successful_requests:
                    avg_time = sum(r['time'] for r in successful_requests) / len(successful_requests)
                    print(f"      Average Response Time: {avg_time:.2f}ms")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 2: High load with chaos
            print(f"\n   Scenario 2: High Load with Chaos (20 concurrent requests)")
            try:
                # Enable chaos for high load
                chaos_config = {
                    "enabled": True,
                    "failure_rate": 0.3,  # 30% failure rate
                    "response_delay": 0.5  # 0.5 second delay
                }
                requests.post(f"{base_url}/api/chaos/configure", json=chaos_config, timeout=5)
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    futures = [executor.submit(make_request, i) for i in range(20)]
                    results = [future.result() for future in concurrent.futures.as_completed(futures)]

                successful_requests = [r for r in results if r['success']]
                failed_requests = [r for r in results if not r['success']]

                print(f"      Successful: {len(successful_requests)}")
                print(f"      Failed: {len(failed_requests)}")
                print(f"      Success Rate: {(len(successful_requests)/20)*100:.1f}%")
                
                if successful_requests:
                    avg_time = sum(r['time'] for r in successful_requests) / len(successful_requests)
                    print(f"      Average Response Time: {avg_time:.2f}ms")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 3: Extreme load
            print(f"\n   Scenario 3: Extreme Load (50 concurrent requests)")
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                    futures = [executor.submit(make_request, i) for i in range(50)]
                    results = [future.result() for future in concurrent.futures.as_completed(futures)]

                successful_requests = [r for r in results if r['success']]
                failed_requests = [r for r in results if not r['success']]

                print(f"      Successful: {len(successful_requests)}")
                print(f"      Failed: {len(failed_requests)}")
                print(f"      Success Rate: {(len(successful_requests)/50)*100:.1f}%")
                
                if successful_requests:
                    avg_time = sum(r['time'] for r in successful_requests) / len(successful_requests)
                    print(f"      Average Response Time: {avg_time:.2f}ms")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 API load test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement rate limiting, load balancing, and auto-scaling!")

def chaos_api_data_corruption():
    """API data corruption chaos - what happens when data gets corrupted?"""
    print("\n💥 API Data Corruption Chaos...")
    print("🚨 What happens when data gets corrupted during API operations?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup database
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            cursor = pg_conn.cursor()
            cursor.execute("""
                CREATE TABLE transactions (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    description VARCHAR(200) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Database Table Created: transactions")

            # Insert test data
            test_transactions = [
                (100.00, "Payment for services"),
                (250.50, "Product purchase"),
                (75.25, "Subscription fee")
            ]

            print("📝 Creating Test Transactions:")
            for amount, description in test_transactions:
                cursor.execute(
                    "INSERT INTO transactions (amount, description) VALUES (%s, %s)",
                    (amount, description)
                )
                print(f"   + ${amount}: {description}")

            pg_conn.commit()

            # Create chaos API
            app = create_chaos_api()
            app.config['db_conn'] = pg_conn
            app.config['redis_client'] = r
            
            # Set global variables
            import sys
            sys.modules[__name__].db_conn = pg_conn
            sys.modules[__name__].redis_client = r

            # Start API server
            def run_api():
                app.run(host='0.0.0.0', port=5006, debug=False, use_reloader=False)

            api_thread = threading.Thread(target=run_api)
            api_thread.daemon = True
            api_thread.start()

            # Wait for API to start
            time.sleep(2)

            base_url = "http://localhost:5006"

            # Test data corruption scenarios
            print(f"\n🧪 Testing Data Corruption Scenarios:")

            # Scenario 1: Normal data operations
            print(f"\n   Scenario 1: Normal Data Operations")
            try:
                # Create a new transaction
                new_transaction = {
                    "name": "Test User",
                    "email": "test@example.com"
                }
                response = requests.post(f"{base_url}/api/users", json=new_transaction, timeout=5)
                print(f"      Create User Status: {response.status_code}")
                
                if response.status_code == 201:
                    user_data = response.json()
                    print(f"      Created User: {user_data.get('name')} ({user_data.get('email')})")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 2: Simulate data corruption
            print(f"\n   Scenario 2: Simulate Data Corruption")
            try:
                # Manually corrupt data in database
                cursor.execute("UPDATE users SET email = 'corrupted@' WHERE id = 1")
                pg_conn.commit()
                print(f"      📝 Corrupted user email in database")
                
                # Try to retrieve corrupted data
                response = requests.get(f"{base_url}/api/users", timeout=5)
                if response.status_code == 200:
                    users_data = response.json()
                    print(f"      Retrieved {len(users_data.get('users', []))} users")
                    
                    for user in users_data.get('users', []):
                        email = user.get('email', '')
                        if 'corrupted' in email:
                            print(f"         ⚠️  Corrupted data detected: {email}")
                        else:
                            print(f"         ✅ Valid data: {email}")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 3: Cache corruption
            print(f"\n   Scenario 3: Cache Corruption")
            try:
                # Store corrupted data in cache
                r.setex("corrupted_data", 300, "invalid_json{")
                print(f"      📝 Stored corrupted data in cache")
                
                # Try to retrieve from cache
                cached_data = r.get("corrupted_data")
                print(f"      Retrieved from cache: {cached_data}")
                
                # Try to parse as JSON (should fail)
                try:
                    json.loads(cached_data)
                    print(f"      ✅ Cache data is valid JSON")
                except json.JSONDecodeError:
                    print(f"      ❌ Cache data is corrupted JSON")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Scenario 4: Database constraint violations
            print(f"\n   Scenario 4: Database Constraint Violations")
            try:
                # Try to create user with duplicate email
                duplicate_user = {
                    "name": "Duplicate User",
                    "email": "test@example.com"  # Same email as before
                }
                response = requests.post(f"{base_url}/api/users", json=duplicate_user, timeout=5)
                print(f"      Duplicate Email Status: {response.status_code}")
                
                if response.status_code != 201:
                    error_data = response.json()
                    print(f"      Error: {error_data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"      ❌ Test failed: {str(e)[:50]}")

            # Show final database state
            print(f"\n📊 Final Database State:")
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"   Total Users: {user_count}")

            cursor.execute("SELECT name, email FROM users ORDER BY id")
            users = cursor.fetchall()
            for name, email in users:
                status = "⚠️  Corrupted" if 'corrupted' in email else "✅ Valid"
                print(f"   {status} {name} ({email})")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 API data corruption test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement data validation, integrity checks, and monitoring!")

def main():
    """Run API Testing Chaos Scenarios"""
    print("💥 LAB 6: API TESTING CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world API resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_api_timeouts()
        chaos_api_failures()
        chaos_api_load_issues()
        chaos_api_data_corruption()
        
        print("\n🎉 API TESTING CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• API timeouts happen - implement proper timeout handling and retry logic")
        print("• API failures are common - implement circuit breakers and graceful degradation")
        print("• High load causes issues - implement rate limiting and auto-scaling")
        print("• Data corruption occurs - implement validation and integrity checks")
        print("• Real-world API issues are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for API production chaos!")
        
    except Exception as e:
        print(f"❌ API testing chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
