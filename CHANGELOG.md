# Changelog

Adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-07-24

Initial release.

### Added
- **Curriculum engine** (`models.py`, `catalog.py`, `engine.py`) — Exercises with
  self-contained deterministic graders (mcq/numeric/regex/contains/artifact-sigma/
  artifact-yara), role-based Tracks, Trainee progress + mission-readiness scoring & badges.
- **15 exercises / 5 tracks**: SOC Analyst, Detection Engineer, Red Team Operator,
  Mobile Security, Cyber Warfare Operator (multi-domain capstone) — each mapped to a real
  Cognis tool (iocsift, sigmacheck, yaragen, c2detect, phishforge, payloadlab, advsim,
  rootsentry, pincheck, spoofwatch, scryer, maritimeint, cryptotrace, logsift, hazardwatch).
- **SDK** (`import crucible`) + **CLI** (`crucible tracks/ranges/brief/grade/curriculum/progress`)
  with local trainee persistence.
- **One-line install** (`pipx`/`pip` from GitHub, `install.sh`, `install.ps1`).
- **Verification harness** (`bench/run_all.py`): catalog integrity, correct-answers-pass
  (15/15), bogus-answers-rejected (15/15), capstone readiness + badge. 12 tests, CI 3.9–3.13.
