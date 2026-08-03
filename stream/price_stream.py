"""
Stream Layer — Price Stream (TASK-CORE-004).

PriceStream is the composition root of the stream layer: it takes raw
provider output and drives it through the mandated flow before any
consumer sees it —

    raw candle/event
        → StreamEvent (never route raw data directly)
        → StreamValidator (drop invalid)
        → StreamState + CurrentPrice (update runtime state)
        → StreamRouter → subscribers

Mode gating: when the resolved StreamMode is not ACTIVE (weekend,
market closed, paused, manual hold), data events are NOT routed — the
mode is recorded in state and the stream simply waits. This is the
"weekend/pause pauses the stream without breaking the system" rule.

Provider integration: `poll()` is an optional convenience that pulls
the latest candle from a data_layer.providers ProviderManager's active
provider (the FROZEN provider layer) and ingests it. PriceStream never
reaches into a provider's internals, never reads a secret, and never
reads .env — it only calls the frozen public methods. It performs NO
signal/strategy/decision/risk/execution/UI logic.
"""

from datetime import datetime
from typing import List, Optional

from stream.current_price import CurrentPrice
from stream.stream_event import StreamEvent
from stream.stream_mode import StreamMode, resolve_mode
from stream.stream_router import RouteResult, StreamRouter
from stream.stream_state import StreamState
from stream.stream_subscriber import StreamSubscriber
from stream.stream_validator import StreamValidator, ValidationResult


class IngestResult:
    """
    Outcome of ingesting one candle/event: the built event (or None if
    dropped), the validation result, the resolved mode, whether it was
    routed, and the RouteResult when it was.
    """

    def __init__(self, event: Optional[StreamEvent], validation: ValidationResult,
                 mode: StreamMode, routed: bool, route_result: Optional[RouteResult]) -> None:
        self.event = event
        self.validation = validation
        self.mode = mode
        self.routed = routed
        self.route_result = route_result

    @property
    def accepted(self) -> bool:
        """True when the event passed validation (whether or not the mode allowed routing)."""
        return bool(self.validation)


class PriceStream:
    """
    Wires validator + state + current price + router into one flow.
    Every collaborator is injectable for tests; sensible defaults are
    constructed otherwise. Never raises for a data-driven condition.
    """

    def __init__(self, router: Optional[StreamRouter] = None,
                 validator: Optional[StreamValidator] = None,
                 state: Optional[StreamState] = None,
                 current_price: Optional[CurrentPrice] = None) -> None:
        self.router = router or StreamRouter()
        self.validator = validator or StreamValidator()
        self.state = state or StreamState()
        self.current_price = current_price or CurrentPrice()

    def subscribe(self, subscriber: StreamSubscriber) -> None:
        """Attach a consumer (delegates to the router)."""
        self.router.subscribe(subscriber)

    def ingest_event(self, event: Optional[StreamEvent], *, manual_hold: bool = False,
                     paused: bool = False, expected_symbol: Optional[str] = None,
                     now: Optional[datetime] = None) -> IngestResult:
        """
        Run one StreamEvent through the full flow. Validates against the
        previous event (duplicate/sequence). On invalid, returns early
        without touching state/router. On valid, updates state +
        current price always, and routes only when the resolved mode is
        ACTIVE. `now` (optional) drives both the weekend/pause clock and
        the future-timestamp check -- a replay/backtest or a test can
        pin it; production leaves it None (real UTC). Never raises.
        """
        mode = resolve_mode(now=now, manual_hold=manual_hold, paused=paused)

        validation = self.validator.validate(
            event, previous=self.state.last_event, expected_symbol=expected_symbol, now=now
        )
        if not validation:
            # Record the mode even when data is dropped, so a status
            # view reflects e.g. WEEKEND_WAIT during bad-data periods.
            self.state.update(mode=mode)
            return IngestResult(event, validation, mode, routed=False, route_result=None)

        # Valid: update runtime state + current price (always), then
        # route only if the market/mode is actively flowing.
        self.state.update(event=event, mode=mode)
        self.current_price.update_from_event(event)

        if mode.is_flowing():
            route_result = self.router.route(event)
            return IngestResult(event, validation, mode, routed=True, route_result=route_result)
        return IngestResult(event, validation, mode, routed=False, route_result=None)

    def ingest_candle(self, candle, *, source: str = "provider", manual_hold: bool = False,
                      paused: bool = False, expected_symbol: Optional[str] = None,
                      now: Optional[datetime] = None) -> IngestResult:
        """Adapt a data_layer.providers MarketCandle to a StreamEvent, then ingest it. `source` labels the origin."""
        event = StreamEvent.from_candle(candle, source=source)
        return self.ingest_event(event, manual_hold=manual_hold, paused=paused,
                                 expected_symbol=expected_symbol, now=now)

    def poll(self, provider_manager, symbol: str, timeframe: str, limit: int = 1,
             **mode_kwargs) -> List[IngestResult]:
        """
        Optional live-pull convenience: fetch the most recent candle(s)
        for `symbol`/`timeframe` from the ProviderManager's active
        provider (FROZEN provider layer) and ingest each. Returns []
        when no provider is available or no data is returned -- never
        raises for those data-driven conditions. `source="poll"` labels
        these events so a future WebSocket path ("live") is
        distinguishable.
        """
        provider = provider_manager.resolve(symbol)
        if provider is None:
            return []
        try:
            candles = provider.get_candles(symbol, timeframe, limit)
        except NotImplementedError:
            # A stub provider (e.g. an inert Bitget/Keynorq) -- honest
            # "no live data", not an error condition for the stream.
            return []
        results: List[IngestResult] = []
        for candle in candles or []:
            results.append(self.ingest_candle(candle, source="poll", **mode_kwargs))
        return results
