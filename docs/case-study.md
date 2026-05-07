# Case Study

Invoice Router is a proof package for one narrow workflow:

- receive an invoice-like document;
- extract the relevant fields;
- validate arithmetic and business sanity;
- stop uncertain cases in review;
- show the approved shape as accounting-ready previews.

## Scenario families

| Scenario | Outcome | What it proves |
|---|---|---|
| clean-approved-invoice | approved | direct export preview path |
| missing-tax-id-invoice | review | tax compliance guardrail |
| mismatched-total-invoice | review | arithmetic reconciliation guardrail |
| duplicate-invoice | rejected | duplicate rejection path |
| multi-currency-inconsistency-invoice | review | conflicting-currency guardrail |
| minimal-core-invoice | approved | narrow valid baseline |

This makes the repo useful for proposals and technical reviews that need controlled invoice extraction rather than broad platform claims.
