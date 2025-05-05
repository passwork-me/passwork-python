from ..crypto import generate_user_password, get_master_key, get_hash, generate_rsa_keys

class User:
    def get_user_public_key(self, user_id: str):
        response = self.call("GET", f"/api/v1/users/{user_id}/public-key")

        return response["publicKey"]

    def create_user(self, user_data: dict):
        settings = self.call("GET", "/api/v1/app/settings")
        authPasswordComplexity = settings["authPasswordComplexity"] if settings.get("authPasswordComplexity") else {}
        user_data["password"] = generate_user_password(12, authPasswordComplexity)
        master_password = ""
        if self.is_encrypt:
            masterPasswordComplexity = settings["masterPasswordComplexity"] if settings.get("masterPasswordComplexity") else {}
            master_password = generate_user_password(12, masterPasswordComplexity)
            master_key_options = self.get_user_master_key_new_options()

            master_key_data = get_master_key(master_key_options, master_password)
            master_key = master_key_data["hashedString"]

            user_data["masterKeyHash"] = get_hash(master_key)
            user_data["masterKeyOptions"] = master_key_data["masterKeyOptions"]
            user_data["keys"] = generate_rsa_keys(master_password)

        response = self.call("POST", "/api/v1/users", user_data)

        return {"user_id": response["id"], "password": user_data["password"], "master_password": master_password}

    def get_user_master_key_new_options(self):
        return self.call("GET", "/api/v1/users/master-key/new-options")
