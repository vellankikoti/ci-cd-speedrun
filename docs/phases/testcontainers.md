
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
> “Let’s run tests against production. What’s the worst that could happen?”

We’ll prove why that’s a bad idea.

---

# 🚀 Database Testing Scenarios

Below are **production-grade testing scenarios** you’ll implement.

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

> **Chaos Event:** “My dev machine has PostgreSQL 14. Production has PostgreSQL 15!”

---

### ✅ What We’ll Do

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

> **Chaos Event:** “MySQL crashes tests because dev machine has wrong credentials.”

---

### ✅ What We’ll Do

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

> **Chaos Event:** “Code works on MySQL, fails on MariaDB!”

---

### ✅ What We’ll Do

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

- SQL syntax differences  
- Authentication plugin issues  
- Performance differences on joins

---

## 🚀 Scenario 4 – MongoDB TestContainer

### ✅ Why It Matters

NoSQL apps often rely on MongoDB for flexibility.

> **Chaos Event:** “My Mongo queries fail only in production!”

---

### ✅ What We’ll Do

✅ Start a MongoDB container  
✅ Run Python tests with pymongo

---

### ✅ How to Fix It

✅ Keep versions in sync across environments.

---

### ✅ Test Snippet

```python
from testcontainers.mongodb import MongoDbContainer

def test_mongo_container():
    with MongoDbContainer("mongo:6") as mongo:
        conn_str = mongo.get_connection_url()
        assert "mongodb://" in conn_str
```

---

### ✅ Best Practices

✅ Use test-specific databases  
✅ Always close client connections  
✅ Keep Mongo versions consistent

---

### ✅ What Could Go Wrong?

- Timeouts on large documents  
- Indexes missing in tests  
- Version differences between dev and prod

---

## 🚀 Scenario 5 – Redis TestContainer

### ✅ Why It Matters

Redis powers caching, queues, and sessions for modern apps.

> **Chaos Event:** “Local Redis had persistence ON. Production has it OFF.”

---

### ✅ What We’ll Do

✅ Launch Redis container  
✅ Test pub/sub, caching logic

---

### ✅ How to Fix It

✅ Always replicate production configuration.

---

### ✅ Test Snippet

```python
from testcontainers.redis import RedisContainer

def test_redis_container():
    with RedisContainer("redis:7") as redis:
        port = redis.get_exposed_port(6379)
        assert port.isdigit()
```

---

### ✅ Best Practices

✅ Test both ephemeral and persistent modes  
✅ Use short-lived keys for test data  
✅ Always clean up Redis state

---

### ✅ What Could Go Wrong?

- Port conflicts  
- Missing Redis commands in older versions  
- Data leakage between tests

---

## ✅ Scaling Beyond Databases

TestContainers can handle:

- RabbitMQ
- ElasticSearch
- Kafka
- LocalStack for AWS services
- Multi-container test environments

We’ll expand this section with **hundreds of advanced scenarios** as our workshop evolves.

Chaos Agent won’t stand a chance.

---

[⬅️ Previous Phase: Setup](./setup.md) | [Next Phase: Docker Mastery ➡️](./docker.md)
