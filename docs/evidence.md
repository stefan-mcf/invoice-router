# Evidence

## Verification commands

```bash
bash scripts/verify.sh
PYTHONPATH=src python3.11 -m invoice_router.cli run clean-approved-invoice
PYTHONPATH=src python3.11 -m invoice_router.cli validate mismatched-total-invoice
PYTHONPATH=src python3.11 -m invoice_router.cli queue list
```

## What the evidence should show

- approved scenarios produce export previews;
- review scenarios create packets under `artifacts/local/queue/pending/`;
- duplicate scenarios reject without export previews;
- replay confirms deterministic artifact reproduction;
- screenshots show CLI, API, review queue, export preview, and quality-gate proof.
