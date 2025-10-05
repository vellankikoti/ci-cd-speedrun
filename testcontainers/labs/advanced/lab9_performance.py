#!/usr/bin/env python3
"""
Lab 9: Performance Testing - Working Examples
=============================================

Learn performance testing with TestContainers including load testing,
benchmarking, and optimization patterns.
"""

import os
import sys
import time
import threading
import concurrent.futures
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

def demo_database_performance():
    """Database performance testing with real data"""
    print("\n⚡ Database Performance Demo...")
    
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
            CREATE TABLE performance_test (
                id SERIAL PRIMARY KEY,
                data VARCHAR(100) NOT NULL,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Performance Test Table Created")
        
        # Test 1: Insert performance
        print(f"\n🧪 Test 1: Insert Performance")
        start_time = time.time()
        
        for i in range(1000):
            cursor.execute(
                "INSERT INTO performance_test (data, value) VALUES (%s, %s)",
                (f"test_data_{i}", i * 10)
            )
        
        conn.commit()
        insert_time = time.time() - start_time
        print(f"   📝 Inserted 1000 records in {insert_time:.3f}s")
        print(f"   📊 Rate: {1000/insert_time:.0f} records/second")
        
        # Test 2: Query performance
        print(f"\n🧪 Test 2: Query Performance")
        
        # Simple query
        start_time = time.time()
        cursor.execute("SELECT COUNT(*) FROM performance_test")
        count = cursor.fetchone()[0]
        simple_query_time = time.time() - start_time
        print(f"   📊 Simple Query: {count} records in {simple_query_time:.3f}s")
        
        # Complex query
        start_time = time.time()
        cursor.execute("""
            SELECT data, value, created_at 
            FROM performance_test 
            WHERE value > 5000 
            ORDER BY value DESC 
            LIMIT 100
        """)
        results = cursor.fetchall()
        complex_query_time = time.time() - start_time
        print(f"   📊 Complex Query: {len(results)} records in {complex_query_time:.3f}s")
        
        # Test 3: Concurrent access
        print(f"\n🧪 Test 3: Concurrent Access")
        
        def concurrent_query(thread_id):
            try:
                thread_conn = psycopg2.connect(
                    host=postgres.get_container_host_ip(),
                    port=postgres.get_exposed_port(5432),
                    user=postgres.username,
                    password=postgres.password,
                    database=postgres.dbname
                )
                thread_cursor = thread_conn.cursor()
                
                start_time = time.time()
                thread_cursor.execute("SELECT COUNT(*) FROM performance_test")
                count = thread_cursor.fetchone()[0]
                query_time = time.time() - start_time
                
                thread_cursor.close()
                thread_conn.close()
                
                return {"thread_id": thread_id, "count": count, "time": query_time}
            except Exception as e:
                return {"thread_id": thread_id, "error": str(e)}
        
        # Run 10 concurrent queries
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(concurrent_query, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        successful_queries = [r for r in results if "error" not in r]
        failed_queries = [r for r in results if "error" in r]
        
        print(f"   📊 Concurrent Queries: {len(successful_queries)} successful, {len(failed_queries)} failed")
        
        if successful_queries:
            avg_time = sum(r["time"] for r in successful_queries) / len(successful_queries)
            print(f"   📊 Average Query Time: {avg_time:.3f}s")
        
        cursor.close()
        conn.close()

def demo_redis_performance():
    """Redis performance testing with real data"""
    print("\n⚡ Redis Performance Demo...")
    
    with RedisContainer("redis:7-alpine") as redis_container:
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # Test 1: Set performance
        print(f"\n🧪 Test 1: Set Performance")
        start_time = time.time()
        
        for i in range(1000):
            r.set(f"key_{i}", f"value_{i}")
        
        set_time = time.time() - start_time
        print(f"   📝 Set 1000 keys in {set_time:.3f}s")
        print(f"   📊 Rate: {1000/set_time:.0f} operations/second")
        
        # Test 2: Get performance
        print(f"\n🧪 Test 2: Get Performance")
        start_time = time.time()
        
        for i in range(1000):
            r.get(f"key_{i}")
        
        get_time = time.time() - start_time
        print(f"   📖 Retrieved 1000 keys in {get_time:.3f}s")
        print(f"   📊 Rate: {1000/get_time:.0f} operations/second")
        
        # Test 3: Hash operations
        print(f"\n🧪 Test 3: Hash Operations")
        start_time = time.time()
        
        for i in range(1000):
            r.hset(f"hash_{i}", mapping={
                "field1": f"value1_{i}",
                "field2": f"value2_{i}",
                "field3": f"value3_{i}"
            })
        
        hash_time = time.time() - start_time
        print(f"   📝 Created 1000 hashes in {hash_time:.3f}s")
        print(f"   📊 Rate: {1000/hash_time:.0f} operations/second")
        
        # Test 4: Memory usage
        print(f"\n🧪 Test 4: Memory Usage")
        info = r.info()
        print(f"   💾 Memory Used: {info['used_memory_human']}")
        print(f"   📊 Keys in DB: {r.dbsize()}")
        print(f"   📊 Memory per Key: {info['used_memory'] / r.dbsize():.0f} bytes")

def demo_load_testing():
    """Load testing with concurrent operations"""
    print("\n⚡ Load Testing Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        # Setup databases
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
            CREATE TABLE load_test (
                id SERIAL PRIMARY KEY,
                data VARCHAR(100) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Load Test Table Created")
        
        # Load test function
        def load_test_worker(worker_id, operations):
            results = {"worker_id": worker_id, "operations": 0, "errors": 0, "times": []}
            
            try:
                # PostgreSQL operations
                pg_conn = psycopg2.connect(
                    host=postgres.get_container_host_ip(),
                    port=postgres.get_exposed_port(5432),
                    user=postgres.username,
                    password=postgres.password,
                    database=postgres.dbname
                )
                pg_cursor = pg_conn.cursor()
                
                # Redis operations
                redis_client = redis.Redis(
                    host=redis_container.get_container_host_ip(),
                    port=redis_container.get_exposed_port(6379),
                    decode_responses=True
                )
                
                for i in range(operations):
                    try:
                        start_time = time.time()
                        
                        # PostgreSQL operation
                        pg_cursor.execute(
                            "INSERT INTO load_test (data) VALUES (%s)",
                            (f"worker_{worker_id}_data_{i}",)
                        )
                        pg_conn.commit()
                        
                        # Redis operation
                        redis_client.set(f"worker_{worker_id}_key_{i}", f"value_{i}")
                        
                        operation_time = time.time() - start_time
                        results["times"].append(operation_time)
                        results["operations"] += 1
                        
                    except Exception as e:
                        results["errors"] += 1
                
                pg_cursor.close()
                pg_conn.close()
                
            except Exception as e:
                results["errors"] += 1
            
            return results
        
        # Run load test with different worker counts
        worker_counts = [5, 10, 20]
        
        for worker_count in worker_counts:
            print(f"\n🧪 Load Test with {worker_count} Workers")
            
            operations_per_worker = 50
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
                futures = [executor.submit(load_test_worker, i, operations_per_worker) for i in range(worker_count)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            total_time = time.time() - start_time
            
            total_operations = sum(r["operations"] for r in results)
            total_errors = sum(r["errors"] for r in results)
            all_times = [t for r in results for t in r["times"]]
            
            if all_times:
                avg_time = sum(all_times) / len(all_times)
                min_time = min(all_times)
                max_time = max(all_times)
            else:
                avg_time = min_time = max_time = 0
            
            print(f"   📊 Total Operations: {total_operations}")
            print(f"   📊 Total Errors: {total_errors}")
            print(f"   📊 Total Time: {total_time:.3f}s")
            print(f"   📊 Operations/Second: {total_operations/total_time:.0f}")
            print(f"   📊 Average Operation Time: {avg_time:.3f}s")
            print(f"   📊 Min Operation Time: {min_time:.3f}s")
            print(f"   📊 Max Operation Time: {max_time:.3f}s")
        
        cursor.close()
        pg_conn.close()

def demo_benchmarking():
    """Benchmarking different configurations"""
    print("\n⚡ Benchmarking Demo...")
    
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
            CREATE TABLE benchmark_test (
                id SERIAL PRIMARY KEY,
                data VARCHAR(100) NOT NULL,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Benchmark Test Table Created")
        
        # Benchmark different operations
        print(f"\n🧪 Benchmarking Different Operations:")
        
        # Insert benchmark
        start_time = time.time()
        for i in range(1000):
            cursor.execute(
                "INSERT INTO benchmark_test (data, value) VALUES (%s, %s)",
                (f"benchmark_data_{i}", i)
            )
        conn.commit()
        insert_time = time.time() - start_time
        print(f"   📝 Insert 1000 records: {insert_time:.3f}s ({1000/insert_time:.0f} ops/sec)")
        
        # Select benchmark
        start_time = time.time()
        cursor.execute("SELECT * FROM benchmark_test")
        results = cursor.fetchall()
        select_time = time.time() - start_time
        print(f"   📖 Select all records: {select_time:.3f}s ({len(results)/select_time:.0f} ops/sec)")
        
        # Update benchmark
        start_time = time.time()
        for i in range(1000):
            cursor.execute(
                "UPDATE benchmark_test SET value = %s WHERE id = %s",
                (i * 2, i + 1)
            )
        conn.commit()
        update_time = time.time() - start_time
        print(f"   📝 Update 1000 records: {update_time:.3f}s ({1000/update_time:.0f} ops/sec)")
        
        # Delete benchmark
        start_time = time.time()
        cursor.execute("DELETE FROM benchmark_test")
        conn.commit()
        delete_time = time.time() - start_time
        print(f"   🗑️ Delete all records: {delete_time:.3f}s")
        
        # Show performance summary
        print(f"\n📊 Performance Summary:")
        print(f"   Insert: {1000/insert_time:.0f} ops/sec")
        print(f"   Select: {len(results)/select_time:.0f} ops/sec")
        print(f"   Update: {1000/update_time:.0f} ops/sec")
        print(f"   Delete: {len(results)/delete_time:.0f} ops/sec")
        
        cursor.close()
        conn.close()

def main():
    """Run Lab 9 - Performance Testing"""
    print("🚀 LAB 9: Performance Testing - Working Examples")
    print("=" * 60)
    print("✨ Master performance testing with TestContainers!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_database_performance()
        demo_redis_performance()
        demo_load_testing()
        demo_benchmarking()
        
        print("\n✅ Lab 9 completed successfully!")
        print("Key concepts learned:")
        print("• Database performance testing with real data")
        print("• Redis performance testing and optimization")
        print("• Load testing with concurrent operations")
        print("• Benchmarking different configurations")
        print("• Performance analysis and optimization")
        print("\n💪 You're ready for real-world scenarios!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()