# Invoice Router — Concept and Scope

Date: 2026-05-07
Repo: invoice-router
Visibility target: public proof repo with fixture-safe local execution by default

## Concept pitch

Invoice Router is a concrete proof project for invoice and document automation. It shows how invoice-like documents can be converted into structured, validated, accounting-ready previews with a deterministic review boundary.

The repo is intentionally narrow. It does not try to be a general document platform, an OCR benchmark, or an accounting connector suite. It proves one dependable outcome: turn messy invoice inputs into auditable structured data with clear approval, review, and rejection behavior.

## Demand signals addressed

This project is shaped for work that usually mentions one or more of the following:

- invoice or document extraction
- OCR-assisted data entry with validation
- accounting-ready JSON or CSV previews
- manual review queues for uncertain AI output
- n8n, Make, or Zapier handoffs
- spreadsheet-friendly or accounting-friendly outputs

## Systems and workflows made visible

- local OCR-style extraction mock
- local LLM-style confidence mock
- review queue operations
- n8n
- Make
- Zapier
- CSV review workflows
- Xero-style, Fortnox-style, and QuickBooks-style payload previews

## Concrete proof flows

- Clean invoice -> approved extraction -> export previews
- Missing tax ID -> review packet
- Mismatched total -> review packet with arithmetic findings
- Duplicate invoice number -> rejected
- Multi-currency inconsistency -> review packet
- Minimal invoice -> approved with narrow required-field set

## Evidence target

A complete proof package includes:

- synthetic invoice fixtures
- deterministic run artifacts
- structured extraction, validation, routing, and export preview JSON
- review packets for flagged scenarios
- client-readable handoff notes
- screenshot panels showing proof, not decoration
- tests and verification scripts proving repeatability

## Proposal use

Best used when a project needs invoice intake, controlled extraction, accounting preview generation, or a review gate between AI output and downstream systems.

First milestone to suggest:

> Process sample invoice documents, validate the extracted fields and totals, route edge cases into review, and return accounting-ready previews plus replayable audit artifacts.

## Relationship to other repositories

- `automation-kit` remains a useful source of shared local proof conventions and optional reusable utilities.
- `review-router` is the closest reference for review queue behavior and replayable artifacts.
- `sheets-airtable-sync` is a strong reference for typed mapping and output proof surfaces.

These repos inform conventions only. Invoice Router remains its own standalone proof package.

## Safety and scope boundaries

- Local proof repo by default.
- Synthetic fixtures only until explicit approval is given for real client data.
- Empty credential placeholders only.
- No live OCR, live LLM, live accounting, or live email calls in the default proof.
- No automatic visibility, release, or external publication action outside explicit operator control.
- No cloud deployment, paid resource creation, or production-readiness claim in the first proof sprint.
- Evidence must remain deterministic: sample input, structured output, validation log, test output, and handoff notes.
