#!/usr/bin/env python3
"""
Lab 8: Advanced Patterns
========================

Learn advanced TestContainers patterns including custom containers,
network testing, data persistence, and complex scenarios.
"""

import os
import time
import threading
import tempfile
import json

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis")
    exit(1)

def demo_custom_container():
    """Custom container patterns"""
    print("🔧 Custom Container Patterns")
    
    # Demonstrate custom container patterns using standard containers
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ Custom PostgreSQL container started on port {postgres.get_exposed_port(5432)}")
        
        # Show how to customize container behavior
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"📊 Container info: {version.split()[1]}")
        
        cursor.close()
        conn.close()
        
        print("✅ Custom container patterns demonstrated!")

def demo_data_persistence():
    """Data persistence patterns"""
    print("\n💾 Data Persistence Demo")
    
    # Create a temporary directory for data persistence
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Created temporary directory: {temp_dir}")
    
    try:
        # First container - create data
        with PostgresContainer("postgres:15-alpine") as postgres1:
            print("✅ First PostgreSQL container started")
            
            conn1 = psycopg2.connect(
                host=postgres1.get_container_host_ip(),
                port=postgres1.get_exposed_port(5432),
                user=postgres1.username,
                password=postgres1.password,
                database=postgres1.dbname
            )
            
            cursor1 = conn1.cursor()
            cursor1.execute("""
                CREATE TABLE persistent_data (
                    id SERIAL PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert test data
            test_messages = [
                "First message in container 1",
                "Second message in container 1",
                "Data should persist across containers"
            ]
            
            for message in test_messages:
                cursor1.execute("INSERT INTO persistent_data (message) VALUES (%s)", (message,))
            
            conn1.commit()
            
            # Export data to demonstrate persistence concept
            cursor1.execute("SELECT id, message FROM persistent_data ORDER BY id")
            data = cursor1.fetchall()
            
            # Save to file (simulating data export)
            data_file = os.path.join(temp_dir, "exported_data.json")
            with open(data_file, 'w') as f:
                json.dump([{"id": row[0], "message": row[1]} for row in data], f)
            
            print(f"📤 Exported {len(data)} records to file")
            
            cursor1.close()
            conn1.close()
        
        print("🔄 First container stopped, starting second container...")
        
        # Second container - simulate loading data
        with PostgresContainer("postgres:15-alpine") as postgres2:
            print("✅ Second PostgreSQL container started")
            
            conn2 = psycopg2.connect(
                host=postgres2.get_container_host_ip(),
                port=postgres2.get_exposed_port(5432),
                user=postgres2.username,
                password=postgres2.password,
                database=postgres2.dbname
            )
            
            cursor2 = conn2.cursor()
            cursor2.execute("""
                CREATE TABLE persistent_data (
                    id SERIAL PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Load data from file (simulating data import)
            with open(data_file, 'r') as f:
                imported_data = json.load(f)
            
            for record in imported_data:
                cursor2.execute("INSERT INTO persistent_data (message) VALUES (%s)", (record["message"],))
            
            conn2.commit()
            
            # Verify data was loaded
            cursor2.execute("SELECT COUNT(*) FROM persistent_data")
            count = cursor2.fetchone()[0]
            print(f"📥 Imported {count} records into new container")
            
            # Add new data to demonstrate independence
            cursor2.execute("INSERT INTO persistent_data (message) VALUES (%s)", ("New message in container 2",))
            conn2.commit()
            
            cursor2.execute("SELECT message FROM persistent_data ORDER BY id")
            all_messages = cursor2.fetchall()
            print(f"📊 Total messages in second container: {len(all_messages)}")
            
            cursor2.close()
            conn2.close()
    
    finally:
        # Cleanup
        if os.path.exists(data_file):
            os.remove(data_file)
        os.rmdir(temp_dir)
    
    print("✅ Data persistence demo completed!")

def demo_network_communication():
    """Network communication between containers"""
    print("\n🌐 Network Communication Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print("✅ PostgreSQL and Redis containers started")
        
        # Setup PostgreSQL
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        # Setup Redis
        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        print("🔌 Both containers connected")
        
        # Simulate cross-service communication
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE service_logs (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(50),
                action VARCHAR(100),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        pg_conn.commit()
        
        def log_action(service_name, action):
            """Log action to PostgreSQL"""
            pg_cursor.execute(
                "INSERT INTO service_logs (service_name, action) VALUES (%s, %s)",
                (service_name, action)
            )
            pg_conn.commit()
        
        def cache_result(key, value, ttl=300):
            """Cache result in Redis"""
            redis_client.setex(key, ttl, value)
            log_action("cache_service", f"Cached {key}")
        
        def get_cached_result(key):
            """Get cached result from Redis"""
            result = redis_client.get(key)
            if result:
                log_action("cache_service", f"Cache hit for {key}")
            else:
                log_action("cache_service", f"Cache miss for {key}")
            return result
        
        # Simulate service interactions
        print("🧪 Testing service interactions:")
        
        # Service A caches data
        cache_result("user:123", json.dumps({"name": "Alice", "email": "alice@example.com"}))
        print("📝 Service A cached user data")
        
        # Service B retrieves cached data
        cached_user = get_cached_result("user:123")
        if cached_user:
            user_data = json.loads(cached_user)
            print(f"📄 Service B retrieved user: {user_data['name']}")
        
        # Service C tries to get non-existent data
        missing_data = get_cached_result("user:999")
        print(f"❌ Service C cache miss: {missing_data is None}")
        
        # Multiple services log actions
        services = ["auth_service", "order_service", "notification_service"]
        actions = ["user_login", "order_created", "email_sent"]
        
        for service, action in zip(services, actions):
            log_action(service, action)
            print(f"✅ {service} logged: {action}")
        
        # Analyze service communication
        pg_cursor.execute("""
            SELECT service_name, COUNT(*) as action_count
            FROM service_logs
            GROUP BY service_name
            ORDER BY action_count DESC
        """)
        service_stats = pg_cursor.fetchall()
        
        print(f"📊 Service communication stats:")
        for service, count in service_stats:
            print(f"   {service}: {count} actions")
        
        # Check cache statistics
        cache_keys = redis_client.keys("*")
        print(f"   Redis: {len(cache_keys)} cached items")
        
        pg_cursor.close()
        pg_conn.close()
        
        print("✅ Network communication demo completed!")

def demo_concurrent_testing():
    """Concurrent database operations"""
    print("\n⚡ Concurrent Testing Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print("✅ PostgreSQL started for concurrent testing")
        
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
            CREATE TABLE concurrent_test (
                id SERIAL PRIMARY KEY,
                thread_id INTEGER,
                operation_id INTEGER,
                data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        
        print("📊 Database setup for concurrent testing")
        
        def worker_thread(thread_id, connection_params, operations=10):
            """Worker thread that performs database operations"""
            try:
                # Each thread gets its own connection
                thread_conn = psycopg2.connect(**connection_params)
                thread_cursor = thread_conn.cursor()
                
                for op_id in range(operations):
                    # Simulate some work
                    data = f"Thread {thread_id} operation {op_id} data"
                    
                    thread_cursor.execute("""
                        INSERT INTO concurrent_test (thread_id, operation_id, data)
                        VALUES (%s, %s, %s)
                    """, (thread_id, op_id, data))
                    
                    # Random delay to simulate real work
                    time.sleep(0.01)
                
                thread_conn.commit()
                thread_cursor.close()
                thread_conn.close()
                
                print(f"✅ Thread {thread_id} completed {operations} operations")
                
            except Exception as e:
                print(f"❌ Thread {thread_id} failed: {e}")
        
        # Connection parameters for threads
        connection_params = {
            'host': postgres.get_container_host_ip(),
            'port': postgres.get_exposed_port(5432),
            'user': postgres.username,
            'password': postgres.password,
            'database': postgres.dbname
        }
        
        print("🚀 Starting concurrent operations with 3 threads...")
        start_time = time.time()
        
        # Create and start threads
        threads = []
        for thread_id in range(3):
            thread = threading.Thread(
                target=worker_thread,
                args=(thread_id, connection_params, 10)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Analyze results
        final_conn = psycopg2.connect(**connection_params)
        final_cursor = final_conn.cursor()
        
        final_cursor.execute("SELECT COUNT(*) FROM concurrent_test")
        total_records = final_cursor.fetchone()[0]
        
        final_cursor.execute("""
            SELECT thread_id, COUNT(*) as operations
            FROM concurrent_test
            GROUP BY thread_id
            ORDER BY thread_id
        """)
        thread_stats = final_cursor.fetchall()
        
        print(f"📊 Concurrent testing results:")
        print(f"   Total time: {duration:.2f} seconds")
        print(f"   Total records: {total_records}")
        print(f"   Operations per second: {total_records / duration:.2f}")
        print(f"   Thread performance:")
        for thread_id, count in thread_stats:
            print(f"     Thread {thread_id}: {count} operations")
        
        final_cursor.close()
        final_conn.close()
        
        print("✅ Concurrent testing demo completed!")

def demo_health_checks():
    """Container health checks and monitoring"""
    print("\n🏥 Health Checks Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print("✅ Containers started for health monitoring")
        
        def check_postgres_health():
            """Check PostgreSQL health"""
            try:
                conn = psycopg2.connect(
                    host=postgres.get_container_host_ip(),
                    port=postgres.get_exposed_port(5432),
                    user=postgres.username,
                    password=postgres.password,
                    database=postgres.dbname,
                    connect_timeout=5
                )
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return {"status": "healthy", "response_time": "< 5s"}
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}
        
        def check_redis_health():
            """Check Redis health"""
            try:
                r = redis.Redis(
                    host=redis_container.get_container_host_ip(),
                    port=redis_container.get_exposed_port(6379),
                    socket_connect_timeout=5
                )
                start_time = time.time()
                r.ping()
                response_time = (time.time() - start_time) * 1000
                return {"status": "healthy", "response_time": f"{response_time:.2f}ms"}
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}
        
        def run_health_checks():
            """Run all health checks"""
            print("🔍 Running health checks...")
            
            pg_health = check_postgres_health()
            redis_health = check_redis_health()
            
            print(f"   PostgreSQL: {pg_health['status']}")
            if pg_health['status'] == 'healthy':
                print(f"     Response time: {pg_health['response_time']}")
            else:
                print(f"     Error: {pg_health['error']}")
            
            print(f"   Redis: {redis_health['status']}")
            if redis_health['status'] == 'healthy':
                print(f"     Response time: {redis_health['response_time']}")
            else:
                print(f"     Error: {redis_health['error']}")
            
            overall_status = "healthy" if all(
                h['status'] == 'healthy' for h in [pg_health, redis_health]
            ) else "degraded"
            
            print(f"   Overall system: {overall_status}")
            return overall_status
        
        # Monitor health over time
        print("🔄 Monitoring health over 6 seconds...")
        for i in range(3):
            status = run_health_checks()
            if i < 2:  # Don't sleep after last check
                time.sleep(2)
        
        print("✅ Health checks demo completed!")

def main():
    """Run Lab 8"""
    print("🎯 LAB 8: Advanced Patterns")
    print("=" * 40)
    
    try:
        demo_custom_container()
        demo_data_persistence()
        demo_network_communication()
        demo_concurrent_testing()
        demo_health_checks()
        
        print("\n✅ Lab 8 completed!")
        print("Key concepts learned:")
        print("• Custom container creation and configuration")
        print("• Data persistence patterns and strategies")
        print("• Network communication between containers")
        print("• Concurrent testing and thread safety")
        print("• Health checks and monitoring patterns")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()