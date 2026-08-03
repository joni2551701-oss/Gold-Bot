"""
Signals — Canonical Signal serializer (TASK-CORE-008 / STEP-08).

Turns a canonical signal (and, optionally, the derived views the STEP-08
pipeline produced around it) into a dict / JSON string every platform can
consume. It reuses SignalSchema.to_dict()/to_json() for the signal itself
rather than re-listing fields, and folds the optional strength / enrichment /
presentation / route views into one flat, JSON-native payload.

Pure formatting — no analysis, no decision, no I/O.
"""

import json
from typing import List, Optional

from signal_layer.signal_builder.schema import SignalSchema
from signal_layer.signal_scoring.quality import SignalStrength
from signal_layer.signal_builder.enricher import SignalEnrichment
from signal_layer.signal_formatter.formatter import SignalPresentation


def to_dict(signal: SignalSchema) -> dict:
    """The canonical signal alone, as a JSON-safe dict (reuses SignalSchema.to_dict)."""
    return signal.to_dict()


def to_json(signal: SignalSchema) -> str:
    """The canonical signal alone, as a JSON string (reuses SignalSchema.to_json)."""
    return signal.to_json()


def serialize_payload(
    signal: SignalSchema,
    *,
    strength: Optional[SignalStrength] = None,
    enrichment: Optional[SignalEnrichment] = None,
    presentation: Optional[SignalPresentation] = None,
    routes: Optional[List[str]] = None,
    lifecycle: Optional[str] = None,
) -> dict:
    """
    The full canonical payload: the signal plus whichever derived views the
    caller supplies. Every sub-view uses its own to_dict(); absent views are
    simply omitted (None), never faked.
    """
    payload = {"signal": signal.to_dict()}
    if strength is not None:
        payload["strength"] = strength.value
    if enrichment is not None:
        payload["enrichment"] = enrichment.to_dict()
    if presentation is not None:
        payload["presentation"] = presentation.to_dict()
    if routes is not None:
        payload["routes"] = list(routes)
    if lifecycle is not None:
        payload["lifecycle"] = lifecycle
    return payload


def payload_to_json(payload: dict) -> str:
    """Render a serialize_payload() dict to a JSON string."""
    return json.dumps(payload)
