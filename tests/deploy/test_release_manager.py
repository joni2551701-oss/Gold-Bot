"""
Phase P1 (Production Deployment Pipeline Foundation) --
scripts/deploy/release_manager.py tests.

Pure filesystem logic, tested against a pytest tmp_path standing in
for /opt/goldbot -- no VPS, systemd, or SSH involved anywhere in this
file. This is deliberate (see docs/PHASE_P1_AUDIT.md): the
release-selection/rollback decision logic was pulled out of the bash
scripts into this pure module specifically so it could be unit-tested
without live infrastructure.
"""

import io
import os
import sys
import contextlib

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "deploy"))
import release_manager as rm  # noqa: E402


def _make_release(deploy_path, release_id):
    path = os.path.join(deploy_path, "releases", release_id)
    os.makedirs(path, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# new_release_id
# ---------------------------------------------------------------------------

def test_new_release_id_is_14_digits():
    release_id = rm.new_release_id()
    assert len(release_id) == 14
    assert release_id.isdigit()


def test_new_release_id_matches_pattern():
    assert rm.RELEASE_ID_PATTERN.match(rm.new_release_id())


def test_new_release_id_is_monotonic_non_decreasing():
    import time

    first = rm.new_release_id()
    time.sleep(0.01)
    second = rm.new_release_id()
    assert second >= first


# ---------------------------------------------------------------------------
# list_releases
# ---------------------------------------------------------------------------

def test_list_releases_empty_when_deploy_path_missing(tmp_path):
    assert rm.list_releases(str(tmp_path / "does_not_exist")) == []


def test_list_releases_empty_when_releases_dir_missing(tmp_path):
    assert rm.list_releases(str(tmp_path)) == []


def test_list_releases_returns_single_release(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    assert rm.list_releases(str(tmp_path)) == ["20260101000000"]


def test_list_releases_sorted_oldest_first(tmp_path):
    _make_release(str(tmp_path), "20260103000000")
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    assert rm.list_releases(str(tmp_path)) == [
        "20260101000000", "20260102000000", "20260103000000",
    ]


def test_list_releases_ignores_non_matching_names(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    os.makedirs(os.path.join(str(tmp_path), "releases", "not-a-release-id"), exist_ok=True)
    os.makedirs(os.path.join(str(tmp_path), "releases", "12345"), exist_ok=True)
    assert rm.list_releases(str(tmp_path)) == ["20260101000000"]


def test_list_releases_ignores_files_not_directories(tmp_path):
    releases_dir = os.path.join(str(tmp_path), "releases")
    os.makedirs(releases_dir, exist_ok=True)
    with open(os.path.join(releases_dir, "20260101000000"), "w") as f:
        f.write("not a directory")
    assert rm.list_releases(str(tmp_path)) == []


def test_list_releases_many_releases_still_sorted(tmp_path):
    ids = [f"202601{day:02d}000000" for day in range(1, 11)]
    for release_id in reversed(ids):
        _make_release(str(tmp_path), release_id)
    assert rm.list_releases(str(tmp_path)) == ids


# ---------------------------------------------------------------------------
# current_release
# ---------------------------------------------------------------------------

def test_current_release_none_when_no_symlink(tmp_path):
    assert rm.current_release(str(tmp_path)) is None


def test_current_release_none_when_current_is_a_plain_file(tmp_path):
    with open(os.path.join(str(tmp_path), "current"), "w") as f:
        f.write("not a symlink")
    assert rm.current_release(str(tmp_path)) is None


def test_current_release_returns_target_release_id(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    os.symlink(
        os.path.join("releases", "20260101000000"),
        os.path.join(str(tmp_path), "current"),
    )
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_current_release_handles_trailing_slash_in_target(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    os.symlink(
        os.path.join("releases", "20260101000000") + "/",
        os.path.join(str(tmp_path), "current"),
    )
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_current_release_none_when_symlink_target_is_malformed(tmp_path):
    os.symlink("garbage-target", os.path.join(str(tmp_path), "current"))
    assert rm.current_release(str(tmp_path)) is None


def test_current_release_none_when_symlink_is_dangling(tmp_path):
    os.symlink(
        os.path.join("releases", "20990101000000"),
        os.path.join(str(tmp_path), "current"),
    )
    # readlink still returns a valid-looking id even though the
    # target doesn't exist -- current_release() only validates the
    # id's shape, not that the directory actually exists.
    assert rm.current_release(str(tmp_path)) == "20990101000000"


# ---------------------------------------------------------------------------
# previous_release
# ---------------------------------------------------------------------------

def test_previous_release_none_with_zero_releases(tmp_path):
    assert rm.previous_release(str(tmp_path)) is None


def test_previous_release_none_with_one_release(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    assert rm.previous_release(str(tmp_path)) is None


def test_previous_release_with_two_releases_no_current(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    assert rm.previous_release(str(tmp_path)) == "20260101000000"


def test_previous_release_when_current_is_newest(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    assert rm.previous_release(str(tmp_path)) == "20260101000000"


def test_previous_release_when_current_is_oldest(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    assert rm.previous_release(str(tmp_path)) is None


def test_previous_release_with_three_releases_current_is_middle(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    _make_release(str(tmp_path), "20260103000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    assert rm.previous_release(str(tmp_path)) == "20260101000000"


def test_previous_release_falls_back_when_current_release_id_not_in_releases_dir(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    os.symlink(
        os.path.join("releases", "20990101000000"),
        os.path.join(str(tmp_path), "current"),
    )
    assert rm.previous_release(str(tmp_path)) == "20260101000000"


def test_previous_release_stable_across_repeated_calls(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    first = rm.previous_release(str(tmp_path))
    second = rm.previous_release(str(tmp_path))
    assert first == second == "20260101000000"


# ---------------------------------------------------------------------------
# switch_current
# ---------------------------------------------------------------------------

def test_switch_current_creates_symlink(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    current_link = os.path.join(str(tmp_path), "current")
    assert os.path.islink(current_link)


def test_switch_current_points_at_correct_release(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_switch_current_overwrites_existing_symlink(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    assert rm.current_release(str(tmp_path)) == "20260102000000"


def test_switch_current_rejects_malformed_release_id(tmp_path):
    with pytest.raises(ValueError):
        rm.switch_current(str(tmp_path), "not-a-valid-id")


def test_switch_current_rejects_short_numeric_id(tmp_path):
    with pytest.raises(ValueError):
        rm.switch_current(str(tmp_path), "12345")


def test_switch_current_rejects_nonexistent_release_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        rm.switch_current(str(tmp_path), "20990101000000")


def test_switch_current_does_not_touch_current_on_invalid_id(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    with pytest.raises(ValueError):
        rm.switch_current(str(tmp_path), "bad-id")
    # current must still point at the original, valid release
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_switch_current_does_not_touch_current_on_missing_release(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    with pytest.raises(FileNotFoundError):
        rm.switch_current(str(tmp_path), "20990101000000")
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_switch_current_removes_stale_tmp_link(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    tmp_link = os.path.join(str(tmp_path), "current.tmp")
    os.symlink("garbage", tmp_link)
    rm.switch_current(str(tmp_path), "20260101000000")
    assert rm.current_release(str(tmp_path)) == "20260101000000"
    assert not os.path.lexists(tmp_link)


def test_switch_current_is_idempotent(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_switch_current_never_leaves_current_pointing_nowhere(tmp_path):
    """After any successful switch, `current` must resolve to a real directory."""
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    current_link = os.path.join(str(tmp_path), "current")
    assert os.path.isdir(current_link)


# ---------------------------------------------------------------------------
# rollback scenario (integration of previous_release + switch_current)
# ---------------------------------------------------------------------------

def test_rollback_scenario_switches_back_to_previous(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260102000000")

    target = rm.previous_release(str(tmp_path))
    assert target == "20260101000000"
    rm.switch_current(str(tmp_path), target)
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_rollback_never_deletes_releases_directory(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    target = rm.previous_release(str(tmp_path))
    rm.switch_current(str(tmp_path), target)
    # both release directories must still exist -- rollback is a
    # symlink switch, never a delete/rebuild (RULE 5).
    assert rm.list_releases(str(tmp_path)) == ["20260101000000", "20260102000000"]


def test_rollback_to_oldest_release_leaves_nothing_further_to_roll_back_to(tmp_path):
    """
    previous_release() walks strictly backwards through history, it
    never wraps around -- once `current` is the oldest release, a
    second rollback attempt has no target (rollback.sh's own
    "no previous release available" failure path handles this case,
    see test_deploy_scripts_shape.py).
    """
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260102000000")

    first_target = rm.previous_release(str(tmp_path))
    assert first_target == "20260101000000"
    rm.switch_current(str(tmp_path), first_target)

    assert rm.previous_release(str(tmp_path)) is None


# ---------------------------------------------------------------------------
# CLI (argparse) surface
# ---------------------------------------------------------------------------

def _run_cli(argv):
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exit_code = rm.main(argv)
    return exit_code, stdout.getvalue().strip()


def test_cli_new_id_prints_a_valid_id():
    exit_code, output = _run_cli(["new-id"])
    assert exit_code == 0
    assert rm.RELEASE_ID_PATTERN.match(output)


def test_cli_list_prints_nothing_for_empty_deploy_path(tmp_path):
    exit_code, output = _run_cli(["list", str(tmp_path)])
    assert exit_code == 0
    assert output == ""


def test_cli_list_prints_one_release_per_line(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    exit_code, output = _run_cli(["list", str(tmp_path)])
    assert exit_code == 0
    assert output.splitlines() == ["20260101000000", "20260102000000"]


def test_cli_current_exit_1_when_unset(tmp_path):
    exit_code, output = _run_cli(["current", str(tmp_path)])
    assert exit_code == 1
    assert output == ""


def test_cli_current_prints_release_id_when_set(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    rm.switch_current(str(tmp_path), "20260101000000")
    exit_code, output = _run_cli(["current", str(tmp_path)])
    assert exit_code == 0
    assert output == "20260101000000"


def test_cli_previous_exit_1_when_none_available(tmp_path):
    exit_code, output = _run_cli(["previous", str(tmp_path)])
    assert exit_code == 1
    assert output == ""


def test_cli_previous_prints_previous_release_id(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    _make_release(str(tmp_path), "20260102000000")
    rm.switch_current(str(tmp_path), "20260102000000")
    exit_code, output = _run_cli(["previous", str(tmp_path)])
    assert exit_code == 0
    assert output == "20260101000000"


def test_cli_activate_switches_current_and_prints_id(tmp_path):
    _make_release(str(tmp_path), "20260101000000")
    exit_code, output = _run_cli(["activate", str(tmp_path), "20260101000000"])
    assert exit_code == 0
    assert output == "20260101000000"
    assert rm.current_release(str(tmp_path)) == "20260101000000"


def test_cli_activate_exit_2_on_invalid_id(tmp_path):
    exit_code, _ = _run_cli(["activate", str(tmp_path), "not-valid"])
    assert exit_code == 2


def test_cli_activate_exit_2_on_missing_release(tmp_path):
    exit_code, _ = _run_cli(["activate", str(tmp_path), "20990101000000"])
    assert exit_code == 2


def test_cli_requires_a_subcommand():
    with pytest.raises(SystemExit):
        rm.main([])


def test_cli_unknown_subcommand_raises_system_exit():
    with pytest.raises(SystemExit):
        rm.main(["not-a-real-subcommand"])


# ---------------------------------------------------------------------------
# Isolation from Trading Core (RULE 1)
# ---------------------------------------------------------------------------

def test_release_manager_module_imports_nothing_from_trading_core():
    """
    Static guard: release_manager.py must never import risk/, core/,
    decision/, execution/, strategies/, signals/, context/, or ai/ --
    it is pure deploy-path filesystem logic and has no business
    reading Trading Core state.
    """
    module_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "scripts", "deploy", "release_manager.py",
    )
    with open(module_path) as f:
        source = f.read()
    forbidden_prefixes = (
        "import risk", "from risk", "import core", "from core",
        "import decision", "from decision", "import execution", "from execution",
        "import strategies", "from strategies", "import signals", "from signals",
        "import context", "from context", "import ai", "from ai",
    )
    for line in source.splitlines():
        stripped = line.strip()
        assert not stripped.startswith(forbidden_prefixes), (
            f"release_manager.py must not import Trading Core: {stripped!r}"
        )
