# Changelog

Adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] — 2026-07-24

### Added
- **Arsenal** (`arsenal.py`): the entire cognis-digital portfolio (400+ tools) auto-compiled
  into familiarization modules, classified into 12 domain tracks (Detection, Offense, Mobile,
  Firmware, OSINT, GNSS/EW, Crypto, Cloud, AppSec, AI/LLM, GRC, Threat-Intel). Garrison now
  spans **437 exercises/modules across 17 tracks** — a comprehensive soldier/enterprise kit,
  not a handful of exercises.
- **Official certificates** (`certificate.py`, `garrison certify`): a real, openable **PDF**
  Certificate of Qualification in the Cognis branded-document house style (dark-violet ground,
  off-white serif, violet accents, embedded white Cognis mark) — rendered via headless
  Chrome/Edge `--print-to-pdf`, no third-party libraries. Recipient, track/level/badge, issue
  date, deterministic credential ID + verification hash, seal, and signature line. Gracefully
  falls back to standalone branded HTML when no browser is present. Issued only when a trainee
  is qualified/mission-ready in a track.
- CLI: `garrison arsenal` (toolset by domain), `garrison certify <track>`.
- Renamed from the working prototype; 20 tests.

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
- **SDK** (`import garrison`) + **CLI** (`garrison tracks/ranges/brief/grade/curriculum/progress`)
  with local trainee persistence.
- **One-line install** (`pipx`/`pip` from GitHub, `install.sh`, `install.ps1`).
- **Verification harness** (`bench/run_all.py`): catalog integrity, correct-answers-pass
  (15/15), bogus-answers-rejected (15/15), capstone readiness + badge. 12 tests, CI 3.9–3.13.
