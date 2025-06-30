import redis
import pytest

def test_connect_real_redis():
    client = redis.Redis(
        host="localhost",
        port=6379,
        db=0
    )
    pong = client.ping()
    assert pong is True
