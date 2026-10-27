"""Behaviour tests for tools/check_dependency_freshness.py (no network: fetchers are stubs)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_dependency_freshness as checker  # noqa: E402

SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"


class TestWorkflowActions(unittest.TestCase):
    def status(self, line: str, latest: str):
        packages = checker.parse_workflow_actions(line, "ci.yml")
        return checker.collect_status(packages, lambda _name: latest, deferrals={})

    def test_pinned_action_reads_version_from_comment(self):
        [row] = self.status(f"      - uses: actions/checkout@{SHA} # v7.0.1\n", "7.1.0")
        self.assertEqual(row["minimum"], "7.0.1")
        self.assertTrue(row["outdated"])
        self.assertTrue(checker.needs_review(row))

    def test_held_action_is_held_not_a_failed_check(self):
        [row] = self.status(f"      - uses: actions/checkout@v7 # freshness-hold: upstream workflow\n", "8.0.0")
        self.assertFalse(row["check_failed"], row)
        self.assertFalse(checker.needs_review(row))
        self.assertIn("HELD: upstream workflow", "\n".join(checker._render_table([row])))


if __name__ == "__main__":
    unittest.main()
