# First live measurement of the Tier 3 judge

**Date:** 2026-09-05
**Status:** preliminary — small model, small sample, CPU-only. Read the caveats.

## How this was produced

`scripts/i18n_qa` was written without any access to Ollama (see the README's
warning). This is its first execution against a real model.

- **Where:** a disposable Linux x86_64 cloud container, **not** the target Mac.
- **Ollama:** v0.33.3. **Model:** `qwen2.5:3b-instruct` (Q4, 1.9 GB).
- **Sample:** 16 seed cells (9 known-bad, 7 known-good), locales `es` and `fr`.
- **Speed:** ~40–70 s/cell on CPU. Metal on the target Mac will be far faster.

The 3B model is **well below** the 7–14B that ADR-ollama-setup recommends, and
16 cells is a tenth of the seed set. Nothing here settles whether a properly
sized judge works. It does, however, settle one design question decisively.

## The headline: `distractor_became_correct` was pure noise

The judge names a distractor on **16 of 16 cells — every known-good cell and
every known-bad cell alike.**

| signal | recall | false-positive rate | precision |
|---|---|---|---|
| distractor signal only | 9/9 = **100%** | 7/7 = **100%** | 56% |
| semantic flags only (stem, correct option, polarity, numbers, explanation) | 2/9 = 22% | 1/7 = 14% | 67% |
| either (current behaviour) | 100% | **100%** | 56% |

A signal that fires on 100% of good cells and 100% of bad cells carries **zero
information**. It is not a weak signal to be tuned; at this model size it is
noise, and because the current verdict logic treats it as a hard failure it
alone drags the whole judge to a 100% false-positive rate and a `DISABLED`
verdict for every locale.

This is precisely the risk both ADRs predicted — the non-literal distractor
convention is the hardest thing to explain to a judge — and the prompt already
leads with a capitalised warning about it. The warning was not enough for a 3B
model.

## What the semantic flags did well

Ignoring the distractor signal entirely, the judge cleanly caught **both real
sign-swap defects**, the exact class that cost a day of agent time to find:

- `zeichen-68` (es) — obstacle-passing vs Zeichen 214 mandatory-direction
- `zeichen-132` (es) — "Mofa frei" moped plate vs "Fußgänger" supplementary sign

Both fired `correct_option_equivalent`, `polarity_preserved`,
`numbers_preserved` and `explanation_facts_preserved` together — a strong,
legible pattern. One known-good cell (`autobahn-01`, es) fired the same way and
is a genuine false positive worth reading.

The nine `high_stakes` leak cells were **not** caught semantically. They were
only "caught" by the noise distractor signal, which is not a real catch. That
matters less than it sounds: Tier 1 (`check_data_integrity.py`) already catches
leaked tokens deterministically, which is where that defect belongs.

Two synthetic defect classes were missed entirely at this model size:
`synthetic_digit_flip` (0/1) and `synthetic_swapped_correct_option` (0/1).

## Recommended changes before spending a real eval run

1. **Do not let `distractor_became_correct` drive a `fail` on its own.**
   Demote it to advisory: record it, never let it fail a cell by itself. Revisit
   only if a 7–14B model shows it discriminating between good and bad cells.
2. **Re-run the gate on semantic flags only** and compare. On this sample that
   alone takes the false-positive rate from 100% to 14%.
3. **Require the evidence quote for distractor claims too.** The downgrade rule
   already saved one bad verdict (`zeichen-132`, ar) that came back with no
   quote.
4. **Judge the model on the two sign-swap cases first.** They are cheap, real,
   and the defect class actually worth catching.

## Caveats, stated plainly

- 3B model; 7–14B recommended. Bigger models may use the distractor field far
  better — or may not. Unmeasured.
- n=16, one module pair, two locales. `fr` contributed no known-good cells, so
  its 100% precision is meaningless.
- CPU-only container, not Apple Silicon with Metal.
- No conclusion here should be read as "the judge does/doesn't work". The one
  robust finding is about the distractor signal, and it is robust because a
  signal firing on every single cell needs no large sample to diagnose.

Raw artefacts: `tmp/judge_seed_report.md`, `tmp/judge_seed_log.jsonl`.
