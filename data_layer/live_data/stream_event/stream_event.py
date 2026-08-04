"""
Stream models -- StreamEvent and the state/status/capability value types
for the Price Stream (v1.1 Phase 1, module 4).

`StreamEvent` is the single unit the stream produces and the
CandleBuilder (module 3) consumes; it is frozen/immutable and satisfies
`CandleBuilder.on_event` exactly. Replay (module 8) emits the same type
with `source=REPLAY`.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from data_layer.market_memory.candle_record import CandleSource


class StreamState(Enum):
    """Market lifecycle states (DD-046)."""
    INITIALIZING = "initializing"
    CONNECTING = "connecting"
    STREAMING = "streaming"
    WAITING_FOR_MARKET = "waiting_for_market"
    RECONNECTING = "reconnecting"
    SHUTDOWN = "shutdown"


class ProviderStatus(Enum):
    """Standardized provider status (DD-048/DD-051)."""
    UP = "up"
    DOWN = "down"
    MARKET_CLOSED = "market_closed"
    RATE_LIMITED = "rate_limited"


class AssetClass(Enum):
    """
    Asset class drives waiting-mode behavior (DD-047): CRYPTO trades 24/7
    and never enters waiting mode; METAL/FOREX honor a market calendar.
    """
    METAL = "metal"
    FOREX = "forex"
    CRYPTO = "crypto"


@dataclass(frozen=True)
class ProviderCapabilities:
    """
    What a provider can do (DD-049). PriceStream reads capabilities rather
    than guessing the provider type.
    """
    supports_streaming: bool = False
    supports_polling: bool = False
    supports_replay: bool = False
    supports_historical: bool = False
    supports_volume: bool = False


@dataclass(frozen=True)
class ProviderHealth:
    """Standardized provider health snapshot (DD-051)."""
    status: ProviderStatus
    detail: str = ""
    last_error: Optional[str] = None


@dataclass(frozen=True)
class StreamEvent:
    """One price observation. Immutable; consumed by CandleBuilder.on_event."""
    asset: str
    price: float
    timestamp: datetime            # UTC, timezone-aware
    volume: Optional[float] = None
    source: CandleSource = CandleSource.STREAM
