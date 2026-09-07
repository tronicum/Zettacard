# Tier 3 judge - seeded viability report

- model: `qwen2.5:3b-instruct`
- digests: qwen2.5:3b-instruct@sha256:357c53fb659c
- ollama: 0.33.3
- prompt: judge_v1.md@3b4f5d52a278
- cells: 16

## How to read this

**Precision on the known-good half is what decides viability.** A judge that flags
everything has perfect recall and is worthless: nobody reads a review queue of
hundreds of items, and the tier gets switched off within a week. Read the FP-rate
column first, the recall column second.

Thresholds (ADR-llm-translation-qa / ADR-ollama-setup §6): FP rate on known-good
<= 10 % **and** recall >= 70 % enables a locale; FP > 20 % disables it whatever the
recall; anything in between is advisory - reported, never queued, never blocking.

The known-good cells are *presumed* good (ledger-clean, not natively reviewed). A
flag on one of them may be a real find; check before counting it as a false positive.

### Flag policy: `fail` only (strict - what would block)

| locale | n_bad | caught | recall | n_good | FP | FP rate | precision | errors | median s/cell | decision |
|---|---|---|---|---|---|---|---|---|---|---|
| es | 7 | 5 | 71% | 7 | 4 | 57% | 56% | 0 | 39.5 | DISABLED (too many false positives to be readable) |
| fr | 2 | 2 | 100% | 0 | 0 | nan% | 100% | 0 | 51.5 | DISABLED (too many false positives to be readable) |
| **all** | 9 | 7 | 78% | 7 | 4 | 57% | 64% | 0 | | DISABLED (too many false positives to be readable) |

Recall by defect class (how many of each real defect the judge caught):

| defect | n | caught | recall |
|---|---|---|---|
| leaked_high_stakes_token_in_target | 3 | 3 | 100% |
| synthetic_digit_flip | 1 | 0 | 0% |
| synthetic_foreign_cell | 2 | 2 | 100% |
| synthetic_swapped_correct_option | 1 | 0 | 0% |
| wrong_sign_mofa_vs_pedestrian | 1 | 1 | 100% |
| wrong_sign_obstacle_vs_214 | 1 | 1 | 100% |

### Flag policy: `fail` or `unsure` (the actual review-queue size)

| locale | n_bad | caught | recall | n_good | FP | FP rate | precision | errors | median s/cell | decision |
|---|---|---|---|---|---|---|---|---|---|---|
| es | 7 | 6 | 86% | 7 | 6 | 86% | 50% | 0 | 39.5 | DISABLED (too many false positives to be readable) |
| fr | 2 | 2 | 100% | 0 | 0 | nan% | 100% | 0 | 51.5 | DISABLED (too many false positives to be readable) |
| **all** | 9 | 8 | 89% | 7 | 6 | 86% | 57% | 0 | | DISABLED (too many false positives to be readable) |

Recall by defect class (how many of each real defect the judge caught):

| defect | n | caught | recall |
|---|---|---|---|
| leaked_high_stakes_token_in_target | 3 | 3 | 100% |
| synthetic_digit_flip | 1 | 0 | 0% |
| synthetic_foreign_cell | 2 | 2 | 100% |
| synthetic_swapped_correct_option | 1 | 0 | 0% |
| wrong_sign_mofa_vs_pedestrian | 1 | 1 | 100% |
| wrong_sign_obstacle_vs_214 | 1 | 1 | 100% |
