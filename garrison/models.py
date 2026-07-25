"""Garrison core models — Exercise, Track, Trainee — and a deterministic grader.

An Exercise is one range task with objectives and a *self-contained* grader (no
external service needed to score). A Track is a role-based curriculum path. A
Trainee accumulates scores → readiness. Pure stdlib.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


@dataclass
class Exercise:
    id: str
    title: str
    track: str            # role this belongs to (SOC, RedTeam, ...)
    domain: str           # detection | offense | mobile | osint | grc | cyberwar ...
    difficulty: int       # 1..5
    tool: str             # the Cognis tool used to learn/solve it
    brief: str
    objectives: list
    grader: dict          # {"type": ..., ...} — see grade()
    hints: list = field(default_factory=list)
    points: int = 100

    def as_dict(self):
        return asdict(self)


@dataclass
class Track:
    name: str             # role, e.g. "Detection Engineer"
    description: str
    exercise_ids: list
    badge: str            # awarded at completion


def grade(exercise: "Exercise", submission: str) -> dict:
    """Deterministic, offline grading. Returns {passed, score, max, feedback}."""
    g = exercise.grader
    t = g.get("type")
    sub = (submission or "").strip()
    mx = exercise.points
    lo = sub.lower()

    def ok(score, msg):
        return {"passed": score >= mx * 0.6, "score": round(score, 1), "max": mx, "feedback": msg}

    if t == "mcq":
        return ok(mx if lo == str(g["answer"]).lower() else 0,
                  "correct" if lo == str(g["answer"]).lower() else f"expected {g['answer']}")
    if t == "numeric":
        try:
            passed = abs(float(sub) - float(g["answer"])) <= float(g.get("tol", 0))
        except ValueError:
            passed = False
        return ok(mx if passed else 0, "correct" if passed else f"expected ~{g['answer']}")
    if t == "regex":
        passed = re.search(g["pattern"], sub, re.I) is not None
        return ok(mx if passed else 0, "matches" if passed else "no match for expected pattern")
    if t == "contains":
        need = [k.lower() for k in g["all"]] if "all" in g else [k.lower() for k in g.get("any", [])]
        hits = [k for k in need if k in lo]
        if "all" in g:
            score = mx * (len(hits) / len(need)) if need else 0
            return ok(score, f"{len(hits)}/{len(need)} required elements present")
        return ok(mx if hits else 0, "found expected term" if hits else "missing expected term(s)")
    if t == "artifact_sigma":
        need = ["title", "logsource", "detection", "condition"]
        hits = [k for k in need if k in lo]
        score = mx * (len(hits) / len(need))
        return ok(score, f"sigma structure {len(hits)}/{len(need)} (title/logsource/detection/condition)")
    if t == "artifact_yara":
        need = ["rule ", "strings:", "condition:"]
        hits = [k for k in need if k in lo]
        score = mx * (len(hits) / len(need))
        return ok(score, f"yara structure {len(hits)}/{len(need)}")
    return {"passed": False, "score": 0, "max": mx, "feedback": f"unknown grader '{t}'"}


@dataclass
class Trainee:
    name: str
    completed: dict = field(default_factory=dict)   # exercise_id -> score(0..1)

    def record(self, exercise: "Exercise", result: dict):
        self.completed[exercise.id] = round(result["score"] / result["max"], 3) if result["max"] else 0.0

    def track_readiness(self, track: "Track", by_id: dict) -> dict:
        scores = [self.completed.get(eid, 0.0) for eid in track.exercise_ids]
        done = sum(1 for s in scores if s >= 0.6)
        avg = sum(scores) / len(scores) if scores else 0.0
        level = ("mission-ready" if done == len(scores) and avg >= 0.85 else
                 "qualified" if done >= len(scores) * 0.7 else
                 "in-training" if done else "not-started")
        return {"track": track.name, "completed": done, "total": len(scores),
                "avg_score": round(avg, 3), "level": level,
                "badge": track.badge if level == "mission-ready" else None}
