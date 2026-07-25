"""Official certificate generator — ANVIL-branded HTML → PDF.

Matches the Cognis branded-document house style (project-anvil): dark-violet
ground, off-white serif, violet accents, white Cognis logo (data-URI), NO gold —
rendered to PDF via headless Chrome/Edge (`--print-to-pdf`). Opens in PDFGear /
Photos / any viewer. The same recipe drives every branded PDF and pitch deck.

Falls back to writing the .html (and always leaves a deterministic credential ID).
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import html
import os
import subprocess

_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(_DIR, "logo_white.png")

# --- Cognis house palette (from project-anvil DESIGN) ---
GROUND, SURFACE, PANEL = "#0a0713", "#160f2b", "#1c1536"
INK, SOFT, FAINT, LINE = "#f3eefc", "#bcb0d6", "#8478a3", "#332a52"
VIOLET, VIOLET2, DEEP = "#8b5cf6", "#a78bfa", "#6d28d9"

_BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def credential_id(trainee, track, date_str):
    h = hashlib.sha256(f"{trainee}|{track}|{date_str}".encode()).hexdigest()
    return "CNS-GAR-" + h[:12].upper()


def _logo_uri():
    try:
        with open(LOGO, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def render_html(trainee, track, level, badge, *, date_str=None, score=None,
                issuer="Cognis Digital LLC", signatory="Director, Cognis Digital"):
    date_str = date_str or datetime.date.today().isoformat()
    cid = credential_id(trainee, track, date_str)
    e = html.escape
    kind = "QUALIFICATION" if level in ("mission-ready", "qualified") else "COMPLETION"
    score_html = (f'<span class="dot">&middot;</span> composite score '
                  f'<b>{round(score*100)}%</b>' if score is not None else '')
    logo = _logo_uri()
    logo_html = f'<img src="{logo}" alt="Cognis"/>' if logo else '<div class="mark">C</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: 11in 8.5in; margin: 0; }}
:root{{--violet:{VIOLET};--violet2:{VIOLET2};--deep:{DEEP};--ink:{INK};--soft:{SOFT};--faint:{FAINT};--line:{LINE};
--serif:"Iowan Old Style","Palatino Linotype",Georgia,serif;--mono:ui-monospace,"Cascadia Mono",Consolas,monospace;
--sans:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:11in;height:8.5in}}
body{{background:radial-gradient(1200px 600px at 85% -8%,#2a1a52 0%,transparent 55%),
 radial-gradient(1000px 600px at 0% 108%,#241a44 0%,transparent 55%),{GROUND};
 color:var(--ink);font-family:var(--sans);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.frame{{position:absolute;inset:0.38in;border:1.5px solid var(--line);
 box-shadow:inset 0 0 0 6px transparent,inset 0 0 0 7px #ffffff10}}
.edge{{position:absolute;inset:0.30in;border:3px solid var(--deep);border-image:linear-gradient(135deg,var(--violet),var(--deep)) 1}}
.wrap{{position:absolute;inset:0.7in;display:flex;flex-direction:column;align-items:center;text-align:center}}
.top{{display:flex;align-items:center;gap:14px;margin-top:4px}}
.top img{{width:52px;height:52px;filter:drop-shadow(0 0 10px #8b5cf680)}}
.top .mark{{width:52px;height:52px;border:2px solid var(--violet);border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:30px;color:#fff}}
.brand{{font-family:var(--serif);font-size:26px;letter-spacing:.14em;color:#fff}}
.eyebrow{{font-family:var(--mono);font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--violet2);margin:6px 0 0}}
h1{{font-family:var(--serif);font-weight:600;font-size:46px;letter-spacing:.02em;margin:26px 0 0}}
.lede{{color:var(--soft);font-size:15px;margin:22px 0 0}}
.name{{font-family:var(--serif);font-style:italic;font-size:58px;color:#fff;margin:6px 0 2px;text-shadow:0 0 22px #8b5cf655}}
.rule{{width:62%;height:1px;background:linear-gradient(90deg,transparent,var(--violet),transparent);margin:2px 0 0}}
.body{{color:var(--soft);font-size:16px;max-width:8in;margin:22px 0 0;line-height:1.5}}
.body b{{color:var(--ink)}}
.level{{font-family:var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--violet2);font-size:19px;margin:16px 0 0}}
.badge{{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;
 color:#fff;background:var(--deep);border:1px solid var(--violet);border-radius:999px;padding:5px 14px}}
.dot{{color:var(--faint);margin:0 6px}}
.foot{{position:absolute;left:0.9in;right:0.9in;bottom:0.5in;display:flex;justify-content:space-between;align-items:flex-end}}
.foot .l{{text-align:left;font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.06em;line-height:1.7}}
.foot .l b{{color:var(--violet2)}}
.foot .r{{text-align:center}}
.sig{{width:2.4in;border-top:1px solid var(--soft);padding-top:6px;font-family:var(--serif);font-size:14px;color:var(--ink)}}
.sig small{{display:block;font-family:var(--sans);font-size:10px;color:var(--faint);margin-top:2px}}
.seal{{position:absolute;right:1.0in;bottom:1.3in;width:120px;height:120px;border-radius:50%;
 border:3px solid var(--violet);display:flex;flex-direction:column;align-items:center;justify-content:center;
 background:radial-gradient(circle,#241a44,#160f2b);box-shadow:0 0 24px #8b5cf640}}
.seal .st{{font-size:30px;color:var(--violet2)}}
.seal small{{font-family:var(--mono);font-size:8px;letter-spacing:.14em;color:var(--soft);margin-top:2px}}
</style></head><body>
<div class="edge"></div><div class="frame"></div>
<div class="wrap">
  <div class="top">{logo_html}<span class="brand">COGNIS DIGITAL</span></div>
  <div class="eyebrow">Cognis Neural Suite &nbsp;&middot;&nbsp; Garrison Cyber-Operations Curriculum</div>
  <h1>Certificate of {kind}</h1>
  <div class="lede">This is to certify that</div>
  <div class="name">{e(trainee)}</div><div class="rule"></div>
  <div class="body">has attained the standing of <span class="level">{e(level.upper())}</span><br/>
    in the <b>{e(track)}</b> track of the Garrison cyber-operations curriculum {score_html}.</div>
  <div class="badge">CREDENTIAL &nbsp;{e(badge)}</div>
</div>
<div class="seal"><div class="st">&#9733;</div><small>MISSION&nbsp;READY</small></div>
<div class="foot">
  <div class="l">ISSUED <b>{date_str}</b><br/>CREDENTIAL ID <b>{cid}</b><br/>
    tamper-evident by ID hash &middot; verify at cognis.digital</div>
  <div class="r"><div class="sig">{e(signatory)}<small>{e(issuer)} &middot; Wyoming, USA</small></div></div>
</div>
</body></html>"""


def _browser():
    for p in _BROWSERS:
        if os.path.exists(p):
            return p
    return None


def write(trainee, track, level, badge, out_path, **kw):
    """Write a branded PDF (via headless browser) or, failing that, the HTML."""
    html_str = render_html(trainee, track, level, badge, **kw)
    base = os.path.splitext(out_path)[0]
    html_path = base + ".html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_str)
    if out_path.lower().endswith(".pdf"):
        br = _browser()
        if br:
            try:
                subprocess.run([br, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                                f"--print-to-pdf={out_path}", "file:///" + html_path.replace("\\", "/")],
                               timeout=90, creationflags=0x08000000,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                    return out_path
            except Exception:
                pass
        return html_path  # browser unavailable/failed — HTML is still branded + printable
    return html_path
