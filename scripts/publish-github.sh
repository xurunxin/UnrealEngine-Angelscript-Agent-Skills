#!/usr/bin/env bash
set -euo pipefail

owner="${1:-xurunxin}"
repo_name="${2:-UnrealEngine-Angelscript-Agent-Skills}"
visibility="${3:-private}"
description="Agent Skills and Wiki for UnrealEngine-Angelscript and EmmsUI development."

case "$visibility" in
  private|public|internal) ;;
  *) echo "visibility must be private, public, or internal" >&2; exit 2 ;;
esac

command -v gh >/dev/null || { echo "GitHub CLI (gh) is required." >&2; exit 1; }
command -v git >/dev/null || { echo "Git is required." >&2; exit 1; }
gh auth status >/dev/null

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

[[ -d .git ]] || { echo "Missing .git repository metadata." >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo "Working tree is not clean." >&2; exit 1; }

full_name="$owner/$repo_name"
if ! gh repo view "$full_name" >/dev/null 2>&1; then
  gh repo create "$full_name" "--$visibility" \
    --description "$description" \
    --source . \
    --remote origin
elif ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/$full_name.git"
fi

git push -u origin main
printf 'Published: https://github.com/%s\n' "$full_name"
