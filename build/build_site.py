#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Paper Trail Forms — static site builder.

Every page on the site is generated from here, so the shell (head, nav,
footer, legal line) can never drift between pages. Run it, then run
qc_site.py; deployment is blocked unless QC passes.

    python build/build_site.py
"""
import os
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from spec_tools import DOC_TOOLS, CALC_TOOLS, doc_form, CURRENCY_OPTIONS, TERM_OPTIONS  # noqa: E402
from spec_guides import GUIDES  # noqa: E402

# The domain has NOT been bought. It is the canonical target so that the
# day it is approved, nothing but config.js and this line need to change.
SITE_URL = "https://papertrailforms.com"
BRAND = "Paper Trail Forms"
TODAY = "2026-07-30"

FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128441;</text></svg>")


def nav(depth):
    """depth 0 = site root, 1 = /guides/"""
    up = "../" * depth
    return """<header class="site-header"><nav class="nav container">
  <a class="brand" href="{u}index.html">&#128441; Paper Trail <span style="opacity:.75">Forms</span></a>
  <div class="nav-links">
    <a href="{u}invoice-generator.html">Invoice</a>
    <a href="{u}receipt-maker.html">Receipt</a>
    <a href="{u}estimate-generator.html">Estimate</a>
    <a href="{u}index.html#calculators">Calculators</a>
    <a href="{u}guides/index.html">Guides</a>
    <a class="btn-cta" data-shop-link href="#">Printable Forms</a>
  </div>
</nav></header>""".format(u=up)


def footer(depth):
    up = "../" * depth
    return """<footer class="site-footer"><div class="container">
  <div class="foot-links">
    <a href="{u}index.html">Home</a>
    <a href="{u}invoice-generator.html">Invoice Generator</a>
    <a href="{u}receipt-maker.html">Receipt Maker</a>
    <a href="{u}estimate-generator.html">Estimate Generator</a>
    <a href="{u}guides/index.html">Guides</a>
    <a href="{u}about.html">About</a>
    <a href="{u}privacy.html">Privacy</a>
    <a href="{u}terms.html">Terms</a>
  </div>
  <p class="legal">{brand} provides free document tools and general business
  information. It is not a law firm, an accounting firm, or a tax adviser, and
  nothing on this site is legal, accounting, or tax advice &mdash; requirements
  for invoices, receipts, late fees, and record retention vary by country and by
  jurisdiction, so verify what applies to you before relying on it. The tools run
  entirely in your browser: what you type is never transmitted to us and is
  stored only in your own browser. &copy; 2026 {brand}</p>
</div></footer>""".format(u=up, brand=BRAND)


def page(slug, title, description, body, depth=0, tool=None, canonical=None):
    up = "../" * depth
    body_attr = ' data-tool="%s"' % tool if tool else ""
    canon = canonical or (SITE_URL + "/" + slug)
    tools_js = ('<script src="%stools.js" defer></script>' % up) if tool else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{u}styles.css">
<script src="{u}config.js" defer></script>
{tools_js}
</head>
<body{body_attr}>
{nav}
{body}
{footer}
</body>
</html>
""".format(title=title, description=description, canon=canon, favicon=FAVICON,
           u=up, tools_js=tools_js, body_attr=body_attr,
           nav=nav(depth), body=body, footer=footer(depth))


def faq_block(items):
    if not items:
        return ""
    out = ['<h2>Frequently asked questions</h2>']
    for q, a in items:
        out.append('<details class="faq"><summary>%s</summary><p>%s</p></details>'
                   % (q, a))
    return "\n".join(out)


# ---------------------------------------------------------------- tools

def render_doc_tool(t):
    body = """<main class="container">
  <p class="breadcrumb"><a href="./index.html">Home</a> &rsaquo; {h1}</p>
  <div class="tool-layout">
    <form class="panel" id="tool-form" onsubmit="return false;">
      <h2>Fill this in</h2>
      <p class="hint">Everything updates as you type. Nothing leaves your browser.</p>
      {form}
      <div class="tool-actions">
        <button type="button" class="btn btn-primary" id="print-doc">Print / Save as PDF</button>
        <button type="button" class="btn-mini" id="reset-doc">Start over</button>
      </div>
    </form>
    <div>
      <div class="doc" id="doc"></div>
      <p class="hint no-print" style="margin-top:10px">Tip: choose &ldquo;Save as PDF&rdquo;
      as the destination in the print dialog. Only the document prints &mdash; not this page.</p>
    </div>
  </div>

  <article class="prose">
  <h1>{h1}</h1>
  <p>{lede}</p>
  <h2>How it works</h2>
  <ol class="steps">
  <li>Fill in your details and the client's. They are remembered in this browser for next time.</li>
  <li>Add a line for each item or task, with a quantity and a rate.</li>
  <li>Set tax, any discount, and the terms. The totals recalculate as you type.</li>
  <li>Press <strong>Print / Save as PDF</strong> and choose Save as PDF.</li>
  </ol>
  <div class="notice"><strong>Your data stays yours.</strong> This tool makes no
  network requests. What you type is held in your browser's local storage on your
  own machine, so closing the tab does not lose it &mdash; and clearing your browser
  data removes it entirely.</div>
  {faq}
  <h2>Keep reading</h2>
  <p>{related}</p>
  </article>
</main>"""
    related = ('<a href="./guides/index.html">All guides</a> &middot; '
               '<a href="./guides/what-to-include-on-an-invoice.html">What to include on an invoice</a> &middot; '
               '<a href="./guides/invoice-vs-receipt-vs-estimate.html">Invoice vs receipt vs estimate</a> &middot; '
               '<a href="./guides/net-30-payment-terms-explained.html">Net 30 explained</a>')
    return page(t["slug"], t["title"], t["description"],
                body.format(h1=t["h1"], form=doc_form(t["tool"]),
                            lede=t["lede"], faq=faq_block(t["faq"]),
                            related=related),
                depth=0, tool=t["tool"])


def calc_fields(t):
    """Field tuples are (kind, id, label, extra, extra2).

    kind "select"   : extra = [(value, label)], extra2 = note
    kind "number"   : extra = default value, extra2 = space-separated list of
                      the "mode" values this field is visible for (optional)
    kind "currency" / "terms" / "date" : no extras
    """
    out = []
    for f in t["fields"]:
        kind, fid, label = f[0], f[1], f[2]
        extra = f[3] if len(f) > 3 else None
        extra2 = f[4] if len(f) > 4 else ""
        if kind == "select":
            opts = "".join('<option value="%s">%s</option>' % (v, lbl)
                           for v, lbl in extra)
            n = '<div class="note">%s</div>' % extra2 if extra2 else ""
            out.append('<div class="field"><label for="%s">%s</label>'
                       '<select id="%s">%s</select>%s</div>'
                       % (fid, label, fid, opts, n))
        elif kind == "currency":
            opts = "".join('<option value="%s">%s</option>' % (v, lbl)
                           for v, lbl in CURRENCY_OPTIONS)
            out.append('<div class="field"><label for="%s">%s</label>'
                       '<select id="%s">%s</select></div>' % (fid, label, fid, opts))
        elif kind == "terms":
            opts = "".join('<option value="%s"%s>%s</option>'
                           % (v, ' selected' if v == "net30" else "", lbl)
                           for v, lbl in TERM_OPTIONS)
            out.append('<div class="field"><label for="%s">%s</label>'
                       '<select id="%s">%s</select></div>' % (fid, label, fid, opts))
        elif kind == "date":
            out.append('<div class="field"><label for="%s">%s</label>'
                       '<input type="date" id="%s"></div>' % (fid, label, fid))
        else:
            mode = ' data-mode-field="%s"' % extra2 if extra2 else ""
            value = extra or ""
            out.append('<div class="field"%s><label for="%s">%s</label>'
                       '<input type="number" step="any" id="%s" value="%s"></div>'
                       % (mode, fid, label, fid, value))
    return "\n".join(out)


def render_calc_tool(t):
    body = """<main class="container">
  <p class="breadcrumb"><a href="./index.html">Home</a> &rsaquo; {h1}</p>
  <div class="tool-layout">
    <form class="panel" id="tool-form" onsubmit="return false;">
      <h2>Your numbers</h2>
      <p class="hint">Results update as you type. Nothing leaves your browser.</p>
      {fields}
    </form>
    <div class="readout">
      <div class="big-label" id="out-label">{big_label}</div>
      <div class="big" id="out-big">&mdash;</div>
      <div class="rows" id="out-rows"></div>
      <p class="explain">Figures are rounded to two decimals. Use them as a working
      estimate and check anything that has to be exact against your own records.</p>
    </div>
  </div>

  <article class="prose">
  <h1>{h1}</h1>
  <p>{lede}</p>
  {faq}
  <h2>Keep reading</h2>
  <p>{related}</p>
  </article>
</main>"""
    related = ('<a href="./guides/index.html">All guides</a> &middot; '
               '<a href="./invoice-generator.html">Free invoice generator</a> &middot; '
               '<a href="./guides/how-to-charge-late-fees.html">How to charge late fees</a> &middot; '
               '<a href="./guides/how-to-set-your-freelance-rate.html">Setting your rate</a>')
    return page(t["slug"], t["title"], t["description"],
                body.format(h1=t["h1"], fields=calc_fields(t), lede=t["lede"],
                            big_label=t["big_label"], faq=faq_block(t["faq"]),
                            related=related),
                depth=0, tool=t["tool"])


# --------------------------------------------------------------- guides

def render_guide(g):
    body = """<main class="container narrow">
  <p class="breadcrumb"><a href="../index.html">Home</a> &rsaquo;
  <a href="./index.html">Guides</a> &rsaquo; {meta}</p>
  <article class="prose">
  <h1>{h1}</h1>
  <p class="updated">Updated July 2026 &middot; {brand}</p>
  {body}
  {faq}
  </article>
</main>"""
    return page("guides/" + g["slug"], g["title"], g["description"],
                body.format(meta=g["meta"], h1=g["h1"], brand=BRAND,
                            body=g["body"], faq=faq_block(g["faq"])),
                depth=1)


def render_guides_index():
    cards = "".join(
        '<a class="card-link" href="./%s"><div class="card">'
        '<div class="meta">%s</div><h3>%s</h3><p>%s</p></div></a>'
        % (g["slug"], g["meta"], g["h1"], g["description"]) for g in GUIDES)
    body = """<main class="container">
  <p class="breadcrumb"><a href="../index.html">Home</a> &rsaquo; Guides</p>
  <article class="prose">
  <h1>Small Business Paperwork Guides</h1>
  <p>Plain-language explainers on invoicing, getting paid, and pricing &mdash; written
  for people who run the business and do the paperwork on the same day. Every guide
  links to the tool that does the arithmetic.</p>
  </article>
  <div class="grid grid-2" style="margin-bottom:40px">{cards}</div>
</main>"""
    return page("guides/index.html", "Small Business Invoicing &amp; Pricing Guides",
                "Plain-language guides on invoicing, payment terms, late fees, "
                "pricing, and record keeping for freelancers and small businesses.",
                body.format(cards=cards), depth=1)


# ----------------------------------------------------------------- home

def render_home():
    doc_cards = "".join(
        '<a class="card-link" href="./%s"><div class="card"><div class="meta">Document</div>'
        '<h3>%s</h3><p>%s</p></div></a>'
        % (t["slug"], t["h1"], t["lede"].split(". ")[0] + ".") for t in DOC_TOOLS)
    calc_cards = "".join(
        '<a class="card-link" href="./%s"><div class="card"><div class="meta">Calculator</div>'
        '<h3>%s</h3><p>%s</p></div></a>'
        % (t["slug"], t["h1"], t["lede"].split(". ")[0] + ".") for t in CALC_TOOLS)
    guide_cards = "".join(
        '<a class="card-link" href="./guides/%s"><div class="card"><div class="meta">%s</div>'
        '<h3>%s</h3><p>%s</p></div></a>'
        % (g["slug"], g["meta"], g["h1"], g["description"]) for g in GUIDES[:4])

    body = """<section class="hero"><div class="container">
  <h1>Free small business paperwork, done in your browser</h1>
  <p class="sub">Invoices, receipts, estimates, and the calculators that sit behind
  them. No signup, no watermark, no upload &mdash; everything runs on your own
  machine and prints straight to PDF.</p>
  <div class="hero-badges">
    <span class="badge">&#10004; No account needed</span>
    <span class="badge">&#10004; Nothing uploaded</span>
    <span class="badge">&#10004; Prints clean to PDF</span>
  </div>
  <a class="btn btn-primary" href="./invoice-generator.html">Make an invoice</a>
  <a class="btn btn-ghost" href="./estimate-generator.html">Make an estimate</a>
</div></section>

<section class="block"><div class="container">
  <h2 class="section-title">Make a document</h2>
  <p class="section-sub">Fill the form, watch it build, print it. Your details are
  remembered in this browser so the next one takes seconds.</p>
  <div class="grid grid-3">{doc_cards}</div>
</div></section>

<section class="block alt" id="calculators"><div class="container">
  <h2 class="section-title">Run the numbers</h2>
  <p class="section-sub">The arithmetic small businesses get wrong most often &mdash;
  late fees, reverse sales tax, hourly rates, margin against markup, and due dates.</p>
  <div class="grid grid-3">{calc_cards}</div>
</div></section>

<section class="block"><div class="container">
  <h2 class="section-title">Guides</h2>
  <p class="section-sub">What has to be on an invoice, what net 30 really means, and
  how to price work without losing money on it.</p>
  <div class="grid grid-2">{guide_cards}</div>
  <p style="margin-top:18px"><a href="./guides/index.html">See all guides &rarr;</a></p>
</div></section>

<section class="block alt" data-requires-shop><div class="container">
  <div class="cta-box">
    <h3>Prefer a printable pack you can fill in and reuse?</h3>
    <p>Our fillable PDF form packs cover invoices, estimates, receipts, mileage,
    and job sheets &mdash; typed in, saved, and printed as often as you need.</p>
    <a class="btn btn-primary" data-shop-link href="#">Browse the printable forms</a>
  </div>
</div></section>

<section class="block"><div class="container narrow">
  <article class="prose">
  <h2>Why these tools are free</h2>
  <p>They cost us nothing to run. There is no server doing the work and no database
  holding your data &mdash; the whole thing is a page in your browser, which is also
  why there is no account to create and no limit on how many documents you make.</p>
  <p>We also sell printable, fillable PDF form packs for people who would rather
  type into a saved file than open a website. If the free tools do the job, use
  them and ignore the shop; that is the intended outcome.</p>
  <h2>What these tools do not do</h2>
  <p>They do not file your taxes, track your books, or tell you what your local
  rules require. Invoice content requirements, late-fee limits, and record
  retention periods all vary by country and jurisdiction &mdash; check yours. Nothing
  here is legal, accounting, or tax advice.</p>
  </article>
</div></section>"""
    return page("index.html",
                "Free Invoice Generator &amp; Small Business Calculators",
                "Free browser-based invoice generator, receipt maker, estimate "
                "generator, late fee calculator, sales tax calculator, and hourly "
                "rate calculator. No signup, nothing uploaded.",
                body.format(doc_cards=doc_cards, calc_cards=calc_cards,
                            guide_cards=guide_cards),
                depth=0, canonical=SITE_URL + "/")


# ---------------------------------------------------------------- legal

LEGAL = {
    "about.html": ("About " + BRAND, "About Paper Trail Forms: who runs it, how "
                   "the tools work, and how to report a problem.", """
  <h1>About {brand}</h1>
  <p>{brand} makes free paperwork tools for people who run small businesses and
  do their own admin &mdash; freelancers, trades, single-van operations, and the
  people who keep them organised.</p>
  <h2>How the tools work</h2>
  <p>Every tool on this site runs entirely inside your browser. There is no
  account, no server processing your entries, and no upload. What you type is
  held in your browser's local storage, on your own device, so the form still has
  your details next time. Clearing your browser data clears it.</p>
  <p>That design is also why the tools are free: they cost nothing to operate, so
  there is nothing to recover from you.</p>
  <h2>How this site makes money</h2>
  <p>Two ways, both optional for you. We sell printable fillable PDF form packs
  for people who prefer a saved file to a web page. And we may display advertising
  on these pages. Neither changes what the free tools do.</p>
  <h2>Accuracy and corrections</h2>
  <p>The calculators are unit tested, and the guides are written from general
  small-business practice rather than from any single jurisdiction's rules. If you
  find something wrong &mdash; a calculation that does not match your own working, a
  guide that is out of date, a broken page &mdash; tell us and we will fix it.
  Corrections are welcome and get priority over new features.</p>
  <h2>What we are not</h2>
  <p>We are not a law firm, an accounting firm, or a tax adviser, and nothing on
  this site is advice of any of those kinds. Requirements for invoices, receipts,
  late fees, and record retention vary by country and jurisdiction. Verify what
  applies to you.</p>
"""),
    "privacy.html": ("Privacy Policy — " + BRAND,
                     "How Paper Trail Forms handles data: nothing you type is "
                     "transmitted, what local storage holds, and cookies.", """
  <h1>Privacy Policy</h1>
  <p class="updated">Last updated 30 July 2026</p>
  <h2>The short version</h2>
  <p>Nothing you type into the tools on this site is sent to us. There is no
  account, no login, and no server-side copy of your invoices, receipts,
  estimates, or calculations.</p>
  <h2>What stays in your browser</h2>
  <p>The document tools save your entries to <strong>localStorage</strong>, a
  storage area belonging to your own browser on your own device, so that your
  business details are still there when you return. We cannot read it. You can
  remove it at any time by clearing site data in your browser, or by using the
  &ldquo;Start over&rdquo; button on a tool page.</p>
  <h2>Hosting logs</h2>
  <p>This site is served as static files by our hosting provider. Like any web
  host, it records standard request information such as IP address, user agent,
  and the page requested, for security and reliability. We do not combine that
  with anything you type into the tools, because we never receive what you type.</p>
  <h2>Advertising</h2>
  <p>We may display advertising on this site through Google AdSense. When
  advertising is active, Google and its partners may use cookies or similar
  technologies to serve and measure ads, including personalised ads where you
  have consented and where local rules allow. You can review and change Google's
  ad settings at <a href="https://myadcenter.google.com" target="_blank"
  rel="noopener">myadcenter.google.com</a>. Ad scripts load only when advertising
  is enabled on the site; when it is not, no advertising code is loaded at all.</p>
  <h2>Email</h2>
  <p>If we offer an email list on this site, joining it is voluntary, the address
  is processed by our email provider for that purpose only, and every message
  includes an unsubscribe link. We do not sell or rent addresses.</p>
  <h2>Children</h2>
  <p>This is a business tools site and is not directed at children.</p>
  <h2>Your rights and contact</h2>
  <p>Because we do not hold your documents, most data requests have nothing to
  retrieve. For anything relating to email or hosting records, or to ask a
  question about this policy, contact us through the details on our
  <a href="./about.html">About page</a>.</p>
"""),
    "terms.html": ("Terms of Use — " + BRAND,
                   "Terms of use for Paper Trail Forms: no warranty, not "
                   "professional advice, acceptable use, and your content.", """
  <h1>Terms of Use</h1>
  <p class="updated">Last updated 30 July 2026</p>
  <h2>Acceptance</h2>
  <p>By using this site you agree to these terms. If you do not agree, please do
  not use it.</p>
  <h2>Not professional advice</h2>
  <p>{brand} provides general information and calculation tools. It is not a law
  firm, an accounting firm, or a tax adviser, and nothing on this site constitutes
  legal, accounting, or tax advice. Requirements for invoices, receipts, late
  fees, tax rates, and record retention vary by country and jurisdiction and
  change over time. You are responsible for verifying what applies to you, and
  for the accuracy of any document you produce with these tools.</p>
  <h2>No warranty</h2>
  <p>The tools and content are provided &ldquo;as is&rdquo; without warranties of
  any kind, express or implied, including fitness for a particular purpose. We
  work to keep the calculators correct and test them, but we do not warrant that
  the site will be error-free or uninterrupted.</p>
  <h2>Limitation of liability</h2>
  <p>To the fullest extent permitted by law, we are not liable for any indirect,
  incidental, or consequential loss, or for lost profits, revenue, or data,
  arising from use of this site or documents produced with it.</p>
  <h2>Your content</h2>
  <p>Documents you create with these tools are yours. We do not receive them, do
  not store them, and claim no rights in them.</p>
  <h2>Acceptable use</h2>
  <p>Do not use this site to create fraudulent, misleading, or unlawful documents,
  to impersonate another business, or to attempt to disrupt the site or its users.</p>
  <h2>Intellectual property</h2>
  <p>The site design, text, and code are ours. You may use the tools and their
  output freely for your own business purposes; you may not republish the site's
  content or code as your own.</p>
  <h2>Changes</h2>
  <p>We may update these terms. The date above shows the current version.</p>
"""),
}


def render_legal():
    out = {}
    for slug, (title, desc, body) in LEGAL.items():
        out[slug] = page(slug, title, desc,
                         '<main class="container narrow"><article class="prose">'
                         + body.format(brand=BRAND) + "</article></main>", depth=0)
    return out


def render_404():
    body = """<main class="container narrow"><article class="prose">
  <h1>Page not found</h1>
  <p>That page does not exist &mdash; it may have been renamed or the link may be
  incomplete. Here is everything on the site:</p>
  <ul>
    <li><a href="/index.html">Home</a></li>
    <li><a href="/invoice-generator.html">Free invoice generator</a></li>
    <li><a href="/receipt-maker.html">Free receipt maker</a></li>
    <li><a href="/estimate-generator.html">Free estimate generator</a></li>
    <li><a href="/late-fee-calculator.html">Late payment fee calculator</a></li>
    <li><a href="/sales-tax-calculator.html">Sales tax calculator</a></li>
    <li><a href="/hourly-rate-calculator.html">Freelance hourly rate calculator</a></li>
    <li><a href="/margin-markup-calculator.html">Margin and markup calculator</a></li>
    <li><a href="/payment-terms-calculator.html">Invoice due date calculator</a></li>
    <li><a href="/guides/index.html">Guides</a></li>
  </ul>
</article></main>"""
    return page("404.html", "Page not found — " + BRAND,
                "That page does not exist on Paper Trail Forms. Here is the "
                "full list of free invoice, receipt, estimate, and calculator "
                "tools on the site.",
                body, depth=0)


# ------------------------------------------------------------- sitemap

def render_sitemap(slugs):
    rows = []
    for slug, prio in slugs:
        loc = SITE_URL + "/" + ("" if slug == "index.html" else slug)
        rows.append('  <url><loc>%s</loc><lastmod>%s</lastmod>'
                    '<priority>%s</priority></url>' % (loc, TODAY, prio))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def main():
    written = []
    slugs = [("index.html", "1.0")]

    written.append(write("index.html", render_home()))

    for t in DOC_TOOLS:
        written.append(write(t["slug"], render_doc_tool(t)))
        slugs.append((t["slug"], "0.9"))
    for t in CALC_TOOLS:
        written.append(write(t["slug"], render_calc_tool(t)))
        slugs.append((t["slug"], "0.9"))

    written.append(write("guides/index.html", render_guides_index()))
    slugs.append(("guides/index.html", "0.7"))
    for g in GUIDES:
        written.append(write("guides/" + g["slug"], render_guide(g)))
        slugs.append(("guides/" + g["slug"], "0.7"))

    for slug, html in render_legal().items():
        written.append(write(slug, html))
        slugs.append((slug, "0.3"))

    written.append(write("404.html", render_404()))
    written.append(write("sitemap.xml", render_sitemap(slugs)))
    written.append(write("robots.txt",
                         "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
                         % SITE_URL))
    written.append(write("ads.txt",
                         "# Uncomment the line below once AdSense approves this "
                         "domain (see docs/OPERATIONS.md).\n"
                         "# google.com, pub-6709396576574623, DIRECT, "
                         "f08c47fec0942fa0\n"))
    written.append(write(".nojekyll", ""))

    print("built %d files, %d indexed URLs" % (len(written), len(slugs)))
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
