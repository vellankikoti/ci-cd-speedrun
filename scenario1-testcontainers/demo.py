#!/usr/bin/env python3
"""
Scenario 1: TestContainers Magic - Demo Script
==============================================

This script demonstrates the power of TestContainers by showing:
1. How mocks can lie and miss real bugs
2. How TestContainers provides real database testing
3. The "magic moment" when a real constraint catches a bug

Run this script to see the demonstration without the web interface.
"""

import os
import sys
import time
from datetime import datetime

# Configure TestContainers
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

# Platform-specific Docker host configuration
if sys.platform == "win32":
    os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
else:
    os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

try:
    from testcontainers.postgres import PostgresContainer
    import psycopg
    from psycopg import IntegrityError
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install testcontainers psycopg[binary]")
    sys.exit(1)

class MockDatabase:
    """A mock database that doesn't enforce constraints"""
    
    def __init__(self):
        self.votes = []
        self.next_id = 1
    
    def execute(self, query, params=None):
        """Mock execute that doesn't enforce UNIQUE constraints"""
        if "INSERT INTO votes" in query:
            # Mock always allows inserts - no constraint checking!
            vote_id = self.next_id
            self.next_id += 1
            self.votes.append({
                'id': vote_id,
                'user_id': params[0],
                'choice': params[1]
            })
            return True
        elif "SELECT" in query:
            return self.votes
        return True
    
    def commit(self):
        pass
    
    def rollback(self):
        pass

def submit_vote_mock(db, user_id, choice):
    """Submit vote using mock database"""
    try:
        db.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, choice)
        )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

def submit_vote_testcontainers(conn, user_id, choice):
    """Submit vote using real PostgreSQL database"""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, choice)
        )
        conn.commit()
        return True
    except IntegrityError:
        conn.rollback()
        return False
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def setup_test_database(container):
    """Set up test database schema"""
    conn = psycopg.connect(
        host=container.get_container_host_ip(),
        port=container.get_exposed_port(5432),
        user=container.username,
        password=container.password,
        dbname=container.dbname
    )
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(100) UNIQUE NOT NULL,
            choice VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def demo_mock_problem():
    """Demonstrate the problem with mocks"""
    print("\n" + "="*70)
    print("❌ MOCK DATABASE TESTING - THE PROBLEM")
    print("="*70)
    
    mock_db = MockDatabase()
    
    print("\n🧪 Testing with Mock Database:")
    print("   - No constraint enforcement")
    print("   - No real SQL behavior")
    print("   - False confidence")
    
    print("\n📝 Test 1: First vote")
    result1 = submit_vote_mock(mock_db, "user1", "Python")
    print(f"   Result: {'✅ PASS' if result1 else '❌ FAIL'}")
    print(f"   Votes in mock: {len(mock_db.votes)}")
    
    print("\n📝 Test 2: Duplicate vote (should fail in production)")
    result2 = submit_vote_mock(mock_db, "user1", "Python")
    print(f"   Result: {'✅ PASS' if result2 else '❌ FAIL'}")
    print(f"   Votes in mock: {len(mock_db.votes)}")
    print("   ⚠️  PROBLEM: Mock allows duplicate vote!")
    
    print("\n📝 Test 3: Multiple duplicates")
    for i in range(3):
        result = submit_vote_mock(mock_db, "user1", "Python")
        print(f"   Vote {i+3}: {'✅ PASS' if result else '❌ FAIL'}")
    
    print(f"   Total votes in mock: {len(mock_db.votes)}")
    print("   ⚠️  PROBLEM: Same user voted 5 times!")
    
    print("\n💥 PRODUCTION IMPACT:")
    print("   - Users can vote multiple times")
    print("   - Data integrity compromised")
    print("   - Business logic violated")
    print("   - Security vulnerability")
    
    print("\n🎯 LESSON LEARNED:")
    print("   Mocks can lie! They don't test real database behavior.")
    print("   Use TestContainers for real database testing.")
    print("="*70)

def demo_testcontainers_solution():
    """Demonstrate TestContainers solution"""
    print("\n" + "="*70)
    print("✅ TESTCONTAINERS TESTING - THE SOLUTION")
    print("="*70)
    
    print("\n🚀 Starting real PostgreSQL container...")
    start_time = time.time()
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        setup_time = time.time() - start_time
        print(f"✅ PostgreSQL ready! (startup: {setup_time:.1f}s)")
        
        # Set up database
        setup_test_database(postgres)
        
        # Get connection details from container
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        
        print("\n🧪 Testing with Real PostgreSQL Database:")
        print("   - Real constraint enforcement")
        print("   - Real SQL behavior")
        print("   - Real confidence")
        
        print("\n📝 Test 1: First vote")
        result1 = submit_vote_testcontainers(conn, "user1", "Python")
        print(f"   Result: {'✅ PASS' if result1 else '❌ FAIL'}")
        
        # Check vote count
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user1",))
        count1 = cur.fetchone()[0]
        cur.close()
        print(f"   Votes in database: {count1}")
        
        print("\n📝 Test 2: Duplicate vote (should fail)")
        result2 = submit_vote_testcontainers(conn, "user1", "Python")
        print(f"   Result: {'✅ PASS' if result2 else '❌ FAIL'}")
        print("   🎯 MAGIC: Real database caught duplicate vote!")
        
        # Check vote count
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user1",))
        count2 = cur.fetchone()[0]
        cur.close()
        print(f"   Votes in database: {count2}")
        
        print("\n📝 Test 3: Different user, same choice")
        result3 = submit_vote_testcontainers(conn, "user2", "Python")
        print(f"   Result: {'✅ PASS' if result3 else '❌ FAIL'}")
        
        # Check total votes
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes")
        total_count = cur.fetchone()[0]
        cur.close()
        print(f"   Total votes in database: {total_count}")
        
        print("\n🎯 PRODUCTION IMPACT:")
        print("   - Users can only vote once")
        print("   - Data integrity maintained")
        print("   - Business logic enforced")
        print("   - Security vulnerability prevented")
        
        print("\n✨ LESSON LEARNED:")
        print("   TestContainers provides real database testing!")
        print("   Catches bugs that mocks would miss!")
        print("   Gives real confidence in production!")
        print("="*70)
        
        conn.close()

def demo_side_by_side():
    """Show side-by-side comparison"""
    print("\n" + "="*70)
    print("⚖️  SIDE-BY-SIDE COMPARISON")
    print("="*70)
    
    print("\n📊 Mock Database Results:")
    mock_db = MockDatabase()
    
    # Mock tests
    mock_results = []
    for i in range(5):
        result = submit_vote_mock(mock_db, "user1", "Python")
        mock_results.append(f"Vote {i+1}: {'✅' if result else '❌'}")
    
    for result in mock_results:
        print(f"   {result}")
    print(f"   Total votes: {len(mock_db.votes)}")
    print("   ❌ Mock allows unlimited votes!")
    
    print("\n📊 TestContainers Results:")
    with PostgresContainer("postgres:15-alpine") as postgres:
        setup_test_database(postgres)
        # Get connection details from container
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        
        testcontainers_results = []
        for i in range(5):
            result = submit_vote_testcontainers(conn, "user1", "Python")
            testcontainers_results.append(f"Vote {i+1}: {'✅' if result else '❌'}")
        
        for result in testcontainers_results:
            print(f"   {result}")
        
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user1",))
        count = cur.fetchone()[0]
        cur.close()
        print(f"   Total votes: {count}")
        print("   ✅ TestContainers enforces constraints!")
        
        conn.close()
    
    print("\n🏆 WINNER: TestContainers!")
    print("   Real database testing beats mock testing!")
    print("="*70)

def main():
    """Run the complete demonstration"""
    print("🧪 Scenario 1: TestContainers Magic - Demo")
    print("=" * 50)
    print("⚡ CI/CD Speed Run - PyCon ES 2025")
    print("")
    print("🎯 Learning: Real database testing vs mocks")
    print("🔧 Technology: Python + PostgreSQL + TestContainers")
    print("⏱️  Time: 5 minutes")
    print("")
    
    try:
        # Run demonstrations
        demo_mock_problem()
        demo_testcontainers_solution()
        demo_side_by_side()
        
        print("\n🎉 Demo complete!")
        print("")
        print("💡 Key Takeaways:")
        print("   • Mocks can give false confidence")
        print("   • TestContainers provides real database testing")
        print("   • Real constraints catch real bugs")
        print("   • TestContainers = Production parity")
        print("")
        print("🚀 Ready for the web demo? Run: python app.py")
        print("🌐 Then open: http://localhost:5001")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Make sure Docker is running and try again")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
