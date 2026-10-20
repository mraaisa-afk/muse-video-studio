#!/usr/bin/env bash
# Personalise the repository before publishing.
#
#   bash scripts/setup_repo.sh <github-username> [repo-name]
#
# Replaces the YOURNAME placeholder everywhere it appears, so clone URLs,
# issue-template links and the changelog all point at your real repository.
set -euo pipefail

USER_ARG="${1:-}"
REPO_ARG="${2:-muse-video-studio}"

if [[ -z "$USER_ARG" ]]; then
  echo "usage: bash scripts/setup_repo.sh <github-username> [repo-name]" >&2
  exit 1
fi

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
files=(
  "README.md"
  "docs/quickstart.md"
  "docs/faq.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  ".github/ISSUE_TEMPLATE/config.yml"
)

count=0
for f in "${files[@]}"; do
  [[ -f "$root/$f" ]] || continue
  if grep -q "YOURNAME" "$root/$f"; then
    sed -i.bak "s/YOURNAME/${USER_ARG}/g" "$root/$f"
    rm -f "$root/$f.bak"
    count=$((count + 1))
    echo "  updated $f"
  fi
done

if grep -rq "YOURNAME" "$root" --include="*.md" --include="*.yml" 2>/dev/null; then
  echo
  echo "  warning: YOURNAME still appears in:"
  grep -rl "YOURNAME" "$root" --include="*.md" --include="*.yml" | sed 's|'"$root"'/|    |'
fi

echo
echo "  done — ${count} file(s) updated for github.com/${USER_ARG}/${REPO_ARG}"
echo
echo "  next:"
echo "    python3 tests/run_tests.py"
echo "    git init -b main && git add . && git commit -m 'feat: video-studio skill v1.0.0'"
echo "    gh repo create ${REPO_ARG} --public --source=. --remote=origin --push"
