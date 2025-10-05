#!/usr/bin/env python3
"""
Lab 5: Multi-Database Testing - Working Examples
================================================

Master testing applications that use multiple database types.
Learn to work with PostgreSQL, MySQL, Redis, and MongoDB in complex scenarios.
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
        'redis': 'redis',
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

def demo_multi_database_setup():
    """Multi-database setup with real data operations"""
    print("\n🗄️ Multi-Database Setup Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Connect to all databases
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )

        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )


        # Test all connections
        print("\n🔗 Testing Database Connections:")
        
        # PostgreSQL
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("SELECT current_database(), current_user, version()")
        pg_db, pg_user, pg_version = pg_cursor.fetchone()
        print(f"   🐘 PostgreSQL: {pg_db} as {pg_user} ({pg_version.split()[1]})")

        # MySQL
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SELECT DATABASE(), USER(), VERSION()")
        mysql_db, mysql_user, mysql_version = mysql_cursor.fetchone()
        
        # Parse version safely
        version_parts = mysql_version.split()
        version_num = version_parts[1] if len(version_parts) > 1 else mysql_version
        print(f"   🐬 MySQL: {mysql_db} as {mysql_user} ({version_num})")

        # Redis
        r.ping()
        redis_info = r.info()
        print(f"   🔴 Redis: {redis_info['redis_version']} (Memory: {redis_info['used_memory_human']})")


        # Cleanup
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def demo_ecommerce_architecture():
    """E-commerce architecture with multiple databases"""
    print("\n🛒 E-commerce Architecture Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ All Services Ready:")
        print(f"   📊 PostgreSQL (Orders): {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"   👥 MySQL (Users): {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        print(f"   💾 Redis (Cache): {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Setup PostgreSQL (Orders)
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()

        pg_cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 PostgreSQL: Orders table created")

        # Setup MySQL (Users)
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        mysql_cursor = mysql_conn.cursor()

        mysql_cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 MySQL: Users table created")

        # Setup Redis (Cache)
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        print("📊 Redis: Cache service ready")


        # Create test data
        print("\n📝 Creating Test Data:")

        # Users in MySQL
        users = [
            ("alice_j", "alice@example.com"),
            ("bob_s", "bob@example.com"),
            ("carol_d", "carol@example.com")
        ]

        print("   👥 Creating Users (MySQL):")
        for username, email in users:
            mysql_cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (username, email)
            )
            print(f"      + {username} ({email})")

        mysql_conn.commit()

        # Orders in PostgreSQL
        orders = [
            (1, "MacBook Pro", 1, 2499.99, "completed"),
            (1, "Wireless Mouse", 2, 29.99, "shipped"),
            (2, "Coffee Mug", 3, 12.99, "pending"),
            (3, "Python Book", 1, 49.99, "completed")
        ]

        print("   📦 Creating Orders (PostgreSQL):")
        for user_id, product, quantity, price, status in orders:
            pg_cursor.execute(
                "INSERT INTO orders (user_id, product_name, quantity, price, status) VALUES (%s, %s, %s, %s, %s)",
                (user_id, product, quantity, price, status)
            )
            print(f"      + Order: {product} x{quantity} - ${price} ({status})")

        pg_conn.commit()

        # Cache in Redis
        print("   💾 Caching Data (Redis):")
        for i, (username, email) in enumerate(users, 1):
            user_data = f"{username} ({email})"
            r.setex(f"user:{i}", 300, user_data)  # 5 minutes TTL
            print(f"      + user:{i}: {user_data} (TTL: 300s)")


        # Cross-database analysis
        print(f"\n🔍 Cross-Database Analysis:")

        # Get user with most orders
        pg_cursor.execute("""
            SELECT user_id, COUNT(*) as order_count, 
                   SUM(price * quantity) as total_spent,
                   AVG(price * quantity) as avg_order_value
            FROM orders 
            GROUP BY user_id 
            ORDER BY order_count DESC, total_spent DESC
        """)

        order_stats = pg_cursor.fetchall()
        print("   📊 Order Statistics:")
        for user_id, order_count, total_spent, avg_order in order_stats:
            # Get user details from MySQL
            mysql_cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
            username, email = mysql_cursor.fetchone()
            
            # Get cached data from Redis
            cached_user = r.get(f"user:{user_id}")
            cache_status = "HIT" if cached_user else "MISS"
            
            print(f"      👤 {username} ({email}):")
            print(f"         📦 Orders: {order_count} | Total: ${total_spent:.2f} | Avg: ${avg_order:.2f}")
            print(f"         💾 Cache: {cache_status}")


        # Cleanup
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def demo_data_synchronization():
    """Data synchronization between multiple databases"""
    print("\n🔄 Data Synchronization Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ Synchronization Services Ready:")
        print(f"   📊 PostgreSQL (Master): {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"   📊 MySQL (Replica): {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        print(f"   💾 Redis (Sync Queue): {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Setup master database (PostgreSQL)
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()

        pg_cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 PostgreSQL: Products table created (Master)")

        # Setup replica database (MySQL)
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        mysql_cursor = mysql_conn.cursor()

        mysql_cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("📊 MySQL: Products table created (Replica)")

        # Setup sync queue (Redis)
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        print("📊 Redis: Sync queue ready")

        # Initial data in master
        products = [
            ("MacBook Pro", 2499.99, 10),
            ("iPhone", 999.99, 25),
            ("iPad", 599.99, 15),
            ("AirPods", 199.99, 50)
        ]

        print("\n📝 Creating Initial Products (Master):")
        for name, price, stock in products:
            pg_cursor.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (name, price, stock)
            )
            print(f"   + {name}: ${price} (Stock: {stock})")

        pg_conn.commit()

        # Simulate synchronization
        print(f"\n🔄 Synchronizing Data to Replica:")

        # Get all products from master
        pg_cursor.execute("SELECT id, name, price, stock FROM products ORDER BY id")
        master_products = pg_cursor.fetchall()

        sync_count = 0
        for product_id, name, price, stock in master_products:
            # Insert into replica
            mysql_cursor.execute(
                "INSERT INTO products (id, name, price, stock) VALUES (%s, %s, %s, %s)",
                (product_id, name, price, stock)
            )
            
            # Add to sync queue
            sync_event = f"sync:product:{product_id}:{name}:{price}:{stock}"
            r.lpush("sync_queue", sync_event)
            
            sync_count += 1
            print(f"   📤 Synced: {name} (ID: {product_id})")

        mysql_conn.commit()

        # Process sync queue
        print(f"\n📥 Processing Sync Queue:")
        processed_events = 0
        while processed_events < sync_count:
            event = r.rpop("sync_queue")
            if event:
                event_parts = event.split(":")
                product_id, name, price, stock = event_parts[2], event_parts[3], event_parts[4], event_parts[5]
                print(f"   📥 Processed: {name} (ID: {product_id})")
                processed_events += 1

        # Verify synchronization
        print(f"\n🔍 Synchronization Verification:")

        # Count products in both databases
        pg_cursor.execute("SELECT COUNT(*) FROM products")
        master_count = pg_cursor.fetchone()[0]
        mysql_cursor.execute("SELECT COUNT(*) FROM products")
        replica_count = mysql_cursor.fetchone()[0]

        print(f"   📊 Master (PostgreSQL): {master_count} products")
        print(f"   📊 Replica (MySQL): {replica_count} products")
        print(f"   ✅ Synchronized: {'Yes' if master_count == replica_count else 'No'}")

        # Show sample data comparison
        print(f"\n📋 Sample Data Comparison:")
        pg_cursor.execute("SELECT name, price, stock FROM products ORDER BY id LIMIT 2")
        master_sample = pg_cursor.fetchall()
        mysql_cursor.execute("SELECT name, price, stock FROM products ORDER BY id LIMIT 2")
        replica_sample = mysql_cursor.fetchall()

        for i, (master_row, replica_row) in enumerate(zip(master_sample, replica_sample)):
            print(f"   Product {i+1}:")
            print(f"      Master: {master_row[0]} - ${master_row[1]} (Stock: {master_row[2]})")
            print(f"      Replica: {replica_row[0]} - ${replica_row[1]} (Stock: {replica_row[2]})")
            print(f"      Match: {'✅' if master_row == replica_row else '❌'}")

        # Cleanup
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def demo_transaction_coordination():
    """Transaction coordination across multiple databases"""
    print("\n⚡ Transaction Coordination Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print(f"✅ Transaction Services Ready:")
        print(f"   📊 PostgreSQL (Orders): {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"   📊 MySQL (Inventory): {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
        print(f"   💾 Redis (Coordination): {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

        # Setup databases
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        pg_cursor = pg_conn.cursor()

        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        mysql_cursor = mysql_conn.cursor()

        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Create tables
        pg_cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                total_price DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending'
            )
        """)

        mysql_cursor.execute("""
            CREATE TABLE inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(100) UNIQUE NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                reserved INTEGER NOT NULL DEFAULT 0
            )
        """)

        print("📊 Tables Created: orders (PostgreSQL), inventory (MySQL)")

        # Insert inventory data
        inventory_items = [
            ("MacBook Pro", 10),
            ("iPhone", 25),
            ("iPad", 15)
        ]

        print("📝 Creating Inventory (MySQL):")
        for product, stock in inventory_items:
            mysql_cursor.execute(
                "INSERT INTO inventory (product_name, stock) VALUES (%s, %s)",
                (product, stock)
            )
            print(f"   + {product}: {stock} units")

        mysql_conn.commit()

        # Simulate distributed transaction
        print(f"\n⚡ Simulating Distributed Transaction:")

        # Transaction 1: Order MacBook Pro
        transaction_id = "txn_001"
        product_name = "MacBook Pro"
        quantity = 2
        unit_price = 2499.99
        total_price = quantity * unit_price

        print(f"   🔄 Transaction {transaction_id}: Order {quantity}x {product_name}")

        # Phase 1: Prepare
        print(f"   📋 Phase 1: Prepare")
        
        # Check inventory
        mysql_cursor.execute("SELECT stock FROM inventory WHERE product_name = %s", (product_name,))
        available_stock = mysql_cursor.fetchone()[0]
        
        if available_stock >= quantity:
            print(f"      ✅ Inventory check: {available_stock} units available")
            
            # Reserve inventory
            mysql_cursor.execute(
                "UPDATE inventory SET stock = stock - %s, reserved = reserved + %s WHERE product_name = %s",
                (quantity, quantity, product_name)
            )
            mysql_conn.commit()
            print(f"      ✅ Inventory reserved: {quantity} units")
            
            # Create order
            pg_cursor.execute(
                "INSERT INTO orders (product_name, quantity, total_price) VALUES (%s, %s, %s)",
                (product_name, quantity, total_price)
            )
            pg_conn.commit()
            print(f"      ✅ Order created: ${total_price}")
            
            # Store transaction state in Redis
            r.hset(f"transaction:{transaction_id}", mapping={
                "status": "committed",
                "product": product_name,
                "quantity": str(quantity),
                "total": str(total_price),
                "timestamp": str(int(time.time()))
            })
            
            print(f"   ✅ Transaction {transaction_id}: COMMITTED")
            
        else:
            print(f"      ❌ Inventory check: Only {available_stock} units available")
            print(f"   ❌ Transaction {transaction_id}: ROLLED BACK")
            
            # Store failed transaction in Redis
            r.hset(f"transaction:{transaction_id}", mapping={
                "status": "rolled_back",
                "reason": "insufficient_inventory",
                "timestamp": str(int(time.time()))
            })

        # Show final state
        print(f"\n📊 Final State:")

        # Order count
        pg_cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = pg_cursor.fetchone()[0]
        print(f"   📦 Orders (PostgreSQL): {order_count}")

        # Inventory state
        mysql_cursor.execute("SELECT product_name, stock, reserved FROM inventory")
        inventory_state = mysql_cursor.fetchall()
        print(f"   📦 Inventory (MySQL):")
        for product, stock, reserved in inventory_state:
            print(f"      {product}: {stock} available, {reserved} reserved")

        # Transaction log
        transaction_data = r.hgetall(f"transaction:{transaction_id}")
        print(f"   📝 Transaction Log (Redis):")
        for key, value in transaction_data.items():
            print(f"      {key}: {value}")

        # Cleanup
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def main():
    """Run Lab 5 - Multi-Database Testing"""
    print("🚀 LAB 5: Multi-Database Testing - Working Examples")
    print("=" * 60)
    print("✨ Master testing applications with multiple database types!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_multi_database_setup()
        demo_ecommerce_architecture()
        demo_data_synchronization()
        demo_transaction_coordination()
        
        print("\n✅ Lab 5 completed successfully!")
        print("Key concepts learned:")
        print("• Multi-database setup and connection management")
        print("• E-commerce architecture with different database types")
        print("• Data synchronization between databases")
        print("• Distributed transaction coordination")
        print("• Real-world multi-database scenarios")
        print("\n💪 You're ready for API testing scenarios!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()