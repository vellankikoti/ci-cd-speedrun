#!/usr/bin/env python3
"""
✅ THE TRUTH: Reality Tests with TestContainers
================================================

These tests face reality.
They're fast. They're green. They're REAL.

This is what happens when tests use production-parity infrastructure.
"""

import pytest
from testcontainers.postgres import PostgresContainer
import psycopg
from psycopg import IntegrityError


def test_single_vote_works():
    """✅ First vote succeeds with real database"""
    with PostgresContainer("postgres:15-alpine") as postgres:
        # Real connection to real PostgreSQL
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        cursor = conn.cursor()

        # Create table with UNIQUE constraint
        cursor.execute("""
            CREATE TABLE votes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                choice VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()

        # Insert first vote
        cursor.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            ("user123", "Python")
        )
        conn.commit()

        # Verify it worked
        cursor.execute("SELECT COUNT(*) FROM votes")
        count = cursor.fetchone()[0]
        assert count == 1

        cursor.close()
        conn.close()


def test_duplicate_vote_is_blocked():
    """
    🎯 THE MAGIC MOMENT: Duplicate vote is BLOCKED

    Unlike the fantasy test, this test uses a REAL database
    with REAL constraints. The second vote FAILS as it should.
    """
    with PostgresContainer("postgres:15-alpine") as postgres:
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        cursor = conn.cursor()

        # Create table with UNIQUE constraint
        cursor.execute("""
            CREATE TABLE votes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                choice VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()

        # First vote - succeeds
        cursor.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            ("user123", "Python")
        )
        conn.commit()

        # Second vote - BLOCKED by UNIQUE constraint
        with pytest.raises(IntegrityError):
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("user123", "Python")  # Same user!
            )
            conn.commit()

        # Verify only one vote exists
        conn.rollback()  # Clear the failed transaction
        cursor.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", ("user123",))
        count = cursor.fetchone()[0]
        assert count == 1  # Only one vote, as it should be!

        cursor.close()
        conn.close()


def test_multiple_duplicate_attempts_all_fail():
    """
    ✅ REALITY CHECK: ALL duplicate attempts fail

    This proves the constraint works consistently.
    In production, users cannot vote multiple times.
    """
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
            CREATE TABLE votes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                choice VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()

        user_id = "user123"

        # First vote - succeeds
        cursor.execute(
            "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
            (user_id, "Python")
        )
        conn.commit()

        # Try to vote 10 more times - ALL FAIL
        for i in range(10):
            with pytest.raises(IntegrityError):
                cursor.execute(
                    "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                    (user_id, f"Choice{i}")
                )
                conn.commit()
            conn.rollback()

        # Verify still only one vote
        cursor.execute("SELECT COUNT(*) FROM votes WHERE user_id = %s", (user_id,))
        count = cursor.fetchone()[0]
        assert count == 1  # Still just one vote!

        cursor.close()
        conn.close()


def test_different_users_can_vote():
    """
    ✅ POSITIVE TEST: Different users CAN vote

    This proves the constraint allows valid votes
    while blocking invalid ones.
    """
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
            CREATE TABLE votes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                choice VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()

        # Three different users vote
        users = ["alice", "bob", "charlie"]
        for user in users:
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                (user, "Python")
            )
            conn.commit()

        # Verify all three votes recorded
        cursor.execute("SELECT COUNT(*) FROM votes")
        count = cursor.fetchone()[0]
        assert count == 3

        # But if any user tries again - BLOCKED
        with pytest.raises(IntegrityError):
            cursor.execute(
                "INSERT INTO votes (user_id, choice) VALUES (%s, %s)",
                ("alice", "JavaScript")  # Alice already voted!
            )
            conn.commit()

        cursor.close()
        conn.close()


# ==============================================================================
# THE SOLUTION IN SUMMARY
# ==============================================================================

"""
These tests provide REAL CONFIDENCE:

1. Fast: ✅ (1-2 seconds per test)
2. Green: ✅ (pass when correct, fail when wrong)
3. Correct: ✅ (tests real behavior!)

Why they work in production:
- Real database constraints (UNIQUE, FOREIGN KEY, CHECK)
- Real connection behavior
- Real transaction handling
- Production parity

The difference:
- Fantasy tests: Fast green lies
- Reality tests: Fast green truth

TestContainers makes this possible:
- Spin up real PostgreSQL in 1-2 seconds
- Isolated test environment (no shared state)
- Automatic cleanup (no manual work)
- Same database engine as production

Run both test suites:
  Fantasy: `pytest tests/test_fantasy.py -v`  (lies)
  Reality: `pytest tests/test_reality.py -v`  (truth)

Compare the results and see which one you trust.
"""
