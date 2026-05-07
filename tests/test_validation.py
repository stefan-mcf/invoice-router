from invoice_router.runtime import build_runtime


def test_validation_detects_arithmetic_mismatch() -> None:
    runtime = build_runtime()
    ingest = runtime.registry.load_ingest('mismatched-total-invoice')
    extraction = runtime.extractor.extract(ingest)
    report = runtime.validator.validate(ingest, extraction)
    findings = report.model_dump(mode='json')['findings']
    assert any(finding['reason_code'] == 'arithmetic_mismatch' for finding in findings)
