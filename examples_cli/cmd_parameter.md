# Using the --cmd Parameter for Complex Commands

This example demonstrates when it's more convenient to use the `--cmd` parameter instead of the direct command syntax.

## Use Case

You need to run a complex script that includes special characters, redirections, or piping that might be interpreted by the shell before reaching Passwork CLI. In this example, you're connecting to a server using SSH with a password stored in Passwork.

## Command

```bash
passwork-cli exec \
  --host "https://passwork.example.com" \
  --token "your_access_token" \
  --master-key "your_master_key" \
  --password-id "server_password" \
  --cmd "sshpass -p $SERVER_PASSWORD ssh user@example.com 'find /var/logs -name \"*.log\" | grep \"error\" | xargs tail -n 100'"
```

## When to Use --cmd

The `--cmd` parameter is particularly useful in these scenarios:

1. Commands with complex shell syntax (pipes, redirections, multiple commands)
2. Commands that use quotes which would be difficult to escape in the direct syntax
3. When you want to utilize shell features like variable substitution within your command
4. For commands that would otherwise be interpreted by your shell before being passed to Passwork CLI

## How It Works

1. Passwork CLI connects to your Passwork server using the provided credentials
2. It retrieves the password with ID `server_password`
3. The password is decrypted using your master key
4. Passwork CLI creates an environment variable named `SERVER_PASSWORD` (from the password's name in Passwork)
5. The entire command string in `--cmd` is executed in a shell, with access to the environment variable 