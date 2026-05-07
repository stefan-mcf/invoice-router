from __future__ import annotations

from fastapi.testclient import TestClient

from invoice_router.api import create_app


def main() -> None:
    client = TestClient(create_app())
    health = client.get('/health')
    assert health.status_code == 200
    assert health.json()['fixture_safe'] is True

    scenarios = client.get('/scenarios')
    assert scenarios.status_code == 200
    assert len(scenarios.json()['scenarios']) >= 6

    run = client.post('/run', json={'scenario': 'clean-approved-invoice'})
    assert run.status_code == 200
    payload = run.json()
    assert payload['routing_outcome'] == 'approved'

    validate = client.post('/validate', json={'scenario': 'mismatched-total-invoice'})
    assert validate.status_code == 200
    findings = validate.json()['findings']
    assert any(item['reason_code'] == 'arithmetic_mismatch' for item in findings)


if __name__ == '__main__':
    main()
