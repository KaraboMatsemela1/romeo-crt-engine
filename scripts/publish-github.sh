#!/usr/bin/env bash
set -euo pipefail

OWNER="KaraboMatsemela1"
REPO="romeo-crt-engine"

command -v gh >/dev/null 2>&1 || {
  echo "GitHub CLI (gh) is required: https://cli.github.com/" >&2
  exit 1
}

gh auth status

gh repo create "$OWNER/$REPO" \
  --private \
  --description "Evidence-driven CRT strategy research, validation and execution engine" \
  --source . \
  --remote origin \
  --push
