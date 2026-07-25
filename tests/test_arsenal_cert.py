import os

import garrison
from garrison import arsenal, certificate, engine
from garrison.models import Trainee, grade


def test_arsenal_scale_and_tracks():
    mods, tracks = arsenal.build()
    assert len(mods) > 300                        # whole portfolio → modules
    assert any(t.name.startswith("Arsenal ·") for t in tracks)
    # merged into the engine
    assert len(garrison.catalog()) > 300
    assert len(garrison.tracks()) >= 15


def test_arsenal_modules_wellformed():
    mods, _ = arsenal.build()
    for m in mods[:50]:
        assert m.objectives and m.tool and m.grader["type"] == "contains"
        assert m.grader.get("any")
        assert m.domain


def test_arsenal_module_gradeable():
    mods, _ = arsenal.build()
    m = mods[0]
    # naming a key term from the tool's own description passes its check
    assert grade(m, m.grader["any"][0])["passed"]


def test_arsenal_every_module_in_a_track():
    mods, tracks = arsenal.build()
    covered = {eid for t in tracks for eid in t.exercise_ids}
    assert {m.id for m in mods} <= covered


def test_credential_id_deterministic():
    a = certificate.credential_id("Jane Doe", "SOC Analyst", "2026-07-24")
    b = certificate.credential_id("Jane Doe", "SOC Analyst", "2026-07-24")
    c = certificate.credential_id("John Doe", "SOC Analyst", "2026-07-24")
    assert a == b and a != c and a.startswith("CNS-GAR-")


def test_certificate_html_content():
    h = certificate.render_html("Cpl. A. Stone", "Detection Engineer", "mission-ready",
                                "DETECTION-ENGINEER-QUALIFIED", date_str="2026-07-24", score=0.92)
    assert h.startswith("<!doctype html") and h.rstrip().endswith("</html>")
    assert "Cpl. A. Stone" in h and "Detection Engineer" in h
    assert "MISSION-READY" in h and "DETECTION-ENGINEER-QUALIFIED" in h
    assert "COGNIS DIGITAL" in h and "data:image/png;base64," in h  # branded + logo embedded


def test_certify_refuses_then_issues(tmp_path, monkeypatch):
    monkeypatch.setenv("GARRISON_HOME", str(tmp_path))
    import importlib
    import garrison.engine as eng
    importlib.reload(eng)
    t = Trainee("Recruit")
    # not qualified yet -> refused
    assert "error" in eng.certify(t, "SOC Analyst")
    # qualify the whole track
    for ex, ans in [("soc-ioc", "evil-c2.xyz"), ("soc-spray", "password spray"),
                    ("soc-triage", "a")]:
        eng.grade(ex, ans, trainee=t)
    r = eng.certify(t, "SOC Analyst", out_path=str(tmp_path / "cert.pdf"))
    assert "path" in r and os.path.exists(r["path"])   # .pdf if a browser is present, else .html
    assert r["credential_id"].startswith("CNS-GAR-")
    importlib.reload(eng)


def test_html_escape_in_name():
    h = certificate.render_html("<script>x", "SOC Analyst", "qualified", "B", date_str="2026-07-24")
    assert "<script>x" not in h and "&lt;script&gt;" in h
