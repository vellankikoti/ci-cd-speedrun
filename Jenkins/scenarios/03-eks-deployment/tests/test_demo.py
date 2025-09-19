#!/usr/bin/env python3
"""
Test suite for EKS Demo Script
"""

import pytest
import subprocess
import unittest.mock as mock
from demo import EKSDemo

class TestEKSDemo:
    """Test cases for EKSDemo class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.demo = EKSDemo(cluster_name='test-cluster', stack_name='test-stack', region='us-west-2')
    
    def test_init(self):
        """Test EKSDemo initialization."""
        demo = EKSDemo()
        assert demo.cluster_name.startswith('workshop-demo-')
        assert demo.stack_name.startswith('workshop-demo-stack-')
        assert demo.region == 'us-east-1'  # default region
    
    def test_init_with_custom_params(self):
        """Test EKSDemo initialization with custom parameters."""
        demo = EKSDemo(cluster_name='my-cluster', stack_name='my-stack', region='us-east-1')
        assert demo.cluster_name == 'my-cluster'
        assert demo.stack_name == 'my-stack'
        assert demo.region == 'us-east-1'
    
    @mock.patch('demo.subprocess.run')
    def test_check_prerequisites_success(self, mock_subprocess):
        """Test successful prerequisites check."""
        # Mock successful tool checks
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.check_prerequisites()
        
        assert result is True
        assert mock_subprocess.call_count == 4  # aws, kubectl, eksctl, helm
    
    @mock.patch('demo.subprocess.run')
    def test_check_prerequisites_failure(self, mock_subprocess):
        """Test prerequisites check with missing tools."""
        # Mock failed tool check
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'aws')
        
        result = self.demo.check_prerequisites()
        
        assert result is False
    
    @mock.patch('demo.subprocess.run')
    def test_check_aws_credentials_success(self, mock_subprocess):
        """Test successful AWS credentials check."""
        # Mock successful AWS credentials check
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = '{"Account": "123456789012", "UserId": "test-user"}'
        
        result = self.demo.check_aws_credentials()
        
        assert result is True
        assert self.demo.account_id == '123456789012'
    
    @mock.patch('demo.subprocess.run')
    def test_check_aws_credentials_failure(self, mock_subprocess):
        """Test AWS credentials check failure."""
        # Mock failed AWS credentials check
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'aws')
        
        result = self.demo.check_aws_credentials()
        
        assert result is False
    
    @mock.patch('demo.subprocess.run')
    def test_run_tests_success(self, mock_subprocess):
        """Test successful test execution."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.run_tests()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('demo.subprocess.run')
    def test_run_tests_failure(self, mock_subprocess):
        """Test test execution failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'pytest')
        
        result = self.demo.run_tests()
        
        assert result is False
    
    @mock.patch('demo.subprocess.run')
    def test_deploy_cluster_success(self, mock_subprocess):
        """Test successful cluster deployment."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.deploy_cluster()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('demo.subprocess.run')
    def test_configure_kubectl_success(self, mock_subprocess):
        """Test successful kubectl configuration."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.configure_kubectl()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('demo.subprocess.run')
    def test_post_deploy_setup_success(self, mock_subprocess):
        """Test successful post-deployment setup."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.post_deploy_setup()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('demo.subprocess.run')
    def test_generate_connection_info_success(self, mock_subprocess):
        """Test successful connection info generation."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.generate_connection_info()
        
        assert result is True
        mock_subprocess.assert_called_once()
    
    @mock.patch('demo.subprocess.run')
    def test_show_cluster_status_success(self, mock_subprocess):
        """Test successful cluster status display."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.show_cluster_status()
        
        assert result is True
        assert mock_subprocess.call_count == 2  # get nodes and get pods
    
    @mock.patch('demo.subprocess.run')
    def test_deploy_sample_app_success(self, mock_subprocess):
        """Test successful sample application deployment."""
        mock_subprocess.return_value.returncode = 0
        
        result = self.demo.deploy_sample_app()
        
        assert result is True
        assert mock_subprocess.call_count == 4  # create deployment, expose service, get services, wait
    
    def test_show_final_status(self, capsys):
        """Test final status display."""
        self.demo.account_id = '123456789012'
        self.demo.show_final_status()
        
        captured = capsys.readouterr()
        assert 'Demo completed successfully!' in captured.out
        assert 'Cluster Name: test-cluster' in captured.out
        assert 'Stack Name: test-stack' in captured.out
        assert 'Region: us-west-2' in captured.out
        assert 'Account ID: 123456789012' in captured.out

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
