"""Arsenal — turn the entire cognis-digital repo portfolio into training modules.

Every tool in the arsenal becomes a familiarization module: classified into a
domain, briefed from its real description, and graded by a deterministic
knowledge check (name what the tool does). This is what makes Garrison a
*comprehensive* kit — a soldier or enterprise team can train across the whole
toolset, not a handful of exercises. Generated from the bundled inventory; pure stdlib.
"""

from __future__ import annotations

import json
import os
import re

from .models import Exercise, Track

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arsenal_data.json")

# domain classification (keyword → domain) + the track it rolls into
DOMAINS = [
    ("detection", "Detection & Hunting", r"detect|sigma|yara|siem|hunt|ioc|c2|beacon|edr|threat|anomal|log|malware|forensic"),
    ("offense", "Offensive & Red Team", r"red.?team|offens|exploit|payload|adversary|phish|recon|attack|pentest|fuzz"),
    ("mobile", "Mobile Security", r"mobile|android|\bios\b|\bapk\b|mastg|jailbreak|root"),
    ("firmware", "Firmware & Hardware", r"firmware|uefi|bios|secure.?boot|hardware|jtag|\brf\b|embedded|rtos|packer|binary"),
    ("osint", "OSINT & Situational Awareness", r"osint|maritime|\bais\b|adsb|ads-b|vessel|conflict|situational|geoint|satellite|recon|drone|uas"),
    ("gnss", "GNSS / EW", r"gnss|gps|spoof|jam|interference|navigation"),
    ("crypto", "Crypto & Blockchain", r"blockchain|crypto|wallet|sanction|token|defi|onchain|ledger|cipher"),
    ("cloud", "Cloud & Kubernetes", r"kubernetes|k8s|cloud|container|terraform|\biac\b|admission|serverless|docker"),
    ("appsec", "AppSec & Supply Chain", r"sbom|dependency|supply.?chain|sql|cors|api|waf|secret|cert|tls|pki|oauth"),
    ("ai", "AI / LLM Security", r"\bmcp\b|\bllm\b|agent|prompt|model|rag|skill|neural|inference"),
    ("grc", "GRC & Compliance", r"compliance|fedramp|oscal|stig|nist|rmf|cmmc|soc.?2|hipaa|poam|clearance|scif|readiness|governance"),
    ("intel", "Threat Intelligence", r"cti|intel|report|enrich|attribution|actor|campaign"),
]

_STOP = set("the a an and or of to in for with is are be it this that your you use using into from "
            "self hosted self-hosted open source local cli tool run runs generate detect".split())


def _domain(name, desc):
    blob = (name + " " + (desc or "")).lower()
    for key, _label, pat in DOMAINS:
        if re.search(pat, blob):
            return key
    return "appsec"  # sensible default bucket


def _key_terms(name, desc):
    """Distinctive words a trainee could name to show they know the tool."""
    words = [w for w in re.split(r"[^a-z0-9]+", (desc or "").lower())
             if len(w) >= 4 and w not in _STOP]
    seen, terms = set(), []
    for w in words:
        if w not in seen:
            seen.add(w); terms.append(w)
        if len(terms) >= 6:
            break
    nm = name.replace("cognis-", "").lower()
    return list(dict.fromkeys([nm] + terms))[:6] or [nm]


def _load():
    with open(_DATA, encoding="utf-8") as f:
        return json.load(f)


_CACHE = None


def build():
    """Return (modules, tracks) generated from the full arsenal. Cached."""
    global _CACHE
    if _CACHE:
        return _CACHE
    repos = [r for r in _load() if (r.get("description") or "").strip()]
    label = {k: lbl for k, lbl, _ in DOMAINS}
    label["appsec"] = "AppSec & Supply Chain"
    modules, by_domain = [], {}
    for r in repos:
        name = r["name"]
        # skip meta/umbrella + boundary-sensitive repos from training modules
        low = (name + " " + (r.get("description") or "")).lower()
        if any(b in low for b in ("weapon", "target prioritization", "face recogn",
                                  "awesome-", "neural-suite", "arsenal")):
            continue
        dom = _domain(name, r.get("description"))
        track_name = f"Arsenal · {label[dom]}"
        ex = Exercise(
            id=f"arsenal-{name.replace('cognis-', '')}"[:48],
            title=f"Field the tool: {name}", track=track_name, domain=dom,
            difficulty=2, tool=name, brief=(r.get("description") or "").strip(),
            objectives=[f"Know what {name} does and when to reach for it",
                        f"Run {name} on a sample and read its output"],
            grader={"type": "contains", "any": _key_terms(name, r.get("description"))},
            hints=[f"Read the {name} README; the answer is its core function"],
            points=50)
        modules.append(ex)
        by_domain.setdefault(dom, []).append(ex.id)
    tracks = [Track(f"Arsenal · {label[d]}",
                    f"Familiarization across every {label[d]} tool in the arsenal.",
                    ids, f"ARSENAL-{d.upper()}-FAMILIAR")
              for d, ids in sorted(by_domain.items())]
    _CACHE = (modules, tracks)
    return _CACHE
