#!/usr/bin/env python3
"""
TestContainers Quick Examples
=============================

Clean, powerful examples demonstrating key TestContainers concepts.
"""

import os
import time

# Configure TestContainers
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    from testcontainers.mysql import MySqlContainer
    from testcontainers.mongodb import MongoDbContainer
    import psycopg2
    import redis
    import pymysql
    import pymongo
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis pymysql pymongo")
    exit(1)

def example_1_basic_postgres():
    """Basic PostgreSQL container"""
    print("🐘 Basic PostgreSQL")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
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
        print(f"✅ PostgreSQL {version.split()[1]} running on port {postgres.get_exposed_port(5432)}")
        
        cursor.close()
        conn.close()

def example_2_multi_database():
    """Multiple databases working together"""
    print("\n🗄️ Multi-Database Setup")
    
    with PostgresContainer("postgres:15-alpine") as pg, \
         RedisContainer("redis:7-alpine") as redis_container, \
         MySqlContainer("mysql:8.0") as mysql:
        
        # PostgreSQL for main data
        pg_conn = psycopg2.connect(
            host=pg.get_container_host_ip(),
            port=pg.get_exposed_port(5432),
            user=pg.username,
            password=pg.password,
            database=pg.dbname
        )
        
        # Redis for caching
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # MySQL for analytics
        mysql_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        
        print("✅ All databases connected")
        
        # Store user in PostgreSQL
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100))")
        pg_cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
        pg_conn.commit()
        
        # Cache user session in Redis
        r.set("session:alice", "active", ex=3600)
        
        # Store analytics in MySQL
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("CREATE TABLE analytics (event VARCHAR(100), count INT)")
        mysql_cursor.execute("INSERT INTO analytics (event, count) VALUES ('user_login', 1)")
        mysql_conn.commit()
        
        print("📊 Data stored across all databases")
        
        pg_cursor.close()
        pg_conn.close()
        mysql_cursor.close()
        mysql_conn.close()

def example_3_api_simulation():
    """Simulate API testing with database"""
    print("\n🌐 API Simulation")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2)
            )
        """)
        
        # API functions
        def create_product(name, price):
            cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id", (name, price))
            product_id = cursor.fetchone()[0]
            conn.commit()
            return {"id": product_id, "name": name, "price": price}
        
        def get_product(product_id):
            cursor.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            return {"id": result[0], "name": result[1], "price": result[2]} if result else None
        
        # Test API operations
        product1 = create_product("Laptop", 999.99)
        product2 = create_product("Mouse", 29.99)
        
        print(f"✅ Created products: {product1['name']}, {product2['name']}")
        
        retrieved = get_product(product1['id'])
        print(f"✅ Retrieved: {retrieved['name']} - ${retrieved['price']}")
        
        cursor.close()
        conn.close()

def example_4_data_pipeline():
    """ETL pipeline with multiple containers"""
    print("\n🔄 Data Pipeline")
    
    # Extract from PostgreSQL
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE sales (
                id SERIAL PRIMARY KEY,
                product VARCHAR(100),
                amount DECIMAL(10,2),
                date DATE
            )
        """)
        
        sales_data = [
            ("Laptop", 999.99, "2024-01-01"),
            ("Mouse", 29.99, "2024-01-01"),
            ("Laptop", 999.99, "2024-01-02"),
            ("Keyboard", 79.99, "2024-01-02")
        ]
        
        for product, amount, date in sales_data:
            cursor.execute("INSERT INTO sales (product, amount, date) VALUES (%s, %s, %s)", (product, amount, date))
        
        conn.commit()
        
        # Extract aggregated data
        cursor.execute("""
            SELECT product, COUNT(*) as sales_count, SUM(amount) as total_revenue
            FROM sales
            GROUP BY product
        """)
        aggregated_data = cursor.fetchall()
        
        print(f"📊 Extracted {len(aggregated_data)} product summaries")
        
        cursor.close()
        conn.close()
    
    # Load into Redis for caching
    with RedisContainer("redis:7-alpine") as redis_container:
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        for product, count, revenue in aggregated_data:
            r.hset(f"product:{product}", mapping={
                "sales_count": str(count),
                "total_revenue": str(float(revenue))
            })
        
        print(f"💾 Cached {len(aggregated_data)} product summaries in Redis")
        
        # Verify data
        for product, _, _ in aggregated_data:
            stats = r.hgetall(f"product:{product}")
            print(f"   {product}: {stats['sales_count']} sales, ${stats['total_revenue']} revenue")

def example_5_mongodb_document_store():
    """MongoDB document storage"""
    print("\n🍃 MongoDB Document Store")
    
    with MongoDbContainer("mongo:7.0") as mongo:
        client = pymongo.MongoClient(mongo.get_connection_url())
        db = client.test_db
        collection = db.products
        
        # Insert document
        product_doc = {
            "name": "MacBook Pro",
            "price": 1999.99,
            "specs": {
                "ram": "16GB",
                "storage": "512GB SSD",
                "processor": "M2"
            },
            "reviews": [
                {"rating": 5, "comment": "Excellent laptop!"},
                {"rating": 4, "comment": "Great performance"}
            ]
        }
        
        result = collection.insert_one(product_doc)
        print(f"✅ Inserted document with ID: {result.inserted_id}")
        
        # Query document
        product = collection.find_one({"name": "MacBook Pro"})
        print(f"📊 Found: {product['name']} with {len(product['reviews'])} reviews")
        
        client.close()

def example_6_concurrent_testing():
    """Concurrent database operations"""
    print("\n⚡ Concurrent Testing")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
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
                thread_id INTEGER,
                data TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        
        import threading
        
        def worker(thread_id, connection_params):
            conn = psycopg2.connect(**connection_params)
            cursor = conn.cursor()
            
            for i in range(10):
                cursor.execute(
                    "INSERT INTO concurrent_test (thread_id, data) VALUES (%s, %s)",
                    (thread_id, f"Thread {thread_id} data {i}")
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Thread {thread_id} completed")
        
        # Start 3 concurrent threads
        connection_params = {
            'host': postgres.get_container_host_ip(),
            'port': postgres.get_exposed_port(5432),
            'user': postgres.username,
            'password': postgres.password,
            'database': postgres.dbname
        }
        
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker, args=(i, connection_params))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify results
        final_conn = psycopg2.connect(**connection_params)
        final_cursor = final_conn.cursor()
        final_cursor.execute("SELECT COUNT(*) FROM concurrent_test")
        count = final_cursor.fetchone()[0]
        print(f"📊 Total records created: {count}")
        
        final_cursor.close()
        final_conn.close()

def main():
    """Run all examples"""
    print("🚀 TestContainers Quick Examples")
    print("=" * 40)
    
    try:
        example_1_basic_postgres()
        example_2_multi_database()
        example_3_api_simulation()
        example_4_data_pipeline()
        example_5_mongodb_document_store()
        example_6_concurrent_testing()
        
        print("\n✅ All examples completed!")
        print("\nKey concepts demonstrated:")
        print("• Basic container lifecycle")
        print("• Multi-database coordination")
        print("• API testing patterns")
        print("• Data pipeline processing")
        print("• Document database usage")
        print("• Concurrent operations")
        
    except Exception as e:
        print(f"❌ Examples failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()