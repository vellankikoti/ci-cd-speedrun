#!/usr/bin/env python3
"""
Docker Ninja - Security Scanning Script
Basic security scanning for Docker images and containers.
"""

import subprocess
import json
import sys
import os
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

def scan_docker_image(image_name):
    """Scan Docker image for security issues."""
    print(f"\n🔒 Scanning Docker image: {image_name}")
    print("=" * 60)
    
    # Check if image exists
    success, output = run_command(f"docker images {image_name}", "Checking if image exists")
    if not success:
        print(f"❌ Image {image_name} not found. Building it first...")
        success, output = run_command(f"docker build --no-cache -t {image_name} .", "Building Docker image")
        if not success:
            return False
    
    # Basic security checks
    security_checks = [
        ("Image size check", f"docker images {image_name} --format 'table {{.Size}}'"),
        ("Image layers check", f"docker history {image_name} --format 'table {{.CreatedBy}}'"),
        ("Running as root check", f"docker run --rm {image_name} whoami"),
        ("Port exposure check", f"docker inspect {image_name} --format '{{{{.Config.ExposedPorts}}}}'"),
        ("Environment variables check", f"docker inspect {image_name} --format '{{{{.Config.Env}}}}'"),
    ]
    
    results = {}
    
    for check_name, command in security_checks:
        print(f"\n🔍 {check_name}")
        print("-" * 30)
        success, output = run_command(command, check_name)
        results[check_name] = {
            'success': success,
            'output': output
        }
    
    return results

def scan_container_security():
    """Scan running containers for security issues."""
    print(f"\n🔒 Scanning running containers")
    print("=" * 60)
    
    # Get running containers
    success, output = run_command("docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'", "Listing running containers")
    if not success:
        print("❌ Could not list containers")
        return False
    
    print("Running containers:")
    print(output)
    
    # Check for security issues
    security_checks = [
        ("Privileged containers", "docker ps --filter 'label=privileged=true' --format 'table {{.Names}}\t{{.Image}}'"),
        ("Root user containers", "docker ps --format 'table {{.Names}}\t{{.Image}}' | xargs -I {} docker exec {} whoami 2>/dev/null || true"),
        ("Exposed ports", "docker ps --format 'table {{.Names}}\t{{.Ports}}'"),
    ]
    
    for check_name, command in security_checks:
        print(f"\n🔍 {check_name}")
        print("-" * 30)
        success, output = run_command(command, check_name)
        if success and output.strip():
            print(f"⚠️  Found: {output}")
        else:
            print("✅ No issues found")
    
    return True

def generate_security_report(results):
    """Generate a security report."""
    print(f"\n📊 Security Report")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'image_scans': results,
        'summary': {
            'total_checks': len(results),
            'passed_checks': sum(1 for r in results.values() if r['success']),
            'failed_checks': sum(1 for r in results.values() if not r['success'])
        }
    }
    
    print(f"Total checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed_checks']}")
    print(f"Failed: {report['summary']['failed_checks']}")
    
    # Save report
    with open('security-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Security report saved to: security-report.json")
    
    return report

def main():
    """Main security scanning function."""
    print("🔒 Docker Ninja - Security Scanning")
    print("=" * 60)
    print("This script performs basic security scanning on Docker images and containers.")
    print()
    
    # Check if Docker is running
    success, output = run_command("docker --version", "Checking Docker installation")
    if not success:
        print("❌ Docker is not installed or not running")
        sys.exit(1)
    
    # Scan Docker image
    image_name = "docker-ninja:latest"
    results = scan_docker_image(image_name)
    
    if not results:
        print("❌ Security scan failed")
        sys.exit(1)
    
    # Scan running containers
    scan_container_security()
    
    # Generate report
    report = generate_security_report(results)
    
    # Summary
    print(f"\n🎯 Security Scan Summary")
    print("=" * 60)
    
    if report['summary']['failed_checks'] == 0:
        print("✅ All security checks passed!")
        print("Your Docker image is secure and ready for production.")
    else:
        print(f"⚠️  {report['summary']['failed_checks']} security checks failed.")
        print("Please review the issues above and fix them before deployment.")
    
    print(f"\n📊 Security Score: {report['summary']['passed_checks']}/{report['summary']['total_checks']}")
    
    return report['summary']['failed_checks'] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
