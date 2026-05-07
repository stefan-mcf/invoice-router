from fastapi.testclient import TestClient

from invoice_router.api import create_app


def test_api_health_contract() -> None:
    client = TestClient(create_app())
    response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['fixture_safe'] is True
    assert payload['live_services_used'] is False
    assert payload['synthetic_data_only'] is True


def test_api_run_endpoint() -> None:
    client = TestClient(create_app())
    response = client.post('/run', json={'scenario': 'clean-approved-invoice'})
    assert response.status_code == 200
    assert response.json()['routing_outcome'] == 'approved'
