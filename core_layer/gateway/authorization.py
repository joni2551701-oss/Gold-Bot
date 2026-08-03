"""
Gateway authorization (v1.1 Phase 1, module 10).

Answers "may this principal use this service/capability?" -- an access
decision only, never a trading decision. An Authorizer returns True/False;
it never raises and never inspects payloads. Two foundation
implementations ship: allow-all and a role-based policy.

Imports only sibling gateway value types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional, Set

from core_layer.gateway.gateway_request import Principal


class Authorizer(ABC):
    @abstractmethod
    def authorize(self, principal: Principal, service: str,
                  capability: Optional[str] = None) -> bool:
        """Whether `principal` may call `service` (optionally `capability`)."""


class AllowAllAuthorizer(Authorizer):
    def authorize(self, principal: Principal, service: str,
                  capability: Optional[str] = None) -> bool:
        return True


class RoleAuthorizer(Authorizer):
    """
    Role-based policy. `policy` maps a service name to the set of roles
    allowed to call it. A service absent from the policy is open by default
    (open unless restricted); a service present requires one matching role.
    """

    def __init__(self, policy: Optional[Dict[str, Set[str]]] = None):
        self._policy = {k: set(v) for k, v in (policy or {}).items()}

    def set_policy(self, service: str, roles: Set[str]) -> None:
        self._policy[service] = set(roles)

    def authorize(self, principal: Principal, service: str,
                  capability: Optional[str] = None) -> bool:
        required = self._policy.get(service)
        if required is None:
            return True                      # not restricted
        return any(principal.has_role(r) for r in required)
