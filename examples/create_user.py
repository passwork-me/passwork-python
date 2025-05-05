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


# Example: Create user 
try:
    # Fetch available user roles
    roles_response = passwork.call("GET", "/api/v1/user-roles", {"includeUserRole": '1', "isOnlyManageable": '1'})
    if not roles_response or not roles_response.get("items"):
        print("Error: Could not fetch user roles or no manageable roles found.")
        exit(1)

    # Find the 'user' role (adjust if needed)
    user_role_items = [r for r in roles_response["items"] if r.get("code") == "user"]
    if not user_role_items:
        print("Error: Default 'user' role not found.")
        exit(1)
    default_user_role_id = user_role_items[0]["id"]
    
    # Define user data
    user_data = {
        "email": "test_user_python@example.com",
        "fullName": "Python Test User",
        "login": "python_test_user",
        "userRoleId": default_user_role_id,
        # "userGroupIds": [], 
    }
    
    # Create the user
    new_user = passwork.create_user(user_data)

    # Construct the success message
    message = f"User '{user_data['fullName']}' created with ID: {new_user['user_id']}"
    if 'password' in new_user and new_user['password']:
         message += f", password: {new_user['password']}"
    if 'master_password' in new_user and new_user['master_password']:
        message += f", master password: {new_user['master_password']}"

    print(message)

except Exception as e:
    print(f"Error: {e}") 