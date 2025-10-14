#!/usr/bin/env python3
"""
🧪 Scenario 1: TestContainers Magic - Interactive Workshop
==========================================================

A hands-on, interactive workshop that teaches TestContainers through
live demonstrations, real containers, and guided exercises.

This is NOT just running code - this is EXPERIENCING containers in action!

Run this script and follow along as we:
1. See mocks fail with live examples
2. Watch TestContainers catch bugs in real-time
3. Observe containers spinning up (Docker Desktop or CLI)
4. Run hands-on exercises yourself
5. Understand WHY TestContainers beats mocks

Duration: 10-15 minutes
Level: Beginner to Intermediate
Prerequisites: Docker running (automatically available in Codespaces!)
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# ==============================================================================
# ENVIRONMENT DETECTION
# ==============================================================================

def detect_environment():
    """Detect if running in Codespaces, local, or other environment"""
    if os.getenv('CODESPACES') == 'true':
        return 'codespaces'
    elif os.getenv('GITPOD_WORKSPACE_ID'):
        return 'gitpod'
    else:
        return 'local'

ENVIRONMENT = detect_environment()

# Configure TestContainers
os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"

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
    print("Run: python setup.py")
    sys.exit(1)

# ==============================================================================
# HELPER FUNCTIONS FOR INTERACTIVE EXPERIENCE
# ==============================================================================

def print_header(title, subtitle=""):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    if subtitle:
        print(f"   {subtitle}")
    print("="*70)

def print_step(number, title, description=""):
    """Print formatted step"""
    print(f"\n{'='*70}")
    print(f"📍 STEP {number}: {title}")
    if description:
        print(f"   {description}")
    print(f"{'='*70}")

def wait_for_user(message="Press ENTER to continue..."):
    """Wait for user to press enter"""
    input(f"\n💡 {message}")

def show_docker_tip():
    """Show environment-appropriate Docker viewing instructions"""
    print("\n" + "⚠️ " * 20)
    if ENVIRONMENT == 'codespaces':
        print("👀 TIP: Watch Containers in Real-Time!")
        print("   Run this in another terminal tab:")
        print("   $ watch -n 1 'docker ps --format \"table {{.Names}}\\t{{.Status}}\"'")
        print("")
        print("   You'll see:")
        print("   • Containers spinning up")
        print("   • Real PostgreSQL instances")
        print("   • Automatic cleanup when done")
        print("")
        print("   📍 Running in GitHub Codespaces - Docker is ready!")
    else:
        print("👀 TIP: Open Docker Desktop NOW!")
        print("   Watch the 'Containers' tab to see TestContainers in action")
        print("   You'll see:")
        print("   • Containers spinning up")
        print("   • Real PostgreSQL instances")
        print("   • Automatic cleanup when done")
    print("⚠️ " * 20)

def show_code(title, code, language="python"):
    """Display code with syntax highlighting"""
    print(f"\n📝 {title}:")
    print("```" + language)
    print(code)
    print("```")

def run_command_visible(command, description):
    """Run command and show output"""
    print(f"\n🔧 Running: {description}")
    print(f"   Command: {command}")
    print("\n" + "-"*70)
    result = subprocess.run(command, shell=True, text=True)
    print("-"*70)
    return result.returncode == 0

# ==============================================================================
# SECTION 1: THE PROBLEM - Mocks Can Lie
# ==============================================================================

def demo_mock_problem():
    """Demonstrate how mocks can give false confidence"""

    print_header("SECTION 1: The Problem with Mocks",
                 "See how mocks can lie and let bugs slip to production")

    wait_for_user("Ready to see the problem? Press ENTER...")

    # Show mock database code
    mock_code = """
class MockDatabase:
    def __init__(self):
        self.votes = []

    def insert_vote(self, user_id, choice):
        # Mock ALWAYS succeeds - no constraint checking!
        self.votes.append({'user_id': user_id, 'choice': choice})
        return True  # Always returns success!
"""

    show_code("Mock Database Implementation", mock_code)

    print("\n❌ THE PROBLEM:")
    print("   Mocks don't enforce database constraints")
    print("   No UNIQUE checks, no FOREIGN KEY validation")
    print("   Tests pass but production breaks!")

    wait_for_user("Let's run a test with this mock...")

    # Simulate mock test
    print_step(1, "Test with Mock Database", "Watch how it allows duplicate votes")

    class MockDatabase:
        def __init__(self):
            self.votes = []

        def insert_vote(self, user_id, choice):
            self.votes.append({'user_id': user_id, 'choice': choice})
            return True

    mock_db = MockDatabase()

    print("\n🧪 Test Scenario: Same user votes multiple times")
    print("\nAttempt 1: user123 votes for Python")
    result1 = mock_db.insert_vote("user123", "Python")
    print(f"   Result: {'✅ SUCCESS' if result1 else '❌ FAILED'}")
    print(f"   Total votes: {len(mock_db.votes)}")

    time.sleep(1)

    print("\nAttempt 2: user123 votes for Python AGAIN")
    result2 = mock_db.insert_vote("user123", "Python")
    print(f"   Result: {'✅ SUCCESS' if result2 else '❌ FAILED'} (⚠️ This should have failed!)")
    print(f"   Total votes: {len(mock_db.votes)}")

    time.sleep(1)

    print("\nAttempt 3: user123 votes for Python AGAIN!")
    result3 = mock_db.insert_vote("user123", "Python")
    print(f"   Result: {'✅ SUCCESS' if result3 else '❌ FAILED'} (⚠️ Still succeeding!)")
    print(f"   Total votes: {len(mock_db.votes)}")

    print("\n💥 PROBLEM IDENTIFIED:")
    print(f"   • Mock allowed {len(mock_db.votes)} votes from same user!")
    print("   • Test passed with flying colors")
    print("   • But in production: Same user could vote unlimited times")
    print("   • Business logic broken, data integrity compromised")

    wait_for_user("See the problem? Let's see the solution...")

# ==============================================================================
# SECTION 2: THE MAGIC - TestContainers Catches Bugs
# ==============================================================================

def demo_testcontainers_magic():
    """Demonstrate TestContainers catching real bugs"""

    print_header("SECTION 2: TestContainers Magic",
                 "Watch real containers catch bugs that mocks miss")

    show_docker_tip()
    if ENVIRONMENT == 'codespaces':
        wait_for_user("Ready to see containers? Press ENTER to start...")
    else:
        wait_for_user("Docker Desktop open? Press ENTER to start containers...")

    # Show real database code
    real_code = """
# Real PostgreSQL with TestContainers
with PostgresContainer("postgres:15-alpine") as postgres:
    conn = psycopg.connect(...)

    # Create table with UNIQUE constraint
    cursor.execute('''
        CREATE TABLE votes (
            user_id VARCHAR(100) UNIQUE NOT NULL,
            choice VARCHAR(50) NOT NULL
        )
    ''')
"""

    show_code("Real Database with TestContainers", real_code)

    print("\n✅ THE SOLUTION:")
    print("   Real PostgreSQL container with real constraints")
    print("   UNIQUE constraint on user_id prevents duplicates")
    print("   Tests behave exactly like production!")

    wait_for_user("Ready to see the magic? Press ENTER...")

    print_step(1, "Starting PostgreSQL Container",
               "Watch Docker Desktop - you'll see a new container appear!")

    print("\n🚀 Spinning up PostgreSQL container...")
    print("   Image: postgres:15-alpine")
    print("   Starting...")

    start_time = time.time()

    with PostgresContainer("postgres:15-alpine") as postgres:
        startup_time = time.time() - start_time

        print(f"   ✅ Container ready in {startup_time:.1f} seconds!")
        print(f"   Host: {postgres.get_container_host_ip()}")
        print(f"   Port: {postgres.get_exposed_port(5432)}")
        print(f"   Database: {postgres.dbname}")

        if ENVIRONMENT == 'codespaces':
            print("\n👀 CHECK YOUR DOCKER WATCH TERMINAL!")
            print("   You should see a PostgreSQL container running")
            print("   Run: docker ps | grep postgres")
        else:
            print("\n👀 CHECK DOCKER DESKTOP NOW!")
            print("   You should see a PostgreSQL container running")

        wait_for_user("See it? Press ENTER to create table...")

        print_step(2, "Creating Table with UNIQUE Constraint",
                   "This constraint will catch duplicate votes!")

        # Connect to database
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )

        cursor = conn.cursor()

        # Create table
        cursor.execute("""
            CREATE TABLE votes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                choice VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        print("\n✅ Table created with schema:")
        print("   • id: SERIAL PRIMARY KEY")
        print("   • user_id: VARCHAR(100) UNIQUE NOT NULL  ← The magic!")
        print("   • choice: VARCHAR(50) NOT NULL")
        print("   • created_at: TIMESTAMP")

        wait_for_user("Table created. Press ENTER to test voting...")

        print_step(3, "Testing with Real Database",
                   "Same test as before, but with real constraints")

        print("\n🧪 Test Scenario: Same user votes multiple times")

        # Attempt 1
        print("\nAttempt 1: user123 votes for Python")
        try:
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("user123", "Python")
            )
            conn.commit()
            print("   Result: ✅ SUCCESS")
            cursor.execute("SELECT COUNT(*) FROM votes")
            count = cursor.fetchone()[0]
            print(f"   Total votes in database: {count}")
        except IntegrityError as e:
            conn.rollback()
            print(f"   Result: ❌ BLOCKED - {e}")

        time.sleep(2)

        # Attempt 2 - THE MAGIC MOMENT
        print("\nAttempt 2: user123 votes for Python AGAIN")
        print("   ⚠️  Watch for the magic...")
        time.sleep(1)
        try:
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("user123", "Python")
            )
            conn.commit()
            print("   Result: ✅ SUCCESS (This shouldn't happen!)")
        except IntegrityError as e:
            conn.rollback()
            print("   Result: ❌ BLOCKED by UNIQUE constraint!")
            print(f"\n   🎯 MAGIC MOMENT!")
            print(f"   Real database caught the duplicate vote!")
            print(f"   Error: {str(e)[:100]}...")
            cursor.execute("SELECT COUNT(*) FROM votes")
            count = cursor.fetchone()[0]
            print(f"   Total votes in database: {count} (not 2!)")

        time.sleep(2)

        # Attempt 3
        print("\nAttempt 3: user123 votes for Python ONE MORE TIME")
        try:
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("user123", "Python")
            )
            conn.commit()
            print("   Result: ✅ SUCCESS")
        except IntegrityError:
            conn.rollback()
            print("   Result: ❌ BLOCKED again!")
            print("   Real constraints prevent ALL duplicates!")

        print("\n🎉 TEST RESULTS:")
        cursor.execute("SELECT COUNT(*) FROM votes")
        final_count = cursor.fetchone()[0]
        print(f"   • Total votes in database: {final_count}")
        print(f"   • Expected: 1 vote")
        print(f"   • Result: {'✅ CORRECT!' if final_count == 1 else '❌ FAILED'}")
        print("\n   ✨ TestContainers prevented 2 duplicate votes!")
        print("   ✨ In production: Same protection automatically!")

        cursor.close()
        conn.close()

        wait_for_user("Test complete! Press ENTER to see cleanup...")

        print("\n🧹 Cleaning up...")
        print("   Stopping container...")

    print("   ✅ Container stopped and removed automatically!")
    if ENVIRONMENT == 'codespaces':
        print("\n👀 CHECK YOUR DOCKER WATCH TERMINAL!")
        print("   The PostgreSQL container should be gone")
        print("   TestContainers cleaned up automatically!")
    else:
        print("\n👀 CHECK DOCKER DESKTOP AGAIN!")
        print("   The PostgreSQL container should be gone")
        print("   TestContainers cleaned up automatically!")

# ==============================================================================
# SECTION 3: SIDE-BY-SIDE COMPARISON
# ==============================================================================

def show_comparison():
    """Show side-by-side comparison"""

    print_header("SECTION 3: Side-by-Side Comparison",
                 "Mock vs TestContainers - The Clear Winner")

    print("\n" + "="*70)
    print("📊 COMPARISON TABLE")
    print("="*70)

    comparison = [
        ("Feature", "Mock Database", "TestContainers"),
        ("-"*20, "-"*22, "-"*22),
        ("Constraint Enforcement", "❌ None", "✅ Full"),
        ("Database Behavior", "❌ Simulated", "✅ Real"),
        ("Production Parity", "❌ No", "✅ Yes"),
        ("Catches Real Bugs", "❌ No", "✅ Yes"),
        ("Test Confidence", "⚠️  False", "✅ Real"),
        ("Setup Time", "✅ Fast", "✅ Fast (1-2s)"),
        ("Cleanup", "✅ Auto", "✅ Auto"),
        ("Learning Curve", "✅ Easy", "✅ Easy"),
    ]

    for row in comparison:
        print(f"{row[0]:<25} {row[1]:<25} {row[2]:<25}")

    print("\n" + "="*70)
    print("🏆 WINNER: TestContainers")
    print("="*70)

    print("\n✨ KEY TAKEAWAYS:")
    print("   1. Mocks can lie - they don't test real behavior")
    print("   2. TestContainers uses real databases with real constraints")
    print("   3. Containers start fast (1-2 seconds)")
    print("   4. Automatic cleanup - no manual work")
    print("   5. Production parity - tests behave like production")
    print("   6. Catches bugs mocks would miss")

# ==============================================================================
# SECTION 4: HANDS-ON EXERCISE
# ==============================================================================

def hands_on_exercise():
    """Interactive hands-on exercise"""

    print_header("SECTION 4: Your Turn - Hands-On Exercise",
                 "Practice what you learned with a real scenario")

    print("\n📝 EXERCISE: E-commerce Product Inventory")
    print("\nScenario:")
    print("   You're building an e-commerce system")
    print("   Products must have unique SKUs")
    print("   Write a test to verify SKU uniqueness")

    wait_for_user("Ready to try? Press ENTER...")

    print("\n💡 SOLUTION:")

    solution_code = """
def test_product_sku_uniqueness():
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg.connect(...)
        cursor = conn.cursor()

        # Create products table
        cursor.execute('''
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        ''')

        # Insert first product
        cursor.execute(
            "INSERT INTO products (sku, name, price) VALUES (%s, %s, %s)",
            ("LAPTOP-001", "MacBook Pro", 2499.99)
        )
        conn.commit()  # Should succeed

        # Try to insert duplicate SKU
        with pytest.raises(IntegrityError):
            cursor.execute(
                "INSERT INTO products (sku, name, price) VALUES (%s, %s, %s)",
                ("LAPTOP-001", "Dell XPS", 1999.99)  # Same SKU!
            )
            conn.commit()  # Should fail!
"""

    show_code("Test Product SKU Uniqueness", solution_code)

    print("\n🎯 What This Tests:")
    print("   ✅ UNIQUE constraint on SKU works")
    print("   ✅ Duplicate SKUs are prevented")
    print("   ✅ Same behavior as production database")

    wait_for_user("Want to run this exercise? Press ENTER...")

    print("\n🚀 Running exercise...")

    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE products (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
        """)

        print("\n✅ Table created")

        cursor.execute(
            "INSERT INTO products (sku, name, price) VALUES (%s, %s, %s)",
            ("LAPTOP-001", "MacBook Pro", 2499.99)
        )
        conn.commit()
        print("✅ First product inserted: LAPTOP-001")

        try:
            cursor.execute(
                "INSERT INTO products (sku, name, price) VALUES (%s, %s, %s)",
                ("LAPTOP-001", "Dell XPS", 1999.99)
            )
            conn.commit()
            print("❌ Duplicate SKU was allowed (BUG!)")
        except IntegrityError:
            conn.rollback()
            print("✅ Duplicate SKU blocked by UNIQUE constraint!")
            print("   🎯 Test passed! Constraint works correctly!")

        cursor.close()
        conn.close()

# ==============================================================================
# MAIN WORKSHOP FLOW
# ==============================================================================

def main():
    """Main workshop entry point"""

    print("\n" + "🧪" * 30)
    print("\n" + " " * 15 + "TestContainers Magic Workshop")
    print(" " * 15 + "Interactive Learning Experience")
    print("\n" + "🧪" * 30)

    print("\n📋 What We'll Cover:")
    print("   1. The Problem: How mocks can lie (5 min)")
    print("   2. The Magic: TestContainers in action (5 min)")
    print("   3. Comparison: Mock vs TestContainers (2 min)")
    print("   4. Hands-On: Practice exercise (3 min)")
    print("\n   Total Time: ~15 minutes")

    print("\n✅ Prerequisites Check:")
    print("   • Python 3.10+: ✅")
    if ENVIRONMENT == 'codespaces':
        print("   • Docker: ✅ (Available in Codespaces)")
        print("   • Environment: GitHub Codespaces 🚀")
    else:
        print("   • Docker Desktop: ⚠️  Make sure it's running!")
        print("   • Environment: Local Machine")
    print("   • TestContainers: ✅")

    wait_for_user("All set? Let's begin...")

    try:
        # Section 1: The Problem
        demo_mock_problem()

        # Section 2: The Magic
        demo_testcontainers_magic()

        # Section 3: Comparison
        show_comparison()

        # Section 4: Hands-On
        hands_on_exercise()

        # Final Summary
        print_header("🎉 Workshop Complete!", "You're now a TestContainers expert!")

        print("\n✨ What You Learned:")
        print("   ✅ Why mocks can give false confidence")
        print("   ✅ How TestContainers uses real containers")
        print("   ✅ How to catch bugs mocks would miss")
        print("   ✅ How to write production-parity tests")
        print("   ✅ Best practices for integration testing")

        print("\n🚀 Next Steps:")
        print("   1. Try TestContainers in your own projects")
        print("   2. Replace mocks with real database tests")
        print("   3. Test different database versions")
        print("   4. Explore other TestContainers (Redis, MongoDB, etc.)")

        print("\n📚 Resources:")
        print("   • TestContainers Docs: https://testcontainers-python.readthedocs.io/")
        print("   • This Workshop Code: scenario1-testcontainers/")
        print("   • Demo Files: demo.py, tests/")

        print("\n" + "🎯" * 30)
        print("\n   Thank you for participating!")
        print("   Questions? Email: vellankikoti@gmail.com")
        print("\n" + "🎯" * 30)

    except KeyboardInterrupt:
        print("\n\n⚠️  Workshop interrupted!")
        print("   Run again anytime: python workshop.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Check that Docker is running")
        print("   Run: docker ps")

if __name__ == "__main__":
    main()
