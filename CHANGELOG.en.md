# Changelog

All notable changes to this fork (`SanHsien/AIHOT`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This file records only the changes made by this fork; for upstream changes, see upstream releases.

## [Unreleased]

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
