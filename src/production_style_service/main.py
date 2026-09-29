"""Service entry point."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from production_style_service.config import ConfigError, load_config, parse_service_config
from production_style_service.logging_config import setup_logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.example.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Production-style service")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to a JSON config file",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (default: INFO)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    setup_logging(args.log_level)

    try:
        raw_config = load_config(args.config)
        config = parse_service_config(raw_config)
    except ConfigError as exc:
        logger.error("Failed to start: %s", exc)
        return 1

    logger.info("Service starting with config: %s", config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
