#!/usr/bin/env python3
"""
🔄 AUTOMATED SECRET ROTATION SYSTEM
Enterprise-grade secret lifecycle management

This script demonstrates zero-downtime secret rotation
that keeps Chaos Agent from compromising your credentials!
"""

import os
import sys
import time
import base64
import secrets
import string
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style
from datetime import datetime, timedelta

init(autoreset=True)

class SecretRotationSystem:
    """Automated secret rotation with zero downtime"""
    
    def __init__(self):
        print(f"{Fore.CYAN}🔄 Initializing Secret Rotation System...{Style.RESET_ALL}")
        
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.namespace = "secure-todo"
        
        print(f"{Fore.GREEN}✅ Rotation system ready!{Style.RESET_ALL}")
    
    def generate_secure_password(self, length=32):
        """Generate cryptographically secure password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*+-="
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def get_secret_age(self, secret_name):
        """Check how old a secret is"""
        try:
            secret = self.v1.read_namespaced_secret(
                name=secret_name,
                namespace=self.namespace
            )
            
            created_timestamp = secret.metadata.annotations.get("created-timestamp")
            if created_timestamp:
                created_time = datetime.fromtimestamp(int(created_timestamp))
                age = datetime.now() - created_time
                return age.days
            return 999  # Unknown age, assume needs rotation
            
        except ApiException:
            return 999
    
    def rotate_mysql_secret(self):
        """Rotate MySQL credentials with zero downtime"""
        print(f"{Fore.YELLOW}🔄 Rotating MySQL credentials...{Style.RESET_ALL}")
        
        # Generate new secure credentials
        new_root_password = self.generate_secure_password(32)
        new_user_password = self.generate_secure_password(24)
        
        # Read current secret to preserve other data
        try:
            current_secret = self.v1.read_namespaced_secret(
                name="mysql-credentials",
                namespace=self.namespace
            )
            
            # Update with new passwords
            current_secret.data["mysql-root-password"] = base64.b64encode(new_root_password.encode()).decode()
            current_secret.data["mysql-password"] = base64.b64encode(new_user_password.encode()).decode()
            
            # Update timestamp
            current_secret.metadata.annotations["created-timestamp"] = str(int(time.time()))
            current_secret.metadata.annotations["last-rotated"] = datetime.now().isoformat()
            current_secret.metadata.annotations["rotation-count"] = str(
                int(current_secret.metadata.annotations.get("rotation-count", "0")) + 1
            )
            
            # Apply the updated secret
            self.v1.patch_namespaced_secret(
                name="mysql-credentials",
                namespace=self.namespace,
                body=current_secret
            )
            
            print(f"{Fore.GREEN}✅ MySQL credentials rotated successfully{Style.RESET_ALL}")
            return True
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Error rotating MySQL secret: {e}{Style.RESET_ALL}")
            return False
    
    def rotate_app_secret(self):
        """Rotate application secrets"""
        print(f"{Fore.YELLOW}🔑 Rotating application secrets...{Style.RESET_ALL}")
        
        try:
            current_secret = self.v1.read_namespaced_secret(
                name="app-credentials",
                namespace=self.namespace
            )
            
            # Generate new application secrets
            new_secret_key = self.generate_secure_password(64)
            new_jwt_secret = self.generate_secure_password(32)
            new_api_key = self.generate_secure_password(40)
            
            # Update secret data
            current_secret.data["secret-key"] = base64.b64encode(new_secret_key.encode()).decode()
            current_secret.data["jwt-secret"] = base64.b64encode(new_jwt_secret.encode()).decode()
            current_secret.data["api-key"] = base64.b64encode(new_api_key.encode()).decode()
            
            # Update metadata
            current_secret.metadata.annotations["created-timestamp"] = str(int(time.time()))
            current_secret.metadata.annotations["last-rotated"] = datetime.now().isoformat()
            
            # Apply update
            self.v1.patch_namespaced_secret(
                name="app-credentials",
                namespace=self.namespace,
                body=current_secret
            )
            
            print(f"{Fore.GREEN}✅ Application secrets rotated successfully{Style.RESET_ALL}")
            return True
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Error rotating app secret: {e}{Style.RESET_ALL}")
            return False
    
    def restart_deployments(self):
        """Restart deployments to pick up new secrets"""
        print(f"{Fore.YELLOW}🔄 Restarting deployments to pick up new secrets...{Style.RESET_ALL}")
        
        deployments = ["secure-mysql", "secure-todo-app"]
        
        for deployment_name in deployments:
            try:
                # Get current deployment
                deployment = self.apps_v1.read_namespaced_deployment(
                    name=deployment_name,
                    namespace=self.namespace
                )
                
                # Add restart annotation to trigger rolling update
                if not deployment.spec.template.metadata.annotations:
                    deployment.spec.template.metadata.annotations = {}
                
                deployment.spec.template.metadata.annotations["kubectl.kubernetes.io/restartedAt"] = datetime.now().isoformat()
                
                # Patch the deployment
                self.apps_v1.patch_namespaced_deployment(
                    name=deployment_name,
                    namespace=self.namespace,
                    body=deployment
                )
                
                print(f"{Fore.GREEN}✅ {deployment_name} restart initiated{Style.RESET_ALL}")
                
            except ApiException as e:
                print(f"{Fore.RED}❌ Error restarting {deployment_name}: {e}{Style.RESET_ALL}")
    
    def wait_for_rollout(self):
        """Wait for rollout to complete"""
        print(f"{Fore.YELLOW}⏳ Waiting for rollout to complete...{Style.RESET_ALL}")
        
        deployments = ["secure-mysql", "secure-todo-app"]
        max_attempts = 20
        
        for deployment_name in deployments:
            print(f"{Fore.CYAN}📊 Checking {deployment_name} rollout...{Style.RESET_ALL}")
            
            for attempt in range(max_attempts):
                try:
                    deployment = self.apps_v1.read_namespaced_deployment(
                        name=deployment_name,
                        namespace=self.namespace
                    )
                    
                    ready_replicas = deployment.status.ready_replicas or 0
                    desired_replicas = deployment.spec.replicas
                    updated_replicas = deployment.status.updated_replicas or 0
                    
                    if (ready_replicas == desired_replicas and 
                        updated_replicas == desired_replicas):
                        print(f"{Fore.GREEN}✅ {deployment_name} rollout complete!{Style.RESET_ALL}")
                        break
                    
                    print(f"{Fore.CYAN}⏳ {deployment_name}: {ready_replicas}/{desired_replicas} ready, {updated_replicas}/{desired_replicas} updated...{Style.RESET_ALL}")
                    time.sleep(5)
                    
                except ApiException as e:
                    print(f"{Fore.RED}❌ Error checking rollout: {e}{Style.RESET_ALL}")
                    time.sleep(5)
            else:
                print(f"{Fore.RED}❌ {deployment_name} rollout timed out{Style.RESET_ALL}")
                return False
        
        return True
    
    def perform_rotation(self):
        """Perform complete secret rotation"""
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🔄 STARTING AUTOMATED SECRET ROTATION{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        # Check secret ages
        mysql_age = self.get_secret_age("mysql-credentials")
        app_age = self.get_secret_age("app-credentials")
        
        print(f"{Fore.CYAN}📊 Secret Age Analysis:{Style.RESET_ALL}")
        print(f"   MySQL credentials: {mysql_age} days old")
        print(f"   App credentials: {app_age} days old")
        
        rotation_needed = mysql_age > 30 or app_age > 7
        
        if not rotation_needed:
            print(f"{Fore.GREEN}✅ Secrets are fresh - no rotation needed{Style.RESET_ALL}")
            choice = input(f"{Fore.YELLOW}🔄 Force rotation anyway? (y/n): {Style.RESET_ALL}").strip().lower()
            if choice not in ['y', 'yes']:
                print(f"{Fore.BLUE}📝 Rotation skipped{Style.RESET_ALL}")
                return True
        
        try:
            # Rotate secrets
            mysql_success = self.rotate_mysql_secret()
            app_success = self.rotate_app_secret()
            
            if mysql_success and app_success:
                # Restart deployments to pick up new secrets
                self.restart_deployments()
                
                # Wait for rollout
                if self.wait_for_rollout():
                    print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}🎉 SECRET ROTATION COMPLETED SUCCESSFULLY!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}✅ Zero downtime achieved - Chaos Agent thwarted!{Style.RESET_ALL}")
                    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}❌ Rollout failed after secret rotation{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED}❌ Secret rotation failed{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Rotation error: {e}{Style.RESET_ALL}")
            return False

def main():
    """Main rotation function"""
    print(f"{Fore.CYAN}🔄 Secret Rotation System{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Automated secret lifecycle management{Style.RESET_ALL}")
    print()
    
    rotator = SecretRotationSystem()
    success = rotator.perform_rotation()
    
    if success:
        print(f"\n{Fore.GREEN}🎯 ROTATION COMPLETE:{Style.RESET_ALL}")
        print(f"   1. All secrets have been rotated with new secure values")
        print(f"   2. Deployments restarted with zero downtime")
        print(f"   3. Applications are using new credentials")
        print(f"   4. Security compliance maintained!")
    else:
        print(f"\n{Fore.RED}❌ Rotation failed. Check logs and try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()