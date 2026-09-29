"""Configuration loading utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


class ConfigError(Exception):
    """Raised when a configuration file cannot be loaded or is invalid."""


@dataclass(frozen=True)
class ServiceConfig:
    """Typed, validated service configuration fields."""

    port: int
    host: str
    enable_logging: bool


REQUIRED_FIELDS: dict[str, type] = {
    "port": int,
    "host": str,
    "enable_logging": bool,
}


def _validate_field(data: dict[str, Any], key: str, expected_type: type) -> str | None:
    """Return an error message for this field, or None if it is valid."""
    if key not in data:
        return f"Missing required config field: {key!r}"

    value = data[key]
    # bool is a subclass of int, so exclude it explicitly when an int is expected
    if expected_type is int and isinstance(value, bool):
        return f"Config field {key!r} must be an int, got bool"
    if not isinstance(value, expected_type):
        article = "an" if expected_type.__name__[0].lower() in "aeiou" else "a"
        return (
            f"Config field {key!r} must be {article} {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )
    return None


def _validate_port_format(value: int) -> str | None:
    if not 1 <= value <= 65535:
        return f"Config field 'port' must be between 1 and 65535, got {value}"
    return None


def _validate_host_format(value: str) -> str | None:
    if not value.strip():
        return "Config field 'host' must not be empty"
    if any(ch.isspace() for ch in value):
        return f"Config field 'host' must not contain whitespace, got {value!r}"
    return None


FORMAT_VALIDATORS: dict[str, Callable[[Any], str | None]] = {
    "port": _validate_port_format,
    "host": _validate_host_format,
}


def parse_service_config(data: dict[str, Any]) -> ServiceConfig:
    """Extract and validate the known required fields from a raw config dict.

    Raises:
        ConfigError: listing every missing, mistyped, or malformed required field.
    """
    errors: list[str] = []
    for key, expected_type in REQUIRED_FIELDS.items():
        type_error = _validate_field(data, key, expected_type)
        if type_error is not None:
            errors.append(type_error)
            continue

        validate_format = FORMAT_VALIDATORS.get(key)
        if validate_format is not None:
            format_error = validate_format(data[key])
            if format_error is not None:
                errors.append(format_error)

    if errors:
        raise ConfigError("Invalid config: " + "; ".join(errors))

    return ServiceConfig(
        port=data["port"],
        host=data["host"],
        enable_logging=data["enable_logging"],
    )


def load_config(path: str | Path) -> dict[str, Any]:
    """Load and parse a JSON configuration file.

    Raises:
        ConfigError: if the file is missing, unreadable, or not valid JSON.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        raw = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Could not read config file {config_path}: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"Config root must be a JSON object in {config_path}")

    return data
