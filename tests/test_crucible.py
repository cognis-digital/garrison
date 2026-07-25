import io
import json
import os
from contextlib import redirect_stdout

import garrison
from garrison import cli, engine
from garrison.models import Exercise, Track, Trainee, grade


def test_sdk_surface():
    assert garrison.catalog() and garrison.tracks()
    assert garrison.track("SOC Analyst").name == "SOC Analyst"
    assert garrison.brief("de-sigma")["tool"] == "sigmacheck"


def test_catalog_filters():
    soc = garrison.catalog(track="SOC Analyst")
    assert soc and all(e.track == "SOC Analyst" for e in soc)
    det = garrison.catalog(domain="detection")
    assert det and all(e.domain == "detection" for e in det)


def _ex(gr, pts=100):
    return Exercise("t", "T", "Trk", "d", 1, "tool", "b", ["o"], gr, [], pts)


def test_grade_mcq():
    e = _ex({"type": "mcq", "answer": "b"})
    assert grade(e, "b")["passed"] and not grade(e, "a")["passed"]


def test_grade_numeric_tol():
    e = _ex({"type": "numeric", "answer": 72, "tol": 0})
    assert grade(e, "72")["passed"] and not grade(e, "73")["passed"]
    assert not grade(e, "not-a-number")["passed"]


def test_grade_regex():
    e = _ex({"type": "regex", "pattern": r"\bT1078\b"})
    assert grade(e, "it is T1078")["passed"] and not grade(e, "T9999")["passed"]


def test_grade_contains_any_and_all():
    ea = _ex({"type": "contains", "any": ["mitm", "interception"]})
    assert grade(ea, "prevents MITM")["passed"] and not grade(ea, "nope")["passed"]
    el = _ex({"type": "contains", "all": ["strings", "condition"]})
    assert grade(el, "has strings and condition")["passed"]
    assert not grade(el, "only strings")["passed"]  # 1/2 < 0.6


def test_grade_artifacts():
    s = _ex({"type": "artifact_sigma"}, pts=150)
    good = grade(s, "title: x\nlogsource: y\ndetection:\n condition: sel")
    assert good["passed"] and good["score"] == 150
    assert not grade(s, "title only")["passed"]
    y = _ex({"type": "artifact_yara"})
    assert grade(y, "rule r { strings: $a=1 condition: $a }")["passed"]


def test_unknown_grader():
    assert not grade(_ex({"type": "bogus"}), "x")["passed"]


def test_trainee_readiness_and_badge():
    cw = engine.track("Cyber Warfare Operator")
    bi = engine.by_id()
    t = Trainee("x")
    # not started
    assert t.track_readiness(cw, bi)["level"] == "not-started"
    # ace the whole track
    from bench.run_all import SOLUTIONS
    for eid in cw.exercise_ids:
        engine.grade(eid, SOLUTIONS[eid], trainee=t)
    r = t.track_readiness(cw, bi)
    assert r["level"] == "mission-ready" and r["badge"] == cw.badge


def test_persistence(tmp_path, monkeypatch):
    monkeypatch.setenv("GARRISON_HOME", str(tmp_path))
    import importlib
    import garrison.engine as eng
    importlib.reload(eng)
    t = eng.load_trainee("alice")
    eng.grade("soc-triage", "a", trainee=t)
    eng.save_trainee(t)
    t2 = eng.load_trainee("alice")
    assert t2.completed.get("soc-triage", 0) >= 0.6
    importlib.reload(eng)  # restore


def _run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(argv)
    return rc, buf.getvalue()


def test_cli_flow(tmp_path, monkeypatch):
    monkeypatch.setenv("GARRISON_HOME", str(tmp_path))
    assert _run(["tracks"])[0] == 0
    assert "Cyber Warfare" in _run(["tracks"])[1]
    assert _run(["ranges", "--track", "SOC Analyst"])[0] == 0
    rc, out = _run(["brief", "cw-gnss"])
    assert rc == 0 and "spoof" in out.lower()
    rc, out = _run(["grade", "soc-spray", "password spray"])
    assert rc == 0 and "PASS" in out
    rc, out = _run(["grade", "soc-spray", "brute force"])
    assert rc == 2 and "FAIL" in out
    assert _run(["curriculum", "Cyber Warfare Operator"])[0] == 0
    assert _run(["progress"])[0] == 0


def test_bench_all_pass():
    from bench.run_all import evaluate
    assert evaluate()["all_pass"] is True
