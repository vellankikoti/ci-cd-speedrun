#!/usr/bin/env python3
"""
🎬 TestContainers Power Demo
============================

This demo showcases the incredible power of TestContainers with real-world scenarios.
Watch as we spin up entire database clusters, test complex integrations, and handle
chaos engineering - all in seconds!
"""

import os
import sys
import time
from pathlib import Path

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

# Add workshop directory to path
sys.path.insert(0, str(Path(__file__).parent))

from testcontainers.postgres import PostgresContainer
from testcontainers.mysql import MySqlContainer
from testcontainers.redis import RedisContainer
from testcontainers.mongodb import MongoDbContainer
import psycopg2
import pymysql
import redis
import pymongo

def print_banner():
    """Print the demo banner"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    🎬 TESTCONTAINERS POWER DEMO 🎬              ║
║                                                                  ║
║  Watch the magic happen as we spin up entire database clusters! ║
║  Real databases, real data, real testing - all in seconds!      ║
╚══════════════════════════════════════════════════════════════════╝
""")

def demo_postgres():
    """Demo PostgreSQL with TestContainers"""
    print("\n🐘 PostgreSQL Demo - Enterprise Database Testing")
    print("=" * 50)
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ PostgreSQL started on port {postgres.get_exposed_port(5432)}")
        
        # Connect and create a table
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))")
        cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com')")
        conn.commit()
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print(f"✅ Created table and inserted {len(users)} users")
        for user in users:
            print(f"   👤 {user[1]} ({user[2]})")
        
        cursor.close()
        conn.close()
        print("✅ PostgreSQL demo completed - container automatically cleaned up!")

def demo_mysql():
    """Demo MySQL with TestContainers"""
    print("\n🐬 MySQL Demo - High-Performance Database Testing")
    print("=" * 50)
    
    with MySqlContainer("mysql:8.0") as mysql:
        print(f"✅ MySQL started on port {mysql.get_exposed_port(3306)}")
        
        # Connect and create a table
        conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2))")
        cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 999.99), ('Mouse', 29.99), ('Keyboard', 79.99)")
        conn.commit()
        
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        print(f"✅ Created products table with {len(products)} items")
        for product in products:
            print(f"   🛍️ {product[1]} - ${product[2]}")
        
        cursor.close()
        conn.close()
        print("✅ MySQL demo completed - container automatically cleaned up!")

def demo_redis():
    """Demo Redis with TestContainers"""
    print("\n🔴 Redis Demo - Lightning-Fast Caching")
    print("=" * 50)
    
    with RedisContainer("redis:7.2-alpine") as redis_container:
        print(f"✅ Redis started on port {redis_container.get_exposed_port(6379)}")
        
        # Connect and test Redis
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )
        
        # Test basic operations
        r.set("workshop:user:1", "Alice")
        r.set("workshop:user:2", "Bob")
        r.set("workshop:session:abc123", "active")
        
        # Test data structures
        r.lpush("workshop:queue", "task1", "task2", "task3")
        r.sadd("workshop:tags", "python", "testing", "containers")
        
        print("✅ Stored user data and session info")
        print(f"   👤 User 1: {r.get('workshop:user:1')}")
        print(f"   👤 User 2: {r.get('workshop:user:2')}")
        print(f"   🔑 Session: {r.get('workshop:session:abc123')}")
        print(f"   📋 Queue length: {r.llen('workshop:queue')}")
        print(f"   🏷️ Tags: {r.smembers('workshop:tags')}")
        
        print("✅ Redis demo completed - container automatically cleaned up!")

def demo_mongodb():
    """Demo MongoDB with TestContainers"""
    print("\n🍃 MongoDB Demo - Document Database Power")
    print("=" * 50)
    
    with MongoDbContainer("mongo:7.0") as mongo:
        print(f"✅ MongoDB started on port {mongo.get_exposed_port(27017)}")
        
        # Connect and test MongoDB
        client = pymongo.MongoClient(
            mongo.get_connection_url()
        )
        
        db = client.test_db
        collection = db.products
        
        # Insert documents
        products = [
            {"name": "MacBook Pro", "price": 1999.99, "category": "laptop", "specs": {"ram": "16GB", "storage": "512GB"}},
            {"name": "iPhone 15", "price": 999.99, "category": "phone", "specs": {"storage": "128GB", "color": "space_gray"}},
            {"name": "AirPods Pro", "price": 249.99, "category": "audio", "specs": {"noise_cancellation": True}}
        ]
        
        result = collection.insert_many(products)
        print(f"✅ Inserted {len(result.inserted_ids)} products")
        
        # Query documents
        laptops = collection.find({"category": "laptop"})
        print("   💻 Laptops found:")
        for laptop in laptops:
            print(f"      {laptop['name']} - ${laptop['price']}")
        
        # Aggregation pipeline
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}, "avg_price": {"$avg": "$price"}}},
            {"$sort": {"avg_price": -1}}
        ]
        
        categories = list(collection.aggregate(pipeline))
        print("   📊 Category analysis:")
        for cat in categories:
            print(f"      {cat['_id']}: {cat['count']} items, avg ${cat['avg_price']:.2f}")
        
        client.close()
        print("✅ MongoDB demo completed - container automatically cleaned up!")

def main():
    """Run the complete TestContainers power demo"""
    print_banner()
    
    print("\n🚀 Starting TestContainers Power Demo...")
    print("This will showcase the incredible power of TestContainers with real databases!")
    print("\nPress Enter to begin...")
    input()
    
    try:
        # Run all demos
        demo_postgres()
        time.sleep(1)
        
        demo_mysql()
        time.sleep(1)
        
        demo_redis()
        time.sleep(1)
        
        demo_mongodb()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETE! 🎉")
        print("=" * 60)
        print("\nWhat you just witnessed:")
        print("✅ 4 different databases started and configured automatically")
        print("✅ Real data operations performed on each database")
        print("✅ Complex queries and aggregations executed")
        print("✅ All containers cleaned up automatically")
        print("✅ Zero manual setup or configuration required")
        print("\nThis is the power of TestContainers - real testing with real databases!")
        print("\nReady to dive deeper? Run: python workshop.py")
        
except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("This might be due to Docker not running or network issues.")
        print("Please ensure Docker Desktop is running and try again.")

if __name__ == "__main__":
    main()
