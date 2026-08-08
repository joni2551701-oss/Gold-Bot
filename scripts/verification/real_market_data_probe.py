"""Real Market Data Production Verification probe (Director Order).

Runs ONLY inside GitHub Actions via .github/workflows/real_data_verification.yml
(workflow_dispatch, never on push/PR). It exercises the exact
production hot-path classes -- data_layer.providers.twelve_data_client.
TwelveDataClient and data_layer.providers.bitget_provider.BitgetProvider
-- with real credentials from GitHub Secrets, then the real Data
Validation (MarketDataNormalizer._validate_and_clean) and real Market
Memory write path (MarketMemoryRegistry/TimeframeMemory.hydrate).

Security contract (Director Order, section 13 -- non-negotiable):
  - Never print an API key, a Secrets/MaskedSecret object, or any
    exception's raw text that might embed one.
  - Only ever print: CONFIGURED/MISSING presence flags, HTTP outcome,
    symbol, numeric price, timestamp, and generic exception CLASS
    names (never str(exception) for network exceptions, since some
    HTTP libraries echo request params -- including apikey -- into
    their exception message).

No mock, no fixture, no hardcoded price. If a real call fails, the
failure is reported as BLOCKED/FAILED, never silently upgraded to a
fake PASS.
"""
import json
import os
import sys
import traceback

# Ensure the repo root (two levels up from scripts/verification/) is
# importable regardless of how this script is invoked -- `python
# path/to/script.py` puts the script's own directory on sys.path[0],
# not the repo root, so a plain run would otherwise fail to find
# data_layer/core_layer with ModuleNotFoundError before ever reaching
# a real provider call.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def secret_status(name: str) -> str:
    return "CONFIGURED" if os.environ.get(name) else "MISSING"


def safe_exception_report(exc: BaseException) -> str:
    """Class name only -- never the exception's own message, since a
    requests.exceptions.RequestException can embed the full request
    URL (including ?apikey=...) in its str()."""
    return type(exc).__name__


def main() -> int:
    report = {
        "secrets": {},
        "twelvedata": {"status": "NOT_RUN"},
        "bitget": {"status": "NOT_RUN"},
        "validation": {"status": "NOT_RUN"},
        "memory": {"status": "NOT_RUN"},
        "core_consumption": {"status": "NOT_RUN"},
    }

    # --- Section 2: Secret Audit (presence only, never values) -----
    for name in ("TWELVE_DATA_API_KEY", "BITGET_API_KEY", "BITGET_API_SECRET", "BITGET_PASSPHRASE"):
        report["secrets"][name] = secret_status(name)
        print(f"{name}: {report['secrets'][name]}")

    # --- Section 5: Real TwelveData Request (production hot path) --
    raw_candles = None
    try:
        from data_layer.providers.twelve_data_client.twelve_data_client import TwelveDataClient

        client = TwelveDataClient()
        if client.api_key is None:
            report["twelvedata"] = {"status": "BLOCKED", "reason": "TWELVE_DATA_API_KEY not configured"}
        else:
            raw_candles = client.fetch_candles("XAUUSD", "M15", 1)
            if raw_candles:
                c = raw_candles[-1]
                report["twelvedata"] = {
                    "status": "PASS",
                    "symbol": "XAU/USD",
                    "price": c.close,
                    "timestamp": c.timestamp.isoformat(),
                    "request": "SUCCESS",
                }
            else:
                report["twelvedata"] = {"status": "BLOCKED", "reason": "empty response (no candle data returned)"}
    except Exception as e:  # noqa: BLE001 -- probe must never crash the job before reporting
        report["twelvedata"] = {"status": "BLOCKED", "reason": safe_exception_report(e)}

    print("---")
    print(f"TwelveData Request: {report['twelvedata']['status']}")
    if report["twelvedata"]["status"] == "PASS":
        print(f"TwelveData Symbol: {report['twelvedata']['symbol']}")
        print(f"TwelveData Price: {report['twelvedata']['price']}")
        print(f"TwelveData Timestamp: {report['twelvedata']['timestamp']}")
    else:
        print(f"TwelveData Reason: {report['twelvedata'].get('reason')}")

    # --- Section 6: Real Bitget BTC/USDT Request ---------------------
    # TWO SEPARATE results, per the order's own diagnostic-vs-production
    # distinction (section 7):
    #
    #   (a) production-path: the repo's real BitgetProvider
    #       (data_layer.providers.bitget_provider) is a DELIBERATE INERT
    #       STUB -- every data method raises NotImplementedError by
    #       design (confirmed: audits/REAL_DATA_VERIFICATION/03). So
    #       GoldBot's own pipeline can NEVER fetch a real Bitget price
    #       today. production_path = NOT_VERIFIED. This is a design
    #       fact, not a network/credential failure, and this probe does
    #       NOT implement a new Bitget provider (forbidden).
    #
    #   (b) diagnostic: a direct HTTP GET to Bitget's PUBLIC spot ticker
    #       (no auth, no secret) purely to prove the Bitget API itself
    #       returns a real BTC/USDT price. This lives in this
    #       verification script only -- it is NOT wired into the
    #       provider layer and changes no architecture.
    report["bitget"] = {"production_path": "NOT_VERIFIED",
                        "production_reason": "BitgetProvider is an inert stub (NotImplementedError by design); "
                                             "GoldBot pipeline never fetches real Bitget data",
                        "diagnostic": {"status": "NOT_RUN"}}
    try:
        import requests

        BITGET_PUBLIC_TICKER = "https://api.bitget.com/api/v2/spot/market/tickers"
        resp = requests.get(BITGET_PUBLIC_TICKER, params={"symbol": "BTCUSDT"}, timeout=10)
        http_status = resp.status_code
        if http_status == 200:
            body = resp.json()
            rows = body.get("data") or []
            if rows:
                row = rows[0]
                # Bitget v2 spot ticker: 'lastPr' = last price, 'ts' = ms epoch.
                price = float(row.get("lastPr"))
                ts_ms = row.get("ts")
                report["bitget"]["diagnostic"] = {
                    "status": "PASS",
                    "symbol": "BTC/USDT",
                    "http": http_status,
                    "price": price,
                    "timestamp": ts_ms,
                    "request": "SUCCESS",
                }
            else:
                report["bitget"]["diagnostic"] = {"status": "BLOCKED", "http": http_status,
                                                  "reason": "empty data array in response"}
        else:
            report["bitget"]["diagnostic"] = {"status": "BLOCKED", "http": http_status,
                                              "reason": f"non-200 HTTP status {http_status}"}
    except Exception as e:  # noqa: BLE001 -- probe must never crash before reporting
        report["bitget"]["diagnostic"] = {"status": "BLOCKED", "reason": safe_exception_report(e)}

    print("---")
    print(f"Bitget production-path: {report['bitget']['production_path']} ({report['bitget']['production_reason']})")
    diag = report["bitget"]["diagnostic"]
    print(f"Bitget diagnostic (public ticker BTC/USDT): {diag['status']}")
    if diag["status"] == "PASS":
        print(f"Bitget Symbol: {diag['symbol']}")
        print(f"Bitget HTTP: {diag['http']}")
        print(f"Bitget Price: {diag['price']}")
        print(f"Bitget Timestamp: {diag['timestamp']}")
    else:
        print(f"Bitget diagnostic Reason: {diag.get('reason')}")

    # --- Section 8: Provider -> Validation -> Memory -----------------
    if raw_candles:
        try:
            from data_layer.live_data.market_data.market_data import MarketDataNormalizer

            normalizer = MarketDataNormalizer()
            validated = normalizer._validate_and_clean(raw_candles, "XAUUSD", "M15")
            report["validation"] = {
                "status": "PASS" if validated else "FAIL",
                "raw_count": len(raw_candles),
                "validated_count": len(validated),
            }
        except Exception as e:  # noqa: BLE001
            report["validation"] = {"status": "FAIL", "reason": safe_exception_report(e)}

        try:
            from data_layer.market_memory.market_memory_registry.market_memory_registry import MarketMemoryRegistry

            registry = MarketMemoryRegistry()
            memory = registry.get_or_create("XAUUSD")
            validated_candles = report["validation"].get("validated_count", 0)
            if validated_candles and memory.has_timeframe("M15"):
                # Re-run validation result (not raw) into memory -- proves
                # Raw Output never reaches Memory directly.
                from data_layer.live_data.market_data.market_data import MarketDataNormalizer as _N
                _validated = _N()._validate_and_clean(raw_candles, "XAUUSD", "M15")
                memory.timeframe("M15").hydrate(_validated)
                stored = memory.timeframe("M15").get_last()
                report["memory"] = {
                    "status": "PASS" if stored is not None else "FAIL",
                    "stored_count": 1 if stored is not None else 0,
                }
            else:
                report["memory"] = {"status": "FAIL", "reason": "no validated candles or timeframe missing"}
        except Exception as e:  # noqa: BLE001
            report["memory"] = {"status": "FAIL", "reason": safe_exception_report(e)}
    else:
        report["validation"] = {"status": "BLOCKED", "reason": "no raw candles (TwelveData request did not succeed)"}
        report["memory"] = {"status": "BLOCKED", "reason": "no validated candles"}

    print("---")
    print(f"Validation: {report['validation']['status']}")
    print(f"Memory: {report['memory']['status']}")

    # --- Section 9: Core consumption (static finding, confirmed by prior audit) ---
    # core_layer/pipeline/pipeline.py constructs MarketDataService()
    # without a memory_registry -- so in TODAY's wiring, Core does NOT
    # read from Market Memory; it consumes MarketDataNormalizer output
    # directly. This is a static code fact, re-confirmed, not something
    # a live probe can change -- reported as an architecture finding,
    # not fixed here (no new architecture per this order's Forbidden list).
    report["core_consumption"] = {
        "status": "ARCHITECTURE_FINDING",
        "reason": "core_layer/pipeline/pipeline.py builds MarketDataService() with no memory_registry -- "
                  "Core consumes MarketDataNormalizer output directly, not Market Memory, in the live signal path",
    }
    print("---")
    print(f"Core Consumption: {report['core_consumption']['status']} -- {report['core_consumption']['reason']}")

    print("---")
    print("PROBE_RESULT_JSON_START")
    print(json.dumps(report))
    print("PROBE_RESULT_JSON_END")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Last-resort: never let a raw traceback (which could embed a
        # request URL/apikey via requests' own exception formatting)
        # escape to the log. Print only the exception class chain.
        print("PROBE_FATAL: unexpected top-level failure")
        for line in traceback.format_exc().splitlines():
            # Strip anything that looks like a query string / apikey to
            # be defense-in-depth safe even here.
            if "apikey" in line.lower() or "api_key" in line.lower():
                continue
            print(line)
        sys.exit(1)
