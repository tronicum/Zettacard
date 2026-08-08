# AGENTS.md — working agreement for anyone (human or AI) contributing to Zettacard

This file is the entry point for any agent — Claude, another model, or a human contributor — picking up work in this repo. Read this before touching anything.

## What this project is

Original, openly-licensed learning content and tooling for German exam prep and workplace-compliance training, offered as an offline-first PWA in 12 languages. Currently 8 modules: **Fuehrerschein** (Klasse B/BE driving theory), **Motorrad**, **LKW**, **Angelschein** (fishing license), and 4 workplace-compliance modules — **Datenschutz** (GDPR), **Arbeitssicherheit** (occupational safety), **KI-Verordnung** (EU AI Act), **IT-Sicherheit**. All modules share the same fact-layer/text-layer content schema and the same 12-locale requirement. Not a clone of any official Fragenkatalog or compliance-training vendor's material — see `docs/README_pilot.md` and the license rationale below for why.

## Non-negotiable constraints

Read these before generating or editing any content — they came out of real legal analysis, not arbitrary preference:

1. **Never source or paraphrase from the official Fragenkatalog** (current or old/"leaked" editions), or from any third-party exam-prep or compliance-training company's text. Generate original content from primary legal sources (StVO/StVZO/FeV, GDPR, ArbSchG, EU AI Act, BSI/ISO standards, etc.) and from standardized, law-published sign specs (StVO Anlage 1-4). If you're unsure whether a phrasing is "too close" to a known commercial product, flag it in the card rather than guessing.
2. **Track legal changes, not proprietary catalog changes.** When source law/regulation amendments or official exam-format changes are published, that's fair game to update content against. Don't design pipelines that sync against someone else's compiled catalog.
3. **Every content file ships with the license already attached** — `license` field in JSON meta + repo-root `LICENSE.md` (CC BY-NC-SA 4.0). Don't remove or weaken it without an explicit PO decision.
4. **Content is not legally reviewed by a professional.** Every batch must carry a `legal_review_status` field and get flagged as such in its card until a real review happens. Don't silently upgrade this status.
5. **Multilingual by construction, all 12 locales, no exceptions.** New content always uses the fact-layer/text-layer schema (see `data/generate_pilot.py` for the reference shape) and must ship with `de, en, uk, pl, ar, zh, hi, tr, fr, ru, es, it` all populated from the start — never hardcode single-language question objects, and never land a new UI string, topic label, or landing-page section in only DE/EN "for now." This project has repeatedly had to go back and fill locale gaps (missing `UI_STRINGS`/`TOPIC_LABELS` translations, a DE/EN-only landing page, an 8-question DE-wording desync from the other 10 locales) — treat a locale/coverage check (grep for empty/missing keys across all 12 locale files, or an equivalent script) as part of verification before calling anything content- or UI-string-related done, not an afterthought.
6. **Offline-first.** Output stays as flat, static JSON bundles suitable for service-worker precaching. No feature should require a live backend call to serve content. See "Offline architecture" below for the current shape.

## Repo layout

- `app/` — the actual PWA, deployed as-is (no build step). `index.html` is the marketing landing page; `app.html`/`app.js`/`styles.css` are the app itself; `service-worker.js` handles offline caching; `manifest.json` is the PWA manifest. `app/data/<exam_type>/{core.json, locales/*.json}` is the **runtime** content the app fetches — a generated artifact, not hand-edited (see below). `app/assets/signs/*.svg` are the rendered sign icons; `app/.well-known/jwks.json` publishes the public key for verifying signed completion credentials.
- `data/` — editable master content, one or more source JSON files per module (e.g. `pilot_questions.json`, `angelschein_seed.json`, `*_pilot.json` for the workplace modules, plus assorted `batch*`/`i18n_*` files from incremental content/translation rounds). Content agents edit these files, not `app/data/`. `data/modules_manifest.json` declares which modules/classes/regions exist and their picker labels. **`data/build_modules.py` derives the runtime files** (`app/data/modules.json` + `app/data/<exam_type>/{core.json,locales/*.json}`) — run `python3 build_modules.py` from within `data/` after ANY content or manifest change; the copy is not automatic.
- `assets/` — sign/diagram generation. **`assets/generate_signs.py` is a single shared script that draws every StVO sign SVG** (plus `batch_a/b/c/d_signs.py` helper modules and `build_sign_reference.py`); output goes to `assets/signs/*.svg` and (in the same run) `app/assets/signs/*.svg`. Because all sign-drawing logic lives in this one file, **parallel agents must not edit it concurrently** — fixes to multiple signs go one agent at a time, sequentially (see "Parallel vs. sequential work" below). `assets/generate_diagrams.py` similarly generates non-sign diagrams.
- `netlify/functions/sign-credential.js` — a Netlify Function that signs completion records as JWT credentials (see `docs/open-badges-signing-scoping.md` / `-setup.md`). Requires `ZETTACARD_SIGNING_PRIVATE_JWK` set in the Netlify UI, never committed.
- `scripts/` — small Node utilities: `generate_signing_keypair.mjs` (one-time keypair generation for the above) and `test_sign_credential.js`.
- `netlify.toml` — deploy config: publishes `app/` with no build command (the `app/data/` tree is a pre-generated artifact, not something Netlify compiles), routes `netlify/functions/`, and sets cache headers (service worker never cached, `/data/*` always revalidated, `/assets/*` short-cached).
- `package.json` — exists solely so Netlify's function bundler can resolve the `jose` npm dependency used by `sign-credential.js`. The app itself (`app/`) remains build-step-free static files; this is not a "the project now has a build step" signal.
- `docs/` — process and content documentation: `README_pilot.md` (schema/content notes), `PERSONAS.md` (roles), `KANBAN.md` (board + workflow), plus various planning docs for specific efforts (translation completeness, signing setup, etc.).
- `BACKLOG.md` — the kanban board, in plain markdown (see `docs/KANBAN.md` for how to use it). Its `Done` entries are also a real record of project-specific lessons learned (verification gotchas, locale-gap patterns, sign-icon audit findings) — worth grepping before starting related work.
- `LICENSE.md` — CC BY-NC-SA 4.0, applies to generated content.

## Offline architecture (orientation only — see `app/service-worker.js` comments for full detail)

`service-worker.js` precaches only the small app shell plus the top-level module manifest (`app/data/modules.json`) at install time. Per-module, per-locale content files and sign/diagram SVGs are **not** precached by default — they're runtime-cached lazily as the fetch handler intercepts requests, so only the module(s)/locale(s)/image(s) a given visitor actually opens become available offline for them. On top of that, `app.js` has an explicit per-module "make available offline" button (`offlineAssetUrls()`/`checkOfflineReadiness()`/`prepareOffline()`) that proactively fetches a chosen module's current-language content plus every sign/diagram image its questions reference, so a visitor can prepare a module ahead of time instead of only getting offline coverage for whatever they happened to click on already — this works with ZERO changes to `service-worker.js` itself, since its existing fetch handler already caches any successful fetch it intercepts; adding proactive-fetch coverage for something new (e.g. a different asset type) only ever needs the URL added to `offlineAssetUrls()`. Keep this in mind before assuming "offline" means "everything is precached": adding a module or locale does not require touching the service worker's precache list, but a bug in the runtime-cache fetch handler affects offline availability project-wide.

## Working discipline: don't trust self-reported "looks right"

For anything visual or otherwise subjective (redrawn sign icons, UI/landing-page rendering, RTL layout, screenshots), do not accept a sub-agent's own claim that a fix "looks right" as the fix being done. Independently re-render/re-screenshot and actually look at the result yourself before closing it out. This project's own history (see `BACKLOG.md`) has caught agents being wrong on the same fix 2-3 rounds in a row this way (e.g. a sign-icon fix-agent repeatedly misjudging its own render of a horse-and-rider pictogram until an independent check caught it). Applies whether you're the one who made the fix or the one reviewing it — "the agent that did the fix says it's fine" is not itself verification.

## Working with the attached Claude Project's docs — no git, no undo

This repo's docs (`docs/*.md`, `BACKLOG.md`, `AGENTS.md`, etc.) are all in git, so a bad edit is always recoverable via `git diff`/`git checkout`/history. The Zettacard **Claude Project** attached to this repo's sessions (currently holding `fuehrerschein-learning-data-plan.md`, `compliance-competitor-pricing-and-course-gaps.md`, `netlify-deploy-status.md`) is **not** version-controlled the same way — writing to a project doc replaces its content outright, with no diff view and no built-in undo. An agent overwrote `fuehrerschein-learning-data-plan.md` with placeholder text this way on 2026-08-08 (a stray/erroneous write call made without reading the doc first) and the original content could not be recovered — only reconstructed from context, imperfectly. Learn from this:

1. **Always `project_read` (or equivalent) before any `project_write` to an existing path.** Never write to a path you haven't just read in the same turn, even for what feels like a routine update — there is no git-style diff to catch a mistake after the fact.
2. **Double-check the path and content are what you intend before the write call actually fires** — a placeholder, a draft meant for a different file, or content copied from the wrong buffer becomes permanent the instant the call succeeds.
3. **If a project doc's content matters and might need recovery later, consider mirroring the important bits into a git-tracked file in this repo** (e.g. under `docs/`) so there's at least one durable, diffable copy — don't rely solely on the project as the only record of anything load-bearing.
4. **If you do overwrite something by mistake anyway:** say so immediately and plainly (don't paper over it or bury it in an unrelated update), check this repo's git history and any local working copies for a reconstructable version before declaring it unrecoverable, and if nothing can be found, rebuild the best version you can from first principles/available context and flag clearly that it's a reconstruction, not the original.

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
3. Validate before calling it done. There is **no automated schema-check script in this repo today** — despite what an earlier version of this file implied, don't assume one exists. In practice validation has meant: a small ad-hoc Python/Node script per change (locale-key-completeness check, image_ref → file-exists check, `node --check`/`python3 -c "import ast; ast.parse(...)"` for syntax), and for anything visual, actually rendering/screenshotting it (see "Working discipline" below). Building a real, reusable schema-validation script would be a legitimate improvement — flag it to the PO rather than silently building one as a side effect of an unrelated card.
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
5. Per standing PO instruction: don't deploy every small change automatically — deploying is a deliberate step, not an implicit part of "done."
