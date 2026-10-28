"""Entrypoint for `python -m tangkhul_lib`."""

from __future__ import annotations

import sys

from tangkhul_lib.cli import main

if __name__ == "__main__":
    sys.exit(main())
