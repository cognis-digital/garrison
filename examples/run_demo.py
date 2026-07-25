"""Example: browse tracks, grade a couple exercises, show readiness."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import garrison  # noqa: E402

def main():
    print("Tracks:", [t.name for t in garrison.tracks()])
    t = garrison.Trainee("demo")
    for ex, ans in [("soc-spray", "password spray"), ("cw-gnss", "co-location"),
                    ("cw-isr", "72")]:
        r = garrison.grade(ex, ans, trainee=t)
        print(f"  {ex}: {'PASS' if r['passed'] else 'FAIL'} ({r['score']}/{r['max']})")
    for r in garrison.readiness(t):
        if r["completed"]:
            print(f"  {r['track']}: {r['level']} ({r['completed']}/{r['total']})")

if __name__ == "__main__":
    main()
