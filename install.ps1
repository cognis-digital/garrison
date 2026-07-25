# Garrison one-line installer (Windows). Zero dependencies; Python 3.9+.
$ErrorActionPreference = "Stop"
if (Get-Command pipx -ErrorAction SilentlyContinue) {
  pipx install "git+https://github.com/cognis-digital/garrison"
} else {
  python -m pip install --user "git+https://github.com/cognis-digital/garrison"
}
Write-Host "garrison installed - run:  garrison tracks"
