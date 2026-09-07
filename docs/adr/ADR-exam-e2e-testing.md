# ADR-0001: Automated end-to-end exam testing across all languages

- **Status:** Proposed
- **Date:** 2026-09-05
- **Deciders:** PO (pending); drafted by an AI agent from a read of the actual repo state on this date
- **Numbering note:** `docs/adr/` did not exist before this document. Convention set here: `ADR-<nnnn>: <title>` in the H1, file name `ADR-<short-slug>.md`, sections Title / Status / Date / Context / Decision Drivers / Considered Options / Decision / Consequences / Implementation Notes. Next ADR is `ADR-0002` (the planned local-LLM content-equivalence ADR should take that number).

## Context

Zettacard is a build-step-free static PWA. `netlify.toml` publishes `app/` as the site root (`command = "true"`, no build). The app is a single classic script, `app/app.js` (~7.8k lines), driving `app/app.html`; there is no bundler, no module system and no component boundary to unit-test against.

Content is a generated artifact: `data/build_modules.py` derives `app/data/<module>/core.json` (ids, `correct` letter arrays, `question_type`, `points`, `high_stakes`, `image_ref`, `class_scope`/`region_scope`) and `app/data/<module>/locales/<lang>.json` (`{question, options{a..}, explanation}` keyed by question id) from the editable masters in `data/` (`data/pilot_questions.json` for the driving-licence module, `*_pilot.json` for most others). There are 25 module directories under `app/data/`. The four driving-licence modules all ship all 12 locales (de, en, es, fr, it, pl, ru, uk, tr, ar, hi, zh) with no id gaps as of today:

| module | questions | locales | exam draw |
|---|---|---|---|
| `fuehrerschein` | 531 (139 with a sign image) | 12 | 30 |
| `motorrad` | 138 | 12 | 30 |
| `lkw` | 90 | 12 | 30 |
| `fuehrerschein_bus` | 48 | 12 | 28 |

How an exam actually runs in the app (relevant to every option below, read from `app/app.js`):

- A run is a **random draw** (`drawExamQuestions()`, `Math.random()` via `shuffle()`), topic-weighted through `EXAM_TOPIC_DRAW`, of `examQuestionCount()` questions (30 default, per-module overrides). One run therefore touches ~6% of the 531-question pool.
- Options are rendered in **randomised order** (`shuffledOptionEntries()`), but each `.option` div carries the original key in `data-key`, so `#exam-options .option[data-key="b"]` is stable regardless of display order. `q.correct` is always an array; 5 `fuehrerschein` questions are `multi_choice` and score all-or-nothing (`isExamAnswerCorrect()`).
- Grading is `computeExamResults()`: error points vs `maxErrorPoints()`, plus the "at most one wrong high-stakes question" rule. The results screen sets `#exam-results-title` to class `exam-results-pass` / `exam-results-fail`, prints a summary in `#exam-results-summary`, and lists every wrong answer as `.exam-review-item` under `#exam-results-review` (or a "no mistakes" paragraph).
- Only **Simulation** mode records a completion; Training mode has no timer. Both draw identically.
- Language: `detectLang()` reads `navigator.languages` on first visit; afterwards `#lang-select` (header, inert while a modal is open) calls `setLang()`. If a module lacks a locale, `fetchLocaleTextWithFallback()` silently falls back to `en` then `de` and sets `state.contentLangFallback` - i.e. a missing translation does **not** fail visibly in the UI.
- There is no `data-question-id` on the exam DOM. The exam view shows only text; question identity has to come from matching `#exam-question` text back to the locale file (what `scripts/test_full_exam_badge.mjs` does) or from reading the page's global `state.exam.questions` via `page.evaluate` (app.js is a classic script, so its top-level `const state` is reachable from the page's global scope).
- Gates before the exam can start: the DN-89 storage-consent dialog (`#storage-consent-notice`, buttons `#storage-consent-yes` / `#storage-consent-no`, 10 s auto-decline), the mandatory first-visit module picker (`#module-picker`, buttons matched by localized label from `data/modules_manifest.json`), a class/scope step for the driving modules (`.exam-mode-btn`), and an optional module-intro carousel (`#module-intro-skip`). Then `#exam-start-btn` -> `#exam-picker` -> `#exam-pick-training` / `#exam-pick-simulation` -> `#exam-view`.

What exists today for testing:

- `playwright` **1.62.1** (the library, not the `@playwright/test` runner) is the only devDependency. Node 22 locally.
- `scripts/test_storage_consent.mjs` (DN-90): plain-Node Playwright script, 5 consent scenarios, defaults to `http://localhost:8080`, handles the missing-browser case by falling back from the sandbox path `/opt/pw-browsers/chromium` to Playwright's managed Chromium.
- `scripts/test_full_exam_badge.mjs`: drives a full Simulation run for `arbeitssicherheit` in German, answering every question correctly from `core.json`, then verifies the signed badge. This is already 80% of a one-language exam E2E - but it hardcodes the sandbox Chromium path, defaults to production, matches questions by DE text only and takes the first scope option.
- `scripts/test_hinweisgeberschutz_smoke.mjs`: module-picker smoke test, same shape.
- `scripts/dev-serve.sh`: `python3 -m http.server --directory app` on 8080 (kills a stale listener first). `npm run dev` / `npm run test:storage-consent` exist in `package.json`.
- `data/build_modules.py` ends with a sanity pass: every core question has a scope field and a DE text. Nothing checks the other 11 locales beyond "the file parsed".
- There is **no CI**: no `.github/`, no Netlify build plugin; deploys go out from the local tree via the Netlify MCP connector (see `AGENTS.md`), and `AGENTS.md` asks for a live curl/Playwright check after each deploy by hand.

The user's ask is "a proper test to do the exam in all of them": every language, driving-licence modules at minimum, actually completing the exam through the UI, proving the answer key in `core.json` is what the UI scores as correct, and proving no empty/untranslated/placeholder text reaches the screen.

The motivating incident: a `fuehrerschein` locale file that had gone stale relative to the German source. It still had the right ids, four options and a correct key that scored, but the translated question described an entirely different traffic sign. Structurally valid, semantically wrong. Note for scale: `app/data/fuehrerschein/locales/*` already shows smaller drift of the same family - e.g. `vorfahrt-02`'s uk/pl distractors ("Заборона в'їзду" / "Zakaz wjazdu" = *no entry*) don't correspond to the DE distractor ("Sie müssen in jedem Fall kurz anhalten") even though the correct option matches.

## Decision Drivers

1. **Coverage that matters:** every language x every driving module must be *completable* and *gradeable* through the real UI, and the JSON answer key must be demonstrably what the UI scores.
2. **Data integrity through the UI, not only in JSON:** empty text, `undefined`, fallback-to-English, placeholder tokens must fail a test.
3. **Honesty about the stale-locale bug:** don't oversell E2E as the fix for a content-equivalence problem; name the complementary check.
4. **Matrix cost:** 12 x 531 (plus 138 + 90 + 48) is 9,684 question/locale pairs. Exam mode reaches 30 per run at random. Anything that claims "every question through exam mode in every language" must state the runtime honestly.
5. **Zero-build, no-CI repo:** must run from `npm run ...` against `scripts/dev-serve.sh` on a laptop today, and be liftable to GitHub Actions + Netlify Deploy Previews later without rewriting.
6. **Minimal new surface:** Playwright is already installed and proven in three scripts; the project has a stated bias against adding dependencies to a zero-dependency PWA.
7. **Maintenance by agents and a solo PO:** selectors and flows are documented in-repo; tests should read like the existing scripts so future rounds can extend them.
8. **Mobile reality:** the PWA is used on phones (390x844 viewport in the consent test, iOS install page `get-app.html`), and `ar` is RTL - at least one non-Chromium engine matters eventually, but not for the exam-logic questions this ADR is about.

## Considered Options

The five candidates. Each is judged on the same four jobs: (J1) full exam run per language, (J2) answer-key-vs-UI scoring in both directions, (J3) per-question render integrity across the whole pool, (J4) the stale-locale class.

### Option 1 - Playwright Test runner (`@playwright/test`), data-driven matrix with sharding

**What it is.** Playwright's own test runner on top of the library already in `node_modules`: parameterised tests, projects, fixtures, retries, `--shard`, HTML/JSON reporters, trace-on-failure.

**How it would work here.**
- `tests/e2e/exam.spec.mjs` generates one `test()` per `(module, lang, mode)` from a small matrix table, via `for` loops at module scope (Playwright's documented parameterisation pattern).
- A shared fixture opens `app.html` with `locale: "<lang>-XX"` so `detectLang()` picks the language before the mandatory module picker renders (the trick `test_full_exam_badge.mjs` already uses, because `#lang-select` is inert behind the picker), clicks `#storage-consent-yes`, picks the module by manifest label, takes the first scope option, skips the intro, opens `#exam-picker`.
- **Correct run:** read the drawn ids via `page.evaluate(() => state.exam.questions.map(q => q.id))` after `startExam` (no app change needed), then for each question assert `#exam-question` text equals `locale[id].question`, assert `.option` count equals `Object.keys(locale[id].options).length` and every option's text is non-empty, click `.option[data-key=k]` for each `k` in `core[id].correct`, click `#exam-next-btn`. At `#exam-results` assert class `exam-results-pass`, zero `.exam-review-item`, and the "no mistakes" text.
- **Wrong run:** same drive, but click a key *not* in `correct` (or, for `multi_choice`, a strict subset). Assert `exam-results-fail`, `.exam-review-item` count == number of questions, and that each review item's "right answer" text equals `locale[id].options[correct]`. This proves the key in `core.json` is what the UI believes is correct, per question, in both directions.
- **Language integrity:** assert `page.evaluate(() => state.contentLangFallback) === null` (no silent English), and run a placeholder regex over every rendered question/option (`TODO|TBD|lorem|\{\{|\}\}|\[\[|undefined|null|^\s*$`), plus "non-DE locale text identical to DE text" for questions longer than ~25 chars (a copy-paste-not-translated smell; short option words like "Stop" are exempt by length).
- **Pool-wide render check (J3):** *not* through exam mode. Use the flashcard detail view (`#list` card -> `#detail-view`, `renderDetail()` walks `filteredQuestions()` with prev/next) which is deterministic and visits every question, or a proposed test-only hook (below). This is where all 531 x 12 renders happen.
- Sharding: `npx playwright test --shard=1/4` across 4 CI jobs; locally `--workers=4`.

**Matrix and runtime, measured against how the app works.** An exam run is ~30 questions x (1-2 clicks + next + ~120 ms settle) ≈ 6-10 s headless, plus ~2 s page setup. Per driving module: 12 langs x 2 runs (correct, wrong) ≈ 24 runs ≈ 4 min serial. Four modules ≈ 96 runs ≈ 15 min serial, **~4 min with 4 workers**. Covering every question *in exam mode* is a coupon-collector problem: expected draws to see all 531 at 30 per draw ≈ (531/30)·H(531) ≈ 120 runs per language, ~1,450 runs for `fuehrerschein` alone (2-4 h). **Not wise.** The pool-wide check via the detail view costs ~40-60 ms per question -> 531 x 12 ≈ 5-6 min serial for `fuehrerschein`, ~10 min for all four driving modules, and it is what actually delivers "every question renders in every language".

**Strengths.** Same engine as the three existing scripts; auto-waiting locators remove the `waitForTimeout(120)` sleeps in the current script; built-in sharding, retries, traces, HTML report; `--project` can add WebKit/Firefox later for the RTL/iOS question without touching test code; parameterised matrix is first-class; JSON reporter is easy to summarise per language.

**Weaknesses.** One more devDependency (`@playwright/test`, same version line as `playwright`); test files use `test()`/`expect()` conventions rather than the repo's plain-Node `fail()` style; the existing three scripts would either be ported or coexist as a second style. Random draw means a "correct run" exercises different questions each time - fine for J1/J2, misleading if anyone reads it as pool coverage.

**Cost / maintenance.** Low-medium. ~300 lines for the spec + ~150 lines of shared page helpers, most of which are lifted from `test_full_exam_badge.mjs`. Selectors are ids already documented in `app.html` comments. Adding a module is one row in the matrix table.

**CI fit (Netlify static site).** Good. Netlify itself should stay `command = "true"` - its build image has no browsers and its minutes are the wrong place to run 10 min of Chromium. The natural home is a GitHub Actions workflow (`microsoft/playwright-github-action` or `npx playwright install --with-deps chromium`) that serves `app/` with `scripts/dev-serve.sh` (or `npx serve app`) and, on PRs, additionally points `BASE_URL` at the Netlify Deploy Preview URL. Sharding maps 1:1 onto a matrix job. Until CI exists, `npm run test:e2e` locally before the MCP deploy is the gate `AGENTS.md` already asks for by hand.

### Option 2 - Status quo extended: plain `playwright` library scripts under `scripts/` (no runner)

**What it is.** Keep the current style: one `scripts/test_exam_all_langs.mjs` in the mould of `test_full_exam_badge.mjs`, looping modules x languages inside `main()`, with `fail()` and exit codes.

**How it would work here.** Exactly the drive described in Option 1, but the loop is hand-written: `for (mod of MODULES) for (lang of LANGS) { correctRun(); wrongRun(); }`, one browser, one context per language (fresh consent each time). A second script, or a flag, walks the detail view for the pool-wide render check. Parallelism would be hand-rolled with `Promise.all` over contexts, or by launching the script N times with a `--shard` argument the script parses itself.

**Strengths.** Zero new dependencies. Same idiom as the three existing scripts, so agents extending it copy known-good code. No config file, no runner opinions. Works today with `npm run dev` in one terminal.

**Weaknesses.** Everything the runner gives for free has to be re-implemented and maintained by hand: parallel workers, retries on a flaky click, per-test timeouts (one hung `waitForSelector` stalls the whole 96-run loop), a per-(module, lang) pass/fail report, screenshots/traces on failure. The existing scripts already show the cost of not having it: `waitForTimeout(500)` sleeps, `process.exit(1)` on first failure (no "which of the 12 languages broke" summary), sandbox-only browser paths. At 96 exam runs + ~10k detail renders, "first failure aborts" is a real ergonomics problem - a broken `hi` locale would hide a broken `zh` one.

**Cost / maintenance.** Lowest to start (~250 lines), rising over time as the hand-rolled harness grows the features above. Every future test (course layer, practice quiz, certificates) repeats the same boilerplate.

**CI fit.** Fine but manual: a GitHub Actions job runs `node scripts/test_exam_all_langs.mjs http://localhost:8080`; sharding means N jobs each passing a different `--langs=` slice; reporting is stdout only.

### Option 3 - Cypress

**What it is.** Browser-driven E2E framework with its own runner/GUI, running tests inside the browser via a proxy.

**How it would work here.** `cypress/e2e/exam.cy.js` reads `core.json`/`locales/*.json` with `cy.readFile()` or `cy.fixture()`; the same click flow with `cy.get('#exam-options .option[data-key=b]')`. Language would be forced via `onBeforeLoad` overriding `navigator.language(s)` (Cypress has no context-level `locale`). Access to page globals (`state`) via `cy.window()`.

**Strengths.** Excellent interactive time-travel debugger, which genuinely helps when a click flow diverges in one of 12 languages; large ecosystem; readable retry-ability model.

**Weaknesses.** A second browser-automation stack alongside the already-working Playwright scripts (the project would carry both, or throw the existing three away). Parallelisation/sharding across machines is a paid Cypress Cloud feature or a third-party splitter - for a 96-run matrix plus a ~6k-render loop that is the feature we need most. Chromium/Firefox/WebKit-experimental only; `cy.readFile` over 12 x ~600 KB locale files per spec is slow relative to Node `readFile` in a fixture. Heavy install (~600 MB binary cache) for a zero-dependency repo. Overriding `navigator.language` is fiddlier than Playwright's `locale`.

**Cost / maintenance.** Medium-high: new tool, new config, new idiom to teach the agents, and no reuse of existing scripts.

**CI fit.** Good on GitHub Actions (`cypress-io/github-action`), runs fine against a static server or a Deploy Preview; free parallelism is not built in.

### Option 4 - WebdriverIO (WebDriver / BiDi)

**What it is.** Standards-based automation (W3C WebDriver, WebDriver BiDi) with a mature runner; the route to real Safari (safaridriver) and real iOS Safari via Appium.

**How it would work here.** `wdio.conf.js` + `test/specs/exam.e2e.js`; same selector flow with `$('#exam-next-btn').click()`; language by launching the browser with `--lang=<lang>` (Chrome) or a per-capability profile; page globals via `browser.execute(() => state.exam.questions)`.

**Strengths.** The only option that can drive *real* Safari/iOS (the PWA's install target) without emulation; standards-based so browser choice is decoupled from the tool; solid runner with capabilities matrix, retries, sharding via multiple capabilities and `maxInstances`.

**Weaknesses.** Overkill for the questions in this ADR - the exam-logic and locale-integrity assertions are engine-independent and Chromium answers them completely. WebDriver round-trips are slower than CDP (matters at ~10k detail-view renders). Setup surface (services, drivers, Appium for iOS) is the largest of the five. Again a second stack next to Playwright.

**Cost / maintenance.** High. Worth it only when a Safari-specific rendering question (RTL Arabic layout, iOS standalone-mode quirks, service-worker behaviour) becomes the thing being tested - that is a different ADR.

**CI fit.** Good for Chromium on GitHub Actions; real Safari needs a macOS runner (expensive minutes) and iOS needs Appium + simulator - not a fit for an every-commit gate on a static site.

### Option 5 - Headless-DOM "in-process" tests: load `app.js` into jsdom / happy-dom under `node:test`

**What it is.** No browser. A Node test boots `app.html` + `app.js` inside jsdom (or happy-dom), stubs `fetch` to read `app/data/**` from disk, stubs `localStorage`/`history`/`navigator`, and calls the app's own functions (`loadModuleData`, `startExam`, `renderExamQuestion`, `computeExamResults`) directly while asserting on the DOM.

**How it would work here.** `tests/dom/exam.test.mjs`: for each `(module, lang)`, set `navigator.languages`, run `loadModuleData(mod, scope)`, then iterate **every question** (not a draw) by setting `state.exam = { questions: state.questions, answers: {}, ... }` and calling `renderExamQuestion()` per index, asserting text/options, clicking `.option` divs via `dispatchEvent`, then `computeExamResults()`. Full 12 x 531 in well under a minute.

**Strengths.** The only approach where the *full* matrix (every question, every language, both correct and wrong, through the real render code) is cheap enough to run on every commit. No browser binary, no server, no consent dialog. Deterministic (`Math.random` can be stubbed).

**Weaknesses.** `app.js` was never written to be imported: it is a 7.8k-line classic script with top-level side effects (consent gate, `history.pushState`, service-worker registration, `matchMedia`, `caches`, `IntersectionObserver`, inert-behind-dialog handling). Booting it in jsdom means either a growing pile of stubs that must track every new browser API the app adopts, or refactoring `app.js` for testability - a change with product risk the project has explicitly avoided. jsdom does not do layout, so it says nothing about RTL, overflow, focus visibility or the PWA shell. It is a *unit/integration* test of render code, not an E2E test of what a visitor sees; it would not have caught, for example, the DN-40 "LKW under Russian crashes" bug's *visible* symptom (it would have caught the thrown error, which is arguably enough). Adds jsdom/happy-dom as a dependency.

**Cost / maintenance.** Medium to start (the stub layer is the hard part), and fragile over time as `app.js` grows. Attractive as a *future* layer once/if `app.js` gets any structural split, not as the first move.

**CI fit.** Excellent - pure Node, seconds, no browsers. Could even run inside Netlify's build (`command`) without a browser, though the repo deliberately keeps that `true`.

### Summary matrix

| | J1 full run / lang | J2 key-vs-UI both ways | J3 whole pool renders | J4 stale locale | New deps | Runtime (4 driving modules, 12 langs) | Effort |
|---|---|---|---|---|---|---|---|
| 1 Playwright Test | yes | yes | yes (detail view, sampled or full) | no (see below) | `@playwright/test` | ~4 min sharded exam runs + ~10 min pool walk | low-med |
| 2 Plain Playwright scripts | yes | yes | yes, slower/hand-rolled | no | none | same, serial unless hand-sharded | low, grows |
| 3 Cypress | yes | yes | yes | no | Cypress | similar; paid parallelism | med-high |
| 4 WebdriverIO | yes | yes | yes, slowest | no | WDIO + drivers | slower per action | high |
| 5 jsdom in-process | partial (no real browser) | yes | yes, full matrix in seconds | no | jsdom + stubs | < 1 min | med, fragile |

**None of the five catches J4 on its own.** See "The stale-locale bug, honestly" below.

## Decision

**Adopt Option 1: Playwright Test (`@playwright/test`) as the E2E layer, with a data-driven (module x language) matrix, exam runs sampled by design, and the pool-wide render walk done through the deterministic flashcard detail view - paired with a Node-level data-integrity script that is not an E2E test at all.**

Reasoning:

- Playwright is the incumbent and already proven against this app's exact gates (consent, inert header, mandatory picker, scope step, intro carousel). Option 1 is the smallest step that turns three ad-hoc scripts into a matrix with parallelism, per-language reporting, retries and failure traces - the things a 96-run matrix needs and Option 2 would end up re-implementing badly.
- Options 3 and 4 bring a second automation stack for no gain on the questions asked; Option 4 is the right answer to a *different* question (real Safari/iOS) and is noted as a future ADR trigger.
- Option 5 is the only one that makes the *full* 12 x 531 matrix cheap, but its cost lands on `app.js`'s structure. Its core idea - "check every question against the answer key without a browser" - is captured far more cheaply as pure-JSON checks (Recommended test pyramid, layer 1), which need no DOM at all. The DOM-level part of Option 5 is deferred.
- Full-matrix testing **through exam mode** is rejected on cost and on principle: the draw is random, so it would take ~1,450 runs to cover `fuehrerschein` in one language and still prove nothing extra about grading that 30 questions don't already prove. Exam-mode E2E answers "is the exam completable and does the key score as the key" - a per-(module, lang) property, not a per-question one. Per-question properties belong in the JSON layer (every commit) and the detail-view walk (nightly / pre-deploy).

### The stale-locale bug, honestly

The incident locale file had correct ids, four options, a scoring correct key and non-empty, non-placeholder, non-German text. Every assertion above passes on it. **A UI E2E test cannot catch this class of bug**, because nothing in the DOM is wrong; the bug lives in the relation between two natural-language strings (DE source vs translation). Anyone claiming otherwise is testing something else.

What E2E *does* contribute to that class: it makes sure the failure is not *also* structural (the wrong-sign locale still loads, still renders, still scores), and it can carry a handful of cheap **deterministic proxies** for equivalence that need the rendered text (or just the JSON):

1. **Sign-number parity.** 139 `fuehrerschein` questions have `image_ref: "signs/<nnn>"`. Today 49 of them cite their `Zeichen <nnn>` number in the question text in *all 12* locales (measured 2026-09-05). Rule: if DE mentions `<nnn>` from `image_ref`, every locale must mention the same `<nnn>`, and no locale may mention a *different* three-digit sign number. This would have flagged the incident if the stale text named its (different) sign - a common pattern in this dataset.
2. **Numeric/legal-token parity.** Extract numbers with units and section references (`50 km/h`, `0,5 ‰`, `1,5 m`, `§ 8`, `Zeichen 205`) from DE; require the same multiset in each locale (allowing decimal-separator variance). Wrong-sign or wrong-rule translations very often change a number.
3. **Correct-option lexical anchor.** For sign questions, the correct DE option is usually a short canonical phrase ("Vorfahrt gewähren", "Halteverbot"); a per-language glossary of those ~60 phrases lets the check require the glossary term (or one of its listed variants) to appear in the locale's correct option. Cheap, high-precision, low-recall.
4. **Source-hash provenance (the real structural fix).** Have `build_modules.py` (or the master file) stamp each translation with `source_hash = sha1(de.question + de.options)` at the time it was produced, and fail the build when a locale's `source_hash` no longer matches the current DE text. This turns "stale" from an invisible semantic property into a structural one: any DE edit invalidates its 11 translations until they are re-attested. It would have caught the incident deterministically, at build time, in milliseconds. This is a content-pipeline change and is out of scope for this ADR's test code, but it is the recommendation that most reduces the need for anything smarter.

The genuinely semantic check - "does the Hindi question describe the same sign as the German one?" - is a **content-equivalence** problem: back-translate or embed each locale entry and compare against DE, with a human review of low-similarity items. A separate ADR is being written on doing this with local LLMs. That layer, not E2E, is the answer to the incident; E2E's job is everything around it.

## Consequences

**Positive**
- One command proves, for all 4 driving modules x 12 languages, that an exam can be started, every drawn question renders with its full option set, the `core.json` key is exactly what the UI scores as correct, a deliberately wrong run is scored as wrong with the right "right answer" shown, a score/verdict appears, and no silent English fallback occurred.
- Reuses the existing Playwright install and flows; the three existing scripts can be ported incrementally (or left as-is) rather than rewritten.
- Sharding and per-test reporting make "which language broke" a one-glance answer instead of a first-failure abort.
- Clean upgrade path to WebKit/Firefox projects for RTL/iOS questions, and to Deploy-Preview URLs once a CI workflow exists.
- The pyramid below keeps the every-commit gate at seconds (JSON checks) and puts the ~15-minute browser matrix where it belongs (pre-deploy / nightly).

**Negative**
- Adds `@playwright/test` as a devDependency and a `playwright.config.mjs`; two test idioms coexist in the repo until the older scripts are ported.
- Exam-mode coverage is a sample by design. Someone reading a green run as "all 531 questions verified in the UI" would be wrong; the pool walk and the JSON layer are what cover the pool, and the README/script names must say so.
- Reading `state.exam.questions` through `page.evaluate` couples the test to an app-internal global. Mitigation: add a `data-question-id` attribute on `#exam-view` in a later app change and switch the test to it. The ADR does not make that change.
- The stale-locale class is explicitly **not** caught by this decision; it needs the provenance hash and/or the content-equivalence ADR. Shipping E2E first must not be read as "translation staleness is now tested".
- ~15 min of browser time per full run is a real cost with no CI runner today; until GitHub Actions exists the PO or an agent runs it locally before deploys, which is exactly the discipline `AGENTS.md` already asks for but does not enforce.
- Some checks (placeholder regex, DE-identical text) will produce a few false positives on legitimately identical short strings and on shared numerals; a small per-question allowlist file will be needed.

## Recommended test pyramid

| layer | what | tool | runtime | when |
|---|---|---|---|---|
| **1. JSON data integrity** | for every module: every `core.json` id present in every shipped locale; every entry has non-empty `question`, an `options` map whose keys are a superset of `correct`, non-empty option strings, no placeholder tokens (`TODO`, `TBD`, `lorem`, `{{`, `[[`, `undefined`, `null`), option-key set identical to DE, `correct` keys valid, non-DE text not byte-identical to DE above a length threshold, sign-number and numeric-token parity (proxies 1-2 above), `image_ref` file exists under `app/assets/signs/` | Node script, no browser (`scripts/check_locale_integrity.mjs`) | seconds | every commit; also as the first step of `build_modules.py`'s sanity pass if desired |
| **2. Content equivalence** | DE-vs-locale semantic similarity per question; provenance `source_hash` check; human review queue for low-similarity items | local LLM / embeddings (separate ADR), plus the build-time hash | minutes-hours | on translation rounds; hash check every build |
| **3. Full-UI E2E** | exam matrix (module x lang x {correct, wrong}); consent gate; module picker; pool walk through the detail view (sampled: every 10th question per language on PRs; full nightly / pre-deploy) | `@playwright/test`, Chromium, sharded | ~4 min sharded (exam) + ~10 min (full pool walk) | pre-deploy and nightly; PR-sized sample on every PR once CI exists |

Layer 1 catches structural drift; layer 2 catches the incident class; layer 3 catches "the app can't actually be used in this language". They overlap deliberately at the cheap end (layer 1 re-checks in JSON what layer 3 samples in the DOM) so that a red layer 3 nearly always has a precise layer-1 explanation.

## Implementation Notes

Concrete next steps, in order. Nothing below has been done; this ADR is the only file this round touched.

1. **Add the runner.** `npm i -D @playwright/test@1.62` (match the installed `playwright` 1.62.1 exactly; mismatched versions are a known foot-gun). `npx playwright install chromium`. Commit `playwright.config.mjs` with: `testDir: "tests/e2e"`, `use.baseURL: process.env.BASE_URL || "http://localhost:8080"`, `use.viewport: {width: 390, height: 844}`, `retries: process.env.CI ? 1 : 0`, `reporter: [["list"], ["html", {open: "never"}]]`, `timeout: 120_000` (one exam run), and a `webServer` entry that runs `scripts/dev-serve.sh 8080` when `BASE_URL` is unset (`reuseExistingServer: true`).

2. **Shared page helpers** in `tests/e2e/helpers/app.mjs`, extracted from `scripts/test_full_exam_badge.mjs`: `openApp(page, lang)` (context `locale` -> consent yes -> wait), `pickModule(page, examType, lang)` (label from `data/modules_manifest.json`, first scope option, intro skip), `startExam(page, mode)`, `drawnQuestionIds(page)` (`page.evaluate(() => state.exam.questions.map(q => q.id))`), `answerAndNext(page, keys)`, `readResults(page)`. Keep the sandbox-vs-laptop Chromium fallback logic out of tests entirely - the runner manages the browser.

3. **`tests/e2e/exam-matrix.spec.mjs`.** Matrix constants: `DRIVING_MODULES = ["fuehrerschein","motorrad","lkw","fuehrerschein_bus"]`, `LANGS = ["de","en","es","fr","it","pl","ru","uk","tr","ar","hi","zh"]`. For each pair, two tests: `correct run passes with zero review items` and `wrong run fails and lists every question with the key's right answer`. Both assert `state.contentLangFallback === null`, the per-question text/option assertions, and the placeholder regex on rendered text. Tag them `@exam` so they can be selected with `--grep @exam`.

4. **`tests/e2e/pool-walk.spec.mjs`.** Per (driving module, lang): open the detail view on the first list card, iterate with the detail "next" control across `filteredQuestions()` (all topics, all classes of the chosen scope), asserting question/option text non-empty and matching the locale file for the question id read from `state.detailIndex` / `filteredQuestions()`. Env `POOL_STRIDE=10` samples every 10th question for PR runs; `POOL_STRIDE=1` is the full walk. Tag `@pool`.

5. **`scripts/check_locale_integrity.mjs`** (layer 1, no browser): implement the checks in the pyramid table; exit non-zero with a per-module, per-locale, per-id list. Add an allowlist file `data/locale_check_allowlist.json` for legitimate DE-identical strings. Consider calling it from `data/build_modules.py`'s sanity section so a broken locale never reaches `app/data/`.

6. **`package.json` scripts** (names proposed; `dev` and `test:storage-consent` stay):
   - `"test:data": "node scripts/check_locale_integrity.mjs"`
   - `"test:e2e": "playwright test"`
   - `"test:e2e:exam": "playwright test --grep @exam"`
   - `"test:e2e:pool": "POOL_STRIDE=1 playwright test --grep @pool"`
   - `"test:e2e:pool:sample": "POOL_STRIDE=10 playwright test --grep @pool"`
   - `"test:e2e:shard": "playwright test --shard=$SHARD"` (used by CI as `SHARD=1/4`)
   - `"test:e2e:report": "playwright show-report"`
   - `"test:all": "npm run test:data && npm run test:e2e:exam && npm run test:e2e:pool:sample"`

7. **Port the existing scripts** (optional, second round): `test_storage_consent.mjs` -> `tests/e2e/storage-consent.spec.mjs`; `test_full_exam_badge.mjs` keeps its standalone form because it needs a real signing function and a live JWKS - it is a deploy-verification script, not a PR test.

8. **Small app follow-ups to reduce test coupling** (separate, tiny PRs; not part of this ADR's change set): `data-question-id="<id>"` on `#exam-view` and `#detail-view`; a visible "content shown in English - <lang> not translated yet" notice driven by `state.contentLangFallback` (the E2E test asserts on the internal flag until then); optionally a `?zcTestDraw=<ids>` query hook honoured by `drawExamQuestions()` only when the page is served from localhost, to make an exam run deterministic when a specific question must be reproduced.

9. **CI (when the repo gets one).** `.github/workflows/e2e.yml`: job `data` runs `npm run test:data` on every push (seconds); job `e2e` runs on PRs and on `workflow_dispatch`, matrix `shard: [1/4, 2/4, 3/4, 4/4]`, `npx playwright install --with-deps chromium`, `npm run test:e2e:shard`, uploads `playwright-report/` on failure. When Netlify Deploy Previews are enabled for the GitHub repo, set `BASE_URL` to the preview URL (from the deploy-status check) so the same suite runs against the real CDN/headers. Keep `netlify.toml`'s `command = "true"` - Netlify's build is not the place for browsers. A nightly `schedule:` run executes `test:e2e:pool` in full.

10. **Provenance hash (layer 2, structural half).** In `data/build_modules.py`, when splitting a master file, compute `sha1(de.question + json(de.options))` per id and compare against a `source_hash` stored next to each non-DE translation in the master; fail the build on mismatch, with a `--reattest <lang>` flag for translation rounds. Design this alongside the local-LLM content-equivalence ADR so both write to the same per-id review ledger.

## Related

- `scripts/test_full_exam_badge.mjs`, `scripts/test_storage_consent.mjs`, `scripts/test_hinweisgeberschutz_smoke.mjs` - the existing Playwright flows this decision builds on.
- `data/build_modules.py` (sanity checks at the end of `main()`), `docs/fuehrerschein-translation-completeness-plan.md`.
- `BACKLOG.md` DN-40 (locale-fallback crash), DN-41 (sign QA via real screenshots), DN-89/DN-90 (consent gate + first Playwright regression test).
- ADR-0002 (planned): content-equivalence checking of translations with local LLMs.
