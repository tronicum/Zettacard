# ADR-0006: Automated Translation-Validation Engine (semantic + acoustic audit)

| | |
|---|---|
| **Status** | Proposed (2026-09-05) |
| **Supersedes / extends** | Extends `ADR-llm-translation-qa.md` (strategy), `ADR-ollama-setup.md` (ops), `ADR-tts-accessibility.md` (audio delivery). Incorporates the measurement in `docs/adr/tier3-first-measurement.md` as a hard design input. Replaces nothing. |
| **Numbering note** | `docs/adr/` currently holds both `ADR-0001` and `ADR-001`, plus `0003`, `0004`, `0005`. This document takes `0006`, the next number that no file in either scheme uses. It uses the four-digit form, which is the majority form, and does not touch the two colliding files; reconciling them is a separate housekeeping change. |
| **Intended file location** | `docs/adr/ADR-0006-translation-validation-engine.md` |

---

## 1. Decision in one paragraph

Zettacard's translation audit will be a **tiered, evidence-gated pipeline in which model judgement is the last and narrowest tier, never the first, and in which every model signal is admitted per locale only after it has beaten a measured false-positive bar on the committed seed set.** Tiers 0 and 1 (`scripts/translation_ledger.py`, `scripts/check_data_integrity.py`) remain the only CI gates. A new deterministic Tier 1b covers numerals, units, legal-term pairs and script homoglyphs without a model. Tier 3, the LLM judge, is restructured from one global rubric call into three narrow passes: (A1) the existing six-boolean equivalence rubric, now restricted to stem, correct option, polarity, numbers and explanation; (A2) a *blind* logical-skeleton extraction pass that never shows the model both languages in the same prompt; (A3) a *pairwise, control-calibrated* distractor pass that replaces the `distractor_became_correct` field, which was measured to carry zero information at 3B. The acoustic audit (Component B) is built on **forced alignment against known text plus deterministic signal analysis over a synthesis manifest**, with free ASR and multimodal audio judgement demoted to gated, per-locale advisory signals because both have unmeasured and, for `bar`/`apc`, probably worse error characteristics than the Piper output they would be auditing. The output (Component C) is an extension of the existing receipt format in `data/translation_state/verdicts/<module>.jsonl`, adding a typed `findings[]` array and a per-locale calibration reference, so that CI can continue to verify receipts by hashing alone.

The rest of this document justifies each clause of that paragraph with the measured facts that force it.

---

## 2. Context the design must not contradict

### 2.1 The data, as it actually is

A "cell" is one `(module, question id, locale)` triple. The master file `data/pilot_questions.json` (531 questions for `fuehrerschein`) carries `text.<locale>.{question, options{a..d}}` and `explanation.<locale>` for fifteen live locales (`de en es fr it pl ru uk tr ar hi zh bar fa ro`), with `he apc ja ko` partial. `data/build_modules.py` fans this out into `app/data/<module>/core.json` (`id`, `correct[]`, `high_stakes`, `points`, `question_type`, `image_ref`, `legal_basis`, `class_scope`) and one `locales/<lang>.json` per language. 526 questions are `single_choice`; five (`mehrfach-01..05`) are `multi_choice` with two or three correct letters, scored all-or-nothing. 82 questions are `high_stakes`.

Two facts about that shape drive everything below. First, **the answer key is shared across all locales**: `correct` lives in `core.json`, not in the locale file, so a translation is "correct" only relative to letters it did not choose. Second, **German terms are kept verbatim inside every locale by convention** (`«Fußgänger»`, `Zeichen 214`, `1010-53`, `(Halten)`), including inside RTL Arabic and Persian and inside Devanagari, Hindi, and CJK text. The judge, the numeral checker and the acoustic auditor all have to treat a German token inside a non-Latin sentence as *expected*, not as an untranslated leftover.

### 2.2 The defects found so far, and what class each belongs to

| Defect | Cells | Class | What caught it |
|---|---|---|---|
| `zeichen-68`: ten locales describe an obstacle-passing sign; German describes Zeichen 214 (mandatory direction) | 10 | **Staleness** (German revised, only `en` regenerated) | Tier 0 ledger, <1 s, zero FP |
| `zeichen-132`: eight locales describe a "Mofa frei" plate; German describes Zusatzzeichen 1010-53 "Fußgänger" | 8 | Staleness | Tier 0 |
| `zeichen-04`: sign number 133 instead of 136 | 5 | Staleness, surfaced as a numeral mismatch | Tier 0; also catchable deterministically by numeral diff |
| `high_stakes` authoring token leaked into the German explanation, then translated into ten languages ("hence marked high_stakes", "d'où la qualification high_stakes") | 99 | **Source contamination propagated faithfully** | Tier 1 leaked-token check |
| Ukrainian with Latin homoglyphs inside Cyrillic words | n/a | **Encoding/script defect**, invisible to a reader, breaks search | Ad-hoc script inspection; needs a Tier 1b rule |

None of these was a translation-*quality* failure in the sense that a translation benchmark would measure. Three were "the translation is a perfect translation of an older German"; one was "the translation is a perfect translation of a contaminated German"; one was "the translation is fine, the bytes are not". The point is not that model judgement is unnecessary — the seed set's synthetic classes (swapped correct option, foreign cell, digit flip) are exactly the cases where only a bilingual reader can tell — but that **the cheapest tiers have the best precision and must run first, and the model must only ever see cells that have already passed them.**

### 2.3 The Tier 3 measurement that shapes Component A

`docs/adr/tier3-first-measurement.md` records the first real run of `scripts/i18n_qa/judge.py` (Ollama 0.33.3, `qwen2.5:3b-instruct`, 16 seed cells, `es` + `fr`):

- `distractor_became_correct` fired on **16 of 16** cells — every known-good and every known-bad cell alike. 100 % recall, 100 % false-positive rate. The field is indistinguishable from a constant.
- The five semantic booleans alone (stem / correct-option / polarity / numbers / explanation) gave **22 % recall at 14 % FP** and caught both real sign-swaps.

That is a small model on a small sample and the numbers themselves will move. What will not move is the *shape* of the result: a global question of the form "which of these three options is now a viable answer?" is one the model answers by always naming something, because the prompt has told it in capitals that distractors are the thing to worry about and a 3B model resolves a salient instruction into a positive response. The rest of the rubric asked "is X preserved?" and the model could answer "yes"; the distractor field asked "which letters?" and an empty list is a much less natural completion than a letter. **The failure is in the question posed, not only in the model size.** §4.4 redesigns the question; it does not re-specify the measured one.

### 2.4 Why distractors are hard here specifically

This project *deliberately* allows non-literal distractors. `vorfahrt-03` is a live example: the German option d is "so lange langsam weiterrollen, bis die Kreuzung frei ist"; the Chinese option d is "只有在天黑时才需要停车" ("stop only when it is dark"). That is **correct behaviour** under the localisation convention. The auditor therefore has exactly two questions per distractor — *is it still clearly wrong for the target question* and *is it not a paraphrase of the correct option* — and any check that measures literal equivalence flags hundreds of good cells. This is already stated in `prompts/judge_v1.md` and enforced by `derive_verdict()`'s discard of correct-key letters; this ADR keeps that rule and builds the pairwise pass around it.

### 2.5 The TTS pipeline, as measured

Piper renders every locale locally. Russian rendered at roughly 1.7 s per utterance on the development machine; `fuehrerschein` in one locale is 531 × 6 = 3,186 utterances, approximately 28 MB Ogg Opus and 58 MB AAC. Delivery is Ogg Opus with an AAC/M4A fallback, because Safari plays Opus only in an Ogg container and only from 18.4. German terms are verbatim in every locale, and a **mixed-voice splice** (German voice for German terms, target voice for the rest) has been prototyped and works. That splice is the single most important fact for Component B: a *correct* clip legitimately changes voice mid-sentence, so any timbre-discontinuity detector without access to the splice plan will produce false artifacts on precisely the cells that were rendered correctly.

### 2.6 The batch unit named in the brief

The brief's ingest unit is "4 DIN A4 pages of exam questions (German vs target) plus a 15-minute TTS track". Mapped onto this repository's data: a bilingual cell (question, four options, explanation, both languages) is roughly 150–250 words of German plus the target; four A4 pages of bilingual text at exam-sheet density is on the order of **20–30 cells** (estimate; depends on script and layout). A cell rendered as six utterances at conversational rate runs roughly 35–60 s of audio (estimate; not yet measured on the shipped Opus files — `ffprobe` over `app/data/<module>/audio/` will give the real number), so 15 minutes is again on the order of **15–25 cells**. The two inputs are therefore the *same* batch seen twice, and the engine keys the audio audit to the cells of the text batch rather than treating the audio as an opaque quarter-hour.

---

## 3. Architecture overview

```
                    ┌──────────────────────────────────────────────────────────┐
  batch manifest ──►│ Tier 0  translation_ledger.py   staleness (hash)         │ CI gate (exists)
  (module, ids,     │ Tier 1  check_data_integrity.py structural / leaks       │ CI gate (exists)
   locales,         │ Tier 1b numeral+unit diff, term-pair registry, script     │ CI gate (NEW, no model)
   audio ids)       │         homoglyphs, TTS verbalisation table              │
                    ├──────────────────────────────────────────────────────────┤
                    │ Tier 2  embed_screen.py  ranking only                    │ local (exists)
                    ├──────────────────────────────────────────────────────────┤
                    │ Tier 3  A1 equivalence rubric  (judge_v2: 5 booleans)    │ local, gated per locale
                    │         A2 blind logic-skeleton extraction + diff        │ local, gated per locale
                    │         A3 pairwise distractor pass with controls        │ local, gated per locale,
                    │                                                          │   OFF until it earns it
                    ├──────────────────────────────────────────────────────────┤
                    │ Tier 4  B1 manifest + DSP artifact scan   (deterministic)│ local, no model
                    │         B2 forced alignment vs known text (small model)  │ local, gated per locale
                    │         B3 unit-segment ASR spot-check    (ASR)          │ local, gated per locale
                    │         B4 multimodal audio judge         (sampled)      │ local, advisory only
                    ├──────────────────────────────────────────────────────────┤
                    │ Receipts  verdicts/<module>.jsonl  (schema v2, §6)       │ committed; CI verifies
                    │ Calibration  calibration/<locale>.json  (§5)             │ committed; CI verifies
                    └──────────────────────────────────────────────────────────┘
```

Three properties are invariant across every tier:

1. **The model never decides.** Every verdict is derived in Python from typed fields (`derive_verdict()` today; `derive_findings()` in v2), unit-tested over the full combinatorial space of inputs. A model's own `verdict` field is recorded as `model_self_verdict` and ignored.
2. **Every finding carries a quote.** A boolean `false` or a flagged letter without a source-side and target-side quote is downgraded to `unsure`; this is already the rule and it is retained because an unquotable accusation cannot be reviewed and cannot be used by a self-correcting translator.
3. **Every signal is gated per locale by a committed calibration record.** A signal that has not beaten its FP bar for a locale is still *run* (so that the numbers keep accumulating) but its findings are emitted with `gated: true` and excluded from the derived verdict. CI checks the gate without a model by comparing the finding's `signal` against the calibration file's `enabled[]` list.

The pipeline is short-circuiting in the sense that Tier 3 does not run on a cell that Tier 0 marks stale or Tier 1/1b fails. That is not an optimisation; it is a correctness rule. A stale cell judged by a model produces a receipt whose `source_hash` no longer matches today's German, which `verify_receipts.py` would reject anyway, and the model's opinion of a stale cell is meaningless — the entire `zeichen-68` class would have come back as "stem not equivalent", which is true but is the wrong diagnosis (the fix is regeneration, not review).

---

## 4. Component A — Fixed-Logic Semantic Alignment Auditor

### 4.1 Token and context budget, measured against real cells

`build_prompt()` renders `judge_v1.md` plus two cell blocks. For a Latin-script locale a rendered prompt is on the order of 900–1,300 tokens in Qwen's tokenizer (estimate; `--dry-run --explain` prints character counts, and `prompt_eval_count` in the Ollama reply gives the true token count for every call — receipts should record it). Arabic, Hindi, Chinese and Ukrainian tokenize at roughly 1.5–3× the token density of the equivalent Latin text on most open tokenizers (estimate, varies by model; verify from `prompt_eval_count` across locales on the seed set). A 4K default context (`num_ctx` in Ollama unless overridden) is therefore enough for one cell and not enough for a "batch in one prompt" design. The engine never batches multiple cells into one prompt: it costs attention across cells, makes evidence quotes ambiguous, and destroys the one-cell-one-receipt hash discipline. The batch unit of the brief is a scheduling unit, not a prompt unit.

The per-cell token budget is spent deliberately:

- **A1** sends both languages once (the current design).
- **A2** sends *one* language per call, twice — smaller prompts, and the model cannot cheat by copying structure across languages.
- **A3** sends the target question, the target correct option(s), and *one* target distractor, three times, plus two control calls. Each of these is small (~300–500 tokens, estimate).

A full A1+A2+A3 pass is therefore on the order of 8 model calls per cell against today's 1. Against a batch of ~25 cells that is ~200 calls; at the ADR's still-unmeasured 5–15 s per call on a 7–14B model on the development Mac it is 15–50 minutes per batch per locale (estimate; `elapsed_ms` in receipts will replace this with a measurement after the first sweep). That is acceptable for an overnight sweep of the 82 `high_stakes` questions and not acceptable as a pre-commit hook, which is consistent with Tier 3 being advisory.

### 4.2 Pass A1 — the equivalence rubric, narrowed

`judge_v2.md` is `judge_v1.md` with the `distractor_became_correct` field **removed from the schema and the prose**. The remaining five booleans keep their definitions (they measured at 22 % recall / 14 % FP at 3B and caught both real sign-swaps, which is the one part of the first measurement that was encouraging). Three changes to the prompt body:

1. The distractor rule paragraph is shortened to a single sentence telling the model that options *not* marked correct are out of scope for this call. Removing the capitalised warning removes the salience that produced the constant-fire behaviour; the distractor question is asked elsewhere, differently.
2. The `evidence` field is split into `evidence_source` and `evidence_target`, each `maxLength: 200`, each required to be a **verbatim substring** of the corresponding cell block. Python verifies the substring property after the call. A quote that is not a substring is treated as no quote, and the finding downgrades to `unsure`. This costs nothing at inference time and converts "the model hallucinated an evidence phrase" from an undetectable failure into a counted one.
3. `numbers_preserved` is demoted from a model boolean to a *confirmation* of the Tier 1b numeral diff. The model still answers it, because a numeral rendered as a word (`drei Minuten` → `三分钟` → `три хвилини`) is not reachable by a regex, but a disagreement between the model and Tier 1b is itself recorded as a finding, and Tier 1b wins whenever it has a digit-level match on both sides.

The verdict derivation stays in Python and its unit tests are extended from 2^5 to include the two-quote rule.

### 4.3 Pass A2 — blind logical-skeleton extraction

This pass exists for the brief's "If X applies, unless Y occurs, you must NOT…" requirement, and its design principle is that **the model must never compare the two languages itself.** Cross-lingual comparison is the task at which a small model is weakest and at which it most readily produces a plausible-sounding rationalisation. Monolingual extraction into a fixed schema is a task at which even small models are reasonably reliable, and the comparison is then done in Python, where it is exact.

For each of the stem, each correct option and the explanation (not the distractors — see §4.4), two independent calls are made, one with the German text and one with the target text, each with the same schema:

```json
{
  "deontic":     {"enum": ["must", "must_not", "may", "may_not", "is", "is_not", "none"]},
  "agent":       {"type": "string", "maxLength": 60},
  "action":      {"type": "string", "maxLength": 120},
  "conditions":  {"type": "array", "items": {"type": "string", "maxLength": 100}},
  "exceptions":  {"type": "array", "items": {"type": "string", "maxLength": 100}},
  "quantities":  {"type": "array", "items": {"type": "object", "properties": {
                    "value": {"type": "string"}, "unit": {"type": "string"},
                    "comparator": {"enum": ["=", ">", ">=", "<", "<=", "none"]}}}},
  "scope_all":   {"type": "boolean"},
  "scope_only":  {"type": "boolean"}
}
```

`deontic` is the field that catches polarity inversions across grammatical restructuring: Cantonese and Mandarin negate the modal (`唔可以` / `不得` / `不可以`) rather than the verb, Arabic uses `لا يجوز` versus `يجب`, Hindi distinguishes `नहीं चाहिए` from `नहीं कर सकते` — and a translation engine flattening "darf nicht" into "muss nicht" (must-not into need-not) is precisely the failure that survives a fluency check. `scope_all` and `scope_only` capture the German `immer`/`auch wenn` versus `nur dann` distinction of `vorfahrt-03` (option a "immer vollständig anhalten, auch wenn kein anderes Fahrzeug zu sehen ist" versus option b "nur dann anhalten, wenn…"), which is a quantifier-scope distinction rather than a polarity one and is not captured by any of the five booleans. `conditions` and `exceptions` are free strings and are not compared by string equality — they are compared by *count* and by presence of quantities. A German option with one condition and one exception whose target skeleton has one condition and zero exceptions is a `CONDITIONAL_STRUCTURE_MISMATCH` finding; the strings are the evidence.

The Python comparator emits a finding when `deontic` differs (severity `CRITICAL_LOGIC`), when `scope_only`/`scope_all` differ (severity `CRITICAL_LOGIC`), when the exception count differs (severity `CRITICAL_LOGIC`), when the condition count differs (severity `MAJOR_LOGIC` — condition merging is often a legitimate restructuring, so this is one severity lower and needs a human), and when a quantity value or comparator differs (`CRITICAL_LOGIC`; also cross-checked against Tier 1b). Three things about this design are non-obvious and deliberate:

- The German-side extraction is **cached by source hash**. There are 531 German questions and fifteen locales; the German skeleton is computed once per German edit, not once per locale, which removes roughly half the A2 cost.
- The German-side extraction doubles as a **model competence probe**. The German text is the authoritative, well-formed input. If the model produces `deontic: none` for a German option that plainly contains `dürfen … nicht`, the model is unfit for A2 on that cell, and the target extraction is skipped and recorded as `ABSTAIN_MODEL_INCOMPETENT` rather than being compared against garbage. The seed set's German half gives the base rate of this failure per model, and it goes into the calibration record.
- Extraction is done at `temperature: 0` with the tight schema; the README's finding that determinism depends on schema tightness applies with full force here, and the `deontic` enum is the only reason the pass is reproducible enough to receipt.

What A2 cannot do: it cannot tell whether two free-text conditions mean the same thing. That is A1's job, with lower precision. A2's value is that its failure modes are *orthogonal* to A1's: A1 fails when the model is fooled by fluency, A2 fails when the model cannot parse one side. A cell has to fool both to escape.

### 4.4 Pass A3 — the distractor auditor, redesigned around the measurement

The measured signal asked, in one global call with both languages visible and a capitalised warning, "name any distractor that is now viable". It returned a letter every time. The redesign changes four things at once, and the ADR is explicit that each is a hypothesis to be measured on the seed set, not a fix known to work.

**(1) Pairwise, target-only, one distractor per call.** For each distractor letter `d`, the model receives the *target* question, the *target* correct option(s), and the *target* option `d` — and nothing in German. It is asked a three-way question with a forced enum:

```
Given this question and this correct answer, classify the candidate option:
  "clearly_wrong"   – it states a rule that is false for this question
  "same_as_correct" – it states the same rule as the correct answer, in other words
  "also_true"       – it states a different rule that is also a correct answer to the question
Quote the phrase in the candidate that decides your classification.
```

The German is withheld deliberately. Under the localisation convention the German distractor is *not* the reference for the target distractor, so showing it invites the literalness check the project forbids. The question is monolingual entailment, which is closer to what instruction-tuned models are trained on than cross-lingual judgement.

**(2) Two controls per cell, run before the three real calls, decide whether the cell's A3 result is admissible at all.** The positive control feeds the correct option *itself* as the candidate; the only acceptable answer is `same_as_correct`. The negative control feeds the German distractor that Tier 1b's term registry marks as most obviously false (for `parken-01`, option d "Halten ist nur nachts erlaubt", translated — in this case, the target's own option d); the only acceptable answer is `clearly_wrong`. A model that fails either control on a cell is recorded as `ABSTAIN_CONTROL_FAILED` for that cell and its three real answers are discarded. The measurement in §2.3 predicts that a 3B model will fail the negative control on most cells; if so, A3 is *provably* disabled at 3B by its own controls, per cell, rather than by a global judgement, and the receipts say so.

**(3) The finding requires the quote to be a substring and requires agreement with a second phrasing.** Each real call is issued twice with the candidate-first and correct-first orderings swapped in the prompt. A `same_as_correct` or `also_true` that appears in only one ordering is position bias, not a finding. This doubles A3's cost (six real calls per cell) and is the price of making "the model always names something" detectable: position bias is invisible in a single call and glaring across a swap.

**(4) Per-locale gate with a stricter bar than A1.** A1's gate is FP ≤ 10 % and recall ≥ 70 %. A3's gate is FP ≤ 5 % on the known-good half *and* control pass-rate ≥ 90 %, because the base rate of genuinely broken distractors is low and a 10 % FP rate on ~2,100 cells per locale (531 × 4 options minus correct) would open ~200 review items for at most a handful of real defects. Below that bar the pass runs, records, and is excluded from the verdict.

The honest expectation, stated as such: **A3 may remain unusable below roughly the 7–14B class and may remain unusable for `hi`, `ar`, `uk`, `fa` and `bar` at any locally hostable size**, because the target-only design makes the pass entirely dependent on the model's monolingual competence in the target, and that is exactly where small open models are weakest. The design does not pretend otherwise; it makes the per-locale outcome a committed calibration artefact (§5) so that a locale with A3 disabled is a recorded fact rather than an invisible gap. The way to verify is `seed_eval.py` extended with an `--pass a3` mode; the seed set already contains the `synthetic_swapped_correct_option` class (12 cells), which is the class A3 exists to catch, and the "presumed good" half is the FP denominator.

### 4.5 Legal false friends: the term-pair registry (Tier 1b + an extraction call)

The brief's example is a real cell. `parken-01` turns on the §12 StVO distinction: parking is holding for more than three minutes or leaving the vehicle. The fifteen live locales render the pair as follows (from the master file): `en` stopping/parking with the German in parentheses; `uk` зупинка/стоянка; `ar` التوقف المؤقت/الوقوف; `zh` 停车/停放; `bar` Halten/Parken. The Chinese pair is one character apart and 停车 colloquially covers both meanings, which is exactly the compression the brief describes and exactly the case a fluency judge waves through.

The design is deterministic first, model second:

- A committed **term-pair registry** per module, `data/term_pairs/<module>.json`, lists rigid legal pairs and, per locale, the *distinct* renderings the project has chosen: `{"pair": ["Halten", "Parken"], "legal_basis": "§12 StVO", "zh": ["停车", "停放"], "uk": ["зупинка", "стоянка"], ...}`. Candidate pairs for `fuehrerschein` that are already visible in the data: Halten/Parken, Vorfahrt/Vorrang, Fahrbahn/Straße, Gehweg/Radweg, Fahrerlaubnis/Führerschein, Vorschriftzeichen/Richtzeichen/Gefahrzeichen, Sperrfrist/Fahrverbot, Fahruntüchtigkeit (absolute/relative). The registry is authored by a reviewer, not by a model; it is small (tens of entries) and it is the single most valuable artefact this ADR asks a human to produce.
- **Tier 1b check, no model:** for every cell whose German contains both members of a pair, the target must contain both registered renderings, and they must be distinct strings. `parken-01/zh` passes because 停车 and 停放 are both present. A locale that renders both as 停车 fails with `TERM_PAIR_COLLAPSED`, evidence being the two German terms and the single target term. This is a substring check and runs in CI.
- **Extraction call (Tier 3, cheap):** for cells where the registry has no rendering for that locale yet, the model is asked to *extract* — "list the word or phrase this text uses for `Halten` and the word or phrase it uses for `Parken`" — with a two-string schema. The reply is not a judgement; it is a proposed registry entry, written to a `term_pairs/proposed/` file for a reviewer to accept. Extraction is a task small models do well, and it converts a judgement problem into a lookup problem for every later run.

The false-friend problem therefore never reaches A1 as a free-form question. A1 sees the term pair only indirectly, through `correct_option_equivalent` on `parken-01`'s option c, where a collapsed term would make the option read as "parking is when you park for more than three minutes" — tautological rather than wrong, and a case the model might well pass. The registry catches it upstream.

### 4.6 Numerals, units and script hygiene (Tier 1b, no model)

`zeichen-04`'s 133-versus-136 is a Tier 0 catch today only because the German was edited; a translation engine that hallucinates a sign number on a fresh translation would not be stale and would reach the model. A deterministic numeral diff is cheaper and more precise than asking `numbers_preserved`:

- Extract from both sides every token matching sign numbers (`\b\d{3}(?:[.-]\d{1,2})?\b`, covering `136`, `330.1`, `1010-53`), paragraph references (`§\s?\d+`, `Art\.\s?\d+`, `Abs\.\s?\d+`), quantities with units (`\d+(?:[.,]\d+)?\s?(km/h|m|km|Meter|Minuten|Sekunden|Promille|‰|%|kg|t|Jahre|Monate)`), and bare numbers. Normalise: decimal comma to point; Arabic-Indic (`٠١٢`), Eastern Arabic-Indic (Persian `۰۱۲`), Devanagari (`०१२`) and fullwidth digits to ASCII; `‰` and `Promille` and `промилле`/`промілі` to one canonical unit; `公里/小时` and `км/год` and `км/ч` and `كم/س` to `km/h`. Small-number words are mapped per locale for one to twelve (`drei` → 3, `三` → 3, `три` → 3, `ثلاث` → 3) because `drei Minuten` in `parken-01` is written out on every side.
- The multiset of `(value, unit_class)` on the German side must be a subset of the target's. A German quantity absent from the target is `NUMERAL_MISSING` (`CRITICAL_LOGIC` when it appears in the stem or a correct option; `MINOR_PHRASING` in the explanation). A target quantity with no German counterpart is `NUMERAL_ADDED` at `MAJOR_LOGIC`, because a translator inventing "30 km/h" where the German has none is a real pattern.
- Script hygiene: for every locale with a non-Latin primary script, every whitespace-delimited word is checked for mixed Unicode script blocks. A word mixing Cyrillic and Latin (`uk`, `ru`), Arabic and Latin inside a single word (`ar`, `fa`, `apc`), or Devanagari and Latin (`hi`) is `HOMOGLYPH_MIX` at `STRUCTURAL` severity — unless the whole word is in the German-term allowlist (`Fußgänger`, `Zeichen`, `StVO`, sign ids), which is derived from the registry and from the German source text itself. This is the rule that would have caught the Ukrainian homoglyphs on first commit.

None of this is novel; its place in the ADR is to state that these checks run *before* the model and that A1's `numbers_preserved` is a fallback for word-form numerals, not the primary signal.

### 4.7 Multi-choice cells

The five `mehrfach-*` questions are scored all-or-nothing on two or three correct letters. A1 runs per correct option (each `correct_option_equivalent` is evaluated separately and the receipt records the per-letter result); A2 extracts a skeleton per correct option; A3 uses *all* correct options as the "correct answer" block, since a distractor paraphrasing any one of them is a defect. The derive step is unchanged: any hard boolean false on any correct letter is a fail, because in an all-or-nothing question a single broken correct option breaks the whole item.

---

## 5. Calibration records and the per-locale gate

Every model signal (`a1.*`, `a2.*`, `a3`, `b2`, `b3`, `b4`) is enabled per locale by a committed file:

```
data/translation_state/calibration/<locale>.json
{
  "locale": "es",
  "seed_set_sha256": "…",             // hash of seed/known_good.json + known_bad.json at run time
  "runs": [{
    "at": "2026-09-05T…Z",
    "model": "qwen2.5:7b-instruct", "model_digest": "sha256:…", "ollama_version": "0.33.3",
    "prompt_template_sha256": {"judge_v2.md": "…", "skeleton_v1.md": "…", "distractor_pair_v1.md": "…"},
    "signals": {
      "a1.stem_equivalent":   {"n_good": 73, "n_bad": 73, "fp": 0.08, "recall": 0.74, "decision": "enabled"},
      "a3":                   {"n_good": 73, "n_bad": 12, "fp": 0.31, "recall": 0.92,
                               "control_pass_rate": 0.41, "decision": "disabled"},
      …
    }
  }],
  "enabled": ["a1.stem_equivalent", "a1.correct_option_equivalent", "a1.polarity_preserved", "a2.deontic", …]
}
```

The numbers in that example are illustrative placeholders, not measurements; the file is written by `seed_eval.py` and never by hand. Decisions follow the gate table already in the README for A1 (FP ≤ 10 % and recall ≥ 70 % → enabled; FP ≤ 20 % → advisory; else disabled), the stricter A3 bar in §4.4, and the acoustic gates in §6.5. A receipt produced under one calibration record carries that record's hash, so a later re-calibration that disables a signal does not silently rewrite history — `verify_receipts.py` reports the receipt as `produced under superseded calibration` and the sweep is re-run.

This is what makes the "may remain unusable" clause in §4.4 a first-class outcome. A locale whose calibration file lists `a3` as `disabled` is not a hole in coverage; it is a documented, hash-pinned statement that the project measured the signal and declined to trust it, and CI can verify that no receipt for that locale used it.

---

## 6. Component B — Acoustic-Linguistic TTS Judge

### 6.1 What the audio audit is actually for

The audio is generated *from the text that Tier 3 has just judged*, by a deterministic synthesiser, from a known phoneme sequence, under a known splice plan. Almost none of the information a human listener would extract from fifteen minutes of audio is unknown to the system that produced it. The only genuinely unknown quantities are: (i) did the synthesiser render the text it was given, completely and in order; (ii) did text normalisation verbalise units and numbers the way a native speaker of the target reads them; (iii) did the splice introduce a gap, click, clipped edge or mis-ordered segment; (iv) is the pacing within the band a learner can follow; and (v) did a pause land where it changes meaning. Every one of these has a cheaper and more precise answer than "transcribe it and see".

### 6.2 The synthesis manifest is the primary input

Component B is designed against a manifest that the TTS build must emit alongside each Opus/AAC file, and this ADR makes that manifest a requirement on `ADR-tts-accessibility.md`'s pipeline. Per utterance:

```json
{
  "cell": {"module": "fuehrerschein", "id": "parken-01", "locale": "ar", "field": "options.c"},
  "text_sha256": "…",                 // hash of the exact string handed to the synthesiser
  "target_hash": "…",                 // cells.target_hash, so audio receipts tie to text receipts
  "segments": [
    {"i": 0, "voice": "ar_JO-kareem-medium", "text": "يُعتبر وقوفًا إذا بقيت متوقفًا لأكثر من ", "t0_ms": 0,    "t1_ms": 2140,
     "phonemes": "…", "verbalised": "… أكثر من ثلاث دقائق …"},
    {"i": 1, "voice": "de_DE-thorsten-medium", "text": "Halten", "t0_ms": 2140, "t1_ms": 2610, "splice": "xfade_20ms"},
    …
  ],
  "audio": {"opus_sha256": "…", "aac_sha256": "…", "duration_ms": 6420, "sample_rate": 22050}
}
```

`verbalised` is the string after the synthesiser's text normalisation — the expansion of `30 km/h` into `dreißig Kilometer pro Stunde` or `ثلاثون كيلومتراً في الساعة` — and `phonemes` is what the phonemizer produced. Piper exposes the phoneme sequence through its espeak-ng front end (verify against the installed Piper version; if the build wrapper cannot capture it, the phoneme field is optional and B2 loses some precision but not its function). With this manifest, the "mixed-voice splice" problem of §2.5 disappears by construction: a voice change at a segment boundary listed in the manifest is expected, and only a discontinuity *not* at a manifest boundary is an artifact.

### 6.3 B1 — deterministic signal analysis over the manifest (no model)

Runs on every utterance of every locale; cheap enough for the full 3,186-utterance module in minutes (estimate; this is single-pass PCM analysis after decoding).

- **Duration sanity.** Expected duration is predicted from character count per locale with a per-voice rate fitted on the known-good seed utterances (a linear fit of `duration_ms` on grapheme or phoneme count; the residual band is the calibration). An utterance more than three residual standard deviations short is `AUDIO_TRUNCATED` (`ACOUSTIC_MEANING`, because a dropped clause is a meaning change); more than three long is `AUDIO_PACING` (`ACOUSTIC_ARTIFACT`).
- **Silence and gap analysis.** RMS below −50 dBFS (threshold to be tuned per voice; a starting value, not a measurement) for longer than 400 ms inside a segment is `AUDIO_INTERNAL_GAP`; at a manifest splice boundary, the tolerance is the crossfade length plus 120 ms, above which it is `AUDIO_SPLICE_GAP`. Leading or trailing silence beyond 300 ms is `AUDIO_PADDING` at `MINOR` severity.
- **Splice integrity.** At each manifest boundary the first-difference of the PCM is examined over ±5 ms; a step exceeding a per-voice threshold is `AUDIO_SPLICE_CLICK`. Clipping (three or more consecutive full-scale samples) anywhere is `AUDIO_CLIPPING`. Loudness mismatch between the German-voice segments and the target-voice segments greater than 4 LU (starting threshold) is `AUDIO_LEVEL_MISMATCH` — the two Piper voices are not level-matched by default and a learner hears the German term as shouted or whispered.
- **Container check.** The Ogg Opus and the AAC files must decode to durations within 50 ms of each other and of the manifest's `duration_ms`. A Safari-only playback failure would present as a container problem, not an acoustic one, and this catches an Opus accidentally muxed into WebM.

B1 has no false-positive problem in the model sense — its thresholds are tunable and its findings are mechanically checkable — and it is the only part of Component B that runs on every utterance unconditionally.

### 6.4 B2 — forced alignment against known text

The question "did the synthesiser render the text it was given, in order, with no dropped or repeated words" is not a speech-recognition problem. It is a forced-alignment problem: the text is known, and the task is to find where each word starts and ends. CTC-based forced alignment with a multilingual acoustic model (the MMS-family forced aligner supports on the order of a thousand languages via a shared romanised phone set; verify the exact language coverage and licence of whichever aligner is installed before relying on it for `bar` or `apc`) produces per-word timestamps and a per-word alignment confidence. This is decisively more robust than free ASR on a low-resource variety, because the aligner is not asked to *guess* words, only to *place* them, and a mis-placed word manifests as low alignment confidence rather than as a plausible wrong transcript.

B2 emits:

- `AUDIO_WORD_DROPPED` / `AUDIO_WORD_REPEATED` when the alignment confidence for a word (or a run of words) falls below the per-locale floor set from the seed utterances. Severity is `ACOUSTIC_MEANING` if the word is in the A2 skeleton's `deontic`, `exceptions` or `quantities` sets for that field (a dropped `nicht`, `nur`, `außer`, `三分钟`), `ACOUSTIC_ARTIFACT` otherwise. This is the link the brief asks for between pauses and legal meaning: the acoustic layer knows which words are load-bearing because the semantic layer told it.
- `AUDIO_BOUNDARY_PAUSE` when the inter-word gap exceeds a per-locale threshold *at a position that A2 marks as inside a condition or exception clause*. A pause of 600 ms between "Nein," and "auf engen Brücken ist das Parken verboten" (`parken-27`) is a rhetorical pause; the same pause between "darf" and "nicht" changes what a listener hears. The threshold is applied only inside skeleton spans, which is what keeps the finding rate low.
- `AUDIO_GERMAN_TERM_MISALIGNED` when a German-voice segment (from the manifest) aligns poorly against the German-phoneme reference. This is the round-trip check for German terms embedded in RTL or non-Latin text: the stored string is in logical order and Piper's sentence splitter, the bidi algorithm and the splice plan all have to agree on where `«Fußgänger»` sits; if the German voice rendered the term but the aligner finds it at the wrong offset relative to the surrounding Arabic, the segment order was scrambled by bidi reordering before synthesis. The manifest's `t0_ms`/`t1_ms` for the German segment versus the aligner's placement of the surrounding target words is the evidence.

B2's gate is per locale and is measured the same way as A1: alignment confidence distributions on the known-good seed utterances give the floor, and a synthetic bad set (utterances re-synthesised from text with one load-bearing word deleted) gives the recall. For `bar` and `apc`, the honest expectation is that the aligner treats them as German and Levantine-adjacent Arabic respectively and that its confidence floor is lower and noisier; whether it is *usable* is what the calibration run decides, and it is a much better bet than free ASR for the reasons above.

### 6.5 Multimodal audio judging versus an ASR loop — the comparison

The brief asks for an honest comparison. Both are evaluated against the criterion that governs the whole engine: **does the auditor have better error characteristics than the thing it audits, per locale, and can its output be receipted?**

**Asynchronous ASR loop (Whisper-class).** Transcribe the utterance, diff against the `verbalised` manifest text, flag differences.

- *Strengths.* Mature tooling, runs locally on the development Mac, deterministic enough at greedy decoding to receipt (model digest + audio hash + transcript hash). Good on `de en es fr it pl ru uk tr zh ar` in their standard varieties. Excellent at catching a *wrong* verbalisation of a unit, because the transcript literally contains what was said ("thirty kilometres per hour" versus "thirty k-m-h").
- *Weaknesses that matter here.* (i) On a low-resource variety the ASR error rate is unknown and likely worse than Piper's rendering error rate; Whisper has no Bavarian model and will transcribe `bar` audio as Standard German with heavy substitutions, so the diff against the Bavarian `verbalised` text is dominated by the *ASR's* normalisation, not the TTS's. Palestinian Arabic (`apc`) audio will be transcribed into MSA orthography with the same effect. (ii) ASR language-ID on a mixed-voice clip flips between German and the target at the splice, producing transcripts that are wrong in a way that looks like a TTS defect. (iii) ASR normalises numbers back to digits non-deterministically ("thirty" → "30"), so a diff against `verbalised` needs its own normaliser and the whole exercise turns into comparing two normalisers. (iv) Transcript diffs have no notion of which words are load-bearing.
- *Verdict.* Use it, but only as **B3, a spot-check confined to unit and number segments**, on locales where the calibration run shows its WER on known-good utterances is below a bar (starting proposal: ≤ 8 % word error on the seed utterances; a number to be replaced by measurement), and never on the whole track. The unit segments are short (a second or two), the vocabulary is closed (the per-locale verbalisation table of §6.6), and the failure mode that matters — the synthesiser said the unit wrong — is exactly what a transcript shows. For `bar`, `apc`, `fa`, `hi` the calibration will very probably disable B3; that is a recorded outcome, not a gap.

**Direct multimodal audio-to-text judging (an audio-capable LLM given the clip and the text, asked to judge).**

- *Strengths.* One pass, no transcript normalisation problem, can in principle judge prosody and naturalness, can be asked the load-bearing-word question directly.
- *Weaknesses that matter here.* (i) Capability in the low-resource locales is unmeasured and there is no reason to expect a general audio model to be better at Bavarian than a speech-specific one. (ii) A 15-minute track is far outside the audio context of any locally hostable model this ADR is aware of (an estimate, not a measurement: verify against the model card of whatever is installed), so the track is chunked by utterance anyway, at which point the "one pass" advantage is gone. (iii) The judgement is a free-form model opinion of precisely the kind the whole engine is designed to keep out of the verdict: a "this sounds unnatural" without a timestamp and a mechanical check behind it is not actionable and cannot be receipted beyond "the model said so". (iv) Local hosting: at the time of writing this ADR cannot confirm that an audio-input model is served through the Ollama API that `ollama_client.py` speaks; if it is not, the receipt provenance chain (`model_digest`, `options_sha256`) breaks and a new client with equivalent provenance would be required before any result counts. This must be verified, not assumed. (v) The same "always names something" behaviour measured in §2.3 should be expected of an audio judge asked "is anything wrong with this clip", and there is not yet a seed set of known-bad audio to measure it against.
- *Verdict.* **B4, sampled and advisory only**, run on a small random sample of utterances per batch plus every utterance that B1/B2 flagged, with a forced enum schema (`{"defect": ["none", "truncated", "wrong_word", "mispronounced_unit", "unnatural_pause", "voice_glitch"], "at_ms": int, "quote": string}`) and the substring rule applied to `quote` against the `verbalised` text. Its findings never enter the derived verdict until a known-bad audio seed set exists and the signal has beaten a gate. Its main *practical* value in the near term is triage ordering for a human listener, which is a Tier 2 role, not a Tier 3 one.

**Decision.** The acoustic auditor is **manifest + DSP (B1) and forced alignment (B2) as the primary signals, ASR confined to unit segments and gated per locale (B3), multimodal judging sampled and advisory (B4).** Neither of the brief's two candidates is the backbone, because neither has better error characteristics than Piper on the locales where Piper is most likely to be wrong; the backbone is the fact that the system already knows what the audio is supposed to contain.

### 6.6 Units, per mille and the verbalisation table

Mispronounced units are almost never an acoustic defect. They are a text-normalisation defect: the synthesiser was handed `0,5 Promille` or `30 km/h` and its front end expanded it (or failed to and spelled letters). The check therefore belongs *upstream of the audio*, on the manifest's `verbalised` field:

- A committed **verbalisation table** per locale, `data/tts/verbalisation/<locale>.json`, maps each unit and numeral pattern that Tier 1b extracts (§4.6) to its expected spoken form: `km/h` → `Kilometer pro Stunde` / `kilómetros por hora` / `кілометрів на годину` / `公里每小时` / `كيلومتر في الساعة`; `Promille` and `‰` → `Promille` / `por mil` / `проміле` / `千分之…` / `في الألف`; decimal comma handling (`0,5` → `null Komma fünf` versus `cero coma cinco` versus `零点五`); sign ids (`1010-53` → digits read individually with the hyphen as a pause, *not* "one thousand and ten minus fifty-three"); paragraph signs (`§12 Abs. 2` → `Paragraph zwölf Absatz zwei`). The table is small, authored by a reviewer, and every entry is a string the deterministic check can look for in `verbalised`.
- `UNIT_VERBALISATION_MISSING` fires when Tier 1b found a unit in the text and the manifest's `verbalised` string contains neither the table's expected spoken form nor the raw token (the raw token surviving means the front end will spell it letter by letter, which is `UNIT_VERBALISATION_RAW`). Both are `ACOUSTIC_MEANING` when the unit sits in the stem or a correct option: a learner who hears "thirty k-m-h" learns nothing wrong, but one who hears "zero point five percent" for `0,5 Promille` learns a number ten times too large.
- B3 then confirms, on the audio, that the expected spoken form was actually produced, for the locales where ASR is gated on. Where it is gated off, the verbalisation check stands alone, which is an acceptable position: the front end's expansion is deterministic, so a correct `verbalised` string and a rendered segment of plausible duration (B1) is strong evidence without a transcript.

The per-mille case deserves the explicit note that `‰` is the highest-risk glyph in the corpus: several front ends have no entry for it, some read it as `%`, and Chinese `千分之零点五` inverts the reading order relative to the digits. The corpus contains it in at least five `fahrtuechtigkeit-*` cells, three of which encode legal thresholds (`0,5`, `1,1`).

### 6.7 Budget

For a batch of ~20 cells × 6 utterances × one locale: B1 is sub-minute; B2 is on the order of real-time or faster on CPU for a CTC aligner (estimate; measure on the Mac); B3 runs on perhaps 20–40 short unit segments; B4 on 10 sampled plus flagged utterances. The full-module sweep (3,186 utterances) is an overnight job per locale for B2, which matches the Tier 3 sweep cadence. Audio receipts are one line per utterance and, at 3,186 lines per module-locale, need their own file: `data/translation_state/audio_verdicts/<module>.<locale>.jsonl`, keyed by `(id, field, target_hash, opus_sha256)`.

---

## 7. Component C — Production Output Schema

### 7.1 Design constraints inherited from the receipt store

`receipts.py` already defines the contract: append-only JSONL per module, `REQUIRED_FIELDS = (module, id, locale, source_hash, target_hash, model, model_digest, prompt_sha256, verdict, at)`, later lines win, `verify_receipts.py` compares `source_hash`/`target_hash` against today's data and needs no model. The v2 schema **adds fields and never removes or renames one**, so every existing receipt line stays valid and `verify_receipts.py` keeps working unchanged on v1 lines. A `schema: 2` field distinguishes the two; its absence means v1.

### 7.2 The receipt record (schema 2)

```json
{
  "schema": 2,
  "module": "fuehrerschein", "id": "parken-01", "locale": "zh",
  "source_hash": "…", "target_hash": "…",
  "at": "2026-09-05T22:14:03Z", "engine_version": "tve-0.6.0",
  "calibration_sha256": "…",
  "batch": {"batch_id": "2026-09-05-zh-parken-01..parken-30", "page_range": "1-4", "audio_ids": ["…"]},

  "model": "qwen2.5:7b-instruct", "model_digest": "sha256:…", "ollama_version": "0.33.3",
  "prompt_sha256": "…",
  "prompts": {
    "judge_v2.md": "…sha256…", "skeleton_v1.md": "…sha256…", "distractor_pair_v1.md": "…sha256…"
  },
  "options_sha256": "…",
  "calls": [
    {"pass": "a1", "prompt_sha256": "…", "prompt_eval_count": 1187, "eval_count": 92, "elapsed_ms": 6120},
    {"pass": "a2", "side": "de", "field": "options.c", "prompt_sha256": "…", "cached": true},
    {"pass": "a2", "side": "zh", "field": "options.c", "prompt_sha256": "…", "elapsed_ms": 2870},
    {"pass": "a3", "candidate": "positive_control", "order": "cf", "result": "same_as_correct"},
    {"pass": "a3", "candidate": "negative_control", "order": "cf", "result": "clearly_wrong"},
    {"pass": "a3", "candidate": "a", "order": "cf", "result": "clearly_wrong"},
    {"pass": "a3", "candidate": "a", "order": "fc", "result": "clearly_wrong"}
  ],

  "verdict": "fail",
  "reasons": ["a1.correct_option_equivalent", "tier1b.TERM_PAIR_COLLAPSED"],
  "model_self_verdict": "pass",
  "confidence": 0.81,

  "findings": [
    {
      "signal": "tier1b.term_pair",
      "code": "TERM_PAIR_COLLAPSED",
      "severity": "CRITICAL_LOGIC",
      "gated": false,
      "field": "options.c",
      "evidence": {
        "source_quote": "länger als drei Minuten hält",
        "target_quote": "停车时间超过三分钟",
        "source_span": [22, 51], "target_span": [0, 9],
        "detail": {"pair": ["Halten", "Parken"], "registry_zh": ["停车", "停放"], "found_zh": ["停车"]}
      },
      "repair": {
        "action": "retranslate_field",
        "constraints": [
          {"kind": "pin_term", "source": "Halten", "target": "停车"},
          {"kind": "pin_term", "source": "Parken", "target": "停放"},
          {"kind": "preserve_quantity", "value": "3", "unit": "min"}
        ]
      }
    },
    {
      "signal": "a3", "code": "DISTRACTOR_CHECK", "severity": "INFO", "gated": true,
      "field": "options.*",
      "evidence": {"detail": {"controls": "passed", "results": {"a": "clearly_wrong", "b": "clearly_wrong", "d": "clearly_wrong"}}},
      "note": "a3 is disabled for zh by calibration …; recorded, not counted"
    }
  ]
}
```

Field semantics that are load-bearing:

- **`verdict` and `reasons` are derived in Python** from `findings[]` by `derive_findings()`: the highest severity among non-gated findings whose signal is in the calibration's `enabled[]` list determines the verdict (`CRITICAL_LOGIC` or `STRUCTURAL` → `fail`; `MAJOR_LOGIC` or a soft boolean → `unsure`; `MINOR_PHRASING` or `INFO` only → `pass` with findings; any `ABSTAIN_*` or protocol error → `error`, never `pass`). The 2^n unit-test discipline of `derive_verdict()` carries over.
- **`gated`** marks a finding produced by a signal that is not enabled for this locale. It is stored so that the numbers keep accumulating and so that a later re-calibration can re-derive verdicts from stored findings without re-running the model. CI verifies that no non-gated finding's `signal` is absent from the calibration file whose hash the receipt names; a receipt that claims an ungated finding from a disabled signal is corrupt.
- **`evidence.source_span` / `target_span`** are character offsets into the *normalised* cell text as rendered by `render_cell_block()`, verified as substrings at write time. A finding whose quotes fail the substring test is written with `severity: "UNVERIFIED"` and cannot contribute to the verdict.
- **`repair`** is the actionable part for a self-correcting translation engine, and it is deliberately *not* prose. It is a small closed vocabulary of actions (`retranslate_field`, `regenerate_from_source` for stale cells, `fix_numeral`, `fix_script`, `re_render_utterance`, `re_verbalise_unit`, `review_only`) with typed constraints (`pin_term`, `preserve_quantity`, `preserve_deontic`, `preserve_exception_count`, `forbid_paraphrase_of` with an option letter). A translation prompt builder can turn `constraints[]` into a system-prompt block mechanically; a human reviewer can read it; and because the vocabulary is closed, the next engine run can verify that the constraint was honoured (the pinned term is present, the quantity survived) *without a model*, which is how the loop converges instead of oscillating.

### 7.3 Severity taxonomy

| Severity | Meaning | Verdict effect | Examples |
|---|---|---|---|
| `STALE` | Tier 0: German changed since translation | `fail` (regenerate, do not review) | `zeichen-68` class |
| `STRUCTURAL` | Tier 1/1b: mechanical defect | `fail` | missing option key, `HOMOGLYPH_MIX`, leaked token |
| `CRITICAL_LOGIC` | The answer key is wrong for this locale, or a rule is inverted | `fail` | `deontic` mismatch, `NUMERAL_MISSING` in correct option, `TERM_PAIR_COLLAPSED`, `stem_equivalent=false` |
| `MAJOR_LOGIC` | Meaning likely changed; needs a reader | `unsure` | condition-count mismatch, `NUMERAL_ADDED`, `explanation_facts_preserved=false` |
| `MINOR_PHRASING` | Meaning intact; wording or explanation drift | `pass` with findings | explanation numeral in a different form, padding |
| `ACOUSTIC_MEANING` | Audio does not say what the text says, at a load-bearing word | `fail` (audio only; text verdict unaffected) | dropped `nicht`, `UNIT_VERBALISATION_MISSING` on a threshold, `AUDIO_TRUNCATED` |
| `ACOUSTIC_ARTIFACT` | Audio says the right thing badly | `unsure` (audio) | splice click, level mismatch, pacing outlier, unlisted voice change |
| `INFO` | Recorded, no effect | none | gated signals, control results, cached extractions |
| `UNVERIFIED` | A model claim whose quote failed the substring test | none (counted in calibration as a protocol failure) | |

Text and audio verdicts are separate fields on separate receipt files; a cell whose text passes and whose audio fails must not be re-translated, only re-rendered, and conflating the two would send the wrong `repair.action`.

### 7.4 Audio receipt record

`data/translation_state/audio_verdicts/<module>.<locale>.jsonl`, one line per utterance:

```json
{
  "schema": 2, "module": "fuehrerschein", "id": "fahrtuechtigkeit-18", "locale": "uk", "field": "options.c",
  "target_hash": "…", "text_sha256": "…", "manifest_sha256": "…",
  "audio": {"opus_sha256": "…", "aac_sha256": "…", "duration_ms": 5310},
  "at": "…", "engine_version": "tve-0.6.0", "calibration_sha256": "…",
  "tools": {
    "b1": {"impl": "tve.dsp", "version": "0.6.0"},
    "b2": {"aligner": "…", "model_digest": "…"},
    "b3": {"asr": "whisper-…", "model_digest": "…", "decoding": "greedy"},
    "b4": null
  },
  "verdict": "fail", "reasons": ["b3.UNIT_VERBALISATION_MISSING"],
  "findings": [{
    "signal": "tier1b.verbalisation", "code": "UNIT_VERBALISATION_RAW", "severity": "ACOUSTIC_MEANING", "gated": false,
    "at_ms": [3120, 3690],
    "evidence": {"text_token": "0,5 ‰", "verbalised": "… 0,5 ‰ …", "expected": "нуль цілих п'ять проміле"},
    "repair": {"action": "re_verbalise_unit", "constraints": [{"kind": "spoken_form", "token": "‰", "form": "проміле"}]}
  }]
}
```

`verify_receipts.py` gains an `--audio` mode that checks, without any model: `target_hash` matches today's translation, `opus_sha256` matches the shipped file, `manifest_sha256` matches the shipped manifest, `calibration_sha256` names a committed calibration file, and no non-gated finding uses a signal that file disables. A re-translation invalidates the audio receipt (the `target_hash` moves), and a re-render invalidates it (the audio hash moves), which is the same rule the text receipts already follow.

### 7.5 Telemetry for the self-correction loop

The translation engine consumes receipts through a small derived view rather than the raw JSONL: `scripts/i18n_qa/repair_queue.py` (proposed) folds the latest receipt per cell into `tmp/repair_queue.<locale>.json`, grouped by `repair.action`, with the constraints merged per cell, and with three counters per locale that are the loop's health metrics: **re-open rate** (cells that failed again after a repair that claimed to honour the constraints — the metric that says the translator is not reading the constraints), **constraint-violation rate** (repairs where the deterministic post-check found the pinned term absent — the metric that says the constraint vocabulary is not being turned into prompt text correctly), and **gated-finding volume** (findings recorded but not counted — the metric that says how much the project is *not* seeing because signals are disabled, and therefore how much a stronger model would buy). None of these needs a model to compute.

---

## 8. Consequences

**Positive.** The engine's precision is bounded below by Tiers 0/1/1b, which have no model and zero measured false positives; everything above them can only add recall. The one measured-worthless signal is removed from the verdict path rather than re-specified, and its replacement is designed so that its own controls disable it per cell when the model is not up to it. Every model claim is quote-verified, hash-pinned and calibration-gated, and CI verifies all of that with no GPU and no model host. The acoustic audit does not depend on ASR in the locales where ASR is least trustworthy. Findings carry a closed-vocabulary repair instruction, so the translation loop can converge mechanically.

**Negative and honest.** Per-cell model cost rises from one call to roughly eight (estimate), which confines Tier 3 to sweeps rather than pre-commit. A3 will very probably be disabled for several locales at any locally hostable model size, and the project will know that but will not have a distractor check there; the alternative — a signal that fires on everything — is worse. The term-pair registry and the verbalisation table require human authoring per locale before the corresponding checks are meaningful, and until they exist those checks degrade to "no rendering registered", which is a recorded gap. B4's provenance chain is unverified until an audio-capable model is confirmed reachable through a client that records digests. The TTS build must be changed to emit the manifest; without it, B1 loses splice awareness and would produce the false artifacts the mixed-voice design otherwise invites.

**Verification path, in order.** (1) Extend `seed_eval.py` with `--pass a1|a2|a3` and run all three on the 146-cell seed set with `qwen2.5:7b-instruct` and one 12–14B candidate; write the first `calibration/<locale>.json` files from the results. (2) Author `term_pairs/fuehrerschein.json` for the eight pairs named in §4.5 and the fifteen live locales; run Tier 1b in CI. (3) Add the manifest to the TTS build and run B1 over the existing Opus files for one locale. (4) Construct a known-bad audio seed set (re-synthesise 30 utterances with one load-bearing word deleted, 30 with a unit token left raw) and calibrate B2 and B3 per locale. (5) Only then decide on B4. Every number this document calls an estimate is replaced by a measurement at the step that produces it.
