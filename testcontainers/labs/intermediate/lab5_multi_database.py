#!/usr/bin/env python3
"""
Lab 5: Multi-Database Testing
=============================

Master testing applications that use multiple database types.
"""

import os

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.mysql import MySqlContainer
    from testcontainers.redis import RedisContainer
    from testcontainers.mongodb import MongoDbContainer
    import psycopg2
    import pymysql
    import redis
    import pymongo
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary pymysql redis pymongo")
    exit(1)

def demo_multi_database_setup():
    """Multi-database setup demo"""
    print("🗄️ Multi-Database Setup")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print("✅ All databases started:")
        print(f"   PostgreSQL: port {postgres.get_exposed_port(5432)}")
        print(f"   MySQL: port {mysql.get_exposed_port(3306)}")
        print(f"   Redis: port {redis_container.get_exposed_port(6379)}")

        # Test connections
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

        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        print("✅ All connections successful!")
        
        pg_conn.close()
        mysql_conn.close()

def demo_cross_database_coordination():
    """Cross-database data coordination"""
    print("\n🔄 Cross-Database Coordination")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

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

        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Store data across databases
        # PostgreSQL: User data
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        pg_cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        pg_conn.commit()

        # MySQL: Product data
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2)
            )
        """)
        mysql_cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 999.99)")
        mysql_conn.commit()

        # Redis: Session data
        redis_client.set("session:alice", "active")
        redis_client.set("cart:alice", "laptop_001")

        print("📊 Data stored across databases:")

        # Query from each database
        pg_cursor.execute("SELECT name, email FROM users")
        user = pg_cursor.fetchone()
        print(f"   PostgreSQL: {user[0]} ({user[1]})")

        mysql_cursor.execute("SELECT name, price FROM products")
        product = mysql_cursor.fetchone()
        print(f"   MySQL: {product[0]} - ${product[1]}")

        session = redis_client.get("session:alice")
        cart = redis_client.get("cart:alice")
        print(f"   Redis: Session {session}, Cart {cart}")

        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def demo_sql_nosql_integration():
    """SQL + NoSQL integration demo"""
    print("\n🍃 SQL + NoSQL Integration")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MongoDbContainer("mongo:7.0") as mongo:

        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        # Connect to MongoDB
        mongo_client = pymongo.MongoClient(mongo.get_connection_url())
        db = mongo_client.test_db
        collection = db.products

        # PostgreSQL: Structured data
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100),
                total DECIMAL(10,2)
            )
        """)
        pg_cursor.execute("INSERT INTO orders (customer_name, total) VALUES ('Alice', 999.99)")
        pg_conn.commit()

        # MongoDB: Document data
        product_doc = {
            "name": "MacBook Pro",
            "price": 999.99,
            "specs": {"ram": "16GB", "storage": "512GB"},
            "reviews": [
                {"rating": 5, "comment": "Great laptop!"},
                {"rating": 4, "comment": "Good performance"}
            ]
        }
        collection.insert_one(product_doc)

        print("📊 Data stored in both databases:")

        # Query PostgreSQL
        pg_cursor.execute("SELECT customer_name, total FROM orders")
        order = pg_cursor.fetchone()
        print(f"   PostgreSQL: Order for {order[0]} - ${order[1]}")

        # Query MongoDB
        product = collection.find_one({"name": "MacBook Pro"})
        print(f"   MongoDB: {product['name']} with {len(product['reviews'])} reviews")

        pg_cursor.close()
        pg_conn.close()
        mongo_client.close()

def demo_transaction_coordination():
    """Transaction coordination across databases"""
    print("\n⚡ Transaction Coordination")
    
    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Create tables
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                balance DECIMAL(10,2)
            )
        """)
        pg_cursor.execute("INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00)")
        pg_conn.commit()

        # Simulate distributed transaction
        try:
            # Start transaction in PostgreSQL
            pg_cursor.execute("BEGIN")
            
            # Update account balance
            pg_cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice'")
            
            # Update cache in Redis
            redis_client.set("account:alice:balance", "900.00")
            redis_client.set("transaction:status", "completed")
            
            # Commit PostgreSQL transaction
            pg_cursor.execute("COMMIT")
            
            print("✅ Distributed transaction completed")
            
            # Verify consistency
            pg_cursor.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
            db_balance = pg_cursor.fetchone()[0]
            cache_balance = redis_client.get("account:alice:balance")
            
            print(f"📊 DB balance: {db_balance}, Cache balance: {cache_balance}")
            
        except Exception as e:
            pg_cursor.execute("ROLLBACK")
            redis_client.set("transaction:status", "failed")
            print(f"❌ Transaction failed: {e}")

        pg_cursor.close()
        pg_conn.close()

def demo_microservices_pattern():
    """Microservices database pattern"""
    print("\n🏗️ Microservices Database Pattern")
    
    with PostgresContainer("postgres:15-alpine") as user_db, \
         MySqlContainer("mysql:8.0") as order_db, \
         RedisContainer("redis:7-alpine") as cache:

        # User service database
        user_conn = psycopg2.connect(
            host=user_db.get_container_host_ip(),
            port=user_db.get_exposed_port(5432),
            user=user_db.username,
            password=user_db.password,
            database=user_db.dbname
        )

        # Order service database
        order_conn = pymysql.connect(
            host=order_db.get_container_host_ip(),
            port=order_db.get_exposed_port(3306),
            user=order_db.username,
            password=order_db.password,
            database=order_db.dbname
        )

        # Cache service
        cache_client = redis.Redis(
            host=cache.get_container_host_ip(),
            port=cache.get_exposed_port(6379),
            decode_responses=True
        )

        # Setup user service
        user_cursor = user_conn.cursor()
        user_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        user_cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        user_conn.commit()

        # Setup order service
        order_cursor = order_conn.cursor()
        order_cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product VARCHAR(100),
                amount DECIMAL(10,2)
            )
        """)
        order_cursor.execute("INSERT INTO orders (user_id, product, amount) VALUES (1, 'Laptop', 999.99)")
        order_conn.commit()

        # Simulate cross-service query
        print("📊 Cross-service data query:")
        
        # Get user from user service
        user_cursor.execute("SELECT id, name FROM users WHERE email = 'alice@example.com'")
        user = user_cursor.fetchone()
        print(f"   User: {user[1]} (ID: {user[0]})")
        
        # Get orders from order service
        order_cursor.execute("SELECT product, amount FROM orders WHERE user_id = %s", (user[0],))
        orders = order_cursor.fetchall()
        print(f"   Orders: {orders}")
        
        # Cache the result
        cache_client.set(f"user:{user[0]}:orders", str(orders))
        print(f"   Cached: {cache_client.get(f'user:{user[0]}:orders')}")

        user_cursor.close()
        user_conn.close()
        order_cursor.close()
        order_conn.close()

def main():
    """Run Lab 5"""
    print("🗄️ LAB 5: Multi-Database Testing")
    print("=" * 40)
    
    try:
        demo_multi_database_setup()
        demo_cross_database_coordination()
        demo_sql_nosql_integration()
        demo_transaction_coordination()
        demo_microservices_pattern()
        
        print("\n✅ Lab 5 completed!")
        print("Key concepts learned:")
        print("• Multi-database coordination")
        print("• Cross-database data management")
        print("• SQL + NoSQL integration")
        print("• Transaction coordination patterns")
        print("• Microservices database architecture")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()