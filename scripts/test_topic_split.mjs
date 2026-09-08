#!/usr/bin/env node
// Roadmap 3.3: `verkehrszeichen` split by sign shape.
//
// Three things this has to get right, and each has a way of failing quietly:
//  1. The five new topic codes render TRANSLATED labels. They carry no
//     strings of their own (they borrow SIGN_CATEGORY_LABELS via
//     getTopicLabel's signCategory marker), so the failure mode is a chip
//     reading "zeichen_gefahr" — which anhaenger_be actually shipped once.
//  2. Each chip filters to the count build_modules.py derived.
//  3. `verkehrszeichen` still works as a FILTER even though no question
//     carries it any more, because the seven sign primers hand off to it.
//     If the umbrella breaks, "practise this topic now" silently shows an
//     empty list.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_topic_split.mjs

import { chromium } from "playwright";
import { existsSync } from "node:fs";

const SITE = process.argv[2] || "http://localhost:8802";
let failures = 0;
const fail = (m) => { console.error("  FAIL: " + m); failures++; };
const ok = (m) => console.log("  ok: " + m);

const EXPECTED = {
  zeichen_richt: 48, zeichen_verbot: 29, zeichen_gefahr: 26,
  zeichen_sonstige: 24, zeichen_gebot: 11,
};
const UMBRELLA_TOTAL = Object.values(EXPECTED).reduce((a, b) => a + b, 0);

async function launchChromium() {
  const p = "/opt/pw-browsers/chromium";
  return existsSync(p) ? chromium.launch({ executablePath: p }) : chromium.launch();
}

const browser = await launchChromium();
const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));

await page.goto(`${SITE}/app.html`, { waitUntil: "networkidle" });
if (await page.isVisible("#storage-consent-notice")) {
  await page.click("#storage-consent-yes"); await page.waitForTimeout(200);
}
await page.locator('[data-exam-type="fuehrerschein"]').first().click();
await page.waitForTimeout(400);
let scope = page.locator("#module-picker [data-scope-code]");
if (!(await scope.count())) scope = page.locator("#module-picker-body button");
await scope.first().click();
await page.waitForTimeout(2000);
if (await page.isVisible("#module-hub")) {
  await page.locator("#module-hub-primary").click();
  await page.waitForTimeout(700);
}

// 1 + 2: every new topic is a chip, reads as words, and filters correctly.
for (const [code, expected] of Object.entries(EXPECTED)) {
  const chip = page.locator(`#filters button[data-topic="${code}"], #filters [data-topic="${code}"]`);
  if (!(await chip.count())) { fail(`no filter chip for ${code}`); continue; }
  const label = (await chip.first().innerText()).trim();
  if (!label || label === code) fail(`${code} chip shows the raw code, not a label`);
  else ok(`${code} -> "${label}"`);
  await chip.first().click();
  await page.waitForTimeout(400);
  const n = await page.locator("#list .q-card").count();
  if (n === expected) ok(`  filters to ${n} questions`);
  else fail(`${code} filtered to ${n}, expected ${expected}`);
}

// The old umbrella must be gone from the chip row...
const oldChip = page.locator('#filters [data-topic="verkehrszeichen"]');
if (await oldChip.count()) fail("verkehrszeichen is still a filter chip");
else ok("verkehrszeichen is no longer a chip");

// ...but must still work as a filter, which is what the primers hand off to.
const n = await page.evaluate(() => {
  state.topicFilter = "verkehrszeichen";
  render();
  return document.querySelectorAll("#list .q-card").length;
});
if (n === UMBRELLA_TOTAL) ok(`verkehrszeichen umbrella still selects all ${n}`);
else fail(`verkehrszeichen umbrella selected ${n}, expected ${UMBRELLA_TOTAL}`);

// The umbrella is not a chip, but it IS a heading over the seven sign
// primers. A label-less umbrella renders the raw code there - the exact way
// anhaenger_be shipped broken once.
const primerLabels = await page.evaluate(() =>
  ["verkehrszeichen", "vorfahrt", "shape_category"].map((c) => [c, primerTopicLabel(c, "de")]));
for (const [code, label] of primerLabels) {
  if (!label || label === code) fail(`primer heading for ${code} shows the raw code`);
  else ok(`primer heading ${code} -> "${label}"`);
}

if (errors.length) { errors.slice(0,3).forEach((e) => fail("page error: " + e.slice(0,160))); }
await browser.close();
console.log(failures ? `\nFAILURES: ${failures}` : "\nall topic-split checks passed");
process.exit(failures ? 1 : 0);
