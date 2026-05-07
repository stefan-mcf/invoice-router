# Invoice Router — Project Summary

Date: 2026-05-07
Repo: invoice-router
Purpose: standalone proof repository for fixture-safe invoice extraction, validation, review routing, and accounting-ready export previews.

## Implemented scope

- typed invoice ingest, extraction, validation, routing, review, and export contracts;
- synthetic fixtures spanning approval, review, and rejection paths;
- deterministic extraction with confidence and trace evidence;
- validation and reconciliation engine;
- file-backed review queue and replayable audit artifacts;
- CLI and local API control surfaces;
- accounting-ready export previews;
- low-code workflow mapping docs;
- optional shared-convention integration notes;
- screenshot, evidence, and verification bundle.

## Boundary

Invoice Router is intentionally fixture-safe by default.

It does not include:
- live OCR integrations;
- live LLM calls;
- real accounting API writes;
- customer data;
- cloud deployment;
- external submissions or release automation.

## Verification entrypoints

- `bash scripts/verify.sh`
- `PYTHONPATH=src python3.11 scripts/public_readiness_check.py`
- `PYTHONPATH=src python3.11 scripts/generate_screenshots.py`

## Public docs entrypoints

- `README.md`
- `docs/architecture.md`
- `docs/api.md`
- `docs/case-study.md`
- `docs/evidence.md`
- `docs/public-readiness-checklist.md`
