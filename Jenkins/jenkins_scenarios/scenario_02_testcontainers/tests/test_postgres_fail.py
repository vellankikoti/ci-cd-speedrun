import pytest
import psycopg2
from psycopg2 import OperationalError
from testcontainers.postgres import PostgresContainer

def test_postgres_container_failure():
    with PostgresContainer("postgres:15") as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql"
        )
        # Tamper credentials to force a failure
        broken_url = url.replace("test:test", "test:wrongpass")

        with pytest.raises(OperationalError):
            psycopg2.connect(broken_url)
