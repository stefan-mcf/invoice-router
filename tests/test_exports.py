from invoice_router.runtime import build_runtime


def test_approved_run_emits_all_export_targets() -> None:
    runtime = build_runtime()
    payload = runtime.run('clean-approved-invoice')
    run = runtime.get_run(payload['run_id'])
    export_targets = [item['target'] for item in run['export_preview']]
    assert export_targets == ['xero', 'fortnox', 'quickbooks', 'csv']
