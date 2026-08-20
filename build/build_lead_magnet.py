#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_lead_magnet.py — the free printable forms kit offered on
free-paperwork-kit.html.

    python build/build_lead_magnet.py

WHY IT IS BUILT THIS WAY
------------------------
The W4 content queue said to reuse the A-plan fillable PDFs as the lead
magnet. Handed over unchanged, those three files ARE the shop's paid
products: the Etsy listing pack sells "Fillable Invoice Template",
"Fillable Estimate Template", "Fillable Receipt Template 3 Per Page"
individually and bundles the same three as the "Small Business Forms
Starter Kit". Giving them away on a site that cross-links to that shop
would have retired four listings without anyone deciding to.

So the free kit reuses the same layout code and gives away a different
thing. Every AcroForm field is suppressed, which turns the identical
pages into print-and-write forms: you print them and fill them in by
hand. What the paid listings sell -- typing into the file, saving it,
reusing it -- stays behind the till, and it is exactly what their titles
advertise. Nothing new was drawn; this is the freemium line drawn
through work that already existed.

The layout primitives live in the private WEB_FACTORY tree, so this
script imports that module by path rather than vendoring a copy that
would drift. If the source is missing, it says so instead of silently
producing something else.

The URL is deliberately absent from the PDF footer. papertrailforms.com
is not bought yet, and a kit in circulation carrying a dead domain is
worse than one carrying only the brand name. Add the URL here on
domain day.
"""
import importlib.util
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SOURCE = os.path.join(os.path.expanduser("~"), "Desktop", "WEB_FACTORY",
                      "tools", "build_prototypes_smb.py")
OUT = os.path.join(ROOT, "downloads", "paper-trail-printable-forms-kit.pdf")

# doc_header() draws these under the big title. The originals sell the
# fillable behaviour this edition does not have.
SUBTITLES = {
    "INVOICE": "Printable invoice form - print it and fill it in by hand.",
    "ESTIMATE": "Printable quotation form - valid until the date shown.",
}
BRAND_LINE = "Paper Trail Forms - free printable small business forms"


def load_source():
    if not os.path.exists(SOURCE):
        sys.exit("layout source not found: %s\n"
                 "It lives in the private WEB_FACTORY tree; restore that "
                 "folder (repo allforyou-bit/web-factory) and re-run." % SOURCE)
    spec = importlib.util.spec_from_file_location("smb_forms", SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class PrintForm(object):
    """Stands in for canvas.acroForm so no interactive fields are emitted.

    textfield() vanishes entirely -- the label and the rule under it are
    drawn separately, so the blank line to write on survives. checkbox()
    draws the box it would otherwise have made interactive, because a
    receipt with no payment-method boxes is a worse form, not a simpler one.
    """

    def __init__(self, canv):
        self.canv = canv

    def textfield(self, **kw):
        return None

    def checkbox(self, **kw):
        x, y = kw["x"], kw["y"]
        size = kw.get("size", 10)
        self.canv.saveState()
        self.canv.setStrokeColor(kw.get("borderColor"))
        self.canv.setLineWidth(kw.get("borderWidth", 1))
        self.canv.rect(x, y, size, size, fill=0, stroke=1)
        self.canv.restoreState()
        return None


def patch(mod, outdir):
    """Suppress form fields, retitle, and redirect output to `outdir`."""
    import reportlab.rl_config
    reportlab.rl_config.invariant = 1  # stable bytes across rebuilds

    base_canvas = mod.canvas.Canvas

    class PrintCanvas(base_canvas):
        @property
        def acroForm(self):
            return PrintForm(self)

    class CanvasModule(object):
        Canvas = PrintCanvas

    mod.canvas = CanvasModule
    mod.field = lambda *a, **k: None

    orig_header = mod.doc_header

    def doc_header(c, title, subtitle, meta):
        return orig_header(c, title, SUBTITLES.get(title, subtitle), meta)

    mod.doc_header = doc_header

    orig_footer = mod.footer

    def footer(c, text):
        return orig_footer(c, text + "   -   " + BRAND_LINE)

    mod.footer = footer
    mod.OUT = outdir


def main():
    from pypdf import PdfWriter

    mod = load_source()
    tmp = tempfile.mkdtemp(prefix="ptf-kit-")
    patch(mod, tmp)

    parts = [mod.build_invoice(), mod.build_estimate(), mod.build_receipt()]

    writer = PdfWriter()
    for p in parts:
        writer.append(p)
    writer.add_metadata({
        "/Title": "Printable Small Business Forms Kit",
        "/Author": "Paper Trail Forms",
        "/Subject": "Printable invoice, estimate, and receipt forms",
    })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    buf = io.BytesIO()
    writer.write(buf)
    with open(OUT, "wb") as fh:
        fh.write(buf.getvalue())

    pages = len(writer.pages)
    print("OK %s" % os.path.relpath(OUT, ROOT).replace("\\", "/"))
    print("   %d pages, %s bytes" % (pages, format(os.path.getsize(OUT), ",")))
    if pages != 3:
        sys.exit("expected 3 pages (invoice, estimate, receipt 3-up)")


if __name__ == "__main__":
    main()
