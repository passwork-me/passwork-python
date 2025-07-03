# Passwork Client

A Python client for interacting with the Passwork password management API. It provides secure password storage, retrieval, and management with client-side encryption support.

## Installation

You can install the package directly from Github:

```bash
pip install git+ssh://git@github.com:passwork-me/passwork-python.git
```

Or using HTTPS:

```bash
pip install git+https://github.com/passwork-me/passwork-python.git
```

## Features

- Client-side encryption with master password support
- Automatic token refresh
- Encrypted session storage and restoration
- Multi-level encryption (PBKDF2, RSA, AES)
- Attachment handling
- User and role management
- Vault management
- Password sharing via inbox
- Custom fields support
- Tagging system
- Command-line interface (CLI) for password retrieval and direct API access
- Docker container for CI/CD pipelines

## Command-Line Interface (CLI)

The package includes a powerful CLI that allows you to:

```bash
# Retrieve a password and use it in a command
passwork-cli exec --password-id "db_password_id" mysql -u admin -h localhost -p$DB_PASSWORD database_name

# Search for passwords by tags and use them in a script
passwork-cli exec --tags "production,database" ./deploy.sh

# Make direct API calls
passwork-cli api --method GET --endpoint "v1/vaults"

# Refresh an expired token
passwork-cli api --refresh-token "your_refresh_token" --method POST --endpoint "v1/auth/refresh-token"
```

For detailed CLI documentation and examples, see the [CLI README](cli/README.md) and the [examples directory](examples_cli/).

## Docker Support

For CI/CD pipelines and containerized environments, a Docker image is provided:

```bash
# Pull the Docker image
docker pull passwork/passwork-cli:latest
docker tag passwork/passwork-cli:latest passwork-cli

# Or build it yourself
docker build -f docker/Dockerfile -t passwork-cli .

# Run a command using the container
docker run -it --rm \
  -e PASSWORK_HOST="https://your-passwork.com" \
  -e PASSWORK_TOKEN="your_token" \
  -e PASSWORK_MASTER_KEY="your_master_key" \
  passwork-cli exec --password-id "db_password_id" ./deploy.sh
```

### Using in Bitbucket Pipelines

```yaml
pipelines:
  default:
    - step:
        name: Deploy with Passwork credentials
        image: passwork-cli
        script:
          - passwork-cli exec --password-id "deploy_credentials" ./deploy.sh
```

For more Docker examples and configuration options, see the [Docker README](docker/README.md).

## Basic Usage

```python
from passwork_client import PassworkClient

# Initialize the client
client = PassworkClient(host="https://your-passwork-instance.com")
# To disable SSL certificate verification (e.g., for a self-signed certificate), initialize like this:
# client = PassworkClient(host="https://your-passwork-instance.com", verify_ssl=False)

# Login with a token
client.set_tokens("access-token")

# Set master password for encryption/decryption
client.set_master_password("your-master-password")

# Create a vault
vault_id = client.create_vault("My Vault")

# Create a password
password_data = {
    "vaultId": vault_id,
    "title": "My Password",
    "login": "username",
    "password": "secure-password",
    "url": "https://example.com"
}
password_id = client.create_password(password_data)

# Get a password
password = client.get_password(password_id)
```

## Advanced Usage

### Session Management

Save and restore sessions to avoid repeated authentication:

```python
# Save session to file (encrypted)
encryption_key = client.save_session("session.file", None, True)

# Later, load the session
client = PassworkClient("https://your-passwork-instance.com")
client.load_session("session.file", encryption_key)
```

### Password Management

Create passwords with custom fields, tags, and attachments:

```python
password = {
    "name": "Service Name",
    "login": "username",
    "password": "secure-password",
    "vaultId": vault_id,
    "folderId": folder_id,  # Optional
    "description": "Description text",
    "url": "https://service-url.com",
    "tags": ["tag1", "tag2"],
    "customs": [
        {
            "name": "Additional login",
            "value": "second-username",
            "type": "text"
        },
        {
            "name": "Recovery code",
            "value": "recovery-code-value",
            "type": "password"
        },
        {
            "name": "TOTP",
            "value": "JBSWY3DPEHPK3PXP",
            "type": "totp"
        }
    ],
    "attachments": [
        {
            "path": "path/to/file.png",
            "name": "file.png"
        }
    ]
}

password_id = client.create_password(password)
```

Update an existing password:

```python
update_data = {
    "login": "new-username",
    "password": "new-password",
    "vaultId": vault_id
}
client.update_password(password_id, update_data)
```

Delete a password:

```python
bin_item_id = client.delete_password(password_id)
```

### User Management

Create a new user:

```python
# Get available user roles
user_roles = client.get_user_roles({"includeUserRole": True, "isOnlyManageable": True})
user_role = [role for role in user_roles["items"] if role["code"] == "user"][0]

# Create user
user_data = {
    "login": "new_user",
    "userRoleId": user_role["id"],
    "userGroupIds": []
}
new_user = client.create_user(user_data)
# Returns user_id, password, and master_password
```

### Password Sharing

Share a password with another user via inbox:

```python
# Recipient can access the shared password
inbox_password = client.get_inbox_password(inbox_id)
```

### Direct API Calls

For operations not covered by helper methods:

```python
# Make a direct API call
response = client.call("DELETE", f"/api/v1/folders/{folder_id}")
```

## Requirements

- Python 3.10+
- requests>=2.31.0
- python-dotenv>=1.0.0
- cryptography>=42.0.0
- pbkdf2>=1.3

## Documentation

For more detailed examples, see the `examples` directory in the repository.

## License

MIT License

Copyright (c) 2025 Passwork

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
