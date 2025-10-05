#!/usr/bin/env python3
"""
Lab 3: Data Management - Chaos Scenarios
========================================

Experience data management chaos in production environments.
Learn how to handle data corruption, race conditions, and cleanup failures.
"""

import os
import sys
import time
import threading
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

def chaos_data_corruption():
    """Data corruption chaos - what happens when data gets corrupted?"""
    print("\n💥 Data Corruption Chaos...")
    print("🚨 What happens when data gets corrupted during operations?")
    
    try:
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
            
            # Create accounts table
            cursor.execute("""
                CREATE TABLE accounts (
                    id SERIAL PRIMARY KEY,
                    account_number VARCHAR(20) UNIQUE NOT NULL,
                    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                    owner_name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("📊 Table Created: accounts")
            
            # Insert initial accounts
            accounts = [
                ("ACC001", 1000.00, "Alice Johnson"),
                ("ACC002", 2500.00, "Bob Smith"),
                ("ACC003", 500.00, "Carol Davis")
            ]
            
            print("📝 Creating Initial Accounts:")
            for acc_num, balance, owner in accounts:
                cursor.execute(
                    "INSERT INTO accounts (account_number, balance, owner_name) VALUES (%s, %s, %s)",
                    (acc_num, balance, owner)
                )
                print(f"   + {acc_num}: {owner} - ${balance}")
            
            conn.commit()
            
            # Simulate data corruption scenarios
            print(f"\n🧪 Simulating Data Corruption Scenarios:")
            
            # Scenario 1: Invalid data types
            print(f"\n   Scenario 1: Invalid Data Types")
            try:
                cursor.execute("INSERT INTO accounts (account_number, balance, owner_name) VALUES (%s, %s, %s)",
                             ("ACC004", "INVALID_AMOUNT", "David Wilson"))
                print("   ❌ Invalid amount accepted (should have failed!)")
            except Exception as e:
                print(f"   ✅ Invalid amount rejected: {str(e).split('(')[0]}")
                conn.rollback()
            
            # Scenario 2: Duplicate account numbers
            print(f"\n   Scenario 2: Duplicate Account Numbers")
            try:
                cursor.execute("INSERT INTO accounts (account_number, balance, owner_name) VALUES (%s, %s, %s)",
                             ("ACC001", 2000.00, "Eve Wilson"))
                print("   ❌ Duplicate account accepted (should have failed!)")
            except Exception as e:
                print(f"   ✅ Duplicate account rejected: {str(e).split('(')[0]}")
                conn.rollback()
            
            # Scenario 3: Negative balances
            print(f"\n   Scenario 3: Negative Balances")
            try:
                cursor.execute("INSERT INTO accounts (account_number, balance, owner_name) VALUES (%s, %s, %s)",
                             ("ACC005", -100.00, "Frank Miller"))
                print("   ❌ Negative balance accepted (should have failed!)")
            except Exception as e:
                print(f"   ✅ Negative balance rejected: {str(e).split('(')[0]}")
                conn.rollback()
            
            # Scenario 4: Null required fields
            print(f"\n   Scenario 4: Null Required Fields")
            try:
                cursor.execute("INSERT INTO accounts (account_number, balance, owner_name) VALUES (%s, %s, %s)",
                             (None, 1000.00, "Grace Lee"))
                print("   ❌ Null account number accepted (should have failed!)")
            except Exception as e:
                print(f"   ✅ Null account number rejected: {str(e).split('(')[0]}")
                conn.rollback()
            
            # Show current state
            cursor.execute("SELECT account_number, balance, owner_name FROM accounts ORDER BY account_number")
            current_accounts = cursor.fetchall()
            
            print(f"\n📊 Current Account State ({len(current_accounts)} accounts):")
            for acc_num, balance, owner in current_accounts:
                print(f"   {acc_num}: {owner} - ${balance}")
            
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"   💥 Data corruption test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Always validate data and use constraints!")

def chaos_race_conditions():
    """Race condition chaos - concurrent data modifications"""
    print("\n💥 Race Condition Chaos...")
    print("🚨 What happens when multiple processes modify the same data?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            
            # Create inventory table
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE inventory (
                    id SERIAL PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    reserved INTEGER NOT NULL DEFAULT 0,
                    available INTEGER GENERATED ALWAYS AS (quantity - reserved) STORED
                )
            """)
            print("📊 Table Created: inventory")
            
            # Insert initial inventory
            cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)",
                         ("MacBook Pro", 10))
            cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)",
                         ("iPhone", 25))
            cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)",
                         ("iPad", 15))
            conn.commit()
            
            print("📝 Initial Inventory:")
            cursor.execute("SELECT product_name, quantity, reserved, available FROM inventory")
            inventory = cursor.fetchall()
            for product, qty, reserved, available in inventory:
                print(f"   {product}: {qty} total, {reserved} reserved, {available} available")
            
            # Simulate race conditions
            print(f"\n🧪 Simulating Race Conditions:")
            
            results = []
            errors = []
            
            def reserve_product(product_name, amount, worker_id):
                try:
                    # Get fresh connection for each thread
                    worker_conn = psycopg2.connect(
                        host=postgres.get_container_host_ip(),
                        port=postgres.get_exposed_port(5432),
                        user=postgres.username,
                        password=postgres.password,
                        database=postgres.dbname
                    )
                    worker_cursor = worker_conn.cursor()
                    
                    # Start transaction
                    worker_cursor.execute("BEGIN")
                    
                    # Check available quantity
                    worker_cursor.execute("SELECT available FROM inventory WHERE product_name = %s", (product_name,))
                    available = worker_cursor.fetchone()[0]
                    
                    if available >= amount:
                        # Reserve the items
                        worker_cursor.execute(
                            "UPDATE inventory SET reserved = reserved + %s WHERE product_name = %s",
                            (amount, product_name)
                        )
                        worker_conn.commit()
                        results.append(f"Worker {worker_id}: Reserved {amount} {product_name} (was {available} available)")
                    else:
                        worker_conn.rollback()
                        results.append(f"Worker {worker_id}: Failed to reserve {amount} {product_name} (only {available} available)")
                    
                    worker_cursor.close()
                    worker_conn.close()
                    
                except Exception as e:
                    errors.append(f"Worker {worker_id}: {str(e)[:50]}")
            
            # Start multiple threads trying to reserve the same product
            threads = []
            for i in range(5):
                thread = threading.Thread(target=reserve_product, args=("MacBook Pro", 3, i+1))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            print("   📊 Race Condition Results:")
            for result in results:
                print(f"      {result}")
            
            if errors:
                print("   ❌ Errors:")
                for error in errors:
                    print(f"      {error}")
            
            # Show final inventory state
            cursor.execute("SELECT product_name, quantity, reserved, available FROM inventory")
            final_inventory = cursor.fetchall()
            
            print(f"\n📊 Final Inventory State:")
            for product, qty, reserved, available in final_inventory:
                print(f"   {product}: {qty} total, {reserved} reserved, {available} available")
            
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"   💥 Race condition test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Use proper locking and transactions for concurrent access!")

def chaos_cleanup_failures():
    """Cleanup failure chaos - what happens when cleanup fails?"""
    print("\n💥 Cleanup Failure Chaos...")
    print("🚨 What happens when data cleanup fails or is incomplete?")
    
    try:
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
                CREATE TABLE temp_sessions (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100) UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour')
                )
            """)
            print("📊 Table Created: temp_sessions")
            
            # Insert test sessions
            sessions = [
                ("sess_001", 1001, "user_data_1"),
                ("sess_002", 1002, "user_data_2"),
                ("sess_003", 1003, "user_data_3"),
                ("sess_004", 1004, "user_data_4"),
                ("sess_005", 1005, "user_data_5")
            ]
            
            print("📝 Creating Test Sessions:")
            for session_id, user_id, data in sessions:
                cursor.execute(
                    "INSERT INTO temp_sessions (session_id, user_id, data) VALUES (%s, %s, %s)",
                    (session_id, user_id, data)
                )
                print(f"   + {session_id}: User {user_id}")
            
            conn.commit()
            
            # Simulate cleanup failures
            print(f"\n🧪 Simulating Cleanup Failures:")
            
            # Scenario 1: Partial cleanup failure
            print(f"\n   Scenario 1: Partial Cleanup Failure")
            try:
                # Try to delete some sessions
                cursor.execute("DELETE FROM temp_sessions WHERE user_id IN (1001, 1002)")
                deleted_count = cursor.rowcount
                print(f"   ✅ Deleted {deleted_count} sessions")
                
                # Simulate failure for remaining cleanup
                cursor.execute("DELETE FROM temp_sessions WHERE user_id = 9999")  # Non-existent user
                print(f"   ❌ Cleanup failed for remaining sessions")
                
            except Exception as e:
                print(f"   💥 Cleanup error: {str(e)[:50]}")
                conn.rollback()
            
            # Show remaining data
            cursor.execute("SELECT COUNT(*) FROM temp_sessions")
            remaining_sessions = cursor.fetchone()[0]
            print(f"   📊 Remaining sessions: {remaining_sessions}")
            
            if remaining_sessions > 0:
                cursor.execute("SELECT session_id, user_id FROM temp_sessions")
                remaining = cursor.fetchall()
                print("   Remaining sessions:")
                for session_id, user_id in remaining:
                    print(f"      {session_id}: User {user_id}")
            
            # Scenario 2: Orphaned data
            print(f"\n   Scenario 2: Orphaned Data")
            cursor.execute("""
                CREATE TABLE user_profiles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    profile_data TEXT
                )
            """)
            
            cursor.execute("INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)",
                         (1001, "profile_data_1"))
            cursor.execute("INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)",
                         (1002, "profile_data_2"))
            conn.commit()
            
            print("   📊 Created user_profiles table with 2 profiles")
            
            # Simulate user deletion without cleaning up profiles
            cursor.execute("DELETE FROM temp_sessions WHERE user_id = 1001")
            print("   ❌ Deleted user session but left profile data")
            
            # Check for orphaned data
            cursor.execute("""
                SELECT p.user_id, p.profile_data 
                FROM user_profiles p 
                LEFT JOIN temp_sessions s ON p.user_id = s.user_id 
                WHERE s.user_id IS NULL
            """)
            orphaned = cursor.fetchall()
            
            print(f"   📊 Found {len(orphaned)} orphaned profiles:")
            for user_id, profile_data in orphaned:
                print(f"      User {user_id}: {profile_data}")
            
            # Scenario 3: Cleanup timeout
            print(f"\n   Scenario 3: Cleanup Timeout")
            cursor.execute("SELECT COUNT(*) FROM temp_sessions")
            sessions_before = cursor.fetchone()[0]
            
            print(f"   📊 Sessions before cleanup: {sessions_before}")
            
            # Simulate slow cleanup operation
            start_time = time.time()
            try:
                cursor.execute("DELETE FROM temp_sessions WHERE created_at < CURRENT_TIMESTAMP")
                conn.commit()
                end_time = time.time()
                print(f"   ✅ Cleanup completed in {end_time - start_time:.3f}s")
            except Exception as e:
                end_time = time.time()
                print(f"   ❌ Cleanup failed after {end_time - start_time:.3f}s: {str(e)[:50]}")
                conn.rollback()
            
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"   💥 Cleanup failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement robust cleanup strategies and monitor for orphaned data!")

def chaos_data_consistency():
    """Data consistency chaos - what happens when data becomes inconsistent?"""
    print("\n💥 Data Consistency Chaos...")
    print("🚨 What happens when data becomes inconsistent across operations?")
    
    try:
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
            
            # Create related tables
            cursor.execute("""
                CREATE TABLE customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER REFERENCES customers(id),
                    total_amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE order_items (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER REFERENCES orders(id),
                    product_name VARCHAR(100) NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL
                )
            """)
            
            print("📊 Tables Created: customers, orders, order_items")
            
            # Insert test data
            cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)",
                         ("Alice Johnson", "alice@example.com"))
            cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)",
                         ("Bob Smith", "bob@example.com"))
            conn.commit()
            
            print("📝 Created 2 customers")
            
            # Simulate inconsistent data scenarios
            print(f"\n🧪 Simulating Data Consistency Issues:")
            
            # Scenario 1: Orphaned orders
            print(f"\n   Scenario 1: Orphaned Orders")
            cursor.execute("INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
                         (1, 299.99))  # Valid customer
            cursor.execute("INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
                         (999, 149.99))  # Invalid customer (orphaned)
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM orders")
            total_orders = cursor.fetchone()[0]
            print(f"   📊 Total orders: {total_orders}")
            
            cursor.execute("""
                SELECT o.id, o.customer_id, c.name, o.total_amount
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                ORDER BY o.id
            """)
            order_details = cursor.fetchall()
            
            print("   Order details:")
            for order_id, customer_id, customer_name, amount in order_details:
                if customer_name:
                    print(f"      Order {order_id}: {customer_name} - ${amount}")
                else:
                    print(f"      Order {order_id}: ORPHANED (Customer {customer_id} not found) - ${amount}")
            
            # Scenario 2: Inconsistent order totals
            print(f"\n   Scenario 2: Inconsistent Order Totals")
            cursor.execute("INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                         (1, "Laptop", 1, 999.99))
            cursor.execute("INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                         (1, "Mouse", 1, 29.99))
            conn.commit()
            
            # Calculate actual total from items
            cursor.execute("SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = 1")
            actual_total = cursor.fetchone()[0]
            
            cursor.execute("SELECT total_amount FROM orders WHERE id = 1")
            stored_total = cursor.fetchone()[0]
            
            print(f"   📊 Order 1 totals:")
            print(f"      Stored total: ${stored_total}")
            print(f"      Calculated total: ${actual_total}")
            print(f"      Consistent: {'✅' if stored_total == actual_total else '❌'}")
            
            # Scenario 3: Data integrity violations
            print(f"\n   Scenario 3: Data Integrity Violations")
            try:
                cursor.execute("INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                             (999, "Invalid Product", 1, 99.99))  # Invalid order_id
                print("   ❌ Invalid order item accepted (should have failed!)")
            except Exception as e:
                print(f"   ✅ Invalid order item rejected: {str(e).split('(')[0]}")
                conn.rollback()
            
            # Show final data state
            print(f"\n📊 Final Data State:")
            cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM orders")
            order_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM order_items")
            item_count = cursor.fetchone()[0]
            
            print(f"   Customers: {customer_count}")
            print(f"   Orders: {order_count}")
            print(f"   Order Items: {item_count}")
            
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"   💥 Data consistency test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Use foreign keys, constraints, and regular data validation!")

def main():
    """Run Data Management Chaos Scenarios"""
    print("💥 LAB 3: DATA MANAGEMENT CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world data management resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_data_corruption()
        chaos_race_conditions()
        chaos_cleanup_failures()
        chaos_data_consistency()
        
        print("\n🎉 DATA MANAGEMENT CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Data corruption happens - use constraints and validation")
        print("• Race conditions occur - use proper locking and transactions")
        print("• Cleanup can fail - implement robust cleanup strategies")
        print("• Data consistency matters - use foreign keys and regular validation")
        print("• Real-world data management is complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for data management production chaos!")
        
    except Exception as e:
        print(f"❌ Data management chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
