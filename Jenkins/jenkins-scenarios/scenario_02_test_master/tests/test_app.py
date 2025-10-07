#!/usr/bin/env python3
"""
Test Master - Application Tests
Basic tests for the Flask application.
"""

import pytest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import DatabaseManager, User

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_manager():
    """Create a test database manager."""
    # Use in-memory database for testing
    manager = DatabaseManager(':memory:')
    return manager

def test_home_page(client):
    """Test the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Master' in response.data
    assert b'Database Integration Demo' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'status' in data
    assert 'timestamp' in data
    assert 'database_status' in data

def test_users_endpoint_get(client):
    """Test getting all users."""
    response = client.get('/users')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'success' in data
    assert 'users' in data
    assert 'count' in data

def test_users_endpoint_post(client):
    """Test creating a new user."""
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = client.post('/users', json=user_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] == True
    assert 'user' in data
    assert data['user']['name'] == 'Test User'
    assert data['user']['email'] == 'test@example.com'

def test_user_operations(client):
    """Test individual user operations."""
    # Create a user first
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = client.post('/users', json=user_data)
    assert response.status_code == 200
    
    data = response.get_json()
    user_id = data['user']['id']
    
    # Test getting the user
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] == True
    assert data['user']['id'] == user_id
    
    # Test updating the user
    update_data = {
        'name': 'Updated User',
        'email': 'updated@example.com'
    }
    
    response = client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] == True
    assert data['user']['name'] == 'Updated User'
    
    # Test deleting the user
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success'] == True

def test_database_manager(db_manager):
    """Test database manager operations."""
    # Test creating a user
    user = db_manager.create_user('Test User', 'test@example.com')
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'
    assert user.id is not None
    
    # Test getting the user
    retrieved_user = db_manager.get_user(user.id)
    assert retrieved_user is not None
    assert retrieved_user.name == 'Test User'
    
    # Test getting all users
    all_users = db_manager.get_all_users()
    assert len(all_users) == 1
    assert all_users[0].name == 'Test User'
    
    # Test updating the user
    updated_user = db_manager.update_user(user.id, name='Updated User')
    assert updated_user is not None
    assert updated_user.name == 'Updated User'
    
    # Test deleting the user
    success = db_manager.delete_user(user.id)
    assert success == True
    
    # Verify user is deleted
    deleted_user = db_manager.get_user(user.id)
    assert deleted_user is None

def test_database_connection(db_manager):
    """Test database connection."""
    assert db_manager.test_connection() == True

def test_user_model():
    """Test User model."""
    user = User(id=1, name='Test User', email='test@example.com')
    assert user.id == 1
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
