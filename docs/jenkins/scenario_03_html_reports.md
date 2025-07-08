# 📊 Scenario 03: HTML Reports Chaos

## Overview

This scenario teaches you how to generate, archive, and view beautiful HTML test reports in Jenkins, making your CI/CD results visually clear and enterprise-ready.

---

## 📁 Directory Structure

```
Jenkins/jenkins_scenarios/scenario_03_html_reports/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── report_generator.py
├── requirements.txt
└── tests/
    ├── test_config_validation_pass.py
    ├── test_config_validation_fail.py
    ├── test_api_health_pass.py
    ├── test_api_health_fail.py
    ├── test_postgres_pass.py
    ├── test_postgres_fail.py
    ├── test_redis_pass.py
    ├── test_redis_fail.py
    ├── test_secret_scan_pass.py
    └── test_secret_scan_fail.py
```

---

## ✅ How to Set Up the Pipeline in Jenkins UI

1. **Open Jenkins** in your browser.
2. Click **"New Item"**.
3. Enter a name (e.g., `scenario_03_html_reports`), select **Pipeline**, and click OK.
4. In the pipeline config:
   - Under **Pipeline script**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git** and enter your repository URL.
   - Set **Script Path** to `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile`.
5. Click **Save**.

---

## ✅ How to Run the Pipeline

1. Click **"Build with Parameters"** (if parameters are defined).
2. Click **Build**.
3. Watch the console output for test execution and report generation.
4. Download/view HTML reports from Jenkins artifacts after the build completes.

---

## ✅ What the Pipeline Does

- Builds a Docker image with all dependencies
- Runs a suite of Python tests (config validation, API health, DB, Redis, secrets)
- Generates HTML and JSON reports for each test
- Archives reports as Jenkins build artifacts

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Report Generation Failures

```python
def test_report_generation_failure():
    """Simulate HTML report generation failures"""
    try:
        # Simulate disk space issues
        if os.path.exists("/tmp/disk_full"):
            raise OSError("No space left on device")
            
        # Generate report
        generate_html_report(test_results)
        
    except Exception as e:
        # Fallback to simple text report
        generate_text_report(test_results)
        assert "text" in str(e).lower() or "space" in str(e).lower()
```

### ✅ Scenario 2: Slow Report Generation

```python
def test_slow_report_generation():
    """Test report generation under load"""
    import time
    start_time = time.time()
    
    # Generate large report
    large_dataset = [{"test": f"test_{i}", "result": "pass"} for i in range(10000)]
    generate_html_report(large_dataset)
    
    # Verify it completes within reasonable time
    assert time.time() - start_time < 30.0
```

### ✅ Scenario 3: Corrupted Report Data

```python
def test_corrupted_report_data():
    """Test handling of corrupted test data"""
    corrupted_data = [
        {"test": "valid_test", "result": "pass"},
        {"test": "corrupted_test", "result": None},  # Corrupted
        {"test": "another_test", "result": "fail"}
    ]
    
    # Should handle corrupted data gracefully
    report = generate_html_report(corrupted_data)
    assert "corrupted_test" in report
    assert "error" in report.lower()
```

---

## ✅ Troubleshooting

- **Reports not found:**
  - Check the archive path in the Jenkinsfile matches the reports output directory.
  - Ensure the tests generate reports in the expected location.
- **Build fails:**
  - Check for missing dependencies in `requirements.txt`.
  - Review the Docker build logs for errors.
- **HTML not rendering:**
  - Download the HTML report and open it in your browser.

---

## ✅ Useful Commands

- See running containers:
  ```bash
  docker ps
  ```
- Check logs for a container:
  ```bash
  docker logs <container_id>
  ```
- Remove a container:
  ```bash
  docker rm -f <container_id>
  ```

---

## 📊 Monitoring & Reporting

### ✅ Report Metrics

- Report generation time
- Report file size
- Number of tests reported
- Report accessibility score

### ✅ Chaos Metrics

- Report generation failure rate
- Recovery time from report failures
- Data corruption detection rate

---

**Next:** [Scenario 01: Docker Build](scenario_01_docker_build.md) | [Scenario 02: Testcontainers](scenario_02_testcontainers.md) | [Scenario 04: Manage Secrets](scenario_04_manage_secrets.md) | [Scenario 05: Deploy to EKS](scenario_05_deploy_eks.md)

---

**This scenario helps you master enterprise-grade reporting in Jenkins, making your CI/CD results clear and actionable!** 🔥 