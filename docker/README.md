# Passwork CLI Docker Container

This directory contains Docker configuration for running Passwork CLI in a containerized environment, which is particularly useful for CI/CD pipelines in Bitbucket or other CI systems.

## Building the Docker Image

```bash
cd docker
docker build -t passwork-cli .
```

## Using the Docker Container

### Basic Usage

Run the container with your Passwork credentials as environment variables:

```bash
docker run -it --rm \
  -e PASSWORK_HOST="https://your-passwork-instance.com" \
  -e PASSWORK_TOKEN="your_access_token" \
  -e PASSWORK_MASTER_KEY="your_master_key" \
  passwork-cli exec --password-id "your_password_id" env
```

### Using Docker Compose

1. Create a docker-compose.yml file based on the example:

```bash
cp docker-compose.example.yml docker-compose.yml
# Edit docker-compose.yml if needed
```

2. Create a `.env` file based on the example:

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. Run with Docker Compose:

```bash
docker-compose run --rm passwork-cli exec --password-id "your_password_id" env
```

## Examples

### Retrieve a password and use it in a command

```bash
docker run -it --rm \
  -e PASSWORK_HOST="https://your-passwork.com" \
  -e PASSWORK_TOKEN="your_token" \
  -e PASSWORK_MASTER_KEY="your_master_key" \
  passwork-cli exec --password-id "db_password_id" mysql -h db_host -u admin -p$DB_PASSWORD db_name
```

### Make a direct API call

```bash
docker run -it --rm \
  -e PASSWORK_HOST="https://your-passwork.com" \
  -e PASSWORK_TOKEN="your_token" \
  passwork-cli api --method GET --endpoint "v1/vaults"
```

## Using in Bitbucket Pipelines

Add this to your `bitbucket-pipelines.yml`:

```yaml
pipelines:
  default:
    - step:
        name: Deploy with Passwork credentials
        image: passwork-cli
        script:
          - passwork-cli exec --password-id "deploy_credentials" ./deploy.sh
        services:
          - docker
        caches:
          - docker
```

You can also use the Docker image directly from a container registry if you push it there:

```yaml
pipelines:
  default:
    - step:
        name: Deploy with Passwork credentials
        image: your-registry.com/passwork-cli:latest
        script:
          - passwork-cli exec --password-id "deploy_credentials" ./deploy.sh
```

Don't forget to set up repository variables in Bitbucket:
- `PASSWORK_HOST`
- `PASSWORK_TOKEN`
- `PASSWORK_MASTER_KEY`

## Security Considerations

- The Docker image runs as a non-root user for improved security
- Always use secure environment variables in CI/CD pipelines for your credentials
- Consider using refresh tokens for long-running pipelines 