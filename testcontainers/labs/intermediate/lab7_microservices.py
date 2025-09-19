#!/usr/bin/env python3
"""
Lab 7: Microservices Integration (Simple Version)
=================================================

Learn how to test microservices that interact with multiple
databases and services using TestContainers.
"""

import os
import time

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

import json
import threading
from datetime import datetime

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.mysql import MySqlContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import pymysql
    import redis
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("Please run: python3 setup.py from testcontainers directory")
    exit(1)

def print_header():
    """Print lab header"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║               🏗️ LAB 7: MICROSERVICES INTEGRATION 🏗️            ║
║                                                                  ║
║  Learn to test microservices architectures with multiple        ║
║  databases and inter-service communication patterns.            ║
╚══════════════════════════════════════════════════════════════════╝
""")

def demo_user_service():
    """Demo User Service with PostgreSQL"""
    print("\n👤 User Service Demo")
    print("=" * 50)

    with PostgresContainer("postgres:15-alpine") as postgres:
        print("✅ User Service PostgreSQL started")

        # User Service Database
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        print("📊 User Service database initialized")

        class UserService:
            def __init__(self, db_conn):
                self.conn = db_conn
                self.cursor = db_conn.cursor()

            def create_user(self, username, email, full_name):
                """Create a new user"""
                try:
                    self.cursor.execute("""
                        INSERT INTO users (username, email, full_name)
                        VALUES (%s, %s, %s) RETURNING id
                    """, (username, email, full_name))
                    user_id = self.cursor.fetchone()[0]
                    self.conn.commit()
                    return {"success": True, "user_id": user_id}
                except psycopg2.IntegrityError as e:
                    self.conn.rollback()
                    return {"success": False, "error": "User already exists"}

            def get_user(self, user_id):
                """Get user by ID"""
                self.cursor.execute("""
                    SELECT id, username, email, full_name, is_active
                    FROM users WHERE id = %s
                """, (user_id,))
                user = self.cursor.fetchone()
                if user:
                    return {
                        "success": True,
                        "user": {
                            "id": user[0],
                            "username": user[1],
                            "email": user[2],
                            "full_name": user[3],
                            "is_active": user[4]
                        }
                    }
                return {"success": False, "error": "User not found"}

            def deactivate_user(self, user_id):
                """Deactivate a user"""
                self.cursor.execute("""
                    UPDATE users SET is_active = false WHERE id = %s
                """, (user_id,))
                if self.cursor.rowcount > 0:
                    self.conn.commit()
                    return {"success": True}
                return {"success": False, "error": "User not found"}

        # Test User Service
        user_service = UserService(conn)

        print("\n🧪 Testing User Service:")

        # Create users
        result1 = user_service.create_user("alice", "alice@example.com", "Alice Johnson")
        print(f"   ✅ Created user: {result1}")

        result2 = user_service.create_user("bob", "bob@example.com", "Bob Smith")
        print(f"   ✅ Created user: {result2}")

        # Test duplicate user
        result3 = user_service.create_user("alice", "alice2@example.com", "Alice Duplicate")
        print(f"   ❌ Duplicate user test: {result3}")

        # Get user
        user_data = user_service.get_user(result1["user_id"])
        print(f"   📄 Retrieved user: {user_data['user']['username']}")

        cursor.close()
        conn.close()

        print("✅ User Service testing completed!")
        return {"alice_id": result1["user_id"], "bob_id": result2["user_id"]}

def demo_order_service(user_ids):
    """Demo Order Service with MySQL"""
    print("\n📦 Order Service Demo")
    print("=" * 50)

    with MySqlContainer("mysql:8.0") as mysql:
        print("✅ Order Service MySQL started")

        # Order Service Database
        conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        print("📊 Order Service database initialized")

        class OrderService:
            def __init__(self, db_conn):
                self.conn = db_conn
                self.cursor = db_conn.cursor()

            def create_order(self, user_id, product_name, quantity, unit_price):
                """Create a new order"""
                total_amount = quantity * unit_price
                self.cursor.execute("""
                    INSERT INTO orders (user_id, product_name, quantity, unit_price, total_amount)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, product_name, quantity, unit_price, total_amount))
                order_id = self.cursor.lastrowid
                self.conn.commit()
                return {
                    "success": True,
                    "order_id": order_id,
                    "total_amount": total_amount
                }

            def get_orders_by_user(self, user_id):
                """Get all orders for a user"""
                self.cursor.execute("""
                    SELECT id, product_name, quantity, unit_price, total_amount, status
                    FROM orders WHERE user_id = %s ORDER BY created_at DESC
                """, (user_id,))
                orders = self.cursor.fetchall()
                return {
                    "success": True,
                    "orders": [
                        {
                            "id": order[0],
                            "product_name": order[1],
                            "quantity": order[2],
                            "unit_price": float(order[3]),
                            "total_amount": float(order[4]),
                            "status": order[5]
                        }
                        for order in orders
                    ]
                }

            def update_order_status(self, order_id, status):
                """Update order status"""
                self.cursor.execute("""
                    UPDATE orders SET status = %s WHERE id = %s
                """, (status, order_id))
                if self.cursor.rowcount > 0:
                    self.conn.commit()
                    return {"success": True}
                return {"success": False, "error": "Order not found"}

        # Test Order Service
        order_service = OrderService(conn)

        print("\n🧪 Testing Order Service:")

        # Create orders
        order1 = order_service.create_order(user_ids["alice_id"], "Laptop Pro", 1, 1299.99)
        print(f"   ✅ Created order for Alice: Order #{order1['order_id']} - ${order1['total_amount']}")

        order2 = order_service.create_order(user_ids["bob_id"], "Wireless Mouse", 2, 49.99)
        print(f"   ✅ Created order for Bob: Order #{order2['order_id']} - ${order2['total_amount']}")

        order3 = order_service.create_order(user_ids["alice_id"], "USB-C Hub", 1, 79.99)
        print(f"   ✅ Created another order for Alice: Order #{order3['order_id']} - ${order3['total_amount']}")

        # Get user orders
        alice_orders = order_service.get_orders_by_user(user_ids["alice_id"])
        print(f"   📋 Alice has {len(alice_orders['orders'])} orders")

        # Update order status
        status_update = order_service.update_order_status(order1["order_id"], "confirmed")
        print(f"   ✅ Updated order status: {status_update}")

        cursor.close()
        conn.close()

        print("✅ Order Service testing completed!")
        return {"order_ids": [order1["order_id"], order2["order_id"], order3["order_id"]]}

def demo_notification_service(user_ids, order_info):
    """Demo Notification Service with Redis"""
    print("\n📢 Notification Service Demo")
    print("=" * 50)

    with RedisContainer("redis:7-alpine") as redis_container:
        print("✅ Notification Service Redis started")

        # Notification Service Cache
        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        print("📊 Notification Service cache initialized")

        class NotificationService:
            def __init__(self, redis_client):
                self.redis = redis_client

            def send_notification(self, user_id, message, notification_type="info"):
                """Send notification to user"""
                notification = {
                    "user_id": user_id,
                    "message": message,
                    "type": notification_type,
                    "timestamp": datetime.now().isoformat(),
                    "read": False
                }

                # Store in user's notification queue
                queue_key = f"notifications:{user_id}"
                self.redis.lpush(queue_key, json.dumps(notification))

                # Set expiry for 7 days
                self.redis.expire(queue_key, 7 * 24 * 3600)

                # Track notification stats
                stats_key = f"notification_stats:{notification_type}"
                self.redis.incr(stats_key)

                return {"success": True, "notification_id": f"{user_id}_{int(time.time())}"}

            def get_user_notifications(self, user_id, limit=10):
                """Get user notifications"""
                queue_key = f"notifications:{user_id}"
                notifications = self.redis.lrange(queue_key, 0, limit - 1)
                return {
                    "success": True,
                    "notifications": [json.loads(notif) for notif in notifications]
                }

            def mark_notification_read(self, user_id, index):
                """Mark specific notification as read"""
                queue_key = f"notifications:{user_id}"
                notification_json = self.redis.lindex(queue_key, index)
                if notification_json:
                    notification = json.loads(notification_json)
                    notification["read"] = True
                    self.redis.lset(queue_key, index, json.dumps(notification))
                    return {"success": True}
                return {"success": False, "error": "Notification not found"}

            def get_notification_stats(self):
                """Get notification statistics"""
                stats = {}
                for key in self.redis.keys("notification_stats:*"):
                    notification_type = key.split(":")[-1]
                    stats[notification_type] = int(self.redis.get(key))
                return stats

        # Test Notification Service
        notification_service = NotificationService(redis_client)

        print("\n🧪 Testing Notification Service:")

        # Send notifications
        notif1 = notification_service.send_notification(
            user_ids["alice_id"],
            "Welcome to our platform!",
            "welcome"
        )
        print(f"   📧 Sent welcome notification to Alice: {notif1}")

        notif2 = notification_service.send_notification(
            user_ids["alice_id"],
            f"Your order #{order_info['order_ids'][0]} has been confirmed!",
            "order_update"
        )
        print(f"   📦 Sent order notification to Alice: {notif2}")

        notif3 = notification_service.send_notification(
            user_ids["bob_id"],
            "Welcome to our platform!",
            "welcome"
        )
        print(f"   📧 Sent welcome notification to Bob: {notif3}")

        # Get user notifications
        alice_notifications = notification_service.get_user_notifications(user_ids["alice_id"])
        print(f"   📋 Alice has {len(alice_notifications['notifications'])} notifications")

        # Mark notification as read
        read_result = notification_service.mark_notification_read(user_ids["alice_id"], 0)
        print(f"   ✅ Marked notification as read: {read_result}")

        # Get stats
        stats = notification_service.get_notification_stats()
        print(f"   📊 Notification stats: {stats}")

        print("✅ Notification Service testing completed!")

def demo_service_integration():
    """Demo integration between all services"""
    print("\n🔗 Service Integration Demo")
    print("=" * 50)

    # This simulates how microservices work together
    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container:

        print("✅ All microservices started")

        # Setup all services (simplified)
        # User Service
        user_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        # Order Service
        order_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )

        # Notification Service
        notif_redis = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Quick setup
        user_cursor = user_conn.cursor()
        user_cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(50), email VARCHAR(100))")
        user_conn.commit()

        order_cursor = order_conn.cursor()
        order_cursor.execute("CREATE TABLE orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_name VARCHAR(100), total_amount DECIMAL(10,2))")
        order_conn.commit()

        print("📊 All services initialized")

        # Simulate complete user journey
        print("\n🚀 Simulating complete user journey:")

        # 1. User registration
        user_cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", ("charlie", "charlie@example.com"))
        user_id = user_cursor.fetchone()[0]
        user_conn.commit()
        print(f"   👤 User registered: charlie (ID: {user_id})")

        # 2. Send welcome notification
        welcome_notif = {
            "user_id": user_id,
            "message": "Welcome Charlie! Thanks for joining us.",
            "type": "welcome",
            "timestamp": datetime.now().isoformat()
        }
        notif_redis.lpush(f"notifications:{user_id}", json.dumps(welcome_notif))
        print(f"   📧 Welcome notification sent")

        # 3. User places order
        order_cursor.execute("""
            INSERT INTO orders (user_id, product_name, total_amount)
            VALUES (%s, %s, %s)
        """, (user_id, "Premium Headphones", 199.99))
        order_id = order_cursor.lastrowid
        order_conn.commit()
        print(f"   📦 Order placed: #{order_id} for $199.99")

        # 4. Send order confirmation notification
        order_notif = {
            "user_id": user_id,
            "message": f"Order #{order_id} confirmed! Your Premium Headphones will ship soon.",
            "type": "order_confirmation",
            "timestamp": datetime.now().isoformat()
        }
        notif_redis.lpush(f"notifications:{user_id}", json.dumps(order_notif))
        print(f"   📧 Order confirmation notification sent")

        # 5. Check user's complete state
        print(f"\n📊 Complete user state for Charlie:")

        # User info
        user_cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
        user_info = user_cursor.fetchone()
        print(f"   👤 User: {user_info[0]} ({user_info[1]})")

        # Orders
        order_cursor.execute("SELECT id, product_name, total_amount FROM orders WHERE user_id = %s", (user_id,))
        orders = order_cursor.fetchall()
        print(f"   📦 Orders: {len(orders)} orders totaling ${sum(float(order[2]) for order in orders)}")

        # Notifications
        notifications = notif_redis.lrange(f"notifications:{user_id}", 0, -1)
        print(f"   📧 Notifications: {len(notifications)} notifications")

        user_cursor.close()
        user_conn.close()
        order_cursor.close()
        order_conn.close()

        print("✅ Service integration demo completed!")

def main():
    """Run Lab 7"""
    print_header()

    try:
        # Test individual services
        user_ids = demo_user_service()
        time.sleep(1)

        order_info = demo_order_service(user_ids)
        time.sleep(1)

        demo_notification_service(user_ids, order_info)
        time.sleep(1)

        # Test service integration
        demo_service_integration()

        print("\n" + "=" * 60)
        print("🎉 LAB 7 COMPLETED!")
        print("=" * 60)
        print("\nWhat you learned:")
        print("✅ Microservices architecture testing")
        print("✅ Multi-database service coordination")
        print("✅ Inter-service communication patterns")
        print("✅ Service isolation and integration testing")
        print("✅ Real-world microservices scenarios")

        print("\n🚀 Ready for Lab 8? Learn about advanced testing patterns!")

        return True

    except Exception as e:
        print(f"\n❌ Lab failed: {e}")
        print("Make sure Docker is running and try again.")
        return False

if __name__ == "__main__":
    main()