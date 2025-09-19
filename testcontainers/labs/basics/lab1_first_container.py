#!/usr/bin/env python3
"""
Lab 1: Your First Container
===========================

Learn TestContainers fundamentals with a real PostgreSQL database.
"""

import os
import time

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    import psycopg2
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary")
    exit(1)

def demo_basic_container():
    """Basic container lifecycle demo"""
    print("🚀 Starting PostgreSQL container...")
    start_time = time.time()
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ Started in {time.time() - start_time:.2f}s")
        print(f"   Host: {postgres.get_container_host_ip()}")
        print(f"   Port: {postgres.get_exposed_port(5432)}")
        print(f"   Database: {postgres.dbname}")

def demo_database_operations():
    """Database operations demo"""
    print("\n🔌 Database Operations Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        # Connect
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert data
        users = [
            ("Alice Johnson", "alice@example.com"),
            ("Bob Smith", "bob@example.com"),
            ("Carol Davis", "carol@example.com")
        ]
        
        for name, email in users:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
        
        conn.commit()
        
        # Query data
        cursor.execute("SELECT id, name, email FROM users ORDER BY id")
        rows = cursor.fetchall()
        
        print("📊 Users:")
        for row in rows:
            print(f"   {row[0]}: {row[1]} ({row[2]})")
        
        # Complex query
        cursor.execute("""
            SELECT 
                COUNT(*) as total_users,
                COUNT(DISTINCT SUBSTRING(email FROM '@(.*)')) as unique_domains
            FROM users
        """)
        stats = cursor.fetchone()
        print(f"📈 Total: {stats[0]} users, {stats[1]} domains")
        
        cursor.close()
        conn.close()

def demo_version_comparison():
    """Compare different PostgreSQL versions"""
    print("\n🔄 Version Comparison Demo")
    
    versions = ["postgres:14-alpine", "postgres:15-alpine"]
    
    for version in versions:
        with PostgresContainer(version) as postgres:
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version_info = cursor.fetchone()[0]
            print(f"✅ {version}: {version_info.split()[1]}")
            
            cursor.close()
            conn.close()

def challenge_solution():
    """Product management challenge solution"""
    print("\n🏆 Challenge: Product Management System")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(50) NOT NULL
            )
        """)
        
        # Insert products
        products = [
            ("Laptop", 999.99, "Electronics"),
            ("Coffee Mug", 12.99, "Kitchen"),
            ("Book", 24.99, "Education"),
            ("Headphones", 199.99, "Electronics"),
            ("Notebook", 8.99, "Office")
        ]
        
        for name, price, category in products:
            cursor.execute(
                "INSERT INTO products (name, price, category) VALUES (%s, %s, %s)",
                (name, price, category)
            )
        
        conn.commit()
        
        # Query by category
        cursor.execute("SELECT name, price FROM products WHERE category = %s", ("Electronics",))
        electronics = cursor.fetchall()
        print(f"📱 Electronics: {electronics}")
        
        # Total value
        cursor.execute("SELECT SUM(price) FROM products")
        total = cursor.fetchone()[0]
        print(f"💰 Total value: ${total}")
        
        # Most expensive
        cursor.execute("SELECT name, price FROM products ORDER BY price DESC LIMIT 1")
        expensive = cursor.fetchone()
        print(f"💎 Most expensive: {expensive[0]} - ${expensive[1]}")
        
        cursor.close()
        conn.close()

def main():
    """Run Lab 1"""
    print("🚀 LAB 1: Your First Container")
    print("=" * 40)
    
    try:
        demo_basic_container()
        demo_database_operations()
        demo_version_comparison()
        challenge_solution()
        
        print("\n✅ Lab 1 completed!")
        print("Key concepts learned:")
        print("• Real database containers, not mocks")
        print("• Automatic cleanup and isolation")
        print("• Same behavior across environments")
        print("• Easy version testing")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()
