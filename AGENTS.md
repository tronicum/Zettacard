# AGENTS.md — working agreement for anyone (human or AI) contributing to Zettacard

This file is the entry point for any agent — Claude, another model, or a human contributor — picking up work in this repo. Read this before touching anything.

## What this project is

Original, openly-licensed learning content and tooling for German exam prep, starting with the Klasse B driving-theory exam (Fuehrerschein) and later the fishing-license exam (Angelschein). Not a clone of the official amtlicher Fragenkatalog — see `docs/README_pilot.md` and the license rationale below for why.

## Non-negotiable constraints

Read these before generating or editing any content — they came out of real legal analysis, not arbitrary preference:

1. **Never source or paraphrase from the official Fragenkatalog** (current or old/"leaked" editions), or from any third-party exam-prep company's question text. Generate original questions from the primary legal source (StVO/StVZO/FeV) and from standardized, law-published sign specs (StVO Anlage 1-4). If you're unsure whether a phrasing is "too close" to a known commercial product, flag it in the card rather than guessing.
2. **Track legal changes, not proprietary catalog changes.** When StVO/StVZO/FeV amendments or official exam-format changes (e.g. point-system reforms) are published in the Verkehrsblatt/Bundesgesetzblatt, that's fair game to update content against. Don't design pipelines that sync against someone else's compiled catalog.
3. **Every content file ships with the license already attached** — `license` field in JSON meta + repo-root `LICENSE.md` (CC BY-NC-SA 4.0). Don't remove or weaken it without an explicit PO decision.
4. **Content is not legally reviewed by a professional.** Every batch must carry a `legal_review_status` field and get flagged as such in its card until a real review happens. Don't silently upgrade this status.
5. **Multilingual by construction.** New content always uses the fact-layer/text-layer schema (see `data/generate_pilot.py` for the reference shape) — never hardcode single-language question objects.
6. **Offline-first.** Output stays as flat, static JSON bundles suitable for service-worker precaching. No feature should require a live backend call to serve content.

## Repo layout

- `data/` — editable master content per module: `pilot_questions.json` (Fuehrerschein, all locales) and `angelschein_seed.json` (Angelschein, seed/demo content only - see DN-11/DN-39). Content agents edit THESE files. `data/modules_manifest.json` declares which modules/classes/regions exist and their picker labels. **`data/build_modules.py` derives the runtime files the app actually fetches** (`app/data/modules.json` + `app/data/<exam_type>/{core.json,locales/*.json}`) - run `python3 build_modules.py` from within `data/` after ANY content or manifest change, and copy is NOT automatic. `generate_pilot.py` is the original pilot-batch generator, superseded by direct edits to `pilot_questions.json` for content since DN-5.
- `docs/` — process and content documentation: `README_pilot.md` (schema/content notes), `PERSONAS.md` (roles), `KANBAN.md` (board + workflow).
- `BACKLOG.md` — the kanban board, in plain markdown (see `docs/KANBAN.md` for how to use it).
- `LICENSE.md` — CC BY-NC-SA 4.0, applies to generated content.

## Roles

This project runs light scrumban with four personas: **Product Owner**, **Scrum Master**, **Developer**, **Student**. Full definitions in `docs/PERSONAS.md`. When you pick up a card, know which hat you're wearing — a Developer generating content should not also grade its own Student-review gate.

## Workflow (quick version, full detail in docs/KANBAN.md)

1. Pull the top card from `Ready` in `BACKLOG.md` (respect WIP limits).
2. Move it to `In Progress`, do the work as the Developer persona.
3. Run validation (schema check script; extend it as the schema grows).
4. Move to `Student Review` — do a pass as the Student persona (does this read clearly, does it feel exam-realistic, is anything confusing).
5. Only after Student Review passes, move to `Done` and commit, referencing the card ID in the commit message.
6. Scrum Master role: keep `BACKLOG.md` tidy, enforce WIP limits, don't originate content decisions.
7. Product Owner role: decides what's next in `Ready`, writes/approves acceptance criteria, is the only one who can change scope, license terms, or the non-negotiable constraints above (in practice: that's Stefan, or an agent explicitly told to act as PO on his behalf).

## Commit conventions

`[<card-id>] <short summary>` — e.g. `[DN-3] Add multi-select question type to schema`. Keep commits scoped to one card where possible.
