import time
import random
from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text
import sqlalchemy
import pytest

# Emojis for logs
CHECK = "✅"
CROSS = "❌"
BOLT = "⚡"
CHAOS = "💥"
SPARKLES = "✨"

# Colors for terminal logs
def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

GREEN = "32"
RED = "31"
YELLOW = "33"
BLUE = "34"

def log_info(msg):
    print(colorize(f"{SPARKLES} {msg}", BLUE))

def log_success(msg):
    print(colorize(f"{CHECK} {msg}", GREEN))

def log_warning(msg):
    print(colorize(f"{CHAOS} {msg}", YELLOW))

def log_error(msg):
    print(colorize(f"{CROSS} {msg}", RED))

def chaos_delay():
    """
    Randomly adds a few seconds of delay to simulate chaos.
    Great for workshop impact to show real-world slowness!
    """
    if random.choice([True, False]):
        delay = random.randint(2, 5)
        log_warning(f"Chaos delay introduced... sleeping {delay} seconds.")
        time.sleep(delay)

def get_engine(container):
    url = container.get_connection_url()
    url = url.replace("mysql://", "mysql+pymysql://")
    engine = create_engine(url, echo=False, future=True)
    return engine

def test_mariadb_version():
    """
    ✅ Test Case 1 - Check MariaDB version
    """
    log_info("🚀 Starting test: Check MariaDB version")

    chaos_delay()

    with MySqlContainer("mariadb:11.1") as mariadb:
        engine = get_engine(mariadb)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            log_info(f"MariaDB Version fetched: {version}")
            assert "MariaDB" in version

    log_success("MariaDB version test passed!")

def test_insert_and_query():
    """
    ✅ Test Case 2 - Insert and Query One Row
    """
    log_info("🚀 Starting test: Insert and Query One Row")

    chaos_delay()

    with MySqlContainer("mariadb:11.1") as mariadb:
        engine = get_engine(mariadb)

        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                );
            """))
            conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
            result = conn.execute(text("SELECT name FROM users WHERE name='Alice';"))
            row = result.fetchone()
            log_info(f"Queried name: {row[0]}")
            assert row[0] == "Alice"

    log_success("Insert and Query One Row test passed!")

def test_multiple_rows():
    """
    ✅ Test Case 3 - Insert Multiple Rows and Count
    """
    log_info("🚀 Starting test: Insert Multiple Rows and Count")

    chaos_delay()

    with MySqlContainer("mariadb:11.1") as mariadb:
        engine = get_engine(mariadb)

        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                );
            """))
            conn.execute(text("""
                INSERT INTO users (name) VALUES
                    ('Bob'), ('Charlie');
            """))
            result = conn.execute(text("SELECT COUNT(*) FROM users;"))
            count = result.scalar()
            log_info(f"Total rows in table: {count}")
            assert count == 2

    log_success("Insert Multiple Rows and Count test passed!")

def test_primary_key_constraint():
    """
    ✅ Test Case 4 - Primary Key constraint
    """
    log_info("🚀 Starting test: Primary Key constraint violation")

    chaos_delay()

    with MySqlContainer("mariadb:11.1") as mariadb:
        engine = get_engine(mariadb)

        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY,
                    name VARCHAR(255)
                );
            """))
            conn.execute(text("""
                INSERT INTO users (id, name) VALUES (10, 'David');
            """))
            log_info("Inserted first row with id=10.")
            
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                conn.execute(text("""
                    INSERT INTO users (id, name) VALUES (10, 'Eve');
                """))
                log_error("This insert should fail due to primary key constraint.")

    log_success("Primary Key constraint test passed!")

def test_empty_table_after_truncate():
    """
    ✅ Test Case 5 - Table empty after TRUNCATE
    """
    log_info("🚀 Starting test: Table empty after TRUNCATE")

    chaos_delay()

    with MySqlContainer("mariadb:11.1") as mariadb:
        engine = get_engine(mariadb)

        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                );
            """))
            conn.execute(text("""
                INSERT INTO users (name) VALUES ('Alice');
            """))
            conn.execute(text("TRUNCATE TABLE users;"))
            result = conn.execute(text("SELECT COUNT(*) FROM users;"))
            count = result.scalar()
            log_info(f"Rows after TRUNCATE: {count}")
            assert count == 0

    log_success("Table empty after TRUNCATE test passed!")
