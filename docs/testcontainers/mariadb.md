# MariaDB Container Testing

**Why MariaDB?**

✅ MariaDB is a drop-in replacement for MySQL with open-source community support, making it perfect for containerized tests in CI/CD.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check MariaDB Version

Verifies the container is running and accessible.

```python
result = conn.execute(text("SELECT VERSION();")).fetchone()
assert "MariaDB" in result[0]
````

---

### ✅ Test Case 2 — Insert and Query

Tests simple INSERT and SELECT functionality.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
result = conn.execute(text("SELECT name FROM users;")).fetchone()
assert result[0] == "Alice"
```

---

### ✅ Test Case 3 — Insert Multiple Rows

Inserts multiple rows and confirms row count.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Bob'), ('Charlie');"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 3
```

---

### ✅ Test Case 4 — Primary Key Constraint

Tests primary key uniqueness.

```python
conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'David');"))
with pytest.raises(Exception):
    conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Eve');"))
```

---

### ✅ Test Case 5 — Truncate Table

Clears data and verifies the table is empty.

```python
conn.execute(text("TRUNCATE TABLE users;"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 0
```

---

## ✅ How to Run the Tests

Run:

```bash
pytest -v testcontainers/test_mariadb_container.py
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

* Inspect logs for the MariaDB container:

  ```bash
  docker logs <container_id>
  ```

---