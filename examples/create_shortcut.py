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


# Example: Create shortcut
try:
    PASSWORD_ID = ""
    VAULT_ID = ""
    FOLDER_ID = None

    shortcut_id = passwork.create_shortcut(PASSWORD_ID, VAULT_ID, FOLDER_ID) 

    print(f"Shortcut was created: {shortcut_id}") 

except Exception as e:
    print(f"Error: {e}") 