/* Unit tests for the pure half of tools.js. Run by qc_site.py — a
   failure here blocks deployment, same rule as the question banks.
   No test framework: node + assert only, so there is nothing to install. */
const assert = require("assert");
const PT = require("../tools.js");

let passed = 0;
function t(name, fn) {
  try { fn(); passed++; }
  catch (e) {
    console.error("FAIL: " + name + "\n  " + e.message);
    process.exitCode = 1;
  }
}
const near = (a, b, msg) => assert.ok(Math.abs(a - b) < 0.005, `${msg}: ${a} != ${b}`);

/* ---- money / rounding ---- */
t("money formats with separators and 2dp", () => {
  assert.strictEqual(PT.money(1234.5, "USD"), "$1,234.50");
  assert.strictEqual(PT.money(0, "CAD"), "CA$0.00");
  assert.strictEqual(PT.money(-12.345, "USD"), "-$12.35");
  assert.strictEqual(PT.money(1000000, "GBP"), "£1,000,000.00");
});
t("round2 handles the classic float cases", () => {
  assert.strictEqual(PT.round2(1.005), 1.01);
  assert.strictEqual(PT.round2(2.675), 2.68);
  assert.strictEqual(PT.round2(0.1 + 0.2), 0.3);
});
t("num strips currency noise", () => {
  assert.strictEqual(PT.num("$1,200.50"), 1200.5);
  assert.strictEqual(PT.num(""), 0);
  assert.strictEqual(PT.num("abc"), 0);
});

/* ---- document totals ---- */
t("docTotals sums line items", () => {
  const r = PT.docTotals([{ qty: 3, rate: 40 }, { qty: 1, rate: 120 }], 0, null, 0);
  assert.strictEqual(r.subtotal, 240);
  assert.strictEqual(r.total, 240);
});
t("docTotals applies tax after a percentage discount", () => {
  const r = PT.docTotals([{ qty: 1, rate: 1000 }], 10, { type: "percent", value: 20 }, 0);
  assert.strictEqual(r.discount, 200);
  assert.strictEqual(r.taxable, 800);
  assert.strictEqual(r.tax, 80);
  assert.strictEqual(r.total, 880);
});
t("docTotals adds shipping after tax", () => {
  const r = PT.docTotals([{ qty: 2, rate: 50 }], 10, null, 15);
  assert.strictEqual(r.tax, 10);
  assert.strictEqual(r.total, 125);
});
t("docTotals never discounts below zero", () => {
  const r = PT.docTotals([{ qty: 1, rate: 100 }], 0, { type: "amount", value: 500 }, 0);
  assert.strictEqual(r.discount, 100);
  assert.strictEqual(r.total, 0);
});
t("docTotals ignores blank rows", () => {
  const r = PT.docTotals([{ qty: "", rate: "" }, { qty: 2, rate: 10 }], 0, null, 0);
  assert.strictEqual(r.subtotal, 20);
});

/* ---- sales tax ---- */
t("salesTax adds tax", () => {
  const r = PT.salesTax(100, 8.25, "add");
  assert.strictEqual(r.tax, 8.25);
  assert.strictEqual(r.gross, 108.25);
});
t("salesTax backs tax out of a gross figure", () => {
  const r = PT.salesTax(108.25, 8.25, "remove");
  near(r.net, 100, "net");
  near(r.tax, 8.25, "tax");
});
t("salesTax round-trips", () => {
  const g = PT.salesTax(249.99, 13, "add").gross;
  near(PT.salesTax(g, 13, "remove").net, 249.99, "round trip");
});

/* ---- late fees ---- */
t("lateFee monthly charges part months as whole months", () => {
  const r = PT.lateFee(1000, 1.5, 31, "monthly");
  assert.strictEqual(r.months, 2);
  assert.strictEqual(r.fee, 30);
  assert.strictEqual(r.total, 1030);
});
t("lateFee monthly at exactly 30 days is one month", () => {
  assert.strictEqual(PT.lateFee(1000, 1.5, 30, "monthly").months, 1);
});
t("lateFee annual accrues daily", () => {
  const r = PT.lateFee(5000, 18, 45, "annual");
  near(r.fee, 5000 * 0.18 * 45 / 365, "annual fee");
});
t("lateFee flat ignores days", () => {
  const r = PT.lateFee(800, 25, 90, "flat");
  assert.strictEqual(r.fee, 25);
  assert.strictEqual(r.total, 825);
});
t("lateFee is zero when nothing is overdue", () => {
  assert.strictEqual(PT.lateFee(1000, 1.5, 0, "monthly").fee, 0);
  assert.strictEqual(PT.lateFee(1000, 1.5, -10, "monthly").fee, 0);
});

/* ---- hourly rate ---- */
t("hourlyRate works backwards from take-home", () => {
  const r = PT.hourlyRate({
    targetIncome: 60000, expenses: 6000, taxPct: 25,
    weeksOff: 4, hoursPerWeek: 40, billablePct: 60
  });
  assert.strictEqual(r.weeksWorked, 48);
  near(r.billableHours, 1152, "billable hours");
  near(r.revenueNeeded, 88000, "revenue needed");
  near(r.hourlyRate, 88000 / 1152, "rate");
  near(r.dayRate, r.hourlyRate * 8, "day rate");
});
t("hourlyRate does not divide by zero", () => {
  const r = PT.hourlyRate({ targetIncome: 50000, hoursPerWeek: 0, billablePct: 50 });
  assert.strictEqual(r.hourlyRate, 0);
});

/* ---- margin vs markup ---- */
t("marginMarkup separates margin from markup", () => {
  const r = PT.marginMarkup({ cost: 60, price: 100 });
  assert.strictEqual(r.profit, 40);
  near(r.marginPct, 40, "margin");
  near(r.markupPct, 66.67, "markup");
});
t("marginMarkup prices from a target margin", () => {
  const r = PT.marginMarkup({ cost: 60, marginPct: 40 });
  assert.strictEqual(r.price, 100);
});
t("marginMarkup prices from a target markup", () => {
  const r = PT.marginMarkup({ cost: 60, markupPct: 50 });
  assert.strictEqual(r.price, 90);
  near(r.marginPct, 33.33, "margin from markup");
});
t("marginMarkup survives a 100% margin request", () => {
  const r = PT.marginMarkup({ cost: 50, marginPct: 100 });
  assert.ok(isFinite(r.price), "price stays finite");
});

/* ---- discount and sale price ---- */
t("discountPrice takes a percentage off a list price", () => {
  const r = PT.discountPrice({ list: 100, discountPct: 20 });
  assert.strictEqual(r.salePrice, 80);
  assert.strictEqual(r.saved, 20);
  near(r.discountPct, 20, "discount pct");
});
t("discountPrice derives the discount from a sale price", () => {
  const r = PT.discountPrice({ list: 250, salePrice: 200 });
  near(r.discountPct, 20, "derived discount");
  assert.strictEqual(r.saved, 50);
});
t("discountPrice leaves the margin analysis out until a cost is given", () => {
  const r = PT.discountPrice({ list: 100, discountPct: 20 });
  assert.strictEqual(r.hasCost, false);
  assert.strictEqual(r.breakEvenMultiplier, undefined,
                     "no cost means no invented margin figures");
});
t("discountPrice shows the profit falling faster than the price", () => {
  /* the headline claim of the guide, pinned as a test: 10% off a 30%
     margin costs a third of the profit, not a tenth */
  const r = PT.discountPrice({ list: 1000, cost: 700, discountPct: 10 });
  assert.strictEqual(r.profitBefore, 300);
  assert.strictEqual(r.profitAfter, 200);
  near(r.marginBefore, 30, "margin before");
  near(r.marginAfter, 22.22, "margin after");
  near(r.profitDropPct, 33.33, "share of profit given up");
});
t("discountPrice reports the volume needed to stand still", () => {
  const r = PT.discountPrice({ list: 100, cost: 60, discountPct: 20 });
  assert.strictEqual(r.profitAfter, 20);
  near(r.breakEvenMultiplier, 2, "must double the volume");
  near(r.extraVolumePct, 100, "100% more units");
});
t("discountPrice refuses a break-even once the sale is at or below cost", () => {
  const r = PT.discountPrice({ list: 100, cost: 60, discountPct: 50 });
  assert.strictEqual(r.belowCost, true);
  assert.strictEqual(r.breakEvenMultiplier, null,
                     "no volume recovers a below-cost price");
  assert.strictEqual(r.extraVolumePct, null);
});
t("discountPrice clamps a discount to the 0-100 range", () => {
  assert.strictEqual(PT.discountPrice({ list: 100, discountPct: 140 }).salePrice, 0);
  assert.strictEqual(PT.discountPrice({ list: 100, discountPct: -30 }).salePrice, 100);
});
t("discountPrice survives a zero list price", () => {
  const r = PT.discountPrice({ list: 0, salePrice: 0 });
  assert.ok(isFinite(r.discountPct), "no divide by zero");
  assert.strictEqual(r.salePrice, 0);
});

/* ---- due dates ---- */
t("dueDate handles net terms", () => {
  assert.strictEqual(PT.dueDate("2026-01-15", "net30").due, "2026-02-14");
  assert.strictEqual(PT.dueDate("2026-01-15", "net30").days, 30);
  assert.strictEqual(PT.dueDate("2026-11-20", "net45").due, "2027-01-04");
});
t("dueDate handles due-on-receipt", () => {
  const r = PT.dueDate("2026-03-02", "due");
  assert.strictEqual(r.due, "2026-03-02");
  assert.strictEqual(r.days, 0);
});
t("dueDate handles end of month, including February", () => {
  assert.strictEqual(PT.dueDate("2026-02-03", "eom").due, "2026-02-28");
  assert.strictEqual(PT.dueDate("2024-02-03", "eom").due, "2024-02-29");
});
t("dueDate handles the 15th of the following month", () => {
  assert.strictEqual(PT.dueDate("2026-12-28", "eom15").due, "2027-01-15");
});
t("dueDate crosses a leap day correctly", () => {
  assert.strictEqual(PT.dueDate("2024-02-27", "net7").due, "2024-03-05");
});
t("dueDate rejects garbage input without throwing", () => {
  assert.strictEqual(PT.dueDate("not-a-date", "net30").due, "");
  assert.strictEqual(PT.dueDate("", "net30").due, "");
});

/* ---- early payment discount ---- */
t("earlyPayDiscount prices 2/10 net 30", () => {
  const r = PT.earlyPayDiscount(1000, 2, 10, 30);
  assert.strictEqual(r.saved, 20);
  assert.strictEqual(r.payNow, 980);
  near(r.annualisedPct, 37.24, "annualised cost");
});

/* ---- job sheet totals ---- */
t("jobTotals keeps labour and parts apart", () => {
  const r = PT.jobTotals(
    [{ hours: 2.5, rate: 80 }, { hours: 1, rate: 80 }],
    [{ qty: 2, rate: 45.5 }],
    {});
  assert.strictEqual(r.hours, 3.5);
  assert.strictEqual(r.labour, 280);
  assert.strictEqual(r.parts, 91);
  assert.strictEqual(r.subtotal, 371);
  assert.strictEqual(r.total, 371);
});
t("jobTotals adds the call-out before the discount", () => {
  const r = PT.jobTotals([{ hours: 1, rate: 100 }], [], {
    callOut: 50, discount: { type: "percent", value: 10 }
  });
  assert.strictEqual(r.subtotal, 150);
  /* 10% of 150, not 10% of 100 — the discount covers the whole visit */
  assert.strictEqual(r.discount, 15);
  assert.strictEqual(r.total, 135);
});
t("jobTotals taxes the discounted amount only", () => {
  const r = PT.jobTotals([{ hours: 4, rate: 75 }], [{ qty: 1, rate: 200 }], {
    taxPct: 15, discount: { type: "amount", value: 100 }
  });
  assert.strictEqual(r.subtotal, 500);
  assert.strictEqual(r.taxable, 400);
  assert.strictEqual(r.tax, 60);
  assert.strictEqual(r.total, 460);
});
t("jobTotals never lets a discount go past the subtotal", () => {
  const r = PT.jobTotals([{ hours: 1, rate: 50 }], [], {
    discount: { type: "amount", value: 999 }
  });
  assert.strictEqual(r.discount, 50);
  assert.strictEqual(r.total, 0);
});
t("jobTotals survives empty and junk input", () => {
  const r = PT.jobTotals(null, undefined, null);
  assert.strictEqual(r.total, 0);
  assert.strictEqual(r.hours, 0);
  const j = PT.jobTotals([{ hours: "two", rate: "abc" }], [{ qty: "", rate: "" }], {});
  assert.strictEqual(j.total, 0);
});
t("jobTotals handles fractional hours without float drift", () => {
  const r = PT.jobTotals([{ hours: 0.1, rate: 0.2 }, { hours: 1.15, rate: 100 }], [], {});
  assert.strictEqual(r.labour, 115.02);
  assert.strictEqual(r.hours, 1.25);
});

if (!process.exitCode) console.log(`tools.js: ${passed} assertions passed`);
else console.error("tools.js unit tests FAILED");
