#!/usr/bin/env python3
"""
Lab 5: Multi-Database Testing - Chaos Scenarios
===============================================

Experience multi-database chaos in production environments.
Learn how to handle database failures, synchronization issues, and distributed transaction problems.
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
        'psycopg2': 'psycopg2-binary',
        'pymysql': 'pymysql',
        'redis': 'redis',
        'pymongo': 'pymongo'
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
    from testcontainers.mongodb import MongoDbContainer
    import psycopg2
    import pymysql
    import redis
    import pymongo
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary pymysql redis pymongo")
    sys.exit(1)

def chaos_database_failures():
    """Database failure chaos - what happens when databases fail?"""
    print("\n💥 Database Failure Chaos...")
    print("🚨 What happens when one database fails in a multi-database system?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             MySqlContainer("mysql:8.0") as mysql, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup distributed system
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

            pg_cursor = pg_conn.cursor()
            mysql_cursor = mysql_conn.cursor()

            # Create tables
            pg_cursor.execute("""
                CREATE TABLE critical_orders (
                    id SERIAL PRIMARY KEY,
                    order_id VARCHAR(100) UNIQUE NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)

            mysql_cursor.execute("""
                CREATE TABLE user_accounts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT UNIQUE NOT NULL,
                    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
                )
            """)
            print("📊 Tables Created: critical_orders (PostgreSQL), user_accounts (MySQL)")

            # Insert test data
            pg_cursor.execute("INSERT INTO critical_orders (order_id, amount) VALUES (%s, %s)", ("ORD001", 1000.00))
            pg_cursor.execute("INSERT INTO critical_orders (order_id, amount) VALUES (%s, %s)", ("ORD002", 2500.00))
            pg_conn.commit()

            mysql_cursor.execute("INSERT INTO user_accounts (user_id, balance) VALUES (%s, %s)", (1001, 5000.00))
            mysql_cursor.execute("INSERT INTO user_accounts (user_id, balance) VALUES (%s, %s)", (1002, 3000.00))
            mysql_conn.commit()

            print("📝 Test Data Created: 2 orders, 2 user accounts")

            # Simulate database failures
            print(f"\n🧪 Simulating Database Failures:")

            # Scenario 1: PostgreSQL failure during order processing
            print(f"\n   Scenario 1: PostgreSQL Failure")
            try:
                # Simulate order processing
                pg_cursor.execute("SELECT order_id, amount FROM critical_orders WHERE status = 'pending'")
                pending_orders = pg_cursor.fetchall()
                
                print(f"      📦 Processing {len(pending_orders)} pending orders...")
                
                for order_id, amount in pending_orders:
                    # Simulate random failure
                    import random
                    if random.random() < 0.4:  # 40% failure rate
                        raise Exception("PostgreSQL connection lost - database unavailable")
                    
                    # Process order
                    pg_cursor.execute("UPDATE critical_orders SET status = 'processed' WHERE order_id = %s", (order_id,))
                    print(f"         ✅ {order_id}: ${amount} - Processed")
                
                pg_conn.commit()
                print(f"      ✅ All orders processed successfully")
                
            except Exception as e:
                print(f"      ❌ Order processing failed: {str(e)[:50]}")
                pg_conn.rollback()
                print(f"      🔄 Orders remain in pending state")

            # Scenario 2: MySQL failure during account updates
            print(f"\n   Scenario 2: MySQL Failure")
            try:
                # Simulate account updates
                mysql_cursor.execute("SELECT user_id, balance FROM user_accounts")
                accounts = mysql_cursor.fetchall()
                
                print(f"      👥 Updating {len(accounts)} user accounts...")
                
                for user_id, balance in accounts:
                    # Simulate random failure
                    if random.random() < 0.3:  # 30% failure rate
                        raise Exception("MySQL connection timeout - database unreachable")
                    
                    # Update account
                    new_balance = balance + 100.00  # Simulate deposit
                    mysql_cursor.execute("UPDATE user_accounts SET balance = %s WHERE user_id = %s", (new_balance, user_id))
                    print(f"         ✅ User {user_id}: ${balance} -> ${new_balance}")
                
                mysql_conn.commit()
                print(f"      ✅ All accounts updated successfully")
                
            except Exception as e:
                print(f"      ❌ Account update failed: {str(e)[:50]}")
                mysql_conn.rollback()
                print(f"      🔄 Accounts remain in original state")

            # Scenario 3: Redis failure during caching
            print(f"\n   Scenario 3: Redis Failure")
            try:
                # Simulate cache operations
                cache_operations = [
                    ("user:1001", "Alice Johnson"),
                    ("user:1002", "Bob Smith"),
                    ("order:ORD001", "Processed"),
                    ("order:ORD002", "Pending")
                ]
                
                print(f"      💾 Caching {len(cache_operations)} items...")
                
                for key, value in cache_operations:
                    # Simulate random failure
                    if random.random() < 0.2:  # 20% failure rate
                        raise Exception("Redis connection lost - cache unavailable")
                    
                    r.setex(key, 300, value)  # 5 minutes TTL
                    print(f"         ✅ {key}: {value} (TTL: 300s)")
                
                print(f"      ✅ All items cached successfully")
                
            except Exception as e:
                print(f"      ❌ Caching failed: {str(e)[:50]}")
                print(f"      🔄 Cache operations skipped")

            # Show final system state
            print(f"\n📊 Final System State:")

            # PostgreSQL state
            pg_cursor.execute("SELECT COUNT(*) FROM critical_orders WHERE status = 'processed'")
            processed_orders = pg_cursor.fetchone()[0]
            pg_cursor.execute("SELECT COUNT(*) FROM critical_orders")
            total_orders = pg_cursor.fetchone()[0]
            print(f"   📦 Orders (PostgreSQL): {processed_orders}/{total_orders} processed")

            # MySQL state
            mysql_cursor.execute("SELECT AVG(balance) FROM user_accounts")
            avg_balance = mysql_cursor.fetchone()[0]
            print(f"   👥 Accounts (MySQL): Average balance ${avg_balance:.2f}")

            # Redis state
            cache_keys = r.dbsize()
            print(f"   💾 Cache (Redis): {cache_keys} keys")

            pg_cursor.close()
            pg_conn.close()
            mysql_cursor.close()
            mysql_conn.close()

    except Exception as e:
        print(f"   💥 Database failure test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement database failover and circuit breakers!")

def chaos_synchronization_issues():
    """Synchronization chaos - what happens when data gets out of sync?"""
    print("\n💥 Synchronization Chaos...")
    print("🚨 What happens when databases get out of sync?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             MySqlContainer("mysql:8.0") as mysql, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup synchronized tables
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

            pg_cursor = pg_conn.cursor()
            mysql_cursor = mysql_conn.cursor()

            # Create synchronized tables
            pg_cursor.execute("""
                CREATE TABLE products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            mysql_cursor.execute("""
                CREATE TABLE products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    stock INT NOT NULL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("📊 Synchronized Tables Created: products (PostgreSQL & MySQL)")

            # Initial synchronized data
            products = [
                ("MacBook Pro", 2499.99, 10),
                ("iPhone", 999.99, 25),
                ("iPad", 599.99, 15)
            ]

            print("📝 Creating Initial Synchronized Data:")
            for i, (name, price, stock) in enumerate(products, 1):
                # Insert into PostgreSQL
                pg_cursor.execute(
                    "INSERT INTO products (id, name, price, stock) VALUES (%s, %s, %s, %s)",
                    (i, name, price, stock)
                )
                
                # Insert into MySQL
                mysql_cursor.execute(
                    "INSERT INTO products (id, name, price, stock) VALUES (%s, %s, %s, %s)",
                    (i, name, price, stock)
                )
                
                print(f"   + {name}: ${price} (Stock: {stock})")

            pg_conn.commit()
            mysql_conn.commit()

            # Simulate synchronization issues
            print(f"\n🧪 Simulating Synchronization Issues:")

            # Scenario 1: Partial synchronization failure
            print(f"\n   Scenario 1: Partial Synchronization Failure")
            
            # Update PostgreSQL only
            pg_cursor.execute("UPDATE products SET price = 2299.99 WHERE name = 'MacBook Pro'")
            pg_conn.commit()
            print(f"      📝 PostgreSQL: MacBook Pro price updated to $2299.99")
            
            # Simulate sync failure for this update
            print(f"      ❌ Sync failed: MySQL not updated")
            
            # Update MySQL only
            mysql_cursor.execute("UPDATE products SET stock = 5 WHERE name = 'iPhone'")
            mysql_conn.commit()
            print(f"      📝 MySQL: iPhone stock updated to 5")
            
            # Simulate sync failure for this update
            print(f"      ❌ Sync failed: PostgreSQL not updated")

            # Scenario 2: Conflicting updates
            print(f"\n   Scenario 2: Conflicting Updates")
            
            # Update same product in both databases with different values
            pg_cursor.execute("UPDATE products SET stock = 8 WHERE name = 'iPad'")
            pg_conn.commit()
            print(f"      📝 PostgreSQL: iPad stock = 8")
            
            mysql_cursor.execute("UPDATE products SET stock = 12 WHERE name = 'iPad'")
            mysql_conn.commit()
            print(f"      📝 MySQL: iPad stock = 12")
            
            print(f"      ⚠️  Conflict detected: iPad has different stock values!")

            # Scenario 3: Data corruption during sync
            print(f"\n   Scenario 3: Data Corruption During Sync")
            
            # Simulate corrupted data
            pg_cursor.execute("UPDATE products SET name = 'MacBook Pro (Corrupted)' WHERE name = 'MacBook Pro'")
            pg_conn.commit()
            print(f"      📝 PostgreSQL: MacBook Pro name corrupted")
            
            # Simulate sync of corrupted data
            mysql_cursor.execute("UPDATE products SET name = 'MacBook Pro (Corrupted)' WHERE name = 'MacBook Pro'")
            mysql_conn.commit()
            print(f"      📝 MySQL: Corrupted data synced")

            # Check synchronization status
            print(f"\n🔍 Synchronization Status Check:")

            # Compare data between databases
            pg_cursor.execute("SELECT name, price, stock FROM products ORDER BY id")
            pg_products = pg_cursor.fetchall()
            
            mysql_cursor.execute("SELECT name, price, stock FROM products ORDER BY id")
            mysql_products = mysql_cursor.fetchall()

            print(f"   📊 Data Comparison:")
            for i, (pg_row, mysql_row) in enumerate(zip(pg_products, mysql_products)):
                print(f"      Product {i+1}:")
                print(f"         PostgreSQL: {pg_row[0]} - ${pg_row[1]} (Stock: {pg_row[2]})")
                print(f"         MySQL: {mysql_row[0]} - ${mysql_row[1]} (Stock: {mysql_row[2]})")
                print(f"         Sync Status: {'✅' if pg_row == mysql_row else '❌'}")

            # Store sync issues in Redis
            sync_issues = [
                "MacBook Pro price mismatch",
                "iPhone stock mismatch", 
                "iPad stock conflict",
                "MacBook Pro name corruption"
            ]

            print(f"\n📝 Storing Sync Issues in Redis:")
            for i, issue in enumerate(sync_issues):
                r.setex(f"sync_issue:{i}", 3600, issue)  # 1 hour TTL
                print(f"   + {issue}")

            # Show sync issue summary
            print(f"\n📊 Sync Issue Summary:")
            print(f"   Total issues: {len(sync_issues)}")
            print(f"   Stored in Redis: {r.dbsize()} keys")

            pg_cursor.close()
            pg_conn.close()
            mysql_cursor.close()
            mysql_conn.close()

    except Exception as e:
        print(f"   💥 Synchronization test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement conflict resolution and data validation!")

def chaos_distributed_transaction_failures():
    """Distributed transaction failure chaos"""
    print("\n💥 Distributed Transaction Failure Chaos...")
    print("🚨 What happens when distributed transactions fail?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             MySqlContainer("mysql:8.0") as mysql, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup distributed transaction system
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

            pg_cursor = pg_conn.cursor()
            mysql_cursor = mysql_conn.cursor()

            # Create transaction tables
            pg_cursor.execute("""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    order_id VARCHAR(100) UNIQUE NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)

            mysql_cursor.execute("""
                CREATE TABLE payments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id VARCHAR(100) NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            print("📊 Transaction Tables Created: orders (PostgreSQL), payments (MySQL)")

            # Simulate distributed transaction failures
            print(f"\n🧪 Simulating Distributed Transaction Failures:")

            # Scenario 1: Two-phase commit failure
            print(f"\n   Scenario 1: Two-Phase Commit Failure")
            
            transaction_id = "txn_001"
            order_id = "ORD001"
            amount = 1000.00

            print(f"   🔄 Transaction {transaction_id}: Order {order_id} - ${amount}")

            # Phase 1: Prepare
            print(f"   📋 Phase 1: Prepare")
            
            # Prepare PostgreSQL (orders)
            try:
                pg_cursor.execute("INSERT INTO orders (order_id, amount) VALUES (%s, %s)", (order_id, amount))
                print(f"      ✅ PostgreSQL: Order prepared")
            except Exception as e:
                print(f"      ❌ PostgreSQL: Prepare failed - {str(e)[:30]}")
                raise

            # Prepare MySQL (payments)
            try:
                mysql_cursor.execute("INSERT INTO payments (order_id, amount) VALUES (%s, %s)", (order_id, amount))
                print(f"      ✅ MySQL: Payment prepared")
            except Exception as e:
                print(f"      ❌ MySQL: Prepare failed - {str(e)[:30]}")
                # Rollback PostgreSQL
                pg_conn.rollback()
                print(f"      🔄 PostgreSQL: Rolled back")
                raise

            # Phase 2: Commit (simulate failure)
            print(f"   📋 Phase 2: Commit")
            
            # Simulate random commit failure
            import random
            if random.random() < 0.5:  # 50% failure rate
                print(f"      ❌ Commit failed: Network timeout")
                
                # Rollback both databases
                pg_conn.rollback()
                mysql_conn.rollback()
                print(f"      🔄 Both databases rolled back")
                
                # Store failed transaction
                r.hset(f"failed_txn:{transaction_id}", mapping={
                    "order_id": order_id,
                    "amount": str(amount),
                    "reason": "commit_timeout",
                    "timestamp": str(int(time.time()))
                })
                
                print(f"   ❌ Transaction {transaction_id}: FAILED")
            else:
                # Commit both databases
                pg_conn.commit()
                mysql_conn.commit()
                print(f"      ✅ Both databases committed")
                print(f"   ✅ Transaction {transaction_id}: SUCCESS")

            # Scenario 2: Partial commit failure
            print(f"\n   Scenario 2: Partial Commit Failure")
            
            transaction_id = "txn_002"
            order_id = "ORD002"
            amount = 2500.00

            print(f"   🔄 Transaction {transaction_id}: Order {order_id} - ${amount}")

            # Prepare both databases
            pg_cursor.execute("INSERT INTO orders (order_id, amount) VALUES (%s, %s)", (order_id, amount))
            mysql_cursor.execute("INSERT INTO payments (order_id, amount) VALUES (%s, %s)", (order_id, amount))
            print(f"   📋 Phase 1: Both databases prepared")

            # Commit PostgreSQL successfully
            pg_conn.commit()
            print(f"   ✅ PostgreSQL: Committed")

            # Simulate MySQL commit failure
            try:
                mysql_conn.commit()
                print(f"   ✅ MySQL: Committed")
                print(f"   ✅ Transaction {transaction_id}: SUCCESS")
            except Exception as e:
                print(f"   ❌ MySQL: Commit failed - {str(e)[:30]}")
                print(f"   ⚠️  Partial commit detected: PostgreSQL committed, MySQL failed")
                
                # Store partial commit
                r.hset(f"partial_txn:{transaction_id}", mapping={
                    "order_id": order_id,
                    "amount": str(amount),
                    "postgresql": "committed",
                    "mysql": "failed",
                    "timestamp": str(int(time.time()))
                })
                
                print(f"   ❌ Transaction {transaction_id}: PARTIAL COMMIT")

            # Show transaction state
            print(f"\n📊 Transaction State:")

            # Orders in PostgreSQL
            pg_cursor.execute("SELECT COUNT(*) FROM orders")
            order_count = pg_cursor.fetchone()[0]
            print(f"   📦 Orders (PostgreSQL): {order_count}")

            # Payments in MySQL
            mysql_cursor.execute("SELECT COUNT(*) FROM payments")
            payment_count = mysql_cursor.fetchone()[0]
            print(f"   💳 Payments (MySQL): {payment_count}")

            # Failed transactions in Redis
            failed_txns = r.keys("failed_txn:*")
            partial_txns = r.keys("partial_txn:*")
            print(f"   ❌ Failed Transactions: {len(failed_txns)}")
            print(f"   ⚠️  Partial Transactions: {len(partial_txns)}")

            pg_cursor.close()
            pg_conn.close()
            mysql_cursor.close()
            mysql_conn.close()

    except Exception as e:
        print(f"   💥 Distributed transaction test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement proper distributed transaction patterns and recovery!")

def chaos_data_consistency_issues():
    """Data consistency chaos - what happens when data becomes inconsistent?"""
    print("\n💥 Data Consistency Chaos...")
    print("🚨 What happens when data becomes inconsistent across databases?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres, \
             MySqlContainer("mysql:8.0") as mysql, \
             RedisContainer("redis:7-alpine") as redis_container:

            print(f"✅ PostgreSQL Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
            print(f"✅ MySQL Ready: {mysql.get_container_host_ip()}:{mysql.get_exposed_port(3306)}")
            print(f"✅ Redis Ready: {redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(6379)}")

            # Setup related tables
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

            pg_cursor = pg_conn.cursor()
            mysql_cursor = mysql_conn.cursor()

            # Create related tables
            pg_cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)

            mysql_cursor.execute("""
                CREATE TABLE user_profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20)
                )
            """)
            print("📊 Related Tables Created: users (PostgreSQL), user_profiles (MySQL)")

            # Insert test data
            users = [
                (1, "alice_j", "alice@example.com"),
                (2, "bob_s", "bob@example.com"),
                (3, "carol_d", "carol@example.com")
            ]

            profiles = [
                (1, "Alice Johnson", "555-0101"),
                (2, "Bob Smith", "555-0102"),
                (3, "Carol Davis", "555-0103")
            ]

            print("📝 Creating Test Data:")
            for user_id, username, email in users:
                pg_cursor.execute(
                    "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)",
                    (user_id, username, email)
                )
                print(f"   + User {user_id}: {username} ({email})")

            for user_id, full_name, phone in profiles:
                mysql_cursor.execute(
                    "INSERT INTO user_profiles (user_id, full_name, phone) VALUES (%s, %s, %s)",
                    (user_id, full_name, phone)
                )
                print(f"   + Profile {user_id}: {full_name} ({phone})")

            pg_conn.commit()
            mysql_conn.commit()

            # Simulate data consistency issues
            print(f"\n🧪 Simulating Data Consistency Issues:")

            # Scenario 1: Orphaned records
            print(f"\n   Scenario 1: Orphaned Records")
            
            # Delete user from PostgreSQL but not from MySQL
            pg_cursor.execute("DELETE FROM users WHERE id = 3")
            pg_conn.commit()
            print(f"      📝 PostgreSQL: User 3 deleted")
            print(f"      📝 MySQL: User 3 profile still exists")
            print(f"      ⚠️  Orphaned record detected: Profile exists without user")

            # Scenario 2: Data type mismatches
            print(f"\n   Scenario 2: Data Type Mismatches")
            
            # Insert invalid data
            try:
                pg_cursor.execute("INSERT INTO users (id, username, email) VALUES (%s, %s, %s)", (4, "dave_w", "invalid-email"))
                pg_conn.commit()
                print(f"      📝 PostgreSQL: User 4 with invalid email inserted")
            except Exception as e:
                print(f"      ❌ PostgreSQL: Invalid email rejected - {str(e)[:30]}")
                pg_conn.rollback()

            # Scenario 3: Constraint violations
            print(f"\n   Scenario 3: Constraint Violations")
            
            # Try to insert duplicate username
            try:
                pg_cursor.execute("INSERT INTO users (id, username, email) VALUES (%s, %s, %s)", (5, "alice_j", "alice2@example.com"))
                pg_conn.commit()
                print(f"      📝 PostgreSQL: Duplicate username inserted")
            except Exception as e:
                print(f"      ❌ PostgreSQL: Duplicate username rejected - {str(e)[:30]}")
                pg_conn.rollback()

            # Scenario 4: Referential integrity issues
            print(f"\n   Scenario 4: Referential Integrity Issues")
            
            # Try to insert profile for non-existent user
            try:
                mysql_cursor.execute("INSERT INTO user_profiles (user_id, full_name, phone) VALUES (%s, %s, %s)", (999, "Ghost User", "555-9999"))
                mysql_conn.commit()
                print(f"      📝 MySQL: Profile for non-existent user inserted")
                print(f"      ⚠️  Referential integrity violation: Profile references non-existent user")
            except Exception as e:
                print(f"      ❌ MySQL: Referential integrity violation - {str(e)[:30]}")
                mysql_conn.rollback()

            # Check data consistency
            print(f"\n🔍 Data Consistency Check:")

            # Check for orphaned records
            mysql_cursor.execute("""
                SELECT p.user_id, p.full_name 
                FROM user_profiles p 
                LEFT JOIN (SELECT 1 as id UNION SELECT 2 as id) u ON p.user_id = u.id
                WHERE u.id IS NULL
            """)
            orphaned_profiles = mysql_cursor.fetchall()

            print(f"   📊 Orphaned Records: {len(orphaned_profiles)}")
            for user_id, full_name in orphaned_profiles:
                print(f"      Profile {user_id}: {full_name} (user deleted)")

            # Check data counts
            pg_cursor.execute("SELECT COUNT(*) FROM users")
            user_count = pg_cursor.fetchone()[0]
            mysql_cursor.execute("SELECT COUNT(*) FROM user_profiles")
            profile_count = mysql_cursor.fetchone()[0]

            print(f"   📊 Data Counts:")
            print(f"      Users (PostgreSQL): {user_count}")
            print(f"      Profiles (MySQL): {profile_count}")
            print(f"      Consistent: {'✅' if user_count == profile_count else '❌'}")

            # Store consistency issues in Redis
            consistency_issues = [
                "Orphaned profile for user 3",
                "Data type mismatch in email field",
                "Duplicate username constraint violation",
                "Referential integrity violation"
            ]

            print(f"\n📝 Storing Consistency Issues in Redis:")
            for i, issue in enumerate(consistency_issues):
                r.setex(f"consistency_issue:{i}", 3600, issue)  # 1 hour TTL
                print(f"   + {issue}")

            pg_cursor.close()
            pg_conn.close()
            mysql_cursor.close()
            mysql_conn.close()

    except Exception as e:
        print(f"   💥 Data consistency test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Implement data validation and referential integrity checks!")

def main():
    """Run Multi-Database Chaos Scenarios"""
    print("💥 LAB 5: MULTI-DATABASE CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world multi-database resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_database_failures()
        chaos_synchronization_issues()
        chaos_distributed_transaction_failures()
        chaos_data_consistency_issues()
        
        print("\n🎉 MULTI-DATABASE CHAOS COMPLETED!")
        print("Key lessons learned:")
        print("• Database failures happen - implement failover and circuit breakers")
        print("• Synchronization issues occur - implement conflict resolution")
        print("• Distributed transactions can fail - implement proper patterns")
        print("• Data consistency matters - implement validation and integrity checks")
        print("• Real-world multi-database systems are complex - TestContainers helps you prepare!")
        print("\n💪 You're now ready for multi-database production chaos!")
        
    except Exception as e:
        print(f"❌ Multi-database chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
