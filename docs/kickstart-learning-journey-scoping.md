# Scoping: Kickstart Learning Journey — Primers, Practice Quizzes, Path Wizard (DN-52)

Status: scoping only, no PO decision to build yet. Came out of a PO brainstorm (2026-08-08) about
bridging a true beginner from "knows nothing about this topic" to "confident enough to start real
practice," rather than dropping every new user straight into a flashcard list or a 30-question exam
with no context. This document lays out what that actually takes, grounded in what this app already
has (so the plan reuses real infrastructure instead of assuming a blank slate) and what's genuinely
new.

## 0. The ask, distilled

The PO's own framing of the funnel (verbatim shape, lightly organized):

1. A one-time first introduction / learning-style choice.
2. Build up knowledge (short topic primers, easy-to-chew chunks).
3. Learn via flashcards.
4. Smaller practice exams — mixed, per-subject, or overall — as a middle tier between flashcards
   and the real exam.
5. Relearn missed ones.
6. Get better at the final exam.

Explicitly a **hybrid, skip-ahead-friendly** design: a confident user should be able to jump
straight to the real exam from the first screen; someone who only wants flashcards should never be
nagged about primers. Nobody gets railroaded through a linear wizard.

## 1. What already exists vs. what's genuinely new

Worth being precise here, since three of the six funnel steps already exist in some form and the
plan should extend that infrastructure rather than duplicate it:

| Funnel step | Status | Existing mechanism |
|---|---|---|
| 1. First intro / style choice | **Partially exists, needs extending** | The per-module intro wizard (DN-43, `MODULE_INTRO_STRINGS` + `modules_manifest.json`'s `intro.steps` block) already shows a short, skippable, step-based walkthrough once per device/profile before a module's first use, reopenable via a header button. It currently only explains *what a module covers* - it doesn't yet offer a real "how do you want to start" choice. |
| 2. Topic primers | **New** | No equivalent exists. This is genuinely new content + a new view. |
| 3. Flashcards | **Exists, unchanged** | The existing detail/flashcard view, topic-filtered, with "try it yourself" self-answer. |
| 4. Smaller practice exams | **New mechanic** | Today there is flashcards (no pressure, browse-only) and Exam Simulation/Training (fixed 30 questions, real pass/fail rule, feeds certificates for compliance modules). There is no lightweight, low-stakes, shorter quiz tier in between. |
| 5. Relearn missed ones | **Already wired, verify it stays wired** | `feedExamResultsIntoSrs()` already pipes any exam-shaped attempt's right/wrong answers into the Leitner spaced-repetition schedule (DN-16) automatically - this already works for Exam Simulation/Training today. The new practice-quiz tier just needs to call the same generic hook; it does not need new tracking logic invented from scratch. |
| 6. Final exam | **Exists, unchanged** | Exam Simulation, reframed in the funnel as the graduation point rather than the only "real" option. |

## 2. New content type 1: the shape/category primer

A single, short primer (5-8 chunked cards, each well under a minute to read) teaching that a
sign's **shape and color already tell you what kind of rule it is**, before the learner has to
memorize individual signs at all:

- Triangle, yellow/white with red border → **Gefahrzeichen** (warning - advisory, not a command).
- Red circle → **Verbotszeichen** (prohibition - a hard "not allowed").
- Blue circle → **Gebotszeichen** (mandatory action - a hard "must do").
- Rectangle (various colors) → **Richtzeichen** (guidance/information).

This maps exactly onto the four categories `assets/build_sign_reference.py` already assigns every
sign into (`gefahrzeichen`/`verbotszeichen`/`gebotszeichen`/`richtzeichen`, plus `sonstige` for
uncategorized leftovers) - the taxonomy already exists in `app/data/fuehrerschein/sign_reference.json`,
it's just being used today only as a reference-view grouping, not as a taught concept. Reusing it
here means zero new legal claims (the categorization is already sourced from `generate_signs.py`'s
own template mapping) and a natural "now go browse the Sign Reference view, sorted by these exact
categories" handoff at the end of the primer.

Also covers the PO's "why signs are one-sided" point as a concrete, memorable fact: German traffic
signs are genuinely designed to be unreadable/blank from the back specifically so a driver facing
the wrong direction doesn't misread a rule meant for someone else - a good closing hook that also
sets up the situational-crossing primers (section 4) by establishing that *who* a sign applies to
depends on *where you're standing*, not just what the sign says.

**Module scope**: this is Fuehrerschein/Motorrad/LKW-specific (StVO signs). Not applicable to
Angelschein or the workplace-compliance modules - they have no sign-shape system.

## 3. New content type 2: topic primers

One short primer per `topic_code`, matching the same topics already used for the topic-filter chips
(`TOPIC_LABELS`) - so the content model already has its natural key. Each primer: the core rule in
plain language, the *why* (the underlying logic, not just the fact), a short "here's the trap"
callout naming the specific way people usually get this topic wrong, then a direct handoff into
`state.topicFilter` already scoped to that topic ("try 5 questions on this now").

Applies to every module eventually, but content depth/format should flex per topic:

- **Fuehrerschein**: 11 topics (verkehrszeichen, vorfahrt, gefahr, umwelt, verhalten, autobahn,
  parken, ladung, fahrtuechtigkeit, erstehilfe, anhaenger_be) - the biggest, most mature content
  set, natural pilot.
- **Motorrad/LKW**: same shape, smaller topic counts (5 and 4 respectively).
- **Angelschein**: fishing-license topics - same format should work, not yet scoped in detail.
- **Compliance modules** (Datenschutz, Arbeitssicherheit, KI-Verordnung, IT-Sicherheit,
  Hinweisgeberschutz): same primer shape works well here too ("GDPR basics in 8 minutes" for
  Datenschutz's topics) - arguably even more valuable here, since workplace-compliance learners are
  often required to complete training with zero prior context, more so than a driving-test
  candidate who's usually had some real-world exposure to traffic already.

**Sourcing discipline** (per `AGENTS.md`'s non-negotiable constraints - this applies in full):
primers must be written fresh from primary sources (StVO/StVZO for driving content, the actual
statute text for compliance modules), never paraphrased from a driving-school textbook or
compliance-training vendor's explainer material, and must carry the same `legal_review_status: "NOT
legally reviewed"` flag every other content batch in this project starts with, until DN-12 happens.

## 4. New content type 3: situational crossing/scenario primers

A deeper layer on top of topic primers, for the topics where "a situation, reasoned through" is the
actual shape of the rule rather than "a fact to know":

- **Vorfahrt** (flagship pilot): a short **decision flow** - is there a sign? Follow it. No sign, is
  it a roundabout? Different rule applies. Neither? Default to right-before-left - followed by 3-4
  **worked examples**, each a specific intersection walked through step by step. This can reuse
  DN-3's existing 7 birds-eye Vorfahrt diagrams (numbered priority markers, already visually
  verified) as source art, adding the missing explanatory layer ("car 2 waits *because* no sign
  overrides the default and this isn't a roundabout") on top of already-verified facts rather than
  inventing new ones.
- **Autobahn**: overtaking scenarios - who may pass whom, when, on which side.
- **Gefahrenlehre**: a specific hazard scenario (fog, black ice, aquaplaning) and the correct
  response chain.
- **Parken und Halten**: lighter format than a full decision tree - more "which of these curb/sign
  combinations lets you park" visual comparisons, since it's about correctly reading a specific
  configuration rather than reasoning through multiple actors.
- **Verkehrszeichen**: doesn't need its own scenario format - it's fully covered by the
  shape/category primer (section 2) feeding into these.
- **Erste Hilfe**: doesn't fit this format at all - it's procedural (an ordered sequence of steps),
  not situational. Would want a checklist-walkthrough format instead, out of scope for this doc.

**Open design question**: general decision-flow-first-then-examples, or a pure gallery of worked
examples? Not mutually exclusive - a short flow up front, then a handful of worked examples applying
it, is probably right, but changes how much new diagram art each topic needs versus how much it can
lean on what's already shipped (Vorfahrt can lean heavily on existing art; Autobahn/Gefahrenlehre
would need new diagrams).

## 5. New mechanic: the practice-quiz tier

The genuinely missing rung in the funnel. Distinct from both existing modes:

|  | Flashcards | **Practice quiz (new)** | Exam Simulation |
|---|---|---|---|
| Length | Browse at will | Short, e.g. 10-15 questions | Fixed 30 (`EXAM_QUESTION_COUNT`) |
| Scope | Topic-filtered or all | Topic-scoped, mixed, or "overall" (learner's choice) | Fixed topic-weighted draw (`EXAM_TOPIC_DRAW`) |
| Pressure | None - reveal at will | Low - immediate right/wrong, a score at the end | Real - pass/fail rule, timer in Simulation sub-mode |
| Stakes | None | None - explicitly casual, retake-friendly | Real - Simulation passes feed `recordCompletion()` and the certificate/credential system |
| Feeds Leitner SRS | Only via explicit know/don't-know self-assessment | Yes, via the same generic `feedExamResultsIntoSrs()`-style hook exam mode already uses | Yes (already wired) |

Framing matters as much as mechanics here, per the PO's brainstorm: this tier should feel like "try
a quick round," not "a smaller exam" - the UI copy needs to actively signal *no stakes* so a
beginner isn't afraid to attempt it, and a "dare to take the real exam early" framing works for the
*opposite* type of user (confident/returning) choosing to skip straight to Exam Simulation as a
diagnostic. Both are legitimate entry points into the same underlying quiz-drawing logic
(`drawExamQuestions()` already generalizes across modules); the practice-quiz tier is really a
lower-stakes, shorter, more flexibly-scoped sibling mode reusing most of that machinery, not a
parallel implementation.

**Open design question**: does an early, voluntary Exam Simulation attempt that happens to pass
count as the module's real, certificate-worthy completion? Recommended: yes - a genuine pass is a
genuine pass regardless of when it's attempted, and a fail should read as useful diagnostic
information, never a strike against the learner. Worth an explicit PO confirmation before Phase 3
below, since it touches the existing compliance-credential system's behavior.

## 6. New entry point: the kickstart path wizard

The piece that ties everything together and gives it a name a user actually sees, per the PO's "it
needs to be well explained that this is a kickstart learning mode" instruction. Extends the existing
DN-43 module-intro-wizard rather than building a new mechanism:

- Shown automatically the first time a user opens a module (same trigger DN-43 already uses -
  `hasSeenIntro(examType)` / `markIntroSeen(examType)`), reopenable afterward from the same header
  entry point the "About this module" button already provides.
- Instead of (or in addition to) the current "what does this module cover" walkthrough, presents an
  explicit **three-path choice**, each with real explanatory copy rather than bare labels:
  - **"Learn the basics first"** → topic primers (section 3), explicitly reassuring ("you don't
    need to know anything yet, this takes 5-10 minutes and gets you ready to practice").
  - **"Study with flashcards"** → the existing flashcard view, framed as self-paced, no pressure.
  - **"Test yourself"** → Exam Simulation, reframed as diagnostic rather than a one-shot final gate
    ("see what you already know, then we'll show you exactly what to focus on") - and should route
    a low score toward the practice-quiz tier or topic primers for whatever topics it flagged,
    closing the loop rather than leaving the learner stuck with just a number.
- On a **return visit**, this could evolve from a one-time onboarding screen into a light ongoing
  dashboard - "3 of 11 topics learned, 12 flashcards reviewed, last exam attempt 68%, due for
  review: 4 questions" - motivating a learner to keep coming back rather than only ever seeing this
  once. This needs its own small piece of state (which primers has this profile completed, per
  module) - a new, cheap addition alongside the existing `intro-seen-<examType>` /
  `dn-p-<profile>-*` localStorage keys, following the same per-profile namespacing discipline
  already in place.
- Nobody is ever forced through all three - a confident user must be able to jump straight into
  Exam Simulation from this very first screen, and once a path is chosen the wizard doesn't
  reappear except via its explicit reopen entry point.

## 7. What this does NOT cover (deliberately out of scope for this doc)

- **Erste Hilfe's checklist/procedural format** - flagged above as needing a different shape
  entirely; worth its own follow-up scoping once the primer/scenario formats above are built and the
  right pattern for a step-sequence format is clearer.
- **Any new legal claims** - every primer, scenario, and quiz reuses or reasons more deeply about
  content already verified elsewhere in this project (existing questions, existing sign categories,
  existing diagrams); nothing here should introduce a fact not already sourced.
- **A full redesign of the module-intro-wizard's existing "what this module covers" content** -
  that content stays; the wizard is being extended with a path choice, not replaced.
- **DN-43's existing DE/EN-only gap in `modules_manifest.json`'s `intro.steps` content** (a
  pre-existing, separately-flagged gap, distinct from `MODULE_INTRO_STRINGS`' UI chrome strings
  which already cover all 12 locales) - real, but a pre-existing issue this doc didn't create; worth
  fixing at some point but not blocking on for this feature.

## 8. Recommended build order

Content-first, mechanic-second, entry-point-last - each phase should be independently useful even if
the PO stops after it, and each later phase depends on the one before actually existing:

1. **Phase 1 - shape/category primer + Fuehrerschein topic primers.** Pure content, reuses existing
   sign-category taxonomy and topic-filter infrastructure, zero new app mechanics. Fuehrerschein
   only, as the pilot. Smallest, fastest-to-ship, immediately useful on its own (reachable via a
   simple new entry point even before the full wizard exists, e.g. a small "Learn the basics" link
   from the existing module-intro screen).
2. **Phase 2 - situational crossing primers for Vorfahrt** (reusing DN-3's existing diagrams), then
   Autobahn/Gefahrenlehre/Parken once the format is proven.
3. **Phase 3 - the practice-quiz tier.** The genuinely new mechanic; needs the PO's confirmation on
   the "does an early exam pass count as real completion" question first (section 5). Reuses
   `drawExamQuestions()`/`feedExamResultsIntoSrs()` rather than new scoring logic.
4. **Phase 4 - the kickstart path wizard**, tying phases 1-3 together with the three-path choice and
   framing copy. Deliberately last, since it's presenting choices that need to already exist and
   work before they can be offered as a menu.
5. **Phase 5 (stretch) - roll the primer content out to every other module** (Motorrad, LKW,
   Angelschein, all 5 compliance modules) once the Fuehrerschein pilot has proven the format,
   following this project's established pilot-then-scale pattern (same as DN-11/DN-48/DN-50).

## 9. Open questions for the PO

- Confirm the "early voluntary exam pass still counts as real completion" call (section 5) before
  Phase 3 starts.
- Decision-flow-then-examples vs. pure worked-example-gallery for situational primers (section 4) -
  can be decided per-topic rather than as one global rule.
- Whether the kickstart wizard's return-visit dashboard (section 6) is worth building in Phase 4, or
  should wait for real usage signal that a one-time wizard isn't enough.
- Whether to pilot Phase 1 on Fuehrerschein only (recommended) or attempt it across multiple modules
  simultaneously - recommended against, given every other successful content rollout in this project
  went pilot-then-scale, not all-modules-at-once.
