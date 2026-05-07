from invoice_router.runtime import build_runtime


def test_extractor_finds_source_references() -> None:
    runtime = build_runtime()
    ingest = runtime.registry.load_ingest('clean-approved-invoice')
    extraction = runtime.extractor.extract(ingest)
    assert extraction.fields['invoice_number'].source_reference is not None
    assert extraction.fields['tax_id'].value == 'US-123456'
