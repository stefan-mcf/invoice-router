from invoice_router.cli import main


def test_cli_list_runs() -> None:
    code = main(['list'])
    assert code == 0


def test_cli_health_json() -> None:
    code = main(['health', '--json'])
    assert code == 0
