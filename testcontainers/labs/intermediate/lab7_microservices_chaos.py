#!/usr/bin/env python3
"""
Lab 7: Microservices Integration - Chaos Scenarios
==================================================

Experience microservices chaos in production environments.
Learn how to handle service failures, network issues, and distributed system problems.
"""

import os
import sys
import time
import json
import threading
import random
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

def create_chaos_microservice(service_name, port):
    """Create a microservice with chaos simulation"""
    app = Flask(__name__)
    
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
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            if simulate_chaos():
                return jsonify({
                    'service': service_name,
                    'status': 'unhealthy',
                    'error': 'Simulated chaos failure',
                    'timestamp': time.time()
                }), 500
            
            if db_conn:
                cursor = db_conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
            
            if redis_client:
                redis_client.ping()
            
            return jsonify({
                'service': service_name,
                'status': 'healthy',
                'database': 'connected' if db_conn else 'not_available',
                'cache': 'connected' if redis_client else 'not_available',
                'chaos_mode': chaos_mode,
                'timestamp': time.time()
            })
        except Exception as e:
            return jsonify({
                'service': service_name,
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    @app.route('/api/chaos/configure', methods=['POST'])
    def configure_chaos():
        global chaos_mode, failure_rate, response_delay
        
        data = request.get_json()
        chaos_mode = data.get('enabled', False)
        failure_rate = data.get('failure_rate', 0.0)
        response_delay = data.get('response_delay', 0.0)
        
        return jsonify({
            'service': service_name,
            'chaos_mode': chaos_mode,
            'failure_rate': failure_rate,
            'response_delay': response_delay,
            'message': 'Chaos configuration updated'
        })
    
    @app.route('/api/data', methods=['GET'])
    def get_data():
        try:
            if simulate_chaos():
                return jsonify({'error': 'Simulated data access failure'}), 500
            
            if db_conn:
                cursor = db_conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                cursor.close()
                
                return jsonify({
                    'service': service_name,
                    'data_count': count,
                    'status': 'success'
                })
            else:
                return jsonify({'error': 'Database not available'}), 503
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

def chaos_service_failures():
    """Service failure chaos - what happens when microservices fail?"""
    print("\n💥 Service Failure Chaos...")
    print("🚨 What happens when microservices fail randomly or consistently?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             MySqlContainer("mysql:8.0") as mysql, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup databases
            pg_conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )

            mysql_conn = pymysql.connect(
                host=mysql.get_container_host_ip(),
                port=mysql.get_exposed_port(3306),
                user=mysql.username,
                password=mysql.password,
                database=mysql.dbname
            )

            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )

            # Create tables
            pg_cursor = pg_conn.cursor()
            pg_cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            mysql_cursor = mysql_conn.cursor()
            mysql_cursor.execute("""
                CREATE TABLE orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_name VARCHAR(100) NOT NULL,
                    quantity INT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            print("📊 Database Tables Created: users (PostgreSQL), orders (MySQL)")

            # Insert test data
            users = [
                ("Alice Johnson", "alice@example.com"),
                ("Bob Smith", "bob@example.com"),
                ("Carol Davis", "carol@example.com")
            ]

            print("📝 Creating Test Data:")
            for name, email in users:
                pg_cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (name, email)
                )
                print(f"   + User: {name} ({email})")

            pg_conn.commit()

            # Create chaos microservices
            user_service = create_chaos_microservice("user-service", 5001)
            order_service = create_chaos_microservice("order-service", 5002)
            notification_service = create_chaos_microservice("notification-service", 5003)

            # Set global variables
            import sys
            sys.modules[__name__].db_conn = pg_conn
            sys.modules[__name__].mysql_conn = mysql_conn
            sys.modules[__name__].redis_client = r

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

            print(f"\n🚀 Microservices Started:")
            print(f"   👤 User Service: http://localhost:5001")
            print(f"   📦 Order Service: http://localhost:5002")
            print(f"   🔔 Notification Service: http://localhost:5003")

            # Test service failure scenarios
            print(f"\n🧪 Testing Service Failure Scenarios:")

            # Scenario 1: Normal operation
            print(f"\n   Scenario 1: Normal Operation")
            services = [
                ("User Service", "http://localhost:5001/api/health"),
                ("Order Service", "http://localhost:5002/api/health"),
                ("Notification Service", "http://localhost:5003/api/health")
            ]

            for service_name, health_url in services:
                try:
                    response = requests.get(health_url, timeout=5)
                    if response.status_code == 200:
                        health_data = response.json()
                        status = health_data.get('status', 'unknown')
                        print(f"      ✅ {service_name}: {status}")
                    else:
                        print(f"      ❌ {service_name}: Unhealthy ({response.status_code})")
                except Exception as e:
                    print(f"      ❌ {service_name}: Error - {str(e)[:30]}")

            # Scenario 2: Enable chaos mode
            print(f"\n   Scenario 2: Enable Chaos Mode")
            chaos_config = {
                "enabled": True,
                "failure_rate": 0.3,  # 30% failure rate
                "response_delay": 1.0  # 1 second delay
            }

            for service_name, port in [("User Service", 5001), ("Order Service", 5002), ("Notification Service", 5003)]:
                try:
                    response = requests.post(f"http://localhost:{port}/api/chaos/configure", json=chaos_config, timeout=5)
                    if response.status_code == 200:
                        config_data = response.json()
                        print(f"      ✅ {service_name}: Chaos enabled (failure_rate: {config_data['failure_rate']})")
                    else:
                        print(f"      ❌ {service_name}: Failed to configure chaos")
                except Exception as e:
                    print(f"      ❌ {service_name}: Error - {str(e)[:30]}")

            # Scenario 3: Test with chaos enabled
            print(f"\n   Scenario 3: Test with Chaos Enabled")
            success_count = 0
            failure_count = 0

            for i in range(10):
                for service_name, health_url in services:
                    try:
                        response = requests.get(health_url, timeout=10)
                        if response.status_code == 200:
                            success_count += 1
                            print(f"      Request {i+1} - {service_name}: ✅ Success")
                        else:
                            failure_count += 1
                            print(f"      Request {i+1} - {service_name}: ❌ Failed ({response.status_code})")
                    except Exception as e:
                        failure_count += 1
                        print(f"      Request {i+1} - {service_name}: ❌ Exception ({str(e)[:30]})")

            print(f"\n      📊 Chaos Test Results:")
            print(f"         Successful Requests: {success_count}")
            print(f"         Failed Requests: {failure_count}")
            print(f"         Success Rate: {(success_count/(success_count+failure_count))*100:.1f}%")

            # Scenario 4: Disable chaos and test recovery
            print(f"\n   Scenario 4: Disable Chaos and Test Recovery")
            recovery_config = {
                "enabled": False,
                "failure_rate": 0.0,
                "response_delay": 0.0
            }

            for service_name, port in [("User Service", 5001), ("Order Service", 5002), ("Notification Service", 5003)]:
                try:
                    response = requests.post(f"http://localhost:{port}/api/chaos/configure", json=recovery_config, timeout=5)
                    if response.status_code == 200:
                        print(f"      ✅ {service_name}: Chaos disabled")
                    else:
                        print(f"      ❌ {service_name}: Failed to disable chaos")
                except Exception as e:
                    print(f"      ❌ {service_name}: Error - {str(e)[:30]}")

            # Test recovery
            print(f"      🔄 Testing Recovery:")
            for service_name, health_url in services:
                try:
                    response = requests.get(health_url, timeout=5)
                    if response.status_code == 200:
                        health_data = response.json()
                        status = health_data.get('status', 'unknown')
                        print(f"         ✅ {service_name}: {status}")
                    else:
                        print(f"         ❌ {service_name}: Still unhealthy ({response.status_code})")
                except Exception as e:
                    print(f"         ❌ {service_name}: Error - {str(e)[:30]}")

            # Cleanup
            pg_cursor.close()
            pg_conn.close()
            mysql_cursor.close()
            mysql_conn.close()

    except Exception as e:
        print(f"   💥 Service failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement circuit breakers, retries, and graceful degradation!")

def chaos_network_partitions():
    """Network partition chaos - what happens when services can't communicate?"""
    print("\n💥 Network Partition Chaos...")
    print("🚨 What happens when microservices lose network connectivity?")
    
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
                CREATE TABLE distributed_data (
                    id SERIAL PRIMARY KEY,
                    service_name VARCHAR(50) NOT NULL,
                    data_key VARCHAR(100) NOT NULL,
                    data_value TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Database Table Created: distributed_data")

            # Insert initial data
            initial_data = [
                ("user-service", "user_count", "100"),
                ("order-service", "order_count", "250"),
                ("notification-service", "notification_count", "500")
            ]

            print("📝 Creating Initial Distributed Data:")
            for service_name, data_key, data_value in initial_data:
                cursor.execute(
                    "INSERT INTO distributed_data (service_name, data_key, data_value) VALUES (%s, %s, %s)",
                    (service_name, data_key, data_value)
                )
                print(f"   + {service_name}: {data_key} = {data_value}")

            pg_conn.commit()

            # Simulate network partition scenarios
            print(f"\n🧪 Simulating Network Partition Scenarios:")

            # Scenario 1: Service isolation
            print(f"\n   Scenario 1: Service Isolation")
            print(f"      📡 User Service: Isolated from network")
            print(f"      📡 Order Service: Connected to network")
            print(f"      📡 Notification Service: Connected to network")
            print(f"      ⚠️  User Service cannot communicate with other services")

            # Scenario 2: Data inconsistency
            print(f"\n   Scenario 2: Data Inconsistency")
            
            # Simulate conflicting updates from different partitions
            cursor.execute("UPDATE distributed_data SET data_value = '150', version = version + 1 WHERE service_name = 'user-service'")
            pg_conn.commit()
            print(f"      📝 Partition A: User count updated to 150")

            # Simulate another partition updating the same data
            cursor.execute("UPDATE distributed_data SET data_value = '200', version = version + 1 WHERE service_name = 'user-service'")
            pg_conn.commit()
            print(f"      📝 Partition B: User count updated to 200")
            print(f"      ⚠️  Data inconsistency detected: Same data updated by different partitions")

            # Scenario 3: Split-brain scenario
            print(f"\n   Scenario 3: Split-Brain Scenario")
            
            # Simulate conflicting service decisions
            print(f"      🧠 Service A: User 123 is active")
            print(f"      🧠 Service B: User 123 is inactive")
            print(f"      ⚠️  Split-brain detected: Conflicting service states")

            # Scenario 4: Service discovery failure
            print(f"\n   Scenario 4: Service Discovery Failure")
            
            # Simulate service registry corruption
            r.setex("service:user-service", 60, "corrupted_data")
            r.setex("service:order-service", 60, "corrupted_data")
            print(f"      📝 Service registry corrupted")
            
            # Try to discover services
            service_keys = r.keys("service:*")
            discovered_services = []
            
            for key in service_keys:
                try:
                    service_data = r.hgetall(key)
                    if service_data and 'corrupted' not in str(service_data):
                        discovered_services.append(key.decode('utf-8'))
                except:
                    pass
            
            print(f"      🔍 Discovered Services: {len(discovered_services)}")
            print(f"      ❌ Service discovery failed due to corrupted registry")

            # Show final data state
            print(f"\n📊 Final Data State:")
            cursor.execute("SELECT service_name, data_key, data_value, version FROM distributed_data ORDER BY service_name")
            data_state = cursor.fetchall()
            
            for service_name, data_key, data_value, version in data_state:
                print(f"   {service_name}: {data_key} = {data_value} (version {version})")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Network partition test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement conflict resolution and data synchronization strategies!")

def chaos_cascading_failures():
    """Cascading failure chaos - what happens when one service failure causes others to fail?"""
    print("\n💥 Cascading Failure Chaos...")
    print("🚨 What happens when one service failure causes a cascade of failures?")
    
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
                CREATE TABLE service_dependencies (
                    id SERIAL PRIMARY KEY,
                    service_name VARCHAR(50) NOT NULL,
                    depends_on VARCHAR(50) NOT NULL,
                    dependency_type VARCHAR(20) NOT NULL,
                    is_critical BOOLEAN DEFAULT true
                )
            """)
            print("📊 Database Table Created: service_dependencies")

            # Define service dependencies
            dependencies = [
                ("order-service", "user-service", "data", True),
                ("notification-service", "user-service", "data", True),
                ("notification-service", "order-service", "event", True),
                ("payment-service", "order-service", "data", True),
                ("shipping-service", "order-service", "data", True),
                ("analytics-service", "user-service", "data", False),
                ("analytics-service", "order-service", "data", False)
            ]

            print("📝 Creating Service Dependencies:")
            for service, depends_on, dep_type, is_critical in dependencies:
                cursor.execute(
                    "INSERT INTO service_dependencies (service_name, depends_on, dependency_type, is_critical) VALUES (%s, %s, %s, %s)",
                    (service, depends_on, dep_type, is_critical)
                )
                critical_text = "Critical" if is_critical else "Optional"
                print(f"   + {service} depends on {depends_on} ({dep_type}) - {critical_text}")

            pg_conn.commit()

            # Simulate cascading failures
            print(f"\n🧪 Simulating Cascading Failures:")

            # Scenario 1: User Service Failure
            print(f"\n   Scenario 1: User Service Failure")
            print(f"      ❌ User Service: FAILED")
            
            # Check which services depend on user service
            cursor.execute("SELECT service_name, dependency_type, is_critical FROM service_dependencies WHERE depends_on = 'user-service'")
            dependent_services = cursor.fetchall()
            
            print(f"      📊 Services depending on User Service:")
            for service_name, dep_type, is_critical in dependent_services:
                status = "❌ FAILED" if is_critical else "⚠️  DEGRADED"
                print(f"         {service_name}: {status} ({dep_type} dependency)")

            # Scenario 2: Order Service Failure
            print(f"\n   Scenario 2: Order Service Failure")
            print(f"      ❌ Order Service: FAILED")
            
            # Check which services depend on order service
            cursor.execute("SELECT service_name, dependency_type, is_critical FROM service_dependencies WHERE depends_on = 'order-service'")
            dependent_services = cursor.fetchall()
            
            print(f"      📊 Services depending on Order Service:")
            for service_name, dep_type, is_critical in dependent_services:
                status = "❌ FAILED" if is_critical else "⚠️  DEGRADED"
                print(f"         {service_name}: {status} ({dep_type} dependency)")

            # Scenario 3: Cascading failure chain
            print(f"\n   Scenario 3: Cascading Failure Chain")
            failure_chain = [
                "User Service fails due to database connection timeout",
                "Order Service fails due to user data unavailability",
                "Notification Service fails due to order event unavailability",
                "Payment Service fails due to order data unavailability",
                "Shipping Service fails due to order data unavailability",
                "Analytics Service degrades due to missing user and order data"
            ]
            
            print(f"      📉 Failure Chain:")
            for i, failure in enumerate(failure_chain, 1):
                print(f"         {i}. {failure}")
                time.sleep(0.2)  # Simulate delay between failures

            print(f"      💥 System-wide failure: All critical services affected!")

            # Scenario 4: Recovery simulation
            print(f"\n   Scenario 4: Recovery Simulation")
            recovery_steps = [
                "User Service recovers from database timeout",
                "Order Service recovers as user data becomes available",
                "Notification Service recovers as order events resume",
                "Payment Service recovers as order data becomes available",
                "Shipping Service recovers as order data becomes available",
                "Analytics Service fully recovers as all data becomes available"
            ]
            
            print(f"      🔄 Recovery Steps:")
            for i, step in enumerate(recovery_steps, 1):
                print(f"         {i}. {step}")
                time.sleep(0.2)  # Simulate delay between recoveries

            print(f"      ✅ System fully recovered: All services operational!")

            # Show dependency analysis
            print(f"\n📊 Dependency Analysis:")
            cursor.execute("""
                SELECT service_name, COUNT(*) as dependency_count,
                       SUM(CASE WHEN is_critical THEN 1 ELSE 0 END) as critical_dependencies
                FROM service_dependencies 
                GROUP BY service_name 
                ORDER BY dependency_count DESC
            """)
            
            dependency_analysis = cursor.fetchall()
            for service_name, dep_count, critical_deps in dependency_analysis:
                print(f"   {service_name}: {dep_count} dependencies ({critical_deps} critical)")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Cascading failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement circuit breakers, bulkheads, and graceful degradation!")

def chaos_data_consistency_issues():
    """Data consistency chaos - what happens when data becomes inconsistent across services?"""
    print("\n💥 Data Consistency Chaos...")
    print("🚨 What happens when data becomes inconsistent across microservices?")
    
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
                CREATE TABLE user_profiles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    service_name VARCHAR(50) NOT NULL,
                    profile_data JSONB NOT NULL,
                    version INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Database Table Created: user_profiles")

            # Insert initial consistent data
            initial_profiles = [
                (1, "user-service", '{"name": "Alice Johnson", "email": "alice@example.com", "status": "active"}'),
                (1, "order-service", '{"name": "Alice Johnson", "email": "alice@example.com", "status": "active"}'),
                (1, "notification-service", '{"name": "Alice Johnson", "email": "alice@example.com", "status": "active"}')
            ]

            print("📝 Creating Initial Consistent Data:")
            for user_id, service_name, profile_data in initial_profiles:
                cursor.execute(
                    "INSERT INTO user_profiles (user_id, service_name, profile_data) VALUES (%s, %s, %s)",
                    (user_id, service_name, profile_data)
                )
                print(f"   + User {user_id} in {service_name}: {profile_data}")

            pg_conn.commit()

            # Simulate data consistency issues
            print(f"\n🧪 Simulating Data Consistency Issues:")

            # Scenario 1: Partial updates
            print(f"\n   Scenario 1: Partial Updates")
            
            # Update user in user-service only
            cursor.execute("""
                UPDATE user_profiles 
                SET profile_data = '{"name": "Alice Johnson (Updated)", "email": "alice.updated@example.com", "status": "active"}',
                    version = version + 1
                WHERE user_id = 1 AND service_name = 'user-service'
            """)
            pg_conn.commit()
            print(f"      📝 User Service: Profile updated to Alice Johnson (Updated)")

            # Update user in order-service only
            cursor.execute("""
                UPDATE user_profiles 
                SET profile_data = '{"name": "Alice Johnson", "email": "alice@example.com", "status": "inactive"}',
                    version = version + 1
                WHERE user_id = 1 AND service_name = 'order-service'
            """)
            pg_conn.commit()
            print(f"      📝 Order Service: Profile updated to inactive status")

            print(f"      ⚠️  Data inconsistency: Different services have different user data")

            # Scenario 2: Orphaned records
            print(f"\n   Scenario 2: Orphaned Records")
            
            # Create orphaned record
            cursor.execute("""
                INSERT INTO user_profiles (user_id, service_name, profile_data) 
                VALUES (999, 'user-service', '{"name": "Ghost User", "email": "ghost@example.com", "status": "active"}')
            """)
            pg_conn.commit()
            print(f"      📝 User Service: Ghost user created (ID: 999)")
            print(f"      ⚠️  Orphaned record: Ghost user exists in user-service but not in other services")

            # Scenario 3: Version conflicts
            print(f"\n   Scenario 3: Version Conflicts")
            
            # Simulate concurrent updates with different versions
            cursor.execute("""
                UPDATE user_profiles 
                SET profile_data = '{"name": "Alice Johnson", "email": "alice@example.com", "status": "premium"}',
                    version = 5
                WHERE user_id = 1 AND service_name = 'notification-service'
            """)
            pg_conn.commit()
            print(f"      📝 Notification Service: Profile updated to premium status (version 5)")

            # Try to update with older version
            cursor.execute("""
                UPDATE user_profiles 
                SET profile_data = '{"name": "Alice Johnson", "email": "alice@example.com", "status": "basic"}',
                    version = 3
                WHERE user_id = 1 AND service_name = 'notification-service'
            """)
            pg_conn.commit()
            print(f"      📝 Notification Service: Attempted update with older version (version 3)")
            print(f"      ⚠️  Version conflict: Update with older version may overwrite newer data")

            # Scenario 4: Data corruption
            print(f"\n   Scenario 4: Data Corruption")
            
            # Simulate corrupted data
            cursor.execute("""
                UPDATE user_profiles 
                SET profile_data = '{"name": "Alice Johnson", "email": "corrupted@", "status": "active"}'
                WHERE user_id = 1 AND service_name = 'user-service'
            """)
            pg_conn.commit()
            print(f"      📝 User Service: Profile corrupted with invalid email")
            print(f"      ⚠️  Data corruption: Invalid data format in user profile")

            # Show final data state
            print(f"\n📊 Final Data State:")
            cursor.execute("""
                SELECT user_id, service_name, profile_data, version, last_updated
                FROM user_profiles 
                ORDER BY user_id, service_name
            """)
            
            data_state = cursor.fetchall()
            for user_id, service_name, profile_data, version, last_updated in data_state:
                print(f"   User {user_id} in {service_name}:")
                print(f"      Data: {profile_data}")
                print(f"      Version: {version}")
                print(f"      Updated: {last_updated}")

            # Show consistency analysis
            print(f"\n🔍 Consistency Analysis:")
            cursor.execute("""
                SELECT user_id, COUNT(*) as service_count,
                       COUNT(DISTINCT profile_data) as unique_profiles,
                       MAX(version) as max_version,
                       MIN(version) as min_version
                FROM user_profiles 
                GROUP BY user_id 
                ORDER BY user_id
            """)
            
            consistency_analysis = cursor.fetchall()
            for user_id, service_count, unique_profiles, max_version, min_version in consistency_analysis:
                consistent = "✅" if unique_profiles == 1 else "❌"
                print(f"   {consistent} User {user_id}: {service_count} services, {unique_profiles} unique profiles, versions {min_version}-{max_version}")

            cursor.close()
            pg_conn.close()

    except Exception as e:
        print(f"   💥 Data consistency test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement data validation, versioning, and consistency checks!")

def main():
    """Run Microservices Chaos Scenarios"""
    print("💥 LAB 7: MICROSERVICES CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world microservices resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_service_failures()
        chaos_network_partitions()
        chaos_cascading_failures()
        chaos_data_consistency_issues()
        
        print("\n🎉 MICROSERVICES CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Service failures happen - implement circuit breakers and retries")
        print("• Network partitions occur - implement conflict resolution strategies")
        print("• Cascading failures are real - implement bulkheads and graceful degradation")
        print("• Data consistency matters - implement validation and versioning")
        print("• Real-world microservices are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for microservices production chaos!")
        
    except Exception as e:
        print(f"❌ Microservices chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
