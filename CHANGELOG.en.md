# Changelog

All notable changes to this fork (`SanHsien/AIHOT`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This file records only the changes made by this fork; for upstream changes, see upstream releases.

## [Unreleased]

### Changed
- Synced upstream `ce83484..79d962e` (PR #273–#275): alerts may go to a group bot webhook (`FEISHU_ALERT_WEBHOOK_URL`), daily-report dates of another year carry the year, sign-in path detection covers Devise, WordPress and file extensions.
- Synced upstream `cc66cce..ce83484` (124 commits: 4.0.0 engine/site split, migration rules, security boundaries, collection fixes); README and AGENTS carry the new structure.
- Dropped the earlier ports of PR #79/#83/#85: upstream solved each itself (see `docs/UPSTREAM.md`), so the divergence rows are gone; the `_aihot.initialBackfillOnly` switch is removed in favour of upstream's built-in rule.
- Removed `CLAUDE.md` and merged its notes into `AGENTS.md`; every agent now reads `AGENTS.md` only.

### Security
- Fixed three defects in upstream-held code (rows in `docs/DIVERGENCE.md`): agent Markdown link text now escapes backslashes, so an outside title cannot open a link (CodeQL #13); prefix redirects treat the path as data (CodeQL #15); trimming the sign-in attempt table keeps the overall count, so forged `X-Forwarded-For` cannot reset the cap.
- The other 38 CodeQL alerts were dismissed one by one with source/sink reasons; see item 9 of `docs/DECISIONS.md`.
- Early adoption of upstream security fix commits `e4478cb`, `879afa3`, `14fe1da`, `31fa181`:
  - Bump `source-map-js` to 1.2.2 (fixes GHSA-68fv-2mgg-jv7q DoS vulnerability).
  - Bump `@modelcontextprotocol/client` to 2.2.0 (fixes GHSA-6qxp-vccf-f47h credential leak vulnerability).
  - Bump `sharp` to 0.35.5 (fixes GHSA-wq5f-xc86-pv6w librsvg dependency vulnerability).

### Fixed
- The divergence check in `fork-check` never actually ran (CI lacked the upstream base commit and the checker printed `Skipping check.` with exit 0): a missing base is now exit 2 and the workflow fetches upstream main first.
- `check_divergence.py` counts a renamed upstream file as divergent (the `R` status used to slip through).
- `check_dependency_freshness.py` shows an action held with `# freshness-hold:` as `HELD` instead of `CHECK FAILED`.
- The `dependency-freshness` workflow marks a failed Dependabot PR listing as `CHECK FAILED` instead of "no pull requests".

### Added
- Fork development scaffold and standards:
  - `AGENTS.md`: Single source of truth for AI coding agents and development conventions.
  - `CLAUDE.md`: Lightweight patch for Claude Code.
  - `FORK.md`: Fork purpose, upstream tracking policy, and contribution boundaries.
  - `NOTICE.md`: Licensing, brand restrictions, and third-party asset attribution.
  - `SKILL.md`: Project skill contract and locator.
  - `docs/DIVERGENCE.md`: Registry of modified upstream-owned files.
  - `docs/DEVELOPMENT.md`: Local development, prerequisites, and testing guide.
  - `docs/DECISIONS.md`: Architectural decisions log.
  - `REVIEW.md`: Initial quality review and verification report.
  - `tools/upstream_baseline.json`: Upstream baseline commit (`04846072`) watermark.
  - `tools/check_divergence.py`: Automated tool checking divergence registry against git diff.
  - `tools/dev_check.ps1`: One-key local quality check script.
  - `scripts/verify-env.py`: Environment prerequisites verification script.
  - `.gitattributes`: Normalizing line endings (`* text=auto eol=lf`).
  - `README.en.md`: Upstream documentation mirror.
- Translated `README.md` into Traditional Chinese with fork orientation and developer guidelines.

### Changed
- Merged upstream `main` through `cc66cce`: production-core synchronization, public interface 3.0.0, daily/weekly/monthly reporting, topic chronicles, leaderboard v17, mobile rewrite, and two follow-up fixes.
- Updated the Traditional Chinese and English READMEs for the latest upstream capabilities.
- Added six-axis upstream decisions and revisit conditions in `docs/UPSTREAM.md`; advanced `tools/upstream_baseline.json`.
- Removed remote branch `codex/article-body-fidelity-20261002`; both fork and upstream now retain only `main`.
- Ported upstream PR #83: added `summaryIsBody: true` support in RSS sources and new contract test `tests/rss-summary-body.test.ts`.
- Ported upstream PR #85: added `_aihot.initialBackfillOnly` option in feed collection to prevent historical backlog overflow on long-running feeds (addresses Issue #86).

### Fixed
- Ported upstream PR #79: normalized paths to POSIX separators in `tests/architecture.test.ts`, resolving false architecture boundary failures on Windows.
