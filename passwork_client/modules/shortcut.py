from ..crypto import encrypt_aes, decrypt_aes
from ..utils import get_encryption_key, decrypt_and_save_item_attachment

class Shortcut:
    """
    A client for interacting with the Passwork Shortcut API.
    All methods in this class are related to shortcut management functionality.
    """
    def create_shortcut(self, password_id: str, vault_id: str, folder_id: str | None = None):
        password = self.get_item(password_id)

        encrypted_key = None
        if self.is_encrypt:
            password_encrypted_key = get_encryption_key(
                password["vaultMasterKeyEncrypted"],
                password["keyEncrypted"],
                self.user_private_key
            )
            vault = self.get_vault(vault_id)
            vault_password = self.get_vault_password(vault)
            encrypted_key = encrypt_aes(password_encrypted_key, vault_password)

        shortcut = {
            "vaultId": vault_id,
            "folderId": folder_id,
            "itemId": password_id,
            "keyEncrypted": encrypted_key
        }

        response = self.call("POST", "/api/v1/shortcuts", shortcut)

        return response["id"]

    def get_shortcut(self, shortcut_id: str):
        shortcut = self.call("GET", f"/api/v1/shortcuts/{shortcut_id}")
        shortcut["password"] = self.get_item(shortcut["id"])
        return shortcut

    def download_shortcut_attachment(self, shortcut, download_path):
        password = shortcut["password"]
        return self.download_item_attachment(password, download_path)

    def search_shortcut(self, query: str = None, tags: list[str] = None, color_codes: list[int] = None, url: str = None,
                       vault_ids: list[str] = None, folder_ids: list[str] = None):
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
        search_results = self.call("GET", "/api/v1/shortcuts/search", payload)
        return search_results.get("items", [])

    def search_and_decrypt_shortcut(self, query: str = None, tags: list[str] = None, color_codes: list[int] = None, url: str = None,
                                    vault_ids: list[str] = None, folder_ids: list[str] = None):
        search_results = self.search_shortcut(query, tags, color_codes, url, vault_ids, folder_ids)

        # Extract item IDs from search results
        item_ids = [item["shortcut"]["id"] for item in search_results]

        # Get and decrypt detailed information for all items
        if item_ids:
            return self.get_shortcut_items(item_ids)
        else:
            return []

    def get_shortcut_items(self, item_ids: list[str]):

        if not item_ids:
            return []

        requests = []
        for id in item_ids:
            requests.append({
                "method": "GET",
                "relativeUrl": f"/api/v1/shortcuts/{id}",
            })

        shortcuts = self.send_batch(requests)

        # Process each item in the response
        decrypted_items = {}
        for shortcut in shortcuts:
            decrypted_items[shortcut["id"]] = shortcut

        items = self.get_items(decrypted_items.keys())
        for item in items:
            decrypted_items[item["id"]]["password"] = item

        return list(decrypted_items.values())