# AGENTS.md — working agreement for anyone (human or AI) contributing to Zettacard

This file is the entry point for any agent — Claude, another model, or a human contributor — picking up work in this repo. Read this before touching anything.

## What this project is

Original, openly-licensed learning content and tooling for German exam prep and workplace-compliance training, offered as an offline-first PWA in 15 languages (12 as of the original writing; `bar`, `fa`, `ro` were added 2026-09-05 — always take the live count from `data/build_modules.py`'s `fs_locales`/`compliance_locales`, not from prose in this file). Currently 8 modules: **Fuehrerschein** (Klasse B/BE driving theory), **Motorrad**, **LKW**, **Angelschein** (fishing license), and 4 workplace-compliance modules — **Datenschutz** (GDPR), **Arbeitssicherheit** (occupational safety), **KI-Verordnung** (EU AI Act), **IT-Sicherheit**. All modules share the same fact-layer/text-layer content schema and the same 12-locale requirement. Not a clone of any official Fragenkatalog or compliance-training vendor's material — see `docs/README_pilot.md` and the license rationale below for why.

## Non-negotiable constraints

Read these before generating or editing any content — they came out of real legal analysis, not arbitrary preference:

1. **Never source or paraphrase from the official Fragenkatalog** (current or old/"leaked" editions), or from any third-party exam-prep or compliance-training company's text. Generate original content from primary legal sources (StVO/StVZO/FeV, GDPR, ArbSchG, EU AI Act, BSI/ISO standards, etc.) and from standardized, law-published sign specs (StVO Anlage 1-4). If you're unsure whether a phrasing is "too close" to a known commercial product, flag it in the card rather than guessing.
   - **Visual-accuracy fallback references, PO-approved 2026-08-09, updated 2026-08-21**: for checking whether a *sign icon's own shape/color/pictogram* is drawn correctly (not question content), prefer StVO Anlage 1-4 itself first (it's the actual law), then Wikimedia Commons' per-sign SVGs indexed via [Bildtafel der Verkehrszeichen in der Bundesrepublik Deutschland seit 2017](https://de.wikipedia.org/wiki/Bildtafel_der_Verkehrszeichen_in_der_Bundesrepublik_Deutschland_seit_2017) — confirmed 2026-08-21 (PO-checked the Commons license tag directly) that these are tagged **public domain**, § 5 Abs. 1 UrhG (official work *with* regulatory content — these SVGs render Anlage 1-4 StVO itself, not someone's copyrighted interpretation of it), then the official ADAC "Verkehrszeichen in Deutschland" brochure (already used for the DN-46/DN-47 sign-icon rounds, still useful as a secondary cross-check); a commercial driving-theory site's own sign-catalog page (e.g. ARAL's Theorietrainer) may be used as a visual-only fallback when a sign isn't clearly covered by any of those. Because the Commons SVGs are themselves public domain (unlike ADAC's brochure, which is ADAC's own copyrighted rendering), a faithful 1:1 redraw matching one exactly carries no derivative-work risk the way tracing ADAC's specific artwork would — but as of 2026-08-21 this project still hand-draws its own sign SVGs in `assets/generate_signs.py` rather than importing the Commons files directly; direct import (replacing hand-drawn icons with the actual Commons SVG files) is a real, not-yet-decided option, tracked as a `BACKLOG.md` item — see `app/legal/quellen.html`'s Wikimedia Commons row for the sourcing note either way. Never read, copy, or paraphrase any reference site's question text, explanations, or wording into this project's content — that remains squarely inside this constraint's ban on third-party exam-prep company text, no exception. The goal stated by the PO: this project's own content should be best-in-class, not a derivative of any reference.
2. **Track legal changes, not proprietary catalog changes.** When source law/regulation amendments or official exam-format changes are published, that's fair game to update content against. Don't design pipelines that sync against someone else's compiled catalog.
3. **Every content file ships with the license already attached** — `license`/`license_note` field in JSON meta + repo-root `LICENSE.md`. **CC BY-NC-SA 4.0 is the default for content we author, not a universal blanket** — `LICENSE.md` itself already carves this out ("does not automatically cover any third-party assets added later... which would carry their own terms if not produced by us"). When a module or asset ingests third-party material under different terms (a CC BY-SA corpus, a public-domain government work, a Licence-Ouverte source, a Wikimedia Commons image, etc.), that module/asset's own `license`/`license_note`/`attribution` field must state its *real* license, even if that means it diverges from the rest of the app — never silently relabel it as CC BY-NC-SA 4.0 to keep things uniform. This has already happened once (`sportboot_binnen`/`sportboot_see`'s `attribution` field crediting MIT-licensed tooling + an official ELWIS Fragenkatalog) and is already a planned, explicit decision for a second case (the France/Switzerland boating modules shipping under CC BY-SA 4.0 instead of the default — see `TODO.md` item 5). Record every such source in `app/legal/quellen.html`'s per-source table (body/source, licence, note — see its existing "Switzerland & France (boating licence, planned)" section for the pattern) so licensing provenance stays visible in one place, not just buried in a JSON `meta` block. Don't remove or weaken any of this without an explicit PO decision.
4. **Content is not legally reviewed by a professional.** Every batch must carry a `legal_review_status` field and get flagged as such in its card until a real review happens. Don't silently upgrade this status.
5. **Multilingual by construction, every locale the build declares, no exceptions.** New content always uses the fact-layer/text-layer schema (see `data/generate_pilot.py` for the reference shape) and must ship with every locale in `build_modules.py`'s locale lists populated from the start — as of 2026-09-05 that is `de, en, uk, pl, ar, zh, hi, tr, fr, ru, es, it` plus `bar, fa, ro`
   - **Two tiers, and the difference is legal, not cosmetic.** For the driving-licence exam, 12 languages (en, fr, el, it, pl, pt, ro, ru, hr, es, tr, and Modern Standard Arabic) are *official exam languages*: a candidate can sit the real Theorieprüfung in them, so our translation is a rehearsal of the actual exam paper and must match German exam register exactly. Every other locale (bar, fa, he, apc, ja, ko, …) is a **study aid** — the learner still sits the exam in German. Study-aid locales may keep the German term alongside the translation; official-language locales may not invent terminology. Confirmed against ADAC and TÜV/DEKRA sources 2026-09-05.
   - Whatever the tier, never hardcode single-language question objects, and never land a new UI string, topic label, or landing-page section in only DE/EN "for now." This project has repeatedly had to go back and fill locale gaps (missing `UI_STRINGS`/`TOPIC_LABELS` translations, a DE/EN-only landing page, an 8-question DE-wording desync from the other 10 locales) — treat a locale/coverage check (`npm run check:data`, or a grep for empty/missing keys across every locale file) as part of verification before calling anything content- or UI-string-related done, not an afterthought.
6. **Offline-first.** Output stays as flat, static JSON bundles suitable for service-worker precaching. No feature should require a live backend call to serve content. See "Offline architecture" below for the current shape.

## Where content lives, and which repo is the master (changed 2026-09-06)

**`../zettacard-kb` is the content master.** Content is authored, fixed and
versioned there. This repo builds *from* it and publishes. That is a reversal of
how it worked until 2026-09-06 — do not follow older instructions saying otherwise.

**The rules for all of this live in [`data-rules.md`](data-rules.md)**, which is
byte-identical in both repos. Read it before touching content, sources, review
status, hashing, locales or media. It covers: which repo is master; the
HugoFara/boating-licence reference architecture the PO named (read the actual
repo, not a paraphrase); source registration and `law`/`reference`/`unverified`
grading; the review gate (`pending` -> `approved`, and only approved content is
export-eligible); the three separate meanings of "verified"; the `source_hash`
recipe that must not drift between the repos; locale tiers; the non-literal
distractor convention; and UUID-referenced media on the SSD.

The three things that bite most often, repeated here so no one can miss them:

1. **A content fix goes into `zettacard-kb`.** `Zettacard/data/` and
   `Zettacard/app/data/` are both generated; a fix applied there is lost work.
2. **Nothing publishes unless a human moved it to `approved`** (or a deterministic
   generator declared `auto_approved`).
3. **"Verified" is three unrelated things** — human review, source freshness, and
   translation currency. Never report one as if it covered another.

## Repo layout

- `app/` — the actual PWA, deployed as-is (no build step). `index.html` is the marketing landing page; `app.html`/`app.js`/`styles.css` are the app itself; `service-worker.js` handles offline caching; `manifest.json` is the PWA manifest. `app/data/<exam_type>/{core.json, locales/*.json}` is the **runtime** content the app fetches — a generated artifact, not hand-edited (see below). `app/assets/signs/*.svg` are the rendered sign icons; `app/.well-known/jwks.json` publishes the public key for verifying signed completion credentials.
- `data/` — editable master content, one or more source JSON files per module (e.g. `pilot_questions.json`, `angelschein_seed.json`, `*_pilot.json` for the workplace modules, plus assorted `batch*`/`i18n_*` files from incremental content/translation rounds). Content agents edit these files, not `app/data/`. `data/modules_manifest.json` declares which modules/classes/regions exist and their picker labels. **`data/build_modules.py` derives the runtime files** (`app/data/modules.json` + `app/data/<exam_type>/{core.json,locales/*.json}`) — run `python3 build_modules.py` from within `data/` after ANY content or manifest change; the copy is not automatic.
- `assets/` — sign/diagram generation. **`assets/generate_signs.py` is a single, fully self-contained script that draws every StVO sign SVG** - it defines its own `SIGNS`/`BATCH_A_SIGNS`/`BATCH_B_SIGNS`/`BATCH_C_SIGNS`/`BATCH_D_SIGNS` dicts internally and merges them via `.update()`; `assets/batch_a_signs.py`/`batch_b_signs.py`/`batch_c_signs.py`/`batch_d_signs.py` are **dead, unused leftover files** - nothing imports them, confirmed 2026-08-09 (a misconception this doc itself carried until then - don't edit those files expecting it to affect generated output). `assets/build_sign_reference.py` is separate (derives the in-app Sign Reference catalog from already-verified question text, doesn't draw anything). Running `generate_signs.py` writes output to `assets/signs/*.svg` and (in the same run) `app/assets/signs/*.svg`. Because all sign-drawing logic lives in this one file, **parallel agents must not edit it concurrently** — fixes to multiple signs go one agent at a time, sequentially (see "Parallel vs. sequential work" below). `assets/generate_diagrams.py` similarly generates non-sign diagrams.
- `netlify/functions/sign-credential.js` — a Netlify Function that signs completion records as JWT credentials (see `docs/open-badges-signing-scoping.md` / `-setup.md`). Requires `ZETTACARD_SIGNING_PRIVATE_JWK` set in the Netlify UI, never committed.
- `scripts/` — Node and Python utilities: `generate_signing_keypair.mjs` (one-time keypair generation for the above), `test_sign_credential.js`, and the validation suite added 2026-09-05 — `check_data_integrity.py`, `translation_ledger.py`, `test_exam_matrix.mjs`, `layout_audit.mjs`, `serve-app.mjs` (see "Validation tooling").
- `docs/adr/` — architecture decision records: ADR-0001 (exam E2E strategy), ADR-0003 (mobile layout without media queries), ADR-0005 (TTS/accessibility), ADR-0006 (translation validation engine), plus ADRs on LLM translation QA and the local Ollama setup. Read the relevant one before re-litigating a decision.
- `netlify.toml` — deploy config: publishes `app/` with no build command (the `app/data/` tree is a pre-generated artifact, not something Netlify compiles), routes `netlify/functions/`, and sets cache headers (service worker never cached, `/data/*` always revalidated, `/assets/*` short-cached).
- `package.json` — exists solely so Netlify's function bundler can resolve the `jose` npm dependency used by `sign-credential.js`. The app itself (`app/`) remains build-step-free static files; this is not a "the project now has a build step" signal.
- `docs/` — process and content documentation: `README_pilot.md` (schema/content notes), `PERSONAS.md` (roles), `KANBAN.md` (board + workflow), plus various planning docs for specific efforts (translation completeness, signing setup, etc.).
- `BACKLOG.md` — the kanban board, in plain markdown (see `docs/KANBAN.md` for how to use it). Its `Done` entries are also a real record of project-specific lessons learned (verification gotchas, locale-gap patterns, sign-icon audit findings) — worth grepping before starting related work.
- `LICENSE.md` — CC BY-NC-SA 4.0, applies to generated content.

## Offline architecture (orientation only — see `app/service-worker.js` comments for full detail)

`service-worker.js` precaches only the small app shell plus the top-level module manifest (`app/data/modules.json`) at install time. Per-module, per-locale content files and sign/diagram SVGs are **not** precached by default — they're runtime-cached lazily as the fetch handler intercepts requests, so only the module(s)/locale(s)/image(s) a given visitor actually opens become available offline for them. On top of that, `app.js` has an explicit per-module "make available offline" button (`offlineAssetUrls()`/`checkOfflineReadiness()`/`prepareOffline()`) that proactively fetches a chosen module's current-language content plus every sign/diagram image its questions reference, so a visitor can prepare a module ahead of time instead of only getting offline coverage for whatever they happened to click on already — this works with ZERO changes to `service-worker.js` itself, since its existing fetch handler already caches any successful fetch it intercepts; adding proactive-fetch coverage for something new (e.g. a different asset type) only ever needs the URL added to `offlineAssetUrls()`. Keep this in mind before assuming "offline" means "everything is precached": adding a module or locale does not require touching the service worker's precache list, but a bug in the runtime-cache fetch handler affects offline availability project-wide.

## Working discipline: don't trust self-reported "looks right"

For anything visual or otherwise subjective (redrawn sign icons, UI/landing-page rendering, RTL layout, screenshots), do not accept a sub-agent's own claim that a fix "looks right" as the fix being done. Independently re-render/re-screenshot and actually look at the result yourself before closing it out. This project's own history (see `BACKLOG.md`) has caught agents being wrong on the same fix 2-3 rounds in a row this way (e.g. a sign-icon fix-agent repeatedly misjudging its own render of a horse-and-rider pictogram until an independent check caught it). Applies whether you're the one who made the fix or the one reviewing it — "the agent that did the fix says it's fine" is not itself verification.

## Lessons that cost us something (added 2026-09-05)

Each of these is a real failure from a real session, not a hypothetical. They are cheap to read and expensive to rediscover.

### Test the control a user must touch, not the state behind it

The worst bug of the 2026-09-05 session: after switching language, **nothing was clickable** for every non-German locale on staging. Three separate automated passes said the language switch worked. They were all wrong in the same way — they set `#lang-select` through `page.evaluate`, which changes the value without going through the menu the user must open. `#lang-select` lives inside `#app-menu`; switching left the menu open with `setInertBehindDialog(true)` still applied, so the whole app below it was inert. A human found it in seconds.

The rule: **if a real user has to open something, click something, or dismiss something to reach a control, the test has to do that too.** Setting the underlying state directly tests the model and skips the thing that actually broke. Where a test must bypass UI for speed, say so in a comment and keep at least one path that clicks for real.

The fix itself carries a second lesson, now commented in `wireStaticControls()`: close the menu via `history.back()`, not `closeAppMenu()`. `openAppMenu()` does a `pushState()`, and the `popstate` handler is what closes it — closing directly leaves the history entry behind, so the user's next Back press appears to do nothing.

### Agent self-reports are not evidence

Four parallel agents each reported full coverage of all 531 questions in their locale. All four had missed the same card (`zeichen-132`). I stamped them verified on their word; the ledger then said "verified" about four translations that did not exist. **An agent saying it checked everything is a claim, not a result.** Spot-check with a script that reads the files, over a key the agent had no reason to expect.

### Staleness is its own defect class, and no schema check finds it

When a German master is edited and its translations are not regenerated, every translation is still structurally perfect — right keys, right option count, right answer index — and semantically wrong. Schema validation passes. UI tests pass. The learner reads a question that no longer matches the German.

`scripts/translation_ledger.py` exists for exactly this: it stores a SHA-256 of the German cell (question + options + explanation + `correct`) per locale, so a German edit invalidates every stamped translation of it. `check` / `stamp` / `status`; state lives in `data/translation_state/<module>.json`. **After editing German, run `check` — do not assume the translations still hold.**

Do not try to detect staleness by comparing translated text to the German heuristically. That was measured: two rounds of deterministic content-equivalence heuristics produced 421 and then 715 false positives. It does not work, and the reason is the next item.

### Distractors are deliberately not literal translations

Wrong options are rendered freely so they read naturally in the target language. A checker that flags "this option is not an equivalent of the German" flags hundreds of *correct* entries. **Never "fix" a freely-rendered distractor into a literal one.** Only the correct option, the question stem, and the explanation carry an equivalence obligation.

### `build_modules.py` deletes before it rebuilds

It calls `shutil.rmtree()` on each built module's `locales/` and regenerates from `data/`. Two consequences:

1. **Edit masters in `data/`, never in `app/data/`.** A hand-edit to a runtime file is deleted on the next build with nothing to rebuild it from.
2. **A new locale must be added to `fs_locales` *and* `compliance_locales` before the build runs.** A locale that exists only as a generated file, and is not in those lists, is deleted permanently. Romanian was nearly lost this way. Both lists now carry a comment saying so.

Related: macOS AppleDouble files (`._bar.json`) landed in a locales directory and were picked up into `meta.locales` as if they were real locales. Filter `._*` when globbing locale files.

### Small-screen layout without media queries

`app/styles.css` deliberately contains **zero `@media` queries**, and ADR-0003 recommends keeping it that way. Small-screen fixes went in as a `--tap-min: 44px` token applied to tap targets, `dvh` alongside `vh` on `max-height` rules (iOS toolbar), and modal anchoring extended from `#app-menu` to all seven screen-like dialogs. Prefer a token or a fluid unit over a breakpoint.

### Defensive locale fallbacks in `app.js`

Every `SOME_STRINGS[state.lang]` lookup now ends in `|| SOME_STRINGS.en`. A locale that reaches the UI before its dictionary block exists used to throw and blank the screen. Keep the fallback when adding a new dictionary.

Note that `UI_STRINGS` is what *gates locale existence*: `detectLang` and the saved-language restore both check membership. Adding a locale to the data without a `UI_STRINGS` block makes it unreachable.

### Audio codec, if TTS work resumes

Safari plays Opus only in an **Ogg** container, only from 18.4, never WebM or MP4. Ship Ogg Opus plus an AAC/M4A fallback. (ADR-0005.)

### Environment

`device_bash` runs in a Linux VM (`aarch64`), not on macOS — there is no `xcrun`/`simctl` and no route to the Mac's localhost. iOS-simulator work has to be driven from the Mac itself. `@playwright/test`'s runner hung with zero output on a trivial spec in this environment; the working setup is the plain `playwright` library plus `scripts/serve-app.mjs` (`python3 -m http.server` failed silently as a `webServer`). Both are documented in the file headers.

## Validation tooling (this now exists — the older text below saying it doesn't is superseded)

- `npm run check:data` — `scripts/check_data_integrity.py`, 7 checks including master↔generated drift in both directions, answer-key resolvability per locale, and leaked authoring tokens. The token check is **case-sensitive** on `TODO|FIXME|XXX|TBD` on purpose: case-insensitive matched the Spanish word "todo" across the whole locale.
- `npm run check:translations` — `scripts/translation_ledger.py` staleness check (above).
- `npm run test:exam` — `scripts/test_exam_matrix.mjs`, 96 exam runs / ~19,900 assertions, proving the answer key in both directions (key passes, wrong answer fails).
- `npm run test:layout` — `scripts/layout_audit.mjs`.

Run `check:data` and `test:exam` before any deploy. None of these catch the class of bug in "test the control a user must touch" — a human still opens the app.

## Parallel vs. sequential work

Rule of thumb: **file-disjoint work can be parallelized, file-shared work must be sequential.**
- Safe to parallelize: separate content modules, separate docs, independent locale chunks — different agents/sessions touching different files.
- Must be sequential (one agent/session at a time, finish-then-next): anything touching `assets/generate_signs.py` (all sign icons live in this one file — concurrent edits clobber each other), and anything touching `app/app.js` (the single app-logic file — multiple UI features landing here in parallel will conflict). When in doubt about whether two pieces of work share a file, check before assuming it's parallelizable.
- Before any task large enough to need multiple sequential agent dispatches or a substantial architecture/UI change, check in with the PO on scope first rather than assuming — see the Workflow section below on who owns scope decisions.

## Roles

This project runs light scrumban with four personas: **Product Owner**, **Scrum Master**, **Developer**, **Student**. Full definitions in `docs/PERSONAS.md`. When you pick up a card, know which hat you're wearing — a Developer generating content should not also grade its own Student-review gate.

## Workflow (quick version, full detail in docs/KANBAN.md)

1. Pull the top card from `Ready` in `BACKLOG.md` (respect WIP limits).
2. Move it to `In Progress`, do the work as the Developer persona.
3. Validate before calling it done — run the checks in "Validation tooling" above (`check:data`, `check:translations`, `test:exam`, `test:layout`) plus, for anything visual, actually rendering/screenshotting it (see "Working discipline"). Add ad-hoc checks on top where a change has a property none of those cover; extend the existing scripts rather than starting a fifth one.
4. Move to `Student Review` — do a pass as the Student persona (does this read clearly, does it feel exam-realistic, is anything confusing).
5. Only after Student Review passes, move to `Done` and commit, referencing the card ID in the commit message.
6. Scrum Master role: keep `BACKLOG.md` tidy, enforce WIP limits, don't originate content decisions.
7. Product Owner role: decides what's next in `Ready`, writes/approves acceptance criteria, is the only one who can change scope, license terms, or the non-negotiable constraints above (in practice: that's Stefan, or an agent explicitly told to act as PO on his behalf).

## Commit conventions

`[<card-id>] <short summary>` — e.g. `[DN-3] Add multi-select question type to schema`. Keep commits scoped to one card where possible.

## Deploy (once work is committed and the PO wants it live)

1. If `data/` content or `data/modules_manifest.json` changed: `cd data && python3 build_modules.py` (regenerates `app/data/**`). If any StVO sign/diagram was touched: `python3 assets/generate_signs.py` (and `assets/generate_diagrams.py` if applicable) from the repo root — both write to `assets/` AND `app/assets/` in the same run, and `assets/build_sign_reference.py` if `app/data/fuehrerschein/sign_reference.json` needs regenerating too. Re-run these before committing, not after.
2. Commit and push to `main` on GitHub (`tronicum/Zettacard`) — proxy env vars must be unset for `git push` to work in this environment: `env -u https_proxy -u HTTPS_PROXY -u http_proxy -u HTTP_PROXY -u no_proxy -u NO_PROXY git push`.
3. Deploy to Netlify (site `zettacard`, siteId `b244f9b2-e45a-48c0-9f59-0405f587c213`) via the Netlify MCP connector's `deploy-site` operation, then run the `npx @netlify/mcp@latest --site-id ... --proxy-path "..."` command it returns (same unset-proxy-vars requirement as the git push).
4. Verify the live site, not just the deploy log: `curl` a changed data/asset file's live URL to confirm the new content actually served, and/or a live Playwright pass for anything UI-visible. A successful Netlify deploy message is not itself proof the change is live and correct.
5. Before step 2, run `npm run check:data` and `npm run test:exam`. A build that regenerates `app/data/**` can silently drop a locale (see "build_modules.py deletes before it rebuilds") — the drift check is what catches it.
6. Per standing PO instruction: don't deploy every small change automatically — deploying is a deliberate step, not an implicit part of "done."
