# `scripts/i18n_qa` - local-LLM translation QA (Tiers 2 and 3)

Implements the model-based half of `docs/adr/ADR-llm-translation-qa.md`, with the
operational setup from `docs/adr/ADR-ollama-setup.md`. Python 3 standard library
only - nothing to `pip install`. The only external dependency is Ollama, running
on your Mac.

> ## Read this before you trust anything in here
>
> **These scripts were written in a Linux VM with no Ollama installed and no
> network route to your Mac's `localhost:11434`. Not one line has ever been
> executed against a real model.** What *is* verified is everything that does not
> need a model: prompt construction, verdict derivation, rejection of malformed
> replies, receipt round-tripping, the seed set, and the hash agreement with
> `translation_ledger.py` - 31 tests in `test_offline.py`, all passing (see
> "Offline tests" below). The live path - does Ollama answer, does the model fill
> the schema, are the verdicts any good - is unmeasured. `seed_eval.py` exists
> precisely to measure it; run it before you believe a single verdict.
>
> **Update, 2026-09-05 - the WIRE FORMAT has since been validated.** A real
> Ollama (v0.33.3, Linux x86_64) was installed in a throwaway cloud container
> and driven with `qwen2.5:0.5b-instruct`. That container is not your Mac and
> the model is far too small to judge anything, so this says nothing about
> verdict quality - but it does settle the API questions this package had only
> assumed. See "Validated wire format" below. Verdict quality remains entirely
> unmeasured.

## Validated wire format

Observed against Ollama **v0.33.3** on 2026-09-05, using `qwen2.5:0.5b-instruct`
in a disposable Linux container. Recorded because this package was otherwise
written entirely against the ADR's description of the API rather than the API
itself. If a future Ollama disagrees with any of this, the response wins.

- **`format` accepts a full JSON Schema object** and the model's `response` field
  comes back as a string containing schema-conforming JSON. Confirmed end to end.
- **`/api/tags` exposes `digest`** per model (64-hex), alongside `size` and a
  `details` block carrying `quantization_level`, `parameter_size`,
  `context_length` and `embedding_length`. The provenance recording in
  `ollama_client.py` is therefore sound.
- **`/api/generate` returns** `response`, `model`, `done`, `done_reason`,
  `eval_count`, `eval_duration`, `load_duration`, `prompt_eval_count`,
  `prompt_eval_duration`, `prompt_eval_cached_count`, `total_duration`,
  `context`, `created_at`. The field names this package reads all exist.
- **Both `/api/embed` and `/api/embeddings` are live routes.** Neither 404s; a
  model that cannot embed returns a descriptive error instead. The fallback in
  `ollama_client.py` is correct, and an embedding failure will surface as a
  model-capability error rather than a routing one.
- **Determinism depends on schema tightness, not only on `temperature: 0`.**
  This is the finding worth keeping. With a LOOSE schema (`confidence` as an
  unbounded integer, `distractor_became_correct` as free strings) two identical
  requests at `temperature: 0, seed: 42` produced DIFFERENT output, and the
  model returned `confidence: 100` and a whole sentence where an option letter
  belonged. With the TIGHT schema this package actually uses - `confidence`
  bounded `0..1`, `distractor_became_correct` an `enum` of option letters - five
  identical requests were byte-identical, and a cold-loaded call matched a warm
  one. The constrained schema in `judge.py` is doing real work; do not relax it
  to "let the model explain itself".

None of this measures whether a model's judgements are any *good*. That is still
`seed_eval.py`'s job, and it has not been run.

## Where this sits

| Tier | What | Where | Gates CI? |
|---|---|---|---|
| 0 | source-hash staleness ledger | `scripts/translation_ledger.py` | **yes** |
| 1 | deterministic structural lint | `scripts/check_data_integrity.py` | **yes** |
| 2 | embedding pre-filter (ranking only) | `embed_screen.py` | no |
| 3 | bilingual LLM judge | `judge.py` | no - it opens review items |
| - | receipts of Tier 3 verdicts | `receipts.py`, `verify_receipts.py` | receipts, not the model |

Tiers 0 and 1 are already implemented, already run in `npm run check:all`, and
catch the defect classes they catch with **zero** false positives. Nothing here
replaces them. If you only ever run one thing, run those.

## The rule that makes or breaks this tool

This project's distractor options are **deliberately not literal translations**:
a translator may replace a wrong answer with one that is more plausible for a
reader of that language. A judge that asks "is this a faithful translation"
would flag several hundred perfectly good cells, and you would switch it off
inside a week.

So distractors are checked for exactly two things - *still clearly wrong*, and
*not a restatement of the correct option* - and nothing else. That rule is
stated in capitals in `prompts/judge_v1.md`, enforced again in
`judge.derive_verdict()` (any correct-key letter the model names is discarded),
and pinned by tests. Do not "improve" the prompt into a literalness check.

## Run it on the Mac, in this order

### 0. Prerequisites (once)

Follow `docs/adr/ADR-ollama-setup.md` §3: install Ollama, put the model store on
the external SSD, raise the keep-alive so the model is not reloaded from the SSD
between cells.

```bash
export OLLAMA_MODELS=/Volumes/<SSD-NAME>/ollama
export OLLAMA_KEEP_ALIVE=60m
export OLLAMA_NUM_PARALLEL=1
ollama serve            # leave this running in its own terminal

# in a second terminal
ollama pull bge-m3                 # ~1.2 GB, Tier 2
ollama pull qwen2.5:7b-instruct    # ~4.7 GB, Tier 3 candidate 1
ollama pull aya-expanse:8b         # ~5 GB, Tier 3 for hi/ar/uk/tr/ro (CC-BY-NC - your call)
```

Your machine (Apple Silicon, **36 GB unified memory**, external SSD) comfortably
holds `bge-m3` plus a 12-14B judge resident at the same time, and can host a
single 27B at Q4 (~17-20 GB) with the browser closed. So the ADR's per-locale
model policy is affordable here as written; you are not forced into the "one 8B
model for everything" fallback that a 16 GB machine would impose. Nothing else
about the machine is assumed.

### 1. Offline tests and preflight (seconds)

```bash
python3 scripts/i18n_qa/test_offline.py                    # no Ollama needed
python3 scripts/i18n_qa/ollama_client.py --model bge-m3 --model qwen2.5:7b-instruct
```

The second command is the readiness check: it prints the Ollama version and the
**full sha256 digest** of each model (tags move; digests are what receipts pin).
If Ollama is not running, or a model is missing, it says which and what to type.

### 2. Build the labelled set (seconds, no model)

```bash
python3 scripts/i18n_qa/seed_eval.py build-seed
```

Writes `seed/known_bad.json` and `seed/known_good.json` (73 + 73 cells as of
2026-09-05, balanced per locale). The bad half is reconstructed from this repo's
real, documented defects, with the defective text embedded verbatim so the files
keep working after `tmp/` is cleaned:

| defect class | n | source |
|---|---|---|
| `wrong_sign_obstacle_vs_214` (`zeichen-68`) | 10 | `tmp/pilot_questions.backup-20260905-072649.json` |
| `wrong_sign_mofa_vs_pedestrian` (`zeichen-132`) | 10 | same backup / `tmp/pilot.pre-z132fix.json` |
| `wrong_number_133_vs_136` (`zeichen-04`) | 5 | same backup |
| `leaked_high_stakes_token_in_target` | 12 | `tmp/datenschutz_pilot.pre-highstakes.json` |
| `synthetic_swapped_correct_option` | 12 | generated (answer-key breakage) |
| `synthetic_foreign_cell` | 12 | generated (another question's target cell) |
| `synthetic_digit_flip` | 12 | generated (one digit changed in the stem) |

The German half of every bad cell is today's German, byte-identical - these are
pure translation defects, not Tier 0 staleness. The good half is an equal number
of ledger-clean cells per locale, with **no id shared between the halves**
(a cell scored twice with opposite labels would corrupt both numbers).

The good half is *presumed* good, not proven good. If the judge flags one and you
agree it is wrong, move it to the bad half - the measurement gets better, and you
have found a real defect.

### 3. Run the viability experiment (the gate on everything else)

```bash
python3 scripts/i18n_qa/seed_eval.py run --model qwen2.5:7b-instruct
python3 scripts/i18n_qa/seed_eval.py run --model aya-expanse:8b        # second opinion
cat tmp/judge_seed_report.md
```

~146 cells; at the ADR's 5-15 s/cell estimate that is roughly 12-35 minutes per
model (an estimate, not a measurement - the report prints the real median).
Prompts and raw replies go to `tmp/judge_seed_log.jsonl` for audit.

**Read the false-positive column first.** Precision on the known-good half is
what decides viability; a judge that flags everything has perfect recall and is
worthless. The gate, per locale:

| result | decision |
|---|---|
| FP rate <= 10 % **and** recall >= 70 % | **enabled** - may block |
| FP rate <= 20 %, recall short of 70 % | **advisory** - report, never queue |
| FP rate > 20 % | **disabled** for that locale, whatever the recall |

Expect the honest answer to differ per locale: es/fr/it/pl/ru/tr/zh should be
fine on a 7-14B model; hi, ar and uk are where small open models are weakest and
where this repo has had no native review. If a locale lands in "disabled",
that is a useful result, not a failure of the tool.

### 4. Only then: screen and judge real content

```bash
# Tier 2 - ranked candidates, never a pass/fail
python3 scripts/i18n_qa/embed_screen.py --module fuehrerschein --top 40 --json tmp/tier2_candidates.json

# Tier 3 - one cell, printing the prompt and the raw reply
python3 scripts/i18n_qa/judge.py --module fuehrerschein --id zeichen-132 --locale ar --explain

# Tier 3 - the high-stakes sweep for the locales the experiment enabled
python3 scripts/i18n_qa/judge.py --module fuehrerschein --high-stakes --locales pl,tr --model qwen2.5:7b-instruct

# build every prompt without calling anything (works with Ollama switched off)
python3 scripts/i18n_qa/judge.py --module fuehrerschein --id zeichen-68 --locale pl --dry-run --explain
```

Each judged cell appends one receipt line to
`data/translation_state/verdicts/<module>.jsonl`. Commit those with the content
change: they are the evidence CI checks.

### 5. What CI does (no model, ever)

```bash
npm run check:data            # Tier 1
npm run check:translations    # Tier 0
npm run check:receipts        # verify_receipts.py --require high_stakes
```

`verify_receipts.py` re-derives today's German hash and today's translation hash
and demands a receipt that matches both. A German edit or a re-translation
invalidates the receipt, exactly as it invalidates a Tier 0 stamp. It never
fails on a `fail` verdict - Tier 3 is advisory, and a verdict is a review item.

Today `--require high_stakes` reports ~902 missing receipts for `fuehrerschein`
alone, so **do not put it in `check:all` until the sweep has run**; run it by
hand, or with `--require none` (which only checks the integrity of the receipts
that do exist).

## Offline tests

```
$ python3 scripts/i18n_qa/test_offline.py
...
PASSED: 31 test(s), no model and no network involved
```

They cover: prompt determinism (including dict-order independence), the verdict
derivation over all 2^5 boolean combinations x distractor lists x evidence
present/absent, the correct-letter discard rule, thirteen kinds of malformed
model reply (prose, empty, truncated JSON, array, wrong types, out-of-range
confidence, unknown option letter, markdown fences) each of which must produce
`error` and never `pass`, receipt round-tripping and provenance validation, the
"Ollama is down" and "model not pulled" error messages, the embedding screen
never seeing a distractor, seed-set balance and disjointness, and the agreement
between `cells.source_hash` and `translation_ledger.source_hash`.

Scratch files go to `tmp/i18n_qa_test/`.

## Files

| file | what |
|---|---|
| `cells.py` | load/normalise/hash one cell; re-exports `translation_ledger.source_hash` rather than reimplementing it |
| `ollama_client.py` | stdlib HTTP client; injectable transport; provenance on every call; also a CLI preflight |
| `judge.py` | Tier 3 rubric prompt, schema, and the Python-side verdict derivation |
| `prompts/judge_v1.md` | the rubric. Versioned; its sha256 is in every receipt. Add `judge_v2.md`, never edit this in place once verdicts exist |
| `seed_eval.py` | builds the labelled set and measures precision/recall per locale |
| `embed_screen.py` | Tier 2 ranking pre-filter (stem + correct option only) |
| `receipts.py` | append-only verdict receipts |
| `verify_receipts.py` | the CI-side check that needs no model |
| `test_offline.py` | everything above, tested without a model |
| `seed/` | the committed labelled set |

## Deliberate non-goals

- No translating. A `fail` is a review item; re-translation stays a content card.
- No hosted API fallback. Content does not leave the machine (ADR driver D3).
- No writing into `data/translation_state/<module>.json`. The ledger's schema is
  committed and Tier 0 stays dumb; verdicts live in `verdicts/` beside it.
- No blocking on a model verdict anywhere in CI.
