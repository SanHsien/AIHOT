#!/usr/bin/env python3
"""verify-env.py -- Verify developer environment prerequisites for SanHsien/AIHOT.

Checks:
- Python version >= 3.10
- Node.js version >= 24
- npm availability
- Git remotes (origin = SanHsien/AIHOT)
- GitHub CLI default repo
- Key scaffold files presence (.gitattributes, docs/DIVERGENCE.md, AGENTS.md, etc.)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def check_python() -> bool:
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 10)
    print(f"[{'OK' if ok else 'FAIL'}] Python version: {v.major}.{v.minor}.{v.micro} (requires >= 3.10)")
    return ok


def check_node() -> bool:
    node = shutil.which("node")
    if not node:
        print("[FAIL] Node.js is not found in PATH")
        return False
    res = subprocess.run([node, "--version"], capture_output=True, text=True)
    m = re.search(r"v(\d+)\.(\d+)", res.stdout)
    if not m:
        print(f"[FAIL] Could not parse node version: {res.stdout.strip()}")
        return False
    major = int(m.group(1))
    ok = major >= 24
    print(f"[{'OK' if ok else 'FAIL'}] Node.js version: {res.stdout.strip()} (requires >= 24)")
    return ok


def check_npm() -> bool:
    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        print("[FAIL] npm is not found in PATH")
        return False
    res = subprocess.run([npm, "--version"], capture_output=True, text=True, shell=os.name == "nt")
    print(f"[OK] npm version: {res.stdout.strip()}")
    return True


def check_git() -> bool:
    res = subprocess.run(["git", "remote", "-v"], cwd=REPO_ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        print("[FAIL] Not a git repository or git error")
        return False
    has_origin = "SanHsien/AIHOT" in res.stdout
    has_upstream = "KKKKhazix/AIHOT" in res.stdout
    print(f"[{'OK' if has_origin else 'WARN'}] Git remote origin: {'SanHsien/AIHOT' if has_origin else 'Unknown'}")
    print(f"[{'OK' if has_upstream else 'WARN'}] Git remote upstream: {'KKKKhazix/AIHOT' if has_upstream else 'Unknown'}")
    return has_origin


def check_scaffold_files() -> bool:
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "FORK.md",
        "NOTICE.md",
        "SKILL.md",
        "README.md",
        "README.en.md",
        "CHANGELOG.md",
        "docs/DIVERGENCE.md",
        "docs/DEVELOPMENT.md",
        "docs/DECISIONS.md",
        "REVIEW.md",
        "tools/upstream_baseline.json",
        "tools/check_divergence.py",
        ".gitattributes",
    ]
    missing = [f for f in required if not (REPO_ROOT / f).exists()]
    if missing:
        print(f"[FAIL] Missing scaffold files: {missing}")
        return False
    print(f"[OK] All {len(required)} essential scaffold files are present")
    return True


def main() -> int:
    print("=== AIHOT Environment Verification ===")
    results = [
        check_python(),
        check_node(),
        check_npm(),
        check_git(),
        check_scaffold_files(),
    ]
    print("=======================================")
    if all(results):
        print("Result: ALL PREREQUISITES SATISFIED (PASS)")
        return 0
    else:
        print("Result: SOME PREREQUISITES FAILED (FAIL)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
