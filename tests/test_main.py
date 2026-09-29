import json

from production_style_service.main import (
    EXIT_CONFIG_ERROR,
    EXIT_OK,
    EXIT_UNEXPECTED_ERROR,
    main,
    parse_args,
)


def test_parse_args_defaults():
    args = parse_args([])

    assert args.log_level == "INFO"


def test_parse_args_overrides():
    args = parse_args(["--config", "custom.json", "--log-level", "DEBUG"])

    assert str(args.config) == "custom.json"
    assert args.log_level == "DEBUG"


def test_main_uses_default_config():
    exit_code = main([])

    assert exit_code == EXIT_OK


def test_main_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"port": 8080, "host": "0.0.0.0", "enable_logging": True})
    )

    exit_code = main(["--config", str(config_path)])

    assert exit_code == EXIT_OK


def test_main_invalid_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"port": "not-an-int"}))

    exit_code = main(["--config", str(config_path)])

    assert exit_code == EXIT_CONFIG_ERROR


def test_main_missing_config(tmp_path):
    exit_code = main(["--config", str(tmp_path / "missing.json")])

    assert exit_code == EXIT_CONFIG_ERROR


def test_main_unexpected_error_is_caught(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"port": 8080, "host": "0.0.0.0", "enable_logging": True})
    )

    def boom(_path):
        raise RuntimeError("boom")

    monkeypatch.setattr("production_style_service.main.load_service_config", boom)

    exit_code = main(["--config", str(config_path)])

    assert exit_code == EXIT_UNEXPECTED_ERROR
