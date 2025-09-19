#!/usr/bin/env python3
"""
Lab 2: Database Connections
===========================

Connect to different database types with TestContainers.
"""

import os

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

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
    exit(1)

def demo_postgres():
    """PostgreSQL connection demo"""
    print("🐘 PostgreSQL Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ Started on port {postgres.get_exposed_port(5432)}")
        
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
        print(f"📊 Version: {version.split()[1]}")
        
        # Create and test table
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✅ Created {count} users")
        
        cursor.close()
        conn.close()

def demo_mysql():
    """MySQL connection demo"""
    print("\n🐬 MySQL Demo")
    
    with MySqlContainer("mysql:8.0") as mysql:
        print(f"✅ Started on port {mysql.get_exposed_port(3306)}")
        
        conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"📊 Version: {version.split('-')[0]}")
        
        # Create and test table
        cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2)
            )
        """)
        
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("Laptop", 999.99))
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("Mouse", 29.99))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        print(f"✅ Created {count} products")
        
        cursor.close()
        conn.close()

def demo_redis():
    """Redis connection demo"""
    print("\n🔴 Redis Demo")
    
    with RedisContainer("redis:7-alpine") as redis_container:
        print(f"✅ Started on port {redis_container.get_exposed_port(6379)}")
        
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # Test operations
        r.set("test:key", "Hello TestContainers!")
        r.set("test:counter", 42)
        r.lpush("test:list", "item1", "item2", "item3")
        
        # Retrieve data
        value = r.get("test:key")
        counter = r.get("test:counter")
        list_items = r.lrange("test:list", 0, -1)
        
        print(f"📊 String: {value}")
        print(f"📊 Counter: {counter}")
        print(f"📊 List: {list_items}")

def demo_connection_patterns():
    """Show common connection patterns"""
    print("\n🔌 Connection Patterns Demo")
    
    # Pattern 1: Single database
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        print("✅ Single database connection")
        conn.close()
    
    # Pattern 2: Multiple databases
    with PostgresContainer("postgres:15-alpine") as pg, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        # Connect to all
        pg_conn = psycopg2.connect(
            host=pg.get_container_host_ip(),
            port=pg.get_exposed_port(5432),
            user=pg.username,
            password=pg.password,
            database=pg.dbname
        )
        
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        
        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        print("✅ Multi-database connection")
        
        pg_conn.close()
        mysql_conn.close()

def main():
    """Run Lab 2"""
    print("🔌 LAB 2: Database Connections")
    print("=" * 40)
    
    try:
        demo_postgres()
        demo_mysql()
        demo_redis()
        demo_connection_patterns()
        
        print("\n✅ Lab 2 completed!")
        print("Key concepts learned:")
        print("• PostgreSQL, MySQL, Redis connections")
        print("• Database-specific connection patterns")
        print("• Multi-database coordination")
        print("• Real database testing, not mocks")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()