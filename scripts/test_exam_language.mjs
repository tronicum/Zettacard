#!/usr/bin/env node
// ADR-app-0002 § 5: there is a third language, and it decides whether a
// Prüfungssimulation is telling the truth.
//
// The app has always had two — the UI's 18 locales and a module's study
// locales — and conflated them with a third that was decided and never built:
// the languages the REAL exam may be sat in. A Greek speaker studies the
// Führerschein in Greek and sits the Theorieprüfung in German or English.
// Until now the app ran a "simulation" in Greek, which rehearses a situation
// that cannot happen and is the one thing a simulation must not do.
//
// So these assertions are about honesty, not about a dialog appearing: the
// question is asked only where it arises, the run really is in the chosen
// language, every card says so, the answer is remembered, and a module whose
// exam languages nobody has established claims nothing.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_exam_language.mjs
import { chromium } from "playwright";
import { existsSync, readFileSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };

const mods = JSON.parse(readFileSync("app/data/modules.json", "utf8")).modules;
const forType = t => mods.find(m => m.exam_type === t) || {};

// 0. the manifest itself
const fs_ = forType("fuehrerschein").examLanguages;
Array.isArray(fs_) && fs_.includes("de") && !fs_.includes("el")
  ? ok(`fuehrerschein exam languages: ${fs_.length}, German in, Greek out`)
  : fail(`examLanguages is ${JSON.stringify(fs_)}`);
forType("angelschein").examLanguages === null
  ? ok("angelschein claims nothing (unestablished, not 'German only')")
  : fail(`angelschein asserts ${JSON.stringify(forType("angelschein").examLanguages)}`);
mods.filter(m => m.kind !== "licence" && m.examLanguages != null).length === 0
  ? ok("no non-licence module claims an exam language") : fail("a non-licence module has examLanguages");

const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, locale: "el-GR" });
const page = await ctx.newPage();
const errs = []; page.on("pageerror", e => errs.push(String(e)));
await page.goto(`${SITE}/app.html?exam=fuehrerschein&scope=B`, { waitUntil: "networkidle" });
if (await page.isVisible("#storage-consent-notice")) { await page.click("#storage-consent-yes"); }
await page.waitForTimeout(1800);
await page.evaluate(() => { state.lang = "el"; try { closeModuleHub(); } catch (e) {} });
await page.waitForTimeout(400);

// 1. the question arises for a Greek learner, and not for a German one
let needed = await page.evaluate(() => examLangNeeded("fuehrerschein"));
needed && !needed.includes("el") ? ok(`Greek learner is asked; options: ${needed.join(", ")}`)
                                 : fail(`examLangNeeded returned ${JSON.stringify(needed)}`);
needed = await page.evaluate(() => { state.lang = "de"; return examLangNeeded("fuehrerschein"); });
needed === null ? ok("a German learner is not asked a question that has one answer")
                : fail(`German learner asked: ${JSON.stringify(needed)}`);
await page.evaluate(() => { state.lang = "el"; });

// 2. only the simulation is bound; Training is study
await page.evaluate(() => { state.exam = null; });
await page.evaluate(() => startExam("training"));
await page.waitForTimeout(900);
let st = await page.evaluate(() => ({ sheet: !document.querySelector("#exam-lang-sheet").hidden, lang: state.exam && state.exam.lang }));
!st.sheet && !st.lang ? ok("Training runs in the study language, unasked") : fail("Training asked for an exam language");
await page.evaluate(() => { state.exam = null; document.querySelector("#exam-view").hidden = true; });

// 3. the simulation asks, and the sheet offers only servable exam languages
const started = page.evaluate(() => startExam("simulation"));
await page.waitForTimeout(700);
const sheet = await page.evaluate(() => ({
  open: !document.querySelector("#exam-lang-sheet").hidden,
  desc: document.querySelector("#exam-lang-desc").textContent,
  langs: [...document.querySelectorAll("#exam-lang-list button")].map(e => e.dataset.lang),
}));
sheet.open ? ok("the simulation asks") : fail("no sheet");
sheet.langs.length && !sheet.langs.includes("el")
  ? ok(`offers ${sheet.langs.join(", ")} — never the language the exam is not in`)
  : fail(`offered ${JSON.stringify(sheet.langs)}`);
/Ελλην|Greek/.test(sheet.desc) ? ok("the explanation names the learner's own language")
                               : fail(`desc: ${sheet.desc}`);

// 4. choosing German really runs the exam in German
await page.click('#exam-lang-list button[data-lang="de"]');
await started;
await page.waitForTimeout(1200);
const run = await page.evaluate(() => ({
  lang: state.exam && state.exam.lang,
  view: !document.querySelector("#exam-view").hidden,
  q: document.querySelector("#exam-question").textContent,
  badge: (document.querySelector("#exam-lang-badge") || {}).textContent || "",
}));
run.view && run.lang === "de" ? ok("the run is in German") : fail(`view=${run.view} lang=${run.lang}`);
/[a-zA-ZäöüßÄÖÜ]/.test(run.q) && !/[Ͱ-Ͽ]/.test(run.q)
  ? ok(`the question really is German, not Greek: "${run.q.slice(0, 52)}…"`)
  : fail(`question text: ${run.q.slice(0, 80)}`);
// %20 in this string means the global escape() was used instead of the app's
// escapeHtml() - a real bug the first run of this test caught.
run.badge && !/%\d\d/.test(run.badge)
  ? ok(`every card says so: "${run.badge}"`)
  : fail(`per-card marker missing or URL-escaped: "${run.badge}"`);

// 5. the answer is remembered, so it is asked once and not every run
const remembered = await page.evaluate(() => storedExamLang("fuehrerschein"));
remembered === "de" ? ok("the choice is remembered") : fail(`stored ${remembered}`);
await page.evaluate(() => { state.exam = null; document.querySelector("#exam-view").hidden = true; });
await page.evaluate(() => startExam("simulation"));
await page.waitForTimeout(1200);
const second = await page.evaluate(() => ({
  sheet: !document.querySelector("#exam-lang-sheet").hidden,
  lang: state.exam && state.exam.lang,
}));
!second.sheet && second.lang === "de" ? ok("the second run does not ask again") : fail(`sheet=${second.sheet} lang=${second.lang}`);

if (errs.length) errs.slice(0, 2).forEach(e => fail("page error: " + e.slice(0, 140)));
await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\nexam-language checks passed");
process.exit(f ? 1 : 0);
