import pytest
import psycopg2
from psycopg2 import OperationalError
from testcontainers.postgres import PostgresContainer

def test_postgres_container_failure():
    with PostgresContainer("postgres:15") as postgres:
        # Get the correct connection URL
        connection_url = postgres.get_connection_url()

        # Tamper the URL to simulate failure
        wrong_url = connection_url.replace("test:test", "test:wrongpassword")

        with pytest.raises(OperationalError):
            psycopg2.connect(wrong_url)
