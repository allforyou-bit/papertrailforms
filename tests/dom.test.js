/* DOM tests: load the BUILT pages in jsdom, run the real config.js and
   tools.js against them, and assert what a visitor would actually see.
   The unit tests cover the arithmetic; these cover the wiring — the half
   that breaks when a field id is renamed in one file and not the other.

   jsdom is a dev-only dependency (not committed, not shipped). If it is
   missing these tests are skipped rather than failed, so the gate still
   runs on a clean checkout — qc_site.py reports which mode it used. */
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const ROOT = path.join(__dirname, "..");
let JSDOM;
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  console.log("dom tests: SKIPPED (jsdom not installed — run npm install jsdom)");
  process.exit(0);
}

const CONFIG = fs.readFileSync(path.join(ROOT, "config.js"), "utf8");
const TOOLS = fs.readFileSync(path.join(ROOT, "tools.js"), "utf8");

let passed = 0;
function t(name, fn) {
  try { fn(); passed++; }
  catch (e) {
    console.error("FAIL: " + name + "\n  " + (e && e.message));
    process.exitCode = 1;
  }
}

/** Load a built page, run the site scripts, fire DOMContentLoaded. */
function load(page) {
  const html = fs.readFileSync(path.join(ROOT, page), "utf8");
  const dom = new JSDOM(html, {
    url: "https://papertrailforms.com/" + page,
    runScripts: "outside-only",
    pretendToBeVisual: true
  });
  const w = dom.window;
  w.eval(CONFIG);
  w.eval(TOOLS);
  w.document.dispatchEvent(new w.Event("DOMContentLoaded"));
  return w;
}

function set(w, id, value) {
  const el = w.document.getElementById(id);
  assert.ok(el, "field #" + id + " exists on the page");
  el.value = value;
  el.dispatchEvent(new w.Event("input", { bubbles: true }));
  el.dispatchEvent(new w.Event("change", { bubbles: true }));
  return el;
}

/* ---------------- invoice generator ---------------- */
t("invoice generator renders a total from typed line items", () => {
  const w = load("invoice-generator.html");
  const rows = w.document.querySelectorAll("#items .li-row");
  assert.ok(rows.length >= 2, "starts with blank line rows");

  set(w, "from", "Rivera Studio");
  set(w, "to", "Brightline Cleaning Co.");
  set(w, "date", "2026-01-15");
  set(w, "terms", "net30");
  set(w, "taxPct", "10");

  const r0 = rows[0];
  r0.querySelector(".li-desc").value = "Design work";
  r0.querySelector(".li-qty").value = "3";
  r0.querySelector(".li-rate").value = "100";
  r0.querySelector(".li-rate").dispatchEvent(new w.Event("input", { bubbles: true }));

  const doc = w.document.getElementById("doc").textContent;
  assert.ok(doc.includes("Rivera Studio"), "business name is on the document");
  assert.ok(doc.includes("Brightline Cleaning Co."), "client is on the document");
  assert.ok(doc.includes("Design work"), "line item description shows");
  assert.ok(doc.includes("$300.00"), "subtotal 3 x 100 shows");
  assert.ok(doc.includes("$330.00"), "total with 10% tax shows");
  assert.ok(doc.includes("2026-02-14"), "net 30 due date is calculated");
});

t("invoice generator persists entries to localStorage", () => {
  const w = load("invoice-generator.html");
  set(w, "from", "Persisted Co.");
  const saved = JSON.parse(w.localStorage.getItem("pt-invoice"));
  assert.strictEqual(saved.from, "Persisted Co.");
});

t("adding a line row extends the document", () => {
  const w = load("invoice-generator.html");
  const before = w.document.querySelectorAll("#items .li-row").length;
  w.document.getElementById("add-item").dispatchEvent(
    new w.Event("click", { bubbles: true }));
  assert.strictEqual(
    w.document.querySelectorAll("#items .li-row").length, before + 1);
});

/* ---------------- receipt maker ---------------- */
t("receipt maker stamps PAID and shows no due date", () => {
  const w = load("receipt-maker.html");
  set(w, "method", "e-transfer");
  const doc = w.document.getElementById("doc");
  assert.ok(doc.textContent.includes("PAID"), "PAID stamp is present");
  assert.ok(doc.textContent.includes("e-transfer"), "payment method shows");
  assert.ok(!doc.textContent.includes("Total due"), "a receipt does not ask for money");
});

/* ---------------- job sheet generator ---------------- */
t("job sheet renders labour and parts as separate tables", () => {
  const w = load("job-sheet-generator.html");
  const labour = w.document.querySelectorAll("#labour .li-row");
  const parts = w.document.querySelectorAll("#parts .li-row");
  assert.ok(labour.length >= 2, "starts with blank labour rows");
  assert.ok(parts.length >= 2, "starts with blank parts rows");

  set(w, "from", "Halcyon Mechanical");
  set(w, "to", "Brightline Cleaning Co.");
  set(w, "technician", "R. Okafor");
  set(w, "jobType", "repair");
  set(w, "requested", "No hot water on the second floor.");
  set(w, "performed", "Replaced thermostat.");

  const l0 = labour[0];
  l0.querySelector(".li-desc").value = "Diagnose and replace thermostat";
  l0.querySelector(".li-qty").value = "2.5";
  l0.querySelector(".li-rate").value = "80";
  l0.querySelector(".li-rate").dispatchEvent(new w.Event("input", { bubbles: true }));

  const p0 = parts[0];
  p0.querySelector(".li-desc").value = "Thermostat unit";
  p0.querySelector(".li-qty").value = "1";
  p0.querySelector(".li-rate").value = "91";
  p0.querySelector(".li-rate").dispatchEvent(new w.Event("input", { bubbles: true }));

  const doc = w.document.getElementById("doc").textContent;
  assert.ok(doc.includes("Work Order"), "titled as a work order");
  assert.ok(doc.includes("R. Okafor"), "technician shows");
  assert.ok(doc.includes("Repair"), "job type label shows");
  assert.ok(doc.includes("No hot water"), "work requested shows");
  assert.ok(doc.includes("Replaced thermostat"), "work performed shows");
  assert.ok(doc.includes("$200.00"), "labour 2.5h x 80 shows");
  assert.ok(doc.includes("$91.00"), "parts total shows");
  assert.ok(doc.includes("$291.00"), "job value shows");
  assert.ok(doc.includes("2.50 h"), "hours are totalled");
});

t("job sheet is labelled a record of work, not a bill", () => {
  const w = load("job-sheet-generator.html");
  const doc = w.document.getElementById("doc").textContent;
  assert.ok(doc.includes("not an invoice"), "the disclaimer stamp is present");
  assert.ok(!doc.includes("Total due"), "a job sheet does not ask for money");
  assert.ok(doc.includes("Customer signature"), "signature block prints with it");
});

t("job sheet persists to its own localStorage key", () => {
  const w = load("job-sheet-generator.html");
  set(w, "technician", "S. Duarte");
  const saved = JSON.parse(w.localStorage.getItem("pt-job-sheet"));
  assert.strictEqual(saved.technician, "S. Duarte");
  assert.strictEqual(w.localStorage.getItem("pt-invoice"), null,
                     "it does not overwrite the invoice's saved state");
});

t("adding a parts line does not add a labour line", () => {
  const w = load("job-sheet-generator.html");
  const labourBefore = w.document.querySelectorAll("#labour .li-row").length;
  const partsBefore = w.document.querySelectorAll("#parts .li-row").length;
  w.document.getElementById("add-part").dispatchEvent(
    new w.Event("click", { bubbles: true }));
  assert.strictEqual(
    w.document.querySelectorAll("#parts .li-row").length, partsBefore + 1);
  assert.strictEqual(
    w.document.querySelectorAll("#labour .li-row").length, labourBefore);
});

/* ---------------- curated shop cross-links ---------------- */
t("cross-sell blocks are wired from config and hidden without a url", () => {
  const w = load("job-sheet-generator.html");
  const block = w.document.querySelector('[data-shop-listing="job-sheet"]');
  assert.ok(block, "the cross-sell block exists in the markup");
  const url = (w.SITE_CONFIG.shopListings || {})["job-sheet"];
  if (url) {
    assert.strictEqual(block.hidden, false, "shown once a url is configured");
    assert.strictEqual(
      block.querySelector("[data-shop-listing-link]").getAttribute("href"), url);
  } else {
    assert.strictEqual(block.hidden, true, "no url means no dead link");
  }
});

t("an unconfigured cross-sell key stays hidden", () => {
  const w = load("invoice-generator.html");
  const block = w.document.querySelector("[data-shop-listing]");
  assert.ok(block, "invoice page carries a cross-sell block");
  block.setAttribute("data-shop-listing", "not-a-real-key");
  w.document.dispatchEvent(new w.Event("DOMContentLoaded"));
  assert.strictEqual(block.hidden, true, "unknown key hides the whole block");
});

/* ---------------- calculators ---------------- */
t("late fee calculator shows the fee and the new balance", () => {
  const w = load("late-fee-calculator.html");
  set(w, "method", "monthly");
  set(w, "amount", "1000");
  set(w, "rate", "1.5");
  set(w, "days", "45");
  assert.strictEqual(w.document.getElementById("out-big").textContent, "$30.00");
  const rows = w.document.getElementById("out-rows").textContent;
  assert.ok(rows.includes("$1,030.00"), "new balance due is shown");
});

t("sales tax calculator reverses tax out of a gross total", () => {
  const w = load("sales-tax-calculator.html");
  set(w, "mode", "remove");
  set(w, "amount", "113");
  set(w, "rate", "13");
  assert.strictEqual(w.document.getElementById("out-big").textContent, "$100.00");
  assert.strictEqual(w.document.getElementById("out-label").textContent,
                     "Price before tax");
});

t("hourly rate calculator reports the floor rate", () => {
  const w = load("hourly-rate-calculator.html");
  set(w, "income", "60000");
  set(w, "expenses", "6000");
  set(w, "tax", "25");
  set(w, "weeksOff", "4");
  set(w, "hours", "40");
  set(w, "billable", "60");
  assert.strictEqual(w.document.getElementById("out-big").textContent, "$76.39");
});

t("margin calculator swaps its input field with the mode", () => {
  const w = load("margin-markup-calculator.html");
  const priceField = w.document.querySelector('[data-mode-field="price"]');
  const targetField = w.document.querySelector('[data-mode-field~="margin"]');
  assert.ok(priceField && targetField, "both mode-specific fields exist");
  set(w, "mode", "price");
  assert.strictEqual(priceField.hidden, false, "price field shown in price mode");
  assert.strictEqual(targetField.hidden, true, "target field hidden in price mode");
  set(w, "mode", "margin");
  assert.strictEqual(priceField.hidden, true, "price field hidden in margin mode");
  assert.strictEqual(targetField.hidden, false, "target field shown in margin mode");
  set(w, "cost", "60");
  set(w, "target", "40");
  assert.strictEqual(w.document.getElementById("out-big").textContent, "$100.00");
});

t("due date calculator prices an early-payment discount", () => {
  const w = load("payment-terms-calculator.html");
  set(w, "date", "2026-01-15");
  set(w, "terms", "net30");
  set(w, "amount", "1000");
  set(w, "discPct", "2");
  set(w, "discDays", "10");
  assert.strictEqual(w.document.getElementById("out-big").textContent, "2026-02-14");
  const rows = w.document.getElementById("out-rows").textContent;
  assert.ok(rows.includes("$980.00"), "discounted amount shown");
  assert.ok(rows.includes("2026-01-25"), "discount deadline shown");
});

/* ---------------- config gates ---------------- */
t("shop links are wired when a shop url is configured, hidden when not", () => {
  const w = load("index.html");
  const link = w.document.querySelector("[data-shop-link]");
  assert.ok(link, "a shop link exists in the markup");
  if (w.SITE_CONFIG.etsyShopUrl) {
    assert.strictEqual(link.getAttribute("href"), w.SITE_CONFIG.etsyShopUrl);
    assert.strictEqual(link.hidden, false);
  } else {
    assert.strictEqual(link.hidden, true, "no url means no broken link");
  }
});

t("no advertising script loads while adsenseClient is empty", () => {
  const w = load("index.html");
  assert.strictEqual(w.SITE_CONFIG.adsenseClient, "",
                     "adsense stays off until approval");
  const ads = w.document.querySelectorAll('script[src*="googlesyndication"]');
  assert.strictEqual(ads.length, 0, "no ad script injected");
});

if (!process.exitCode) console.log(`dom tests: ${passed} checks passed`);
else console.error("dom tests FAILED");
