# Architecture

Invoice Router is a small Python package with six layers:

1. `scenario_registry.py` loads synthetic scenarios, expected outcomes, and notes.
2. `extractor.py` converts a synthetic invoice source into typed extracted fields with confidence and source references.
3. `validation.py` checks required fields, totals, dates, currencies, tax IDs, duplicates, and line items.
4. `routing.py` turns validation output into approval, review, or rejection.
5. `review_queue.py` persists review packets in a file-backed queue.
6. `runtime.py` orchestrates runs, writes artifacts, and exposes CLI/API-facing operations.

## Artifact layout

Runs are written under `artifacts/local/runs/<run_id>/` with these files:

- `input.json`
- `extraction.json`
- `validation.json`
- `routing.json`
- `export-preview.json`
- `handoff-notes.md`
- `audit-log.json`

Review packets are written under `artifacts/local/queue/` in `pending/`, `claimed/`, `resolved/`, and `dead-letter/` subdirectories.

## Determinism rules

- scenarios are synthetic and stored in git;
- extraction uses template-matched values from the fixture payload;
- validation emits stable reason codes;
- replay uses the same scenario input and compares serialized artifacts.
