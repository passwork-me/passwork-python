import sys
import os
# import json - Removed
from passwork_client import PassworkClient

# Configuration
ACCESS_TOKEN = ""
REFRESH_TOKEN = "" # Optional (if you need to refresh access token)
MASTER_KEY = "" # Master key (if client side encryption is enabled)
HOST = "https://passwork" # Passwork host

# Login to Passwork
try:
    passwork = PassworkClient(HOST)
    passwork.set_tokens(ACCESS_TOKEN, REFRESH_TOKEN)
    if bool(MASTER_KEY):
        passwork.set_master_key(MASTER_KEY)
except Exception as e:
    print(f"Error: {e}") 
    exit(1)

# Example: Create item
try:
    VAULT_ID = ""
    COLOR = 8
    
    # Example custom fields 
    custom_fields = [
        {
            "name": "Text Field",
            "value": "Field value",
            "type": "text"
        },
        {
            "name": "Custom Password",
            "value": "Secret123!",
            "type": "password"
        },
        {
            "name": "TOTP",
            "value": "ABCDEFGHIJKLMNOP",
            "type": "totp"
        }
    ]
    
    # Prepare item data
    item_data = {
        "vaultId": VAULT_ID,
        "name": "New Item",
        "login": "test_user",
        "password": "Test_password123!",
        "url": "https://example.com",
        "description": "Item description",
        "color": COLOR,
        "tags": ["tag1", "tag2"],
        "customs": custom_fields
    }
    
    # Create item
    item_id = passwork.create_item(item_data)
    print(f"Item created with ID: {item_id}")
    
    # Get the created item
    item = passwork.get_item(item_id)
    print(f"Created item: {item}")

except Exception as e:
    print(f"Error: {e}") 