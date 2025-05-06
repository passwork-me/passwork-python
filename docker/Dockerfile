FROM python:3.11-slim

LABEL maintainer="Passwork Team"
LABEL description="Passwork CLI Docker Image for CI/CD pipelines"

# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install passwork-cli
RUN pip install --no-cache-dir git+ssh://git@github.com:passwork-me/passwork-python.git

# Create a non-root user to run the CLI
RUN groupadd -r passwork && useradd -r -g passwork passwork
USER passwork

# Set the entrypoint to passwork-cli
ENTRYPOINT ["passwork-cli"]
CMD ["--help"] 