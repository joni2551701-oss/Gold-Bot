from assistant.identity import AssistantIdentity
from assistant.identity_manager import IdentityManager
from assistant.identity_registry import SENIOR_IDENTITY, SENIORITA_IDENTITY


def test_identity_manager_default_registry_get():
    manager = IdentityManager()
    assert manager.get("Senior") == SENIOR_IDENTITY
    assert manager.get("Seniorita") == SENIORITA_IDENTITY


def test_identity_manager_get_unknown_returns_none():
    manager = IdentityManager()
    assert manager.get("Nonexistent") is None


def test_identity_manager_exists():
    manager = IdentityManager()
    assert manager.exists("Senior") is True
    assert manager.exists("Nonexistent") is False


def test_identity_manager_default_returns_senior():
    manager = IdentityManager()
    assert manager.default() == SENIOR_IDENTITY


def test_identity_manager_default_falls_back_when_senior_excluded():
    custom = [SENIORITA_IDENTITY]
    manager = IdentityManager(identities=custom)
    assert manager.default() == SENIOR_IDENTITY


def test_identity_manager_all_returns_every_registered_identity():
    manager = IdentityManager()
    names = {i.name for i in manager.all()}
    assert names == {"Senior", "Seniorita"}


def test_identity_manager_injectable_custom_registry():
    custom_identity = AssistantIdentity(
        name="Custom", display_name="Custom", description="x", default_voice="Custom", default_avatar="custom_avatar",
    )
    manager = IdentityManager(identities=[custom_identity])
    assert manager.get("Custom") == custom_identity
    assert manager.exists("Senior") is False
