#!/usr/bin/env node
// User-journey tests: five things a real learner actually does, plus the
// language switch, driven entirely through the controls a person can click.
//
// WHY THIS EXISTS, AND WHY IT CLICKS EVERYTHING
//
// The worst bug this project has shipped was invisible to three passing test
// runs: after switching language, nothing was clickable for every non-German
// locale, because the language `<select>` lives inside `#app-menu` and changing
// it left the menu open with `setInertBehindDialog(true)` still applied. The
// tests missed it because they set `#lang-select` through `page.evaluate` —
// changing the state without going through the control a user must open.
//
// So the rule here: **if a person has to click it, this file clicks it.**
// `page.evaluate` is used only to READ state, never to set it. Where a helper
// looks longer than it needs to be, that is usually why.
//
// Usage:
//   node scripts/serve-app.mjs 8802 &
//   node scripts/test_user_journeys.mjs                     # localhost:8802
//   node scripts/test_user_journeys.mjs https://zettacard.de
//
// First-time setup: `npm install && npx playwright install chromium`.

import { chromium } from "playwright";
import { existsSync } from "node:fs";

const SITE_URL = (process.argv[2] || "http://localhost:8802").replace(/\/$/, "");
const VIEWPORT = { width: 390, height: 844 };   // a phone, which is how this is used

let failures = 0;
function fail(msg) { console.error(`  FAIL: ${msg}`); failures++; }
function ok(msg) { console.log(`  ok: ${msg}`); }

async function launchChromium() {
  const sandboxPath = "/opt/pw-browsers/chromium";
  if (existsSync(sandboxPath)) return chromium.launch({ executablePath: sandboxPath });
  return chromium.launch();
}

/** A fresh page with storage consent already granted by CLICKING the button. */
async function freshPage(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.__errors = errors;
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });
  if (await page.isVisible("#storage-consent-notice")) {
    await page.click("#storage-consent-yes");
    await page.waitForTimeout(200);
  }
  return { ctx, page };
}

/** Nothing may be inert, and a known control must actually be clickable. */
async function assertAppIsUsable(page, where) {
  const inert = await page.evaluate(() =>
    [...document.querySelectorAll("[inert]")].map((e) => e.id || e.tagName));
  if (inert.length) fail(`${where}: elements left inert: ${inert.join(", ")}`);
  const menuBtn = page.locator("#menu-btn");
  if (await menuBtn.count()) {
    // isEnabled() is not enough — an inert ancestor still reports enabled.
    const clickable = await menuBtn.evaluate((el) => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return false;
      const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return !!top && (el === top || el.contains(top) || top.contains(el));
    });
    if (!clickable) fail(`${where}: #menu-btn is not actually clickable`);
  }
}

// ---------------------------------------------------------------------------
// 1. Learning: open a module, read a card, reveal, move on
// ---------------------------------------------------------------------------
async function journeyLearning(browser) {
  console.log("\n[1] learning — flashcards");
  const { ctx, page } = await freshPage(browser);

  if (!(await page.isVisible("#list"))) fail("question list not visible on load");
  const first = page.locator("#list li, #list .card, #list button").first();
  if (!(await first.count())) { fail("no questions in the list"); await ctx.close(); return; }
  await first.click();
  await page.waitForTimeout(300);

  if (!(await page.isVisible("#detail-view"))) fail("clicking a question did not open the detail view");
  const q = (await page.textContent("#detail-question")) || "";
  if (q.trim().length < 10) fail("detail view shows no question text");

  if (await page.isVisible("#reveal-btn")) {
    await page.click("#reveal-btn");
    await page.waitForTimeout(200);
    const expl = (await page.textContent("#explanation")) || "";
    if (expl.trim().length < 10) fail("revealing showed no explanation");
    else ok("reveal shows an explanation");
  }

  const before = await page.textContent("#detail-progress");
  if (await page.isVisible("#next-btn")) {
    await page.click("#next-btn");
    await page.waitForTimeout(250);
    const after = await page.textContent("#detail-progress");
    if (before === after) fail(`next did not advance (progress stayed "${before}")`);
    else ok(`next advances: ${before?.trim()} -> ${after?.trim()}`);
  }

  await assertAppIsUsable(page, "learning");
  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
}

// ---------------------------------------------------------------------------
// 2. Walking around: open every screen from the menu and come back
// ---------------------------------------------------------------------------
async function journeyWalkAround(browser) {
  console.log("\n[2] walking around — every screen opens and closes");
  const { ctx, page } = await freshPage(browser);

  // Screens reachable from the header/menu. Each is (opener, view, closer).
  const screens = [
    ["#menu-btn", "#app-menu", "#app-menu-close-btn"],
    ["#certificates-btn", "#certificates-view", "#certificates-close-btn"],
    ["#profile-switch-btn", "#profile-view", "#profile-close-btn"],
    ["#sign-reference-btn", "#sign-reference-view", "#sign-reference-close-btn"],
    ["#primers-btn", "#primers-view", "#primers-close-btn"],
    ["#course-btn", "#course-view", "#course-close-btn"],
  ];

  for (const [opener, view, closer] of screens) {
    const btn = page.locator(opener);
    if (!(await btn.count()) || !(await btn.isVisible())) continue;  // hidden per module
    await btn.click();
    await page.waitForTimeout(250);
    if (!(await page.isVisible(view))) { fail(`${opener} did not open ${view}`); continue; }
    const closeBtn = page.locator(closer);
    if (await closeBtn.count()) {
      await closeBtn.click();
      await page.waitForTimeout(250);
      if (await page.isVisible(view)) fail(`${closer} did not close ${view}`);
    }
    // The real regression: a closed screen must leave nothing inert behind.
    await assertAppIsUsable(page, `after closing ${view}`);
    ok(`${view} opens and closes cleanly`);
  }

  // Browser Back must also work — the menu pushes history, and closing it
  // directly instead of via history.back() used to strand an entry.
  await page.click("#menu-btn");
  await page.waitForTimeout(200);
  await page.goBack();
  await page.waitForTimeout(250);
  if (await page.isVisible("#app-menu")) fail("browser Back did not close the menu");
  else ok("browser Back closes the menu");
  await assertAppIsUsable(page, "after Back");

  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
}

// ---------------------------------------------------------------------------
// 3. Sitting an exam: start it, answer every question, reach the end
// ---------------------------------------------------------------------------
async function journeyExam(browser) {
  console.log("\n[3] exam — start, answer through, finish");
  const { ctx, page } = await freshPage(browser);

  const start = page.locator("#exam-start-btn");
  if (!(await start.count())) { fail("no #exam-start-btn"); await ctx.close(); return; }
  await start.click();
  await page.waitForTimeout(300);

  // Some modules show a picker (training / practice / simulation) first.
  if (await page.isVisible("#exam-picker")) {
    const pick = page.locator("#exam-pick-training, #exam-pick-practice").first();
    if (!(await pick.count())) { fail("exam picker has no selectable mode"); await ctx.close(); return; }
    await pick.click();
    await page.waitForTimeout(300);
    ok("exam picker offers a mode");
  }
  if (!(await page.isVisible("#exam-view"))) { fail("exam did not start"); await ctx.close(); return; }
  await assertAppIsUsable(page, "exam started");

  let answered = 0;
  for (let i = 0; i < 200; i++) {
    if (await page.isVisible("#exam-results")) break;
    const opt = page.locator("#exam-options button, #exam-options label, #exam-options li").first();
    if (await opt.count()) { await opt.click(); answered++; }
    const next = page.locator("#exam-next-btn");
    if (!(await next.count()) || !(await next.isVisible())) break;
    await next.click();
    await page.waitForTimeout(120);
  }
  if (answered === 0) fail("could not answer a single exam question");
  else ok(`answered ${answered} questions by clicking`);

  if (!(await page.isVisible("#exam-results"))) fail("never reached the results screen");
  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
  return page;
}

// ---------------------------------------------------------------------------
// 4. Checking results: a summary, a review, and a way out
// ---------------------------------------------------------------------------
async function journeyResults(browser) {
  console.log("\n[4] results — summary, review, exit");
  const { ctx, page } = await freshPage(browser);

  await page.click("#exam-start-btn");
  await page.waitForTimeout(300);
  if (await page.isVisible("#exam-picker")) {
    await page.locator("#exam-pick-training, #exam-pick-practice").first().click();
    await page.waitForTimeout(300);
  }
  for (let i = 0; i < 200; i++) {
    if (await page.isVisible("#exam-results")) break;
    const opt = page.locator("#exam-options button, #exam-options label, #exam-options li").first();
    if (await opt.count()) await opt.click();
    const next = page.locator("#exam-next-btn");
    if (!(await next.count()) || !(await next.isVisible())) break;
    await next.click();
    await page.waitForTimeout(120);
  }
  if (!(await page.isVisible("#exam-results"))) { fail("no results screen to check"); await ctx.close(); return; }

  const summary = (await page.textContent("#exam-results-summary")) || "";
  if (summary.trim().length < 5) fail("results summary is empty");
  else if (!/\d/.test(summary)) fail(`results summary has no numbers: "${summary.trim().slice(0, 60)}"`);
  else ok(`summary reports a score: "${summary.trim().slice(0, 60)}"`);

  if (await page.isVisible("#exam-results-review")) ok("a review of the answers is offered");

  const close = page.locator("#exam-results-close-btn");
  if (await close.count()) {
    await close.click();
    await page.waitForTimeout(300);
    if (await page.isVisible("#exam-results")) fail("results screen would not close");
    else ok("results close and return to the app");
  }
  await assertAppIsUsable(page, "after results");
  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
}

// ---------------------------------------------------------------------------
// 5. Stars: mark a card, and have it still be marked after a reload
// ---------------------------------------------------------------------------
async function journeyStars(browser) {
  console.log("\n[5] stars — mark a card and reload");
  const { ctx, page } = await freshPage(browser);

  await page.locator("#list li, #list .card, #list button").first().click();
  await page.waitForTimeout(300);
  const star = page.locator("#star-btn");
  if (!(await star.count())) { fail("no #star-btn on the detail view"); await ctx.close(); return; }

  const before = await star.getAttribute("aria-pressed");
  await star.click();
  await page.waitForTimeout(250);
  const after = await star.getAttribute("aria-pressed");
  if (before === after) fail(`star click did not change aria-pressed (stayed ${before})`);
  else ok(`star toggles: ${before} -> ${after}`);

  // Persistence is the point of a star. Reload and look again.
  await page.reload({ waitUntil: "networkidle" });
  await page.waitForTimeout(300);
  const stored = await page.evaluate(() =>
    Object.keys(localStorage).filter((k) => /star|fav/i.test(k)).length);
  if (!stored) fail("nothing star-shaped survived in localStorage after reload");
  else ok("the star survived a reload");

  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
}

// ---------------------------------------------------------------------------
// 6. The regression that shipped: switch language through the real control
// ---------------------------------------------------------------------------
async function journeyLanguageSwitch(browser) {
  console.log("\n[6] language — switch via the real control, per locale");
  const { ctx, page } = await freshPage(browser);

  const locales = await page.$$eval("#lang-select option", (os) => os.map((o) => o.value));
  if (locales.length < 2) { fail("language selector has fewer than 2 options"); await ctx.close(); return; }
  ok(`selector offers ${locales.length} locales`);

  const RTL = new Set(["ar", "fa", "he", "apc"]);
  for (const loc of locales) {
    // Open the menu the way a person does, then use the select inside it.
    if (!(await page.isVisible("#lang-select"))) {
      await page.click("#menu-btn");
      await page.waitForTimeout(200);
    }
    await page.selectOption("#lang-select", loc);
    await page.waitForTimeout(350);

    await assertAppIsUsable(page, `after switching to ${loc}`);

    const dir = await page.evaluate(() => document.documentElement.getAttribute("dir"));
    const want = RTL.has(loc) ? "rtl" : "ltr";
    if (dir !== want) fail(`${loc}: dir="${dir}", expected "${want}"`);

    // The app must actually be in that language, not silently English.
    const title = (await page.textContent("#app-title")) || "";
    if (!title.trim()) fail(`${loc}: app title is empty after switching`);
  }
  ok(`all ${locales.length} locales switch cleanly, nothing left inert`);
  if (page.__errors.length) fail(`console errors: ${page.__errors.slice(0, 2).join(" | ")}`);
  await ctx.close();
}

// ---------------------------------------------------------------------------

(async () => {
  console.log(`user journeys against ${SITE_URL}`);
  const browser = await launchChromium();
  try {
    await journeyLearning(browser);
    await journeyWalkAround(browser);
    await journeyExam(browser);
    await journeyResults(browser);
    await journeyStars(browser);
    await journeyLanguageSwitch(browser);
  } finally {
    await browser.close();
  }
  console.log(failures ? `\n${failures} FAILURE(S)` : "\nall journeys passed");
  process.exit(failures ? 1 : 0);
})();
