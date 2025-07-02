#!/usr/bin/env python3
"""
🔐 ADVANCED SECRET LIFECYCLE MANAGEMENT
Enterprise-grade secret operations and compliance system

This script provides comprehensive secret management capabilities
beyond basic rotation - for production-ready secret governance!
"""

import os
import sys
import time
import json
import base64
import secrets
import string
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style
from cryptography.fernet import Fernet
import yaml

# Initialize colorful output
init(autoreset=True)

class EnterpriseSecretManager:
    """Advanced secret lifecycle management with enterprise features"""
    
    def __init__(self):
        print(f"{Fore.CYAN}🔐 Initializing Enterprise Secret Manager...{Style.RESET_ALL}")
        
        # Load Kubernetes config
        try:
            config.load_kube_config()
        except:
            try:
                config.load_incluster_config()
            except:
                print(f"{Fore.RED}❌ Could not load K8s config!{Style.RESET_ALL}")
                sys.exit(1)
        
        # Initialize K8s clients
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.namespace = "secure-todo"
        
        # Secret policies and configurations
        self.secret_policies = {
            "mysql-credentials": {
                "rotation_days": 30,
                "password_length": 32,
                "complexity": "high",
                "backup_count": 3
            },
            "app-credentials": {
                "rotation_days": 7,
                "password_length": 64,
                "complexity": "maximum",
                "backup_count": 5
            }
        }
        
        print(f"{Fore.GREEN}✅ Enterprise Secret Manager ready!{Style.RESET_ALL}")
    
    def generate_secure_password(self, length=32, complexity="high"):
        """Generate password based on complexity requirements"""
        if complexity == "maximum":
            # Maximum security: all character types, no ambiguous chars
            alphabet = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%^&*+-="
        elif complexity == "high":
            # High security: letters, numbers, symbols
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*+-="
        else:
            # Standard security: letters and numbers
            alphabet = string.ascii_letters + string.digits
        
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def hash_secret_value(self, value):
        """Create hash of secret value for audit purposes"""
        return hashlib.sha256(value.encode()).hexdigest()[:16]
    
    def backup_secret(self, secret_name):
        """Create backup of existing secret before rotation"""
        try:
            # Read current secret
            current_secret = self.v1.read_namespaced_secret(
                name=secret_name,
                namespace=self.namespace
            )
            
            # Create backup secret name
            timestamp = int(time.time())
            backup_name = f"{secret_name}-backup-{timestamp}"
            
            # Create backup secret
            backup_secret = client.V1Secret(
                metadata=client.V1ObjectMeta(
                    name=backup_name,
                    namespace=self.namespace,
                    labels={
                        "backup-of": secret_name,
                        "backup-timestamp": str(timestamp),
                        "managed-by": "enterprise-secret-manager"
                    },
                    annotations={
                        "backup-reason": "pre-rotation-backup",
                        "original-secret": secret_name,
                        "backup-date": datetime.now().isoformat()
                    }
                ),
                data=current_secret.data,
                type=current_secret.type
            )
            
            self.v1.create_namespaced_secret(
                namespace=self.namespace,
                body=backup_secret
            )
            
            print(f"{Fore.BLUE}💾 Backup created: {backup_name}{Style.RESET_ALL}")
            return backup_name
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Backup failed for {secret_name}: {e}{Style.RESET_ALL}")
            return None
    
    def cleanup_old_backups(self, secret_name, keep_count=3):
        """Clean up old backup secrets, keeping only the most recent"""
        try:
            # List all secrets with backup label
            secrets = self.v1.list_namespaced_secret(
                namespace=self.namespace,
                label_selector=f"backup-of={secret_name}"
            )
            
            # Sort by timestamp (newest first)
            backup_secrets = []
            for secret in secrets.items:
                timestamp = secret.metadata.labels.get("backup-timestamp", "0")
                backup_secrets.append((int(timestamp), secret.metadata.name))
            
            backup_secrets.sort(reverse=True)
            
            # Delete old backups beyond keep_count
            deleted_count = 0
            for i, (timestamp, backup_name) in enumerate(backup_secrets):
                if i >= keep_count:
                    try:
                        self.v1.delete_namespaced_secret(
                            name=backup_name,
                            namespace=self.namespace
                        )
                        deleted_count += 1
                        print(f"{Fore.YELLOW}🗑️  Cleaned up old backup: {backup_name}{Style.RESET_ALL}")
                    except ApiException:
                        pass
            
            if deleted_count > 0:
                print(f"{Fore.GREEN}✅ Cleaned up {deleted_count} old backups{Style.RESET_ALL}")
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Backup cleanup failed: {e}{Style.RESET_ALL}")
    
    def audit_secret_access(self, secret_name, operation, details=None):
        """Create audit log entry for secret operations"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "secret_name": secret_name,
            "operation": operation,
            "namespace": self.namespace,
            "user": "enterprise-secret-manager",
            "details": details or {}
        }
        
        # In production, this would go to a secure audit system
        # For demo, we'll store in a ConfigMap
        try:
            audit_data = json.dumps(audit_entry)
            
            # Try to read existing audit log
            try:
                audit_cm = self.v1.read_namespaced_config_map(
                    name="secret-audit-log",
                    namespace=self.namespace
                )
                existing_logs = audit_cm.data.get("audit_entries", "[]")
                logs = json.loads(existing_logs)
            except ApiException:
                logs = []
                audit_cm = None
            
            # Add new entry
            logs.append(audit_entry)
            
            # Keep only last 100 entries
            if len(logs) > 100:
                logs = logs[-100:]
            
            # Create or update audit ConfigMap
            audit_configmap = client.V1ConfigMap(
                metadata=client.V1ObjectMeta(
                    name="secret-audit-log",
                    namespace=self.namespace,
                    labels={"audit": "secret-operations"}
                ),
                data={"audit_entries": json.dumps(logs, indent=2)}
            )
            
            if audit_cm:
                self.v1.patch_namespaced_config_map(
                    name="secret-audit-log",
                    namespace=self.namespace,
                    body=audit_configmap
                )
            else:
                self.v1.create_namespaced_config_map(
                    namespace=self.namespace,
                    body=audit_configmap
                )
            
            print(f"{Fore.CYAN}📝 Audit logged: {operation} on {secret_name}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Audit logging failed: {e}{Style.RESET_ALL}")
    
    def validate_secret_compliance(self, secret_name):
        """Validate secret against compliance requirements"""
        try:
            secret = self.v1.read_namespaced_secret(
                name=secret_name,
                namespace=self.namespace
            )
            
            compliance_issues = []
            
            # Check required annotations
            required_annotations = [
                "created-timestamp",
                "rotation-policy",
                "security-level"
            ]
            
            for annotation in required_annotations:
                if annotation not in (secret.metadata.annotations or {}):
                    compliance_issues.append(f"Missing annotation: {annotation}")
            
            # Check rotation age
            created_timestamp = secret.metadata.annotations.get("created-timestamp")
            if created_timestamp:
                created_time = datetime.fromtimestamp(int(created_timestamp))
                age = datetime.now() - created_time
                
                policy = self.secret_policies.get(secret_name, {})
                max_age = policy.get("rotation_days", 30)
                
                if age.days > max_age:
                    compliance_issues.append(f"Secret exceeds rotation policy: {age.days} > {max_age} days")
            
            # Check secret data structure
            if not secret.data:
                compliance_issues.append("Secret has no data")
            
            # Check for weak passwords (basic check)
            for key, value in (secret.data or {}).items():
                if "password" in key.lower():
                    decoded_value = base64.b64decode(value).decode()
                    if len(decoded_value) < 12:
                        compliance_issues.append(f"Weak password in {key}: too short")
            
            return {
                "compliant": len(compliance_issues) == 0,
                "issues": compliance_issues,
                "last_checked": datetime.now().isoformat()
            }
            
        except ApiException as e:
            return {
                "compliant": False,
                "issues": [f"Cannot access secret: {e}"],
                "last_checked": datetime.now().isoformat()
            }
    
    def generate_compliance_report(self):
        """Generate comprehensive compliance report"""
        print(f"{Fore.CYAN}📊 Generating Compliance Report...{Style.RESET_ALL}")
        
        report = {
            "report_date": datetime.now().isoformat(),
            "namespace": self.namespace,
            "secrets_analyzed": [],
            "overall_compliance": True,
            "total_issues": 0
        }
        
        # Check all managed secrets
        managed_secrets = list(self.secret_policies.keys())
        
        for secret_name in managed_secrets:
            compliance = self.validate_secret_compliance(secret_name)
            
            secret_report = {
                "name": secret_name,
                "compliant": compliance["compliant"],
                "issues": compliance["issues"],
                "issue_count": len(compliance["issues"])
            }
            
            report["secrets_analyzed"].append(secret_report)
            
            if not compliance["compliant"]:
                report["overall_compliance"] = False
                report["total_issues"] += len(compliance["issues"])
        
        return report
    
    def display_compliance_report(self):
        """Display formatted compliance report"""
        report = self.generate_compliance_report()
        
        print(f"\n{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🔐 SECRET COMPLIANCE REPORT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        print(f"📅 Report Date: {report['report_date']}")
        print(f"🏠 Namespace: {report['namespace']}")
        
        # Overall status
        if report["overall_compliance"]:
            print(f"✅ {Fore.GREEN}OVERALL STATUS: COMPLIANT{Style.RESET_ALL}")
        else:
            print(f"❌ {Fore.RED}OVERALL STATUS: NON-COMPLIANT{Style.RESET_ALL}")
            print(f"🚨 Total Issues: {report['total_issues']}")
        
        print(f"\n{Fore.YELLOW}📋 SECRET ANALYSIS:{Style.RESET_ALL}")
        
        for secret in report["secrets_analyzed"]:
            if secret["compliant"]:
                status_color = Fore.GREEN
                status = "✅ COMPLIANT"
            else:
                status_color = Fore.RED
                status = "❌ NON-COMPLIANT"
            
            print(f"   {status_color}{status}{Style.RESET_ALL} {secret['name']}")
            
            if secret["issues"]:
                for issue in secret["issues"]:
                    print(f"      🚨 {issue}")
        
        # Recommendations
        if not report["overall_compliance"]:
            print(f"\n{Fore.YELLOW}🔧 RECOMMENDED ACTIONS:{Style.RESET_ALL}")
            print(f"   1. Run secret rotation: python3 rotate-secrets.py")
            print(f"   2. Update secret annotations for compliance")
            print(f"   3. Strengthen weak passwords")
            print(f"   4. Review and update rotation policies")
    
    def export_secrets_manifest(self, output_dir="k8s-manifests"):
        """Export current secrets as Kubernetes manifests (for GitOps)"""
        print(f"{Fore.CYAN}📤 Exporting secrets to manifests...{Style.RESET_ALL}")
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        for secret_name in self.secret_policies.keys():
            try:
                secret = self.v1.read_namespaced_secret(
                    name=secret_name,
                    namespace=self.namespace
                )
                
                # Create manifest (with data removed for security)
                manifest = {
                    "apiVersion": "v1",
                    "kind": "Secret",
                    "metadata": {
                        "name": secret.metadata.name,
                        "namespace": secret.metadata.namespace,
                        "labels": dict(secret.metadata.labels or {}),
                        "annotations": dict(secret.metadata.annotations or {})
                    },
                    "type": secret.type,
                    "data": {
                        key: "# REDACTED - Use external secret management"
                        for key in secret.data.keys()
                    }
                }
                
                # Write to file
                output_file = Path(output_dir) / f"{secret_name}.yaml"
                with open(output_file, 'w') as f:
                    yaml.dump(manifest, f, default_flow_style=False)
                
                print(f"{Fore.GREEN}✅ Exported: {output_file}{Style.RESET_ALL}")
                
            except ApiException as e:
                print(f"{Fore.RED}❌ Failed to export {secret_name}: {e}{Style.RESET_ALL}")
    
    def interactive_menu(self):
        """Interactive menu for secret management operations"""
        while True:
            print(f"\n{Fore.CYAN}🔐 ENTERPRISE SECRET MANAGER{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
            print(f"1. 📊 Generate Compliance Report")
            print(f"2. 💾 Backup All Secrets")
            print(f"3. 🗑️  Cleanup Old Backups")
            print(f"4. 📤 Export Secret Manifests")
            print(f"5. 🔍 Audit Secret Access")
            print(f"6. 🔄 Validate All Secrets")
            print(f"7. 📝 View Audit Log")
            print(f"8. ❌ Exit")
            
            choice = input(f"\n{Fore.YELLOW}Enter choice (1-8): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.display_compliance_report()
            
            elif choice == "2":
                print(f"{Fore.YELLOW}💾 Creating backups...{Style.RESET_ALL}")
                for secret_name in self.secret_policies.keys():
                    self.backup_secret(secret_name)
            
            elif choice == "3":
                print(f"{Fore.YELLOW}🗑️  Cleaning up old backups...{Style.RESET_ALL}")
                for secret_name in self.secret_policies.keys():
                    policy = self.secret_policies[secret_name]
                    self.cleanup_old_backups(secret_name, policy.get("backup_count", 3))
            
            elif choice == "4":
                self.export_secrets_manifest()
            
            elif choice == "5":
                secret_name = input(f"{Fore.YELLOW}Enter secret name: {Style.RESET_ALL}").strip()
                operation = input(f"{Fore.YELLOW}Enter operation: {Style.RESET_ALL}").strip()
                self.audit_secret_access(secret_name, operation)
            
            elif choice == "6":
                print(f"{Fore.YELLOW}🔍 Validating all secrets...{Style.RESET_ALL}")
                for secret_name in self.secret_policies.keys():
                    compliance = self.validate_secret_compliance(secret_name)
                    status = "✅ COMPLIANT" if compliance["compliant"] else "❌ NON-COMPLIANT"
                    print(f"   {status} {secret_name}")
            
            elif choice == "7":
                self.display_audit_log()
            
            elif choice == "8":
                print(f"{Fore.GREEN}👋 Goodbye! Secrets remain secure.{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please try again.{Style.RESET_ALL}")
    
    def display_audit_log(self):
        """Display recent audit log entries"""
        try:
            audit_cm = self.v1.read_namespaced_config_map(
                name="secret-audit-log",
                namespace=self.namespace
            )
            
            logs = json.loads(audit_cm.data.get("audit_entries", "[]"))
            
            print(f"\n{Fore.CYAN}📝 RECENT AUDIT LOG ENTRIES:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            # Show last 10 entries
            for entry in logs[-10:]:
                timestamp = entry["timestamp"][:19]  # Remove microseconds
                print(f"{Fore.YELLOW}{timestamp}{Style.RESET_ALL} | "
                      f"{entry['operation']} | "
                      f"{entry['secret_name']}")
            
            if not logs:
                print(f"{Fore.BLUE}📝 No audit entries found{Style.RESET_ALL}")
        
        except ApiException:
            print(f"{Fore.BLUE}📝 No audit log available yet{Style.RESET_ALL}")

def main():
    """Main function"""
    print(f"{Fore.CYAN}🔐 Enterprise Secret Lifecycle Manager{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Advanced secret operations and compliance{Style.RESET_ALL}")
    print()
    
    manager = EnterpriseSecretManager()
    manager.interactive_menu()

if __name__ == "__main__":
    main()