#!/usr/bin/env node
// DN-89 regression test: the storage-consent notice (app/app.js's
// STORAGE_CONSENT_KEY gate + app/app.html's #storage-consent-notice
// markup) must behave as a REAL gate, not a dismissible banner - see
// BACKLOG.md's DN-89 card for the full design rationale and history
// (including a wipeAppStorage() bug this exact test caught during
// development, before it ever shipped).
//
// Defaults to a local dev server (see scripts/dev-serve.sh) so it can be
// run before anything is deployed; pass a URL to run it against a real
// deploy instead, same convention as the other scripts/test_*.mjs files.
//
// Usage:
//   scripts/dev-serve.sh &                                   # in one terminal
//   node scripts/test_storage_consent.mjs                    # localhost:8080
//   node scripts/test_storage_consent.mjs https://zettacard-staging.netlify.app
//
// First-time setup (Playwright's browser binary isn't committed to the
// repo): `npm install && npx playwright install chromium`.

import { chromium } from "playwright";
import { existsSync } from "node:fs";

const SITE_URL = (process.argv[2] || "http://localhost:8080").replace(/\/$/, "");
const VIEWPORT = { width: 390, height: 844 };

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  process.exitCode = 1;
}

async function launchChromium() {
  // The cloud sandbox this feature was originally built in pins Playwright
  // to a fixed /opt/pw-browsers/chromium path; a real dev machine instead
  // has its own managed install (`npx playwright install chromium`). Only
  // use the sandbox path if it actually exists, so this script also just
  // works unmodified on a normal laptop.
  const sandboxPath = "/opt/pw-browsers/chromium";
  if (existsSync(sandboxPath)) return chromium.launch({ executablePath: sandboxPath });
  return chromium.launch();
}

async function scenario1FreshVisitYes(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });

  if (!(await page.isVisible("#storage-consent-notice"))) {
    fail("[1] consent notice did not show on a fresh visit");
  }

  await page.click("#storage-consent-yes");
  await page.waitForTimeout(300);

  const consent = await page.evaluate(() => localStorage.getItem("zc-storage-consent"));
  if (consent !== "granted") fail(`[1] expected consent=granted after Yes, got ${consent}`);
  if (await page.isVisible("#storage-consent-notice")) fail("[1] notice still visible after Yes click");

  // prove persistence actually works now: a write should survive a reload
  await page.evaluate(() => localStorage.setItem("dn-smoke-check", "1"));
  await page.reload({ waitUntil: "networkidle" });
  const survived = await page.evaluate(() => localStorage.getItem("dn-smoke-check"));
  if (survived !== "1") fail("[1] a write made after granting did not survive a reload");

  console.log("[1] fresh visit + Yes: OK (granted, notice dismissed, writes persist)");
  await ctx.close();
}

async function scenario2FreshVisitNo(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  // Seed data as if this were a returning implied-consent-era visitor,
  // BEFORE app.js ever runs, so wipeAppStorage() has something real to wipe.
  await page.addInitScript(() => {
    localStorage.setItem("dn-lang", "en");
    localStorage.setItem("dn-completions-seed-test", "1");
  });
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });

  await page.click("#storage-consent-no");
  await page.waitForTimeout(300);

  const consent = await page.evaluate(() => localStorage.getItem("zc-storage-consent"));
  if (consent !== "declined") fail(`[2] expected consent=declined after No, got ${consent}`);

  const remaining = await page.evaluate(() => Object.keys(localStorage));
  const leaked = remaining.filter((k) => k !== "zc-storage-consent");
  if (leaked.length) fail(`[2] decline did not wipe pre-existing keys: ${leaked.join(", ")}`);

  await page.reload({ waitUntil: "networkidle" });
  const stillDeclined = await page.evaluate(() => localStorage.getItem("zc-storage-consent"));
  if (stillDeclined !== "declined") fail("[2] decline did not persist across reload");
  if (await page.isVisible("#storage-consent-notice")) fail("[2] notice reappeared for a visitor who already declined");

  console.log("[2] fresh visit + No: OK (declined, pre-existing keys wiped, decision persists)");
  await ctx.close();
}

async function scenario3AutoDecline(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });
  await page.waitForTimeout(10_500); // the notice's own 10s auto-decline timer

  const consent = await page.evaluate(() => localStorage.getItem("zc-storage-consent"));
  if (consent !== "declined") fail(`[3] expected auto-decline after 10s of silence, got ${consent}`);
  if (await page.isVisible("#storage-consent-notice")) fail("[3] notice still visible after auto-decline fired");

  console.log("[3] 10s silence: OK (auto-declined, notice faded)");
  await ctx.close();
}

async function scenario4ReturningGranted(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });
  await page.click("#storage-consent-yes");
  await page.waitForTimeout(300);

  await page.reload({ waitUntil: "networkidle" });
  if (await page.isVisible("#storage-consent-notice")) {
    fail("[4] notice reappeared for a returning visitor who already granted");
  } else {
    console.log("[4] returning visit after Yes: OK (notice never comes back)");
  }
  await ctx.close();
}

async function scenario5ReturningDeclined(browser) {
  const ctx = await browser.newContext({ viewport: VIEWPORT });
  const page = await ctx.newPage();
  await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });
  await page.click("#storage-consent-no");
  await page.waitForTimeout(300);

  await page.reload({ waitUntil: "networkidle" });
  if (await page.isVisible("#storage-consent-notice")) {
    fail("[5] notice reappeared for a returning visitor who already declined");
  } else {
    console.log("[5] returning visit after No: OK (notice never comes back)");
  }
  await ctx.close();
}

async function main() {
  console.log(`Testing storage consent (DN-89) against ${SITE_URL} ...`);
  const browser = await launchChromium();
  try {
    await scenario1FreshVisitYes(browser);
    await scenario2FreshVisitNo(browser);
    await scenario4ReturningGranted(browser);
    await scenario5ReturningDeclined(browser);
    await scenario3AutoDecline(browser); // slowest (~10s) - run last
  } finally {
    await browser.close();
  }
  if (process.exitCode) {
    console.error("\nOne or more storage-consent scenarios FAILED - see above.");
  } else {
    console.log("\nAll storage-consent scenarios passed.");
  }
}

main();
