# Case Study

Invoice Router covers one narrow workflow:

- receive an invoice-like document;
- extract the relevant fields;
- validate arithmetic and business sanity;
- stop uncertain cases in review;
- show the approved shape as accounting-ready previews.

## Scenario families

| Scenario | Outcome | Operational value |
|---|---|---|
| clean-approved-invoice | approved | direct export preview path |
| missing-tax-id-invoice | review | tax compliance guardrail |
| mismatched-total-invoice | review | arithmetic reconciliation guardrail |
| duplicate-invoice | rejected | duplicate rejection path |
| multi-currency-inconsistency-invoice | review | conflicting-currency guardrail |
| minimal-core-invoice | approved | narrow valid baseline |

This makes the repo useful for technical reviews and delivery planning that need controlled invoice extraction rather than broad platform claims.
