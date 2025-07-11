#!/usr/bin/env python3
"""
🦸‍♂️ PYTHON HERO SOLUTION - UPDATED
Automated Vote App Deployment - Chaos-Proof & Port-Conflict-Free!

Updated to use port 31000 to avoid conflicts with Jenkins (8080) and MkDocs (8000)
"""

import os
import sys
import time
import yaml
import socket
import subprocess
from pathlib import Path
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style

# Initialize colorful output
init(autoreset=True)

class ChaosDefeatVoteAppDeployer:
    """Python Hero's Chaos-Defeating Vote App Deployer 🚀"""
    
    def __init__(self):
        """Initialize the chaos-defeating deployment system"""
        print(f"{Fore.CYAN}🚀 Initializing Python K8s Hero System...{Style.RESET_ALL}")
        
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
        
        # Configuration - Updated ports to avoid conflicts
        self.namespace = "vote-app"
        self.app_name = "vote-app"
        self.image = "quay.io/sjbylo/flask-vote-app:latest"
        self.node_port = 31000  # Changed from 30001 to avoid conflicts
        self.port_forward_port = 31500  # Unique port for port forwarding
        
        print(f"{Fore.GREEN}✅ Hero system ready to defeat Chaos Agent!{Style.RESET_ALL}")
    
    def detect_kubernetes_environment(self):
        """Detect what kind of Kubernetes environment we're running on"""
        try:
            context = subprocess.check_output(
                ["kubectl", "config", "current-context"], 
                text=True, 
                stderr=subprocess.DEVNULL
            ).strip()
            
            if "docker-desktop" in context.lower():
                return "docker-desktop"
            elif "minikube" in context.lower():
                return "minikube"
            elif any(cloud in context.lower() for cloud in ["eks", "gke", "aks"]):
                return "cloud"
            else:
                return "unknown"
        except:
            return "unknown"
    
    def check_port_availability(self, port):
        """Check if a port is available on localhost"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                return result != 0  # True if port is available
        except:
            return True
    
    def find_available_port(self, start_port=31500, max_tries=10):
        """Find an available port for port forwarding"""
        for i in range(max_tries):
            port = start_port + i
            if self.check_port_availability(port):
                return port
        return start_port  # Fallback
    
    def create_namespace(self):
        """Create namespace - Hero handles this automatically!"""
        print(f"{Fore.YELLOW}📁 Creating namespace: {self.namespace}{Style.RESET_ALL}")
        
        namespace = client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=self.namespace,
                labels={
                    "created-by": "python-hero",
                    "purpose": "chaos-demo",
                    "workshop": "k8s-chaos-workshop"
                }
            )
        )
        
        try:
            self.v1.create_namespace(namespace)
            print(f"{Fore.GREEN}✅ Namespace created successfully{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                print(f"{Fore.BLUE}📝 Namespace already exists - Hero adapts!{Style.RESET_ALL}")
            else:
                raise e
    
    def create_configmap(self):
        """Create ConfigMap - Hero never forgets configuration!"""
        print(f"{Fore.YELLOW}⚙️  Creating ConfigMap with poll configuration{Style.RESET_ALL}")
        
        config_data = {
            "poll_question": "What's your favorite programming language?",
            "poll_options": "Python,JavaScript,Go,Rust,Java",
            "db_type": "sqlite",
            "app_title": "Chaos-Proof Vote App"
        }
        
        configmap = client.V1ConfigMap(
            metadata=client.V1ObjectMeta(
                name="vote-config",
                namespace=self.namespace,
                labels={"app": self.app_name}
            ),
            data=config_data
        )
        
        try:
            self.v1.create_namespaced_config_map(
                namespace=self.namespace,
                body=configmap
            )
            print(f"{Fore.GREEN}✅ ConfigMap created with poll settings{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                # Update existing configmap
                self.v1.patch_namespaced_config_map(
                    name="vote-config",
                    namespace=self.namespace,
                    body=configmap
                )
                print(f"{Fore.BLUE}📝 ConfigMap updated - Hero adapts!{Style.RESET_ALL}")
            else:
                raise e
    
    def create_deployment(self):
        """Create Deployment - Hero makes it bulletproof!"""
        print(f"{Fore.YELLOW}🚀 Creating bulletproof deployment{Style.RESET_ALL}")
        
        # Define deployment with hero-level reliability
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(
                name=self.app_name,
                namespace=self.namespace,
                labels={"app": self.app_name}
            ),
            spec=client.V1DeploymentSpec(
                replicas=2,  # Hero deploys with redundancy!
                selector=client.V1LabelSelector(
                    match_labels={"app": self.app_name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": self.app_name}
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=self.app_name,
                                image=self.image,
                                ports=[
                                    client.V1ContainerPort(container_port=8080)
                                ],
                                env=[
                                    client.V1EnvVar(
                                        name="DB_TYPE",
                                        value_from=client.V1EnvVarSource(
                                            config_map_key_ref=client.V1ConfigMapKeySelector(
                                                name="vote-config",
                                                key="db_type"
                                            )
                                        )
                                    )
                                ],
                                # Hero adds health checks!
                                liveness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/",
                                        port=8080
                                    ),
                                    initial_delay_seconds=30,
                                    period_seconds=10,
                                    failure_threshold=3
                                ),
                                readiness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/",
                                        port=8080
                                    ),
                                    initial_delay_seconds=10,
                                    period_seconds=5
                                ),
                                # Hero sets resource limits!
                                resources=client.V1ResourceRequirements(
                                    requests={
                                        "memory": "128Mi",
                                        "cpu": "100m"
                                    },
                                    limits={
                                        "memory": "256Mi", 
                                        "cpu": "200m"
                                    }
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
                body=deployment
            )
            print(f"{Fore.GREEN}✅ Deployment created with health checks and resource limits{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                self.apps_v1.patch_namespaced_deployment(
                    name=self.app_name,
                    namespace=self.namespace,
                    body=deployment
                )
                print(f"{Fore.BLUE}📝 Deployment updated - Hero evolves!{Style.RESET_ALL}")
            else:
                raise e
    
    def create_service(self):
        """Create Service - Hero makes it accessible with conflict-free ports!"""
        print(f"{Fore.YELLOW}🌐 Creating service for external access (port {self.node_port}){Style.RESET_ALL}")
        
        service = client.V1Service(
            metadata=client.V1ObjectMeta(
                name=f"{self.app_name}-service",
                namespace=self.namespace,
                labels={"app": self.app_name}
            ),
            spec=client.V1ServiceSpec(
                selector={"app": self.app_name},
                ports=[
                    client.V1ServicePort(
                        port=80,
                        target_port=8080,
                        node_port=self.node_port,  # Using conflict-free port
                        protocol="TCP"
                    )
                ],
                type="NodePort"
            )
        )
        
        try:
            self.v1.create_namespaced_service(
                namespace=self.namespace,
                body=service
            )
            print(f"{Fore.GREEN}✅ Service created - accessible at port {self.node_port}{Style.RESET_ALL}")
        except ApiException as e:
            if e.status == 409:
                print(f"{Fore.BLUE}📝 Service already exists - Hero is efficient!{Style.RESET_ALL}")
            else:
                raise e
    
    def wait_for_deployment(self):
        """Wait for deployment to be ready - Hero is patient!"""
        print(f"{Fore.YELLOW}⏳ Waiting for deployment to be ready...{Style.RESET_ALL}")
        
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                deployment = self.apps_v1.read_namespaced_deployment(
                    name=self.app_name,
                    namespace=self.namespace
                )
                
                ready_replicas = deployment.status.ready_replicas or 0
                desired_replicas = deployment.spec.replicas
                
                if ready_replicas == desired_replicas:
                    print(f"{Fore.GREEN}🎉 Deployment ready! {ready_replicas}/{desired_replicas} pods running{Style.RESET_ALL}")
                    return True
                
                print(f"{Fore.CYAN}⏳ Progress: {ready_replicas}/{desired_replicas} pods ready (attempt {attempt + 1})...{Style.RESET_ALL}")
                time.sleep(10)
                
            except ApiException as e:
                print(f"{Fore.RED}❌ Error checking deployment: {e}{Style.RESET_ALL}")
                time.sleep(10)
        
        print(f"{Fore.RED}❌ Deployment did not become ready in time{Style.RESET_ALL}")
        return False
    
    def get_access_info(self):
        """Get access information - Hero provides smart environment detection!"""
        print(f"{Fore.CYAN}🌐 Getting access information...{Style.RESET_ALL}")
        
        try:
            # Get service info
            service = self.v1.read_namespaced_service(
                name=f"{self.app_name}-service",
                namespace=self.namespace
            )
            
            node_port = service.spec.ports[0].node_port
            
            # Detect environment
            env_type = self.detect_kubernetes_environment()
            
            # Find available port for port forwarding
            pf_port = self.find_available_port(self.port_forward_port)
            
            print(f"{Fore.GREEN}🎯 ACCESS YOUR VOTE APP:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Environment detected: {env_type.upper()}{Style.RESET_ALL}")
            print()
            
            if env_type == "docker-desktop":
                print(f"{Fore.YELLOW}🐳 DOCKER DESKTOP ACCESS:{Style.RESET_ALL}")
                print(f"   💻 Try: http://localhost:{node_port}")
                print(f"   🔄 If that fails, use port forwarding below")
                
            elif env_type == "minikube":
                print(f"{Fore.YELLOW}🎯 MINIKUBE ACCESS:{Style.RESET_ALL}")
                try:
                    minikube_ip = subprocess.check_output(
                        ["minikube", "ip"], 
                        text=True, 
                        stderr=subprocess.DEVNULL
                    ).strip()
                    print(f"   🌐 Minikube: http://{minikube_ip}:{node_port}")
                except:
                    print(f"   🌐 Minikube: http://$(minikube ip):{node_port}")
                    print(f"   💡 Get IP: minikube ip")
                print(f"   🚀 Auto-open: minikube service {self.app_name}-service -n {self.namespace}")
                
            elif env_type == "cloud":
                print(f"{Fore.YELLOW}☁️  CLOUD CLUSTER ACCESS:{Style.RESET_ALL}")
                print(f"   🌍 Get node IP: kubectl get nodes -o wide")
                print(f"   🔗 Access: http://<any-external-ip>:{node_port}")
                
            else:
                print(f"{Fore.YELLOW}❓ UNKNOWN ENVIRONMENT:{Style.RESET_ALL}")
                print(f"   🌐 Try: http://localhost:{node_port}")
                print(f"   💡 Or get node IPs: kubectl get nodes -o wide")
            
            print()
            print(f"{Fore.GREEN}🌐 UNIVERSAL ACCESS (Always Works):{Style.RESET_ALL}")
            print(f"   🔧 Port Forward: kubectl port-forward svc/{self.app_name}-service -n {self.namespace} {pf_port}:80")
            print(f"   🌍 Then access: http://localhost:{pf_port}")
            print(f"   📝 Keep the port-forward terminal open while using the app")
            
            print()
            print(f"{Fore.YELLOW}🗳️  INTERACTION INSTRUCTIONS:{Style.RESET_ALL}")
            print(f"   1. Open any of the URLs above in your browser")
            print(f"   2. Vote for your favorite programming language")
            print(f"   3. See real-time results in the chart")
            print(f"   4. Refresh to see vote counts update")
            print(f"   5. Try voting from different browsers/devices!")
            
            # Return the most likely working URL
            if env_type == "minikube":
                try:
                    minikube_ip = subprocess.check_output(
                        ["minikube", "ip"], text=True, stderr=subprocess.DEVNULL
                    ).strip()
                    return f"http://{minikube_ip}:{node_port}"
                except:
                    return f"http://localhost:{pf_port} (use port-forward)"
            else:
                return f"http://localhost:{node_port}"
            
        except ApiException as e:
            print(f"{Fore.RED}❌ Error getting service info: {e}{Style.RESET_ALL}")
            return None
    
    def start_port_forward_helper(self):
        """Provide helpful port forwarding command"""
        pf_port = self.find_available_port(self.port_forward_port)
        
        print(f"\n{Fore.CYAN}🔧 QUICK PORT FORWARD SETUP:{Style.RESET_ALL}")
        print(f"   Run this in a new terminal:")
        print(f"   {Fore.WHITE}kubectl port-forward svc/{self.app_name}-service -n {self.namespace} {pf_port}:80{Style.RESET_ALL}")
        print(f"   Then access: {Fore.GREEN}http://localhost:{pf_port}{Style.RESET_ALL}")
        
        # Ask if user wants to auto-start port forwarding
        try:
            choice = input(f"\n{Fore.YELLOW}🚀 Start port forwarding automatically? (y/n): {Style.RESET_ALL}").strip().lower()
            if choice in ['y', 'yes']:
                print(f"{Fore.CYAN}🔧 Starting port forwarding...{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📝 This will run in the background. Press Ctrl+C to stop it later.{Style.RESET_ALL}")
                
                # Start port forwarding in background
                cmd = [
                    "kubectl", "port-forward", 
                    f"svc/{self.app_name}-service", 
                    f"{pf_port}:80", 
                    "-n", self.namespace
                ]
                
                import subprocess
                import signal
                import atexit
                
                # Start the process
                pf_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Register cleanup
                def cleanup():
                    try:
                        pf_process.terminate()
                    except:
                        pass
                
                atexit.register(cleanup)
                
                # Give it a moment to start
                time.sleep(2)
                
                print(f"{Fore.GREEN}✅ Port forwarding started! Access at: http://localhost:{pf_port}{Style.RESET_ALL}")
                return f"http://localhost:{pf_port}"
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏭️  Skipping port forwarding setup{Style.RESET_ALL}")
        except:
            pass
        
        return None
    
    def deploy_everything(self):
        """Deploy everything - The Hero's Master Plan!"""
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🦸‍♂️ PYTHON HERO DEPLOYMENT STARTING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        try:
            # Execute hero deployment sequence
            self.create_namespace()
            self.create_configmap()
            self.create_deployment()
            self.create_service()
            
            # Wait for success
            if self.wait_for_deployment():
                url = self.get_access_info()
                
                # Offer port forwarding if needed
                if "localhost:31000" in str(url) and not self.check_port_availability(31000):
                    self.start_port_forward_helper()
                
                print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}🎉 CHAOS AGENT DEFEATED!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✅ Vote app deployed successfully with Python automation{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
                
                return True
            else:
                print(f"{Fore.RED}❌ Deployment failed - even heroes need debugging sometimes!{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
            return False

def main():
    """Main function - Let the hero save the day!"""
    print(f"{Fore.CYAN}🎭 SCENARIO 1: Chaos Strikes Manual Deployments{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🦸‍♂️ Python Hero to the rescue!{Style.RESET_ALL}")
    print()
    
    # Deploy with hero automation
    deployer = ChaosDefeatVoteAppDeployer()
    success = deployer.deploy_everything()
    
    if success:
        print(f"\n{Fore.GREEN}🎯 NEXT STEPS:{Style.RESET_ALL}")
        print(f"   1. Open the vote app URL in your browser")
        print(f"   2. Cast your vote and see real-time results")
        print(f"   3. Run the monitoring script: python3 monitor-deployment.py")
        print(f"   4. Celebrate defeating Chaos Agent! 🎉")
    else:
        print(f"\n{Fore.RED}❌ Deployment failed. Check troubleshooting.md{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()