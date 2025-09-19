#!/usr/bin/env python3
"""
Test suite for CloudFormation template validation
"""

import pytest
import yaml
from pathlib import Path

class TestCloudFormationTemplate:
    """Test cases for CloudFormation template."""
    
    def setup_method(self):
        """Set up test fixtures."""
        template_path = Path(__file__).parent.parent / 'eks-cluster-cost-optimized.yaml'
        with open(template_path, 'r') as f:
            self.template = yaml.safe_load(f)
    
    def test_template_structure(self):
        """Test CloudFormation template structure."""
        assert 'AWSTemplateFormatVersion' in self.template
        assert 'Description' in self.template
        assert 'Parameters' in self.template
        assert 'Resources' in self.template
        assert 'Outputs' in self.template
        assert 'Conditions' in self.template
    
    def test_parameters(self):
        """Test required parameters."""
        parameters = self.template['Parameters']
        
        required_params = [
            'ClusterName', 'ClusterVersion', 'NodeInstanceType',
            'NodeDesiredCapacity', 'NodeMinSize', 'NodeMaxSize',
            'VpcCidr', 'EnableLogging', 'EnableALBController'
        ]
        
        for param in required_params:
            assert param in parameters, f"Parameter {param} is missing"
    
    def test_parameter_defaults(self):
        """Test parameter default values."""
        parameters = self.template['Parameters']
        
        assert parameters['ClusterName']['Default'] == 'eks-demo-cluster'
        assert parameters['ClusterVersion']['Default'] == '1.30'
        assert parameters['NodeInstanceType']['Default'] == 't3.small'
        assert parameters['NodeDesiredCapacity']['Default'] == 3
        assert parameters['NodeMinSize']['Default'] == 1
        assert parameters['NodeMaxSize']['Default'] == 5
        assert parameters['VpcCidr']['Default'] == '10.0.0.0/16'
        assert parameters['EnableLogging']['Default'] == 'true'
        assert parameters['EnableALBController']['Default'] == 'true'
    
    def test_required_resources(self):
        """Test required resources are present."""
        resources = self.template['Resources']
        
        required_resources = [
            'VPC', 'InternetGateway', 'VPCGatewayAttachment',
            'PublicSubnet1', 'PublicSubnet2', 'PrivateSubnet1', 'PrivateSubnet2',
            'PublicRouteTable', 'PrivateRouteTable', 'NatGateway',
            'ClusterSecurityGroup', 'NodeSecurityGroup',
            'EKSClusterRole', 'NodeInstanceRole', 'EKSCluster',
            'EKSOidcProvider', 'NodeGroup'
        ]
        
        for resource in required_resources:
            assert resource in resources, f"Resource {resource} is missing"
    
    def test_conditional_resources(self):
        """Test conditional resources."""
        resources = self.template['Resources']
        
        # ALB Controller role should be conditional
        assert 'ALBControllerRole' in resources
        assert 'Condition' in resources['ALBControllerRole']
        assert resources['ALBControllerRole']['Condition'] == 'EnableALBController'
    
    def test_conditions(self):
        """Test conditions are properly defined."""
        conditions = self.template['Conditions']
        
        assert 'EnableLogging' in conditions
        assert 'EnableALBController' in conditions
        
        # Test condition logic
        assert conditions['EnableLogging'] == {'Fn::Equals': [{'Ref': 'EnableLogging'}, 'true']}
        assert conditions['EnableALBController'] == {'Fn::Equals': [{'Ref': 'EnableALBController'}, 'true']}
    
    def test_outputs(self):
        """Test required outputs."""
        outputs = self.template['Outputs']
        
        required_outputs = [
            'ClusterName', 'ClusterArn', 'ClusterEndpoint', 'OidcIssuer',
            'VpcId', 'PublicSubnetIds', 'PrivateSubnetIds', 'NodeSecurityGroupId',
            'NodeGroupName', 'EKSClusterRoleArn', 'NodeInstanceRoleArn',
            'ConnectionCommand', 'CostEstimate'
        ]
        
        for output in required_outputs:
            assert output in outputs, f"Output {output} is missing"
    
    def test_eks_cluster_configuration(self):
        """Test EKS cluster configuration."""
        cluster = self.template['Resources']['EKSCluster']
        
        # Check cluster properties
        properties = cluster['Properties']
        assert 'Name' in properties
        assert 'Version' in properties
        assert 'RoleArn' in properties
        assert 'ResourcesVpcConfig' in properties
        assert 'Logging' in properties
        
        # Check VPC config
        vpc_config = properties['ResourcesVpcConfig']
        assert 'SubnetIds' in vpc_config
        assert 'SecurityGroupIds' in vpc_config
        assert 'EndpointPublicAccess' in vpc_config
        assert 'EndpointPrivateAccess' in vpc_config
        
        # Check logging configuration
        logging = properties['Logging']
        assert 'ClusterLogging' in logging
        assert 'EnabledTypes' in logging['ClusterLogging']
    
    def test_node_group_configuration(self):
        """Test node group configuration."""
        node_group = self.template['Resources']['NodeGroup']
        
        properties = node_group['Properties']
        assert 'ClusterName' in properties
        assert 'NodeRole' in properties
        assert 'Subnets' in properties
        assert 'ScalingConfig' in properties
        assert 'AmiType' in properties
        assert 'InstanceTypes' in properties
        
        # Check scaling config
        scaling_config = properties['ScalingConfig']
        assert 'DesiredSize' in scaling_config
        assert 'MinSize' in scaling_config
        assert 'MaxSize' in scaling_config
    
    def test_security_groups(self):
        """Test security group configurations."""
        cluster_sg = self.template['Resources']['ClusterSecurityGroup']
        node_sg = self.template['Resources']['NodeSecurityGroup']
        
        # Check cluster security group
        cluster_sg_props = cluster_sg['Properties']
        assert 'GroupDescription' in cluster_sg_props
        assert 'VpcId' in cluster_sg_props
        assert 'SecurityGroupIngress' in cluster_sg_props
        
        # Check node security group
        node_sg_props = node_sg['Properties']
        assert 'GroupDescription' in node_sg_props
        assert 'VpcId' in node_sg_props
        assert 'SecurityGroupIngress' in node_sg_props
    
    def test_iam_roles(self):
        """Test IAM role configurations."""
        cluster_role = self.template['Resources']['EKSClusterRole']
        node_role = self.template['Resources']['NodeInstanceRole']
        
        # Check cluster role
        cluster_role_props = cluster_role['Properties']
        assert 'AssumeRolePolicyDocument' in cluster_role_props
        assert 'ManagedPolicyArns' in cluster_role_props
        
        # Check node role
        node_role_props = node_role['Properties']
        assert 'AssumeRolePolicyDocument' in node_role_props
        assert 'ManagedPolicyArns' in node_role_props
    
    def test_cost_optimization_features(self):
        """Test cost optimization features."""
        # Check single NAT Gateway (cost optimization)
        nat_gateway = self.template['Resources']['NatGateway']
        assert nat_gateway['Type'] == 'AWS::EC2::NatGateway'
        
        # Check t3.small default instance type
        parameters = self.template['Parameters']
        assert parameters['NodeInstanceType']['Default'] == 't3.small'
        
        # Check cost estimate in outputs
        outputs = self.template['Outputs']
        assert 'CostEstimate' in outputs
        assert 't3.small' in outputs['CostEstimate']['Value']
    
    def test_workshop_specific_features(self):
        """Test workshop-specific features."""
        # Check workshop tags
        vpc = self.template['Resources']['VPC']
        vpc_tags = vpc['Properties']['Tags']
        
        workshop_tags = [tag for tag in vpc_tags if tag['Key'] == 'Purpose']
        assert len(workshop_tags) > 0
        assert workshop_tags[0]['Value'] == 'Workshop EKS Cluster'
        
        # Check connection command output
        outputs = self.template['Outputs']
        connection_cmd = outputs['ConnectionCommand']['Value']
        assert 'aws eks update-kubeconfig' in connection_cmd

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
