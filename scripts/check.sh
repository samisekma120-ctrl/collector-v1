#!/usr/bin/env bash
set -euo pipefail

echo "== Backend: ruff =="
ruff check .

echo "== Backend: pytest =="
pytest -q

echo "== Frontend: npm ci + build =="
pushd frontend-react >/dev/null
npm ci
npm run build
popd >/dev/null

echo "✅ Quality gate OK"
