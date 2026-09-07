/**
 * DN-96: shared helpers for the multilingual exam E2E suite.
 * See docs/adr/ADR-exam-e2e-testing.md for why the suite is shaped this way.
 *
 * The important subtlety: an exam run is a RANDOM draw (drawExamQuestions()
 * uses Math.random()), and options are rendered in randomised order. So a test
 * cannot hardcode which questions appear or where an option sits. Instead we:
 *   - read the drawn ids out of the page's own `state` (app.js is a classic
 *     script, so its top-level `const state` is reachable from window scope), and
 *   - click options by their stable `data-key` attribute, which carries the
 *     original a/b/c/d key regardless of display order.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = path.resolve(HERE, '..', '..');
export const APP = path.join(REPO, 'app');

export const DRIVING_MODULES = ['fuehrerschein', 'motorrad', 'lkw', 'fuehrerschein_bus'];
export const ALL_LOCALES = ['de', 'en', 'es', 'fr', 'it', 'pl', 'ru', 'uk', 'tr', 'ar', 'hi', 'zh'];

/** Text that must never reach a learner's screen. */
export const PLACEHOLDER_RE =
  /\b(TODO|TBD|FIXME|lorem ipsum|undefined|null|high_stakes|grundstoff|topic_code)\b|\{\{|\}\}|\[\[/i;

/** Non-DE text identical to the DE text is a copy-paste-not-translated smell.
 *  Short strings are exempt: "Stop", "Airbag", "ABS" legitimately coincide. */
export const MIN_UNTRANSLATED_LEN = 25;

export function readCore(module) {
  const raw = fs.readFileSync(path.join(APP, 'data', module, 'core.json'), 'utf8');
  const parsed = JSON.parse(raw);
  const byId = {};
  for (const q of parsed.questions) byId[q.id] = q;
  return { meta: parsed.meta, byId, ids: parsed.questions.map(q => q.id) };
}

export function readLocale(module, lang) {
  return JSON.parse(
    fs.readFileSync(path.join(APP, 'data', module, 'locales', `${lang}.json`), 'utf8'));
}

export function localesFor(module) {
  return fs.readdirSync(path.join(APP, 'data', module, 'locales'))
    .filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)).sort();
}

/** Read app.js's top-level `state` (see note in startTrainingExam). */
export function readAppState(page, pick) {
  return page.evaluate(
    expr => (typeof state === 'undefined' ? null : Function('state', `return (${expr});`)(state)),
    pick);
}

/**
 * Drive the app from a cold load to the exam-mode picker, in one language.
 *
 * The language is set through the browser context's `locale` (see the config)
 * rather than the header dropdown, because `#lang-select` is inert while the
 * mandatory first-visit module picker is open - detectLang() reads
 * navigator.languages before that picker renders.
 */
export async function openToExamPicker(page, { module, moduleLabel }) {
  await page.goto('/app.html', { waitUntil: 'networkidle' });

  // DN-89 storage-consent gate. It auto-declines after 10s, so accept promptly.
  const consent = page.locator('#storage-consent-yes');
  if (await consent.count() && await consent.isVisible()) await consent.click();

  // Mandatory first-visit module picker, matched by its localized label.
  const picker = page.locator('#module-picker');
  if (await picker.count() && await picker.isVisible()) {
    await picker.getByRole('button', { name: moduleLabel }).first().click();
    // Driving modules then ask for a class/scope; take the first offered.
    const scope = page.locator('#module-picker .exam-mode-btn:visible');
    if (await scope.count()) await scope.first().click();
  }

  // Optional module-intro carousel.
  for (let i = 0; i < 5; i++) {
    const skip = page.locator('#module-intro-skip');
    if (!(await skip.count()) || !(await skip.isVisible())) break;
    await skip.click();
    await page.waitForTimeout(150);
  }

  await page.locator('#exam-start-btn').click();
  await page.locator('#exam-picker').waitFor({ state: 'visible' });
}

/** Start a Training run and return the ids the app actually drew, in order. */
export async function startTrainingExam(page) {
  await page.locator('#exam-pick-training').click();
  await page.locator('#exam-view').waitFor({ state: 'visible' });
  // NOTE: app.js declares `const state` at the top level of a CLASSIC script,
  // so it lives in the global lexical environment, NOT on `window`. It must be
  // referenced by bare name; `window.state` is undefined here.
  const ids = await page.evaluate(
    () => (typeof state !== 'undefined' && state.exam && state.exam.questions || []).map(q => q.id));
  if (!ids.length) throw new Error('could not read drawn question ids from page state');
  return ids;
}

/** Every option key currently on screen, in DOM order. */
export async function visibleOptionKeys(page) {
  return page.evaluate(() =>
    [...document.querySelectorAll('#exam-options .option')].map(o => o.dataset.key));
}

export async function answerAndAdvance(page, keys) {
  for (const k of keys) await page.locator(`#exam-options .option[data-key="${k}"]`).click();
  await page.locator('#exam-next-btn').click();
  await page.waitForTimeout(60);
}

/** Pick keys that are deliberately wrong for this question. */
export function wrongKeys(correct, available) {
  const wrong = available.filter(k => !correct.includes(k));
  return wrong.length ? [wrong[0]] : [];
}
