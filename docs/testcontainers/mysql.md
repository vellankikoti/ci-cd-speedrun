# MySQL Container Testing

**Why MySQL?**

✅ Extremely popular in web apps, fast to spin up in containers, and a great candidate for chaos testing in CI/CD.

---

## ✅ Test Cases Implemented

### ✅ Test Case 1 — Check MySQL Version

Runs a query to ensure MySQL is running and accessible.

```python
result = conn.execute(text("SELECT VERSION();")).fetchone()
assert "MySQL" in result[0] or "MariaDB" in result[0]
````

---

### ✅ Test Case 2 — Insert and Query

Inserts a single record and retrieves it.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
result = conn.execute(text("SELECT name FROM users;")).fetchone()
assert result[0] == "Alice"
```

---

### ✅ Test Case 3 — Insert Multiple Rows

Adds multiple rows and verifies the total count.

```python
conn.execute(text("INSERT INTO users (name) VALUES ('Bob'), ('Charlie');"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 3
```

---

### ✅ Test Case 4 — Primary Key Constraint

Verifies the primary key prevents duplicate entries.

```python
conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'David');"))
with pytest.raises(Exception):
    conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Eve');"))
```

---

### ✅ Test Case 5 — Truncate Table

Clears the table and confirms it’s empty.

```python
conn.execute(text("TRUNCATE TABLE users;"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 0
```

---

## ✅ How to Run the Tests

Run:

```bash
pytest -v testcontainers/test_mysql_container.py
```

✅ Expected:

```
5 passed in X.XXs
```

---

## ✅ Useful Commands

* See running containers:

  ```bash
  docker ps
  ```

* Check MySQL logs:

  ```bash
  docker logs <container_id>
  ```

---
