import logging

from production_style_service.logging_config import setup_logging


def test_setup_logging_sets_level(monkeypatch):
    calls = {}
    monkeypatch.setattr(
        logging,
        "basicConfig",
        lambda **kwargs: calls.update(kwargs),
    )

    setup_logging("DEBUG")

    assert calls["level"] == logging.DEBUG


def test_setup_logging_invalid_level_falls_back_to_info(monkeypatch):
    calls = {}
    monkeypatch.setattr(
        logging,
        "basicConfig",
        lambda **kwargs: calls.update(kwargs),
    )

    setup_logging("NOT_A_LEVEL")

    assert calls["level"] == logging.INFO


def test_setup_logging_is_case_insensitive(monkeypatch):
    calls = {}
    monkeypatch.setattr(
        logging,
        "basicConfig",
        lambda **kwargs: calls.update(kwargs),
    )

    setup_logging("warning")

    assert calls["level"] == logging.WARNING
