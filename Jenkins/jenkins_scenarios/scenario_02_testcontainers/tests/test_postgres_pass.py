import psycopg2
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer

def test_postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        url = postgres.get_connection_url()

        # Remove the +psycopg2 driver name
        url = url.replace("postgresql+psycopg2", "postgresql")

        parsed = urlparse(url)

        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            user=parsed.username,
            password=parsed.password,
            dbname=parsed.path.lstrip("/"),
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version}")
        assert version is not None
