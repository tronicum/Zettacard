#!/usr/bin/env node
// Roadmap 3.4: derived topic lessons.
//
// The point of 3.4 is a lesson a learner can READ IN THEIR OWN LANGUAGE. The
// old course had prose in de/en covering one of Fuehrerschein's topics, while
// its questions exist in 18 locales - so the test that matters is not "a
// lesson renders", it is "a lesson renders in Arabic". Hence the locale loop.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_derived_lessons.mjs

import { chromium } from "playwright";
import { existsSync } from "node:fs";

const SITE = process.argv[2] || "http://localhost:8802";
let failures = 0;
const fail = (m) => { console.error("  FAIL: " + m); failures++; };
const ok = (m) => console.log("  ok: " + m);

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
  await page.locator("#module-hub-primary").click(); await page.waitForTimeout(700);
}

// The course button lives in the menu, like every other screen's opener.
await page.locator("#menu-btn").click(); await page.waitForTimeout(300);
if (!(await page.locator("#course-btn").isVisible())) { fail("#course-btn not in the menu"); }
else {
  await page.locator("#course-btn").click();
  await page.waitForTimeout(1200);
  if (!(await page.isVisible("#course-view"))) fail("course view did not open");

  const lessons = await page.locator("#course-view [data-lesson-id]").count();
  if (lessons >= 15) ok(`${lessons} lessons listed (3 authored + derived)`);
  else fail(`only ${lessons} lessons listed, expected 15+`);

  // Every lesson must show a NAME. A derived lesson carries no title object -
  // it borrows the topic label - so a regression here shows up as a raw id
  // like "fuehrerschein-derived-zeichen_verbot" on screen.
  const titles = await page.locator("#course-view [data-lesson-id] strong").allInnerTexts();
  const rawIds = titles.filter((t) => /derived|^[a-z0-9_-]+$/.test(t.trim()) && t.includes("-"));
  if (rawIds.length === 0) ok("no lesson shows a raw id as its title");
  else fail(`${rawIds.length} lessons show a raw id: ${rawIds.slice(0, 3).join(", ")}`);

  const derived = page.locator('[data-lesson-id^="fuehrerschein-derived-"]');
  const n = await derived.count();
  if (n >= 14) ok(`${n} derived lessons present`);
  else fail(`only ${n} derived lessons`);

  // ...and one of them must actually open and have readable text.
  await derived.first().click();
  await page.waitForTimeout(900);
  if (!(await page.isVisible("#course-reader"))) fail("a derived lesson did not open");
  else {
    const title = (await page.locator("#course-reader-title").innerText()).trim();
    const body = (await page.locator("#course-reader-body").innerText()).trim();
    if (title && !title.includes("-derived-")) ok(`derived lesson titled "${title}"`);
    else fail(`derived lesson title is a raw id: "${title}"`);
    if (body.length > 80) ok(`worked example reads (${body.length} chars)`);
    else fail(`worked example body too short: "${body.slice(0, 60)}"`);
  }
}

// THE POINT OF 3.4: the same lesson, in languages the old prose never had.
for (const lang of ["ar", "uk", "fa"]) {
  const text = await page.evaluate(async (loc) => {
    const res = await fetch(`data/fuehrerschein/course_locales/${loc}.json`);
    const bundle = await res.json();
    const key = Object.keys(bundle).find((k) => k.startsWith("fuehrerschein-derived"));
    return key ? (bundle[key].body || "") : "";
  }, lang);
  if (text.length > 80) ok(`${lang}: derived lesson text present (${text.length} chars)`);
  else fail(`${lang}: derived lesson has no usable text`);
}

if (errors.length) errors.slice(0, 3).forEach((e) => fail("page error: " + e.slice(0, 160)));
await browser.close();
console.log(failures ? `\nFAILURES: ${failures}` : "\nall derived-lesson checks passed");
process.exit(failures ? 1 : 0);
