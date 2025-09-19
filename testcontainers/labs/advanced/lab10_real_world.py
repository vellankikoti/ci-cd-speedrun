#!/usr/bin/env python3
"""
Lab 10: Real-World Scenarios (Simple Version)
=============================================

Apply everything you've learned to test real-world applications
including e-commerce systems, monitoring, and production patterns.
"""

import os
import time

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

import json
import uuid
from datetime import datetime, timedelta
import random

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
    print(f"❌ Missing required packages: {e}")
    print("Please run: python3 setup.py from testcontainers directory")
    exit(1)

def print_header():
    """Print lab header"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║               🌍 LAB 10: REAL-WORLD SCENARIOS 🌍               ║
║                                                                  ║
║  Test complete applications with realistic data and scenarios.   ║
║  This is your final challenge - production-ready testing!       ║
╚══════════════════════════════════════════════════════════════════╝
""")

def demo_ecommerce_system():
    """Demo complete e-commerce system testing"""
    print("\n🛒 E-Commerce System Testing")
    print("=" * 50)

    with PostgresContainer("postgres:15-alpine") as postgres, \
         MySqlContainer("mysql:8.0") as mysql, \
         RedisContainer("redis:7-alpine") as redis_container, \
         MongoDbContainer("mongo:7.0") as mongo:

        print("✅ All e-commerce services started")

        # Setup User Service (PostgreSQL)
        user_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        user_cursor = user_conn.cursor()
        user_cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                address TEXT,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT true
            )
        """)

        user_cursor.execute("""
            CREATE TABLE user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_token VARCHAR(255) UNIQUE,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        user_conn.commit()

        # Setup Product Service (MySQL)
        product_conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user=mysql.username,
            password=mysql.password,
            database=mysql.dbname
        )

        product_cursor = product_conn.cursor()
        product_cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INT DEFAULT 0,
                category_id INT,
                sku VARCHAR(100) UNIQUE,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        product_cursor.execute("""
            CREATE TABLE categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                parent_id INT
            )
        """)

        product_cursor.execute("""
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                order_number VARCHAR(50) UNIQUE,
                total_amount DECIMAL(10,2) NOT NULL,
                status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
                shipping_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        product_cursor.execute("""
            CREATE TABLE order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT REFERENCES orders(id),
                product_id INT,
                quantity INT NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_price DECIMAL(10,2) NOT NULL
            )
        """)
        product_conn.commit()

        # Setup Cache Service (Redis)
        cache_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Setup Analytics Service (MongoDB)
        mongo_client = pymongo.MongoClient(mongo.get_connection_url())
        analytics_db = mongo_client.ecommerce_analytics

        print("📊 All databases initialized")

        # Seed data
        print("\n🌱 Seeding test data...")

        # Categories
        categories = [
            ("Electronics", "Electronic devices and gadgets"),
            ("Computers", "Laptops, desktops, and accessories"),
            ("Mobile", "Smartphones and accessories"),
            ("Home", "Home and garden items")
        ]

        category_ids = {}
        for name, desc in categories:
            product_cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, desc))
            category_ids[name] = product_cursor.lastrowid
        product_conn.commit()

        # Products
        products = [
            ("MacBook Pro 16\"", "High-performance laptop for professionals", 2499.99, 10, "Electronics", "MBP16-001"),
            ("iPhone 15 Pro", "Latest smartphone with advanced features", 999.99, 25, "Mobile", "IP15P-001"),
            ("Wireless Mouse", "Ergonomic wireless mouse", 49.99, 100, "Computers", "WM-001"),
            ("USB-C Hub", "7-in-1 USB-C connectivity hub", 79.99, 50, "Computers", "USBCH-001"),
            ("Smart Home Speaker", "Voice-controlled smart speaker", 129.99, 30, "Home", "SHS-001")
        ]

        product_ids = {}
        for name, desc, price, stock, category, sku in products:
            product_cursor.execute("""
                INSERT INTO products (name, description, price, stock_quantity, category_id, sku)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, category_ids[category], sku))
            product_ids[name] = product_cursor.lastrowid
        product_conn.commit()

        # Users
        users = [
            ("alice@example.com", "Alice", "Johnson", "123 Main St, City, State", "+1-555-0101"),
            ("bob@example.com", "Bob", "Smith", "456 Oak Ave, City, State", "+1-555-0102"),
            ("carol@example.com", "Carol", "Davis", "789 Pine Rd, City, State", "+1-555-0103"),
            ("david@example.com", "David", "Wilson", "321 Elm St, City, State", "+1-555-0104")
        ]

        user_ids = {}
        for email, first, last, address, phone in users:
            user_cursor.execute("""
                INSERT INTO users (email, first_name, last_name, address, phone)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (email, first, last, address, phone))
            user_ids[email] = user_cursor.fetchone()[0]
        user_conn.commit()

        print(f"   📦 Created {len(products)} products in {len(categories)} categories")
        print(f"   👥 Created {len(users)} user accounts")

        # Simulate real e-commerce workflows
        print("\n🛍️ Simulating e-commerce workflows...")

        def create_user_session(user_id):
            """Create user session"""
            session_token = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(hours=24)

            user_cursor.execute("""
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (%s, %s, %s)
            """, (user_id, session_token, expires_at))
            user_conn.commit()

            # Cache session in Redis
            cache_client.setex(f"session:{session_token}", 86400, json.dumps({
                "user_id": user_id,
                "created_at": datetime.now().isoformat()
            }))

            return session_token

        def add_to_cart(session_token, product_id, quantity):
            """Add item to shopping cart"""
            cart_key = f"cart:{session_token}"
            cache_client.hset(cart_key, str(product_id), quantity)
            cache_client.expire(cart_key, 3600)  # 1 hour expiry

        def create_order(session_token):
            """Create order from cart"""
            cart_key = f"cart:{session_token}"
            cart_items = cache_client.hgetall(cart_key)

            if not cart_items:
                return None

            # Get user from session
            session_data = cache_client.get(f"session:{session_token}")
            if not session_data:
                return None

            session_info = json.loads(session_data)
            user_id = session_info["user_id"]

            # Get user details
            user_cursor.execute("SELECT first_name, last_name, address FROM users WHERE id = %s", (user_id,))
            user_data = user_cursor.fetchone()

            # Calculate total
            total_amount = 0
            order_items = []

            for product_id, quantity in cart_items.items():
                product_cursor.execute("SELECT name, price FROM products WHERE id = %s", (int(product_id),))
                product_data = product_cursor.fetchone()

                if product_data:
                    name, price = product_data
                    quantity = int(quantity)
                    item_total = float(price) * quantity
                    total_amount += item_total

                    order_items.append({
                        "product_id": int(product_id),
                        "name": name,
                        "quantity": quantity,
                        "unit_price": float(price),
                        "total_price": item_total
                    })

            # Create order
            order_number = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"

            product_cursor.execute("""
                INSERT INTO orders (user_id, order_number, total_amount, shipping_address)
                VALUES (%s, %s, %s, %s)
            """, (user_id, order_number, total_amount, user_data[2]))
            order_id = product_cursor.lastrowid

            # Add order items
            for item in order_items:
                product_cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item["product_id"], item["quantity"], item["unit_price"], item["total_price"]))

            product_conn.commit()

            # Clear cart
            cache_client.delete(cart_key)

            # Log analytics
            analytics_db.order_events.insert_one({
                "event_type": "order_created",
                "order_id": order_id,
                "order_number": order_number,
                "user_id": user_id,
                "total_amount": total_amount,
                "items_count": len(order_items),
                "timestamp": datetime.now()
            })

            return {
                "order_id": order_id,
                "order_number": order_number,
                "total_amount": total_amount,
                "items": order_items
            }

        # Simulate user journeys
        print("   🛒 Simulating user shopping journeys...")

        # Alice's journey
        alice_session = create_user_session(user_ids["alice@example.com"])
        add_to_cart(alice_session, product_ids["MacBook Pro 16\""], 1)
        add_to_cart(alice_session, product_ids["Wireless Mouse"], 1)
        alice_order = create_order(alice_session)
        print(f"   ✅ Alice's order: {alice_order['order_number']} - ${alice_order['total_amount']}")

        # Bob's journey
        bob_session = create_user_session(user_ids["bob@example.com"])
        add_to_cart(bob_session, product_ids["iPhone 15 Pro"], 1)
        add_to_cart(bob_session, product_ids["USB-C Hub"], 1)
        bob_order = create_order(bob_session)
        print(f"   ✅ Bob's order: {bob_order['order_number']} - ${bob_order['total_amount']}")

        # Carol's journey
        carol_session = create_user_session(user_ids["carol@example.com"])
        add_to_cart(carol_session, product_ids["Smart Home Speaker"], 2)
        carol_order = create_order(carol_session)
        print(f"   ✅ Carol's order: {carol_order['order_number']} - ${carol_order['total_amount']}")

        # Analytics and reporting
        print("\n📊 Running analytics and reports...")

        # Order statistics
        product_cursor.execute("""
            SELECT COUNT(*) as total_orders, SUM(total_amount) as total_revenue
            FROM orders
        """)
        order_stats = product_cursor.fetchone()
        print(f"   📈 Total orders: {order_stats[0]}, Revenue: ${order_stats[1]}")

        # Top products
        product_cursor.execute("""
            SELECT p.name, SUM(oi.quantity) as total_sold
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY p.name
            ORDER BY total_sold DESC
            LIMIT 3
        """)
        top_products = product_cursor.fetchall()
        print(f"   🏆 Top products:")
        for product, sold in top_products:
            print(f"     {product}: {sold} sold")

        # Cache statistics
        session_keys = cache_client.keys("session:*")
        cart_keys = cache_client.keys("cart:*")
        print(f"   💾 Cache: {len(session_keys)} active sessions, {len(cart_keys)} active carts")

        # MongoDB analytics
        total_events = analytics_db.order_events.count_documents({})
        print(f"   📊 Analytics: {total_events} events logged")

        # Clean up connections
        user_cursor.close()
        user_conn.close()
        product_cursor.close()
        product_conn.close()
        mongo_client.close()

        print("✅ E-commerce system testing completed!")

def demo_monitoring_system():
    """Demo application monitoring and metrics"""
    print("\n📊 Monitoring System Demo")
    print("=" * 50)

    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        print("✅ Monitoring infrastructure started")

        # Metrics Database
        metrics_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        metrics_cursor = metrics_conn.cursor()
        metrics_cursor.execute("""
            CREATE TABLE system_metrics (
                id SERIAL PRIMARY KEY,
                metric_name VARCHAR(100),
                metric_value DECIMAL(10,4),
                metric_unit VARCHAR(20),
                service_name VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        metrics_cursor.execute("""
            CREATE TABLE alerts (
                id SERIAL PRIMARY KEY,
                alert_name VARCHAR(100),
                severity VARCHAR(20),
                message TEXT,
                service_name VARCHAR(50),
                is_resolved BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            )
        """)
        metrics_conn.commit()

        # Metrics Cache
        metrics_cache = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        print("📊 Monitoring system initialized")

        class MonitoringSystem:
            def __init__(self, db_conn, cache_client):
                self.conn = db_conn
                self.cursor = db_conn.cursor()
                self.cache = cache_client

            def record_metric(self, name, value, unit, service):
                """Record a system metric"""
                self.cursor.execute("""
                    INSERT INTO system_metrics (metric_name, metric_value, metric_unit, service_name)
                    VALUES (%s, %s, %s, %s)
                """, (name, value, unit, service))
                self.conn.commit()

                # Cache latest value
                cache_key = f"metric:{service}:{name}"
                self.cache.setex(cache_key, 300, str(value))

            def create_alert(self, name, severity, message, service):
                """Create system alert"""
                self.cursor.execute("""
                    INSERT INTO alerts (alert_name, severity, message, service_name)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (name, severity, message, service))
                alert_id = self.cursor.fetchone()[0]
                self.conn.commit()

                # Cache active alert
                alert_key = f"alert:{alert_id}"
                self.cache.setex(alert_key, 3600, json.dumps({
                    "name": name,
                    "severity": severity,
                    "message": message,
                    "service": service
                }))

                return alert_id

            def get_service_health(self, service):
                """Get service health metrics"""
                # Get latest metrics from cache
                cpu_usage = self.cache.get(f"metric:{service}:cpu_usage")
                memory_usage = self.cache.get(f"metric:{service}:memory_usage")
                response_time = self.cache.get(f"metric:{service}:response_time")

                # Check for active alerts
                alert_keys = self.cache.keys(f"alert:*")
                active_alerts = 0
                for key in alert_keys:
                    alert_data = self.cache.get(key)
                    if alert_data:
                        alert = json.loads(alert_data)
                        if alert["service"] == service:
                            active_alerts += 1

                return {
                    "service": service,
                    "cpu_usage": float(cpu_usage) if cpu_usage else None,
                    "memory_usage": float(memory_usage) if memory_usage else None,
                    "response_time": float(response_time) if response_time else None,
                    "active_alerts": active_alerts,
                    "status": "degraded" if active_alerts > 0 else "healthy"
                }

        # Test monitoring system
        monitor = MonitoringSystem(metrics_conn, metrics_cache)

        print("\n🔍 Simulating system monitoring...")

        # Simulate metrics collection
        services = ["web_server", "database", "cache", "api_gateway"]

        for i in range(10):
            for service in services:
                # Generate realistic metrics
                cpu_usage = random.uniform(10, 85)
                memory_usage = random.uniform(20, 75)
                response_time = random.uniform(50, 500)

                monitor.record_metric("cpu_usage", cpu_usage, "percent", service)
                monitor.record_metric("memory_usage", memory_usage, "percent", service)
                monitor.record_metric("response_time", response_time, "milliseconds", service)

                # Create alerts for high usage
                if cpu_usage > 80:
                    monitor.create_alert(
                        "High CPU Usage",
                        "warning",
                        f"CPU usage is {cpu_usage:.1f}%",
                        service
                    )

                if memory_usage > 70:
                    monitor.create_alert(
                        "High Memory Usage",
                        "warning",
                        f"Memory usage is {memory_usage:.1f}%",
                        service
                    )

                if response_time > 400:
                    monitor.create_alert(
                        "Slow Response Time",
                        "critical",
                        f"Response time is {response_time:.0f}ms",
                        service
                    )

            time.sleep(0.1)  # Simulate time passing

        print("   📊 Collected 10 rounds of metrics from 4 services")

        # Generate monitoring reports
        print("\n📋 Monitoring Reports:")

        for service in services:
            health = monitor.get_service_health(service)
            print(f"   🖥️ {service}:")
            print(f"     Status: {health['status']}")
            if health['cpu_usage']:
                print(f"     CPU: {health['cpu_usage']:.1f}%")
            if health['memory_usage']:
                print(f"     Memory: {health['memory_usage']:.1f}%")
            if health['response_time']:
                print(f"     Response Time: {health['response_time']:.0f}ms")
            print(f"     Active Alerts: {health['active_alerts']}")

        # Overall system statistics
        metrics_cursor.execute("""
            SELECT service_name, AVG(metric_value) as avg_cpu
            FROM system_metrics
            WHERE metric_name = 'cpu_usage'
            GROUP BY service_name
        """)
        cpu_averages = metrics_cursor.fetchall()

        print(f"\n📊 System Overview:")
        for service, avg_cpu in cpu_averages:
            print(f"   {service}: Avg CPU {avg_cpu:.1f}%")

        # Alert summary
        metrics_cursor.execute("""
            SELECT severity, COUNT(*) as alert_count
            FROM alerts
            GROUP BY severity
        """)
        alert_summary = metrics_cursor.fetchall()

        print(f"   🚨 Alerts Generated:")
        for severity, count in alert_summary:
            print(f"     {severity}: {count} alerts")

        metrics_cursor.close()
        metrics_conn.close()

        print("✅ Monitoring system demo completed!")

def main():
    """Run Lab 10"""
    print_header()

    try:
        demo_ecommerce_system()
        time.sleep(2)

        demo_monitoring_system()

        print("\n" + "=" * 60)
        print("🎉 LAB 10 COMPLETED!")
        print("=" * 60)
        print("\nCongratulations! You've completed the final lab!")
        print("\nWhat you mastered:")
        print("✅ Complete e-commerce system testing")
        print("✅ Multi-service integration patterns")
        print("✅ Real-world data scenarios")
        print("✅ System monitoring and alerting")
        print("✅ Production-ready testing strategies")

        print("\n🏆 You are now a TestContainers Expert!")
        print("🚀 Ready to test any application with confidence!")

        return True

    except Exception as e:
        print(f"\n❌ Lab failed: {e}")
        print("Make sure Docker is running and try again.")
        return False

if __name__ == "__main__":
    main()