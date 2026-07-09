#!/usr/bin/env bash
# Build PDF guides (desktop + mobile) from dedicated Python builders.
#
# Usage:
#   ./build.sh template
#   ./build.sh all
#
# Output: ../pdf/desktop/<slug>.pdf and ../pdf/mobile/<slug>.pdf
# Requires: python3, node, and npm install in this directory.
# Chromium: set CHROME_PATH to your Chrome/Chromium binary if the default is unavailable.
set -euo pipefail
cd "$(dirname "$0")"
REPO="$(cd .. && pwd)"
OUTDIR="$REPO/pdf"
mkdir -p "$OUTDIR" _html

declare -A SLUG=(
  [template]=template-style-reference
)

declare -A BUILDER=(
  [template]=pages/template.py
)

build_one () {
  local id="$1" slug="${SLUG[$1]:-}" builder="${BUILDER[$1]:-}"
  [ -z "$slug" ] && { echo "unknown page id: $1 (use: ${!SLUG[*]})"; return 1; }
  python3 "$builder" >/dev/null
  node render.js "_html/$slug.html" "$OUTDIR/$slug"
  echo "built $slug -> pdf/desktop/$slug.pdf + pdf/mobile/$slug.pdf"
}

if [ "$#" -eq 0 ]; then
  echo "usage: ./build.sh <id...|all> (ids: ${!SLUG[*]})"; exit 1
fi
if [ "$1" = "all" ]; then set -- "${!SLUG[@]}"; fi
for a in "$@"; do build_one "$a"; done
