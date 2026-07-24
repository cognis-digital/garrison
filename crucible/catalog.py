"""Crucible catalog — the curriculum: exercises (each mapped to a Cognis tool +
a self-contained grader) organized into role-based tracks. Content, no logic.
"""

from __future__ import annotations

from .models import Exercise, Track

EXERCISES = [
    # ---------------- SOC Analyst ----------------
    Exercise("soc-ioc", "Free the indicators", "SOC Analyst", "triage", 1, "iocsift",
             "An advisory names the C2 domain `evil-c2[.]xyz`. Defang-free, extract it.",
             ["Recognize a defanged IOC", "Normalize to a usable domain"],
             {"type": "contains", "any": ["evil-c2.xyz"]},
             ["'[.]' is a defang of '.'"], 100),
    Exercise("soc-spray", "Name the auth attack", "SOC Analyst", "detection", 2, "logsift",
             "50 failed logins across 50 accounts, 1 try each, from one IP in 2 min. What is it?",
             ["Distinguish brute-force vs password-spray"],
             {"type": "mcq", "answer": "password spray",
              "choices": ["brute force", "password spray", "credential stuffing"]},
             ["Few attempts, many accounts = spray"], 100),
    Exercise("soc-triage", "Rank the emergency", "SOC Analyst", "triage", 2, "hazardwatch",
             "Two alerts: (A) tornado warning over a data center, (B) a routine cert expiry in 30d. "
             "Which is severity EXTREME?",
             ["Map alert to severity"],
             {"type": "mcq", "answer": "a", "choices": ["a", "b"]}, [], 100),

    # ---------------- Detection Engineer ----------------
    Exercise("de-sigma", "Author a Sigma rule", "Detection Engineer", "detection", 3, "sigmacheck",
             "Write a minimal Sigma rule detecting process creation of `mimikatz.exe`.",
             ["Structure a Sigma rule", "logsource + detection + condition"],
             {"type": "artifact_sigma"},
             ["Needs title, logsource, detection, condition"], 150),
    Exercise("de-yara", "Author a YARA rule", "Detection Engineer", "detection", 3, "yaragen",
             "Write a YARA rule matching the string 'this program cannot be run in DOS mode'.",
             ["Structure a YARA rule", "strings + condition"],
             {"type": "artifact_yara"}, ["rule X { strings: ... condition: ... }"], 150),
    Exercise("de-c2", "Name the framework", "Detection Engineer", "detection", 4, "c2detect",
             "A beacon uses a JARM/JA4 fingerprint + named-pipe pattern classic to which C2?",
             ["Attribute infra to a C2 family"],
             {"type": "contains", "any": ["cobalt strike", "cobaltstrike"]},
             ["The most-emulated commercial C2"], 150),

    # ---------------- Red Team Operator ----------------
    Exercise("rt-attack", "Map to ATT&CK", "Red Team Operator", "offense", 3, "advsim",
             "Give the MITRE ATT&CK technique ID for 'Valid Accounts'.",
             ["Reference ATT&CK technique IDs"],
             {"type": "regex", "pattern": r"\bT1078\b"}, ["Txxxx format"], 120),
    Exercise("rt-payload", "Classify the payload", "Red Team Operator", "offense", 2, "payloadlab",
             "A .lnk file spawns powershell -enc <base64>. Payload category?",
             ["Recognize LOLBin/loader patterns"],
             {"type": "contains", "any": ["loader", "downloader", "stager"]}, [], 100),
    Exercise("rt-phish", "Scope a phish (authorized)", "Red Team Operator", "offense", 2, "phishforge",
             "Name the FIRST control that must exist before running a phishing simulation.",
             ["Authorization precedes action"],
             {"type": "contains", "any": ["authorization", "scope", "consent", "rules of engagement", "roe"]},
             ["scopeward exists for this reason"], 100),

    # ---------------- Mobile Security ----------------
    Exercise("mob-root", "Spot the rooted device", "Mobile Security", "mobile", 2, "rootsentry",
             "List two runtime signals that indicate a rooted/jailbroken device.",
             ["Enumerate integrity signals"],
             {"type": "contains", "any": ["su ", "magisk", "frida", "hook", "emulator", "jailbreak", "root"]},
             [], 100),
    Exercise("mob-pin", "Why pin certificates", "Mobile Security", "mobile", 3, "pincheck",
             "In one word, TLS pinning defends against which class of attacker on the network?",
             ["Understand MITM risk"],
             {"type": "contains", "any": ["mitm", "man-in-the-middle", "interception", "proxy"]}, [], 100),

    # ---------------- Cyber Warfare Operator (flagship, multi-domain) ----------------
    Exercise("cw-gnss", "Read the spoof signature", "Cyber Warfare Operator", "cyberwar", 4, "spoofwatch",
             "Many distinct aircraft suddenly report the SAME position. Spoofing signature name?",
             ["Recognize GNSS spoofing signatures"],
             {"type": "contains", "any": ["co-location", "colocation", "same point", "co location"]},
             ["vs. a kinematic 'teleport'"], 150),
    Exercise("cw-isr", "Interpret the ISR read-out", "Cyber Warfare Operator", "cyberwar", 4, "scryer",
             "Observer says: 228 contacts, 156 non-cooperative. How many are cooperative (AIS/ADS-B)?",
             ["Reason over fused multi-INT counts"],
             {"type": "numeric", "answer": 72, "tol": 0}, ["228 - 156"], 150),
    Exercise("cw-osint", "Attribute the vessel", "Cyber Warfare Operator", "cyberwar", 4, "maritimeint",
             "A ship goes dark, meets another at sea, reappears heavier. What evasion pattern?",
             ["Recognize sanctions-evasion at sea"],
             {"type": "contains", "any": ["dark rendezvous", "ship-to-ship", "sts", "rendezvous", "transfer"]},
             [], 150),
    Exercise("cw-crypto", "Trace the sanction", "Cyber Warfare Operator", "cyberwar", 5, "cryptotrace",
             "An address is 2 hops from an OFAC-listed wallet. Exposure type?",
             ["Distinguish direct vs indirect exposure"],
             {"type": "contains", "any": ["indirect", "hop", "taint", "proximity"]}, [], 150),
]

TRACKS = [
    Track("SOC Analyst", "Triage and first response.",
          ["soc-ioc", "soc-spray", "soc-triage"], "SOC-ANALYST-QUALIFIED"),
    Track("Detection Engineer", "Author and tune detections.",
          ["de-sigma", "de-yara", "de-c2"], "DETECTION-ENGINEER-QUALIFIED"),
    Track("Red Team Operator", "Authorized offense + emulation.",
          ["rt-phish", "rt-payload", "rt-attack"], "RED-TEAM-QUALIFIED"),
    Track("Mobile Security", "Mobile app & device security.",
          ["mob-root", "mob-pin"], "MOBILE-SECURITY-QUALIFIED"),
    Track("Cyber Warfare Operator", "Multi-domain cyber + GNSS + ISR + OSINT (capstone).",
          ["cw-gnss", "cw-isr", "cw-osint", "cw-crypto"], "CYBER-WARFARE-OPERATOR"),
]
