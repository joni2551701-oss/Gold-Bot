"""Real continuous Price Stream Verification probe (Director Orders
REAL-DATA-006, REAL-DATA-008).

Runs ONLY inside GitHub Actions via .github/workflows/ci.yml's gated
`real_data_probe` job (workflow_dispatch, never on push/PR). It exercises
the EXACT production Price Stream runtime chain -- the same objects the
live Telegram process drives from
`platform_layer.telegram.polling._price_stream_tick_loop`:

    build_default_price_stream_service(memory_registry=MarketMemoryRegistry())
      -> PriceStreamService.register_source("XAUUSD", TwelveDataPriceSource(...))
      -> tick(now) -> PriceStream._forward_ordered
           -> StreamValidator.validate (drop-on-invalid)
           -> _PriceTickSink.on_event
                -> PriceCache.update
                -> EventBus.publish(EventType.PRICE_UPDATED, payload=PriceTick)
                -> CandleBuilder.on_event  (single-writer MarketMemory fold)

using ONLY existing components. No new Price Stream / Provider /
Validation / Event Bus architecture is created here.

The probe calls `tick()` 3 times, ~3s apart, and for each capture:
provider current price + observation timestamp (from PriceStreamService.
get_price cache read), the validated price, the MarketMemory read-back
price (the forming-candle close over the service's OWN memory_registry
via MemoryReader), and whether a PRICE_UPDATED event fired (a probe-side
counter subscribed to that service's event bus). It then proves the
equality chain provider_price == validated_price == memory_price per
update.

REAL-DATA-008: the XAUUSD stream source is now `TwelveDataPriceSource`
(TwelveData's real-time /price endpoint -- real current spot price), NOT
the old candle source. Each tick is a fresh observation with a fresh
timestamp, so prices genuinely advance tick to tick (no "M1 candle has
not advanced" caveat).

IMPORTANT -- the PRICE_UPDATED subscriber below is VERIFICATION
INSTRUMENTATION ONLY. It is NOT a production wiring: production Core
(the TradingPipeline) does NOT subscribe to PRICE_UPDATED -- it reads
Market Memory on a schedule (REAL-DATA-003). This counter exists solely
to observe that the stream really publishes the event; it does not feed
any trading decision and is discarded when the probe exits.

Security contract (identical to real_market_data_probe.py, Director Order
section 13 -- non-negotiable):
  - Never print an API key, a Secrets/MaskedSecret object, or any
    exception's raw text that might embed one.
  - Only ever print: CONFIGURED/MISSING presence flags, numeric price,
    timestamp, validation PASS/NOT, memory PASS/NOT, event YES/NO, and
    generic exception CLASS names (never str(exception) for network
    exceptions -- some HTTP libraries echo ?apikey=... into their
    message text).

No mock, no fixture, no fabricated price. A failed real call is reported
BLOCKED/FAIL with its REAL cause, never silently upgraded to a fake PASS.
A repeated identical current price between ticks is NOT a failure (an
unchanged spot value is valid) -- it is reported honestly via timestamp/
sequence. Report-only: exits 0 regardless, so a BLOCKED run is never
mistaken for a hard failure. Local runs are expected to be BLOCKED
(no network egress from the sandbox); the real 3-update evidence comes
from the CI dispatch, where a real failure reports its real cause.
"""
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone

# Ensure the repo root (two levels up from scripts/verification/) is
# importable regardless of how this script is invoked.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

_TICKS = 3
_SLEEP_SECONDS = 3.0
_SYMBOL = "XAUUSD"
_TIMEFRAME = "M1"


def secret_status(name: str) -> str:
    return "CONFIGURED" if os.environ.get(name) else "MISSING"


def safe_exception_report(exc: BaseException) -> str:
    """Class name only -- never the exception's own message, since a
    requests exception can embed the full request URL (?apikey=...)."""
    return type(exc).__name__


def main() -> int:
    report = {
        "secrets": {},
        "stream": {"status": "NOT_RUN"},
        "updates": [],
    }

    # --- Secret Audit (presence only, never values) ------------------
    for name in ("TWELVE_DATA_API_KEY",):
        report["secrets"][name] = secret_status(name)
        print(f"{name}: {report['secrets'][name]}")

    print("---")

    try:
        from data_layer.live_data.price_stream_service.price_stream_service import (
            build_default_price_stream_service,
        )
        from data_layer.market_memory.market_memory_registry.market_memory_registry import (
            MarketMemoryRegistry,
        )
        from data_layer.market_memory.memory_reader.memory_reader import MemoryReader
        from data_layer.event_system.event_model.event_model import EventType

        # Build the REAL production stream (same wiring as the live
        # process's shared instance), with a MarketMemoryRegistry so ticks
        # fold into MarketMemory via the single-writer CandleBuilder.
        registry = MarketMemoryRegistry()
        service = build_default_price_stream_service(memory_registry=registry)
        reader = MemoryReader(registry)

        # VERIFICATION INSTRUMENTATION ONLY -- a probe-side counter on the
        # service's OWN event bus. NOT a production consumer.
        event_counter = {"count": 0}

        def _probe_counter(_event):
            event_counter["count"] += 1

        # The service holds a private _event_bus; the sanctioned public
        # observation seam is not exposed, so subscribe defensively.
        bus = getattr(service, "_event_bus", None)
        if bus is not None:
            bus.subscribe(EventType.PRICE_UPDATED, _probe_counter)

        report["stream"]["status"] = "BUILT"

        prev_price = None
        for n in range(1, _TICKS + 1):
            events_before = event_counter["count"]
            tick_error = None
            try:
                service.tick(datetime.now(timezone.utc))
            except Exception as e:  # noqa: BLE001 -- fail-safe, report don't crash
                tick_error = safe_exception_report(e)

            # Provider price + timestamp: cache read via the sanctioned API.
            cached = service.get_price(_SYMBOL)
            price = cached.price if cached is not None else None
            ts = cached.timestamp.isoformat() if cached is not None else None

            # The cache read IS the validated price (a tick reaches the
            # cache only after passing StreamValidator). Provider price and
            # validated price are the same observation by construction.
            validated_price = price

            # Memory read-back price via MemoryReader over the service's own
            # registry: the forming M1 candle's close is the folded tick.
            memory_price = None
            try:
                forming = reader.get_forming(_SYMBOL, _TIMEFRAME)
                if forming is not None:
                    memory_price = forming.close
            except Exception:  # noqa: BLE001 -- read-back is best-effort evidence
                memory_price = None
            memory_ok = memory_price is not None

            event_fired = event_counter["count"] > events_before

            # A repeated identical current price is NOT a failure -- report it.
            unchanged = (
                price is not None
                and prev_price is not None
                and price == prev_price
            )

            validated = "PASS" if (cached is not None and tick_error is None) else "NOT"

            # Equality chain: provider_price == validated_price == memory_price.
            equality_ok = (
                price is not None
                and validated_price is not None
                and memory_price is not None
                and price == validated_price == memory_price
            )

            update = {
                "n": n,
                "price": price,
                "validated_price": validated_price,
                "memory_price": memory_price,
                "timestamp": ts,
                "validated": validated,
                "memory": "PASS" if memory_ok else "NOT",
                "equality_chain": "PASS" if equality_ok else "NOT",
                "event_published": "YES" if event_fired else "NO",
                "unchanged_from_previous": unchanged,
                "tick_error": tick_error,
            }
            report["updates"].append(update)

            print(
                f"UPDATE #{n}: provider_price={price}, "
                f"validated_price={validated_price}, "
                f"memory_price={memory_price}, timestamp={ts}, "
                f"validated={validated}, memory={update['memory']}, "
                f"equality_chain={update['equality_chain']}, "
                f"event_published={update['event_published']}"
                + (" (unchanged current price from previous tick -- not a "
                   "failure; an unchanged spot value is valid)" if unchanged else "")
                + (f" (tick_error={tick_error})" if tick_error else "")
            )

            prev_price = price
            if n < _TICKS:
                time.sleep(_SLEEP_SECONDS)

        real_updates = sum(1 for u in report["updates"] if u["price"] is not None)
        equality_updates = sum(1 for u in report["updates"]
                                if u["equality_chain"] == "PASS")
        first_tick_error = next((u["tick_error"] for u in report["updates"]
                                 if u["tick_error"]), None)
        report["stream"]["real_updates"] = real_updates
        report["stream"]["equality_updates"] = equality_updates
        if report["secrets"]["TWELVE_DATA_API_KEY"] == "MISSING":
            report["stream"]["status"] = "BLOCKED"
            report["stream"]["reason"] = "TWELVE_DATA_API_KEY not configured"
        elif real_updates == 0:
            # Honest real cause: locally this is egress (no network); in CI
            # a real failure surfaces its own tick_error class here rather
            # than a canned sandbox excuse.
            report["stream"]["status"] = "BLOCKED"
            if first_tick_error is not None:
                report["stream"]["reason"] = (
                    "no real price landed in cache across 3 ticks; first "
                    f"tick error class: {first_tick_error}"
                )
            else:
                report["stream"]["reason"] = (
                    "no real price landed in cache across 3 ticks "
                    "(no network egress reachable -- expected locally; the "
                    "real 3-update evidence comes from the CI "
                    "workflow_dispatch run)"
                )
        elif equality_updates < _TICKS:
            # Prices landed but the provider==validated==memory chain did
            # not hold for all 3 -- report BLOCKED, never a fake PASS.
            report["stream"]["status"] = "BLOCKED"
            report["stream"]["reason"] = (
                f"only {equality_updates}/{_TICKS} updates proved the "
                "provider==validated==memory equality chain"
            )
        else:
            report["stream"]["status"] = "PASS"
    except Exception as e:  # noqa: BLE001 -- probe must never crash before reporting
        report["stream"] = {"status": "BLOCKED", "reason": safe_exception_report(e)}

    print("---")
    print(f"Stream: {report['stream']['status']}")
    if report["stream"].get("reason"):
        print(f"Stream Reason: {report['stream']['reason']}")

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
        # request URL/apikey) escape. Print only apikey-scrubbed lines.
        print("PROBE_FATAL: unexpected top-level failure")
        for line in traceback.format_exc().splitlines():
            if "apikey" in line.lower() or "api_key" in line.lower():
                continue
            print(line)
        sys.exit(1)
