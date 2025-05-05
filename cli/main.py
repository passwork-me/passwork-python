#!/usr/bin/env python3
import sys
import json
import argparse
import shlex
import os
import warnings
import urllib3

# Suppress SSL certificate verification warnings
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

from .commands import COMMAND_STRATEGIES
from .utils import get_client_from_args, get_value_from_args_or_env

class PassworkArgumentParser(argparse.ArgumentParser):
    """Custom argument parser that stops on first unrecognized argument."""
    def parse_known_args(self, args=None, namespace=None):
        # Parse only the known arguments, leave the rest for command
        return super().parse_known_args(args, namespace)

def main():
    """Main entry point for the Passwork CLI."""
    # Create the main parser
    parser = PassworkArgumentParser(
        description="Passwork CLI - Command line interface for Passwork password manager"
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest="command", help="Command mode")
    
    # 1. Execute command mode
    cmd_parser = subparsers.add_parser("exec", help="Execute a command with passwords as environment variables")
    # Common arguments for exec command
    cmd_parser.add_argument("--host", help="Passwork API host URL")
    cmd_parser.add_argument("--token", help="Passwork access token")
    cmd_parser.add_argument("--refresh-token", help="Passwork refresh token")
    cmd_parser.add_argument("--master-key", help="Passwork master key for decryption")
    cmd_parser.add_argument("--no-ssl-verify", action="store_true", help="Disable SSL certificate verification")
    # Password identification (one of these must be used)
    pwd_group = cmd_parser.add_argument_group("Password identification (at least one required)")
    pwd_group.add_argument("--password-id", help="ID of password(s) to retrieve (comma-separated for multiple)")
    pwd_group.add_argument("--shortcut-id", help="ID of shortcut(s) to retrieve (comma-separated for multiple)")
    pwd_group.add_argument("--vault-id", help="ID(s) of vault(s) to search in (comma-separated for multiple)")
    pwd_group.add_argument("--folder-id", help="ID(s) of folder(s) to search in (comma-separated for multiple)")
    pwd_group.add_argument("--tags", help="Tag(s) to search for (comma-separated for multiple)")
    cmd_parser.add_argument("--cmd", help="Command to execute")
    
    # 2. API Call mode
    api_parser = subparsers.add_parser("api", help="Make a direct API call to Passwork")
    # Common arguments for api command
    api_parser.add_argument("--host", help="Passwork API host URL")
    api_parser.add_argument("--token", help="Passwork access token")
    api_parser.add_argument("--refresh-token", help="Passwork refresh token")
    api_parser.add_argument("--master-key", help="Passwork master key for decryption")
    api_parser.add_argument("--no-ssl-verify", action="store_true", help="Disable SSL certificate verification")
    # API specific arguments
    api_parser.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE"], help="HTTP method")
    api_parser.add_argument("--endpoint", required=True, help="API endpoint (e.g. v1/items) without leading /api/")
    api_parser.add_argument("--params", help="JSON string of parameters to pass to the API call")
    api_parser.add_argument("--field", help="Field to extract from the API response")
    
    # Parse the arguments, but keep unknown ones as command to execute
    args, remaining = parser.parse_known_args()
    
    # Handle command for exec mode (Docker-like syntax)
    if args.command == "exec":
        if args.cmd and remaining:
            print("Error: Cannot use both --cmd and direct command at the same time", file=sys.stderr)
            sys.exit(1)
        elif remaining:
            # Join the remaining arguments as the command to execute
            args.cmd = " ".join(shlex.quote(arg) for arg in remaining)
        elif not args.cmd:
            print("Error: No command specified. Use --cmd or append command directly", file=sys.stderr)
            sys.exit(1)
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Get values from args or environment variables
        args.host = get_value_from_args_or_env(args.host, "PASSWORK_HOST", required=True)
        args.token = get_value_from_args_or_env(args.token, "PASSWORK_TOKEN", required=True)
        args.refresh_token = get_value_from_args_or_env(args.refresh_token, "PASSWORK_REFRESH_TOKEN", required=False)
        args.master_key = get_value_from_args_or_env(args.master_key, "PASSWORK_MASTER_KEY", required=False)
        
        # Initialize the client
        client = get_client_from_args(args)
        
        # Create the strategy based on the command
        strategy_class = COMMAND_STRATEGIES.get(args.command)
        if not strategy_class:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
            
        strategy = strategy_class()
        
        # Execute the strategy
        exit_code = strategy.execute(client, args)
        sys.exit(exit_code)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 