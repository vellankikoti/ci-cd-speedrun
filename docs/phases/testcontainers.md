# 🧪 Phase 1 – TestContainers

Welcome to **Phase 1** of the CI/CD Chaos Workshop — the place where we build truly reliable tests using TestContainers!

This phase covers:

✅ Database container testing  
✅ Isolated, repeatable environments  
✅ Automatic teardown between tests  
✅ Fast feedback for developers  
✅ Beautiful reporting for stakeholders

> 🎯 **Goal:** Prove our tests survive chaos — no matter what the environment.

---

## ✅ Why TestContainers?

TestContainers lets us:

- Launch real databases in Docker
- Run them alongside our Python tests
- Avoid flaky tests that depend on external services
- Guarantee identical test environments everywhere

**Chaos Agent:**  
> "Let's run tests against production. What's the worst that could happen?"

We'll prove why that's a bad idea.

---

## 🚀 Database Testing Scenarios

Below are **production-grade testing scenarios** you'll implement.

Each follows the same pattern:

- Start a container (PostgreSQL, MySQL, etc.)
- Run tests in Python using pytest
- Tear down automatically
- Analyze logs and results

These scenarios are your first defense against chaos.

---

## 🚀 Scenario 1 – PostgreSQL TestContainer

### ✅ Why It Matters

PostgreSQL is a common backend for modern apps. Reliable tests ensure migrations and queries work safely.

> **Chaos Event:** "My dev machine has PostgreSQL 14. Production has PostgreSQL 15!"

---

### ✅ What We'll Do

✅ Spin up a PostgreSQL container  
✅ Connect with SQLAlchemy  
✅ Run migrations and tests

---

### ✅ How to Fix It

✅ Always test against the same Postgres version as production.

---

### ✅ Test Snippet

```python
from testcontainers.postgres import PostgresContainer

def test_postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        conn_url = postgres.get_connection_url()
        # Connect with SQLAlchemy or psycopg2 and run tests
        assert conn_url.startswith("postgresql://")
```

---

### ✅ Best Practices

✅ Always specify Postgres version  
✅ Truncate tables between tests  
✅ Never test against a shared local instance

---

### ✅ What Could Go Wrong?

- Connection refused errors  
- Port conflicts if containers not cleaned up  
- Version mismatch between local and prod

---

## 🚀 Scenario 2 – MySQL TestContainer

### ✅ Why It Matters

MySQL powers tons of legacy apps and new workloads.

> **Chaos Event:** "MySQL crashes tests because dev machine has wrong credentials."

---

### ✅ What We'll Do

✅ Spin up MySQL container  
✅ Run pytest database tests

---

### ✅ How to Fix It

✅ Use environment variables for credentials.

---

### ✅ Test Snippet

```python
from testcontainers.mysql import MySqlContainer

def test_mysql_container():
    with MySqlContainer("mysql:8.0") as mysql:
        url = mysql.get_connection_url()
        # Connect with SQLAlchemy or pymysql and run tests
        assert "mysql" in url
```

---

### ✅ Best Practices

✅ Never hardcode passwords  
✅ Use transactions to isolate tests  
✅ Clean up containers after tests

---

### ✅ What Could Go Wrong?

- Slow container startup times  
- Wrong ports exposed  
- Credential errors

---

## 🚀 Scenario 3 – MariaDB TestContainer

### ✅ Why It Matters

MariaDB is popular for cost-effective apps and easy MySQL migrations.

> **Chaos Event:** "Code works on MySQL, fails on MariaDB!"

---

### ✅ What We'll Do

✅ Launch MariaDB container  
✅ Run pytest integration tests

---

### ✅ How to Fix It

✅ Test MariaDB-specific SQL syntax differences.

---

### ✅ Test Snippet

```python
from testcontainers.mariadb import MariaDbContainer

def test_mariadb_container():
    with MariaDbContainer("mariadb:10.6") as mariadb:
        url = mariadb.get_connection_url()
        assert "mariadb" in url
```

---

### ✅ Best Practices

✅ Test MySQL and MariaDB separately  
✅ Avoid vendor-specific SQL unless necessary  
✅ Watch out for default charset differences

---

### ✅ What Could Go Wrong?

- SQL syntax differences between MySQL and MariaDB  
- Character set encoding issues  
- Performance differences in complex queries

---

## 🚀 Scenario 4 – MongoDB TestContainer

### ✅ Why It Matters

MongoDB is perfect for document-based data and modern web apps.

> **Chaos Event:** "MongoDB connection fails because dev machine has different auth setup!"

---

### ✅ What We'll Do

✅ Launch MongoDB container  
✅ Test document operations  
✅ Verify indexing and queries

---

### ✅ How to Fix It

✅ Use containerized MongoDB for consistent testing.

---

### ✅ Test Snippet

```python
from testcontainers.mongodb import MongoDbContainer

def test_mongodb_container():
    with MongoDbContainer("mongo:6.0") as mongo:
        client = mongo.get_connection_client()
        db = client.test_db
        collection = db.test_collection
        
        # Insert and query documents
        result = collection.insert_one({"name": "test"})
        assert result.inserted_id is not None
```

---

### ✅ Best Practices

✅ Use transactions for data consistency  
✅ Clean up collections between tests  
✅ Test both read and write operations

---

### ✅ What Could Go Wrong?

- Authentication issues  
- Network connectivity problems  
- Version compatibility issues

---

## 🚀 Scenario 5 – Redis TestContainer

### ✅ Why It Matters

Redis is essential for caching, sessions, and real-time data.

> **Chaos Event:** "Redis connection fails in CI but works locally!"

---

### ✅ What We'll Do

✅ Launch Redis container  
✅ Test caching operations  
✅ Verify pub/sub functionality

---

### ✅ How to Fix It

✅ Use containerized Redis for consistent testing.

---

### ✅ Test Snippet

```python
from testcontainers.redis import RedisContainer

def test_redis_container():
    with RedisContainer("redis:7-alpine") as redis:
        client = redis.get_client()
        
        # Test basic operations
        client.set("key", "value")
        assert client.get("key") == b"value"
```

---

### ✅ Best Practices

✅ Flush database between tests  
✅ Test both string and hash operations  
✅ Verify connection pooling

---

### ✅ What Could Go Wrong?

- Memory issues with large datasets  
- Connection pool exhaustion  
- Network timeouts

---

## 🎯 Running Your Tests

### ✅ Quick Start

```bash
# Install dependencies
pip install testcontainers pytest

# Run all database tests
pytest testcontainers/ -v

# Run specific database tests
pytest testcontainers/test_mysql_container.py -v
pytest testcontainers/test_postgres_container.py -v
```

### ✅ Expected Output

```
testcontainers/test_mysql_container.py::test_mysql_version PASSED
testcontainers/test_mysql_container.py::test_mysql_insert_query PASSED
testcontainers/test_mysql_container.py::test_mysql_multiple_rows PASSED
testcontainers/test_mysql_container.py::test_mysql_primary_key PASSED
testcontainers/test_mysql_container.py::test_mysql_truncate PASSED
```

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Container Crashes

```python
def test_container_crash_recovery():
    """Test that our app handles container crashes gracefully"""
    with PostgresContainer("postgres:15") as postgres:
        # Start container
        conn = create_connection(postgres.get_connection_url())
        
        # Simulate container crash
        postgres.get_docker_client().stop(postgres.get_container_id())
        
        # Verify our app handles the crash
        with pytest.raises(ConnectionError):
            conn.execute("SELECT 1")
```

### ✅ Scenario 2: Network Delays

```python
def test_network_delay_handling():
    """Test that our app handles network delays"""
    with RedisContainer("redis:7-alpine") as redis:
        # Simulate network delay
        import time
        start_time = time.time()
        
        client = redis.get_client()
        client.set("test", "value")
        
        # Verify operation completes within reasonable time
        assert time.time() - start_time < 5.0
```

### ✅ Scenario 3: Resource Limits

```python
def test_memory_limit_handling():
    """Test that our app handles memory constraints"""
    with MongoDbContainer("mongo:6.0") as mongo:
        # Set memory limit
        mongo.with_memory_limit("100m")
        
        # Try to insert large dataset
        client = mongo.get_connection_client()
        db = client.test_db
        collection = db.test_collection
        
        # This should work or fail gracefully
        try:
            collection.insert_many([{"data": "x" * 1000} for _ in range(1000)])
        except Exception as e:
            # Handle memory constraint gracefully
            assert "memory" in str(e).lower() or "resource" in str(e).lower()
```

---

## 📊 Monitoring & Reporting

### ✅ HTML Reports

```bash
# Generate HTML test reports
pytest testcontainers/ --html=reports/testcontainers-report.html --self-contained-html
```

### ✅ Coverage Reports

```bash
# Install coverage
pip install pytest-cov

# Run with coverage
pytest testcontainers/ --cov=testcontainers --cov-report=html
```

---

## 🎯 Next Steps

✅ **Phase 1 Complete:** You now have bulletproof database tests!  
✅ **Ready for Phase 2:** [Docker Mastery](docker.md)  
✅ **Chaos Agent Status:** Defeated in database testing! 🕶️

---

**Remember:** TestContainers make your tests as reliable as production. When chaos strikes, your tests will be your first line of defense! 🔥
