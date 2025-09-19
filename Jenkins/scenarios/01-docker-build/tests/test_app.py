#!/usr/bin/env python3
"""
Test suite for Docker Build Pipeline Demo Application
"""

import pytest
import json
import time
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data
        assert 'environment' in data
    
    def test_health_endpoint_structure(self, client):
        """Test health endpoint response structure"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        required_fields = ['status', 'timestamp', 'version', 'environment']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_api_info_endpoint(self, client):
        """Test API info endpoint"""
        response = client.get('/api/info')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['name'] == 'Docker Build Pipeline Demo'
        assert 'version' in data
        assert 'description' in data
        assert 'endpoints' in data
        assert isinstance(data['endpoints'], list)
    
    def test_api_status_endpoint(self, client):
        """Test API status endpoint"""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'application' in data
        assert 'system' in data
        assert 'health' in data
        
        # Check application info
        assert data['application']['name'] == 'Docker Build Pipeline Demo'
        assert data['application']['status'] == 'running'
        
        # Check health info
        assert data['health']['status'] == 'healthy'
        assert 'checks' in data['health']
    
    def test_api_echo_endpoint(self, client):
        """Test API echo endpoint"""
        test_data = {"message": "Hello, Docker!", "test": True}
        
        response = client.post('/api/echo', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['echo'] == test_data
        assert 'timestamp' in data
        assert 'received_at' in data
    
    def test_api_echo_empty_data(self, client):
        """Test API echo endpoint with empty data"""
        response = client.post('/api/echo', 
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['echo'] == {}
    
    def test_api_load_test_endpoint(self, client):
        """Test load test endpoint"""
        response = client.get('/api/load-test')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'result' in data
        assert 'execution_time' in data
        assert 'timestamp' in data
        assert isinstance(data['result'], int)
        assert isinstance(data['execution_time'], float)

class TestMainPage:
    """Test main page"""
    
    def test_main_page(self, client):
        """Test main page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Docker Build Pipeline Demo' in response.data
        assert b'Application Status' in response.data
        assert b'Build Information' in response.data
        assert b'Available Endpoints' in response.data

class TestErrorHandling:
    """Test error handling"""
    
    def test_nonexistent_endpoint(self, client):
        """Test non-existent endpoint returns 404"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_invalid_json_echo(self, client):
        """Test echo endpoint with invalid JSON"""
        response = client.post('/api/echo', 
                             data="invalid json",
                             content_type='application/json')
        # Flask returns 400 for invalid JSON
        assert response.status_code == 400

class TestPerformance:
    """Test performance characteristics"""
    
    def test_health_response_time(self, client):
        """Test health endpoint response time"""
        start_time = time.time()
        response = client.get('/health')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
    
    def test_load_test_performance(self, client):
        """Test load test endpoint performance"""
        start_time = time.time()
        response = client.get('/api/load-test')
        end_time = time.time()
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['execution_time'] < 1.0  # Should complete within 1 second

class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow(self, client):
        """Test complete workflow"""
        # Test health
        health_response = client.get('/health')
        assert health_response.status_code == 200
        
        # Test info
        info_response = client.get('/api/info')
        assert info_response.status_code == 200
        
        # Test status
        status_response = client.get('/api/status')
        assert status_response.status_code == 200
        
        # Test echo
        echo_data = {"test": "integration", "workflow": True}
        echo_response = client.post('/api/echo',
                                  data=json.dumps(echo_data),
                                  content_type='application/json')
        assert echo_response.status_code == 200
        
        # Test load test
        load_response = client.get('/api/load-test')
        assert load_response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
