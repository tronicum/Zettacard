# Führerschein translation completeness — assessment and plan

Status: PLANNING ONLY — no translation work has been implemented from this
document yet, per explicit instruction (2026-08-06). This is an honest
assessment of what's actually there today plus a proposed path forward, not
a claim that any of it has been done.

## What "not translated into all languages" turned out to mean

A direct check of `data/pilot_questions.json` (531 questions across all
Führerschein topics, both classes B/BE) confirms every single question
already has a non-empty `text` and `explanation` entry for all 12 supported
locales (de, en, uk, pl, ar, zh, hi, tr, fr, ru, es, it) — there is no
question anywhere in the Führerschein module that falls back to German or
English because a translation is technically missing. In that narrow
sense, coverage is already 100%.

So the concern this document addresses isn't missing translations — it's
**translation quality assurance**, which is a real and much less certain
thing. Two concrete gaps are already known:

1. **A confirmed, specific desync.** This session's content-quality pass
   (DN-20b/DN-25) rewrote the DE (and reviewed EN) text for 42 of the 50
   `vorfahrt-01..25`/`zeichen-01..25` questions, improving distractors and
   simplifying wording. 8 of those ids had DE wording change meaningfully
   enough that the other 10 locales' translations (uk/pl/ar/zh/hi/tr/fr/ru/
   es/it) now describe the OLD German phrasing, not the new one:
   `vorfahrt-04, vorfahrt-05, vorfahrt-06, vorfahrt-09, vorfahrt-13,
   vorfahrt-17, vorfahrt-24, zeichen-06`. This is a small, well-defined,
   already-flagged fix (8 questions × 10 locales = 80 translation entries).

2. **An unverified assumption for everything else.** The other 481
   Führerschein questions (topic breakdown below) have never had a
   systematic quality/accuracy pass on their non-DE/EN locales — they were
   populated via earlier incremental translation rounds (the various
   `data/i18n_<locale>_*.json` and `data/batch*_questions.json` files still
   sitting in the repo are historical staging artifacts from those rounds,
   already merged into `pilot_questions.json` — not a sign of missing
   work, but also not evidence the merged translations were ever spot-
   checked for accuracy against the German canonical meaning). DE is
   authoritative and EN has had real editorial attention throughout this
   project's history, but the other 10 locales for the bulk of the content
   have only ever been machine/batch-translated once, with no independent
   verification step comparable to what DE/EN got.

### Current topic breakdown (531 questions total)

- `verkehrszeichen` (signs): 138
- `vorfahrt` (right of way): 44
- `erstehilfe` (accidents/first aid): 42
- `autobahn`: 41
- `fahrtuechtigkeit` (fitness to drive): 40
- `gefahr` (hazard perception): 40
- `ladung` (loading/cargo): 40
- `parken`: 40
- `umwelt` (environment): 40
- `verhalten` (behavior): 40
- `anhaenger_be` (BE-only trailer questions): 26

## What a real QA pass would actually involve

Verifying translation *accuracy* (not just presence) at scale needs a
different method than the presence check above. Two realistic approaches,
not mutually exclusive:

1. **Back-translation spot-check.** For a sample of questions per topic per
   locale, translate the stored non-DE/EN text back to German (or English)
   and compare the *meaning* against the canonical DE question - catches
   wrong-answer-key mismatches, garbled grammar, or a translation that
   drifted from the German legal fact it's supposed to represent (the
   highest-stakes failure mode, since a mistranslated `correct` explanation
   could teach someone the wrong traffic rule in their own language).
2. **Native-fluency review pass**, ideally per locale, reading the stored
   text directly rather than round-tripping through DE/EN - catches
   awkward phrasing and register issues that back-translation can mask
   (a back-translation can round-trip "successfully" while the original
   was still clunky or unnatural in that language).

Both are realistically AI-assisted (WebSearch-verifiable facts, an LLM
doing the back-translation/native-read pass) rather than requiring 10
human native speakers, but the RESULT needs the same honesty this
project already applies to legal content: flag confidence level, don't
claim more certainty than the method actually supports, and treat any
found high-stakes (safety-critical, `high_stakes: true`) mistranslation as
a real bug, not a style nit.

## Proposed phased plan (not yet started)

**Phase 0 — quick, already-scoped fix.** Sync the 8 known-desynced ids'
other-10-locale translations to match their updated DE wording. Small,
bounded, no new process needed — a single agent dispatch could do this in
one pass.

**Phase 1 — targeted pass on `high_stakes` questions.** Of the 531
questions, a WebSearch/manifest-derivable subset carries `high_stakes:
true` (safety-critical - wrong information here is the most damaging kind
of translation error). Prioritize back-translation spot-checks on this
subset first across all 10 non-DE/EN locales, since it's the smallest set
with the highest cost of being wrong.

**Phase 2 — full-catalog back-translation sweep.** Extend the same method
to the remaining `grundstoff`-flagged (core-curriculum) questions, then
the rest, topic by topic. This is the largest phase - 481 questions × 10
locales is a genuinely big sweep, well suited to a parallel-agent
Workflow (one agent per locale, or per topic, given this project's
established pattern) rather than a single sequential pass, once the user
explicitly opts into that scale of work.

**Phase 3 — native-fluency spot-check on a sample.** After the
back-translation sweep clears the "is this factually the same rule"
question, a smaller targeted native-fluency pass on a random sample per
locale (not the full catalog) checks for the phrasing-quality issues
back-translation can't catch, similar in spirit to how this project has
handled sign-icon verification (systematic pass, then targeted follow-up
on lower-confidence findings).

**What this is NOT:** a claim that today's translations are wrong. It's
likely most of them are fine — batch translation of factual, short-form
quiz content is one of the more reliable use cases for it, and nothing in
this session's Playwright verification across languages has surfaced a
broken or nonsensical render in any locale. This plan exists because
"probably fine" and "verified" are different claims, and this project's
own standing discipline (WebSearch-verify legal facts, don't assert
without checking) argues for closing that gap deliberately rather than
assuming it's already closed.

## Recommendation

Do Phase 0 (the 8-id desync fix) essentially any time - it's small,
bounded, and already fully scoped. Hold Phases 1-3 until the PO explicitly
wants to commit that scale of review effort (this could reasonably be a
multi-agent Workflow given the volume), since a full 481-question ×
10-locale sweep is a substantial effort that deserves an explicit go-ahead
rather than being bundled into an unrelated task.
