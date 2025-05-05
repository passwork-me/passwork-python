import pytest
import os
import json
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_response():
    """Create a mock response with customizable content."""
    def _create_mock_response(status_code=200, json_data=None):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data or {}
        return mock_resp
    return _create_mock_response

@pytest.fixture
def mock_client():
    """Create a mock PassworkClient with mocked _request method."""
    from passwork_client import PassworkClient
    
    with patch('passwork_client.modules.api_client.requests.request') as mock_request:
        client = PassworkClient('https://mock-passwork-api.com')
        client._request = MagicMock()
        client.is_encrypt = False
        yield client

@pytest.fixture
def mock_encrypted_client():
    """Create a mock PassworkClient with encryption enabled."""
    from passwork_client import PassworkClient
    
    with patch('passwork_client.modules.api_client.requests.request') as mock_request:
        client = PassworkClient('https://mock-passwork-api.com')
        client._request = MagicMock()
        client.is_encrypt = True
        # Set encryption-related attributes
        client.master_key = "mock_master_key"
        client.master_key_hash = "mock_master_key_hash"
        client.user_private_key = "mock_private_key"
        client.user_public_key = "mock_public_key"
        yield client

@pytest.fixture
def load_mock_data():
    """Load mock data from JSON files."""
    def _load_data(filename):
        mock_data_dir = os.path.join(os.path.dirname(__file__), 'mock_data')
        file_path = os.path.join(mock_data_dir, filename)
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r') as f:
            return json.load(f)
    return _load_data

@pytest.fixture
def vault_mock_data(load_mock_data):
    """Load vault mock data."""
    return {
        "id": "mock_vault_id",
        "name": "Mock Vault",
        "masterKeyEncrypted": "encrypted_master_key",
        "keyEncrypted": "encrypted_key"
    }

@pytest.fixture
def password_mock_data(load_mock_data):
    """Load password mock data."""
    return {
        "id": "mock_password_id",
        "name": "Mock Password",
        "passwordEncrypted": "encrypted_password",
        "vaultId": "mock_vault_id",
        "vaultMasterKeyEncrypted": "encrypted_vault_master_key",
        "keyEncrypted": "encrypted_key",
        "customs": [
            {
                "name": "Custom Field",
                "valueEncrypted": "encrypted_value",
                "type": "text"
            }
        ],
        "attachments": []
    } 