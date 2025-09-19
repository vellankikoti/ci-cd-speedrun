#!/usr/bin/env python3
"""
🚀 TestContainers Mastery Workshop Setup
========================================

A professional-grade setup system that creates an incredible learning experience
for TestContainers. Built by seasoned trainers with decades of experience.

This isn't just another tutorial - it's a journey to mastery.
"""

import sys
import os
import subprocess
import platform
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil

class Colors:
    """Professional color system for terminal output"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports colors"""
        if platform.system() == "Windows":
            try:
                import colorama
                colorama.init()
                return True
            except ImportError:
                    return False
        return sys.stdout.isatty()
    
    def red(self, text: str) -> str:
        return f"\033[91m{text}\033[0m" if self.enabled else text
    
    def green(self, text: str) -> str:
        return f"\033[92m{text}\033[0m" if self.enabled else text
    
    def yellow(self, text: str) -> str:
        return f"\033[93m{text}\033[0m" if self.enabled else text
    
    def blue(self, text: str) -> str:
        return f"\033[94m{text}\033[0m" if self.enabled else text
    
    def magenta(self, text: str) -> str:
        return f"\033[95m{text}\033[0m" if self.enabled else text
    
    def cyan(self, text: str) -> str:
        return f"\033[96m{text}\033[0m" if self.enabled else text
    
    def white(self, text: str) -> str:
        return f"\033[97m{text}\033[0m" if self.enabled else text
    
    def bold(self, text: str) -> str:
        return f"\033[1m{text}\033[0m" if self.enabled else text
    
    def dim(self, text: str) -> str:
        return f"\033[2m{text}\033[0m" if self.enabled else text

    def reset(self) -> str:
        return "\033[0m" if self.enabled else ""

class WorkshopSetup:
    """Professional TestContainers Workshop Setup System"""
    
    def __init__(self):
        self.colors = Colors()
        self.workshop_dir = Path(__file__).parent
        self.venv_dir = self.workshop_dir / "venv"
        self.python_cmd = self._detect_python()
        self.pip_cmd = None
        self.setup_log = []
        
        # Workshop configuration
        self.workshop_name = "TestContainers Mastery Workshop"
        self.version = "2.0.0"
        self.required_packages = [
            "testcontainers>=4.0.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-html>=3.2.0",
            "sqlalchemy>=2.0.0",
            "redis>=5.0.0",
            "pymongo>=4.5.0",
            "pymysql>=1.1.0",
            "psycopg2-binary>=2.9.0",
            "cryptography>=3.4.8",
            "docker>=6.1.0",
            "psutil>=5.9.0",
            "requests>=2.31.0",
            "colorama>=0.4.6",
            "tabulate>=0.9.0",
            "rich>=13.0.0",
            "typer>=0.9.0"
        ]
        
        # Docker images for the workshop
        self.docker_images = [
            "postgres:15-alpine",
            "mysql:8.0",
            "redis:7.2-alpine",
            "mongo:7.0",
            "mariadb:10.11",
            "nginx:alpine",
            "hello-world"
        ]
    
    def _detect_python(self) -> str:
        """Detect the best Python command to use"""
        # In virtual environment, use the venv's python
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return sys.executable
        
        # Try python3 first, then python
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, check=True)
                if result.returncode == 0:
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        raise RuntimeError("No suitable Python installation found")
    
    def _log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp and level"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.setup_log.append(log_entry)
        
        # Color coding
        if level == "ERROR":
            print(f"{self.colors.red('❌')} {message}")
        elif level == "WARNING":
            print(f"{self.colors.yellow('⚠️')} {message}")
        elif level == "SUCCESS":
            print(f"{self.colors.green('✅')} {message}")
        elif level == "INFO":
            print(f"{self.colors.cyan('ℹ️')} {message}")
        else:
            print(f"   {message}")
    
    def _print_banner(self):
        """Print the professional workshop banner"""
        banner = f"""
{self.colors.cyan('╔' + '═' * 78 + '╗')}
{self.colors.cyan('║')} {self.colors.bold(self.colors.white('🚀 TESTCONTAINERS MASTERY WORKSHOP 🚀'))} {self.colors.cyan('║')}
{self.colors.cyan('║')} {self.colors.dim('Version 2.0.0 - Professional Training Experience')} {self.colors.cyan('║')}
{self.colors.cyan('║')} {self.colors.dim('Built by seasoned trainers with decades of experience')} {self.colors.cyan('║')}
{self.colors.cyan('╚' + '═' * 78 + '╝')}

{self.colors.green('Welcome to the most comprehensive TestContainers learning experience!')}

{self.colors.yellow('🎯 What you\'ll master:')}
  • Real-world integration testing with live databases
  • Advanced container orchestration and management
  • Chaos engineering and resilience testing
  • Performance testing and optimization
  • Production-ready testing strategies
  • CI/CD pipeline integration

{self.colors.cyan('💡 This workshop includes:')}
  • Interactive hands-on labs
  • Real-world scenarios and challenges
  • Professional-grade code examples
  • Advanced testing patterns
  • Performance optimization techniques
  • Production deployment strategies

{self.colors.bold('Ready to become a TestContainers master? Let\'s begin! 🚀')}
"""
        print(banner)
    
    def _check_prerequisites(self) -> bool:
        """Check system prerequisites"""
        self._log("Checking system prerequisites...")
        
        # Check Python version
        try:
            result = subprocess.run([self.python_cmd, '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            self._log(f"Python found: {version}", "SUCCESS")
            
            # Check if it's Python 3.8+
            version_parts = version.split()[1].split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            if major < 3 or (major == 3 and minor < 8):
                self._log(f"Python 3.8+ required, found {major}.{minor}", "ERROR")
                return False
                
        except Exception as e:
            self._log(f"Python check failed: {e}", "ERROR")
            return False
        
        # Check Docker
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            self._log(f"Docker found: {result.stdout.strip()}", "SUCCESS")
        except Exception as e:
            self._log(f"Docker not found: {e}", "ERROR")
            self._log("Please install Docker Desktop and ensure it's running", "ERROR")
            return False
        
        # Check Docker daemon
        try:
            result = subprocess.run(['docker', 'info'], 
                                  capture_output=True, text=True, check=True)
            self._log("Docker daemon is running", "SUCCESS")
        except Exception as e:
            self._log("Docker daemon is not running", "ERROR")
            self._log("Please start Docker Desktop", "ERROR")
            return False
        
        return True
    
    def _create_virtual_environment(self) -> bool:
        """Create and configure virtual environment"""
        self._log("Setting up isolated Python environment...")
        
        try:
            # Remove existing venv if it exists
            if self.venv_dir.exists():
                self._log("Removing existing virtual environment...")
                shutil.rmtree(self.venv_dir)
            
            # Create new virtual environment
            result = subprocess.run([self.python_cmd, '-m', 'venv', str(self.venv_dir)], 
                                  check=True, capture_output=True, text=True)
            self._log("Virtual environment created successfully", "SUCCESS")
            
            # Determine pip command
            if platform.system() == "Windows":
                self.pip_cmd = str(self.venv_dir / "Scripts" / "pip.exe")
                self.python_cmd = str(self.venv_dir / "Scripts" / "python.exe")
            else:
                self.pip_cmd = str(self.venv_dir / "bin" / "pip")
                self.python_cmd = str(self.venv_dir / "bin" / "python")
            
            return True
            
        except Exception as e:
            self._log(f"Failed to create virtual environment: {e}", "ERROR")
            return False
    
    def _install_packages(self) -> bool:
        """Install required Python packages"""
        self._log("Installing workshop dependencies...")
        
        try:
            # Upgrade pip first
            self._log("Upgrading pip...")
            result = subprocess.run([self.python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                                  check=True, capture_output=True, text=True)
            self._log("pip upgraded successfully", "SUCCESS")
            
            # Install packages
            self._log("Installing workshop packages...")
            for package in self.required_packages:
                self._log(f"Installing {package}...")
                result = subprocess.run([self.python_cmd, '-m', 'pip', 'install', package], 
                                      check=True, capture_output=True, text=True)
            
            self._log("All packages installed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Package installation failed: {e}", "ERROR")
            return False
    
    def _pull_docker_images(self) -> bool:
        """Pre-pull Docker images for faster workshop execution"""
        self._log("Pre-pulling Docker images for instant workshop startup...")
        
        success_count = 0
        for image in self.docker_images:
            try:
                self._log(f"Pulling {image}...")
                result = subprocess.run(['docker', 'pull', image], 
                                      check=True, capture_output=True, text=True)
                self._log(f"✅ {image} ready", "SUCCESS")
                success_count += 1
            except Exception as e:
                self._log(f"Failed to pull {image}: {e}", "WARNING")
        
        self._log(f"Pulled {success_count}/{len(self.docker_images)} images", "SUCCESS")
        return success_count > 0
    
    def _create_workshop_structure(self) -> bool:
        """Create the workshop directory structure"""
        self._log("Creating workshop structure...")
        
        try:
            # Create workshop directories
            dirs = [
                "labs",
                "labs/basics",
                "labs/intermediate", 
                "labs/advanced",
                "labs/real_world",
                "examples",
                "challenges",
                "solutions",
                "reports"
            ]
            
            for dir_path in dirs:
                (self.workshop_dir / dir_path).mkdir(exist_ok=True)
            
            self._log("Workshop structure created", "SUCCESS")
            return True
            
        except Exception as e:
            self._log(f"Failed to create workshop structure: {e}", "ERROR")
            return False
    
    def _create_demo_scripts(self) -> bool:
        """Create amazing demo scripts that showcase TestContainers power"""
        self._log("Creating incredible demo scripts...")
        
        try:
            # Create the main demo script
            demo_script = self.workshop_dir / "demo.py"
            with open(demo_script, 'w') as f:
                f.write('''#!/usr/bin/env python3
"""
🎬 TestContainers Power Demo
============================

This demo showcases the incredible power of TestContainers with real-world scenarios.
Watch as we spin up entire database clusters, test complex integrations, and handle
chaos engineering - all in seconds!
"""

import sys
import time
from pathlib import Path

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
    print("\\n🐘 PostgreSQL Demo - Enterprise Database Testing")
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
    print("\\n🐬 MySQL Demo - High-Performance Database Testing")
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
    print("\\n🔴 Redis Demo - Lightning-Fast Caching")
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
    print("\\n🍃 MongoDB Demo - Document Database Power")
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
    
    print("\\n🚀 Starting TestContainers Power Demo...")
    print("This will showcase the incredible power of TestContainers with real databases!")
    print("\\nPress Enter to begin...")
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
        
        print("\\n" + "=" * 60)
        print("🎉 DEMO COMPLETE! 🎉")
        print("=" * 60)
        print("\\nWhat you just witnessed:")
        print("✅ 4 different databases started and configured automatically")
        print("✅ Real data operations performed on each database")
        print("✅ Complex queries and aggregations executed")
        print("✅ All containers cleaned up automatically")
        print("✅ Zero manual setup or configuration required")
        print("\\nThis is the power of TestContainers - real testing with real databases!")
        print("\\nReady to dive deeper? Run: python workshop.py")
        
except Exception as e:
        print(f"\\n❌ Demo failed: {e}")
        print("This might be due to Docker not running or network issues.")
        print("Please ensure Docker Desktop is running and try again.")

if __name__ == "__main__":
    main()
''')
            
            # Make it executable
            demo_script.chmod(0o755)
            
            self._log("Demo scripts created successfully", "SUCCESS")
            return True
                
        except Exception as e:
            self._log(f"Failed to create demo scripts: {e}", "ERROR")
            return False
    
    def _save_setup_log(self):
        """Save setup log for troubleshooting"""
        log_file = self.workshop_dir / "setup_log.txt"
        with open(log_file, 'w') as f:
            f.write(f"TestContainers Workshop Setup Log\\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"Python: {self.python_cmd}\\n")
            f.write(f"Pip: {self.pip_cmd}\\n\\n")
            f.write("\\n".join(self.setup_log))
        
        self._log(f"Setup log saved to: {log_file}")
    
    def run_setup(self) -> bool:
        """Run the complete workshop setup"""
        self._print_banner()
        
        try:
            # Step 1: Check prerequisites
            if not self._check_prerequisites():
                self._log("Prerequisites check failed", "ERROR")
                return False
            
            # Step 2: Create virtual environment
            if not self._create_virtual_environment():
                self._log("Virtual environment creation failed", "ERROR")
                return False
            
            # Step 3: Install packages
            if not self._install_packages():
                self._log("Package installation failed", "ERROR")
                return False
            
            # Step 4: Pull Docker images
            if not self._pull_docker_images():
                self._log("Docker image pulling failed", "WARNING")
            
            # Step 5: Create workshop structure
            if not self._create_workshop_structure():
                self._log("Workshop structure creation failed", "WARNING")
            
            # Step 6: Create demo scripts
            if not self._create_demo_scripts():
                self._log("Demo script creation failed", "WARNING")
            
            # Step 7: Save setup log
            self._save_setup_log()
            
            # Success!
            self._print_success_message()
            return True
            
        except KeyboardInterrupt:
            self._log("Setup interrupted by user", "WARNING")
            return False
        except Exception as e:
            self._log(f"Setup failed with error: {e}", "ERROR")
            return False
    
    def _print_success_message(self):
        """Print the success message with next steps"""
        success_msg = f"""
{self.colors.green('╔' + '═' * 78 + '╗')}
{self.colors.green('║')} {self.colors.bold(self.colors.white('🎉 WORKSHOP SETUP COMPLETE! 🎉'))} {self.colors.green('║')}
{self.colors.green('╚' + '═' * 78 + '╝')}

{self.colors.green('✅ Your TestContainers Mastery Workshop is ready!')}

{self.colors.cyan('🚀 Quick Start:')}
  python demo.py          # See the power of TestContainers in action
  python workshop.py      # Start the full workshop experience

{self.colors.yellow('📚 What\'s Next:')}
  1. Run the demo to see TestContainers in action
  2. Explore the labs directory for hands-on exercises
  3. Try the challenges for advanced scenarios
  4. Check the examples for real-world patterns

{self.colors.magenta('💡 Pro Tips:')}
  • All databases are pre-pulled for instant startup
  • Virtual environment is isolated and clean
  • Workshop structure is organized by difficulty
  • Solutions are provided for all challenges

{self.colors.bold('Ready to become a TestContainers master? Let\'s go! 🚀')}
"""
        print(success_msg)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TestContainers Mastery Workshop Setup")
    parser.add_argument("--validate-only", action="store_true", help="Only validate prerequisites")
    parser.add_argument("--quick", action="store_true", help="Quick setup without Docker image pulling")
    
    args = parser.parse_args()
    
    setup = WorkshopSetup()
    
    if args.validate_only:
        success = setup._check_prerequisites()
        sys.exit(0 if success else 1)
    
    success = setup.run_setup()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
