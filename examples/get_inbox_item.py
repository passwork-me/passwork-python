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

# Example: Get inbox password
try:
    INBOX_ID = ""
    inbox = passwork.get_inbox_item(INBOX_ID)
    download_path = os.path.join("./attachments", INBOX_ID)
        
    #passwork.download_inbox_attachment(inbox, download_path)

    print(f"Decrypted inbox password: {inbox}") 

except Exception as e:
    print(f"Error: {e}") 