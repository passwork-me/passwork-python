#!/usr/bin/env python3
import sys
import json
from .base import PassworkCommand

class ApiCallStrategy(PassworkCommand):
    """
    Strategy for making direct API calls to the Passwork API.
    """
    def execute(self, client, args):
        try:
            # Parse the parameters if provided
            payload = {}
            if args.params:
                try:
                    payload = json.loads(args.params)
                except json.JSONDecodeError as e:
                    print(f"Error parsing parameters JSON: {e}", file=sys.stderr)
                    return 1
            
            # Format the endpoint correctly (add /api/ prefix)
            endpoint = args.endpoint
            # Remove leading slash if present
            if endpoint.startswith('/'):
                endpoint = endpoint[1:]
            # Add /api/ prefix
            endpoint = f"/api/{endpoint}"

            # Execute the API call using the updated call method
            response = client.call(
                method=args.method,
                endpoint=endpoint,
                payload=payload
            )
            
            # Extract field from response if specified
            if args.field:
                extracted_data = self._extract_field(response, args.field)
                # Print the extracted data
                print(json.dumps(extracted_data, indent=2))
            else:
                # Print the full response as JSON
                print(json.dumps(response, indent=2))
                
            return 0
            
        except Exception as e:
            print(f"Error making API call: {e}", file=sys.stderr)
            return 1
    
    def _extract_field(self, data, field_name):
        """
        Extract a specific field from the API response.
        If the response is an array, extract the field from each item.
        
        Args:
            data: The API response data (dict or list)
            field_name: Name of the field to extract
            
        Returns:
            The extracted field value or list of values
        """
        # If data is a list, extract field from each item
        if isinstance(data, list):
            result = []
            for item in data:
                if isinstance(item, dict) and field_name in item:
                    result.append(item[field_name])
            return result
        
        # If data is a dict, extract the field
        elif isinstance(data, dict):
            # Handle nested fields using dot notation (e.g., "user.name")
            if "." in field_name:
                parts = field_name.split(".", 1)  # Split into first part and rest
                if parts[0] in data and isinstance(data[parts[0]], (dict, list)):
                    return self._extract_field(data[parts[0]], parts[1])
                return None
            
            # Handle extracting from a nested array using brackets (e.g., "items[0]")
            elif "[" in field_name and field_name.endswith("]"):
                base_name, index_str = field_name.split("[", 1)
                index = int(index_str[:-1])  # Remove the closing bracket and convert to int
                
                if base_name in data and isinstance(data[base_name], list) and 0 <= index < len(data[base_name]):
                    return data[base_name][index]
                return None
            
            # Simple field extraction
            elif field_name in data:
                return data[field_name]
        
        # Field not found or data type not supported
        return None 