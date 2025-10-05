#!/usr/bin/env python3
"""
Lab 1: PostgreSQL Chaos - Real-World Failures
=============================================

Experience PostgreSQL chaos in production environments and learn how to handle failures.
This is where you build real-world resilience and confidence with database testing.
"""

import os
import sys
from pathlib import Path

# Python version check
if sys.version_info < (3, 10):
    print("❌ Python 3.10 or higher is required")
    print(f"   Current version: {sys.version}")
    print("   Please upgrade Python and try again")
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
        print("   or run: python setup.py")
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

def chaos_version_conflicts():
    """Version compatibility chaos - the real world is messy!"""
    print("\n💥 Version Compatibility Chaos...")
    print("🚨 Your app works with PostgreSQL 13, but production uses 15...")
    
    versions_to_test = [
        ("postgres:13-alpine", "PostgreSQL 13"),
        ("postgres:15-alpine", "PostgreSQL 15")
    ]
    
    test_results = []
    
    for version, name in versions_to_test:
        try:
            with PostgresContainer(version) as postgres:
                conn = psycopg2.connect(
                    host=postgres.get_container_host_ip(),
                    port=postgres.get_exposed_port(5432),
                    user=postgres.username,
                    password=postgres.password,
                    database=postgres.dbname
                )
                
                cursor = conn.cursor()
                
                # Get version info
                cursor.execute("SELECT version()")
                version_info = cursor.fetchone()[0]
                version_num = version_info.split()[1]
                
                # Test features that might break
                features = {}
                
                # JSONB test
                try:
                    cursor.execute("SELECT jsonb_build_object('user', 'alice', 'age', 25)")
                    result = cursor.fetchone()[0]
                    features['JSONB'] = f"✅ {result}"
                except Exception as e:
                    features['JSONB'] = f"❌ {str(e)[:30]}"
                
                # Window functions test
                try:
                    cursor.execute("""
                        SELECT name, price, ROW_NUMBER() OVER (ORDER BY price DESC) as rank
                        FROM (VALUES ('Laptop', 999.99), ('Mouse', 29.99)) AS t(name, price)
                    """)
                    results = cursor.fetchall()
                    features['Window'] = f"✅ {len(results)} rows"
                except Exception as e:
                    features['Window'] = f"❌ {str(e)[:30]}"
                
                # Array functions test
                try:
                    cursor.execute("SELECT ARRAY[1,2,3] && ARRAY[3,4,5]")
                    result = cursor.fetchone()[0]
                    features['Arrays'] = f"✅ {result}"
                except Exception as e:
                    features['Arrays'] = f"❌ {str(e)[:30]}"
                
                test_results.append({
                    'name': name,
                    'version': version_num,
                    'features': features
                })
                
                cursor.close()
                conn.close()
                
        except Exception as e:
            test_results.append({
                'name': name,
                'version': 'FAILED',
                'features': {'Connection': f"💥 {str(e)[:30]}"}
            })
    
    print("\n📊 Version Test Results:")
    for result in test_results:
        print(f"\n🔍 {result['name']} ({result['version']}):")
        for feature, status in result['features'].items():
            print(f"   {feature:<8}: {status}")
    
    # Show compatibility issues
    working_versions = [r for r in test_results if r['version'] != 'FAILED']
    if len(working_versions) > 1:
        print(f"\n⚠️  Compatibility Issues Found:")
        print(f"   Different versions may behave differently in production!")
        print(f"   Always test with your production PostgreSQL version!")

def chaos_data_constraints():
    """Data corruption simulation - test your constraints!"""
    print("\n💥 Data Constraint Chaos...")
    print("🚨 What happens when bad data arrives?")
    
    try:
        with PostgresContainer("postgres:15-alpine") as postgres:
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=postgres.username,
                password=postgres.password,
                database=postgres.dbname
            )
            
            cursor = conn.cursor()
            
            # Create table with constraints
            cursor.execute("""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_name VARCHAR(50) NOT NULL,
                    amount DECIMAL(10,2) CHECK (amount > 0),
                    email VARCHAR(100) UNIQUE,
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            print("📊 Table Created: orders (with constraints)")
            
            # Test constraint violations with real data
            test_cases = [
                ("Valid Order", ("Alice Johnson", 99.99, "alice@example.com")),
                ("Negative Amount", ("Bob Smith", -50.00, "bob@example.com")),
                ("Duplicate Email", ("Carol Davis", 150.00, "alice@example.com")),
                ("Null Name", (None, 75.00, "dave@example.com")),
                ("Valid Order 2", ("Eve Wilson", 200.00, "eve@example.com"))
            ]
            
            print("\n🧪 Testing Data Insertions:")
            successful_inserts = 0
            failed_inserts = 0
            
            for description, (name, amount, email) in test_cases:
                try:
                    cursor.execute(
                        "INSERT INTO orders (customer_name, amount, email) VALUES (%s, %s, %s)",
                        (name, amount, email)
                    )
                    conn.commit()
                    print(f"   ✅ {description}: {name} - ${amount} ({email})")
                    successful_inserts += 1
                except Exception as e:
                    error_msg = str(e).split('\n')[0]
                    print(f"   ❌ {description}: {error_msg}")
                    conn.rollback()
                    failed_inserts += 1
            
            # Show current data
            cursor.execute("SELECT id, customer_name, amount, email FROM orders ORDER BY id")
            orders = cursor.fetchall()
            
            print(f"\n📋 Current Orders ({len(orders)} total):")
            for order_id, name, amount, email in orders:
                print(f"   #{order_id}: {name} - ${amount} ({email})")
            
            # Test transaction rollback with real scenario
            print(f"\n🔄 Testing Transaction Rollback:")
            try:
                cursor.execute("BEGIN")
                print("   Starting transaction...")
                
                cursor.execute("INSERT INTO orders (customer_name, amount, email) VALUES (%s, %s, %s)", 
                             ("Transaction Test", 300.00, "transaction@example.com"))
                print("   + Added: Transaction Test - $300.00")
                
                cursor.execute("INSERT INTO orders (customer_name, amount, email) VALUES (%s, %s, %s)", 
                             ("Invalid Order", -100.00, "invalid@example.com"))
                print("   + Added: Invalid Order - $-100.00 (should fail)")
                
                cursor.execute("COMMIT")
                print("   ❌ Transaction completed (should have failed!)")
            except Exception as e:
                cursor.execute("ROLLBACK")
                print(f"   ✅ Transaction rolled back: {str(e).split('(')[0]}")
                print("   🔄 All changes reverted - database is clean!")
            
            # Final state
            cursor.execute("SELECT COUNT(*) FROM orders")
            final_count = cursor.fetchone()[0]
            print(f"\n📊 Final State: {final_count} orders in database")
            print(f"   Successful inserts: {successful_inserts}")
            print(f"   Failed inserts: {failed_inserts}")
            
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"   💥 Data constraint test failed: {e}")
    
    print(f"\n⚠️  Real-world lesson: Bad data is everywhere - test your constraints!")

def main():
    """Run PostgreSQL Chaos Scenarios"""
    print("💥 LAB 1: POSTGRESQL CHAOS - Real-World Failures")
    print("=" * 60)
    print("🚨 This is where you build real-world resilience!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        chaos_version_conflicts()
        chaos_data_constraints()
        
        print("\n🎉 CHAOS SCENARIOS COMPLETED!")
        print("Key lessons learned:")
        print("• Version compatibility is REAL - test multiple versions")
        print("• Data constraints matter - test edge cases")
        print("• Transactions can fail - handle rollbacks")
        print("• Real-world is messy - TestContainers helps you prepare!")
        print("\n💪 You're now ready for production chaos!")
        
    except Exception as e:
        print(f"❌ Chaos scenarios failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
