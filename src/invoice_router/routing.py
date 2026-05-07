from __future__ import annotations

from invoice_router.models import ReasonCode, RouteOutcome, RoutingDecision, ValidationReport


class InvoiceRouter:
    def route(self, report: ValidationReport, overall_confidence: float) -> RoutingDecision:
        reason_codes = [finding.reason_code for finding in report.findings]
        if report.exact_duplicate:
            return RoutingDecision(
                outcome=RouteOutcome.REJECTED,
                reasons=[ReasonCode.DUPLICATE_EXACT],
                review_packet_required=False,
                export_allowed=False,
                recommended_next_step=(
                    "Reject the invoice as an exact duplicate and preserve the duplicate key."
                ),
            )
        if overall_confidence < 0.75 or any(
            reason in reason_codes
            for reason in [
                ReasonCode.MISSING_REQUIRED_FIELD,
                ReasonCode.CONFIDENCE_BELOW_THRESHOLD,
                ReasonCode.ARITHMETIC_MISMATCH,
                ReasonCode.CURRENCY_INCONSISTENCY,
                ReasonCode.DATE_SANITY_FAILURE,
                ReasonCode.TAX_ID_ISSUE,
                ReasonCode.LINE_ITEM_INCOMPLETE,
            ]
        ):
            return RoutingDecision(
                outcome=RouteOutcome.FLAGGED_FOR_REVIEW,
                reasons=sorted(set(reason_codes), key=lambda reason: reason.value),
                review_packet_required=True,
                export_allowed=False,
                recommended_next_step=(
                    "Queue the invoice for manual review with findings and evidence snippets."
                ),
            )
        return RoutingDecision(
            outcome=RouteOutcome.APPROVED,
            reasons=sorted(set(reason_codes), key=lambda reason: reason.value),
            review_packet_required=False,
            export_allowed=True,
            recommended_next_step=(
                "Approve the invoice and generate export previews for accounting review."
            ),
        )
