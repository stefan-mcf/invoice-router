from __future__ import annotations

import hashlib
from datetime import date

from invoice_router.models import (
    ExtractionResult,
    InvoiceIngest,
    ReasonCode,
    Severity,
    ValidationFinding,
    ValidationReport,
)


class InvoiceValidator:
    def validate(
        self,
        ingest: InvoiceIngest,
        extraction: ExtractionResult,
    ) -> ValidationReport:
        findings: list[ValidationFinding] = []
        required_fields = [
            "vendor_name",
            "invoice_number",
            "invoice_date",
            "currency",
            "subtotal",
            "total",
        ]
        for field_name in required_fields:
            if extraction.fields[field_name].value is None:
                findings.append(
                    ValidationFinding(
                        severity=Severity.ERROR,
                        reason_code=ReasonCode.MISSING_REQUIRED_FIELD,
                        message=f"Required field '{field_name}' is missing",
                        field_name=field_name,
                    )
                )
        if extraction.fields["tax_id"].value in {None, ""}:
            findings.append(
                ValidationFinding(
                    severity=Severity.WARNING,
                    reason_code=ReasonCode.TAX_ID_ISSUE,
                    message="Tax ID is missing",
                    field_name="tax_id",
                )
            )
        for field_name, extracted in extraction.fields.items():
            if field_name == "line_items":
                continue
            if extracted.value is not None and extracted.confidence < 0.75:
                findings.append(
                    ValidationFinding(
                        severity=Severity.WARNING,
                        reason_code=ReasonCode.CONFIDENCE_BELOW_THRESHOLD,
                        message=f"Field '{field_name}' confidence is below threshold",
                        field_name=field_name,
                    )
                )
        subtotal = float(ingest.subtotal or 0.0)
        tax_amount = float(ingest.tax_amount or 0.0)
        total = float(ingest.total or 0.0)
        arithmetic_delta = round((subtotal + tax_amount) - total, 2)
        if abs(arithmetic_delta) > 0.01:
            findings.append(
                ValidationFinding(
                    severity=Severity.ERROR,
                    reason_code=ReasonCode.ARITHMETIC_MISMATCH,
                    message=f"Subtotal + tax does not equal total (delta={arithmetic_delta:.2f})",
                    field_name="total",
                )
            )
        if ingest.invoice_date is not None:
            year = int(ingest.invoice_date.split("-")[0])
            current_year = date.today().year
            if year < 2020 or year > current_year + 5:
                findings.append(
                    ValidationFinding(
                        severity=Severity.ERROR,
                        reason_code=ReasonCode.DATE_SANITY_FAILURE,
                        message="Invoice date falls outside the accepted sanity range",
                        field_name="invoice_date",
                    )
                )
        currencies = {
            currency for currency in [ingest.currency, *ingest.currency_mentions] if currency
        }
        line_item_currencies = {item.currency for item in ingest.line_items if item.currency}
        if len(currencies | line_item_currencies) > 1:
            findings.append(
                ValidationFinding(
                    severity=Severity.ERROR,
                    reason_code=ReasonCode.CURRENCY_INCONSISTENCY,
                    message="Multiple currencies appear in the same invoice scenario",
                    field_name="currency",
                )
            )
        for index, item in enumerate(ingest.line_items, start=1):
            if not item.description or item.quantity <= 0 or item.unit_price <= 0:
                findings.append(
                    ValidationFinding(
                        severity=Severity.ERROR,
                        reason_code=ReasonCode.LINE_ITEM_INCOMPLETE,
                        message=f"Line item {index} is incomplete",
                        field_name="line_items",
                    )
                )
                break
        duplicate_key = hashlib.sha256(
            f"{ingest.vendor_name}|{ingest.invoice_number}|{ingest.currency}|{ingest.total}".encode()
        ).hexdigest()[:16]
        exact_duplicate = ingest.known_duplicate
        if exact_duplicate:
            findings.append(
                ValidationFinding(
                    severity=Severity.ERROR,
                    reason_code=ReasonCode.DUPLICATE_EXACT,
                    message="Invoice matches a known duplicate",
                    field_name="invoice_number",
                )
            )
        approved_candidate = not any(finding.severity == Severity.ERROR for finding in findings)
        return ValidationReport(
            findings=findings,
            approved_candidate=approved_candidate,
            duplicate_key=duplicate_key,
            exact_duplicate=exact_duplicate,
            arithmetic_delta=arithmetic_delta,
        )
