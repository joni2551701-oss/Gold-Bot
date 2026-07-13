# tests/fixtures/

This directory intentionally holds no `.py` files.

The reusable fixtures this directory's name suggests (`test_user`,
`premium_user`, `vip_user`, `admin_user`, `owner_user`,
`mock_signal_candidate`, `mock_pipeline`, `mock_ai_result`) are all
defined in `tests/conftest.py` instead. Pytest auto-shares every
fixture in `conftest.py` with every test file under `tests/`
(including this directory's siblings — `unit/`, `integration/`,
`security/`) via dependency injection: request one by name as a test
function parameter, no import required.

Putting them in a separate importable module (e.g.
`tests/fixtures/factories.py`, imported as `from tests.fixtures.factories
import ...`) would require `tests/__init__.py` to exist so
`tests.fixtures.factories` resolves as a proper dotted import — this
repo currently has no `tests/__init__.py`, and adding one purely to
support this import style would be its own structural change with its
own risk, for a directory whose contents pytest already shares
automatically without it.

See `docs/testing_strategy.md`'s "Fixtures" section for the full list
and usage examples.
