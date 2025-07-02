import pytest
import random
import time
from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text
import sqlalchemy

# Colors for log output
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def chaos_delay(max_seconds=3):
    """
    Introduce a random delay to simulate chaos in test execution.
    """
    delay = random.randint(0, max_seconds)
    if delay > 0:
        print(f"{YELLOW}💥 Chaos delay introduced... sleeping {delay} seconds.{RESET}")
        time.sleep(delay)

def get_mysql_engine():
    """
    Start a MySQL container and return SQLAlchemy engine.
    """
    mysql = MySqlContainer("mysql:8.0") \
        .with_command("--default-authentication-plugin=mysql_native_password") \
        .with_env("MYSQL_ROOT_PASSWORD", "test")

    mysql.start()

    url = mysql.get_connection_url().replace("mysql://", "mysql+pymysql://")
    engine = create_engine(url)

    return mysql, engine


def test_mysql_version():
    """
    ✅ Test Case 1 - Check MySQL version
    """
    print(f"{CYAN}✨ 🚀 Starting test: Check MySQL Version{RESET}")
    chaos_delay()

    mysql, engine = get_mysql_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"{GREEN}✅ MySQL Version: {version}{RESET}")
            assert "8.0" in version
    finally:
        mysql.stop()

    print(f"{GREEN}✅ MySQL Version test passed!{RESET}\n")


def test_insert_and_query():
    """
    ✅ Test Case 2 - Insert and Query One Row
    """
    print(f"{CYAN}✨ 🚀 Starting test: Insert and Query One Row{RESET}")
    chaos_delay()

    mysql, engine = get_mysql_engine()
    try:
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
            assert row[0] == "Alice"
            print(f"{GREEN}✅ Successfully inserted and queried Alice!{RESET}")
    finally:
        mysql.stop()

    print(f"{GREEN}✅ Insert and Query test passed!{RESET}\n")


def test_multiple_rows():
    """
    ✅ Test Case 3 - Insert Multiple Rows and Count
    """
    print(f"{CYAN}✨ 🚀 Starting test: Insert Multiple Rows and Count{RESET}")
    chaos_delay()

    mysql, engine = get_mysql_engine()
    try:
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
            print(f"{GREEN}✅ Total rows in users table: {count}{RESET}")
            assert count == 2
    finally:
        mysql.stop()

    print(f"{GREEN}✅ Multiple Rows test passed!{RESET}\n")


def test_primary_key_constraint():
    """
    ✅ Test Case 4 - Primary Key constraint
    """
    print(f"{CYAN}✨ 🚀 Starting test: Primary Key Constraint{RESET}")
    chaos_delay()

    mysql, engine = get_mysql_engine()
    try:
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
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                conn.execute(text("""
                    INSERT INTO users (id, name) VALUES (10, 'Eve');
                """))
            print(f"{GREEN}✅ Primary key constraint triggered as expected!{RESET}")
    finally:
        mysql.stop()

    print(f"{GREEN}✅ Primary Key Constraint test passed!{RESET}\n")


def test_empty_table_after_truncate():
    """
    ✅ Test Case 5 - Table empty after TRUNCATE
    """
    print(f"{CYAN}✨ 🚀 Starting test: Table empty after TRUNCATE{RESET}")
    chaos_delay()

    mysql, engine = get_mysql_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                );
            """))
            conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
            conn.execute(text("TRUNCATE TABLE users;"))
            result = conn.execute(text("SELECT COUNT(*) FROM users;"))
            count = result.scalar()
            assert count == 0
            print(f"{GREEN}✅ Table successfully truncated. Row count: {count}{RESET}")
    finally:
        mysql.stop()

    print(f"{GREEN}✅ TRUNCATE test passed!{RESET}\n")
