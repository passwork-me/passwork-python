# Passwork CLI Tool

Command-line interface for retrieving passwords from Passwork password manager and using them securely in your scripts and commands.

## Installation

```bash
pip install git+ssh://git@github.com:passwork-me/passwork-python.git
```

Or using HTTPS:

```bash
pip install git+https://github.com/passwork-me/passwork-python.git
```

## Overview

Passwork CLI operates in two main modes:

1. **exec** - Retrieves passwords from Passwork, adds them to environment variables, and runs a specified command with access to these variables.
2. **api** - Provides direct access to the Passwork API, allowing you to execute any API methods and receive responses in JSON format.

## Common Arguments

All commands support the following arguments:

| Argument | Environment Variable | Description |
|----------|----------------------|-------------|
| `--host` | `PASSWORK_HOST` | Passwork server URL |
| `--token` | `PASSWORK_TOKEN` | API access token |
| `--refresh-token` | `PASSWORK_REFRESH_TOKEN` | Refresh token (optional) |
| `--master-key` | `PASSWORK_MASTER_KEY` | Master key for decryption |
| `--no-ssl-verify` | - | Disable SSL certificate verification (use with caution) |

## 1. Execute Mode (exec)

Retrieves passwords from Passwork, decrypts them, adds them to environment variables, and runs the specified command with access to these variables.

### Syntax

```bash
passwork-cli exec [options] command_to_execute
```

Or using the `--cmd` parameter:

```bash
passwork-cli exec [options] --cmd "command_to_execute"
```

### Password Identification

For the `exec` command, you must specify at least one of the following parameters:

| Argument | Description |
|----------|-------------|
| `--password-id` | ID of a password or passwords (comma-separated for multiple) |
| `--vault-id` | ID of a vault or vaults (comma-separated for multiple) |
| `--folder-id` | ID of a folder or folders (comma-separated for multiple) |
| `--tags` | Tags for searching passwords (comma-separated for multiple) |

### How It Works

1. **Authentication**: Connects to the Passwork server using the provided credentials
2. **Password Retrieval**: Searches for passwords based on the specified criteria (ID, vault, folder, or tags)
3. **Decryption**: Decrypts the retrieved passwords using the master key
4. **Environment Setup**: Creates environment variables from:
   - The main password value (named after the password entry name)
   - All custom fields in the password entry
5. **Command Execution**: Runs the specified command in a new process with access to these environment variables

### Features

- **Multiple Password Support**: Can retrieve and use multiple passwords in a single command
- **Custom Field Access**: All custom fields of a password entry are available as environment variables
- **Variable Naming**: Password names are converted to uppercase, spaces and special characters are replaced with underscores
- **Docker-like Syntax**: Command can be specified directly after the CLI arguments, similar to `docker exec`
- **Return Code Preservation**: The exit code of your command is preserved and returned by the CLI

### Typical Use Cases

- **Database Access**: Connect to databases without storing passwords in configuration files
- **API Authentication**: Run scripts that require API keys or tokens
- **Deployment Scripts**: Execute deployment scripts with access to credentials for multiple services
- **Server Administration**: Perform administrative tasks requiring privileged access
- **CI/CD Pipeline**: Securely pass credentials to automated processes

### Usage Examples

#### Basic Password Retrieval and Command Execution

```bash
# Using environment variables for credentials and direct command syntax
export PASSWORK_HOST="https://passwork.example.com"
export PASSWORK_TOKEN="your_token"
export PASSWORK_MASTER_KEY="your_master_key"

# Retrieve password by ID and run MySQL client
passwork-cli exec --password-id "db_password_id" mysql -u admin -h localhost -p$DB_PASSWORD database_name
```

#### Using Multiple Passwords from a Folder

```bash
# Retrieve all passwords from a project folder and run deployment script
passwork-cli exec --folder-id "project_folder_id" ./deploy.sh
```

#### Using Multiple Passwords with Different Identifiers

```bash
# Retrieve passwords by multiple criteria
passwork-cli exec \
  --password-id "specific_password_id" \
  --tags "production,database" \
  --folder-id "api_credentials" \
  ./complex_deployment.sh
```

#### Commands with Complex Shell Syntax

```bash
# For commands with pipes, redirections, or shell functions, use --cmd
passwork-cli exec --password-id "server_creds" --cmd "ssh user@server 'cat /var/log/app.log | grep ERROR' > local_errors.log"
```

#### Connecting to a Server with Self-Signed Certificate

```bash
# Disable SSL verification for development or testing environments
passwork-cli exec --no-ssl-verify --password-id "test_server_password" ssh user@test-server.local
```

## 2. API Mode (api)

Provides direct access to the Passwork API, allowing you to execute any backend API methods and receive responses in JSON format.

### Syntax

```bash
passwork-cli api [options]
```

### API Arguments

The `api` command requires the following arguments:

| Argument | Description |
|----------|-------------|
| `--method` | HTTP method (GET, POST, PUT, DELETE) |
| `--endpoint` | API endpoint (e.g., v1/vaults) |
| `--params` | JSON string of parameters (optional) |
| `--field` | Field to extract from the response (optional) |

### How It Works

1. **Authentication**: Connects to the Passwork server using the provided credentials
2. **Request Formation**: Creates an HTTP request to the specified API endpoint with the selected method
3. **Request Sending**: Sends the request to the server with the necessary authentication headers
4. **Response Processing**: Receives and processes the API response
5. **Filtering (optional)**: If the `--field` parameter is specified, extracts only that field from the response
6. **Result Output**: Outputs the result in JSON format

### Usage Examples

#### Getting a List of All Vaults

```bash
passwork-cli api --method GET --endpoint "v1/vaults"
```

#### Getting a Specific Password and Extracting Only Its Name

```bash
passwork-cli api --method GET --endpoint "v1/items/password_id" --field "name"
```

#### Searching for Passwords by Tag and Extracting Only Their Names

```bash
passwork-cli api \
  --method GET \
  --endpoint "v1/items/search" \
  --params '{"tags":["api","production"]}' \
  --field "name"
```

#### Refreshing an Access Token

```bash
passwork-cli api \
  --host "https://passwork.example.com" \
  --token "your_expired_token" \
  --refresh-token "your_refresh_token" \
  --method POST \
  --endpoint "v1/auth/refresh-token" \
  --field "token"
```

#### Using with Self-Signed Certificate

```bash
# Disable SSL verification for a development Passwork instance
passwork-cli api --no-ssl-verify --method GET --endpoint "v1/user/profile"
```

## Security Considerations

- Credentials are never saved to disk
- Commands with passwords are not stored in shell history
- Passwords are only available in the environment of the executed command
- It is recommended to use environment variables for storing Passwork credentials
- The `--no-ssl-verify` flag should only be used in development environments with self-signed certificates

## Detailed Examples

For detailed examples of various use cases, see the [examples directory](../examples_cli/):

- [Using a Single Password](../examples_cli/single_password.md)
- [Using Multiple Passwords](../examples_cli/multiple_passwords.md)
- [Finding Passwords by Tags](../examples_cli/search_by_tags.md)
- [Making Direct API Calls](../examples_cli/direct_api_call.md)
- [Working with Custom Fields](../examples_cli/custom_fields.md)
- [Using the --cmd Parameter](../examples_cli/cmd_parameter.md)
- [Retrieving Passwords from a Folder](../examples_cli/folder_search.md)
- [Refreshing Your Access Token](../examples_cli/refresh_token.md)
