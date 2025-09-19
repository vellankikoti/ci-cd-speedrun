# 🚀 TestContainers Workshop

> Simple, powerful integration testing with real databases - **anywhere, anytime!**

## 🎯 Quick Start

```bash
# Setup (one command)
python3 quick_setup.py

# Activate virtual environment
source venv/bin/activate

# Run interactive demo
python demo.py

# Or run individual labs
python labs/basics/lab1_first_container.py
```

## 📚 What You'll Learn

TestContainers lets you run **real databases** in Docker containers for testing - no mocks, no setup, no configuration!

### ✅ **Perfect for:**
- Integration testing
- Database testing
- API testing
- Workshop demonstrations
- Learning database technologies

### 🎯 **Key Benefits:**
- **Real databases** - PostgreSQL, MySQL, Redis, MongoDB
- **Isolated tests** - Each test gets a fresh database
- **Cross-platform** - Works on Windows, macOS, Linux
- **Zero setup** - No database installation required
- **Automatic cleanup** - Containers removed after tests

## 🎮 Interactive Demo

Run the interactive demo to see TestContainers in action:

```bash
python3 demo.py
```

**Demo Options:**
1. 🐘 **PostgreSQL** - Relational database operations
2. 🐬 **MySQL** - Alternative SQL database
3. 🔴 **Redis** - Key-value caching
4. 🍃 **MongoDB** - NoSQL document database
5. 🔄 **Multi-Container** - All databases together
6. 🧪 **Interactive Labs** - Step-by-step learning

## 📖 Workshop Labs

**Progressive Learning Path:**

### 📚 **Basics (Start Here)**
- **Lab 1:** Your First Container - Learn the fundamentals
- **Lab 2:** Database Connections - Master connection patterns
- **Lab 3:** Data Management - Setup, teardown, and test isolation
- **Lab 4:** Multiple Containers - Orchestrate complex scenarios

### 🎓 **Intermediate**
- **Lab 5:** Multi-Database - Advanced integration patterns

### 🚀 **Advanced**
- **Lab 9:** Performance - Optimize your tests

**Run any lab individually:**
```bash
cd labs/basics
python3 lab1_first_container.py
```

## 🔧 Requirements

- **Python 3.7+**
- **Docker** (Docker Desktop or Docker Engine)
- **Internet connection** (for downloading images)

**Automatically installed dependencies:**
- `testcontainers` - The main library
- `psycopg2-binary` - PostgreSQL adapter
- `pymysql` - MySQL adapter
- `redis` - Redis client
- `pymongo` - MongoDB driver

## 💡 Real-World Examples

### Quick PostgreSQL Test
```python
from testcontainers.postgres import PostgresContainer
import psycopg2

with PostgresContainer("postgres:15-alpine") as postgres:
    conn = psycopg2.connect(
        host=postgres.get_container_host_ip(),
        port=postgres.get_exposed_port(5432),
        user=postgres.username,
        password=postgres.password,
        database=postgres.dbname
    )

    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print(f"Connected to: {version[0]}")
```

### Redis Caching Test
```python
from testcontainers.redis import RedisContainer
import redis

with RedisContainer("redis:7-alpine") as redis_container:
    r = redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379)
    )

    r.set("test_key", "Hello TestContainers!")
    value = r.get("test_key")
    print(f"Cached value: {value.decode()}")
```

## 🛠️ Troubleshooting

### **Docker Issues**
```bash
# Check Docker is running
docker ps

# Fix permissions (Linux/macOS)
sudo chmod 666 /var/run/docker.sock
```

### **Package Issues**
```bash
# Reinstall dependencies
python3 setup.py

# Manual installation
pip install testcontainers psycopg2-binary pymysql redis pymongo
```

### **Connection Issues**
- Ensure Docker Desktop is running
- Check firewall settings
- Verify internet connectivity

## 🎯 Workshop Flow

**For Instructors:**

1. **Setup Check** (5 mins)
   ```bash
   python3 setup.py
   ```

2. **Interactive Demo** (15 mins)
   ```bash
   python3 demo.py
   ```

3. **Hands-on Labs** (45 mins)
   - Start with Lab 1
   - Progress through basics
   - Advanced labs as time permits

4. **Q&A and Exploration** (15 mins)

**For Self-Study:**
- Work through labs at your own pace
- Experiment with different databases
- Try the multi-container scenarios

## 🌟 Why TestContainers?

### **Traditional Testing Problems:**
❌ Mock databases don't catch real issues
❌ Shared test databases cause conflicts
❌ Database setup is complex and error-prone
❌ Tests behave differently in different environments

### **TestContainers Solutions:**
✅ **Real databases** catch real issues
✅ **Isolated containers** prevent conflicts
✅ **Automatic setup** - just run your tests
✅ **Consistent behavior** everywhere

## 📈 Production Benefits

- **Higher confidence** in database integrations
- **Faster debugging** with realistic test data
- **Better test coverage** of edge cases
- **Easier onboarding** for new team members
- **Consistent CI/CD** across environments

## 🎉 Success Stories

> *"TestContainers transformed our testing strategy. We caught 3 production bugs that our mocks missed!"*

> *"Setup time went from 2 hours to 2 minutes. Our new developers are productive immediately."*

> *"Same tests run on developer laptops and CI/CD - no more 'works on my machine'!"*

---

## 🚀 **Ready to Start?**

```bash
# Quick start
python3 setup.py && python3 demo.py

# Or dive into labs
cd labs/basics && python3 lab1_first_container.py
```

**Happy testing with real databases! 🎯**