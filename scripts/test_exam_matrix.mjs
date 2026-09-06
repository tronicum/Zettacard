#!/usr/bin/env node
/**
 * DN-96: multilingual exam end-to-end suite. Implements ADR-0001
 * (docs/adr/ADR-exam-e2e-testing.md).
 *
 * WHY PLAIN PLAYWRIGHT AND NOT @playwright/test
 * ---------------------------------------------
 * ADR-0001 recommends the `@playwright/test` runner (its Option 1). That was
 * implemented first and abandoned: in this project's dev environment the
 * runner hangs indefinitely with zero output even on a trivial spec that only
 * calls page.setContent(), while the `playwright` LIBRARY drives a real
 * browser here without trouble. The blocker is the runner's own worker/browser
 * bootstrap, not the tests. So this is ADR-0001's Option 2: plain-Node scripts
 * in the same style as scripts/test_storage_consent.mjs and
 * test_full_exam_badge.mjs, with sharding/retries/reporting given up in
 * exchange for something that actually runs. If the runner is ever fixed, the
 * assertions below port over almost unchanged.
 *
 * WHAT THIS PROVES, for every driving module x every locale, through the real UI:
 *   1. the exam is completable end to end;
 *   2. answering from core.json's `correct` key yields a PASS with zero review
 *      items - the JSON answer key IS what the UI scores as correct;
 *   3. answering deliberately wrongly yields a FAIL listing every question -
 *      the same claim proven in the opposite direction, which is what rules
 *      out a test that would still pass against a broken answer key;
 *   4. no rendered question or option is empty or carries placeholder /
 *      leaked-authoring text;
 *   5. the app did not silently fall back to another language
 *      (fetchLocaleTextWithFallback sets state.contentLangFallback) - without
 *      this, a missing translation would look like a passing test.
 *
 * WHAT IT DELIBERATELY DOES NOT PROVE
 * -----------------------------------
 * Whether a translation is semantically faithful to the German. A stale locale
 * describing an entirely different traffic sign renders perfectly and scores
 * correctly - no UI test can see it. That is scripts/translation_ledger.py's
 * job. Overselling this suite as covering that would be the real mistake.
 *
 * USAGE
 *   node scripts/test_exam_matrix.mjs                  # full matrix
 *   node scripts/test_exam_matrix.mjs --lang de        # one language
 *   node scripts/test_exam_matrix.mjs --module lkw     # one module
 *   node scripts/test_exam_matrix.mjs --quick          # smallest module, de+en
 * Exit code 1 on any failure.
 */
import { createRequire } from 'module';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..');
const APP = path.join(REPO, 'app');
const require = createRequire(path.join(REPO, 'package.json'));
const { chromium } = require('playwright');

const DRIVING_MODULES = ['fuehrerschein', 'motorrad', 'lkw', 'fuehrerschein_bus'];
/**
 * Text that must never reach a learner's screen.
 *
 * Split into two patterns on purpose. The authoring markers (TODO/TBD/FIXME)
 * are matched CASE-SENSITIVELY: they are always written in caps, and matching
 * them case-insensitively produced a false positive on the perfectly correct
 * Spanish word "todo" ("all") in bus-lenkzeiten-02/08 - caught on this
 * suite's first full run. The rest stay case-insensitive.
 */
const PLACEHOLDER_RE = /\b(TODO|TBD|FIXME|XXX)\b|\{\{|\}\}|\[\[/;
const PLACEHOLDER_RE_I = /\b(lorem ipsum|undefined|high_stakes|grundstoff|topic_code)\b/i;
const hasPlaceholder = s => PLACEHOLDER_RE.test(s) || PLACEHOLDER_RE_I.test(s);
const MIN_UNTRANSLATED_LEN = 25;

const argv = process.argv.slice(2);
const argOf = n => { const i = argv.indexOf(n); return i === -1 ? null : argv[i + 1]; };
const ONLY_LANG = argOf('--lang');
const ONLY_MODULE = argOf('--module');
const QUICK = argv.includes('--quick');

const readJSON = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const core = m => {
  const p = readJSON(path.join(APP, 'data', m, 'core.json'));
  const byId = {}; for (const q of p.questions) byId[q.id] = q;
  return { byId, count: p.questions.length };
};
const locale = (m, l) => readJSON(path.join(APP, 'data', m, 'locales', `${l}.json`));
const localesFor = m => fs.readdirSync(path.join(APP, 'data', m, 'locales'))
  .filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)).sort();

const MANIFEST = readJSON(path.join(APP, 'data', 'modules.json'));
const labelFor = (m, l) => {
  const e = MANIFEST.modules.find(x => x.exam_type === m);
  return e && e.label && (e.label[l] || e.label.en || e.label.de);
};

// ---- static server -----------------------------------------------------
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.ico': 'image/x-icon',
  '.webmanifest': 'application/manifest+json', '.woff2': 'font/woff2' };
function serve(port) {
  const s = http.createServer((req, res) => {
    let rel = decodeURIComponent(req.url.split('?')[0]);
    if (rel === '/') rel = '/app.html';
    const f = path.join(APP, rel);
    if (!f.startsWith(APP) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.writeHead(404); return res.end('nf');
    }
    res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => s.listen(port, () => r(s)));
}

// ---- page driving ------------------------------------------------------
/** app.js declares `const state` at the top level of a CLASSIC script, so it
 *  is a global LEXICAL binding, not a property of window. It must be read by
 *  bare name; `window.state` is undefined. */
const appState = (page, expr) =>
  page.evaluate(e => (typeof state === 'undefined' ? null : Function('state', `return (${e});`)(state)), expr);

async function openToExamPicker(page, base, moduleLabel) {
  await page.goto(`${base}/app.html`, { waitUntil: 'networkidle' });
  const consent = page.locator('#storage-consent-yes');            // DN-89 gate, auto-declines after 10s
  if (await consent.count() && await consent.isVisible()) await consent.click();
  await page.waitForTimeout(400);
  const picker = page.locator('#module-picker');
  if (await picker.count() && await picker.isVisible()) {
    await picker.getByRole('button', { name: moduleLabel }).first().click();
    await page.waitForTimeout(500);
    const scope = page.locator('#module-picker .exam-mode-btn:visible');
    if (await scope.count()) { await scope.first().click(); await page.waitForTimeout(600); }
  }
  for (let i = 0; i < 5; i++) {                                     // optional intro carousel
    const skip = page.locator('#module-intro-skip');
    if (!(await skip.count()) || !(await skip.isVisible())) break;
    await skip.click(); await page.waitForTimeout(200);
  }
  await page.locator('#exam-start-btn').click();
  await page.locator('#exam-picker').waitFor({ state: 'visible', timeout: 10000 });
}

async function startTraining(page) {
  await page.locator('#exam-pick-training').click();
  await page.locator('#exam-view').waitFor({ state: 'visible', timeout: 10000 });
  const ids = await appState(page, 'state.exam && state.exam.questions ? state.exam.questions.map(q=>q.id) : []');
  if (!ids || !ids.length) throw new Error('could not read drawn question ids from app state');
  return ids;
}
const optionKeys = page => page.evaluate(
  () => [...document.querySelectorAll('#exam-options .option')].map(o => o.dataset.key));

async function answer(page, keys) {
  for (const k of keys) await page.locator(`#exam-options .option[data-key="${k}"]`).click();
  await page.locator('#exam-next-btn').click();
  await page.waitForTimeout(50);
}

// ---- the suite ---------------------------------------------------------
const failures = [];
let checks = 0;
const check = (cond, msg) => { checks++; if (!cond) failures.push(msg); };

async function runCorrect(page, base, mod, lang, C, L, DE) {
  await openToExamPicker(page, base, labelFor(mod, lang));
  const ids = await startTraining(page);
  for (const id of ids) {
    const q = C.byId[id], t = L[id];
    if (!t) { failures.push(`${mod}/${lang}/${id}: missing from locale file`); return; }
    const shown = (await page.locator('#exam-question').innerText()).trim();
    check(shown !== '', `${mod}/${lang}/${id}: rendered question is empty`);
    check(shown === t.question.trim(),
      `${mod}/${lang}/${id}: on-screen question does not match locale data`);
    check(!hasPlaceholder(shown), `${mod}/${lang}/${id}: placeholder text on screen: ${shown.slice(0,60)}`);
    if (lang !== 'de' && DE[id] && t.question.length >= MIN_UNTRANSLATED_LEN) {
      check(t.question !== DE[id].question,
        `${mod}/${lang}/${id}: question identical to German - untranslated?`);
    }
    const keys = await optionKeys(page);
    check(keys.slice().sort().join() === Object.keys(t.options).sort().join(),
      `${mod}/${lang}/${id}: on-screen option keys [${keys}] differ from data [${Object.keys(t.options)}]`);
    for (const k of keys) {
      const txt = (await page.locator(`#exam-options .option[data-key="${k}"]`).innerText()).trim();
      check(txt !== '', `${mod}/${lang}/${id}: option ${k} renders empty`);
      check(!hasPlaceholder(txt), `${mod}/${lang}/${id}: option ${k} has placeholder text: ${txt.slice(0,60)}`);
    }
    for (const k of q.correct) {
      check(keys.includes(k),
        `${mod}/${lang}/${id}: answer key '${k}' is not among the rendered options - unanswerable`);
    }
    await answer(page, q.correct);
  }
  await page.locator('#exam-results').waitFor({ state: 'visible', timeout: 10000 });
  const cls = await page.locator('#exam-results-title').getAttribute('class') || '';
  check(/exam-results-pass/.test(cls),
    `${mod}/${lang}: answering entirely from core.json's key did NOT pass (class="${cls}")`);
  const reviews = await page.locator('#exam-results-review .exam-review-item').count();
  check(reviews === 0, `${mod}/${lang}: correct run still produced ${reviews} review item(s)`);
  const fb = await appState(page, 'state.contentLangFallback');
  check(!fb, `${mod}/${lang}: app silently fell back to '${fb}' - locale not really used`);
}

async function runWrong(page, base, mod, lang, C) {
  await openToExamPicker(page, base, labelFor(mod, lang));
  const ids = await startTraining(page);
  let wrongCount = 0;
  for (const id of ids) {
    const q = C.byId[id];
    const keys = await optionKeys(page);
    const wrong = keys.filter(k => !q.correct.includes(k));
    if (!wrong.length) { await answer(page, q.correct); continue; }
    await answer(page, [wrong[0]]); wrongCount++;
  }
  await page.locator('#exam-results').waitFor({ state: 'visible', timeout: 10000 });
  const cls = await page.locator('#exam-results-title').getAttribute('class') || '';
  check(/exam-results-fail/.test(cls),
    `${mod}/${lang}: deliberately wrong answers did NOT fail (class="${cls}") - answer key may be wrong`);
  const reviews = await page.locator('#exam-results-review .exam-review-item').count();
  check(reviews === wrongCount,
    `${mod}/${lang}: ${wrongCount} wrong answers but ${reviews} review item(s) listed`);
}

const PORT = 8805;
const server = await serve(PORT);
const base = `http://localhost:${PORT}`;
const browser = await chromium.launch();
const started = Date.now();
let ran = 0;

let modules = ONLY_MODULE ? [ONLY_MODULE] : DRIVING_MODULES;
if (QUICK) modules = ['fuehrerschein_bus'];

for (const mod of modules) {
  const C = core(mod);
  const DE = locale(mod, 'de');
  let langs = localesFor(mod);
  if (ONLY_LANG) langs = langs.filter(l => l === ONLY_LANG);
  if (QUICK) langs = langs.filter(l => ['de', 'en'].includes(l));
  process.stdout.write(`\n${mod} (${C.count} questions)\n`);
  for (const lang of langs) {
    const L = locale(mod, lang);
    for (const [name, fn] of [['key->pass', runCorrect], ['wrong->fail', runWrong]]) {
      const ctx = await browser.newContext({ locale: `${lang}-${lang.toUpperCase()}` });
      const page = await ctx.newPage();
      const before = failures.length;
      try {
        await (fn === runCorrect ? runCorrect(page, base, mod, lang, C, L, DE)
                                 : runWrong(page, base, mod, lang, C));
      } catch (e) {
        failures.push(`${mod}/${lang} [${name}]: ${e.message.split('\n')[0]}`);
      }
      await ctx.close(); ran++;
      const bad = failures.length - before;
      process.stdout.write(`  ${bad ? 'FAIL' : 'ok  '}  ${lang.padEnd(3)} ${name}${bad ? `  (${bad} problem(s))` : ''}\n`);
    }
  }
}
await browser.close(); server.close();

const secs = ((Date.now() - started) / 1000).toFixed(0);
console.log(`\n${ran} exam runs, ${checks} assertions, ${secs}s`);
if (failures.length) {
  console.error(`\nFAILED - ${failures.length} problem(s):\n`);
  for (const f of failures.slice(0, 60)) console.error('  ' + f);
  if (failures.length > 60) console.error(`  ... and ${failures.length - 60} more`);
  process.exit(1);
}
console.log('OK - every exam completed, answer keys verified in both directions.');
