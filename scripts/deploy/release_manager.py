#!/usr/bin/env python3
"""
scripts/deploy/release_manager.py -- Phase P1 (Production Deployment
Pipeline Foundation) release-selection logic.

Pure and VPS-independent: reads/writes only the `releases/` directory
and `current` symlink under a given deploy path on the local
filesystem. No network, no systemd, no SSH -- those stay in the thin
bash wrappers (release_deploy.sh / rollback.sh) that shell out to this
module's CLI. Keeping the decision logic (which release is current,
which is previous, how to atomically switch) in pure Python makes it
unit-testable against a temp directory without a real VPS, systemd, or
SSH access -- see tests/deploy/test_release_manager.py.

Release IDs are UTC timestamps, `YYYYMMDDHHMMSS` (14 digits) -- this
also makes lexicographic sort order equal chronological order, so
`list_releases()` needs no separate parsing/sorting-by-mtime step.
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

RELEASE_ID_PATTERN = re.compile(r"^\d{14}$")


def new_release_id() -> str:
    """A fresh UTC-timestamp release id, e.g. '20260721180912'."""
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def _releases_dir(deploy_path: str) -> str:
    return os.path.join(deploy_path, "releases")


def _current_link(deploy_path: str) -> str:
    return os.path.join(deploy_path, "current")


def list_releases(deploy_path: str) -> list:
    """All valid release ids under releases/, oldest first."""
    releases_dir = _releases_dir(deploy_path)
    if not os.path.isdir(releases_dir):
        return []
    names = [
        name
        for name in os.listdir(releases_dir)
        if RELEASE_ID_PATTERN.match(name)
        and os.path.isdir(os.path.join(releases_dir, name))
    ]
    return sorted(names)


def current_release(deploy_path: str):
    """The release id `current` points at, or None if unset/broken."""
    link = _current_link(deploy_path)
    if not os.path.islink(link):
        return None
    target = os.readlink(link)
    release_id = os.path.basename(target.rstrip("/"))
    if not RELEASE_ID_PATTERN.match(release_id):
        return None
    return release_id


def previous_release(deploy_path: str):
    """
    The release immediately before the current one, for rollback.

    Returns None when there is nothing to roll back to: no releases,
    only one release, or `current` already points at the oldest
    release. If `current` is unset/broken but at least two releases
    exist, falls back to the second-newest release as the safest
    rollback target.
    """
    releases = list_releases(deploy_path)
    if len(releases) < 2:
        return None
    current = current_release(deploy_path)
    if current is None or current not in releases:
        return releases[-2]
    idx = releases.index(current)
    if idx == 0:
        return None
    return releases[idx - 1]


def switch_current(deploy_path: str, release_id: str) -> None:
    """
    Atomically point `current` at releases/<release_id>.

    Uses a temp symlink + os.replace() (POSIX rename), which is
    atomic -- there is no moment where `current` points at nothing or
    a half-written target. Raises ValueError/FileNotFoundError on a
    malformed id or a release directory that does not exist; never
    partially switches.
    """
    if not RELEASE_ID_PATTERN.match(release_id):
        raise ValueError(f"invalid release id: {release_id!r}")
    release_dir = os.path.join(_releases_dir(deploy_path), release_id)
    if not os.path.isdir(release_dir):
        raise FileNotFoundError(f"release directory does not exist: {release_dir}")

    current_link = _current_link(deploy_path)
    tmp_link = current_link + ".tmp"
    if os.path.lexists(tmp_link):
        os.remove(tmp_link)
    os.symlink(os.path.join("releases", release_id), tmp_link)
    os.replace(tmp_link, current_link)


def _cmd_new_id(_args) -> int:
    print(new_release_id())
    return 0


def _cmd_list(args) -> int:
    for release_id in list_releases(args.deploy_path):
        print(release_id)
    return 0


def _cmd_current(args) -> int:
    release_id = current_release(args.deploy_path)
    if release_id is None:
        return 1
    print(release_id)
    return 0


def _cmd_previous(args) -> int:
    release_id = previous_release(args.deploy_path)
    if release_id is None:
        return 1
    print(release_id)
    return 0


def _cmd_activate(args) -> int:
    switch_current(args.deploy_path, args.release_id)
    print(args.release_id)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("new-id", help="Print a fresh release id.").set_defaults(
        func=_cmd_new_id
    )

    for name, func, needs_release_id in [
        ("list", _cmd_list, False),
        ("current", _cmd_current, False),
        ("previous", _cmd_previous, False),
        ("activate", _cmd_activate, True),
    ]:
        sub = subparsers.add_parser(name)
        sub.add_argument("deploy_path")
        if needs_release_id:
            sub.add_argument("release_id")
        sub.set_defaults(func=func)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError) as e:
        print(f"release_manager: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
