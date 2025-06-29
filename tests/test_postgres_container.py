from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
import sqlalchemy
import pytest


@pytest.fixture(scope="module")
def pg_engine():
    """
    Fixture to spin up a Postgres container and create the `users` table.

    This guarantees that:
    - the container starts only once for all tests in this file
    - the `users` table exists before any test runs
    """
    with PostgresContainer("postgres:15") as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as conn:
            # Create the table once and commit
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT
                );
            """))
            conn.commit()

        yield engine

        engine.dispose()


@pytest.fixture(autouse=True)
def truncate_users_table(pg_engine):
    """
    Automatically truncate the users table before every test.

    This ensures tests do not interfere with each other.
    """
    with pg_engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE users;"))
        conn.commit()


def test_postgres_version(pg_engine):
    """
    ✅ Test Case 1 - Check Postgres version

    Confirms that the Postgres container is running and responding
    by querying its version string.
    """
    with pg_engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        assert "PostgreSQL" in version


def test_insert_and_query(pg_engine):
    """
    ✅ Test Case 2 - Insert and Query One Row

    Demonstrates inserting a single row into the users table and
    reading it back successfully.
    """
    with pg_engine.connect() as conn:
        conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
        conn.commit()

        result = conn.execute(text("SELECT name FROM users WHERE name='Alice';"))
        row = result.fetchone()
        assert row[0] == "Alice"


def test_multiple_row_inserts(pg_engine):
    """
    ✅ Test Case 3 - Insert Multiple Rows and Count

    Inserts multiple rows and verifies that the row count matches
    the expected number.
    """
    with pg_engine.connect() as conn:
        conn.execute(
            text("INSERT INTO users (name) VALUES ('Bob'), ('Charlie');")
        )
        conn.commit()

        result = conn.execute(text("SELECT COUNT(*) FROM users;"))
        count = result.scalar()
        assert count == 2


def test_primary_key_constraint(pg_engine):
    """
    ✅ Test Case 4 - Test Primary Key Constraint

    Tries inserting duplicate primary key values to demonstrate
    how database constraints protect data integrity.
    """
    with pg_engine.connect() as conn:
        conn.execute(text("INSERT INTO users (id, name) VALUES (10, 'David');"))
        conn.commit()

    with pg_engine.connect() as conn:
        with pytest.raises(sqlalchemy.exc.IntegrityError) as excinfo:
            conn.execute(text("INSERT INTO users (id, name) VALUES (10, 'Eve');"))
            conn.commit()

        assert "duplicate key value" in str(excinfo.value)


def test_table_empty_after_truncate(pg_engine):
    """
    ✅ Test Case 5 - Verify Table Empty After Truncate

    Confirms that the users table is empty at the start of a test,
    demonstrating good test isolation for CI/CD.
    """
    with pg_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users;"))
        count = result.scalar()
        assert count == 0
