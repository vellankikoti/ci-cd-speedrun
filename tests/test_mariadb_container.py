from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text
import sqlalchemy
import pytest


def test_mariadb_version():
    """
    ✅ Test Case 1 - Check MariaDB version
    """
    with MySqlContainer("mariadb:11.1") as mariadb:
        url = mariadb.get_connection_url()
        url = url.replace("mysql://", "mysql+pymysql://")

        engine = create_engine(url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print("MariaDB Version:", version)
            assert "MariaDB" in version


def test_insert_and_query():
    """
    ✅ Test Case 2 - Insert and Query One Row
    """
    with MySqlContainer("mariadb:11.1") as mariadb:
        url = mariadb.get_connection_url()
        url = url.replace("mysql://", "mysql+pymysql://")

        engine = create_engine(url)

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


def test_multiple_rows():
    """
    ✅ Test Case 3 - Insert Multiple Rows and Count
    """
    with MySqlContainer("mariadb:11.1") as mariadb:
        url = mariadb.get_connection_url()
        url = url.replace("mysql://", "mysql+pymysql://")

        engine = create_engine(url)

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
            assert count == 2


def test_primary_key_constraint():
    """
    ✅ Test Case 4 - Primary Key constraint
    """
    with MySqlContainer("mariadb:11.1") as mariadb:
        url = mariadb.get_connection_url()
        url = url.replace("mysql://", "mysql+pymysql://")

        engine = create_engine(url)

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


def test_empty_table_after_truncate():
    """
    ✅ Test Case 5 - Table empty after TRUNCATE
    """
    with MySqlContainer("mariadb:11.1") as mariadb:
        url = mariadb.get_connection_url()
        url = url.replace("mysql://", "mysql+pymysql://")

        engine = create_engine(url)

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
            assert count == 0
