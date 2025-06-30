import psycopg2
from testcontainers.postgres import PostgresContainer

def test_postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=PostgresContainer.USER,
            password=PostgresContainer.PASSWORD,
            database=PostgresContainer.DB
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Postgres version: {version}")
        assert version is not None
