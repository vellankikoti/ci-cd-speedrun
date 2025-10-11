#!/usr/bin/env python3
"""
💀 SECURITY CHAOS DEMO - Scenario 02
"Your Secrets Belong to Me Now!" - Chaos Agent

This script demonstrates devastating security failures when secrets are mismanaged.
Educational demonstration of security anti-patterns - NEVER use these practices!
"""

import os
import sys
import time
import subprocess
from pathlib import Path

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.MAGENTA}{'='*70}{Colors.NC}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{text}{Colors.NC}")
    print(f"{Colors.MAGENTA}{'='*70}{Colors.NC}\n")

def print_step(text):
    """Print a step"""
    print(f"{Colors.CYAN}▶ {text}{Colors.NC}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")

def print_critical(text):
    """Print critical security issue"""
    print(f"{Colors.RED}{Colors.BOLD}🚨 CRITICAL: {text}{Colors.NC}")

def run_command(cmd, check=False):
    """Run command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e

def main():
    """Main chaos demo"""

    print_header("💀 KUBERNETES SECURITY CHAOS DEMO - Scenario 02")
    print_header("\"Your Secrets Belong to Me Now!\" - Chaos Agent")

    print(f"{Colors.CYAN}🎓 Learning Objectives:{Colors.NC}")
    print(f"   • See the devastating impact of poor secret management")
    print(f"   • Understand security vulnerabilities in Kubernetes")
    print(f"   • Learn why automated secret management is critical")
    print(f"   • Experience compliance failures firsthand")

    print(f"\n{Colors.RED}{Colors.BOLD}⚠️  EXTREME WARNING: This demonstrates CRITICAL security failures!{Colors.NC}")
    print(f"{Colors.YELLOW}   Every practice shown here is a real-world attack vector.{Colors.NC}")
    print(f"{Colors.YELLOW}   NEVER use these patterns in production!{Colors.NC}")

    input(f"\n{Colors.BOLD}Press ENTER to unleash the security chaos...{Colors.NC}")

    script_dir = Path(__file__).parent
    insecure_yaml = script_dir / "insecure-deployment.yaml"

    if not insecure_yaml.exists():
        print_error(f"Insecure YAML not found: {insecure_yaml}")
        sys.exit(1)

    # STEP 1: Show the insecure YAML
    print_header("STEP 1: The Security Nightmare Configuration")
    print_step("📄 Examining the insecure deployment...")

    print(f"\n{Colors.RED}🔓 Exposed Secrets in Plain Text:{Colors.NC}\n")

    # Highlight security issues
    with open(insecure_yaml, 'r') as f:
        in_secret_section = False
        for i, line in enumerate(f, 1):
            if 'stringData:' in line or 'data:' in line:
                in_secret_section = True

            if 'SECURITY DISASTER' in line or 'EXPOSED' in line or 'HARDCODED' in line:
                print(f"{Colors.RED}{Colors.BOLD}{i:3d} | {line.rstrip()}{Colors.NC}")
            elif in_secret_section and ':' in line and not line.strip().startswith('#'):
                if any(keyword in line.lower() for keyword in ['password', 'secret', 'key', 'token']):
                    print(f"{Colors.YELLOW}{i:3d} | {line.rstrip()}{Colors.NC}")
                else:
                    print(f"{Colors.BLUE}{i:3d} | {line.rstrip()}{Colors.NC}")
            elif line.strip().startswith('#'):
                print(f"{Colors.CYAN}{i:3d} | {line.rstrip()}{Colors.NC}")
            else:
                print(f"{i:3d} | {line.rstrip()}")

            if 'kind:' in line and in_secret_section:
                in_secret_section = False

    input(f"\n{Colors.BOLD}Press ENTER to deploy this security disaster...{Colors.NC}")

    # STEP 2: Deploy the insecure configuration
    print_header("STEP 2: Deploying the Insecure Configuration")

    print_step("Deploying security nightmare to cluster...")
    result = run_command(f"kubectl apply -f {insecure_yaml}")

    if result.returncode == 0:
        print_success("Deployment 'succeeded' (with catastrophic security flaws!)")
    else:
        print_error("Deployment failed (at least something prevented this disaster!)")
        print(result.stderr)

    time.sleep(3)

    # STEP 3: Show exposed secrets
    print_header("STEP 3: Extracting Your Exposed Secrets")

    print_critical("Chaos Agent is extracting your credentials...")

    print_step("\n1. Extracting secrets from Kubernetes Secret resource...")
    result = run_command("kubectl get secret mysql-password -n insecure-todo -o jsonpath='{.data}'")

    if result.returncode == 0 and result.stdout:
        print_warning("Secret data found (base64 encoded - trivial to decode):")
        print(f"   {result.stdout[:100]}...")

    print_step("\n2. Reading ConfigMap with 'secrets' (WRONG!)...")
    result = run_command("kubectl get configmap app-secrets -n insecure-todo -o jsonpath='{.data}'")

    if result.returncode == 0 and result.stdout:
        print_critical("ConfigMap secrets exposed in PLAIN TEXT:")
        # Parse and display
        import json
        try:
            data = json.loads(result.stdout)
            for key, value in data.items():
                print(f"   🔓 {key}: {value}")
        except:
            print(f"   {result.stdout}")

    print_step("\n3. Checking environment variables in pods...")
    result = run_command("kubectl get pods -n insecure-todo -o jsonpath='{.items[0].spec.containers[*].env[*].value}'")

    if result.returncode == 0 and result.stdout:
        print_critical("Hardcoded secrets in environment variables:")
        values = result.stdout.split()
        for val in values:
            if any(term in val.lower() for term in ['password', 'secret', 'key', 'token']):
                print(f"   🔓 {val}")

    # STEP 4: Show network exposure
    print_header("STEP 4: Network Exposure - Database on the Internet!")

    print_step("Checking exposed services...")
    result = run_command("kubectl get svc -n insecure-todo")

    print(f"\n{Colors.YELLOW}Service Status:{Colors.NC}")
    print(result.stdout)

    if 'NodePort' in result.stdout and '30306' in result.stdout:
        print_critical("MySQL database exposed to INTERNET via NodePort 30306!")
        print(f"   {Colors.RED}Anyone can connect: mysql://localhost:30306{Colors.NC}")
        print(f"   {Colors.RED}No firewall, no network policies, no protection!{Colors.NC}")

    # STEP 5: Security Assessment
    print_header("STEP 5: Security Assessment")

    print_critical("COMPLIANCE FAILURES:")

    failures = [
        ("SOC2", "FAIL - No access controls, no audit logging, no encryption"),
        ("PCI DSS", "FAIL - Payment data at risk, credentials insecure"),
        ("GDPR", "FAIL - No data protection, breach notification impossible"),
        ("HIPAA", "FAIL - PHI unprotected, no encryption at rest/transit"),
        ("ISO 27001", "FAIL - No security controls, no risk management"),
    ]

    for standard, reason in failures:
        print(f"   ❌ {Colors.RED}{standard:12s}{Colors.NC} - {reason}")

    print(f"\n{Colors.RED}{Colors.BOLD}🎯 SECURITY VULNERABILITIES FOUND:{Colors.NC}\n")

    vulnerabilities = [
        ("CRITICAL", "Plain-text passwords in YAML (committed to Git)", "CVSS 9.8"),
        ("CRITICAL", "Database exposed to internet via NodePort", "CVSS 9.1"),
        ("CRITICAL", "Secrets stored in ConfigMap (no encryption)", "CVSS 9.0"),
        ("CRITICAL", "Hardcoded credentials in environment variables", "CVSS 8.9"),
        ("HIGH", "Containers running as root (privilege escalation)", "CVSS 8.2"),
        ("HIGH", "No secret rotation (permanent compromise)", "CVSS 7.5"),
        ("HIGH", "No network policies (lateral movement possible)", "CVSS 7.8"),
        ("MEDIUM", "No resource limits (DoS vulnerability)", "CVSS 6.5"),
    ]

    for severity, issue, cvss in vulnerabilities:
        severity_color = Colors.RED if severity == "CRITICAL" else Colors.YELLOW
        print(f"   {severity_color}[{severity:8s}]{Colors.NC} {issue} ({cvss})")

    # STEP 6: Live Breach Simulation
    print_header("STEP 6: Live Breach Simulation")

    print(f"{Colors.RED}{Colors.BOLD}🎭 Simulating Chaos Agent's Attack...{Colors.NC}\n")

    attack_steps = [
        ("🔍 Scanning for exposed services", 1),
        ("🎯 Found MySQL on NodePort 30306", 0.5),
        ("💾 Extracting database credentials from YAML", 1),
        ("🔓 Successfully connected to MySQL as root", 0.5),
        ("📥 Downloading entire user database", 2),
        ("🔑 Extracting API keys from environment variables", 1),
        ("💳 Found Stripe API key - stealing payment data", 1),
        ("🐙 Found GitHub token - cloning private repos", 1),
        ("☁️  Found AWS credentials - accessing cloud resources", 1),
        ("⚡ Achieved privilege escalation (root access)", 1),
        ("🚀 Installing cryptominer on compromised pods", 1.5),
        ("💰 Your cluster is now mining Bitcoin for Chaos Agent", 1),
        ("🎮 Game Over - Total compromise achieved", 0.5),
    ]

    for step, delay in attack_steps:
        print(f"   {Colors.RED}► {step}{Colors.NC}")
        time.sleep(delay)

    print(f"\n{Colors.RED}{Colors.BOLD}💀 CHAOS AGENT WINS!{Colors.NC}")
    print(f"{Colors.RED}   \"Your data belongs to me now!\"{Colors.NC}")

    # STEP 7: The Solution
    print_header("STEP 7: There's a Better Way... 🦸")

    print(f"{Colors.GREEN}{Colors.BOLD}What if you could:{Colors.NC}\n")

    print(f"   ✅ Generate cryptographically secure passwords automatically")
    print(f"   ✅ Never store secrets in plain text - ever!")
    print(f"   ✅ Encrypt secrets at rest in Kubernetes")
    print(f"   ✅ Rotate secrets automatically every 30 days")
    print(f"   ✅ Isolate database from internet (ClusterIP only)")
    print(f"   ✅ Run containers as non-root users")
    print(f"   ✅ Enforce security contexts and policies")
    print(f"   ✅ Monitor security compliance in real-time")
    print(f"   ✅ Pass SOC2, PCI DSS, GDPR, HIPAA, ISO 27001")

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}That's what Python Security Hero does!{Colors.NC}")

    print(f"\n{Colors.CYAN}🔧 Optional: Launch Security Breach Dashboard{Colors.NC}")
    print(f"   python3 chaos/security-breach-dashboard.py")
    print(f"   Open: http://localhost:6000")
    print(f"   See live visualization of the security breach!")

    # Cleanup option
    print_header("Cleanup")

    cleanup = input(f"\n{Colors.YELLOW}Clean up the insecure deployment? (y/n): {Colors.NC}").lower()

    if cleanup == 'y':
        print_step("Removing insecure resources...")
        run_command(f"kubectl delete -f {insecure_yaml} --ignore-not-found=true")
        run_command("kubectl delete namespace insecure-todo --ignore-not-found=true")
        print_success("Security nightmare cleaned up!")
    else:
        print_warning("Insecure resources left running. Clean up manually with:")
        print(f"   kubectl delete namespace insecure-todo")

    print_header("🎓 Security Chaos Demo Complete!")

    print(f"\n{Colors.GREEN}Next Steps:{Colors.NC}")
    print(f"   1. Run hero solution: {Colors.BOLD}python3 hero-solution/deploy-secure-todo.py{Colors.NC}")
    print(f"   2. Compare: 0% security vs 100% secure")
    print(f"   3. Learn automated secret management")
    print(f"   4. Never expose secrets again! 🔐")

    print(f"\n{Colors.CYAN}Remember: Automated security is the only security!{Colors.NC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Security chaos demo interrupted!{Colors.NC}")
        print(f"{Colors.CYAN}Run cleanup if needed:{Colors.NC}")
        print(f"   kubectl delete namespace insecure-todo --ignore-not-found=true")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.NC}")
        sys.exit(1)
