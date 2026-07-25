"""Garrison benchmark — catalog integrity + deterministic grading + readiness.

Validates: every exercise is well-formed and maps to a tool; every track
references real exercises; the canonical correct answer PASSES each grader and a
bogus answer FAILS (graders actually discriminate); a trainee who solves a whole
track reaches mission-ready + earns the badge. Offline, deterministic.
Regenerates RESULTS.md.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from garrison import engine, grade, load_trainee  # noqa: E402
from garrison.catalog import EXERCISES, TRACKS  # noqa: E402
from garrison.models import Trainee  # noqa: E402

# canonical correct answers (the answer key lives in the harness, not the catalog)
SOLUTIONS = {
    "soc-ioc": "evil-c2.xyz", "soc-spray": "password spray", "soc-triage": "a",
    "de-sigma": "title: Mimikatz\nlogsource:\n category: process_creation\ndetection:\n s: Image|endswith mimikatz.exe\n condition: s",
    "de-yara": 'rule dosmode { strings: $a = "..." condition: $a }',
    "de-c2": "Cobalt Strike", "rt-attack": "T1078", "rt-payload": "loader",
    "rt-phish": "signed rules of engagement / authorization first",
    "mob-root": "su binary present, magisk, frida hooks, emulator artifacts",
    "mob-pin": "prevents MITM interception", "cw-gnss": "co-location signature",
    "cw-isr": "72", "cw-osint": "dark rendezvous ship-to-ship transfer",
    "cw-crypto": "indirect exposure by hop / taint",
}

GRADER_TYPES = {"mcq", "numeric", "regex", "contains", "artifact_sigma", "artifact_yara"}


def evaluate():
    ids = {e.id for e in EXERCISES}
    # integrity
    integ = all(e.objectives and e.tool and e.points > 0 and e.grader.get("type") in GRADER_TYPES
                for e in EXERCISES)
    tracks_ok = all(all(eid in ids for eid in t.exercise_ids) for t in TRACKS)
    covered = {eid for t in TRACKS for eid in t.exercise_ids}
    all_in_track = covered == ids

    # grading: correct answers pass, bogus answers fail
    passes = sum(1 for e in EXERCISES if grade(e.id, SOLUTIONS.get(e.id, "")).get("passed"))
    bogus_fail = sum(1 for e in EXERCISES if not grade(e.id, "zzz-nonsense-000").get("passed"))

    # readiness: solve the whole Cyber Warfare track -> mission-ready + badge
    cw = engine.track("Cyber Warfare Operator")
    t = Trainee("bench")
    for eid in cw.exercise_ids:
        grade(eid, SOLUTIONS[eid], trainee=t)
    r = t.track_readiness(cw, engine.by_id())
    ready_ok = r["level"] == "mission-ready" and r["badge"] == cw.badge

    return {"exercises": len(EXERCISES), "tracks": len(TRACKS),
            "catalog_integrity": integ, "tracks_reference_valid": tracks_ok,
            "every_exercise_in_a_track": all_in_track,
            "correct_answers_pass": f"{passes}/{len(EXERCISES)}",
            "bogus_answers_fail": f"{bogus_fail}/{len(EXERCISES)}",
            "capstone_readiness_ok": ready_ok,
            "all_pass": integ and tracks_ok and all_in_track and passes == len(EXERCISES)
                        and bogus_fail == len(EXERCISES) and ready_ok}


def write_results(res):
    lines = ["# Garrison — benchmark results", "",
             "Catalog integrity + deterministic grading + readiness. Offline, deterministic. "
             "Regenerate with `python bench/run_all.py`.", "",
             f"- Exercises: **{res['exercises']}** across **{res['tracks']}** role tracks",
             f"- Catalog integrity: **{res['catalog_integrity']}**",
             f"- Tracks reference valid exercises: **{res['tracks_reference_valid']}**",
             f"- Every exercise is in a track: **{res['every_exercise_in_a_track']}**",
             f"- Correct answers pass: **{res['correct_answers_pass']}**",
             f"- Bogus answers rejected: **{res['bogus_answers_fail']}**",
             f"- Capstone readiness + badge: **{res['capstone_readiness_ok']}**", ""]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(root, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    res = evaluate()
    write_results(res)
    print(json.dumps(res, indent=2))
