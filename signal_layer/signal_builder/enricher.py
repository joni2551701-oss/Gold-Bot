"""
Signals — Canonical Signal enricher (TASK-CORE-008 / STEP-08).

Attaches already-computed environmental metadata to a canonical signal:
current price, spread, session, volatility, regime, a build timestamp and a
build version. It READS these values from optional upstream objects
(MarketSnapshot / CurrentPrice / a session or regime label) — it never
recomputes structure, liquidity, regime, or volatility itself, and it sizes
no risk.

Two outputs, both additive and non-destructive:
1. A SignalEnrichment record (the free-form environmental detail the frozen
   A15 SignalSchema has no fields for — carried alongside, per the STEP-08
   reuse-first decision, rather than by extending SignalSchema).
2. A copy of the SignalSchema with its EXISTING optional fields (session,
   market_phase, asset_type) filled in when a caller supplies them —
   produced with dataclasses.replace so the original frozen instance is
   never mutated.
"""

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional, Tuple

from signal_layer.signal_builder.schema import SignalSchema

BUILD_VERSION = "signals-canonical/1.0"


@dataclass(frozen=True)
class SignalEnrichment:
    """Environmental metadata for one canonical signal — all reads, never computed here."""
    build_version: str = BUILD_VERSION
    enriched_at: Optional[datetime] = None
    current_price: Optional[float] = None
    spread: Optional[float] = None
    session: Optional[str] = None
    volatility: Optional[str] = None
    regime: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "build_version": self.build_version,
            "enriched_at": self.enriched_at.isoformat() if self.enriched_at else None,
            "current_price": self.current_price,
            "spread": self.spread,
            "session": self.session,
            "volatility": self.volatility,
            "regime": self.regime,
        }


def enrich(
    signal: SignalSchema,
    *,
    current_price: Optional[float] = None,
    spread: Optional[float] = None,
    session: Optional[str] = None,
    volatility: Optional[str] = None,
    regime: Optional[str] = None,
    market_phase: Optional[str] = None,
    asset_type: Optional[str] = None,
) -> Tuple[SignalSchema, SignalEnrichment]:
    """
    Return (enriched_signal, enrichment). The enriched_signal is a copy of
    `signal` with session/market_phase/asset_type filled in only where the
    caller supplied a value AND the field was still None (never overwrites an
    already-set field). Pure — reads its inputs, computes nothing about the
    market.
    """
    updates = {}
    if session is not None and signal.session is None:
        updates["session"] = session
    if market_phase is not None and signal.market_phase is None:
        updates["market_phase"] = market_phase
    if asset_type is not None and signal.asset_type is None:
        updates["asset_type"] = asset_type

    enriched = replace(signal, **updates) if updates else signal

    enrichment = SignalEnrichment(
        build_version=BUILD_VERSION,
        enriched_at=datetime.now(timezone.utc),
        current_price=current_price,
        spread=spread,
        session=session if session is not None else signal.session,
        volatility=volatility,
        regime=regime,
    )
    return enriched, enrichment
