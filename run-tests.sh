#!/usr/bin/env bash

set -e  # exit immediately if a command fails

echo "🔍 Running tests with coverage..."

# Activate virtualenv if needed (optional)
# source venv/bin/activate

# Environment for tests
export ENV=test
export DATABASE_URL=sqlite:///:memory:

pytest \
  --verbose \
  --disable-warnings \
  --maxfail=1 \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=html \
  app/tests/

echo "✅ Tests completed successfully"
echo "📊 Coverage HTML report generated at: htmlcov/index.html"
