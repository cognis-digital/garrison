<h1 align="center">Garrison</h1>
<p align="center"><i>A self-hosted cyber-ops training range &amp; curriculum — role-based tracks, briefed exercises, offline auto-grading, mission-readiness scoring. The code-first answer to a paid cyber-training program.</i></p>
<p align="center">Part of the Cognis Neural Suite · <a href="https://cognis.digital">cognis.digital</a></p>

---

Garrison turns the Cognis security toolset into a **curriculum**. Operators run briefed
exercises across **role tracks**, submissions are **graded deterministically offline**, and
progress rolls up into **mission-readiness** with completion badges. No cloud, no seat
licenses, no data leaving your network — an **SDK + one-line CLI** you own.

## One-line install
```bash
# pipx (recommended) or pip — zero dependencies, Python 3.9+
pipx install git+https://github.com/cognis-digital/garrison
# or:  curl -sSL https://raw.githubusercontent.com/cognis-digital/garrison/main/install.sh | sh
# Windows: iwr -useb https://raw.githubusercontent.com/cognis-digital/garrison/main/install.ps1 | iex
```

## Use the CLI
```bash
garrison tracks                       # role-based curriculum paths
garrison ranges --track "SOC Analyst" # exercises in a track
garrison brief cw-gnss                # objectives, tool, hints for one exercise
garrison grade soc-spray "password spray"   # submit an answer — scored + tracked
garrison curriculum "Cyber Warfare Operator"
garrison progress                     # your readiness across every track
```

## Use the SDK
```python
import garrison
garrison.tracks()                              # the role paths
garrison.brief("de-sigma")                     # exercise brief + objectives
t = garrison.load_trainee("me")
garrison.grade("soc-spray", "password spray", trainee=t)
garrison.save_trainee(t)
garrison.readiness(t)                          # [{track, level, badge, ...}]
```

## Tracks (mission-ready role paths)
| Track | Focus | Tools it trains on |
|---|---|---|
| **SOC Analyst** | triage & first response | iocsift · logsift · hazardwatch |
| **Detection Engineer** | author & tune detections | sigmacheck · yaragen · c2detect |
| **Red Team Operator** | authorized offense + emulation | phishforge · payloadlab · advsim |
| **Mobile Security** | app & device security | rootsentry · pincheck |
| **Cyber Warfare Operator** | multi-domain capstone | spoofwatch · scryer · maritimeint · cryptotrace |

## Why it beats a paid training org
- **Self-hosted & offline** — runs on your network; nothing is uploaded.
- **Deterministic, auditable grading** — every exercise scores itself; no black box, no proctor.
- **Code-first & extensible** — add an exercise = one `Exercise(...)` with a self-contained grader; tracks are plain data.
- **Unifies real tooling** — each exercise trains on an actual open Cognis tool, not slideware.
- **Free** — no seats, no certification paywall; readiness + badges are yours.

## Verification
`python bench/run_all.py` — 15 exercises across 5 tracks: catalog integrity, every correct
answer passes (15/15), every bogus answer is rejected (15/15), and a full-track trainee
reaches **mission-ready + badge**. 12 tests, CI 3.9–3.13.

## Extend it
```python
from garrison.models import Exercise
Exercise("de-new", "Detect X", "Detection Engineer", "detection", 3, "sigmacheck",
         "Write a Sigma rule for …", ["objective"], {"type": "artifact_sigma"}, points=150)
```

---
<p align="center">© 2026 Cognis Digital LLC · <a href="https://cognis.digital">cognis.digital</a> · COCL-1.0</p>
