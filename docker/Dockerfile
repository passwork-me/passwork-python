FROM python:3.11-slim AS builder
WORKDIR /app
COPY . .
RUN pip install --prefix=/install --no-cache-dir .

FROM python:3.11-slim
LABEL maintainer="Passwork Team"
LABEL description="Passwork CLI Docker Image for CI/CD pipelines"

COPY --from=builder /install /usr/local

RUN groupadd -r passwork --gid=1001 && \
  useradd -r -g passwork --uid=1001 passwork

USER passwork
ENTRYPOINT ["passwork-cli"]
CMD ["--help"]
