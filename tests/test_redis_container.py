import pytest
from testcontainers.redis import RedisContainer
import redis
import time


def test_redis_ping():
    """
    ✅ Test Case 1 - Basic PING command
    """
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(host=host, port=int(port), decode_responses=False)
        assert client.ping() is True


def test_set_and_get():
    """
    ✅ Test Case 2 - SET and GET a key
    """
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(host=host, port=int(port), decode_responses=False)
        client.set("key", "value")
        value = client.get("key")
        assert value == b"value"


def test_increment_key():
    """
    ✅ Test Case 3 - Increment a key
    """
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(host=host, port=int(port), decode_responses=False)
        client.set("counter", 5)
        client.incr("counter")
        result = client.get("counter")
        assert int(result) == 6


def test_delete_key():
    """
    ✅ Test Case 4 - Delete a key
    """
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(host=host, port=int(port), decode_responses=False)
        client.set("temp", "data")
        client.delete("temp")
        result = client.get("temp")
        assert result is None


def test_key_expiration():
    """
    ✅ Test Case 5 - Key expires after TTL
    """
    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(host=host, port=int(port), decode_responses=False)
        client.setex("session", 2, "active")
        value = client.get("session")
        assert value == b"active"

        time.sleep(3)
        value_after_expiry = client.get("session")
        assert value_after_expiry is None
