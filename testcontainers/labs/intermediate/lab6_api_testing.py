#!/usr/bin/env python3
"""
Lab 6: API Testing
==================

Learn how to test APIs that interact with databases using TestContainers.
"""

import os
import json

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    from testcontainers.redis import RedisContainer
    import psycopg2
    import redis
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary redis")
    exit(1)

def demo_simple_api_testing():
    """Simple API testing with database"""
    print("🌐 Simple API Testing")

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
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # API functions
        def create_user(name, email):
            try:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                    (name, email)
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return {"status": "success", "user_id": user_id, "name": name, "email": email}
            except psycopg2.IntegrityError:
                conn.rollback()
                return {"status": "error", "message": "Email already exists"}

        def get_user(user_id):
            cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return {"status": "success", "user": {"id": user[0], "name": user[1], "email": user[2]}}
            else:
                return {"status": "error", "message": "User not found"}

        def list_users():
            cursor.execute("SELECT id, name, email FROM users ORDER BY id")
            users = cursor.fetchall()
            return {
                "status": "success",
                "users": [{"id": u[0], "name": u[1], "email": u[2]} for u in users],
                "count": len(users)
            }

        # Test API operations
        print("🧪 Testing API operations:")

        # Create users
        result1 = create_user("Alice Johnson", "alice@example.com")
        result2 = create_user("Bob Smith", "bob@example.com")
        print(f"✅ Created users: {result1['name']}, {result2['name']}")

        # Test duplicate email
        result3 = create_user("Alice Duplicate", "alice@example.com")
        print(f"❌ Duplicate email test: {result3['message']}")

        # Get user
        user_result = get_user(result1["user_id"])
        print(f"✅ Retrieved user: {user_result['user']['name']}")

        # List users
        list_result = list_users()
        print(f"✅ Listed {list_result['count']} users")

        # Test non-existent user
        not_found_result = get_user(999)
        print(f"❌ Non-existent user test: {not_found_result['message']}")

        cursor.close()
        conn.close()

def demo_api_with_caching():
    """API testing with database and caching"""
    print("\n⚡ API with Caching")

    with PostgresContainer("postgres:15-alpine") as postgres, \
         RedisContainer("redis:7-alpine") as redis_container:

        # Setup database
        pg_conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )

        # Setup Redis
        redis_client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                price DECIMAL(10,2),
                description TEXT
            )
        """)

        # Insert sample products
        products = [
            ("Laptop Pro", 1299.99, "High-performance laptop for professionals"),
            ("Wireless Mouse", 49.99, "Ergonomic wireless mouse with long battery"),
            ("Mechanical Keyboard", 129.99, "RGB backlit mechanical keyboard"),
            ("USB-C Hub", 79.99, "7-in-1 USB-C hub for connectivity")
        ]

        for name, price, desc in products:
            pg_cursor.execute(
                "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)",
                (name, price, desc)
            )
        pg_conn.commit()

        # API functions with caching
        def get_product_with_cache(product_id):
            cache_key = f"product:{product_id}"

            # Try cache first
            cached_product = redis_client.get(cache_key)
            if cached_product:
                return {
                    "status": "success",
                    "product": json.loads(cached_product),
                    "source": "cache"
                }

            # Query database
            pg_cursor.execute(
                "SELECT id, name, price, description FROM products WHERE id = %s",
                (product_id,)
            )
            product = pg_cursor.fetchone()

            if product:
                product_data = {
                    "id": product[0],
                    "name": product[1],
                    "price": float(product[2]),
                    "description": product[3]
                }

                # Cache for 5 minutes
                redis_client.setex(cache_key, 300, json.dumps(product_data))

                return {
                    "status": "success",
                    "product": product_data,
                    "source": "database"
                }
            else:
                return {"status": "error", "message": "Product not found"}

        def search_products(keyword):
            cache_key = f"search:{keyword.lower()}"

            # Try cache first
            cached_results = redis_client.get(cache_key)
            if cached_results:
                return {
                    "status": "success",
                    "results": json.loads(cached_results),
                    "source": "cache"
                }

            # Query database
            pg_cursor.execute(
                "SELECT id, name, price FROM products WHERE name ILIKE %s OR description ILIKE %s",
                (f"%{keyword}%", f"%{keyword}%")
            )
            products = pg_cursor.fetchall()

            results = [
                {"id": p[0], "name": p[1], "price": float(p[2])}
                for p in products
            ]

            # Cache search results for 2 minutes
            redis_client.setex(cache_key, 120, json.dumps(results))

            return {
                "status": "success",
                "results": results,
                "source": "database"
            }

        # Test caching behavior
        print("🧪 Testing API with caching:")

        # Get product (from database)
        result1 = get_product_with_cache(1)
        print(f"✅ First call (DB): {result1['product']['name']} - Source: {result1['source']}")

        # Get same product (from cache)
        result2 = get_product_with_cache(1)
        print(f"⚡ Second call (Cache): {result2['product']['name']} - Source: {result2['source']}")

        # Search products
        search1 = search_products("laptop")
        print(f"✅ Search 'laptop' (DB): Found {len(search1['results'])} products - Source: {search1['source']}")

        search2 = search_products("laptop")
        print(f"⚡ Search 'laptop' (Cache): Found {len(search2['results'])} products - Source: {search2['source']}")

        # Different search
        search3 = search_products("mouse")
        print(f"✅ Search 'mouse' (DB): Found {len(search3['results'])} products - Source: {search3['source']}")

        # Show cache statistics
        cache_keys = redis_client.keys("*")
        print(f"📊 Cache statistics: {len(cache_keys)} cached items")

        pg_cursor.close()
        pg_conn.close()

def demo_api_error_scenarios():
    """API error scenarios testing"""
    print("\n🚨 API Error Scenarios")

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
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER CHECK (quantity > 0),
                total DECIMAL(10,2) CHECK (total >= 0),
                status VARCHAR(20) DEFAULT 'pending'
            )
        """)
        conn.commit()

        def create_order(user_id, product_id, quantity, total):
            try:
                # Validate inputs
                if quantity <= 0:
                    return {"status": "error", "message": "Quantity must be positive"}

                if total < 0:
                    return {"status": "error", "message": "Total cannot be negative"}

                cursor.execute("""
                    INSERT INTO orders (user_id, product_id, quantity, total)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (user_id, product_id, quantity, total))

                order_id = cursor.fetchone()[0]
                conn.commit()

                return {
                    "status": "success",
                    "order_id": order_id,
                    "user_id": user_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "total": total
                }

            except psycopg2.Error as e:
                conn.rollback()
                return {"status": "error", "message": f"Database error: {str(e)}"}

        def get_order_stats():
            cursor.execute("""
                SELECT
                    COUNT(*) as total_orders,
                    SUM(total) as total_revenue,
                    AVG(total) as avg_order_value
                FROM orders
            """)
            stats = cursor.fetchone()
            return {
                "total_orders": stats[0],
                "total_revenue": float(stats[1]) if stats[1] else 0,
                "avg_order_value": float(stats[2]) if stats[2] else 0
            }

        # Test error scenarios
        print("🧪 Testing error scenarios:")

        # Valid orders
        valid_order1 = create_order(1, 101, 2, 199.98)
        valid_order2 = create_order(2, 102, 1, 49.99)
        print(f"✅ Valid orders: {valid_order1['order_id']}, {valid_order2['order_id']}")

        # Invalid quantity
        invalid_quantity = create_order(1, 101, -1, 100.00)
        print(f"❌ Invalid quantity: {invalid_quantity['message']}")

        # Invalid total
        invalid_total = create_order(1, 101, 1, -50.00)
        print(f"❌ Invalid total: {invalid_total['message']}")

        # Database constraint violations
        try:
            cursor.execute("""
                INSERT INTO orders (user_id, product_id, quantity, total)
                VALUES (%s, %s, %s, %s)
            """, (1, 101, -5, 100.00))
            conn.commit()
            print("Unexpected success with negative quantity")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"✅ Database correctly rejected negative quantity: {type(e).__name__}")

        # Get statistics
        stats = get_order_stats()
        print(f"📊 Order stats: {stats['total_orders']} orders, ${stats['total_revenue']:.2f} revenue")

        cursor.close()
        conn.close()

def main():
    """Run Lab 6"""
    print("🌐 LAB 6: API Testing")
    print("=" * 40)
    
    try:
        demo_simple_api_testing()
        demo_api_with_caching()
        demo_api_error_scenarios()
        
        print("\n✅ Lab 6 completed!")
        print("Key concepts learned:")
        print("• API testing with real databases")
        print("• Testing API operations (CRUD)")
        print("• Database and cache integration testing")
        print("• Error scenario testing")
        print("• API performance with caching patterns")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()