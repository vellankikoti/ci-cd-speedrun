#!/usr/bin/env python3
"""
EKS Cluster Manager for Jenkins Workshop
Handles EKS cluster deployment, configuration, and management with cost optimization.
"""

import argparse
import boto3
import json
import subprocess
import sys
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class EKSManager:
    def __init__(self, region: str = 'us-west-2'):
        """Initialize EKS Manager with AWS clients."""
        self.region = region
        self.cf_client = boto3.client('cloudformation', region_name=region)
        self.eks_client = boto3.client('eks', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        
    def get_account_id(self) -> str:
        """Get AWS account ID."""
        return self.sts_client.get_caller_identity()['Account']
    
    def deploy_cluster(self, cluster_name: str, stack_name: str, node_instance_type: str = 't3.small', 
                      node_count: int = 3, enable_logging: bool = True, enable_alb_controller: bool = True) -> bool:
        """Deploy EKS cluster using CloudFormation."""
        print(f"🚀 Starting EKS cluster deployment...")
        print(f"   Cluster Name: {cluster_name}")
        print(f"   Stack Name: {stack_name}")
        print(f"   Region: {self.region}")
        print(f"   Node Instance Type: {node_instance_type}")
        print(f"   Node Count: {node_count}")
        
        # Read CloudFormation template
        template_path = Path(__file__).parent / 'eks-cluster-cost-optimized.yaml'
        with open(template_path, 'r') as f:
            template_body = f.read()
        
        # Prepare parameters
        parameters = [
            {'ParameterKey': 'ClusterName', 'ParameterValue': cluster_name},
            {'ParameterKey': 'NodeInstanceType', 'ParameterValue': node_instance_type},
            {'ParameterKey': 'NodeDesiredCapacity', 'ParameterValue': str(node_count)},
            {'ParameterKey': 'NodeMinSize', 'ParameterValue': '1'},
            {'ParameterKey': 'NodeMaxSize', 'ParameterValue': str(max(5, node_count + 2))},
            {'ParameterKey': 'EnableLogging', 'ParameterValue': str(enable_logging).lower()},
            {'ParameterKey': 'EnableALBController', 'ParameterValue': str(enable_alb_controller).lower()},
        ]
        
        # Deploy stack
        try:
            print("📋 Creating CloudFormation stack...")
            response = self.cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Tags=[
                    {'Key': 'Purpose', 'Value': 'Workshop EKS Cluster'},
                    {'Key': 'CreatedBy', 'Value': 'Jenkins EKS Manager'},
                    {'Key': 'CreatedAt', 'Value': datetime.now().isoformat()}
                ]
            )
            
            print(f"✅ Stack creation initiated: {response['StackId']}")
            
            # Wait for stack creation
            print("⏳ Waiting for stack creation to complete...")
            waiter = self.cf_client.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
            
            print("✅ EKS cluster deployed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to deploy EKS cluster: {str(e)}")
            return False
    
    def configure_kubectl(self, cluster_name: str) -> bool:
        """Configure kubectl for the EKS cluster."""
        print(f"🔧 Configuring kubectl for cluster: {cluster_name}")
        
        try:
            # Update kubeconfig
            cmd = ['aws', 'eks', 'update-kubeconfig', '--region', self.region, '--name', cluster_name]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print("✅ kubectl configured successfully")
            
            # Verify cluster connectivity
            print("🔍 Verifying cluster connectivity...")
            verify_cmd = ['kubectl', 'get', 'nodes']
            result = subprocess.run(verify_cmd, capture_output=True, text=True, check=True)
            
            print("✅ Cluster connectivity verified")
            print("📋 Cluster nodes:")
            print(result.stdout)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to configure kubectl: {str(e)}")
            print(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False
    
    def post_deploy_setup(self, cluster_name: str, stack_name: str) -> bool:
        """Run post-deployment setup including add-ons installation."""
        print(f"🔧 Running post-deployment setup for cluster: {cluster_name}")
        
        try:
            # Get stack outputs
            stack_outputs = self._get_stack_outputs(stack_name)
            if not stack_outputs:
                print("❌ Failed to get stack outputs")
                return False
            
            vpc_id = stack_outputs.get('VpcId')
            oidc_issuer = stack_outputs.get('OidcIssuer')
            alb_controller_role_arn = stack_outputs.get('ALBControllerRoleArn')
            
            # Install EBS CSI Driver add-on
            print("🔧 Installing EBS CSI Driver add-on...")
            self._install_ebs_csi_driver(cluster_name)
            
            # Install AWS Load Balancer Controller if enabled
            if alb_controller_role_arn:
                print("🔧 Installing AWS Load Balancer Controller...")
                self._install_alb_controller(cluster_name, vpc_id, alb_controller_role_arn)
            
            # Install Metrics Server
            print("🔧 Installing Metrics Server...")
            self._install_metrics_server()
            
            # Create default storage class
            print("🔧 Creating default storage class...")
            self._create_default_storage_class()
            
            # Create cluster admin role binding
            print("🔧 Creating cluster admin access...")
            self._create_cluster_admin_binding()
            
            print("✅ Post-deployment setup completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Post-deployment setup failed: {str(e)}")
            return False
    
    def generate_connection_info(self, cluster_name: str, output_file: str = 'connection-info.txt') -> bool:
        """Generate connection information and commands."""
        print(f"📋 Generating connection information for cluster: {cluster_name}")
        
        try:
            # Get cluster information
            cluster_info = self.eks_client.describe_cluster(name=cluster_name)
            cluster = cluster_info['cluster']
            
            # Get account ID
            account_id = self.get_account_id()
            
            # Generate connection info
            connection_info = f"""
🎉 EKS Cluster Connection Information
=====================================

Cluster Details:
- Cluster Name: {cluster_name}
- Region: {self.region}
- Account ID: {account_id}
- Endpoint: {cluster['endpoint']}
- Version: {cluster['version']}
- Status: {cluster['status']}

🔗 Connection Commands:
======================

1. Configure kubectl:
   aws eks update-kubeconfig --region {self.region} --name {cluster_name}

2. Verify connection:
   kubectl get nodes
   kubectl get pods --all-namespaces

3. Check cluster status:
   aws eks describe-cluster --name {cluster_name} --region {self.region}

4. Get cluster endpoint:
   aws eks describe-cluster --name {cluster_name} --region {self.region} --query 'cluster.endpoint'

5. List node groups:
   aws eks list-nodegroups --cluster-name {cluster_name} --region {self.region}

📊 Useful kubectl Commands:
===========================

# View all resources
kubectl get all --all-namespaces

# View nodes with details
kubectl get nodes -o wide

# View system pods
kubectl get pods -n kube-system

# View storage classes
kubectl get storageclass

# View services
kubectl get services --all-namespaces

# View ingress controllers
kubectl get pods -n kube-system | grep -i load

🧪 Test Commands:
=================

# Deploy a test application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services

# Test storage
kubectl create -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 1Gi
EOF

kubectl get pvc test-pvc

# Clean up test resources
kubectl delete deployment nginx
kubectl delete service nginx
kubectl delete pvc test-pvc

💰 Cost Optimization Tips:
==========================

1. Use t3.small instances for development/testing
2. Scale down nodes when not in use
3. Use Spot instances for non-critical workloads
4. Enable cluster autoscaler for dynamic scaling
5. Monitor costs with AWS Cost Explorer

📚 Additional Resources:
========================

- EKS User Guide: https://docs.aws.amazon.com/eks/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- AWS Load Balancer Controller: https://kubernetes-sigs.github.io/aws-load-balancer-controller/

Generated at: {datetime.now().isoformat()}
"""
            
            # Write to file
            with open(output_file, 'w') as f:
                f.write(connection_info)
            
            print(f"✅ Connection information saved to: {output_file}")
            print("\n" + "="*50)
            print(connection_info)
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to generate connection info: {str(e)}")
            return False
    
    def _get_stack_outputs(self, stack_name: str) -> Dict[str, str]:
        """Get CloudFormation stack outputs."""
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack = response['Stacks'][0]
            outputs = {}
            for output in stack.get('Outputs', []):
                outputs[output['OutputKey']] = output['OutputValue']
            return outputs
        except Exception as e:
            print(f"❌ Failed to get stack outputs: {str(e)}")
            return {}
    
    def _install_ebs_csi_driver(self, cluster_name: str) -> bool:
        """Install EBS CSI Driver add-on."""
        try:
            # Create EBS CSI Driver IAM role
            account_id = self.get_account_id()
            oidc_issuer = self.eks_client.describe_cluster(name=cluster_name)['cluster']['identity']['oidc']['issuer']
            oidc_id = oidc_issuer.split('/')[-1]
            
            role_name = f"{cluster_name}-ebs-csi-driver-role"
            
            # Check if role exists
            try:
                self.iam_client.get_role(RoleName=role_name)
                print(f"✅ EBS CSI Driver role already exists: {role_name}")
            except self.iam_client.exceptions.NoSuchEntityException:
                # Create role
                trust_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Federated": f"arn:aws:iam::{account_id}:oidc-provider/{oidc_id}"
                            },
                            "Action": "sts:AssumeRoleWithWebIdentity",
                            "Condition": {
                                "StringEquals": {
                                    f"{oidc_id}:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa",
                                    f"{oidc_id}:aud": "sts.amazonaws.com"
                                }
                            }
                        }
                    ]
                }
                
                self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(trust_policy),
                    Description="IAM role for EBS CSI Driver"
                )
                
                # Attach managed policy
                self.iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
                )
                
                print(f"✅ Created EBS CSI Driver role: {role_name}")
            
            # Update EBS CSI Driver add-on
            role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
            self.eks_client.update_addon(
                clusterName=cluster_name,
                addonName='aws-ebs-csi-driver',
                serviceAccountRoleArn=role_arn,
                resolveConflicts='OVERWRITE'
            )
            
            print("✅ EBS CSI Driver add-on updated")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install EBS CSI Driver: {str(e)}")
            return False
    
    def _install_alb_controller(self, cluster_name: str, vpc_id: str, role_arn: str) -> bool:
        """Install AWS Load Balancer Controller."""
        try:
            # Create service account
            service_account_yaml = f"""
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-load-balancer-controller
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: {role_arn}
"""
            
            # Apply service account
            subprocess.run(['kubectl', 'apply', '-f', '-'], 
                         input=service_account_yaml, text=True, check=True)
            
            # Add Helm repository
            subprocess.run(['helm', 'repo', 'add', 'eks', 'https://aws.github.io/eks-charts'], check=True)
            subprocess.run(['helm', 'repo', 'update'], check=True)
            
            # Install ALB Controller
            install_cmd = [
                'helm', 'upgrade', '--install', 'aws-load-balancer-controller', 'eks/aws-load-balancer-controller',
                '--namespace', 'kube-system',
                '--set', f'clusterName={cluster_name}',
                '--set', 'serviceAccount.create=false',
                '--set', 'serviceAccount.name=aws-load-balancer-controller',
                '--set', f'region={self.region}',
                '--set', f'vpcId={vpc_id}'
            ]
            
            subprocess.run(install_cmd, check=True)
            
            print("✅ AWS Load Balancer Controller installed")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install ALB Controller: {str(e)}")
            return False
    
    def _install_metrics_server(self) -> bool:
        """Install Metrics Server."""
        try:
            subprocess.run([
                'kubectl', 'apply', '-f',
                'https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml'
            ], check=True)
            
            print("✅ Metrics Server installed")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install Metrics Server: {str(e)}")
            return False
    
    def _create_default_storage_class(self) -> bool:
        """Create default storage class."""
        try:
            storage_class_yaml = """
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
"""
            
            subprocess.run(['kubectl', 'apply', '-f', '-'], 
                         input=storage_class_yaml, text=True, check=True)
            
            print("✅ Default storage class created")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create storage class: {str(e)}")
            return False
    
    def _create_cluster_admin_binding(self) -> bool:
        """Create cluster admin role binding."""
        try:
            # Get current user ARN
            caller_identity = self.sts_client.get_caller_identity()
            user_arn = caller_identity['Arn']
            
            # Create cluster role binding
            role_binding_yaml = f"""
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: workshop-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: {user_arn}
"""
            
            subprocess.run(['kubectl', 'apply', '-f', '-'], 
                         input=role_binding_yaml, text=True, check=True)
            
            print("✅ Cluster admin access configured")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create cluster admin binding: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='EKS Cluster Manager for Jenkins Workshop')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy EKS cluster')
    deploy_parser.add_argument('--cluster-name', required=True, help='EKS cluster name')
    deploy_parser.add_argument('--stack-name', required=True, help='CloudFormation stack name')
    deploy_parser.add_argument('--region', default='us-west-2', help='AWS region')
    deploy_parser.add_argument('--node-instance-type', default='t3.small', help='Node instance type')
    deploy_parser.add_argument('--node-count', type=int, default=3, help='Number of nodes')
    deploy_parser.add_argument('--enable-logging', action='store_true', help='Enable EKS logging')
    deploy_parser.add_argument('--enable-alb-controller', action='store_true', help='Enable ALB Controller')
    
    # Configure kubectl command
    config_parser = subparsers.add_parser('configure-kubectl', help='Configure kubectl')
    config_parser.add_argument('--cluster-name', required=True, help='EKS cluster name')
    config_parser.add_argument('--region', default='us-west-2', help='AWS region')
    
    # Post-deploy command
    post_deploy_parser = subparsers.add_parser('post-deploy', help='Run post-deployment setup')
    post_deploy_parser.add_argument('--cluster-name', required=True, help='EKS cluster name')
    post_deploy_parser.add_argument('--stack-name', required=True, help='CloudFormation stack name')
    post_deploy_parser.add_argument('--region', default='us-west-2', help='AWS region')
    
    # Generate connection info command
    info_parser = subparsers.add_parser('generate-connection-info', help='Generate connection info')
    info_parser.add_argument('--cluster-name', required=True, help='EKS cluster name')
    info_parser.add_argument('--region', default='us-west-2', help='AWS region')
    info_parser.add_argument('--output-file', default='connection-info.txt', help='Output file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize EKS Manager
    eks_manager = EKSManager(region=args.region)
    
    # Execute command
    success = False
    
    if args.command == 'deploy':
        success = eks_manager.deploy_cluster(
            cluster_name=args.cluster_name,
            stack_name=args.stack_name,
            node_instance_type=args.node_instance_type,
            node_count=args.node_count,
            enable_logging=args.enable_logging,
            enable_alb_controller=args.enable_alb_controller
        )
    elif args.command == 'configure-kubectl':
        success = eks_manager.configure_kubectl(args.cluster_name)
    elif args.command == 'post-deploy':
        success = eks_manager.post_deploy_setup(args.cluster_name, args.stack_name)
    elif args.command == 'generate-connection-info':
        success = eks_manager.generate_connection_info(args.cluster_name, args.output_file)
    
    if success:
        print("✅ Command completed successfully!")
        sys.exit(0)
    else:
        print("❌ Command failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
