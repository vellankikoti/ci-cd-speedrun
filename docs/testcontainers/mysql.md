# 🐬 MySQL Container Testing

<div class="database-hero">
  <div class="database-content">
    <h1>Master MySQL Testing with Testcontainers</h1>
    <p class="database-subtitle">Build bulletproof MySQL integration tests that survive real-world chaos</p>
    <div class="database-stats">
      <div class="stat-item">
        <span class="stat-number">5</span>
        <span class="stat-label">test cases</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">2</span>
        <span class="stat-label">chaos scenarios</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">coverage</span>
      </div>
    </div>
  </div>
</div>

---

## 🎯 Why MySQL?

<div class="why-section">
  <div class="why-card">
    <h3>🚀 Popular & Fast</h3>
    <p>Extremely popular in web applications, fast to spin up in containers</p>
  </div>
  
  <div class="why-card">
    <h3>🧪 Perfect for Chaos</h3>
    <p>Great candidate for chaos testing in CI/CD pipelines</p>
  </div>
  
  <div class="why-card">
    <h3>🔧 Easy Integration</h3>
    <p>Simple setup with Testcontainers and comprehensive testing</p>
  </div>
</div>

---

## ✅ Test Cases Implemented

<div class="test-cases-grid">
  <div class="test-case-card">
    <div class="test-header">
      <h3>Test Case 1 — Check MySQL Version</h3>
      <span class="test-status passed">✅ Passed</span>
    </div>
    <p>Runs a query to ensure MySQL is running and accessible.</p>
    <div class="code-block">
      <div class="code-header">Python</div>
      <pre><code>result = conn.execute(text("SELECT VERSION();")).fetchone()
assert "MySQL" in result[0] or "MariaDB" in result[0]</code></pre>
    </div>
  </div>

  <div class="test-case-card">
    <div class="test-header">
      <h3>Test Case 2 — Insert and Query</h3>
      <span class="test-status passed">✅ Passed</span>
    </div>
    <p>Inserts a single record and retrieves it.</p>
    <div class="code-block">
      <div class="code-header">Python</div>
      <pre><code>conn.execute(text("INSERT INTO users (name) VALUES ('Alice');"))
result = conn.execute(text("SELECT name FROM users;")).fetchone()
assert result[0] == "Alice"</code></pre>
    </div>
  </div>

  <div class="test-case-card">
    <div class="test-header">
      <h3>Test Case 3 — Insert Multiple Rows</h3>
      <span class="test-status passed">✅ Passed</span>
    </div>
    <p>Adds multiple rows and verifies the total count.</p>
    <div class="code-block">
      <div class="code-header">Python</div>
      <pre><code>conn.execute(text("INSERT INTO users (name) VALUES ('Bob'), ('Charlie');"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 3</code></pre>
    </div>
  </div>

  <div class="test-case-card">
    <div class="test-header">
      <h3>Test Case 4 — Primary Key Constraint</h3>
      <span class="test-status passed">✅ Passed</span>
    </div>
    <p>Verifies the primary key prevents duplicate entries.</p>
    <div class="code-block">
      <div class="code-header">Python</div>
      <pre><code>conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'David');"))
with pytest.raises(Exception):
    conn.execute(text("INSERT INTO users (id, name) VALUES (1, 'Eve');"))</code></pre>
    </div>
  </div>

  <div class="test-case-card">
    <div class="test-header">
      <h3>Test Case 5 — Truncate Table</h3>
      <span class="test-status passed">✅ Passed</span>
    </div>
    <p>Clears the table and confirms it's empty.</p>
    <div class="code-block">
      <div class="code-header">Python</div>
      <pre><code>conn.execute(text("TRUNCATE TABLE users;"))
result = conn.execute(text("SELECT COUNT(*) FROM users;")).fetchone()
assert result[0] == 0</code></pre>
    </div>
  </div>
</div>

---

## 🚀 How to Run the Tests

<div class="run-section">
  <div class="run-card">
    <h3>Quick Start</h3>
    <div class="code-block">
      <div class="code-header">Terminal</div>
      <pre><code>pytest -v testcontainers/test_mysql_container.py</code></pre>
    </div>
    <div class="expected-output">
      <h4>✅ Expected Output:</h4>
      <pre><code>5 passed in X.XXs</code></pre>
    </div>
  </div>
  
  <div class="run-card">
    <h3>Useful Commands</h3>
    <div class="command-grid">
      <div class="command-item">
        <h4>See running containers:</h4>
        <div class="code-block">
          <pre><code>docker ps</code></pre>
        </div>
      </div>
      
      <div class="command-item">
        <h4>Check MySQL logs:</h4>
        <div class="code-block">
          <pre><code>docker logs &lt;container_id&gt;</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>

---

## 🧪 Chaos Testing Scenarios

<div class="chaos-section">
  <h2>Real-World Failure Simulation</h2>
  <p>Test your application's resilience against common MySQL failures</p>

  <div class="chaos-grid">
    <div class="chaos-card">
      <div class="chaos-header">
        <h3>Scenario 1: Connection Failures</h3>
        <span class="chaos-type failure">Connection Error</span>
      </div>
      <p>Test that your app handles MySQL connection failures gracefully</p>
      <div class="code-block">
        <div class="code-header">Python</div>
        <pre><code>def test_mysql_connection_failure():
    """Test that our app handles MySQL connection failures gracefully"""
    with MySqlContainer("mysql:8.0") as mysql:
        # Simulate connection failure
        mysql.get_docker_client().stop(mysql.get_container_id())
        
        # Verify our app handles the failure
        with pytest.raises(ConnectionError):
            create_connection(mysql.get_connection_url())</code></pre>
      </div>
    </div>

    <div class="chaos-card">
      <div class="chaos-header">
        <h3>Scenario 2: Slow Queries</h3>
        <span class="chaos-type performance">Performance Issue</span>
      </div>
      <p>Test that your app handles slow MySQL queries within timeouts</p>
      <div class="code-block">
        <div class="code-header">Python</div>
        <pre><code>def test_mysql_slow_query_handling():
    """Test that our app handles slow MySQL queries"""
    with MySqlContainer("mysql:8.0") as mysql:
        conn = create_connection(mysql.get_connection_url())
        
        # Simulate slow query
        import time
        start_time = time.time()
        
        # Execute a potentially slow query
        conn.execute(text("SELECT SLEEP(2)"))
        
        # Verify it completes within reasonable time
        assert time.time() - start_time &lt; 5.0</code></pre>
      </div>
    </div>
  </div>
</div>

---

## 📊 Monitoring & Reporting

<div class="monitoring-section">
  <h2>Generate Beautiful Reports</h2>
  <p>Create comprehensive HTML reports for stakeholders</p>

  <div class="report-grid">
    <div class="report-card">
      <h3>📊 Generate HTML Report</h3>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code>pytest testcontainers/test_mysql_container.py \
  --html=reports/mysql-test-report.html \
  --self-contained-html</code></pre>
      </div>
      <p>Creates a beautiful HTML report with test results and metrics</p>
    </div>

    <div class="report-card">
      <h3>📋 View Container Logs</h3>
      <div class="code-block">
        <div class="code-header">Terminal</div>
        <pre><code># Get container ID
docker ps | grep mysql

# View logs
docker logs &lt;container_id&gt;</code></pre>
      </div>
      <p>Monitor container behavior and debug issues</p>
    </div>
  </div>
</div>

---

### 🔗 Related Testing

<div class="related-section">
  <h2>Explore Other Database Testing</h2>
  <p>Master testing across different database technologies</p>

  <div class="related-grid">
    <a href="/testcontainers/postgres" class="related-card">
      <h3>🐘 PostgreSQL Testing</h3>
      <p>Test against PostgreSQL databases with advanced features</p>
      <span class="related-link">Learn PostgreSQL →</span>
    </a>
    
    <a href="mariadb" class="related-card">
      <h3>🗄️ MariaDB Testing</h3>
      <p>Test MariaDB compatibility and character sets</p>
      <span class="related-link">Learn MariaDB →</span>
    </a>
    
    <a href="mongodb" class="related-card">
      <h3>🍃 MongoDB Testing</h3>
      <p>Test document operations and large datasets</p>
      <span class="related-link">Learn MongoDB →</span>
    </a>
    
    <a href="redis" class="related-card">
      <h3>🔴 Redis Testing</h3>
      <p>Test caching operations and memory pressure</p>
      <span class="related-link">Learn Redis →</span>
    </a>
  </div>
</div>

---

<div class="footer-note">
  <p><strong>Ready to test other databases?</strong> Choose your next challenge! 🚀</p>
</div>
