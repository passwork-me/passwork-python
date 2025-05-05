# Working with Custom Fields

This example demonstrates how to access and use custom fields from Passwork passwords.

## Use Case

You have a database password in Passwork that includes not just the main password but also custom fields for the database hostname, port, username, and SSL certificate. You need to use all these fields to connect to the database.

## Command

```bash
# Set your Passwork credentials as environment variables
export PASSWORK_HOST="https://passwork.example.com"
export PASSWORK_TOKEN="your_access_token"
export PASSWORK_MASTER_KEY="your_master_key"

# Get the database password with its custom fields
passwork-cli exec \
  --password-id "db_prod_cluster" \
  mysql -h $DB_HOSTNAME -P $DB_PORT -u $DB_USERNAME -p$DB_PASSWORD --ssl-ca=$DB_CERTIFICATE -e 'SHOW DATABASES;'
```

## How It Works

1. Passwork CLI connects to the server and retrieves the password with ID "db_prod_cluster"
2. The password and all its custom fields are decrypted
3. Environment variables are created for:
   - `DB_PASSWORD` (from the main password)
   - `DB_HOSTNAME` (from a custom field named "Hostname")
   - `DB_PORT` (from a custom field named "Port")
   - `DB_USERNAME` (from a custom field named "Username")
   - `DB_CERTIFICATE` (from a custom field named "Certificate")
4. The MySQL command is executed with all these environment variables
