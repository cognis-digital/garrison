#!/bin/sh
# Garrison one-line installer. Zero dependencies; Python 3.9+.
set -e
if command -v pipx >/dev/null 2>&1; then
  pipx install "git+https://github.com/cognis-digital/garrison"
else
  python3 -m pip install --user "git+https://github.com/cognis-digital/garrison"
fi
echo "garrison installed — run:  garrison tracks"
