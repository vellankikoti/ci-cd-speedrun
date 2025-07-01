# 🔐 Scenario 4: Manage Secrets — CI/CD Chaos Workshop

## 🚀 Overview

**Scenario 4** teaches enterprise-grade secret management by simulating real-world DevOps chaos:
- Detect leaked secrets
- Scan code for credentials
- Enforce best practices
- Generate beautiful, actionable reports

This scenario is fully isolated and integrates with Jenkins and Docker, producing both JSON and visually stunning HTML reports.

---

## ✨ Features
- **Gitleaks-powered** secret scanning (fast, reliable)
- **PASS mode:** Scans clean code, expects no secrets
- **FAIL mode:** Scans code with realistic fake secrets, expects detection
- **Enterprise HTML/JSON reports** (color-coded, bar charts, accessible)
- **Jenkins pipeline integration** with parameters
- **Robust Docker build** (minimal, reproducible)
- **Bulletproof error handling** and cleanup

---

## 📁 File Structure

```
Jenkins/jenkins_scenarios/scenario_04_manage_secrets/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
├── report_templates/
│   └── html_report_template.html
├── tests/
│   ├── run_tests.py
│   ├── test_secret_scan_fail.py
│   └── test_secret_scan_pass.py
```

---

## ⚡️ Quick Start

### 1. **Build & Run Locally**

```bash
cd Jenkins/jenkins_scenarios/scenario_04_manage_secrets
# Build Docker image
docker build -t scenario4-secrets .
# PASS mode (should find no secrets)
docker run --rm -e SCENARIO_4_PASS=true scenario4-secrets
# FAIL mode (should detect secrets)
docker run --rm -e SCENARIO_4_PASS=false scenario4-secrets
```

- Reports will be generated in the `reports/` directory.

---

### 2. **Jenkins Pipeline Usage**

- Use the provided `Jenkinsfile` in this directory.
- **Parameters:**
  - `RUN_SCENARIO_4` (boolean): Enable/disable scenario
  - `SCENARIO_4_PASS` (boolean): Run PASS (clean) or FAIL (leaky) test

#### **Pipeline Steps:**
1. **Builds Docker image** for scenario 4
2. **Runs secret scan** in container (PASS or FAIL mode)
3. **Archives HTML/JSON reports** as Jenkins artifacts
4. **Marks build as failed** if secrets are found (in FAIL mode)
5. **Prints beautiful console logs** with links to reports

#### **To Run:**
- Go to Jenkins → This scenario pipeline
- Click **"Build with Parameters"**
- Set `RUN_SCENARIO_4` and `SCENARIO_4_PASS` as desired
- Download/view reports from Jenkins artifacts

---

## 📊 Report Details
- **HTML reports**: Color-coded, accessible, with bar charts and secret details
- **JSON reports**: Raw gitleaks output for automation
- **Location**: `reports/` directory (archived by Jenkins)
- **No secrets found**: Green, success message
- **Secrets found**: Red/yellow, with type, file, line, masked snippet, severity

---

## 🛠️ Troubleshooting
- **Docker build fails?** Ensure you have network access and Docker permissions.
- **Gitleaks not found?** The Dockerfile installs the latest release automatically.
- **No reports?** Check container logs and ensure `reports/` is mounted or present.
- **Jenkins errors?** Make sure workspace is clean and parameters are set.
- **HTML not rendering?** Use Jenkins artifact viewer or open in any browser.

---

## 🏆 Enterprise-Ready
- Fully isolated from other scenarios
- No UI changes required in Jenkins
- Pure config-as-code
- Works on any Jenkins/Docker setup
- Robust, re-runnable, and demo-ready

---

## 🙌 Credits
Built for the **CI/CD Chaos Workshop** — Scenario 4: Manage Secrets

For questions or improvements, contact the workshop maintainers.
