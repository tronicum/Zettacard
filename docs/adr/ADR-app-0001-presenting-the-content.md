# ADR-app-0001 — Presenting the content

**Status:** Accepted, 2026-09-06
**Repo:** `Zettacard`
**Related:** `zettacard-kb` ADR-0001 through ADR-0005; this repo's ADR-0003 (mobile layout: no `@media`, `--tap-min`, `dvh`)

## Context

The KB is now the content master (KB ADR-0001). It holds 35 modules, ~2,493 questions, the driving family in 18 locales, compliance in 15, and two `fun_translation` modules in `de`/`en`. Content reaches this repo through `src/export_to_zettacard.py` in the KB, which writes what `build_modules.py` already expects. The app is an offline-first PWA: static files, no build step, Netlify at zettacard.de, a service worker that runtime-caches lazily.

Measured from `app/app.js` on disk today:

| Fact | Consequence |
|---|---|
| 16 locale-keyed string dictionaries | UI strings are content-shaped but live in app code |
| 15 of them carry 12 locales; `PRACTICE_QUIZ_STRINGS` carries 2 (`de`, `en`) | Ten live locales see the wrong language on the practice quiz. Live defect. |
| Six locales exist in data with no UI: `bar`, `fa`, `ro`, `el`, `hr`, `pt` | The app is the thing limiting which locales exist |
| `UI_STRINGS` gates existence: `detectLang` and the saved-language restore test membership | A locale absent from `UI_STRINGS` is unreachable regardless of data |
| `RTL_LANGS = new Set(["ar"])` | `fa` renders LTR. `he` and `apc` are planned. |
| `app.html` language selector has 12 options | Same gate, second place |
| `build_modules.py` runs `shutil.rmtree()` on `locales/` before regenerating from `fs_locales` / `compliance_locales` | A locale not in those arrays is deleted with nothing to rebuild from. Romanian was nearly lost. |
| Language selector lives inside `#app-menu` | Switching language left the menu open under `setInertBehindDialog(true)`; nothing clickable, every non-German locale, staging |
| `styles.css` has zero `@media` queries | Kept, per this repo's ADR-0003 |

The KB knows about `review_status`, citation grade, drift, `tier`, `module_kind`, licence, the identification banner, and defects. The app shows none of it.

## Decision

**The app presents what the KB knows and stops being the thing that limits which locales exist.** Specifically:

1. UI strings become content: authored and translated in the KB, exported like questions, loaded by the app at runtime. `app.js` keeps a `de` and `en` fallback inline and nothing else.
2. Locale existence is derived from the exported data, not from `UI_STRINGS` membership.
3. The language picker leaves `#app-menu` and becomes a first-class control that is not a dialog.
4. Verification state is surfaced as a quiet, consistent label with one place to learn more; it never filters.
5. `module_kind` is visible on every module card and every question screen.
6. RTL is a data property of a locale, not a hard-coded set.
7. Adding a locale follows a written checklist across both repos, enforced by a build check.
8. The cache strategy splits into core, per-locale and media layers so more locales do not mean more bytes for everyone.

## The locale gap and where UI strings belong

UI strings are an awkward middle case. They are content-shaped — a `{locale: string}` map, translated, reviewable, subject to the same "faithful translation of a wrong source" rule as everything else — but they live in app code because that is where they were convenient.

**Position: they belong in the KB.** Reasons:

- The KB already has the machinery: locale cells, `tier`, `review_status`, provenance, hashes, defects. Every argument for moving questions into the KB applies to "Nächste Frage" too.
- The KB is where the 18-locale generation pipeline runs. Six locales exist in data and not in the UI *because* the UI is outside that pipeline.
- Hand-maintaining 16 dictionaries × 18 locales × N keys in a JavaScript file is how `PRACTICE_QUIZ_STRINGS` ended up with two locales.

Mechanism:

- KB adds a pseudo-module `content/_ui/` with `strings.jsonl`, one record per string key (`kb_id = _ui:<dictionary>.<key>`), `text.<loc>.question` holding the string. Options are empty. `module_kind: "ui_strings"` is added to the KB enum (an additive change to ADR-0001, recorded here and mirrored in the KB's ADR index).
- `export_to_zettacard.py` writes `app/locales/<loc>/ui.json` per locale, flat `{ "<dictionary>.<key>": "…" }`.
- `app.js` loads `locales/<lang>/ui.json` on language selection, falls back key-by-key to `en` then `de`, and exposes `t(dict, key)`. The 16 dictionaries are collapsed into a single lookup; the dictionary name becomes a key prefix.
- `UI_STRINGS` and its 15 siblings are reduced to the inline `de` and `en` fallback needed before any fetch completes, and to nothing else. They stop gating existence.
- Locale existence is `app/locales/index.json`, written by the export, listing every locale with `name`, `native_name`, `dir` (`ltr`/`rtl`), `tier` and a `complete` flag (true when every UI key has a cell). `detectLang` and the saved-language restore test against that list.

**The `PRACTICE_QUIZ_STRINGS` defect is fixed first, in 0.11, by hand,** with the 12 live locales added directly to the dictionary, because ten live locales are seeing the wrong language now and the KB mechanism is a 0.13 deliverable. It is logged as a defect in the KB (`data/defects/_ui.jsonl`) so the cascade rule applies when the strings move.

Until 0.13, a locale absent from `UI_STRINGS` remains unreachable. That is accepted for two minor releases and no longer.

## The language picker

The selector moves out of `#app-menu` to the app header, visible on every screen including the first one, as a native `<select>` styled to `--tap-min` height, or a button that opens a **popover** (`popover` attribute, not `<dialog>`, not the menu overlay). Requirements:

| Requirement | Why |
|---|---|
| Visible before any German is readable | A learner who cannot read "Menü" cannot find a picker inside the menu |
| Labelled by a language icon plus the current locale's *native* name | No text in a language the learner may not read |
| Keyboard-reachable: first or second tab stop from page load | Accessibility, and the only way to recover if pointer events are broken |
| Not a dialog, not inside any element that `setInertBehindDialog` touches | This is the bug-class removal |
| Changing language closes nothing and opens nothing; it re-renders the current screen in place | Language change must never alter navigation state |
| Options listed in each language's own native name, not translated into the current UI language | Same reason as the label |
| Sourced from `locales/index.json`, not hard-coded in `app.html` | Removes the second existence gate |

Why this is a bug-class removal rather than a relocation: the failure was that a state change (language) happened inside a modal context (the menu with inert applied behind it), and the code path that re-rendered on language change did not know it was inside a modal. Any control inside any modal is exposed to the same class. Moving the control to a non-modal surface, and making language change a pure re-render with no navigation side effects, means there is no modal context for it to be inside. A regression test opens the picker, changes language, and asserts that no element has `inert` and that a known button on the underlying screen is clickable.

`setInertBehindDialog` itself gains a guard: it refuses to set inert if the active element is outside the dialog, and logs. That is a defence, not the fix.

## Presenting verification state

KB ADR-0003 requires the build to surface `review_status`, citation grade and citation drift as visible labels and forbids filtering on them. Zero cells are `approved`. Every citation is `unverified`. The honest state of the app today is "nothing here has been reviewed by a native speaker", and that must be visible somewhere a learner actually looks, without shouting on every card and without making the app feel broken.

The design, in three layers:

**Layer 1 — one line on the module card and the module intro.** A single short status line under the module title, in the UI language, from a fixed vocabulary:

| KB state (per locale, aggregated over the module) | Line shown |
|---|---|
| All cells `approved` | "Reviewed" |
| Mix | "Partly reviewed — 120 of 531 reviewed" |
| None `approved`, any `auto_approved` | "Machine-checked, not yet reviewed by a person" |
| None `approved`, none `auto_approved` | "Not yet reviewed" |
| Module's `legal_review_status` not reviewed | appended: " · rights not legally reviewed" |

This is where a learner decides whether to start. It is calm, factual, and once per module.

**Layer 2 — a small mark on the question card, never a sentence.** In the card's footer, next to the question number, a single glyph with a `title`/`aria-label`:

| Cell state | Mark |
|---|---|
| `approved` | none |
| `auto_approved` or `pending` | a hollow circle, `aria-label="Not yet reviewed"` |
| `rejected` (still publishable under ADR-0003) | a filled circle, `aria-label="Flagged for correction"` |
| open defect on this cell or cascaded from `de` | a filled circle, same label, defect id in the `title` |
| citation grade `law` and drift detected | a small paragraph-sign glyph, `aria-label="Cited law may have changed"` |
| locale `tier` is `translation` (not an official exam language) | a small "study aid" text tag, once, in the card header |

The mark is the same size as the question number and the same colour as secondary text. It does not use red. Today it appears on every card, which is the truth. When the review count moves, it disappears from reviewed cards, which is the incentive.

**Layer 3 — one screen that explains it.** Tapping any mark, or the Layer 1 line, opens a non-modal panel (same popover mechanism as the picker) titled "About this content" showing: locale tier in plain words, `review_status` of this cell, who or what generated it and when (`provenance.locales.<loc>.generator`, `.at`), whether the German source it was made from is still the current one (`against_source_hash == hashes.source_hash`), any open defect ids, the module licence with its URL, and for translated cells: "The official exam is in German. This translation is a study aid." That last sentence is mandatory for `tier: translation` cells in `exam_prep` modules and comes from the KB, not the app.

Nothing in any layer filters. There is no "hide unreviewed" toggle. Any PR that adds one is a violation of KB ADR-0003 and this ADR.

The build produces per-module, per-locale aggregates for Layer 1 in `build_modules.py` from `review_status` and `legal_review_status`; `app.js` does no counting at runtime.

## Module kinds and identification

| `module_kind` | On the module card | On every question screen | Licence line |
|---|---|---|---|
| `exam_prep` | "Exam preparation" tag | none beyond Layer 2 marks | CC BY-NC-SA 4.0 in "About this content" |
| `compliance` | "Training" tag | none | CC BY-NC-ND 4.0, with "may not be redistributed in modified form" |
| `fun_translation` | The mandatory `identification` banner from `module.json`, in the UI language if it has one, else `en`, else `de` — **not** a tag | The banner's first sentence as a persistent card header line | As `module.json` states |

The `fun_translation` banner is rendered from `module.json` verbatim and cannot be suppressed by a preference. These modules are grouped under their own heading in the module picker, never interleaved with the German licence modules. The module picker groups by `module_kind` first, then by the existing order.

## RTL

`RTL_LANGS` is deleted. `dir` comes from `locales/index.json` per locale, written by the KB export from the locale registry. On language change, `document.documentElement.dir` and `lang` are set from that entry. `fa` is `rtl` today; `he` and `apc` will be `rtl` when added; nothing in `app.js` needs to change for them.

Layout consequences, checked once and covered by a visual test in the two RTL locales that exist: option key labels (`a`–`d`) stay on the reading-start side; the language picker stays at the reading-end side of the header; progress bars use logical properties (`inset-inline-start`, `margin-inline`), which `styles.css` adopts throughout in 0.12 — a mechanical change, no `@media` involved.

## Media playback

When the 40,711 objects exist (KB ADR-0002; 0 today):

- The export writes `media/manifest.json` per module listing, per `kb_id` and locale, the UUIDs for `audio/opus`, `audio/aac` and `subtitle/srt`. The app never derives a UUID itself; it reads the manifest.
- `<audio>` with two `<source>` children: `audio/ogg; codecs=opus` first, `audio/mp4` second. The browser picks. No user-agent sniffing. Safari before 18.4 falls through to AAC as intended.
- Subtitles: SRT is converted to WebVTT by the KB export at write time (`.vtt` next to `.srt`, same UUID stem) because `<track>` accepts only VTT. The app uses `<track kind="subtitles" srclang="<loc>">`.
- Media is fetched on demand and runtime-cached by the service worker under a separate cache name (`media-v<N>`) with an LRU cap (proposal: 200 MB, configurable in `service-worker.js`). Media is never precached. A learner who never presses play never downloads a byte of it.
- A "download this module's audio for offline use" button per module and locale is a 0.20 deliverable, storage-consented via the existing `STORAGE_CONSENT_STRINGS` flow.

## The add-a-locale checklist (both repos, in order)

This exists because `build_modules.py` deletes what it cannot rebuild. Do the steps in this order; nothing is deployed until step 9.

| # | Repo | Step |
|---|---|---|
| 1 | KB | Add the locale to the locale registry (`config/locales.json`: code, native name, `dir`, `tier` default). |
| 2 | KB | Generate or import cells for at least `content/_ui/` and one module. Cells land `pending`. |
| 3 | KB | Run `export_to_zettacard.py`; confirm `app/locales/index.json` lists the locale and `app/locales/<loc>/ui.json` exists. |
| 4 | Zettacard | Add the locale to `fs_locales` and/or `compliance_locales` in `build_modules.py`. **This is the rmtree trap. Do this before running the build.** |
| 5 | Zettacard | Run `build_modules.py`. Confirm `locales/<loc>/` exists for every module that has cells. |
| 6 | Zettacard | Run the build check (0.15+): every locale in `locales/index.json` must appear in the arrays, and vice versa. The build fails otherwise. |
| 7 | Zettacard | Open the app with `?lang=<loc>`, confirm the picker shows the native name, confirm `dir` is right, confirm Layer 1 says "Not yet reviewed". |
| 8 | Zettacard | Run the inert regression test and the RTL visual test if applicable. |
| 9 | Zettacard | Bump the service-worker cache version for the core cache only. Deploy to staging. Then production. |
| 10 | KB | Record the locale as `present` in the modules' `locales` block via the normal pipeline; no manual edit. |

Until step 6 exists, step 4 is enforced by a code-review checklist item and by the person doing it reading this table.

## Offline and cache consequences

No build step is preserved. More locales means more data. The service worker moves from one runtime cache to three:

| Cache | Contents | Strategy |
|---|---|---|
| `core-v<N>` | HTML, `app.js`, `styles.css`, `locales/index.json`, inline `de`/`en` fallback | Precache on install; version bump invalidates |
| `locale-<loc>-v<N>` | `locales/<loc>/ui.json` plus every module file for that locale that has been opened | Runtime, cache-first, populated lazily as today; a learner who uses one locale never fetches another |
| `media-v<N>` | Audio and VTT by UUID | Runtime, LRU-capped, never precached |

Switching language fetches `ui.json` for the new locale (small) and re-uses whatever module files are already cached for it. The first offline use of a new locale requires the learner to have opened the module once online, which is the current behaviour and is stated in the storage consent copy.

`build_modules.py` gains a per-locale size report so that a locale whose module files exceed a threshold is noticed at build time, not by a learner on a metered connection.

## Consequences

- `app.js` loses ~16 dictionaries and gains a loader and `t()`. The `de`/`en` inline fallback stays so the first paint never waits on a fetch.
- Six locales become reachable in 0.13 with no further app change per locale.
- The app shows, honestly, that nothing has been reviewed. That is uncomfortable and correct, and it is the visible pressure that gets reviewers engaged via the KB's CSV export (KB ADR-0005, 0.11).
- The language picker is one control that does one thing; the inert bug class cannot recur through it.
- `build_modules.py` grows a check that turns the rmtree trap into a build failure.
- Nothing here filters content. Nothing here adds a build step.

## Version roadmap 0.11 → 0.23

Current version is 0.10.1; target is 0.23.42. *(The PO's `0.10.01` normalises to `0.10.1` under semver; `0.23.42` is valid as written.)* Minor versions are bumped in step with `zettacard-kb`; the KB-side table is in KB ADR-0005, section "Version roadmap", and the two are maintained together.

| Minor | App delivers | KB counterpart (ADR-0005) |
|---|---|---|
| 0.11 | `PRACTICE_QUIZ_STRINGS` filled for all 12 live locales; language picker out of `#app-menu`; inert regression test | Shared record model; CSV export + Markdown dossier; `LICENSE.txt` and sidecar |
| 0.12 | `fa` rendered RTL (interim: add to `RTL_LANGS`); logical CSS properties; verification labels (Layers 1–3) behind a query flag | CSV import → proposals; `kb promote`; CSV round-trip in CI |
| 0.13 | `locales/index.json` and `ui.json` loading; `UI_STRINGS` stops gating; `bar fa ro el hr pt` reachable; `RTL_LANGS` deleted | `content/_ui/strings.jsonl` exported for 18 locales |
| 0.14 | Verification labels on by default; `module_kind` tags and `fun_translation` banner; picker grouped by kind | GIFT export/import; Moodle XML export |
| 0.15 | Build check: `index.json` ⇔ `fs_locales`/`compliance_locales`; per-locale size report | Moodle XML import; GIFT and Moodle round-trip |
| 0.16 | `he` added end to end via the checklist as the proving run | QTI 2.1 export |
| 0.17 | Three-cache service worker; storage consent copy updated | Anki export/import |
| 0.18 | Compliance completion screen aligned with SCORM lesson status semantics | SCORM 1.2 package |
| 0.19 | — (app holds; patches only) | xAPI spec |
| 0.20 | Audio playback with Opus/AAC sources, VTT tracks, `media-v<N>` cache, per-module download | `--with-media`; first real objects on SSD |
| 0.21 | `apc` locale via the checklist | H5P and Aiken export |
| 0.22 | "Known issue" mark from defect ids in "About this content" | Defect history in sidecar |
| 0.23 | Stabilisation; `0.23.x` patches only | Stabilisation; sidecar schema frozen at v1 |

## Follow-up work

- Write the `locales/index.json` schema and the `ui.json` key naming rule (`<dictionary>.<key>`, lower snake) before 0.13; the KB export and the app loader both validate against it.
- Decide the exact glyphs for Layer 2 with the PO on a real phone at `--tap-min`; the `aria-label` text is fixed here, the glyph is not.
- Confirm the LRU cap for `media-v<N>` against real object sizes once any exist.
- The `?lang=` query parameter used in the checklist must not persist into the saved-language preference without the learner choosing it in the picker; specify this in 0.11.
- Add the "Not yet reviewed" copy to `content/_ui/` as the first strings, so that the label itself is translated by the same pipeline it describes.
