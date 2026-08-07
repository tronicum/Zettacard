#!/usr/bin/env node
// Automated end-to-end test (DN: mini-exam -> signed badge check).
//
// This is NOT a unit test against sign-credential.js in isolation (see
// test_sign_credential.js for that) - it drives the REAL app UI in a real
// browser exactly like a visitor would: pick a module, start a genuine
// Exam Simulation (not Training mode - only Simulation records completions
// and attempts real signing, see finishExam()/recordCompletion() in
// app/app.js), answer every question CORRECTLY (using the actual
// published content's own answer key, not a stub), and then verifies the
// resulting completion record actually got a real, independently
// cryptographically-verifiable signature - not just an HTTP 200.
//
// Why this exists: a raw curl against /.netlify/functions/sign-credential
// (see docs, or scripts/test_sign_credential.js) only proves the function
// itself works in isolation. It does NOT prove that a real user who opens
// the app, picks a module, and passes a Simulation actually ends up with
// verified:true and a real proof.jwt in their stored completion record -
// that requires the full client flow (recordCompletion -> trySignCompletion
// -> persistCompletionUpdate) to run for real, in a real browser, against
// the real deployed content. This script is the only thing in the repo
// that checks that whole chain end-to-end.
//
// Usage:
//   node scripts/test_full_exam_badge.mjs [siteUrl] [examType]
// Defaults to https://zettacard.netlify.app and "arbeitssicherheit" (the
// shortest/simplest module content-wise, 40 questions / 30-question draw,
// single scope, no class-picker step - fastest reliable module to script).
//
// Exit code 0 = pass (real signed badge confirmed), non-zero = failure,
// with a human-readable reason printed either way.

import { chromium } from "playwright";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

const SITE_URL = process.argv[2] || "https://zettacard.netlify.app";
const EXAM_TYPE = process.argv[3] || "arbeitssicherheit";
const LANG = "de";

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  process.exit(1);
}

async function loadAnswerKey(examType, lang) {
  // Reads the same published content the live app fetches, straight from
  // the repo's own app/data tree - this is the module's real answer key,
  // not a hand-maintained duplicate that could drift out of sync.
  const core = JSON.parse(await readFile(path.join(REPO_ROOT, "app/data", examType, "core.json"), "utf8"));
  const locale = JSON.parse(await readFile(path.join(REPO_ROOT, "app/data", examType, "locales", `${lang}.json`), "utf8"));
  const byQuestionText = new Map();
  core.questions.forEach((q) => {
    const t = locale[q.id];
    if (!t) return;
    byQuestionText.set(t.question, { correct: q.correct, questionType: q.question_type, id: q.id });
  });
  return byQuestionText;
}

async function loadModuleLabel(examType, lang) {
  const manifest = JSON.parse(await readFile(path.join(REPO_ROOT, "data/modules_manifest.json"), "utf8"));
  const mod = manifest.modules.find((m) => m.exam_type === examType);
  if (!mod) fail(`No module "${examType}" found in data/modules_manifest.json.`);
  return mod.label[lang] || mod.label.en;
}

async function main() {
  console.log(`Loading answer key for ${EXAM_TYPE}/${LANG} from local repo content...`);
  const answerKey = await loadAnswerKey(EXAM_TYPE, LANG);
  console.log(`  ${answerKey.size} question/answer pairs loaded.`);
  const MODULE_LABEL = await loadModuleLabel(EXAM_TYPE, LANG);
  console.log(`Module label to match in the picker: "${MODULE_LABEL}"`);

  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  // ignoreHTTPSErrors: this sandbox routes outbound HTTPS through a
  // TLS-intercepting proxy for allow-listed egress; Chromium doesn't trust
  // that proxy's CA the way curl/node's own trust store does, so without
  // this every external request fails with ERR_CERT_AUTHORITY_INVALID
  // (confirmed - curl to the same URL works fine). Not a concern for what
  // this script tests (the JWT signature itself is verified independently
  // below via `jose`, which is the real proof, not just an HTTPS padlock).
  // locale: "de-DE" so detectLang() (app.js) picks German from
  // navigator.language BEFORE the mandatory first-visit module picker ever
  // renders - trying to switch language via #lang-select AFTER that picker
  // is already open doesn't work, because setInertBehindDialog(true) makes
  // the header (including #lang-select) inert while a modal is open.
  const context = await browser.newContext({ ignoreHTTPSErrors: true, locale: "de-DE" });
  const page = await context.newPage();
  page.on("pageerror", (e) => console.error("  [browser page error]", e.message));

  try {
    console.log(`Opening ${SITE_URL}/app.html ...`);
    await page.goto(`${SITE_URL}/app.html`, { waitUntil: "networkidle" });

    // German is already forced via the context's locale (see above) so
    // detectLang() picks it up before the mandatory module picker renders.

    // Module picker: pick the target module (arbeitssicherheit by default).
    // On a first-ever visit (fresh browser profile, no module chosen yet)
    // app.js opens this picker automatically and mandatorily - clicking
    // #module-switch-btn in that case would just hit the picker's own
    // modal overlay. Only click it if the picker isn't already open.
    console.log(`Selecting module: ${EXAM_TYPE} ...`);
    const pickerAlreadyOpen = await page.locator("#module-picker:not([hidden])").isVisible().catch(() => false);
    if (!pickerAlreadyOpen) {
      await page.click("#module-switch-btn");
    }
    await page.waitForSelector("#module-picker:not([hidden])");
    // The module picker has no data-exam-type hooks - it renders plain
    // buttons labelled with each module's localized display name. Match by
    // that label text (loaded from data/modules_manifest.json below).
    await page.locator("#module-picker-body button").filter({ hasText: MODULE_LABEL }).first().click();
    await page.waitForTimeout(500);
    // Some modules have >1 scope option (a second picker step); this
    // script targets single-option modules like arbeitssicherheit by
    // default, but if a scope step appears, just take the first option.
    const scopeStepVisible = await page.locator("#module-picker-cancel").isVisible().catch(() => false)
      && !(await page.locator("#exam-start-btn").isVisible().catch(() => false));
    if (scopeStepVisible) {
      await page.locator("#module-picker-body .exam-mode-btn").first().click();
      await page.waitForTimeout(500);
    }

    // Skip the module-intro carousel if it appears (first-time-per-module UX).
    const introSkip = page.locator("#module-intro-skip");
    if (await introSkip.isVisible().catch(() => false)) {
      await introSkip.click();
      await page.waitForTimeout(300);
    }

    console.log("Starting exam: opening exam picker...");
    await page.click("#exam-start-btn");
    await page.waitForSelector("#exam-picker:not([hidden])");
    console.log("Choosing Simulation mode (required for a certificate/signed badge)...");
    await page.click("#exam-pick-simulation");
    await page.waitForSelector("#exam-view:not([hidden])");

    let answered = 0;
    for (;;) {
      const qText = (await page.locator("#exam-question").textContent()).trim();
      const entry = answerKey.get(qText);
      if (!entry) {
        console.warn(`  [warn] no answer-key match for question text: "${qText.slice(0, 60)}..." - leaving unanswered.`);
      } else {
        const keys = Array.isArray(entry.correct) ? entry.correct : [entry.correct];
        for (const key of keys) {
          await page.locator(`#exam-options .option[data-key="${key}"]`).click();
        }
        answered += 1;
      }
      const nextBtn = page.locator("#exam-next-btn");
      const btnText = (await nextBtn.textContent()).trim();
      await nextBtn.click();
      await page.waitForTimeout(120);
      const resultsVisible = await page.locator("#exam-results:not([hidden])").isVisible().catch(() => false);
      if (resultsVisible) break;
    }
    console.log(`Answered ${answered} question(s). Exam finished.`);

    await page.waitForSelector("#exam-results:not([hidden])");
    const verdictClass = await page.locator("#exam-results-title").getAttribute("class");
    const verdictText = (await page.locator("#exam-results-title").textContent()).trim();
    console.log(`Result: ${verdictText} (${verdictClass})`);
    if (!verdictClass || !verdictClass.includes("pass")) {
      fail(`Exam did not pass (result: "${verdictText}") - cannot check for a signed badge on a failed/no-certificate run.`);
    }

    // Give the background trySignCompletion() fetch (fired from
    // recordCompletion()) a moment to complete against the live function.
    console.log("Waiting for background signing attempt to settle...");
    await page.waitForTimeout(2500);

    const record = await page.evaluate((examType) => {
      const key = Object.keys(localStorage).find((k) => k.endsWith(":completions") || k === "completions" || k.includes("completions"));
      if (!key) return null;
      const all = JSON.parse(localStorage.getItem(key) || "[]");
      const matches = all.filter((r) => r.examType === examType);
      return matches.length ? matches[matches.length - 1] : null;
    }, EXAM_TYPE);

    if (!record) fail("No completion record found in localStorage after passing the exam.");
    console.log(`Completion record id: ${record.id}`);
    console.log(`  verified: ${record.verified}`);
    console.log(`  signedKid: ${record.signedKid}`);

    if (record.verified !== true || !record.signedJwt) {
      fail(`Completion record is NOT signed (verified=${record.verified}). The badge produced by this run is a self-issued/unverified fallback, not a real signed credential.`);
    }

    // Independently verify the JWT's signature against the LIVE published
    // JWKS - this is the actual proof, not just trusting the app's own
    // "verified: true" flag (which the app sets itself and could in
    // principle be wrong even if well-intentioned).
    const { jwtVerify, createRemoteJWKSet } = await import("jose");
    const JWKS = createRemoteJWKSet(new URL(`${SITE_URL}/.well-known/jwks.json`));
    const { payload } = await jwtVerify(record.signedJwt, JWKS, { issuer: SITE_URL });
    console.log("Independent signature verification: PASSED");
    console.log(`  achievement: ${payload.vc.credentialSubject.achievement.name}`);

    console.log("\nPASS: real exam completed, real signed badge issued and independently verified.");
    process.exitCode = 0;
  } catch (e) {
    fail(e.stack || e.message);
  } finally {
    await browser.close();
  }
}

main();
