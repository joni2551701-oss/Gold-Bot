"""
Data Layer — API error classification (Pre-Phase 59 Architecture
Readiness Review, AC-07; extended by Phase 59.1 TASK 5).

classify_api_error() turns an already-caught data-fetch exception
(from data_layer/providers/twelve_data_client.py's TwelveDataClient.fetch_candles(),
via data_layer/live_data/market_data.py's MarketDataNormalizer.get_candles(), or via
data_layer/providers/twelve_data_provider.py's TwelveDataProvider) into a
standard, structured core_layer.errors.exceptions.ExternalAPIError (Phase
A18) -- for richer logging only. It does NOT change control flow: the
caller still catches, logs, and degrades to an empty candle list
exactly as it does today; this function is never itself raised, only
constructed and logged. See docs/ARCHITECTURE_READINESS_REVIEW.md's
AC-07 section for why data_layer/providers/twelve_data_client.py's own retry/backoff
logic and data_layer/live_data/market_data.py's existing try/except/degrade behavior
are both left untouched.

Phase 59.1 (Market Data Provider Abstraction, TASK 5) adds
classify_empty_response() -- a distinct, precise condition (the
provider returned zero candles) that data_layer/providers/twelve_data_client.py's own
fetch_candles() already handles by returning [] rather than raising
(see its own "if not values: ... return []" branch), so it cannot be
detected from an exception type the way API_001/API_002 are. Callers
that already know they got an empty list (e.g.
data_layer/providers/twelve_data_provider.py) call this directly instead of
classify_api_error().
"""

import requests

from core_layer.errors import codes
from core_layer.errors.exceptions import ExternalAPIError


def classify_api_error(exception: Exception, module: str = "TwelveDataClient") -> ExternalAPIError:
    """
    Never raises: always returns a well-formed ExternalAPIError,
    regardless of the input exception's type. A requests.Timeout (or
    the ConnectionError data_layer/providers/twelve_data_client.py's fetch_candles()
    raises after exhausting its retries on a network failure) maps to
    API_001. A message that mentions "symbol" (Twelve Data's own error
    responses for an unsupported/misspelled symbol include the word
    "symbol" -- e.g. "**symbol** parameter is missing or invalid")
    maps to API_003 -- a best-effort, message-content heuristic,
    disclosed as such: data_layer/providers/twelve_data_client.py's fetch_candles()
    collapses every non-429 API error into one generic ValueError
    (see its own "else: raise ValueError(...)" branch, deliberately
    left untouched by this phase), so message content is the only
    signal available without modifying that retry/error-handling code.
    Anything else (a rate-limit ValueError, or an unrecognized
    exception type) maps to API_002.
    """
    message = str(exception)

    if isinstance(exception, (requests.exceptions.Timeout, ConnectionError)):
        code = codes.API_001
    elif "symbol" in message.lower():
        code = codes.API_003
    else:
        code = codes.API_002

    return ExternalAPIError(
        code=code,
        message=message,
        module=module,
        details={"exception_type": type(exception).__name__},
    )


def classify_empty_response(symbol: str, timeframe: str, module: str = "TwelveDataProvider") -> ExternalAPIError:
    """
    Never raises: a precise, known condition (a provider call
    completed without error but returned zero candles), not a
    heuristic. Always maps to API_004. Distinct from
    classify_api_error() -- there is no exception to classify here,
    only an empty result the caller already observed.
    """
    return ExternalAPIError(
        code=codes.API_004,
        message=f"No candle data returned for {symbol} at {timeframe}",
        module=module,
        details={"symbol": symbol, "timeframe": timeframe},
    )
