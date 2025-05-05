import pytest
import json
import os
from unittest.mock import patch, MagicMock
from passwork_client import PassworkClient
from passwork_client.crypto import decrypt_aes, rsa_decrypt
from passwork_client.utils import get_encryption_key

class TestItem:
    
    @pytest.fixture
    def real_mock_item_data(self, load_mock_data):
        """Load real item mock data from saved response."""
        return load_mock_data('item_response.json')
    
    @pytest.fixture
    def real_mock_keys_data(self, load_mock_data):
        """Load real user keys mock data from saved response."""
        return load_mock_data('user_keys_response.json')
        
    def test_get_item_with_real_mock_data(self, mock_encrypted_client, real_mock_item_data, real_mock_keys_data):
        """
        Test get_item method using real mock data saved from API responses.
        This test verifies that the item object is properly decrypted and 
        matches the expected result.
        """
        # Setup mock_encrypted_client to use real mock data
        mock_encrypted_client._request.side_effect = [
            real_mock_item_data  # Return mock item data on request
        ]
        
        # Setup client with actual encryption keys from mock data
        mock_encrypted_client.master_key = "9XwaDw2uumh15+1KMmjIHqZtSQqBb28wiOOdmM376SSGxViRD833HTklq31dJmo7JUrB8gIgY3l8AtWqDKmEog=="
        mock_encrypted_client.user_private_key = decrypt_aes(
            real_mock_keys_data["keys"]["privateEncrypted"], 
            mock_encrypted_client.master_key
        )
        mock_encrypted_client.user_public_key = real_mock_keys_data["keys"]["public"]
        
        # Call the get_item method with the real item ID
        item_id = "673c4da03779c24fd60a80b2"
        item = mock_encrypted_client.get_item(item_id)
        
        # Verify the method made the correct request
        mock_encrypted_client._request.assert_called_once_with(
            "GET", f"/api/v1/items/{item_id}"
        )
        
        # Expected item object after decryption
        expected_item = {
            'id': '673c4da03779c24fd60a80b2',
            'vaultId': '66f2d2efc8d8ccee4d033a84',
            'folderId': None,
            'passwordEncrypted': 'amt4cwv48xb6pp1h71b76xjhahr3amhg71tpmwjf6t468tjr8dn6gwk9emumyphb858mpm1t993kedv6e5r5jhb28xnk6d1f6t4pygr',
            'keyEncrypted': 'amt4cwv48xb6pp1h71aq2ubea5p36ujaan1mpcv7egu6yjb1e9242jkab94qguknd964mw29exq3jtaf6dvpmnkd8dwpgjjpe1tm2xjb91j7jnujdhj6mcuc6tc62gj66gukgwv9a4yku',
            'customs': [
                {'type': 'text', 'value': 'custom-login', 'name': 'Custom name'},
                {'type': 'password', 'value': 'lANeOlEzJ9f2isl$60=q', 'name': 'Custom password'},
                {'type': 'totp', 'value': 'abc', 'name': 'Custom TOTP'}
            ],
            'attachments': [
                {
                    'id': '67f7ed34077a9f28a3086cc2',
                    'encryptedKey': 'amt4cwv48xb6pp1h5dgngmurah442xapc8rmjkutdww72u1qdctmenum6mnmmv226du3gxap6xgqan9b6hcqgvhjcdcpcu1pf9jmcw1fet272na38cv4mhu4d585cnbjcn9q8u3p9n254ru9d16mcv31ad452v3q9d3mej1h8xn64e1g65bpaaup71jk0tvp5dkq8kv69mumcvkmewtmydba6dx52bvadwtpwjuj75amyv2m6hu6rnv9f9upmp3e6n1n0k23ddq30cufamyg',
                    'name': 'test.txt'
                }
            ],
            'name': 'name-test',
            'login': 'login-test',
            'url': 'https://example.com',
            'description': 'notes test',
            'tags': ['test', 'test-2'],
            'isDeleted': False,
            'color': 5,
            'isFavorite': True,
            'vaultMasterKeyEncrypted': 'U9HkOZpHO6XBOK0y78wVG2BDtEJqYyP2RgdOqoHj3ELcpgsFDH+AYihvsd+4d2p5yoer8vNJUh9T6XN1AjrFjNTYyivDYWnE63J5fF2qgdHvsgiDI5My5quWIMxFMgrxopEjcnwbeWoSlR624Is8tKodfYcXlzplOW+ZxQcp8Sc=',
            'password': 'kzwugR]VH-9KF0:~d8h%'
        }
        
        # Verify the item object is correctly decrypted
        # First, check that the password field is decrypted
        assert 'password' in item, "Password field should be present in the result"
        assert item['password'] == expected_item['password'], "Decrypted password doesn't match expected value"
        
        # Check that the customs fields are decrypted
        assert len(item['customs']) == len(expected_item['customs']), "Number of customs fields doesn't match"
        for i, custom in enumerate(item['customs']):
            assert custom['name'] == expected_item['customs'][i]['name'], f"Custom field name {i} doesn't match"
            assert custom['value'] == expected_item['customs'][i]['value'], f"Custom field value {i} doesn't match"
            assert custom['type'] == expected_item['customs'][i]['type'], f"Custom field type {i} doesn't match"
        
        # Check basic fields
        assert item['name'] == expected_item['name'], "Name field doesn't match"
        assert item['login'] == expected_item['login'], "Login field doesn't match"
        assert item['description'] == expected_item['description'], "Description field doesn't match"
        
        # Check that the entire item object matches the expected result
        assert item == expected_item, "Decrypted item object doesn't match expected value" 