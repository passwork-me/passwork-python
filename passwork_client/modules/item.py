import json
from ..crypto import encrypt_aes
from ..utils import (
    encrypt_item_customs,
    validate_item_customs,
    format_item_attachments,
    decrypt_item, get_encryption_key,
    decrypt_item_attachments, decrypt_item_customs,
    decrypt_and_save_item_attachment
)

class Item:
    def create_item(self, item_data: dict) -> str:
        vault = self.get_vault(item_data["vaultId"])
        vault_password = self.get_vault_password(vault)

        self.encrypt_item(item_data, vault_password)
        self.encrypt_item_customs(item_data, vault_password)
        self.encrypt_item_attachments(item_data, vault_password)
        item_data.setdefault("name", "")

        response = self.call("POST", "/api/v1/items", item_data)

        return response["id"]

    def update_item(self, item_id: str, item_data: dict):
        vault = self.get_vault(item_data["vaultId"])
        vault_password = self.get_vault_password(vault)

        self.encrypt_item(item_data, vault_password)
        self.encrypt_item_customs(item_data, vault_password)
        self.encrypt_item_attachments(item_data, vault_password)

        response = self.call("PATCH", f"/api/v1/items/{item_id}", item_data)

    def delete_item(self, item_id: str):
        response = self.call('DELETE', f"/api/v1/items/{item_id}")

        return response["binItemId"]

    def get_item(self, item_id: str):
        item_data = self.call("GET", f"/api/v1/items/{item_id}")

        if self.is_encrypt:
            encrypted_key = get_encryption_key(
                item_data["vaultMasterKeyEncrypted"],
                item_data["keyEncrypted"],
                self.user_private_key
            )
        else:
            encrypted_key = ''

        self.decrypt_item(item_data, encrypted_key)

        self.decrypt_item_customs(item_data, encrypted_key)

        return item_data

    def get_items(self, item_ids: list[str]):
        if not item_ids:
            return []

        requests = []
        for id in item_ids:
            requests.append({
                "method": "GET",
                "relativeUrl": f"/api/v1/items/{id}",
            })

        items = self.send_batch(requests)

        # Process each item in the response
        decrypted_items = []
        for item_data in items:
            if self.is_encrypt:
                encrypted_key = get_encryption_key(
                    item_data["vaultMasterKeyEncrypted"],
                    item_data["keyEncrypted"],
                    self.user_private_key
                )
            else:
                encrypted_key = ''
                
            # Decrypt the item using the same methods as get_item
            self.decrypt_item(item_data, encrypted_key)
            self.decrypt_item_customs(item_data, encrypted_key)

            decrypted_items.append(item_data)

        return decrypted_items

    def search_items(self, query: str = None, tags: list[str] = None, color_codes: list[int] = None, url: str = None,
               vault_ids: list[str] = None, folder_ids: list[str] = None):
        # Build payload with only non-None parameters
        payload = {}
        if query is not None:
            payload["query"] = query
        if url is not None:
            payload["url"] = url
        if tags is not None:
            payload["tags"] = tags
        if color_codes is not None:
            payload["colorCodes"] = color_codes
        if vault_ids is not None:
            payload["vaultIds"] = vault_ids
        if folder_ids is not None:
            payload["folderIds"] = folder_ids
            
        # Make the request using the call method which will handle array formatting
        search_results = self.call("GET", "/api/v1/items/search", payload)

        return search_results.get("items", [])
        
    def search_and_decrypt(self, query: str = None, tags: list[str] = None, color_codes: list[int] = None, url: str = None,
                          vault_ids: list[str] = None, folder_ids: list[str] = None):
        # Get search results
        search_results = self.search_items(query, tags, color_codes, url, vault_ids, folder_ids)
        
        # Extract item IDs from search results
        item_ids = [item["id"] for item in search_results]

        # Get and decrypt detailed information for all items
        if item_ids:
            return self.get_items(item_ids)
        else:
            return []

    def download_item_attachment(self, item: dict, download_path: str):
        attachments = item.get("attachments")

        attachments_data = self.prepare_attachments_data(attachments, item.get("id"))
        if not attachments_data:
            return None

        encrypted_key = ''

        if self.is_encrypt:
            encrypted_key = get_encryption_key(
                item["vaultMasterKeyEncrypted"],
                item["keyEncrypted"],
                self.user_private_key
            )
        for attachment_data in attachments_data:
            decrypt_and_save_item_attachment(attachment_data, encrypted_key, download_path)

    def prepare_attachments_data(self, attachments: dict, item_id: str):
        attachments_data = []
        for attachment in attachments:
            attachments_data.append(self.get_item_attachment(item_id, attachment["id"]))

        if not attachments_data:
            return None

        return attachments_data

    def get_item_attachment(self, item_id: str, attachment_id: str):
        return self.call("GET", f"/api/v1/items/{item_id}/attachment/{attachment_id}")

    def decrypt_item(self, item_data: dict, encrypted_key: str):
        if "passwordEncrypted" in item_data and item_data["passwordEncrypted"]:
            item_data["password"] = decrypt_item(
                item_data["passwordEncrypted"],
                encrypted_key
            )

    def decrypt_item_customs(self, item_data: dict, encrypted_key: str):
        if "customs" in item_data and item_data["customs"]:
            for custom in item_data["customs"]:
                decrypt_item_customs(custom, encrypted_key)

    def encrypt_item(self, item_data: dict, vault_password: str):
        if "password" in item_data:
            item_data["passwordEncrypted"] = encrypt_aes(item_data["password"], vault_password)
            item_data.pop("password", None)

        item_data["keyEncrypted"] = encrypt_aes(vault_password, vault_password)

    def encrypt_item_customs(self, item_data: dict, vault_password: str):
        if "customs" in item_data and len(item_data["customs"]) > 0:
            validate_item_customs(item_data["customs"])
            item_data["customs"] = encrypt_item_customs(item_data["customs"], vault_password)

    def encrypt_item_attachments(self, item_data: dict, vault_password: str):
        if "attachments" in item_data and len(item_data["attachments"]) > 0:
            item_data["attachments"] = format_item_attachments(item_data["attachments"], vault_password)