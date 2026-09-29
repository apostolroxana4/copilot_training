import json

import pytest

from production_style_service.config import (
    ConfigError,
    ServiceConfig,
    load_config,
    parse_service_config,
)


def test_load_config_valid(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"key": "value"}))

    config = load_config(config_path)

    assert config == {"key": "value"}


def test_load_config_missing_file(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path / "missing.json")


def test_load_config_invalid_json(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{not valid json")

    with pytest.raises(ConfigError, match="Invalid JSON"):
        load_config(config_path)


def test_load_config_non_object_root(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps([1, 2, 3]))

    with pytest.raises(ConfigError, match="must be a JSON object"):
        load_config(config_path)


def test_parse_service_config_valid():
    data = {"port": 8080, "host": "0.0.0.0", "enable_logging": True}

    config = parse_service_config(data)

    assert config == ServiceConfig(port=8080, host="0.0.0.0", enable_logging=True)


def test_parse_service_config_missing_field():
    data = {"port": 8080, "host": "0.0.0.0"}

    with pytest.raises(ConfigError, match="Missing required config field: 'enable_logging'"):
        parse_service_config(data)


def test_parse_service_config_missing_multiple_fields():
    with pytest.raises(ConfigError) as exc_info:
        parse_service_config({})

    message = str(exc_info.value)
    assert "'port'" in message
    assert "'host'" in message
    assert "'enable_logging'" in message


def test_parse_service_config_wrong_type():
    data = {"port": "8080", "host": "0.0.0.0", "enable_logging": True}

    with pytest.raises(ConfigError, match="'port' must be an int"):
        parse_service_config(data)


def test_parse_service_config_port_out_of_range():
    data = {"port": 70000, "host": "0.0.0.0", "enable_logging": True}

    with pytest.raises(ConfigError, match="'port' must be between 1 and 65535"):
        parse_service_config(data)


def test_parse_service_config_empty_host():
    data = {"port": 8080, "host": "   ", "enable_logging": True}

    with pytest.raises(ConfigError, match="'host' must not be empty"):
        parse_service_config(data)


def test_parse_service_config_host_with_whitespace():
    data = {"port": 8080, "host": "bad host", "enable_logging": True}

    with pytest.raises(ConfigError, match="'host' must not contain whitespace"):
        parse_service_config(data)


def test_parse_service_config_bool_rejected_for_port():
    data = {"port": True, "host": "0.0.0.0", "enable_logging": True}

    with pytest.raises(ConfigError, match="'port' must be an int, got bool"):
        parse_service_config(data)
