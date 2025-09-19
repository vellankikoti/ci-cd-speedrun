#!/usr/bin/env python3
"""
Lab 4: Multiple Containers
==========================

Learn to orchestrate multiple containers together with TestContainers.
"""

import os
import time

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

def demo_multi_container():
    """Multiple containers working together"""
    print("🔄 Multi-Container Orchestration")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print("✅ Both containers started:")
        print(f"   PostgreSQL: port {postgres.get_exposed_port(5432)}")
        print(f"   Redis: port {redis_container.get_exposed_port(6379)}")

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

        # Setup data in PostgreSQL
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        users = [
            ("Alice Johnson", "alice@example.com"),
            ("Bob Smith", "bob@example.com"),
            ("Carol Davis", "carol@example.com")
        ]

        for name, email in users:
            pg_cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))

        pg_conn.commit()

        # Cache sessions in Redis
        for i, (name, email) in enumerate(users, 1):
            session_key = f"user:{i}:session"
            r.set(session_key, f"active:{name.lower().replace(' ', '_')}")
            r.expire(session_key, 3600)  # 1 hour expiry

        print("📊 Data stored in both databases:")

        # Query PostgreSQL
        pg_cursor.execute("SELECT id, name, email FROM users")
        pg_users = pg_cursor.fetchall()
        print(f"   PostgreSQL: {len(pg_users)} users")
        for user_id, name, email in pg_users:
            print(f"     {user_id}: {name} ({email})")

        # Query Redis
        redis_keys = r.keys("user:*:session")
        print(f"   Redis: {len(redis_keys)} sessions")
        for key in redis_keys:
            session_data = r.get(key)
            ttl = r.ttl(key)
            print(f"     {key}: {session_data} (expires in {ttl}s)")

        # Cross-database operations
        print("\n🔄 Cross-database operations:")
        pg_cursor.execute("SELECT id, name FROM users WHERE name = %s", ("Alice Johnson",))
        user = pg_cursor.fetchone()
        if user:
            user_id, name = user
            session_key = f"user:{user_id}:session"
            session = r.get(session_key)
            print(f"   User '{name}' (ID: {user_id}) has session: {session}")

        # Update session data
        r.set(f"user:{user_id}:last_activity", time.time())
        print(f"   Updated last activity for user {user_id}")

        pg_cursor.close()
        pg_conn.close()

def demo_sequential_containers():
    """Sequential container usage patterns"""
    print("\n🔄 Sequential Container Usage")
    
    # Phase 1: PostgreSQL data processing
    print("1️⃣ Phase 1: PostgreSQL data processing")
    user_data = []

    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE sales (
                id SERIAL PRIMARY KEY,
                product VARCHAR(100),
                amount DECIMAL(10,2),
                user_id INTEGER
            )
        """)

        sales_data = [
            ("Laptop", 999.99, 1),
            ("Mouse", 29.99, 1),
            ("Keyboard", 79.99, 2),
            ("Monitor", 299.99, 2),
            ("Headphones", 149.99, 3)
        ]

        for product, amount, user_id in sales_data:
            cursor.execute("INSERT INTO sales (product, amount, user_id) VALUES (%s, %s, %s)",
                         (product, amount, user_id))

        conn.commit()

        # Process data
        cursor.execute("SELECT user_id, SUM(amount) as total FROM sales GROUP BY user_id")
        user_totals = cursor.fetchall()

        for user_id, total in user_totals:
            user_data.append({"user_id": user_id, "total_spent": float(total)})

        print(f"   📊 Processed {len(user_data)} user spending totals")

        cursor.close()
        conn.close()

    # Phase 2: Redis caching
    print("2️⃣ Phase 2: Redis caching")
    with RedisContainer("redis:7-alpine") as redis_container:
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Cache processed data
        for user in user_data:
            cache_key = f"user_spending:{user['user_id']}"
            r.set(cache_key, user['total_spent'])
            r.expire(cache_key, 300)  # 5 minutes

        print(f"   💾 Cached spending data for {len(user_data)} users")

        # Verify cached data
        print("   📋 Cached data verification:")
        for user in user_data:
            cache_key = f"user_spending:{user['user_id']}"
            cached_value = r.get(cache_key)
            print(f"     User {user['user_id']}: ${cached_value}")

def demo_data_pipeline():
    """Data pipeline with multiple containers"""
    print("\n🔄 Data Pipeline Demo")
    
    # Step 1: Extract data from PostgreSQL
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE raw_data (
                id SERIAL PRIMARY KEY,
                category VARCHAR(50),
                value DECIMAL(10,2),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert sample data
        raw_data = [
            ("electronics", 100.00),
            ("books", 25.50),
            ("electronics", 150.75),
            ("clothing", 75.25),
            ("books", 30.00)
        ]

        for category, value in raw_data:
            cursor.execute("INSERT INTO raw_data (category, value) VALUES (%s, %s)", (category, value))

        conn.commit()

        # Extract aggregated data
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(value) as avg_value, SUM(value) as total_value
            FROM raw_data
            GROUP BY category
        """)
        aggregated_data = cursor.fetchall()

        print(f"   📊 Extracted {len(aggregated_data)} categories from PostgreSQL")
        for category, count, avg_val, total_val in aggregated_data:
            print(f"     {category}: {count} items, avg ${avg_val:.2f}, total ${total_val:.2f}")

        cursor.close()
        conn.close()

    # Step 2: Transform and load into Redis
    with RedisContainer("redis:7-alpine") as redis_container:
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Store aggregated data in Redis
        for category, count, avg_val, total_val in aggregated_data:
            r.hset(f"stats:{category}", mapping={
                "count": str(count),
                "avg_value": str(float(avg_val)),
                "total_value": str(float(total_val))
            })

        print(f"   💾 Loaded {len(aggregated_data)} categories into Redis")

        # Verify data in Redis
        print("   📋 Redis data verification:")
        for category, _, _, _ in aggregated_data:
            stats = r.hgetall(f"stats:{category}")
            print(f"     {category}: {stats}")

def main():
    """Run Lab 4"""
    print("🔄 LAB 4: Multiple Containers")
    print("=" * 40)
    
    try:
        demo_multi_container()
        demo_sequential_containers()
        demo_data_pipeline()
        
        print("\n✅ Lab 4 completed!")
        print("Key concepts learned:")
        print("• Multi-container orchestration")
        print("• Cross-database operations")
        print("• Sequential container patterns")
        print("• Data processing pipelines")
        print("• Real-world multi-service testing")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()