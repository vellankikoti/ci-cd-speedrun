# 🚀 Phase 1 - Database Testing with Testcontainers

Welcome to **Phase 1** of the CI/CD Chaos Workshop — where we learn how to spin up real databases on demand for automated testing using **Testcontainers**.

This phase demonstrates:
✅ Running databases in real Docker containers  
✅ Writing Python tests against real databases  
✅ Generating HTML reports automatically  
✅ Integrating tests into a CI/CD pipeline  
✅ Chaos-inspired practices like random failures or delays

---

## 🔍 What’s Inside?

This phase covers **five databases**, each with five practical test cases:

- **MariaDB** → CRUD operations, constraints
- **MySQL** → inserts, constraints, multiple rows
- **PostgreSQL** → transactions, truncate checks
- **MongoDB** → document inserts, updates, deletions
- **Redis** → key-value operations, TTL expiration

All tests use **pytest** + **testcontainers** to spin up ephemeral containers.

---

## ✨ How to Run All Tests

### Run single tests file

Example:

```bash
pytest tests/test_mariadb_container.py
````

Or with live logs:

```bash
pytest -s tests/test_mariadb_container.py
```

---

### Run all tests at once

```bash
pytest tests/
```

Or for HTML reports:

```bash
pytest tests/ --html=reports/test_report.html --self-contained-html
```

> ✅ This generates beautiful HTML reports under:
>
> ```
> reports/test_report.html
> ```

---

## 🐳 How It Works

✅ Containers spin up before each test (or test class).
✅ Tests connect to real database ports.
✅ After tests finish:

* Containers auto-stop
* No leftover state
* Chaos achieved 😈

Testcontainers Desktop beautifully visualizes container lifecycles during test runs:

* **Green dots** = containers ready
* **Yellow dots** = starting up
* **Red dots** = stopping

This makes demos highly visual and engaging!

---

## 💻 Example - PostgreSQL

Example test snippet:

```python
def test_postgres_version(pg_engine):
    with pg_engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        assert "PostgreSQL" in version
```

---

## ✅ Test Reports

Tests generate HTML reports for awesome workshop demos.

* Launch tests:

  ```bash
  pytest tests/test_mongodb_container.py \
      --html=reports/mongodb-test-report.html \
      --self-contained-html
  ```

* Open the report in your browser and show logs, passing tests, failures, and timing.

---

## 🤯 Chaos Engineering Ideas

Enhance tests for chaos:

* Random container kill signals
* Random delays on DB calls
* High CPU load during tests

These chaos practices teach why resilience matters in real-world pipelines!

---

## 📊 Demo Flow

When demonstrating this phase:

1. Start Testcontainers Desktop.
2. Run tests with `pytest -s`.
3. Show containers appearing/disappearing visually.
4. Open HTML report live.
5. Discuss:

   * How ephemeral containers help keep tests isolated.
   * Why this improves CI/CD reliability.
   * How Testcontainers saves infrastructure cost.

---

## 💡 Why Use Testcontainers?

✅ No local DB installation
✅ 100% reproducibility
✅ Perfect for Dockerized CI/CD pipelines
✅ Chaos Engineering experiments
✅ Modern DevOps practice!

Let’s keep it chaotic…and fun! 🎉

---

> \[!TIP]
> Try running:
>
> ```
> pytest -s tests/test_redis_container.py
> ```
>
> And watch Redis appear in Testcontainers Desktop!

---

[⬅️ Previous Phase Setup](./setup.md) | [➡️ Next Phase → Docker](./docker.md)
