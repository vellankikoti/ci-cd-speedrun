#!/usr/bin/env python3
"""
Lab 2: Database Connections - Working Examples
==============================================

Connect to different database types with TestContainers - PostgreSQL, MySQL, and Redis.
Learn how to work with multiple database technologies in your tests.
"""

import os
import sys
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

def demo_postgresql():
    """PostgreSQL connection demo with real data"""
    print("\n🐘 PostgreSQL Connection Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Get version and connection info
        cursor.execute("SELECT current_database(), current_user, version()")
        db_name, user, version = cursor.fetchone()
        print(f"🔗 Connected: {db_name} as {user}")
        print(f"📋 Version: {version.split()[0]} {version.split()[1]}")
        
        # Create products table
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                in_stock BOOLEAN DEFAULT true
            )
        """)
        print("📊 Table Created: products")
        
        # Insert sample data
        products = [
            ("MacBook Pro", 2499.99, "Electronics", True),
            ("Coffee Mug", 12.99, "Kitchen", True),
            ("Python Book", 49.99, "Education", False),
            ("Wireless Mouse", 29.99, "Electronics", True)
        ]
        
        print("📝 Inserting Products:")
        for name, price, category, in_stock in products:
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (%s, %s, %s, %s)",
                (name, price, category, in_stock)
            )
            status = "✅" if in_stock else "❌"
            print(f"   {status} {name} - ${price} ({category})")
        
        conn.commit()
        
        # Query with aggregations
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(price) as avg_price,
                   SUM(CASE WHEN in_stock THEN 1 ELSE 0 END) as in_stock_count
            FROM products 
            GROUP BY category 
            ORDER BY avg_price DESC
        """)
        
        results = cursor.fetchall()
        print(f"\n📊 Category Analysis:")
        for category, count, avg_price, in_stock_count in results:
            print(f"   {category}: {count} items | Avg: ${avg_price:.2f} | In Stock: {in_stock_count}/{count}")
        
        cursor.close()
        conn.close()

def demo_mysql():
    """MySQL connection demo with real data"""
    print("\n🐬 MySQL Connection Demo...")
    
    with MySqlContainer("mysql:8.0") as mysql:
        print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        
        conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        
        cursor = conn.cursor()
        
        # Get version and connection info
        cursor.execute("SELECT DATABASE(), USER(), VERSION()")
        db_name, user, version = cursor.fetchone()
        print(f"🔗 Connected: {db_name} as {user}")
        
        # Parse version safely
        version_parts = version.split()
        if len(version_parts) >= 2:
            print(f"📋 Version: {version_parts[0]} {version_parts[1]}")
        else:
            print(f"📋 Version: {version}")
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending'
            )
        """)
        print("📊 Table Created: orders")
        
        # Insert sample orders
        orders = [
            ("Alice Johnson", 299.99, "processing"),
            ("Bob Smith", 149.99, "shipped"),
            ("Carol Davis", 89.99, "pending"),
            ("David Wilson", 459.99, "delivered")
        ]
        
        print("📝 Inserting Orders:")
        for customer, amount, status in orders:
            cursor.execute(
                "INSERT INTO orders (customer_name, total_amount, status) VALUES (%s, %s, %s)",
                (customer, amount, status)
            )
            print(f"   📦 {customer} - ${amount} ({status})")
        
        conn.commit()
        
        # Query with status analysis
        cursor.execute("""
            SELECT status, COUNT(*) as count, AVG(total_amount) as avg_amount,
                   MIN(total_amount) as min_amount, MAX(total_amount) as max_amount
            FROM orders 
            GROUP BY status 
            ORDER BY avg_amount DESC
        """)
        
        results = cursor.fetchall()
        print(f"\n📊 Order Status Analysis:")
        for status, count, avg_amount, min_amount, max_amount in results:
            print(f"   {status.capitalize()}: {count} orders | Avg: ${avg_amount:.2f} | Range: ${min_amount:.2f}-${max_amount:.2f}")
        
        cursor.close()
        conn.close()

def demo_redis():
    """Redis connection demo with real data"""
    print("\n🔴 Redis Connection Demo...")
    
    with RedisContainer("redis:7-alpine") as redis_container:
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")
        
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # Test connection
        info = r.info()
        print(f"🔗 Connected: Redis {info['redis_version']}")
        print(f"📋 Memory: {info['used_memory_human']} | Uptime: {info['uptime_in_seconds']}s")
        
        # Store session data
        print("📝 Storing Session Data:")
        sessions = {
            "user:1001": {"name": "Alice", "email": "alice@example.com", "login_time": "2024-01-15 10:30:00"},
            "user:1002": {"name": "Bob", "email": "bob@example.com", "login_time": "2024-01-15 11:15:00"},
            "user:1003": {"name": "Carol", "email": "carol@example.com", "login_time": "2024-01-15 12:00:00"}
        }
        
        for session_key, session_data in sessions.items():
            r.hset(session_key, mapping=session_data)
            r.expire(session_key, 3600)  # 1 hour TTL
            print(f"   🔑 {session_key}: {session_data['name']} ({session_data['email']})")
        
        # Store cache data
        print("\n📝 Storing Cache Data:")
        cache_items = [
            ("product:1001", "MacBook Pro - $2499.99", 300),
            ("product:1002", "Coffee Mug - $12.99", 600),
            ("product:1003", "Python Book - $49.99", 1800)
        ]
        
        for key, value, ttl in cache_items:
            r.set(key, value, ex=ttl)
            print(f"   💾 {key}: {value} (TTL: {ttl}s)")
        
        # Query session data
        print(f"\n📊 Active Sessions ({r.dbsize()} total keys):")
        for session_key in sessions.keys():
            session_data = r.hgetall(session_key)
            ttl = r.ttl(session_key)
            print(f"   👤 {session_data['name']} ({session_data['email']}) - TTL: {ttl}s")
        
        # Query cache data
        print(f"\n📊 Cache Status:")
        for key, _, _ in cache_items:
            value = r.get(key)
            ttl = r.ttl(key)
            if value:
                print(f"   💾 {key}: {value} (TTL: {ttl}s)")
            else:
                print(f"   ❌ {key}: Expired")

def demo_cross_database():
    """Cross-database operations demo"""
    print("\n🔄 Cross-Database Operations Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:
        
        print("✅ All databases ready!")
        
        # PostgreSQL - User data
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()
        
        # MySQL - Order data
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        mysql_cursor = mysql_conn.cursor()
        
        # Redis - Session data
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # Create users in PostgreSQL
        pg_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            )
        """)
        
        users = [("Alice Johnson", "alice@example.com"), ("Bob Smith", "bob@example.com")]
        for name, email in users:
            pg_cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        pg_conn.commit()
        
        # Create orders in MySQL
        mysql_cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(100) NOT NULL,
                amount DECIMAL(10,2) NOT NULL
            )
        """)
        
        orders = [("alice@example.com", 299.99), ("bob@example.com", 149.99)]
        for email, amount in orders:
            mysql_cursor.execute("INSERT INTO orders (user_email, amount) VALUES (%s, %s)", (email, amount))
        mysql_conn.commit()
        
        # Store sessions in Redis
        for name, email in users:
            r.hset(f"session:{email}", mapping={"name": name, "email": email, "active": "true"})
        
        print("📊 Cross-Database Data Created:")
        print("   PostgreSQL: 2 users")
        print("   MySQL: 2 orders")
        print("   Redis: 2 sessions")
        
        # Cross-database query simulation
        print(f"\n🔍 Cross-Database Analysis:")
        pg_cursor.execute("SELECT name, email FROM users ORDER BY name")
        users_data = pg_cursor.fetchall()
        
        for name, email in users_data:
            # Get orders from MySQL
            mysql_cursor.execute("SELECT COUNT(*), SUM(amount) FROM orders WHERE user_email = %s", (email,))
            order_count, total_amount = mysql_cursor.fetchone()
            
            # Get session from Redis
            session = r.hgetall(f"session:{email}")
            session_status = "Active" if session.get("active") == "true" else "Inactive"
            
            print(f"   👤 {name} ({email})")
            print(f"      📦 Orders: {order_count} | Total: ${total_amount or 0:.2f}")
            print(f"      🔑 Session: {session_status}")
        
        # Cleanup
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def main():
    """Run Lab 2 - Database Connections"""
    print("🚀 LAB 2: Database Connections - Working Examples")
    print("=" * 60)
    print("✨ Connect to PostgreSQL, MySQL, and Redis with TestContainers!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_postgresql()
        demo_mysql()
        demo_redis()
        demo_cross_database()
        
        print("\n✅ Lab 2 completed successfully!")
        print("Key concepts learned:")
        print("• Multiple database types with TestContainers")
        print("• PostgreSQL, MySQL, and Redis connections")
        print("• Cross-database operations and data analysis")
        print("• Real-world multi-database scenarios")
        print("\n💪 You're ready for data management patterns!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()