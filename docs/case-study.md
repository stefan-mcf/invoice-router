# Case study: routing invoices without hiding uncertainty

Invoice processing is easy to automate when every document is clean. Real operational risk sits in the exceptions: totals do not reconcile, tax identifiers are missing, currencies conflict, the same invoice arrives twice, or extracted values are not reliable enough to post.

Invoice Router is a Python workflow that turns invoice-like input into a typed record, validates the business rules, and routes the result to approval, human review, or rejection. Accounting exports are prepared only after the route remains approved.

## The operating model

```text
invoice input
     │
     ▼
typed extraction
     │
     ▼
field confidence and source references
     │
     ▼
business validation
     │
     ▼
routing decision
 ┌───┼──────────┐
 ▼   ▼          ▼
approve review  reject
 │      │
 ▼      ▼
export  queue packet
preview
```

Each run writes a replayable set of artefacts: the input, extraction, validation findings, routing decision, export preview, handover notes, and audit log. Review packets move through pending, claimed, resolved, and dead-letter states in a file-backed queue.

## Scenario coverage

Six controlled invoice scenarios exercise the decisions that matter:

| Scenario | Route | Why |
| --- | --- | --- |
| Clean invoice | Approve | Required fields and totals pass |
| Minimal valid invoice | Approve | Narrow accepted baseline |
| Missing tax ID | Review | Compliance information needs confirmation |
| Mismatched total | Review | Line items and stated total disagree |
| Currency inconsistency | Review | Conflicting currency values require a decision |
| Duplicate invoice | Reject | Reprocessing would create a duplicate payable |

## Key engineering decisions

### Confidence is attached to fields

Extraction does not reduce an invoice to one overall score. Each required value carries confidence, a source reference, and a missing reason where applicable. Review can therefore focus on the uncertain fields.

### Validation and routing are separate

Validation emits stable findings for arithmetic, dates, currencies, tax IDs, duplicates, and line items. Routing policy turns those findings into an operational decision. The separation keeps business rules inspectable.

### Review is a first-class state

Uncertain invoices are written to a queue rather than treated as failed automation. Packets can be claimed and resolved by a named reviewer, leaving a record of the decision and note.

### Exports cannot bypass approval

Xero-style, Fortnox-style, QuickBooks-style, and CSV previews are created only for approved runs. Rejected and review-routed invoices do not produce an accounting-ready result.

### Runs are replayable

Replaying a scenario regenerates the same serialised artefacts. That makes routing changes and regression testing easier to inspect.

## Result

The repository includes:

- typed extraction, validation, routing, queue, and export contracts;
- six scenarios spanning approval, review, and rejection;
- a file-backed operator queue with claim and resolution actions;
- CLI and FastAPI control surfaces;
- four accounting export preview formats;
- per-run audit and handover records;
- low-code mapping notes for Make, n8n, and Zapier;
- 15 automated tests, static analysis, and generated implementation screenshots.

The result is an invoice workflow that automates clean cases while preserving a clear decision path for anything uncertain.

## Scope and production path

The current inputs are controlled invoice records and the extraction stage is deterministic. The project does not call a live OCR or language model service, post to an accounting platform, process customer documents, or send email.

A production implementation would add an approved document source, OCR or extraction adapter, encrypted storage, role-based review, accounting OAuth scopes, write readback, and retention policy. The routing and validation contracts are already separated so those adapters can be added without weakening the approval rules.

## Explore the implementation

- [Architecture](architecture.md)
- [API surface](api.md)
- [Local walkthrough](sandbox-walkthrough.md)
- [Validation record](evidence.md)
- [Low-code mappings](low-code/)
- [Back to the repository overview](../README.md)
