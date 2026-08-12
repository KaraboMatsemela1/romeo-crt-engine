from pathlib import Path


def test_env_example_disables_live_trading() -> None:
    text = Path(".env.example").read_text(encoding="utf-8")
    assert "LIVE_TRADING_AUTHORIZED=false" in text
