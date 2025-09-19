#!/usr/bin/env python3
"""
Lab 9: Performance Testing (Simple Version)
===========================================

Learn how to performance test your database applications
with TestContainers and realistic data loads.
"""

import os
import time

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

import threading
import random

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("Please run: python3 setup.py from testcontainers directory")
    exit(1)

def print_header():
    """Print lab header"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                🚀 LAB 9: PERFORMANCE TESTING 🚀                ║
║                                                                  ║
║  Learn how to performance test database applications             ║
║  with realistic loads and concurrent operations.                ║
╚══════════════════════════════════════════════════════════════════╝
""")

def demo_database_load_testing():
    """Demo database load testing"""
    print("\n📊 Database Load Testing Demo")
    print("=" * 50)

    with PostgresContainer("postgres:15-alpine") as postgres:
        print("✅ PostgreSQL started for load testing")

        # Connect to database
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        # Setup test table
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE test_performance (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        print("📈 Running load test with 1000 inserts...")

        start_time = time.time()

        # Insert test data
        for i in range(1000):
            cursor.execute(
                "INSERT INTO test_performance (name, data) VALUES (%s, %s)",
                (f"User {i}", f"Test data for user {i} " * 10)
            )

            if i % 100 == 0:
                conn.commit()
                print(f"   ✅ Inserted {i} records...")

        conn.commit()
        end_time = time.time()

        # Performance results
        duration = end_time - start_time
        records_per_second = 1000 / duration

        print(f"\n📊 Performance Results:")
        print(f"   Total time: {duration:.2f} seconds")
        print(f"   Records per second: {records_per_second:.2f}")
        print(f"   Average time per insert: {(duration * 1000) / 1000:.2f} ms")

        # Test query performance
        print("\n🔍 Testing query performance...")
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM test_performance")
        count = cursor.fetchone()[0]
        end_time = time.time()

        print(f"   Query time: {(end_time - start_time) * 1000:.2f} ms")
        print(f"   Total records: {count}")

        cursor.close()
        conn.close()

        print("✅ Database load testing completed!")

def demo_concurrent_operations():
    """Demo concurrent database operations"""
    print("\n🔄 Concurrent Operations Demo")
    print("=" * 50)

    with PostgresContainer("postgres:15-alpine") as postgres:
        print("✅ PostgreSQL started for concurrent testing")

        def worker_function(worker_id, connection_params):
            """Worker function for concurrent operations"""
            try:
                conn = psycopg2.connect(**connection_params)
                cursor = conn.cursor()

                # Each worker inserts 50 records
                for i in range(50):
                    cursor.execute(
                        "INSERT INTO concurrent_test (worker_id, record_id, data) VALUES (%s, %s, %s)",
                        (worker_id, i, f"Data from worker {worker_id}, record {i}")
                    )

                conn.commit()
                cursor.close()
                conn.close()
                print(f"   ✅ Worker {worker_id} completed")

            except Exception as e:
                print(f"   ❌ Worker {worker_id} failed: {e}")

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
                worker_id INTEGER,
                record_id INTEGER,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

        # Connection parameters for workers
        connection_params = {
            'host': postgres.get_container_host_ip(),
            'port': postgres.get_exposed_port(5432),
            'user': postgres.username,
            'password': postgres.password,
            'database': postgres.dbname
        }

        print("🚀 Starting 5 concurrent workers...")
        start_time = time.time()

        # Create and start worker threads
        threads = []
        for worker_id in range(5):
            thread = threading.Thread(
                target=worker_function,
                args=(worker_id, connection_params)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()

        # Check results
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM concurrent_test")
        total_records = cursor.fetchone()[0]

        cursor.execute("SELECT worker_id, COUNT(*) FROM concurrent_test GROUP BY worker_id ORDER BY worker_id")
        worker_stats = cursor.fetchall()

        print(f"\n📊 Concurrent Operations Results:")
        print(f"   Total time: {end_time - start_time:.2f} seconds")
        print(f"   Total records inserted: {total_records}")
        print(f"   Records per worker:")
        for worker_id, count in worker_stats:
            print(f"     Worker {worker_id}: {count} records")

        cursor.close()
        conn.close()

        print("✅ Concurrent operations testing completed!")

def demo_redis_performance():
    """Demo Redis performance testing"""
    print("\n⚡ Redis Performance Demo")
    print("=" * 50)

    with RedisContainer("redis:7-alpine") as redis_container:
        print("✅ Redis started for performance testing")

        # Connect to Redis
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        print("📈 Testing Redis SET operations...")

        start_time = time.time()

        # Test SET operations
        for i in range(1000):
            r.set(f"key:{i}", f"value_{i}_{'x' * 100}")

            if i % 200 == 0:
                print(f"   ✅ Set {i} keys...")

        end_time = time.time()
        set_duration = end_time - start_time

        print("📈 Testing Redis GET operations...")

        start_time = time.time()

        # Test GET operations
        for i in range(1000):
            value = r.get(f"key:{i}")

            if i % 200 == 0:
                print(f"   ✅ Got {i} keys...")

        end_time = time.time()
        get_duration = end_time - start_time

        # Test pipeline operations
        print("📈 Testing Redis pipeline operations...")

        start_time = time.time()

        pipe = r.pipeline()
        for i in range(1000):
            pipe.set(f"pipe_key:{i}", f"pipe_value_{i}")

        pipe.execute()
        end_time = time.time()
        pipeline_duration = end_time - start_time

        print(f"\n📊 Redis Performance Results:")
        print(f"   SET operations: {set_duration:.2f}s ({1000/set_duration:.0f} ops/sec)")
        print(f"   GET operations: {get_duration:.2f}s ({1000/get_duration:.0f} ops/sec)")
        print(f"   Pipeline operations: {pipeline_duration:.2f}s ({1000/pipeline_duration:.0f} ops/sec)")
        print(f"   Pipeline speedup: {set_duration/pipeline_duration:.1f}x faster")

        print("✅ Redis performance testing completed!")

def main():
    """Run Lab 9"""
    print_header()

    try:
        demo_database_load_testing()
        time.sleep(1)

        demo_concurrent_operations()
        time.sleep(1)

        demo_redis_performance()

        print("\n" + "=" * 60)
        print("🎉 LAB 9 COMPLETED!")
        print("=" * 60)
        print("\nWhat you learned:")
        print("✅ Database load testing techniques")
        print("✅ Concurrent operations and thread safety")
        print("✅ Redis performance optimization")
        print("✅ Performance measurement and benchmarking")
        print("✅ Real-world performance testing patterns")

        print("\n🚀 Congratulations! You've completed all TestContainers labs!")
        print("    You're now ready to test production-grade applications!")

        return True

    except Exception as e:
        print(f"\n❌ Lab failed: {e}")
        print("Make sure Docker is running and try again.")
        return False

if __name__ == "__main__":
    main()