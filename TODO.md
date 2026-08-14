# TODO — boating-licence integration arc

Working list for the yachting/boating-licence integration effort (started
2026-08-14, researching `HugoFara/boating-licence`). Ordered roughly by
dependency, not strict priority — some can happen in parallel. See
`BACKLOG.md`'s "Done" section for what's already shipped and the full
detail behind each finished item; this file is just the forward-looking
list so a future session doesn't have to reconstruct it from chat history.

1. **Fix this session's repo access** — `git push` to `tronicum/Zettacard`
   is blocked by the git proxy ("not in this session's authorized
   repository set"), even though the folder is connected via the device
   bridge. Needs a setting change on the account/session-source side, not
   something fixable from inside a session. User is aware, fixing from
   another session. Blocks: real `git push` for everything below, instead
   of the current bundle-delivered-as-a-file-attachment workaround.

2. **Push zettacard-kb to an actual GitHub repo.** Currently it only
   exists as a local repo in whatever session built it, delivered to the
   user as a git bundle (`zettacard-kb-init.bundle`). Needs a real empty
   GitHub repo (user has a local folder for it: `zettacard-kb`) and #1
   fixed, or continued manual bundle-merge in the meantime.

3. **Deploy the 2026-08-14 ELWIS/sportboot changes to staging**, not just
   production — this round went straight to production
   (`b244f9b2-e45a-48c0-9f59-0405f587c213`), skipping the usual
   staging-first (`480e3ec6-76f6-414e-a7bc-eb3e661f5816`) checkpoint.
   Staging currently still has the old ~80-question pool. Cheap to fix,
   just wasn't done yet.

4. **Sportboot Binnen/See: fill in the other 10 locales.** The 515-question
   ELWIS import shipped DE+EN only; the prior (smaller) pool had all 12.
   `fetchLocaleTextWithFallback()` means non-DE/EN users aren't broken in
   the meantime, just seeing English.

5. **Build France (Permis Plaisance, 146 questions) and Switzerland (190
   questions) modules** from `HugoFara/boating-licence`'s own generated
   corpus, with attribution, per the user's explicit choice. NOT STARTED -
   structural conversion, module registration
   (`modules_manifest.json`/`TOPIC_LABELS`/`app/index.html` cards/exam-
   tuning maps) all still to do. **Licensing constraint, decided
   2026-08-14**: that corpus is CC BY-SA 4.0 (ShareAlike) - ingesting it
   means the France/Switzerland modules' content has to stay CC BY-SA 4.0
   too, NOT the CC BY-NC-SA 4.0 this app's other modules use. Anyone else
   can legally reuse Zettacard's France/CH question text commercially as
   long as they attribute + stay BY-SA - a real, already-flagged tradeoff,
   not an oversight if it ships this way.

6. **zettacard-kb: `--from-live` mode + real staleness checking.** v1 only
   reads local `data/*_pilot.json` (still missing lksg/kartellrecht/
   kyc_aml/hinweisgeberschutz locally as of 2026-08-14) and only
   fingerprints citation STRINGS, not the actual underlying law text the
   way `boating-licence`'s own `staleness.yml` does (scheduled GitHub
   Action, fetches upstream sources, diffs against a lockfile, files an
   issue on drift). Once zettacard-kb has a real GitHub repo (#2), the
   same pattern could run there on a schedule.

7. **Randomize per-question answer-option order at render time.** Not
   started - flagged 2026-08-14. WHY this matters, specifically now: the
   515 ELWIS questions are verbatim official-catalog text, and answer-key
   "cheat sheets" for official German license catalogs (by question
   number -> correct letter) circulate publicly online - a fixed a/b/c/d
   order means a memorized cheat sheet defeats the whole point of using
   this app to actually learn the material, not just pattern-match a
   letter. More generally, across EVERY module in the app (checked
   2026-08-14): `drawExamQuestions()`/the practice-quiz draw already
   shuffle QUESTION selection and order via `shuffle()` (app.js ~line
   4256), but nothing shuffles OPTION order within a question - it's
   always whatever order the source JSON has, every time, in every mode
   (flashcards/exam/practice). That's a real, easy-to-close consistency
   gap on its own even ignoring the cheat-sheet angle: fixed option order
   lets any learner unconsciously memorize "the answer is always C" for a
   given question instead of actually reading the options, which
   undermines the app's own stated learning goals.
   **Implementation shape** (not yet built): shuffle each question's
   option order at render time (flashcards + exam + practice all funnel
   through shared render functions, so one shuffle point could cover all
   three), keeping the `correct` field's semantics intact - safest is to
   shuffle a working copy (letter -> text pairs) and remap which
   *rendered* letter is correct, rather than mutating `q.correct` itself,
   so answer-checking logic and any code that reads `q.correct` directly
   (SRS/review-queue logic, certificate signing, exam scoring) doesn't
   need to change - only the DISPLAY mapping does. Needs care around
   `image_ref`-bearing questions where an option's text might reference
   "the marking shown at position 2" - would need an audit for any
   options whose text depends on positional order before this is safe to
   turn on globally rather than just for the new sportboot modules.

8. **Second-pass translation-fidelity verification**, inspired by
   `boating-licence`'s own `translate_answers/` -> `translate_verdicts/`
   two-subagent pattern (one translates, an independent second one checks
   fidelity against the original before anything ships). Zettacard
   currently only does structural JSON validation after a translation
   batch, not a semantic re-check - worth adding given the it_sicherheit
   Hindi corruption near-miss earlier this same week was caught by luck,
   not process.

9. **Long-standing, still open**: confirm whether the GitHub PAT pasted
   into an earlier session has been revoked; confirm whether any of this
   session's bundled commits have actually been merged/pushed to GitHub
   yet.
