#!/usr/bin/env python3
"""
Pipeline Genesis - Test Suite
Simple tests for the Flask application.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import app
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
    assert b'Pipeline Genesis' in response.data
    assert b'Your first Jenkins pipeline is working!' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'Pipeline Genesis app is running perfectly!' in data['message']

def test_info_endpoint(client):
    """Test the system information endpoint."""
    response = client.get('/info')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['app_name'] == 'Pipeline Genesis'
    assert 'python_version' in data
    assert 'platform' in data
    assert 'working_directory' in data
    assert 'timestamp' in data

def test_app_structure():
    """Test that the app has the expected structure."""
    assert hasattr(app, 'route')
    assert callable(app.run)

def test_environment_variables():
    """Test that environment variables are handled correctly."""
    # Test default environment
    os.environ.pop('ENVIRONMENT', None)
    assert os.environ.get('ENVIRONMENT', 'development') == 'development'
    
    # Test custom environment
    os.environ['ENVIRONMENT'] = 'testing'
    assert os.environ.get('ENVIRONMENT') == 'testing'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
