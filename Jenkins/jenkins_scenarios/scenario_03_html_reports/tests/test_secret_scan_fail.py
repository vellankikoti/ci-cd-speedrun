"""
Scenario 03: HTML Reports Chaos - Secret Scanning Tests (FAIL)

These tests simulate real-world secret security failures that should
always fail to demonstrate common enterprise security problems.
"""

import pytest
import os
import tempfile
import json
import re
from pathlib import Path


class TestSecretScanFail:
    """Test secret scanning scenarios that should fail"""

    def test_hardcoded_secrets_in_environment(self):
        """Test detection of hardcoded secrets in environment variables"""
        # Set up environment with hardcoded secrets (intentionally insecure for testing)
        insecure_env = {
            'DATABASE_PASSWORD': 'admin123password',  # Hardcoded password
            'API_SECRET_KEY': 'sk_live_1234567890abcdef1234567890abcdef',  # Hardcoded API key
            'JWT_SIGNING_KEY': 'my_super_secret_jwt_key_123',  # Hardcoded JWT key
            'AWS_SECRET_ACCESS_KEY': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',  # Hardcoded AWS key
            'ENCRYPTION_KEY': 'this_is_my_encryption_key_do_not_share'  # Hardcoded encryption key
        }
        
        # Set environment variables
        for key, value in insecure_env.items():
            os.environ[key] = value
        
        try:
            # Scan for hardcoded secrets
            detected_secrets = []
            for env_key, env_value in insecure_env.items():
                # Check if environment variable contains what looks like a secret
                if any(pattern in env_key.lower() for pattern in ['password', 'secret', 'key', 'token']):
                    if not env_value.startswith('${') and len(env_value) > 10:
                        detected_secrets.append(f"{env_key}={env_value}")
            
            # This should fail because secrets are hardcoded
            assert len(detected_secrets) == 0, f"Found hardcoded secrets: {detected_secrets}"
            
        finally:
            # Clean up environment variables
            for key in insecure_env.keys():
                os.environ.pop(key, None)

    def test_secrets_exposed_in_configuration_files(self):
        """Test detection of secrets in configuration files"""
        # Create configuration with exposed secrets
        insecure_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "admin",
                "password": "supersecretpassword123",  # Hardcoded password
                "connection_string": "postgresql://admin:supersecretpassword123@localhost:5432/mydb"
            },
            "external_apis": {
                "payment_service": {
                    "url": "https://api.payment.com",
                    "api_key": "pk_live_51234567890abcdef12345678",  # Hardcoded API key
                    "secret_key": "sk_live_abcdef1234567890abcdef12"  # Hardcoded secret
                },
                "email_service": {
                    "smtp_host": "smtp.example.com",
                    "smtp_password": "email_service_password_456"  # Hardcoded SMTP password
                }
            },
            "encryption": {
                "secret_key": "my_32_character_secret_key_123456",  # Hardcoded encryption key
                "jwt_secret": "jwt_signing_secret_do_not_share_789"  # Hardcoded JWT secret
            },
            "aws": {
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # Hardcoded AWS secret
            }
        }
        
        # Write insecure configuration to file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(insecure_config, f, indent=2)
            config_file = f.name
        
        try:
            # Read and scan configuration file for secrets
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            # Define patterns that indicate hardcoded secrets
            secret_patterns = [
                r'password["\s]*:["\s]*[^${\s][^"]{8,}',  # Hardcoded passwords
                r'secret["\s]*:["\s]*[^${\s][^"]{16,}',   # Hardcoded secrets
                r'key["\s]*:["\s]*[^${\s][^"]{16,}',      # Hardcoded keys
                r'token["\s]*:["\s]*[^${\s][^"]{20,}',    # Hardcoded tokens
                r'AKIA[0-9A-Z]{16}',                      # AWS Access Key pattern
                r'sk_live_[a-zA-Z0-9]{24,}',              # Stripe secret key pattern
                r'pk_live_[a-zA-Z0-9]{24,}',              # Stripe public key pattern
            ]
            
            # Scan for secret patterns
            found_secrets = []
            for pattern in secret_patterns:
                matches = re.findall(pattern, config_content, re.IGNORECASE)
                found_secrets.extend(matches)
            
            # This should fail because secrets are exposed
            assert len(found_secrets) == 0, f"Found exposed secrets in config: {found_secrets}"
            
        finally:
            # Clean up temporary file
            os.unlink(config_file)

    def test_api_keys_logged_in_plain_text(self):
        """Test detection of API keys being logged in plain text"""
        def insecure_log_function(message, api_key=None, user_data=None):
            """Insecure logging function that exposes secrets"""
            log_entries = []
            
            # This is intentionally insecure logging
            if api_key:
                log_entries.append(f"API request with key: {api_key}")
            
            if user_data and 'password' in user_data:
                log_entries.append(f"User authentication with password: {user_data['password']}")
            
            log_entries.append(f"Message: {message}")
            return log_entries
        
        # Simulate logging with sensitive data
        sensitive_api_key = "sk_live_1234567890abcdef1234567890abcdef"
        user_credentials = {
            "username": "john_doe",
            "password": "user_secret_password_123"
        }
        
        # Generate insecure logs
        log_entries = insecure_log_function(
            "Processing payment request",
            api_key=sensitive_api_key,
            user_data=user_credentials
        )
        
        # Check if secrets are exposed in logs
        exposed_secrets = []
        for log_entry in log_entries:
            if sensitive_api_key in log_entry:
                exposed_secrets.append("API key exposed in logs")
            if user_credentials['password'] in log_entry:
                exposed_secrets.append("Password exposed in logs")
        
        # This should fail because secrets are in logs
        assert len(exposed_secrets) == 0, f"Secrets exposed in logs: {exposed_secrets}"

    def test_weak_secret_generation(self):
        """Test detection of weak secret generation"""
        def generate_weak_secrets():
            """Generate intentionally weak secrets"""
            return {
                "api_key": "123456789012345678901234",  # Sequential numbers
                "session_secret": "password123",         # Dictionary word + numbers
                "encryption_key": "aaaaaaaaaaaaaaaa",    # Repeated characters
                "jwt_secret": "secret",                  # Too short
                "database_password": "admin",            # Common password
                "token": "abcdefghijklmnop"              # Sequential letters
            }
        
        def validate_secret_strength(secret, secret_type):
            """Validate secret strength"""
            issues = []
            
            # Check minimum length
            min_lengths = {
                "api_key": 32,
                "session_secret": 24,
                "encryption_key": 32,
                "jwt_secret": 32,
                "database_password": 12,
                "token": 24
            }
            
            min_length = min_lengths.get(secret_type, 16)
            if len(secret) < min_length:
                issues.append(f"Secret too short (minimum {min_length} characters)")
            
            # Check for common weak patterns
            weak_patterns = [
                (r'^(123|abc|password|admin|secret|test)', "Contains common weak prefix"),
                (r'(.)\1{3,}', "Contains repeated characters"),
                (r'^[a-z]+, "Contains only lowercase letters"),
                (r'^[0-9]+, "Contains only numbers"),
                (r'^[a-zA-Z]+, "Contains only letters"),
            ]
            
            for pattern, message in weak_patterns:
                if re.search(pattern, secret, re.IGNORECASE):
                    issues.append(message)
            
            return len(issues) == 0, issues
        
        # Test weak secrets
        weak_secrets = generate_weak_secrets()
        
        failed_validations = []
        for secret_type, secret_value in weak_secrets.items():
            is_strong, issues = validate_secret_strength(secret_value, secret_type)
            if not is_strong:
                failed_validations.append(f"{secret_type}: {issues}")
        
        # This should fail because all secrets are weak
        assert len(failed_validations) == 0, f"Weak secrets detected: {failed_validations}"

    def test_secrets_in_version_control_simulation(self):
        """Test detection of secrets that would be committed to version control"""
        # Simulate files that would be committed with secrets
        files_with_secrets = {
            ".env": """
# Environment configuration
DATABASE_URL=postgresql://user:secretpassword123@localhost:5432/mydb
API_KEY=sk_live_1234567890abcdef1234567890abcdef
JWT_SECRET=my_jwt_secret_key_do_not_commit_this
STRIPE_SECRET_KEY=sk_test_abcdefghijklmnopqrstuvwxyz123456
""",
            "config.py": """
# Application configuration
DATABASE_PASSWORD = "hardcoded_db_password_123"
API_SECRET_KEY = "my_secret_api_key_456"
ENCRYPTION_KEY = "32_character_encryption_key_789"
""",
            "docker-compose.yml": """
version: '3.8'
services:
  database:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: supersecretpassword
      POSTGRES_USER: admin
  redis:
    image: redis:6
    command: redis-server --requirepass myredispassword123
"""
        }
        
        # Scan files for secrets
        secrets_found = []
        
        for filename, content in files_with_secrets.items():
            # Patterns that indicate secrets in files
            secret_patterns = [
                r'password["\s]*[:=]["\s]*[^"\s$]{8,}',
                r'secret["\s]*[:=]["\s]*[^"\s$]{12,}',
                r'key["\s]*[:=]["\s]*[^"\s$]{16,}',
                r'token["\s]*[:=]["\s]*[^"\s$]{20,}',
                r'sk_[a-zA-Z0-9_]{20,}',
                r'postgresql://[^:\s]+:[^@\s]+@',
            ]
            
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    secrets_found.extend([f"{filename}: {match}" for match in matches])
        
        # This should fail because secrets would be committed
        assert len(secrets_found) == 0, f"Secrets found in version control files: {secrets_found}"

    def test_insecure_secret_transmission(self):
        """Test detection of insecure secret transmission"""
        def simulate_api_request(url, headers=None, data=None):
            """Simulate API request that might expose secrets"""
            security_issues = []
            
            # Check if using HTTP instead of HTTPS
            if url.startswith('http://'):
                security_issues.append("Using insecure HTTP for secret transmission")
            
            # Check if secrets are in URL parameters
            if any(param in url.lower() for param in ['password=', 'secret=', 'key=', 'token=']):
                security_issues.append("Secrets found in URL parameters")
            
            # Check if secrets are in headers without proper security
            if headers:
                for header_name, header_value in headers.items():
                    if 'authorization' in header_name.lower():
                        if not header_value.startswith(('Bearer ', 'Basic ')):
                            security_issues.append("Authorization header format insecure")
            
            # Check if secrets are in request body as plain text
            if data and isinstance(data, dict):
                sensitive_fields = ['password', 'secret', 'key', 'token']
                for field in sensitive_fields:
                    if field in data and isinstance(data[field], str):
                        if len(data[field]) > 8:  # Likely a real secret
                            security_issues.append(f"Secret found in plain text body: {field}")
            
            return security_issues
        
        # Test insecure API requests
        insecure_requests = [
            {
                "url": "http://api.example.com/login?password=mysecretpassword123",
                "headers": {"Content-Type": "application/json"},
                "data": None
            },
            {
                "url": "https://api.example.com/authenticate",
                "headers": {"Authorization": "mysecrettoken123"},  # Wrong format
                "data": None
            },
            {
                "url": "https://api.example.com/user/update",
                "headers": {"Content-Type": "application/json"},
                "data": {"username": "john", "password": "newpassword123", "api_key": "sk_live_secret123"}
            }
        ]
        
        all_security_issues = []
        for i, request in enumerate(insecure_requests):
            issues = simulate_api_request(
                request["url"], 
                request["headers"], 
                request["data"]
            )
            if issues:
                all_security_issues.extend([f"Request {i+1}: {issue}" for issue in issues])
        
        # This should fail because of insecure transmission
        assert len(all_security_issues) == 0, f"Insecure secret transmission detected: {all_security_issues}"

    def test_expired_secrets_still_active(self):
        """Test detection of expired secrets that are still active"""
        import datetime
        
        def check_secret_expiration(secret_registry):
            """Check if any secrets have expired but are still active"""
            current_time = datetime.datetime.now()
            expired_active_secrets = []
            
            for secret_name, secret_info in secret_registry.items():
                expiration_date = datetime.datetime.fromisoformat(secret_info['expires_at'])
                is_active = secret_info['is_active']
                
                if expiration_date < current_time and is_active:
                    expired_active_secrets.append(f"{secret_name} expired on {expiration_date}")
            
            return expired_active_secrets
        
        # Simulate secret registry with expired secrets
        secret_registry = {
            "api_key_prod": {
                "expires_at": "2023-12-01T00:00:00",  # Expired
                "is_active": True  # But still active
            },
            "database_password": {
                "expires_at": "2023-11-15T00:00:00",  # Expired
                "is_active": True  # But still active
            },
            "jwt_signing_key": {
                "expires_at": "2024-06-01T00:00:00",  # Not expired
                "is_active": True
            }
        }
        
        # Check for expired but active secrets
        expired_secrets = check_secret_expiration(secret_registry)
        
        # This should fail because expired secrets are still active
        assert len(expired_secrets) == 0, f"Expired secrets still active: {expired_secrets}"

    def test_secrets_in_error_messages(self):
        """Test detection of secrets being exposed in error messages"""
        def generate_error_with_secret_exposure(operation, secret_value):
            """Generate error message that accidentally exposes secrets"""
            error_messages = []
            
            if operation == "database_connection":
                error_messages.append(f"Database connection failed: postgresql://user:{secret_value}@localhost:5432/db")
            elif operation == "api_call":
                error_messages.append(f"API call failed with key {secret_value}: Invalid credentials")
            elif operation == "encryption":
                error_messages.append(f"Encryption failed using key '{secret_value}': Invalid key format")
            elif operation == "authentication":
                error_messages.append(f"Authentication failed for token {secret_value}: Token expired")
            
            return error_messages
        
        # Test operations that might expose secrets in errors
        test_operations = [
            ("database_connection", "supersecretdbpassword123"),
            ("api_call", "sk_live_1234567890abcdef1234567890abcdef"),
            ("encryption", "my_32_character_encryption_key_123"),
            ("authentication", "jwt_secret_token_do_not_expose_456")
        ]
        
        exposed_secrets_in_errors = []
        for operation, secret in test_operations:
            error_messages = generate_error_with_secret_exposure(operation, secret)
            for error_msg in error_messages:
                if secret in error_msg:
                    exposed_secrets_in_errors.append(f"{operation}: Secret exposed in error message")
        
        # This should fail because secrets are in error messages
        assert len(exposed_secrets_in_errors) == 0, f"Secrets exposed in errors: {exposed_secrets_in_errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])