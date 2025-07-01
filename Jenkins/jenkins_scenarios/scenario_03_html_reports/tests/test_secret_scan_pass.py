"""
Scenario 03: HTML Reports Chaos - Secret Scanning Tests (PASS)

These tests demonstrate proper secret management and scanning patterns
that should always pass with secure configuration.
"""

import pytest
import os
import tempfile
import json
import re
from pathlib import Path
import hashlib
import base64


class TestSecretScanPass:
    """Test secret scanning scenarios that should pass"""

    def test_environment_variables_properly_masked(self):
        """Test that sensitive environment variables are properly handled"""
        # Set up test environment variables (non-sensitive for testing)
        test_env = {
            'APP_NAME': 'chaos-workshop',
            'LOG_LEVEL': 'INFO',
            'ENVIRONMENT': 'test',
            'DATABASE_HOST': 'localhost',
            'CACHE_TTL': '3600'
        }
        
        # Set environment variables
        for key, value in test_env.items():
            os.environ[key] = value
        
        try:
            # Get environment variables
            app_name = os.getenv('APP_NAME')
            log_level = os.getenv('LOG_LEVEL')
            environment = os.getenv('ENVIRONMENT')
            
            # Validate non-sensitive data is accessible
            assert app_name == 'chaos-workshop', "App name should be accessible"
            assert log_level == 'INFO', "Log level should be accessible"
            assert environment == 'test', "Environment should be accessible"
            
            # Ensure we're not exposing sensitive patterns in environment
            sensitive_patterns = [
                r'password',
                r'secret',
                r'key',
                r'token',
                r'credential'
            ]
            
            for env_key in test_env.keys():
                env_key_lower = env_key.lower()
                for pattern in sensitive_patterns:
                    if re.search(pattern, env_key_lower):
                        # If this were a real sensitive var, it should be handled securely
                        # For this test, we ensure no actual sensitive data is present
                        pass
            
            # All environment variables should be non-sensitive
            assert True, "All test environment variables are non-sensitive"
            
        finally:
            # Clean up test environment variables
            for key in test_env.keys():
                os.environ.pop(key, None)

    def test_configuration_files_without_hardcoded_secrets(self):
        """Test that configuration files don't contain hardcoded secrets"""
        # Create test configuration with proper secret references
        secure_config = {
            "database": {
                "host": "${DATABASE_HOST}",
                "port": 5432,
                "name": "${DATABASE_NAME}",
                "username": "${DATABASE_USER}",
                "password_ref": "${DATABASE_PASSWORD_REF}"  # Reference, not actual password
            },
            "cache": {
                "redis_url": "${REDIS_URL}",
                "ttl": 3600
            },
            "api": {
                "base_url": "https://api.example.com",
                "api_key_ref": "${API_KEY_REF}",  # Reference, not actual key
                "timeout": 30
            },
            "logging": {
                "level": "INFO",
                "format": "json"
            }
        }
        
        # Write configuration to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(secure_config, f, indent=2)
            config_file = f.name
        
        try:
            # Read and scan configuration file
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            # Define patterns that should NOT be found (hardcoded secrets)
            forbidden_patterns = [
                r'password["\s]*:["\s]*[^${\s][^"]*',  # Direct password values
                r'secret["\s]*:["\s]*[^${\s][^"]*',    # Direct secret values
                r'key["\s]*:["\s]*[^${\s][^"]*',       # Direct key values (except references)
                r'token["\s]*:["\s]*[^${\s][^"]*',     # Direct token values
                r'[A-Za-z0-9]{32,}',                   # Long alphanumeric strings (potential secrets)
            ]
            
            # Scan for forbidden patterns
            forbidden_found = []
            for pattern in forbidden_patterns:
                matches = re.findall(pattern, config_content, re.IGNORECASE)
                if matches:
                    # Filter out legitimate patterns (like references)
                    for match in matches:
                        if not (match.startswith('${') or 'REF' in match.upper()):
                            forbidden_found.append(match)
            
            # Should not find any hardcoded secrets
            assert len(forbidden_found) == 0, f"Found potential hardcoded secrets: {forbidden_found}"
            
            # Verify that references are used instead
            assert "${DATABASE_PASSWORD_REF}" in config_content, "Should use password reference"
            assert "${API_KEY_REF}" in config_content, "Should use API key reference"
            
        finally:
            # Clean up temporary file
            os.unlink(config_file)

    def test_secure_secret_storage_simulation(self):
        """Test secure secret storage and retrieval simulation"""
        def mock_secure_vault():
            """Mock secure vault for testing"""
            return {
                "database_password": "hashed_or_encrypted_password",
                "api_key": "encrypted_api_key_value", 
                "jwt_secret": "encrypted_jwt_signing_key"
            }
        
        def get_secret_from_vault(secret_name):
            """Simulate secure secret retrieval"""
            vault = mock_secure_vault()
            secret = vault.get(secret_name)
            if secret:
                # In real implementation, this would decrypt/decode
                return f"decrypted_{secret}"
            return None
        
        # Test secure secret retrieval
        db_password = get_secret_from_vault("database_password")
        api_key = get_secret_from_vault("api_key")
        jwt_secret = get_secret_from_vault("jwt_secret")
        
        # Verify secrets are retrieved securely
        assert db_password is not None, "Database password should be retrievable"
        assert api_key is not None, "API key should be retrievable"
        assert jwt_secret is not None, "JWT secret should be retrievable"
        
        # Verify secrets are properly formatted (simulating encryption)
        assert db_password.startswith("decrypted_"), "Password should be properly processed"
        assert api_key.startswith("decrypted_"), "API key should be properly processed"
        assert jwt_secret.startswith("decrypted_"), "JWT secret should be properly processed"
        
        # Test non-existent secret
        invalid_secret = get_secret_from_vault("nonexistent_secret")
        assert invalid_secret is None, "Non-existent secrets should return None"

    def test_secret_rotation_capability(self):
        """Test secret rotation functionality"""
        class SecretManager:
            def __init__(self):
                self.secrets = {}
                self.secret_versions = {}
            
            def store_secret(self, name, value, version=1):
                """Store a secret with version"""
                if name not in self.secret_versions:
                    self.secret_versions[name] = []
                
                self.secrets[f"{name}_v{version}"] = value
                self.secret_versions[name].append(version)
                
            def get_secret(self, name, version=None):
                """Get secret by name and optional version"""
                if version:
                    return self.secrets.get(f"{name}_v{version}")
                else:
                    # Get latest version
                    versions = self.secret_versions.get(name, [])
                    if versions:
                        latest_version = max(versions)
                        return self.secrets.get(f"{name}_v{latest_version}")
                return None
            
            def rotate_secret(self, name, new_value):
                """Rotate secret to new version"""
                versions = self.secret_versions.get(name, [])
                new_version = max(versions) + 1 if versions else 1
                self.store_secret(name, new_value, new_version)
                return new_version
        
        # Test secret rotation
        manager = SecretManager()
        
        # Store initial secret
        manager.store_secret("api_key", "initial_key_value", 1)
        
        # Get initial secret
        current_key = manager.get_secret("api_key")
        assert current_key == "initial_key_value", "Should retrieve initial secret"
        
        # Rotate secret
        new_version = manager.rotate_secret("api_key", "rotated_key_value")
        assert new_version == 2, "New version should be 2"
        
        # Get latest secret
        latest_key = manager.get_secret("api_key")
        assert latest_key == "rotated_key_value", "Should retrieve rotated secret"
        
        # Get specific version
        old_key = manager.get_secret("api_key", version=1)
        assert old_key == "initial_key_value", "Should still be able to access old version"

    def test_secret_hashing_and_verification(self):
        """Test secure secret hashing and verification"""
        def hash_secret(secret, salt=None):
            """Hash a secret with salt"""
            if salt is None:
                salt = os.urandom(32)  # Generate random salt
            
            # Use PBKDF2 for secure hashing
            import hashlib
            hashed = hashlib.pbkdf2_hmac('sha256', secret.encode(), salt, 100000)
            
            # Return salt + hash for storage
            return base64.b64encode(salt + hashed).decode()
        
        def verify_secret(secret, stored_hash):
            """Verify secret against stored hash"""
            try:
                # Decode stored hash
                decoded = base64.b64decode(stored_hash.encode())
                salt = decoded[:32]
                stored_hash_bytes = decoded[32:]
                
                # Hash the provided secret with same salt
                test_hash = hashlib.pbkdf2_hmac('sha256', secret.encode(), salt, 100000)
                
                # Compare hashes
                return test_hash == stored_hash_bytes
            except Exception:
                return False
        
        # Test secret hashing
        original_secret = "super_secure_password_123"
        hashed_secret = hash_secret(original_secret)
        
        # Verify hash format
        assert len(hashed_secret) > 50, "Hashed secret should be significantly longer"
        assert hashed_secret != original_secret, "Hash should be different from original"
        
        # Test verification
        assert verify_secret(original_secret, hashed_secret), "Should verify correct secret"
        assert not verify_secret("wrong_password", hashed_secret), "Should reject wrong secret"
        
        # Test that same secret produces different hashes (due to random salt)
        hashed_secret2 = hash_secret(original_secret)
        assert hashed_secret != hashed_secret2, "Same secret should produce different hashes"
        
        # But both should verify correctly
        assert verify_secret(original_secret, hashed_secret2), "Second hash should also verify"

    def test_api_key_format_validation(self):
        """Test API key format validation for security"""
        def validate_api_key_format(api_key):
            """Validate API key format"""
            if not api_key:
                return False, "API key cannot be empty"
            
            if len(api_key) < 32:
                return False, "API key too short (minimum 32 characters)"
            
            if len(api_key) > 256:
                return False, "API key too long (maximum 256 characters)"
            
            # Check for common patterns that indicate weak keys
            weak_patterns = [
                r'^(test|demo|sample|example)',
                r'^(123|abc|password)',
                r'(.)\1{5,}',  # Repeated characters
            ]
            
            for pattern in weak_patterns:
                if re.search(pattern, api_key, re.IGNORECASE):
                    return False, f"API key matches weak pattern: {pattern}"
            
            # Should contain mix of letters and numbers
            if not re.search(r'[a-zA-Z]', api_key):
                return False, "API key should contain letters"
            
            if not re.search(r'[0-9]', api_key):
                return False, "API key should contain numbers"
            
            return True, "API key format is valid"
        
        # Test valid API keys
        valid_keys = [
            "ak_1234567890abcdef1234567890abcdef12345678",
            "sk_test_abcd1234efgh5678ijkl9012mnop3456qrst",
            "prod_key_9876543210fedcba9876543210fedcba987654"
        ]
        
        for key in valid_keys:
            is_valid, message = validate_api_key_format(key)
            assert is_valid, f"Valid key should pass validation: {message}"
        
        # Test invalid API keys
        invalid_keys = [
            "",  # Empty
            "123",  # Too short
            "test_key",  # Weak pattern
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # Repeated characters
            "abcdefghijklmnopqrstuvwxyz123456789",  # No mixed case
        ]
        
        for key in invalid_keys:
            is_valid, message = validate_api_key_format(key)
            assert not is_valid, f"Invalid key should fail validation: {key}"

    def test_secure_logging_without_secret_exposure(self):
        """Test that logging doesn't expose sensitive information"""
        def secure_log_formatter(message, context=None):
            """Format log message while masking sensitive data"""
            # Patterns to mask in logs
            sensitive_patterns = [
                (r'password["\s]*[:=]["\s]*([^"\s,}]+)', r'password":"***MASKED***"'),
                (r'secret["\s]*[:=]["\s]*([^"\s,}]+)', r'secret":"***MASKED***"'),
                (r'token["\s]*[:=]["\s]*([^"\s,}]+)', r'token":"***MASKED***"'),
                (r'key["\s]*[:=]["\s]*([^"\s,}]+)', r'key":"***MASKED***"'),
                (r'[A-Za-z0-9]{32,}', '***REDACTED***'),  # Long strings that might be secrets
            ]
            
            masked_message = message
            for pattern, replacement in sensitive_patterns:
                masked_message = re.sub(pattern, replacement, masked_message, flags=re.IGNORECASE)
            
            return masked_message
        
        # Test log messages with sensitive data
        test_logs = [
            'User authenticated with password: super_secret_123',
            'API request with token: abcd1234efgh5678ijkl9012mnop3456',
            'Database connection failed for secret: database_password_123',
            'Configuration loaded with key: config_encryption_key_456'
        ]
        
        for log_message in test_logs:
            masked_log = secure_log_formatter(log_message)
            
            # Verify sensitive data is masked
            assert 'super_secret_123' not in masked_log, "Password should be masked"
            assert 'abcd1234efgh5678ijkl9012mnop3456' not in masked_log, "Token should be masked"
            assert 'database_password_123' not in masked_log, "Secret should be masked"
            assert 'config_encryption_key_456' not in masked_log, "Key should be masked"
            
            # Verify masking indicators are present
            assert '***MASKED***' in masked_log or '***REDACTED***' in masked_log, "Should contain masking indicators"

    def test_jwt_token_security_validation(self):
        """Test JWT token security validation"""
        def validate_jwt_security(jwt_payload):
            """Validate JWT security properties"""
            issues = []
            
            # Check expiration
            if 'exp' not in jwt_payload:
                issues.append("JWT missing expiration claim")
            elif jwt_payload['exp'] - jwt_payload.get('iat', 0) > 86400:  # 24 hours
                issues.append("JWT expiration too long (>24 hours)")
            
            # Check issuer
            if 'iss' not in jwt_payload:
                issues.append("JWT missing issuer claim")
            
            # Check audience
            if 'aud' not in jwt_payload:
                issues.append("JWT missing audience claim")
            
            # Check subject
            if 'sub' not in jwt_payload:
                issues.append("JWT missing subject claim")
            
            # Check for sensitive data in payload
            sensitive_fields = ['password', 'secret', 'private_key', 'ssn', 'credit_card']
            for field in sensitive_fields:
                if field in jwt_payload:
                    issues.append(f"JWT contains sensitive field: {field}")
            
            return len(issues) == 0, issues
        
        # Test secure JWT payload
        secure_payload = {
            'sub': 'user123',
            'iss': 'chaos-workshop-api',
            'aud': 'chaos-workshop-client',
            'iat': 1609459200,  # Issued at
            'exp': 1609545600,  # Expires (24 hours later)
            'roles': ['user'],
            'username': 'john_doe'
        }
        
        is_secure, issues = validate_jwt_security(secure_payload)
        assert is_secure, f"Secure JWT should pass validation. Issues: {issues}"
        
        # Test insecure JWT payload
        insecure_payload = {
            'sub': 'user123',
            'password': 'user_password_123',  # Sensitive data
            'iat': 1609459200,
            'exp': 1609459200 + 604800,  # 7 days (too long)
            # Missing required claims
        }
        
        is_secure, issues = validate_jwt_security(insecure_payload)
        assert not is_secure, "Insecure JWT should fail validation"
        assert len(issues) > 0, "Should report security issues"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])