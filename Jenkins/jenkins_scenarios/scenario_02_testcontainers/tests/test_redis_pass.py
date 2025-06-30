import redis
from testcontainers.redis import RedisContainer

def test_redis_container():
    with RedisContainer("redis:7.0.5").with_bind_ports(6379, 6379) as redis_container:
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        print(f"Redis running on {host}:{port}")

        client = redis.StrictRedis(host=host, port=int(port), decode_responses=True)
        client.set("mykey", "myvalue")
        value = client.get("mykey")

        print("Redis GET mykey:", value)
        assert value == "myvalue"
