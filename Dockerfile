FROM python:3.12-slim AS base

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY config ./config

RUN pip install --no-cache-dir .

ENTRYPOINT ["production-style-service"]
CMD ["--config", "config/config.example.json"]
