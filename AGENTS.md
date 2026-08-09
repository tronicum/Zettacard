# AGENTS.md — working agreement for anyone (human or AI) contributing to Zettacard

This file is the entry point for any agent — Claude, another model, or a human contributor — picking up work in this repo. Read this before touching anything.

## What this project is

Original, openly-licensed learning content and tooling for German exam prep and workplace-compliance training, offered as an offline-first PWA in 12 languages. Currently 8 modules: **Fuehrerschein** (Klasse B/BE driving theory), **Motorrad**, **LKW**, **Angelschein** (fishing license), and 4 workplace-compliance modules — **Datenschutz** (GDPR), **Arbeitssicherheit** (occupational safety), **KI-Verordnung** (EU AI Act), **IT-Sicherheit**. All modules share the same fact-layer/text-layer content schema and the same 12-locale requirement. Not a clone of any official Fragenkatalog or compliance-training vendor's material — see `docs/README_pilot.md` and the license rationale below for why.

## Non-negotiable constraints

Read these before generating or editing any content — they came out of real legal analysis, not arbitrary preference:

1. **Never source or paraphrase from the official Fragenkatalog** (current or old/"leaked" editions), or from any third-party exam-prep or compliance-training company's text. Generate original content from primary legal sources (StVO/StVZO/FeV, GDPR, ArbSchG, EU AI Act, BSI/ISO standards, etc.) and from standardized, law-published sign specs (StVO Anlage 1-4). If you're unsure whether a phrasing is "too close" to a known commercial product, flag it in the card rather than guessing.
   - **Visual-accuracy fallback references, PO-approved 2026-08-09**: for checking whether a *sign icon's own shape/color/pictogram* is drawn correctly (not question content), prefer StVO Anlage 1-4 itself first (it's the actual law), then the official ADAC "Verkehrszeichen in Deutschland" brochure (already used for the DN-46/DN-47 sign-icon rounds); a commercial driving-theory site's own sign-catalog page (e.g. ARAL's Theorietrainer) may be used as a visual-only fallback when a sign isn't clearly covered by either. This is narrowly scoped: look at the pictogram to judge shape/color/proportion, same as ADAC's brochure is already used for ("verify against the official pictogram, draw an original simplified interpretation" — never trace/copy the specific artwork). Never read, copy, or paraphrase any of that site's question text, explanations, or wording into this project's content — that remains squarely inside this constraint's ban on third-party exam-prep company text, no exception. The goal stated by the PO: this project's own content should be best-in-class, not a derivative of any reference.
2. **Track legal changes, not proprietary catalog changes.** When source law/regulation amendments or official exam-format changes are published, that's fair game to update content against. Don't design pipelines that sync against someone else's compiled catalog.
3. **Every content file ships with the license already attached** — `license` field in JSON meta + repo-root `LICENSE.md` (CC BY-NC-SA 4.0). Don't remove or weaken it without an explicit PO decision.
4. **Content is not legally reviewed by a professional.** Every batch must carry a `legal_review_status` field and get flagged as such in its card until a real review happens. Don't silently upgrade this status.
5. **Multilingual by construction, all 12 locales, no exceptions.** New content always uses the fact-layer/text-layer schema (see `data/generate_pilot.py` for the reference shape) and must ship with `de, en, uk, pl, ar, zh, hi, tr, fr, ru, es, it` all populated from the start — never hardcode single-language question objects, and never land a new UI string, topic label, or landing-page section in only DE/EN "for now." This project has repeatedly had to go back and fill locale gaps (missing `UI_STRINGS`/`TOPIC_LABELS` translations, a DE/EN-only landing page, an 8-question DE-wording desync from the other 10 locales) — treat a locale/coverage check (grep for empty/missing keys across all 12 locale files, or an equivalent script) as part of verification before calling anything content- or UI-string-related done, not an afterthought.
6. **Offline-first.** Output stays as flat, static JSON bundles suitable for service-worker precaching. No feature should require a live backend call to serve content. See "Offline architecture" below for the current shape.

## Repo layout

- `app/` — the actual PWA, deployed as-is (no build step). `index.html` is the marketing landing page; `app.html`/`app.js`/`styles.css` are the app itself; `service-worker.js` handles offline caching; `manifest.json` is the PWA manifest. `app/data/<exam_type>/{core.json, locales/*.json}` is the **runtime** content the app fetches — a generated artifact, not hand-edited (see below). `app/assets/signs/*.svg` are the rendered sign icons; `app/.well-known/jwks.json` publishes the public key for verifying signed completion credentials.
- `data/` — editable master content, one or more source JSON files per module (e.g. `pilot_questions.json`, `angelschein_seed.json`, `*_pilot.json` for the workplace modules, plus assorted `batch*`/`i18n_*` files from incremental content/translation rounds). Content agents edit these files, not `app/data/`. `data/modules_manifest.json` declares which modules/classes/regions exist and their picker labels. **`data/build_modules.py` derives the runtime files** (`app/data/modules.json` + `app/data/<exam_type>/{core.json,locales/*.json}`) — run `python3 build_modules.py` from within `data/` after ANY content or manifest change; the copy is not automatic.
- `assets/` — sign/diagram generation. **`assets/generate_signs.py` is a single, fully self-contained script that draws every StVO sign SVG** - it defines its own `SIGNS`/`BATCH_A_SIGNS`/`BATCH_B_SIGNS`/`BATCH_C_SIGNS`/`BATCH_D_SIGNS` dicts internally and merges them via `.update()`; `assets/batch_a_signs.py`/`batch_b_signs.py`/`batch_c_signs.py`/`batch_d_signs.py` are **dead, unused leftover files** - nothing imports them, confirmed 2026-08-09 (a misconception this doc itself carried until then - don't edit those files expecting it to affect generated output). `assets/build_sign_reference.py` is separate (derives the in-app Sign Reference catalog from already-verified question text, doesn't draw anything). Running `generate_signs.py` writes output to `assets/signs/*.svg` and (in the same run) `app/assets/signs/*.svg`. Because all sign-drawing logic lives in this one file, **parallel agents must not edit it concurrently** — fixes to multiple signs go one agent at a time, sequentially (see "Parallel vs. sequential work" below). `assets/generate_diagrams.py` similarly generates non-sign diagrams.
- `netlify/functions/sign-credential.js` — a Netlify Function that signs completion records as JWT credentials (see `docs/open-badges-signing-scoping.md` / `-setup.md`). Requires `ZETTACARD_SIGNING_PRIVATE_JWK` set in the Netlify UI, never committed.
- `scripts/` — small Node utilities: `generate_signing_keypair.mjs` (one-time keypair generation for the above) and `test_sign_credential.js`.
- `netlify.toml` — deploy config: publishes `app/` with no build command (the `app/data/` tree is a pre-generated artifact, not something Netlify compiles), routes `netlify/functions/`, and sets cache headers (service worker never cached, `/data/*` always revalidated, `/assets/*` short-cached).
- `package.json` — exists solely so Netlify's function bundler can resolve the `jose` npm dependency used by `sign-credential.js`. The app itself (`app/`) remains build-step-free static files; this is not a "the project now has a build step" signal.
- `docs/` — process and content documentation: `README_pilot.md` (schema/content notes), `PERSONAS.md` (roles), `KANBAN.md` (board + workflow), plus various planning docs for specific efforts (translation completeness, signing setup, etc.).
- `BACKLOG.md` — the kanban board, in plain markdown (see `docs/KANBAN.md` for how to use it). Its `Done` entries are also a real record of project-specific lessons learned (verification gotchas, locale-gap patterns, sign-icon audit findings) — worth grepping before starting related work.
- `LICENSE.md` — CC BY-NC-SA 4.0, applies to generated content.

## Offline architecture (orientation only — see `app/service-worker.js` comments for full detail)

`service-worker.js` precaches only the small app shell plus the top-level module manifest (`app/data/modules.json`) at install time. Per-module, per-locale content files and sign SVGs are **not** precached by default — they're runtime-cached lazily as the fetch handler intercepts requests, so only the module(s)/locale(s)/sign(s) a given visitor actually opens become available offline for them (plus, since a later round, an explicit "prepare for offline" action that proactively fetches a chosen module/locale ahead of time — see the offline-preparation feature if/when built). Keep this in mind before assuming "offline" means "everything is precached": adding a module or locale does not require touching the service worker's precache list, but a bug in the runtime-cache fetch handler affects offline availability project-wide.

## Working discipline: don't trust self-reported "looks right"

For anything visual or otherwise subjective (redrawn sign icons, UI/landing-page rendering, RTL layout, screenshots), do not accept a sub-agent's own claim that a fix "looks right" as the fix being done. Independently re-render/re-screenshot and actually look at the result yourself before closing it out. This project's own history (see `BACKLOG.md`) has caught agents being wrong on the same fix 2-3 rounds in a row this way (e.g. a sign-icon fix-agent repeatedly misjudging its own render of a horse-and-rider pictogram until an independent check caught it). Applies whether you're the one who made the fix or the one reviewing it — "the agent that did the fix says it's fine" is not itself verification.

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
3. Run validation (schema check script, locale-coverage check; extend as the schema grows).
4. Move to `Student Review` — do a pass as the Student persona (does this read clearly, does it feel exam-realistic, is anything confusing).
5. Only after Student Review passes, move to `Done` and commit, referencing the card ID in the commit message.
6. Scrum Master role: keep `BACKLOG.md` tidy, enforce WIP limits, don't originate content decisions.
7. Product Owner role: decides what's next in `Ready`, writes/approves acceptance criteria, is the only one who can change scope, license terms, or the non-negotiable constraints above (in practice: that's Stefan, or an agent explicitly told to act as PO on his behalf).

## Commit conventions

`[<card-id>] <short summary>` — e.g. `[DN-3] Add multi-select question type to schema`. Keep commits scoped to one card where possible.
