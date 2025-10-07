#!/usr/bin/env python3
"""
Security Sentinel - Compliance Checking Script
Check compliance with security standards and best practices.
"""

import os
import sys
import json
import requests
from datetime import datetime

def check_security_headers():
    """Check if security headers are properly configured."""
    print("🔍 Checking Security Headers...")
    
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        headers = response.headers
        
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
            if header not in headers:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"❌ Missing security headers: {missing_headers}")
            return False
        else:
            print("✅ All required security headers present")
            return True
    
    except Exception as e:
        print(f"❌ Error checking security headers: {e}")
        return False

def check_authentication():
    """Check if authentication is properly implemented."""
    print("🔍 Checking Authentication...")
    
    try:
        # Test authentication endpoint
        response = requests.post('http://localhost:5000/auth', 
                               json={'username': 'test', 'password': 'test'}, 
                               timeout=5)
        
        if response.status_code == 401:
            print("✅ Authentication properly rejects invalid credentials")
            return True
        else:
            print("❌ Authentication not properly implemented")
            return False
    
    except Exception as e:
        print(f"❌ Error checking authentication: {e}")
        return False

def check_encryption():
    """Check if encryption is properly configured."""
    print("🔍 Checking Encryption...")
    
    try:
        # Check if HTTPS is available (in production)
        if os.environ.get('ENVIRONMENT') == 'production':
            response = requests.get('https://localhost:5000', timeout=5, verify=False)
            if response.status_code == 200:
                print("✅ HTTPS properly configured")
                return True
            else:
                print("❌ HTTPS not properly configured")
                return False
        else:
            print("✅ Encryption check skipped (development environment)")
            return True
    
    except Exception as e:
        print(f"❌ Error checking encryption: {e}")
        return False

def check_logging():
    """Check if security logging is properly implemented."""
    print("🔍 Checking Security Logging...")
    
    try:
        # Test audit endpoint
        response = requests.get('http://localhost:5000/audit', timeout=5)
        
        if response.status_code == 401:
            print("✅ Audit endpoint properly requires authentication")
            return True
        else:
            print("❌ Audit endpoint not properly secured")
            return False
    
    except Exception as e:
        print(f"❌ Error checking logging: {e}")
        return False

def check_input_validation():
    """Check if input validation is properly implemented."""
    print("🔍 Checking Input Validation...")
    
    try:
        # Test with potentially malicious input
        malicious_inputs = [
            {'username': 'admin', 'password': "'; DROP TABLE users; --"},
            {'username': '<script>alert("xss")</script>', 'password': 'test'},
            {'username': 'admin', 'password': 'test'}
        ]
        
        for input_data in malicious_inputs:
            response = requests.post('http://localhost:5000/auth', 
                                   json=input_data, 
                                   timeout=5)
            
            if response.status_code == 400:
                print(f"✅ Input validation properly rejects malicious input: {input_data}")
            else:
                print(f"❌ Input validation failed for: {input_data}")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error checking input validation: {e}")
        return False

def check_session_management():
    """Check if session management is properly implemented."""
    print("🔍 Checking Session Management...")
    
    try:
        # Test session security
        response = requests.get('http://localhost:5000', timeout=5)
        
        # Check for secure session cookies
        cookies = response.cookies
        if 'session' in cookies:
            session_cookie = cookies['session']
            if session_cookie.secure:
                print("✅ Session cookies are secure")
                return True
            else:
                print("❌ Session cookies are not secure")
                return False
        else:
            print("✅ No session cookies (stateless)")
            return True
    
    except Exception as e:
        print(f"❌ Error checking session management: {e}")
        return False

def check_error_handling():
    """Check if error handling is properly implemented."""
    print("🔍 Checking Error Handling...")
    
    try:
        # Test error handling
        response = requests.get('http://localhost:5000/nonexistent', timeout=5)
        
        if response.status_code == 404:
            print("✅ Error handling properly returns 404 for nonexistent endpoints")
            return True
        else:
            print("❌ Error handling not properly implemented")
            return False
    
    except Exception as e:
        print(f"❌ Error checking error handling: {e}")
        return False

def check_audit_logging():
    """Check if audit logging is properly implemented."""
    print("🔍 Checking Audit Logging...")
    
    try:
        # Test audit logging by making a request
        response = requests.get('http://localhost:5000/security', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'security_events' in data and data['security_events'] > 0:
                print("✅ Audit logging is working")
                return True
            else:
                print("❌ Audit logging not working")
                return False
        else:
            print("❌ Security endpoint not accessible")
            return False
    
    except Exception as e:
        print(f"❌ Error checking audit logging: {e}")
        return False

def generate_compliance_report(results):
    """Generate a compliance report."""
    print(f"\n📊 Compliance Report")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'checks': results,
        'summary': {
            'total_checks': len(results),
            'passed_checks': sum(1 for r in results.values() if r),
            'failed_checks': sum(1 for r in results.values() if not r)
        }
    }
    
    print(f"Total checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed_checks']}")
    print(f"Failed: {report['summary']['failed_checks']}")
    
    # Calculate compliance score
    compliance_score = (report['summary']['passed_checks'] / report['summary']['total_checks']) * 100
    print(f"Compliance Score: {compliance_score:.1f}/100")
    
    # Determine compliance status
    if compliance_score >= 90:
        status = "FULLY_COMPLIANT"
        print("✅ FULLY COMPLIANT")
    elif compliance_score >= 70:
        status = "MOSTLY_COMPLIANT"
        print("⚠️ MOSTLY COMPLIANT")
    else:
        status = "NON_COMPLIANT"
        print("❌ NON COMPLIANT")
    
    report['status'] = status
    
    # Save report
    with open('compliance-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Compliance report saved to: compliance-report.json")
    
    return report

def main():
    """Main compliance checking function."""
    print("🔒 Security Sentinel - Compliance Checking")
    print("=" * 60)
    print("This script checks compliance with security standards.")
    print()
    
    # Run all compliance checks
    checks = {
        'Security Headers': check_security_headers,
        'Authentication': check_authentication,
        'Encryption': check_encryption,
        'Logging': check_logging,
        'Input Validation': check_input_validation,
        'Session Management': check_session_management,
        'Error Handling': check_error_handling,
        'Audit Logging': check_audit_logging
    }
    
    results = {}
    
    for check_name, check_func in checks.items():
        print(f"\n🧪 {check_name}")
        print("-" * 30)
        
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results[check_name] = False
    
    # Generate report
    report = generate_compliance_report(results)
    
    # Summary
    print(f"\n🎯 Compliance Summary")
    print("=" * 60)
    
    if report['status'] == 'FULLY_COMPLIANT':
        print("✅ Your application is fully compliant with security standards!")
    elif report['status'] == 'MOSTLY_COMPLIANT':
        print("⚠️ Your application is mostly compliant. Some improvements needed.")
    else:
        print("❌ Your application is not compliant. Significant improvements needed.")
    
    print(f"\n📊 Compliance Score: {report['summary']['passed_checks']}/{report['summary']['total_checks']}")
    
    return report['status'] in ['FULLY_COMPLIANT', 'MOSTLY_COMPLIANT']

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
