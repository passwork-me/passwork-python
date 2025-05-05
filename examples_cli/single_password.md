# Using a Single Password by ID

This example demonstrates how to retrieve a single password from Passwork by its ID and use it in a command.

## Use Case

You need to run a database backup script that requires a database password. The password is stored in Passwork with the name "PGPASSWORD", and you want to pass it securely to your script without saving the password in plain text anywhere.

## Command

```bash
passwork-cli exec \
  --host "https://passwork.example.com" \
  --token "your_access_token" \
  --master-key "your_master_key" \
  --password-id "5f8a7b6c9d0e1f2a3b4c5d6e" \
  pg_dump -h localhost -U username -d database > backup.sql
```

## How It Works

1. Passwork CLI connects to your Passwork server using the provided credentials
2. It retrieves the password with ID `5f8a7b6c9d0e1f2a3b4c5d6e`
3. The password is decrypted using your master key
4. Passwork CLI automatically creates an environment variable named `PGPASSWORD` (because that's the name of your password in Passwork)
5. The `pg_dump` command is executed, which automatically uses the `PGPASSWORD` environment variable



