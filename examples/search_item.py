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

# Example: search and decrypt
try:
    tags = [".."] # Optional
    folders = [".."] # Optional
    vaults = [".."] # Optional
    search_query = ".." # Optional
    
    items = passwork.search_and_decrypt(tags=tags, folder_ids=folders, vault_ids=vaults, query=search_query)
    print(f"Decrypted items: {items}")
except Exception as e:
    print(f"Error: {e}")