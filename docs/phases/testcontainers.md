# 🧪 Testcontainers: Bulletproof Your Integration Tests (Database)

Welcome to **Phase 1** of the CI/CD Chaos Workshop — where you'll transform flaky integration tests into production-grade, chaos-hardened pipelines using Testcontainers!

## 🎯 What You'll Experience

- **Real Database Testing**: Spin up actual MySQL, PostgreSQL, MariaDB, MongoDB, and Redis containers for every test run
- **Chaos Engineering**: Experience intentional test failures, random delays, and container crashes to build resilience
- **Production-Grade Patterns**: Learn fixtures, isolation, cleanup, and reporting that work in real CI/CD pipelines
- **Hands-On Mastery**: Write, run, and debug tests against 5 different database technologies

---

## 🚀 Why Testcontainers Matter

**The Problem:** Your tests work on your machine but fail in CI. Why? Because you're testing against different database versions, configurations, or even shared databases that other developers are using.

**The Solution:** Testcontainers spins up fresh, isolated database containers for every test run. No more "works on my machine" — your tests run against the exact same environment every time.

**The Chaos Angle:** What happens when your database crashes mid-test? What if the network is slow? Testcontainers lets you simulate these failures and prove your app survives them.

---

## 🧪 Hands-On Scenarios

### 1. **MySQL: The Foundation**
**What You'll Do:**
- Spin up MySQL 8.0 containers with proper authentication
- Write 5 comprehensive test cases: version checks, CRUD operations, constraints, and cleanup
- Experience chaos delays and random failures
- Learn SQLAlchemy integration patterns

**Real Code You'll Write:**
```python
def test_mysql_version():
    mysql, engine = get_mysql_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        assert "8.0" in result.fetchone()[0]
```

**Chaos Lessons:** Version mismatches, connection failures, and credential chaos

---

### 2. **PostgreSQL: The Modern Choice**
**What You'll Do:**
- Use pytest fixtures for efficient container reuse
- Test PostgreSQL-specific features like SERIAL primary keys
- Implement proper transaction handling and rollbacks
- Experience the power of test isolation with automatic table truncation

**Real Code You'll Write:**
```python
@pytest.fixture(scope="module")
def pg_engine():
    with PostgresContainer("postgres:15") as postgres:
        engine = create_engine(postgres.get_connection_url())
        yield engine
```

**Chaos Lessons:** Connection pooling, transaction isolation, and constraint violations

---

### 3. **MariaDB: The Compatible Alternative**
**What You'll Do:**
- Test MariaDB as a MySQL drop-in replacement
- Discover subtle SQL syntax differences
- Handle character set and encoding challenges
- Compare performance and behavior between MySQL and MariaDB

**Real Code You'll Write:**
```python
def test_mariadb_character_set():
    with MariaDbContainer("mariadb:10.6") as mariadb:
        # Test UTF-8 support and MariaDB-specific features
        conn.execute(text("INSERT INTO users (name) VALUES ('José');"))
```

**Chaos Lessons:** Vendor compatibility, character encoding, and migration challenges

---

### 4. **MongoDB: Document Database Mastery**
**What You'll Do:**
- Work with document-based data instead of relational tables
- Test MongoDB-specific operations: insert, find, update, delete
- Handle large documents and complex queries
- Experience NoSQL testing patterns

**Real Code You'll Write:**
```python
def test_mongodb_document_operations():
    with MongoDbContainer("mongo:6.0") as mongo:
        client = mongo.get_connection_client()
        collection = client.test_db.users
        result = collection.insert_one({"name": "Alice", "age": 30})
        assert result.inserted_id is not None
```

**Chaos Lessons:** Document size limits, indexing failures, and connection drops

---

### 5. **Redis: Caching Under Pressure**
**What You'll Do:**
- Test key-value operations and data structures
- Implement TTL (Time To Live) and expiration testing
- Handle memory pressure and connection limits
- Experience caching-specific failure scenarios

**Real Code You'll Write:**
```python
def test_redis_key_expiration():
    redis_client.setex("session", 2, "active")
    assert redis_client.get("session") == b"active"
    time.sleep(3)
    assert redis_client.get("session") is None
```

**Chaos Lessons:** Memory limits, connection pool exhaustion, and cache invalidation

---

## 🎭 Built-In Chaos Engineering

Every test includes **intentional chaos** to build resilience:

```python
def chaos_delay(max_seconds=3):
    """Introduce random delays to simulate real-world variability"""
    delay = random.randint(0, max_seconds)
    if delay > 0:
        print(f"💥 Chaos delay: sleeping {delay} seconds...")
        time.sleep(delay)
```

**Chaos Scenarios You'll Experience:**
- **Random Delays**: Tests take unpredictable time, simulating network latency
- **Container Crashes**: Databases stop mid-test to verify error handling
- **Resource Limits**: Memory and CPU constraints to test graceful degradation
- **Connection Failures**: Network interruptions to prove retry logic works

---

## 🏗️ Production Patterns You'll Learn

### **Test Isolation**
```python
@pytest.fixture(autouse=True)
def truncate_users_table(pg_engine):
    """Automatically clean up between tests"""
    with pg_engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE users;"))
```

### **Container Lifecycle Management**
```python
def get_mysql_engine():
    mysql = MySqlContainer("mysql:8.0")
    mysql.start()
    try:
        yield create_engine(mysql.get_connection_url())
    finally:
        mysql.stop()
```

### **Comprehensive Error Handling**
```python
def test_primary_key_constraint():
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Duplicate');"))
```

---

## 📊 Reporting & Monitoring

### **Beautiful HTML Reports**
```bash
pytest testcontainers/ --html=reports/testcontainers-report.html --self-contained-html
```

### **Coverage Analysis**
```bash
pytest testcontainers/ --cov=testcontainers --cov-report=html
```

### **Real-Time Container Monitoring**
```bash
# Watch containers start and stop
docker ps

# Inspect logs for debugging
docker logs <container_id>
```

---

## 🚀 How to Run

### **Quick Start**
```bash
# Install dependencies
pip install testcontainers pytest sqlalchemy redis pymongo

# Run all database tests
pytest testcontainers/ -v

# Run specific database tests
pytest testcontainers/test_mysql_container.py -v
pytest testcontainers/test_postgres_container.py -v
pytest testcontainers/test_redis_container.py -v
```

### **Expected Output**
```
✨ 🚀 Starting test: Check MySQL Version
💥 Chaos delay introduced... sleeping 2 seconds.
✅ MySQL Version: 8.0.36
✅ MySQL Version test passed!

✨ 🚀 Starting test: Insert and Query One Row
✅ Successfully inserted and queried Alice!
✅ Insert and Query test passed!
```

---

## 🎯 Learning Outcomes

By the end of Phase 1, you'll be able to:

✅ **Write bulletproof database tests** that work consistently across all environments  
✅ **Handle real-world failures** with proper error handling and retry logic  
✅ **Use Testcontainers effectively** for any database technology  
✅ **Generate professional reports** that stakeholders can understand  
✅ **Debug container issues** quickly and efficiently  
✅ **Apply chaos engineering principles** to make your tests more robust  

---

## 🎭 The Chaos Agent's Challenge

**Chaos Agent:** *"Let's just test against the shared dev database. What could go wrong?"*

**Your Response:** *"Everything! Different developers, different data, different versions. Testcontainers gives us isolated, repeatable, production-like environments for every test run."*

---

## 🏁 Next Steps

✅ **Phase 1 Complete:** You now have chaos-proof database tests!  
✅ **Ready for Phase 2:** [Docker Mastery](docker.md) — where you'll build, analyze, and break real Docker images.  
✅ **Chaos Agent Status:** Defeated in database testing! 🕶️  

---

**Remember:** Testcontainers are your shield against chaos. When production throws a curveball, your tests will be ready! 🚀

> 💡 **Pro Tip:** The chaos delays and random failures in these tests aren't bugs — they're features! They're teaching you to write resilient code that handles real-world unpredictability.

###Reference: https://github.com/vellankikoti/testcontainers-db-message-brokers