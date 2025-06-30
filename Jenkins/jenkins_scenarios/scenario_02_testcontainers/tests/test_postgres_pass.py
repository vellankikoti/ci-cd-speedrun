import psycopg2
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer

def test_postgres_container():
    # Force container port binding to localhost for Jenkins pipeline
    with PostgresContainer("postgres:15").with_bind_ports(5432, 5432) as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql"
        )
        parsed = urlparse(url)

        print("=== URL:", url)
        print("Host:", parsed.hostname)
        print("Port:", parsed.port)
        print("User:", parsed.username)
        print("Password:", parsed.password)
        print("DB Name:", parsed.path.lstrip("/"))

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
