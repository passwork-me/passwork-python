import sys
import os
from passwork_client import PassworkClient

# Configuration
ACCESS_TOKEN = ""
REFRESH_TOKEN = "" # Optional: if you need to refresh the access token
MASTER_KEY = "" # Optional: master key if client-side encryption is enabled
HOST = "https://passwork" # Your Passwork host

# Login to Passwork with SSL verification disabled
try:
    # Set verify_ssl=False to disable SSL certificate verification
    passwork = PassworkClient(HOST, verify_ssl=False)
    passwork.set_tokens(ACCESS_TOKEN, REFRESH_TOKEN)
    if bool(MASTER_KEY):
        passwork.set_master_key(MASTER_KEY)
except Exception as e:
    print(f"Login Error: {e}")
    exit(1)

# Example: Get an item without SSL verification
try:
    ITEM_ID = "" # Provide the item ID you want to fetch
    DOWNLOAD_PATH = os.path.join("./attachments", ITEM_ID)

    # Fetch the item
    item = passwork.get_item(ITEM_ID)
    
    # Uncomment the line below to download attachments for the item
    # passwork.download_item_attachment(item, DOWNLOAD_PATH)
    
    print(f"Decrypted item: {item}")
except Exception as e:
    print(f"Error getting item: {e}") 