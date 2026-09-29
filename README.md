# production-style-service

Python service skeleton with a `src` layout, JSON config loading, logging setup, tests, and Docker support.

## Structure

```
src/production_style_service/
    __init__.py
    config.py      # JSON config loading
    logging_config.py
    main.py        # entry point / CLI
config/
    config.example.json
tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
production-style-service --config config/config.example.json
```

## Test & lint

```bash
pytest
ruff check .
```

## Docker

```bash
docker build -t production-style-service .
docker run --rm production-style-service
```
