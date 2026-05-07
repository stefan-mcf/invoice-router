from pathlib import Path

from invoice_router.runtime import build_runtime


def test_runtime_run_writes_artifacts() -> None:
    runtime = build_runtime()
    payload = runtime.run('clean-approved-invoice')
    run_dir = Path(runtime.root / 'artifacts' / 'local' / 'runs' / payload['run_id'])
    assert (run_dir / 'audit-log.json').exists()
    assert payload['routing_outcome'] == 'approved'


def test_runtime_review_path_creates_packet() -> None:
    runtime = build_runtime()
    payload = runtime.run('missing-tax-id-invoice')
    assert payload['review_required'] is True
    assert payload['review_packet_id'] is not None
