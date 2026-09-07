#!/usr/bin/env node
// Roadmap 3.2: the per-topic traffic light and the one derived next action.
//
// Two halves, deliberately:
//
//  1. topicTrafficState() and hubNextAction() are PURE - counts in, verdict
//     out - so they are unit-tested against synthetic input. Calling a pure
//     function through page.evaluate is reading, not driving: it sets no UI
//     state, which is the line test_user_journeys.mjs draws.
//  2. Everything downstream of them is checked by CLICKING, same rule as
//     every other suite here: a light that renders only in a unit test is a
//     light nobody sees.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_traffic_light.mjs

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

/**
 * Click the first match at a point we have CHECKED is hittable.
 *
 * Not force:true, which would paper over a control a person cannot reach.
 * The exam view is a scrolling dialog under a sticky header: the option is
 * genuinely on screen and elementFromPoint lands inside it, but Playwright's
 * own scroll-into-view slides it under that header and then refuses. So we
 * verify hittability the way assertAppIsUsable() does, and click the point
 * that passed. If the check fails, so does the test - as it should.
 */
async function hittablePoint(page, selector) {
  return page.evaluate((sel) => {
    const elem = document.querySelector(sel);
    if (!elem) return null;
    const r = elem.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const top = document.elementFromPoint(x, y);
    return { x, y, hit: !!(top && (elem === top || elem.contains(top))) };
  }, selector);
}

async function clickHittable(page, selector, label) {
  let box = await hittablePoint(page, selector);
  if (!box) { fail(`${label}: ${selector} has no box`); return false; }
  if (!box.hit) {
    // Not reachable where it stands - scroll to it, as a person would, and
    // check again. At 390x844 the exam's #exam-next-btn starts 6px inside the
    // fold and drops below it the moment an option is selected, so this path
    // is taken on every question. Reported to the PO as a layout finding
    // rather than worked around in the app.
    await page.evaluate((sel) =>
      document.querySelector(sel).scrollIntoView({ block: "center" }), selector);
    await page.waitForTimeout(150);
    box = await hittablePoint(page, selector);
    if (!box || !box.hit) { fail(`${label}: ${selector} unreachable even after scrolling`); return false; }
  }
  await page.mouse.click(box.x, box.y);
  return true;
}

const browser = await launchChromium();
const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));

await page.goto(`${SITE}/app.html`, { waitUntil: "networkidle" });
if (await page.isVisible("#storage-consent-notice")) {
  await page.click("#storage-consent-yes"); await page.waitForTimeout(200);
}

// ---- 1. the classifier, against synthetic counts -------------------------
const CASES = [
  // [total, learned, seen, due] -> expected
  [[40, 0, 0, 0], "grey",   "untouched topic"],
  [[40, 0, 3, 0], "red",    "seen a few, learned none"],
  [[40, 20, 30, 0], "yellow", "half learned"],
  [[40, 36, 40, 0], "green",  "90% learned, nothing due"],
  [[40, 36, 40, 5], "yellow", "90% learned but overdue - not green"],
  [[40, 4, 40, 9], "red",     "overdue and barely learned"],
  [[0, 0, 0, 0],   "grey",    "empty topic never claims progress"],
];
const got = await page.evaluate((cases) =>
  cases.map(([[total, learned, seen, due]]) => topicTrafficState({ total, learned, seen, due })),
  CASES);
CASES.forEach(([, expected, name], i) => {
  if (got[i] === expected) ok(`${name} -> ${expected}`);
  else fail(`${name}: expected ${expected}, got ${got[i]}`);
});

// ---- 2. the next action, against synthetic rows --------------------------
const NEXT = await page.evaluate(() => {
  const row = (code, state) => ({ code, label: code, state });
  return {
    dueWins: hubNextAction([row("a", "grey")], 7).kind,
    firstNotGreen: hubNextAction([row("a", "green"), row("b", "red"), row("c", "red")], 0).topic.code,
    allGreen: hubNextAction([row("a", "green"), row("b", "green")], 0).kind,
  };
});
if (NEXT.dueWins === "review") ok("overdue cards outrank new material");
else fail(`due should win, got ${NEXT.dueWins}`);
if (NEXT.firstNotGreen === "b") ok("picks the FIRST non-green topic, honouring syllabus order");
else fail(`expected topic b, got ${NEXT.firstNotGreen}`);
if (NEXT.allGreen === "simulate") ok("all green -> the run");
else fail(`all green should simulate, got ${NEXT.allGreen}`);

// ---- 3. it actually renders, and moves when a learner studies ------------
await page.locator('[data-exam-type="fuehrerschein"]').first().click();
await page.waitForTimeout(400);
let scope = page.locator("#module-picker [data-scope-code]");
if (!(await scope.count())) scope = page.locator("#module-picker-body button");
await scope.first().click();
await page.waitForTimeout(2000);

if (!(await page.isVisible("#module-hub"))) fail("hub did not open");
const lights = await page.locator("#module-hub-topics [data-topic-state]").count();
if (lights > 0) ok(`${lights} topic rows carry a state`);
else fail("no topic row carries a state");

const allGrey = await page.locator('#module-hub-topics [data-topic-state="grey"]').count();
if (allGrey === lights) ok("a fresh profile is grey everywhere, not falsely green");
else fail(`${lights - allGrey} rows are not grey on a fresh profile`);

const nextText = (await page.locator("#module-hub-next").innerText()).trim();
const nextKind = await page.locator("#module-hub-next").getAttribute("data-next-kind");
if (nextText && nextKind === "learn") ok(`next action: "${nextText}"`);
else fail(`next action wrong on a fresh profile: "${nextText}" (${nextKind})`);

// Every row must SAY its state, not only colour it.
const firstNote = (await page.locator("#module-hub-topics .module-row-note").first().innerText()).trim();
if (/not started|noch nicht/i.test(firstNote)) ok(`state is stated in words: "${firstNote}"`);
else fail(`row note does not state the status in words: "${firstNote}"`);

// Now study, by clicking what a learner clicks, and watch a light move.
// A TRAINING run is the only self-assessment path open to a fresh profile:
// the flashcard "I knew it" control lives in review mode, which needs cards
// already due. Right or wrong does not matter here - either answer writes an
// SRS entry, which is what takes a topic off grey.
await page.locator("#module-hub-training").click();
await page.waitForTimeout(900);
// The run has to be FINISHED, not merely started: feedExamResultsIntoSrs()
// is called from finishExam(), so a run the learner walks out of writes no
// boxes at all - which is right (an abandoned run is not evidence) and means
// this loop must answer every question, not a sample of them.
let answered = 0;
for (let i = 0; i < 40; i++) {
  if (!(await page.isVisible("#exam-view"))) break;
  // The options are div.option[data-key] with role="button", not <button>
  // elements - a "button, label, input" selector matches none of them, which
  // is why this and test_user_journeys.mjs both said "could not answer a
  // single exam question".
  if (!(await page.locator("#exam-options .option").count())) break;
  if (!(await clickHittable(page, "#exam-options .option", `question ${i + 1}`))) break;
  await page.waitForTimeout(150);
  if (!(await clickHittable(page, "#exam-next-btn", `next after question ${i + 1}`))) break;
  answered++;
  await page.waitForTimeout(250);
}
if (answered === 0) fail("could not answer a single training question");
else {
  ok(`answered ${answered} training questions`);
  if (await page.isVisible("#exam-view")) fail(`run did not finish after ${answered} answers`);
  else ok("the training run finished");
  // Getting back to the hub by RELOADING rather than by unwinding the exam
  // view. Two reasons: exiting a run mid-way leaves the exam dialog's inert
  // state in place long enough that #menu-btn is genuinely unreachable, and
  // a reload additionally proves the SRS writes survived - a traffic light
  // that resets on reload would be worse than none.
  await page.reload({ waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  if (await page.isVisible("#storage-consent-notice")) {
    await page.click("#storage-consent-yes"); await page.waitForTimeout(300);
  }
  if (await page.isVisible("#module-hub")) {
    ok("a returning learner lands on the hub");
  } else {
    await clickHittable(page, "#menu-btn", "open the menu");
    await page.waitForTimeout(400);
    await clickHittable(page, "#module-info-btn", "reopen the hub");
    await page.waitForTimeout(900);
  }
  const stillGrey = await page.locator('#module-hub-topics [data-topic-state="grey"]').count();
  if (stillGrey < lights) ok(`a light moved off grey (${lights} grey -> ${stillGrey})`);
  else fail(`answered ${answered} questions and all ${lights} topics are still grey`);
}

if (errors.length) errors.slice(0, 3).forEach((e) => fail("page error: " + e.slice(0, 160)));
await browser.close();
console.log(failures ? `\nFAILURES: ${failures}` : "\nall traffic-light checks passed");
process.exit(failures ? 1 : 0);
