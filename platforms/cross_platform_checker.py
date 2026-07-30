"""
Platform Layer — Cross Platform Checker (PLATFORM-001).

Same result/format shape as `configuration/feature_dependency_validator.py`
(this repo's established validator pattern): a frozen result dataclass
carrying a tuple of violations, plus a `format_*` text renderer. Never
raises, never enables/disables/corrects anything -- read-only, reports
whether a module's own capability declaration is internally complete.

Checks two rules against a module's `Dict[PlatformName, PlatformCapability]`
(from `platforms/capability_registry.py`):
1. Every `PlatformName` must have an entry -- an undeclared platform
   is itself a violation (the Director's "if it doesn't work, say why"
   requirement starts with "every platform must be addressed at all").
2. Every entry whose status is not `SUPPORTED` must carry a non-empty
   `reason`.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from platforms.capability_model import PlatformCapability, SupportStatus
from platforms.platform_model import PlatformName


@dataclass(frozen=True)
class CapabilityViolation:
    """platform: the PlatformName the violation concerns. issue: a human-readable description."""
    platform: PlatformName
    issue: str


@dataclass(frozen=True)
class CheckResult:
    """ok: True only when `violations` is empty."""
    ok: bool
    violations: Tuple[CapabilityViolation, ...]


def check_module_capabilities(
    capabilities: Dict[PlatformName, PlatformCapability],
) -> CheckResult:
    """Never raises: a missing platform or a missing reason is reported structurally as a violation, not an exception."""
    violations: List[CapabilityViolation] = []

    for platform in PlatformName:
        entry = capabilities.get(platform)
        if entry is None:
            violations.append(
                CapabilityViolation(platform=platform, issue="No capability declared for this platform.")
            )
            continue
        if entry.status != SupportStatus.SUPPORTED and not entry.reason:
            violations.append(
                CapabilityViolation(
                    platform=platform,
                    issue=f"Status {entry.status.value} declared with no reason.",
                )
            )

    return CheckResult(ok=(len(violations) == 0), violations=tuple(violations))


def format_capability_violations(result: CheckResult) -> str:
    """Text-format rendering matching this repo's own validator convention."""
    if result.ok:
        return "Complete cross-platform declaration -- no violations."

    lines = ["Incomplete cross-platform declaration:"]
    for violation in result.violations:
        lines.append(f"  {violation.platform.value}: {violation.issue}")
    return "\n".join(lines)
