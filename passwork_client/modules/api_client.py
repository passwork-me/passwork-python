import requests
import base64
import json
import copy
from ..exceptions import PassworkError

class ApiClient:
    """
    Core API client functionality for making HTTP requests and processing responses.
    """
    def __init__(self):
        # No variable initialization here
        pass
        
    def call(self, method, endpoint, payload = None, headers = None):
        """
        Public method to send general api requests and handle responses.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            payload (dict): Data to send with the request
            headers (dict): Custom headers to include in the request
            
        For GET requests, payload is sent as query parameters with arrays formatted as 'param[]'.
        For other request types (POST, PUT, DELETE), payload is sent as JSON in the request body.
        """
        if payload is None:
            payload = {}
            
        kwargs = {}
        
        # Add custom headers if provided
        if headers:
            kwargs["headers"] = headers
        
        # Process parameters based on HTTP method
        if method.upper() == "GET":
            # For GET requests, convert payload to query parameters
            processed_params = {}
            
            for key, value in payload.items():
                # If it's a list/array, add [] to the key
                if isinstance(value, (list, tuple)):
                    processed_params[f"{key}[]"] = value
                else:
                    processed_params[key] = value
                    
            kwargs["params"] = processed_params
        else:
            # For non-GET requests, send payload as JSON in the body
            kwargs["json"] = payload
        
        return self._request(method, endpoint, **kwargs)
        
    def _process_response(self, response):
        """Process API response and handle errors."""
        data = response.json()
        result = {}
        
        if data:
            format = data.get("format", "")
            if format == "base64":
                content = base64.b64decode(data.get("content", "")).decode("utf-8")
                result = json.loads(content)
            else:
                result = data
                
        if response.status_code != 200:
            error_data = result.get("errors", [])
            if any(err.get("code") == "accessTokenExpired" for err in error_data):
                # Let the caller handle token expiration
                return {"_token_expired": True, "errors": error_data}
            
            error_messages = []
            for err in error_data:
                if "field" in err and err['field']:
                    message = f"{err['field']} => {err['message']}"
                else:
                    message = f"{err['message']}"
                error_messages.append(message)
            raise PassworkError(str(error_messages), f"api_error:{response.status_code}")
            
        response.raise_for_status()
        return result
        
    def _request(self, method, endpoint, **kwargs):
        """Helper method to send HTTP requests and handle responses."""
        url = f"{self.host}{endpoint}"
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if self.access_token:
            # Don't overwrite custom auth headers if provided
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = f"Bearer {self.access_token}"
        if self.master_key_hash:
            # Don't overwrite custom master key hash if provided
            if "X-Master-Key-Hash" not in kwargs["headers"]:
                kwargs["headers"]["X-Master-Key-Hash"] = self.master_key_hash
        
        verify_ssl = kwargs.pop("verify", self.verify_ssl)
        
        # For the actual request, add verify parameter
        kwargs["verify"] = verify_ssl
        response = requests.request(method, url, **kwargs)
        result = self._process_response(response)

        # Handle token expiration
        if isinstance(result, dict) and result.get("_token_expired"):
            # Check if auto refresh is enabled
            if self.auto_refresh:
                # Auto refresh is enabled, attempt to refresh the token
                self.update_tokens()
                # Update Authorization header with new token
                if "Authorization" not in kwargs["headers"] or kwargs["headers"]["Authorization"].startswith("Bearer "):
                    kwargs["headers"]["Authorization"] = f"Bearer {self.access_token}"
                if self.master_key_hash:
                    kwargs["headers"]["X-Master-Key-Hash"] = self.master_key_hash
                response = requests.request(method, url, **kwargs)
                result = self._process_response(response)

            else:
                # Auto refresh is disabled
                raise PassworkError("Access token expired", "token_expired")
            
        return result
    
    def set_tokens(self, access_token, refresh_token):
        """Set the API access and refresh tokens directly."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        
    def update_tokens(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise PassworkError("No refresh token available", "no_refresh_token")

        # Store current token to avoid recursion
        current_token = self.access_token
        refresh_token_copy = self.refresh_token
        
        # Temporarily remove tokens to prevent _request from trying to refresh again
        self.access_token = None
        self.refresh_token = None

        url = f"{self.host}/api/v1/sessions/refresh"
        headers = {"Authorization": f"Bearer {current_token}"}
        if hasattr(self, 'master_key_hash') and self.master_key_hash:
            headers["X-Master-Key-Hash"] = self.master_key_hash

        # Use requests directly since we're bypassing the normal API client flow
        response = requests.post(
            url,
            json = {"refreshToken": refresh_token_copy},
            headers = headers,
            verify = self.verify_ssl
        )

        # Process the response manually
        if response.status_code != 200:
            # Handle error
            raise PassworkError(f"Failed to refresh token: {response.status_code}", "refresh_token_failed")
        
        result = response.json()
        
        self.access_token = result["accessToken"]
        self.refresh_token = result["refreshToken"]
        
        if hasattr(self, 'session_path') and self.session_path and hasattr(self, 'save_session'):
            self.save_session(self.session_path, self.session_encryption_key)
            
        return result