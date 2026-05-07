     1|# Invoice Router — Comprehensive Tranched Implementation Plan
     2|
     3|Date: 2026-05-05
     4|Repo: invoice-router
     5|Purpose: build a concrete Upwork proof asset that complements Automation Kit.
     6|
     7|## Strategic objective
     8|
     9|Concrete proof project for document/invoice automation: extract structured fields, validate totals, route to accounting-ready output, and flag review cases.
    10|
    11|Client-facing promise: I can turn messy business documents into structured, validated workflow data with a safe review boundary.
    12|
    13|First milestone shape: Process sample invoices, validate extracted fields and totals, and return accounting-ready JSON plus review flags.
    14|
    15|## Demand grounding
    16|
    17|## Upwork mining signals this project responds to
    18|
    19|Source: /Users/stefan/upwork-memory-profile, May 2026 mining and strategy files.
    20|
    21|- API integration: 751 jobs / 39% in the demand landscape; API/REST appears as connective tissue across the market.
    22|- AI/LLM workflow work: 673 jobs / 35%, strongest when framed as controlled workflow steps rather than vague agent claims.
    23|- n8n/Make/Zapier workflow work: 593 jobs / 31%; Zapier, Make.com, and n8n repeatedly appear in premium and quick-win shortlists.
    24|- Google Sheets automation: 199 jobs / 10% with strong hourly bands; Sheets work is boring but high-trust and easy to close.
    25|- Airtable build/automation: 273 jobs / 14%; Airtable + Make and Airtable + API requests recur in premium shortlists.
    26|- Automation fix/debug: 119 jobs in the 168h mining report; excellent early-review target because clients are already in pain.
    27|- GHL/HubSpot/CRM cluster: 279 jobs / 9.9% in the 168h mining report; high-volume wedge, even if average rates are lower.
    28|- Slack/Discord bots: lower volume but high median niche; useful as an ops-notification proof asset.
    29|
    30|Portfolio rule: each repo proves one client-shaped outcome. Automation Kit remains the reusable local proof framework for running and validating automation patterns; these companion repos show concrete project implementations that can be linked one at a time in Upwork proposals.
    31|
    32|## Build rules
    33|
    34|- Use RED-GREEN-VERIFY for implementation tranches.
    35|- Synthetic fixtures first.
    36|- Mock adapters first.
    37|- Empty credential placeholders only.
    38|- No live SaaS, LLM, OCR, Slack, Discord, Google, Airtable, Zapier, Make, n8n, CRM, or accounting calls until explicitly approved.
    39|- Prefer deterministic outputs over flashy claims.
    40|- Every tranche should end with tests/checks or an explicit docs-only verification.
    41|- Commit only after verification.
    42|- Keep this repo private unless a separate public-readiness review approves otherwise.
    43|
    44|## Project tranches
    45|
    46|### Tranche 0: Repo bootstrap and document boundary
    47|
    48|- Create Python package skeleton.
    49|- Document that fixture invoices are synthetic and OCR/LLM adapters are mocked by default.
    50|- Add empty placeholders for OCR/LLM/accounting credentials.
    51|- Acceptance: no live document processing needed.
    52|
    53|Verification:
    54|
    55|- Add or run the focused test/check for this tranche.
    56|- Inspect generated artifacts manually for private data and unsupported claims.
    57|
    58|Acceptance criteria:
    59|
    60|- The tranche output is committed only after it matches the stated proof scope.
    61|
    62|### Tranche 1: Invoice fixtures and schema
    63|
    64|- Add clean invoice, missing-tax-id invoice, mismatched-total invoice, duplicate-invoice fixture.
    65|- Define invoice extraction schema with vendor, invoice number, dates, line items, tax, total, currency.
    66|- Acceptance: fixtures cover happy and review paths.
    67|
    68|Verification:
    69|
    70|- Add or run the focused test/check for this tranche.
    71|- Inspect generated artifacts manually for private data and unsupported claims.
    72|
    73|Acceptance criteria:
    74|
    75|- The tranche output is committed only after it matches the stated proof scope.
    76|
    77|### Tranche 2: Mock OCR/LLM extraction
    78|
    79|- Implement deterministic extractor over text/HTML/PDF-like fixtures.
    80|- Return confidence and source snippets.
    81|- Acceptance: no live LLM/OCR call occurs.
    82|
    83|Verification:
    84|
    85|- Add or run the focused test/check for this tranche.
    86|- Inspect generated artifacts manually for private data and unsupported claims.
    87|
    88|Acceptance criteria:
    89|
    90|- The tranche output is committed only after it matches the stated proof scope.
    91|
    92|### Tranche 3: Validation engine
    93|
    94|- Validate totals, required IDs, date formats, duplicate invoice numbers, currency consistency.
    95|- Acceptance: mismatched totals and duplicates are flagged accurately.
    96|
    97|Verification:
    98|
    99|- Add or run the focused test/check for this tranche.
   100|- Inspect generated artifacts manually for private data and unsupported claims.
   101|
   102|Acceptance criteria:
   103|
   104|- The tranche output is committed only after it matches the stated proof scope.
   105|
   106|### Tranche 4: Accounting-ready output
   107|
   108|- Generate Xero/Fortnox/QuickBooks-style JSON/CSV outputs.
   109|- Generate manual-review queue for low confidence or validation failures.
   110|- Acceptance: output is directly explainable for accounting workflow jobs.
   111|
   112|Verification:
   113|
   114|- Add or run the focused test/check for this tranche.
   115|- Inspect generated artifacts manually for private data and unsupported claims.
   116|
   117|Acceptance criteria:
   118|
   119|- The tranche output is committed only after it matches the stated proof scope.
   120|
   121|### Tranche 5: n8n/Make handoff docs
   122|
   123|- Map email trigger -> OCR/LLM extraction -> validation -> accounting/Airtable/Sheets route.
   124|- Add n8n-style workflow diagram and Make/Zapier alternatives.
   125|- Acceptance: repo maps to local LLM/OCR/n8n invoice processing jobs.
   126|
   127|Verification:
   128|
   129|- Add or run the focused test/check for this tranche.
   130|- Inspect generated artifacts manually for private data and unsupported claims.
   131|
   132|Acceptance criteria:
   133|
   134|- The tranche output is committed only after it matches the stated proof scope.
   135|
   136|### Tranche 6: Evidence package
   137|
   138|- Generate screenshots for invoice fixture, extracted JSON, validation report, review queue, tests.
   139|- Acceptance: proof is visual and deterministic.
   140|
   141|Verification:
   142|
   143|- Add or run the focused test/check for this tranche.
   144|- Inspect generated artifacts manually for private data and unsupported claims.
   145|
   146|Acceptance criteria:
   147|
   148|- The tranche output is committed only after it matches the stated proof scope.
   149|
   150|### Tranche 7: Verification and private push
   151|
   152|- Run tests/lint/type checks as configured.
   153|- Commit and push private repo.
   154|- Verify remote private visibility and content.
   155|
   156|Verification:
   157|
   158|- Add or run the focused test/check for this tranche.
   159|- Inspect generated artifacts manually for private data and unsupported claims.
   160|
   161|Acceptance criteria:
   162|
   163|- The tranche output is committed only after it matches the stated proof scope.
   164|
   165|
   166|## Final definition of done
   167|
   168|The proof repo is complete when:
   169|
   170|- the README tells a client-shaped story in under 30 seconds;
   171|- fixtures, output, validation/audit logs, and handoff notes are committed;
   172|- tests or validators prove deterministic behavior;
   173|- screenshots show the strongest evidence surface;
   174|- .env.example contains empty placeholders only;
   175|- no live credentials or client data are present;
   176|- the repo is pushed private to GitHub;
   177|- remote visibility and commit alignment are verified.
   178|
   179|## Human approval gates
   180|
   181|Stop and ask before:
   182|
   183|- using real credentials;
   184|- connecting live SaaS accounts;
   185|- sending live Slack/Discord/email/SMS messages;
   186|- using real client data;
   187|- deploying to cloud;
   188|- publishing or changing repo visibility;
   189|- submitting or messaging on Upwork.
   190|