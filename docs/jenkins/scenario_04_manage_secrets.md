# 🔐 Scenario 04: Manage Secrets

## Overview

This scenario teaches you how to detect, scan, and report on secret leaks in your codebase using Gitleaks, all integrated into a Jenkins pipeline. You'll learn to handle both clean and intentionally leaky code, and generate beautiful HTML/JSON reports.

---

## 📁 Directory Structure

```
Jenkins/jenkins_scenarios/scenario_04_manage_secrets/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
├── report_templates/
├── tests/
│   ├── run_tests.py
│   ├── test_secret_scan_pass.py
│   └── test_secret_scan_fail.py
```

---

## ✅ How to Set Up the Pipeline in Jenkins UI

1. **Open Jenkins** in your browser.
2. Click **"New Item"**.
3. Enter a name (e.g., `scenario_04_manage_secrets`), select **Pipeline**, and click OK.
4. In the pipeline config:
   - Under **Pipeline script**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git** and enter your repository URL.
   - Set **Script Path** to `Jenkins/jenkins_scenarios/scenario_04_manage_secrets/Jenkinsfile`.
5. Click **Save**.

---

## ✅ How to Run the Pipeline

1. Click **"Build with Parameters"**.
2. Set the `RUN_SCENARIO_4` parameter to enable/disable the scenario.
3. Set the `SCENARIO_4_PASS` parameter to `true` (clean scan) or `false` (leaky scan).
4. Click **Build**.
5. Download/view HTML and JSON reports from Jenkins artifacts after the build completes.

---

## ✅ What the Pipeline Does

- Builds a Docker image with Gitleaks and all dependencies
- Runs secret scan tests in PASS (clean) or FAIL (leaky) mode
- Generates HTML and JSON reports for each scan
- Archives reports as Jenkins build artifacts

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Secret Detection Failures

```python
def test_secret_detection_failure():
    """Simulate secret detection tool failures"""
    try:
        # Simulate Gitleaks failure
        if os.path.exists("/tmp/gitleaks_failure"):
            raise Exception("Gitleaks process killed")
            
        # Run secret scan
        results = run_gitleaks_scan()
        
    except Exception as e:
        # Fallback to manual scan
        results = run_manual_secret_scan()
        assert "manual" in str(e).lower() or "fallback" in str(e).lower()
```

### ✅ Scenario 2: False Positive Detection

```python
def test_false_positive_handling():
    """Test handling of false positive secret detections"""
    # Simulate false positive
    false_positive_secret = "AKIAIOSFODNN7EXAMPLE"  # Fake AWS key
    
    # Should be detected but marked as false positive
    results = scan_for_secrets([false_positive_secret])
    
    assert len(results) > 0
    assert results[0]["confidence"] == "low"
    assert results[0]["status"] == "false_positive"
```

### ✅ Scenario 3: Secret Rotation Simulation

```python
def test_secret_rotation():
    """Test secret rotation in CI/CD pipeline"""
    old_secret = "old_api_key_12345"
    new_secret = "new_api_key_67890"
    
    # Simulate secret rotation
    rotate_secret(old_secret, new_secret)
    
    # Verify old secret is invalidated
    assert not is_secret_valid(old_secret)
    assert is_secret_valid(new_secret)
```

---

## ✅ Troubleshooting

- **Gitleaks not found:**
  - Ensure the Dockerfile installs Gitleaks correctly (check build logs).
- **No reports generated:**
  - Check the test output and ensure reports are written to the `reports/` directory.
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

### ✅ Security Metrics

- Number of secrets detected
- False positive rate
- Secret rotation frequency
- Compliance score

### ✅ Chaos Metrics

- Secret detection failure rate
- Recovery time from security failures
- False positive handling accuracy

---

**Next:** [Scenario 01: Docker Build](scenario_01_docker_build.md) | [Scenario 02: Testcontainers](scenario_02_testcontainers.md) | [Scenario 03: HTML Reports](scenario_03_html_reports.md) | [Scenario 05: Deploy to EKS](scenario_05_deploy_eks.md)

---

**This scenario helps you master secret management and reporting in Jenkins, making your pipelines secure and audit-ready!** 🔥 