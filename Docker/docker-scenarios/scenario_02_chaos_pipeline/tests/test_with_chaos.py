#!/usr/bin/env python3
"""
Test application with different chaos levels
Provides educational feedback about what's working and what's broken.
"""

import sys
import time
import subprocess
import docker
import requests
import json

class ChaosTester:
    def __init__(self):
        self.client = docker.from_env()
        self.chaos_level = sys.argv[1] if len(sys.argv) > 1 else 'chaos-free'
        
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, check=True):
        """Run a shell command and return result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr

    def test_network_connectivity(self):
        """Test network connectivity between containers"""
        self.log("🌐 Testing network connectivity...", "TEST")
        
        # Try to connect to a service
        success, stdout, stderr = self.run_command("docker exec stable-service ping -c 1 stable-db", check=False)
        
        if success:
            self.log("✅ Network connectivity: WORKING", "SUCCESS")
            return True
        else:
            self.log("❌ Network connectivity: BROKEN", "FAILURE")
            self.log(f"   Error: {stderr.strip()}", "DETAILS")
            return False

    def test_resource_availability(self):
        """Test if system resources are available"""
        self.log("💾 Testing resource availability...", "TEST")
        
        # Try to start a new container
        success, stdout, stderr = self.run_command("docker run --rm --memory=256m busybox echo 'test'", check=False)
        
        if success:
            self.log("✅ Resource availability: WORKING", "SUCCESS")
            return True
        else:
            self.log("❌ Resource availability: BROKEN", "FAILURE")
            self.log(f"   Error: {stderr.strip()}", "DETAILS")
            return False

    def test_service_dependencies(self):
        """Test if service dependencies are working"""
        self.log("🔌 Testing service dependencies...", "TEST")
        
        # Check if stable service is running
        success, stdout, stderr = self.run_command("docker ps --filter 'name=stable-service' --format '{{.Names}}'", check=False)
        
        if success and 'stable-service' in stdout:
            self.log("✅ Service dependencies: WORKING", "SUCCESS")
            return True
        else:
            self.log("❌ Service dependencies: BROKEN", "FAILURE")
            self.log("   Stable service not found or not running", "DETAILS")
            return False

    def test_database_connectivity(self):
        """Test database connectivity"""
        self.log("🗄️ Testing database connectivity...", "TEST")
        
        # Try to connect to MySQL
        success, stdout, stderr = self.run_command("docker exec stable-db mysql -u root -e 'SELECT 1'", check=False)
        
        if success:
            self.log("✅ Database connectivity: WORKING", "SUCCESS")
            return True
        else:
            self.log("❌ Database connectivity: BROKEN", "FAILURE")
            self.log(f"   Error: {stderr.strip()}", "DETAILS")
            return False

    def test_with_chaos_full(self):
        """Test with maximum chaos - everything should fail"""
        self.log("🔥 Testing with CHAOS FULL - everything should fail!", "TEST")
        
        tests = [
            ("Network Connectivity", self.test_network_connectivity()),
            ("Resource Availability", self.test_resource_availability()),
            ("Service Dependencies", self.test_service_dependencies()),
            ("Database Connectivity", self.test_database_connectivity())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"📊 CHAOS FULL Results: {passed}/{total} tests passed", "RESULTS")
        self.log("💥 Expected: All tests should fail due to maximum chaos", "EDUCATION")
        
        return passed == 0  # Should fail all tests

    def test_with_chaos_1(self):
        """Test with chaos level 1 - network fixed, others broken"""
        self.log("🔧 Testing with CHAOS 1 - network fixed, others broken", "TEST")
        
        tests = [
            ("Network Connectivity", self.test_network_connectivity()),
            ("Resource Availability", self.test_resource_availability()),
            ("Service Dependencies", self.test_service_dependencies()),
            ("Database Connectivity", self.test_database_connectivity())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"📊 CHAOS 1 Results: {passed}/{total} tests passed", "RESULTS")
        self.log("🔧 Expected: Network should work, others should fail", "EDUCATION")
        
        return passed >= 1  # At least network should work

    def test_with_chaos_2(self):
        """Test with chaos level 2 - resources fixed, services broken"""
        self.log("⚡ Testing with CHAOS 2 - resources fixed, services broken", "TEST")
        
        tests = [
            ("Network Connectivity", self.test_network_connectivity()),
            ("Resource Availability", self.test_resource_availability()),
            ("Service Dependencies", self.test_service_dependencies()),
            ("Database Connectivity", self.test_database_connectivity())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"📊 CHAOS 2 Results: {passed}/{total} tests passed", "RESULTS")
        self.log("⚡ Expected: Network and resources should work, services broken", "EDUCATION")
        
        return passed >= 2  # Network and resources should work

    def test_with_chaos_3(self):
        """Test with chaos level 3 - services fixed, database broken"""
        self.log("🛠️ Testing with CHAOS 3 - services fixed, database broken", "TEST")
        
        tests = [
            ("Network Connectivity", self.test_network_connectivity()),
            ("Resource Availability", self.test_resource_availability()),
            ("Service Dependencies", self.test_service_dependencies()),
            ("Database Connectivity", self.test_database_connectivity())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"📊 CHAOS 3 Results: {passed}/{total} tests passed", "RESULTS")
        self.log("🛠️ Expected: Everything except database should work", "EDUCATION")
        
        return passed >= 3  # Everything except database should work

    def test_with_chaos_free(self):
        """Test with chaos free - everything should work"""
        self.log("🎉 Testing with CHAOS FREE - everything should work!", "TEST")
        
        tests = [
            ("Network Connectivity", self.test_network_connectivity()),
            ("Resource Availability", self.test_resource_availability()),
            ("Service Dependencies", self.test_service_dependencies()),
            ("Database Connectivity", self.test_database_connectivity())
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        self.log(f"📊 CHAOS FREE Results: {passed}/{total} tests passed", "RESULTS")
        self.log("🎉 Expected: All tests should pass - perfect pipeline!", "EDUCATION")
        
        return passed == total  # All tests should pass

    def run(self):
        """Run tests based on chaos level"""
        self.log(f"🧪 Starting chaos testing for level: {self.chaos_level}", "INFO")
        
        if self.chaos_level == 'chaos-full':
            return self.test_with_chaos_full()
        elif self.chaos_level == 'chaos-1':
            return self.test_with_chaos_1()
        elif self.chaos_level == 'chaos-2':
            return self.test_with_chaos_2()
        elif self.chaos_level == 'chaos-3':
            return self.test_with_chaos_3()
        elif self.chaos_level == 'chaos-free':
            return self.test_with_chaos_free()
        else:
            self.log(f"❌ Unknown chaos level: {self.chaos_level}", "ERROR")
            return False

if __name__ == "__main__":
    tester = ChaosTester()
    success = tester.run()
    sys.exit(0 if success else 1) 