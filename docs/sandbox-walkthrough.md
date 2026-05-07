# Sandbox Walkthrough

1. Create a Python 3.11 virtual environment and install `.[dev]`.
2. Run `bash scripts/verify.sh`.
3. List the scenarios with `invoice-router list`.
4. Run `invoice-router run clean-approved-invoice`.
5. Run `invoice-router run missing-tax-id-invoice` and inspect `artifacts/local/queue/pending/`.
6. Resolve the packet through the CLI or API if desired.
7. Replay the approved run with `invoice-router replay <run_id>`.
