import os
import json
import base64
import requests
from ..crypto import encrypt_aes, decrypt_aes

class SessionManager:
    """
    Manages session tokens, refresh operations, and session persistence.
    """
    def save_session(self, file_path, encryption_key = None, save_master_key = False) -> str:
        """Save session tokens and optionally the master key to a file."""
        if encryption_key is None:
            encryption_key = base64.b64encode(os.urandom(32)).decode()

        # Get master key if we should save it and it exists
        master_key = None
        if save_master_key and hasattr(self, 'master_key'):
            master_key = self.master_key

        session_data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "master_key": master_key if save_master_key else None
        }

        encrypted = encrypt_aes(json.dumps(session_data), encryption_key)
        encrypted_data = base64.b64encode(encrypted.encode("utf-8"))
        with open(file_path, "w") as file:
            file.write(encrypted_data.decode("utf-8"))

        self.session_path = file_path
        self.session_encryption_key = encryption_key

        return encryption_key

    def load_session(self, file_path, encryption_key):
        """Load session tokens and optionally the master key from a file."""
        with open(file_path, "r") as file:
            encrypted_data = file.read()

        decrypted_data = json.loads(decrypt_aes(base64.b64decode(encrypted_data).decode("utf-8"), encryption_key))
        self.access_token = decrypted_data["access_token"]
        self.refresh_token = decrypted_data["refresh_token"]

        # Store session info
        self.session_path = file_path
        self.session_encryption_key = encryption_key
        
        # Get the loaded master key
        loaded_master_key = decrypted_data.get("master_key")
        
        # If master key was saved, try to set it using set_master_key method
        if loaded_master_key and hasattr(self, 'set_master_key'):
            try:
                self.set_master_key(loaded_master_key)
            except ValueError as e:
                # Optionally handle the error differently for session load
                print(f"Warning: Master key loaded from session failed validation: {e}")
        
        return loaded_master_key 