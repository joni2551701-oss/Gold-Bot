"""
MemoryCodec -- serialize/restore a MarketMemory to/from bytes, with schema
versioning (DD-070) and optional compression. v1.1 Phase 1, module 6.

Serializes each timeframe's CLOSED candles (OHLC + timestamp + volume);
the extended CandleRecord fields (sequence, source, ...) are regenerated
on restore via Module 1 hydrate, so the durable form stays small and
provider-independent. Deterministic (canonical ordering) so a snapshot is
reproducible and hashable.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from data_layer.providers.twelve_data_client import Candle
from data_layer.market_memory.market_memory import MarketMemory

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class SnapshotMetadata:
    """Per-snapshot metadata (DD-070)."""
    asset: str
    timeframe_count: int
    candle_count: int
    schema_version: int
    created_at: datetime
    bootstrap_version: str
    integrity_hash: str

    def as_dict(self) -> dict:
        return {
            "asset": self.asset,
            "timeframe_count": self.timeframe_count,
            "candle_count": self.candle_count,
            "schema_version": self.schema_version,
            "created_at": self.created_at.isoformat(),
            "bootstrap_version": self.bootstrap_version,
            "integrity_hash": self.integrity_hash,
        }


def _candle_to_dict(c: Candle) -> dict:
    return {"t": c.timestamp.isoformat(), "o": c.open, "h": c.high,
            "l": c.low, "c": c.close}


def _dict_to_candle(d: dict) -> Candle:
    ts = datetime.fromisoformat(d["t"])
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return Candle(timestamp=ts, open=d["o"], high=d["h"], low=d["l"],
                  close=d["c"])


class MemoryCodec:
    """Serializes MarketMemory to versioned, optionally gzipped bytes."""

    def __init__(self, compress: bool = True):
        self._compress = compress

    def _timeframe_payload(self, memory: MarketMemory) -> Dict[str, List[dict]]:
        out: Dict[str, List[dict]] = {}
        for tf in memory.timeframes():
            out[tf] = [_candle_to_dict(rec.to_candle())
                       for rec in memory.timeframe(tf).get_series()]
        return out

    @staticmethod
    def _hash(tf_payload: Dict[str, List[dict]]) -> str:
        canonical = json.dumps(tf_payload, sort_keys=True,
                               separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def serialize(self, memory: MarketMemory, now: datetime,
                  bootstrap_version: str = "") -> Tuple[bytes, SnapshotMetadata]:
        tf_payload = self._timeframe_payload(memory)
        candle_count = sum(len(v) for v in tf_payload.values())
        integrity_hash = self._hash(tf_payload)
        meta = SnapshotMetadata(
            asset=memory.asset,
            timeframe_count=len(tf_payload),
            candle_count=candle_count,
            schema_version=SCHEMA_VERSION,
            created_at=now,
            bootstrap_version=bootstrap_version,
            integrity_hash=integrity_hash,
        )
        doc = {"schema_version": SCHEMA_VERSION,
               "metadata": meta.as_dict(),
               "timeframes": tf_payload}
        raw = json.dumps(doc, separators=(",", ":")).encode("utf-8")
        return (gzip.compress(raw) if self._compress else raw), meta

    def deserialize(self, data: bytes
                    ) -> Tuple[SnapshotMetadata, Dict[str, List[Candle]]]:
        raw = self._maybe_decompress(data)
        doc = json.loads(raw.decode("utf-8"))
        version = doc.get("schema_version")
        if version != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported snapshot schema_version {version!r} "
                f"(expected {SCHEMA_VERSION}) -- migration required")
        m = doc["metadata"]
        meta = SnapshotMetadata(
            asset=m["asset"], timeframe_count=m["timeframe_count"],
            candle_count=m["candle_count"], schema_version=m["schema_version"],
            created_at=datetime.fromisoformat(m["created_at"]),
            bootstrap_version=m.get("bootstrap_version", ""),
            integrity_hash=m["integrity_hash"])
        timeframes = {tf: [_dict_to_candle(d) for d in candles]
                      for tf, candles in doc["timeframes"].items()}
        return meta, timeframes

    def verify_hash(self, meta: SnapshotMetadata,
                    timeframes: Dict[str, List[Candle]]) -> bool:
        tf_payload = {tf: [_candle_to_dict(c) for c in candles]
                      for tf, candles in timeframes.items()}
        return self._hash(tf_payload) == meta.integrity_hash

    @staticmethod
    def _maybe_decompress(data: bytes) -> bytes:
        if len(data) >= 2 and data[0] == 0x1F and data[1] == 0x8B:  # gzip magic
            return gzip.decompress(data)
        return data
