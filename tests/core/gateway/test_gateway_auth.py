"""Tests for Gateway authentication + authorization (module 10)."""

from core.gateway.authentication import (
    AllowAllAuthenticator, TokenAuthenticator,
)
from core.gateway.authorization import AllowAllAuthorizer, RoleAuthorizer

from _gfakes import request, principal


# -- authentication -----------------------------------------------------
def test_allow_all_authenticator():
    auth = AllowAllAuthenticator()
    p = auth.authenticate(request("svc"))
    assert p is not None and p.authenticated


def test_token_authenticator_known():
    admin = principal("admin", roles=("admin",))
    auth = TokenAuthenticator({"tok-1": admin})
    assert auth.authenticate(request("svc", token="tok-1")) is admin


def test_token_authenticator_unknown_and_absent():
    auth = TokenAuthenticator({"tok-1": principal("admin")})
    assert auth.authenticate(request("svc", token="bad")) is None
    assert auth.authenticate(request("svc")) is None       # no token


# -- authorization ------------------------------------------------------
def test_allow_all_authorizer():
    assert AllowAllAuthorizer().authorize(principal(), "svc") is True


def test_role_authorizer_open_when_unrestricted():
    authz = RoleAuthorizer({"admin_svc": {"admin"}})
    assert authz.authorize(principal(roles=()), "public_svc") is True


def test_role_authorizer_enforces_role():
    authz = RoleAuthorizer({"admin_svc": {"admin"}})
    assert authz.authorize(principal(roles=("admin",)), "admin_svc") is True
    assert authz.authorize(principal(roles=("user",)), "admin_svc") is False
