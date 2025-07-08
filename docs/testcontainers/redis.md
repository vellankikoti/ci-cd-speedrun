# Redis Container Testing

**Why Redis?**

✅ Essential for caching, sessions, and real-time data. Perfect for chaos testing in CI/CD pipelines.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check Redis Version

Verifies the container is running and accessible.

```python
client = redis.get_client()
info = client.info("server")
assert "redis_version" in info
```

---

### ✅ Test Case 2 — Set and Get

Tests basic key-value operations.

```python
client = redis.get_client()
client.set("name", "Alice")
value = client.get("name")
assert value == b"Alice"
```

---

### ✅ Test Case 3 — Multiple Operations

Tests multiple Redis operations.

```python
client = redis.get_client()
client.set("counter", 0)
client.incr("counter")
client.incr("counter")
value = client.get("counter")
assert value == b"2"
```

---

### ✅ Test Case 4 — Hash Operations

Tests Redis hash data structure.

```python
client = redis.get_client()
client.hset("user:1", "name", "Bob")
client.hset("user:1", "age", "25")
name = client.hget("user:1", "name")
age = client.hget("user:1", "age")
assert name == b"Bob"
assert age == b"25"
```

---

### ✅ Test Case 5 — Clean Up

Removes all keys and verifies cleanup.

```python
client = redis.get_client()
client.flushdb()
keys = client.keys("*")
assert len(keys) == 0
```

---

## ✅ How to Run the Tests

Run:

```bash
pytest -v testcontainers/test_redis_container.py
```

✅ Expected:

```
5 passed in X.XXs
```

---

## ✅ Useful Commands

* Check running containers:

  ```bash
  docker ps
  ```

* View Redis logs:

  ```bash
  docker logs <container_id>
  ```

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Connection Failures

```python
def test_redis_connection_failure():
    """Test that our app handles Redis connection failures gracefully"""
    with RedisContainer("redis:7-alpine") as redis:
        # Simulate connection failure
        redis.get_docker_client().stop(redis.get_container_id())
        
        # Verify our app handles the failure
        with pytest.raises(Exception):
            redis.get_client()
```

### ✅ Scenario 2: Memory Pressure

```python
def test_redis_memory_pressure():
    """Test that our app handles Redis memory constraints"""
    with RedisContainer("redis:7-alpine") as redis:
        client = redis.get_client()
        
        # Set memory limit
        client.config_set("maxmemory", "10mb")
        client.config_set("maxmemory-policy", "allkeys-lru")
        
        # Try to insert large dataset
        try:
            for i in range(1000):
                client.set(f"key{i}", "x" * 1000)
        except Exception as e:
            # Handle memory constraint gracefully
            assert "memory" in str(e).lower() or "OOM" in str(e)
```

---

## 📊 Monitoring & Reporting

### ✅ Generate HTML Report

```bash
pytest testcontainers/test_redis_container.py --html=reports/redis-test-report.html --self-contained-html
```

### ✅ View Container Logs

```bash
# Get container ID
docker ps | grep redis

# View logs
docker logs <container_id>
```

---

**Next:** [MySQL Testing](mysql.md) | [PostgreSQL Testing](postgres.md) | [MariaDB Testing](mariadb.md) | [MongoDB Testing](mongodb.md)

```

---
