"""
Bootstrap state and strategy enums (v1.1 Phase 1, module 5).

DD-058 (Bootstrap Strategy) and the per-timeframe lifecycle states,
including CANCELLED (DD-055). This module never imports from any layer
above data/.
"""

from __future__ import annotations

from enum import Enum


class BootstrapState(Enum):
    """Per-timeframe (and aggregate) bootstrap lifecycle state."""
    PENDING = "pending"
    LOADING = "loading"
    VALIDATING = "validating"
    HYDRATING = "hydrating"
    READY = "ready"
    FAILED = "failed"
    CANCELLED = "cancelled"     # DD-055


class BootstrapStrategy(Enum):
    """
    How an asset is bootstrapped (DD-058).

    - AUTO: warm restart from cache when fresh, else incremental, else
      cold load. The production default.
    - FULL: always fetch full recent history (ignore cache). Development.
    - INCREMENTAL: fetch only the delta since the last known candle.
    - RECOVERY_ONLY: do not load fresh history; only gap-fill existing
      memory. For post-outage recovery.
    - CACHE_ONLY: load from cache only; never call the provider.
    """
    AUTO = "auto"
    FULL = "full"
    INCREMENTAL = "incremental"
    RECOVERY_ONLY = "recovery_only"
    CACHE_ONLY = "cache_only"
