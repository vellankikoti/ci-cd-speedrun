#!/usr/bin/env python3
"""
Chaos Engineering Workshop - Progressive Chaos Scenarios
Demonstrates real-world chaos engineering concepts with educational value.
"""

import sys
import time
import subprocess
import docker
import threading
import random
import os

class ChaosEngineer:
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

    def chaos_full(self):
        """Everything is broken - maximum chaos"""
        self.log("🔥 CHAOS FULL: Unleashing maximum chaos!", "CHAOS")
        self.log("This scenario demonstrates multiple failure modes:", "EDUCATION")
        self.log("1. Network connectivity issues", "EDUCATION")
        self.log("2. Resource exhaustion", "EDUCATION") 
        self.log("3. Service dependency failures", "EDUCATION")
        self.log("4. Database connection problems", "EDUCATION")
        
        # Create network chaos
        self.log("🌐 Creating network chaos...", "CHAOS")
        self.run_command("docker network create chaos-network")
        self.run_command("docker run -d --name chaos-router --network chaos-network nginx")
        
        # Resource exhaustion
        self.log("💾 Exhausting system resources...", "CHAOS")
        for i in range(5):
            self.run_command(f"docker run -d --name chaos-memory-{i} --memory=512m busybox sh -c 'dd if=/dev/zero of=/dev/null bs=1M'")
        
        # Service failures
        self.log("🔌 Breaking service dependencies...", "CHAOS")
        self.run_command("docker run -d --name chaos-service --network chaos-network python:3.10 sleep 30")
        time.sleep(2)
        self.run_command("docker kill chaos-service")
        
        # Database issues
        self.log("🗄️ Corrupting database connections...", "CHAOS")
        self.run_command("docker run -d --name chaos-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        time.sleep(5)
        self.run_command("docker exec chaos-db pkill mysqld")
        
        self.log("💥 Chaos Full complete! Everything is broken!", "CHAOS")
        return False

    def chaos_1(self):
        """Fixed network issues, but other problems remain"""
        self.log("🔧 CHAOS 1: Network issues fixed, other problems remain", "CHAOS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity restored", "EDUCATION")
        self.log("❌ Resource exhaustion still active", "EDUCATION")
        self.log("❌ Service dependencies broken", "EDUCATION")
        self.log("❌ Database issues persist", "EDUCATION")
        
        # Clean up network chaos
        self.log("🌐 Fixing network connectivity...", "FIX")
        self.run_command("docker network rm chaos-network", check=False)
        self.run_command("docker rm -f chaos-router", check=False)
        
        # But keep resource exhaustion
        self.log("💾 Resource exhaustion still active...", "CHAOS")
        for i in range(3):
            self.run_command(f"docker run -d --name chaos-memory-{i} --memory=512m busybox sh -c 'dd if=/dev/zero of=/dev/null bs=1M'")
        
        # Service failures continue
        self.log("🔌 Service dependencies still broken...", "CHAOS")
        self.run_command("docker run -d --name chaos-service python:3.10 sleep 30")
        time.sleep(2)
        self.run_command("docker kill chaos-service")
        
        self.log("🔧 Chaos 1 complete! Network fixed, other issues remain", "CHAOS")
        return False

    def chaos_2(self):
        """Fixed resource management, but service issues remain"""
        self.log("⚡ CHAOS 2: Resource management fixed, service issues remain", "CHAOS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity working", "EDUCATION")
        self.log("✅ Resource management fixed", "EDUCATION")
        self.log("❌ Service dependencies broken", "EDUCATION")
        self.log("❌ Database issues persist", "EDUCATION")
        
        # Clean up resource chaos
        self.log("💾 Fixing resource management...", "FIX")
        for i in range(5):
            self.run_command(f"docker rm -f chaos-memory-{i}", check=False)
        
        # But keep service failures
        self.log("🔌 Service dependencies still broken...", "CHAOS")
        self.run_command("docker run -d --name chaos-service python:3.10 sleep 30")
        time.sleep(2)
        self.run_command("docker kill chaos-service")
        
        # Database issues persist
        self.log("🗄️ Database issues still active...", "CHAOS")
        self.run_command("docker run -d --name chaos-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        time.sleep(5)
        self.run_command("docker exec chaos-db pkill mysqld")
        
        self.log("⚡ Chaos 2 complete! Resources fixed, services still broken", "CHAOS")
        return False

    def chaos_3(self):
        """Fixed service dependencies, but database issues remain"""
        self.log("🛠️ CHAOS 3: Service dependencies fixed, database issues remain", "CHAOS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity working", "EDUCATION")
        self.log("✅ Resource management working", "EDUCATION")
        self.log("✅ Service dependencies fixed", "EDUCATION")
        self.log("❌ Database issues persist", "EDUCATION")
        
        # Clean up service chaos
        self.log("🔌 Fixing service dependencies...", "FIX")
        self.run_command("docker rm -f chaos-service", check=False)
        
        # Start a stable service
        self.log("🔌 Starting stable service...", "FIX")
        self.run_command("docker run -d --name stable-service python:3.10 sleep 300")
        
        # But database issues persist
        self.log("🗄️ Database issues still active...", "CHAOS")
        self.run_command("docker run -d --name chaos-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        time.sleep(5)
        self.run_command("docker exec chaos-db pkill mysqld")
        
        self.log("🛠️ Chaos 3 complete! Services fixed, database still broken", "CHAOS")
        return False

    def chaos_free(self):
        """Perfect pipeline - all issues resolved"""
        self.log("🎉 CHAOS FREE: Perfect pipeline!", "SUCCESS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity working", "EDUCATION")
        self.log("✅ Resource management working", "EDUCATION")
        self.log("✅ Service dependencies working", "EDUCATION")
        self.log("✅ Database connections stable", "EDUCATION")
        
        # Clean up all chaos
        self.log("🧹 Cleaning up all chaos...", "FIX")
        self.run_command("docker rm -f chaos-db stable-service", check=False)
        
        # Start stable services
        self.log("🚀 Starting stable services...", "SUCCESS")
        self.run_command("docker run -d --name stable-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        self.run_command("docker run -d --name stable-service python:3.10 sleep 300")
        
        # Verify everything works
        time.sleep(5)
        success, stdout, stderr = self.run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
        if success:
            self.log("📊 Current container status:", "INFO")
            print(stdout)
        
        self.log("🎉 Chaos Free complete! Perfect pipeline achieved!", "SUCCESS")
        return True

    def run(self):
        """Run the selected chaos scenario"""
        self.log(f"🚀 Starting chaos scenario: {self.chaos_level}", "INFO")
        
        # Clean up any existing chaos
        self.run_command("docker rm -f $(docker ps -aq --filter 'name=chaos-*')", check=False)
        
        if self.chaos_level == 'chaos-full':
            return self.chaos_full()
        elif self.chaos_level == 'chaos-1':
            return self.chaos_1()
        elif self.chaos_level == 'chaos-2':
            return self.chaos_2()
        elif self.chaos_level == 'chaos-3':
            return self.chaos_3()
        elif self.chaos_level == 'chaos-free':
            return self.chaos_free()
        else:
            self.log(f"❌ Unknown chaos level: {self.chaos_level}", "ERROR")
            return False

if __name__ == "__main__":
    chaos = ChaosEngineer()
    success = chaos.run()
    sys.exit(0 if success else 1) 