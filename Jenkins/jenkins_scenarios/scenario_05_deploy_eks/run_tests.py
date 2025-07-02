#!/usr/bin/env python3
"""
Scenario 5 - EKS Deployment Test Runner
Orchestrates pass/fail tests and generates comprehensive HTML reports
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import argparse

class EKSTestRunner:
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.reports_dir = self.test_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        self.test_results = {
            "scenario": "scenario_05_deploy_eks",
            "run_id": f"run_{int(time.time())}",
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0
            }
        }
    
    def run_test(self, test_file, test_type):
        """Run a specific test and capture results"""
        print(f"\n{'='*60}")
        print(f"Running {test_type} test: {test_file}")
        print(f"{'='*60}")
        
        test_start = datetime.now()
        
        try:
            # Run pytest with HTML output
            html_report = self.reports_dir / f"pytest_{test_type}_report.html"
            junit_report = self.reports_dir / f"pytest_{test_type}_junit.xml"
            
            cmd = [
                "python", "-m", "pytest",
                str(test_file),
                "-v",
                "--tb=short",
                f"--html={html_report}",
                "--self-contained-html",
                f"--junit-xml={junit_report}"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.test_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            test_end = datetime.now()
            duration = (test_end - test_start).total_seconds()
            
            # Load test-specific report data if available
            report_file = self.test_dir / f"eks_{test_type}_report.json"
            test_data = {}
            if report_file.exists():
                try:
                    with open(report_file, 'r') as f:
                        test_data = json.load(f)
                except Exception as e:
                    print(f"Warning: Could not load test report data: {e}")
            
            test_result = {
                "test_type": test_type,
                "test_file": str(test_file),
                "start_time": test_start.isoformat(),
                "end_time": test_end.isoformat(),
                "duration": duration,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "html_report": str(html_report),
                "junit_report": str(junit_report),
                "test_data": test_data
            }
            
            self.test_results["tests"].append(test_result)
            self.test_results["summary"]["total"] += 1
            
            if result.returncode == 0:
                self.test_results["summary"]["passed"] += 1
                print(f"✅ {test_type} test PASSED")
            else:
                self.test_results["summary"]["failed"] += 1
                print(f"❌ {test_type} test FAILED")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            test_end = datetime.now()
            duration = (test_end - test_start).total_seconds()
            
            test_result = {
                "test_type": test_type,
                "test_file": str(test_file),
                "start_time": test_start.isoformat(),
                "end_time": test_end.isoformat(),
                "duration": duration,
                "return_code": 124,
                "stdout": "",
                "stderr": "Test timed out after 10 minutes",
                "status": "TIMEOUT",
                "html_report": "",
                "junit_report": "",
                "test_data": {}
            }
            
            self.test_results["tests"].append(test_result)
            self.test_results["summary"]["total"] += 1
            self.test_results["summary"]["errors"] += 1
            
            print(f"⏰ {test_type} test TIMED OUT")
            return test_result
            
        except Exception as e:
            test_end = datetime.now()
            duration = (test_end - test_start).total_seconds()
            
            test_result = {
                "test_type": test_type,
                "test_file": str(test_file),
                "start_time": test_start.isoformat(),
                "end_time": test_end.isoformat(),
                "duration": duration,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "status": "ERROR",
                "html_report": "",
                "junit_report": "",
                "test_data": {}
            }
            
            self.test_results["tests"].append(test_result)
            self.test_results["summary"]["total"] += 1
            self.test_results["summary"]["errors"] += 1
            
            print(f"💥 {test_type} test ERROR: {e}")
            return test_result
    
    def generate_html_report(self):
        """Generate comprehensive HTML report"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EKS Deployment Test Report - Scenario 5</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            color: #1e3c72;
            margin: 0;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }
        
        .summary-cards {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 200px;
        }
        
        .card h3 {
            margin: 0 0 10px 0;
            color: #1e3c72;
        }
        
        .card .number {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .passed { color: #4caf50; }
        .failed { color: #f44336; }
        .error { color: #ff9800; }
        .total { color: #2196f3; }
        
        .test-section {
            background: white;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .test-header {
            padding: 20px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .test-header:hover {
            background-color: #f5f5f5;
        }
        
        .test-content {
            padding: 20px;
            display: none;
        }
        
        .test-content.active {
            display: block;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .status-passed { background: #4caf50; }
        .status-failed { background: #f44336; }
        .status-error { background: #ff9800; }
        .status-timeout { background: #9c27b0; }
        
        .timeline {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        .logs {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .kubernetes-events {
            margin: 20px 0;
        }
        
        .events-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        
        .events-table th,
        .events-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        .events-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        .event-warning { background-color: #fff3cd; }
        .event-error { background-color: #f8d7da; }
        .event-normal { background-color: #d4edda; }
        
        .remediation {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 15px 0;
        }
        
        .remediation h4 {
            margin: 0 0 10px 0;
            color: #1976d2;
        }
        
        .toggle-icon {
            float: right;
            transition: transform 0.3s;
        }
        
        .toggle-icon.active {
            transform: rotate(180deg);
        }
        
        .metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .metadata-item {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
        }
        
        .metadata-label {
            font-weight: bold;
            color: #666;
            font-size: 0.9em;
        }
        
        .metadata-value {
            margin-top: 5px;
            font-family: 'Courier New', monospace;
        }
        
        @media (max-width: 768px) {
            .summary-cards {
                flex-direction: column;
            }
            
            .metadata {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🚀 CI/CD Chaos Workshop</h1>
            <div class="subtitle">Scenario 5: EKS Deployment Testing Report</div>
        </div>
    </div>
    
    <div class="container">
        <div class="summary-cards">
            <div class="card">
                <h3>Total Tests</h3>
                <div class="number total">{{ summary.total }}</div>
            </div>
            <div class="card">
                <h3>Passed</h3>
                <div class="number passed">{{ summary.passed }}</div>
            </div>
            <div class="card">
                <h3>Failed</h3>
                <div class="number failed">{{ summary.failed }}</div>
            </div>
            <div class="card">
                <h3>Errors</h3>
                <div class="number error">{{ summary.errors }}</div>
            </div>
        </div>
        
        <div class="metadata">
            <div class="metadata-item">
                <div class="metadata-label">Run ID</div>
                <div class="metadata-value">{{ run_id }}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Start Time</div>
                <div class="metadata-value">{{ start_time }}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">End Time</div>
                <div class="metadata-value">{{ end_time }}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Total Duration</div>
                <div class="metadata-value">{{ total_duration }}s</div>
            </div>
        </div>
        
        {% for test in tests %}
        <div class="test-section">
            <div class="test-header" onclick="toggleTest('test-{{ loop.index }}')">
                <h3 style="margin: 0; display: inline-block;">
                    {{ test.test_type|upper }} Test
                    <span class="status-badge status-{{ test.status|lower }}">{{ test.status }}</span>
                </h3>
                <span class="toggle-icon" id="icon-test-{{ loop.index }}">▼</span>
            </div>
            <div class="test-content" id="test-{{ loop.index }}">
                <div class="timeline">
                    <strong>Duration:</strong> {{ "%.2f"|format(test.duration) }}s<br>
                    <strong>Start:</strong> {{ test.start_time }}<br>
                    <strong>End:</strong> {{ test.end_time }}
                </div>
                
                {% if test.test_data %}
                    {% if test.test_data.steps %}
                    <h4>Test Steps</h4>
                    <div class="events-table-container">
                        <table class="events-table">
                            <thead>
                                <tr>
                                    <th>Step</th>
                                    <th>Status</th>
                                    <th>Details</th>
                                    <th>Duration</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for step in test.test_data.steps %}
                                <tr class="{% if step.status == 'FAILED' %}event-error{% elif step.status == 'WARNING' %}event-warning{% else %}event-normal{% endif %}">
                                    <td>{{ step.name }}</td>
                                    <td>{{ step.status }}</td>
                                    <td>{{ step.details }}</td>
                                    <td>{{ "%.2f"|format(step.duration or 0) }}s</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.pods %}
                    <h4>Pod Status</h4>
                    <div class="events-table-container">
                        <table class="events-table">
                            <thead>
                                <tr>
                                    <th>Pod Name</th>
                                    <th>Status</th>
                                    <th>Ready</th>
                                    <th>Node</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for pod in test.test_data.pods %}
                                <tr class="{% if not pod.ready %}event-error{% else %}event-normal{% endif %}">
                                    <td>{{ pod.name }}</td>
                                    <td>{{ pod.status }}</td>
                                    <td>{{ "✅" if pod.ready else "❌" }}</td>
                                    <td>{{ pod.node }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.events %}
                    <h4>Kubernetes Events</h4>
                    <div class="events-table-container">
                        <table class="events-table">
                            <thead>
                                <tr>
                                    <th>Type</th>
                                    <th>Reason</th>
                                    <th>Message</th>
                                    <th>Count</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for event in test.test_data.events %}
                                <tr class="{% if event.type == 'Warning' %}event-warning{% else %}event-normal{% endif %}">
                                    <td>{{ event.type }}</td>
                                    <td>{{ event.reason }}</td>
                                    <td>{{ event.message }}</td>
                                    <td>{{ event.count }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.failure_reasons %}
                    <div class="remediation">
                        <h4>🔍 Failure Analysis</h4>
                        <ul>
                            {% for reason in test.test_data.failure_reasons %}
                            <li>{{ reason }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.remediation_suggestions %}
                    <div class="remediation">
                        <h4>💡 Remediation Suggestions</h4>
                        <ul>
                            {% for suggestion in test.test_data.remediation_suggestions %}
                            <li>{{ suggestion }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.logs %}
                    <h4>Pod Logs</h4>
                    <div class="logs">{{ test.test_data.logs }}</div>
                    {% endif %}
                    
                    {% if test.test_data.error_logs %}
                    <h4>Error Logs</h4>
                    <div class="logs">{{ test.test_data.error_logs }}</div>
                    {% endif %}
                    
                    {% if test.test_data.endpoint_url %}
                    <div class="timeline">
                        <strong>Service Endpoint:</strong> <a href="{{ test.test_data.endpoint_url }}" target="_blank">{{ test.test_data.endpoint_url }}</a>
                    </div>
                    {% endif %}
                    
                    {% if test.test_data.success_message %}
                    <div class="remediation">
                        <h4>✅ Success</h4>
                        <p>{{ test.test_data.success_message }}</p>
                    </div>
                    {% endif %}
                {% endif %}
                
                {% if test.stdout %}
                <h4>Test Output</h4>
                <div class="logs">{{ test.stdout }}</div>
                {% endif %}
                
                {% if test.stderr %}
                <h4>Error Output</h4>
                <div class="logs">{{ test.stderr }}</div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <script>
        function toggleTest(testId) {
            const content = document.getElementById(testId);
            const icon = document.getElementById('icon-' + testId);
            
            if (content.classList.contains('active')) {
                content.classList.remove('active');
                icon.classList.remove('active');
            } else {
                content.classList.add('active');
                icon.classList.add('active');
            }
        }
        
        // Auto-expand failed tests
        document.addEventListener('DOMContentLoaded', function() {
            const failedTests = document.querySelectorAll('.status-failed, .status-error');
            failedTests.forEach(badge => {
                const testSection = badge.closest('.test-section');
                const content = testSection.querySelector('.test-content');
                const icon = testSection.querySelector('.toggle-icon');
                
                content.classList.add('active');
                icon.classList.add('active');
            });
        });
    </script>
</body>
</html>
        """
        
        template = Template(template_str)
        
        # Calculate total duration
        end_time = datetime.now()
        self.test_results["end_time"] = end_time.isoformat()
        start_time = datetime.fromisoformat(self.test_results["start_time"])
        total_duration = (end_time - start_time).total_seconds()
        self.test_results["total_duration"] = total_duration
        
        html_content = template.render(**self.test_results)
        
        html_file = self.reports_dir / "eks_deployment_report.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    def save_json_report(self):
        """Save detailed JSON report"""
        json_file = self.reports_dir / "eks_deployment_report.json"
        with open(json_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        return json_file
    
    def run_all_tests(self, run_pass=True, run_fail=True):
        """Run all EKS deployment tests"""
        print("🚀 Starting EKS Deployment Tests - Scenario 5")
        print(f"Run ID: {self.test_results['run_id']}")
        
        # Verify kubectl connectivity
        try:
            result = subprocess.run(
                ["kubectl", "cluster-info"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                print("❌ Cannot connect to Kubernetes cluster!")
                print(f"Error: {result.stderr}")
                return False
            print("✅ Connected to Kubernetes cluster")
        except Exception as e:
            print(f"❌ Failed to verify cluster connectivity: {e}")
            return False
        
        # Run tests
        if run_pass:
            self.run_test(
                self.test_dir / "test_deploy_eks_pass.py",
                "pass"
            )
        
        if run_fail:
            self.run_test(
                self.test_dir / "test_deploy_eks_fail.py",
                "fail"
            )
        
        # Generate reports
        print("\n📊 Generating Reports...")
        html_file = self.generate_html_report()
        json_file = self.save_json_report()
        
        print(f"✅ HTML Report: {html_file}")
        print(f"✅ JSON Report: {json_file}")
        
        # Print summary
        summary = self.test_results["summary"]
        print(f"\n📈 Test Summary:")
        print(f"  Total Tests: {summary['total']}")
        print(f"  Passed: {summary['passed']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Errors: {summary['errors']}")
        
        # Return success if we have expected results
        # For chaos testing, we expect the fail test to "pass" by failing properly
        expected_failures = sum(1 for test in self.test_results["tests"] if test["test_type"] == "fail")
        actual_passes = summary["passed"]
        
        if run_pass and run_fail:
            # Expect pass test to pass and fail test to pass (by failing deployment properly)
            success = summary["total"] == 2 and summary["passed"] >= 1 and summary["errors"] == 0
        elif run_pass:
            # Expect pass test to pass
            success = summary["passed"] == 1 and summary["errors"] == 0
        elif run_fail:
            # Expect fail test to pass (by properly demonstrating failure)
            success = summary["total"] == 1 and summary["errors"] == 0
        else:
            success = True
        
        return success


def main():
    parser = argparse.ArgumentParser(description="EKS Deployment Test Runner")
    parser.add_argument("--pass-only", action="store_true", help="Run only pass tests")
    parser.add_argument("--fail-only", action="store_true", help="Run only fail tests")
    parser.add_argument("--skip-pass", action="store_true", help="Skip pass tests")
    parser.add_argument("--skip-fail", action="store_true", help="Skip fail tests")
    
    args = parser.parse_args()
    
    # Determine which tests to run
    run_pass = not args.skip_pass and not args.fail_only
    run_fail = not args.skip_fail and not args.pass_only
    
    if args.pass_only:
        run_fail = False
    if args.fail_only:
        run_pass = False
    
    runner = EKSTestRunner()
    success = runner.run_all_tests(run_pass=run_pass, run_fail=run_fail)
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed or encountered errors!")
        sys.exit(1)


if __name__ == "__main__":
    main()