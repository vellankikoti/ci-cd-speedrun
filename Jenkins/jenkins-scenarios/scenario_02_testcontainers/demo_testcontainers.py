#!/usr/bin/env python3
"""
TestContainers Integration Demo Script
Simple and powerful demonstration of TestContainers with PostgreSQL
"""

import os
import sys
import time
from testcontainers.postgres import PostgresContainer

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import TestContainersDatabaseManager

def demo_testcontainers():
    """Simple TestContainers demo"""
    print("\n" + "="*50)
    print("🐳 TestContainers Demo")
    print("="*50)
    
    print("\n📋 Step 1: Starting PostgreSQL TestContainer")
    postgres_container = PostgresContainer("postgres:15")
    postgres_container.start()
    
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(5432)
    print(f"✅ Container started: {host}:{port}")
    
    try:
        print("\n📋 Step 2: Testing Database Connection")
        db_manager = TestContainersDatabaseManager(
            container_host=host,
            container_port=int(port),
            database=postgres_container.dbname,
            username=postgres_container.username,
            password=postgres_container.password
        )
        print("✅ Database connection successful!")

        print("\n📋 Step 3: Initializing Database")
        db_manager.init_database()
        print("✅ Database initialized!")

        print("\n📋 Step 4: Testing Database Operations")
        users = db_manager.get_users()
        print(f"✅ Found {len(users)} users in database")

        new_user = db_manager.create_user("Demo User", "demo@test.com")
        print(f"✅ Created user: {new_user['name']}")

        print("\n🎉 TestContainers demo completed successfully!")

    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        print("\n📋 Step 5: Cleaning Up")
        if 'db_manager' in locals():
            db_manager.close()
        postgres_container.stop()
        print("✅ TestContainers cleaned up")

def main():
    """Main demo function"""
    # Check if running in non-interactive mode (Jenkins)
    if os.getenv('JENKINS_URL') or os.getenv('CI'):
        print("🤖 Running in automated mode (Jenkins/CI)")
        demo_testcontainers()
    else:
        print("Choose a demo to run:")
        print("1. TestContainers database demo")
        
        try:
            choice = input("\nEnter your choice (1): ").strip()
            if choice == "1":
                demo_testcontainers()
            else:
                print("❌ Invalid choice. Running demo by default.")
                demo_testcontainers()
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        except Exception as e:
            print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    main()