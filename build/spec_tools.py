# -*- coding: utf-8 -*-
"""Tool page definitions for Paper Trail Forms.

Each entry produces one page: a form panel on the left, a live result
on the right. The document tools (invoice / receipt / estimate) share a
generated form; the calculators declare their own fields.
"""

CURRENCY_OPTIONS = [
    ("USD", "USD — US dollar"), ("CAD", "CAD — Canadian dollar"),
    ("EUR", "EUR — Euro"), ("GBP", "GBP — British pound"),
    ("AUD", "AUD — Australian dollar"), ("NZD", "NZD — NZ dollar"),
    ("INR", "INR — Indian rupee"), ("ZAR", "ZAR — South African rand"),
]

TERM_OPTIONS = [
    ("due", "Due on receipt"), ("net7", "Net 7"), ("net14", "Net 14"),
    ("net15", "Net 15"), ("net30", "Net 30"), ("net45", "Net 45"),
    ("net60", "Net 60"), ("net90", "Net 90"),
    ("eom", "End of month"), ("eom15", "15th of following month"),
]


def _select(fid, label, options, note=""):
    opts = "".join(
        '<option value="%s">%s</option>' % (v, t) for v, t in options)
    n = '<div class="note">%s</div>' % note if note else ""
    return ('<div class="field"><label for="%s">%s</label>'
            '<select id="%s">%s</select>%s</div>' % (fid, label, fid, opts, n))


def _input(fid, label, kind="text", placeholder="", note="", step=None,
           value=""):
    extra = ' step="%s"' % step if step else ""
    v = ' value="%s"' % value if value else ""
    n = '<div class="note">%s</div>' % note if note else ""
    return ('<div class="field"><label for="%s">%s</label>'
            '<input type="%s" id="%s" placeholder="%s"%s%s>%s</div>'
            % (fid, label, kind, fid, placeholder, extra, v, n))


def _textarea(fid, label, placeholder="", note=""):
    n = '<div class="note">%s</div>' % note if note else ""
    return ('<div class="field"><label for="%s">%s</label>'
            '<textarea id="%s" placeholder="%s"></textarea>%s</div>'
            % (fid, label, fid, placeholder, n))


JOB_TYPE_OPTIONS = [
    ("service", "Service call"), ("repair", "Repair"),
    ("install", "Installation"), ("maintenance", "Scheduled maintenance"),
    ("inspection", "Inspection / survey"), ("callback", "Callback / warranty"),
]


def job_sheet_form():
    """Form for the job sheet / work order generator.

    A work order is not an invoice: it records what was scheduled, who
    attended, what was found, and what was used. Labour and parts are
    kept as separate line-item tables because trades price them
    differently and clients query them separately.
    """
    return "\n".join([
        _input("from", "Your business name", placeholder="Halcyon Mechanical"),
        _textarea("fromDetails", "Your address and contact",
                  "12 Bishop Lane&#10;Halifax NS B3H 1A1&#10;"
                  "902-555-0143"),
        _input("to", "Customer name", placeholder="Brightline Cleaning Co."),
        _textarea("toDetails", "Site address",
                  "88 Water Street&#10;Dartmouth NS B2Y 4S1"),
        _input("contact", "Site contact and phone",
               placeholder="Dana Yeo · 902-555-0199"),
        '<div class="row2">'
        + _input("number", "Job number", placeholder="JOB-0001")
        + _input("date", "Scheduled date", kind="date") + "</div>",
        '<div class="row2">'
        + _input("window", "Arrival window", placeholder="08:00 - 10:00")
        + _input("technician", "Assigned to", placeholder="R. Okafor")
        + "</div>",
        _select("jobType", "Job type", JOB_TYPE_OPTIONS),
        _textarea("requested", "Work requested",
                  "No hot water on the second floor since Tuesday."),
        _select("currency", "Currency", CURRENCY_OPTIONS),
        '<div class="field"><label>Labour</label>'
        '<div class="line-items" id="labour"></div>'
        '<button type="button" class="btn-mini" id="add-labour">'
        '+ Add labour line</button>'
        '<div class="note">Quantity column is hours.</div></div>',
        '<div class="field"><label>Parts and materials</label>'
        '<div class="line-items" id="parts"></div>'
        '<button type="button" class="btn-mini" id="add-part">'
        '+ Add parts line</button></div>',
        _input("callOut", "Call-out or trip fee", kind="number", step="any",
               placeholder="0"),
        '<div class="row2">'
        + _input("taxLabel", "Tax label", placeholder="Sales tax / VAT / GST")
        + _input("taxPct", "Tax %", kind="number", step="any",
                 placeholder="0") + "</div>",
        '<div class="row2">'
        + _select("discountType", "Discount type",
                  [("amount", "Fixed amount"), ("percent", "Percentage")])
        + _input("discountValue", "Discount value", kind="number", step="any",
                 placeholder="0") + "</div>",
        _textarea("performed", "Work performed and findings",
                  "Replaced thermostat, flushed tank, tested to 60C."),
        _textarea("notes", "Notes / terms",
                  "Parts carry a 12-month warranty. Signature confirms the "
                  "work above was completed on site."),
    ])


def doc_form(kind):
    """The shared form for invoice / receipt / estimate / job sheet."""
    if kind == "job-sheet":
        return job_sheet_form()
    is_invoice = kind == "invoice"
    is_receipt = kind == "receipt"
    noun = {"invoice": "Invoice", "receipt": "Receipt",
            "estimate": "Estimate"}[kind]
    date_label = {"invoice": "Invoice date", "receipt": "Date paid",
                  "estimate": "Estimate date"}[kind]

    parts = [
        _input("from", "Your business name", placeholder="Rivera Studio"),
        _textarea("fromDetails", "Your address and contact",
                  "12 Bishop Lane&#10;Halifax NS B3H 1A1&#10;"
                  "hello@riverastudio.ca"),
        _input("to", "Client name", placeholder="Brightline Cleaning Co."),
        _textarea("toDetails", "Client address",
                  "88 Water Street&#10;Dartmouth NS B2Y 4S1"),
        '<div class="row2">'
        + _input("number", noun + " number", placeholder="INV-0001")
        + _input("date", date_label, kind="date") + "</div>",
    ]
    if is_invoice:
        parts.append(_select("terms", "Payment terms", TERM_OPTIONS,
                             "The due date is worked out for you."))
    elif kind == "estimate":
        parts.append(_select("terms", "Valid for", TERM_OPTIONS,
                             "How long the client has to accept."))
    else:
        parts.append(_input("method", "Payment method",
                            placeholder="Card / e-transfer / cash"))

    parts.append(_select("currency", "Currency", CURRENCY_OPTIONS))
    parts.append(
        '<div class="field"><label>Line items</label>'
        '<div class="line-items" id="items"></div>'
        '<button type="button" class="btn-mini" id="add-item">'
        '+ Add line</button></div>')
    parts.append(
        '<div class="row2">'
        + _input("taxLabel", "Tax label", placeholder="Sales tax / VAT / GST")
        + _input("taxPct", "Tax %", kind="number", step="any",
                 placeholder="0") + "</div>")
    parts.append(
        '<div class="row2">'
        + _select("discountType", "Discount type",
                  [("amount", "Fixed amount"), ("percent", "Percentage")])
        + _input("discountValue", "Discount value", kind="number", step="any",
                 placeholder="0") + "</div>")
    parts.append(_input("shipping", "Shipping or delivery", kind="number",
                        step="any", placeholder="0"))
    if not is_receipt:
        parts.append(_textarea(
            "payment", "How to pay",
            "e-transfer to hello@riverastudio.ca&#10;"
            "or cheque payable to Rivera Studio"))
    parts.append(_textarea(
        "notes", "Notes / terms",
        "Thanks for your business. Late payments are subject to "
        "1.5%% per month." if is_invoice else "Thank you."))
    return "\n".join(parts)


DOC_TOOLS = [
    {
        "slug": "invoice-generator.html",
        "tool": "invoice",
        "title": "Free Invoice Generator — Make and Print an Invoice in Your Browser",
        "description": ("Free invoice generator: fill in the form, watch the "
                        "invoice build itself, print or save as PDF. No signup, "
                        "no watermark, nothing uploaded anywhere."),
        "h1": "Free Invoice Generator",
        "lede": ("Fill in the form and the invoice builds itself beside you. "
                 "When it looks right, print it or save it as a PDF. There is "
                 "no signup, no watermark, and no upload — everything happens "
                 "inside your own browser."),
        "keyword": "free invoice generator",
        "cross_sell": {
            "key": "invoice-trade",
            "heading": "Working a trade rather than a desk?",
            "body": ("We sell a fillable trade invoice template &mdash; the "
                     "same layout, set up for handyman and contractor work, as "
                     "a PDF you type into and reprint without opening a "
                     "browser."),
            "cta": "See the trade invoice template",
        },
        "faq": [
            ("Is this invoice generator really free?",
             "Yes, and there is no account to create. The tool runs entirely in "
             "your browser, so there is no server cost to pass on to you and no "
             "usage limit to enforce."),
            ("Does my invoice data get uploaded anywhere?",
             "No. Your entries stay in your browser and are saved only to that "
             "browser's local storage so the form still holds your details when "
             "you come back. Clearing your browser data clears them too."),
            ("How do I save the invoice as a PDF?",
             "Press <strong>Print / Save as PDF</strong>. In the print dialog, "
             "choose “Save as PDF” as the destination. The page is "
             "styled for print, so only the invoice itself appears — no menus, "
             "no form, no ads."),
            ("What has to be on a legal invoice?",
             "At minimum: the word Invoice, a unique number, your business name "
             "and contact details, the client's details, the date, an itemised "
             "list of what you supplied, the amount due, and the payment terms. "
             "Our guide on <a href=\"./guides/what-to-include-on-an-invoice.html\">"
             "what to include on an invoice</a> walks through each one."),
        ],
    },
    {
        "slug": "receipt-maker.html",
        "tool": "receipt",
        "title": "Free Receipt Maker — Print a Payment Receipt Instantly",
        "description": ("Free receipt maker for small businesses: itemise a "
                        "payment, stamp it PAID, print or save as PDF. Runs in "
                        "your browser with no signup."),
        "h1": "Free Receipt Maker",
        "lede": ("A receipt proves a payment already happened, which is why it "
                 "is stamped PAID rather than carrying a due date. Fill in what "
                 "was bought and how it was paid for, then print it or save it "
                 "as a PDF."),
        "keyword": "free receipt maker",
        "faq": [
            ("What is the difference between a receipt and an invoice?",
             "An invoice asks for money; a receipt confirms money arrived. If "
             "the client has not paid yet, use the <a href=\"./invoice-generator.html\">"
             "invoice generator</a> instead. See "
             "<a href=\"./guides/invoice-vs-receipt-vs-estimate.html\">invoice vs "
             "receipt vs estimate</a> for the full comparison."),
            ("Do I have to give a receipt?",
             "Rules vary by country and by transaction type, but issuing one is "
             "good practice regardless: it closes the loop for the client and "
             "gives you both a matching record at tax time."),
            ("Can I use this for cash payments?",
             "Yes. Cash is the case where a receipt matters most, because there "
             "is no bank record backing it up. Put “Cash” in the "
             "payment method field."),
        ],
    },
    {
        "slug": "estimate-generator.html",
        "tool": "estimate",
        "title": "Free Estimate & Quote Generator — Send a Priced Quote Today",
        "description": ("Free estimate and quote generator for contractors and "
                        "freelancers: itemise the work, set how long the price "
                        "holds, print or save as PDF."),
        "h1": "Free Estimate &amp; Quote Generator",
        "lede": ("An estimate is a priced proposal, not a bill. Itemise the "
                 "work, set how long the price holds, and send it the same day "
                 "the client asks — speed wins more jobs than polish does."),
        "keyword": "free estimate generator",
        "cross_sell": {
            "key": "estimate-trade",
            "heading": "Quoting trade work off a clipboard?",
            "body": ("Our fillable trade estimate template covers the same "
                     "ground as this tool in a printable PDF &mdash; useful "
                     "when the quote gets written at the customer's kitchen "
                     "table rather than back at the office."),
            "cta": "See the trade estimate template",
        },
        "faq": [
            ("Is an estimate legally binding?",
             "Generally an estimate is an offer rather than a contract, and it "
             "becomes binding when the client accepts it on the stated terms. "
             "Wording matters, so if the number could move, say so on the "
             "document and say why."),
            ("What is the difference between an estimate and a quote?",
             "In everyday use a quote is a firm price and an estimate is an "
             "approximation that may change. Both use the same document; what "
             "differs is what you promise in the notes."),
            ("How long should an estimate stay valid?",
             "Long enough for the client to decide, short enough that your "
             "material costs have not moved — 14 to 30 days is the usual range. "
             "Set it in the “Valid for” field so it prints on the "
             "document."),
        ],
    },
    {
        "slug": "job-sheet-generator.html",
        "tool": "job-sheet",
        "title": "Free Job Sheet &amp; Work Order Generator for Trades",
        "description": ("Free job sheet and work order generator for trades: "
                        "scheduled visit, labour hours, parts used, findings, "
                        "and a customer signature line. Prints straight to PDF."),
        "h1": "Free Job Sheet &amp; Work Order Generator",
        "lede": ("A job sheet is the record of what actually happened on site "
                 "&mdash; who attended, what they found, what they used, and "
                 "that the customer agreed it was done. Fill it in on the van "
                 "or at the desk, then print it or save it as a PDF."),
        "keyword": "job sheet generator",
        "steps": [
            "Fill in your details and the site address. They are remembered in "
            "this browser for the next job.",
            "Add the labour lines in hours, and the parts and materials "
            "separately &mdash; clients query the two differently.",
            "Write what was requested before the visit and what was found "
            "during it. That pairing is what makes the sheet worth keeping.",
            "Press <strong>Print / Save as PDF</strong>. The signature block "
            "prints with it, ready to sign on site.",
        ],
        "cross_sell": {
            "key": "job-sheet",
            "heading": "Prefer a printable pad you can fill in on site?",
            "body": ("Our Operations Kit is a fillable PDF set &mdash; job "
                     "sheet, purchase order, and price list &mdash; that you "
                     "type into once and reprint as often as you need, with no "
                     "browser involved."),
            "cta": "See the Operations Kit",
        },
        "faq": [
            ("What is the difference between a job sheet and an invoice?",
             "A job sheet records the work: who attended, what was found, what "
             "was fitted, and how long it took. An invoice asks for money for "
             "it. Most trades produce both &mdash; the sheet gets signed on "
             "site, and the <a href=\"./invoice-generator.html\">invoice</a> "
             "follows from what it says."),
            ("Do the totals on a job sheet mean the customer owes that amount?",
             "Not by itself. The figures show what the visit came to so nothing "
             "is a surprise later, but the document is labelled as a record of "
             "work rather than a request for payment. Send the invoice "
             "separately once the sheet is signed."),
            ("Why are labour and parts on separate tables?",
             "Because they are usually priced on different logic &mdash; labour "
             "by the hour, parts at cost plus a markup &mdash; and because a "
             "customer querying a bill almost always queries one or the other. "
             "Our <a href=\"./margin-markup-calculator.html\">margin and markup "
             "calculator</a> works out the parts side."),
            ("Does the customer signature make this a contract?",
             "A signature on a job sheet is normally evidence that the work "
             "described was carried out, not a new agreement about price. What "
             "it is worth depends on your terms and your jurisdiction, so if "
             "the sheet is doing contractual work for you, have your own terms "
             "say so."),
        ],
    },
]


CALC_TOOLS = [
    {
        "slug": "late-fee-calculator.html",
        "tool": "late-fee",
        "title": "Late Payment Fee Calculator — What to Charge on an Overdue Invoice",
        "description": ("Work out the late fee on an overdue invoice: monthly "
                        "interest, annual rate, or a flat charge, with the new "
                        "balance due."),
        "h1": "Late Payment Fee Calculator",
        "lede": ("Most small-business contracts say something like "
                 "“1.5% per month on overdue balances.” This works "
                 "out what that actually comes to, and what the client now "
                 "owes."),
        "keyword": "late payment fee calculator",
        "big_label": "Late fee",
        "fields": [
            ("select", "method", "How your contract charges", [
                ("monthly", "Percent per month (most common)"),
                ("annual", "Annual percentage rate, accrued daily"),
                ("flat", "Flat fee, one charge"),
            ], "A monthly rate is charged per started month."),
            ("number", "amount", "Invoice amount outstanding", "1000"),
            ("number", "rate", "Rate (% or flat amount)", "1.5"),
            ("number", "days", "Days overdue", "45"),
            ("currency", "currency", "Currency", None),
        ],
        "faq": [
            ("How much can I legally charge in late fees?",
             "Caps are set locally, not universally — some jurisdictions limit "
             "the rate on commercial debts, and consumer transactions are often "
             "stricter than business-to-business ones. Check your own rules, and "
             "never charge a rate you did not put in the agreement first."),
            ("Do I need the late fee in my contract?",
             "In practice, yes. A fee that appears for the first time on an "
             "overdue invoice is easy for a client to dispute. Put the rate in "
             "the terms they agreed to, and repeat it on every invoice."),
            ("Is a flat fee better than a percentage?",
             "For small invoices a flat fee is more meaningful, and for large "
             "ones a percentage is. Some businesses use both: a flat charge to "
             "cover the admin, plus interest that keeps accruing."),
        ],
    },
    {
        "slug": "sales-tax-calculator.html",
        "tool": "sales-tax",
        "title": "Sales Tax Calculator — Add Tax or Back It Out of a Total",
        "description": ("Add sales tax to a price, or work out the pre-tax "
                        "figure from a total that already includes it. Works "
                        "for VAT, GST, and HST too."),
        "h1": "Sales Tax Calculator",
        "lede": ("Two jobs in one: add tax to a price, or take a total that "
                 "already includes tax and split it back into the net amount "
                 "and the tax. The reverse direction is the one people get "
                 "wrong, because you cannot just subtract the percentage."),
        "keyword": "sales tax calculator",
        "big_label": "Total with tax",
        "fields": [
            ("select", "mode", "Direction", [
                ("add", "Add tax to a pre-tax price"),
                ("remove", "Back tax out of a total"),
            ], ""),
            ("number", "amount", "Amount", "100"),
            ("number", "rate", "Tax rate %", "8.25"),
            ("currency", "currency", "Currency", None),
        ],
        "faq": [
            ("Why can't I just subtract the tax percentage from the total?",
             "Because the percentage was applied to the smaller pre-tax number, "
             "not to the total. Removing 13% tax from $113 gives $100, not "
             "$98.31. The tool divides by 1 + rate, which is the correct way "
             "round."),
            ("Does this work for VAT, GST, and HST?",
             "Yes. They are all percentage taxes applied on top of a net price, "
             "so the arithmetic is identical — only the name and the rate "
             "change."),
            ("What about stacked state and city tax?",
             "If both apply to the same base, add the rates together and enter "
             "the combined figure. If one is charged on top of the other, run "
             "the calculator twice."),
        ],
    },
    {
        "slug": "hourly-rate-calculator.html",
        "tool": "hourly-rate",
        "title": "Freelance Hourly Rate Calculator — What to Charge",
        "description": ("Work backwards from the income you want to the hourly "
                        "rate that gets you there, after unbillable hours, "
                        "expenses, time off, and tax."),
        "h1": "Freelance Hourly Rate Calculator",
        "lede": ("Most freelancers pick a rate by guessing at what sounds "
                 "reasonable. This goes the other way: start from the income "
                 "you need, subtract the hours you cannot bill, and see the "
                 "rate that actually gets you there."),
        "keyword": "freelance hourly rate calculator",
        "big_label": "Minimum hourly rate",
        "fields": [
            ("number", "income", "Take-home income you want per year", "60000"),
            ("number", "expenses", "Business expenses per year", "6000"),
            ("number", "tax", "Tax and contributions %", "25"),
            ("number", "weeksOff", "Weeks off per year", "4"),
            ("number", "hours", "Hours worked per week", "40"),
            ("number", "billable", "Percent of those hours you can bill", "60"),
            ("currency", "currency", "Currency", None),
        ],
        "faq": [
            ("What billable percentage is realistic?",
             "For most solo freelancers it lands between 50% and 70%. The rest "
             "goes to quoting, invoicing, email, marketing, and admin — real "
             "work that no client pays for directly."),
            ("Should I include my own salary in expenses?",
             "No. Put what you want to take home in the income field and keep "
             "expenses for costs the business incurs: software, insurance, "
             "equipment, accounting, workspace."),
            ("The number looks too high. Is it wrong?",
             "It is usually the first honest look at the arithmetic. If the "
             "rate is unsellable in your market, the lever is rarely the rate "
             "alone — raise the billable percentage, cut overhead, or move to "
             "project pricing where speed stops being a penalty."),
        ],
    },
    {
        "slug": "margin-markup-calculator.html",
        "tool": "margin-markup",
        "title": "Margin vs Markup Calculator — Price a Job Without Losing Money",
        "description": ("Convert between margin and markup, and price from cost "
                        "to a target of either. Confusing the two is a common "
                        "way to underprice."),
        "h1": "Margin &amp; Markup Calculator",
        "lede": ("A 50% markup is a 33% margin, and pricing as though they are "
                 "the same is one of the quietest ways to lose money on a job. "
                 "Enter a cost and either a price or a target, and see both "
                 "figures side by side."),
        "keyword": "margin vs markup calculator",
        "big_label": "Selling price",
        "fields": [
            ("select", "mode", "I want to", [
                ("price", "Enter a price and see both figures"),
                ("margin", "Price from a target margin"),
                ("markup", "Price from a target markup"),
            ], ""),
            ("number", "cost", "Your cost", "60"),
            ("number", "price", "Selling price", "100", "price"),
            ("number", "target", "Target percentage", "40", "margin markup"),
            ("currency", "currency", "Currency", None),
        ],
        "faq": [
            ("What is the difference between margin and markup?",
             "Both measure the same profit, against different bases. Margin is "
             "profit divided by the <em>selling price</em>; markup is profit "
             "divided by the <em>cost</em>. Markup is always the larger number."),
            ("Which one should I price with?",
             "Price with markup, because you start from a cost you know. Report "
             "with margin, because that is what the profit is as a share of the "
             "revenue that appears on your books."),
            ("Why does a 100% margin break the maths?",
             "A 100% margin means profit equals the selling price, which means "
             "the cost is zero. There is no finite price that satisfies it for a "
             "non-zero cost, so the calculator caps the input just below 100%."),
        ],
    },
    {
        "slug": "payment-terms-calculator.html",
        "tool": "payment-terms",
        "title": "Invoice Due Date Calculator — Net 30, EOM, and Early-Payment Discounts",
        "description": ("Work out an invoice due date from any payment term, "
                        "and price an early-payment discount like 2/10 net 30 "
                        "before you offer it."),
        "h1": "Invoice Due Date Calculator",
        "lede": ("Net 30 from the 15th is not “the 15th of next "
                 "month.” Pick a term and get the exact due date, plus what "
                 "an early-payment discount really costs you if you offer one."),
        "keyword": "net 30 due date calculator",
        "big_label": "Payment due",
        "fields": [
            ("date", "date", "Invoice date", ""),
            ("terms", "terms", "Payment terms", None),
            ("number", "amount", "Invoice amount (optional)", "1000"),
            ("number", "discPct", "Early-payment discount % (optional)", "2"),
            ("number", "discDays", "Paid within this many days", "10"),
            ("currency", "currency", "Currency", None),
        ],
        "faq": [
            ("What does “net 30” actually mean?",
             "Payment is due 30 days after the invoice date, not at the end of "
             "the following month and not 30 business days. If you mean "
             "something else, write that instead — ambiguity is what turns into "
             "a 60-day wait."),
            ("What does 2/10 net 30 mean?",
             "The client may take 2% off if they pay within 10 days; otherwise "
             "the full amount is due at 30 days. The calculator shows what you "
             "give up and what that discount costs you on an annualised basis — "
             "it is usually far more than it looks."),
            ("Do shorter terms actually get me paid faster?",
             "Often, yes, and the bigger lever is invoicing the day the work "
             "finishes rather than at month end. See "
             "<a href=\"./guides/net-30-payment-terms-explained.html\">net 30 "
             "payment terms explained</a> for the trade-offs."),
        ],
    },
]
