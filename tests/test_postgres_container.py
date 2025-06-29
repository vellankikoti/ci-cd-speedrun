import pytest
import random
import time
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
import sqlalchemy

# Colors for logs
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def chaos_delay(max_seconds=3):
    """
    Introduce random delays to simulate chaos and variability in test timings.
    """
    delay = random.randint(0, max_seconds)
    if delay > 0:
        print(f"{YELLOW}💥 Chaos delay: sleeping {delay} seconds...{RESET}")
        time.sleep(delay)


@pytest.fixture(scope="module")
def pg_engine():
    """
    Fixture to spin up a Postgres container and create the `users` table.

    Starts once per test module for performance.
    """
    print(f"{CYAN}🔌 Starting Postgres container for test suite...{RESET}")
    chaos_delay()

    with PostgresContainer("postgres:15") as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as conn:
            print(f"{CYAN}⚙️  Creating users table...{RESET}")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT
                );
            """))
            conn.commit()

        yield engine

        engine.dispose()

    print(f"{GREEN}✅ Postgres container stopped.{RESET}")


@pytest.fixture(autouse=True)
def truncate_users_table(pg_engine):
    """
    Automatically truncate users table before each test.
    Ensures test isolation.
    """
    with pg_engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE users;"))
        conn.commit()
    print(f"{CYAN}🧹 Users table truncated before test.{RESET}")
    chaos_delay()


def test_postgres_version(pg_engine):
    """
    ✅ Test Case 1 - Check Postgres version
    """
    print(f"{CYAN}🚀 Running: test_postgres_version{RESET}")
    with pg_engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"{GREEN}✅ Postgres Version: {version}{RESET}")
        assert "PostgreSQL" in version


def test_insert_and_query(pg_engine):
    """
    ✅ Test Case 2 - Insert and Query One Row
    """
    print(f"{CYAN}🚀 Running: test_insert_and_query{RESET}")
    with pg_engine.connect() as conn:
        conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
        conn.commit()

        result = conn.execute(text("SELECT name FROM users WHERE name='Alice';"))
        row = result.fetchone()
        print(f"{GREEN}✅ Fetched row: {row}{RESET}")
        assert row[0] == "Alice"


def test_multiple_row_inserts(pg_engine):
    """
    ✅ Test Case 3 - Insert Multiple Rows and Count
    """
    print(f"{CYAN}🚀 Running: test_multiple_row_inserts{RESET}")
    with pg_engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (name) VALUES
                ('Bob'), ('Charlie');
        """))
        conn.commit()

        result = conn.execute(text("SELECT COUNT(*) FROM users;"))
        count = result.scalar()
        print(f"{GREEN}✅ Row count after insert: {count}{RESET}")
        assert count == 2


def test_primary_key_constraint(pg_engine):
    """
    ✅ Test Case 4 - Test Primary Key Constraint
    """
    print(f"{CYAN}🚀 Running: test_primary_key_constraint{RESET}")
    with pg_engine.connect() as conn:
        conn.execute(text("INSERT INTO users (id, name) VALUES (10, 'David');"))
        conn.commit()

    with pg_engine.connect() as conn:
        with pytest.raises(sqlalchemy.exc.IntegrityError) as excinfo:
            conn.execute(text("INSERT INTO users (id, name) VALUES (10, 'Eve');"))
            conn.commit()

        print(f"{GREEN}✅ Caught integrity error: {excinfo.value}{RESET}")
        assert "duplicate key value" in str(excinfo.value)


def test_table_empty_after_truncate(pg_engine):
    """
    ✅ Test Case 5 - Verify Table Empty After Truncate
    """
    print(f"{CYAN}🚀 Running: test_table_empty_after_truncate{RESET}")
    with pg_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users;"))
        count = result.scalar()
        print(f"{GREEN}✅ Users table row count is {count}{RESET}")
        assert count == 0
