#!/usr/bin/env python3
"""
Test with TestContainers - The Solution
=======================================

This demonstrates how TestContainers catches real bugs
that mocks would miss. Real database, real constraints!

Run this test to see TestContainers magic in action.
"""

import unittest
import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

def submit_vote_testcontainers(conn, user_id, choice):
    """Submit vote using real PostgreSQL database"""
    cur = conn.cursor()
    try:
        # This will fail if user already voted (UNIQUE constraint)
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

class TestVotingWithTestContainers(unittest.TestCase):
    """Test voting functionality with real PostgreSQL database"""
    
    @classmethod
    def setUpClass(cls):
        """Set up real PostgreSQL container for all tests"""
        print("\n🚀 Starting PostgreSQL container...")
        start_time = time.time()
        
        cls.postgres = PostgresContainer("postgres:15-alpine")
        cls.postgres.start()
        
        setup_time = time.time() - start_time
        print(f"✅ PostgreSQL ready! (startup: {setup_time:.1f}s)")
        
        # Set up database schema
        setup_test_database(cls.postgres)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up PostgreSQL container"""
        if hasattr(cls, 'postgres'):
            cls.postgres.stop()
            print("🧹 PostgreSQL container stopped")
    
    def setUp(self):
        """Set up fresh connection for each test"""
        self.conn = psycopg.connect(
            host=self.postgres.get_container_host_ip(),
            port=self.postgres.get_exposed_port(5432),
            user=self.postgres.username,
            password=self.postgres.password,
            dbname=self.postgres.dbname
        )
        
        # Clear votes table for each test
        cur = self.conn.cursor()
        cur.execute("DELETE FROM votes")
        self.conn.commit()
        cur.close()
    
    def tearDown(self):
        """Close connection after each test"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def test_first_vote_succeeds(self):
        """First vote should succeed"""
        result = submit_vote_testcontainers(self.conn, "user1", "Python")
        self.assertTrue(result, "First vote should succeed")
        
        # Verify vote was recorded
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user1",))
        count = cur.fetchone()[0]
        cur.close()
        self.assertEqual(count, 1)
    
    def test_duplicate_vote_fails(self):
        """Duplicate vote should fail - THIS IS THE MAGIC!"""
        # First vote succeeds
        result1 = submit_vote_testcontainers(self.conn, "user1", "Python")
        self.assertTrue(result1, "First vote should succeed")
        
        # Duplicate vote fails - REAL DATABASE CONSTRAINT!
        result2 = submit_vote_testcontainers(self.conn, "user1", "Python")
        self.assertFalse(result2, "Duplicate vote should fail with real database")
        
        # Verify only one vote exists
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user1",))
        count = cur.fetchone()[0]
        cur.close()
        self.assertEqual(count, 1, "Should have exactly 1 vote")
    
    def test_different_users_can_vote_same_choice(self):
        """Different users can vote for the same choice"""
        # User 1 votes for Python
        result1 = submit_vote_testcontainers(self.conn, "user1", "Python")
        self.assertTrue(result1, "User1 vote should succeed")
        
        # User 2 votes for Python (different user, same choice)
        result2 = submit_vote_testcontainers(self.conn, "user2", "Python")
        self.assertTrue(result2, "User2 vote should succeed")
        
        # Verify both votes exist
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes")
        total_count = cur.fetchone()[0]
        cur.close()
        self.assertEqual(total_count, 2, "Should have 2 votes total")
    
    def test_same_user_different_choices_fails(self):
        """Same user voting different choices should fail (UNIQUE constraint)"""
        # User votes for Python
        result1 = submit_vote_testcontainers(self.conn, "user1", "Python")
        self.assertTrue(result1, "First vote should succeed")
        
        # Same user votes for JavaScript - should fail!
        result2 = submit_vote_testcontainers(self.conn, "user1", "JavaScript")
        self.assertFalse(result2, "Same user different choice should fail")
        
        # Verify only first vote exists
        cur = self.conn.cursor()
        cur.execute("SELECT choice FROM votes WHERE user_id = %s", ("user1",))
        choice = cur.fetchone()[0]
        cur.close()
        self.assertEqual(choice, "Python", "Should have only the first choice")
    
    def test_database_constraints_are_real(self):
        """Test that database constraints are actually enforced"""
        # This test verifies we're using a real database with real constraints
        
        # Insert a vote
        submit_vote_testcontainers(self.conn, "user1", "Python")
        
        # Try to insert duplicate directly via SQL - should fail
        cur = self.conn.cursor()
        with self.assertRaises(IntegrityError):
            cur.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("user1", "Python")
            )
            self.conn.commit()
        
        cur.close()
    
    def test_multiple_votes_different_users(self):
        """Multiple users can vote for different choices"""
        users_and_choices = [
            ("user1", "Python"),
            ("user2", "JavaScript"),
            ("user3", "Go"),
            ("user4", "Rust")
        ]
        
        for user_id, choice in users_and_choices:
            result = submit_vote_testcontainers(self.conn, user_id, choice)
            self.assertTrue(result, f"Vote for {user_id} should succeed")
        
        # Verify all votes exist
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM votes")
        total_count = cur.fetchone()[0]
        cur.close()
        self.assertEqual(total_count, 4, "Should have 4 votes total")

def demonstrate_testcontainers_solution():
    """Demonstrate TestContainers solution clearly"""
    print("\n" + "="*60)
    print("✅ TESTCONTAINERS TESTING - THE SOLUTION")
    print("="*60)
    
    print("\n🚀 Starting real PostgreSQL container...")
    start_time = time.time()
    
    with PostgresContainer("postgres:15-alpine") as postgres:
        setup_time = time.time() - start_time
        print(f"✅ PostgreSQL ready! (startup: {setup_time:.1f}s)")
        
        # Set up database
        setup_test_database(postgres)

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
        print("="*60)
        
        conn.close()

if __name__ == '__main__':
    print("🧪 Running TestContainers Tests...")
    print("This demonstrates the power of real database testing!")
    
    # Run the demonstration
    demonstrate_testcontainers_solution()
    
    # Run unit tests
    print("\n🧪 Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    print("\n🎉 TestContainers magic complete!")
    print("💡 This is why TestContainers beats mocks!")
