"""
Gateway authentication (v1.1 Phase 1, module 10).

Answers "who is calling?" -- identity only, never trading authority. An
Authenticator turns a request into a Principal (or None if it cannot be
identified). Two foundation implementations ship: allow-all (development /
internal use) and a token map. Real credential backends plug in later
behind the same interface.

Imports only sibling gateway value types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional

from core_layer.gateway.gateway_request import GatewayRequest, Principal, ANONYMOUS


class Authenticator(ABC):
    @abstractmethod
    def authenticate(self, request: GatewayRequest) -> Optional[Principal]:
        """Return the calling Principal, or None if not identifiable."""


class AllowAllAuthenticator(Authenticator):
    """Every request is the anonymous-but-authenticated principal."""

    def __init__(self, principal: Optional[Principal] = None):
        self._principal = principal or Principal(
            id="anonymous", authenticated=True)

    def authenticate(self, request: GatewayRequest) -> Optional[Principal]:
        return self._principal


class TokenAuthenticator(Authenticator):
    """Map an opaque token to a Principal; unknown/absent token -> None."""

    def __init__(self, tokens: Optional[Dict[str, Principal]] = None):
        self._tokens = dict(tokens or {})

    def register_token(self, token: str, principal: Principal) -> None:
        self._tokens[token] = principal

    def authenticate(self, request: GatewayRequest) -> Optional[Principal]:
        if not request.token:
            return None
        return self._tokens.get(request.token)


__all__ = ["Authenticator", "AllowAllAuthenticator", "TokenAuthenticator",
           "ANONYMOUS"]
