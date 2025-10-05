#!/usr/bin/env python3
"""
Lab 3: Data Management - Working Examples
=========================================

Master test data setup, teardown, and isolation patterns with TestContainers.
Learn professional data management techniques for reliable testing.
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
        'psycopg2': 'psycopg2-binary'
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
    import psycopg2
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary")
    sys.exit(1)

def demo_setup_teardown():
    """Setup and teardown patterns with real data"""
    print("\n🔄 Setup & Teardown Demo...")
    
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
        
        # Setup phase - Create schema
        print("📊 Setting up test schema...")
        cursor.execute("""
            CREATE TABLE customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                total_amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("📊 Tables Created: customers, orders")
        
        # Insert test data
        customers = [
            ("Alice Johnson", "alice@example.com"),
            ("Bob Smith", "bob@example.com"),
            ("Carol Davis", "carol@example.com")
        ]
        
        print("📝 Inserting Test Customers:")
        for name, email in customers:
            cursor.execute(
                "INSERT INTO customers (name, email) VALUES (%s, %s)",
                (name, email)
            )
            print(f"   + {name} ({email})")
        
        # Insert orders
        orders = [
            (1, 299.99, "completed"),
            (1, 149.99, "pending"),
            (2, 89.99, "shipped"),
            (3, 459.99, "completed")
        ]
        
        print("📝 Inserting Test Orders:")
        for customer_id, amount, status in orders:
            cursor.execute(
                "INSERT INTO orders (customer_id, total_amount, status) VALUES (%s, %s, %s)",
                (customer_id, amount, status)
            )
            print(f"   + Order for Customer {customer_id}: ${amount} ({status})")
        
        conn.commit()
        
        # Verify setup
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        print(f"\n📊 Setup Complete: {customer_count} customers, {order_count} orders")
        
        # Test data isolation
        print(f"\n🧪 Testing Data Isolation:")
        cursor.execute("""
            SELECT c.name, COUNT(o.id) as order_count, 
                   SUM(o.total_amount) as total_spent,
                   AVG(o.total_amount) as avg_order
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name
            ORDER BY total_spent DESC
        """)
        
        results = cursor.fetchall()
        for name, order_count, total_spent, avg_order in results:
            print(f"   👤 {name}: {order_count} orders | Total: ${total_spent or 0:.2f} | Avg: ${avg_order or 0:.2f}")
        
        # Teardown phase
        print(f"\n🧹 Teardown Phase:")
        cursor.execute("DROP TABLE orders CASCADE")
        print("   - Dropped orders table")
        cursor.execute("DROP TABLE customers CASCADE")
        print("   - Dropped customers table")
        
        cursor.close()
        conn.close()
        print("✅ Teardown complete - database is clean!")

def demo_data_factories():
    """Data factory patterns for generating test data"""
    print("\n🏭 Data Factory Demo...")
    
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
        
        # Create products table
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                in_stock BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Table Created: products")
        
        # Data factory functions
        def create_electronics_products(count):
            products = []
            electronics = ["Laptop", "Phone", "Tablet", "Headphones", "Mouse", "Keyboard", "Monitor", "Camera"]
            for i in range(count):
                name = f"{electronics[i % len(electronics)]} {i+1}"
                price = round(50 + (i * 25.50), 2)
                products.append((name, price, "Electronics", True))
            return products
        
        def create_kitchen_products(count):
            products = []
            kitchen = ["Coffee Mug", "Plate", "Bowl", "Spoon", "Fork", "Knife", "Cutting Board", "Pan"]
            for i in range(count):
                name = f"{kitchen[i % len(kitchen)]} {i+1}"
                price = round(5 + (i * 2.50), 2)
                products.append((name, price, "Kitchen", True))
            return products
        
        def create_books(count):
            products = []
            subjects = ["Python", "JavaScript", "Database", "DevOps", "Machine Learning", "Web Development"]
            for i in range(count):
                name = f"{subjects[i % len(subjects)]} Programming Book {i+1}"
                price = round(20 + (i * 5.00), 2)
                products.append((name, price, "Books", True))
            return products
        
        # Generate test data using factories
        print("🏭 Generating Test Data with Factories:")
        
        electronics = create_electronics_products(5)
        print(f"   📱 Electronics: {len(electronics)} products")
        for name, price, category, in_stock in electronics:
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (%s, %s, %s, %s)",
                (name, price, category, in_stock)
            )
            print(f"      + {name} - ${price}")
        
        kitchen = create_kitchen_products(3)
        print(f"   🍽️  Kitchen: {len(kitchen)} products")
        for name, price, category, in_stock in kitchen:
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (%s, %s, %s, %s)",
                (name, price, category, in_stock)
            )
            print(f"      + {name} - ${price}")
        
        books = create_books(4)
        print(f"   📚 Books: {len(books)} products")
        for name, price, category, in_stock in books:
            cursor.execute(
                "INSERT INTO products (name, price, category, in_stock) VALUES (%s, %s, %s, %s)",
                (name, price, category, in_stock)
            )
            print(f"      + {name} - ${price}")
        
        conn.commit()
        
        # Analyze generated data
        print(f"\n📊 Generated Data Analysis:")
        cursor.execute("""
            SELECT category, COUNT(*) as count, 
                   AVG(price) as avg_price,
                   MIN(price) as min_price,
                   MAX(price) as max_price
            FROM products 
            GROUP BY category 
            ORDER BY avg_price DESC
        """)
        
        results = cursor.fetchall()
        for category, count, avg_price, min_price, max_price in results:
            print(f"   {category}: {count} items | Avg: ${avg_price:.2f} | Range: ${min_price:.2f}-${max_price:.2f}")
        
        cursor.close()
        conn.close()

def demo_test_isolation():
    """Test isolation patterns - each test gets clean data"""
    print("\n🔒 Test Isolation Demo...")
    
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
        
        # Create test table
        cursor.execute("""
            CREATE TABLE test_results (
                id SERIAL PRIMARY KEY,
                test_name VARCHAR(100) NOT NULL,
                result VARCHAR(20) NOT NULL,
                execution_time DECIMAL(5,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Table Created: test_results")
        
        # Simulate multiple test runs
        test_scenarios = [
            ("User Registration Test", "PASS", 0.125),
            ("Login Test", "PASS", 0.089),
            ("Password Reset Test", "FAIL", 0.234),
            ("Profile Update Test", "PASS", 0.156),
            ("Data Export Test", "PASS", 0.445),
            ("Email Notification Test", "FAIL", 0.178)
        ]
        
        print(f"\n🧪 Simulating Test Runs:")
        for test_name, result, execution_time in test_scenarios:
            cursor.execute(
                "INSERT INTO test_results (test_name, result, execution_time) VALUES (%s, %s, %s)",
                (test_name, result, execution_time)
            )
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"   {status_icon} {test_name}: {result} ({execution_time}s)")
        
        conn.commit()
        
        # Test isolation - each test gets fresh data
        print(f"\n🔒 Testing Isolation - Fresh Data for Each Test:")
        
        # Simulate test 1
        print(f"\n   Test 1: User Management Tests")
        cursor.execute("SELECT COUNT(*) FROM test_results")
        count_before = cursor.fetchone()[0]
        print(f"      Data before test: {count_before} records")
        
        # Add test-specific data
        cursor.execute("INSERT INTO test_results (test_name, result, execution_time) VALUES (%s, %s, %s)",
                      ("User Creation Test", "PASS", 0.067))
        cursor.execute("INSERT INTO test_results (test_name, result, execution_time) VALUES (%s, %s, %s)",
                      ("User Deletion Test", "PASS", 0.034))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM test_results")
        count_after = cursor.fetchone()[0]
        print(f"      Data after test: {count_after} records")
        print(f"      Test added: {count_after - count_before} records")
        
        # Simulate test 2 (should start fresh)
        print(f"\n   Test 2: Payment Processing Tests")
        cursor.execute("SELECT COUNT(*) FROM test_results")
        count_before = cursor.fetchone()[0]
        print(f"      Data before test: {count_before} records")
        
        # Add test-specific data
        cursor.execute("INSERT INTO test_results (test_name, result, execution_time) VALUES (%s, %s, %s)",
                      ("Payment Success Test", "PASS", 0.123))
        cursor.execute("INSERT INTO test_results (test_name, result, execution_time) VALUES (%s, %s, %s)",
                      ("Payment Failure Test", "PASS", 0.089))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM test_results")
        count_after = cursor.fetchone()[0]
        print(f"      Data after test: {count_after} records")
        print(f"      Test added: {count_after - count_before} records")
        
        # Show final test results
        print(f"\n📊 Final Test Results Summary:")
        cursor.execute("""
            SELECT result, COUNT(*) as count, 
                   AVG(execution_time) as avg_time,
                   MIN(execution_time) as min_time,
                   MAX(execution_time) as max_time
            FROM test_results 
            GROUP BY result 
            ORDER BY count DESC
        """)
        
        results = cursor.fetchall()
        for result, count, avg_time, min_time, max_time in results:
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"   {status_icon} {result}: {count} tests | Avg: {avg_time:.3f}s | Range: {min_time:.3f}s-{max_time:.3f}s")
        
        cursor.close()
        conn.close()

def demo_data_cleanup():
    """Data cleanup patterns - automated cleanup"""
    print("\n🧹 Data Cleanup Demo...")
    
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
        
        # Create temporary data table
        cursor.execute("""
            CREATE TABLE temp_data (
                id SERIAL PRIMARY KEY,
                data_type VARCHAR(50) NOT NULL,
                content TEXT,
                expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour')
            )
        """)
        print("📊 Table Created: temp_data (with expiration)")
        
        # Insert various types of temporary data
        temp_data = [
            ("session", "user_session_12345"),
            ("cache", "product_cache_67890"),
            ("log", "error_log_abcdef"),
            ("temp", "temporary_file_xyz"),
            ("session", "user_session_54321"),
            ("cache", "search_cache_98765")
        ]
        
        print("📝 Inserting Temporary Data:")
        for data_type, content in temp_data:
            cursor.execute(
                "INSERT INTO temp_data (data_type, content) VALUES (%s, %s)",
                (data_type, content)
            )
            print(f"   + {data_type}: {content}")
        
        conn.commit()
        
        # Show current data
        cursor.execute("SELECT COUNT(*) FROM temp_data")
        total_data = cursor.fetchone()[0]
        print(f"\n📊 Current Data: {total_data} temporary records")
        
        # Simulate cleanup by data type
        print(f"\n🧹 Cleaning Up by Data Type:")
        
        # Clean up sessions
        cursor.execute("DELETE FROM temp_data WHERE data_type = 'session'")
        sessions_deleted = cursor.rowcount
        print(f"   - Deleted {sessions_deleted} session records")
        
        # Clean up cache
        cursor.execute("DELETE FROM temp_data WHERE data_type = 'cache'")
        cache_deleted = cursor.rowcount
        print(f"   - Deleted {cache_deleted} cache records")
        
        # Clean up expired data (simulate)
        cursor.execute("DELETE FROM temp_data WHERE expires_at < CURRENT_TIMESTAMP")
        expired_deleted = cursor.rowcount
        print(f"   - Deleted {expired_deleted} expired records")
        
        conn.commit()
        
        # Show remaining data
        cursor.execute("SELECT COUNT(*) FROM temp_data")
        remaining_data = cursor.fetchone()[0]
        print(f"\n📊 Remaining Data: {remaining_data} records")
        
        if remaining_data > 0:
            cursor.execute("SELECT data_type, content FROM temp_data")
            remaining = cursor.fetchall()
            print("   Remaining records:")
            for data_type, content in remaining:
                print(f"      {data_type}: {content}")
        
        # Final cleanup
        cursor.execute("DROP TABLE temp_data")
        print(f"\n🧹 Final Cleanup: Dropped temp_data table")
        
        cursor.close()
        conn.close()
        print("✅ Cleanup complete - database is clean!")

def main():
    """Run Lab 3 - Data Management"""
    print("🚀 LAB 3: Data Management - Working Examples")
    print("=" * 60)
    print("✨ Master test data setup, teardown, and isolation patterns!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_setup_teardown()
        demo_data_factories()
        demo_test_isolation()
        demo_data_cleanup()
        
        print("\n✅ Lab 3 completed successfully!")
        print("Key concepts learned:")
        print("• Setup and teardown patterns for clean tests")
        print("• Data factory patterns for generating test data")
        print("• Test isolation - each test gets fresh data")
        print("• Automated data cleanup strategies")
        print("• Professional data management techniques")
        print("\n💪 You're ready for multiple container scenarios!")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()