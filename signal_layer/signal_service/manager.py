"""
Signals — Canonical Signal manager / orchestrator (TASK-CORE-008 / STEP-08).

SignalManager is the one entry point of the signals/ layer. It runs the
STEP-08 pipeline over a setup-layer StrategyResult and returns a canonical
signal ready for any consumer:

    StrategyResult -> precheck -> build (SignalSchema) -> validate ->
        strength -> enrich -> format -> serialize -> route -> lifecycle
                                                              -> CanonicalSignalResult

It composes the existing/new signals/ pieces (schema.SignalSchema +
validate_signal, quality, enricher, formatter, serializer, router, lifecycle)
and REUSES signals.schema for the canonical model rather than defining a
second one (STEP-08 reuse-first decision). The live signal_engine.py /
SignalCandidate path is untouched and unimported.

Strict boundary — this layer does NOT: compute market structure, choose a
strategy, size risk, make a decision, send to a platform, or read secrets.
The StrategyResult is read duck-typed (same discipline as
strategies.result.from_signal_candidate), so an empty/None/partial result
yields a defined INVALID CanonicalSignalResult, never a raise.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from signal_layer.signal_engine.base import SignalContract
from signal_layer.signal_builder.schema import SignalSchema, ValidationResult, generate_signal_id
from signal_layer.signal_validator import validator as _validator
from signal_layer.signal_scoring import quality as _quality
from signal_layer.signal_builder import enricher as _enricher
from signal_layer.signal_formatter import formatter as _formatter
from signal_layer.signal_formatter import serializer as _serializer
from signal_layer.signal_service import router as _router
from signal_layer.signal_engine.lifecycle.state import CanonicalSignalStatus

_DIRECTION_MAP = {"LONG": "BUY", "SHORT": "SELL", "NEUTRAL": "NONE"}


@dataclass(frozen=True)
class CanonicalSignalResult:
    """
    The complete STEP-08 output for one setup: the canonical signal plus every
    derived view. `signal` is THE canonical model (SignalSchema) consumers
    read; the rest are optional decorations.
    """
    signal: SignalSchema
    validation: ValidationResult
    strength: _quality.SignalStrength
    status: CanonicalSignalStatus
    enrichment: Optional[_enricher.SignalEnrichment] = None
    presentation: Optional[_formatter.SignalPresentation] = None
    routes: List[str] = field(default_factory=list)
    is_duplicate: bool = False

    @property
    def is_valid(self) -> bool:
        return self.validation.valid and not self.is_duplicate

    def to_payload(self) -> dict:
        """Flat, JSON-native payload for any platform (reuses serializer)."""
        return _serializer.serialize_payload(
            self.signal,
            strength=self.strength,
            enrichment=self.enrichment,
            presentation=self.presentation,
            routes=self.routes,
            lifecycle=self.status.value,
        )


def _entry_from_zone(entry_zone) -> Optional[float]:
    """Midpoint of a (low, high) entry band, or None. Pure read, no computation of structure."""
    if not entry_zone:
        return None
    try:
        low, high = entry_zone
    except (TypeError, ValueError):
        return None
    if low is None or high is None:
        return None
    return round((low + high) / 2.0, 5)


def _derive_take_profit(direction: str, entry, stop, rr) -> Optional[float]:
    """
    Target implied by the setup's OWN reward/risk geometry: tp = entry +/-
    rr * risk. This is descriptive geometry (the inverse of
    strategies.result.compute_rr), NOT risk sizing — no lot size, no account
    risk. None when inputs are missing or the stop distance is degenerate.
    """
    if direction not in ("BUY", "SELL") or None in (entry, stop, rr):
        return None
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    return round(entry + rr * risk, 5) if direction == "BUY" else round(entry - rr * risk, 5)


class SignalManager(SignalContract):
    """Orchestrates the signals/ canonical pipeline. Stateless except for an optional dedup guard."""

    def __init__(self, deduplicator: Optional[_validator.SignalDeduplicator] = None) -> None:
        self._dedup = deduplicator if deduplicator is not None else _validator.SignalDeduplicator()

    # -- SignalContract ---------------------------------------------------

    def validate(self, source) -> ValidationResult:
        """Precheck a StrategyResult carries the minimum a signal needs (never raises)."""
        direction = _DIRECTION_MAP.get(getattr(getattr(source, "direction", None), "name", ""), None)
        entry = _entry_from_zone(getattr(source, "entry_zone", None))
        return _validator.precheck_source(
            # only an actionable BUY/SELL counts as a present direction here
            direction=direction if direction in ("BUY", "SELL") else None,
            entry=entry,
            strategy=getattr(source, "strategy_name", None),
            confidence=getattr(source, "confidence", None),
            rr=getattr(source, "rr", None),
        )

    def build(
        self,
        source,
        *,
        symbol: str = "XAUUSD",
        timeframe: str = "M15",
        session: Optional[str] = None,
        market_phase: Optional[str] = None,
        asset_type: Optional[str] = None,
        current_price: Optional[float] = None,
        spread: Optional[float] = None,
        volatility: Optional[str] = None,
        regime: Optional[str] = None,
    ) -> CanonicalSignalResult:
        """
        Run the full pipeline for one StrategyResult. Always returns a
        CanonicalSignalResult — a missing/empty/invalid setup yields an
        INVALID one (status CREATED), never an exception.
        """
        direction = _DIRECTION_MAP.get(getattr(getattr(source, "direction", None), "name", ""), "NONE")
        confidence = float(getattr(source, "confidence", 0.0) or 0.0)
        rr = getattr(source, "rr", None)
        entry = _entry_from_zone(getattr(source, "entry_zone", None))
        stop = getattr(source, "invalidation", None)
        take_profit = _derive_take_profit(direction, entry, stop, rr)
        has_setup = bool(getattr(source, "has_setup", False))
        reasons = list(getattr(source, "reasons", []) or [])

        signal = SignalSchema(
            signal_id=generate_signal_id(),
            created_at=datetime.now(timezone.utc),
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            asset_type=asset_type,
            session=session,
            market_phase=market_phase,
            entry_price=entry,
            stop_loss=stop,
            take_profit=take_profit,
            strategy_name=getattr(source, "strategy_name", None),
            confidence_score=confidence,
        )

        # validate: setup precheck (direction/entry/strategy/confidence/rr) +
        # structural schema check (price ordering) + a real setup present.
        precheck = self.validate(source)
        structural = _validator.validate(signal)
        errors = list(precheck.errors) + list(structural.errors)
        if not has_setup:
            errors.append("no setup (StrategyResult carries no SETUP_FOUND)")
        validation = ValidationResult(valid=len(errors) == 0, errors=errors)

        is_dup = self._dedup.is_duplicate(signal)
        status = CanonicalSignalStatus.CREATED

        # strength
        strength = _quality.assess(confidence, rr, has_setup=has_setup)
        if not validation.valid:
            strength = _quality.SignalStrength.INVALID

        enrichment = None
        presentation = None
        routes: List[str] = []

        if validation.valid and not is_dup:
            status = CanonicalSignalStatus.VALIDATED
            signal, enrichment = _enricher.enrich(
                signal,
                current_price=current_price,
                spread=spread,
                session=session,
                volatility=volatility,
                regime=regime,
                market_phase=market_phase,
                asset_type=asset_type,
            )
            status = CanonicalSignalStatus.ENRICHED
            presentation = _formatter.format_signal(signal, strength=strength, reasons=reasons)
            routes = _router.route_values(signal)
            status = CanonicalSignalStatus.READY
            self._dedup.register(signal)

        return CanonicalSignalResult(
            signal=signal,
            validation=validation,
            strength=strength,
            status=status,
            enrichment=enrichment,
            presentation=presentation,
            routes=routes,
            is_duplicate=is_dup,
        )

    def serialize(self, built: CanonicalSignalResult) -> dict:
        """Platform-independent payload for a built result (reuses serializer)."""
        return built.to_payload()
