import pytest
import base64
import hashlib
import re
from unittest.mock import patch, MagicMock
from passwork_client.crypto import (
    encrypt_aes, decrypt_aes, generate_string, generate_salt, generate_key,
    generate_password, generate_user_password, get_random_string,
    get_master_key, get_request_headers, get_hash, rsa_decrypt, rsa_encrypt,
    generate_rsa_keys, evp_bytes_to_key
)

class TestCrypto:
    """Unit tests for crypto.py module"""
    
    def test_evp_bytes_to_key(self):
        """Test key derivation function produces correct key lengths and deterministic results"""
        password = "testpassword"
        salt = b"testsalt"
        key_len = 32
        iv_len = 16
        
        key, iv = evp_bytes_to_key(password, salt, key_len, iv_len)
        
        assert len(key) == key_len
        assert len(iv) == iv_len
        key2, iv2 = evp_bytes_to_key(password, salt, key_len, iv_len)
        assert key == key2
        assert iv == iv2
    
    def test_encrypt_decrypt_aes(self):
        """Test AES encryption/decryption cycle preserves original message"""
        message = "Test message to encrypt"
        passphrase = "secret_passphrase"
        
        encrypted = encrypt_aes(message, passphrase)
        assert encrypted != message
        
        decrypted = decrypt_aes(encrypted, passphrase)
        assert decrypted == message
        
        # Empty passphrase case
        encrypted_empty = encrypt_aes(message, "")
        assert base64.b64decode(encrypted_empty).decode('utf-8') == message
    
    def test_encrypt_decrypt_aes_bytes(self):
        """Test AES encryption/decryption with binary data"""
        message = b"Binary test message to encrypt"
        passphrase = "secret_passphrase"
        
        encrypted = encrypt_aes(message, passphrase, is_bytes=True)
        
        decrypted = decrypt_aes(encrypted, passphrase, is_bytes=True)
        assert decrypted == message
    
    def test_generate_string(self):
        """Test string generation with proper length and character set"""
        length = 32
        result = generate_string(length)
        assert len(result) == length
        
        length = 64
        result = generate_string(length)
        assert len(result) == length
        
        allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!")
        assert all(c in allowed_chars for c in result)
    
    def test_generate_salt(self):
        """Test salt generation with correct length and character set"""
        length = 32
        result = generate_salt(length)
        assert len(result) == length
        
        length = 16
        result = generate_salt(length)
        assert len(result) == length
        
        allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!")
        assert all(c in allowed_chars for c in result)
    
    def test_generate_key(self):
        """Test key generation produces 100-char string with valid characters"""
        result = generate_key()
        assert len(result) == 100
        
        allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!")
        assert all(c in allowed_chars for c in result)
    
    def test_generate_password(self):
        """Test password generation with specified length and valid character set"""
        length = 32
        result = generate_password(length)
        assert len(result) == length
        
        length = 20
        result = generate_password(length)
        assert len(result) == length
        
        allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^")
        assert all(c in allowed_chars for c in result)
    
    def test_generate_user_password(self):
        """Test password generation with various complexity requirements"""
        # Basic generation
        result = generate_user_password(32)
        assert len(result) == 32
        
        # Minimum length requirement
        complexity = {"minLength": 40}
        result = generate_user_password(32, complexity)
        assert len(result) == 40
        
        # Digits requirement
        complexity = {"isDigitsRequired": True}
        result = generate_user_password(32, complexity)
        assert any(c in "0123456789" for c in result)
        
        # Uppercase requirement
        complexity = {"isUppercaseRequired": True}
        result = generate_user_password(32, complexity)
        assert any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in result)
        
        # Special characters requirement
        complexity = {"isSpecialCharactersRequired": True}
        result = generate_user_password(32, complexity)
        assert any(c in "!@#$%^" for c in result)
        
        # All requirements combined
        complexity = {
            "minLength": 20,
            "isDigitsRequired": True,
            "isUppercaseRequired": True,
            "isSpecialCharactersRequired": True
        }
        result = generate_user_password(15, complexity)
        assert len(result) == 20
        assert any(c in "0123456789" for c in result)
        assert any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in result)
        assert any(c in "!@#$%^" for c in result)
    
    def test_get_random_string(self):
        """Test random string generation with custom character sets"""
        length = 32
        possible = "abc123"
        result = get_random_string(length, possible)
        assert len(result) == length
        assert all(c in possible for c in result)
        
        length = 10
        possible = "XYZ"
        result = get_random_string(length, possible)
        assert len(result) == length
        assert all(c in possible for c in result)
    
    def test_get_master_key(self):
        """Test master key generation with custom and default parameters"""
        mk_options = {
            "salt": "testsalt",
            "iterations": 1000,
            "bytes": 32,
            "digest": "sha256"
        }
        master_password = "testpassword"
        
        result = get_master_key(mk_options, master_password)
        
        assert "hashedString" in result
        assert "masterKeyOptions" in result
        assert result["masterKeyOptions"] == "pbkdf:sha256:1000:32:testsalt"
        
        # Check deterministic output
        result2 = get_master_key(mk_options, master_password)
        assert result["hashedString"] == result2["hashedString"]
        
        # Default values
        mk_options_minimal = {"salt": "testsalt"}
        result_default = get_master_key(mk_options_minimal, master_password)
        assert result_default["masterKeyOptions"] == "pbkdf:sha256:300000:64:testsalt"
    
    def test_get_request_headers(self):
        """Test header generation with and without master key"""
        token = "test_token"
        master_key = "test_master_key"
        
        # Without master key
        headers = get_request_headers(token, master_key, False)
        assert headers == {"Passwork-Auth": token}
        
        # With master key
        headers = get_request_headers(token, master_key, True)
        assert headers["Passwork-Auth"] == token
        assert "X-Master-Key-Hash" in headers
        
        expected_hash = hashlib.sha256(master_key.encode()).hexdigest()
        assert headers["X-Master-Key-Hash"] == expected_hash
    
    def test_get_hash(self):
        """Test hash generation with different algorithms"""
        test_str = "test_string"
        
        # SHA-256 (default)
        hash_default = get_hash(test_str)
        hash_sha256 = get_hash(test_str, "sha256")
        assert hash_default == hash_sha256
        assert hash_default == hashlib.sha256(test_str.encode()).hexdigest()
        
        # SHA-512
        hash_sha512 = get_hash(test_str, "sha512")
        assert hash_sha512 == hashlib.sha512(test_str.encode()).hexdigest()
        
        # Empty string
        assert get_hash("") == ""
        
        # Unknown hash function (uses SHA-256)
        hash_unknown = get_hash(test_str, "unknown")
        assert hash_unknown == hash_default
    
    @pytest.fixture
    def rsa_key_pair(self):
        """Generate RSA key pair for testing"""
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        return {
            "private": private_pem,
            "public": public_pem
        }
    
    def test_rsa_encrypt_decrypt(self, rsa_key_pair):
        """Test RSA encryption/decryption cycle"""
        data = "test message for RSA"
        
        encrypted_data = rsa_encrypt(data, rsa_key_pair["public"])
        
        decrypted_data = rsa_decrypt(base64.b64encode(encrypted_data), rsa_key_pair["private"])
        
        assert decrypted_data.decode() == data
    
    def test_generate_rsa_keys(self):
        """Test RSA key pair generation and encryption of private key"""
        master_key = "test_master_key"
        
        result = generate_rsa_keys(master_key)
        
        assert "public" in result
        assert "privateEncrypted" in result
        
        assert "-----BEGIN PUBLIC KEY-----" in result["public"]
        assert "-----END PUBLIC KEY-----" in result["public"]
        
        private_encrypted = result["privateEncrypted"]
        
        # Decrypt private key
        private_decrypted = decrypt_aes(private_encrypted, master_key, is_bytes=True)
        private_str = private_decrypted.decode('utf-8')
        
        assert "-----BEGIN PRIVATE KEY-----" in private_str
        assert "-----END PRIVATE KEY-----" in private_str 