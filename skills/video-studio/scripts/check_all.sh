#!/usr/bin/env bash
# Both gates, one command.
#   bash scripts/check_all.sh storyboard.json [master.mp4]
set -uo pipefail

SB="${1:-assets/storyboard.template.json}"
VID="${2:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rc=0

PLATFORM="$(python3 -c "
import json,sys
try:
    print(json.load(open('$SB')).get('project',{}).get('platform','youtube_shorts'))
except Exception:
    print('youtube_shorts')
")"

echo
echo "── Gate A · storyboard lint ─────────────────────────────────────"
python3 "$here/lint_storyboard.py" "$SB" || rc=1

if [[ -n "$VID" ]]; then
  echo
  echo "── Gate B · render QC ($PLATFORM) ──────────────────────────────"
  python3 "$here/qc_video.py" "$VID" --platform "$PLATFORM" || rc=1
else
  echo
  echo "  (no video given — Gate B skipped)"
fi

echo
if [[ $rc -eq 0 ]]; then
  echo "  GATES CLEAR — structure and render are sound. Voice, lip-sync and mix still need a human."
else
  echo "  GATES NOT CLEAR — fix and re-run before publishing."
fi
exit $rc
