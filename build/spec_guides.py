# -*- coding: utf-8 -*-
"""Guide articles for Paper Trail Forms.

Each guide is a plain-language explainer that sends the reader to the
tool that does the arithmetic. Written for small-business owners and
freelancers, not accountants — no jargon that is not immediately
defined, and no advice that pretends to be legal or tax advice.
"""

GUIDES = [
    {
        "slug": "what-to-include-on-an-invoice.html",
        "title": "What to Include on an Invoice (and What Gets You Paid Faster)",
        "description": ("The nine things every invoice needs, plus the four "
                        "details that quietly decide whether you get paid in "
                        "two weeks or two months."),
        "h1": "What to Include on an Invoice",
        "meta": "Invoicing basics",
        "body": """
  <p>An invoice has two jobs. The first is administrative: it has to be a
  record both sides can file, match, and defend at tax time. The second is
  commercial: it has to make paying you the path of least resistance. Most
  invoices do the first job and neglect the second, which is why so many
  small businesses wait sixty days for money they earned in one.</p>

  <h2>The nine things every invoice needs</h2>

  <ol>
  <li><strong>The word “Invoice.”</strong> Not “statement,” not
  “summary.” Accounts-payable systems and inboxes both sort on it.</li>
  <li><strong>A unique invoice number.</strong> Sequential is fine. What matters
  is that no two invoices share one, so a query about “invoice 214”
  can only mean one document.</li>
  <li><strong>Your business name and contact details.</strong> Include the email
  address you actually monitor, not the one on your domain that forwards
  somewhere you check monthly.</li>
  <li><strong>The client's details.</strong> For a company, name the entity, not
  just the person who hired you. If they gave you a purchase order number, put
  it on the invoice — in larger organisations, a missing PO number is the single
  most common reason an invoice sits unpaid.</li>
  <li><strong>The invoice date.</strong> This is the date the clock starts, which
  is why it should be the day you send it, not the day you started the work.</li>
  <li><strong>An itemised description of what you supplied.</strong> One line per
  distinct thing, with quantity and rate. A single line saying
  “Services — $4,000” invites questions that delay payment.</li>
  <li><strong>The amount due, including tax.</strong> Show the subtotal, the tax
  as its own line with the rate, and the total. If you are not registered to
  charge tax, do not show a tax line at all.</li>
  <li><strong>Payment terms and the due date.</strong> Write the actual date, not
  just “Net 30.” Removing the arithmetic removes an excuse.</li>
  <li><strong>How to pay.</strong> Bank details, e-transfer address, payment link
  — whatever you accept, spelled out on the invoice itself.</li>
  </ol>

  <div class="notice">Requirements differ by country, and registered
  businesses often have to show a tax number or specific wording. Check what
  your own tax authority requires; the list above is the commercial core, not
  a legal checklist.</div>

  <h2>The four details that decide how fast you get paid</h2>

  <p><strong>Send it the day the work finishes.</strong> Nothing else on this
  page moves the date as much. An invoice sent on the 30th of the month and an
  invoice sent on the 2nd are, in most approval cycles, a month apart in
  practice.</p>

  <p><strong>Address it to a person as well as an entity.</strong> Invoices sent
  to a generic accounts inbox with no named contact are the ones that fall
  through. Ask, once, who processes payments — then use that name every time.</p>

  <p><strong>Make the total unmissable.</strong> One number, larger than
  everything else on the page. A client scanning on a phone should be able to
  see what they owe without zooming.</p>

  <p><strong>State the late fee before it applies.</strong> A late fee that
  appears for the first time on an overdue invoice is easy to argue with. One
  that has been printed on every invoice since the first, and was in the
  agreement they signed, is not. Our
  <a href="../late-fee-calculator.html">late payment fee calculator</a> shows
  what a given rate actually adds up to.</p>

  <h2>What to leave off</h2>

  <p>Leave off apologies. Leave off long explanations of why the number is what
  it is — the itemisation is the explanation. And leave off any wording that
  makes the payment sound optional: “whenever is convenient” is
  read as permission to wait.</p>

  <h2>Build one now</h2>

  <p>The <a href="../invoice-generator.html">free invoice generator</a> lays out
  all nine elements for you, calculates the due date from the term you pick, and
  prints or saves as a PDF. Nothing is uploaded — the whole thing runs in your
  browser.</p>
""",
        "faq": [
            ("Do I need an invoice number if I only send a few invoices?",
             "Yes. Numbers are how you and your client refer to a specific "
             "document later, and how your own records stay unambiguous. Start "
             "at 0001 and never reuse one."),
            ("Should I put my address on an invoice if I work from home?",
             "You need a business address that reaches you, but it does not have "
             "to be your living room. Many sole traders use a mailbox service or "
             "a registered agent address for exactly this reason."),
            ("Can I invoice before doing the work?",
             "Yes — a deposit invoice is normal, and for new clients it is a "
             "sensible risk control. Label it clearly as a deposit and show how "
             "it will be applied against the final total."),
        ],
    },
    {
        "slug": "net-30-payment-terms-explained.html",
        "title": "Net 30 Payment Terms Explained (and When to Use Something Else)",
        "description": ("What net 30, net 15, EOM, and 2/10 net 30 actually "
                        "mean, how to choose between them, and the term that "
                        "gets small invoices paid fastest."),
        "h1": "Net 30 Payment Terms Explained",
        "meta": "Getting paid",
        "body": """
  <p>Payment terms are the sentence on your invoice that says when the money is
  due. They look like boilerplate. They are actually the single lever on the
  document with the most direct effect on your cash flow, and most small
  businesses copy whatever their first client used without ever choosing.</p>

  <h2>What the common terms mean</h2>

  <table>
  <thead><tr><th>Term</th><th>Means</th><th>Typical use</th></tr></thead>
  <tbody>
  <tr><td>Due on receipt</td><td>Payable immediately</td><td>Small jobs, new clients, retail</td></tr>
  <tr><td>Net 7 / Net 14</td><td>7 or 14 days from the invoice date</td><td>Freelance and trade work</td></tr>
  <tr><td>Net 30</td><td>30 days from the invoice date</td><td>The business-to-business default</td></tr>
  <tr><td>Net 60 / Net 90</td><td>60 or 90 days</td><td>Large corporates, often non-negotiable</td></tr>
  <tr><td>EOM</td><td>End of the month the invoice was issued</td><td>Recurring monthly services</td></tr>
  <tr><td>15 MFI</td><td>The 15th of the month following the invoice</td><td>Clients with fixed payment runs</td></tr>
  <tr><td>2/10 net 30</td><td>2% off if paid in 10 days, otherwise due at 30</td><td>Encouraging early payment</td></tr>
  </tbody>
  </table>

  <p>Net 30 means thirty calendar days from the invoice date. Not thirty business
  days, not the end of the following month, and not thirty days from when the
  client got round to approving it. If you want any of those instead, write
  them out — the ambiguity is never resolved in your favour.</p>

  <h2>Why net 30 became the default</h2>

  <p>It predates instant transfers. Thirty days was roughly how long it took a
  cheque to be raised, signed, posted, and cleared, and it survived into an era
  where the same payment takes seconds. Large organisations keep it because it
  is free working capital; small suppliers keep it because they assume it is
  expected.</p>

  <p>It usually is not. For a solo trade or freelance business, net 14 is
  accepted far more often than people expect, particularly if it has been in the
  agreement since the start rather than introduced later.</p>

  <h2>Choosing a term that fits the client</h2>

  <ul class="checklist">
  <li><strong>New client, small job:</strong> due on receipt, or a deposit up
  front and the balance on delivery.</li>
  <li><strong>Established client, ongoing work:</strong> net 14 or net 30, whichever
  matches how they actually pay rather than what they say.</li>
  <li><strong>Large organisation:</strong> ask about their payment run before you
  quote. If they pay on the 15th and the 30th, an invoice dated the 16th is
  effectively net 44 no matter what you print on it.</li>
  <li><strong>Long project:</strong> milestone invoices, not one at the end. The
  term matters much less than the number of times you get to send one.</li>
  </ul>

  <h2>Early-payment discounts, priced honestly</h2>

  <p>2/10 net 30 sounds cheap. Giving up 2% to be paid 20 days early works out
  to roughly 37% on an annualised basis — far more than the cost of almost any
  short-term credit. It can still be worth it if cash timing is genuinely tight,
  but it should be a deliberate decision rather than a habit copied from a
  template. The
  <a href="../payment-terms-calculator.html">invoice due date calculator</a>
  prices the discount alongside the due date so the trade-off is visible.</p>

  <h2>Terms only work if the invoice arrives</h2>

  <p>A tight term on an invoice sent three weeks late is worse than a loose term
  on one sent the same day. Invoice promptly, state the actual due date rather
  than the term alone, and put the late-fee rate in the agreement before you
  need it.</p>
""",
        "faq": [
            ("Is net 30 from the invoice date or the delivery date?",
             "From the invoice date, unless your contract says otherwise. This "
             "is one more reason to date the invoice the day you send it."),
            ("Can I change payment terms for an existing client?",
             "You can, going forward, with notice. Changing them retroactively "
             "on an outstanding invoice is not enforceable and damages the "
             "relationship. Announce the change, apply it to new work."),
            ("What term gets small invoices paid fastest?",
             "Due on receipt with a payment link, sent the day the work "
             "finishes. The friction you remove matters more than the deadline "
             "you set."),
        ],
    },
    {
        "slug": "invoice-vs-receipt-vs-estimate.html",
        "title": "Invoice vs Receipt vs Estimate: Which Document Do You Send?",
        "description": ("Three documents, three different moments in a job. "
                        "What each one is for, what has to be on it, and the "
                        "mix-ups that cause disputes."),
        "h1": "Invoice vs Receipt vs Estimate",
        "meta": "Document basics",
        "body": """
  <p>These three documents look similar and are constantly used
  interchangeably. They are not interchangeable: each one marks a different
  moment in a job, and sending the wrong one changes what you are actually
  claiming.</p>

  <table>
  <thead><tr><th></th><th>Estimate / Quote</th><th>Invoice</th><th>Receipt</th></tr></thead>
  <tbody>
  <tr><td><strong>When</strong></td><td>Before the work</td><td>After the work, before payment</td><td>After payment</td></tr>
  <tr><td><strong>Says</strong></td><td>“Here is what it would cost”</td><td>“Here is what you owe”</td><td>“Here is proof you paid”</td></tr>
  <tr><td><strong>Carries a due date</strong></td><td>No — a validity date</td><td>Yes</td><td>No</td></tr>
  <tr><td><strong>Creates a receivable</strong></td><td>No</td><td>Yes</td><td>No, it clears one</td></tr>
  <tr><td><strong>Typical dispute</strong></td><td>Scope crept past the number</td><td>“We never received it”</td><td>“We already paid that”</td></tr>
  </tbody>
  </table>

  <h2>The estimate</h2>

  <p>An estimate prices work that has not happened yet. Its most important field
  is not the total — it is the scope, because an estimate is only as protective
  as its description of what is included. The second most important is the
  validity date, which stops a price you gave in March being held against you in
  September.</p>

  <p>A quote and an estimate use the same document. The difference is what you
  promise: a quote is a firm price, an estimate is an approximation that may
  move. If yours can move, say so and say why.</p>

  <h2>The invoice</h2>

  <p>An invoice is a demand for payment and, in your books, the thing that
  creates a receivable. It needs a unique number, a date, an itemisation, the
  total, and terms. Once sent, it should not be edited — if something is wrong,
  issue a credit note or a corrected invoice with a new number, so the audit
  trail stays intact.</p>

  <h2>The receipt</h2>

  <p>A receipt confirms money arrived. It is the client's evidence for their own
  books and, for cash payments, often the only evidence that exists at all. A
  receipt does not carry a due date and should not look like it is asking for
  anything.</p>

  <h2>The mix-ups that cause problems</h2>

  <ul class="checklist">
  <li><strong>Sending an invoice when you meant to quote.</strong> You have just
  billed for work you have not done. Awkward at best; at worst it is treated as
  the agreed price.</li>
  <li><strong>Marking an invoice “paid” instead of issuing a
  receipt.</strong> Workable, but two documents with the same number in
  different states is exactly what confuses a bookkeeper months later.</li>
  <li><strong>Letting an estimate turn into an invoice by silence.</strong> If the
  client accepts and you never invoice, nothing in your books says you are owed
  anything.</li>
  <li><strong>Reusing numbers across the three.</strong> Keep separate sequences:
  EST-, INV-, REC-. Then a number always identifies one document.</li>
  </ul>

  <h2>Make each one</h2>

  <p>All three run in your browser, free and without signup:
  <a href="../estimate-generator.html">estimate generator</a>,
  <a href="../invoice-generator.html">invoice generator</a>, and
  <a href="../receipt-maker.html">receipt maker</a>.</p>
""",
        "faq": [
            ("Can one document be both an invoice and a receipt?",
             "In small cash transactions people often use a single document "
             "marked paid. It works, but keeping them separate leaves a cleaner "
             "trail — one document created the obligation, another cleared it."),
            ("Does a client have to accept an estimate in writing?",
             "Written acceptance is much easier to rely on later. An email "
             "saying “approved, go ahead” is written acceptance; a "
             "phone call is not."),
            ("What is a pro forma invoice?",
             "A document that looks like an invoice but is issued before "
             "supply, usually so a buyer can arrange payment or clear customs. "
             "It does not create a receivable — functionally it is a quote in "
             "invoice clothing."),
        ],
    },
    {
        "slug": "how-to-charge-late-fees.html",
        "title": "How to Charge Late Fees on Overdue Invoices Without Losing the Client",
        "description": ("Setting a late fee that holds up: where it has to "
                        "appear, how much is reasonable, and the escalation "
                        "sequence that recovers money."),
        "h1": "How to Charge Late Fees on Overdue Invoices",
        "meta": "Getting paid",
        "body": """
  <p>A late fee is not really about the money. It is about being the invoice
  that gets paid first when a client's payment run is shorter than their pile of
  bills. That only works if the fee was agreed before it was applied.</p>

  <h2>Where the fee has to appear</h2>

  <p>Three places, in this order:</p>

  <ol class="steps">
  <li><strong>In the agreement.</strong> The contract, engagement letter, or
  accepted quote the client said yes to. This is the one that matters if it is
  ever contested.</li>
  <li><strong>On every invoice.</strong> Not just the overdue ones — a rate that
  has been printed on all twelve invoices this year is a policy, while one that
  appears on the thirteenth is a surprise.</li>
  <li><strong>In the reminder.</strong> State it as a fact about what happens
  next, not as a threat.</li>
  </ol>

  <div class="notice">Caps on late-payment interest are set locally, and
  business-to-business rules often differ from consumer ones. Check what applies
  where you operate before you set a rate. Nothing here is legal advice.</div>

  <h2>How much is reasonable</h2>

  <p>The common small-business rate is 1% to 2% per month on the outstanding
  balance. Above that you start to look punitive, which is exactly the framing a
  client needs to dispute it rather than pay it.</p>

  <p>Two structures are worth considering. A percentage keeps accruing, which
  matters on large invoices. A flat fee is more meaningful on small ones — 1.5%
  of a $200 invoice is $3, which nobody rearranges their week for. Some
  businesses use both: a fixed administration charge plus interest.</p>

  <p>The <a href="../late-fee-calculator.html">late payment fee calculator</a>
  works out the fee three ways — per month, annualised and accrued daily, or
  flat — and shows the new balance.</p>

  <h2>The escalation sequence that actually works</h2>

  <ol class="steps">
  <li><strong>Day 1 after due:</strong> a short, neutral email. Assume it was
  missed, because it usually was. Attach the invoice again.</li>
  <li><strong>Day 7:</strong> reply on the same thread, mention the late-fee rate
  and the date it starts applying.</li>
  <li><strong>Day 14:</strong> phone the person who processes payments, not your
  usual contact. Ask what they need to release it — often the answer is a PO
  number or a form you did not know existed.</li>
  <li><strong>Day 30:</strong> issue a revised invoice including the fee, with a
  firm date, and state what happens after it: work paused, files held, or the
  account passed on.</li>
  <li><strong>Day 45+:</strong> follow through on exactly what you said. Empty
  escalation teaches the client the deadlines are decorative.</li>
  </ol>

  <h2>Waiving the fee on purpose</h2>

  <p>Charging the fee and then waiving it for a good client is a stronger move
  than never charging it. It establishes that the policy is real, and it hands
  you a concession to make. What does not work is applying it inconsistently
  without saying so — that reads as arbitrary, and it is the fastest way to turn
  a payment delay into an argument.</p>

  <h2>Prevention beats collection</h2>

  <p>Deposits on new clients, milestone invoicing on long projects, and invoices
  sent the day work finishes prevent far more overdue balances than any fee
  recovers. See <a href="./net-30-payment-terms-explained.html">net 30 payment
  terms explained</a> for choosing terms that match how the client actually
  pays.</p>
""",
        "faq": [
            ("Can I charge a late fee if it was not in the contract?",
             "You can add it to an invoice, but a client who disputes it has a "
             "strong position, and enforcement in most places rests on an agreed "
             "term. Put it in the agreement first."),
            ("Does interest compound?",
             "Only if your agreement says so. Simple interest on the original "
             "balance is the norm for small-business terms and is far easier to "
             "explain and defend."),
            ("Should I stop work when an invoice goes overdue?",
             "If your agreement allows it and you have warned them, pausing is "
             "usually more effective than any fee. Say it in advance, then do it "
             "on the date you named."),
        ],
    },
    {
        "slug": "how-to-set-your-freelance-rate.html",
        "title": "How to Set Your Freelance Rate (Working Backwards From What You Need)",
        "description": ("Why guessing at an hourly rate underprices you, how to "
                        "calculate a floor from the income you need, and when "
                        "to leave hourly pricing behind."),
        "h1": "How to Set Your Freelance Rate",
        "meta": "Pricing",
        "body": """
  <p>Most freelancers set a rate by finding out what someone else charges and
  shading it downward. That produces a number with no relationship to what the
  business actually needs to survive, and it is why so many people are busy and
  broke at the same time.</p>

  <h2>Start from the floor, not the market</h2>

  <p>Your floor is the rate below which the work is not worth doing. It comes
  out of four inputs:</p>

  <ol>
  <li><strong>The income you want to take home</strong> — after tax, before
  anything else.</li>
  <li><strong>Your business expenses</strong> — software, insurance, equipment,
  accounting, workspace, the things you pay for whether or not you have a
  client this month.</li>
  <li><strong>Tax and contributions</strong> — as a percentage. Self-employment
  usually costs more here than employment did.</li>
  <li><strong>Your billable hours</strong> — the honest number, not the hours you
  work.</li>
  </ol>

  <p>That last one is where the arithmetic usually breaks. A forty-hour week is
  not forty billable hours. Quoting, invoicing, chasing payment, marketing,
  admin, and learning are all real work that no client pays for. For most solo
  freelancers the billable share lands between 50% and 70%. If you assume 100%,
  you will undercharge by roughly half.</p>

  <p>The <a href="../hourly-rate-calculator.html">freelance hourly rate
  calculator</a> runs this backwards for you: income, expenses, tax, time off,
  and billable percentage in, minimum hourly rate out.</p>

  <h2>An example</h2>

  <p>Take home $60,000. Expenses $6,000. Tax and contributions 25%. Four weeks
  off, forty hours a week, 60% billable.</p>

  <ul class="checklist">
  <li>Revenue needed before tax: <strong>$88,000</strong></li>
  <li>Weeks worked: 48 · billable hours: <strong>1,152</strong></li>
  <li>Floor rate: <strong>about $76 an hour</strong></li>
  </ul>

  <p>People who would have quoted $45 are surprised by this. The rate did not go
  up; the hidden hours were always there.</p>

  <h2>The floor is not the price</h2>

  <p>The floor tells you when to say no. What you actually charge is a market
  question, and it is set by the value of the outcome rather than the hours.
  Specialists, urgent work, high-stakes deliverables, and clients with real
  budgets all support prices well above the floor. Being cheap does not win
  those clients — it disqualifies you from them.</p>

  <h2>When to stop charging by the hour</h2>

  <p>Hourly pricing has a structural flaw: getting faster costs you money. Once
  you know a job type well enough to estimate it reliably, quote the job rather
  than the hours. Keep the hourly floor as your internal check — if the fixed
  price divided by your realistic hours lands below the floor, the price is
  wrong.</p>

  <p>Whichever you choose, put it on paper before starting. The
  <a href="../estimate-generator.html">estimate generator</a> produces a priced,
  itemised quote in a couple of minutes.</p>

  <h2>Raising an existing rate</h2>

  <p>Announce it, do not negotiate it. Give existing clients notice, apply it
  from a named date, and quote new clients at the new number immediately. Rates
  that only rise when a client complains about something else never rise.</p>
""",
        "faq": [
            ("Should I list my rate publicly?",
             "It filters out clients who cannot afford you, which saves time, "
             "and it costs you the ones who would have paid more for a "
             "high-value job. Many freelancers publish a starting-from figure "
             "as a compromise."),
            ("How often should I raise my rate?",
             "Annually is a reasonable rhythm, plus whenever you are booked out "
             "well in advance — a persistent waiting list is the clearest signal "
             "the price is under the market."),
            ("What if my calculated floor is above the local market?",
             "Then hourly work in that market cannot fund your target. The "
             "options are to raise the billable share, cut overhead, move to "
             "value-based pricing, or serve clients outside that market."),
        ],
    },
    {
        "slug": "margin-vs-markup.html",
        "title": "Margin vs Markup: The Difference That Quietly Costs You Money",
        "description": ("Margin and markup measure the same profit against "
                        "different bases. Confusing them underprices jobs. The "
                        "conversion, with a worked example."),
        "h1": "Margin vs Markup",
        "meta": "Pricing",
        "body": """
  <p>You buy something for $60 and sell it for $100. Did you make a 40% margin
  or a 67% markup? Both — they are the same $40 of profit measured against
  different bases. Treating them as interchangeable is one of the most common
  and least visible pricing errors in small business.</p>

  <h2>The two formulas</h2>

  <table>
  <thead><tr><th></th><th>Formula</th><th>Base</th><th>$60 cost, $100 price</th></tr></thead>
  <tbody>
  <tr><td><strong>Margin</strong></td><td>(price − cost) ÷ price</td><td>Selling price</td><td>40%</td></tr>
  <tr><td><strong>Markup</strong></td><td>(price − cost) ÷ cost</td><td>Your cost</td><td>66.7%</td></tr>
  </tbody>
  </table>

  <p>Markup is always the larger number, because the cost is always smaller than
  the price. The gap widens fast as profitability rises: a 50% margin is a 100%
  markup, and a 60% margin is a 150% markup.</p>

  <h2>How the mistake costs money</h2>

  <p>Suppose you need a 40% margin to cover overhead and profit, and you price
  by adding 40% to cost. On a $60 item you charge $84. Your actual margin is
  28.6% — you are 11 points short on every unit, and nothing on your invoice
  shows it. At $200,000 of annual revenue that gap is over $22,000.</p>

  <p>The correct price for a 40% margin is cost ÷ (1 − 0.40) = $100. The
  <a href="../margin-markup-calculator.html">margin and markup calculator</a>
  converts in either direction and prices from a target of either.</p>

  <h2>Quick conversion table</h2>

  <table>
  <thead><tr><th>Target margin</th><th>Markup to apply</th><th>Price on a $100 cost</th></tr></thead>
  <tbody>
  <tr><td>10%</td><td>11.1%</td><td>$111.11</td></tr>
  <tr><td>20%</td><td>25%</td><td>$125.00</td></tr>
  <tr><td>25%</td><td>33.3%</td><td>$133.33</td></tr>
  <tr><td>33.3%</td><td>50%</td><td>$150.00</td></tr>
  <tr><td>40%</td><td>66.7%</td><td>$166.67</td></tr>
  <tr><td>50%</td><td>100%</td><td>$200.00</td></tr>
  <tr><td>60%</td><td>150%</td><td>$250.00</td></tr>
  </tbody>
  </table>

  <h2>Which one to use where</h2>

  <p><strong>Price with markup.</strong> You start from a cost you know, so
  applying a multiplier to it is the natural operation at the point of quoting.</p>

  <p><strong>Report with margin.</strong> Margin is profit as a share of revenue,
  which is what appears on your books and what anyone comparing businesses will
  use. It is also the figure that tells you whether the business works at
  scale.</p>

  <p><strong>Never mix them in one conversation.</strong> If a supplier offers
  “40 points” and you assume margin while they mean markup, the
  difference is real money. Ask which base.</p>

  <h2>Don't forget the cost side</h2>

  <p>Both formulas are only as good as the cost you feed in. For service work,
  cost is not just materials — it is the hours at your true internal rate,
  including the unbillable ones. The
  <a href="../hourly-rate-calculator.html">hourly rate calculator</a> works that
  figure out, and it is usually higher than people expect.</p>
""",
        "faq": [
            ("Is a 100% markup the same as a 100% margin?",
             "No. A 100% markup means you doubled the cost, which is a 50% "
             "margin. A 100% margin would mean the cost was zero."),
            ("Which do retailers use?",
             "Retail generally talks in margin, because it maps to the profit "
             "and loss statement. Trades and wholesale more often talk in "
             "markup. Always confirm which base is meant."),
            ("How do I include overhead?",
             "Either load it into the cost figure before applying markup, or "
             "set a target margin high enough to cover overhead plus profit. "
             "Pick one method and use it consistently, or you will double-count."),
        ],
    },
    {
        "slug": "how-to-write-an-estimate-that-wins.html",
        "title": "How to Write an Estimate That Wins the Job",
        "description": ("What separates estimates that get accepted from ones "
                        "that get ignored: scope, options, validity, and the "
                        "speed of the reply."),
        "h1": "How to Write an Estimate That Wins the Job",
        "meta": "Winning work",
        "body": """
  <p>Clients rarely pick the cheapest estimate. They pick the one that makes the
  decision easiest — the one that arrives first, is clear about what is
  included, and does not leave them wondering what happens if something changes.</p>

  <h2>Speed beats polish</h2>

  <p>The single strongest predictor of winning a small job is being the first
  credible reply. A clear estimate sent within a few hours beats a beautifully
  formatted one sent next week, because by then the client has already been
  reassured by someone else. If you cannot price it immediately, reply
  immediately with when you will.</p>

  <h2>Scope is the whole document</h2>

  <p>The total is one line. What decides whether the job goes well is the
  itemisation around it. Write scope so that a stranger could tell whether a
  given task is included, and be explicit about the edges:</p>

  <ul class="checklist">
  <li>What is included, in specific terms — not “site prep” but what
  site prep means here.</li>
  <li>What is explicitly excluded, especially the things clients commonly assume.</li>
  <li>What you need from them, and by when: access, approvals, files, decisions.</li>
  <li>What triggers a change order, and how changes get priced.</li>
  </ul>

  <p>An exclusions list feels negative to write and prevents most disputes.
  Nobody argues about a boundary that was on the page before they said yes.</p>

  <h2>Give options, not one number</h2>

  <p>A single price is a yes-or-no question. Two or three options turn it into a
  choice about scope, which is a far easier conversation and often lands higher
  than your single number would have. A common structure is a lean version, the
  recommended version, and an extended version — most clients choose the
  middle, and some choose the top.</p>

  <h2>Put a validity date on it</h2>

  <p>Prices move. Fourteen to thirty days is normal, and it does two useful
  things: it protects you from a quote resurfacing after your costs changed, and
  it creates a reason to decide. The
  <a href="../estimate-generator.html">estimate generator</a> prints the validity
  date on the document.</p>

  <h2>Say what happens next</h2>

  <p>End with the mechanics, not a hope. Name the acceptance step (reply to this
  email), the deposit if there is one, the lead time once accepted, and how
  invoicing will work. See
  <a href="./invoice-vs-receipt-vs-estimate.html">invoice vs receipt vs
  estimate</a> for how the documents connect.</p>

  <h2>Follow up once, properly</h2>

  <p>One follow-up a few days after sending recovers a meaningful share of jobs
  that would otherwise go silent. Keep it short, offer to adjust the scope
  rather than the price, and then stop. Persistent chasing costs you the next
  job as well as this one.</p>

  <h2>Estimate honestly</h2>

  <p>Winning a job at a price you cannot deliver profitably is worse than losing
  it. Check the number against your floor before you send it — the
  <a href="../hourly-rate-calculator.html">hourly rate calculator</a> and the
  <a href="../margin-markup-calculator.html">margin calculator</a> exist for
  exactly that check.</p>
""",
        "faq": [
            ("Should I show a line-by-line price breakdown?",
             "Itemise the scope, but be careful about pricing every line — it "
             "invites the client to delete lines they do not understand. Many "
             "trades itemise the work and price it in grouped stages."),
            ("How do I handle a client who wants a lower price?",
             "Change the scope, not the rate. Removing something is a "
             "negotiation; discounting the same work teaches them your first "
             "number was inflated."),
            ("What if the job turns out bigger than estimated?",
             "That is what the change-order clause is for. Raise it as soon as "
             "you see it, in writing, with the revised number — not at the end."),
        ],
    },
    {
        "slug": "small-business-record-keeping-basics.html",
        "title": "Small Business Record Keeping Basics (What to Keep and for How Long)",
        "description": ("A simple filing system for invoices, receipts, and "
                        "estimates: numbering, what to retain, how long, and "
                        "the monthly routine that keeps it honest."),
        "h1": "Small Business Record Keeping Basics",
        "meta": "Admin",
        "body": """
  <p>Record keeping only becomes urgent at two moments: when a client disputes
  something, and when someone asks to see your books. Both arrive without
  warning, and the work cannot be done retroactively. The good news is that a
  system that holds up takes about ten minutes a month once it exists.</p>

  <h2>Number everything, in separate sequences</h2>

  <p>Three sequences, never reused, never reset mid-year:</p>

  <ul class="checklist">
  <li><strong>EST-0001</strong> for estimates and quotes</li>
  <li><strong>INV-0001</strong> for invoices</li>
  <li><strong>REC-0001</strong> for receipts you issue</li>
  </ul>

  <p>A gap in a sequence is a question you will have to answer. If you void a
  document, keep the number and mark it void rather than deleting it.</p>

  <h2>What to keep</h2>

  <table>
  <thead><tr><th>Document</th><th>Why it matters</th></tr></thead>
  <tbody>
  <tr><td>Invoices you issued</td><td>Proves income and supports what you claim was billed</td></tr>
  <tr><td>Receipts and bills you paid</td><td>Supports expense claims — no receipt, usually no deduction</td></tr>
  <tr><td>Bank and payment-processor statements</td><td>The independent record everything else is matched against</td></tr>
  <tr><td>Accepted estimates and contracts</td><td>The agreed scope and terms, including any late-fee clause</td></tr>
  <tr><td>Mileage and asset records</td><td>Commonly required in a specific format, and impossible to reconstruct</td></tr>
  </tbody>
  </table>

  <div class="notice">Retention periods are set by your own tax authority and
  commonly run several years past the filing date — longer for property and
  asset records. Check the rule that applies to you rather than assuming; this
  is not tax advice.</div>

  <h2>A filing system that survives contact with reality</h2>

  <p>The best system is the one you will still use in month nine. That usually
  means folders by year, then by type, with filenames that sort correctly:</p>

  <p><code>2026/invoices-out/2026-03-14_INV-0042_brightline.pdf</code></p>

  <p>Date first in ISO format so files sort chronologically, then the document
  number, then the client. Anyone — including future you — can find a document
  from a partial memory of any one of the three.</p>

  <h2>The ten-minute monthly routine</h2>

  <ol class="steps">
  <li>Export or download the month's bank and processor statements.</li>
  <li>Match every deposit to an invoice, and mark those invoices paid.</li>
  <li>Chase anything unpaid past its due date, today rather than next month.</li>
  <li>File the month's expense receipts into the folder for that month.</li>
  <li>Note the total invoiced and the total collected. Those two numbers, tracked
  monthly, tell you more about the business than anything else you could
  measure.</li>
  </ol>

  <h2>Digital copies</h2>

  <p>Scans and PDFs are widely accepted, but keep them somewhere that is backed
  up and not solely on one laptop. If a paper receipt is fading — thermal
  till receipts often go blank within a year — photograph it the day you get
  it.</p>

  <h2>Make the documents in the first place</h2>

  <p>The <a href="../invoice-generator.html">invoice generator</a>,
  <a href="../receipt-maker.html">receipt maker</a>, and
  <a href="../estimate-generator.html">estimate generator</a> produce
  consistently numbered, print-ready documents in your browser. Save each one as
  a PDF into the folder structure above as you create it, and the filing is
  already done.</p>
""",
        "faq": [
            ("Do I need accounting software?",
             "Not at the start. A consistent folder structure, a spreadsheet of "
             "invoices with their status, and monthly bank matching cover a "
             "surprising amount. Software earns its place when volume makes "
             "manual matching slow."),
            ("Are photos of receipts acceptable?",
             "Usually, provided they are legible and complete. Many tax "
             "authorities accept digital copies; check yours, and keep the "
             "originals of anything high-value until you have confirmed."),
            ("How long should I keep records?",
             "Longer than you think, and the exact period depends on your "
             "jurisdiction and the document type. Storage is cheap — when in "
             "doubt, keep it."),
        ],
    },
]
