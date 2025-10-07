#!/usr/bin/env python3
"""
Security Sentinel - Security Scanning Script
Comprehensive security scanning for applications and containers.
"""

import subprocess
import os
import sys
import json
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and return the result."""
    print(f"🔍 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
            return True, result.stdout
        else:
            print("❌ Error!")
            if result.stderr:
                print(result.stderr)
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def scan_dependencies():
    """Scan Python dependencies for vulnerabilities."""
    print("\n🔍 Scanning Python Dependencies...")
    
    # Check if safety is available
    success, output = run_command("safety --version", "Checking safety version")
    if not success:
        print("❌ Safety not available. Installing...")
        run_command("pip install safety", "Installing safety")
    
    # Run safety check
    success, output = run_command("safety check", "Running safety check")
    if success:
        print("✅ No known vulnerabilities in dependencies!")
        return True
    else:
        print("⚠️ Vulnerabilities found in dependencies!")
        return False

def scan_code_quality():
    """Scan code for security issues using bandit."""
    print("\n🔍 Scanning Code Quality...")
    
    # Check if bandit is available
    success, output = run_command("bandit --version", "Checking bandit version")
    if not success:
        print("❌ Bandit not available. Installing...")
        run_command("pip install bandit", "Installing bandit")
    
    # Run bandit scan
    success, output = run_command("bandit -r . -f json", "Running bandit scan")
    if success:
        print("✅ No security issues found in code!")
        return True
    else:
        print("⚠️ Security issues found in code!")
        return False

def scan_docker_image():
    """Scan Docker image for vulnerabilities."""
    print("\n🔍 Scanning Docker Image...")
    
    # Build image first
    success, output = run_command("docker build --no-cache -t security-sentinel:latest .", "Building Docker image")
    if not success:
        print("❌ Failed to build Docker image!")
        return False
    
    # Check if trivy is available
    success, output = run_command("trivy --version", "Checking trivy version")
    if not success:
        print("❌ Trivy not available. Installing...")
        run_command("curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin", "Installing trivy")
    
    # Run trivy scan
    success, output = run_command("trivy image security-sentinel:latest", "Running trivy scan")
    if success:
        print("✅ Docker image scan completed!")
        return True
    else:
        print("⚠️ Docker image vulnerabilities found!")
        return False

def scan_secrets():
    """Scan for hardcoded secrets."""
    print("\n🔍 Scanning for Secrets...")
    
    # Check if truffleHog is available
    success, output = run_command("trufflehog --version", "Checking truffleHog version")
    if not success:
        print("❌ TruffleHog not available. Installing...")
        run_command("pip install truffleHog", "Installing truffleHog")
    
    # Run truffleHog scan
    success, output = run_command("trufflehog filesystem .", "Running truffleHog scan")
    if success:
        print("✅ No secrets found!")
        return True
    else:
        print("⚠️ Potential secrets found!")
        return False

def scan_ssl_certificates():
    """Scan SSL certificates for issues."""
    print("\n🔍 Scanning SSL Certificates...")
    
    # Check if testssl.sh is available
    success, output = run_command("testssl.sh --version", "Checking testssl.sh version")
    if not success:
        print("❌ testssl.sh not available. Installing...")
        run_command("git clone https://github.com/drwetter/testssl.sh.git /tmp/testssl.sh", "Installing testssl.sh")
    
    # Run SSL scan (if we have a target)
    target = os.environ.get('SSL_TARGET', 'localhost:5000')
    success, output = run_command(f"/tmp/testssl.sh/testssl.sh {target}", "Running SSL scan")
    if success:
        print("✅ SSL certificate scan completed!")
        return True
    else:
        print("⚠️ SSL certificate issues found!")
        return False

def scan_network_security():
    """Scan network security."""
    print("\n🔍 Scanning Network Security...")
    
    # Check if nmap is available
    success, output = run_command("nmap --version", "Checking nmap version")
    if not success:
        print("❌ nmap not available. Installing...")
        run_command("apt-get update && apt-get install -y nmap", "Installing nmap")
    
    # Run nmap scan
    target = os.environ.get('SCAN_TARGET', 'localhost')
    success, output = run_command(f"nmap -sV -sC {target}", "Running nmap scan")
    if success:
        print("✅ Network security scan completed!")
        return True
    else:
        print("⚠️ Network security issues found!")
        return False

def generate_security_report(results):
    """Generate a comprehensive security report."""
    print(f"\n📊 Security Report")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'scans': results,
        'summary': {
            'total_scans': len(results),
            'passed_scans': sum(1 for r in results.values() if r),
            'failed_scans': sum(1 for r in results.values() if not r)
        }
    }
    
    print(f"Total scans: {report['summary']['total_scans']}")
    print(f"Passed: {report['summary']['passed_scans']}")
    print(f"Failed: {report['summary']['failed_scans']}")
    
    # Calculate security score
    security_score = (report['summary']['passed_scans'] / report['summary']['total_scans']) * 100
    print(f"Security Score: {security_score:.1f}/100")
    
    # Save report
    with open('security-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Security report saved to: security-report.json")
    
    return report

def main():
    """Main security scanning function."""
    print("🔒 Security Sentinel - Security Scanning")
    print("=" * 60)
    print("This script performs comprehensive security scanning.")
    print()
    
    # Run all security scans
    scans = {
        'Dependencies': scan_dependencies,
        'Code Quality': scan_code_quality,
        'Docker Image': scan_docker_image,
        'Secrets': scan_secrets,
        'SSL Certificates': scan_ssl_certificates,
        'Network Security': scan_network_security
    }
    
    results = {}
    
    for scan_name, scan_func in scans.items():
        print(f"\n🧪 {scan_name}")
        print("-" * 30)
        
        try:
            results[scan_name] = scan_func()
        except Exception as e:
            print(f"❌ {scan_name} failed with exception: {e}")
            results[scan_name] = False
    
    # Generate report
    report = generate_security_report(results)
    
    # Summary
    print(f"\n🎯 Security Scan Summary")
    print("=" * 60)
    
    if report['summary']['failed_scans'] == 0:
        print("✅ All security scans passed!")
        print("Your application is secure and ready for production.")
    else:
        print(f"⚠️ {report['summary']['failed_scans']} security scans failed.")
        print("Please review the issues above and fix them before deployment.")
    
    print(f"\n📊 Security Score: {report['summary']['passed_scans']}/{report['summary']['total_scans']}")
    
    return report['summary']['failed_scans'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
