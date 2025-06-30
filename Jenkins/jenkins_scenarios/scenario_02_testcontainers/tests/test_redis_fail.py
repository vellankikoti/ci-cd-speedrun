import pytest
import redis
from redis.exceptions import ConnectionError
from testcontainers.redis import RedisContainer

def test_redis_container_failure():
    with RedisContainer("redis:7.0.5").with_bind_ports(6379, 6379) as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        # intentionally break the port
        bad_port = int(port) + 999

        client = redis.StrictRedis(host=host, port=bad_port, decode_responses=True)

        with pytest.raises(ConnectionError):
            client.get("mykey")
