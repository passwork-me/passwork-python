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

# Example: Save session to file
try:
    # Save session (session file will be encrypted with random key — encryption_key)
    encryption_key = passwork.save_session("session.file", None, True)
    print(f"Encryption key: {encryption_key}")

    # Save session with encryption key
    # passwork.save_session("session", "P2eYN+VtHH27Hno2plpWwoxFOZ0uFNLzubdEcLUPCSU=", True)
except Exception as e:
    print(f"Error: {e}") 
    

# Example: Load session from file
try:
    # Initialize new client and load
    passwork_load = PassworkClient(HOST) 
    # Load using the key obtained above (ensure it's available)
    if 'encryption_key' in locals():
        passwork_load.load_session("session.file", encryption_key) 
        print(f"Session loaded")
    else:
        print("Error: Encryption key from save step not found.")
except Exception as e:
    print(f"Error: {e}") 
    



