"""
Gateway version service (v1.1 Phase 1, module 10).

Serves the Core version and the Gateway API version so platforms can check
compatibility before they call. Kept as independent constants rather than
importing another module's version string, so the Gateway carries no
upward dependency (same independent-constant pattern used elsewhere in
`core/`); reconciling these with any other version source, should they ever
need to agree, is a future explicit decision.

Imports nothing from the repo.
"""

from __future__ import annotations

from typing import Dict

CORE_VERSION = "1.1.0"          # v1.1 Phase 1 Core Infrastructure
GATEWAY_API_VERSION = "1.0"     # the Gateway's external contract version


class VersionService:
    def __init__(self, core_version: str = CORE_VERSION,
                 api_version: str = GATEWAY_API_VERSION):
        self.core_version = core_version
        self.api_version = api_version

    def info(self) -> Dict[str, str]:
        return {"core_version": self.core_version,
                "api_version": self.api_version}
