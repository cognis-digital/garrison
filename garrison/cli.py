"""Garrison CLI."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__, engine


def cmd_tracks(args):
    for t in engine.tracks():
        print(f"  {t.name:24} ({len(t.exercise_ids)} exercises)  — {t.description}")
        print(f"      badge: {t.badge}")
    return 0


def cmd_ranges(args):
    rows = engine.catalog(track=args.track, domain=args.domain)
    for e in rows:
        print(f"  {e.id:10} [{'*'*e.difficulty:5}] {e.track:22} {e.title}  (tool: {e.tool})")
    print(f"  {len(rows)} exercises")
    return 0


def cmd_brief(args):
    b = engine.brief(args.id)
    if not b:
        print(f"no exercise '{args.id}'"); return 1
    print(f"# {b['title']}  [{b['track']} · {b['domain']} · difficulty {b['difficulty']} · {b['points']}pts]")
    print(f"tool: {b['tool']}\n\n{b['brief']}\n")
    print("Objectives:"); [print(f"  - {o}") for o in b["objectives"]]
    if b["hints"]:
        print("Hints:"); [print(f"  ? {h}") for h in b["hints"]]
    print(f"\nGrade with:  garrison grade {b['id']} \"<your answer>\"")
    return 0


def cmd_grade(args):
    t = engine.load_trainee(args.trainee)
    r = engine.grade(args.id, args.submission, trainee=t)
    if "error" in r:
        print(r["error"]); return 1
    engine.save_trainee(t)
    mark = "PASS" if r["passed"] else "FAIL"
    print(f"[{mark}] {r['score']}/{r['max']} — {r['feedback']}")
    return 0 if r["passed"] else 2


def cmd_curriculum(args):
    t = engine.track(args.role)
    if not t:
        print(f"no track '{args.role}'. Try: " + ", ".join(x.name for x in engine.tracks())); return 1
    bi = engine.by_id()
    print(f"# {t.name} — {t.description}  (badge: {t.badge})")
    for i, eid in enumerate(t.exercise_ids, 1):
        e = bi[eid]
        print(f"  {i}. {eid:10} {e.title}  (tool: {e.tool}, {e.points}pts)")
    return 0


def cmd_certify(args):
    t = engine.load_trainee(args.trainee)
    r = engine.certify(t, args.track, out_path=args.out)
    if "error" in r:
        print(r["error"]); return 1
    print(f"[+] certificate issued -> {r['path']}")
    print(f"    {r['level']} · {r['badge']} · credential {r['credential_id']}")
    return 0


def cmd_arsenal(args):
    from collections import Counter
    dom = Counter(e.domain for e in engine.catalog() if e.id.startswith("arsenal-"))
    total = sum(dom.values())
    print(f"# Arsenal — {total} tools as training modules, across {len(dom)} domains")
    for d, n in dom.most_common():
        print(f"  {d:14} {n} tools")
    print("\n(hand-crafted core exercises are listed under `garrison ranges`)")
    return 0


def cmd_progress(args):
    t = engine.load_trainee(args.trainee)
    print(f"# Progress — {t.name}")
    for r in engine.readiness(t):
        badge = f"  🏅 {r['badge']}" if r["badge"] else ""
        print(f"  {r['track']:24} {r['completed']}/{r['total']}  avg {r['avg_score']:.2f}  "
              f"[{r['level']}]{badge}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="garrison",
                                description="Self-hosted cyber-ops training range & curriculum — Cognis Digital")
    p.add_argument("--version", action="version", version=f"garrison {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("tracks", help="list role-based curriculum tracks").set_defaults(func=cmd_tracks)

    r = sub.add_parser("ranges", help="list exercises (filter by --track / --domain)")
    r.add_argument("--track"); r.add_argument("--domain"); r.set_defaults(func=cmd_ranges)

    b = sub.add_parser("brief", help="show an exercise brief + objectives")
    b.add_argument("id"); b.set_defaults(func=cmd_brief)

    g = sub.add_parser("grade", help="submit an answer to an exercise (scored, tracked)")
    g.add_argument("id"); g.add_argument("submission")
    g.add_argument("--trainee", default="default"); g.set_defaults(func=cmd_grade)

    c = sub.add_parser("curriculum", help="show a role's ordered exercise path")
    c.add_argument("role"); c.set_defaults(func=cmd_curriculum)

    pr = sub.add_parser("progress", help="show a trainee's readiness across tracks")
    pr.add_argument("--trainee", default="default"); pr.set_defaults(func=cmd_progress)

    a = sub.add_parser("arsenal", help="the whole toolset as training modules, by domain")
    a.set_defaults(func=cmd_arsenal)

    ct = sub.add_parser("certify", help="issue an official certificate for a qualified track")
    ct.add_argument("track"); ct.add_argument("--trainee", default="default")
    ct.add_argument("--out"); ct.set_defaults(func=cmd_certify)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
