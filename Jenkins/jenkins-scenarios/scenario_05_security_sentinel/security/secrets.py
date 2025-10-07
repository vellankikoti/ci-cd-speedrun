#!/usr/bin/env python3
"""
Security Sentinel - Secrets Management Script
Secure secrets management and rotation.
"""

import os
import sys
import json
import base64
import secrets
import hashlib
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecretsManager:
    """Secure secrets management class."""
    
    def __init__(self, master_password=None):
        """Initialize secrets manager."""
        self.master_password = master_password or os.environ.get('MASTER_PASSWORD', 'default_password')
        self.secrets_file = 'secrets.json'
        self.encryption_key = self._derive_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _derive_key(self):
        """Derive encryption key from master password."""
        password = self.master_password.encode()
        salt = b'security_sentinel_salt'  # In production, use random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def generate_secret(self, name, length=32):
        """Generate a new secret."""
        secret = secrets.token_urlsafe(length)
        return secret
    
    def store_secret(self, name, value, description=""):
        """Store a secret securely."""
        try:
            # Load existing secrets
            secrets_data = self._load_secrets()
            
            # Encrypt the secret
            encrypted_value = self.cipher.encrypt(value.encode())
            
            # Store the secret
            secrets_data[name] = {
                'value': base64.b64encode(encrypted_value).decode(),
                'description': description,
                'created_at': datetime.now().isoformat(),
                'last_rotated': datetime.now().isoformat()
            }
            
            # Save secrets
            self._save_secrets(secrets_data)
            print(f"✅ Secret '{name}' stored securely")
            return True
            
        except Exception as e:
            print(f"❌ Error storing secret '{name}': {e}")
            return False
    
    def retrieve_secret(self, name):
        """Retrieve a secret."""
        try:
            secrets_data = self._load_secrets()
            
            if name not in secrets_data:
                print(f"❌ Secret '{name}' not found")
                return None
            
            # Decrypt the secret
            encrypted_value = base64.b64decode(secrets_data[name]['value'])
            decrypted_value = self.cipher.decrypt(encrypted_value)
            
            return decrypted_value.decode()
            
        except Exception as e:
            print(f"❌ Error retrieving secret '{name}': {e}")
            return None
    
    def rotate_secret(self, name):
        """Rotate a secret."""
        try:
            secrets_data = self._load_secrets()
            
            if name not in secrets_data:
                print(f"❌ Secret '{name}' not found")
                return False
            
            # Generate new secret
            new_secret = self.generate_secret(name)
            
            # Encrypt and store
            encrypted_value = self.cipher.encrypt(new_secret.encode())
            secrets_data[name]['value'] = base64.b64encode(encrypted_value).decode()
            secrets_data[name]['last_rotated'] = datetime.now().isoformat()
            
            # Save secrets
            self._save_secrets(secrets_data)
            print(f"✅ Secret '{name}' rotated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error rotating secret '{name}': {e}")
            return False
    
    def list_secrets(self):
        """List all secrets."""
        try:
            secrets_data = self._load_secrets()
            
            if not secrets_data:
                print("No secrets found")
                return []
            
            print("📋 Stored Secrets:")
            print("-" * 50)
            
            for name, data in secrets_data.items():
                print(f"Name: {name}")
                print(f"Description: {data['description']}")
                print(f"Created: {data['created_at']}")
                print(f"Last Rotated: {data['last_rotated']}")
                print("-" * 50)
            
            return list(secrets_data.keys())
            
        except Exception as e:
            print(f"❌ Error listing secrets: {e}")
            return []
    
    def delete_secret(self, name):
        """Delete a secret."""
        try:
            secrets_data = self._load_secrets()
            
            if name not in secrets_data:
                print(f"❌ Secret '{name}' not found")
                return False
            
            del secrets_data[name]
            self._save_secrets(secrets_data)
            print(f"✅ Secret '{name}' deleted")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting secret '{name}': {e}")
            return False
    
    def _load_secrets(self):
        """Load secrets from file."""
        if os.path.exists(self.secrets_file):
            with open(self.secrets_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_secrets(self, secrets_data):
        """Save secrets to file."""
        with open(self.secrets_file, 'w') as f:
            json.dump(secrets_data, f, indent=2)
    
    def check_secret_rotation(self):
        """Check if secrets need rotation."""
        try:
            secrets_data = self._load_secrets()
            rotation_needed = []
            
            for name, data in secrets_data.items():
                last_rotated = datetime.fromisoformat(data['last_rotated'])
                days_since_rotation = (datetime.now() - last_rotated).days
                
                if days_since_rotation > 90:  # Rotate every 90 days
                    rotation_needed.append({
                        'name': name,
                        'days_since_rotation': days_since_rotation
                    })
            
            if rotation_needed:
                print("⚠️ Secrets that need rotation:")
                for secret in rotation_needed:
                    print(f"  - {secret['name']} (last rotated {secret['days_since_rotation']} days ago)")
            else:
                print("✅ All secrets are up to date")
            
            return rotation_needed
            
        except Exception as e:
            print(f"❌ Error checking secret rotation: {e}")
            return []
    
    def generate_compliance_report(self):
        """Generate secrets compliance report."""
        try:
            secrets_data = self._load_secrets()
            rotation_needed = self.check_secret_rotation()
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_secrets': len(secrets_data),
                'secrets_needing_rotation': len(rotation_needed),
                'compliance_score': 100 - (len(rotation_needed) * 10),
                'rotation_needed': rotation_needed
            }
            
            print(f"\n📊 Secrets Compliance Report")
            print("=" * 50)
            print(f"Total secrets: {report['total_secrets']}")
            print(f"Secrets needing rotation: {report['secrets_needing_rotation']}")
            print(f"Compliance score: {report['compliance_score']}/100")
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating compliance report: {e}")
            return None

def main():
    """Main secrets management function."""
    print("🔒 Security Sentinel - Secrets Management")
    print("=" * 60)
    print("This script manages secrets securely.")
    print()
    
    # Initialize secrets manager
    manager = SecretsManager()
    
    # Demo secrets management
    print("🔐 Demonstrating Secrets Management...")
    
    # Store some demo secrets
    demo_secrets = {
        'database_password': 'super_secure_db_password_123',
        'api_key': 'sk-1234567890abcdef',
        'jwt_secret': 'jwt_secret_key_for_tokens',
        'encryption_key': 'encryption_key_for_data'
    }
    
    for name, value in demo_secrets.items():
        manager.store_secret(name, value, f"Demo {name}")
    
    # List secrets
    manager.list_secrets()
    
    # Check rotation
    manager.check_secret_rotation()
    
    # Generate compliance report
    report = manager.generate_compliance_report()
    
    # Test secret retrieval
    print("\n🔍 Testing Secret Retrieval...")
    for name in demo_secrets.keys():
        secret = manager.retrieve_secret(name)
        if secret:
            print(f"✅ Retrieved secret '{name}': {secret[:10]}...")
        else:
            print(f"❌ Failed to retrieve secret '{name}'")
    
    # Test secret rotation
    print("\n🔄 Testing Secret Rotation...")
    manager.rotate_secret('database_password')
    
    # Clean up demo secrets
    print("\n🧹 Cleaning up demo secrets...")
    for name in demo_secrets.keys():
        manager.delete_secret(name)
    
    print("\n✅ Secrets management demonstration completed!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
