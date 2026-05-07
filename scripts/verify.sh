#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=src python3.11 -m pytest -q
python3.11 -m ruff check .
PYTHONPATH=src python3.11 -m mypy src
PYTHONPATH=src python3.11 scripts/public_readiness_check.py
PYTHONPATH=src python3.11 scripts/api_smoke.py
PYTHONPATH=src python3.11 scripts/generate_screenshots.py
