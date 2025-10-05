#!/usr/bin/env python3
"""
Lab 9: Performance Testing - Chaos Scenarios
============================================

Experience performance chaos in production environments.
Learn how to handle performance degradation, bottlenecks, and system overload.
"""

import os
import sys
import time
import threading
import random
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

def chaos_performance_degradation():
    """Performance degradation chaos - what happens when systems slow down?"""
    print("\n💥 Performance Degradation Chaos...")
    print("🚨 What happens when systems slow down significantly?")
    
    try:
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
                CREATE TABLE performance_metrics (
                    id SERIAL PRIMARY KEY,
                    operation VARCHAR(50) NOT NULL,
                    response_time_ms INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Performance Metrics Table Created")
            
            # Simulate performance degradation
            print(f"\n🧪 Simulating Performance Degradation:")
            
            # Normal performance baseline
            print(f"\n   Baseline Performance:")
            baseline_operations = [
                ("select", 50),
                ("insert", 75),
                ("update", 80),
                ("delete", 60)
            ]
            
            for operation, response_time in baseline_operations:
                cursor.execute(
                    "INSERT INTO performance_metrics (operation, response_time_ms) VALUES (%s, %s)",
                    (operation, response_time)
                )
                print(f"      {operation}: {response_time}ms")
            
            # Gradual degradation
            print(f"\n   Gradual Performance Degradation:")
            degradation_levels = [1.5, 2.0, 3.0, 5.0, 10.0]
            
            for level in degradation_levels:
                print(f"      Degradation Level: {level}x")
                
                for operation, baseline_time in baseline_operations:
                    degraded_time = int(baseline_time * level)
                    cursor.execute(
                        "INSERT INTO performance_metrics (operation, response_time_ms) VALUES (%s, %s)",
                        (operation, degraded_time)
                    )
                    print(f"         {operation}: {degraded_time}ms ({level}x slower)")
                
                time.sleep(0.1)  # Simulate time passing
            
            conn.commit()
            
            # Analyze performance degradation
            print(f"\n📊 Performance Degradation Analysis:")
            
            cursor.execute("""
                SELECT operation, 
                       AVG(response_time_ms) as avg_response_time,
                       MAX(response_time_ms) as max_response_time,
                       COUNT(*) as measurements
                FROM performance_metrics
                GROUP BY operation
                ORDER BY avg_response_time DESC
            """)
            
            performance_analysis = cursor.fetchall()
            for operation, avg_time, max_time, measurements in performance_analysis:
                print(f"   {operation.upper()}:")
                print(f"      Avg Response Time: {avg_time:.1f}ms")
                print(f"      Max Response Time: {max_time}ms")
                print(f"      Measurements: {measurements}")
                
                if avg_time > 1000:
                    print(f"      🚨 CRITICAL: Performance severely degraded!")
                elif avg_time > 500:
                    print(f"      ⚠️  WARNING: Performance degraded!")
                elif avg_time > 200:
                    print(f"      ⚠️  CAUTION: Performance slightly degraded!")
                else:
                    print(f"      ✅ Performance acceptable!")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Performance degradation test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement performance monitoring and alerting!")

def chaos_memory_leaks():
    """Memory leak chaos - what happens when memory usage grows uncontrollably?"""
    print("\n💥 Memory Leak Chaos...")
    print("🚨 What happens when memory usage grows uncontrollably?")
    
    try:
        with RedisContainer("redis:7-alpine") as redis_container:
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )
            
            # Simulate memory leak scenarios
            print(f"\n🧪 Simulating Memory Leaks:")
            
            # Scenario 1: Unbounded data growth
            print(f"\n   Scenario 1: Unbounded Data Growth")
            for i in range(1000):
                # Store data without TTL (memory leak)
                r.set(f"leak_data_{i}", f"leak_value_{i}" * 100)  # Large values
                
                if i % 100 == 0:
                    info = r.info()
                    memory_used = info['used_memory_human']
                    print(f"      Stored {i} items, Memory: {memory_used}")
            
            # Scenario 2: Accumulating logs
            print(f"\n   Scenario 2: Accumulating Logs")
            for i in range(500):
                # Store logs without cleanup
                r.lpush("application_logs", f"Log entry {i}: {random.random()}")
                
                if i % 100 == 0:
                    log_count = r.llen("application_logs")
                    print(f"      Log entries: {log_count}")
            
            # Scenario 3: Session data accumulation
            print(f"\n   Scenario 3: Session Data Accumulation")
            for i in range(200):
                # Store session data without cleanup
                session_data = {
                    "user_id": i,
                    "session_id": f"sess_{i}",
                    "data": f"session_data_{i}" * 50
                }
                r.hset(f"session:{i}", mapping=session_data)
                
                if i % 50 == 0:
                    print(f"      Sessions stored: {i}")
            
            # Analyze memory usage
            print(f"\n📊 Memory Usage Analysis:")
            
            info = r.info()
            print(f"   Memory Used: {info['used_memory_human']}")
            print(f"   Memory Peak: {info['used_memory_peak_human']}")
            print(f"   Keys in DB: {r.dbsize()}")
            print(f"   Memory per Key: {info['used_memory'] / r.dbsize():.0f} bytes")
            
            # Check for memory pressure
            memory_usage = info['used_memory']
            max_memory = info.get('maxmemory', 0)
            
            if max_memory > 0:
                memory_percentage = (memory_usage / max_memory) * 100
                print(f"   Memory Usage: {memory_percentage:.1f}% of max memory")
                
                if memory_percentage > 90:
                    print(f"   🚨 CRITICAL: Memory usage critical!")
                elif memory_percentage > 80:
                    print(f"   ⚠️  WARNING: Memory usage high!")
                else:
                    print(f"   ✅ Memory usage acceptable!")
            
            # Test system behavior under memory pressure
            print(f"\n🧪 Testing System Behavior Under Memory Pressure:")
            
            try:
                r.ping()
                print(f"   ✅ Cache ping successful")
            except Exception as e:
                print(f"   ❌ Cache ping failed: {str(e)[:50]}")
            
            try:
                r.set("test_key", "test_value")
                print(f"   ✅ Cache write successful")
            except Exception as e:
                print(f"   ❌ Cache write failed: {str(e)[:50]}")
            
            try:
                r.get("test_key")
                print(f"   ✅ Cache read successful")
            except Exception as e:
                print(f"   ❌ Cache read failed: {str(e)[:50]}")
    
    except Exception as e:
        print(f"   💥 Memory leak test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement memory monitoring and cleanup strategies!")

def chaos_database_bottlenecks():
    """Database bottleneck chaos - what happens when databases become bottlenecks?"""
    print("\n💥 Database Bottleneck Chaos...")
    print("🚨 What happens when databases become performance bottlenecks?")
    
    try:
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
                CREATE TABLE bottleneck_test (
                    id SERIAL PRIMARY KEY,
                    data VARCHAR(100) NOT NULL,
                    value INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Bottleneck Test Table Created")
            
            # Simulate database bottlenecks
            print(f"\n🧪 Simulating Database Bottlenecks:")
            
            # Scenario 1: Lock contention
            print(f"\n   Scenario 1: Lock Contention")
            print(f"      Simulating concurrent updates on same row...")
            
            # Insert test data
            cursor.execute("INSERT INTO bottleneck_test (data, value) VALUES ('contention_test', 0)")
            conn.commit()
            
            # Simulate lock contention
            for i in range(10):
                try:
                    cursor.execute("UPDATE bottleneck_test SET value = value + 1 WHERE data = 'contention_test'")
                    conn.commit()
                    print(f"      Update {i+1}: Success")
                except Exception as e:
                    print(f"      Update {i+1}: Failed - {str(e)[:50]}")
            
            # Scenario 2: Long-running queries
            print(f"\n   Scenario 2: Long-running Queries")
            print(f"      Simulating expensive operations...")
            
            # Insert large dataset
            for i in range(1000):
                cursor.execute(
                    "INSERT INTO bottleneck_test (data, value) VALUES (%s, %s)",
                    (f"data_{i}", i)
                )
            
            conn.commit()
            print(f"      Inserted 1000 records")
            
            # Simulate expensive query
            start_time = time.time()
            cursor.execute("""
                SELECT data, value, created_at
                FROM bottleneck_test
                WHERE value > 500
                ORDER BY value DESC
                LIMIT 100
            """)
            results = cursor.fetchall()
            query_time = time.time() - start_time
            
            print(f"      Expensive query: {len(results)} results in {query_time:.3f}s")
            
            # Scenario 3: Connection pool exhaustion
            print(f"\n   Scenario 3: Connection Pool Exhaustion")
            print(f"      Simulating multiple concurrent connections...")
            
            def simulate_connection(conn_id):
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
                    return f"Connection {conn_id}: Success"
                except Exception as e:
                    return f"Connection {conn_id}: Failed - {str(e)[:30]}"
            
            # Simulate concurrent connections
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(simulate_connection, i) for i in range(20)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            successful_connections = [r for r in results if "Success" in r]
            failed_connections = [r for r in results if "Failed" in r]
            
            print(f"      Successful connections: {len(successful_connections)}")
            print(f"      Failed connections: {len(failed_connections)}")
            
            # Analyze bottleneck impact
            print(f"\n📊 Bottleneck Impact Analysis:")
            
            cursor.execute("SELECT COUNT(*) FROM bottleneck_test")
            total_records = cursor.fetchone()[0]
            print(f"   Total Records: {total_records}")
            
            cursor.execute("SELECT AVG(value) FROM bottleneck_test")
            avg_value = cursor.fetchone()[0]
            print(f"   Average Value: {avg_value:.2f}")
            
            cursor.execute("SELECT MAX(value) FROM bottleneck_test")
            max_value = cursor.fetchone()[0]
            print(f"   Max Value: {max_value}")
            
            # Test system behavior under bottleneck
            print(f"\n🧪 Testing System Behavior Under Bottleneck:")
            
            try:
                cursor.execute("SELECT 1")
                cursor.fetchone()
                print(f"   ✅ Simple query successful")
            except Exception as e:
                print(f"   ❌ Simple query failed: {str(e)[:50]}")
            
            try:
                cursor.execute("SELECT COUNT(*) FROM bottleneck_test")
                count = cursor.fetchone()[0]
                print(f"   ✅ Count query successful: {count} records")
            except Exception as e:
                print(f"   ❌ Count query failed: {str(e)[:50]}")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 Database bottleneck test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement query optimization and connection pooling!")

def chaos_system_overload():
    """System overload chaos - what happens when systems are overloaded?"""
    print("\n💥 System Overload Chaos...")
    print("🚨 What happens when systems are overloaded with requests?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             RedisContainer("redis:7-alpine") as redis_container:
            
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            # Setup systems
            conn = psycopg2.connect(
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
            
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE overload_test (
                    id SERIAL PRIMARY KEY,
                    request_id VARCHAR(50) NOT NULL,
                    response_time_ms INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Overload Test Table Created")
            
            # Simulate system overload
            print(f"\n🧪 Simulating System Overload:")
            
            # Scenario 1: Gradual load increase
            print(f"\n   Scenario 1: Gradual Load Increase")
            load_levels = [10, 25, 50, 100, 200, 500]
            
            for level in load_levels:
                print(f"      Load Level: {level} requests/second")
                
                # Simulate requests at this load level
                for i in range(level):
                    request_id = f"req_{level}_{i}"
                    
                    # Simulate response time based on load
                    if level < 50:
                        response_time = random.randint(50, 100)
                        status = "success"
                    elif level < 200:
                        response_time = random.randint(100, 500)
                        status = "success"
                    else:
                        response_time = random.randint(500, 2000)
                        status = "timeout" if random.random() < 0.3 else "success"
                    
                    cursor.execute(
                        "INSERT INTO overload_test (request_id, response_time_ms, status) VALUES (%s, %s, %s)",
                        (request_id, response_time, status)
                    )
                
                conn.commit()
                print(f"         Processed {level} requests")
            
            # Scenario 2: Sudden traffic spike
            print(f"\n   Scenario 2: Sudden Traffic Spike")
            spike_requests = 1000
            print(f"      Processing {spike_requests} requests simultaneously...")
            
            for i in range(spike_requests):
                request_id = f"spike_{i}"
                
                # Simulate system under extreme load
                if random.random() < 0.5:  # 50% success rate under extreme load
                    response_time = random.randint(1000, 5000)
                    status = "success"
                else:
                    response_time = random.randint(5000, 10000)
                    status = "failed"
                
                cursor.execute(
                    "INSERT INTO overload_test (request_id, response_time_ms, status) VALUES (%s, %s, %s)",
                    (request_id, response_time, status)
                )
            
            conn.commit()
            print(f"      Processed {spike_requests} spike requests")
            
            # Analyze overload impact
            print(f"\n📊 Overload Impact Analysis:")
            
            cursor.execute("""
                SELECT status, 
                       COUNT(*) as count,
                       AVG(response_time_ms) as avg_response_time,
                       MAX(response_time_ms) as max_response_time
                FROM overload_test
                GROUP BY status
                ORDER BY count DESC
            """)
            
            overload_analysis = cursor.fetchall()
            for status, count, avg_time, max_time in overload_analysis:
                print(f"   {status.upper()}:")
                print(f"      Count: {count}")
                print(f"      Avg Response Time: {avg_time:.1f}ms")
                print(f"      Max Response Time: {max_time}ms")
                
                if status == "success":
                    if avg_time > 2000:
                        print(f"      🚨 CRITICAL: Response times severely degraded!")
                    elif avg_time > 1000:
                        print(f"      ⚠️  WARNING: Response times degraded!")
                    else:
                        print(f"      ✅ Response times acceptable!")
                else:
                    print(f"      ❌ Requests failing under load!")
            
            # Test system recovery
            print(f"\n🧪 Testing System Recovery:")
            
            # Simulate load reduction
            print(f"   Reducing load to normal levels...")
            
            for i in range(10):
                request_id = f"recovery_{i}"
                response_time = random.randint(50, 100)
                status = "success"
                
                cursor.execute(
                    "INSERT INTO overload_test (request_id, response_time_ms, status) VALUES (%s, %s, %s)",
                    (request_id, response_time, status)
                )
            
            conn.commit()
            print(f"   System recovery: 10 requests processed successfully")
            
            cursor.close()
            conn.close()
    
    except Exception as e:
        print(f"   💥 System overload test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement load balancing and auto-scaling!")

def main():
    """Run Performance Testing Chaos Scenarios"""
    print("💥 LAB 9: PERFORMANCE TESTING CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world performance resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_performance_degradation()
        chaos_memory_leaks()
        chaos_database_bottlenecks()
        chaos_system_overload()
        
        print("\n🎉 PERFORMANCE TESTING CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Performance degradation happens - implement monitoring and alerting")
        print("• Memory leaks occur - implement cleanup and monitoring strategies")
        print("• Database bottlenecks are real - implement query optimization and connection pooling")
        print("• System overload happens - implement load balancing and auto-scaling")
        print("• Real-world performance issues are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for performance production chaos!")
        
    except Exception as e:
        print(f"❌ Performance testing chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
