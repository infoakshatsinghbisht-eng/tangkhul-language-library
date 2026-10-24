"""Command-line interface for Tangkhul Language Library."""

from __future__ import annotations

import argparse
import sys

from tangkhul_lib import __version__
from tangkhul_lib.core.config import LibraryConfig


def main(argv: list[str] | None = None) -> int:
    """Entrypoint for the `tangkhul` command-line utility."""
    parser = argparse.ArgumentParser(
        prog="tangkhul",
        description="Tangkhul Language Library CLI — tools for language preservation and research.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Print project configuration and environment status.",
    )

    args = parser.parse_args(argv)

    if args.info:
        config = LibraryConfig.from_environment()
        print(f"Tangkhul Language Library v{__version__}")
        print(f"Project root: {config.paths.root_dir}")
        print(f"Data directory: {config.paths.data_dir}")
        print(f"Manifests: {config.paths.manifests_dir}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
