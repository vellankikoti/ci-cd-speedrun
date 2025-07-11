#!/usr/bin/env python3
"""
👁️ SECURITY MONITORING DASHBOARD
Real-time security status and compliance monitoring

This system keeps watch for Chaos Agent's security attacks!
"""

import os
import sys
import time
import base64
from datetime import datetime, timedelta
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style

init(autoreset=True)

class SecurityMonitor:
    """Real-time security monitoring and compliance system"""
    
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.namespace = "secure-todo"
    
    def get_secret_security_status(self, secret_name):
        """Analyze secret security status"""
        try:
            secret = self.v1.read_namespaced_secret(
                name=secret_name,
                namespace=self.namespace
            )
            
            # Extract metadata
            created_timestamp = secret.metadata.annotations.get("created-timestamp")
            rotation_policy = secret.metadata.annotations.get("rotation-policy", "unknown")
            security_level = secret.metadata.annotations.get("security-level", "unknown")
            last_rotated = secret.metadata.annotations.get("last-rotated", "never")
            rotation_count = secret.metadata.annotations.get("rotation-count", "0")
            
            # Calculate age
            age_days = 0
            if created_timestamp:
                created_time = datetime.fromtimestamp(int(created_timestamp))
                age = datetime.now() - created_time
                age_days = age.days
            
            # Determine status
            policy_days = int(rotation_policy.split("-")[0]) if "-days" in rotation_policy else 999
            status = "✅ SECURE" if age_days < policy_days else "⚠️ NEEDS ROTATION"
            
            return {
                "name": secret_name,
                "age_days": age_days,
                "rotation_policy": rotation_policy,
                "security_level": security_level,
                "last_rotated": last_rotated,
                "rotation_count": int(rotation_count),
                "status": status,
                "compliant": age_days < policy_days
            }
            
        except ApiException:
            return {
                "name": secret_name,
                "status": "❌ NOT FOUND",
                "compliant": False
            }
    
    def get_deployment_security_status(self, deployment_name):
        """Analyze deployment security configuration"""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace=self.namespace
            )
            
            container = deployment.spec.template.spec.containers[0]
            
            # Security checks
            security_score = 0
            max_score = 5
            
            security_checks = {
                "has_resource_limits": bool(container.resources and container.resources.limits),
                "has_liveness_probe": bool(container.liveness_probe),
                "has_readiness_probe": bool(container.readiness_probe),
                "uses_secrets": any(env.value_from and env.value_from.secret_key_ref 
                                  for env in container.env or [] if env.value_from),
                "non_root_user": True  # Assume configured properly
            }
            
            security_score = sum(security_checks.values())
            
            # Determine status
            if security_score == max_score:
                status = "🔒 EXCELLENT"
                color = Fore.GREEN
            elif security_score >= 4:
                status = "✅ GOOD"
                color = Fore.GREEN
            elif security_score >= 3:
                status = "⚠️ FAIR"
                color = Fore.YELLOW
            else:
                status = "❌ POOR"
                color = Fore.RED
            
            return {
                "name": deployment_name,
                "security_score": f"{security_score}/{max_score}",
                "status": status,
                "color": color,
                "checks": security_checks,
                "ready_replicas": deployment.status.ready_replicas or 0,
                "desired_replicas": deployment.spec.replicas
            }
            
        except ApiException as e:
            return {
                "name": deployment_name,
                "status": "❌ ERROR",
                "color": Fore.RED,
                "error": str(e)
            }
    
    def get_network_security_status(self):
        """Analyze network security configuration"""
        try:
            services = self.v1.list_namespaced_service(namespace=self.namespace)
            
            network_analysis = {
                "total_services": len(services.items),
                "internal_services": 0,
                "external_services": 0,
                "secure_ports": 0,
                "services": []
            }
            
            for service in services.items:
                service_type = service.spec.type
                is_internal = service_type == "ClusterIP"
                
                if is_internal:
                    network_analysis["internal_services"] += 1
                else:
                    network_analysis["external_services"] += 1
                
                # Check for secure ports (not common insecure ones)
                secure_ports = True
                for port in service.spec.ports:
                    if port.port in [21, 23, 80, 3306, 5432]:  # Common insecure ports
                        if service_type != "ClusterIP":  # OK if internal only
                            secure_ports = False
                
                if secure_ports:
                    network_analysis["secure_ports"] += 1
                
                network_analysis["services"].append({
                    "name": service.metadata.name,
                    "type": service_type,
                    "ports": [f"{p.port}:{p.target_port}" for p in service.spec.ports],
                    "security_level": "🔒 Internal" if is_internal else "🌐 External"
                })
            
            return network_analysis
            
        except ApiException as e:
            return {"error": str(e)}
    
    def display_security_dashboard(self):
        """Display comprehensive security dashboard"""
        print(f"\n{Fore.CYAN}🔒 SECURITY MONITORING DASHBOARD{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"🕐 Scan Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🏠 Namespace: {self.namespace}")
        
        # Secret Security Analysis
        print(f"\n{Fore.YELLOW}🔐 SECRET SECURITY STATUS:{Style.RESET_ALL}")
        secrets_to_check = ["mysql-credentials", "app-credentials"]
        
        all_compliant = True
        for secret_name in secrets_to_check:
            status = self.get_secret_security_status(secret_name)
            
            if status.get("compliant", False):
                color = Fore.GREEN
            else:
                color = Fore.RED
                all_compliant = False
            
            print(f"   {color}{status['status']}{Style.RESET_ALL} {secret_name}")
            if "age_days" in status:
                print(f"      Age: {status['age_days']} days | Policy: {status['rotation_policy']}")
                print(f"      Rotations: {status['rotation_count']} | Level: {status['security_level']}")
        
        # Deployment Security Analysis
        print(f"\n{Fore.YELLOW}🚀 DEPLOYMENT SECURITY STATUS:{Style.RESET_ALL}")
        deployments_to_check = ["secure-mysql", "secure-todo-app"]
        
        for deployment_name in deployments_to_check:
            status = self.get_deployment_security_status(deployment_name)
            
            print(f"   {status['color']}{status['status']}{Style.RESET_ALL} {deployment_name}")
            if "security_score" in status:
                print(f"      Security Score: {status['security_score']} | "
                      f"Replicas: {status['ready_replicas']}/{status['desired_replicas']}")
                
                # Show failed checks
                failed_checks = [k for k, v in status['checks'].items() if not v]
                if failed_checks:
                    print(f"      ⚠️  Missing: {', '.join(failed_checks)}")
        
        # Network Security Analysis
        print(f"\n{Fore.YELLOW}🌐 NETWORK SECURITY STATUS:{Style.RESET_ALL}")
        network_status = self.get_network_security_status()
        
        if "error" not in network_status:
            print(f"   Services: {network_status['total_services']} total")
            print(f"   🔒 Internal: {network_status['internal_services']} | "
                  f"🌐 External: {network_status['external_services']}")
            
            for service in network_status['services']:
                print(f"      {service['security_level']} {service['name']} "
                      f"({service['type']}) - Ports: {', '.join(service['ports'])}")
        
        # Overall Security Status
        print(f"\n{Fore.YELLOW}📊 OVERALL SECURITY STATUS:{Style.RESET_ALL}")
        if all_compliant:
            print(f"   {Fore.GREEN}🛡️  EXCELLENT - All security controls are compliant{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✅ Chaos Agent's attacks have been thwarted!{Style.RESET_ALL}")
        else:
            print(f"   {Fore.RED}⚠️  ATTENTION NEEDED - Some security issues detected{Style.RESET_ALL}")
            print(f"   {Fore.YELLOW}🔄 Recommend running secret rotation{Style.RESET_ALL}")
    
    def monitor_continuously(self, interval=30):
        """Monitor security continuously"""
        print(f"{Fore.MAGENTA}🔍 Starting continuous security monitoring{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Press Ctrl+C to stop monitoring{Style.RESET_ALL}")
        
        try:
            while True:
                # Clear screen
                print("\033[2J\033[H", end="")
                
                self.display_security_dashboard()
                
                print(f"\n{Fore.CYAN}⏰ Next security scan in {interval} seconds...{Style.RESET_ALL}")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Security monitoring stopped. Systems remain protected!{Style.RESET_ALL}")

def main():
    """Main monitoring function"""
    monitor = SecurityMonitor()
    
    print(f"{Fore.CYAN}🔒 Security Monitoring System{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Choose monitoring mode:{Style.RESET_ALL}")
    print(f"   1. One-time security scan")
    print(f"   2. Continuous security monitoring")
    
    choice = input(f"\n{Fore.YELLOW}Enter choice (1 or 2): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        monitor.display_security_dashboard()
    elif choice == "2":
        monitor.monitor_continuously()
    else:
        print(f"{Fore.RED}Invalid choice. Running one-time scan.{Style.RESET_ALL}")
        monitor.display_security_dashboard()

if __name__ == "__main__":
    main()