#!/usr/bin/env python3
"""
Real TestContainers Integration Tests
Tests using actual TestContainers with PostgreSQL database
"""

import os
import sys
import json
import time
import threading
import requests
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.compose import DockerCompose

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TestContainersDatabaseManager
import app

class TestTestContainersIntegration:
    """Test real TestContainers integration with PostgreSQL"""

    @classmethod
    def setup_class(cls):
        """Set up TestContainers PostgreSQL for all tests"""
        print("\n🐳 Starting TestContainers PostgreSQL...")
        
        # Start PostgreSQL container
        cls.postgres_container = PostgresContainer("postgres:15")
        cls.postgres_container.start()
        
        # Get connection details
        cls.host = cls.postgres_container.get_container_host_ip()
        cls.port = cls.postgres_container.get_exposed_port(5432)
        cls.database = cls.postgres_container.get_database_name()
        cls.username = cls.postgres_container.get_username()
        cls.password = cls.postgres_container.get_password()
        
        print(f"✅ PostgreSQL container started: {cls.host}:{cls.port}")
        print(f"📊 Database: {cls.database}, User: {cls.username}")

    @classmethod
    def teardown_class(cls):
        """Clean up TestContainers"""
        print("\n🛑 Stopping TestContainers...")
        cls.postgres_container.stop()
        print("✅ TestContainers stopped")

    def test_database_connection(self):
        """Test direct database connection"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        
        # Test connection
        assert db_manager.health_check() == True
        print("✅ Database connection test passed")

    def test_database_initialization(self):
        """Test database initialization with TestContainers"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        
        # Initialize database
        db_manager.init_database()
        
        # Test that tables were created
        users = db_manager.get_users()
        assert len(users) >= 5  # Should have 5 sample users
        print("✅ Database initialization test passed")

    def test_crud_operations(self):
        """Test CRUD operations with TestContainers database"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        db_manager.init_database()
        
        # Test CREATE
        new_user = db_manager.create_user("Test User", "test@testcontainers.com")
        assert 'error' not in new_user
        assert new_user['name'] == "Test User"
        assert new_user['email'] == "test@testcontainers.com"
        user_id = new_user['id']
        print("✅ CREATE operation test passed")
        
        # Test READ
        users = db_manager.get_users()
        assert len(users) >= 6  # Original 5 + new user
        print("✅ READ operation test passed")
        
        # Test UPDATE
        updated_user = db_manager.update_user(user_id, name="Updated User")
        assert 'error' not in updated_user
        assert updated_user['name'] == "Updated User"
        print("✅ UPDATE operation test passed")
        
        # Test DELETE
        delete_result = db_manager.delete_user(user_id)
        assert 'error' not in delete_result
        assert 'deleted_user' in delete_result
        print("✅ DELETE operation test passed")

    def test_database_stats(self):
        """Test database statistics with TestContainers"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        db_manager.init_database()
        
        stats = db_manager.get_database_stats()
        assert 'user_count' in stats
        assert 'database_size' in stats
        assert 'tables' in stats
        assert stats['user_count'] >= 5
        print("✅ Database stats test passed")

    def test_concurrent_operations(self):
        """Test concurrent database operations"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        db_manager.init_database()
        
        results = []
        
        def create_user_operation(user_id):
            result = db_manager.create_user(f"Concurrent User {user_id}", f"concurrent{user_id}@test.com")
            if 'error' not in result:
                results.append(user_id)
        
        # Create 10 concurrent threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_user_operation, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        assert len(results) == 10
        print("✅ Concurrent operations test passed")

    def test_error_handling(self):
        """Test error handling with TestContainers"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        db_manager.init_database()
        
        # Test duplicate email
        db_manager.create_user("User 1", "duplicate@test.com")
        result = db_manager.create_user("User 2", "duplicate@test.com")
        assert 'error' in result
        assert 'already exists' in result['error']
        print("✅ Error handling test passed")

    def test_raw_queries(self):
        """Test raw SQL queries with TestContainers"""
        db_manager = TestContainersDatabaseManager(
            self.host, self.port, self.database, self.username, self.password
        )
        db_manager.init_database()
        
        # Test raw query
        results = db_manager.execute_raw_query(
            "SELECT COUNT(*) as total FROM users WHERE name LIKE %s",
            ('%User%',)
        )
        assert len(results) == 1
        assert 'total' in results[0]
        print("✅ Raw queries test passed")


class TestApplicationWithTestContainers:
    """Test the full application with TestContainers"""

    @classmethod
    def setup_class(cls):
        """Set up TestContainers and start application"""
        print("\n🐳 Starting TestContainers for application testing...")
        
        # Start PostgreSQL container
        cls.postgres_container = PostgresContainer("postgres:15")
        cls.postgres_container.start()
        
        # Get connection details
        cls.host = cls.postgres_container.get_container_host_ip()
        cls.port = cls.postgres_container.get_exposed_port(5432)
        cls.database = cls.postgres_container.get_database_name()
        cls.username = cls.postgres_container.get_username()
        cls.password = cls.postgres_container.get_password()
        
        # Set environment variables for the application
        os.environ['DB_TYPE'] = 'testcontainers'
        os.environ['TESTCONTAINERS_HOST'] = cls.host
        os.environ['TESTCONTAINERS_PORT'] = str(cls.port)
        os.environ['DB_NAME'] = cls.database
        os.environ['DB_USER'] = cls.username
        os.environ['DB_PASSWORD'] = cls.password
        os.environ['PORT'] = '5002'  # Use different port for testing
        
        # Start application in background thread
        cls.app_thread = threading.Thread(
            target=app.start_server,
            args=(5002,),
            daemon=True
        )
        cls.app_thread.start()
        
        # Wait for application to start
        time.sleep(3)
        
        cls.base_url = 'http://localhost:5002'
        print(f"✅ Application started with TestContainers: {cls.base_url}")

    @classmethod
    def teardown_class(cls):
        """Clean up TestContainers and application"""
        print("\n🛑 Stopping TestContainers and application...")
        cls.postgres_container.stop()
        print("✅ TestContainers stopped")

    def test_health_endpoint(self):
        """Test health endpoint with TestContainers"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['database'] == 'connected'
        print("✅ Health endpoint test passed")

    def test_users_api(self):
        """Test users API with TestContainers"""
        # Test GET users
        response = requests.get(f"{self.base_url}/api/users")
        assert response.status_code == 200
        
        data = response.json()
        assert 'users' in data
        assert 'count' in data
        assert data['count'] >= 5  # Should have sample users
        print("✅ Users API GET test passed")
        
        # Test POST user
        new_user_data = {
            'name': 'API Test User',
            'email': 'apitest@testcontainers.com'
        }
        
        response = requests.post(
            f"{self.base_url}/api/users",
            json=new_user_data
        )
        assert response.status_code == 201
        
        data = response.json()
        assert 'user' in data
        assert data['user']['name'] == new_user_data['name']
        user_id = data['user']['id']
        print("✅ Users API POST test passed")
        
        # Test PUT user
        update_data = {
            'name': 'Updated API User',
            'email': 'updated@testcontainers.com'
        }
        
        response = requests.put(
            f"{self.base_url}/api/users/{user_id}",
            json=update_data
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data['user']['name'] == update_data['name']
        print("✅ Users API PUT test passed")
        
        # Test DELETE user
        response = requests.delete(f"{self.base_url}/api/users/{user_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert 'deleted_user' in data
        print("✅ Users API DELETE test passed")

    def test_database_endpoints(self):
        """Test database-specific endpoints"""
        # Test DB status
        response = requests.get(f"{self.base_url}/api/db-status")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'connected'
        assert data['database_type'] == 'PostgreSQL'
        print("✅ DB status endpoint test passed")
        
        # Test DB stats
        response = requests.get(f"{self.base_url}/api/db-stats")
        assert response.status_code == 200
        
        data = response.json()
        assert 'user_count' in data
        assert 'database_size' in data
        assert 'tables' in data
        print("✅ DB stats endpoint test passed")

    def test_main_page(self):
        """Test main page loads with TestContainers"""
        response = requests.get(self.base_url)
        assert response.status_code == 200
        
        content = response.text
        assert 'TestContainers Integration Demo' in content
        assert 'PostgreSQL' in content
        assert 'Database Statistics' in content
        print("✅ Main page test passed")

    def test_error_handling(self):
        """Test API error handling"""
        # Test invalid user ID
        response = requests.put(
            f"{self.base_url}/api/users/invalid",
            json={'name': 'Test'}
        )
        assert response.status_code == 400
        print("✅ Error handling test passed")

    def test_performance_with_testcontainers(self):
        """Test performance with TestContainers database"""
        start_time = time.time()
        
        # Create multiple users
        for i in range(20):
            user_data = {
                'name': f'Performance User {i}',
                'email': f'perf{i}@testcontainers.com'
            }
            response = requests.post(f"{self.base_url}/api/users", json=user_data)
            assert response.status_code == 201
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 10.0  # Should complete within 10 seconds
        print(f"✅ Performance test passed: {execution_time:.2f}s for 20 users")


class TestDockerComposeIntegration:
    """Test integration with Docker Compose"""

    def test_docker_compose_setup(self):
        """Test that docker-compose.test.yml works with TestContainers"""
        # This test would run the docker-compose setup
        # and verify it works with TestContainers
        compose_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'docker-compose.test.yml'
        )
        
        if os.path.exists(compose_file):
            # Test that compose file exists and is valid
            with open(compose_file, 'r') as f:
                content = f.read()
                assert 'postgres' in content.lower()
                assert 'testcontainers' in content.lower()
            print("✅ Docker Compose file validation passed")
        else:
            print("⚠️ Docker Compose file not found, skipping test")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
