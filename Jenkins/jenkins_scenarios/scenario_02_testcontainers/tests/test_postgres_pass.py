from testcontainers.postgres import PostgresContainer
import psycopg2

def test_postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        # Fix URL for psycopg2
        connection_url = postgres.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql"
        )
        conn = psycopg2.connect(connection_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version}")
        assert version is not None
