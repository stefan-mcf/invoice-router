# Future Live Integration Gate

This repo does not enable live integrations by default.

A future live stage would require:

- OCR credentials and rate-limit planning;
- model-provider selection and cost controls;
- accounting sandbox credentials and payload approvals;
- explicit customer-data handling rules;
- retry, idempotency, and redaction policy for production-facing runs.

Approval checklist before any live stage:

- credentials approved;
- sandbox targets available;
- payload scopes documented;
- cost ceiling defined;
- fallback behavior documented;
- repository wording updated to distinguish local fixture-safe use from live integrations.
