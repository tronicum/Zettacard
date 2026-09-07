# Mini MVP — Hetzner job runners for translation and QA

**Written:** 2026-09-07
**Scope:** the smallest useful thing that makes two Hetzner root servers earn their keep
**Related:** `scripts/i18n_qa/README.md`, `docs/adr/ADR-llm-translation-qa.md`, `docs/adr/ADR-ollama-setup.md`, `zettacard-kb` ADR-0002 (media), ADR-0003 (verification is a label), `ROADMAP-MVP.md`

## Why this exists, and why it is nearly free

`scripts/i18n_qa` is already written: a four-tier translation QA package, Python
standard library only, 31 offline tests passing, and its Ollama wire format
validated against a real server on 2026-09-05. Its own README opens with an
unusually honest warning:

> *"These scripts were written in a Linux VM with no Ollama installed and no
> network route to your Mac's localhost:11434. Not one line has ever been
> executed against a real model."*

That is the entire gap. The code exists, the tests pass, the schema is tight —
there has simply never been a machine to point it at. Two root servers close it.

**So the mini MVP is not "build a translation platform".** It is: stand up a
model endpoint, run the evaluation that already exists, and only then let it do
work. In that order.

## What runs where

| Concern | Where | Why |
|---|---|---|
| Serving the app | Netlify | Static, already works, no reason to move |
| CI gates (Tier 0 + 1) | GitHub Actions | Deterministic, seconds, must block a PR |
| Model inference (Tier 2 + 3) | **Hetzner, Docker** | Minutes to hours, must never block a PR |
| Translation drafting | **Hetzner, Docker** | Long batch work |
| TTS / subtitles (ADR-0002) | **Hetzner** later | 40,711 objects, 0 produced |
| Content of record | `zettacard-kb` in Git | Unchanged. The box proposes; Git decides |

The dividing line is the one the QA package already draws: **Tiers 0 and 1 gate
CI and are deterministic; Tiers 2 and 3 never gate anything — they open review
items.** A model on a box you own does not change that. It just means the review
items get produced at all.

## The one rule that keeps this safe

> **A job never writes to `main`, and never writes to `content/` directly. It
> opens a branch and a pull request.**

This is not ceremony. `zettacard-kb` ADR-0001 makes the KB the content master and
ADR-0003 makes verification a label rather than a wall — which only works because
a human decides what lands. A job that commits straight to content turns a
proposal into a fact, and the honest `pending` / `unverified` states stop meaning
anything. Same reason `src/import/` writes to `proposals/<batch_id>/` and never
to `content/` (ADR-0005).

Second rule, following from it: **the runner needs no inbound internet access.**
It pulls work from Git, runs, pushes a branch. No open port, no webhook receiver,
no public endpoint. That removes almost the entire attack surface, and it is why
this must not be a GitHub self-hosted Actions runner — those need to be reachable
by workflow dispatch, and on a public repo a fork PR can run code on them.

## The compose shape

Three services, one box to start. The second box is a warm spare, not a cluster —
do not build orchestration for two machines.

```
ollama          official image, models on a named volume, bound to 127.0.0.1
                only, no published port
worker          our image: python3-slim + git + the two repos checked out.
                Runs one job to completion, then exits. Restarted by a timer.
watchtower      optional; pins and updates the ollama image deliberately
```

Everything talks over the compose network. `ollama` publishes nothing to the
host. The worker holds a deploy key scoped to push branches, and nothing else.

Models, per `ADR-ollama-setup.md` and the existing CLI defaults:

- `bge-m3` — embeddings, Tier 2 pre-filter
- `qwen2.5:7b-instruct` — the Tier 3 bilingual judge

Both are pinned by **digest**, not tag. `ollama_client.py` already records the
digest from `/api/tags` per call, which is what makes a verdict reproducible and
a receipt meaningful. Pin them in compose too so a silent upstream retag cannot
change what a receipt refers to.

## The job families

### Job A — measure the judge *(must be first, and it is not optional)*

```
npm run qa:i18n:preflight     # models reachable, digests recorded
npm run qa:i18n:test          # the 31 offline tests, on this machine
npm run qa:i18n:seed          # build the seed set
npm run qa:i18n:eval          # ← the thing that has never run
```

`seed_eval.py` exists specifically to answer "are these verdicts any good", and
the README says plainly: *"run it before you believe a single verdict."* Until it
has, Tier 3 output is not evidence of anything. **This job is the mini MVP's
definition of done for phase one.** Not throughput — one number about quality.

Watch for the trap the README already documents: verdict determinism comes from
**schema tightness**, not from `temperature: 0`. With a loose schema, identical
requests at seed 42 diverged. Do not relax `judge.py`'s schema to let the model
explain itself.

And the rule that decides whether this tool survives contact with the data:
distractors are **deliberately not literal translations**. The judge checks two
things only — still clearly wrong, and not a restatement of the correct option.
A literalness check would flag hundreds of good cells and get switched off in a
week.

### Job B — Tier 2 + 3 over the backlog

Nightly. Embedding pre-filter ranks cells, the judge examines the top slice,
verdicts become **review items with receipts**, and the batch is pushed as a
branch. `verify_receipts.py --require high_stakes` already exists to check that
what is claimed was actually produced by the model it names.

Ordering: `high_stakes` first, then `points` descending, then the locales with
the most learners. There is no point judging Bavarian before Arabic.

### Job C — translation drafting

`zettacard-kb/src/translate_draft.py` already has `plan` / `extract` / `merge` /
`verify`. The worker runs extract → model → merge → **verify**, and pushes a
branch. Two things it must not skip:

- **`merge` enforces option-key equality with German.** Keep it.
- **`verify` compares ID sets, never counts.** That check exists because four
  agents once each reported full coverage of a locale and all four missed the
  same card. A machine worker will make that mistake more consistently than an
  agent, not less.

Everything it produces is `machine_draft` / `pending`, stamped with
`against_source_hash`. That is what makes a draft falsifiable when the German
cell later changes.

### Job D — media (later)

ADR-0002's 40,711 TTS and subtitle objects, UUIDv5-addressed, on the SSD rather
than in Git. Not in this mini MVP, but it is why the box is worth having: it is
compute-heavy, latency-insensitive, embarrassingly parallel, involves no personal
data, and it is worth more to a learner who reads German poorly than any amount
of CI.

## Sequence

1. One box, Docker, Ollama bound to loopback, both models pulled and pinned.
2. Worker image; deploy key that can push branches and nothing else.
3. **Run Job A.** Read the number. Decide whether Tier 3 is usable at all.
4. If yes: Job B nightly, output as PRs, triaged like HUNT candidates.
5. Job C for the locales with real coverage gaps.
6. Second box stays a spare until something is actually saturated.

## Open decisions

- **Server specs.** Hetzner root servers are usually CPU-only (AX/EX line). A 7B
  judge on CPU is workable for overnight batch and unusable interactively; a GPU
  box changes throughput by an order of magnitude and nothing else about this
  plan. Which do you have?
- **Where PRs land.** `zettacard-kb` (content master) for Jobs B and C. Confirm
  the KB is pushed to a real GitHub repo — `TODO.md` item 2 says it may still
  exist only as a local repo delivered by bundle, which would block this.
- **Model licences.** Qwen2.5 and BGE-M3 ship under their own terms. Worth
  five minutes before output derived from them enters a CC-licensed corpus,
  and the answer belongs in `quellen.html` alongside everything else.
