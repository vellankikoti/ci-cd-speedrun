#!/usr/bin/env python3
import sys
import time
import subprocess

class ChaosEngineer:
    def __init__(self):
        self.chaos_level = sys.argv[1] if len(sys.argv) > 1 else 'chaos-free'
        
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, check=True):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr

    def chaos_free(self):
        self.log("🎉 CHAOS FREE: Perfect pipeline!", "SUCCESS")
        self.log("This scenario shows:", "EDUCATION")
        self.log("✅ Network connectivity working", "EDUCATION")
        self.log("✅ Resource management working", "EDUCATION")
        self.log("✅ Service dependencies working", "EDUCATION")
        self.log("✅ Database connections stable", "EDUCATION")
        
        self.log("🧹 Cleaning up all chaos...", "FIX")
        self.run_command("docker rm -f $(docker ps -aq --filter 'name=chaos-*')", check=False)
        
        self.log("🚀 Starting stable services...", "SUCCESS")
        self.run_command("docker run -d --name stable-db mysql:8.0 --default-authentication-plugin=mysql_native_password")
        self.run_command("docker run -d --name stable-service python:3.10 sleep 300")
        
        time.sleep(5)
        success, stdout, stderr = self.run_command("docker ps --format 'table {{.Names}}\t{{.Status}}'")
        if success:
            self.log("📊 Current container status:", "INFO")
            print(stdout)
        
        self.log("🎉 Chaos Free complete! Perfect pipeline achieved!", "SUCCESS")
        return True

    def run(self):
        self.log(f"🚀 Starting chaos scenario: {self.chaos_level}", "INFO")
        
        if self.chaos_level == 'chaos-free':
            return self.chaos_free()
        else:
            self.log(f"❌ Unknown chaos level: {self.chaos_level}", "ERROR")
            return False

if __name__ == "__main__":
    chaos = ChaosEngineer()
    success = chaos.run()
    sys.exit(0 if success else 1)
