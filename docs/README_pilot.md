# Fuehrerschein learning-data pilot (Klasse B)

50 original multiple-choice questions — 25 on **Vorfahrt und Kreuzungen** (right of way), 25 on **Verkehrszeichen** (traffic signs) — in `pilot_questions.json`. This is the first slice of the Fahrschule module for the fluegel-angeln learning-data app.

## Why these two topics

They sit at opposite ends of the content spectrum: Vorfahrt is scenario/reasoning-heavy text with no images, Verkehrszeichen is image-anchored recognition. If the schema and pipeline work for both, they'll generalize to the rest of Grundstoff/Zusatzstoff.

## Schema (fact layer vs. text layer)

Each question has a language-independent **fact layer** — `topic`, `legal_basis` (StVO/StVZO citation), `points` (2–5, matching real exam weighting), `high_stakes` (flags the Vorfahrt-style questions where getting 2 wrong auto-fails you, independent of total error points), `question_type`, `image_ref` (placeholder key for a sign asset — no actual images shipped yet), and `correct` (option keys).

On top of that sits a **text layer**, one block per locale (`de`, `en` so far) holding just the question and option wording. German is canonical; English is a reviewed translation of the same fact, not independently authored — this is what keeps the two languages testing the same thing rather than drifting apart. Adding a third locale (e.g. Turkish, Polish — both in the official exam's language list) means adding another `text.xx` block per question, nothing else changes.

This split is also why the format works well for the planned offline PWA: it's a flat, static JSON bundle you can precache in a service worker and query straight from IndexedDB/local state — no backend calls needed to serve content.

## What's deliberately NOT in here

No text is copied from the official amtlicher Fragenkatalog — see the earlier discussion on its unclear/likely-restricted copyright status. Every question here is independently phrased from the public StVO/StVZO rules and the standardized (non-copyrightable) sign shapes. Sign graphics themselves aren't included — `image_ref` is a placeholder key; actual sign artwork needs to be sourced or redrawn separately (traffic sign shapes/designs are generally reproducible, but this hasn't been separately verified here).

## Known limitations / before this goes further

- **Not legally reviewed.** Citations and sign numbers were compiled from general knowledge of German traffic law, not verified paragraph-by-paragraph against the current StVO/StVZO text or a driving-law professional. A few sign numbers (e.g. 330.1/330.2 style motorway markers) may need a precision check.
- Point values (2/3/4/5) and `high_stakes` flags are my estimate of real-exam-like weighting, not sourced from the actual catalog's point assignments.
- Only single-choice questions so far; the real exam also uses multi-select ("choose all correct answers") — worth adding once the single-choice pipeline is validated.
- No images actually attached yet.

## License

**CC BY-NC-SA 4.0 by default** — see `LICENSE.md`. Free to use and adapt for non-commercial exam-prep purposes, with attribution, and derivatives must stay under the same license. We're not trying to own this data, just to help people pass — commercial reuse needs a separate arrangement.

This is the default for content we author ourselves, not a blanket covering everything in the repo. A module or asset built from ingested third-party material (a CC BY-SA corpus, a public-domain government work, a Wikimedia Commons image, etc.) carries its own real license in its own `license`/`license_note`/`attribution` field instead — see `AGENTS.md` constraint 3 and `app/legal/quellen.html`'s per-source table for the pattern and existing examples (`sportboot_binnen`/`sportboot_see` today; the planned CC BY-SA 4.0 France/Switzerland boating modules per `TODO.md`).

## Suggested next step

Read through a sample by topic and flag anything that reads wrong before we scale the same pipeline to the rest of Grundstoff (Gefahrenlehre, Umwelt/Technik, allgemeines Verhalten) and then Zusatzstoff, and before adding more locales.
