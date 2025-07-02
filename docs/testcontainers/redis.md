# Redis Container Testing

**Why Redis?**

✅ Redis is a blazing-fast in-memory key-value store, ideal for testing ephemeral data and chaos scenarios in CI/CD pipelines.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — PING Command

Checks basic connectivity to Redis.

```python
assert client.ping() is True
````

---

### ✅ Test Case 2 — Set and Get a Key

Stores a value and retrieves it.

```python
client.set("key", "value")
val = client.get("key")
assert val == b"value"
```

---

### ✅ Test Case 3 — Increment a Key

Demonstrates atomic increment operations.

```python
client.set("counter", 5)
client.incr("counter")
result = client.get("counter")
assert int(result) == 6
```

---

### ✅ Test Case 4 — Delete a Key

Deletes a key and ensures it’s gone.

```python
client.set("temp", "data")
client.delete("temp")
val = client.get("temp")
assert val is None
```

---

### ✅ Test Case 5 — Key Expiration (TTL)

Sets a key with an expiration time and confirms it disappears.

```python
client.setex("session", 2, "active")
value = client.get("session")
assert value == b"active"

import time
time.sleep(3)

value_after_expiry = client.get("session")
assert value_after_expiry is None
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

* Inspect Redis logs:

  ```bash
  docker logs <container_id>
  ```

---

**Redis is perfect for lightning-fast chaos tests in your CI/CD pipelines.**

```

---
