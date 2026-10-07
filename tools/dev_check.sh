#!/usr/bin/env bash
set -euo pipefail

echo "==> Environment verification"
python scripts/verify-env.py

echo "==> TypeScript typecheck"
npm run typecheck

echo "==> Web SSR build"
npm run build -w @aihot/web

echo "==> Web tests"
node --test apps/web/tests/*.test.ts

echo "==> Upstream divergence check"
python tools/check_divergence.py

echo "==> Fork divergence tests"
python tests/test_fork_divergence.py

echo ""
echo "All checks passed successfully! Ready to push to main."
