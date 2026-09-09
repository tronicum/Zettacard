# Zettacard — MVP roadmap: ship, wire, listen, then only UX

**Written:** 2026-09-07
**Owner:** PO
**Related:** `docs/adr/ADR-app-0002` (module hub, the three languages, what a badge means), `zettacard-kb/docs/adr/ADR-0005` (interchange formats), `TODO.md` item 10 (deploy workflow)

## Where we are, and what the numbers mean

**PO's call, 2026-09-08: we are roughly at 0.5.** The ladder from here, so the
word "done" has somewhere to point:

| | What it means |
|---|---|
| **0.5 — today** | The app works and is deployed to staging. Phase 3 is in: hub, traffic light, 15 topics, derived lessons in 18 locales. The content pipeline runs KB → app end to end. Five test suites and CI. Known-not-solid: `examLanguages` is decided and unbuilt, the hub is an overlay rather than the app's root, and no content cell is `approved`. (Two items left this list on 2026-09-08: the hub's primary button now resumes, and the landing page's 22 module cards are links.) |
| **1.0 — rock solid** | Zettacard itself, done properly. Not new surface area: the navigation spine settled and implemented, every known-broken item above closed, the journeys suite genuinely green, production linked, and a learner able to go landing page → module → study → readiness check without meeting a dead end or an untranslated screen. |
| **1.2 — the LMS story** | SCORM 1.2 for compliance modules, plus the packaging and proof the existing GIFT/Moodle XML exporters still lack (a top-level command, CI, and one verified import into a real Moodle). Explicitly long-term. |

**Why SCORM is not 1.0.** It is a few days of work and mostly not hard — the
manifest is comparable to `moodle_xml.py`, the runtime shim is ~100 lines, and
unusually for a content vendor we already own the player, since the app is a
build-step-free static PWA that can BE the SCO. What holds it back is not
effort. A SCORM completion lands directly in an employer's compliance record,
which is a stronger claim than GIFT makes — GIFT hands over a question bank
with its review status printed in the header, SCORM hands over evidence that
someone completed something. Shipping that while every cell is outside
`approved`/`auto_approved` would be the one dishonest thing in an otherwise
careful product. Data first, then the claim.

## The shape of this plan

Four phases, strictly ordered, with one rule running through them:

> **After Phase 0, no new content is authored.** Not a jurisdiction, not a module,
> not a locale. The catalogue is 29 modules and ~2,500 questions in up to 18
> languages, and none of it is reaching anyone well. Adding more is the easiest
> way to avoid the harder problem, which is that the presentation layer was
> designed for one module and now carries twenty-nine.

Phases 0 and 1 are infrastructure and should take days, not weeks. Phase 2 is
small. Phase 3 is the actual work and has no fixed end — it is where the product
gets good.

---

## Phase 0 — Ship what already exists

**Goal: a person can open www.zettacard.de today and learn something, in their
own language, without hitting a trap.**

Nothing here is new development. Everything below is already written, tested to
varying degrees, and sitting undeployed. The live site currently predates a full
day of content and fixes.

| # | Task | Why it blocks "people can just learn" |
|---|---|---|
| 0.1 | Push `main` to GitHub | Everything else depends on the remote being current. Today's work exists only on one laptop. |
| 0.2 | `git ls-files app/data \| wc -l` | Confirms the built tree is tracked. `.gitignore` says it is. If it is not, the first Git deploy ships an app with no content. One command, catastrophic if skipped. |
| 0.3 | Run `data/build_modules.py`, confirm "Sanity checks passed" and that **29 module directories survive** | `amateurfunk_a`, `amateurfunk_e`, `lksg`, `waffensachkunde` have no source in the build path. Any partial tree silently drops them. |
| 0.4 | `npm run test:journeys` against a local serve | Six user journeys, written 2026-09-06, never yet executed. The four new fun modules and the globe control have never been opened in a browser on a real device. |
| 0.5 | Deploy **staging** first, look at it | `zettacard-staging` exists and is healthy. TODO item 3 records production being deployed while staging was skipped — do not repeat that here of all places. |
| 0.6 | Deploy production | |

**Exit criteria.** On `www.zettacard.de`: 29 modules in the picker; 18 UI locales
in the globe sheet; the globe reachable *before* answering the storage-consent
prompt; `fuehrerschein:parken-17` showing the corrected answer; the four
`compare` modules present and carrying their identification banner.

**Explicitly not in Phase 0:** anything from ADR-app-0002. The hub, the
vocabulary rename, the traffic light — all of it waits. Phase 0 is about the
gap between what is built and what is served, and that gap is the single
largest source of value available right now.

---

## Phase 1 — The deployment workflow

**Goal: shipping stops being an act of memory.**

### 1.1 Link GitHub to both Netlify projects

The remote already exists (`github.com/tronicum/Zettacard`, `main` tracking
`origin/main`) and `app/data/` is not gitignored, so Netlify can serve the
committed tree directly — `publish = "app"`, `command = "true"` generates
nothing.

**This link is itself the fix for the deploy hazard.** Once Netlify builds from
Git, the deploy artefact stops being "whatever directory someone assembled" and
becomes "what is committed". The four un-built modules can no longer vanish,
because Git carries them.

**The trap:** in the Netlify UI, do **not** use "Add new site → Import an
existing project". That creates a *new* site and abandons site id
`b244f9b2-…`, the `www.zettacard.de` domain, and the function environment
variables including the badge signing key. Use the existing project:
Site configuration → Build & deploy → Continuous deployment → **Link
repository**.

Branch model:

| Branch | Netlify project | URL |
|---|---|---|
| `main` | `zettacard` | www.zettacard.de |
| `staging` | `zettacard-staging` | zettacard-staging.netlify.app |
| pull requests | deploy previews on staging | per-PR URL |

Nothing reaches `main` except via a PR that has a green preview.

### 1.2 Make the build reproducible

Replace `command = "true"` with a command that actually regenerates and checks:

```
python3 data/build_modules.py && python3 scripts/check_data_integrity.py
```

**Plus the preflight that would have caught every near-miss so far:** fail the
build if any directory under `app/data/` present in the previous deploy is
absent from this one. A dozen lines. Without it, a mistake in `BUILT_MODULES`
removes live modules and nothing objects.

### 1.3 CI on GitHub Actions

`node --check app/app.js`, `check:data`, `check:translations`,
`test:exam:quick`, `test:journeys`. Runs on every PR. **Free on a public repo**;
on a private one this fits inside Team's 3,000 monthly minutes many times over.

### 1.4 Retire the tarballs

`zc_deploy.tar.gz`, `zc_deploy_bundle.tar.gz`, `zc_deploy_bundle4.tar.gz`,
`app_test_bundle.tar.gz` are four hand-rolled deploy artefacts in the repo root,
none reproducible, none named for what is in them. Delete or gitignore them.
Leaving artefacts that look like a release process is how the next person
reinvents the manual one.

### On self-hosted runners — the PO has two Hetzner root servers

That removes the cost argument, so the answer rests on the other two, and they
still hold.

**Security.** A self-hosted runner attached to a **public** repository is a
known hazard: a pull request from a fork executes workflow code on your machine.
Phase 2 wants this repo public. So at exactly the moment self-hosting would be
cheapest, it becomes the thing you must not do — and at that same moment,
GitHub-hosted standard runners become **free and unlimited**, because that is
how public-repo billing works. The two curves cross the wrong way.

**Before the repo is public**, a private repo on Team includes 3,000 Actions
minutes a month. This CI run is a few minutes — `node --check`, two Python
integrity checks, Playwright — so the allowance covers hundreds of runs, and
overage is $0.006/min for Linux. There is nothing to save.

**But the servers have an obvious job already, and it is a better one.**
`ADR-0002` specifies text-to-speech and subtitle media, addressed by deterministic
UUIDv5, stored on an SSD rather than in Git: **40,711 objects expected, 0
produced.** That work is compute-heavy, latency-insensitive, embarrassingly
parallel, involves no personal data whatsoever, and is blocked purely on nobody
having run it. It is exactly what owned hardware is good for, and it is worth
more to the primary audience — learners who read German poorly and would benefit
from hearing a question — than shaving cents off a CI bill.

Second candidate, later: hosting a Moodle instance if the B2B demand described
below actually materialises. Having the hardware removes the *infrastructure*
objection to that; it does not remove the data-protection one.

---

## Phase 2 — The feedback loop

**Goal: a learner who spots a bad translation can say so in two taps, and that
report lands in the machinery that already exists for handling defects.**

The model is the one the PO pointed at: *I-Still-Dont-Care-About-Cookies* opens
a **GitHub issue form pre-filled through URL query parameters** — template,
title, labels, and a set of context fields the extension knows and the user
should not have to type.

This fits Zettacard unusually well, because it needs no backend, no accounts and
no server-side storage, which is the whole privacy position of the app.

### 2.1 What the app already knows and should pass

| Field | Source | Why |
|---|---|---|
| `kb_id` | `<module>:<question_id>` | Identifies the card exactly |
| `locale` | current study language | Which translation is wrong |
| `source_hash` | the cell's hash | **The join key.** It survives corrections, so a report can be matched against the KB even after the card has moved on, and it says which *version* was seen |
| `module_kind` | manifest | Whether this is exam_prep, compliance or compare |
| `app_version`, `ui_lang` | app | Reproduction context |
| Report kind | user choice | translation reads wrong / answer looks wrong / question unclear |

### 2.2 Where it plugs in

**A user report is a hunt candidate, not a defect.** It enters the same pipeline
HUNT-0001 used: reported → triaged → confirmed or dismissed. A confirmed one
becomes a `DEF-xxxx`, gets corrected in the canonical German cell, and cascades
to every derived locale by `source_hash` (ADR-0004). That machinery is built and
proven — DEF-0001 was found by a translation agent, DEF-0002 by a hunt. This
adds a third source of findings: the people actually reading the cards, who are
the only ones who can tell us a Persian sentence is awkward.

### 2.3 The decision this forces — and its timing

**Filing an issue requires the repo to be visible to the filer.** So the
feedback loop needs either `tronicum/Zettacard` public, or a public
`zettacard-feedback` repo that receives only issues.

**PO's call: yes to making it public, but after the basics work.** That is the
right sequence and worth stating as a rule rather than a preference — going
public is irreversible in practice. Every commit in the history becomes
permanently readable, including anything that should not have been committed.
So before flipping it:

- Scan the full history, not just the working tree, for key material. The repo
  gitignores `.env`, `.env.local` and `*.pem`, and `docs/open-badges-signing-setup.md`
  documents a private signing key — confirm no earlier commit ever contained one.
  `git log --all -p -- '*.pem' '.env*'` and a secret scanner, not a glance.
- Decide the licence for the *code*. The content licensing is settled
  (`data-rules.md` § 3b); the app code is not the same question.
- Turn on GitHub secret scanning and Dependabot, which are free on public repos.

Because of that irreversibility, **the separate public `zettacard-feedback`
repo is the lower-risk way to start**: it unlocks the loop immediately, keeps
the app history private until the audit is done, and keeps an issue tracker
full of "this word is wrong in Croatian" from burying development issues. The
main repo can go public afterwards on its own timetable, and the CI-cost
benefit arrives then.

**Fallback if neither:** Netlify Forms is currently *not enabled* on either
project. It would work without a GitHub account, which is a real advantage for
this audience — but it puts us back in the position of receiving and storing
user-submitted data ourselves, which the GitHub route avoids entirely.

### 2.4 What must not happen

The report link must not carry anything the user did not knowingly send. No
progress data, no profile name, no answer history. `kb_id`, `locale`,
`source_hash`, version — and the text they type. Nothing else.

---

## Phase 3 — UX only

> **Where this stands, 2026-09-08.** 3.1–3.6 done and live on staging; 3.7
> partly done; 3.8 not started. What came out of doing them and is not in the
> original plan: ADR-app-0003 (what a record claims; the exam/material version
> split), the certificate honesty fixes, CI on GitHub Actions, and
> `claude/navigation-and-module-path-concept.md` — which argues the hub should
> become the app's ROOT rather than another overlay. That is the next
> structural decision, and it is waiting on the PO. The rest of that document
> is now **Phase 4** below.


**Goal: the presentation layer catches up with the catalogue. No new content.**

Everything here is decided in ADR-app-0002 and grounded in fable's read of the
data. Ordered by dependency, not ambition.

### 3.1 Honour the lesson→question link — **DONE** (ba8ab01, 2026-09-07)

`completion_rule: "quiz_pass:0.7"` is declared in the data and **never
evaluated**. `select.count` is ignored. The handoff uses `topic_codes[0]` only.
Fix that one function and the Explain→Try loop, the traffic light and derived
lessons all become possible.

In the same change: **record failed exam runs.** `finishExam()` currently writes
only `if (results.passed && mode === "simulation")`, so trial-to-trial
improvement — the thing the PO says the runs are *for* — is unanswerable from
the stored data.

### 3.2 The traffic light and "what next" — **DONE** (374c4da; gates revised 49aeff0)

Per topic, from the Leitner boxes that already exist (0–4 with `dueAt`, fed by
exam, practice and flashcard self-assessment): grey / red / yellow / green.
One derived next action. Needs one hand-authored thing per module — topic order,
ten strings.

Note: `grundstoff` is **not** usable as a signal. It is `true` for all 531
Führerschein questions and discriminates in only 8 of 25 modules.

### 3.3 Split `verkehrszeichen` — **DONE** (kb 13fa1d7 -> app cf78baf)

138 of 531 Führerschein questions — 26% of the module in one topic. Under any
per-topic scheme it is the topic that never goes green. Split along the sign
reference's existing shape/category grouping. Data change, no new authoring.

### 3.4 Derived lessons — **DONE** (24cbd6e)

A lesson per topic built from rule sentence + media sections + solved worked
examples. **This is the one that reaches the primary audience:** course prose
exists in `de`/`en` only, while questions exist in 18 locales, so a
prose-first lesson serves nobody who needs it most. It also fixes Führerschein's
1-of-11 topic coverage for free.

### 3.5 The module hub — **DONE** (83eda89; cold-launch fix 93ebb7b)

Name, kind chip, "Weiterlernen" as primary action, progress, topics, the run,
coverage notice, "Über dieses Modul" collapsed. A hub, not an intro — it carries
state and the primary button, so the tap is one the learner was making anyway.

### 3.6 `kind`, picker grouping, coverage — **DONE** (ba8ab01, 2026-09-07)

Add `kind` ∈ `licence` | `compliance` | `cert` | `compare` to the manifest — 29
one-word values, hand-written once, from which grouping, run labels, badge
semantics and chips all derive. Group the picker. Collapse variants
(Angelschein ×3 → one row with a region selector). Surface per-locale coverage
as a **fraction**, never a module-level badge, plus a per-card marker when a
card is served in a fallback language.

### 3.7 Vocabulary, in the KB — **PARTLY DONE** (296d23d, a0f8040)

Modul / Thema / Lernen / Übungsquiz / Prüfungssimulation / Lernnachweis, and
their English counterparts including *readiness check* and *self-assessment*.
Done in `zettacard-kb/content/_ui`, re-exported, and the `app.js` `UI_STRINGS`
dictionaries retired — which closes the fork the PO accepted as temporary.

**Status 2026-09-08.** The route exists and 16 of 19 dictionaries read through
it: `zettacard-kb/content/_ui` -> `data/ui_strings.json` ->
`app/data/ui/<locale>.json` -> the app, with the literals kept as fallback.
Left: `UI_STRINGS`, `EXAM_STRINGS` and `MODULE_PICKER_STRINGS` have no accessor
and are read directly at 17 call sites; and **39 of 281 strings exist in de/en
only** — the hub, the traffic light and lesson completion, which are the newest
surfaces and the first a learner meets. Translating those is KB work.

### 3.8 Deletions — **NOT STARTED**

Flashcards as a top-level destination (it is Practice without commitment; keep
the card as a component). Hand-written `intro.steps` in the manifest (7 of 29
modules have them; everything on them is derivable).

---

## Phase 3.9 — The master-data contract (ADR-0007)

Not planned; found by running the KB exporter once and watching it rewrite 38
files. `zettacard-kb/docs/adr/ADR-0007-mastership-and-the-export-contract.md`
is the decision, proposed and awaiting PO approval.

**Done** (kb `b484f96`): the exporter proves ownership before writing
(`_generated`, `--adopt`), the authored metadata has a master in the KB
(`export_meta`, no key shared with `rights`), exports are deterministic
(`generated` out of all 38 payloads into one `data/_export.json`), and
losslessness is a test (`--check-roundtrip`, 37 files losing metadata -> 0).

**The first real export is a PO decision, not a mechanical one.** It is
lossless — zero keys, zero questions — but it carries three corrections that
should be announced rather than discovered:

- 16 compliance modules move CC BY-NC-SA -> CC BY-NC-ND. This is the
  2026-09-06 PO decision finally reaching the exported files; they have been
  publishing the superseded licence since.
- 7 modules lose a stale `module_kind` of `exam_prep` for `compliance`.
- `angelschein`, `angelschein_bayern` and `angelschein_nrw` gain `bar`, `fa`
  and `ro` — roughly 170 question cells, none human-reviewed. Publishable and
  labelled under ADR-0003, but a visible jump in the coverage report.

**Left, in the ADR's order:**

- Delete `build_modules.py`'s hard-coded `fs_locales` / `ang_state_locales` /
  `compliance_locales`. They are a *fourth* place a locale set is declared,
  and `split_module` `rmtree`s `locales/` first — so exporting the three new
  locales would not actually deliver them. This blocks the locale step above.
- Ingest the four built-only modules (`lksg`, `waffensachkunde`,
  `amateurfunk_a`, `amateurfunk_e`). They are in the manifest and exist only
  under `app/data/` with no master in either repo — `rmtree` plus a manifest
  entry is exactly the shape that loses them. ADR-0001 Follow-up 1, still open.
- Ingest the 12 `*_course.json` into the KB. Phase 4 makes the course the
  spine of the learning path; a lost course is a lost path.
- `meta_version` as a third digest beside `exam_version` / `material_version`,
  so a record can say which licence terms it was studied under. Today a
  licence moving SA -> ND bumps nothing.
- `--check-roundtrip` in CI in both repos.

---

## Phase 4 — The learning path

Phase 3 fixed the module: a learner who is already inside one now has a hub, a
traffic light, lessons and a resume button. Phase 4 is about the journey
*between* those things — arriving, choosing, and being able to study in a
language you actually read. It is fable's
`claude/navigation-and-module-path-concept.md` reduced to work items, in that
document's own priority order.

The spine is **Option A**: the course is the path, the topic row opens the
lesson, and the card list is an escape rather than the destination. That was
chosen over B/C/D because the primary audience — someone who reads German
slowly — is helped by one button, not by a menu of study styles.

### 4.1 The A spine — **PARTLY DONE** (009edb9, 9b3141d, ebda9f7)

**Done.** Topic rows open the topic's lesson, with a quiet "Nur Karten"
escape on every row (borrowed from Option B), and `hubNextAction` agrees with
them. The landing page's 22 module cards are real links, `?exam=` alone
resolves through the manifest, a deep link beats a saved selection, and the
hero CTA names the module it resumes.

**Left.** Hub as the app's ROOT rather than another overlay, with hash routes
so a lesson and a topic are addressable — this is the structural decision
fable flags and the one that makes back-navigation predictable. Per-`kind`
next-action defaults (`licence`/`cert` guided, `compliance` test-first,
`compare` cards) — `kind` exists for exactly this and is not yet read here.
One run per module plus a time-limit toggle, replacing the current several.

### 4.2 `examLanguages` and a sticky target language — **NOT STARTED**

ADR-app-0002 § 5 decided this and nothing implements it. fable ranks it
**above** the navigation rework: it is the primary audience's actual problem.
A Greek or Arabic speaker studying for the Führerschein sits an exam that
exists only in German and English; the app currently neither says so nor
remembers what they chose. Wanted: `examLanguages` on the manifest, the § 5
sheet asked once at the first simulation, the answer remembered, and the
exam-start sheet still able to change it. The per-card "DE" gloss and "Auf
Deutsch üben" come after 4.1 and 4.2 both exist.

### 4.3 The Ziel row and the high-stakes gate — **NOT STARTED**

A two-option row under the kind chip on `licence`/`cert` modules, defaulting
to "echte Prüfung": are you preparing for the real exam, or learning out of
interest? It drives the high-stakes gate in the traffic light and the next
action. It must never change the run size or the pass bar — a record has to
mean the same thing whatever the learner said about themselves (ADR-app-0003).

Explicitly **not** doing: a level selector, an expected-level selector, or a
"wie möchtest du lernen" screen. Level is measured, not declared, and an
abstract question asked before any content is the wrong thing to show the
audience least able to answer it.

### 4.4 First-time captions and the landing strip — **NOT STARTED**

Four captions that explain the hub by doing, and a five-step strip on the
landing page that explains by telling — which is where telling belongs.

### 4.5 The device pass — **NOT STARTED**

fable lists 13 things to check on a real 390px phone before calling this
done. The riskiest is #1: cold start in Greek or Ukrainian, ≤ 4 taps from the
landing page to a lesson section on screen, and the derived lesson has to be
*readable*. If it is not, A falls back to the topic row opening the
Übungsquiz, with the lesson behind an "Erklärung" link until the KB review
loop moves the quality. Everything in 4.1–4.4 is written on the assumption
that #1 passes, and nothing has tested it on hardware.

---

## Moodle: recommended *not* now

A Moodle instance is a second product surface, and it cuts against the thing
that makes Zettacard defensible.

Zettacard today holds **no learner data at all**. No accounts, no server state, a
storage-consent gate before anything touches the device. Running a Moodle means
hosting an application that stores names, email addresses, enrolment and
assessment records for identifiable people — a controller relationship under
GDPR, with everything that follows: a processing register, a DPA with the host,
retention rules, subject-access handling, and a breach surface. That is a
serious commitment, and it is not one the MVP needs.

**The exporters already solve the real problem.** `src/export/moodle_xml.py` and
`src/export/gift.py` were built on 2026-09-06 and tested across 2,913 cells. A
compliance customer who wants Zettacard content in their LMS already has one —
we hand them a Moodle XML file and they import it into the instance they already
run, under their own controllership. That is a better business position than
hosting for them.

**Having two Hetzner root servers removes the infrastructure objection, not the
data-protection one.** Where it runs is the cheap part; being the controller for
other people's learning records is the expensive part, and that cost is the same
on owned hardware as on rented.

**Revisit when** a paying customer asks for hosted delivery *and* completion
records they can audit — at which point it is a scoped B2B project with a
contract behind it, not MVP infrastructure. The `compliance` modules are exactly
the ones where that demand will appear, and ADR-0005's SCORM 1.2 export is the
cheaper answer even then.

---

## What "MVP running" means

The bar is not feature completeness. It is:

1. A learner opens the site, picks a language they can read, picks a module,
   and studies — with no dead control, no silent English fallback, and no
   screen that says "Prüfung" when it means four different things.
2. A change goes from a commit to production through staging without anyone
   remembering a command.
3. A wrong translation gets reported, triaged and corrected without leaving
   the tools we already have.

Everything in Phase 3 improves 1. Phase 1 delivers 2. Phase 2 delivers 3.
None of it requires another question to be written.
