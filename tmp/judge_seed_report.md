# Tier 3 judge - seeded viability report

- model: `qwen2.5:7b-instruct`
- digests: qwen2.5:7b-instruct@sha256:845dbda0ea48
- ollama: 0.33.3
- prompt: judge_v1.md@3b4f5d52a278
- cells: 146

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
| ar | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.1 | ADVISORY (report only, do not queue) |
| en | 5 | 1 | 20% | 5 | 0 | 0% | 100% | 0 | 5.7 | ADVISORY (report only, do not queue) |
| es | 7 | 5 | 71% | 7 | 0 | 0% | 100% | 0 | 5.9 | ENABLED (blocking-capable) |
| fr | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.5 | ADVISORY (report only, do not queue) |
| hi | 7 | 2 | 29% | 7 | 1 | 14% | 67% | 0 | 6.1 | ADVISORY (report only, do not queue) |
| it | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.3 | ADVISORY (report only, do not queue) |
| pl | 7 | 2 | 29% | 7 | 0 | 0% | 100% | 0 | 4.6 | ADVISORY (report only, do not queue) |
| ro | 4 | 2 | 50% | 4 | 0 | 0% | 100% | 0 | 6.0 | ADVISORY (report only, do not queue) |
| ru | 6 | 3 | 50% | 6 | 1 | 17% | 75% | 0 | 4.9 | ADVISORY (report only, do not queue) |
| tr | 6 | 2 | 33% | 6 | 0 | 0% | 100% | 0 | 4.9 | ADVISORY (report only, do not queue) |
| uk | 7 | 6 | 86% | 7 | 3 | 43% | 67% | 0 | 7.6 | DISABLED (too many false positives to be readable) |
| zh | 6 | 5 | 83% | 6 | 1 | 17% | 83% | 0 | 5.2 | ADVISORY (report only, do not queue) |
| **all** | 73 | 40 | 55% | 73 | 9 | 12% | 82% | 0 | | ADVISORY (report only, do not queue) |

Recall by defect class (how many of each real defect the judge caught):

| defect | n | caught | recall |
|---|---|---|---|
| leaked_high_stakes_token_in_target | 12 | 4 | 33% |
| synthetic_digit_flip | 12 | 5 | 42% |
| synthetic_foreign_cell | 12 | 12 | 100% |
| synthetic_swapped_correct_option | 12 | 1 | 8% |
| wrong_number_133_vs_136 | 5 | 1 | 20% |
| wrong_sign_mofa_vs_pedestrian | 10 | 8 | 80% |
| wrong_sign_obstacle_vs_214 | 10 | 9 | 90% |

### Flag policy: `fail` or `unsure` (the actual review-queue size)

| locale | n_bad | caught | recall | n_good | FP | FP rate | precision | errors | median s/cell | decision |
|---|---|---|---|---|---|---|---|---|---|---|
| ar | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.1 | ADVISORY (report only, do not queue) |
| en | 5 | 1 | 20% | 5 | 0 | 0% | 100% | 0 | 5.7 | ADVISORY (report only, do not queue) |
| es | 7 | 5 | 71% | 7 | 0 | 0% | 100% | 0 | 5.9 | ENABLED (blocking-capable) |
| fr | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.5 | ADVISORY (report only, do not queue) |
| hi | 7 | 2 | 29% | 7 | 1 | 14% | 67% | 0 | 6.1 | ADVISORY (report only, do not queue) |
| it | 6 | 4 | 67% | 6 | 1 | 17% | 80% | 0 | 5.3 | ADVISORY (report only, do not queue) |
| pl | 7 | 2 | 29% | 7 | 0 | 0% | 100% | 0 | 4.6 | ADVISORY (report only, do not queue) |
| ro | 4 | 2 | 50% | 4 | 0 | 0% | 100% | 0 | 6.0 | ADVISORY (report only, do not queue) |
| ru | 6 | 3 | 50% | 6 | 1 | 17% | 75% | 0 | 4.9 | ADVISORY (report only, do not queue) |
| tr | 6 | 2 | 33% | 6 | 0 | 0% | 100% | 0 | 4.9 | ADVISORY (report only, do not queue) |
| uk | 7 | 6 | 86% | 7 | 3 | 43% | 67% | 0 | 7.6 | DISABLED (too many false positives to be readable) |
| zh | 6 | 5 | 83% | 6 | 1 | 17% | 83% | 0 | 5.2 | ADVISORY (report only, do not queue) |
| **all** | 73 | 40 | 55% | 73 | 9 | 12% | 82% | 0 | | ADVISORY (report only, do not queue) |

Recall by defect class (how many of each real defect the judge caught):

| defect | n | caught | recall |
|---|---|---|---|
| leaked_high_stakes_token_in_target | 12 | 4 | 33% |
| synthetic_digit_flip | 12 | 5 | 42% |
| synthetic_foreign_cell | 12 | 12 | 100% |
| synthetic_swapped_correct_option | 12 | 1 | 8% |
| wrong_number_133_vs_136 | 5 | 1 | 20% |
| wrong_sign_mofa_vs_pedestrian | 10 | 8 | 80% |
| wrong_sign_obstacle_vs_214 | 10 | 9 | 90% |
