"""02_Core_Layer / Pipeline — core_layer.pipeline.

Foundation Freeze v1.0 — canonical architecture.

Migrated in Phase B.3 from the pre-freeze `core/pipeline.py`.
`TradingPipeline` is re-exported here so callers import the module rather
than the file inside it:

    from core_layer.pipeline import TradingPipeline

Per Stable Migration Rule (SMR-001) the moved file's internals are
unchanged — the Data→Context→Signal→AI→Decision→Risk→Telegram flow and the
notification-eligibility filter documented in this module are untouched.

Canonical documentation: 02_Core_Layer/Pipeline/README.md
"""

from core_layer.pipeline.pipeline import TradingPipeline

__all__ = ["TradingPipeline"]
