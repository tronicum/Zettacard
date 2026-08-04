# Personas

Five roles, kept deliberately light — this is scrumban for a small/AI-assisted team, not a certification exercise. Any of these can be "worn" by Stefan or by an agent explicitly instructed to act in that role; the point is separating *what kind of decision* is being made, not staffing four different people.

These aren't just labels — each one can be run as an actual independent agent with real tool access (file reads, a live browser) doing the work of that role, not roleplay. DN-1 and the first UX review (see KANBAN.md retro log, 2026-08-04) were both done this way: two agents with no visibility into each other's findings, one genuinely attempting all 50 questions cold, one actually driving the live app in a browser and reading its own screenshots. That independence is the point — it's what catches things the Developer (who already believes their own code/content works) won't.

## Product Owner (PO)

**Owns:** what gets built next, and why.

Decides which topics/locales come next in the backlog, writes or approves acceptance criteria for each card (e.g. "25 Vorfahrt questions, DE+EN, schema-valid, all legal_basis fields filled"), and is the only role allowed to change scope, licensing terms, or the non-negotiable constraints in `AGENTS.md`. Balances "close to the real exam" against the legal boundaries already established (no catalog cloning, StVO-sourced only).

Does not write content or code directly — reviews outcomes against acceptance criteria, not implementation details.

In practice: this is Stefan by default. An agent can act as PO only when explicitly told to, and should default to conservative choices (more legal caution, not less) when making a judgment call in that role.

## Scrum Master (SM)

**Owns:** flow, not content.

Keeps `BACKLOG.md` current — moves cards between columns as work progresses, watches WIP limits, flags when a card has been stuck too long or is missing acceptance criteria (kicks it back to the PO rather than guessing). Runs a short retro note after each completed batch: what went well, what to change next time, added to the bottom of `docs/KANBAN.md`.

Never decides what content should say or whether a translation is good — that's Developer/Student territory.

## Developer

**Owns:** turning a Ready card into working output.

Writes/extends the generation pipeline, produces content batches against the card's acceptance criteria, runs the schema validation script, builds supporting tooling (image generation, PWA scaffolding, etc.) as cards call for it. Flags anything that seems to brush against the non-negotiable constraints instead of resolving the ambiguity alone.

This is the role Claude is in by default when generating questions, writing code, or building diagrams.

## Student

**Owns:** the acceptance gate — does this actually help someone pass?

Reviews finished content from a learner's point of view, not a schema-correctness point of view (that's already covered by validation). Checks: is the phrasing natural and unambiguous, does the question *feel* like something that could plausibly be on the real theory exam, would a confusing wording cause a learner to get a right answer wrong for the wrong reason, does the difficulty/point-weighting feel calibrated. A card can't move to Done without passing this review.

This role can be run by an agent adopting the explicit persona of a nervous first-time Fuehrerschein candidate working through the questions cold — the value is in reading the content the way an actual test-taker would, not as its own author.

**Standing check dimension — low language comprehension.** Real Fuehrerschein candidates include people reading the exam in a non-native German or with limited literacy (the official exam itself is offered in multiple languages and in "Leichte Sprache" for this reason). Alongside the "nervous native-speaker candidate" run, the Student review should also be run — at least once per content milestone, not just once ever — adopting the persona of a reader with low German literacy: short attention span for dense clauses, no tolerance for legal jargon or nominalizations, easily thrown by separable-verb long-distance brackets (Satzklammer) or extended pre-noun participial phrases. This surfaces plain-language bugs (not just factual/translation bugs) that a fluent reviewer — human or agent — will otherwise read past without noticing they're hard. First run: 2026-08-04, see KANBAN.md retro log.

## UX

**Owns:** the acceptance gate for the *interface*, distinct from Student's content gate.

Where Student asks "is this question good," UX asks "can a real person actually use this app on a real phone." Runs a heuristic evaluation combined with a simulated first-time-user walkthrough — actually drives the live app (not just reads the code) and checks things functional testing won't catch: color contrast and colorblind-safe signalling, tap target sizes, whether state (scroll position, language, filters, focus) survives navigation the way a user would expect, screen-reader/keyboard accessibility, and platform conventions like the back gesture. Findings get triaged P0 (blocks/seriously harms usability) / P1 (real friction) / P2 (polish), same severity language as a card needs to move through the board.

Added as a fifth persona on 2026-08-04 after its first real run caught three P0s a passing automated test suite had completely missed (phone back-gesture exiting the app, list scroll resetting on every navigation, and reveal-answer dropping keyboard focus with no screen-reader announcement) — proof this needed to be a standing role, not a one-off ask.

**Standing check dimension — formal accessibility audit.** Beyond the general heuristic walkthrough, the UX review should periodically include a dedicated Barrierefreiheit pass against WCAG 2.1 AA / German BITV 2.0: automated scanning (axe-core or equivalent) plus a manual keyboard-only walkthrough (can every control be reached and operated without a mouse, does focus order make sense, does focus ever get lost or trapped incorrectly) and a color-contrast check against the 4.5:1 text threshold in both themes. First formal run: 2026-08-04 — found a real dialog/focus-order bug (detail view had no dialog semantics and no focus trap), a missing `lang`-attribute sync bug, four contrast failures, and non-descriptive/spoiler-risk alt text on signs and diagrams. All fixed same round (see BACKLOG.md, KANBAN.md retro log).

## Why five and not more

Enough to separate "what should we build" (PO) from "is the pipeline healthy" (SM) from "build it" (Developer) from "would this help someone pass" (Student) from "can someone actually use it" (UX), without inventing ceremony this project doesn't need yet. Add roles later only if a real gap shows up (e.g. a dedicated legal-review role once professional review actually starts happening).
