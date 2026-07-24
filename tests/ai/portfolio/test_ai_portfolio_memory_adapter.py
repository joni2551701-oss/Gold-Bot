from ai.portfolio.memory_adapter import portfolio_reference_key
from ai.portfolio.models import PortfolioRecord


def _record(**overrides):
    defaults = dict(portfolio_id="p1", portfolio_name="Main Portfolio")
    defaults.update(overrides)
    return PortfolioRecord(**defaults)


def test_portfolio_reference_key_includes_portfolio_id():
    key = portfolio_reference_key(_record(portfolio_id="p_123"))
    assert "p_123" in key


def test_portfolio_reference_key_has_portfolio_prefix():
    key = portfolio_reference_key(_record())
    assert key.startswith("portfolio:")


def test_portfolio_reference_key_is_deterministic():
    record = _record()
    assert portfolio_reference_key(record) == portfolio_reference_key(record)


def test_portfolio_reference_key_different_for_different_records():
    key_a = portfolio_reference_key(_record(portfolio_id="p1"))
    key_b = portfolio_reference_key(_record(portfolio_id="p2"))
    assert key_a != key_b


def test_portfolio_reference_key_returns_string():
    assert isinstance(portfolio_reference_key(_record()), str)


def test_portfolio_reference_key_never_raises_for_minimal_record():
    minimal = PortfolioRecord(portfolio_id="p", portfolio_name="n")
    assert portfolio_reference_key(minimal) == "portfolio:p"
