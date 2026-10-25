# Dependency freshness report

## GitHub Actions (pinned in .github/workflows/)

| Package | Declared in | Requirement | Latest | Status |
| --- | --- | --- | --- | --- |
| `actions/checkout` | `check.yml, codeql.yml, dependency-freshness.yml, fork-check.yml, upstream-check.yml` | `actions/checkout@v7.0.1` | `7.0.1` | OK |
| `actions/setup-node` | `check.yml, fork-check.yml` | `actions/setup-node@v7.0.0` | `7.1.0` | DEFERRED at 7.1.0: check.yml uses upstream v7.0.0; deferred to avoid divergence on upstream-held workflow; re-evaluated 2026-10-24, still held; review when upstream moves check.yml |
| `actions/setup-python` | `dependency-freshness.yml, fork-check.yml, upstream-check.yml` | `actions/setup-python@v7.1.0` | `7.1.0` | OK |
| `github/codeql-action/analyze` | `codeql.yml` | `github/codeql-action/analyze@v4.39.1` | `4.39.1` | OK |
| `github/codeql-action/init` | `codeql.yml` | `github/codeql-action/init@v4.39.1` | `4.39.1` | OK |