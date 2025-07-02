# PostgreSQL Container Testing

**Why PostgreSQL?**

✅ It’s robust, widely used in production, and perfect for chaos testing in CI/CD pipelines.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check PostgreSQL Version

Runs a basic query to confirm the DB is alive.

```python
result = conn.execute(text("SELECT version();")).fetchone()
assert "PostgreSQL" in result[0]
````

---

### ✅ Test Case 2 — Insert and Query

Inserts a single record and verifies retrieval.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
result = conn.execute(text("SELECT name FROM users;")).fetchone()
assert result[0] == "Alice"
```

---

### ✅ Test Case 3 — Insert Multiple Rows

Inserts multiple records and checks row count.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Bob'), ('Charlie');"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 3
```

---

### ✅ Test Case 4 — Primary Key Constraint

Verifies that primary key constraints work properly.

```python
conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'David');"))
with pytest.raises(Exception):
    conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Eve');"))
```

---

### ✅ Test Case 5 — Truncate Table

Clears the table and ensures it’s empty.

```python
conn.execute(text("TRUNCATE users;"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 0
```

---

## ✅ How to Run the Tests

Run:

```bash
pytest -v tests/test_postgres_container.py
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

* View logs for the Postgres container:

  ```bash
  docker logs <container_id>
  ```

---
