# ADR-001: Automated translation-quality checks with local LLMs (Ollama)

- **Status:** Proposed
- **Date:** 2026-09-05
- **Deciders:** PO (Stefan); Developer persona for implementation
- **Numbering note:** this is the first ADR in the repo (`docs/adr/` did not exist before). Convention going forward: `ADR-NNN` sequential in the title, file name `ADR-<slug>.md`, sections Status / Date / Context / Decision Drivers / Considered Options / Decision / Consequences / Implementation Notes. Supersede by adding a new ADR and changing this one's Status, never by rewriting history.

## Context

Zettacard ships every question in 12 locales (`de, en, es, fr, it, pl, ru, uk, tr, ar, hi, zh`; the compliance modules additionally carry `ro`). German is canonical. The data shape the app loads is:

```
app/data/<module>/core.json               # {"meta": {...}, "questions": [{id, topic, correct: ["a"], high_stakes, points, image_ref, ...}]}
app/data/<module>/locales/<lang>.json     # {"<id>": {"question": "...", "options": {"a":..,"b":..,"c":..,"d":..}, "explanation": "..."}}
```

Real example, `app/data/fuehrerschein/core.json` entry and the matching `locales/de.json` entry:

```json
{"id": "zeichen-68", "topic": "Verkehrszeichen", "legal_basis": "§41 StVO, Anlage 2, Zeichen 214",
 "points": 2, "high_stakes": false, "question_type": "single_choice",
 "image_ref": "signs/214", "correct": ["a"], "class_scope": ["B"]}
```
```json
"zeichen-68": {
  "question": "Was schreibt dieses Verkehrszeichen vor?",
  "options": {
    "a": "Sie müssen hier geradeaus oder nach rechts weiterfahren.",
    "b": "Sie müssen hier nur nach rechts abbiegen.",
    "c": "Geradeausfahren ist hier verboten.",
    "d": "Sie dürfen hier in jede Richtung fahren."
  },
  "explanation": "Zeichen 214 ist ein Vorschriftzeichen für die vorgeschriebene Fahrtrichtung: ..."
}
```

These runtime files are **generated** by `data/build_modules.py` from the editable master files (`data/pilot_questions.json` for fuehrerschein, `data/<module>_pilot.json` for the others), where each question carries `text.<lang>.{question, options}` and `explanation.<lang>` side by side. Any QA tooling has to treat the master files as the source of truth (see AGENTS.md, "Repo layout") - more on why this matters in Implementation Notes §0.

Scale today (counted from `app/data/*/locales/de.json` on 2026-09-05): 2,258 questions across 25 module directories, ~16,400 non-German translation cells. The fuehrerschein module alone is 531 questions × 11 target locales = 5,841 cells, averaging ~475 characters of German per question (question + 4 options + explanation).

### The defects this ADR must catch

All of the following were found in shipped or about-to-ship content. None of them is detectable by schema validation: every one was well-formed JSON with the right ids, the right option keys, and non-empty strings.

1. **Staleness after a source revision.** German questions were revised in content-quality passes; English was re-translated, the other ten locales were not. As of this morning `zeichen-68` in `ar/es/fr/...` still described an *obstacle-passing* sign ("Debe pasar por la derecha", "يجب عليك المرور من جهة اليمين") while German describes Zeichen 214 (mandatory direction, "geradeaus oder nach rechts"). `zeichen-132` in `pl`/`ar` still describes a "Mofa frei" supplementary plate while German describes the "Fußgänger" supplementary sign 1010-53. `docs/fuehrerschein-translation-completeness-plan.md` had already flagged eight such ids (`vorfahrt-04, -05, -06, -09, -13, -17, -24, zeichen-06`) on 2026-08-06; more surfaced later. This is the most damaging class: the learner is shown a picture of one sign and taught the rule of a different one, in their own language, with an answer key that is *correct for the German* but meaningless for what they read.
2. **Meaning inversion.** A Hindi compliance question inverted a legal requirement ("must" ↔ "must not"). Single-token polarity flips are invisible to length, structure, and even most similarity checks.
3. **Wrong numbers.** A sign number rendered as 133 instead of 136 in several locales (`zeichen-04`; the 133/136 confusion also exists in project history for the icon itself, see BACKLOG DN-46). Numbers, § references, deadlines (72 h, one month) and sign ids are the load-bearing facts in this content.
4. **False friends**, recurring in Polish (e.g. cognates that look right and mean something else).
5. **Answer-key breakage.** `core.json` marks one letter correct for *all* locales. If a translation makes a distractor read as true, or weakens the correct option so it reads as false, the shared key is silently wrong for that locale only.
6. **Leaked authoring tokens.** The canonical German `datenschutz` file has nine explanations ending in "... - daher als high_stakes markiert." - an internal schema flag that leaked from the generation prompt into learner-facing text (`datenschutz-betroffenenrechte-01/-02/-08`, `-datensicherheit-03/-05`, `-meldepflichten-01/-03/-05/-08`). Because de is canonical, every translation of those explanations inherits the leak.

### Constraints inherited from the repo

- No build step for the app; tooling lives in `data/*.py` (Python, stdlib) and `scripts/*.mjs` (Node). Nothing may require a backend at runtime (this ADR is dev/CI-time only, so that is not affected).
- AGENTS.md rule 5: all 12 locales must be populated from the start. AGENTS.md workflow step 3: there is no reusable validation script yet - building one is explicitly flagged as "a legitimate improvement, flag it to the PO". This ADR is that flag.
- Translations were produced by parallel LLM agents (one per locale) and have never had a systematic accuracy pass except de/en.
- Distractor options are **deliberately not literal translations**. The localization convention is that a distractor must be plausibly wrong *for a reader of that language*, so translators were free to swap in a locally more plausible wrong answer. A check that demands literal equivalence of all four options will flag hundreds of correct entries.

## Decision Drivers

- D1. Catch defect classes 1-6 with a **low false-positive rate**; review fatigue kills a QA gate faster than misses do.
- D2. Deterministic, machine-checkable output that can fail a check in CI and be re-run to get the same answer.
- D3. Runs on a developer Mac (Apple Silicon) with no cloud dependency and no data leaving the machine (content is CC BY-NC-SA and not yet legally reviewed; keeping it local avoids a licensing/tooling discussion for now).
- D4. Cost proportional to change: a one-word German edit must not trigger a 16,000-cell sweep.
- D5. Auditable: every verdict must be traceable to a model, a prompt version, an input hash and a timestamp, and reviewable by a human who does not read the target language.
- D6. Honest about model limits: hi, ar, uk, tr and (to a lesser degree) pl are where open local models are weakest, and those are exactly the locales that have had no native review.

## Considered Options

### O1. Source-hash staleness ledger (deterministic, no model)

Store, per `(module, id, locale)`, the SHA-256 of the *German* question+options+explanation+correct-letters that the translation was last verified against. When German changes, the hash mismatches and the cell is flagged stale until a human or a re-translation re-stamps it.

- Would have caught **every instance of defect 1** (`zeichen-68`, `zeichen-132`, the eight ids from the August plan) with zero false positives and zero model cost.
- Catches nothing about translation *quality*: a bad translation of an unchanged source stays green forever.
- Requires a one-time bootstrap: stamping today's hashes asserts nothing about today's quality, only that later drift will be seen.

### O2. Deterministic content lint (no model)

Regex/structural checks per cell against the German cell: numbers and sign ids present in de (`\b\d{2,4}(-\d+)?\b`, `Zeichen \d+`, `§ ?\d+`, `Art\. ?\d+`, `72 Stunden`) must appear in the translation; forbidden tokens (`high_stakes`, `grundstoff`, `{{`, `TODO`, `[[`); target-script check (Devanagari for hi, Arabic script for ar, Cyrillic incl. `іїєґ` for uk); cell identical to de or en (untranslated); option-count and empty-string checks; length ratio outside a per-language band.

- Catches defect 3 (133/136) and defect 6 (`high_stakes`) exactly, plus whole-cell untranslated fallbacks.
- Cannot see meaning. Numbers that legitimately differ (e.g. "125 cm³" appearing only in a distractor) need an allow-list.

### O3. Multilingual embedding similarity

Embed the German stem+correct option and the target stem+correct option with a multilingual embedding model; flag cosine similarity below a per-language threshold.

- Cheap: an embedding model of ~0.3-0.6B parameters runs in well under a second per cell on Apple Silicon (estimate), so a full 16k-cell sweep is minutes, not hours.
- Catches **drift** (defect 1, when the hash ledger is not yet in place, or when someone re-stamps a hash without actually re-translating) because a sign-214 sentence and an obstacle-passing sentence are far apart.
- Does **not** catch inversion (defect 2): "must" vs "must not" sentences embed almost identically. Does not reliably catch a single wrong number (defect 3). Weak on false friends (defect 4).
- Thresholds must be calibrated per language; cross-lingual similarity for hi/ar is systematically lower than for es/fr even when the translation is perfect.

### O4. Back-translation via local LLM, then compare

Translate the target cell back to German (or English) with a local model, then compare the back-translation to the source with O3 or an LLM judge.

- Lets an English-strong judge assess a Hindi cell indirectly.
- Doubles the model cost and compounds two error sources: a weak Hindi→German step produces a garbled back-translation that gets flagged even when the Hindi is fine (false positive), or smooths over an error (false negative). The August plan proposed this; it is the weakest of the model-based options for hi/ar/uk precisely because that is where the back-translation step is least reliable.

### O5. Direct bilingual LLM-as-judge with an explicit rubric

Show a multilingual instruction model the German cell and the target cell side by side, plus the correct letter from `core.json`, and ask for a structured verdict against a fixed rubric.

- The only option that can catch inversion (2), false friends (4), and answer-key breakage (5) in one pass.
- Requires a model that actually reads the target language. A model that only "sort of" knows Hindi will produce confident, wrong verdicts - both directions.
- Expensive: each call is ~800-1,500 input tokens (bilingual cell + rubric) and ~100-200 output tokens. On an 8B-class model at Q4 on an M-series Mac, that is on the order of 5-15 s per cell (rough estimate, depends heavily on chip and memory bandwidth). A full fuehrerschein sweep (5,841 cells) is therefore on the order of 8-25 hours on one machine; all modules (~16k cells) 1-3 days. A 27-32B model is roughly 3× slower and needs a 32 GB+ Mac. These are order-of-magnitude estimates, not measurements - measure before scheduling anything.

### O6. Hosted API judge (Claude/GPT-class)

Not local, contradicts D3; noted only because it is the honest fallback for hi/ar/uk if local judge quality proves inadequate (see Consequences). Not chosen now.

### Model landscape for O3-O5 (as far as known on 2026-09-05; verify with `ollama pull` before relying on any of this)

Everything below runs via Ollama on Apple Silicon using unified memory; sizes are rough Q4_K_M download sizes and resident memory, not benchmarks.

| Role | Candidate | Approx. size | Notes and caveats |
|---|---|---|---|
| Embedding | `bge-m3` (BAAI) | ~0.57B params, ~1.2 GB | Explicitly multilingual (100+ languages claimed, incl. hi/ar/uk/pl/tr/zh). Published on the Ollama library. First choice for O3. |
| Embedding | `paraphrase-multilingual` (sentence-transformers MiniLM) | ~0.28B, ~0.5 GB | Smaller/faster, ~50 languages, weaker on hi/ar. Fallback. |
| Embedding | multilingual-e5-large | ~0.56B | Strong in published cross-lingual benchmarks; availability on the Ollama library is via community uploads, so treat as "check first". |
| Judge, small | `qwen2.5:7b-instruct` / `qwen3:8b` | ~4.5-5 GB | Qwen 2.5 lists ~29 supported languages incl. de/es/fr/it/pl/ru/tr/ar/zh (Hindi and Ukrainian are *not* in its officially listed set as far as I know - do not assume). Qwen 3 claims 119 languages; the claim is broad and quality on hi/uk should be tested, not assumed. Good structured-JSON compliance. |
| Judge, small | `aya-expanse:8b` (Cohere) | ~5 GB | Officially targets 23 languages, and as far as I can tell that list covers **all 13 locales this repo uses** (de, en, es, fr, it, pl, ro, ru, uk, tr, ar, hi, zh). Weights are CC-BY-NC, acceptable for an internal QA tool. Likely the best small option for hi/ar/uk; worse at strict JSON than Qwen in my experience - use Ollama's schema-constrained output. |
| Judge, small | `llama3.1:8b` | ~4.9 GB | Officially supports only en/de/fr/it/pt/hi/es/th - **no ar, pl, ru, uk, tr, zh**. Only useful as a second opinion for hi. |
| Judge, small | `mistral-nemo:12b` | ~7 GB | Multilingual incl. ar/hi/zh/ru; mid-tier. |
| Judge, mid | `gemma3:12b` / `gemma3:27b`, `qwen2.5:14b`/`:32b`, `qwen3:30b-a3b` | 8-20 GB | Gemma 3 claims 140 languages; the 27B model needs ~18-20 GB resident, i.e. a 32 GB Mac with little else running. Qwen3 30B-A3B (MoE) is fast for its size and fits in ~18 GB. Best local trade-off for the "escalation" tier if the machine has 32-64 GB. |
| Judge, large | `aya-expanse:32b`, `llama3.3:70b`, `qwen2.5:72b` | 20-45 GB | 64 GB+ Mac only; too slow for anything but re-checking a handful of flagged cells. |

Honest summary: for es/fr/it/pl/ru/tr/zh any 7-14B modern model is adequate for "is this the same rule?" judging. For **hi, ar and uk**, expect noticeably worse: models mix up Hindi/Urdu register, hallucinate Ukrainian as Russian, and are weakest at subtle polarity in Arabic. Calibrate with the seeded test set (Implementation Notes §3) before trusting any verdict in those three locales, and keep the model choice per-locale configurable.

## Decision

Adopt a **four-tier escalation pipeline**, cheapest and most reliable first, where each tier only runs on what the previous tier could not clear. Local LLM judging is the *last* tier and runs only on suspicious or changed cells, never as a blanket sweep in CI.

```
                    ┌────────────────────────────────────────┐
 master JSON ─────► │ Tier 0  source-hash staleness ledger    │ ─ stale? ──► flag, block release for that locale
                    │         (data/translation_state/*.json) │
                    └────────────────────────────────────────┘
                                     │ fresh
                    ┌────────────────▼───────────────────────┐
                    │ Tier 1  deterministic lint               │ ─ fail ────► flag (exact: number, token, script)
                    │         numbers/§/sign ids, leaked       │
                    │         tokens, script, untranslated     │
                    └────────────────────────────────────────┘
                                     │ pass
                    ┌────────────────▼───────────────────────┐
                    │ Tier 2  embedding similarity (bge-m3)    │ ─ below threshold ──► candidate
                    │         stem + correct option only       │
                    └────────────────────────────────────────┘
                                     │ candidates + all high_stakes + all changed cells
                    ┌────────────────▼───────────────────────┐
                    │ Tier 3  bilingual LLM judge (Ollama)     │ ─ structured JSON verdict ──► review queue
                    │         rubric, temp 0, schema output    │
                    └────────────────────────────────────────┘
```

Specifically:

1. **Tier 0 is the primary defence against defect 1 and is mandatory in CI.** It is a text-hash comparison, needs no model, and would have caught every staleness incident this project has had. Nothing in Tiers 1-3 is allowed to be a reason to delay Tier 0.
2. **Tier 1 runs in CI on every change** and is the exact-match defence for defects 3 and 6. It fails the build on a mismatched number in stem/correct option/explanation, or a forbidden token anywhere.
3. **Tier 2 runs in CI (CPU, `bge-m3`) on changed cells and on demand for full sweeps.** It produces candidates, never failures on its own, except for the "identical to source" and "far below floor" cases which are unambiguous.
4. **Tier 3 runs on a developer Mac via Ollama**, on: every cell flagged by Tier 2; every cell whose German changed (in addition to the Tier 0 flag, so the re-translation gets judged); every `high_stakes: true` cell on a schedule; and any cell a reviewer asks for. Verdicts are written to the ledger and committed. **CI does not run Tier 3; CI verifies that the ledger has a current verdict for every cell that requires one** ("CI checks the receipts, not the model").
5. **What Tier 3 compares.** The judge is asked three separate, narrowly scoped questions per cell, in this order of importance:
   - (a) Does the target **question stem** ask the same thing as the German stem, including any sign, number, § or condition it mentions?
   - (b) Does the target **correct option** (the letter(s) in `core.json.correct`) state the same rule with the same polarity and the same quantities as the German correct option, such that it is *the* correct answer to the target stem?
   - (c) For each **distractor**: is it still *wrong* with respect to the German correct answer, and does it *not* say the same thing as the correct option? Distractors are explicitly **not** required to be translations of the German distractors. This is the false-positive guard for the non-literal distractor convention.
   - (d) Does the target **explanation** preserve every number, sign id, legal reference and polarity of the German explanation? (Wording may differ; facts may not.)
6. **Model policy:** `bge-m3` for Tier 2; for Tier 3, a per-locale default (`aya-expanse:8b` for hi/ar/uk/tr/ro, `qwen2.5:14b` or `gemma3:12b` for the rest) with an optional escalation model (`gemma3:27b` or `qwen3:30b-a3b`) for any cell where the first verdict is `fail` or `confidence < 0.7`. All model tags are pinned by digest in the ledger, not by name.

## Consequences

### Positive

- Defect 1 (the most damaging class) becomes structurally impossible to ship unnoticed, at essentially zero cost, from the day Tier 0 lands - independent of any model quality question.
- Defects 3 and 6 are caught exactly, in CI, with no model.
- Defects 2, 4 and 5 get a fighting chance for the first time, targeted at the parts of a cell that carry the answer key (stem + correct option + explanation facts), not at distractor wording.
- Everything is local: no content leaves the machine, no API keys, no per-token bill; the Mac that already runs `build_modules.py` runs the checks.
- The ledger is a reviewable artifact: a reviewer who reads no Hindi can still see "judge X, prompt v3, said FAIL on polarity, confidence 0.91, quoted these two phrases" and decide what to do.
- Cost is proportional to change (D4): an unchanged cell with a current verdict is never re-judged.

### Negative and risks

- **Confident wrong verdicts.** A local 8-14B model will sometimes say `pass` on an inverted Hindi sentence and `fail` on a perfectly good Polish idiom, and will say both with `confidence: 0.9`. The confidence field is the model's self-report, not a calibrated probability. Mitigations: seeded test set with known-bad cells (§3) to measure per-locale precision/recall before the tier is allowed to block anything; `fail` verdicts from Tier 3 open a **review item, never an automatic revert**; two-model agreement for hi/ar/uk before a cell is marked "verified".
- **Review fatigue.** If Tier 3 flags 5 % of 16k cells, that is 800 review items nobody will read. The distractor-loose rubric and the "candidates only" policy for Tier 2 exist to keep this down, but the number is unknown until measured. If the seeded-set precision for a locale is below ~0.7, Tier 3 for that locale is advisory only (reported, not queued).
- **Hosted CI cannot run Ollama with a real model at useful speed.** GitHub-hosted runners have no GPU and ~7-16 GB RAM; `bge-m3` on CPU is fine, an 8B judge is not. Options, in order of preference: (i) the ledger-verification design above (chosen); (ii) a self-hosted runner on the dev Mac or a small Linux box with a GPU - adds an always-on machine to maintain; (iii) a hosted API for Tier 3 only - contradicts D3, and would need a PO decision on sending unreviewed content to a third party. If (i) proves too manual, revisit.
- **Determinism is best-effort, not bitwise.** `temperature: 0`, fixed `seed`, pinned model digest and schema-constrained output give repeatable verdicts in practice, but a different Ollama version, quantization, or Metal kernel can change a borderline verdict. The ledger therefore records the digest and Ollama version, and a verdict is only "reproduced" if re-run under the same pair.
- **Bootstrap debt.** Stamping today's hashes into the ledger marks the current state as the baseline, *including* translations that are wrong today. A full one-time Tier 2 + Tier 3 sweep of fuehrerschein (est. 8-25 h of Mac time for Tier 3 at 8B, see O5) is needed to make the baseline mean anything for quality, not just for drift. This can run overnight, per locale, and is resumable via the ledger.
- **Maintenance surface.** A new Python package under `scripts/`, a new committed state directory, a new CI job, and prompt files that need versioning. Modest, but it is a real new component in a repo that deliberately has almost none.
- **Model licensing.** Aya Expanse is CC-BY-NC; fine for internal tooling, would not be fine if the checker were ever offered as a product feature. Recorded here so nobody has to rediscover it.
- **Not a substitute for native review.** The best this pipeline can assert is "no machine-detectable divergence from the German". Register, naturalness and exam-realism in hi/ar/uk still need a human at some point (Phase 3 of the August plan is unchanged by this ADR).

## Implementation Notes

### §0. Fix the source-of-truth drift first (blocking)

Observed on 2026-09-05: today's fixes for `zeichen-04` (133→136), `zeichen-68` and `zeichen-132` were applied directly to `app/data/fuehrerschein/locales/{ar,pl,hi}.json` (see `tmp/apply_ar_fixes.py`), while the master `data/pilot_questions.json` (last modified 2026-08-06) still contains the stale text - `ar` differs from the master in 2 ids, `pl` in 3, `hi` in 4. The next `cd data && python3 build_modules.py` run will silently **regress** these fixes. Before any of the tiers below is built: port the fixes into `data/pilot_questions.json`, rebuild, and confirm `app/data` matches. Tier 0 keys off the master file, so this is not optional. (This ADR does not perform that port; it is a content change and needs its own card.)

### §1. Layout

```
scripts/i18n_qa/
  __init__.py
  common.py            # load master file, normalise a cell, sha256 helpers
  tier0_staleness.py   # ledger compare / stamp
  tier1_lint.py        # numbers, tokens, script, untranslated
  tier2_embed.py       # bge-m3 via Ollama /api/embed
  tier3_judge.py       # rubric prompt, schema-constrained JSON via Ollama /api/chat
  prompts/
    judge_v1.md        # versioned; hash of this file goes into every verdict
  ci_verify.py         # fails if any required verdict is missing/stale
data/translation_state/
  <module>.json        # the ledger, committed
```

Python 3 stdlib only (`json`, `hashlib`, `re`, `urllib.request`, `unicodedata`) so nothing needs installing beyond Ollama itself; matches `data/build_modules.py`. Tiers 2-3 talk to `http://localhost:11434` and fail with a clear message if it is not running.

### §2. The ledger (Tier 0)

One file per module, keyed by question id then locale:

```json
{
  "meta": {"module": "fuehrerschein", "source": "data/pilot_questions.json", "ledger_version": 1},
  "zeichen-68": {
    "source_hash": "sha256:3f1c…",            // hash of de question + options + explanation + core.correct
    "locales": {
      "ar": {"verified_against": "sha256:3f1c…", "verified_at": "2026-09-05",
             "how": "manual-fix tmp/apply_ar_fixes.py",
             "tier3": {"verdict": "pass", "confidence": 0.86, "model": "aya-expanse:8b@sha256:…",
                       "prompt": "judge_v1@sha256:…", "ollama": "0.x.y", "at": "2026-09-05T08:12:00Z"}},
      "es": {"verified_against": "sha256:9a02…", "verified_at": "2026-08-01", "how": "batch DN-35"}
    }
  }
}
```

`source_hash` is recomputed from the master on every run; a locale whose `verified_against` differs is **stale**. In the example, `es` is stale (its hash is the pre-revision German) - exactly the `zeichen-68` case. Hash input is normalised (NFC, whitespace-collapsed, options in `a..d` order, `correct` letters sorted) so a pure whitespace edit does not invalidate 11 translations.

Bootstrap: `python3 scripts/i18n_qa/tier0_staleness.py --module fuehrerschein --stamp-all --how "bootstrap 2026-09-05"` writes today's hashes for every cell. That asserts nothing about quality; it only makes future drift visible. Cells known to be stale today should be stamped with the *old* hash so they show up immediately - the simplest way is to bootstrap, then re-translate the known-bad ids and stamp only those.

Commands:

```
python3 scripts/i18n_qa/tier0_staleness.py --module fuehrerschein            # report stale cells, exit 1 if any
python3 scripts/i18n_qa/tier0_staleness.py --module fuehrerschein --id zeichen-68 --locale ar --stamp --how "re-translated by <agent>, reviewed <who>"
python3 scripts/i18n_qa/tier0_staleness.py --all-modules --json > tmp/stale.json
```

Rule for content agents (to be added to AGENTS.md when this lands): **whoever changes a German cell must either re-translate and stamp all locales in the same card, or leave them stale and say so in the card.** Silently stamping without re-translating is the one thing the ledger cannot detect; Tier 2 exists partly to catch that.

### §3. Deterministic lint (Tier 1)

Per cell, comparing target to de:

- **Numbers/ids:** every token matched in the de *stem, correct option(s) and explanation* by `\b\d{1,4}(?:[.,]\d+)?\b`, `Zeichen \d+(-\d+)?`, `§ ?\d+[a-z]?`, `Art\. ?\d+`, `Anlage \d` must appear in the target's corresponding field. Distractors are checked only for numbers that appear in the de correct option (so a translated distractor cannot accidentally carry the correct number). Per-module allow-list file for legitimate divergences.
- **Forbidden tokens:** `high_stakes`, `grundstoff`, `legal_basis`, `{{`, `}}`, `[[`, `TODO`, `FIXME`, "```". Applied to **all** locales including de - this is what catches defect 6 at its source.
- **Script check:** hi must contain Devanagari (`ऀ-ॿ`), ar Arabic (`؀-ۿ`), uk/ru Cyrillic, with uk additionally required to contain at least one of `іїєґ` somewhere in the file (a cheap "this is not Russian" heuristic - file-level, not per cell, to avoid false positives on short cells), zh CJK. Latin-only content in these locales = untranslated.
- **Untranslated:** target field byte-identical to de or en (ignoring quoted sign names like "Fußgänger", which are legitimately kept).
- **Structure:** same option keys as core, no empty strings, `correct` letters exist.
- **Length ratio:** target/de character ratio outside `[0.4, 2.5]` (zh lower bound ~0.25) → warn, not fail.

Exit non-zero on any fail; warnings are listed. Runs in well under a second per module.

### §4. Embedding tier (Tier 2)

```
python3 scripts/i18n_qa/tier2_embed.py --module fuehrerschein --locales ar,hi,uk --changed-only
```

For each cell, embed two strings per language: `stem` and `stem + " " + correct_option` (never distractors, never the explanation alone). Cosine similarity via `POST /api/embed {"model":"bge-m3", "input":[...]}`; embeddings cached in `tmp/embed_cache/<sha256-of-text>.json` so an unchanged German cell is embedded once across all locales. Thresholds live in `scripts/i18n_qa/thresholds.json`, per locale, and are set empirically: run the sweep once, plot the distribution, and put the threshold at the point where the seeded-bad cells (below) separate from the bulk. Do **not** pick a number a priori; hi/ar will sit lower than es/fr for perfect translations. Output is a candidate list (`tmp/tier2_candidates.json`), not a failure, except for `similarity < 0.2` (near-certain wrong content) which fails.

**Seeded test set (needed before Tiers 2 and 3 can be trusted):** `scripts/i18n_qa/seed/known_bad.json` - a hand-built list of ~40 cells with a known defect, built from *this repo's own history*: the pre-fix `zeichen-68`/`zeichen-132` texts for ar/es/fr/pl, the 133/136 cell, the Hindi inversion, three or four Polish false friends, and a few synthetic ones (swap a correct option with a distractor; negate a sentence). Plus ~40 known-good cells. Every prompt or threshold change is measured against this set; per-locale precision/recall goes into the PR description. This is the only way to know whether "confidence: 0.9" means anything.

### §5. Judge tier (Tier 3)

Prompt skeleton (`prompts/judge_v1.md`, rendered per cell; kept in German-plus-English to match the models' strongest instruction languages):

```
You are checking whether a translated multiple-choice exam question preserves the meaning of its German source.
The German is authoritative. Distractor options are NOT required to be translations - they only need to be
clearly wrong answers to the question. Judge meaning, polarity (must / must not), numbers, sign numbers and
legal references. Ignore style, register and word order.

SOURCE (de):
  question: "Was schreibt dieses Verkehrszeichen vor?"
  correct option (a): "Sie müssen hier geradeaus oder nach rechts weiterfahren."
  distractors: b: "...", c: "...", d: "..."
  explanation: "Zeichen 214 ist ein Vorschriftzeichen ..."

TARGET (ar):
  question: "..."
  option a: "..."   <- must be the correct answer
  options b, c, d: "..."
  explanation: "..."

Answer ONLY with JSON matching the schema.
```

Ollama call:

```python
body = {
  "model": "aya-expanse:8b",
  "messages": [{"role": "user", "content": prompt}],
  "stream": False,
  "options": {"temperature": 0, "seed": 42, "num_ctx": 4096},
  "format": {                      # JSON-schema-constrained output (supported by recent Ollama versions)
    "type": "object",
    "required": ["stem_equivalent", "correct_option_equivalent", "polarity_preserved",
                 "numbers_preserved", "distractor_became_correct", "explanation_facts_preserved",
                 "verdict", "confidence", "evidence"],
    "properties": {
      "stem_equivalent": {"type": "boolean"},
      "correct_option_equivalent": {"type": "boolean"},
      "polarity_preserved": {"type": "boolean"},
      "numbers_preserved": {"type": "boolean"},
      "distractor_became_correct": {"type": "array", "items": {"type": "string", "enum": ["a","b","c","d"]}},
      "explanation_facts_preserved": {"type": "boolean"},
      "verdict": {"type": "string", "enum": ["pass", "fail", "unsure"]},
      "confidence": {"type": "number", "minimum": 0, "maximum": 1},
      "evidence": {"type": "string", "maxLength": 400}
    }
  }
}
```

`verdict` is derived in code from the booleans, not trusted from the model: any of `stem_equivalent`, `correct_option_equivalent`, `polarity_preserved`, `numbers_preserved` false, or a non-empty `distractor_became_correct`, is a `fail` regardless of what the model wrote in `verdict`. `evidence` must quote the two phrases that differ; a fail without a quote is downgraded to `unsure`. Multi-choice questions (5 in fuehrerschein) pass all correct letters.

Runtime controls:

```
python3 scripts/i18n_qa/tier3_judge.py --module fuehrerschein --from tmp/tier2_candidates.json
python3 scripts/i18n_qa/tier3_judge.py --module fuehrerschein --high-stakes --locales hi,ar,uk --model aya-expanse:8b
python3 scripts/i18n_qa/tier3_judge.py --module datenschutz --changed-only --escalate-model gemma3:27b
python3 scripts/i18n_qa/tier3_judge.py --module fuehrerschein --id zeichen-68 --locale pl --explain   # print prompt + raw reply
```

- Results are cached by `(cell_hash_de, cell_hash_target, model_digest, prompt_hash)`; a re-run with nothing changed makes zero model calls.
- Batching: one cell per call. Multi-cell prompts save prompt-processing time but make the model cross-contaminate verdicts and break caching granularity; not worth it.
- Concurrency: Ollama serialises requests on one model by default; run one process per locale on a big Mac only if memory allows two model instances (usually it does not). Expect throughput of roughly 4-12 cells/min at 8B (estimate).
- Every verdict is appended to `data/translation_state/<module>.json` under `tier3` and to an append-only `tmp/tier3_log.jsonl` with the full prompt and raw reply for audit; the ledger keeps only the summary.

### §6. CI (GitHub Actions or Netlify build hook; no model beyond `bge-m3`)

```
on: pull_request, paths: ["data/*_pilot.json", "data/pilot_questions.json", "data/translation_state/**"]
steps:
  - python3 scripts/i18n_qa/tier1_lint.py --all-modules                      # exact checks, fail on error
  - python3 scripts/i18n_qa/tier0_staleness.py --all-modules                 # fail if any stale cell
  - python3 scripts/i18n_qa/ci_verify.py --require-tier3 high_stakes,changed  # fail if a required verdict is missing
  - (optional, CPU) ollama serve & ollama pull bge-m3 && tier2 --changed-only # candidates as PR comment only
```

`ci_verify.py` is the piece that makes the local-only Tier 3 acceptable: it compares the ledger against the diff (changed German cells, `high_stakes` cells) and fails if a required cell has no verdict whose `model`/`prompt` are on the current allow-list and whose hashes match. The developer runs Tier 3 on the Mac, commits the ledger, and CI goes green. If a self-hosted runner ever exists, the same scripts run there unchanged.

### §7. Phased rollout

| Phase | What | Effort (est.) | Gate to next |
|---|---|---|---|
| **P0** | Port today's `app/data` hot-fixes back into `data/pilot_questions.json`, rebuild, diff. | hours | `app/data` == build output |
| **P1** | Tier 0 ledger + Tier 1 lint, bootstrap for all modules, wire into CI, fix the nine `high_stakes` leaks in `datenschutz` de (+ their 12 translations), add the "stamp or declare stale" rule to AGENTS.md. | 1-2 days | CI red on a deliberately re-worded German cell; green after stamp |
| **P2** | Seeded test set (§4). Tier 2 with `bge-m3`; calibrate per-locale thresholds; full sweep of fuehrerschein (minutes). Triage candidates by hand once. | 1-2 days + review | precision on seeded set reported |
| **P3** | Tier 3 judge on: all Tier 2 candidates, all 82 `high_stakes` fuehrerschein cells × 11 locales (~900 calls, a few hours), then the eight ids from the August plan. Measure per-locale precision/recall on the seeded set with two candidate models. Decide per locale: blocking / advisory / disabled. | 2-3 days incl. overnight runs | per-locale decision recorded in `thresholds.json` |
| **P4** | Overnight full Tier 3 sweep of fuehrerschein, then motorrad/lkw/fuehrerschein_bus, then the 12/13-locale compliance modules; skip the 2-locale modules (`dora`, `nis2`, `kartellrecht`, `kyc_aml`, `lksg`, `fadp_ch`, `sportboot_*`) until they are localised. `ci_verify --require-tier3 changed,high_stakes` becomes blocking. | several nights of Mac time | ledger complete |
| **P5** | Revisit: is Tier 3 advisory-only for hi/ar/uk still acceptable, or is O6 (hosted judge) or native review needed there? Separate ADR if the answer changes D3. | - | - |

### §8. What this ADR deliberately does not do

- It does not make the LLM the gate for anything. Tier 0 and Tier 1 gate; Tiers 2-3 generate review items.
- It does not translate. When a cell is stale or failed, re-translation is still a content card done by an agent or a human, reviewed, and then stamped.
- It does not touch `app/`, `data/build_modules.py`, or any locale file. The only runtime-adjacent change is a new committed directory `data/translation_state/`, which `build_modules.py` ignores.
