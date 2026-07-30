"""PLATFORM-001 -- Universal Navigation model foundation tests (platforms/). TASK-002C adds is_valid_screen_id()/category/content_type tests (ADR-002)."""

from platforms.navigation_model import NavigationNode, is_valid_screen_id
from platforms.platform_model import PlatformName


def test_navigation_node_defaults():
    node = NavigationNode(id="main.home", label_key="menu.main", permission="USER")
    assert node.platforms == []
    assert node.children == []
    assert node.category is None
    assert node.content_type is None


def test_navigation_node_accepts_category_and_content_type():
    node = NavigationNode(
        id="signals.list",
        label_key="menu.signals",
        permission="USER",
        category="signals",
        content_type="list",
    )
    assert node.category == "signals"
    assert node.content_type == "list"


def test_is_valid_screen_id_accepts_adr002_examples():
    for screen_id in ("dashboard.home", "dashboard.analytics", "signals.list", "signals.details", "settings.main", "settings.notifications", "profile.main"):
        assert is_valid_screen_id(screen_id) is True


def test_is_valid_screen_id_rejects_malformed_ids():
    for bad in ("", "settings", "Settings.Main", "settings.", ".settings", "settings..main", "settings main", None, 123):
        assert is_valid_screen_id(bad) is False


def test_navigation_node_nests_children():
    child = NavigationNode(id="settings.language", label_key="rkm.language", permission="USER")
    root = NavigationNode(
        id="settings",
        label_key="rkm.settings",
        permission="USER",
        platforms=[PlatformName.TELEGRAM_BOT],
        children=[child],
    )

    assert root.children == [child]
    assert root.platforms == [PlatformName.TELEGRAM_BOT]


def test_navigation_model_source_has_no_telegram_or_database_import():
    """Static check: this contract file itself never imports telegram/ or database/, per its own docstring."""
    import ast
    import inspect

    import platforms.navigation_model as module

    tree = ast.parse(inspect.getsource(module))
    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])

    assert "telegram" not in imported_roots
    assert "database" not in imported_roots
