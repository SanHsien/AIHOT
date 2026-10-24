"""Enforce that `docs/DIVERGENCE.md` lists exactly the upstream files this fork has
changed or deleted since the reviewed baseline -- no more, no less.

This fork's stated policy is: track upstream directly, accept divergence as the
expected outcome, and write every divergence down clearly enough that a future sync
does not need to re-derive the judgment call.

    python tools/check_divergence.py [--json] [--repo-dir PATH] [--divergence-doc PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO_ROOT / "tools" / "upstream_baseline.json"
DIVERGENCE_DOC_PATH = REPO_ROOT / "docs" / "DIVERGENCE.md"

RENAME_ALIASES = {"README.en.md": "README.md"}

_TABLE_ROW_RE = re.compile(r"^\|\s*`([^`]+)`")


class DivergenceCheckError(RuntimeError):
    """Raised when the baseline or the divergence document cannot be read."""


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.is_file():
        raise DivergenceCheckError(f"missing baseline file: {path}")
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DivergenceCheckError(f"invalid baseline file: {path}: {exc}") from exc
    reviewed_through = baseline.get("reviewed_through")
    if not reviewed_through or len(reviewed_through) != 40:
        raise DivergenceCheckError(f"{path} is missing a full 40-character reviewed_through")
    return baseline


def run_git(args: list[str], repo_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def base_commit_available(base_sha: str, repo_dir: Path) -> bool:
    result = run_git(["cat-file", "-e", f"{base_sha}^{{commit}}"], repo_dir)
    return result.returncode == 0


def owned_files_at_base(base_sha: str, repo_dir: Path) -> set[str]:
    result = run_git(["ls-tree", "-r", "--name-only", base_sha], repo_dir)
    if result.returncode != 0:
        raise DivergenceCheckError(f"git ls-tree failed: {result.stderr.strip()}")
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def changed_since_base(base_sha: str, repo_dir: Path) -> list[tuple[str, str]]:
    result = run_git(["diff", "--name-status", base_sha, "--"], repo_dir)
    if result.returncode != 0:
        raise DivergenceCheckError(f"git diff failed: {result.stderr.strip()}")
    pairs = []
    seen_paths = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, path = parts[0][0], parts[-1]
        pairs.append((status, path))
        seen_paths.add(path)

    # Fold in untracked files so unstaged additions (like aliased mirrors) are checked
    untracked_result = run_git(["status", "--porcelain"], repo_dir)
    if untracked_result.returncode == 0:
        for line in untracked_result.stdout.splitlines():
            if line.startswith("?? "):
                path = line[3:].strip()
                if path not in seen_paths:
                    pairs.append(("A", path))
    return pairs


def compute_divergent_files(pairs: list[tuple[str, str]], owned: set[str]) -> set[str]:
    divergent: set[str] = set()
    for status, path in pairs:
        modified_or_deleted_upstream_file = status in ("M", "D") and path in owned
        aliased_addition_for_a_changed_upstream_file = (
            status == "A" and path in RENAME_ALIASES and RENAME_ALIASES[path] in owned
        )
        if modified_or_deleted_upstream_file or aliased_addition_for_a_changed_upstream_file:
            divergent.add(path)
    return divergent


REGISTRY_COLUMNS = 5  # 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理
_ESCAPE_PAIR_RE = re.compile(r"\\.", re.DOTALL)


def _column_count(row: str) -> int:
    without_escapes = _ESCAPE_PAIR_RE.sub("", row.strip())
    if without_escapes.startswith("|"):
        without_escapes = without_escapes[1:]
    if without_escapes.endswith("|"):
        without_escapes = without_escapes[:-1]
    return len(without_escapes.split("|"))


def malformed_rows(text: str) -> list[tuple[int, int, str]]:
    bad: list[tuple[int, int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        match = _TABLE_ROW_RE.match(stripped)
        if not match:
            continue
        columns = _column_count(stripped)
        if columns != REGISTRY_COLUMNS:
            bad.append((number, columns, match.group(1).strip()))
    return bad


def parse_registered_paths(text: str) -> set[str]:
    paths: set[str] = set()
    for line in text.splitlines():
        match = _TABLE_ROW_RE.match(line.strip())
        if match:
            paths.add(match.group(1).strip())
    return paths


def compare(divergent: set[str], registered: set[str]) -> tuple[set[str], set[str]]:
    return divergent - registered, registered - divergent


def render_report(
    base_sha: str,
    divergent: set[str],
    registered: set[str],
    changed_not_registered: set[str],
    registered_not_changed: set[str],
) -> str:
    lines = [
        f"Base commit: {base_sha[:7]}",
        f"{len(divergent)} upstream file(s) diverge from the baseline; "
        f"{len(registered)} registered in docs/DIVERGENCE.md.",
    ]
    if changed_not_registered:
        lines.append("")
        lines.append("Changed but NOT registered in docs/DIVERGENCE.md:")
        lines.extend(f"  - {path}" for path in sorted(changed_not_registered))
    if registered_not_changed:
        lines.append("")
        lines.append("Registered in docs/DIVERGENCE.md but NOT actually changed:")
        lines.extend(f"  - {path}" for path in sorted(registered_not_changed))
    if not changed_not_registered and not registered_not_changed:
        lines.append("OK: the divergence registry matches the actual changes.")
    return "\n".join(lines)


def render_json(
    base_sha: str,
    divergent: set[str],
    registered: set[str],
    changed_not_registered: set[str],
    registered_not_changed: set[str],
    warning: str | None = None,
    malformed: list[tuple[int, int, str]] | None = None,
) -> str:
    payload = {
        "base_commit": base_sha,
        "changed_upstream_files": sorted(divergent),
        "registered_files": sorted(registered),
        "changed_but_not_registered": sorted(changed_not_registered),
        "registered_but_not_changed": sorted(registered_not_changed),
        "malformed_rows": [
            {"line": number, "columns": columns, "path": path}
            for number, columns, path in (malformed or [])
        ],
        "warning": warning,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-dir", type=Path, default=REPO_ROOT)
    parser.add_argument("--divergence-doc", type=Path, default=DIVERGENCE_DOC_PATH)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON report instead of plain text.",
    )
    args = parser.parse_args()

    try:
        baseline = load_baseline()
    except DivergenceCheckError as exc:
        print(f"ERROR: {exc}")
        return 2
    base_sha = baseline["reviewed_through"]

    if not base_commit_available(base_sha, args.repo_dir):
        warning = (
            f"WARNING: base commit {base_sha[:7]} is not available in this local "
            "repository. Skipping check."
        )
        print(warning)
        if args.json:
            print(render_json(base_sha, set(), set(), set(), set(), warning=warning))
        return 0

    try:
        owned = owned_files_at_base(base_sha, args.repo_dir)
        pairs = changed_since_base(base_sha, args.repo_dir)
        if not args.divergence_doc.is_file():
            raise DivergenceCheckError(f"missing divergence document: {args.divergence_doc}")
        doc_text = args.divergence_doc.read_text(encoding="utf-8")
    except DivergenceCheckError as exc:
        print(f"ERROR: {exc}")
        return 2

    divergent = compute_divergent_files(pairs, owned)
    registered = parse_registered_paths(doc_text)
    changed_not_registered, registered_not_changed = compare(divergent, registered)
    malformed = malformed_rows(doc_text)

    if args.json:
        print(
            render_json(
                base_sha,
                divergent,
                registered,
                changed_not_registered,
                registered_not_changed,
                malformed=malformed,
            )
        )
    else:
        print(
            render_report(
                base_sha, divergent, registered, changed_not_registered, registered_not_changed
            )
        )
        if malformed:
            print("")
            print(
                f"Rows with the wrong number of columns (need {REGISTRY_COLUMNS}: "
                "上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理):"
            )
            for number, columns, path in malformed:
                print(f"  - line {number}: {columns} column(s) -> {path}")

    return 1 if (changed_not_registered or registered_not_changed or malformed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
