from invoice_router.runtime import build_runtime


def test_duplicate_invoice_rejects() -> None:
    runtime = build_runtime()
    ingest = runtime.registry.load_ingest('duplicate-invoice')
    extraction = runtime.extractor.extract(ingest)
    report = runtime.validator.validate(ingest, extraction)
    routing = runtime.router.route(report, extraction.overall_confidence)
    assert routing.outcome == 'rejected'
    assert routing.export_allowed is False
