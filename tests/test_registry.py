from invoice_router.runtime import build_runtime


def test_registry_lists_scenarios() -> None:
    runtime = build_runtime()
    scenarios = runtime.list_scenarios()
    assert len(scenarios) >= 6
    assert any(item['name'] == 'clean-approved-invoice' for item in scenarios)
