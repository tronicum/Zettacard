# ADR-app-0003 — What a Zettacard record claims, and what binds it to the material

**Status:** Draft, for PO approval. Stated by the PO 2026-09-08; written up here.
**Supersedes nothing.** Extends ADR-app-0002 § 4 (what a badge means) with a
per-class taxonomy and adds a versioning invariant it did not cover.

## The problem

Zettacard now issues a record when a Prüfungssimulation is passed, and the same
machinery produces it for every module. But the modules are not the same kind of
thing, and a record that reads identically across them is dishonest in at least
one direction:

- Passing the Führerschein simulation predicts readiness for a **state exam that
  someone else administers**. Zettacard cannot award a licence and never will.
- Passing a Datenschutz Pflichtschulung completes **a course Zettacard wrote**.
  There is no external exam anywhere. Here the record IS the artefact, and
  Zettacard is the one vouching for it.
- Passing the California simulation attests **nothing**, because there is no
  exam it could predict for a learner in Germany. ADR-app-0002 § 4 already says
  `compare` gets no badge; the code did not implement that until 2026-09-08.

A learner, and more importantly a reader of the record — an employer, a
colleague on LinkedIn — must be able to tell which of these they are looking at
without reading documentation.

## Decision 1 — three classes, derived from `kind`

No new field. `kind` already carries the distinction.

| Class | `kind` | Who examines | What a record may claim |
|---|---|---|---|
| **Prepares for an external Prüfung** | `licence`, `cert` | someone else (TÜV/DEKRA, LF, the Prüfungsausschuss) | "passed a Zettacard simulation of X" — a **prediction of readiness**, never the qualification |
| **Zettacard's own course** | `compliance` | Zettacard | "completed Zettacard's course in X, evidenced by N passed quizzes" — Zettacard **vouches for this**, and says so |
| **For interest** | `compare` | nobody | nothing. No badge, no share. A playful outcome only |

The middle class is the one that was under-described. These courses are derived
— by Zettacard, as any provider derives theirs — and what they prove is exactly
that the learner worked through the material and demonstrated it repeatedly by
passing the quizzes for each module. That is a real, ordinary thing, and it is
the one class where Zettacard is entitled to be the issuer rather than the
predictor. Saying so plainly is stronger than borrowing the language of an
authority that is not involved.

**Consequence for wording.** The record's *visible name* must place itself in
its class, because the surfaces it appears on (a LinkedIn Licenses &
Certifications card, a PDF header) show a name and an issuer and nothing else.
"Führerschein - Klasse B / Zettacard" is a misrepresentation on its face
regardless of what the payload says; it was live until 2026-09-08.

## Decision 2 — the 2027 Fahrschulreform changes the preparation, not the exam

The PO's point, and it is correct in direction: from 2027 this kind of
self-training is expected to become a legal route. Two precisions, because
this is exactly the claim that leaks into marketing copy:

1. **It is draft law, not law.** As of August 2026 the reform is still in
   parliamentary proceedings; early 2027 is the earliest anticipated date. Until
   it is in force, nothing may be written in the present tense.
2. **What becomes legal is self-study as PREPARATION.** The Präsenzpflicht for
   Theorieunterricht is to be dropped and app-based learning is explicitly named
   among the permitted preparation methods — but *die Theorieprüfung bleibt
   bestehen*. The state exam remains, administered by the official body. Nothing
   in the reform lets a private provider issue a licence or an official
   certificate.

So the reform makes Zettacard a **legitimate way to prepare**, which is worth
saying and worth being proud of. It does not move Führerschein out of the first
class above. After 2027 as before it, Zettacard predicts; the state examines.

Sources: [fahrschulreform2027.de](https://fahrschulreform2027.de/),
[Kanzlei Dr. Hartmann & Partner](https://www.ra-hartmann.de/fuehrerscheinreform-2027-was-sich-bei-fahrschule-theoriepruefung-und-fahrstunden-aendern-soll/).
Re-check before any copy ships: a draft can change, and this one is load-bearing.

## Decision 3 — the exam is versioned; the material may improve without it

**Invariant, as the PO stated it: the exam must be versioned and the test must
match that version. Questions can improve or change. If a change would alter
the exam questions' answers, the exam must be adjusted. If not, the material
can improve and diversify freely against the same exam.**

This is the rule that makes versioning usable rather than ceremonial. A digest
over the whole module would bump on a typo fix, a new locale or a better
explanation, so every record would cite a version nobody else ever had and the
number would mean nothing. The distinction that carries meaning is not "did
anything change" but **"could this change what is correct".**

### Two versions, not one

**Exam version** — a digest over the answer-determining surface only:

- the set of question ids the module draws from
- each question's `correct`, `points`, `high_stakes`
- each question's canonical-locale (`de`, the KB's `SOURCE_LOCALE`) question and
  option text, because rewording the German can change what the right answer is

**Material version** — a digest over everything else: explanations,
translations, course prose and derived lessons, media, and the picker copy.

A record cites the **exam version** it was tested against; that is the claim.
It may also cite the material version it studied from, which is information,
not evidence.

### What this permits, and it is most of the work

Improving a translation, rewriting an explanation, adding a locale,
regenerating the derived lessons after a topic split, adding a diagram — all
move the material version and leave the exam untouched. Records stay valid.
Nobody is asked to re-certify because Ukrainian got better. That is the point:
the material is meant to diversify, and a versioning scheme that punished
improvement would be a scheme people route around.

### What must bump the exam

Changing an answer key. Adding or removing a question from the draw. Changing a
question's points or its `high_stakes` flag — both change the pass rule for the
run, since two wrong safety-critical questions fail it regardless of score.
Rewording the canonical German such that a different option becomes right.
DEF-0002 is the worked example: `parken-17` had been keyed "wheels toward the
kerb" for *uphill* parking, which steers an unbraked car into the road. Fixing
that changed what "passed" means, and a record made before it attested
something different. It should bump.

### The translation edge, deliberately drawn

A translation is material, not exam — but a learner sits the run in their own
language, so a mistranslation changes what *they* were asked. The line is drawn
at the canonical locale because that is where correctness is defined, and a
translation that changes meaning is a **defect**, not a version. The machinery
for that already exists and should be the mechanism: the KB stores
`hashes.per_locale` and `source_hash` per question, `staleness.py` compares
them, and the export refuses stale locales unless `--allow-stale`. A translation
that drifts from a corrected source is caught there, before it can reach a run.

### What is needed to implement it

1. Compute both digests at build time from the KB's existing hashes — no new
   hand-kept field, and `source_hash` is most of the exam digest already.
2. Publish `exam_version` and `material_version` per module in `modules.json`.
3. Carry `exam_version` on every completion record, alongside the run conditions
   it already has (`passedAt`, `errorPoints`, `wrongHighStakes`,
   `totalQuestions`) plus the pass rule applied and whether it was timed.
4. The app can then say something true it cannot say today: "taken against exam
   version X of 2026-09-08; the current exam version is Y" — and stay silent
   when they match, which will be the normal case.
5. An old record stays valid and stays readable as what it was. The archive is
   the point, not an embarrassment.

Whether an old record should *expire* is a separate question, and for compliance
it is the employer's to answer. The decision here is only that a record must be
precise enough for someone else to decide.

## What this does not do

- It does not create a professional or "Wirtschaftsprüfer-level" tier. Same
  content taken by someone whose job depends on it is the same evidence; what
  differs is the reader's context, which the product cannot certify. Precision
  is offered instead of weight.
- It does not vary a run's size or pass bar by anything the learner says about
  themselves. For the first class those mirror the real exam, and softening them
  would make the prediction a lie.
- It does not reopen ADR-app-0002.

## Implementation status

Done 2026-09-08 (commit `1ded456`):
- `compare` modules no longer issue a record at all.
- The credential's visible name leads with the issuer and the nature of the
  claim; the qualification is the subject of the assessment, not the award.

Not done:
- Per-class wording for the record title and the Open Badges `achievement.name`
  (three templates, KB-mastered, 18 locales).
- The exam/material version split, and carrying `exam_version` plus the run
  conditions on every record.
- The fixed self-assessment sentence on compliance records.
- Anything about 2027 in user-facing copy — blocked on the reform actually
  passing.
