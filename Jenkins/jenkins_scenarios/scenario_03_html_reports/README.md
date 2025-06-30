# 🚀 Scenario 3 – Archiving HTML Reports

## ✅ Why It Matters

Beautiful HTML reports help:

- Visualize Docker image details
- Share insights with stakeholders
- Keep audit trails for compliance

> **Chaos Event:**  
> “No reports found. Jenkins build fails.”

---

## ✅ What You’ll Do

✅ Generate a Docker analysis HTML report.  
✅ Archive the report as a Jenkins artifact.  
✅ View reports directly from Jenkins UI.

---

## ✅ How to Run

1. Ensure Docker and Python are available in Jenkins.

2. Place your report generator script in:
    ```
    workshop_tools/generate_docker_report.py
    ```

3. Run your Jenkins job with this pipeline.

---

## ✅ Chaos Fixes

- Double-check report paths.  
- Avoid workspace clean-up between stages.  
- Ensure Jenkins has permission to read/write the `reports/` folder.

---

## ✅ Expected Output

✅ Console log should show:
````

🚀 Generating Docker analysis report...
📊 Archiving Docker HTML report...

````

✅ In Jenkins UI:
- Navigate to **Artifacts**
- Click to download or view:
    ```
    reports/version_3/docker_report.html
    ```

---

## ✅ Best Practices

- Always fingerprint important artifacts.  
- Clean up old reports to save disk space.  
- Store reports under consistent paths for easier archiving.

---
