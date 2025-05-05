import hashlib
import base64
from pbkdf2 import PBKDF2
from ..crypto import decrypt_aes
from ..exceptions import PassworkError

class MasterKeyManager:
    """
    Handles master key and password management, encryption settings.
    """
    def set_master_password(self, master_password):
        """Derive master key from password and set it."""
        if not master_password:
            # If password is None, disable encryption by setting master key to None
            self.set_master_key(None)
            return

        # Fetch options needed to derive the key
        try:
            self.mk_options = self.call("GET", "/api/v1/users/master-key/options")
            options_parts = self.mk_options["masterKeyOptions"].split(":")
            salt, iterations, key_length = options_parts[4], int(options_parts[2]), int(options_parts[3])

            # Derive the master key using PBKDF2
            derived_master_key = base64.b64encode(
                PBKDF2(master_password, salt, iterations=iterations, digestmodule=hashlib.sha256).read(key_length)
            ).decode()

            # Set the derived master key
            self.set_master_key(derived_master_key)

        except Exception as e:
            # Handle errors during option fetching or key derivation
            self.set_master_key(None) # Ensure encryption is disabled on error
            # Simply propagate the exception
            raise
            
    def set_master_key(self, master_key):
        """
        Set the master key directly, update encryption status, and fetch/decrypt user keys.
        """
        if not master_key:
            # Disable encryption and clear related attributes
            self.is_encrypt = False
            self.master_key = None
            self.master_key_hash = None
            self.user_private_key = None
            self.user_public_key = None
            self.mk_options = None
            return

        # If master_key is provided, attempt to enable encryption
        self.master_key = master_key
        self.master_key_hash = hashlib.sha256(self.master_key.encode()).hexdigest()

        # Fetch and decrypt user keys using the provided master key
        try:
            keys = self.call("GET", "/api/v1/users/keys")["keys"]
            self.user_private_key = decrypt_aes(keys["privateEncrypted"], self.master_key)
            self.user_public_key = keys["public"]
            # Successfully set keys, enable encryption
            self.is_encrypt = True
        except Exception as e:
            # Failed to fetch/decrypt keys, likely invalid master_key
            # Revert changes and disable encryption
            self.master_key = None
            self.master_key_hash = None
            self.user_private_key = None
            self.user_public_key = None
            self.is_encrypt = False
            # Simply propagate the exception
            raise 