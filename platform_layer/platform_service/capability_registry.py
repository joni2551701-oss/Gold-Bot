"""
Platform Layer — module capability registry (PLATFORM-001).

Same registry pattern as `platform_layer/platform_service/platform_registry.py`/
`assets/asset_registry.py`. Keyed by module name (a free-text string
identifying whatever module is declaring its cross-platform support --
e.g. "platform_layer.telegram.signal_access_service" -- not a Python import path
requirement, just a stable label), each value a full
`Dict[PlatformName, PlatformCapability]` covering every platform.

Never imports `telegram/`, `database/`, or any Trading Core package --
this stores declarations, it does not run or gate anything.
"""

from typing import Dict, List, Optional

from platform_layer.platform_service.capability_model import PlatformCapability
from platform_layer.platform_service.platform_model import PlatformName


class DuplicateModuleCapabilityError(ValueError):
    """Raised by register() when the module name is already present in the registry."""


class ModuleCapabilityRegistry:
    def __init__(self) -> None:
        self._declarations: Dict[str, Dict[PlatformName, PlatformCapability]] = {}

    def register(self, module_name: str, capabilities: Dict[PlatformName, PlatformCapability]) -> None:
        """Raises DuplicateModuleCapabilityError if module_name is already registered."""
        if module_name in self._declarations:
            raise DuplicateModuleCapabilityError(
                f"Module capability already registered: {module_name}"
            )
        self._declarations[module_name] = dict(capabilities)

    def get(self, module_name: str) -> Optional[Dict[PlatformName, PlatformCapability]]:
        """Returns None if module_name was never registered -- never raises."""
        return self._declarations.get(module_name)

    def list(self) -> List[str]:
        """Every registered module name."""
        return list(self._declarations.keys())
