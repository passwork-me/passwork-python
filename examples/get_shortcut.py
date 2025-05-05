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

# Example: Get shortcut
try:
    SHORTCUT_ID = ""
    #DOWNLOAD_PATH = os.path.join("./attachments", SHORTCUT_ID) 

    shortcut = passwork.get_shortcut(SHORTCUT_ID) 
    
    # Attachment download call (assuming method exists)
    #passwork.download_shortcut_attachment(shortcut, DOWNLOAD_PATH)
    
    print(f"Decrypted shortcut: {shortcut}") 

except Exception as e:
    print(f"Error: {e}") 