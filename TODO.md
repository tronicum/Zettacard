# TODO — current arc

**Re-scoped 2026-09-08 by the PO.** The previous arc was the boating-licence
integration; it is now secondary (their data can be transformed into our format
whenever we want it — they already have data, and that is a conversion job, not
a discovery one). The arc that replaced it, in the PO's own order:

> the app works, our data is clean, and — long run — our master data is
> exportable to Moodle or a corporate LMS.

**One of those is already done, and it changes the order.** The LMS export
works today: `zettacard-kb/src/export/{gift,moodle_xml,pack}.py`, built under
ADR-0005, verified 2026-09-08 on `kyc_aml` — 450 cells per format across 15
locales, each with a sidecar carrying what the target format has no slot for,
plus LICENSE.txt. The GIFT header states the licence, says the module is not
reviewed by a licensed lawyer, flags the AMLR 2027 threshold change, and
declares itself lossy with a pointer to the sidecar.

So the long-run item is not the blocker. **The data is**, exactly as ranked —
and the exporter says so itself on every run:

    30 not in ['approved', 'auto_approved'], exported with the status
    labelled — ADR-0003

Every cell we can ship is unreviewed. The export is honest about it, which is
why it can ship at all; but "our data is clean" is the thing standing between
that and a corporate LMS customer.

## The arc, in dependency order

1. **The app works.** Phase 3 is done and on staging (roadmap 3.1–3.6, 3.7
   partly). The open structural decision is
   `claude/navigation-and-module-path-concept.md` rev. 3 — whether the hub
   becomes the app's root with the course as its spine. Waiting on the PO.
   Ranked above it by that document: `examLanguages` and a sticky target
   language, because "explain in Ukrainian, test in German" is the primary
   audience's real problem and the machinery already exists.

2. **The data is clean.** The measurable gap, not a vague one:
   - 22 stale and 8658 untracked entries in the translation ledger.
   - 39 of 281 UI strings exist in de/en only — the hub, the traffic light and
     lesson completion, the first surfaces a learner meets.
   - No module has a cell in `approved`/`auto_approved`. ADR-0003 makes
     verification a label rather than a gate, which is right, but the label
     currently always says the same thing.
   - The review loop the PO sketched (a feedback form, or thumbs up/down on a
     translation) is in `IDEAS.md` — and it is what would move this number.

3. **Export to Moodle / corporate LMS.** Built. What is left is packaging and
   proof, not implementation: no top-level command wires the three exporters
   together, nothing runs them in CI, and no one has imported the output into a
   real Moodle to confirm it lands. SCORM is named in ADR-0005 as the format a
   compliance customer will actually ask for and is not built.

## Deferred — the boating-licence integration arc

Kept for the trail. Secondary as of 2026-09-08: their data can be transformed
into our format when we want it.

1. ~~**Fix this session's repo access**~~ — **still true, worked around.**
   Pushing from a Cowork session remains impossible; everything is committed
   locally and pushed by the PO by hand. Bug report:
   `docs/bug-08ec8f0a-github-push.md`. Original text: — `git push` to `tronicum/Zettacard`
   is blocked by the git proxy ("not in this session's authorized
   repository set"), even though the folder is connected via the device
   bridge. Needs a setting change on the account/session-source side, not
   something fixable from inside a session. User is aware, fixing from
   another session. Blocks: real `git push` for everything below, instead
   of the current bundle-delivered-as-a-file-attachment workaround.

2. ~~**Push zettacard-kb to an actual GitHub repo.**~~ — **DONE** 2026-09-08.
   Pushed to `tronicum/zettacard-kb` (private), with a `restore-2026-09-08`
   tag. Original text: Currently it only
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

10. **Optimize the deploy workflow — it is entirely manual and undocumented.**
    Flagged 2026-09-06, after wiring four `fun_translation` modules and finding
    there was no way to ship them without a human doing it by hand.

    **What exists today.** Nothing deploys on its own. There is no `.github/`
    directory, `netlify.toml` has `publish = "app"` and `command = "true"`, and
    the production project (`b244f9b2-e45a-48c0-9f59-0405f587c213`,
    `www.zettacard.de`) has **no linked Git repo**. So `git push` publishes
    nothing at all — which is easy to believe it does, and nobody finds out
    until they check the live site. The current live deploy predates a day's
    worth of committed content.

    **The evidence it hurts.** The repo root currently holds
    `zc_deploy.tar.gz`, `zc_deploy_bundle.tar.gz`, `zc_deploy_bundle4.tar.gz`
    and `app_test_bundle.tar.gz` — four hand-rolled deploy tarballs, none
    reproducible, none named after what is in them. Item 3 above records
    production being deployed while staging was skipped, and staging still
    holding an old question pool. That is the same problem twice.

    **The step that is easy to get wrong.** `app/data/` is a build artifact of
    `data/build_modules.py`, but only *partly*: the script owns
    `core.json`/`locales/` for the modules in `BUILT_MODULES` and deliberately
    leaves everything else alone. `amateurfunk_a`, `amateurfunk_e`, `lksg` and
    `waffensachkunde` live under `app/data/` with **no source in the repo's
    build path**. Any deploy assembled from a partial copy of `app/` — a
    tarball, a staged subset, a fresh checkout that never had them — silently
    drops four live modules. This was very nearly done on 2026-09-06 and was
    caught only by listing the directory first.

    **What "optimized" should mean, roughly in order:**
    - A single documented command, in `package.json` next to the test scripts,
      that runs `build_modules.py`, asserts no module directory disappeared,
      runs the checks, and deploys. Not a tarball.
    - **A preflight that fails loudly** if `app/data/` is missing any directory
      the previous deploy had. This is the check that would have caught every
      near-miss so far, and it is a dozen lines.
    - Staging (`480e3ec6-76f6-414e-a7bc-eb3e661f5816`) first, then production —
      currently possible and routinely skipped, so make skipping the deliberate
      act rather than the default.
    - Decide the Git question properly: either link the repo so pushes deploy,
      or keep manual deploys and *say so* in `README.md` and `AGENTS.md`, since
      the present state reads as continuous deployment and is not.
    - Run `npm run test:journeys` against the built tree as part of it. The
      journey tests exist as of 2026-09-06 and nothing calls them automatically.
    - Resolve the four stray tarballs — `.gitignore` them or delete them, but
      do not leave artifacts that look like a release process.

    Depends on nothing. Blocked by nothing. Cheap, and every content round so
    far has paid the cost of not having it.

11. **zettacard-kb's eventual role: still an open design question, deliberately
    not decided 2026-08-15 (2:39am, PO explicitly deferred it).** Two framings
    surfaced in conversation, not yet reconciled:
    - Narrow/near-term: zettacard-kb as a place to hold most of Zettacard's
      material - started 2026-08-15 with a `content-backup/<date>/` snapshot
      of `Zettacard/data/*.json` (66 files, ~20MB), git-tracked, safety-net
      style, not a restructuring.
    - Wider/later: zettacard-kb as the "zentral" backend the PWA's
      `app/data/*.json` gets generated FROM, not just mirrors - which is the
      same question as design-doc `course-layer-and-content-schema-design-
      2026-08-14.md` §8.6 ("does DB-authoritative mean the JSON stops being
      hand-editable?"), just phrased as "should zettacard-kb become that for
      every module" rather than per-module. PO's own framing: **"we will move
      a lot of data forth and back so this is not a fire and forget setup"**
      - explicitly not a one-time migration, an ongoing bidirectional pipeline.
      PO wants this designed with an Opus subagent's help, not decided ad hoc
      inside another task. Needs: the translation-pipeline plan
      (`claude/content-pipeline-rough-plan-2026-08-15.md`) and this decision
      are linked - a bidirectional zettacard-kb pipeline is exactly where
      translation staleness (`source_revision`) and multi-provider translation
      would actually live operationally, not just in the schema.
