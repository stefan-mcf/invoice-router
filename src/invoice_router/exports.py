from __future__ import annotations

from invoice_router.models import (
    AccountingExportPreview,
    ExportTarget,
    ExtractionResult,
    InvoiceIngest,
    RoutingDecision,
)


class ExportPreviewBuilder:
    def build_previews(
        self,
        ingest: InvoiceIngest,
        extraction: ExtractionResult,
        routing: RoutingDecision,
        duplicate_key: str,
    ) -> list[AccountingExportPreview]:
        if not routing.export_allowed:
            return []
        vendor = str(extraction.fields["vendor_name"].value)
        invoice_number = str(extraction.fields["invoice_number"].value)
        currency = str(extraction.fields["currency"].value)
        total = float(extraction.fields["total"].value or 0.0)
        subtotal = float(extraction.fields["subtotal"].value or 0.0)
        tax_amount = float(extraction.fields["tax_amount"].value or 0.0)
        line_items = [item.model_dump(mode="json") for item in ingest.line_items]
        meta = {
            "scenario_name": ingest.scenario_name,
            "run_outcome": routing.outcome,
            "duplicate_key": duplicate_key,
            "validation_summary": list(routing.reasons),
        }
        return [
            AccountingExportPreview(
                target=ExportTarget.XERO,
                payload={
                    "Type": "ACCPAY",
                    "InvoiceNumber": invoice_number,
                    "Contact": {"Name": vendor},
                    "CurrencyCode": currency,
                    "SubTotal": subtotal,
                    "TotalTax": tax_amount,
                    "Total": total,
                    "LineItems": line_items,
                },
                meta=meta,
            ),
            AccountingExportPreview(
                target=ExportTarget.FORTNOX,
                payload={
                    "supplierName": vendor,
                    "externalInvoiceNumber": invoice_number,
                    "currency": currency,
                    "invoiceTotal": total,
                    "rows": line_items,
                },
                meta=meta,
            ),
            AccountingExportPreview(
                target=ExportTarget.QUICKBOOKS,
                payload={
                    "TxnDate": ingest.invoice_date,
                    "VendorRef": {"name": vendor},
                    "DocNumber": invoice_number,
                    "CurrencyRef": {"value": currency},
                    "TotalAmt": total,
                    "Line": line_items,
                },
                meta=meta,
            ),
            AccountingExportPreview(
                target=ExportTarget.CSV,
                payload={
                    "header": [
                        "vendor_name",
                        "invoice_number",
                        "invoice_date",
                        "currency",
                        "subtotal",
                        "tax_amount",
                        "total",
                    ],
                    "rows": [
                        [
                            vendor,
                            invoice_number,
                            ingest.invoice_date,
                            currency,
                            subtotal,
                            tax_amount,
                            total,
                        ]
                    ],
                },
                meta=meta,
            ),
        ]
