"""02_Core_Layer / Secrets — goldbot.core_layer.secrets.

Foundation Freeze v1.0 — canonical architecture.

Migrated in Phase B.2 from the pre-freeze `core/secrets.py`. `Secrets` is
re-exported here so callers import the module rather than the file inside
it:

    from goldbot.core_layer.secrets import Secrets

Per Stable Migration Rule (SMR-001) the moved file's internals are
unchanged. This module's documented scope also covers secret rotation and
the `MaskedSecret` value type currently living in `config.py`; folding
those in is deferred to the post-migration refactoring step (KG-001 /
RT-001 / RT-002) rather than mixed into a migration commit.

Canonical documentation: 02_Core_Layer/Secrets/README.md
"""

from goldbot.core_layer.secrets.secrets import Secrets

__all__ = ["Secrets"]
