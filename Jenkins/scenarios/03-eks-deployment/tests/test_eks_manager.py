#!/usr/bin/env python3
"""
Test suite for EKS Manager
"""

import pytest
import unittest.mock as mock
from eks_manager import EKSManager

class TestEKSManager:
    """Test cases for EKSManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.eks_manager = EKSManager(region='us-west-2')
    
    @mock.patch('eks_manager.boto3.client')
    def test_init(self, mock_boto_client):
        """Test EKSManager initialization."""
        manager = EKSManager(region='us-east-1')
        assert manager.region == 'us-east-1'
        assert mock_boto_client.call_count == 5  # 5 AWS clients
    
    @mock.patch('eks_manager.EKSManager._get_stack_outputs')
    @mock.patch('eks_manager.subprocess.run')
    def test_configure_kubectl_success(self, mock_subprocess, mock_get_outputs):
        """Test successful kubectl configuration."""
        # Mock successful kubectl commands
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "node1\nnode2\nnode3"
        
        result = self.eks_manager.configure_kubectl('test-cluster')
        
        assert result is True
        assert mock_subprocess.call_count == 2  # update-kubeconfig and get nodes
    
    @mock.patch('eks_manager.subprocess.run')
    def test_configure_kubectl_failure(self, mock_subprocess):
        """Test kubectl configuration failure."""
        # Mock failed kubectl command
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'aws')
        
        result = self.eks_manager.configure_kubectl('test-cluster')
        
        assert result is False
    
    @mock.patch('eks_manager.EKSManager._get_stack_outputs')
    @mock.patch('eks_manager.subprocess.run')
    def test_post_deploy_setup_success(self, mock_subprocess, mock_get_outputs):
        """Test successful post-deployment setup."""
        # Mock stack outputs
        mock_get_outputs.return_value = {
            'VpcId': 'vpc-12345',
            'OidcIssuer': 'https://oidc.eks.us-west-2.amazonaws.com/id/12345',
            'ALBControllerRoleArn': 'arn:aws:iam::123456789012:role/test-alb-role'
        }
        
        # Mock successful subprocess calls
        mock_subprocess.return_value.returncode = 0
        
        result = self.eks_manager.post_deploy_setup('test-cluster', 'test-stack')
        
        assert result is True
    
    @mock.patch('eks_manager.EKSManager._get_stack_outputs')
    def test_post_deploy_setup_no_outputs(self, mock_get_outputs):
        """Test post-deployment setup with no stack outputs."""
        mock_get_outputs.return_value = {}
        
        result = self.eks_manager.post_deploy_setup('test-cluster', 'test-stack')
        
        assert result is False
    
    @mock.patch('eks_manager.EKSManager.eks_client')
    @mock.patch('eks_manager.EKSManager.get_account_id')
    def test_generate_connection_info_success(self, mock_get_account, mock_eks_client):
        """Test successful connection info generation."""
        # Mock cluster info
        mock_eks_client.describe_cluster.return_value = {
            'cluster': {
                'name': 'test-cluster',
                'endpoint': 'https://test-cluster.eks.us-west-2.amazonaws.com',
                'version': '1.30',
                'status': 'ACTIVE'
            }
        }
        mock_get_account.return_value = '123456789012'
        
        result = self.eks_manager.generate_connection_info('test-cluster', 'test-info.txt')
        
        assert result is True
    
    @mock.patch('eks_manager.EKSManager.eks_client')
    def test_generate_connection_info_failure(self, mock_eks_client):
        """Test connection info generation failure."""
        mock_eks_client.describe_cluster.side_effect = Exception("Cluster not found")
        
        result = self.eks_manager.generate_connection_info('test-cluster', 'test-info.txt')
        
        assert result is False
    
    @mock.patch('eks_manager.EKSManager.cf_client')
    def test_get_stack_outputs_success(self, mock_cf_client):
        """Test successful stack outputs retrieval."""
        mock_cf_client.describe_stacks.return_value = {
            'Stacks': [{
                'Outputs': [
                    {'OutputKey': 'ClusterName', 'OutputValue': 'test-cluster'},
                    {'OutputKey': 'VpcId', 'OutputValue': 'vpc-12345'}
                ]
            }]
        }
        
        outputs = self.eks_manager._get_stack_outputs('test-stack')
        
        assert outputs['ClusterName'] == 'test-cluster'
        assert outputs['VpcId'] == 'vpc-12345'
    
    @mock.patch('eks_manager.EKSManager.cf_client')
    def test_get_stack_outputs_failure(self, mock_cf_client):
        """Test stack outputs retrieval failure."""
        mock_cf_client.describe_stacks.side_effect = Exception("Stack not found")
        
        outputs = self.eks_manager._get_stack_outputs('test-stack')
        
        assert outputs == {}
    
    @mock.patch('eks_manager.EKSManager.iam_client')
    @mock.patch('eks_manager.EKSManager.eks_client')
    @mock.patch('eks_manager.subprocess.run')
    def test_install_ebs_csi_driver_success(self, mock_subprocess, mock_eks_client, mock_iam_client):
        """Test successful EBS CSI Driver installation."""
        # Mock cluster info
        mock_eks_client.describe_cluster.return_value = {
            'cluster': {
                'identity': {
                    'oidc': {
                        'issuer': 'https://oidc.eks.us-west-2.amazonaws.com/id/12345'
                    }
                }
            }
        }
        
        # Mock role doesn't exist
        mock_iam_client.get_role.side_effect = mock_iam_client.exceptions.NoSuchEntityException(
            {'Error': {'Code': 'NoSuchEntity'}}, 'get_role'
        )
        
        # Mock successful role creation
        mock_iam_client.create_role.return_value = {}
        mock_iam_client.attach_role_policy.return_value = {}
        
        # Mock successful addon update
        mock_eks_client.update_addon.return_value = {}
        
        result = self.eks_manager._install_ebs_csi_driver('test-cluster')
        
        assert result is True
    
    @mock.patch('eks_manager.subprocess.run')
    def test_install_metrics_server_success(self, mock_subprocess):
        """Test successful Metrics Server installation."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.eks_manager._install_metrics_server()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('eks_manager.subprocess.run')
    def test_install_metrics_server_failure(self, mock_subprocess):
        """Test Metrics Server installation failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'kubectl')
        
        result = self.eks_manager._install_metrics_server()
        
        assert result is False
    
    @mock.patch('eks_manager.subprocess.run')
    def test_create_default_storage_class_success(self, mock_subprocess):
        """Test successful storage class creation."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.eks_manager._create_default_storage_class()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('eks_manager.subprocess.run')
    def test_create_cluster_admin_binding_success(self, mock_subprocess):
        """Test successful cluster admin binding creation."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.eks_manager._create_cluster_admin_binding()
        
        assert result is True
        mock_subprocess.assert_called_once()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
