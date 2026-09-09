#!/usr/bin/env node
// fable's check #1, the riskiest assumption in Phase 4: a cold start in a
// language the learner reads, landing page to a lesson section on screen, in
// at most four taps. Everything in 4.1-4.4 is built on it and nothing had
// tested it.
//
// What this CAN measure: the tap count, that each tap has somewhere to go,
// that back-navigation from a lesson reaches the landing page without a dead
// end or a dialog stranded over a dialog, and what is above the fold at
// 390x844.
//
// What it CANNOT measure, and this is the actual risk: whether the derived
// lesson is READABLE. It counts characters; a person has to read them. If it
// is not, fable's fallback is the topic row opening the Übungsquiz with the
// lesson behind an "Erklärung" link.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_cold_start.mjs
import { chromium } from "playwright";
import { existsSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };
const note = m => console.log("  ..  " + m);

const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});
// Greek: a locale with partial content, so the fallback path is exercised too.
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, locale: "el-GR" });
const page = await ctx.newPage();
const errs = []; page.on("pageerror", e => errs.push(String(e)));

let taps = 0;
const tap = async (sel, why) => { await page.click(sel); taps += 1; note(`tap ${taps}: ${why}`); await page.waitForTimeout(900); };

// Cold: no storage, straight off the landing page.
await page.goto(`${SITE}/index.html`, { waitUntil: "networkidle" });
await page.waitForTimeout(700);
await tap('.module-card[href*="exam=fuehrerschein"]', "the Führerschein card on the landing page");
await page.waitForLoadState("networkidle");
if (await page.isVisible("#storage-consent-notice")) {
  await tap("#storage-consent-yes", "the storage-consent notice");
}
await page.waitForTimeout(1500);
if (await page.isVisible("#module-picker")) {
  const scope = page.locator("#module-picker button").first();
  await tap("#module-picker button", `the scope step: "${(await scope.innerText()).trim().slice(0, 30)}"`);
}
await page.waitForTimeout(1200);

const onHub = await page.evaluate(() => !document.querySelector("#module-hub").hidden);
onHub ? ok("landed on the module hub") : fail("did not reach the hub");

// What is above the fold before any scrolling - ADR-app-0002 § 1's order.
const fold = await page.evaluate(() => {
  const vis = sel => { const e = document.querySelector(sel); if (!e) return false;
    const r = e.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight && r.height > 0; };
  return {
    title: vis("#module-hub-title"), chip: vis("#module-hub-chip"),
    primary: vis("#module-hub-primary"), progress: vis("#module-hub-progress"),
    rows: [...document.querySelectorAll("#module-hub-topics .hub-topic-btn")]
      .filter(e => e.getBoundingClientRect().bottom <= window.innerHeight).length,
  };
});
fold.title && fold.chip && fold.primary && fold.progress
  ? ok("above the fold: name, kind, primary button and progress")
  : fail(`above the fold missing: ${JSON.stringify(fold)}`);
fold.rows >= 2 ? ok(`${fold.rows} topic rows visible without scrolling`)
               : fail(`only ${fold.rows} topic row(s) above the fold; the ADR asks for at least 2`);

// The primary must reach a lesson.
await tap("#module-hub-primary", "the hub's primary button");
await page.waitForTimeout(1200);
const lesson = await page.evaluate(() => {
  const r = document.querySelector("#course-reader");
  const body = document.querySelector("#course-reader-body");
  const pv = document.querySelector("#practice-view");
  return { open: r && !r.hidden, title: (document.querySelector("#course-reader-title") || {}).textContent || "",
           chars: (body && body.textContent || "").trim().length,
           quiz: pv && !pv.hidden,
           quizQ: (document.querySelector("#practice-question") || {}).textContent || "",
           cards: document.querySelectorAll("#list div.q-card").length };
});
// A topic can legitimately have no lesson in this locale - `vorfahrt` has two
// authored lessons, both de/en only, and derive_topic_lessons() declines to
// generate a derived one where an authored one exists. The requirement is
// that the learner lands somewhere in THEIR language, not that a lesson
// exists everywhere. A card list is the failure; the Übungsquiz is not.
if (!lesson.open && lesson.quiz) {
  taps <= 4 ? ok(`no lesson in this locale, so the Übungsquiz in ${taps} taps (target ≤ 4)`)
            : fail(`${taps} taps to the quiz; target is 4`);
  /[\u0370-\u03FF]/.test(lesson.quizQ)
    ? ok(`and it really is in Greek: "${lesson.quizQ.slice(0, 46)}…"`)
    : fail(`quiz text is not Greek: "${lesson.quizQ.slice(0, 60)}"`);
  note("This is fable's documented fallback, not a pass on the lesson path.");
} else if (lesson.open) {
  taps <= 4 ? ok(`a lesson section is on screen in ${taps} taps (target ≤ 4)`)
            : fail(`${taps} taps to the first lesson; target is 4`);
  note(`lesson: "${lesson.title.slice(0, 60)}"`);
  lesson.chars > 200 ? ok(`section has ${lesson.chars} characters of body text`)
                     : fail(`section body is only ${lesson.chars} characters`);
  note("READABILITY IS NOT ASSERTED HERE - a person has to read it. This is fable's risk #1.");
} else {
  fail(`after ${taps} taps the learner is in neither a lesson nor a quiz `
     + `(${lesson.cards} cards on screen) - a bare card list is the failure `
     + `Option A exists to remove`);
}

// Back out: lesson -> hub -> picker -> landing, no dead end, no stranded dialog.
const chain = [];
for (let i = 0; i < 5; i++) {
  await page.goBack().catch(() => {});
  await page.waitForTimeout(700);
  const st = await page.evaluate(() => {
    const open = [...document.querySelectorAll(".exam-modal, .detail, .exam-view")]
      .filter(e => !e.hidden).map(e => e.id);
    return { url: location.pathname, open, cards: document.querySelectorAll("#list div.q-card").length };
  });
  chain.push(st.open.length ? st.open.join("+") : (st.url.endsWith("index.html") ? "landing" : `list(${st.cards})`));
  if (st.open.length > 1) fail(`dialog over dialog while going back: ${st.open.join(" + ")}`);
  if (st.url.endsWith("index.html")) break;
}
note(`back chain: ${chain.join(" -> ")}`);
chain[chain.length - 1] === "landing"
  ? ok("back-navigation reaches the landing page")
  : fail(`back-navigation ended at "${chain[chain.length - 1]}", not the landing page`);

if (errs.length) errs.slice(0, 2).forEach(e => fail("page error: " + e.slice(0, 140)));
await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\ncold-start checks passed");
process.exit(f ? 1 : 0);
