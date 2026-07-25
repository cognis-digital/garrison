"""Garrison engine — the SDK surface: browse the catalog, brief/grade exercises,
track a trainee's progress and readiness. Pure stdlib; progress persists to JSON.
"""

from __future__ import annotations

import json
import os

from . import arsenal
from .catalog import EXERCISES, TRACKS
from .models import Trainee, grade as _grade

HOME = os.environ.get("GARRISON_HOME") or os.path.join(os.path.expanduser("~"), ".garrison")


def all_exercises():
    """Hand-crafted core exercises + the auto-generated arsenal (whole portfolio)."""
    return EXERCISES + arsenal.build()[0]


def all_tracks():
    return TRACKS + arsenal.build()[1]


def by_id():
    return {e.id: e for e in all_exercises()}


def catalog(track=None, domain=None):
    out = all_exercises()
    if track:
        out = [e for e in out if e.track.lower() == track.lower()]
    if domain:
        out = [e for e in out if e.domain.lower() == domain.lower()]
    return out


def tracks():
    return all_tracks()


def track(name):
    for t in all_tracks():
        if t.name.lower() == name.lower():
            return t
    return None


def brief(exercise_id):
    e = by_id().get(exercise_id)
    if not e:
        return None
    return {"id": e.id, "title": e.title, "track": e.track, "domain": e.domain,
            "difficulty": e.difficulty, "tool": e.tool, "points": e.points,
            "brief": e.brief, "objectives": e.objectives, "hints": e.hints}


def grade(exercise_id, submission, trainee: "Trainee" = None):
    e = by_id().get(exercise_id)
    if not e:
        return {"error": f"no exercise '{exercise_id}'"}
    result = _grade(e, submission)
    if trainee is not None:
        trainee.record(e, result)
    return result


def readiness(trainee: "Trainee"):
    bi = by_id()
    return [trainee.track_readiness(t, bi) for t in all_tracks()]


def certify(trainee: "Trainee", track_name, out_path=None):
    """Issue an official certificate IF the trainee is qualified in the track."""
    from . import certificate
    t = track(track_name)
    if not t:
        return {"error": f"no track '{track_name}'"}
    r = trainee.track_readiness(t, by_id())
    if r["level"] not in ("qualified", "mission-ready"):
        return {"error": f"not yet qualified in '{t.name}' (status: {r['level']}, "
                         f"{r['completed']}/{r['total']} done)"}
    if not out_path:
        os.makedirs(os.path.join(HOME, "certs"), exist_ok=True)
        safe = "".join(c if c.isalnum() else "_" for c in f"{trainee.name}_{t.name}")
        out_path = os.path.join(HOME, "certs", safe + ".pdf")
    certificate.write(trainee.name, t.name, r["level"], t.badge, out_path,
                      score=r["avg_score"])
    return {"path": out_path, "level": r["level"], "badge": t.badge,
            "credential_id": certificate.credential_id(
                trainee.name, t.name, __import__("datetime").date.today().isoformat())}


# ---- trainee persistence -------------------------------------------------
def _path(name):
    os.makedirs(HOME, exist_ok=True)
    safe = "".join(c if c.isalnum() else "_" for c in name)
    return os.path.join(HOME, f"trainee_{safe}.json")


def load_trainee(name="default") -> "Trainee":
    p = _path(name)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        return Trainee(d.get("name", name), d.get("completed", {}))
    return Trainee(name)


def save_trainee(trainee: "Trainee"):
    p = _path(trainee.name)
    json.dump({"name": trainee.name, "completed": trainee.completed},
              open(p, "w", encoding="utf-8"), indent=2)
    return p
