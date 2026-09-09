#!/usr/bin/env node
// Automated accessibility checks.
//
// WHAT THIS CANNOT DO, stated first so nobody reads a green run as a claim of
// accessibility: automated tooling catches a minority of WCAG failures -
// commonly put at 30-40%. It finds missing alt text, unlabelled controls and
// contrast failures. It cannot tell whether alt text is USEFUL, whether the
// reading order makes sense, or whether a learner using a screen reader can
// actually get through a Prüfungssimulation. Those need a person.
//
// So this file has two layers. The first is axe-core over the app's real
// views. The second is the checks axe cannot make because they are about THIS
// app's own semantics - the traffic light, the modal stack, and the language
// of parts, which is the one WCAG rule this product breaks by construction:
// a Greek learner sitting a German exam gets German text inside a page
// declared lang="el", so every word is read with a Greek voice.
//
// Usage: node scripts/serve-app.mjs 8802 & node scripts/test_accessibility.mjs
import { chromium } from "playwright";
import { existsSync, readFileSync } from "node:fs";
const SITE = process.argv[2] || "http://localhost:8802";
let f = 0; const ok = m => console.log("  ok: " + m); const fail = m => { console.error("  FAIL: " + m); f++; };
const note = m => console.log("  ..  " + m);

const AXE = readFileSync("node_modules/axe-core/axe.min.js", "utf8");
const b = await chromium.launch(existsSync("/opt/pw-browsers/chromium") ? { executablePath: "/opt/pw-browsers/chromium" } : {});

async function page(url, lang = "de-DE") {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, locale: lang });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: "networkidle" });
  if (await p.isVisible("#storage-consent-notice")) await p.click("#storage-consent-yes");
  await p.waitForTimeout(1800);
  return { ctx, p };
}
async function axeScan(p, label) {
  await p.addScriptTag({ content: AXE });
  const r = await p.evaluate(async () => await window.axe.run(document, {
    resultTypes: ["violations"],
    runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] },
  }));
  const v = r.violations.filter(x => x.nodes.length);
  if (!v.length) { ok(`axe: ${label} — no violations`); return 0; }
  fail(`axe: ${label} — ${v.length} rule(s) violated`);
  v.sort((a, c) => c.nodes.length - a.nodes.length).forEach(x =>
    console.error(`        ${x.impact.padEnd(8)} ${x.id} (${x.nodes.length}) — ${x.help}`));
  return v.length;
}

// ---------- layer 1: axe over the real views ----------
let { ctx, p } = await page(`${SITE}/index.html`);
await axeScan(p, "landing page");
await ctx.close();

({ ctx, p } = await page(`${SITE}/app.html?exam=fuehrerschein&scope=B`));
await axeScan(p, "module hub");
await p.evaluate(() => { try { closeModuleHub(); } catch (e) {} });
await p.waitForTimeout(500);
await axeScan(p, "question list");
await p.locator("#list .q-card").first().click();
await p.waitForTimeout(600);
await axeScan(p, "card detail");

// ---------- layer 2: what axe cannot see ----------

// 2a. The traffic light must not be colour alone (WCAG 1.4.1).
await p.goBack(); await p.waitForTimeout(400);
await p.evaluate(() => openModuleHub());
await p.waitForTimeout(900);
const light = await p.evaluate(() => {
  const rows = [...document.querySelectorAll("#module-hub-topics .hub-topic-btn")];
  return { n: rows.length, labelled: rows.filter(r => (r.getAttribute("aria-label") || "").length > 4).length };
});
light.n && light.labelled === light.n
  ? ok(`traffic light: all ${light.n} topic rows name their state in words, not only colour`)
  : fail(`${light.n - light.labelled} of ${light.n} topic rows signal state by colour alone`);

// 2b. Opening a dialog must move focus into it, and closing must not strand it.
const focusIn = await p.evaluate(() => {
  const hub = document.querySelector("#module-hub");
  return hub.contains(document.activeElement);
});
focusIn ? ok("opening the hub moves focus into it") : fail("focus stayed outside the opened dialog");
const inertOk = await p.evaluate(() => ({
  header: document.querySelector("header").inert === true,
  main: document.querySelector("main").inert === true,
}));
inertOk.header && inertOk.main
  ? ok("background is inert while a dialog is open")
  : fail(`background reachable behind the dialog: ${JSON.stringify(inertOk)}`);
await p.evaluate(() => closeModuleHub());
await p.waitForTimeout(600);
const released = await p.evaluate(() => ({
  header: document.querySelector("header").inert === true,
  main: document.querySelector("main").inert === true,
  active: document.activeElement && document.activeElement.tagName,
}));
!released.header && !released.main
  ? ok("closing releases it — nothing is left unreachable")
  : fail(`inert not released: ${JSON.stringify(released)}`);
await ctx.close();

// 2c. Language of parts (WCAG 3.1.2). This is the one the product breaks by
// construction, and the exam-language feature made it visible rather than
// causing it: a fallback card, or a simulation switched to German, is text in
// a language the surrounding page does not declare. A screen reader then
// pronounces German with the learner's own voice, which for Greek or Arabic
// is not an accent — it is unintelligible.
({ ctx, p } = await page(`${SITE}/app.html?exam=fuehrerschein&scope=B`, "el-GR"));
await p.evaluate(() => { state.lang = "el"; try { closeModuleHub(); } catch (e) {} });
await p.waitForTimeout(500);
const docLang = await p.evaluate(() => document.documentElement.lang);
note(`page declares lang="${docLang}"`);
const started = p.evaluate(() => startExam("simulation"));
await p.waitForTimeout(800);
if (await p.isVisible("#exam-lang-sheet")) {
  await p.click('#exam-lang-list button[data-lang="de"]');
  await started;
  await p.waitForTimeout(1200);
}
const parts = await p.evaluate(() => {
  const q = document.querySelector("#exam-question");
  const opts = [...document.querySelectorAll("#exam-options .option")];
  const declared = el => { let n = el; while (n && n !== document.documentElement) { if (n.lang) return n.lang; n = n.parentElement; } return document.documentElement.lang; };
  return {
    runLang: state.exam && state.exam.lang,
    pageLang: document.documentElement.lang,
    questionDeclaredAs: declared(q),
    optionsDeclaredAs: opts.length ? declared(opts[0]) : null,
  };
});
if (parts.runLang && parts.runLang !== parts.pageLang) {
  parts.questionDeclaredAs === parts.runLang
    ? ok(`exam text in ${parts.runLang} is declared lang="${parts.runLang}" inside a lang="${parts.pageLang}" page`)
    : fail(`WCAG 3.1.2: exam runs in ${parts.runLang} but the text is announced as `
         + `"${parts.questionDeclaredAs}" — a screen reader reads German with a `
         + `${parts.pageLang} voice`);
  parts.optionsDeclaredAs === parts.runLang
    ? ok(`answer options likewise`)
    : fail(`WCAG 3.1.2: answer options announced as "${parts.optionsDeclaredAs}", not "${parts.runLang}"`);
} else note("no language switch happened; 3.1.2 not exercised");
await axeScan(p, "exam run");
await ctx.close();

await b.close();
console.log(f ? `\nFAILURES: ${f}` : "\naccessibility checks passed");
console.log("Reminder: automated checks cover a minority of WCAG. A green run is not a claim of accessibility.");
process.exit(f ? 1 : 0);
