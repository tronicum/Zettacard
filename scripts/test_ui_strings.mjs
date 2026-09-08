#!/usr/bin/env node
// Roadmap 3.7: UI strings mastered in zettacard-kb, read from app/data/ui/.
//
// The literals in app.js remain the fallback while this is converted one
// dictionary at a time, so the checks that matter here are the FAILURE modes
// rather than the happy path: a locale the KB has not translated yet must
// fall back rather than render blank, and a missing bundle must leave the app
// exactly as it was. A half-converted dictionary that silently blanks a label
// would be worse than an unconverted one.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_ui_strings.mjs

import { chromium } from "playwright";
import { existsSync } from "node:fs";

const SITE = process.argv[2] || "http://localhost:8802";
let fails = 0;
const ok = (m) => console.log("  ok: " + m);
const fail = (m) => { console.error("  FAIL: " + m); fails++; };

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
  await page.click("#storage-consent-yes"); await page.waitForTimeout(300);
}

// Loaded at BOOT, not only on a language change - the consent notice and the
// first-run picker render before anything else, and a cold start that used
// literals while every later screen used the KB is the kind of inconsistency
// nobody reports.
const boot = await page.evaluate(() => ({
  loaded: !!uiStringsBundle,
  keys: uiStringsBundle ? Object.keys(uiStringsBundle).length : 0,
  args: uiStringsArgs ? Object.keys(uiStringsArgs).length : 0,
}));
if (boot.loaded) ok(`bundle loaded at boot: ${boot.keys} keys, ${boot.args} templated`);
else fail("bundle not loaded at boot");

const de = await page.evaluate(() => {
  const H = hubStrings("de");
  return { topics: H.topics, learned: H.learnedOf(3, 7), next: H.nextLearn("Vorfahrt") };
});
if (de.topics) ok(`plain string from the KB: "${de.topics}"`); else fail("plain string empty");
if (de.learned === "3 von 7 gelernt") ok(`{n}/{total} template resolves: "${de.learned}"`);
else fail(`template wrong: "${de.learned}"`);
if (de.next === "Weiter mit Vorfahrt") ok(`named placeholder resolves: "${de.next}"`);
else fail(`named placeholder wrong: "${de.next}"`);

// A locale the KB carries for other dictionaries but NOT for this one.
const uk = await page.evaluate(async () => {
  await loadUiStrings("uk");
  const H = hubStrings("uk");
  return { topics: H.topics, learned: H.learnedOf(3, 7) };
});
if (uk.topics) ok(`untranslated locale falls back, not blank: "${uk.topics}"`);
else fail("untranslated locale rendered blank");
if (/3.*7/.test(uk.learned)) ok(`fallback template still fills: "${uk.learned}"`);
else fail(`fallback template broke: "${uk.learned}"`);

// No bundle at all: the app must be byte-for-byte what it was before 3.7.
const none = await page.evaluate(() => {
  const saved = uiStringsBundle;
  uiStringsBundle = null;
  const H = hubStrings("de");
  const r = { topics: H.topics, learned: H.learnedOf(3, 7) };
  uiStringsBundle = saved;
  return r;
});
if (none.topics && /3.*7/.test(none.learned)) ok("no bundle -> literals, app unchanged");
else fail("the no-bundle fallback path is broken");

if (errors.length) errors.slice(0, 3).forEach((e) => fail("page error: " + e.slice(0, 140)));
await browser.close();
console.log(fails ? `\nFAILURES: ${fails}` : "\nall ui-strings checks passed");
process.exit(fails ? 1 : 0);
