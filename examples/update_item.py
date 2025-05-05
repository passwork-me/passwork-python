import sys
import os
# import json - Removed
from passwork_client import PassworkClient

# Configuration
ACCESS_TOKEN = ""
REFRESH_TOKEN = "" # Optional (if you need to refresh access token)
MASTER_KEY = "" # Master key (if client side encryption is enabled)
HOST = "https://passwork" # Passwork host
# VAULT_ID removed from configuration

# Login to Passwork
try:
    passwork = PassworkClient(HOST)
    passwork.set_tokens(ACCESS_TOKEN, REFRESH_TOKEN)
    if bool(MASTER_KEY):
        passwork.set_master_key(MASTER_KEY)
except Exception as e:
    print(f"Error: {e}") 
    exit(1)

# Example: Update item
try:
    # ID of the item to update
    ITEM_ID = ""
    VAULT_ID = ""
    
    # Get current item
    item = passwork.get_item(ITEM_ID)
    print(f"Current item: {item}")
    
    # Prepare updated data
    updated_data = {
        "vaultId": VAULT_ID,
        "name": "Updated Item Name",
        "login": "updated_user",
        "password": "Updated_Password_456!",
        "url": "https://updated-example.com",
        "description": "Updated description",
        "tags": ["updated", "tag2", "tag3"],
        "customs": [
            {
                "name": "Updated Custom Field",
                "value": "Updated value",
                "type": "text"
            },
            {
                "name": "Updated Password Field",
                "value": "NewSecret456!",
                "type": "password"
            }
        ]
    }
    
    # Update the item
    passwork.update_item(ITEM_ID, updated_data)
    
    # Get the updated item
    updated_item = passwork.get_item(ITEM_ID)
    print(f"Updated item: {updated_item}")

except Exception as e:
    print(f"Error: {e}") 