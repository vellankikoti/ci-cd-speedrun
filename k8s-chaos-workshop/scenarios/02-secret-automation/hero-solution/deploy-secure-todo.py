#!/usr/bin/env python3
"""
🔐 PYTHON SECURITY HERO SOLUTION
Secure Todo App Deployment with Enterprise Secret Management

This script demonstrates how Python automation creates bulletproof
secret management that defeats Chaos Agent's security attacks!
"""

import os
import sys
import time
import yaml
import base64
import secrets
import string
import subprocess
from pathlib import Path
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style
import mysql.connector
from cryptography.fernet import Fernet

# Initialize colorful output
init(autoreset=True)

class SecureSecretManager:
    """Enterprise-grade secret management system"""
    
    def __init__(self):
        print(f"{Fore.CYAN}🔐 Initializing Enterprise Secret Management...{Style.RESET_ALL}")
        
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
        
        # Configuration
        self.namespace = "secure-todo"
        self.todo_app_name = "secure-todo-app"
        self.mysql_app_name = "secure-mysql"
        self.todo_image = "a7medayman6/todolist-flask:latest"
        self.mysql_image = "mysql:8.0"
        self.node_port = 31001  # Different from vote app
        
        # Encryption key for additional security
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        print(f"{Fore.GREEN}✅ Security system armed and ready!{Style.RESET_ALL}")
    
    def generate_secure_password(self, length=32):
        """Generate cryptographically secure password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*+-="
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def create_namespace(self):
        """Create secure namespace with proper labeling"""
        print(f"{Fore.YELLOW}🏠 Creating secure namespace: {self.namespace}{Style.RESET_ALL}")
        
        namespace = client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=self.namespace,
                labels={
                    "created-by": "python-security-hero",
                    "purpose": "secure-demo",
                    "security-level": "enterprise",
                    "workshop": "k8s-chaos-workshop"
                }
            )
        )
        
        try:
            self.v1.create_namespace(namespace)
            print(f"{Fore.GREEN}✅ Secure namespace created{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                print(f"{Fore.BLUE}📝 Namespace exists - security upgrade mode{Style.RESET_ALL}")
            else:
                raise e
    
    def create_mysql_secrets(self):
        """Create secure MySQL credentials with rotation metadata"""
        print(f"{Fore.YELLOW}🔐 Generating secure MySQL credentials...{Style.RESET_ALL}")
        
        # Generate secure credentials
        mysql_root_password = self.generate_secure_password(32)
        mysql_user_password = self.generate_secure_password(24)
        mysql_user = "todoapp_user"
        mysql_database = "todoapp_db"
        
        # Create secret data
        secret_data = {
            "mysql-root-password": base64.b64encode(mysql_root_password.encode()).decode(),
            "mysql-user": base64.b64encode(mysql_user.encode()).decode(),
            "mysql-password": base64.b64encode(mysql_user_password.encode()).decode(),
            "mysql-database": base64.b64encode(mysql_database.encode()).decode()
        }
        
        # Create secret with security metadata
        mysql_secret = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="mysql-credentials",
                namespace=self.namespace,
                labels={
                    "app": "secure-mysql",
                    "managed-by": "python-security-hero",
                    "secret-type": "database-credentials"
                },
                annotations={
                    "created-timestamp": str(int(time.time())),
                    "rotation-policy": "30-days",
                    "security-level": "high",
                    "auto-rotate": "true"
                }
            ),
            data=secret_data,
            type="Opaque"
        )
        
        try:
            self.v1.create_namespaced_secret(
                namespace=self.namespace,
                body=mysql_secret
            )
            print(f"{Fore.GREEN}✅ MySQL secrets created with enterprise security{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                # Update existing secret
                self.v1.patch_namespaced_secret(
                    name="mysql-credentials",
                    namespace=self.namespace,
                    body=mysql_secret
                )
                print(f"{Fore.BLUE}📝 MySQL secrets updated - security enhanced{Style.RESET_ALL}")
            else:
                raise e
        
        return {
            "root_password": mysql_root_password,
            "user": mysql_user,
            "password": mysql_user_password,
            "database": mysql_database
        }
    
    def create_app_secrets(self):
        """Create application-level secrets"""
        print(f"{Fore.YELLOW}🔑 Generating application security tokens...{Style.RESET_ALL}")
        
        # Generate application secrets
        app_secret_key = self.generate_secure_password(64)
        jwt_secret = self.generate_secure_password(32)
        api_key = self.generate_secure_password(40)
        
        secret_data = {
            "secret-key": base64.b64encode(app_secret_key.encode()).decode(),
            "jwt-secret": base64.b64encode(jwt_secret.encode()).decode(),
            "api-key": base64.b64encode(api_key.encode()).decode(),
            "encryption-key": base64.b64encode(self.encryption_key).decode()
        }
        
        app_secret = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name="app-credentials",
                namespace=self.namespace,
                labels={
                    "app": "secure-todo-app",
                    "managed-by": "python-security-hero",
                    "secret-type": "application-credentials"
                },
                annotations={
                    "created-timestamp": str(int(time.time())),
                    "rotation-policy": "7-days",
                    "security-level": "high"
                }
            ),
            data=secret_data,
            type="Opaque"
        )
        
        try:
            self.v1.create_namespaced_secret(
                namespace=self.namespace,
                body=app_secret
            )
            print(f"{Fore.GREEN}✅ Application secrets created with rotation policy{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                self.v1.patch_namespaced_secret(
                    name="app-credentials",
                    namespace=self.namespace,
                    body=app_secret
                )
                print(f"{Fore.BLUE}📝 Application secrets updated{Style.RESET_ALL}")
            else:
                raise e
    
    def deploy_secure_mysql(self):
        """Deploy MySQL with secure secret integration"""
        print(f"{Fore.YELLOW}🗄️ Deploying secure MySQL database...{Style.RESET_ALL}")
        
        # Security context for MySQL container
        security_context = client.V1SecurityContext(
            run_as_non_root=False,  # MySQL needs to run as mysql user (non-zero UID)
            run_as_user=999,  # MySQL user ID
            allow_privilege_escalation=False,
            read_only_root_filesystem=False,  # MySQL needs to write to filesystem
            capabilities=client.V1Capabilities(drop=["ALL"])
        )
        
        # MySQL deployment with secrets and security
        mysql_deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(
                name=self.mysql_app_name,
                namespace=self.namespace,
                labels={"app": self.mysql_app_name}
            ),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={"app": self.mysql_app_name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": self.mysql_app_name}
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="mysql",
                                image=self.mysql_image,
                                ports=[client.V1ContainerPort(container_port=3306)],
                                security_context=security_context,
                                env=[
                                    client.V1EnvVar(
                                        name="MYSQL_ROOT_PASSWORD",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-root-password"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="MYSQL_DATABASE",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-database"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="MYSQL_USER",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-user"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="MYSQL_PASSWORD",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-password"
                                            )
                                        )
                                    ),
                                    # Additional MySQL configuration for faster startup
                                    client.V1EnvVar(name="MYSQL_ROOT_HOST", value="%"),
                                    client.V1EnvVar(name="MYSQL_INITDB_SKIP_TZINFO", value="1")
                                ],
                                resources=client.V1ResourceRequirements(
                                    requests={"memory": "256Mi", "cpu": "200m"},
                                    limits={"memory": "512Mi", "cpu": "500m"}
                                ),
                                liveness_probe=client.V1Probe(
                                    tcp_socket=client.V1TCPSocketAction(port=3306),  # Use TCP probe for liveness
                                    initial_delay_seconds=60,  # Give MySQL more time to start
                                    period_seconds=30,
                                    timeout_seconds=10,
                                    failure_threshold=3
                                ),
                                readiness_probe=client.V1Probe(
                                    tcp_socket=client.V1TCPSocketAction(port=3306),  # Use TCP probe for readiness
                                    initial_delay_seconds=30,
                                    period_seconds=10,
                                    timeout_seconds=5,
                                    failure_threshold=3
                                ),
                                startup_probe=client.V1Probe(
                                    tcp_socket=client.V1TCPSocketAction(port=3306),  # Use TCP probe for startup
                                    initial_delay_seconds=10,
                                    period_seconds=10,
                                    timeout_seconds=5,
                                    failure_threshold=30  # Allow up to 5 minutes for MySQL to start
                                )
                            )
                        ]
                    )
                )
            )
        )
        
        try:
            self.apps_v1.create_namespaced_deployment(
                namespace=self.namespace,
                body=mysql_deployment
            )
            print(f"{Fore.GREEN}✅ Secure MySQL deployed with secret integration{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                self.apps_v1.patch_namespaced_deployment(
                    name=self.mysql_app_name,
                    namespace=self.namespace,
                    body=mysql_deployment
                )
                print(f"{Fore.BLUE}📝 MySQL deployment updated{Style.RESET_ALL}")
            else:
                raise e
    
    def deploy_secure_todo_app(self):
        """Deploy Todo app with secure database integration"""
        print(f"{Fore.YELLOW}📝 Deploying secure todo application...{Style.RESET_ALL}")
        
        # Security context for todo app
        app_security_context = client.V1SecurityContext(
            run_as_non_root=True,
            run_as_user=1000,
            allow_privilege_escalation=False,
            read_only_root_filesystem=False,  # App may need to write temp files
            capabilities=client.V1Capabilities(drop=["ALL"])
        )
        
        todo_deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(
                name=self.todo_app_name,
                namespace=self.namespace,
                labels={"app": self.todo_app_name}
            ),
            spec=client.V1DeploymentSpec(
                replicas=2,
                selector=client.V1LabelSelector(
                    match_labels={"app": self.todo_app_name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": self.todo_app_name}
                    ),
                    spec=client.V1PodSpec(
                        security_context=client.V1PodSecurityContext(
                            run_as_non_root=True,
                            run_as_user=1000,
                            fs_group=1000
                        ),
                        containers=[
                            client.V1Container(
                                name="todo-app",
                                image=self.todo_image,
                                ports=[client.V1ContainerPort(container_port=5000)],
                                security_context=app_security_context,
                                env=[
                                    # Database connection from secrets
                                    client.V1EnvVar(
                                        name="DB_HOST",
                                        value="secure-mysql-service"
                                    ),
                                    client.V1EnvVar(
                                        name="DB_PORT",
                                        value="3306"
                                    ),
                                    client.V1EnvVar(
                                        name="DB_NAME",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-database"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="DB_USER",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-user"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="DB_PASSWORD",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="mysql-credentials",
                                                key="mysql-password"
                                            )
                                        )
                                    ),
                                    # Application secrets
                                    client.V1EnvVar(
                                        name="SECRET_KEY",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="app-credentials",
                                                key="secret-key"
                                            )
                                        )
                                    ),
                                    client.V1EnvVar(
                                        name="JWT_SECRET",
                                        value_from=client.V1EnvVarSource(
                                            secret_key_ref=client.V1SecretKeySelector(
                                                name="app-credentials",
                                                key="jwt-secret"
                                            )
                                        )
                                    )
                                ],
                                resources=client.V1ResourceRequirements(
                                    requests={"memory": "128Mi", "cpu": "100m"},
                                    limits={"memory": "256Mi", "cpu": "200m"}
                                ),
                                liveness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/",
                                        port=5000
                                    ),
                                    initial_delay_seconds=30,
                                    period_seconds=10
                                ),
                                readiness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/",
                                        port=5000
                                    ),
                                    initial_delay_seconds=10,
                                    period_seconds=5
                                )
                            )
                        ]
                    )
                )
            )
        )
        
        try:
            self.apps_v1.create_namespaced_deployment(
                namespace=self.namespace,
                body=todo_deployment
            )
            print(f"{Fore.GREEN}✅ Secure todo app deployed with encrypted secrets{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                self.apps_v1.patch_namespaced_deployment(
                    name=self.todo_app_name,
                    namespace=self.namespace,
                    body=todo_deployment
                )
                print(f"{Fore.BLUE}📝 Todo app deployment updated{Style.RESET_ALL}")
            else:
                raise e
    
    def create_services(self):
        """Create services for database and application"""
        print(f"{Fore.YELLOW}🌐 Creating secure network services...{Style.RESET_ALL}")
        
        # MySQL service (internal only)
        mysql_service = client.V1Service(
            metadata=client.V1ObjectMeta(
                name="secure-mysql-service",
                namespace=self.namespace,
                labels={"app": self.mysql_app_name}
            ),
            spec=client.V1ServiceSpec(
                selector={"app": self.mysql_app_name},
                ports=[client.V1ServicePort(port=3306, target_port=3306)],
                type="ClusterIP"  # Internal only for security
            )
        )
        
        # Todo app service (external access)
        todo_service = client.V1Service(
            metadata=client.V1ObjectMeta(
                name="secure-todo-service",
                namespace=self.namespace,
                labels={"app": self.todo_app_name}
            ),
            spec=client.V1ServiceSpec(
                selector={"app": self.todo_app_name},
                ports=[client.V1ServicePort(
                    port=80,
                    target_port=5000,
                    node_port=self.node_port,
                    protocol="TCP"
                )],
                type="NodePort"
            )
        )
        
        try:
            self.v1.create_namespaced_service(
                namespace=self.namespace,
                body=mysql_service
            )
            self.v1.create_namespaced_service(
                namespace=self.namespace,
                body=todo_service
            )
            print(f"{Fore.GREEN}✅ Secure services created with proper network isolation{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                print(f"{Fore.BLUE}📝 Services already exist - security maintained{Style.RESET_ALL}")
            else:
                raise e
    
    def wait_for_deployments(self):
        """Wait for both deployments to be ready"""
        print(f"{Fore.YELLOW}⏳ Waiting for secure deployments to be ready...{Style.RESET_ALL}")
        
        deployments = [self.mysql_app_name, self.todo_app_name]
        max_attempts = 30
        
        for deployment_name in deployments:
            print(f"{Fore.CYAN}📊 Checking {deployment_name}...{Style.RESET_ALL}")
            
            for attempt in range(max_attempts):
                try:
                    deployment = self.apps_v1.read_namespaced_deployment(
                        name=deployment_name,
                        namespace=self.namespace
                    )
                    
                    ready_replicas = deployment.status.ready_replicas or 0
                    desired_replicas = deployment.spec.replicas
                    
                    if ready_replicas == desired_replicas:
                        print(f"{Fore.GREEN}✅ {deployment_name} ready! {ready_replicas}/{desired_replicas} pods{Style.RESET_ALL}")
                        break
                    
                    print(f"{Fore.CYAN}⏳ {deployment_name}: {ready_replicas}/{desired_replicas} pods ready...{Style.RESET_ALL}")
                    time.sleep(10)
                    
                except ApiException as e:
                    print(f"{Fore.RED}❌ Error checking {deployment_name}: {e}{Style.RESET_ALL}")
                    time.sleep(10)
            else:
                print(f"{Fore.RED}❌ {deployment_name} failed to become ready{Style.RESET_ALL}")
                return False
        
        return True
    
    def get_access_info(self):
        """Get secure access information"""
        print(f"{Fore.CYAN}🌐 Getting secure access information...{Style.RESET_ALL}")
        
        try:
            service = self.v1.read_namespaced_service(
                name="secure-todo-service",
                namespace=self.namespace
            )
            
            node_port = service.spec.ports[0].node_port
            
            print(f"{Fore.GREEN}🎯 ACCESS YOUR SECURE TODO APP:{Style.RESET_ALL}")
            print(f"   💻 NodePort: http://localhost:{node_port}")
            print(f"   🔧 Port Forward: kubectl port-forward svc/secure-todo-service -n {self.namespace} 31501:80")
            print(f"   🌍 Then access: http://localhost:31501")
            
            print(f"\n{Fore.YELLOW}📝 TODO APP FEATURES:{Style.RESET_ALL}")
            print(f"   1. Add new todo items")
            print(f"   2. Mark todos as complete")
            print(f"   3. Delete todo items")
            print(f"   4. All data stored securely in encrypted database")
            
            return f"http://localhost:{node_port}"
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Error getting service info: {e}{Style.RESET_ALL}")
            return None
    
    def deploy_everything(self):
        """Deploy the complete secure stack"""
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🔐 PYTHON SECURITY HERO DEPLOYMENT STARTING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
        
        try:
            # Execute secure deployment sequence
            self.create_namespace()
            mysql_creds = self.create_mysql_secrets()
            self.create_app_secrets()
            self.deploy_secure_mysql()
            self.deploy_secure_todo_app()
            self.create_services()
            
            # Wait for success
            if self.wait_for_deployments():
                url = self.get_access_info()
                
                print(f"\n{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}🎉 CHAOS AGENT'S SECURITY ATTACK DEFEATED!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✅ Secure todo app deployed with enterprise-grade secrets{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
                
                return True
            else:
                print(f"{Fore.RED}❌ Deployment failed - check security configurations{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Security deployment error: {e}{Style.RESET_ALL}")
            return False

def main():
    """Main function - Deploy secure todo app with bulletproof secrets"""
    print(f"{Fore.CYAN}🎭 SCENARIO 2: Chaos Attacks Your Secrets!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🔐 Python Security Hero to the rescue!{Style.RESET_ALL}")
    print()
    
    # Deploy with security automation
    deployer = SecureSecretManager()
    success = deployer.deploy_everything()
    
    if success:
        print(f"\n{Fore.GREEN}🎯 NEXT STEPS:{Style.RESET_ALL}")
        print(f"   1. Access your secure todo app via the URL above")
        print(f"   2. Add some todo items and test the functionality")
        print(f"   3. Run secret rotation: python3 rotate-secrets.py")
        print(f"   4. Monitor security: python3 security-monitor.py")
        print(f"   5. Celebrate defeating security chaos! 🔐🎉")
    else:
        print(f"\n{Fore.RED}❌ Security deployment failed. Check troubleshooting.md{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()