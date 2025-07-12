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
```

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

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: MySQL vs MariaDB Compatibility

```python
def test_mariadb_mysql_compatibility():
    """Test that our app works with both MySQL and MariaDB"""
    with MariaDbContainer("mariadb:10.6") as mariadb:
        conn = create_connection(mariadb.get_connection_url())
        
        # Test MariaDB-specific features
        result = conn.execute(text("SELECT @@version_comment;")).fetchone()
        assert "MariaDB" in result[0]
```

### ✅ Scenario 2: Character Set Issues

```python
def test_mariadb_character_set():
    """Test that our app handles MariaDB character set differences"""
    with MariaDbContainer("mariadb:10.6") as mariadb:
        conn = create_connection(mariadb.get_connection_url())
        
        # Test UTF-8 support
        conn.execute(text("INSERT INTO users (name) VALUES ('José');"))
        result = conn.execute(text("SELECT name FROM users WHERE name = 'José';")).fetchone()
        assert result[0] == "José"
```

---

## 📊 Monitoring & Reporting

### ✅ Generate HTML Report

```bash
pytest testcontainers/test_mariadb_container.py --html=reports/mariadb-test-report.html --self-contained-html
```

### ✅ View Container Logs

```bash
# Get container ID
docker ps | grep mariadb

# View logs
docker logs <container_id>
```

---