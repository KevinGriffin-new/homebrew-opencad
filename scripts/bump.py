#!/usr/bin/env python3
"""Bump both casks to a Land Survey release and the host build it is pinned to.

The plugin loads in exactly one OpenCADStudio build, and a cask cannot depend on
a version of another cask. So the host cask never moves on its own: it moves to
whatever host the plugin's release says it was built for, in the same commit.

    bump.py                # latest plugin release
    bump.py 0.4.25         # a specific one
    bump.py --check        # exit 1 if the casks disagree with each other

Exit codes: 0 bumped or already current, 1 inconsistent casks (--check),
3 waiting: the plugin targets a host whose signed build is not published yet.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PLUGIN_REPO = "KevinGriffin-new/opencad-landsurvey-plugin"
HOST_REPO = "KevinGriffin-new/OpenCADStudio"
CASKS = Path(__file__).resolve().parents[1] / "Casks"
HOST_CASK = CASKS / "opencadstudio.rb"
PLUGIN_CASK = CASKS / "opencad-landsurvey.rb"
WAITING = 3


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def asset(repo: str, tag: str, name: str) -> str | None:
    """A small release asset's text, or None if the release or asset is missing."""
    try:
        return gh("release", "download", tag, "-R", repo, "-p", name, "-O", "-")
    except subprocess.CalledProcessError:
        return None


def sha256_of(text: str | None, what: str) -> str:
    m = re.match(r"\s*([0-9a-f]{64})\b", text or "")
    if not m:
        raise SystemExit(f"no sha256 in {what}: {text!r}")
    return m.group(1)


def replace_one(text: str, pattern: str, repl: str, path: Path) -> str:
    out, n = re.subn(pattern, repl, text, flags=re.M)
    if n != 1:
        raise SystemExit(f"{path.name}: expected one match for {pattern!r}, found {n}")
    return out


def cask_field(path: Path, field: str) -> str:
    m = re.search(rf'^  {field} "([^"]+)"', path.read_text(), re.M)
    if not m:
        raise SystemExit(f"{path.name}: no {field}")
    return m.group(1)


def caveat_host(path: Path) -> str:
    m = re.search(r"Built for OpenCADStudio (\S+) exactly", path.read_text())
    if not m:
        raise SystemExit(f"{path.name}: no host version in caveats")
    return m.group(1)


def check() -> int:
    host = cask_field(HOST_CASK, "version")
    pinned = caveat_host(PLUGIN_CASK)
    if host != pinned:
        print(f"opencadstudio is {host} but opencad-landsurvey is built for {pinned}")
        return 1
    print(f"consistent: opencadstudio {host}, opencad-landsurvey "
          f"{cask_field(PLUGIN_CASK, 'version')}")
    return 0


def bump(plugin_version: str | None) -> int:
    tag = plugin_version and f"v{plugin_version.lstrip('v')}"
    if tag is None:
        tag = json.loads(gh("release", "view", "-R", PLUGIN_REPO, "--json", "tagName"))["tagName"]
    version = tag.lstrip("v")

    meta = asset(PLUGIN_REPO, tag, "opencad.landsurvey-macos-aarch64.dylib.build.json")
    if meta is None:
        raise SystemExit(f"{PLUGIN_REPO} {tag} has no macOS build metadata")
    host_tag = json.loads(meta)["host_release"]
    host_version = host_tag.lstrip("v")
    plugin_sha = sha256_of(
        asset(PLUGIN_REPO, tag, "opencad.landsurvey-macos-aarch64.tar.gz.sha256"),
        f"{tag} tarball .sha256")

    dmg = f"OpenCADStudio-{host_tag}-macos-arm64-signed.dmg"
    host_sha_text = asset(HOST_REPO, f"{host_tag}-signed", f"{dmg}.sha256")
    if host_sha_text is None:
        print(f"waiting: plugin {version} targets host {host_tag}, but "
              f"{HOST_REPO} has no {host_tag}-signed release with {dmg}.sha256 yet")
        return WAITING
    host_sha = sha256_of(host_sha_text, f"{dmg}.sha256")

    host = HOST_CASK.read_text()
    host = replace_one(host, r'^  version "[^"]+"', f'  version "{host_version}"', HOST_CASK)
    host = replace_one(host, r'^  sha256 "[^"]+"', f'  sha256 "{host_sha}"', HOST_CASK)

    plugin = PLUGIN_CASK.read_text()
    plugin = replace_one(plugin, r'^  version "[^"]+"', f'  version "{version}"', PLUGIN_CASK)
    plugin = replace_one(plugin, r'^  sha256 "[^"]+"', f'  sha256 "{plugin_sha}"', PLUGIN_CASK)
    plugin = replace_one(plugin, r"Built for OpenCADStudio \S+ exactly",
                         f"Built for OpenCADStudio {host_version} exactly", PLUGIN_CASK)

    changed = host != HOST_CASK.read_text() or plugin != PLUGIN_CASK.read_text()
    HOST_CASK.write_text(host)
    PLUGIN_CASK.write_text(plugin)
    print(f"{'bumped' if changed else 'current'}: opencad-landsurvey {version}, "
          f"opencadstudio {host_version}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("version", nargs="?", help="plugin version (default: latest release)")
    ap.add_argument("--check", action="store_true", help="verify the casks agree")
    args = ap.parse_args()
    return check() if args.check else bump(args.version)


if __name__ == "__main__":
    sys.exit(main())
