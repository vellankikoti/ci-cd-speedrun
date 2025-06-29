# 🎯 Phase 1: Chaos Testing with Testcontainers 🐳

> **“Test your chaos before chaos tests you.”**  
> — CI/CD Chaos Workshop

Welcome to Phase 1 of our **CI/CD Chaos Workshop!**  
This is where the fun truly begins.

---

## 🚀 Why Testcontainers?

✅ **Fast** → Starts real DBs in seconds  
✅ **Real** → No mocks. No fakes. 100% real containers.  
✅ **Clean** → Auto-removal guarantees a fresh start  
✅ **Chaos-ready** → Simulate network slowness, latency, flaky services

We use Python and Testcontainers to spin up real databases **on the fly** for integration testing.

---

## 🧪 What You’ll Learn

- How to **launch databases in Docker** via Python
- How to write **real integration tests** against live DBs
- How to add **chaos delays** to test resilience
- How to generate **HTML reports** with pytest
- How to impress your friends with **Testcontainers Desktop**

---

## 💻 Supported Databases

We built beautiful chaos tests for:

| Database     | Version |
| ------------ | ------- |
| ✅ PostgreSQL | 15      |
| ✅ MySQL      | 8.0     |
| ✅ MariaDB    | 11.1    |
| ✅ MongoDB    | 7.0     |
| ✅ Redis      | 7.2     |

All tests:
- Are **isolated** (no leftover data)
- Automatically clean up between runs
- Print logs so you can **SEE containers spin up & down**
- Demonstrate real DB behaviors (e.g. constraints, transactions)

---

## 🛠️ How to Run Tests

### 🔥 Run All Tests

```bash
python run_tests.py
````

Or using pytest directly:

```bash
pytest -s tests/
```

---

### ✅ Run a Specific Database (e.g. MySQL)

```bash
pytest -s tests/test_mysql_container.py
```

---

### 🎨 Run MongoDB Tests + HTML Report

If you want a fancy HTML report:

```bash
pytest -s tests/test_mongodb_container.py
```

Or generate a full HTML report:

```bash
pytest tests/test_mongodb_container.py --html=reports/mongodb-test-report.html --self-contained-html
```

Then open:

```
reports/mongodb-test-report.html
```

---

## 💥 Example Chaos Test: MySQL

Here’s how easy it is to spin up a MySQL container **and break things:**

```python
from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text

with MySqlContainer("mysql:8.0") as mysql:
    url = mysql.get_connection_url().replace("mysql://", "mysql+pymysql://")
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                name VARCHAR(255)
            );
        """))
        conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Alice');"))
```

---

## 🎲 Adding Chaos Delays

Want chaos?

Add random delays in your tests:

```python
import time
import random

delay = random.randint(0, 3)
if delay:
    print(f"🌪️ Introducing chaos delay of {delay} seconds...")
    time.sleep(delay)
```

This simulates:

* Network slowness
* Slow container startups
* Random production weirdness

---

## 📊 Generating Test Reports

We love **beautiful reports!**

✅ For HTML reports:

```bash
pytest tests/test_mysql_container.py --html=reports/mysql-test-report.html --self-contained-html
```

Then open your browser to:

```
reports/mysql-test-report.html
```

These reports look gorgeous and help debug test failures during chaos experiments.

---

## 👀 Demo Tips

✅ Launch **Testcontainers Desktop**
➡️ Watch containers start and stop in real-time!

✅ Sprinkle in chaos delays
➡️ Show how resilient tests handle slow DB starts.

✅ Switch DB versions on the fly
➡️ Just change Docker tags!

---

## 🚀 Why This Matters

This chaos testing is the **foundation of your CI/CD pipelines.**
By testing real DBs, you avoid surprises in production:

> **“If your tests don’t run against real services, they’re not real tests.”**

Let’s break things early — so customers never see the chaos.

---

[⬅️ Previous Phase](./setup.md) | [➡️ Next Phase → Docker Chaos](./docker.md)

---