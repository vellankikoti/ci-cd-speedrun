# MongoDB Container Testing

**Why MongoDB?**

✅ MongoDB is a leading NoSQL database. It’s widely used in modern applications and a great candidate for chaos testing in containerized pipelines.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check MongoDB Version

Verifies the container is running the expected version.

```python
version = client.server_info()["version"]
assert version.startswith("7.")
````

---

### ✅ Test Case 2 — Insert and Find Document

Inserts a single document and retrieves it.

```python
db.users.insert_one({"name": "Alice"})
result = db.users.find_one({"name": "Alice"})
assert result["name"] == "Alice"
```

---

### ✅ Test Case 3 — Insert Multiple Documents

Inserts multiple documents and counts them.

```python
db.users.insert_many([{"name": "Bob"}, {"name": "Charlie"}])
count = db.users.count_documents({})
assert count == 2
```

---

### ✅ Test Case 4 — Update a Document

Updates a document’s field.

```python
db.users.insert_one({"name": "David"})
db.users.update_one({"name": "David"}, {"$set": {"name": "Daniel"}})
result = db.users.find_one({"name": "Daniel"})
assert result is not None
```

---

### ✅ Test Case 5 — Delete a Document

Deletes a document and confirms it’s gone.

```python
db.users.insert_one({"name": "Eve"})
db.users.delete_one({"name": "Eve"})
result = db.users.find_one({"name": "Eve"})
assert result is None
```

---

## ✅ How to Run the Tests

Run:

```bash
pytest -v testcontainers/test_mongodb_container.py
```

✅ Expected:

```
5 passed in X.XXs
```

---

## ✅ Useful Commands

* List running containers:

  ```bash
  docker ps
  ```

* Inspect MongoDB logs:

  ```bash
  docker logs <container_id>
  ```

---