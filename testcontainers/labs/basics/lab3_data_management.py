#!/usr/bin/env python3
"""
Lab 3: Data Management
======================

Master test data setup, teardown, and isolation patterns.
"""

import os

# Configure TestContainers to use local Docker
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    import psycopg2
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg2-binary")
    exit(1)

def demo_setup_teardown():
    """Setup and teardown patterns"""
    print("🔄 Setup & Teardown Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print("✅ Container started")
        
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Setup phase
        cursor.execute("""
            CREATE TABLE test_data (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                value TEXT
            )
        """)
        
        test_data = [
            ("Test 1", "Value 1"),
            ("Test 2", "Value 2"),
            ("Test 3", "Value 3")
        ]
        
        for name, value in test_data:
            cursor.execute("INSERT INTO test_data (name, value) VALUES (%s, %s)", (name, value))
        
        conn.commit()
        
        # Verify setup
        cursor.execute("SELECT COUNT(*) FROM test_data")
        count = cursor.fetchone()[0]
        print(f"📊 Setup: {count} records created")
        
        # Test operations
        cursor.execute("SELECT name, value FROM test_data ORDER BY id")
        records = cursor.fetchall()
        print("📋 Data:")
        for name, value in records:
            print(f"   • {name}: {value}")
        
        cursor.close()
        conn.close()
        
        print("✅ Test operations complete")
    
    print("🧹 Automatic teardown complete")

def demo_test_isolation():
    """Test isolation demonstration"""
    print("\n🔒 Test Isolation Demo")
    
    # Test 1: Create data
    print("🧪 Test 1: Creating data")
    with PostgresContainer("postgres:15-alpine") as postgres1:
        conn = psycopg2.connect(
            host=postgres1.get_container_host_ip(),
            port=postgres1.get_exposed_port(5432),
            user=postgres1.username,
            password=postgres1.password,
            database=postgres1.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100))")
        cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob')")
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"   📊 Created {count} users")
        
        cursor.close()
        conn.close()
    
    # Test 2: Fresh container
    print("🧪 Test 2: Fresh container")
    with PostgresContainer("postgres:15-alpine") as postgres2:
        conn = psycopg2.connect(
            host=postgres2.get_container_host_ip(),
            port=postgres2.get_exposed_port(5432),
            user=postgres2.username,
            password=postgres2.password,
            database=postgres2.dbname
        )
        
        cursor = conn.cursor()
        
        # Try to access data from Test 1
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"   ❌ Unexpected: Found {count} users from previous test!")
        except psycopg2.errors.UndefinedTable:
            print("   ✅ Perfect isolation: No data from previous test")
            conn.rollback()  # Rollback the failed transaction
        
        # Create fresh data
        cursor.execute("CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(100))")
        cursor.execute("INSERT INTO products (name) VALUES ('Laptop'), ('Mouse')")
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        print(f"   📊 Created {count} products (independent)")
        
        cursor.close()
        conn.close()
    
    print("✅ Each container is completely independent")

def demo_data_seeding():
    """Data seeding strategies"""
    print("\n🌱 Data Seeding Demo")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Strategy 1: Direct SQL
        print("📝 Strategy 1: Direct SQL seeding")
        cursor.execute("""
            CREATE TABLE employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(50),
                salary DECIMAL(10,2)
            )
        """)
        
        cursor.execute("""
            INSERT INTO employees (name, department, salary) VALUES
            ('Alice Johnson', 'Engineering', 75000.00),
            ('Bob Smith', 'Marketing', 65000.00),
            ('Carol Davis', 'Engineering', 80000.00),
            ('David Wilson', 'Sales', 70000.00)
        """)
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        print(f"   ✅ Seeded {count} employees")
        
        # Strategy 2: Python factory
        print("🏭 Strategy 2: Python data factory")
        
        def create_employee(name, dept, salary):
            cursor.execute(
                "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
                (name, dept, salary)
            )
        
        test_employees = [
            ("Eve Brown", "HR", 60000.00),
            ("Frank Miller", "Engineering", 85000.00),
        ]
        
        for name, dept, salary in test_employees:
            create_employee(name, dept, salary)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        total = cursor.fetchone()[0]
        print(f"   ✅ Total: {total} employees")
        
        # Show results
        cursor.execute("SELECT department, COUNT(*), AVG(salary) FROM employees GROUP BY department")
        stats = cursor.fetchall()
        print("📊 Department stats:")
        for dept, count, avg_salary in stats:
            print(f"   {dept}: {count} employees, avg ${avg_salary:,.0f}")
        
        cursor.close()
        conn.close()

def demo_fixtures():
    """Test fixtures pattern"""
    print("\n🧪 Test Fixtures Demo")
    
    def create_test_database():
        """Fixture: Create test database with sample data"""
        postgres = PostgresContainer("postgres:15-alpine")
        postgres.start()
        
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                status VARCHAR(20) DEFAULT 'active'
            )
        """)
        
        # Insert test data
        customers = [
            ("John Doe", "john@example.com"),
            ("Jane Smith", "jane@example.com"),
            ("Bob Johnson", "bob@example.com")
        ]
        
        for name, email in customers:
            cursor.execute(
                "INSERT INTO customers (name, email) VALUES (%s, %s)",
                (name, email)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return postgres
    
    # Use fixture
    postgres = create_test_database()
    
    try:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]
        print(f"✅ Fixture created {count} test customers")
        
        cursor.close()
        conn.close()
        
    finally:
        postgres.stop()

def main():
    """Run Lab 3"""
    print("🧹 LAB 3: Data Management")
    print("=" * 40)
    
    try:
        demo_setup_teardown()
        demo_test_isolation()
        demo_data_seeding()
        demo_fixtures()
        
        print("\n✅ Lab 3 completed!")
        print("Key concepts learned:")
        print("• Setup and teardown patterns")
        print("• Test isolation with fresh containers")
        print("• Data seeding strategies")
        print("• Test fixtures for reusable setup")
        print("• Automatic cleanup prevents pollution")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("Ensure Docker is running and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()