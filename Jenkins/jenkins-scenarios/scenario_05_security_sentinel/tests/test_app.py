#!/usr/bin/env python3
"""
Security Sentinel - Application Tests
Tests for the Flask application with security features.
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
    assert b'Security Sentinel' in response.data
    assert b'DevSecOps Mastery' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'timestamp' in data
    assert 'security_status' in data
    assert 'uptime' in data
    assert 'request_count' in data
    assert 'cpu_percent' in data
    assert 'memory_percent' in data

def test_security_endpoint(client):
    """Test the security endpoint."""
    response = client.get('/security')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'security_score' in data
    assert 'vulnerabilities' in data
    assert 'security_events' in data
    assert 'security_headers' in data
    assert 'authentication' in data
    assert 'encryption' in data
    assert 'logging' in data

def test_compliance_endpoint(client):
    """Test the compliance endpoint."""
    response = client.get('/compliance')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'compliance_score' in data
    assert 'status' in data
    assert 'checks' in data
    assert 'timestamp' in data

def test_authentication_endpoint(client):
    """Test the authentication endpoint."""
    # Test with valid credentials
    response = client.post('/auth', json={'username': 'admin', 'password': 'password'})
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] == True
    
    # Test with invalid credentials
    response = client.post('/auth', json={'username': 'admin', 'password': 'wrong'})
    assert response.status_code == 401
    
    data = response.get_json()
    assert data['success'] == False

def test_audit_endpoint(client):
    """Test the audit endpoint."""
    # Test without authentication
    response = client.get('/audit')
    assert response.status_code == 401
    
    # Test with authentication (simulate session)
    with client.session_transaction() as sess:
        sess['authenticated'] = True
    
    response = client.get('/audit')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'security_events' in data
    assert 'total_events' in data
    assert 'timestamp' in data

def test_security_headers(client):
    """Test that security headers are present."""
    response = client.get('/')
    
    # Check for security headers
    assert 'X-Content-Type-Options' in response.headers
    assert 'X-Frame-Options' in response.headers
    assert 'X-XSS-Protection' in response.headers
    assert 'Strict-Transport-Security' in response.headers
    assert 'Referrer-Policy' in response.headers
    assert 'Content-Security-Policy' in response.headers

def test_input_validation(client):
    """Test input validation for security."""
    # Test with SQL injection attempt
    response = client.post('/auth', json={'username': "admin'; DROP TABLE users; --", 'password': 'test'})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert 'SQL injection' in data['error']
    
    # Test with XSS attempt
    response = client.post('/auth', json={'username': '<script>alert("xss")</script>', 'password': 'test'})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data
    assert 'XSS' in data['error']

def test_security_events_logging(client):
    """Test that security events are logged."""
    # Make a request that should trigger security event logging
    response = client.post('/auth', json={'username': 'admin', 'password': 'wrong'})
    
    # Check security endpoint for events
    response = client.get('/security')
    data = response.get_json()
    
    assert data['security_events'] > 0

def test_shutdown_endpoint(client):
    """Test the graceful shutdown endpoint."""
    response = client.post('/shutdown')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'message' in data
    assert 'shutdown_in' in data
    assert 'timestamp' in data

def test_security_score_calculation(client):
    """Test that security score is calculated correctly."""
    response = client.get('/security')
    data = response.get_json()
    
    assert 0 <= data['security_score'] <= 100
    assert data['vulnerabilities'] >= 0
    assert data['security_events'] >= 0

def test_compliance_score_calculation(client):
    """Test that compliance score is calculated correctly."""
    response = client.get('/compliance')
    data = response.get_json()
    
    assert 0 <= data['compliance_score'] <= 100
    assert data['status'] in ['compliant', 'non_compliant']

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

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
