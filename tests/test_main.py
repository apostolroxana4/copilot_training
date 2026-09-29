import json

from production_style_service.main import main


def test_main_success(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"port": 8080, "host": "0.0.0.0", "enable_logging": True})
    )

    exit_code = main(["--config", str(config_path)])

    assert exit_code == 0


def test_main_invalid_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"port": "not-an-int"}))

    exit_code = main(["--config", str(config_path)])

    assert exit_code == 1


def test_main_missing_config(tmp_path):
    exit_code = main(["--config", str(tmp_path / "missing.json")])

    assert exit_code == 1
