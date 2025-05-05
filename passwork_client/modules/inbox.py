from base64 import b64encode
from ..utils import get_encryption_key, decrypt_item, decrypt_and_save_item_attachment
from ..crypto import rsa_encrypt, rsa_decrypt, encrypt_aes, decrypt_aes

class Inbox:
    """
    A client for interacting with the Passwork Inbox API.
    All methods in this class are related to inbox management functionality.
    """
    def get_inbox_item(self, inbox_item_id: str):
        inbox_item = self.call("GET", f"/api/v1/inbox-items/{inbox_item_id}")

        if self.is_encrypt:
            vault_password = rsa_decrypt(inbox_item["inbox"]["keyEncrypted"], self.user_private_key).decode("utf-8")
            self._decrypt_inbox_password(inbox_item, vault_password)
        
        return inbox_item

    def _decrypt_inbox_password(self, password: dict, encrypted_key: str):
        if not encrypted_key:
            return password

        password["password"] = decrypt_item(password["passwordEncrypted"], encrypted_key)

    def download_inbox_attachment(self, inbox: dict, download_path: str):

        if "attachments" not in inbox or not inbox["attachments"]:
            return None

        attachments_data = self.prepare_attachments_data(inbox["attachments"], inbox['id'])
        if not attachments_data:
            return None

        if self.is_encrypt:
            encrypted_key = rsa_decrypt(inbox["inbox"]["keyEncrypted"], self.user_private_key).decode("utf-8")
        else:
            encrypted_key = ""

        for attachment_data in attachments_data:
            decrypt_and_save_item_attachment(attachment_data, encrypted_key, download_path)