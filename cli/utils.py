#!/usr/bin/env python3
import os
import urllib3
from passwork_client import PassworkClient

# Suppress SSL certificate verification warnings globally
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def get_client_from_args(args):
    """
    Initialize and configure a PassworkClient from command line arguments.
    
    Args:
        args (Namespace): Command line arguments
        
    Returns:
        PassworkClient: Initialized client
    """
    # Create the client with SSL verification option
    verify_ssl = not getattr(args, 'no_ssl_verify', False)
    client = PassworkClient(args.host, verify_ssl=verify_ssl)
    
    # Set tokens
    client.set_tokens(args.token, args.refresh_token)
    
    # Set master key if provided
    if args.master_key:
        client.set_master_key(args.master_key)
        
    return client

def get_value_from_args_or_env(args_value, env_var_name, required=False):
    """
    Get a value from command line arguments or environment variable.
    The environment variable name should already include the PASSWORK_ prefix.
    
    Args:
        args_value: Value from command line arguments
        env_var_name (str): Name of the environment variable (with prefix)
        required (bool): Whether the value is required
        
    Returns:
        str: The value from arguments or environment
        
    Raises:
        ValueError: If the value is required but not found
    """
    if args_value is not None:
        return args_value
        
    env_value = os.environ.get(env_var_name)
    if env_value:
        return env_value
        
    if required:
        raise ValueError(f"Required value not provided via arguments or environment variable {env_var_name}")
        
    return None 