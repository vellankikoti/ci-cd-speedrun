#!/usr/bin/env python3
"""
Chaos Engineering Analyzer
Provides educational insights about what happened and what was learned.
"""

import sys
import time
import subprocess
import json

class ChaosAnalyzer:
    def __init__(self):
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

    def analyze_chaos_full(self):
        """Analyze the chaos-full scenario"""
        self.log("🔥 CHAOS FULL ANALYSIS", "ANALYSIS")
        self.log("=" * 50, "ANALYSIS")
        
        self.log("📚 What We Learned:", "EDUCATION")
        self.log("1. Network isolation can completely break microservices", "EDUCATION")
        self.log("2. Resource exhaustion affects all containers", "EDUCATION")
        self.log("3. Service dependencies are critical for system health", "EDUCATION")
        self.log("4. Database failures cascade to application failures", "EDUCATION")
        
        self.log("💡 Key Insights:", "INSIGHTS")
        self.log("- Single points of failure can bring down entire systems", "INSIGHTS")
        self.log("- Monitoring network connectivity is crucial", "INSIGHTS")
        self.log("- Resource limits prevent cascading failures", "INSIGHTS")
        self.log("- Health checks help detect issues early", "INSIGHTS")
        
        self.log("🛠️ How to Fix:", "SOLUTIONS")
        self.log("- Use service mesh for network resilience", "SOLUTIONS")
        self.log("- Implement resource quotas and limits", "SOLUTIONS")
        self.log("- Add circuit breakers for service calls", "SOLUTIONS")
        self.log("- Use database connection pooling", "SOLUTIONS")

    def analyze_chaos_1(self):
        """Analyze the chaos-1 scenario"""
        self.log("🔧 CHAOS 1 ANALYSIS", "ANALYSIS")
        self.log("=" * 50, "ANALYSIS")
        
        self.log("📚 What We Learned:", "EDUCATION")
        self.log("1. Fixing network issues improves overall stability", "EDUCATION")
        self.log("2. Resource exhaustion still affects performance", "EDUCATION")
        self.log("3. Service dependencies remain critical", "EDUCATION")
        self.log("4. Database issues persist despite network fixes", "EDUCATION")
        
        self.log("💡 Key Insights:", "INSIGHTS")
        self.log("- Network connectivity is foundational", "INSIGHTS")
        self.log("- Resource management is independent of networking", "INSIGHTS")
        self.log("- Each layer of the stack needs separate attention", "INSIGHTS")
        self.log("- Incremental fixes show partial improvements", "INSIGHTS")
        
        self.log("🛠️ How to Fix:", "SOLUTIONS")
        self.log("- Implement proper resource monitoring", "SOLUTIONS")
        self.log("- Use horizontal pod autoscaling", "SOLUTIONS")
        self.log("- Add service mesh for dependency management", "SOLUTIONS")
        self.log("- Implement database failover mechanisms", "SOLUTIONS")

    def analyze_chaos_2(self):
        """Analyze the chaos-2 scenario"""
        self.log("⚡ CHAOS 2 ANALYSIS", "ANALYSIS")
        self.log("=" * 50, "ANALYSIS")
        
        self.log("📚 What We Learned:", "EDUCATION")
        self.log("1. Resource management is crucial for stability", "EDUCATION")
        self.log("2. Service dependencies are still vulnerable", "EDUCATION")
        self.log("3. Database issues are independent of infrastructure", "EDUCATION")
        self.log("4. Multiple layers of resilience are needed", "EDUCATION")
        
        self.log("💡 Key Insights:", "INSIGHTS")
        self.log("- Resource management affects all services", "INSIGHTS")
        self.log("- Service dependencies need explicit handling", "INSIGHTS")
        self.log("- Database resilience requires special attention", "INSIGHTS")
        self.log("- Layered architecture needs layered fixes", "INSIGHTS")
        
        self.log("🛠️ How to Fix:", "SOLUTIONS")
        self.log("- Implement service mesh for dependency management", "SOLUTIONS")
        self.log("- Add health checks and readiness probes", "SOLUTIONS")
        self.log("- Use database clustering and replication", "SOLUTIONS")
        self.log("- Implement graceful degradation patterns", "SOLUTIONS")

    def analyze_chaos_3(self):
        """Analyze the chaos-3 scenario"""
        self.log("🛠️ CHAOS 3 ANALYSIS", "ANALYSIS")
        self.log("=" * 50, "ANALYSIS")
        
        self.log("📚 What We Learned:", "EDUCATION")
        self.log("1. Service dependencies can be managed effectively", "EDUCATION")
        self.log("2. Database issues are the final frontier", "EDUCATION")
        self.log("3. Most application issues are infrastructure-related", "EDUCATION")
        self.log("4. Database resilience is critical for data integrity", "EDUCATION")
        
        self.log("💡 Key Insights:", "INSIGHTS")
        self.log("- Service mesh solves many dependency issues", "INSIGHTS")
        self.log("- Database resilience is different from app resilience", "INSIGHTS")
        self.log("- Data integrity is paramount", "INSIGHTS")
        self.log("- Almost there! Just database issues remain", "INSIGHTS")
        
        self.log("🛠️ How to Fix:", "SOLUTIONS")
        self.log("- Implement database clustering (MySQL Group Replication)", "SOLUTIONS")
        self.log("- Use database proxies for load balancing", "SOLUTIONS")
        self.log("- Add database connection pooling", "SOLUTIONS")
        self.log("- Implement proper backup and recovery procedures", "SOLUTIONS")

    def analyze_chaos_free(self):
        """Analyze the chaos-free scenario"""
        self.log("🎉 CHAOS FREE ANALYSIS", "ANALYSIS")
        self.log("=" * 50, "ANALYSIS")
        
        self.log("📚 What We Achieved:", "EDUCATION")
        self.log("1. Perfect network connectivity", "EDUCATION")
        self.log("2. Optimal resource management", "EDUCATION")
        self.log("3. Robust service dependencies", "EDUCATION")
        self.log("4. Stable database connections", "EDUCATION")
        
        self.log("💡 Key Insights:", "INSIGHTS")
        self.log("- Comprehensive resilience is achievable", "INSIGHTS")
        self.log("- Each layer contributes to overall stability", "INSIGHTS")
        self.log("- Monitoring and observability are crucial", "INSIGHTS")
        self.log("- Production-ready systems require multiple layers", "INSIGHTS")
        
        self.log("🏆 Best Practices Demonstrated:", "SOLUTIONS")
        self.log("- Service mesh for network resilience", "SOLUTIONS")
        self.log("- Resource quotas and limits", "SOLUTIONS")
        self.log("- Health checks and readiness probes", "SOLUTIONS")
        self.log("- Database clustering and replication", "SOLUTIONS")
        self.log("- Comprehensive monitoring and alerting", "SOLUTIONS")

    def get_container_status(self):
        """Get current container status for analysis"""
        success, stdout, stderr = self.run_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", check=False)
        if success:
            self.log("📊 Current Container Status:", "INFO")
            print(stdout)
        else:
            self.log("❌ Could not get container status", "ERROR")

    def run(self):
        """Run analysis based on chaos level"""
        self.log(f"📊 Starting chaos analysis for level: {self.chaos_level}", "INFO")
        
        # Get current container status
        self.get_container_status()
        
        if self.chaos_level == 'chaos-full':
            self.analyze_chaos_full()
        elif self.chaos_level == 'chaos-1':
            self.analyze_chaos_1()
        elif self.chaos_level == 'chaos-2':
            self.analyze_chaos_2()
        elif self.chaos_level == 'chaos-3':
            self.analyze_chaos_3()
        elif self.chaos_level == 'chaos-free':
            self.analyze_chaos_free()
        else:
            self.log(f"❌ Unknown chaos level: {self.chaos_level}", "ERROR")
            return False
        
        self.log("🎓 Analysis complete! Check the insights above.", "INFO")
        return True

if __name__ == "__main__":
    analyzer = ChaosAnalyzer()
    success = analyzer.run()
    sys.exit(0 if success else 1) 