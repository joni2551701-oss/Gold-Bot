"""core_layer/configuration/settings -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `settings.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `settings.py`.
"""
from core_layer.configuration.settings.settings import (
    dataclass,
    Config,
    Environment,
    resolve_environment,
    ApplicationSettings,
    build_settings_from_config,
)

__all__ = [
    "dataclass",
    "Config",
    "Environment",
    "resolve_environment",
    "ApplicationSettings",
    "build_settings_from_config",
]
