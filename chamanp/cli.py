# SPDX-License-Identifier: LGPL-3.0-or-later
"""Minimal public command-line interface for CHAMANP."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from chamanp import ChamanpConfig, __version__, run, validate_config


def main(argv=None):
    """Run the CHAMANP command-line interface."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "check-config":
            config = ChamanpConfig.from_toml(args.config)
            validate_config(config)
            print(f"Configuration OK: {args.config}")
            return 0

        if args.command == "run":
            config = ChamanpConfig.from_toml(args.config)
            validate_config(config)
            result = run(config)
            print("CHAMANP run completed.")
            print(f"Status: {result.status}")
            print(f"Output directory: {_output_directory(result)}")
            return 0

        parser.print_help()
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def _build_parser():
    parser = ArgumentParser(prog="chamanp")
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser(
        "check-config",
        help="load and validate a TOML configuration profile",
    )
    check_parser.add_argument("config", help="path to a TOML configuration profile")

    run_parser = subparsers.add_parser(
        "run",
        help="load a TOML configuration profile and run CHAMANP",
    )
    run_parser.add_argument("config", help="path to a TOML configuration profile")

    return parser


def _output_directory(result):
    path = Path(result.curated_path)
    return str(path.parent) if path.parent != Path(".") else "."


if __name__ == "__main__":
    raise SystemExit(main())
