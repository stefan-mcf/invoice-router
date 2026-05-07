from invoice_router.backbone import get_health


def test_backbone_health_includes_capabilities() -> None:
    health = get_health()
    assert 'capabilities' in health
    assert 'invoice-ingest-schema' in health['capabilities']
