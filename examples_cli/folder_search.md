# Retrieving Passwords from a Specific Folder

Before using this example, you need to organize your passwords in Passwork by creating a folder for your project and placing all related secrets in it. For instance, create a folder named "Project X" and add all database passwords, API keys, and other credentials needed for this project.

## Use Case

You're deploying an application that requires access to multiple credentials stored in the same Passwork folder. All necessary credentials for this project are organized in a single folder.

## Command

```bash
# Set your Passwork credentials as environment variables
export PASSWORK_HOST="https://passwork.example.com"
export PASSWORK_TOKEN="your_access_token"
export PASSWORK_MASTER_KEY="your_master_key"

# Get all passwords from a specific folder and run your deployment script
passwork-cli exec --folder-id "folder123" ./deploy_project.sh
```

## Alternate Command (using --cmd parameter)

```bash
passwork-cli exec \
  --host "https://passwork.example.com" \
  --token "your_access_token" \
  --master-key "your_master_key" \
  --folder-id "folder123" \
  --cmd "./deploy_project.sh"
```

## How It Works

1. Passwork CLI connects to your Passwork server using the provided credentials
2. It searches for all passwords in the folder with ID `folder123`
3. All passwords are retrieved and decrypted using your master key
4. For each password, an environment variable is created using the password name
5. Your deployment script runs with access to all the environment variables

## Getting the Folder ID

To find the ID of your folder:

1. In Passwork web interface, navigate to the folder
2. The folder ID is visible in the URL in your browser:
   `https://passwork.example.com/#/folder/folder123/passwords`
   
   In this example, `folder123` is your folder ID. 