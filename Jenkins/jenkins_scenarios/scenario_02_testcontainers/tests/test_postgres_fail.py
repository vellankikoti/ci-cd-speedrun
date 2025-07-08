import pytest
import psycopg2
from psycopg2 import OperationalError
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer

def test_postgres_container_failure():
    with PostgresContainer("postgres:15").with_bind_ports(5432, 5432) as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql"
        )
        parsed = urlparse(url)

        wrong_password = "wrongpass"

        with pytest.raises(OperationalError):
            psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=wrong_password,
                dbname=parsed.path.lstrip("/"),
            )
