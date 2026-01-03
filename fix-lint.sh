#!/usr/bin/env bash
set -euo pipefail

# fix-lint.sh
# Convenience script to auto-format and run flake8 on the `app` directory.
# It uses isort/black/autopep8 to apply fixes where possible, then runs flake8
# to show remaining linting issues. Adjust tools as needed.

ROOT_DIR=$(dirname -- "${BASH_SOURCE[0]}")
APP_DIR="$ROOT_DIR/app"

echo "🔍 Running lint-fix for: $APP_DIR"

# Prefer using virtualenv if active; otherwise use system python
PY_CMD=${PYTHON:-python3}

echo "Installing/ensuring formatter and linter packages (flake8, black, isort, autopep8 autoflake)..."
$PY_CMD -m pip install --upgrade pip >/dev/null
$PY_CMD -m pip install --upgrade flake8 black isort autopep8 autoflake >/dev/null

echo "Running isort..."
isort "$APP_DIR"

echo "Running black..."
black "$APP_DIR"

echo "🧹 Removing unused imports & variables..."
autoflake \
  --remove-all-unused-imports \
  --remove-unused-variables \
  --ignore-init-module-imports \
  --recursive \
  --in-place \
  "$APP_DIR"

echo "🛠️  Auto-fixing formatting issues with autopep8..."
autopep8 --in-place --aggressive --aggressive --recursive "$APP_DIR"

echo "🔍 Verifying with flake8..."
flake8 "$APP_DIR"

echo "Done. If flake8 reported issues, address them or add/adjust rules in .flake8 config."
echo "✅ Linting completed successfully"

exit 0
