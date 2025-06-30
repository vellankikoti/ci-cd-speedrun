import os
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

def test_postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        conn = psycopg2.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.USER,
            password=postgres.PASSWORD,
            database=postgres.DB
        )
        cur = conn.cursor()
        cur.execute("SELECT version()")
        result = cur.fetchone()
        assert "PostgreSQL" in result[0]
