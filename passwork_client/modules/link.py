from ..crypto import (generate_key, get_hash, encrypt_aes, decrypt_aes)
from ..utils import get_encryption_key
from ..enums.link_type_enum import LinkType
from ..enums.link_expiration_time_enum import LinkExpirationTime

class Link:

    def create_link(self, type: LinkType, expiration_time: LinkExpirationTime, item_id: str = None, shortcut_id: str = None):

        if shortcut_id:
            shortcut = self.get_shortcut(shortcut_id)
            item = shortcut["password"]
        else:
            item = self.get_item(item_id)

        item_data = {
            "name": item["name"],
            "login": item["login"],
            "url": item["url"],
            "description": item["description"],
        }

        code = None
        link_key_hash = None
        link_key_encrypted = None
        if self.is_encrypt:
            code = generate_key()
            encrypted_key = get_encryption_key(
                item["vaultMasterKeyEncrypted"],
                item["keyEncrypted"],
                self.user_private_key
            )

            link_key_hash = get_hash(code)
            link_key_encrypted = encrypt_aes(code, encrypted_key)
            self.encrypt_item(item, code)
            if "passwordEncrypted" in item:
                item_data["passwordEncrypted"] = item["passwordEncrypted"]

            if "attachments" in item and len(item["attachments"]) > 0:
                link_attachments = []
                for attachment in item.get("attachments"):
                    key = decrypt_aes(attachment["encryptedKey"], encrypted_key)
                    link_attachments.append({"id": attachment["id"], "name": attachment["name"], "encryptedKey": encrypt_aes(key, code)})

                item_data["attachments"] = link_attachments
        else:
            item_data["passwordEncrypted"] = item["passwordEncrypted"]
            item_data["attachments"] = item["attachments"]

        self.encrypt_item_customs(item, code)
        if "customs" in item and len(item["customs"]) > 0:
            item_data["customs"] = item["customs"]


        payload = {
            "itemId": item['id'],
            "itemData": item_data,
            "keyHash": link_key_hash,
            "keyEncrypted": link_key_encrypted,
            "type": type.value,
            "expirationTime" : expiration_time.value
        }

        if shortcut_id:
            payload["shortcutId"] = shortcut_id

        response = self.call("POST", "/api/v1/links", payload)

        url = response["url"]
        if code:
            url = url + f"#code={code}"
        return url
