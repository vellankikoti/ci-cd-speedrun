import pytest
import random
import time
from testcontainers.redis import RedisContainer
import redis

# Colors for logs
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def chaos_delay(max_seconds=3):
    """
    Introduce random delays to simulate chaos and variability in test timings.
    """
    delay = random.randint(0, max_seconds)
    if delay > 0:
        print(f"{YELLOW}💥 Chaos delay: sleeping {delay} seconds...{RESET}")
        time.sleep(delay)


@pytest.fixture(scope="module")
def redis_client():
    """
    Fixture to spin up a Redis container for all tests in the module.
    """
    print(f"{CYAN}🔌 Starting Redis container...{RESET}")
    chaos_delay()

    with RedisContainer("redis:7.2") as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)
        client = redis.StrictRedis(
            host=host,
            port=int(port),
            decode_responses=False
        )
        print(f"{GREEN}✅ Connected to Redis at {host}:{port}{RESET}")
        yield client

    print(f"{GREEN}✅ Redis container stopped.{RESET}")


@pytest.fixture(autouse=True)
def flush_db(redis_client):
    """
    Flush the Redis DB before each test to ensure test isolation.
    """
    redis_client.flushall()
    print(f"{CYAN}🧹 Redis DB flushed before test.{RESET}")
    chaos_delay()


def test_redis_ping(redis_client):
    """
    ✅ Test Case 1 - Basic PING command
    """
    print(f"{CYAN}🚀 Running: test_redis_ping{RESET}")
    assert redis_client.ping() is True
    print(f"{GREEN}✅ Redis responded to PING successfully!{RESET}")


def test_set_and_get(redis_client):
    """
    ✅ Test Case 2 - SET and GET a key
    """
    print(f"{CYAN}🚀 Running: test_set_and_get{RESET}")
    redis_client.set("key", "value")
    value = redis_client.get("key")
    print(f"{GREEN}✅ Retrieved value for key: {value}{RESET}")
    assert value == b"value"


def test_increment_key(redis_client):
    """
    ✅ Test Case 3 - Increment a key
    """
    print(f"{CYAN}🚀 Running: test_increment_key{RESET}")
    redis_client.set("counter", 5)
    redis_client.incr("counter")
    result = redis_client.get("counter")
    print(f"{GREEN}✅ Counter value after increment: {result}{RESET}")
    assert int(result) == 6


def test_delete_key(redis_client):
    """
    ✅ Test Case 4 - Delete a key
    """
    print(f"{CYAN}🚀 Running: test_delete_key{RESET}")
    redis_client.set("temp", "data")
    redis_client.delete("temp")
    result = redis_client.get("temp")
    print(f"{GREEN}✅ Deleted key check: result={result}{RESET}")
    assert result is None


def test_key_expiration(redis_client):
    """
    ✅ Test Case 5 - Key expires after TTL
    """
    print(f"{CYAN}🚀 Running: test_key_expiration{RESET}")
    redis_client.setex("session", 2, "active")
    value = redis_client.get("session")
    print(f"{GREEN}✅ Value immediately after set: {value}{RESET}")
    assert value == b"active"

    print(f"{YELLOW}⏳ Waiting for key to expire...{RESET}")
    time.sleep(3)

    value_after_expiry = redis_client.get("session")
    print(f"{GREEN}✅ Value after expiry check: {value_after_expiry}{RESET}")
    assert value_after_expiry is None
