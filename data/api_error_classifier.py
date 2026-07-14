"""
Data Layer — API error classification (Pre-Phase 59 Architecture
Readiness Review, AC-07).

classify_api_error() turns an already-caught data-fetch exception
(from data/twelve_data_client.py's TwelveDataClient.fetch_candles(),
via data/market_data.py's MarketDataNormalizer.get_candles()) into a
standard, structured core.errors.exceptions.ExternalAPIError (Phase
A18) -- for richer logging only. It does NOT change control flow: the
caller still catches, logs, and degrades to an empty candle list
exactly as it does today; this function is never itself raised, only
constructed and logged. See docs/ARCHITECTURE_READINESS_REVIEW.md's
AC-07 section for why data/twelve_data_client.py's own retry/backoff
logic and data/market_data.py's existing try/except/degrade behavior
are both left untouched.
"""

import requests

from core.errors import codes
from core.errors.exceptions import ExternalAPIError


def classify_api_error(exception: Exception, module: str = "TwelveDataClient") -> ExternalAPIError:
    """
    Never raises: always returns a well-formed ExternalAPIError,
    regardless of the input exception's type. A requests.Timeout (or
    the ConnectionError data/twelve_data_client.py's fetch_candles()
    raises after exhausting its retries on a network failure) maps to
    API_001; anything else (a rate-limit or malformed-response
    ValueError, or an unrecognized exception type) maps to API_002.
    """
    if isinstance(exception, (requests.exceptions.Timeout, ConnectionError)):
        code = codes.API_001
    else:
        code = codes.API_002

    return ExternalAPIError(
        code=code,
        message=str(exception),
        module=module,
        details={"exception_type": type(exception).__name__},
    )
