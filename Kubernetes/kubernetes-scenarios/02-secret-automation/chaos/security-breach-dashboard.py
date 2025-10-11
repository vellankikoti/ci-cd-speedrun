#!/usr/bin/env python3
"""
💀 SECURITY BREACH SIMULATION DASHBOARD
"Watch your secrets get stolen in real-time!"

This dashboard visualizes what happens when you deploy with poor security practices.
Educational demonstration of security anti-patterns.
"""

from flask import Flask, render_template_string, jsonify
import subprocess
import json
import base64
from datetime import datetime
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💀 Security Breach Simulation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        .hacked-banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(90deg, #ff0000 0%, #8b0000 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            z-index: 1000;
            animation: pulse 2s infinite;
            box-shadow: 0 5px 20px rgba(255, 0, 0, 0.5);
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .container {
            max-width: 1400px;
            margin: 80px auto 0;
        }

        .header {
            text-align: center;
            padding: 30px 0;
            border: 3px solid #00ff00;
            border-radius: 10px;
            background: rgba(0, 255, 0, 0.05);
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px #00ff00;
        }

        .header p {
            font-size: 1.2em;
            color: #ff0000;
        }

        .breach-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .breach-card {
            background: rgba(255, 0, 0, 0.1);
            border: 2px solid #ff0000;
            border-radius: 10px;
            padding: 20px;
        }

        .breach-card h2 {
            color: #ff0000;
            margin-bottom: 15px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .exposed-secrets {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            border-left: 4px solid #ff0000;
        }

        .secret-item {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .secret-item:last-child {
            border-bottom: none;
        }

        .secret-label {
            color: #ffff00;
            font-weight: bold;
        }

        .secret-value {
            color: #ff0000;
            font-family: monospace;
            background: rgba(255, 0, 0, 0.2);
            padding: 5px 10px;
            border-radius: 3px;
        }

        .attack-log {
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 5px;
            max-height: 300px;
            overflow-y: auto;
            font-size: 0.9em;
        }

        .attack-entry {
            padding: 5px 0;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(-20px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .attack-entry.critical {
            color: #ff0000;
        }

        .attack-entry.warning {
            color: #ffff00;
        }

        .attack-entry.info {
            color: #00ff00;
        }

        .security-score {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #8b0000 0%, #ff0000 100%);
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .score-value {
            font-size: 5em;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
            margin-bottom: 10px;
        }

        .score-label {
            font-size: 1.5em;
            color: white;
        }

        .vulnerability-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }

        .vulnerability-card {
            background: rgba(139, 0, 0, 0.3);
            border: 2px solid #8b0000;
            border-radius: 10px;
            padding: 15px;
        }

        .vulnerability-card h3 {
            color: #ff6666;
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        .severity-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .severity-critical {
            background: #ff0000;
            color: white;
        }

        .severity-high {
            background: #ff6600;
            color: white;
        }

        .severity-medium {
            background: #ffaa00;
            color: black;
        }

        .glitch {
            animation: glitch 1s infinite;
        }

        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }

        .solution-banner {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
        }

        .solution-banner h2 {
            font-size: 2em;
            margin-bottom: 15px;
        }

        .solution-banner p {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="hacked-banner glitch">
        🚨 SECURITY BREACH IN PROGRESS 🚨
    </div>

    <div class="container">
        <div class="header">
            <h1>💀 CHAOS AGENT'S TROPHY ROOM</h1>
            <p>"Your secrets belong to me now!" - Chaos Agent</p>
        </div>

        <div class="security-score">
            <div class="score-value" id="security-score">0%</div>
            <div class="score-label">SECURITY SCORE</div>
            <p style="color: white; margin-top: 10px;">❌ FAILS ALL COMPLIANCE STANDARDS</p>
        </div>

        <div class="breach-grid">
            <div class="breach-card">
                <h2>🔓 EXPOSED SECRETS</h2>
                <div class="exposed-secrets" id="exposed-secrets">
                    <div class="secret-item">
                        <span class="secret-label">Loading exposed credentials...</span>
                    </div>
                </div>
            </div>

            <div class="breach-card">
                <h2>📊 LIVE ATTACK LOG</h2>
                <div class="attack-log" id="attack-log">
                    <div class="attack-entry info">[SYSTEM] Monitoring insecure deployment...</div>
                </div>
            </div>
        </div>

        <div class="vulnerability-grid" id="vulnerabilities">
            <!-- Populated by JavaScript -->
        </div>

        <div class="solution-banner">
            <h2>🦸 PYTHON SECURITY HERO TO THE RESCUE!</h2>
            <p>✅ Automated secret generation with cryptographic security</p>
            <p>✅ Kubernetes Secrets encryption at rest</p>
            <p>✅ Zero plain-text exposure - ever!</p>
            <p>✅ Automated secret rotation every 30 days</p>
            <p>✅ Network isolation - database internal only</p>
            <p>✅ Security contexts - non-root, dropped privileges</p>
            <p style="margin-top: 20px; font-size: 1.3em;">
                <strong>Run the hero solution:</strong>
                <code style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; display: block; margin-top: 10px;">
                    python3 hero-solution/deploy-secure-todo.py
                </code>
            </p>
        </div>
    </div>

    <script>
        let attackLogEntries = [];

        const vulnerabilities = [
            {
                title: "Plain-Text Passwords in YAML",
                severity: "CRITICAL",
                description: "Passwords committed to Git repository, visible to anyone with access",
                cvss: "9.8"
            },
            {
                title: "Database Exposed to Internet",
                severity: "CRITICAL",
                description: "MySQL accessible via NodePort 30306, no authentication required",
                cvss: "9.1"
            },
            {
                title: "Hardcoded API Keys",
                severity: "CRITICAL",
                description: "API keys, tokens, and secrets hardcoded in environment variables",
                cvss: "8.9"
            },
            {
                title: "No Secret Rotation",
                severity: "HIGH",
                description: "Compromised credentials remain valid forever",
                cvss: "7.5"
            },
            {
                title: "Root Container Execution",
                severity: "HIGH",
                description: "Containers running as root user (UID 0), privilege escalation possible",
                cvss: "8.2"
            },
            {
                title: "Secrets in ConfigMap",
                severity: "CRITICAL",
                description: "Sensitive data stored in ConfigMap (not encrypted at rest)",
                cvss: "9.0"
            },
            {
                title: "No Resource Limits",
                severity: "MEDIUM",
                description: "No CPU/memory limits, DoS attack vulnerability",
                cvss: "6.5"
            },
            {
                title: "No Network Policies",
                severity: "HIGH",
                description: "Unrestricted pod-to-pod communication, lateral movement possible",
                cvss: "7.8"
            }
        ];

        function renderVulnerabilities() {
            const container = document.getElementById('vulnerabilities');
            container.innerHTML = vulnerabilities.map(vuln => `
                <div class="vulnerability-card">
                    <h3>❌ ${vuln.title}</h3>
                    <span class="severity-badge severity-${vuln.severity.toLowerCase()}">${vuln.severity}</span>
                    <span class="severity-badge" style="background: #333; margin-left: 10px;">CVSS ${vuln.cvss}</span>
                    <p style="margin-top: 10px; color: #ccc;">${vuln.description}</p>
                </div>
            `).join('');
        }

        function addAttackLogEntry(message, severity = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const entry = `<div class="attack-entry ${severity}">[${timestamp}] ${message}</div>`;

            attackLogEntries.unshift(entry);
            if (attackLogEntries.length > 20) {
                attackLogEntries.pop();
            }

            document.getElementById('attack-log').innerHTML = attackLogEntries.join('');
        }

        function fetchExposedSecrets() {
            fetch('/api/secrets')
                .then(response => response.json())
                .then(data => {
                    const secretsContainer = document.getElementById('exposed-secrets');
                    secretsContainer.innerHTML = data.secrets.map(secret => `
                        <div class="secret-item">
                            <span class="secret-label">${secret.label}</span>
                            <span class="secret-value">${secret.value}</span>
                        </div>
                    `).join('');

                    // Update security score
                    document.getElementById('security-score').textContent = data.security_score + '%';

                    // Add to attack log
                    if (data.secrets.length > 0) {
                        addAttackLogEntry(`🚨 Extracted ${data.secrets.length} credentials from insecure deployment`, 'critical');
                    }
                })
                .catch(error => {
                    addAttackLogEntry('⚠️ Error extracting secrets (deployment may not exist)', 'warning');
                });
        }

        function simulateAttacks() {
            const attacks = [
                { msg: "🔍 Scanning for exposed services...", severity: "info" },
                { msg: "🎯 Found MySQL on NodePort 30306 - JACKPOT!", severity: "critical" },
                { msg: "💾 Extracting database credentials...", severity: "critical" },
                { msg: "🔓 Successfully accessed MySQL as root", severity: "critical" },
                { msg: "📥 Downloading user database...", severity: "critical" },
                { msg: "🔑 Found API keys in environment variables", severity: "critical" },
                { msg: "🌐 Accessing insecure-todo-service...", severity: "warning" },
                { msg: "📝 Reading ConfigMap with secrets...", severity: "critical" },
                { msg: "💳 Stripe API key extracted", severity: "critical" },
                { msg: "🔐 AWS credentials compromised", severity: "critical" },
                { msg: "🐙 GitHub token stolen", severity: "critical" },
                { msg: "⚡ Privilege escalation successful (root access)", severity: "critical" },
                { msg: "🚀 Installing cryptominer on compromised pods", severity: "critical" },
                { msg: "💰 Your cluster is now mining Bitcoin for Chaos Agent", severity: "critical" },
                { msg: "🎭 Game over! All secrets compromised.", severity: "critical" }
            ];

            let i = 0;
            const interval = setInterval(() => {
                if (i < attacks.length) {
                    addAttackLogEntry(attacks[i].msg, attacks[i].severity);
                    i++;
                } else {
                    clearInterval(interval);
                    addAttackLogEntry("👹 Chaos Agent owns your cluster. Good luck explaining this to compliance!", "critical");
                }
            }, 2000);
        }

        // Initialize
        renderVulnerabilities();
        fetchExposedSecrets();

        // Start simulated attacks
        setTimeout(simulateAttacks, 2000);

        // Refresh secrets every 10 seconds
        setInterval(fetchExposedSecrets, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the breach dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/secrets')
def get_secrets():
    """Extract exposed secrets from the insecure deployment"""
    secrets = []

    try:
        # Try to get secrets from the insecure namespace
        cmd = "kubectl get secret mysql-password -n insecure-todo -o json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            secret_data = json.loads(result.stdout)
            data = secret_data.get('data', {})

            # Decode base64 encoded secrets
            for key, value in data.items():
                decoded = base64.b64decode(value).decode('utf-8')
                secrets.append({
                    'label': f'Secret: {key}',
                    'value': decoded
                })

        # Try to get configmap "secrets"
        cmd = "kubectl get configmap app-secrets -n insecure-todo -o json"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            cm_data = json.loads(result.stdout)
            data = cm_data.get('data', {})

            for key, value in data.items():
                secrets.append({
                    'label': f'ConfigMap: {key}',
                    'value': value
                })

    except Exception as e:
        pass

    # Add some example exposed credentials
    if len(secrets) == 0:
        secrets = [
            {'label': 'MySQL Root Password', 'value': 'root_password_456'},
            {'label': 'MySQL User Password', 'value': 'super_secret_password_123'},
            {'label': 'API Key', 'value': 'api_key_hardcoded_in_yaml'},
            {'label': 'JWT Secret', 'value': 'jwt_secret_token_12345'},
            {'label': 'Admin Password', 'value': 'admin123'},
            {'label': 'Stripe API Key', 'value': 'sk_live_EXPOSED_API_KEY'},
            {'label': 'AWS Access Key', 'value': 'AKIAIOSFODNN7EXAMPLE'},
            {'label': 'GitHub Token', 'value': 'ghp_EXPOSED_GITHUB_TOKEN_1234567890'},
        ]

    return jsonify({
        'secrets': secrets,
        'security_score': 0,  # Complete failure
        'vulnerabilities': len(secrets),
        'timestamp': datetime.now().isoformat()
    })

def find_free_port(start_port=6000, max_attempts=100):
    """Find a free port starting from start_port"""
    import socket

    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue

    # Fallback to random port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Main function"""
    print("\n" + "="*70)
    print("💀 Security Breach Simulation Dashboard")
    print("="*70 + "\n")

    # Find available port
    port = find_free_port(6000)

    print("⚠️  WARNING: This dashboard simulates a security breach!")
    print("   It demonstrates what happens with poor security practices.")
    print("\n📊 Dashboard features:")
    print("   💀 Live secret extraction visualization")
    print("   🚨 Simulated attack log")
    print("   📋 Vulnerability assessment")
    print("   📈 Security score (spoiler: it's 0%)")
    print(f"\n🌐 URL: http://localhost:{port}")
    if port != 6000:
        print(f"   ℹ️  Port 6000 was busy, using port {port} instead")
    print("⌨️  Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()
