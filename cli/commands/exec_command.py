#!/usr/bin/env python3
import os
import re
import sys
import json
import subprocess
from .base import PassworkCommand

class ExecuteCommandStrategy(PassworkCommand):
    """
    Strategy for retrieving passwords and executing a command with them
    as environment variables.
    
    Supports:
    1. Single password by ID
    2. Multiple passwords by IDs
    3. Password search by vault ID, folder ID, or tags
    """
    def execute(self, client, args):
        try:
            # Get passwords based on provided parameters
            passwords = self._get_passwords(client, args)
            
            if not passwords:
                print("Error: No passwords found", file=sys.stderr)
                return 1
            
            # Set up environment with passwords
            env = os.environ.copy()
            
            # Add each password to environment variables
            for password_item in passwords:
                # Use sanitized password name as environment variable name
                env_var_name = self._sanitize_env_var_name(password_item.get("name", "PASSWORD"))

                item = password_item
                if "password" in password_item and type(password_item["password"]) is dict:
                    item = password_item["password"]

                # Set password as environment variable
                if "password" in item:
                    env[env_var_name] = item["password"]

                # Process custom fields of type "text" or "password"
                if "customs" in item and item["customs"]:
                    for custom in item["customs"]:
                        if custom.get("type") in ["text", "password"] and "name" in custom and "value" in custom:
                            # Sanitize custom field name to make a valid environment variable
                            custom_env_var = self._sanitize_env_var_name(custom["name"])
                            env[custom_env_var] = custom["value"]

            # Execute the command
            process = subprocess.run(args.cmd, shell=True, env=env)

            return process.returncode
            
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            return 1
    
    def _get_passwords(self, client, args):
        """
        Get passwords based on the provided arguments.
        
        Strategy:
        1. If password_id is provided, get a single password or multiple (if comma-separated)
        2. If search parameters are provided, search for passwords
        
        Returns:
            list: List of password objects
        """
        # Case 1: Password ID(s)
        if hasattr(args, 'password_id') and args.password_id:
            # Trim the parameter
            password_id = args.password_id.strip()
            if not password_id:
                return []
                
            # Check if it contains multiple IDs (comma-separated)
            if ',' in password_id:
                # Split by comma, clean each value and filter out empty ones
                id_list = [id.strip() for id in password_id.split(',')]
                id_list = [id for id in id_list if id]
                
                if not id_list:
                    return []
                    
                # If we have multiple IDs, get all of them
                if len(id_list) > 1:
                    return client.get_items(id_list)
                # If we only have one ID after cleaning, use it as a single ID
                else:
                    password = client.get_item(id_list[0])
                    return [password] if password else []
            
            # Single ID
            password = client.get_item(password_id)
            return [password] if password else []

        # Case 1: Shortcut ID(s)
        if hasattr(args, 'shortcut_id') and args.shortcut_id:
            # Trim the parameter
            shortcut_id = args.shortcut_id.strip()
            if not shortcut_id:
                return []

            # Check if it contains multiple IDs (comma-separated)
            if ',' in shortcut_id:
                # Split by comma, clean each value and filter out empty ones
                id_list = [id.strip() for id in shortcut_id.split(',')]
                id_list = [id for id in id_list if id]

                if not id_list:
                    return []

                # If we have multiple IDs, get all of them
                if len(id_list) > 1:
                    return client.get_shortcut_items(id_list)
                # If we only have one ID after cleaning, use it as a single ID
                else:
                    shortcut = client.get_shortcut(id_list[0])
                    return [shortcut] if shortcut else []

            # Single ID
            shortcut = client.get_shortcut(shortcut_id)
            return [shortcut] if shortcut else []
        
        # Case 2: Search parameters
        search_params = {}
        
        # Check if any search parameter is provided and process it
        # Vault IDs
        if hasattr(args, 'vault_id') and args.vault_id:
            # Trim and validate
            vault_id = args.vault_id.strip()
            if vault_id:
                # Process as list if contains commas
                if ',' in vault_id:
                    values = [item.strip() for item in vault_id.split(',')]
                    values = [item for item in values if item]
                    if values:
                        search_params['vault_ids'] = values
                else:
                    search_params['vault_ids'] = [vault_id]
        
        # Folder IDs
        if hasattr(args, 'folder_id') and args.folder_id:
            # Trim and validate
            folder_id = args.folder_id.strip()
            if folder_id:
                # Process as list if contains commas
                if ',' in folder_id:
                    values = [item.strip() for item in folder_id.split(',')]
                    values = [item for item in values if item]
                    if values:
                        search_params['folder_ids'] = values
                else:
                    search_params['folder_ids'] = [folder_id]
            
        # Tags
        if hasattr(args, 'tags') and args.tags:
            # Trim and validate
            tags = args.tags.strip()
            if tags:
                # Process as list if contains commas
                if ',' in tags:
                    values = [item.strip() for item in tags.split(',')]
                    values = [item for item in values if item]
                    if values:
                        search_params['tags'] = values
                else:
                    search_params['tags'] = [tags]
        
        # If no search parameters, throw error
        if not search_params:
            raise ValueError("No password ID or search criteria provided")
            
        # Search and decrypt
        items = client.search_and_decrypt(**search_params)
        items.extend(client.search_and_decrypt_shortcut(**search_params))
        return items
    
    def _sanitize_env_var_name(self, name):
        """
        Sanitize a name to make it a valid environment variable name.
        
        Rules:
        1. Replace non-alphanumeric with underscore
        2. Ensure starts with a letter
        3. Convert to uppercase
        
        Args:
            name (str): Original name
            
        Returns:
            str: Sanitized environment variable name
        """
        # Replace non-alphanumeric with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9]', '_', name)
        
        # Ensure starts with a letter
        if not sanitized[0].isalpha():
            sanitized = 'P_' + sanitized
            
        return sanitized