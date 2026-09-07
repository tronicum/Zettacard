#!/usr/bin/env node
// Module-hub smoke test (ADR-app-0002 § 1, roadmap 3.5).
//
// Same rule as test_user_journeys.mjs, and for the same reason: if a person
// has to click it, this file clicks it. page.evaluate is used only to READ
// state, never to set it. The hub is an overlay that calls
// setInertBehindDialog(), which is exactly the mechanism behind the worst
// bug this project has shipped (a language switch that left the whole app
// inert behind an open menu), so the inert assertions below are not
// decoration - they are the reason this file exists.
//
// Usage:
//   node scripts/serve-app.mjs 8802 &
//   node scripts/test_module_hub.mjs                     # localhost:8802
import { chromium } from "playwright";
import { existsSync } from "node:fs";

// Same launcher as test_user_journeys.mjs: the sandboxed container ships a
// Chromium at a fixed path, and the workspace VM this may also run in has
// no way to install one (no sudo, so playwright's install-deps cannot run).
async function launchChromium() {
  const sandboxPath = "/opt/pw-browsers/chromium";
  if (existsSync(sandboxPath)) return chromium.launch({ executablePath: sandboxPath });
  return chromium.launch();
}
const SITE = process.argv[2] || "http://localhost:8802";
const VIEWPORT = { width: 390, height: 844 };
let failures = 0;
const fail = (m) => { console.error("  FAIL: " + m); failures++; };
const ok = (m) => console.log("  ok: " + m);

const browser = await launchChromium();
const ctx = await browser.newContext({ viewport: VIEWPORT });
const page = await ctx.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });

await page.goto(`${SITE}/app.html`, { waitUntil: "networkidle" });
if (await page.isVisible("#storage-consent-notice")) {
  await page.click("#storage-consent-yes");
  await page.waitForTimeout(200);
}

// The picker is mandatory on a first visit.
if (!(await page.isVisible("#module-picker"))) fail("module picker not shown on first visit");
const row = page.locator('[data-exam-type="fuehrerschein"]');
if (!(await row.count())) { fail("no fuehrerschein row in picker"); }
else {
  await row.first().click();
  await page.waitForTimeout(400);
  // A module with more than one scope shows the scope step first
  // (fuehrerschein is B / BE), so the hub is two clicks away, not one.
  const scope = page.locator("#module-picker [data-scope-code]");
  if (await scope.count()) {
    await scope.first().click();
    ok("scope step shown for a multi-scope module");
  }
  await page.waitForTimeout(1800);

  // 1. The hub, not the question list, not the intro wizard.
  if (await page.isVisible("#module-hub")) ok("opening a module lands on the hub");
  else fail("hub not visible after selecting a module");
  if (await page.isVisible("#module-intro")) fail("old intro wizard still opens");

  const txt = async (sel) => (await page.locator(sel).innerText().catch(() => "")).trim();
  for (const [sel, name] of [
    ["#module-hub-title", "name"], ["#module-hub-chip", "kind chip"],
    ["#module-hub-primary", "primary action"], ["#module-hub-progress", "progress"],
    ["#module-hub-sim", "simulation button"], ["#module-hub-practice", "practice button"],
    ["#module-hub-about-summary", "about summary"], ["#module-hub-close", "close"],
  ]) {
    const t = await txt(sel);
    if (t) ok(`${name}: "${t.slice(0, 58)}"`); else fail(`${name} (${sel}) is empty`);
  }

  const topics = await page.locator("#module-hub-topics .hub-topic-btn").count();
  if (topics > 0) ok(`${topics} topic rows`); else fail("no topic rows rendered");

  // First run must read as a start, not a resume.
  const primary = await txt("#module-hub-primary");
  if (/starten|Start/i.test(primary)) ok("first run says start, not resume");
  else fail(`first run primary reads "${primary}"`);

  // 2. The bug class that shipped before: an overlay left inert behind it.
  await page.locator("#module-hub-primary").click();
  await page.waitForTimeout(600);
  if (await page.isVisible("#module-hub")) fail("hub still open after primary action");
  else ok("primary action closes the hub");
  const inert = await page.evaluate(() =>
    [...document.querySelectorAll("[inert]")].map((e) => e.id || e.tagName));
  if (inert.length) fail("left inert: " + inert.join(", ")); else ok("nothing left inert");
  const menuClickable = await page.locator("#menu-btn").evaluate((el) => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return false;
    const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return !!top && (el === top || el.contains(top) || top.contains(el));
  });
  if (menuClickable) ok("app is clickable afterwards"); else fail("app not clickable after hub");

  // 3. Reopen via the module button, then Back. The button lives INSIDE
  // #app-menu - the same container as #lang-select, which is the structure
  // behind this project's worst shipped bug - so a user has to open the
  // menu first, and so does this test. Clicking it while the menu is shut
  // would be testing a control nobody can reach.
  await page.locator("#menu-btn").click();
  await page.waitForTimeout(300);
  if (await page.locator("#module-info-btn").isVisible()) {
    ok("module button reachable once the menu is open");
    await page.locator("#module-info-btn").click();
    await page.waitForTimeout(500);
    if (await page.isVisible("#module-hub")) ok("header button reopens the hub");
    else fail("header button did not reopen the hub");
    await page.goBack();
    await page.waitForTimeout(500);
    if (await page.isVisible("#module-hub")) fail("back did not close the hub");
    else ok("back closes the hub");
    const inert2 = await page.evaluate(() =>
      [...document.querySelectorAll("[inert]")].map((e) => e.id || e.tagName));
    if (inert2.length) fail("inert after back: " + inert2.join(", ")); else ok("nothing inert after back");
  } else fail("#module-info-btn not visible inside an opened menu");
}

if (errors.length) { console.error("  page errors:"); errors.forEach((e) => console.error("   - " + e.slice(0,200))); failures += errors.length; }
await browser.close();
console.log(failures ? `\nFAILURES: ${failures}` : "\nall hub smoke checks passed");
process.exit(failures ? 1 : 0);
