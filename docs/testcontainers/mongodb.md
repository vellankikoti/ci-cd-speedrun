# MongoDB Container Testing

**Why MongoDB?**

✅ Perfect for document-based data, flexible schema, and modern web applications. Great for chaos testing in CI/CD pipelines.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check MongoDB Version

Verifies the container is running and accessible.

```python
client = mongo.get_connection_client()
db = client.admin
result = db.command("serverStatus")
assert "version" in result
```

---

### ✅ Test Case 2 — Insert and Query Document

Tests basic document insertion and retrieval.

```python
db = client.test_db
collection = db.users
result = collection.insert_one({"name": "Alice", "age": 30})
assert result.inserted_id is not None

doc = collection.find_one({"name": "Alice"})
assert doc["age"] == 30
```

---

### ✅ Test Case 3 — Insert Multiple Documents

Inserts multiple documents and confirms count.

```python
collection = db.users
docs = [{"name": "Bob"}, {"name": "Charlie"}]
result = collection.insert_many(docs)
assert len(result.inserted_ids) == 2

count = collection.count_documents({})
assert count == 3
```

---

### ✅ Test Case 4 — Update Document

Tests document update functionality.

```python
collection = db.users
collection.update_one({"name": "Alice"}, {"$set": {"age": 31}})
doc = collection.find_one({"name": "Alice"})
assert doc["age"] == 31
```

---

### ✅ Test Case 5 — Delete Documents

Removes documents and verifies deletion.

```python
collection = db.users
collection.delete_many({})
count = collection.count_documents({})
assert count == 0
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

* Check running containers:

  ```bash
  docker ps
  ```

* View MongoDB logs:

  ```bash
  docker logs <container_id>
  ```

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Connection Failures

```python
def test_mongodb_connection_failure():
    """Test that our app handles MongoDB connection failures gracefully"""
    with MongoDbContainer("mongo:6.0") as mongo:
        # Simulate connection failure
        mongo.get_docker_client().stop(mongo.get_container_id())
        
        # Verify our app handles the failure
        with pytest.raises(Exception):
            mongo.get_connection_client()
```

### ✅ Scenario 2: Large Document Handling

```python
def test_mongodb_large_document():
    """Test that our app handles large documents in MongoDB"""
    with MongoDbContainer("mongo:6.0") as mongo:
        client = mongo.get_connection_client()
        db = client.test_db
        collection = db.large_docs
        
        # Create large document
        large_doc = {"data": "x" * 10000, "id": 1}
        
        # Insert and verify
        result = collection.insert_one(large_doc)
        assert result.inserted_id is not None
        
        # Retrieve and verify
        doc = collection.find_one({"id": 1})
        assert len(doc["data"]) == 10000
```

---

## 📊 Monitoring & Reporting

### ✅ Generate HTML Report

```bash
pytest testcontainers/test_mongodb_container.py --html=reports/mongodb-test-report.html --self-contained-html
```

### ✅ View Container Logs

```bash
# Get container ID
docker ps | grep mongo

# View logs
docker logs <container_id>
```

---

**Next:** [MySQL Testing](mysql.md) | [PostgreSQL Testing](postgres.md) | [MariaDB Testing](mariadb.md) | [Redis Testing](redis.md)