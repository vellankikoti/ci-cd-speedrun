#!/usr/bin/env python3
"""
Enterprise-Grade Report Generator for CI/CD Chaos Workshop
Generates beautiful, self-contained HTML reports with modern design
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET


class EnterpriseReportGenerator:
    """Generate stunning enterprise-grade HTML reports"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        self.scenarios = [
            {
                "id": "config_validation", 
                "name": "Config Validation", 
                "icon": "⚙️",
                "color": "#3498db"
            },
            {
                "id": "api_health", 
                "name": "API Health Check", 
                "icon": "🏥",
                "color": "#2ecc71"
            },
            {
                "id": "postgres", 
                "name": "Postgres Database", 
                "icon": "🐘",
                "color": "#9b59b6"
            },
            {
                "id": "redis", 
                "name": "Redis Cache", 
                "icon": "📦",
                "color": "#e74c3c"
            },
            {
                "id": "secret_scan", 
                "name": "Secret Scanning", 
                "icon": "🔐",
                "color": "#f39c12"
            }
        ]
    
    def get_css_styles(self) -> str:
        """Get modern CSS styles for reports"""
        return """
/* Enterprise Report Styles */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
    --info-color: #3498db;
    --light-bg: #f8f9fa;
    --dark-bg: #2c3e50;
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --card-shadow-hover: 0 8px 15px rgba(0, 0, 0, 0.2);
    --border-radius: 8px;
    --transition: all 0.3s ease;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    line-height: 1.6;
    color: var(--primary-color);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    overflow: hidden;
}

.header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><pattern id="grain" width="100" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="20" fill="url(%23grain)"/></svg>');
    opacity: 0.1;
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.header .subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    position: relative;
    z-index: 1;
}

.build-info {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    margin: 1rem -2rem -2rem -2rem;
    backdrop-filter: blur(10px);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    background: var(--light-bg);
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    text-align: center;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--secondary-color);
}

.stat-card.success::before { background: var(--success-color); }
.stat-card.danger::before { background: var(--danger-color); }
.stat-card.warning::before { background: var(--warning-color); }

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.scenarios-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
}

.scenario-card {
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    overflow: hidden;
    transition: var(--transition);
}

.scenario-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--card-shadow-hover);
}

.scenario-header {
    padding: 1.5rem;
    border-left: 4px solid var(--secondary-color);
    position: relative;
}

.scenario-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.scenario-icon {
    font-size: 1.5rem;
}

.scenario-status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-passed {
    background: var(--success-color);
    color: white;
}

.status-failed {
    background: var(--danger-color);
    color: white;
}

.status-skipped {
    background: #95a5a6;
    color: white;
}

.scenario-body {
    padding: 1.5rem;
    padding-top: 0;
}

.test-summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}

.test-metric {
    text-align: center;
    padding: 0.75rem;
    background: var(--light-bg);
    border-radius: var(--border-radius);
}

.test-metric-number {
    font-size: 1.5rem;
    font-weight: 700;
}

.test-metric-label {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.25rem;
}

.progress-bar {
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin: 1rem 0;
}

.progress-fill {
    height: 100%;
    background: var(--success-color);
    transition: width 0.5s ease;
}

.scenario-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}

.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--border-radius);
    text-decoration: none;
    font-weight: 600;
    transition: var(--transition);
    cursor: pointer;
    text-align: center;
}

.btn-primary {
    background: var(--secondary-color);
    color: white;
}

.btn-primary:hover {
    background: #2980b9;
    transform: translateY(-1px);
}

.btn-outline {
    background: transparent;
    border: 2px solid var(--secondary-color);
    color: var(--secondary-color);
}

.btn-outline:hover {
    background: var(--secondary-color);
    color: white;
}

.test-details {
    background: white;
    margin: 1.5rem 0;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
    overflow: hidden;
}

.test-item {
    border-bottom: 1px solid #eee;
    padding: 1rem 1.5rem;
    transition: var(--transition);
}

.test-item:hover {
    background: var(--light-bg);
}

.test-item:last-child {
    border-bottom: none;
}

.test-name {
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.test-duration {
    font-size: 0.9rem;
    color: #666;
    background: var(--light-bg);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}

.test-description {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.error-details {
    background: #fff5f5;
    border: 1px solid #fed7d7;
    border-radius: var(--border-radius);
    padding: 1rem;
    margin-top: 0.5rem;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.85rem;
    color: var(--danger-color);
    white-space: pre-wrap;
    overflow-x: auto;
}

.footer {
    background: var(--light-bg);
    padding: 2rem;
    text-align: center;
    color: #666;
    border-top: 1px solid #eee;
}

.theme-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: white;
    border: none;
    box-shadow: var(--card-shadow);
    cursor: pointer;
    font-size: 1.5rem;
    transition: var(--transition);
    z-index: 1000;
}

.theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: var(--card-shadow-hover);
}

/* Dark Theme */
[data-theme="dark"] {
    --primary-color: #ecf0f1;
    --light-bg: #34495e;
    color: var(--primary-color);
}

[data-theme="dark"] body {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
}

[data-theme="dark"] .container {
    background: #2c3e50;
}

[data-theme="dark"] .stat-card,
[data-theme="dark"] .scenario-card,
[data-theme="dark"] .test-details {
    background: #34495e;
    color: var(--primary-color);
}

[data-theme="dark"] .test-item:hover {
    background: #3d566e;
}

/* Responsive Design */
@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        padding: 1rem;
    }
    
    .scenarios-grid {
        grid-template-columns: 1fr;
        padding: 1rem;
    }
    
    .header h1 {
        font-size: 2rem;
    }
    
    .test-summary {
        grid-template-columns: 1fr;
    }
}

/* Chart Styles */
.chart-container {
    position: relative;
    height: 200px;
    margin: 1rem 0;
}

.chart {
    width: 100%;
    height: 100%;
}

/* Animations */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: slideIn 0.6s ease-out;
}

/* Loading States */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid var(--secondary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
"""

    def get_javascript(self) -> str:
        """Get JavaScript for interactive features"""
        return """
// Enterprise Report JavaScript
class ReportEnhancer {
    constructor() {
        this.initThemeToggle();
        this.initAnimations();
        this.initCharts();
    }

    initThemeToggle() {
        const toggle = document.querySelector('.theme-toggle');
        if (!toggle) return;

        const currentTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', currentTheme);
        toggle.textContent = currentTheme === 'dark' ? '☀️' : '🌙';

        toggle.addEventListener('click', () => {
            const theme = document.documentElement.getAttribute('data-theme');
            const newTheme = theme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            toggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        });
    }

    initAnimations() {
        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        });

        document.querySelectorAll('.scenario-card, .stat-card').forEach(el => {
            observer.observe(el);
        });

        // Progress bar animations
        setTimeout(() => {
            document.querySelectorAll('.progress-fill').forEach(bar => {
                const width = bar.getAttribute('data-width');
                bar.style.width = width + '%';
            });
        }, 500);
    }

    initCharts() {
        // Simple SVG chart creation
        this.createPieCharts();
        this.createBarCharts();
    }

    createPieCharts() {
        document.querySelectorAll('.pie-chart').forEach(container => {
            const passed = parseInt(container.dataset.passed || 0);
            const failed = parseInt(container.dataset.failed || 0);
            const total = passed + failed;
            
            if (total === 0) return;

            const passedPercentage = (passed / total) * 100;
            const radius = 45;
            const circumference = 2 * Math.PI * radius;
            const strokeDasharray = circumference;
            const strokeDashoffset = circumference - (passedPercentage / 100) * circumference;

            container.innerHTML = `
                <svg width="120" height="120" class="chart">
                    <circle cx="60" cy="60" r="${radius}" fill="transparent" 
                            stroke="#e9ecef" stroke-width="10"/>
                    <circle cx="60" cy="60" r="${radius}" fill="transparent" 
                            stroke="var(--success-color)" stroke-width="10"
                            stroke-dasharray="${strokeDasharray}"
                            stroke-dashoffset="${strokeDashoffset}"
                            transform="rotate(-90 60 60)"
                            style="transition: stroke-dashoffset 1s ease-in-out"/>
                    <text x="60" y="65" text-anchor="middle" font-size="16" font-weight="bold" fill="var(--primary-color)">
                        ${Math.round(passedPercentage)}%
                    </text>
                </svg>
            `;
        });
    }

    createBarCharts() {
        document.querySelectorAll('.bar-chart').forEach(container => {
            const data = JSON.parse(container.dataset.chart || '[]');
            if (data.length === 0) return;

            const maxValue = Math.max(...data.map(d => d.value));
            const barHeight = 150;
            const barWidth = 30;
            const spacing = 40;
            const chartWidth = data.length * spacing;

            let svg = `<svg width="${chartWidth}" height="${barHeight + 40}" class="chart">`;
            
            data.forEach((item, index) => {
                const height = (item.value / maxValue) * barHeight;
                const x = index * spacing + 5;
                const y = barHeight - height;
                
                svg += `
                    <rect x="${x}" y="${y}" width="${barWidth}" height="${height}" 
                          fill="var(--secondary-color)" rx="2"/>
                    <text x="${x + barWidth/2}" y="${barHeight + 15}" 
                          text-anchor="middle" font-size="10" fill="var(--primary-color)">
                        ${item.label}
                    </text>
                    <text x="${x + barWidth/2}" y="${y - 5}" 
                          text-anchor="middle" font-size="10" fill="var(--primary-color)">
                        ${item.value}
                    </text>
                `;
            });
            
            svg += '</svg>';
            container.innerHTML = svg;
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ReportEnhancer();
});

// Utility functions
function toggleDetails(element) {
    const details = element.nextElementSibling;
    if (details && details.classList.contains('error-details')) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show toast notification
        const toast = document.createElement('div');
        toast.textContent = 'Copied to clipboard!';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            z-index: 1001;
            animation: slideIn 0.3s ease-out;
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    });
}
"""

    def parse_pytest_json(self, json_file: Path) -> Dict[str, Any]:
        """Parse pytest JSON report"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            tests = []
            for test in data.get('tests', []):
                tests.append({
                    'name': test.get('nodeid', '').split('::')[-1],
                    'outcome': test.get('outcome', 'unknown'),
                    'duration': test.get('duration', 0),
                    'file': test.get('nodeid', '').split('::')[0],
                    'error': test.get('call', {}).get('longrepr', '') if test.get('outcome') == 'failed' else None
                })
            
            summary = data.get('summary', {})
            return {
                'tests': tests,
                'total': summary.get('total', 0),
                'passed': summary.get('passed', 0),
                'failed': summary.get('failed', 0),
                'skipped': summary.get('skipped', 0),
                'duration': data.get('duration', 0),
                'created': data.get('created', datetime.now().isoformat())
            }
        except Exception as e:
            print(f"Error parsing {json_file}: {e}")
            return self.get_empty_report()

    def get_empty_report(self) -> Dict[str, Any]:
        """Get empty report structure"""
        return {
            'tests': [],
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'duration': 0,
            'created': datetime.now().isoformat()
        }

    def generate_scenario_report(self, scenario: Dict[str, str], test_data: Dict[str, Any], mode: str = 'pass') -> str:
        """Generate individual scenario report"""
        status = 'passed' if test_data['failed'] == 0 else 'failed'
        status_class = 'status-passed' if status == 'passed' else 'status-failed'
        
        # Calculate pass rate
        pass_rate = (test_data['passed'] / max(test_data['total'], 1)) * 100
        
        # Generate test details HTML
        test_details_html = ""
        for test in test_data['tests']:
            error_html = ""
            if test['error']:
                error_html = f"""
                <div class="error-details" style="display: none;">
                    {self.escape_html(test['error'])}
                </div>
                """
            
            test_icon = "✅" if test['outcome'] == 'passed' else "❌" if test['outcome'] == 'failed' else "⏭️"
            test_details_html += f"""
            <div class="test-item">
                <div class="test-name">
                    <span>{test_icon} {test['name']}</span>
                    <span class="test-duration">{test['duration']:.2f}s</span>
                </div>
                <div class="test-description">
                    Test outcome: <strong>{test['outcome'].title()}</strong> | 
                    File: <code>{test['file']}</code>
                </div>
                {error_html}
            </div>
            """

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎪 CI/CD Chaos Workshop - Dashboard</title>
    <style>{self.get_css_styles()}</style>
</head>
<body>
    <button class="theme-toggle" title="Toggle theme">🌙</button>
    
    <div class="container">
        <div class="header">
            <h1>🎪 CI/CD Chaos Workshop</h1>
            <div class="subtitle">Enterprise Test Execution Dashboard</div>
            <div class="build-info">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                <strong>Repository:</strong> github.com/vellankikoti/ci-cd-chaos-workshop |
                <strong>Branch:</strong> phase-3-jenkins
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len([s for s in scenario_reports.values() if s.get('total', 0) > 0])}</div>
                <div class="stat-label">Scenarios Executed</div>
            </div>
            <div class="stat-card success">
                <div class="stat-number">{total_tests}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card success">
                <div class="stat-number">{total_passed}</div>
                <div class="stat-label">Tests Passed</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-number">{total_failed}</div>
                <div class="stat-label">Tests Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{overall_pass_rate:.1f}%</div>
                <div class="stat-label">Overall Pass Rate</div>
            </div>
        </div>

        <div style="padding: 2rem;">
            <h2>📊 Test Execution Overview</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">
                <div>
                    <h3>Overall Test Distribution</h3>
                    <div class="pie-chart" data-passed="{total_passed}" data-failed="{total_failed}"></div>
                </div>
                <div>
                    <h3>Scenario Performance</h3>
                    <div class="bar-chart" data-chart='[
                        {{"label": "Config", "value": {scenario_reports.get("config_validation", {}).get("total", 0)}}},
                        {{"label": "API", "value": {scenario_reports.get("api_health", {}).get("total", 0)}}},
                        {{"label": "DB", "value": {scenario_reports.get("postgres", {}).get("total", 0)}}},
                        {{"label": "Cache", "value": {scenario_reports.get("redis", {}).get("total", 0)}}},
                        {{"label": "Security", "value": {scenario_reports.get("secret_scan", {}).get("total", 0)}}}
                    ]'></div>
                </div>
            </div>
        </div>

        <div style="padding: 0 2rem 2rem;">
            <h2>🎯 Test Scenarios</h2>
            <div class="scenarios-grid">
                {scenario_cards_html}
            </div>
        </div>

        <div class="footer">
            <p>🎪 <strong>CI/CD Chaos Workshop</strong> - Enterprise Test Dashboard</p>
            <p>Master CI/CD resilience through controlled chaos engineering</p>
            <p style="margin-top: 1rem;">
                <strong>🎓 Learning Objectives:</strong> Build bulletproof pipelines | Handle real-world failures | 
                Generate enterprise reports | Master chaos engineering
            </p>
        </div>
    </div>

    <script>{self.get_javascript()}</script>
</body>
</html>
        """
        return html

    def escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return ""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))

    def generate_all_reports(self, build_params: Dict[str, bool] = None):
        """Generate all reports based on available JSON files"""
        if build_params is None:
            # Default parameters - assume all scenarios enabled in pass mode
            build_params = {
                'RUN_CONFIG_VALIDATION': True, 'CONFIG_VALIDATION_PASS': True,
                'RUN_API_HEALTH': True, 'API_HEALTH_PASS': True,
                'RUN_POSTGRES': True, 'POSTGRES_PASS': True,
                'RUN_REDIS': True, 'REDIS_PASS': True,
                'RUN_SECRET_SCAN': True, 'SECRET_SCAN_PASS': True,
            }

        scenario_reports = {}
        
        # Generate individual scenario reports
        for scenario in self.scenarios:
            scenario_id = scenario['id']
            
            # Check if scenario is enabled
            run_param = f"RUN_{scenario_id.upper()}"
            pass_param = f"{scenario_id.upper()}_PASS"
            
            if not build_params.get(run_param, True):
                continue
                
            mode = 'pass' if build_params.get(pass_param, True) else 'fail'
            json_file = self.reports_dir / f"{scenario_id}_{mode}_report.json"
            
            if json_file.exists():
                test_data = self.parse_pytest_json(json_file)
                scenario_reports[scenario_id] = test_data
                
                # Generate individual report
                report_html = self.generate_scenario_report(scenario, test_data, mode)
                html_file = self.reports_dir / f"{scenario_id}_{mode}_report.html"
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(report_html)
                
                print(f"✅ Generated: {html_file}")
            else:
                print(f"⚠️ JSON file not found: {json_file}")
                scenario_reports[scenario_id] = self.get_empty_report()

        # Generate main dashboard
        dashboard_html = self.generate_dashboard(scenario_reports)
        dashboard_file = self.reports_dir / "index.html"
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        print(f"🎉 Generated main dashboard: {dashboard_file}")
        return dashboard_file, scenario_reports


def main():
    """Main function for standalone execution"""
    import sys
    
    reports_dir = sys.argv[1] if len(sys.argv) > 1 else "reports"
    generator = EnterpriseReportGenerator(reports_dir)
    
    # Try to read build parameters from environment or file
    build_params = {}
    
    # Read from environment variables (Jenkins sets these)
    env_params = [
        'RUN_CONFIG_VALIDATION', 'CONFIG_VALIDATION_PASS',
        'RUN_API_HEALTH', 'API_HEALTH_PASS',
        'RUN_POSTGRES', 'POSTGRES_PASS',
        'RUN_REDIS', 'REDIS_PASS',
        'RUN_SECRET_SCAN', 'SECRET_SCAN_PASS'
    ]
    
    for param in env_params:
        env_value = os.getenv(param)
        if env_value is not None:
            build_params[param] = env_value.lower() == 'true'
    
    dashboard_file, reports = generator.generate_all_reports(build_params)
    
    print("\n🎪 Enterprise Report Generation Complete!")
    print(f"📊 Dashboard: {dashboard_file}")
    print(f"📈 Generated {len(reports)} scenario reports")
    print("\n🎯 Next steps:")
    print("1. Open index.html in your browser")
    print("2. Navigate through individual scenario reports")
    print("3. Toggle dark/light theme with the button")
    print("4. Share with your team for maximum impact!")


if __name__ == "__main__":
    main()
.0">
    <title>{scenario['icon']} {scenario['name']} - Test Report</title>
    <style>{self.get_css_styles()}</style>
</head>
<body>
    <button class="theme-toggle" title="Toggle theme">🌙</button>
    
    <div class="container">
        <div class="header">
            <h1>{scenario['icon']} {scenario['name']}</h1>
            <div class="subtitle">Test Execution Report - {mode.title()} Mode</div>
            <div class="build-info">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                <strong>Duration:</strong> {test_data['duration']:.2f}s |
                <strong>Mode:</strong> {mode.title()}
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card success">
                <div class="stat-number">{test_data['total']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card success">
                <div class="stat-number">{test_data['passed']}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-number">{test_data['failed']}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{pass_rate:.1f}%</div>
                <div class="stat-label">Pass Rate</div>
            </div>
        </div>

        <div style="padding: 2rem;">
            <h2>📊 Test Results Overview</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 2rem 0;">
                <div>
                    <h3>Pass/Fail Distribution</h3>
                    <div class="pie-chart" data-passed="{test_data['passed']}" data-failed="{test_data['failed']}"></div>
                </div>
                <div>
                    <h3>Execution Time Analysis</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" data-width="{pass_rate}"></div>
                    </div>
                    <p>Average test duration: {(test_data['duration'] / max(test_data['total'], 1)):.2f}s</p>
                </div>
            </div>

            <h2>🔍 Detailed Test Results</h2>
            <div class="test-details">
                {test_details_html if test_details_html else '<div class="test-item">No tests found</div>'}
            </div>
        </div>

        <div class="footer">
            <p>🎪 CI/CD Chaos Workshop - Scenario Report</p>
            <p>This report was generated automatically by the Enterprise Report Generator</p>
        </div>
    </div>

    <script>{self.get_javascript()}</script>
</body>
</html>
        """
        return html

    def generate_dashboard(self, scenario_reports: Dict[str, Dict[str, Any]]) -> str:
        """Generate main dashboard with all scenarios"""
        total_tests = sum(report.get('total', 0) for report in scenario_reports.values())
        total_passed = sum(report.get('passed', 0) for report in scenario_reports.values())
        total_failed = sum(report.get('failed', 0) for report in scenario_reports.values())
        overall_pass_rate = (total_passed / max(total_tests, 1)) * 100
        
        # Generate scenario cards
        scenario_cards_html = ""
        for scenario in self.scenarios:
            scenario_id = scenario['id']
            report_data = scenario_reports.get(scenario_id, self.get_empty_report())
            
            if report_data['total'] > 0:
                status = 'passed' if report_data['failed'] == 0 else 'failed'
                status_class = 'status-passed' if status == 'passed' else 'status-failed'
                pass_rate = (report_data['passed'] / report_data['total']) * 100
            else:
                status = 'skipped'
                status_class = 'status-skipped'
                pass_rate = 0

            scenario_cards_html += f"""
            <div class="scenario-card" style="border-left-color: {scenario['color']}">
                <div class="scenario-header">
                    <div class="scenario-title">
                        <span class="scenario-icon">{scenario['icon']}</span>
                        <span>{scenario['name']}</span>
                        <span class="scenario-status {status_class}">{status}</span>
                    </div>
                </div>
                <div class="scenario-body">
                    <div class="test-summary">
                        <div class="test-metric">
                            <div class="test-metric-number">{report_data['total']}</div>
                            <div class="test-metric-label">Total</div>
                        </div>
                        <div class="test-metric">
                            <div class="test-metric-number">{report_data['passed']}</div>
                            <div class="test-metric-label">Passed</div>
                        </div>
                        <div class="test-metric">
                            <div class="test-metric-number">{report_data['failed']}</div>
                            <div class="test-metric-label">Failed</div>
                        </div>
                    </div>
                    
                    <div class="progress-bar">
                        <div class="progress-fill" data-width="{pass_rate}" style="background: {scenario['color']}"></div>
                    </div>
                    
                    <div class="scenario-actions">
                        <a href="{scenario_id}_pass_report.html" class="btn btn-primary">📊 View Report</a>
                        <a href="{scenario_id}_fail_report.html" class="btn btn-outline">❌ Fail Mode</a>
                    </div>
                </div>
            </div>
            """

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1