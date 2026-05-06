# Invoice Workflow Extractor

Invoice extraction workflow proof with OCR/LLM mock adapters, validation checks, accounting-ready output, and n8n-style handoff docs.

## Role in the Automation Kit portfolio

Concrete proof project for document/invoice automation: extract structured fields, validate totals, route to accounting-ready output, and flag review cases.

Automation Kit is the reusable local proof framework for running and validating automation patterns. This repo is a concrete client-shaped proof asset: it narrows the story to one Upwork job lane so proposals can link directly to the most relevant evidence.


## Current promotion status

Priority: Backlog.

Role: Document/invoice extraction proof with validation and review boundaries.

Rationale: Useful for document automation jobs, but lower immediate priority than API/debug/Sheets.


## Automation Kit usage-case contract

This repo exists to prove Automation Kit usage in one buyer-shaped workflow. It should stay thin: reusable runner logic belongs in `automation-kit`; this repo owns the case-study fixtures, workflow-specific wrapper, output evidence, and proposal-facing explanation.

Ready-to-link requirements:

- thin wrapper around Automation Kit rather than a duplicate framework;
- synthetic input fixtures and deterministic output examples;
- tests for the main flow and one failure or review path;
- case-study documentation with first milestone shape;
- screenshot or text evidence from one verified local run;
- empty credential placeholders only;
- no live SaaS, cloud, payment, or delivery side effects by default.

Until those requirements are met, keep this repo private and treat it as a scoped backlog proof project, not a portfolio link.

## Client-facing promise

I can turn messy business documents into structured, validated workflow data with a safe review boundary.

## Systems and workflows addressed

- n8n
- Make.com
- email inbox
- OCR
- local LLM mock
- Airtable
- Google Sheets
- Xero/Fortnox/QuickBooks-style accounting output

## Initial proof flows

- Clean invoice -> approved extraction -> accounting JSON
- Missing tax ID -> manual-review queue
- Mismatched total -> validation failure report
- Duplicate invoice number -> reject/dedupe

## First milestone shape

Process sample invoices, validate extracted fields and totals, and return accounting-ready JSON plus review flags.

## Current repo status

This repository currently contains concept, scope, and planning artifacts. The implementation baseline is intentionally local/private and synthetic-first.

## Included files

- `CONCEPT_SCOPE.md` — project concept, market fit, workflow scope, evidence target, and safety boundaries.
- `PLAN.md` — comprehensive tranched implementation plan.
- `.env.example` — empty credential placeholders for later local implementation.
- `.gitignore` — keeps secrets, build outputs, and local artifacts out of git.

## Safety baseline

## Safety and scope boundaries

- Local/private proof repo by default.
- Synthetic fixtures only until explicit approval is given for real client data.
- Empty credential placeholders only.
- No live SaaS calls in the proof baseline.
- No Upwork submission, client message, or off-platform delivery action.
- No public repo visibility change without explicit approval.
- No cloud deployment, paid resource, or production-readiness claim in the initial proof sprint.
- Evidence should be deterministic: sample input, sample output, validation log, test output, and handoff notes.
