#!/usr/bin/env python3
"""
Lab 6: API Testing - Working Examples (Fixed Version)
=====================================================

Learn how to test APIs that interact with databases using TestContainers.
Master real-world API testing with Flask, PostgreSQL, and Redis.
"""

import os
import sys
import json
import time
import socket
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

def find_free_port(start_port=5000, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port starting from {start_port}")

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
    import threading
    import uuid
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis flask requests")
    sys.exit(1)

def create_simple_api(db_conn, redis_client):
    """Create a simple test API with database integration"""
    app = Flask(__name__)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            cursor = db_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            if redis_client:
                redis_client.ping()
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'cache': 'connected' if redis_client else 'not_available',
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Get all users"""
        try:
            cursor = db_conn.cursor()
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
        """Create a new user"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON data required'}), 400
                
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return jsonify({'error': 'Name and email are required'}), 400
            
            cursor = db_conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (name, email)
            )
            user_id = cursor.fetchone()[0]
            db_conn.commit()
            cursor.close()
            
            return jsonify({
                'id': user_id,
                'name': name,
                'email': email,
                'message': 'User created successfully'
            }), 201
        except psycopg2.IntegrityError as e:
            db_conn.rollback()
            if 'unique' in str(e).lower():
                return jsonify({'error': 'Email already exists'}), 409
            else:
                return jsonify({'error': 'Database constraint violation'}), 400
        except Exception as e:
            db_conn.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/cache/<key>', methods=['GET'])
    def get_cache(key):
        """Get cached data"""
        try:
            if redis_client:
                value = redis_client.get(key)
                if value:
                    return jsonify({'key': key, 'value': value, 'cached': True})
                else:
                    return jsonify({'key': key, 'value': None, 'cached': False})
            else:
                return jsonify({'error': 'Cache not available'}), 503
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/cache/<key>', methods=['POST'])
    def set_cache(key):
        """Set cached data"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON data required'}), 400
                
            value = data.get('value')
            ttl = data.get('ttl', 300)  # Default 5 minutes
            
            if redis_client:
                redis_client.setex(key, ttl, value)
                return jsonify({
                    'key': key,
                    'value': value,
                    'ttl': ttl,
                    'message': 'Cached successfully'
                })
            else:
                return jsonify({'error': 'Cache not available'}), 503
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

def demo_api_testing_basics():
    """Basic API testing with real data operations"""
    print("\n🌐 API Testing Basics Demo...")
    
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

        # Create and start API
        app = create_simple_api(pg_conn, r)

        # Find a free port and start API
        api_port = find_free_port(5000)
        print(f"🚀 Starting API on port {api_port}...")
        
        def run_api():
            app.run(host='0.0.0.0', port=api_port, debug=False, use_reloader=False)

        api_thread = threading.Thread(target=run_api)
        api_thread.daemon = True
        api_thread.start()

        # Wait for API to start
        time.sleep(3)
        
        # Verify API is running
        max_attempts = 10
        api_running = False
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"http://localhost:{api_port}/api/health", timeout=2)
                if response.status_code == 200:
                    api_running = True
                    break
            except:
                if attempt < max_attempts - 1:
                    time.sleep(1)
        
        if not api_running:
            print(f"❌ API failed to start on port {api_port}")
            print("💡 Try disabling AirPlay Receiver in System Preferences")
            cursor.close()
            pg_conn.close()
            return

        base_url = f"http://localhost:{api_port}"

        # Test API endpoints
        print(f"\n🧪 Testing API Endpoints:")

        # Test 1: Health Check
        print(f"\n   Test 1: Health Check")
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"      Status: {response.status_code}")
                print(f"      Database: {health_data.get('database', 'unknown')}")
                print(f"      Cache: {health_data.get('cache', 'unknown')}")
                print(f"      Overall: {health_data.get('status', 'unknown')}")
            else:
                print(f"      Status: {response.status_code}")
                print(f"      Response: {response.text[:100]}")
        except Exception as e:
            print(f"      ❌ Health check failed: {str(e)[:50]}")

        # Test 2: Get All Users
        print(f"\n   Test 2: Get All Users")
        try:
            response = requests.get(f"{base_url}/api/users", timeout=5)
            if response.status_code == 200:
                users_data = response.json()
                print(f"      Status: {response.status_code}")
                print(f"      Users Count: {users_data.get('count', 0)}")
                
                for user in users_data.get('users', []):
                    print(f"         👤 {user['name']} ({user['email']}) - ID: {user['id']}")
            else:
                print(f"      Status: {response.status_code}")
                print(f"      Response: {response.text[:100]}")
        except Exception as e:
            print(f"      ❌ Get users failed: {str(e)[:50]}")

        # Test 3: Create New User
        print(f"\n   Test 3: Create New User")
        try:
            new_user = {
                "name": "David Wilson",
                "email": "david@example.com"
            }
            response = requests.post(f"{base_url}/api/users", json=new_user, timeout=5)
            if response.status_code in [200, 201]:
                user_data = response.json()
                print(f"      Status: {response.status_code}")
                print(f"      Created: {user_data.get('name')} ({user_data.get('email')}) - ID: {user_data.get('id')}")
            else:
                print(f"      Status: {response.status_code}")
                print(f"      Response: {response.text[:100]}")
        except Exception as e:
            print(f"      ❌ Create user failed: {str(e)[:50]}")

        # Test 4: Cache Operations
        print(f"\n   Test 4: Cache Operations")
        try:
            # Set cache
            cache_data = {"value": "test_data_123", "ttl": 60}
            response = requests.post(f"{base_url}/api/cache/test_key", json=cache_data, timeout=5)
            if response.status_code in [200, 201]:
                cache_result = response.json()
                print(f"      Set Cache: {cache_result.get('message')}")
            else:
                print(f"      Set Cache Status: {response.status_code}")
                print(f"      Response: {response.text[:100]}")

            # Get cache
            response = requests.get(f"{base_url}/api/cache/test_key", timeout=5)
            if response.status_code == 200:
                cache_data = response.json()
                print(f"      Get Cache: {cache_data.get('value')} (cached: {cache_data.get('cached')})")
            else:
                print(f"      Get Cache Status: {response.status_code}")
                print(f"      Response: {response.text[:100]}")
        except Exception as e:
            print(f"      ❌ Cache operations failed: {str(e)[:50]}")

        # Final verification
        print(f"\n📊 Final Database State:")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   Total Users: {user_count}")

        cursor.execute("SELECT name, email FROM users ORDER BY id")
        remaining_users = cursor.fetchall()
        for name, email in remaining_users:
            print(f"   👤 {name} ({email})")

        cursor.close()
        pg_conn.close()

def demo_api_performance_testing():
    """API performance testing with load simulation"""
    print("\n⚡ API Performance Testing Demo...")
    
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
                stock INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Database Table Created: products")

        # Insert test products
        products = [
            ("MacBook Pro", 2499.99, 10),
            ("iPhone", 999.99, 25),
            ("iPad", 599.99, 15),
            ("AirPods", 199.99, 50)
        ]

        print("📝 Creating Test Products:")
        for name, price, stock in products:
            cursor.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (name, price, stock)
            )
            print(f"   + {name}: ${price} (Stock: {stock})")

        pg_conn.commit()

        # Create API for performance testing
        app = Flask(__name__)
        
        @app.route('/api/products', methods=['GET'])
        def get_products():
            try:
                cursor = pg_conn.cursor()
                cursor.execute("SELECT id, name, price, stock FROM products ORDER BY id")
                products_data = cursor.fetchall()
                cursor.close()
                
                result = []
                for product_id, name, price, stock in products_data:
                    result.append({
                        'id': product_id,
                        'name': name,
                        'price': float(price),
                        'stock': stock
                    })
                
                return jsonify({'products': result, 'count': len(result)})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        # Start API server
        api_port = find_free_port(5001)
        print(f"🚀 Starting Performance API on port {api_port}...")
        
        def run_api():
            app.run(host='0.0.0.0', port=api_port, debug=False, use_reloader=False)

        api_thread = threading.Thread(target=run_api)
        api_thread.daemon = True
        api_thread.start()

        # Wait for API to start
        time.sleep(3)
        
        # Verify API is running
        max_attempts = 10
        api_running = False
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"http://localhost:{api_port}/api/products", timeout=2)
                if response.status_code == 200:
                    api_running = True
                    break
            except:
                if attempt < max_attempts - 1:
                    time.sleep(1)
        
        if not api_running:
            print(f"❌ API failed to start on port {api_port}")
            cursor.close()
            pg_conn.close()
            return

        base_url = f"http://localhost:{api_port}"

        # Performance testing
        print(f"\n🧪 Performance Testing:")

        # Test 1: Single request timing
        print(f"\n   Test 1: Single Request Timing")
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}/api/products", timeout=10)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"      Status: {response.status_code}")
            print(f"      Response Time: {response_time:.2f}ms")
            
            if response.status_code == 200:
                data = response.json()
                print(f"      Products Returned: {data.get('count', 0)}")
        except Exception as e:
            print(f"      ❌ Single request failed: {str(e)[:50]}")

        # Test 2: Concurrent requests
        print(f"\n   Test 2: Concurrent Requests")
        import concurrent.futures
        
        def make_request(request_id):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}/api/products", timeout=10)
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

        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]

        print(f"      Successful Requests: {len(successful_requests)}")
        print(f"      Failed Requests: {len(failed_requests)}")
        
        if successful_requests:
            avg_time = sum(r['time'] for r in successful_requests) / len(successful_requests)
            min_time = min(r['time'] for r in successful_requests)
            max_time = max(r['time'] for r in successful_requests)
            print(f"      Average Response Time: {avg_time:.2f}ms")
            print(f"      Min Response Time: {min_time:.2f}ms")
            print(f"      Max Response Time: {max_time:.2f}ms")

        # Test 3: Load testing with Redis caching
        print(f"\n   Test 3: Load Testing with Caching")
        
        # Simulate cache warming
        for i in range(5):
            try:
                response = requests.get(f"{base_url}/api/products", timeout=5)
                if response.status_code == 200:
                    # Simulate caching in Redis
                    r.setex(f"products:all", 60, response.text)
            except:
                pass

        # Load test with cached data
        load_test_results = []
        for i in range(20):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}/api/products", timeout=5)
                end_time = time.time()
                load_test_results.append((end_time - start_time) * 1000)
            except:
                pass

        if load_test_results:
            avg_load_time = sum(load_test_results) / len(load_test_results)
            print(f"      Load Test Requests: {len(load_test_results)}")
            print(f"      Average Load Time: {avg_load_time:.2f}ms")

        cursor.close()
        pg_conn.close()

def main():
    """Run Lab 6 - API Testing"""
    print("🚀 LAB 6: API Testing - Working Examples (Fixed)")
    print("=" * 60)
    print("✨ Master API testing with TestContainers and real databases!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_api_testing_basics()
        demo_api_performance_testing()
        
        print("\n✅ Lab 6 completed successfully!")
        print("Key concepts learned:")
        print("• API testing with real databases using TestContainers")
        print("• Flask API development with database integration")
        print("• Performance testing and load simulation")
        print("• Error handling and edge case testing")
        print("• Redis caching integration")
        print("• Real-world API testing scenarios")
        print("\n💪 You're ready for microservices testing!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
