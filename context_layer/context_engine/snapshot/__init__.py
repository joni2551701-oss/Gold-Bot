"""context_layer/context_engine/snapshot -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `snapshot.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `snapshot.py`.
"""
from context_layer.context_engine.snapshot.snapshot import (
    json,
    uuid,
    asdict,
    dataclass,
    field,
    datetime,
    timezone,
    List,
    Optional,
    ContextSnapshot,
    most_recent_bias,
    ALLOWED_REGIMES,
    StructureInfo,
    LiquidityInfo,
    ZonesInfo,
    SessionInfo,
    SnapshotMetadata,
    ContextSnapshotSchema,
    generate_snapshot_id,
    ValidationResult,
    validate_snapshot,
    from_context_snapshot,
)

__all__ = [
    "json",
    "uuid",
    "asdict",
    "dataclass",
    "field",
    "datetime",
    "timezone",
    "List",
    "Optional",
    "ContextSnapshot",
    "most_recent_bias",
    "ALLOWED_REGIMES",
    "StructureInfo",
    "LiquidityInfo",
    "ZonesInfo",
    "SessionInfo",
    "SnapshotMetadata",
    "ContextSnapshotSchema",
    "generate_snapshot_id",
    "ValidationResult",
    "validate_snapshot",
    "from_context_snapshot",
]
