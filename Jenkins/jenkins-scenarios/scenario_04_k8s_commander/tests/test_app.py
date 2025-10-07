#!/usr/bin/env python3
"""
K8s Commander - Application Tests
Tests for the Flask application with Kubernetes features.
"""

import pytest
import sys
import os
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'K8s Commander' in response.data
    assert b'Kubernetes Deployment' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'timestamp' in data
    assert 'pod_name' in data
    assert 'namespace' in data
    assert 'node_name' in data
    assert 'uptime' in data
    assert 'request_count' in data
    assert 'cpu_percent' in data
    assert 'memory_percent' in data

def test_ready_endpoint(client):
    """Test the readiness check endpoint."""
    response = client.get('/ready')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'timestamp' in data
    assert 'uptime' in data

def test_metrics_endpoint(client):
    """Test the metrics endpoint."""
    response = client.get('/metrics')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'uptime' in data
    assert 'request_count' in data
    assert 'cpu_percent' in data
    assert 'memory_percent' in data
    assert 'memory_used_mb' in data
    assert 'memory_total_mb' in data
    assert 'disk_percent' in data
    assert 'pod_name' in data
    assert 'namespace' in data
    assert 'node_name' in data

def test_info_endpoint(client):
    """Test the system information endpoint."""
    response = client.get('/info')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['app_name'] == 'K8s Commander'
    assert data['version'] == '1.0.0'
    assert 'python_version' in data
    assert 'platform' in data
    assert 'pod_name' in data
    assert 'namespace' in data
    assert 'node_name' in data
    assert 'pod_ip' in data
    assert 'service_account' in data
    assert 'pid' in data

def test_shutdown_endpoint(client):
    """Test the graceful shutdown endpoint."""
    response = client.post('/shutdown')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'message' in data
    assert 'shutdown_in' in data
    assert 'timestamp' in data

def test_health_status_values(client):
    """Test that health status values are reasonable."""
    response = client.get('/health')
    data = response.get_json()
    
    # Check that values are within reasonable ranges
    assert 0 <= data['cpu_percent'] <= 100
    assert 0 <= data['memory_percent'] <= 100
    assert 0 <= data['disk_percent'] <= 100
    assert data['uptime'] >= 0
    assert data['request_count'] >= 0

def test_metrics_values(client):
    """Test that metrics values are reasonable."""
    response = client.get('/metrics')
    data = response.get_json()
    
    # Check that values are within reasonable ranges
    assert 0 <= data['cpu_percent'] <= 100
    assert 0 <= data['memory_percent'] <= 100
    assert 0 <= data['disk_percent'] <= 100
    assert data['uptime'] >= 0
    assert data['request_count'] >= 0
    assert data['memory_used_mb'] >= 0
    assert data['memory_total_mb'] > 0
    assert data['disk_used_gb'] >= 0
    assert data['disk_total_gb'] > 0

def test_request_count_increment(client):
    """Test that request count increments with each request."""
    # Get initial request count
    response1 = client.get('/health')
    data1 = response1.get_json()
    initial_count = data1['request_count']
    
    # Make another request
    response2 = client.get('/health')
    data2 = response2.get_json()
    new_count = data2['request_count']
    
    # Request count should have increased
    assert new_count > initial_count

def test_uptime_increases(client):
    """Test that uptime increases over time."""
    # Get initial uptime
    response1 = client.get('/health')
    data1 = response1.get_json()
    initial_uptime = data1['uptime']
    
    # Wait a bit
    time.sleep(1)
    
    # Get new uptime
    response2 = client.get('/health')
    data2 = response2.get_json()
    new_uptime = data2['uptime']
    
    # Uptime should have increased
    assert new_uptime > initial_uptime

def test_kubernetes_environment_variables():
    """Test that Kubernetes environment variables are handled."""
    # Test default values
    assert os.environ.get('POD_NAME', 'unknown') == 'unknown'
    assert os.environ.get('POD_NAMESPACE', 'default') == 'default'
    assert os.environ.get('NODE_NAME', 'unknown') == 'unknown'
    assert os.environ.get('POD_IP', 'unknown') == 'unknown'
    assert os.environ.get('SERVICE_ACCOUNT', 'default') == 'default'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
