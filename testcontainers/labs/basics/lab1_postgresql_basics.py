#!/usr/bin/env python3
"""
Lab 1: PostgreSQL Basics - Working Examples
===========================================

Learn PostgreSQL fundamentals with TestContainers - real database operations,
version testing, and CRUD operations. Perfect for building confidence and
understanding database testing basics.
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

def demo_basic_container():
    """Basic container demo - see the magic!"""
    print("\n🚀 Starting PostgreSQL Container...")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        print(f"✅ Container Ready: {postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}")
        print(f"📊 Database: {postgres.dbname} | User: {postgres.username}")
        
        # Test actual connection
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), current_user, version()")
        db_name, user, version = cursor.fetchone()
        
        print(f"🔗 Connected: {db_name} as {user}")
        print(f"📋 Version: {version.split()[0]} {version.split()[1]}")
        
        cursor.close()
        conn.close()

def demo_database_operations():
    """Database operations demo - real CRUD!"""
    print("\n🚀 Database Operations Demo...")
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            database=postgres.dbname
        )
        
        cursor = conn.cursor()
        
        # Create table
        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("📊 Table Created: products")
        
        # Insert data
        products = [
            ("MacBook Pro", 2499.99, "Electronics"),
            ("Coffee Mug", 12.99, "Kitchen"),
            ("Python Book", 49.99, "Education"),
            ("Wireless Mouse", 29.99, "Electronics")
        ]
        
        print("📝 Inserting Products:")
        for name, price, category in products:
            cursor.execute(
                "INSERT INTO products (name, price, category) VALUES (%s, %s, %s)",
                (name, price, category)
            )
            print(f"   + {name} - ${price} ({category})")
        
        conn.commit()
        
        # Read data with aggregations
        print("\n📖 Query Results:")
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(price) as avg_price, 
                   MIN(price) as min_price, MAX(price) as max_price
            FROM products 
            GROUP BY category 
            ORDER BY avg_price DESC
        """)
        
        results = cursor.fetchall()
        for category, count, avg_price, min_price, max_price in results:
            print(f"   {category}: {count} items | Avg: ${avg_price:.2f} | Range: ${min_price:.2f}-${max_price:.2f}")
        
        # Show individual products
        cursor.execute("SELECT id, name, price, category FROM products ORDER BY price DESC")
        products_data = cursor.fetchall()
        
        print(f"\n📋 All Products ({len(products_data)} total):")
        for product_id, name, price, category in products_data:
            print(f"   #{product_id}: {name} - ${price} ({category})")
        
        cursor.close()
        conn.close()

def demo_version_comparison():
    """Version comparison demo - test different versions!"""
    print("\n🚀 Version Comparison Demo...")
    
    versions = [
        ("postgres:13-alpine", "PostgreSQL 13"),
        ("postgres:15-alpine", "PostgreSQL 15")
    ]
    
    version_results = []
    
    for version, name in versions:
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
            
            # Test features
            cursor.execute("SELECT current_setting('server_version_num')")
            version_num_int = int(cursor.fetchone()[0])
            
            # Test JSONB support
            try:
                cursor.execute("SELECT jsonb_build_object('test', 'value')")
                jsonb_support = "✅"
            except:
                jsonb_support = "❌"
            
            # Test window functions
            try:
                cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY 1) as row_num")
                window_support = "✅"
            except:
                window_support = "❌"
            
            version_results.append({
                'name': name,
                'version': version_num,
                'version_num': version_num_int,
                'jsonb': jsonb_support,
                'window': window_support
            })
            
            cursor.close()
            conn.close()
    
    print("📊 Version Comparison Results:")
    print("   Version    | JSONB | Window Functions")
    print("   -----------|-------|----------------")
    for result in version_results:
        print(f"   {result['name']:<11} | {result['jsonb']:<5} | {result['window']}")
    
    # Show feature differences
    if len(version_results) == 2:
        newer = version_results[1] if version_results[1]['version_num'] > version_results[0]['version_num'] else version_results[0]
        older = version_results[0] if version_results[1]['version_num'] > version_results[0]['version_num'] else version_results[1]
        print(f"\n🔍 {newer['name']} has newer features than {older['name']}")

def main():
    """Run Lab 1 - PostgreSQL Basics"""
    print("🚀 LAB 1: PostgreSQL Basics - Working Examples")
    print("=" * 60)
    print("✨ Learn PostgreSQL fundamentals with TestContainers!")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running or not available")
        print("💡 Please start Docker Desktop or Docker Engine")
        sys.exit(1)
    
    try:
        demo_basic_container()
        demo_database_operations()
        demo_version_comparison()
        
        print("\n✅ Lab 1 completed successfully!")
        print("Key concepts learned:")
        print("• Real database containers, not mocks")
        print("• Automatic cleanup and isolation")
        print("• Same behavior across environments")
        print("• Easy version testing")
        print("\n💪 You're ready for chaos scenarios!")
        print("💥 Try: python lab1_chaos.py")
        
    except Exception as e:
        print(f"❌ Lab failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == "__main__":
    main()
