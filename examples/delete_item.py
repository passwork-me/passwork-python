import sys
import os
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

# Example: Delete item
try:
    # ID of the item to delete
    ITEM_ID = ""
    
    # Delete the item
    bin_item_id = passwork.delete_item(ITEM_ID)
    print(f"Item deleted. Bin item ID: {bin_item_id}")
    
except Exception as e:
    print(f"Error: {e}")