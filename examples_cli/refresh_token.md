# Refreshing Your Access Token

This example demonstrates how to refresh your Passwork API access token when it expires.

## Use Case

Access tokens in Passwork have a limited lifetime. When they expire, you need to refresh them using your refresh token to obtain a new valid access token without having to log in again.

## Command

```bash
# Using the api command to refresh your token
passwork-cli api \
  --host "https://passwork.example.com" \
  --token "your_expired_token" \
  --refresh-token "your_refresh_token" \
  --method POST \
  --endpoint "v1/sessions/refresh"
```

## How It Works

1. Passwork CLI connects to your Passwork server
2. It sends a POST request to the refresh token endpoint
3. The server validates your refresh token
4. If valid, the server returns a new access token and refresh token as JSON

## Example Response

The API returns a JSON response containing both the new access token and refresh token:

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refreshToken": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.8sMVAOAiZUYJXGGQE_DvkEjgpaM1M-q0t8AjRqLSNAyKiKL3ykQni6GxCEzYRf0Y"
}
```

## Parsing the Tokens in Scripts

### Using jq (JSON processor)

If you have jq installed, it's easy to parse the JSON response:

```bash
#!/bin/bash

# Get the token response
RESPONSE=$(passwork-cli api \
  --host "https://passwork.example.com" \
  --token "your_expired_token" \
  --refresh-token "your_refresh_token" \
  --method POST \
  --endpoint "v1/sessions/refresh")

# Extract the tokens using jq
NEW_ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.accessToken')
NEW_REFRESH_TOKEN=$(echo $RESPONSE | jq -r '.refreshToken')

```
