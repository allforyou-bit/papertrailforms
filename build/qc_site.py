#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qc_site.py — Paper Trail Forms deployment gate.

Same discipline as the question-bank gates on the quiz properties: the
site does not ship unless this prints ALL PASS.

Checks:
  1.  tools.js unit tests pass under node
  2.  every page has a title, a meta description in range, a canonical,
      and exactly one <h1>
  3.  titles and descriptions are unique across the site
  4.  local link integrity (every href/src resolves to a real file)
  5.  no third-party network requests except the gated AdSense loader
  6.  revenue gates are OFF in the committed config (adsense empty,
      ads.txt commented out) so nothing fires before approval
  7.  the legal trio exists and the disclaimer footer is on every page
  8.  sitemap matches the built pages exactly
  9.  20+ indexable pages (AdSense application threshold)
 10.  calculator pages actually load tools.js and declare data-tool

Exit 0 = ALL PASS. Exit 1 = failures listed.
"""
import os
import re
import subprocess
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []


def fail(msg):
    fails.append(msg)


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


html_files = sorted(
    glob.glob(os.path.join(ROOT, "*.html")) +
    glob.glob(os.path.join(ROOT, "guides", "*.html")))
pages = {rel(p): open(p, encoding="utf-8").read() for p in html_files}

# ---- 1. unit + DOM tests -------------------------------------------
def run_node(script):
    try:
        r = subprocess.run(["node", os.path.join(ROOT, "tests", script)],
                           capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        fail("node is not available — cannot run " + script)
        return "(node missing)"
    if r.returncode != 0:
        fail(script + " failed:\n" + (r.stderr or r.stdout).strip())
    out = (r.stdout or "").strip().splitlines()
    return out[-1] if out else "(no output)"


unit_line = run_node("tools.test.js")
dom_line = run_node("dom.test.js")

# ---- 2-3. head hygiene ---------------------------------------------
titles, descs = {}, {}
for name, txt in pages.items():
    t = re.search(r"<title>(.*?)</title>", txt, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', txt, re.S)
    c = re.search(r'<link rel="canonical" href="(.*?)">', txt)
    h1 = re.findall(r"<h1[^>]*>", txt)
    if not t:
        fail(f"{name}: no <title>")
    elif len(t.group(1)) > 70:
        fail(f"{name}: title is {len(t.group(1))} chars (keep under 70)")
    if not d:
        fail(f"{name}: no meta description")
    elif not (70 <= len(d.group(1)) <= 175):
        fail(f"{name}: meta description is {len(d.group(1))} chars (want 70-175)")
    if not c:
        fail(f"{name}: no canonical")
    if len(h1) != 1:
        fail(f"{name}: {len(h1)} <h1> tags (need exactly 1)")
    if t:
        titles.setdefault(t.group(1), []).append(name)
    if d:
        descs.setdefault(d.group(1), []).append(name)

for val, where in titles.items():
    if len(where) > 1:
        fail("duplicate <title> across " + ", ".join(where))
for val, where in descs.items():
    if len(where) > 1:
        fail("duplicate meta description across " + ", ".join(where))

# ---- 4. local link integrity ---------------------------------------
for name, txt in pages.items():
    base = os.path.dirname(os.path.join(ROOT, name))
    for attr, _frag in re.findall(r'(?:href|src)="([^"#]*?)(#[^"]*)?"', txt):
        if not attr or attr.startswith(("http", "data:", "mailto:", "//")):
            continue
        if attr.startswith("/"):
            p = os.path.join(ROOT, attr.lstrip("/"))
        else:
            p = os.path.normpath(os.path.join(base, attr))
        if attr.endswith("/"):
            p = os.path.join(p, "index.html")
        if not os.path.exists(p):
            fail(f"{name}: broken local link -> {attr}")

# ---- 5. no third-party requests ------------------------------------
ALLOWED_EXTERNAL = (
    "https://myadcenter.google.com",          # informational link in privacy
    "https://pagead2.googlesyndication.com",  # gated AdSense loader (config.js)
    "http://www.sitemaps.org",                # xml namespace
    "http://www.w3.org",                      # svg namespace in the favicon
)
SELF_ORIGIN = ""
_cm = re.search(r'SITE_URL\s*=\s*"(.*?)"',
                open(os.path.join(ROOT, "build", "build_site.py"),
                     encoding="utf-8").read())
if _cm:
    SELF_ORIGIN = _cm.group(1)

for name, txt in pages.items():
    # the canonical tag legitimately points at our own future origin
    body_only = re.sub(r'<link rel="canonical"[^>]*>', "", txt)
    for url in re.findall(r'(?:href|src)="(https?://[^"]+)"', body_only):
        if SELF_ORIGIN and url.startswith(SELF_ORIGIN):
            continue
        if not url.startswith(ALLOWED_EXTERNAL):
            fail(f"{name}: third-party request/link not on the allow list -> {url}")

js = open(os.path.join(ROOT, "tools.js"), encoding="utf-8").read()
for banned in ("fetch(", "XMLHttpRequest", "navigator.sendBeacon", "import("):
    if banned in js:
        fail(f"tools.js: contains {banned} — the tools must make no network calls")

# ---- 6. revenue gates off ------------------------------------------
cfg = open(os.path.join(ROOT, "config.js"), encoding="utf-8").read()
m = re.search(r'adsenseClient:\s*"(.*?)"', cfg)
if not m:
    fail("config.js: adsenseClient key missing")
elif m.group(1):
    fail("config.js: adsenseClient is set before AdSense approval — must stay empty")

ads = open(os.path.join(ROOT, "ads.txt"), encoding="utf-8").read()
live_ads = [ln for ln in ads.splitlines()
            if ln.strip() and not ln.strip().startswith("#")]
if live_ads and not (m and m.group(1)):
    fail("ads.txt: publisher line is live while adsenseClient is empty")

# ---- 7. legal + disclaimer -----------------------------------------
for needed in ("about.html", "privacy.html", "terms.html", "404.html"):
    if needed not in pages:
        fail(f"missing required page: {needed}")
for name, txt in pages.items():
    if "legal, accounting, or tax advice" not in txt:
        fail(f"{name}: footer disclaimer missing")
    if "Paper Trail" not in txt:
        fail(f"{name}: brand missing")

# ---- 8. sitemap ----------------------------------------------------
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
origin = locs[0].rsplit("/", 1)[0] if locs else ""
listed = set()
for loc in locs:
    path = loc[len(origin):].lstrip("/") or "index.html"
    listed.add(path)
    if path not in pages:
        fail(f"sitemap lists a page that does not exist: {path}")
for name in pages:
    if name == "404.html":
        continue
    if name not in listed:
        fail(f"page not in sitemap: {name}")

# ---- 9. page count -------------------------------------------------
indexable = len(pages) - 1  # 404 is not indexable
if indexable < 20:
    fail(f"only {indexable} indexable pages (AdSense wants 20+)")

# ---- 10. tool wiring -----------------------------------------------
for name, txt in pages.items():
    has_tool = 'data-tool="' in txt
    loads = 'tools.js' in txt
    if has_tool and not loads:
        fail(f"{name}: declares data-tool but does not load tools.js")
    if loads and not has_tool:
        fail(f"{name}: loads tools.js but declares no data-tool")
    if has_tool and 'id="tool-form"' not in txt:
        fail(f"{name}: declares data-tool but has no #tool-form")

# ---- report --------------------------------------------------------
print(f"pages: {len(pages)} ({indexable} indexable) · sitemap URLs: {len(locs)}")
print(f"unit tests: {unit_line}")
print(f"dom  tests: {dom_line}")
if fails:
    print(f"\n=== {len(fails)} FAILURE(S) ===")
    for f_ in fails:
        print("FAIL:", f_)
    sys.exit(1)
print("\nALL PASS")
