#!/usr/bin/env python3
"""
Security Sentinel - Security Tests
Tests for security-specific functionality.
"""

import pytest
import sys
import os
import subprocess
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

def test_security_scanning():
    """Test security scanning functionality."""
    print("\n🔍 Testing Security Scanning...")
    
    # Test dependency scanning
    success, output = run_command("python security/scan.py", "Running security scan")
    if success:
        print("✅ Security scan completed successfully!")
        return True
    else:
        print("❌ Security scan failed!")
        return False

def test_compliance_checking():
    """Test compliance checking functionality."""
    print("\n🔍 Testing Compliance Checking...")
    
    # Test compliance checking
    success, output = run_command("python security/compliance.py", "Running compliance check")
    if success:
        print("✅ Compliance check completed successfully!")
        return True
    else:
        print("❌ Compliance check failed!")
        return False

def test_secrets_management():
    """Test secrets management functionality."""
    print("\n🔍 Testing Secrets Management...")
    
    # Test secrets management
    success, output = run_command("python security/secrets.py", "Running secrets management")
    if success:
        print("✅ Secrets management completed successfully!")
        return True
    else:
        print("❌ Secrets management failed!")
        return False

def test_security_headers():
    """Test security headers implementation."""
    print("\n🔍 Testing Security Headers...")
    
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=5)
        
        # Check for security headers
        required_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Referrer-Policy',
            'Content-Security-Policy'
        ]
        
        missing_headers = []
        for header in required_headers:
            if header not in response.headers:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"❌ Missing security headers: {missing_headers}")
            return False
        else:
            print("✅ All required security headers present")
            return True
    
    except Exception as e:
        print(f"❌ Error testing security headers: {e}")
        return False

def test_authentication_security():
    """Test authentication security."""
    print("\n🔍 Testing Authentication Security...")
    
    try:
        import requests
        
        # Test with invalid credentials
        response = requests.post('http://localhost:5000/auth', 
                               json={'username': 'admin', 'password': 'wrong'}, 
                               timeout=5)
        
        if response.status_code == 401:
            print("✅ Authentication properly rejects invalid credentials")
            return True
        else:
            print("❌ Authentication not properly secured")
            return False
    
    except Exception as e:
        print(f"❌ Error testing authentication security: {e}")
        return False

def test_input_validation():
    """Test input validation for security."""
    print("\n🔍 Testing Input Validation...")
    
    try:
        import requests
        
        # Test with SQL injection attempt
        response = requests.post('http://localhost:5000/auth', 
                               json={'username': "admin'; DROP TABLE users; --", 'password': 'test'}, 
                               timeout=5)
        
        if response.status_code == 400:
            print("✅ Input validation properly rejects SQL injection")
            return True
        else:
            print("❌ Input validation failed for SQL injection")
            return False
    
    except Exception as e:
        print(f"❌ Error testing input validation: {e}")
        return False

def test_security_logging():
    """Test security event logging."""
    print("\n🔍 Testing Security Logging...")
    
    try:
        import requests
        
        # Make a request that should trigger logging
        response = requests.get('http://localhost:5000/security', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'security_events' in data and data['security_events'] >= 0:
                print("✅ Security logging is working")
                return True
            else:
                print("❌ Security logging not working")
                return False
        else:
            print("❌ Security endpoint not accessible")
            return False
    
    except Exception as e:
        print(f"❌ Error testing security logging: {e}")
        return False

def test_encryption():
    """Test encryption functionality."""
    print("\n🔍 Testing Encryption...")
    
    try:
        from security.secrets import SecretsManager
        
        # Test secrets manager
        manager = SecretsManager()
        
        # Test secret generation
        secret = manager.generate_secret('test_secret')
        if secret and len(secret) > 0:
            print("✅ Secret generation working")
            return True
        else:
            print("❌ Secret generation failed")
            return False
    
    except Exception as e:
        print(f"❌ Error testing encryption: {e}")
        return False

def test_vulnerability_scanning():
    """Test vulnerability scanning."""
    print("\n🔍 Testing Vulnerability Scanning...")
    
    try:
        # Test if security tools are available
        tools = ['bandit', 'safety', 'trivy']
        available_tools = []
        
        for tool in tools:
            success, output = run_command(f"{tool} --version", f"Checking {tool}")
            if success:
                available_tools.append(tool)
        
        if available_tools:
            print(f"✅ Available security tools: {available_tools}")
            return True
        else:
            print("❌ No security tools available")
            return False
    
    except Exception as e:
        print(f"❌ Error testing vulnerability scanning: {e}")
        return False

def test_compliance_standards():
    """Test compliance with security standards."""
    print("\n🔍 Testing Compliance Standards...")
    
    try:
        import requests
        
        # Test compliance endpoint
        response = requests.get('http://localhost:5000/compliance', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'compliance_score' in data and 0 <= data['compliance_score'] <= 100:
                print("✅ Compliance checking working")
                return True
            else:
                print("❌ Compliance checking failed")
                return False
        else:
            print("❌ Compliance endpoint not accessible")
            return False
    
    except Exception as e:
        print(f"❌ Error testing compliance standards: {e}")
        return False

def main():
    """Run all security tests."""
    print("🔒 Security Sentinel - Security Tests")
    print("=" * 50)
    
    tests = [
        ("Security Scanning", test_security_scanning),
        ("Compliance Checking", test_compliance_checking),
        ("Secrets Management", test_secrets_management),
        ("Security Headers", test_security_headers),
        ("Authentication Security", test_authentication_security),
        ("Input Validation", test_input_validation),
        ("Security Logging", test_security_logging),
        ("Encryption", test_encryption),
        ("Vulnerability Scanning", test_vulnerability_scanning),
        ("Compliance Standards", test_compliance_standards),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} passed!")
                passed += 1
            else:
                print(f"❌ {test_name} failed!")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All security tests passed!")
        return True
    else:
        print("❌ Some security tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
