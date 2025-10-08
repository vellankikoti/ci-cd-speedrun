#!/usr/bin/env python3
"""
TestContainers Integration Demo Script
Demonstrates real TestContainers functionality with PostgreSQL
"""

import os
import sys
import time
import requests
from testcontainers.postgres import PostgresContainer

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import TestContainersDatabaseManager
import app

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🐳 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def demo_testcontainers_database():
    """Demo TestContainers database functionality"""
    print_header("TestContainers Database Integration Demo")
    
    print_step(1, "Starting PostgreSQL TestContainer")
    print("🚀 Starting PostgreSQL container...")
    
    # Start PostgreSQL container
    postgres_container = PostgresContainer("postgres:15")
    postgres_container.start()
    
    # Get connection details
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(5432)
    database = postgres_container.get_database_name()
    username = postgres_container.get_username()
    password = postgres_container.get_password()
    
    print(f"✅ PostgreSQL container started!")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Database: {database}")
    print(f"   Username: {username}")
    
    try:
        print_step(2, "Creating TestContainers Database Manager")
        db_manager = TestContainersDatabaseManager(host, port, database, username, password)
        print("✅ Database manager created with TestContainers connection")
        
        print_step(3, "Initializing Database")
        db_manager.init_database()
        print("✅ Database initialized with tables and sample data")
        
        print_step(4, "Testing Database Operations")
        
        # Test health check
        health = db_manager.health_check()
        print(f"🔍 Health check: {'✅ Healthy' if health else '❌ Unhealthy'}")
        
        # Test getting users
        users = db_manager.get_users()
        print(f"👥 Found {len(users)} users in database")
        
        # Test creating a user
        new_user = db_manager.create_user("TestContainers Demo User", "demo@testcontainers.com")
        if 'error' not in new_user:
            print(f"✅ Created user: {new_user['name']} ({new_user['email']})")
        else:
            print(f"❌ Failed to create user: {new_user['error']}")
        
        # Test updating user
        if 'error' not in new_user:
            updated_user = db_manager.update_user(new_user['id'], name="Updated Demo User")
            if 'error' not in updated_user:
                print(f"✅ Updated user: {updated_user['name']}")
            else:
                print(f"❌ Failed to update user: {updated_user['error']}")
        
        # Test database stats
        stats = db_manager.get_database_stats()
        print(f"📊 Database statistics:")
        print(f"   - User count: {stats.get('user_count', 'Unknown')}")
        print(f"   - Database size: {stats.get('database_size', 'Unknown')}")
        print(f"   - Tables: {len(stats.get('tables', []))}")
        
        print_step(5, "Testing Concurrent Operations")
        import threading
        
        results = []
        def create_user_operation(user_id):
            result = db_manager.create_user(f"Concurrent User {user_id}", f"concurrent{user_id}@test.com")
            if 'error' not in result:
                results.append(user_id)
        
        # Create 5 concurrent threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_user_operation, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print(f"✅ Created {len(results)} users concurrently")
        
        print_step(6, "Final Database State")
        final_users = db_manager.get_users()
        print(f"👥 Total users in database: {len(final_users)}")
        
        # Show some sample users
        print("📋 Sample users:")
        for i, user in enumerate(final_users[:3]):
            print(f"   {i+1}. {user['name']} - {user['email']}")
        
        print("\n🎉 TestContainers database demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print_step(7, "Cleaning Up")
        db_manager.close()
        postgres_container.stop()
        print("✅ TestContainers stopped and cleaned up")

def demo_application_with_testcontainers():
    """Demo the application with TestContainers"""
    print_header("Application with TestContainers Demo")
    
    print_step(1, "Starting PostgreSQL TestContainer for Application")
    postgres_container = PostgresContainer("postgres:15")
    postgres_container.start()
    
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(5432)
    database = postgres_container.get_database_name()
    username = postgres_container.get_username()
    password = postgres_container.get_password()
    
    print(f"✅ PostgreSQL container started: {host}:{port}")
    
    try:
        print_step(2, "Configuring Application for TestContainers")
        # Set environment variables for the application
        os.environ['DB_TYPE'] = 'testcontainers'
        os.environ['TESTCONTAINERS_HOST'] = host
        os.environ['TESTCONTAINERS_PORT'] = str(port)
        os.environ['DB_NAME'] = database
        os.environ['DB_USER'] = username
        os.environ['DB_PASSWORD'] = password
        os.environ['PORT'] = '5003'  # Use different port for demo
        
        print("✅ Environment configured for TestContainers")
        
        print_step(3, "Starting Application Server")
        import threading
        
        # Start application in background thread
        app_thread = threading.Thread(
            target=app.start_server,
            args=(5003,),
            daemon=True
        )
        app_thread.start()
        
        # Wait for application to start
        print("⏳ Waiting for application to start...")
        time.sleep(5)
        
        base_url = 'http://localhost:5003'
        print(f"✅ Application started at {base_url}")
        
        print_step(4, "Testing Application Endpoints")
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check: {data['status']} (Database: {data['database']})")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        # Test users API
        try:
            response = requests.get(f"{base_url}/api/users")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Users API: Found {data['count']} users")
            else:
                print(f"❌ Users API failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Users API error: {e}")
        
        # Test database stats
        try:
            response = requests.get(f"{base_url}/api/db-stats")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Database stats: {data['user_count']} users, {data['database_size']} size")
            else:
                print(f"❌ Database stats failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Database stats error: {e}")
        
        # Test creating a user via API
        try:
            new_user_data = {
                'name': 'API Demo User',
                'email': 'api@testcontainers.com'
            }
            response = requests.post(f"{base_url}/api/users", json=new_user_data)
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Created user via API: {data['user']['name']}")
            else:
                print(f"❌ Create user API failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Create user API error: {e}")
        
        print_step(5, "Application Demo Complete")
        print(f"🌐 Application is running at {base_url}")
        print("🔗 You can open the URL in your browser to see the full interface")
        print("⏳ Press Ctrl+C to stop the demo...")
        
        # Keep the application running for a bit
        try:
            time.sleep(30)  # Run for 30 seconds
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        
    except Exception as e:
        print(f"❌ Error during application demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print_step(6, "Cleaning Up")
        postgres_container.stop()
        print("✅ TestContainers stopped and cleaned up")

def main():
    """Main demo function"""
    print_header("TestContainers Integration Workshop Demo")
    print("This demo shows real TestContainers integration with PostgreSQL")
    print("Choose a demo to run:")
    print("1. Database-only demo (TestContainers + PostgreSQL)")
    print("2. Full application demo (TestContainers + App + API)")
    print("3. Both demos")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            demo_testcontainers_database()
        elif choice == "2":
            demo_application_with_testcontainers()
        elif choice == "3":
            demo_testcontainers_database()
            print("\n" + "="*60)
            input("Press Enter to continue to application demo...")
            demo_application_with_testcontainers()
        else:
            print("❌ Invalid choice. Running database demo by default.")
            demo_testcontainers_database()
    
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
