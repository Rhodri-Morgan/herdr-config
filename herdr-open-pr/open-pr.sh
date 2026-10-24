#!/usr/bin/env bash
# Opens the GitHub PR for the branch checked out in the focused pane's cwd.
set -uo pipefail

herdr_bin="${HERDR_BIN_PATH:-herdr}"

notify() { "$herdr_bin" notification show "Open PR" --body "$1" >/dev/null 2>&1 || true; }

# Action runs outside any pane, so no --current: we want the UI-focused pane.
cwd="$("$herdr_bin" pane current | jq -r '.result.pane.foreground_cwd // .result.pane.cwd // empty')"
[ -n "$cwd" ] || { notify "No focused pane cwd"; exit 1; }

url="$(cd "$cwd" && gh pr view --json url -q .url 2>&1)" || { notify "${url:-No PR for this branch}"; exit 1; }

if [ -x /mnt/c/Windows/explorer.exe ]; then
  /mnt/c/Windows/explorer.exe "$url"   # WSL; exits non-zero even on success
elif command -v xdg-open >/dev/null; then
  xdg-open "$url"
else
  open "$url"
fi
exit 0
