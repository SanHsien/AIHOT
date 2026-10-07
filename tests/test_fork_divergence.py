"""Unit and contract tests for tools/check_divergence.py.

Verifies:
1. Parsing of docs/DIVERGENCE.md.
2. Comparison between divergence doc and git diff against baseline.
3. RENAME_ALIASES handling (README.en.md -> README.md).
4. Malformed row detection (must have exactly 5 columns).
5. Baseline availability checks.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_divergence as checker  # noqa: E402


class TestForkDivergence(unittest.TestCase):
    def test_baseline_is_valid(self):
        baseline = checker.load_baseline()
        self.assertIn("reviewed_through", baseline)
        self.assertEqual(len(baseline["reviewed_through"]), 40)

    def test_parse_registered_paths(self):
        sample = (
            "| 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理 |\n"
            "|---|---|---|---|---|\n"
            "| `README.md` | orig | fork | why | how |\n"
            "| `AGENTS.md` | orig | fork | why | how |\n"
        )
        paths = checker.parse_registered_paths(sample)
        self.assertEqual(paths, {"README.md", "AGENTS.md"})

    def test_column_count_escapes(self):
        self.assertEqual(
            checker._column_count("| `a` | b | c | d | e |"), 5
        )
        self.assertEqual(
            checker._column_count("| `a` | b \\| c | d | e | f |"), 5
        )

    def test_malformed_rows_detected(self):
        sample = (
            "| 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理 |\n"
            "|---|---|---|---|---|\n"
            "| `ok.md` | 1 | 2 | 3 | 4 |\n"
            "| `bad.md` | 1 | 2 | 3 |\n"
        )
        bad = checker.malformed_rows(sample)
        self.assertEqual(len(bad), 1)
        self.assertEqual(bad[0][2], "bad.md")

    def test_real_registry_has_no_malformed_rows(self):
        doc = (REPO_ROOT / "docs" / "DIVERGENCE.md").read_text(encoding="utf-8")
        bad = checker.malformed_rows(doc)
        self.assertEqual(bad, [])

    def test_real_registry_matches_baseline(self):
        baseline = checker.load_baseline()
        base_sha = baseline["reviewed_through"]
        if not checker.base_commit_available(base_sha, REPO_ROOT):
            self.skipTest("Base commit not available locally")

        owned = checker.owned_files_at_base(base_sha, REPO_ROOT)
        pairs = checker.changed_since_base(base_sha, REPO_ROOT)
        doc = (REPO_ROOT / "docs" / "DIVERGENCE.md").read_text(encoding="utf-8")

        divergent = checker.compute_divergent_files(pairs, owned)
        registered = checker.parse_registered_paths(doc)

        changed_not_registered, registered_not_changed = checker.compare(divergent, registered)
        self.assertEqual(
            changed_not_registered,
            set(),
            f"Changed but not registered: {changed_not_registered}",
        )
        self.assertEqual(
            registered_not_changed,
            set(),
            f"Registered but not changed: {registered_not_changed}",
        )


if __name__ == "__main__":
    unittest.main()
