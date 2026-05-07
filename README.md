     1|# Invoice Router
     2|
     3|Invoice extraction workflow proof with OCR/LLM mock adapters, validation checks, accounting-ready output, and n8n-style handoff docs.
     4|
     5|## Role in the Automation Kit portfolio
     6|
     7|Concrete proof project for document/invoice automation: extract structured fields, validate totals, route to accounting-ready output, and flag review cases.
     8|
     9|Automation Kit is the reusable local proof framework for running and validating automation patterns. This repo is a concrete client-shaped proof asset: it narrows the story to one Upwork job lane so proposals can link directly to the most relevant evidence.
    10|
    11|
    12|## Current promotion status
    13|
    14|Priority: Backlog.
    15|
    16|Role: Document/invoice extraction proof with validation and review boundaries.
    17|
    18|Rationale: Useful for document automation jobs, but lower immediate priority than API/debug/Sheets.
    19|
    20|
    21|## Automation Kit usage-case contract
    22|
    23|This repo exists to prove Automation Kit usage in one buyer-shaped workflow. It should stay thin: reusable runner logic belongs in `automation-kit`; this repo owns the case-study fixtures, workflow-specific wrapper, output evidence, and proposal-facing explanation.
    24|
    25|Ready-to-link requirements:
    26|
    27|- thin wrapper around Automation Kit rather than a duplicate framework;
    28|- synthetic input fixtures and deterministic output examples;
    29|- tests for the main flow and one failure or review path;
    30|- case-study documentation with first milestone shape;
    31|- screenshot or text evidence from one verified local run;
    32|- empty credential placeholders only;
    33|- no live SaaS, cloud, payment, or delivery side effects by default.
    34|
    35|Until those requirements are met, keep this repo private and treat it as a scoped backlog proof project, not a portfolio link.
    36|
    37|## Client-facing promise
    38|
    39|I can turn messy business documents into structured, validated workflow data with a safe review boundary.
    40|
    41|## Systems and workflows addressed
    42|
    43|- n8n
    44|- Make.com
    45|- email inbox
    46|- OCR
    47|- local LLM mock
    48|- Airtable
    49|- Google Sheets
    50|- Xero/Fortnox/QuickBooks-style accounting output
    51|
    52|## Initial proof flows
    53|
    54|- Clean invoice -> approved extraction -> accounting JSON
    55|- Missing tax ID -> manual-review queue
    56|- Mismatched total -> validation failure report
    57|- Duplicate invoice number -> reject/dedupe
    58|
    59|## First milestone shape
    60|
    61|Process sample invoices, validate extracted fields and totals, and return accounting-ready JSON plus review flags.
    62|
    63|## Current repo status
    64|
    65|This repository currently contains concept, scope, and planning artifacts. The implementation baseline is intentionally local/private and synthetic-first.
    66|
    67|## Included files
    68|
    69|- `CONCEPT_SCOPE.md` — project concept, market fit, workflow scope, evidence target, and safety boundaries.
    70|- `PLAN.md` — comprehensive tranched implementation plan.
    71|- `.env.example` — empty credential placeholders for later local implementation.
    72|- `.gitignore` — keeps secrets, build outputs, and local artifacts out of git.
    73|
    74|## Safety baseline
    75|
    76|## Safety and scope boundaries
    77|
    78|- Local/private proof repo by default.
    79|- Synthetic fixtures only until explicit approval is given for real client data.
    80|- Empty credential placeholders only.
    81|- No live SaaS calls in the proof baseline.
    82|- No Upwork submission, client message, or off-platform delivery action.
    83|- No public repo visibility change without explicit approval.
    84|- No cloud deployment, paid resource, or production-readiness claim in the initial proof sprint.
    85|- Evidence should be deterministic: sample input, sample output, validation log, test output, and handoff notes.
    86|