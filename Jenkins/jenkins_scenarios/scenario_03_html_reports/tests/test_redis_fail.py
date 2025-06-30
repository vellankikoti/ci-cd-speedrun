import redis
import pytest
from testcontainers.redis import RedisContainer

def test_redis_connection_fail():
    with RedisContainer("redis:7.0.5").with_bind_ports(6379, 6379) as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        # Intentionally wrong port
        bad_port = int(port) + 100

        client = redis.StrictRedis(host=host, port=bad_port, decode_responses=True)

        with pytest.raises(redis.ConnectionError):
            client.get("chaos_key")
