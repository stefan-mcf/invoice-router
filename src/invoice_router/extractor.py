from __future__ import annotations

from invoice_router.models import ExtractedField, ExtractionResult, InvoiceIngest, SourceReference

REQUIRED_FIELDS = [
    "vendor_name",
    "invoice_number",
    "invoice_date",
    "currency",
    "subtotal",
    "total",
]


class InvoiceExtractor:
    def extract(self, ingest: InvoiceIngest) -> ExtractionResult:
        line_lookup = {
            index + 1: line for index, line in enumerate(ingest.document_text.splitlines())
        }
        fields: dict[str, ExtractedField] = {}
        confidences: list[float] = []
        methods: set[str] = set()

        field_order = [
            "vendor_name",
            "invoice_number",
            "invoice_date",
            "due_date",
            "currency",
            "subtotal",
            "tax_amount",
            "total",
            "tax_id",
            "payment_terms",
        ]
        for field_name in field_order:
            raw_value = getattr(ingest, field_name)
            label = self._label(field_name)
            source_reference = self._find_reference(label, line_lookup)
            if raw_value is None:
                confidence = 0.0
                missing_reason = "not present in synthetic source"
            else:
                confidence = 0.97 if field_name in REQUIRED_FIELDS else 0.9
                missing_reason = None
            extraction_method = "template_match" if source_reference else "fixture_hint"
            methods.add(extraction_method)
            fields[field_name] = ExtractedField(
                field_name=field_name,
                value=raw_value,
                confidence=confidence,
                extraction_method=extraction_method,
                source_reference=source_reference,
                missing_reason=missing_reason,
            )
            confidences.append(confidence)

        fields["line_items"] = ExtractedField(
            field_name="line_items",
            value=float(len(ingest.line_items)) if ingest.line_items else 0.0,
            confidence=0.95 if ingest.line_items else 0.0,
            extraction_method="fixture_hint",
            source_reference=SourceReference(
                label="line_items",
                snippet="Structured synthetic line items",
            ),
            missing_reason=None if ingest.line_items else "no line items provided",
        )
        confidences.append(fields["line_items"].confidence)

        missing_fields = [name for name in REQUIRED_FIELDS if fields[name].value is None]
        required_present = [name for name in REQUIRED_FIELDS if fields[name].value is not None]
        overall_confidence = round(sum(confidences) / len(confidences), 4)
        return ExtractionResult(
            scenario_name=ingest.scenario_name,
            fields=fields,
            overall_confidence=overall_confidence,
            extraction_methods=sorted(methods),
            required_fields_present=required_present,
            missing_fields=missing_fields,
        )

    def _label(self, field_name: str) -> str:
        mapping = {
            "vendor_name": "Vendor",
            "invoice_number": "Invoice Number",
            "invoice_date": "Invoice Date",
            "due_date": "Due Date",
            "currency": "Currency",
            "subtotal": "Subtotal",
            "tax_amount": "Tax",
            "total": "Total",
            "tax_id": "Tax ID",
            "payment_terms": "Payment Terms",
        }
        return mapping[field_name]

    def _find_reference(
        self,
        label: str,
        line_lookup: dict[int, str],
    ) -> SourceReference | None:
        for line_number, line in line_lookup.items():
            if label.lower() in line.lower():
                return SourceReference(line_number=line_number, snippet=line.strip(), label=label)
        return None
