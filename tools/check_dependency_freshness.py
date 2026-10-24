"""Compare declared dependency floors against their current upstream releases.

This fork tracks its pinned GitHub Actions used by `.github/workflows/*.yml`
and optional development tools in `requirements-dev.txt`.
Dependabot proposes upgrades one pull request at a time, which answers "is there
a newer release?" but never "how far behind is what we declare, across every
declaration in the repo?". This reads the declarations, asks PyPI (for Python tools)
and the GitHub Releases API (for Actions) for current releases, and writes a Markdown report.

    python tools/check_dependency_freshness.py --output report.md --github-output
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.parse
import urllib.request
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "aihot-dependency-freshness"

REQUIREMENT_FILES = ("requirements-dev.txt",)

_REQUIREMENT_RE = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?\s*(.*)$")
_MINIMUM_RE = re.compile(r"(>=|>|==|~=)\s*([0-9][0-9A-Za-z.!+_-]*)")
_RELEASE_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)*")
_USES_RE = re.compile(
    r"^\s*(?:-\s*)?uses:\s*([\w.\-]+/[\w.\-]+(?:/[\w.\-]+)*)@([0-9a-fA-F]{40}|\S+)"
    r"(?:\s*#\s*(.*))?\s*$",
    re.MULTILINE,
)
HOLD_MARKER = "freshness-hold:"
DEFERRALS_PATH = REPO_ROOT / ".github" / "dependency-deferrals.json"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


class DependencyCheckError(RuntimeError):
    """Raised when dependencies or the workflows directory cannot be read."""


def release_key(version: str) -> tuple[int, ...] | None:
    match = _RELEASE_RE.match(version.strip().lstrip("vV"))
    if not match:
        return None
    return tuple(int(part) for part in match.group(0).split("."))


def is_newer_version(latest: str, declared: str) -> bool:
    latest_key = release_key(latest)
    declared_key = release_key(declared)
    if latest_key is None or declared_key is None:
        return False
    depth = len(declared_key)
    padded = latest_key + (0,) * (depth - len(latest_key))
    return padded[:depth] > declared_key


def load_deferrals(path: Path = DEFERRALS_PATH) -> dict[str, tuple[str, str]]:
    try:
        entries = json.loads(path.read_text(encoding="utf-8")).get("deferrals", {})
    except (OSError, ValueError):
        return {}
    deferrals: dict[str, tuple[str, str]] = {}
    for name, entry in (entries or {}).items():
        if not isinstance(entry, dict):
            continue
        latest = str(entry.get("deferredLatest", "")).strip()
        reason = str(entry.get("reason", "")).strip()
        if latest and reason:
            deferrals[name.lower()] = (latest, reason)
    return deferrals


def parse_requirements(text: str, source: str) -> list[dict[str, str]]:
    packages: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        comment = raw_line.split("#", 1)[1].strip() if "#" in raw_line else ""
        line = raw_line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        hold = comment[len(HOLD_MARKER) :].strip() if comment.startswith(HOLD_MARKER) else ""
        head = line.split(";", 1)[0].strip()
        match = _REQUIREMENT_RE.match(head)
        if not match:
            continue
        name, specifiers = match.groups()
        minimum = _MINIMUM_RE.search(specifiers)
        packages.append(
            {
                "name": name,
                "minimum": minimum.group(2) if minimum else "",
                "requirement": line,
                "source": source,
                "hold": hold,
                "kind": "pypi",
            }
        )
    return packages


def parse_workflow_actions(text: str, source: str) -> list[dict[str, str]]:
    packages: list[dict[str, str]] = []
    for match in _USES_RE.finditer(text):
        action, ref, comment = match.group(1), match.group(2), (match.group(3) or "").strip()
        hold = comment[len(HOLD_MARKER) :].strip() if comment.startswith(HOLD_MARKER) else ""
        version_source = comment if comment else ref
        version_match = _RELEASE_RE.match(version_source.lstrip("vV")) if not hold else None
        minimum = version_match.group(0) if version_match else ""
        packages.append(
            {
                "name": action,
                "minimum": minimum,
                "requirement": f"{action}@{comment or ref[:12]}",
                "source": source,
                "hold": hold,
                "kind": "github-action",
            }
        )
    return packages


def load_direct_dependencies(root: Path = REPO_ROOT) -> list[dict[str, str]]:
    packages: list[dict[str, str]] = []
    seen: set[str] = set()
    for name in REQUIREMENT_FILES:
        path = root / name
        if not path.is_file():
            continue
        for package in parse_requirements(path.read_text(encoding="utf-8"), name):
            key = package["name"].lower().replace("_", "-")
            if key in seen:
                continue
            seen.add(key)
            packages.append(package)
    return packages


def load_workflow_actions(root: Path = REPO_ROOT) -> list[dict[str, str]]:
    workflows_dir = root / ".github" / "workflows"
    if not workflows_dir.is_dir():
        raise DependencyCheckError("missing .github/workflows directory")
    merged: dict[tuple[str, str], dict[str, str]] = {}
    for path in sorted(workflows_dir.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for package in parse_workflow_actions(text, path.name):
            key = (package["name"].lower(), package["minimum"] or package["requirement"])
            existing = merged.get(key)
            if existing is None:
                merged[key] = package
                continue
            sources = existing["source"].split(", ")
            if path.name not in sources:
                sources.append(path.name)
                existing["source"] = ", ".join(sources)
    return sorted(merged.values(), key=lambda p: (p["name"], p["minimum"]))


def fetch_pypi_version(package_name: str, timeout: float = 10.0) -> str | None:
    quoted_name = urllib.parse.quote(package_name, safe="")
    request = urllib.request.Request(
        f"https://pypi.org/pypi/{quoted_name}/json",
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError):
        return None
    version = payload.get("info", {}).get("version")
    return str(version) if version else None


def action_repository(action_name: str) -> str:
    owner, _, rest = action_name.partition("/")
    return f"{owner}/{rest.split('/', 1)[0]}" if rest else action_name


def fetch_github_release(action_name: str, timeout: float = 10.0) -> str | None:
    quoted_name = urllib.parse.quote(action_repository(action_name), safe="/")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    token = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"https://api.github.com/repos/{quoted_name}/releases/latest",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError):
        payload = {}
    tag = str(payload.get("tag_name") or "")
    if release_key(tag) is not None:
        return tag.lstrip("vV")
    return _fetch_latest_version_tag(quoted_name, headers, timeout)


def _fetch_latest_version_tag(
    quoted_name: str, headers: dict[str, str], timeout: float
) -> str | None:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{quoted_name}/tags?per_page=100", headers=headers
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            tags = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(tags, list):
        return None
    best: tuple[tuple[int, ...], str] | None = None
    for entry in tags:
        name = str((entry or {}).get("name") or "") if isinstance(entry, dict) else ""
        key = release_key(name)
        if key is None or not name.lstrip("vV")[:1].isdigit():
            continue
        if best is None or key > best[0]:
            best = (key, name.lstrip("vV"))
    return best[1] if best else None


def collect_status(
    packages: list[dict[str, str]],
    fetch: Callable[[str], str | None],
    deferrals: dict[str, tuple[str, str]] | None = None,
) -> list[dict[str, object]]:
    deferrals = deferrals if deferrals is not None else load_deferrals()
    rows: list[dict[str, object]] = []
    for package in packages:
        minimum = package["minimum"]
        latest = fetch(package["name"])
        reviewed, reason = deferrals.get(package["name"].lower(), ("", ""))
        deferred = bool(reviewed and latest and not is_newer_version(latest, reviewed))
        rows.append(
            {
                **package,
                "latest": latest or "unknown",
                "outdated": bool(minimum and latest and is_newer_version(latest, minimum)),
                "check_failed": not minimum or latest is None,
                "deferred_reason": reason if deferred else "",
            }
        )
    return rows


def needs_review(row: dict[str, object]) -> bool:
    return bool(row["outdated"]) and not row.get("hold") and not row.get("deferred_reason")


def _render_table(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "| Package | Declared in | Requirement | Latest | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        if row["check_failed"]:
            status = "CHECK FAILED"
        elif row.get("hold") and row["outdated"]:
            status = f"HELD: {row['hold']}"
        elif row.get("deferred_reason") and row["outdated"]:
            status = f"DEFERRED at {row['latest']}: {row['deferred_reason']}"
        elif row["outdated"]:
            status = "REVIEW UPDATE"
        else:
            status = "OK"
        lines.append(
            f"| `{row['name']}` | `{row['source']}` | `{row['requirement']}` | "
            f"`{row['latest']}` | {status} |"
        )
    if not rows:
        lines.append("| - | - | - | - | OK |")
    return lines


def render_markdown(
    rows_python: list[dict[str, object]],
    rows_actions: list[dict[str, object]] | None = None,
    error: str | None = None,
) -> str:
    rows_actions = rows_actions if rows_actions is not None else []
    lines = ["# Dependency freshness report", ""]
    if error:
        lines.extend(["## Check failed", "", f"```text\n{error}\n```", ""])
        return "\n".join(lines)

    if rows_python:
        lines.extend(["## Python dev dependencies (PyPI)", ""])
        lines.extend(_render_table(rows_python))
        lines.append("")
    lines.extend(["## GitHub Actions (pinned in .github/workflows/)", ""])
    lines.extend(_render_table(rows_actions))
    return "\n".join(lines)


def write_github_output(
    rows_python: list[dict[str, object]],
    rows_actions: list[dict[str, object]],
    report_path: Path,
) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    rows = rows_python + rows_actions
    outdated = any(needs_review(row) for row in rows)
    check_failed = not rows or any(bool(row["check_failed"]) for row in rows)
    with open(output_path, "a", encoding="utf-8") as output:
        output.write(f"outdated={'true' if outdated else 'false'}\n")
        output.write(f"check_failed={'true' if check_failed else 'false'}\n")
        output.write(f"needs_attention={'true' if outdated or check_failed else 'false'}\n")
        output.write(f"report_path={report_path.as_posix()}\n")


def render_json(
    rows_python: list[dict[str, object]],
    rows_actions: list[dict[str, object]],
    error: str | None,
) -> str:
    payload = {
        "error": error,
        "python_dependencies": rows_python,
        "github_actions": rows_actions,
        "needs_review": [row["name"] for row in rows_python + rows_actions if needs_review(row)],
        "check_failed": any(bool(row["check_failed"]) for row in rows_python + rows_actions),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dependency-freshness-report.md")
    parser.add_argument(
        "--github-output",
        action="store_true",
        help="Write status fields to GITHUB_OUTPUT",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when a declared range has aged.",
    )
    args = parser.parse_args()

    rows_python: list[dict[str, object]] = []
    rows_actions: list[dict[str, object]] = []
    error: str | None = None
    try:
        deferrals = load_deferrals()
        rows_python = collect_status(load_direct_dependencies(), fetch_pypi_version, deferrals)
        rows_actions = collect_status(load_workflow_actions(), fetch_github_release, deferrals)
    except DependencyCheckError as exc:
        error = str(exc)

    report = render_markdown(rows_python, rows_actions, error)
    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(render_json(rows_python, rows_actions, error) if args.json else report)

    if args.github_output:
        write_github_output(rows_python, rows_actions, output_path)
    if error:
        return 2
    if args.strict and any(
        needs_review(row) or bool(row["check_failed"]) for row in rows_python + rows_actions
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
