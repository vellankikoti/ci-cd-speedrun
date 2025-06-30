import psycopg2
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer
import pytest

def test_postgres_connection_fail():
    with PostgresContainer("postgres:15").with_bind_ports(5432, 5432) as postgres:
        url = postgres.get_connection_url().replace("postgresql+psycopg2", "postgresql")
        parsed = urlparse(url)

        # Intentionally wrong password
        with pytest.raises(psycopg2.OperationalError):
            psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password="wrong_password",
                dbname=parsed.path.lstrip("/"),
            )
