from invoice_router.models import ExtractedField, InvoiceIngest


def test_extracted_field_confidence_bounds() -> None:
    field = ExtractedField(
        field_name='vendor_name',
        value='Acme',
        confidence=0.9,
        extraction_method='template_match',
    )
    assert field.confidence == 0.9


def test_invoice_ingest_parses_fixture_shape() -> None:
    ingest = InvoiceIngest(
        scenario_name='demo',
        source_document_name='demo.txt',
        document_text='Vendor: Demo',
        vendor_name='Demo',
        invoice_number='INV-1',
        invoice_date='2026-05-01',
        currency='USD',
        subtotal=10.0,
        tax_amount=1.0,
        total=11.0,
    )
    assert ingest.invoice_number == 'INV-1'
