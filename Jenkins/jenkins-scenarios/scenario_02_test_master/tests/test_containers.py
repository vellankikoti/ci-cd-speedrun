#!/usr/bin/env python3
"""
Test Master - TestContainers Integration Tests
Real database testing with TestContainers.
"""

import pytest
import os
import sys
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from testcontainers.postgres import PostgresContainer
from testcontainers.mysql import MySqlContainer
from testcontainers.redis import RedisContainer
from database import DatabaseManager, User

def test_postgres():
    """Test with real PostgreSQL database using TestContainers."""
    print("\n🐘 Testing with PostgreSQL...")
    
    with PostgresContainer("postgres:13") as postgres:
        # Get connection details
        host = postgres.get_container_host_ip()
        port = postgres.get_exposed_port(5432)
        username = postgres.username
        password = postgres.password
        database = postgres.dbname
        
        print(f"PostgreSQL running at {host}:{port}")
        print(f"Database: {database}, User: {username}")
        
        # Test database operations
        # Note: In a real scenario, you'd configure your app to use this database
        # For this demo, we'll test the connection and basic operations
        
        import psycopg2
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ PostgreSQL version: {version}")
            
            # Test table creation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            
            # Test insert
            cursor.execute(
                "INSERT INTO test_users (name, email) VALUES (%s, %s)",
                ("Test User", "test@example.com")
            )
            
            # Test select
            cursor.execute("SELECT * FROM test_users WHERE email = %s", ("test@example.com",))
            result = cursor.fetchone()
            
            assert result is not None
            assert result[1] == "Test User"
            assert result[2] == "test@example.com"
            
            print("✅ PostgreSQL tests passed!")
            
        except Exception as e:
            print(f"❌ PostgreSQL test failed: {e}")
            raise
        finally:
            conn.close()

def test_mysql():
    """Test with real MySQL database using TestContainers."""
    print("\n🐬 Testing with MySQL...")
    
    with MySqlContainer("mysql:8.0") as mysql:
        # Get connection details
        host = mysql.get_container_host_ip()
        port = mysql.get_exposed_port(3306)
        username = mysql.username
        password = mysql.password
        database = mysql.dbname
        
        print(f"MySQL running at {host}:{port}")
        print(f"Database: {database}, User: {username}")
        
        # Test database operations
        import pymysql
        try:
            conn = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            print(f"✅ MySQL version: {version}")
            
            # Test table creation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            
            # Test insert
            cursor.execute(
                "INSERT INTO test_users (name, email) VALUES (%s, %s)",
                ("Test User", "test@example.com")
            )
            
            # Test select
            cursor.execute("SELECT * FROM test_users WHERE email = %s", ("test@example.com",))
            result = cursor.fetchone()
            
            assert result is not None
            assert result[1] == "Test User"
            assert result[2] == "test@example.com"
            
            print("✅ MySQL tests passed!")
            
        except Exception as e:
            print(f"❌ MySQL test failed: {e}")
            raise
        finally:
            conn.close()

def test_redis():
    """Test with real Redis database using TestContainers."""
    print("\n🔴 Testing with Redis...")
    
    with RedisContainer("redis:7-alpine") as redis:
        # Get connection details
        host = redis.get_container_host_ip()
        port = redis.get_exposed_port(6379)
        
        print(f"Redis running at {host}:{port}")
        
        # Test Redis operations
        import redis
        try:
            r = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Test basic operations
            r.set("test_key", "test_value")
            value = r.get("test_key")
            assert value == "test_value"
            
            # Test hash operations
            r.hset("test_hash", "field1", "value1")
            r.hset("test_hash", "field2", "value2")
            
            hash_data = r.hgetall("test_hash")
            assert hash_data["field1"] == "value1"
            assert hash_data["field2"] == "value2"
            
            # Test list operations
            r.lpush("test_list", "item1", "item2", "item3")
            list_length = r.llen("test_list")
            assert list_length == 3
            
            # Test set operations
            r.sadd("test_set", "member1", "member2", "member3")
            set_members = r.smembers("test_set")
            assert len(set_members) == 3
            
            print("✅ Redis tests passed!")
            
        except Exception as e:
            print(f"❌ Redis test failed: {e}")
            raise

def test_parallel_containers():
    """Test running multiple containers in parallel."""
    print("\n🚀 Testing parallel containers...")
    
    import threading
    import time
    
    results = {}
    
    def test_postgres_parallel():
        try:
            with PostgresContainer("postgres:13") as postgres:
                time.sleep(1)  # Simulate some work
                results['postgres'] = 'success'
        except Exception as e:
            results['postgres'] = f'error: {e}'
    
    def test_mysql_parallel():
        try:
            with MySqlContainer("mysql:8.0") as mysql:
                time.sleep(1)  # Simulate some work
                results['mysql'] = 'success'
        except Exception as e:
            results['mysql'] = f'error: {e}'
    
    def test_redis_parallel():
        try:
            with RedisContainer("redis:7-alpine") as redis:
                time.sleep(1)  # Simulate some work
                results['redis'] = 'success'
        except Exception as e:
            results['redis'] = f'error: {e}'
    
    # Start all tests in parallel
    threads = [
        threading.Thread(target=test_postgres_parallel),
        threading.Thread(target=test_mysql_parallel),
        threading.Thread(target=test_redis_parallel)
    ]
    
    start_time = time.time()
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Parallel tests completed in {duration:.2f} seconds")
    print(f"Results: {results}")
    
    # Verify all tests passed
    for db, result in results.items():
        assert result == 'success', f"{db} test failed: {result}"

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
