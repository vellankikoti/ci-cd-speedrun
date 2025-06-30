import redis
import pytest
from testcontainers.redis import RedisContainer

def test_connect_redis_container():
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        client = redis.Redis(
            host=host,
            port=int(port),
            db=0
        )
        pong = client.ping()
        assert pong is True
