"""
Scenario 03: HTML Reports Chaos - API Health Check Tests (PASS)

These tests demonstrate proper API health checking patterns
that should always pass with a healthy API service.
"""

import pytest
import requests
import json
import time
from unittest.mock import Mock, patch
import responses


class TestApiHealthPass:
    """Test API health check scenarios that should pass"""

    @responses.activate
    def test_basic_health_endpoint_response(self):
        """Test that basic health endpoint returns successful response"""
        # Mock the health endpoint
        health_response = {
            "status": "healthy",
            "timestamp": "2024-01-01T12:00:00Z",
            "version": "1.0.0",
            "uptime": "72h30m15s"
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/health",
            json=health_response,
            status=200
        )
        
        # Test the health endpoint
        response = requests.get("http://localhost:8080/health")
        
        # Validate response
        assert response.status_code == 200, "Health endpoint should return 200 OK"
        assert response.headers.get('content-type', '').startswith('application/json'), "Response should be JSON"
        
        data = response.json()
        assert data['status'] == 'healthy', "Health status should be 'healthy'"
        assert 'timestamp' in data, "Health response should include timestamp"
        assert 'version' in data, "Health response should include version"
        assert 'uptime' in data, "Health response should include uptime"
        
        # Validate response time
        assert response.elapsed.total_seconds() < 1.0, "Health check should respond quickly (< 1s)"

    @responses.activate
    def test_detailed_health_check_with_dependencies(self):
        """Test detailed health check that includes dependency status"""
        detailed_health = {
            "status": "healthy",
            "timestamp": "2024-01-01T12:00:00Z",
            "version": "1.0.0",
            "dependencies": {
                "database": {
                    "status": "healthy",
                    "response_time_ms": 15,
                    "last_check": "2024-01-01T12:00:00Z"
                },
                "cache": {
                    "status": "healthy", 
                    "response_time_ms": 8,
                    "last_check": "2024-01-01T12:00:00Z"
                },
                "external_api": {
                    "status": "healthy",
                    "response_time_ms": 120,
                    "last_check": "2024-01-01T12:00:00Z"
                }
            },
            "metrics": {
                "memory_usage_mb": 256,
                "cpu_usage_percent": 15.5,
                "active_connections": 42,
                "requests_per_minute": 150
            }
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/health/detailed",
            json=detailed_health,
            status=200
        )
        
        # Test the detailed health endpoint
        response = requests.get("http://localhost:8080/health/detailed")
        
        # Validate response structure
        assert response.status_code == 200, "Detailed health endpoint should return 200 OK"
        data = response.json()
        
        assert data['status'] == 'healthy', "Overall status should be healthy"
        assert 'dependencies' in data, "Response should include dependencies"
        assert 'metrics' in data, "Response should include metrics"
        
        # Validate dependencies
        deps = data['dependencies']
        required_deps = ['database', 'cache', 'external_api']
        for dep in required_deps:
            assert dep in deps, f"Missing dependency: {dep}"
            assert deps[dep]['status'] == 'healthy', f"Dependency {dep} should be healthy"
            assert 'response_time_ms' in deps[dep], f"Dependency {dep} should include response time"
            assert deps[dep]['response_time_ms'] < 1000, f"Dependency {dep} response time too high"
        
        # Validate metrics
        metrics = data['metrics']
        assert metrics['memory_usage_mb'] > 0, "Memory usage should be positive"
        assert 0 <= metrics['cpu_usage_percent'] <= 100, "CPU usage should be percentage"
        assert metrics['active_connections'] >= 0, "Active connections should be non-negative"
        assert metrics['requests_per_minute'] >= 0, "Requests per minute should be non-negative"

    @responses.activate
    def test_api_readiness_check(self):
        """Test API readiness endpoint for deployment validation"""
        readiness_response = {
            "ready": True,
            "timestamp": "2024-01-01T12:00:00Z",
            "checks": {
                "database_migrations": {
                    "status": "passed",
                    "last_migration": "20240101_120000_add_index"
                },
                "configuration_loaded": {
                    "status": "passed",
                    "config_version": "v1.2.3"
                },
                "external_services": {
                    "status": "passed",
                    "services_count": 3
                }
            }
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/ready",
            json=readiness_response,
            status=200
        )
        
        # Test readiness endpoint
        response = requests.get("http://localhost:8080/ready")
        
        # Validate response
        assert response.status_code == 200, "Readiness endpoint should return 200 OK"
        data = response.json()
        
        assert data['ready'] is True, "Service should be ready"
        assert 'checks' in data, "Response should include readiness checks"
        
        # Validate readiness checks
        checks = data['checks']
        required_checks = ['database_migrations', 'configuration_loaded', 'external_services']
        for check in required_checks:
            assert check in checks, f"Missing readiness check: {check}"
            assert checks[check]['status'] == 'passed', f"Readiness check {check} should pass"

    @responses.activate
    def test_api_liveness_check(self):
        """Test API liveness endpoint for container orchestration"""
        liveness_response = {
            "alive": True,
            "timestamp": "2024-01-01T12:00:00Z",
            "process_id": 1234,
            "uptime_seconds": 3600
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/live",
            json=liveness_response,
            status=200
        )
        
        # Test liveness endpoint
        response = requests.get("http://localhost:8080/live")
        
        # Validate response
        assert response.status_code == 200, "Liveness endpoint should return 200 OK"
        data = response.json()
        
        assert data['alive'] is True, "Service should be alive"
        assert data['process_id'] > 0, "Process ID should be positive"
        assert data['uptime_seconds'] >= 0, "Uptime should be non-negative"

    @responses.activate  
    def test_api_version_endpoint(self):
        """Test API version endpoint for deployment tracking"""
        version_response = {
            "version": "1.2.3",
            "build_number": "456",
            "commit_hash": "abc123def456",
            "build_date": "2024-01-01T10:00:00Z",
            "environment": "test"
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/version",
            json=version_response,
            status=200
        )
        
        # Test version endpoint
        response = requests.get("http://localhost:8080/version")
        
        # Validate response
        assert response.status_code == 200, "Version endpoint should return 200 OK"
        data = response.json()
        
        assert 'version' in data, "Response should include version"
        assert 'build_number' in data, "Response should include build number"
        assert 'commit_hash' in data, "Response should include commit hash"
        assert 'build_date' in data, "Response should include build date"
        
        # Validate version format (semantic versioning)
        version = data['version']
        version_parts = version.split('.')
        assert len(version_parts) == 3, "Version should follow semantic versioning (x.y.z)"
        for part in version_parts:
            assert part.isdigit(), "Version parts should be numeric"

    @responses.activate
    def test_api_metrics_endpoint(self):
        """Test API metrics endpoint for monitoring"""
        metrics_response = {
            "metrics": {
                "http_requests_total": 1000,
                "http_request_duration_seconds": {
                    "p50": 0.1,
                    "p95": 0.5,
                    "p99": 1.0
                },
                "active_users": 25,
                "database_connections_active": 5,
                "memory_usage_bytes": 268435456,
                "cpu_usage_percent": 12.5
            },
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/metrics",
            json=metrics_response,
            status=200
        )
        
        # Test metrics endpoint
        response = requests.get("http://localhost:8080/metrics")
        
        # Validate response
        assert response.status_code == 200, "Metrics endpoint should return 200 OK"
        data = response.json()
        
        assert 'metrics' in data, "Response should include metrics"
        metrics = data['metrics']
        
        # Validate key metrics
        assert metrics['http_requests_total'] >= 0, "HTTP requests total should be non-negative"
        assert 'http_request_duration_seconds' in metrics, "Should include request duration metrics"
        assert metrics['active_users'] >= 0, "Active users should be non-negative"
        assert metrics['database_connections_active'] >= 0, "DB connections should be non-negative"
        assert metrics['memory_usage_bytes'] > 0, "Memory usage should be positive"
        assert 0 <= metrics['cpu_usage_percent'] <= 100, "CPU usage should be percentage"
        
        # Validate request duration percentiles
        duration = metrics['http_request_duration_seconds']
        assert duration['p50'] <= duration['p95'] <= duration['p99'], "Percentiles should be ordered"
        assert all(p >= 0 for p in duration.values()), "Duration percentiles should be non-negative"

    @responses.activate
    def test_api_health_with_custom_headers(self):
        """Test API health check with custom headers and authentication"""
        responses.add(
            responses.GET,
            "http://localhost:8080/health",
            json={"status": "healthy"},
            status=200,
            headers={
                "X-Health-Check-Version": "1.0",
                "X-Service-Name": "chaos-workshop-api",
                "Cache-Control": "no-cache"
            }
        )
        
        # Test health endpoint with custom headers
        headers = {
            "User-Agent": "HealthCheck/1.0",
            "Accept": "application/json"
        }
        
        response = requests.get("http://localhost:8080/health", headers=headers)
        
        # Validate response and headers
        assert response.status_code == 200, "Health endpoint should return 200 OK"
        assert response.headers.get("X-Health-Check-Version") == "1.0", "Should include health check version"
        assert response.headers.get("X-Service-Name") == "chaos-workshop-api", "Should include service name"
        assert response.headers.get("Cache-Control") == "no-cache", "Should include cache control"
        
        data = response.json()
        assert data['status'] == 'healthy', "Health status should be healthy"

    def test_health_check_timeout_handling(self):
        """Test that health check handles timeouts gracefully"""
        # Mock a slow response that should complete within timeout
        def mock_health_check(timeout=5):
            """Simulate a health check with configurable timeout"""
            start_time = time.time()
            
            # Simulate some processing time (but within timeout)
            time.sleep(0.1)  # 100ms processing time
            
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                raise TimeoutError(f"Health check timed out after {elapsed:.2f}s")
            
            return {
                "status": "healthy",
                "response_time_ms": int(elapsed * 1000),
                "timeout_configured": timeout
            }
        
        # Test successful health check within timeout
        result = mock_health_check(timeout=1.0)
        
        assert result['status'] == 'healthy', "Health check should succeed within timeout"
        assert result['response_time_ms'] < 1000, "Response time should be under 1 second"
        assert result['timeout_configured'] == 1.0, "Timeout should be configured correctly"

    @responses.activate
    def test_api_dependency_health_aggregation(self):
        """Test that API correctly aggregates health from multiple dependencies"""
        # Setup multiple dependency endpoints
        responses.add(
            responses.GET,
            "http://database:5432/health",
            json={"status": "healthy", "connections": 10},
            status=200
        )
        
        responses.add(
            responses.GET,
            "http://cache:6379/health", 
            json={"status": "healthy", "memory_usage": "45%"},
            status=200
        )
        
        responses.add(
            responses.GET,
            "http://external-api:8080/health",
            json={"status": "healthy", "latency_ms": 150},
            status=200
        )
        
        # Mock the main API health endpoint that aggregates dependencies
        aggregated_health = {
            "status": "healthy",
            "dependencies": {
                "database": {"status": "healthy", "connections": 10},
                "cache": {"status": "healthy", "memory_usage": "45%"},
                "external_api": {"status": "healthy", "latency_ms": 150}
            },
            "overall_health_score": 100
        }
        
        responses.add(
            responses.GET,
            "http://localhost:8080/health/aggregate",
            json=aggregated_health,
            status=200
        )
        
        # Test dependency health checks
        db_response = requests.get("http://database:5432/health")
        cache_response = requests.get("http://cache:6379/health")
        api_response = requests.get("http://external-api:8080/health")
        
        # Validate individual dependencies
        assert db_response.status_code == 200, "Database health should be OK"
        assert cache_response.status_code == 200, "Cache health should be OK"
        assert api_response.status_code == 200, "External API health should be OK"
        
        # Test aggregated health
        aggregate_response = requests.get("http://localhost:8080/health/aggregate")
        assert aggregate_response.status_code == 200, "Aggregate health should be OK"
        
        data = aggregate_response.json()
        assert data['status'] == 'healthy', "Overall status should be healthy"
        assert data['overall_health_score'] == 100, "Health score should be 100 for all healthy dependencies"
        
        # Validate all dependencies are included
        deps = data['dependencies']
        assert 'database' in deps, "Database dependency should be included"
        assert 'cache' in deps, "Cache dependency should be included"
        assert 'external_api' in deps, "External API dependency should be included"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])