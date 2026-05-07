     1|# Invoice Router — Concept and Scope
     2|
     3|Date: 2026-05-05
     4|Repo: invoice-router
     5|Visibility target: private proof repo
     6|
     7|## Concept pitch
     8|
     9|Concrete proof project for document/invoice automation: extract structured fields, validate totals, route to accounting-ready output, and flag review cases.
    10|
    11|This project exists because Automation Kit is a reusable tool/framework, while Upwork clients respond faster to concrete proof of a specific business workflow. The repo should prove one thing clearly: I can turn messy business documents into structured, validated workflow data with a safe review boundary.
    12|
    13|## Mined Upwork demand addressed
    14|
    15|## Upwork mining signals this project responds to
    16|
    17|Source: /Users/stefan/upwork-memory-profile, May 2026 mining and strategy files.
    18|
    19|- API integration: 751 jobs / 39% in the demand landscape; API/REST appears as connective tissue across the market.
    20|- AI/LLM workflow work: 673 jobs / 35%, strongest when framed as controlled workflow steps rather than vague agent claims.
    21|- n8n/Make/Zapier workflow work: 593 jobs / 31%; Zapier, Make.com, and n8n repeatedly appear in premium and quick-win shortlists.
    22|- Google Sheets automation: 199 jobs / 10% with strong hourly bands; Sheets work is boring but high-trust and easy to close.
    23|- Airtable build/automation: 273 jobs / 14%; Airtable + Make and Airtable + API requests recur in premium shortlists.
    24|- Automation fix/debug: 119 jobs in the 168h mining report; excellent early-review target because clients are already in pain.
    25|- GHL/HubSpot/CRM cluster: 279 jobs / 9.9% in the 168h mining report; high-volume wedge, even if average rates are lower.
    26|- Slack/Discord bots: lower volume but high median niche; useful as an ops-notification proof asset.
    27|
    28|Portfolio rule: each repo proves one client-shaped outcome. Automation Kit remains the reusable local proof framework for running and validating automation patterns; these companion repos show concrete project implementations that can be linked one at a time in Upwork proposals.
    29|
    30|## Systems and workflows this repo should make visible
    31|
    32|- n8n
    33|- Make.com
    34|- email inbox
    35|- OCR
    36|- local LLM mock
    37|- Airtable
    38|- Google Sheets
    39|- Xero/Fortnox/QuickBooks-style accounting output
    40|
    41|## Concrete proof flows
    42|
    43|- Clean invoice -> approved extraction -> accounting JSON
    44|- Missing tax ID -> manual-review queue
    45|- Mismatched total -> validation failure report
    46|- Duplicate invoice number -> reject/dedupe
    47|
    48|## Evidence target
    49|
    50|A complete proof package should eventually include:
    51|
    52|- sample input fixture;
    53|- deterministic local run;
    54|- structured output JSON/CSV/report;
    55|- validation or audit log;
    56|- client-readable handoff notes;
    57|- README with problem, solution, proof, and safety boundary;
    58|- screenshots of the strongest proof surface;
    59|- tests or validators that prove repeatability.
    60|
    61|## Proposal use
    62|
    63|Best used when a job mentions any of these systems or patterns:
    64|
    65|- n8n
    66|- Make.com
    67|- email inbox
    68|- OCR
    69|- local LLM mock
    70|- Airtable
    71|- Google Sheets
    72|- Xero/Fortnox/QuickBooks-style accounting output
    73|
    74|First milestone to suggest:
    75|
    76|> Process sample invoices, validate extracted fields and totals, and return accounting-ready JSON plus review flags.
    77|
    78|## Relationship to Automation Kit
    79|
    80|- Automation Kit remains the reusable pattern library and local validation framework.
    81|- This repo is a client-shaped implementation/proof wrapper.
    82|- If implementation proceeds, prefer reusing Automation Kit vocabulary: workflow contract, fixtures, mock adapters, validation result, audit log, and handoff note.
    83|- Do not bloat Automation Kit with every vertical proof; use these companion repos to keep each portfolio link focused.
    84|
    85|## Safety and scope boundaries
    86|
    87|- Local/private proof repo by default.
    88|- Synthetic fixtures only until explicit approval is given for real client data.
    89|- Empty credential placeholders only.
    90|- No live SaaS calls in the proof baseline.
    91|- No Upwork submission, client message, or off-platform delivery action.
    92|- No public repo visibility change without explicit approval.
    93|- No cloud deployment, paid resource, or production-readiness claim in the initial proof sprint.
    94|- Evidence should be deterministic: sample input, sample output, validation log, test output, and handoff notes.
    95|