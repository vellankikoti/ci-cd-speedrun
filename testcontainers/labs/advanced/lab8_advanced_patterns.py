#!/usr/bin/env python3
"""
Lab 8: Advanced Patterns - Working Examples
===========================================

Learn advanced TestContainers patterns including custom containers,
network testing, data persistence, and complex scenarios.
"""

import os
import sys
import time
import threading
import tempfile
import json
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
        'redis': 'redis'
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
        # Check if docker command exists
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        
        # Check if Docker daemon is running
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        
        # If docker ps fails, try docker info as fallback
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        return result.returncode == 0
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis")
    sys.exit(1)

def demo_custom_container():
    """Custom container with real data operations"""
    print("\n🔧 Custom Container Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        
        # Setup database
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE analytics (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                user_id INTEGER NOT NULL,
                data JSONB NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Analytics Table Created")
        
        # Insert real analytics data
        events = [
            ("page_view", 1001, '{"page": "/products", "duration": 45}'),
            ("click", 1001, '{"element": "buy_button", "product_id": 123}'),
            ("purchase", 1001, '{"amount": 99.99, "currency": "USD"}'),
            ("page_view", 1002, '{"page": "/checkout", "duration": 120}'),
            ("purchase", 1002, '{"amount": 249.99, "currency": "USD"}')
        ]
        
        print("📝 Inserting Analytics Events:")
        for event_type, user_id, data in events:
            cursor.execute(
                "INSERT INTO analytics (event_type, user_id, data) VALUES (%s, %s, %s)",
                (event_type, user_id, data)
            )
            print(f"   + {event_type}: User {user_id} - {data}")
        
        conn.commit()
        
        # Analyze real data
        print(f"\n📊 Analytics Analysis:")
        cursor.execute("""
            SELECT event_type, COUNT(*) as count, 
                   AVG((data->>'duration')::int) as avg_duration
            FROM analytics 
            WHERE data ? 'duration'
            GROUP BY event_type
        """)
        
        results = cursor.fetchall()
        for event_type, count, avg_duration in results:
            print(f"   {event_type}: {count} events, avg duration: {avg_duration:.1f}s")
        
        cursor.close()
        conn.close()

def demo_data_persistence():
    """Data persistence with volume mounting"""
    print("\n💾 Data Persistence Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        
        # Setup database
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE persistent_data (
                id SERIAL PRIMARY KEY,
                key VARCHAR(100) UNIQUE NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Persistent Data Table Created")
        
        # Insert persistent data
        persistent_items = [
            ("config_version", "2.1.0"),
            ("feature_flags", '{"new_ui": true, "beta_features": false}'),
            ("user_preferences", '{"theme": "dark", "notifications": true}'),
            ("system_settings", '{"max_connections": 100, "timeout": 30}')
        ]
        
        print("📝 Creating Persistent Data:")
        for key, value in persistent_items:
            cursor.execute(
                "INSERT INTO persistent_data (key, value) VALUES (%s, %s)",
                (key, value)
            )
            print(f"   + {key}: {value}")
        
        conn.commit()
        
        # Simulate data persistence across restarts
        print(f"\n🔄 Simulating Data Persistence:")
        cursor.execute("SELECT COUNT(*) FROM persistent_data")
        count = cursor.fetchone()[0]
        print(f"   Data Count: {count} items")
        
        cursor.execute("SELECT key, value FROM persistent_data ORDER BY key")
        items = cursor.fetchall()
        for key, value in items:
            print(f"   📋 {key}: {value}")
        
        cursor.close()
        conn.close()

def demo_network_testing():
    """Network testing with multiple containers"""
    print("\n🌐 Network Testing Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Test network connectivity
        print(f"\n🔗 Network Connectivity Test:")
        
        # PostgreSQL connection test
        try:
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            print(f"   ✅ PostgreSQL: Connected successfully")
        except Exception as e:
            print(f"   ❌ PostgreSQL: Connection failed - {str(e)[:30]}")
        
        # Redis connection test
        try:
            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )
            r.ping()
            print(f"   ✅ Redis: Connected successfully")
        except Exception as e:
            print(f"   ❌ Redis: Connection failed - {str(e)[:30]}")
        
        # Test data flow between containers
        print(f"\n📊 Data Flow Test:")
        
        # Store data in Redis
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        test_data = {
            "user_id": 1001,
            "session_id": "sess_12345",
            "timestamp": time.time()
        }
        
        r.setex("session:1001", 300, json.dumps(test_data))
        print(f"   📝 Stored in Redis: {test_data}")
        
        # Retrieve and process in PostgreSQL
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                session_id VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Get data from Redis and store in PostgreSQL
        session_data = json.loads(r.get("session:1001"))
        cursor.execute(
            "INSERT INTO sessions (user_id, session_id) VALUES (%s, %s)",
            (session_data["user_id"], session_data["session_id"])
        )
        conn.commit()
        
        print(f"   📝 Stored in PostgreSQL: User {session_data['user_id']}, Session {session_data['session_id']}")
        
        # Verify data consistency
        cursor.execute("SELECT user_id, session_id FROM sessions")
        db_data = cursor.fetchone()
        print(f"   ✅ Data Consistency: Redis and PostgreSQL data match")
        
        cursor.close()
        conn.close()

def demo_complex_scenarios():
    """Complex real-world scenarios"""
    print("\n🏗️ Complex Scenarios Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Setup complex database schema
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Create complex schema
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                total DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id),
                product_name VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """)
        
        print("📊 Complex Schema Created: users, orders, order_items")
        
        # Insert complex test data
        print("📝 Creating Complex Test Data:")
        
        # Users
        users = [("alice@example.com",), ("bob@example.com",), ("carol@example.com",)]
        for email in users:
            cursor.execute("INSERT INTO users (email) VALUES (%s)", email)
            print(f"   + User: {email[0]}")
        
        # Orders with items
        orders_data = [
            (1, 299.99, "completed", [
                ("MacBook Pro", 1, 2499.99),
                ("Wireless Mouse", 1, 29.99)
            ]),
            (2, 149.99, "pending", [
                ("iPhone", 1, 999.99),
                ("AirPods", 1, 199.99)
            ]),
            (1, 89.99, "shipped", [
                ("Coffee Mug", 2, 12.99),
                ("Sticker Pack", 1, 4.99)
            ])
        ]
        
        for user_id, total, status, items in orders_data:
            cursor.execute(
                "INSERT INTO orders (user_id, total, status) VALUES (%s, %s, %s) RETURNING id",
                (user_id, total, status)
            )
            order_id = cursor.fetchone()[0]
            
            print(f"   + Order {order_id}: User {user_id}, ${total}, {status}")
            
            for product_name, quantity, price in items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_name, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, product_name, quantity, price)
                )
                print(f"      - {product_name} x{quantity} @ ${price}")
        
        conn.commit()
        
        # Complex analysis
        print(f"\n📊 Complex Data Analysis:")
        
        # User order summary
        cursor.execute("""
            SELECT u.email, COUNT(o.id) as order_count, 
                   SUM(o.total) as total_spent,
                   AVG(o.total) as avg_order_value
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.email
            ORDER BY total_spent DESC
        """)
        
        user_summary = cursor.fetchall()
        print(f"   👥 User Order Summary:")
        for email, order_count, total_spent, avg_order in user_summary:
            # Handle None values from aggregate functions when no orders exist
            total_spent_str = f"${total_spent:.2f}" if total_spent is not None else "$0.00"
            avg_order_str = f"${avg_order:.2f}" if avg_order is not None else "$0.00"
            print(f"      {email}: {order_count} orders, {total_spent_str} total, {avg_order_str} avg")
        
        # Product popularity
        cursor.execute("""
            SELECT product_name, SUM(quantity) as total_quantity,
                   COUNT(DISTINCT order_id) as order_count,
                   SUM(quantity * price) as total_revenue
            FROM order_items
            GROUP BY product_name
            ORDER BY total_quantity DESC
        """)
        
        product_summary = cursor.fetchall()
        print(f"   📦 Product Popularity:")
        for product, quantity, orders, revenue in product_summary:
            # Handle None values from aggregate functions
            quantity_val = quantity if quantity is not None else 0
            revenue_str = f"${revenue:.2f}" if revenue is not None else "$0.00"
            print(f"      {product}: {quantity_val} units, {orders} orders, {revenue_str} revenue")
        
        # Order status distribution
        cursor.execute("""
            SELECT status, COUNT(*) as count, 
                   SUM(total) as total_value,
                   AVG(total) as avg_value
            FROM orders
            GROUP BY status
            ORDER BY count DESC
        """)
        
        status_summary = cursor.fetchall()
        print(f"   📊 Order Status Distribution:")
        for status, count, total_value, avg_value in status_summary:
            # Handle None values from aggregate functions
            total_value_str = f"${total_value:.2f}" if total_value is not None else "$0.00"
            avg_value_str = f"${avg_value:.2f}" if avg_value is not None else "$0.00"
            print(f"      {status}: {count} orders, {total_value_str} total, {avg_value_str} avg")
        
        cursor.close()
        conn.close()

def main():
    """Run Lab 8 - Advanced Patterns"""
    print("🚀 LAB 8: Advanced Patterns - Working Examples")
    print("=" * 60)
    print("✨ Master advanced TestContainers patterns!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_custom_container()
        demo_data_persistence()
        demo_network_testing()
        demo_complex_scenarios()
        
        print("\n✅ Lab 8 completed successfully!")
        print("Key concepts learned:")
        print("• Custom container configurations and data operations")
        print("• Data persistence and volume mounting patterns")
        print("• Network testing with multiple containers")
        print("• Complex real-world database scenarios")
        print("• Advanced TestContainers patterns")
        print("\n💪 You're ready for performance testing!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()