# Crucible one-line installer (Windows). Zero dependencies; Python 3.9+.
$ErrorActionPreference = "Stop"
if (Get-Command pipx -ErrorAction SilentlyContinue) {
  pipx install "git+https://github.com/cognis-digital/crucible"
} else {
  python -m pip install --user "git+https://github.com/cognis-digital/crucible"
}
Write-Host "crucible installed - run:  crucible tracks"
