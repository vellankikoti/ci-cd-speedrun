#!/usr/bin/env python3
"""
Lab 4: Multiple Containers - Working Examples
=============================================

Learn to orchestrate multiple containers together with TestContainers.
Master real-world multi-container scenarios with PostgreSQL, Redis, and more.
"""

import os
import sys
import time
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
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis")
    sys.exit(1)

def demo_multi_container_basic():
    """Multiple containers working together with real data"""
    print("\n🔄 Multi-Container Orchestration Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Connect to both databases
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

        pg_cursor = pg_conn.cursor()

        # Create user sessions table
        pg_cursor.execute("""
            CREATE TABLE user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                session_token VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour')
            )
        """)
        print("📊 PostgreSQL Table Created: user_sessions")

        # Create user profiles table
        pg_cursor.execute("""
            CREATE TABLE user_profiles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                preferences JSONB
            )
        """)
        print("📊 PostgreSQL Table Created: user_profiles")

        # Insert user data
        users = [
            (1001, "Alice Johnson", "alice@example.com", '{"theme": "dark", "notifications": true}'),
            (1002, "Bob Smith", "bob@example.com", '{"theme": "light", "notifications": false}'),
            (1003, "Carol Davis", "carol@example.com", '{"theme": "auto", "notifications": true}')
        ]

        print("📝 Creating User Profiles:")
        for user_id, name, email, preferences in users:
            pg_cursor.execute(
                "INSERT INTO user_profiles (user_id, name, email, preferences) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, preferences)
            )
            print(f"   + User {user_id}: {name} ({email})")

        # Create sessions
        sessions = [
            (1001, "sess_alice_12345"),
            (1002, "sess_bob_67890"),
            (1003, "sess_carol_abcdef")
        ]

        print("📝 Creating User Sessions:")
        for user_id, session_token in sessions:
            pg_cursor.execute(
                "INSERT INTO user_sessions (user_id, session_token) VALUES (%s, %s)",
                (user_id, session_token)
            )
            print(f"   + Session {session_token}: User {user_id}")

        pg_conn.commit()

        # Store session data in Redis
        print("📝 Storing Session Data in Redis:")
        for user_id, session_token in sessions:
            session_data = {
                "user_id": str(user_id),
                "session_token": session_token,
                "last_activity": str(int(time.time())),
                "ip_address": "192.168.1.100"
            }
            r.hset(f"session:{session_token}", mapping=session_data)
            r.expire(f"session:{session_token}", 3600)  # 1 hour TTL
            print(f"   🔑 {session_token}: User {user_id} (TTL: 3600s)")

        # Cross-database query
        print(f"\n🔍 Cross-Database Analysis:")
        pg_cursor.execute("""
            SELECT up.user_id, up.name, up.email, 
                   up.preferences->>'theme' as theme,
                   us.session_token,
                   us.created_at
            FROM user_profiles up
            LEFT JOIN user_sessions us ON up.user_id = us.user_id
            ORDER BY up.user_id
        """)

        results = pg_cursor.fetchall()
        for user_id, name, email, theme, session_token, created_at in results:
            # Get Redis session data
            redis_data = r.hgetall(f"session:{session_token}")
            last_activity = redis_data.get("last_activity", "Unknown")
            
            print(f"   👤 User {user_id}: {name} ({email})")
            print(f"      🎨 Theme: {theme}")
            print(f"      🔑 Session: {session_token}")
            print(f"      ⏰ Last Activity: {last_activity}")

        pg_cursor.close()
        pg_conn.close()

def demo_microservices_simulation():
    """Simulate microservices with multiple containers"""
    print("\n🏗️ Microservices Simulation Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ Database Service Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Cache Service Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Simulate User Service (PostgreSQL)
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()

        # Simulate Order Service (PostgreSQL)
        pg_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        pg_cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                product_name VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("📊 User Service Tables Created: users, orders")

        # Simulate Cache Service (Redis)
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Create test data
        users_data = [
            ("alice_j", "alice@example.com"),
            ("bob_s", "bob@example.com"),
            ("carol_d", "carol@example.com")
        ]

        print("📝 Creating Users:")
        for username, email in users_data:
            pg_cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (username, email)
            )
            print(f"   + {username} ({email})")

        orders_data = [
            (1, "MacBook Pro", 1, 2499.99, "completed"),
            (1, "Wireless Mouse", 2, 29.99, "shipped"),
            (2, "Coffee Mug", 3, 12.99, "pending"),
            (3, "Python Book", 1, 49.99, "completed")
        ]

        print("📝 Creating Orders:")
        for user_id, product, quantity, price, status in orders_data:
            pg_cursor.execute(
                "INSERT INTO orders (user_id, product_name, quantity, price, status) VALUES (%s, %s, %s, %s, %s)",
                (user_id, product, quantity, price, status)
            )
            print(f"   + Order: {product} x{quantity} - ${price} ({status})")

        pg_conn.commit()

        # Simulate API calls with caching
        print(f"\n🌐 Simulating API Calls with Caching:")

        # Get user profile (with caching)
        user_id = 1
        cache_key = f"user_profile:{user_id}"
        
        # Check cache first
        cached_profile = r.get(cache_key)
        if cached_profile:
            print(f"   📱 User {user_id} profile: CACHE HIT - {cached_profile}")
        else:
            # Database query
            pg_cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
            username, email = pg_cursor.fetchone()
            profile_data = f"{username} ({email})"
            
            # Store in cache
            r.setex(cache_key, 300, profile_data)  # 5 minutes TTL
            print(f"   📱 User {user_id} profile: CACHE MISS - {profile_data} (cached for 5min)")

        # Get user orders (with caching)
        orders_cache_key = f"user_orders:{user_id}"
        cached_orders = r.get(orders_cache_key)
        
        if cached_orders:
            print(f"   📦 User {user_id} orders: CACHE HIT - {cached_orders}")
        else:
            # Database query
            pg_cursor.execute("""
                SELECT product_name, quantity, price, status 
                FROM orders 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
            
            orders = pg_cursor.fetchall()
            orders_data = f"{len(orders)} orders"
            
            # Store in cache
            r.setex(orders_cache_key, 180, orders_data)  # 3 minutes TTL
            print(f"   📦 User {user_id} orders: CACHE MISS - {orders_data} (cached for 3min)")

        # Show cache statistics
        cache_info = r.info()
        print(f"\n📊 Cache Service Statistics:")
        print(f"   Memory Used: {cache_info['used_memory_human']}")
        print(f"   Keys in Cache: {r.dbsize()}")
        print(f"   Hit Rate: {cache_info.get('keyspace_hits', 0)} hits")

        pg_cursor.close()
        pg_conn.close()

def demo_container_communication():
    """Demonstrate container-to-container communication"""
    print("\n🔗 Container Communication Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ PostgreSQL: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Simulate message passing between services
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

        # Create event log table
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE event_log (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                service_name VARCHAR(50) NOT NULL,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Event Log Table Created")

        # Simulate event-driven architecture
        events = [
            ("user_registered", "user_service", "User alice@example.com registered"),
            ("order_created", "order_service", "Order #12345 created for user 1"),
            ("payment_processed", "payment_service", "Payment $299.99 processed for order #12345"),
            ("order_shipped", "shipping_service", "Order #12345 shipped to address"),
            ("email_sent", "notification_service", "Confirmation email sent to alice@example.com")
        ]

        print("📝 Simulating Event-Driven Communication:")
        for event_type, service, message in events:
            # Store event in database
            pg_cursor.execute(
                "INSERT INTO event_log (event_type, service_name, message) VALUES (%s, %s, %s)",
                (event_type, service, message)
            )
            
            # Publish event to Redis (message queue simulation)
            r.lpush("event_queue", f"{event_type}:{service}:{message}")
            
            print(f"   📤 {service}: {event_type} - {message}")

        pg_conn.commit()

        # Process events from queue
        print(f"\n📥 Processing Events from Queue:")
        event_count = 0
        while event_count < len(events):
            event = r.rpop("event_queue")
            if event:
                event_type, service, message = event.split(":", 2)
                print(f"   📥 Processed: {service} - {event_type}")
                event_count += 1

        # Show event statistics
        pg_cursor.execute("""
            SELECT service_name, COUNT(*) as event_count,
                   MIN(timestamp) as first_event,
                   MAX(timestamp) as last_event
            FROM event_log 
            GROUP BY service_name 
            ORDER BY event_count DESC
        """)

        results = pg_cursor.fetchall()
        print(f"\n📊 Event Statistics:")
        for service, count, first_event, last_event in results:
            print(f"   {service}: {count} events | First: {first_event} | Last: {last_event}")

        pg_cursor.close()
        pg_conn.close()

def demo_container_health_checks():
    """Demonstrate container health monitoring"""
    print("\n🏥 Container Health Monitoring Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ PostgreSQL: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Health check functions
        def check_postgres_health():
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
                return True, "Healthy"
            except Exception as e:
                return False, str(e)[:50]

        def check_redis_health():
            try:
                r = redis.Redis(
                    host=redis_container.get_container_host_ip(),
                    port=redis_container.get_exposed_port(6379),
                    decode_responses=True
                )
                r.ping()
                info = r.info()
                return True, f"Healthy - Memory: {info['used_memory_human']}"
            except Exception as e:
                return False, str(e)[:50]

        # Perform health checks
        print("🏥 Performing Health Checks:")
        
        pg_healthy, pg_status = check_postgres_health()
        redis_healthy, redis_status = check_redis_health()

        print(f"   🐘 PostgreSQL: {'✅' if pg_healthy else '❌'} {pg_status}")
        print(f"   🔴 Redis: {'✅' if redis_healthy else '❌'} {redis_status}")

        # Simulate health monitoring over time
        print(f"\n📊 Health Monitoring (5 checks):")
        for i in range(5):
            pg_healthy, pg_status = check_postgres_health()
            redis_healthy, redis_status = check_redis_health()
            
            timestamp = time.strftime("%H:%M:%S")
            print(f"   {timestamp} - PostgreSQL: {'✅' if pg_healthy else '❌'} | Redis: {'✅' if redis_healthy else '❌'}")
            
            if i < 4:  # Don't sleep on last iteration
                time.sleep(0.5)

        # Overall health status
        overall_healthy = pg_healthy and redis_healthy
        print(f"\n🏥 Overall System Health: {'✅ HEALTHY' if overall_healthy else '❌ UNHEALTHY'}")
        
        if overall_healthy:
            print("   All services are operational and ready to handle requests")
        else:
            print("   Some services are experiencing issues - check logs for details")

def main():
    """Run Lab 4 - Multiple Containers"""
    print("🚀 LAB 4: Multiple Containers - Working Examples")
    print("=" * 60)
    print("✨ Master multi-container orchestration with TestContainers!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_multi_container_basic()
        demo_microservices_simulation()
        demo_container_communication()
        demo_container_health_checks()
        
        print("\n✅ Lab 4 completed successfully!")
        print("Key concepts learned:")
        print("• Multi-container orchestration with TestContainers")
        print("• Cross-database operations and data synchronization")
        print("• Microservices simulation and service communication")
        print("• Event-driven architecture patterns")
        print("• Container health monitoring and management")
        print("\n💪 You're ready for intermediate scenarios!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()