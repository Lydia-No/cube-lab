#!/usr/bin/env bash
set -euo pipefail

diag_one() {
  local name="$1"
  local hex="$2"
  echo "== ${name} (U+${hex}) =="

  if fc-list ":charset=${hex}" | head -1 >/dev/null 2>&1; then
    echo "YES ✅"
    echo "-- top matches (fc-match -s) --"
    fc-match -s "sans:charset=${hex}" | head -10
    echo "-- sample font files (fc-list) --"
    fc-list ":charset=${hex}" | head -10
  else
    echo "NO ❌"
  fi
  echo
}

echo "Rebuilding cache..."
fc-cache -f >/dev/null 2>&1 || true
echo

diag_one "Hebrew"    "0590"
diag_one "Runic"     "16A0"
diag_one "Cuneiform" "12000"
