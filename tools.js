/* ============================================================
   Paper Trail Forms — tool engine
   ------------------------------------------------------------
   Zero dependencies, zero network requests. Everything runs in
   the visitor's browser and nothing is ever uploaded: the only
   storage used is localStorage, on the visitor's own machine.

   The file is split in two halves on purpose:
     PART 1  pure functions — no DOM, no globals, unit tested by
             tests/tools.test.js under node
     PART 2  DOM wiring — reads data-tool on <body> and binds the
             matching form
   ============================================================ */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PT = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ========================================================
     PART 1 — pure functions
     ======================================================== */

  var CURRENCIES = {
    USD: "$", CAD: "CA$", EUR: "€", GBP: "£",
    AUD: "A$", NZD: "NZ$", INR: "₹", ZAR: "R"
  };

  /** Round to 2 decimals without the classic 1.005 float surprise. */
  function round2(n) {
    if (!isFinite(n)) return 0;
    return Math.round((n + Number.EPSILON) * 100) / 100;
  }

  /** Format a number as money. Always 2 decimals, thousands separated. */
  function money(n, currency) {
    var sym = CURRENCIES[currency] || CURRENCIES.USD;
    var v = round2(Math.abs(Number(n) || 0));
    var parts = v.toFixed(2).split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (Number(n) < 0 ? "-" : "") + sym + parts.join(".");
  }

  function num(v) {
    var n = parseFloat(String(v == null ? "" : v).replace(/[^0-9.\-]/g, ""));
    return isFinite(n) ? n : 0;
  }

  /**
   * Document totals for an invoice / estimate / receipt.
   * items      : [{description, qty, rate}]
   * taxPct     : percentage applied after the discount
   * discount   : {type: "amount"|"percent", value}
   * shipping   : flat amount added after tax
   */
  function docTotals(items, taxPct, discount, shipping) {
    var subtotal = 0;
    (items || []).forEach(function (it) {
      subtotal += num(it.qty) * num(it.rate);
    });
    subtotal = round2(subtotal);

    var d = discount || {};
    var discountAmt = 0;
    if (d.value) {
      discountAmt = d.type === "percent"
        ? subtotal * (num(d.value) / 100)
        : num(d.value);
    }
    discountAmt = round2(Math.min(Math.max(discountAmt, 0), subtotal));

    var taxable = round2(subtotal - discountAmt);
    var tax = round2(taxable * (num(taxPct) / 100));
    var ship = round2(num(shipping));
    return {
      subtotal: subtotal,
      discount: discountAmt,
      taxable: taxable,
      tax: tax,
      shipping: ship,
      total: round2(taxable + tax + ship)
    };
  }

  /**
   * Sales tax, both directions.
   * mode "add"    : amount is pre-tax, return the tax and the gross
   * mode "remove" : amount already includes tax, back it out
   */
  function salesTax(amount, ratePct, mode) {
    var a = num(amount), r = num(ratePct) / 100;
    if (mode === "remove") {
      var net = r === -1 ? 0 : a / (1 + r);
      return { net: round2(net), tax: round2(a - net), gross: round2(a) };
    }
    var tax = a * r;
    return { net: round2(a), tax: round2(tax), gross: round2(a + tax) };
  }

  /**
   * Late fee on an overdue invoice.
   * method "monthly" : rate is % per month (the common contract wording)
   * method "annual"  : rate is % per year, accrued daily on a 365-day year
   * method "flat"    : one fixed charge, days ignored
   * A monthly rate is charged per started month, matching how most
   * small-business contracts are actually written.
   */
  function lateFee(amount, rate, daysLate, method) {
    var a = num(amount), r = num(rate), d = Math.max(0, Math.floor(num(daysLate)));
    var fee = 0, months = 0;
    if (method === "flat") {
      fee = r;
    } else if (method === "annual") {
      fee = a * (r / 100) * (d / 365);
    } else {
      months = Math.ceil(d / 30);
      fee = a * (r / 100) * months;
    }
    fee = round2(Math.max(0, fee));
    return {
      fee: fee,
      months: months,
      days: d,
      total: round2(a + fee),
      dailyEquivalent: d > 0 ? round2(fee / d) : 0
    };
  }

  /**
   * What to charge per hour to actually clear a target take-home.
   * Works backwards from income, not forwards from a guess.
   */
  function hourlyRate(o) {
    o = o || {};
    var income = num(o.targetIncome);
    var expenses = num(o.expenses);
    var taxPct = Math.min(Math.max(num(o.taxPct), 0), 95);
    var weeksOff = Math.min(Math.max(num(o.weeksOff), 0), 51);
    var hoursPerWeek = Math.max(num(o.hoursPerWeek), 0);
    var billablePct = Math.min(Math.max(num(o.billablePct), 1), 100);

    var weeksWorked = 52 - weeksOff;
    var billableHours = weeksWorked * hoursPerWeek * (billablePct / 100);
    var beforeTax = (income + expenses) / (1 - taxPct / 100);
    var rate = round2(billableHours > 0 ? beforeTax / billableHours : 0);
    return {
      weeksWorked: weeksWorked,
      billableHours: round2(billableHours),
      revenueNeeded: round2(beforeTax),
      hourlyRate: rate,
      /* derived from the ROUNDED rate, so the two figures we show a
         visitor stay consistent when they multiply one by eight */
      dayRate: round2(rate * 8)
    };
  }

  /**
   * Margin and markup are not the same number, and pricing off the
   * wrong one is how small shops quietly lose money.
   * Supply cost plus exactly one of: price, marginPct, markupPct.
   */
  function marginMarkup(o) {
    o = o || {};
    var cost = num(o.cost), price;
    if (o.price != null && o.price !== "") {
      price = num(o.price);
    } else if (o.marginPct != null && o.marginPct !== "") {
      var m = Math.min(num(o.marginPct), 99.99) / 100;
      price = m >= 1 ? 0 : cost / (1 - m);
    } else if (o.markupPct != null && o.markupPct !== "") {
      price = cost * (1 + num(o.markupPct) / 100);
    } else {
      price = 0;
    }
    var profit = price - cost;
    return {
      cost: round2(cost),
      price: round2(price),
      profit: round2(profit),
      marginPct: price ? round2((profit / price) * 100) : 0,
      markupPct: cost ? round2((profit / cost) * 100) : 0
    };
  }

  /* ---- date helpers: UTC only, so a timezone never shifts a due date ---- */
  function parseDate(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || "").trim());
    if (!m) return null;
    var d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
    return isNaN(d.getTime()) ? null : d;
  }
  function fmtDate(d) {
    if (!d) return "";
    return d.toISOString().slice(0, 10);
  }
  function addDays(d, n) {
    return new Date(d.getTime() + n * 86400000);
  }
  function endOfMonth(d) {
    return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 0));
  }

  /**
   * Due date from an issue date and a payment term.
   * term: "due"|"net7"|"net14"|"net15"|"net30"|"net45"|"net60"|"net90"
   *       |"eom"      end of the month the invoice was issued
   *       |"eom15"    the 15th of the following month
   *       |"mfi15"    "15th month following invoice"  (same as eom15)
   */
  function dueDate(issue, term) {
    var d = parseDate(issue);
    if (!d) return { due: "", days: 0, label: "" };
    var due, label;
    var netMatch = /^net(\d+)$/.exec(String(term || ""));
    if (term === "due" || term === "net0") {
      due = d; label = "Due on receipt";
    } else if (term === "eom") {
      due = endOfMonth(d); label = "End of month";
    } else if (term === "eom15" || term === "mfi15") {
      var nm = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 15));
      due = nm; label = "15th of the following month";
    } else if (netMatch) {
      due = addDays(d, parseInt(netMatch[1], 10));
      label = "Net " + netMatch[1];
    } else {
      due = addDays(d, 30); label = "Net 30";
    }
    return {
      due: fmtDate(due),
      days: Math.round((due.getTime() - d.getTime()) / 86400000),
      label: label
    };
  }

  /** Early-payment discount, e.g. "2/10 net 30". */
  function earlyPayDiscount(amount, discountPct, discountDays, netDays) {
    var a = num(amount), p = num(discountPct);
    var dd = Math.max(1, num(discountDays)), nd = Math.max(dd + 1, num(netDays));
    var saved = round2(a * (p / 100));
    var annualised = round2((p / (100 - p)) * (365 / (nd - dd)) * 100);
    return { saved: saved, payNow: round2(a - saved), annualisedPct: annualised };
  }

  var api = {
    CURRENCIES: CURRENCIES,
    round2: round2, money: money, num: num,
    docTotals: docTotals, salesTax: salesTax, lateFee: lateFee,
    hourlyRate: hourlyRate, marginMarkup: marginMarkup,
    dueDate: dueDate, earlyPayDiscount: earlyPayDiscount,
    parseDate: parseDate, fmtDate: fmtDate
  };

  /* ========================================================
     PART 2 — DOM wiring (skipped entirely under node)
     ======================================================== */
  if (typeof document === "undefined") return api;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function val(id) { var el = document.getElementById(id); return el ? el.value : ""; }
  function todayISO() { return new Date().toISOString().slice(0, 10); }

  /* ---------- document builders: invoice / estimate / receipt ---------- */

  var DOC_KINDS = {
    invoice: { title: "Invoice", numLabel: "Invoice #", dateLabel: "Invoice date", prefix: "INV-" },
    estimate: { title: "Estimate", numLabel: "Estimate #", dateLabel: "Estimate date", prefix: "EST-" },
    receipt: { title: "Receipt", numLabel: "Receipt #", dateLabel: "Date paid", prefix: "REC-" }
  };

  function addItemRow(values) {
    var wrap = $("#items");
    if (!wrap) return;
    var row = document.createElement("div");
    row.className = "li-row";
    row.innerHTML =
      '<input type="text" class="li-desc" placeholder="Description of work or item" aria-label="Description">' +
      '<input type="number" class="li-qty" placeholder="Qty" step="any" min="0" aria-label="Quantity">' +
      '<input type="number" class="li-rate" placeholder="Rate" step="any" min="0" aria-label="Rate">' +
      '<button type="button" class="btn-mini danger li-del" aria-label="Remove line">&times;</button>';
    wrap.appendChild(row);
    var v = values || {};
    $(".li-desc", row).value = v.description || "";
    $(".li-qty", row).value = v.qty == null ? "1" : v.qty;
    $(".li-rate", row).value = v.rate == null ? "" : v.rate;
    $(".li-del", row).addEventListener("click", function () {
      row.parentNode.removeChild(row);
      if (!$$("#items .li-row").length) addItemRow();
      renderDoc();
    });
    $$("input", row).forEach(function (inp) {
      inp.addEventListener("input", renderDoc);
    });
  }

  function readItems() {
    return $$("#items .li-row").map(function (row) {
      return {
        description: $(".li-desc", row).value,
        qty: $(".li-qty", row).value,
        rate: $(".li-rate", row).value
      };
    });
  }

  function docState() {
    return {
      kind: document.body.getAttribute("data-tool"),
      from: val("from"), fromDetails: val("fromDetails"),
      to: val("to"), toDetails: val("toDetails"),
      number: val("number"), date: val("date"), terms: val("terms"),
      currency: val("currency"), taxLabel: val("taxLabel"), taxPct: val("taxPct"),
      discountType: val("discountType"), discountValue: val("discountValue"),
      shipping: val("shipping"), notes: val("notes"),
      payment: val("payment"), method: val("method"),
      items: readItems()
    };
  }

  function renderDoc() {
    var out = $("#doc");
    if (!out) return;
    var s = docState();
    var kind = DOC_KINDS[s.kind] || DOC_KINDS.invoice;
    var t = docTotals(s.items, s.taxPct, { type: s.discountType, value: s.discountValue }, s.shipping);
    var cur = s.currency || "USD";
    var due = s.kind === "invoice" ? dueDate(s.date, s.terms) : null;

    var rows = s.items.filter(function (it) {
      return String(it.description).trim() || num(it.rate);
    }).map(function (it) {
      return "<tr><td>" + esc(it.description || "&mdash;") + "</td>" +
             '<td class="num">' + (num(it.qty) || 0) + "</td>" +
             '<td class="num">' + money(it.rate, cur) + "</td>" +
             '<td class="num">' + money(num(it.qty) * num(it.rate), cur) + "</td></tr>";
    }).join("");
    if (!rows) {
      rows = '<tr><td colspan="4" style="color:#5b6b82">Add a line item to see it here.</td></tr>';
    }

    var totals = '<div><span>Subtotal</span><span>' + money(t.subtotal, cur) + "</span></div>";
    if (t.discount) totals += "<div><span>Discount</span><span>-" + money(t.discount, cur) + "</span></div>";
    if (t.tax) totals += "<div><span>" + esc(s.taxLabel || "Tax") + " (" + num(s.taxPct) + "%)</span><span>" + money(t.tax, cur) + "</span></div>";
    if (t.shipping) totals += "<div><span>Shipping</span><span>" + money(t.shipping, cur) + "</span></div>";
    totals += '<div class="grand"><span>' + (s.kind === "receipt" ? "Paid" : "Total due") + "</span><span>" + money(t.total, cur) + "</span></div>";

    var metaRight = "";
    if (s.kind === "invoice") {
      metaRight = '<div class="blk"><div class="lbl">' + kind.dateLabel + "</div>" + esc(s.date || todayISO()) +
        '<div class="lbl" style="margin-top:8px">Due</div>' + esc(due.due || "—") +
        " <span style=\"color:#5b6b82\">(" + esc(due.label) + ")</span></div>";
    } else if (s.kind === "receipt") {
      metaRight = '<div class="blk"><div class="lbl">' + kind.dateLabel + "</div>" + esc(s.date || todayISO()) +
        '<div class="lbl" style="margin-top:8px">Payment method</div>' + esc(s.method || "—") + "</div>";
    } else {
      metaRight = '<div class="blk"><div class="lbl">' + kind.dateLabel + "</div>" + esc(s.date || todayISO()) +
        '<div class="lbl" style="margin-top:8px">Valid until</div>' + esc(dueDate(s.date, s.terms).due || "—") + "</div>";
    }

    out.innerHTML =
      '<div class="doc-head">' +
        '<div><div class="doc-title">' + kind.title + "</div>" +
          (s.kind === "receipt" ? '<div style="margin-top:8px"><span class="paid-stamp">PAID</span></div>' : "") +
        "</div>" +
        '<div class="doc-from"><strong>' + esc(s.from || "Your business name") + "</strong><br>" +
          esc(s.fromDetails || "").replace(/\n/g, "<br>") + "</div>" +
      "</div>" +
      '<div class="doc-meta">' +
        '<div class="blk"><div class="lbl">' + (s.kind === "estimate" ? "Prepared for" : "Bill to") + "</div>" +
          "<strong>" + esc(s.to || "Client name") + "</strong><br>" +
          esc(s.toDetails || "").replace(/\n/g, "<br>") + "</div>" +
        '<div class="blk"><div class="lbl">' + kind.numLabel + "</div>" + esc(s.number || kind.prefix + "0001") + "</div>" +
        metaRight +
      "</div>" +
      "<table><thead><tr><th>Description</th>" +
        '<th class="num">Qty</th><th class="num">Rate</th><th class="num">Amount</th>' +
        "</tr></thead><tbody>" + rows + "</tbody></table>" +
      '<div class="totals">' + totals + "</div>" +
      (s.payment ? '<div class="doc-notes"><strong>Payment</strong>\n' + esc(s.payment) + "</div>" : "") +
      (s.notes ? '<div class="doc-notes">' + esc(s.notes) + "</div>" : "");

    try {
      localStorage.setItem("pt-" + s.kind, JSON.stringify(s));
    } catch (e) { /* private mode: the tool still works, it just won't remember */ }
  }

  function restoreDoc(kind) {
    var raw = null;
    try { raw = localStorage.getItem("pt-" + kind); } catch (e) { raw = null; }
    var s = null;
    if (raw) { try { s = JSON.parse(raw); } catch (e) { s = null; } }

    var simple = ["from", "fromDetails", "to", "toDetails", "number", "date",
                  "terms", "currency", "taxLabel", "taxPct", "discountType",
                  "discountValue", "shipping", "notes", "payment", "method"];
    if (s) {
      simple.forEach(function (k) {
        var el = document.getElementById(k);
        if (el && s[k] != null && s[k] !== "") el.value = s[k];
      });
    }
    if (!val("date")) { var dEl = document.getElementById("date"); if (dEl) dEl.value = todayISO(); }
    if (!val("number")) {
      var nEl = document.getElementById("number");
      if (nEl) nEl.value = (DOC_KINDS[kind] || DOC_KINDS.invoice).prefix + "0001";
    }
    if (s && s.items && s.items.length) s.items.forEach(function (it) { addItemRow(it); });
    else { addItemRow(); addItemRow(); }
  }

  function wireDocTool(kind) {
    restoreDoc(kind);
    $$("#tool-form input, #tool-form select, #tool-form textarea").forEach(function (el) {
      el.addEventListener("input", renderDoc);
      el.addEventListener("change", renderDoc);
    });
    var add = $("#add-item");
    if (add) add.addEventListener("click", function () { addItemRow(); renderDoc(); });
    var print = $("#print-doc");
    if (print) print.addEventListener("click", function () { window.print(); });
    var reset = $("#reset-doc");
    if (reset) reset.addEventListener("click", function () {
      if (!window.confirm("Clear this " + kind + " and start over?")) return;
      try { localStorage.removeItem("pt-" + kind); } catch (e) { /* nothing to clear */ }
      window.location.reload();
    });
    renderDoc();
  }

  /* ---------- calculators ---------- */

  function setOut(id, text) { var el = document.getElementById(id); if (el) el.textContent = text; }
  function setRows(id, pairs) {
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = pairs.map(function (p) {
      return "<div><span>" + esc(p[0]) + "</span><span>" + esc(p[1]) + "</span></div>";
    }).join("");
  }

  var CALCS = {
    "late-fee": function () {
      var cur = val("currency") || "USD";
      var r = lateFee(val("amount"), val("rate"), val("days"), val("method"));
      setOut("out-big", money(r.fee, cur));
      var rows = [
        ["Original invoice", money(val("amount"), cur)],
        ["Days overdue", String(r.days)]
      ];
      if (val("method") === "monthly") rows.push(["Months charged (part months round up)", String(r.months)]);
      rows.push(["Late fee", money(r.fee, cur)]);
      rows.push(["New balance due", money(r.total, cur)]);
      if (r.days > 0 && val("method") !== "flat") {
        rows.push(["Works out to, per day", money(r.dailyEquivalent, cur)]);
      }
      setRows("out-rows", rows);
    },
    "sales-tax": function () {
      var cur = val("currency") || "USD";
      var mode = val("mode") || "add";
      var r = salesTax(val("amount"), val("rate"), mode);
      setOut("out-big", money(mode === "remove" ? r.net : r.gross, cur));
      setOut("out-label", mode === "remove" ? "Price before tax" : "Total with tax");
      setRows("out-rows", [
        ["Price before tax", money(r.net, cur)],
        ["Tax at " + num(val("rate")) + "%", money(r.tax, cur)],
        ["Total charged", money(r.gross, cur)]
      ]);
    },
    "hourly-rate": function () {
      var cur = val("currency") || "USD";
      var r = hourlyRate({
        targetIncome: val("income"), expenses: val("expenses"), taxPct: val("tax"),
        weeksOff: val("weeksOff"), hoursPerWeek: val("hours"), billablePct: val("billable")
      });
      setOut("out-big", money(r.hourlyRate, cur));
      setRows("out-rows", [
        ["Weeks worked per year", String(r.weeksWorked)],
        ["Billable hours per year", String(r.billableHours)],
        ["Revenue you must invoice", money(r.revenueNeeded, cur)],
        ["Minimum hourly rate", money(r.hourlyRate, cur)],
        ["Equivalent day rate (8h)", money(r.dayRate, cur)]
      ]);
    },
    "margin-markup": function () {
      var cur = val("currency") || "USD";
      var mode = val("mode") || "price";
      var o = { cost: val("cost") };
      if (mode === "price") o.price = val("price");
      if (mode === "margin") o.marginPct = val("target");
      if (mode === "markup") o.markupPct = val("target");
      var r = marginMarkup(o);
      setOut("out-big", money(r.price, cur));
      setRows("out-rows", [
        ["Cost", money(r.cost, cur)],
        ["Selling price", money(r.price, cur)],
        ["Profit per unit", money(r.profit, cur)],
        ["Margin (profit ÷ price)", r.marginPct.toFixed(2) + "%"],
        ["Markup (profit ÷ cost)", r.markupPct.toFixed(2) + "%"]
      ]);
      /* a field may list several modes, space separated */
      $$("[data-mode-field]").forEach(function (el) {
        var modes = el.getAttribute("data-mode-field").split(/\s+/);
        el.hidden = modes.indexOf(mode) === -1;
      });
    },
    "payment-terms": function () {
      var cur = val("currency") || "USD";
      var r = dueDate(val("date"), val("terms"));
      setOut("out-big", r.due || "—");
      var rows = [
        ["Invoice date", val("date") || "—"],
        ["Term", r.label],
        ["Days to pay", String(r.days)],
        ["Payment due", r.due || "—"]
      ];
      if (num(val("amount")) && num(val("discPct"))) {
        var e = earlyPayDiscount(val("amount"), val("discPct"), val("discDays"), r.days);
        var early = dueDate(val("date"), "net" + Math.max(1, Math.floor(num(val("discDays")))));
        rows.push(["Early-payment discount", num(val("discPct")) + "% if paid by " + early.due]);
        rows.push(["Client pays instead", money(e.payNow, cur)]);
        rows.push(["You give up", money(e.saved, cur)]);
        rows.push(["Cost of that discount, annualised", e.annualisedPct.toFixed(1) + "%"]);
      }
      setRows("out-rows", rows);
    }
  };

  document.addEventListener("DOMContentLoaded", function () {
    var tool = document.body.getAttribute("data-tool");
    if (!tool) return;
    if (DOC_KINDS[tool]) { wireDocTool(tool); return; }
    var calc = CALCS[tool];
    if (!calc) return;
    var dEl = document.getElementById("date");
    if (dEl && !dEl.value) dEl.value = todayISO();
    $$("#tool-form input, #tool-form select").forEach(function (el) {
      el.addEventListener("input", calc);
      el.addEventListener("change", calc);
    });
    calc();
  });

  return api;
});
