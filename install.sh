#!/bin/sh
# Crucible one-line installer. Zero dependencies; Python 3.9+.
set -e
if command -v pipx >/dev/null 2>&1; then
  pipx install "git+https://github.com/cognis-digital/crucible"
else
  python3 -m pip install --user "git+https://github.com/cognis-digital/crucible"
fi
echo "crucible installed — run:  crucible tracks"
