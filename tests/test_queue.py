from invoice_router.runtime import build_runtime


def test_queue_claim_and_resolve() -> None:
    runtime = build_runtime()
    payload = runtime.run('missing-tax-id-invoice')
    packet_id = payload['review_packet_id']
    assert packet_id is not None
    claimed = runtime.claim_packet(packet_id, 'reviewer-1')
    assert claimed['status'] == 'claimed'
    resolved = runtime.resolve_packet(
        packet_id,
        'reviewer-1',
        'approve',
        'Looks acceptable after manual review',
    )
    assert resolved['status'] == 'resolved_approved'
