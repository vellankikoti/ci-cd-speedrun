#!/usr/bin/env python3
"""
EKS Workshop Demo Script
This script demonstrates the EKS cluster deployment functionality
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

class EKSDemo:
    def __init__(self, cluster_name: str = None, stack_name: str = None, region: str = None):
        """Initialize EKS Demo with parameters."""
        self.cluster_name = cluster_name or f"workshop-demo-{int(time.time())}"
        self.stack_name = stack_name or f"workshop-demo-stack-{int(time.time())}"
        self.region = region or self._get_aws_region()
        self.account_id = None
        
    def _get_aws_region(self) -> str:
        """Get AWS region from configuration."""
        try:
            result = subprocess.run(['aws', 'configure', 'get', 'region'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip() or 'us-west-2'
        except subprocess.CalledProcessError:
            return 'us-west-2'
    
    def check_prerequisites(self) -> bool:
        """Check if all required tools are installed."""
        print("🔍 Checking prerequisites...")
        
        required_tools = {
            'aws': 'AWS CLI',
            'kubectl': 'kubectl',
            'eksctl': 'eksctl',
            'helm': 'Helm'
        }
        
        missing_tools = []
        for tool, name in required_tools.items():
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                print(f"✅ {name} found")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"❌ {name} not found")
                missing_tools.append(name)
        
        if missing_tools:
            print(f"\n❌ Missing tools: {', '.join(missing_tools)}")
            print("Please install the missing tools before running the demo.")
            return False
        
        return True
    
    def check_aws_credentials(self) -> bool:
        """Check AWS credentials and get account information."""
        print("\n🔍 Checking AWS credentials...")
        
        try:
            import json
            result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                                  capture_output=True, text=True, check=True)
            
            # Parse account ID from output
            identity = json.loads(result.stdout)
            self.account_id = identity['Account']
            
            print(f"✅ AWS credentials configured (Account: {self.account_id}, Region: {self.region})")
            return True
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"❌ AWS credentials not configured: {e}")
            print("Please run 'aws configure' to set up your credentials.")
            return False
    
    def run_tests(self) -> bool:
        """Run the test suite."""
        print("\n🧪 Running tests...")
        
        try:
            result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v', '--tb=short'], 
                                  check=True)
            print("✅ Tests passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False
    
    def deploy_cluster(self) -> bool:
        """Deploy the EKS cluster."""
        print(f"\n🚀 Deploying EKS cluster...")
        print(f"   Cluster Name: {self.cluster_name}")
        print(f"   Stack Name: {self.stack_name}")
        print(f"   Region: {self.region}")
        
        try:
            cmd = [
                'python', 'eks_manager.py', 'deploy',
                '--cluster-name', self.cluster_name,
                '--stack-name', self.stack_name,
                '--region', self.region,
                '--node-instance-type', 't3.small',
                '--node-count', '3',
                '--enable-logging',
                '--enable-alb-controller'
            ]
            
            result = subprocess.run(cmd, check=True)
            print("✅ EKS cluster deployed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ EKS cluster deployment failed: {e}")
            return False
    
    def configure_kubectl(self) -> bool:
        """Configure kubectl for the cluster."""
        print("\n🔧 Configuring kubectl...")
        
        try:
            cmd = [
                'python', 'eks_manager.py', 'configure-kubectl',
                '--cluster-name', self.cluster_name,
                '--region', self.region
            ]
            
            result = subprocess.run(cmd, check=True)
            print("✅ kubectl configured successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ kubectl configuration failed: {e}")
            return False
    
    def post_deploy_setup(self) -> bool:
        """Run post-deployment setup."""
        print("\n🔧 Running post-deployment setup...")
        
        try:
            cmd = [
                'python', 'eks_manager.py', 'post-deploy',
                '--cluster-name', self.cluster_name,
                '--stack-name', self.stack_name,
                '--region', self.region
            ]
            
            result = subprocess.run(cmd, check=True)
            print("✅ Post-deployment setup completed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Post-deployment setup failed: {e}")
            return False
    
    def generate_connection_info(self) -> bool:
        """Generate connection information."""
        print("\n📋 Generating connection information...")
        
        try:
            output_file = f"connection-info-{self.cluster_name}.txt"
            cmd = [
                'python', 'eks_manager.py', 'generate-connection-info',
                '--cluster-name', self.cluster_name,
                '--region', self.region,
                '--output-file', output_file
            ]
            
            result = subprocess.run(cmd, check=True)
            print(f"✅ Connection information generated: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Connection information generation failed: {e}")
            return False
    
    def show_cluster_status(self) -> bool:
        """Show cluster status."""
        print("\n📊 Cluster Status:")
        print("==================")
        
        try:
            # Show nodes
            print("Nodes:")
            subprocess.run(['kubectl', 'get', 'nodes', '-o', 'wide'], check=True)
            print()
            
            # Show pods
            print("Pods:")
            subprocess.run(['kubectl', 'get', 'pods', '--all-namespaces'], check=True)
            print()
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to show cluster status: {e}")
            return False
    
    def deploy_sample_app(self) -> bool:
        """Deploy a sample application."""
        print("\n🚀 Deploying sample application...")
        
        try:
            # Create deployment
            subprocess.run(['kubectl', 'create', 'deployment', 'nginx', '--image=nginx'], check=True)
            
            # Expose service
            subprocess.run(['kubectl', 'expose', 'deployment', 'nginx', '--port=80', '--type=LoadBalancer'], check=True)
            
            # Show services
            subprocess.run(['kubectl', 'get', 'services'], check=True)
            print()
            
            # Wait for deployment to be ready
            print("⏳ Waiting for service to be ready...")
            subprocess.run(['kubectl', 'wait', '--for=condition=available', '--timeout=300s', 'deployment/nginx'], check=True)
            print()
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to deploy sample application: {e}")
            return False
    
    def show_final_status(self) -> None:
        """Show final status and cleanup instructions."""
        print("🎉 Demo completed successfully!")
        print("===============================")
        print()
        print("📋 Cluster Details:")
        print(f"   Cluster Name: {self.cluster_name}")
        print(f"   Stack Name: {self.stack_name}")
        print(f"   Region: {self.region}")
        print(f"   Account ID: {self.account_id}")
        print()
        print("🔗 Connection Commands:")
        print(f"   aws eks update-kubeconfig --region {self.region} --name {self.cluster_name}")
        print("   kubectl get nodes")
        print("   kubectl get pods --all-namespaces")
        print()
        print(f"📄 Check connection-info-{self.cluster_name}.txt for detailed instructions")
        print()
        print("🧹 To clean up resources:")
        print(f"   aws cloudformation delete-stack --stack-name {self.stack_name} --region {self.region}")
        print("   kubectl delete deployment nginx")
        print("   kubectl delete service nginx")
        print()
        print("💰 Estimated monthly cost: ~$50-80 (3x t3.small nodes + EKS control plane)")
        print()
    
    def run_demo(self) -> bool:
        """Run the complete demo."""
        print("🎓 EKS Workshop Demo Script")
        print("==========================")
        print()
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Check AWS credentials
        if not self.check_aws_credentials():
            return False
        
        # Run tests
        if not self.run_tests():
            return False
        
        # Deploy cluster
        if not self.deploy_cluster():
            return False
        
        # Configure kubectl
        if not self.configure_kubectl():
            return False
        
        # Post-deployment setup
        if not self.post_deploy_setup():
            return False
        
        # Generate connection info
        if not self.generate_connection_info():
            return False
        
        # Show cluster status
        if not self.show_cluster_status():
            return False
        
        # Deploy sample application
        if not self.deploy_sample_app():
            return False
        
        # Show final status
        self.show_final_status()
        
        return True

def main():
    parser = argparse.ArgumentParser(description='EKS Workshop Demo Script')
    parser.add_argument('--cluster-name', help='EKS cluster name (default: auto-generated)')
    parser.add_argument('--stack-name', help='CloudFormation stack name (default: auto-generated)')
    parser.add_argument('--region', help='AWS region (default: from AWS config or us-west-2)')
    parser.add_argument('--skip-tests', action='store_true', help='Skip running tests')
    parser.add_argument('--skip-sample-app', action='store_true', help='Skip deploying sample application')
    
    args = parser.parse_args()
    
    # Create demo instance
    demo = EKSDemo(
        cluster_name=args.cluster_name,
        stack_name=args.stack_name,
        region=args.region
    )
    
    # Override methods if skipping certain steps
    if args.skip_tests:
        demo.run_tests = lambda: True
    if args.skip_sample_app:
        demo.deploy_sample_app = lambda: True
    
    # Run demo
    success = demo.run_demo()
    
    if success:
        print("✅ Demo completed successfully!")
        sys.exit(0)
    else:
        print("❌ Demo failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
