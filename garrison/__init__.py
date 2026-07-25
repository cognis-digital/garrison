"""Garrison — a self-hosted, offline cyber-ops training range & curriculum.

Unifies the Cognis security toolset into role-based tracks (SOC Analyst,
Detection Engineer, Red Team, Mobile Security, Cyber Warfare Operator) with
briefed exercises, deterministic offline grading, and mission-readiness scoring.
The self-hostable answer to a paid cyber-training program — code-first, no cloud.

SDK:
    import garrison
    garrison.tracks(); garrison.catalog(track="SOC Analyst")
    garrison.brief("de-sigma")
    t = garrison.load_trainee("me")
    garrison.grade("soc-spray", "password spray", trainee=t); garrison.save_trainee(t)
    garrison.readiness(t)
"""

from __future__ import annotations

__version__ = "0.2.0"

from .engine import (brief, catalog, certify, grade, load_trainee, readiness,
                     save_trainee, track, tracks)
from .models import Exercise, Track, Trainee

__all__ = ["catalog", "tracks", "track", "brief", "grade", "readiness", "certify",
           "load_trainee", "save_trainee", "Exercise", "Track", "Trainee", "__version__"]
