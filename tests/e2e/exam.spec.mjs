/**
 * DN-96: multilingual exam end-to-end suite.
 *
 * Implements ADR-0001 (docs/adr/ADR-exam-e2e-testing.md).
 *
 * For every driving module x every locale this proves, through the real UI:
 *   1. the exam is completable end-to-end;
 *   2. answering per core.json's `correct` key scores a PASS with zero review
 *      items - i.e. the JSON answer key IS what the UI treats as correct;
 *   3. answering deliberately wrongly scores a FAIL with one review item per
 *      question - the same claim proven in the opposite direction, which is
 *      what rules out a test that would pass against a broken key;
 *   4. no question or option renders empty, and none carries placeholder or
 *      leaked-authoring text;
 *   5. the app did NOT silently fall back to another language
 *      (fetchLocaleTextWithFallback sets state.contentLangFallback), which
 *      would otherwise make a missing translation look like a passing test.
 *
 * NOT covered here, deliberately: whether a translation is semantically
 * faithful to the German. An exam run cannot see that - a stale locale
 * describing the wrong traffic sign renders perfectly and scores correctly.
 * That is scripts/translation_ledger.py's job. See the ADR's test-pyramid
 * section; overselling this suite as catching it would be the mistake.
 */
import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';
import {
  APP, DRIVING_MODULES, PLACEHOLDER_RE, MIN_UNTRANSLATED_LEN,
  readCore, readLocale, localesFor,
  openToExamPicker, startTrainingExam, visibleOptionKeys, answerAndAdvance, wrongKeys,
} from './helpers.mjs';

const MANIFEST = JSON.parse(fs.readFileSync(path.join(APP, 'data', 'modules.json'), 'utf8'));
const labelFor = (module, lang) => {
  const m = MANIFEST.modules.find(x => x.exam_type === module);
  return m && m.label && (m.label[lang] || m.label.en || m.label.de);
};

// One locale is exercised in full for every module. `ONLY_LANG` narrows the
// matrix for a quick local run: ONLY_LANG=de npm run test:e2e
const ONLY_LANG = process.env.ONLY_LANG;

for (const module of DRIVING_MODULES) {
  const core = readCore(module);
  const langs = localesFor(module).filter(l => !ONLY_LANG || l === ONLY_LANG);

  test.describe(`${module} (${core.ids.length} questions)`, () => {
    for (const lang of langs) {
      const locale = readLocale(module, lang);
      const de = readLocale(module, 'de');
      const moduleLabel = labelFor(module, lang);

      // detectLang() reads navigator.languages on first visit, and #lang-select
      // is inert while the mandatory module picker is open - so the browser
      // context's locale, not the dropdown, is how a test picks its language.
      test.describe(`${lang}`, () => {
      test.use({ locale: `${lang}-${lang.toUpperCase()}` });

      test(`[${lang}] answering from the key passes, and renders cleanly`, async ({ page }) => {
        await openToExamPicker(page, { module, moduleLabel });
        const ids = await startTrainingExam(page);
        expect(ids.length, 'exam drew no questions').toBeGreaterThan(0);

        for (const id of ids) {
          const q = core.byId[id];
          const text = locale[id];
          expect(text, `${lang}/${id}: missing from locale file`).toBeTruthy();

          // what is on screen must be this question, in this language
          const onScreen = (await page.locator('#exam-question').innerText()).trim();
          expect(onScreen, `${lang}/${id}: rendered question is empty`).not.toBe('');
          expect(onScreen).toBe(text.question.trim());
          expect(onScreen, `${lang}/${id}: placeholder text on screen`).not.toMatch(PLACEHOLDER_RE);
          if (lang !== 'de' && de[id] && text.question.length >= MIN_UNTRANSLATED_LEN) {
            expect(text.question,
              `${lang}/${id}: question identical to German - untranslated?`).not.toBe(de[id].question);
          }

          const keys = await visibleOptionKeys(page);
          expect(new Set(keys), `${lang}/${id}: option keys differ from the data`)
            .toEqual(new Set(Object.keys(text.options)));
          for (const k of keys) {
            const optText = (await page.locator(`#exam-options .option[data-key="${k}"]`).innerText()).trim();
            expect(optText, `${lang}/${id}: option ${k} is empty`).not.toBe('');
            expect(optText, `${lang}/${id}: option ${k} has placeholder text`).not.toMatch(PLACEHOLDER_RE);
          }

          // every key the answer sheet calls correct must actually be on screen
          for (const k of q.correct) {
            expect(keys, `${lang}/${id}: correct key '${k}' is not an available option`).toContain(k);
          }
          await answerAndAdvance(page, q.correct);
        }

        await page.locator('#exam-results').waitFor({ state: 'visible' });
        await expect(page.locator('#exam-results-title')).toHaveClass(/exam-results-pass/);
        expect(await page.locator('#exam-results-review .exam-review-item').count(),
          'answering entirely from the key still produced review items').toBe(0);

        // a silent fallback would make a missing translation look like a pass
        expect(await page.evaluate(
          () => (typeof state === 'undefined' ? null : state.contentLangFallback)),
          `${lang}: app silently fell back to another language`).toBeFalsy();
      });

      test(`[${lang}] answering wrongly fails and reviews every question`, async ({ page }) => {
        await openToExamPicker(page, { module, moduleLabel });
        const ids = await startTrainingExam(page);

        let answered = 0;
        for (const id of ids) {
          const q = core.byId[id];
          const keys = await visibleOptionKeys(page);
          const wrong = wrongKeys(q.correct, keys);
          if (!wrong.length) { await answerAndAdvance(page, q.correct); continue; }
          await answerAndAdvance(page, wrong);
          answered++;
        }

        await page.locator('#exam-results').waitFor({ state: 'visible' });
        await expect(page.locator('#exam-results-title')).toHaveClass(/exam-results-fail/);
        expect(await page.locator('#exam-results-review .exam-review-item').count(),
          'deliberately wrong answers were not all listed for review').toBe(answered);
      });
      });
    }
  });
}
