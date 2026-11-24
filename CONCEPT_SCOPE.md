# Invoice Router scope

Invoice Router converts synthetic invoice inputs into typed records with field-level confidence, source references and audit artifacts.

- Validates required fields, totals, dates, currencies, tax identifiers, duplicate invoice numbers and line items.
- Routes invoices to approval, operator review or rejection. The file-backed review queue records why a case was flagged and how it was resolved.
- Produces CSV and Xero-, Fortnox- and QuickBooks-style export previews for approved runs.

The local CLI and FastAPI service use deterministic extraction. The default workflow uses synthetic fixtures and runs without live OCR, model inference or accounting writes. The [architecture](docs/architecture.md) describes the artifact layout, and the [verification record](docs/evidence.md) gives repeatable commands and expected results.
