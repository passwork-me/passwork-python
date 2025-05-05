# Using Multiple Passwords in a Single Command

This example shows how to retrieve multiple passwords from Passwork and use them all in a single command.

## Use Case

You need to run a deployment script that requires access to multiple services - a database, an API, and a cloud storage service. Each service has its own credentials stored in Passwork.

## Command

```bash
passwork-cli exec \
  --host "https://passwork.example.com" \
  --token "your_access_token" \
  --master-key "your_master_key" \
  --password-id "db123,api456,storage789" \
  deploy.sh --db-pass=$DATABASE_PASSWORD --api-key=$API_KEY --storage-key=$STORAGE_KEY
```

## How It Works

1. Passwork CLI connects to your Passwork server using the provided credentials
2. It retrieves the three passwords with IDs `db123`, `api456`, and `storage789`
3. Each password is decrypted using your master key
4. Environment variables are created based on the password names:
   - `DATABASE_PASSWORD` (from the name of password `db123`)
   - `API_KEY` (from the name of password `api456`)
   - `STORAGE_KEY` (from the name of password `storage789`)
5. The deployment script is executed with these environment variables
