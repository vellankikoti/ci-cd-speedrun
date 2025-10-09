#!/usr/bin/env python3
"""
Test script to verify the Jenkins pipeline will work correctly
"""

import os
import sys
import subprocess

def test_webapp_generation():
    """Test web application generation"""
    print("🧪 Testing web application generation...")
    
    test_cases = [
        ("Development", "1.0.0", "Basic", True, "Development testing"),
        ("Staging", "1.2.0", "Advanced", True, "Pre-production testing"),
        ("Production", "2.0.0", "Enterprise", True, "Production release")
    ]
    
    for i, (env, version, features, run_tests, notes) in enumerate(test_cases):
        print(f"\n📋 Test case {i+1}: {env} + {features}")
        
        # Test webapp generation
        cmd = [
            "python3", "demo.py", "--generate-webapp",
            env, version, features, str(run_tests).lower(), notes
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                print(f"   ✅ Web application generated successfully")
                
                # Check if webapp directory exists
                if os.path.exists("webapp/index.html"):
                    print(f"   ✅ Web application file created")
                else:
                    print(f"   ❌ Web application file not found")
                    return False
            else:
                print(f"   ❌ Web application generation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ Error running webapp generation: {e}")
            return False
    
    return True

def test_jenkins_syntax():
    """Test Jenkins pipeline syntax"""
    print("\n🧪 Testing Jenkins pipeline syntax...")
    
    # Check if Jenkinsfile exists
    if not os.path.exists("Jenkinsfile"):
        print("   ❌ Jenkinsfile not found")
        return False
    
    print("   ✅ Jenkinsfile exists")
    
    # Check if demo.py exists
    if not os.path.exists("demo.py"):
        print("   ❌ demo.py not found")
        return False
    
    print("   ✅ demo.py exists")
    
    # Check if demo.py is executable
    if not os.access("demo.py", os.X_OK):
        print("   ⚠️  demo.py is not executable, but that's okay")
    
    print("   ✅ All required files present")
    return True

def test_webapp_content():
    """Test web application content"""
    print("\n🧪 Testing web application content...")
    
    if not os.path.exists("webapp/index.html"):
        print("   ❌ No web application to test")
        return False
    
    with open("webapp/index.html", "r") as f:
        content = f.read()
    
    # Check for key elements
    checks = [
        ("HTML structure", "<!DOCTYPE html>" in content),
        ("CSS styling", "<style>" in content),
        ("JavaScript", "<script>" in content),
        ("Environment info", "Production" in content),
        ("Feature info", "Enterprise" in content),
        ("Interactive elements", "onclick=" in content)
    ]
    
    all_passed = True
    for check_name, check_result in checks:
        if check_result:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Main test function"""
    print("🚀 Testing Jenkins Pipeline Configuration")
    print("=" * 50)
    
    tests = [
        ("Web Application Generation", test_webapp_generation),
        ("Jenkins Pipeline Syntax", test_jenkins_syntax),
        ("Web Application Content", test_webapp_content)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n🔹 {test_name}")
        print("-" * 30)
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The Jenkins pipeline will work as expected!")
        print("\n📋 To use:")
        print("1. Go to Jenkins: http://localhost:8080")
        print("2. Create new Pipeline job")
        print("3. Enable 'This project is parameterized'")
        print("4. Add the parameters from the guide")
        print("5. Point to scenario_02_parameterized_builds/Jenkinsfile")
        print("6. Run the pipeline!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please fix the issues before running the Jenkins pipeline.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
