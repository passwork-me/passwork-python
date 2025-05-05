# Making Direct API Calls

This example shows how to use the API command to make direct calls to the Passwork API and extract specific information.

## Use Case

You need to retrieve a list of all vaults in your Passwork account and extract just their names for a report.

## Command

```bash
# Set your Passwork credentials as environment variables
export PASSWORK_HOST="https://passwork.example.com"
export PASSWORK_TOKEN="your_access_token"

# Get all vaults and extract only their names
passwork-cli api \
  --method GET \
  --endpoint "v1/vaults" \
  --field "name"
```

## How It Works

1. Passwork CLI connects to the Passwork server using your credentials
2. It makes a direct GET request to the `/api/v1/vaults` endpoint (automatically prepending `/api/`)
3. The response contains complete details about all vaults
4. The `--field "name"` parameter extracts just the name field from each vault
5. The result is a JSON array of vault names

## Example Output

```json
[
  "Personal Passwords",
  "Work Credentials",
  "Server Access",
  "Client Projects"
]
```

