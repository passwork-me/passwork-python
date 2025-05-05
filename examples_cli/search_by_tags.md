# Finding Passwords by Tags

This example demonstrates how to retrieve passwords using tags instead of specific IDs.

## Use Case

You need to deploy an application to your production environment, which requires multiple passwords from your production database servers. All these passwords are tagged with "production" and "database" in your Passwork vault.

## Command

```bash
# Set your Passwork credentials as environment variables to avoid typing them each time
export PASSWORK_HOST="https://passwork.example.com"
export PASSWORK_TOKEN="your_access_token"
export PASSWORK_MASTER_KEY="your_master_key"

# Now use tags to find all production database passwords
passwork-cli exec --tags "production,database" ./deploy_production.sh
```

## How It Works

1. Passwork CLI connects to the server using credentials from environment variables
2. It searches for all passwords tagged with both "production" AND "database"
3. All matching passwords are retrieved and decrypted
4. For each password, an environment variable is created using the password name
5. The `deploy_production.sh` script runs with access to all these environment variables

