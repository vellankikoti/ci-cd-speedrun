#!/usr/bin/env python3
"""
Lab 2: Database Connections - Chaos Scenarios
=============================================

Experience database connection chaos in production environments.
Learn how to handle connection failures, timeouts, and multi-database issues.
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
        'pymysql': 'pymysql',
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
    from testcontainers.mysql import MySqlContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import pymysql
    import redis
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary pymysql redis")
    sys.exit(1)

def chaos_connection_timeouts():
    """Connection timeout chaos - what happens when connections fail?"""
    print("\n💥 Connection Timeout Chaos...")
    print("🚨 What happens when database connections timeout?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            
            # Test different connection scenarios
            connection_tests = [
                ("Normal Connection", 5, "postgresql://test:test@localhost:5432/test"),
                ("Short Timeout", 1, "postgresql://test:test@localhost:5432/test"),
                ("Wrong Port", 5, "postgresql://test:test@localhost:9999/test"),
                ("Wrong Database", 5, "postgresql://test:test@localhost:5432/wrongdb")
            ]
            
            print("\n🧪 Testing Connection Scenarios:")
            for test_name, timeout, connection_string in connection_tests:
                try:
                    start_time = time.time()
                    conn = psycopg2.connect(
                        host=postgres.get_container_host_ip(),
                        port=postgres.get_exposed_port(5432),
                        user=postgres.username,
                        password=postgres.password,
                        database=postgres.dbname,
                        connect_timeout=timeout
                    )
                    end_time = time.time()
                    conn.close()
                    print(f"   ✅ {test_name}: Connected in {end_time - start_time:.2f}s")
                except Exception as e:
                    end_time = time.time()
                    error_msg = str(e).split('\n')[0]
                    print(f"   ❌ {test_name}: Failed after {end_time - start_time:.2f}s - {error_msg}")
            
    except Exception as e:
        print(f"   💥 Connection test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Always handle connection timeouts gracefully!")

def chaos_concurrent_connections():
    """Concurrent connection chaos - connection pool issues"""
    print("\n💥 Concurrent Connection Chaos...")
    print("🚨 What happens with multiple concurrent connections?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            
            # Test concurrent connections
            import threading
            import queue
            
            results = queue.Queue()
            errors = queue.Queue()
            
            def connection_worker(worker_id, results, errors):
                try:
                    conn = psycopg2.connect(
                        host=postgres.get_container_host_ip(),
                        port=postgres.get_exposed_port(5432),
                        user=postgres.username,
                        password=postgres.password,
                        database=postgres.dbname
                    )
                    
                    cursor = conn.cursor()
                    cursor.execute("SELECT current_user, current_database()")
                    user, db = cursor.fetchone()
                    
                    # Simulate work
                    time.sleep(0.1)
                    
                    cursor.execute("SELECT COUNT(*) FROM pg_stat_activity")
                    active_connections = cursor.fetchone()[0]
                    
                    results.put(f"Worker {worker_id}: {user}@{db} (Active: {active_connections})")
                    
                    cursor.close()
                    conn.close()
                    
                except Exception as e:
                    errors.put(f"Worker {worker_id}: {str(e)[:50]}")
            
            print("\n🧪 Testing Concurrent Connections:")
            threads = []
            
            # Start 10 concurrent connections
            for i in range(10):
                thread = threading.Thread(target=connection_worker, args=(i+1, results, errors))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Show results
            print("   📊 Successful Connections:")
            while not results.empty():
                print(f"   ✅ {results.get()}")
            
            print("   ❌ Failed Connections:")
            while not errors.empty():
                print(f"   💥 {errors.get()}")
            
    except Exception as e:
        print(f"   💥 Concurrent connection test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Monitor connection pools and handle concurrency!")

def chaos_database_version_conflicts():
    """Database version conflicts - different versions behave differently"""
    print("\n💥 Database Version Conflicts...")
    print("🚨 Different database versions have different behaviors!")
    
    # Test PostgreSQL versions
    postgres_versions = [
        ("postgres:13-alpine", "PostgreSQL 13"),
        ("postgres:15-alpine", "PostgreSQL 15")
    ]
    
    print("\n🧪 Testing PostgreSQL Version Differences:")
    for version, name in postgres_versions:
        try:
            with PostgresContainer(version) as postgres:
                conn = psycopg2.connect(
                    host=postgres.get_container_host_ip(),
                    port=postgres.get_exposed_port(5432),
                    user=postgres.username,
                    password=postgres.password,
                    database=postgres.dbname
                )
                
                cursor = conn.cursor()
                
                # Get version info
                cursor.execute("SELECT version()")
                version_info = cursor.fetchone()[0]
                version_num = version_info.split()[1]
                
                # Test features that might differ
                features = {}
                
                # JSONB features
                try:
                    cursor.execute("SELECT jsonb_build_object('test', 'value')")
                    features['JSONB'] = "✅"
                except:
                    features['JSONB'] = "❌"
                
                # Window functions
                try:
                    cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY 1)")
                    features['Window'] = "✅"
                except:
                    features['Window'] = "❌"
                
                # Array functions
                try:
                    cursor.execute("SELECT ARRAY[1,2,3] && ARRAY[3,4,5]")
                    features['Arrays'] = "✅"
                except:
                    features['Arrays'] = "❌"
                
                print(f"   🔍 {name} ({version_num}):")
                for feature, status in features.items():
                    print(f"      {feature}: {status}")
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            print(f"   💥 {name}: Failed - {str(e)[:50]}")
    
    # Test MySQL versions
    mysql_versions = [
        ("mysql:5.7", "MySQL 5.7"),
        ("mysql:8.0", "MySQL 8.0")
    ]
    
    print(f"\n🧪 Testing MySQL Version Differences:")
    for version, name in mysql_versions:
        try:
            with MySqlContainer(version) as mysql:
                conn = pymysql.connect(
                    host=mysql.get_container_host_ip(),
                    port=mysql.get_exposed_port(3306),
                    user=mysql.username,
                    password=mysql.password,
                    database=mysql.dbname
                )
                
                cursor = conn.cursor()
                
                # Get version info
                cursor.execute("SELECT VERSION()")
                version_info = cursor.fetchone()[0]
                version_parts = version_info.split('-')
                version_num = version_parts[0] if version_parts else version_info
                
                # Test features that might differ
                features = {}
                
                # JSON support
                try:
                    cursor.execute("SELECT JSON_OBJECT('test', 'value')")
                    features['JSON'] = "✅"
                except:
                    features['JSON'] = "❌"
                
                # Window functions
                try:
                    cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY 1)")
                    features['Window'] = "✅"
                except:
                    features['Window'] = "❌"
                
                # CTE support
                try:
                    cursor.execute("WITH test AS (SELECT 1) SELECT * FROM test")
                    features['CTE'] = "✅"
                except:
                    features['CTE'] = "❌"
                
                print(f"   🔍 {name} ({version_num}):")
                for feature, status in features.items():
                    print(f"      {feature}: {status}")
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            print(f"   💥 {name}: Failed - {str(e)[:50]}")
    
    print(f"\n⚠️  Real-world lesson: Test with your production database versions!")

def chaos_redis_memory_issues():
    """Redis memory and performance chaos"""
    print("\n💥 Redis Memory Chaos...")
    print("🚨 What happens when Redis runs out of memory?")
    
    try:
        with RedisContainer("redis:7-alpine") as redis_container:
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
            
            r = redis.Redis(
                host=redis_container.get_container_host_ip(),
                port=redis_container.get_exposed_port(6379),
                decode_responses=True
            )
            
            # Get initial memory info
            info = r.info()
            print(f"📊 Initial Memory: {info['used_memory_human']} / {info['maxmemory_human']}")
            
            # Try to fill up memory with large data
            print(f"\n🧪 Testing Memory Limits:")
            large_data = "x" * 1024  # 1KB string
            
            successful_sets = 0
            failed_sets = 0
            
            for i in range(1000):  # Try to set 1000 keys
                try:
                    key = f"large_data:{i}"
                    r.set(key, large_data, ex=60)  # 1 minute TTL
                    successful_sets += 1
                    
                    if i % 100 == 0:
                        info = r.info()
                        print(f"   📊 Set {i} keys: {info['used_memory_human']} used")
                        
                except redis.exceptions.ResponseError as e:
                    if "OOM" in str(e):
                        failed_sets += 1
                        print(f"   ❌ Out of Memory at key {i}: {str(e)[:50]}")
                        break
                    else:
                        raise
            
            # Show final stats
            info = r.info()
            print(f"\n📊 Final Memory Stats:")
            print(f"   Successful sets: {successful_sets}")
            print(f"   Failed sets: {failed_sets}")
            print(f"   Memory used: {info['used_memory_human']}")
            print(f"   Keys in DB: {r.dbsize()}")
            
            # Test key expiration
            print(f"\n⏰ Testing Key Expiration:")
            r.set("test_key", "test_value", ex=2)  # 2 second TTL
            print(f"   Key set with 2s TTL")
            
            time.sleep(1)
            ttl = r.ttl("test_key")
            print(f"   TTL after 1s: {ttl}s")
            
            time.sleep(2)
            exists = r.exists("test_key")
            print(f"   Key exists after 3s: {'Yes' if exists else 'No'}")
            
    except Exception as e:
        print(f"   💥 Redis memory test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Monitor Redis memory usage and set appropriate limits!")

def main():
    """Run Database Connection Chaos Scenarios"""
    print("💥 LAB 2: DATABASE CONNECTION CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world database resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_connection_timeouts()
        chaos_concurrent_connections()
        chaos_database_version_conflicts()
        chaos_redis_memory_issues()
        
        print("\n🎉 DATABASE CONNECTION CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Connection timeouts happen - handle them gracefully")
        print("• Concurrent connections need proper management")
        print("• Database versions behave differently - test with production versions")
        print("• Memory limits matter - monitor Redis and other databases")
        print("• Real-world database issues are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for database production chaos!")
        
    except Exception as e:
        print(f"❌ Database chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
