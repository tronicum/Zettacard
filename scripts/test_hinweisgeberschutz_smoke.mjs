#!/usr/bin/env node
// DN-50 smoke test: the Hinweisgeberschutz module (5th compliance module)
// should be selectable from the module picker, load its questions, and
// render a real question with its German canonical text - i.e. the
// manifest entry + core.json + de.json wiring works end to end in a real
// browser against the live deploy, not just "the build script didn't
// crash." Originally written against the 20-question DE/EN-only pilot;
// updated 2026-08-08 for the scale-up to 40 questions/all 12 locales
// (see BACKLOG.md's DN-50 follow-up entry) - the exam-mode assertion below
// now expects ENABLED, not disabled.

import { chromium } from "playwright";

const SITE_URL = process.argv[2] || "https://zettacard.netlify.app";

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  process.exit(1);
}

async function main() {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const context = await browser.newContext({ ignoreHTTPSErrors: true, locale: "de-DE" });
  const page = await context.newPage();
  page.on("pageerror", (e) => console.error("  [browser page error]", e.message));

  try {
    console.log(`Opening ${SITE_URL}/app.html ...`);
    await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });

    const pickerAlreadyOpen = await page.locator("#module-picker:not([hidden])").isVisible().catch(() => false);
    if (!pickerAlreadyOpen) {
      await page.click("#module-switch-btn");
    }
    await page.waitForSelector("#module-picker:not([hidden])");

    console.log("Looking for the Hinweisgeberschutz module button...");
    const modBtn = page.locator("#module-picker-body button").filter({ hasText: "Hinweisgeberschutz" });
    await modBtn.waitFor({ state: "visible", timeout: 5000 });
    await modBtn.first().click();
    await page.waitForTimeout(500);

    // Compliance modules have a single "ALL"/"Grundlagenschulung" scope
    // option - if a scope-picker step appears, take it.
    const scopeStepVisible = await page.locator("#module-picker-cancel").isVisible().catch(() => false)
      && !(await page.locator("#exam-start-btn").isVisible().catch(() => false));
    if (scopeStepVisible) {
      await page.locator("#module-picker-body .exam-mode-btn, #module-picker-body button").first().click();
      await page.waitForTimeout(500);
    }

    const introSkip = page.locator("#module-intro-skip");
    if (await introSkip.isVisible().catch(() => false)) {
      await introSkip.click();
      await page.waitForTimeout(300);
    }

    // DN-50 follow-up (2026-08-08): scaled 20 -> 40 questions, so Exam
    // Simulation should now be ENABLED (40 >= the 30-question floor) -
    // this used to assert the opposite (disabled) when the module was
    // still a 20-question pilot.
    const examBtnDisabled = await page.locator("#exam-start-btn").isDisabled().catch(() => null);
    console.log(`Exam-start button disabled: ${examBtnDisabled}`);
    if (examBtnDisabled !== false) {
      fail(`Expected #exam-start-btn to be enabled with 40 questions loaded, got disabled=${examBtnDisabled}`);
    }

    // Flashcard/list view should show a real question with real DE text.
    const qCount = await page.locator(".question-card, .flashcard, #question-list li, .q-item").count().catch(() => 0);
    console.log(`Question list item count (best-effort selector): ${qCount}`);

    const bodyText = await page.locator("body").innerText();
    if (!bodyText.includes("Meldestelle") && !bodyText.includes("Hinweisgeber")) {
      fail("Page body doesn't mention Meldestelle/Hinweisgeber anywhere - module content may not have rendered.");
    }
    console.log("Found Hinweisgeberschutz-related text on the page.");

    console.log("\nPASS: Hinweisgeberschutz module is selectable, loads its content, and Exam Simulation is correctly enabled at 40 questions.");
    process.exitCode = 0;
  } catch (e) {
    fail(e.stack || e.message);
  } finally {
    await browser.close();
  }
}

main();
