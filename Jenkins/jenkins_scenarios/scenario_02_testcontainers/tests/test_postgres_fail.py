import psycopg2
import pytest
from psycopg2 import OperationalError
from testcontainers.postgres import PostgresContainer

def test_postgres_container_failure():
    with PostgresContainer("postgres:15") as postgres:
        # Intentionally break credentials
        wrong_password = "wrongpass"

        with pytest.raises(OperationalError):
            conn = psycopg2.connect(
                host=postgres.get_container_host_ip(),
                port=postgres.get_exposed_port(5432),
                user=PostgresContainer.USER,
                password=wrong_password,
                database=PostgresContainer.DB
            )
            conn.close()
