# ADR-0004: Ollama setup and operations for local translation QA (hardware, disk, models, runbook)

- **Status:** Proposed
- **Date:** 2026-09-05
- **Deciders:** PO (Stefan); drafted by an AI agent from a read of the repo and the live ledger on this date
- **Companion to:** `ADR-llm-translation-qa.md` (the *strategy* ADR: four-tier escalation, rubric, ledger design). This document is the *setup and operations* companion. It does not re-argue the strategy.
- **Numbering note:** `docs/adr/` currently holds `ADR-0001` (`ADR-exam-e2e-testing.md`), `ADR-001` (`ADR-llm-translation-qa.md`, written the same day by a different agent and colliding with 0001) and `ADR-0003` (`ADR-mobile-layout.md`, which already notes the collision and reserves `0002` for the translation-QA ADR). This document takes the next free four-digit number, **`ADR-0004`**, and does not touch the other files. The rename of `ADR-001` to `ADR-0002` is still owed; when that happens, update the "Companion to" line above.

---

## Do I need more disk? (short answer)

**Yes.** `6.2 GiB` free is not enough to run this pipeline on the internal disk, and the external SSD you attached is the right fix.

The line you pasted:

```
/dev/disk3s1s1   460Gi    12Gi   6.2Gi    66%   ...
```

is the sealed *system* volume of an APFS container. The `460Gi` is the whole container, the `12Gi` is what *that one volume* uses, and the `6.2Gi` is what is **actually left in the container for anything** - your Data volume, Ollama, everything. So the machine is at roughly 6 GiB free, full stop. (Confirm with `df -h /System/Volumes/Data`, which shows the same "Avail" figure.)

What that buys you, against approximate Ollama download sizes (Q4_K_M unless noted; ±10-15 %, check with `ollama list` after a pull):

| Need | Approx. on disk | Fits in 6.2 GiB? |
|---|---|---|
| `bge-m3` embedding model (Tier 2) | ~1.2 GB | yes |
| one 7-9B instruct judge (`qwen2.5:7b-instruct`, `aya-expanse:8b`, `qwen3:8b`, `llama3.1:8b`) | ~4.5-5.2 GB | **only just, with no headroom** - and macOS gets unstable and starts refusing writes below ~2-3 GB free |
| `bge-m3` + one 7-9B judge | ~6-6.5 GB | **no** |
| one 12-14B judge (`gemma3:12b`, `qwen2.5:14b`, `mistral-nemo:12b`) | ~7-9 GB | no |
| one 27-30B judge (`gemma3:27b`, `qwen3:30b-a3b`, `qwen2.5:32b`) | ~17-20 GB | no |
| two instruct judges (for the two-model agreement rule on hi/ar/uk) | ~10-14 GB | no |

Plus non-model overhead you must budget for: Ollama's partial-download blobs land in the *same* directory during a `pull` (so a pull briefly needs up to 2× the model size if it is retried), the Ollama app itself (~0.5-1 GB with its bundled runners), and `tmp/` caches this pipeline writes (embeddings, judge logs: tens of MB to a few hundred MB). The KV cache during inference is **RAM**, not disk (see "RAM matters more" below) - it does not need disk space, but it does need memory.

**Comfortable working figure: 40-60 GB free for models.** That buys you `bge-m3`, two small judges (one Qwen-family for JSON discipline, one Aya-family for hi/ar/uk coverage), one 12-14B mid model, and room to try one 27-30B model without deleting anything first. **100 GB+** if you want to keep several 27-30B candidates side by side while you evaluate them. Anything below ~15 GB free means one model at a time and deleting between experiments, which is workable for tonight's experiment but not for the phased rollout in the strategy ADR.

**Recommendation:** put the Ollama model store on the external SSD (`OLLAMA_MODELS`, runbook §3) and leave the internal disk alone. Note that the external SSD solves *disk*, not *RAM* - whether a model runs at all is decided by RAM, which this document cannot see (§"RAM matters more").

---

## Context

The strategy ADR (`ADR-llm-translation-qa.md`) decided on a four-tier escalation: source-hash ledger → deterministic lint → embedding similarity → bilingual LLM judge, with the LLM tier running on a developer Mac via Ollama and never in CI. Since it was written, the two model-free tiers have been **implemented and are real code**:

- `scripts/translation_ledger.py` - Tier 0. Per `(module, id, locale)` SHA-256 of the German source cell (`question + options + explanation + correct`), stored in `data/translation_state/<module>.json`. Subcommands `check` (exit 1 on stale/untracked), `stamp` (`--module`, `--locale`, `--id`), `status`. Master files in `data/*_pilot.json` / `data/pilot_questions.json` are the source of truth, not `app/data/`.
- `scripts/check_data_integrity.py` - Tier 1 (structural checks + leaked authoring tokens: `high_stakes`, `grundstoff`, `topic_code`, `TODO`, `FIXME`, `{{...}}`). Passes on all 25 modules today; the nine `datenschutz` `high_stakes` leaks (× 11 locales = 99 learner-visible strings) are fixed.
- `package.json`: `check:data`, `check:translations`, `translations:status`, `translations:stamp`.

Live state on 2026-09-05 (`python3 scripts/translation_ledger.py status`, run by the author of this document):

| module | questions | locales | stale | untracked |
|---|---|---|---|---|
| fuehrerschein, motorrad, lkw, fuehrerschein_bus | 531 / 138 / 90 / 48 | 11 | 0 | 0 |
| datenschutz | 40 | 12 | 0 | 0 |
| arbeitssicherheit, it_sicherheit, ki_act | 40 / 64 / 40 | 12 | 0 | 160 / 256 / 160 |
| hinweisgeberschutz | 40 | 11 | 0 | 440 |
| angelschein_bayern, angelschein_nrw | 48 / 56 | 11 | 0 | 528 / 616 |
| cka | 131 | 3 | 0 | 393 |
| aevo, dora, fadp_ch, kartellrecht, kyc_aml, nis2, sportboot_binnen, sportboot_see | - | 1 | 0 | 76 / 20 / 40 / 30 / 30 / 20 / 300 / 215 |
| **total** | 2,187 tracked | | **0** | **3,284** |

So **3,284 translations in 15 modules have never been checked against their German** (the figure quoted in the card that commissioned this ADR was 3,444 across 16; some stamping has happened since). `check:translations` therefore exits 1 today, by design.

Two things the ledger *cannot* see, found while reading the data for this ADR, and which set the agenda for the LLM tier:

1. **`zeichen-132` is still wrong in four locales, and the ledger says it is fine.** In `data/pilot_questions.json` the German stem describes the "Fußgänger" supplementary sign 1010-53; `ar`, `pl`, `tr` and `uk` still describe a "Mofa frei" plate (`pl` correct option: "Motorowery można tu prowadzić wyłącznie z wyłączonym silnikiem"). The ledger has all eleven locales of `zeichen-132` stamped against the *current* German hash. This is the "stamp without re-reading" failure the ledger docstring warns about, and it is exactly the class only Tiers 2-3 can catch. It is also a ready-made, real, live known-bad set for tonight's experiment (§6).
2. `zeichen-68` (obstacle-passing vs. Zeichen 214) and `zeichen-04` (133 vs. 136) are fixed in the master in all locales - they are the known-good half of the same experiment.

### The hardware question

The user's Mac has ~6.2 GiB free (see the short answer above) and an external SSD has since been attached. **The user's Mac's RAM is unknown to the author of this document** - it was written from a Linux VM that mounts the repo, not from the Mac - and must be reported by the user (§"RAM matters more"). No RAM figure is assumed anywhere below; every model tier is given per RAM size.

## Decision Drivers

- D1. **Runs at all on the machine we have.** Disk is a solved problem with the SSD; RAM decides the model tier and is unknown.
- D2. **Reproducible verdicts** (strategy ADR D2/D5): same input, same model digest, same prompt hash → same JSON. Setup must make pinning easy, not optional.
- D3. **Nothing leaves the machine** (strategy ADR D3). Local Ollama only; no hosted fallback is configured here.
- D4. **Cheap to re-run** (strategy ADR D4): the ledger and a content-hash cache mean an unchanged cell is never re-judged; setup must not fight that (e.g. by unloading the model every five minutes and reloading from a slow bus).
- D5. **Honest about model quality on hi/ar/uk/ro** - the setup includes the measurement that tells us whether the tier is viable per locale, before anything is scheduled.
- D6. **Minimal footprint.** The repo deliberately has almost no tooling; this adds an external service (Ollama) and a few scripts, nothing else. No Python packages beyond stdlib.

## Considered Options

### O1. Free up the internal disk and keep everything internal
Delete ~40-60 GB of whatever is filling the 460 GB container. Fastest bus, no unplug risk, no env var. Rejected as the *primary* plan because the user's own report is that space is the constraint and an SSD is already attached; kept as the fallback if the SSD turns out to be slow or flaky. If they do free the space later, moving the store back is a copy of one directory.

### O2. External SSD as the Ollama model store only (`OLLAMA_MODELS`) - **chosen**
Repo, ledger, caches and Ollama binary stay internal; only the model blobs (the big, static, re-downloadable part) live on the SSD. Cost: slower first load of each model per session; risk: unplugged-disk failure mode (§3). Everything on the SSD is re-downloadable, so losing it loses nothing but time.

### O3. External SSD for the whole working set (repo + Ollama + caches)
Unnecessary: the repo is small, and the judge cache/ledger belong next to the repo so they get committed. Rejected.

### O4. A separate always-on Ollama host (Linux box with a GPU, or a second Mac) reached via `OLLAMA_HOST`
The strategy ADR already lists this as the self-hosted-runner option. Not now: it adds a machine to maintain before we know the tier is viable. Kept as the escalation path if the Mac's RAM turns out to cap us at 8B and 8B proves inadequate for hi/ar/uk.

### O5. Hosted API judge
Contradicts D3; listed for completeness only, as the strategy ADR does.

## Decision

1. **Install Ollama on the Mac** (the Ollama.app installer or Homebrew; not both), verify the HTTP API on `localhost:11434`, and **point the model store at the external SSD** via `OLLAMA_MODELS`, formatted APFS.
2. **Pull a minimal model set first**, sized by the RAM the user reports (§2): `bge-m3` plus **one** 7-9B judge. Pull a second judge and a 12-14B / 27-30B escalation model only after the seeded experiment (§6) shows the tier is viable for at least the Latin/Cyrillic locales.
3. **Pin everything**: model digest (from `/api/tags`), Ollama version (`/api/version`), prompt file hash, `temperature: 0`, fixed `seed`, explicit `num_ctx`, schema-constrained `format`. A verdict without all six is not a receipt.
4. **Run the seeded viability experiment tonight** (§6) before writing any of the Tier 3 sweep tooling. Its output - per-locale recall on known-bad and false-positive rate on known-good - decides whether Tier 3 is blocking, advisory or disabled per locale, exactly as the strategy ADR's Consequences require.
5. **CI never runs Ollama.** CI runs `check:data`, `check:translations` and (once it exists) a receipt verifier over `data/translation_state/`. The Mac produces receipts; CI checks them.

## Consequences

### Positive
- Disk stops being the blocker the same evening; the internal volume stays untouched.
- The first experiment costs one model pull (~5 GB) and under an hour of Mac time, and produces the one number the strategy ADR says it needs before Tier 3 is allowed to queue anything: precision on known-good cells.
- The live `zeichen-132` defect (four locales, stamped as verified) gets a real, non-synthetic test case and, as a side effect, gets found and fixed.
- Everything on the SSD is disposable; nothing that matters (ledger, receipts, prompts) lives there.

### Negative and risks
- **RAM may cap us at 8B.** On a 16 GB Mac, a 7-9B Q4 judge is the practical ceiling with a browser and editor open; 12-14B is possible but tight; 27-30B is out. The strategy ADR's per-locale model policy (`aya-expanse:8b` for hi/ar/uk/tr/ro, `qwen2.5:14b` / `gemma3:12b` elsewhere, `gemma3:27b` escalation) may collapse to "one 8B model for everything" on that machine. That is a quality hit precisely on the locales that need it most; the experiment will show how big.
- **External-bus load latency, and a footgun.** Each model load from the SSD takes seconds to tens of seconds (§3). Ollama's default idle unload (5 minutes) would reload the model from the SSD after every pause; `OLLAMA_KEEP_ALIVE` must be raised for QA sessions. If the SSD is not mounted when Ollama starts, models silently "disappear" from `ollama list`, and a `pull` at that moment writes to a same-named folder on the *internal* disk, after which macOS mounts the real SSD under a different name. Runbook §3 has the guard.
- **Licences are the user's call, not this document's.** Aya Expanse weights are, as far as the author knows, CC-BY-NC-4.0 (non-commercial); Gemma has its own Google terms; Qwen 2.5/3 and Llama 3.x have their own licences with conditions. Internal QA tooling is very likely fine under all of them, but *check each licence page before pulling*, and record the licence next to the digest in the receipt. This ADR does not settle licensing.
- **Model availability and language support are asserted from memory as of 2026-09-05.** Tags, sizes and "supports Hindi/Ukrainian" claims below may be wrong or stale. Verify with `ollama pull` and with the experiment; do not schedule sweeps on the basis of a table in an ADR.
- **Determinism is best-effort.** Same digest + same Ollama version + same options gives repeatable JSON in practice; a different Ollama release, Metal kernel, or a `num_ctx` change can flip a borderline verdict. Receipts record all of it so a non-reproduction is diagnosable, not mysterious.
- **New moving part on the dev machine.** A menu-bar service listening on 11434, an env var, and an SSD that must be plugged in for QA sessions. Modest, but real.

---

## Implementation Notes / Runbook

Everything below is copy-pasteable on the Mac. Nothing in it was run by the author (Linux VM); if a command's output disagrees with this document, the output wins - please paste it into the card.

### §1. Report the machine (do this first - 30 seconds)

```bash
# RAM (GiB) and chip
sysctl -n hw.memsize | awk '{printf "RAM: %.0f GiB\n", $1/1073741824}'
system_profiler SPHardwareDataType | grep -E "Chip|Memory|Model Name"

# Real free space on the internal disk (the Data volume is what you can actually fill)
df -h / /System/Volumes/Data

# External SSD: name, file system, free space
diskutil list external
diskutil info "/Volumes/<SSD-NAME>" | grep -E "File System Personality|Volume Free Space|Case-sensitive"
```

Paste the four outputs into the card. The RAM line decides §2.

### §2. RAM matters more than disk

On Apple Silicon, RAM is *unified memory*: the GPU and CPU share it, and a model's weights must sit in it, whole, to run. Disk decides what you can *store*; RAM decides what you can *run*, and how fast.

Rule of thumb for resident memory of a model in Ollama:

```
resident ≈ weight file size (≈ params × bits/8; Q4 ≈ 0.55-0.6 GB per B params)
         + KV cache (grows with num_ctx; ~0.5-1 GB at num_ctx 4096 on 8B, more on bigger models)
         + ~1-2 GB runtime/Metal overhead
```

macOS itself needs 4-6 GB to stay responsive, and Ollama on macOS will by default only hand the GPU a fraction (roughly two-thirds to three-quarters) of unified memory. So the usable budget for a model is roughly `RAM − 6 GB`, and a model that exceeds it either runs partly on CPU (several times slower) or fails to load.

| RAM | Practical ceiling for this pipeline (Q4) | Notes |
|---|---|---|
| 8 GB | `bge-m3` only; a 3-4B judge (`qwen2.5:3b`, `gemma3:4b`) at best | 7B Q4 (~4.7 GB) will load but swap and crawl with anything else open. Not viable for Tier 3; do Tiers 0-2 here and judge elsewhere (O4). |
| 16 GB | **one 7-9B judge**, comfortably; 12B possible; 14B (~9 GB) only with everything else closed | The most common MacBook configuration. Expect the "one 8B model for all locales" fallback. |
| 24 GB | 12-14B comfortably; two 8B models resident alternately | Two-model agreement on hi/ar/uk becomes practical (sequential, not concurrent). |
| 32 GB | 27B / 30B-A3B (~17-20 GB) possible with little else running | The strategy ADR's escalation tier. Tight; close the browser. |
| 48-64 GB | 27-32B comfortably; 70B Q4 (~40-43 GB) on 64 GB, slowly | Full model policy from the strategy ADR. |
| 96-128 GB | anything in the strategy ADR's table, two models resident at once | - |

Quantisation trade-off, in one line: Q4_K_M (Ollama's default) is the sweet spot; Q8 doubles the memory for a small quality gain we cannot measure on hi/ar anyway; Q2/Q3 shrink further but degrade multilingual and JSON discipline first, which is exactly what we need. Stay on Q4 unless the experiment says otherwise.

Speed, for expectation-setting only: once resident, generation speed is bound by **memory bandwidth**, not by disk and not by "GPU cores". On M-series, an 8B Q4 model produces roughly 15-40 tokens/s depending on chip tier (rough estimate); a 27B model roughly 3× slower. Our judge replies are ~100-200 tokens after a ~1,000-token prompt, hence the strategy ADR's 5-15 s per cell at 8B.

### §3. Install Ollama and put the model store on the SSD

**Install (pick one, not both - both would fight for port 11434):**

```bash
# Option A: the app (menu-bar item, auto-updates, starts at login). Download from https://ollama.com/download
# Option B: Homebrew (CLI + background service)
brew install ollama
brew services start ollama          # or run `ollama serve` in a terminal when you need it
```

Recommendation for this project: **Option B and run `ollama serve` by hand in a terminal during QA sessions**, because that is the only way to set `OLLAMA_MODELS` and `OLLAMA_KEEP_ALIVE` that is completely transparent - you can see the env in the same window. The app reads env vars only via `launchctl setenv` (which does not survive a reboot) or a LaunchAgent plist, which is easy to forget you set.

**Verify:**

```bash
ollama --version
curl -s localhost:11434/api/version        # {"version":"0.x.y"} - record this in every receipt
ollama list                                # models in the store (empty at first)
ollama ps                                  # models currently resident in RAM
```

**Prepare the SSD:** format APFS (Disk Utility → Erase → APFS, *not* exFAT: exFAT works but is slower, has no proper permissions, and ejects less gracefully). Case-insensitive APFS (the default) is fine - Ollama stores blobs under content-addressed names (`sha256-…`) and its manifests are lower-case ASCII, so case sensitivity does not matter. Exclude the volume from Time Machine and Spotlight so 5-20 GB blobs are not indexed or backed up:

```bash
sudo tmutil addexclusion -p /Volumes/<SSD-NAME>/ollama
sudo mdutil -i off /Volumes/<SSD-NAME>
```

**Point Ollama at it, with a guard against the unmounted-disk footgun:**

```bash
# put this in ~/.zshrc (or a small script tmp/ollama-qa.sh in the repo)
export OLLAMA_MODELS=/Volumes/<SSD-NAME>/ollama
export OLLAMA_KEEP_ALIVE=60m         # default 5m would reload the model from the SSD after every pause
export OLLAMA_NUM_PARALLEL=1         # one request at a time; the judge is sequential anyway

# start only if the SSD is really mounted (otherwise a `pull` would create /Volumes/<SSD-NAME> on the internal disk)
if mount | grep -q " /Volumes/<SSD-NAME> "; then
  mkdir -p "$OLLAMA_MODELS" && ollama serve
else
  echo "SSD not mounted - refusing to start Ollama" >&2
fi
```

If you use the app instead: quit it, `launchctl setenv OLLAMA_MODELS /Volumes/<SSD-NAME>/ollama`, `launchctl setenv OLLAMA_KEEP_ALIVE 60m`, relaunch, repeat after every reboot. An alternative that survives reboots is a symlink `~/.ollama/models -> /Volumes/<SSD-NAME>/ollama`; it works, but a dangling symlink when the SSD is out produces confusing "no such file" errors rather than the clear guard message above.

**Moving an existing store** (if you already pulled something internally): stop Ollama, `mv ~/.ollama/models /Volumes/<SSD-NAME>/ollama`, set the env var, start, `ollama list` must show the same models.

**What the external bus changes, precisely:**

- *First use of a model in a session* reads the whole weight file from the SSD into memory. Rough figures: USB 3.x SSD ≈ 0.4-1 GB/s, Thunderbolt/USB4 NVMe ≈ 2-3 GB/s, internal ≈ 3-7 GB/s. A 5 GB model therefore takes roughly 5-12 s to load over USB 3, 2-3 s over Thunderbolt, 1-2 s internal; a 17-20 GB model roughly 20-50 s / 7-10 s / 3-6 s. (Estimates.)
- *Token throughput once resident* is unaffected by the SSD: the weights are in unified memory and the bottleneck is memory bandwidth (§2). The SSD only matters again on the next load.
- Hence `OLLAMA_KEEP_ALIVE=60m` (or `-1` for "never unload" during a sweep): the cost is paid once per session, not once per idle gap.
- *Unplugging mid-run:* Ollama's runner memory-maps the weight file. On a disconnect, pages not yet touched fault and the runner process dies; the in-flight request errors, subsequent requests fail with "model not found" until the disk is back and `ollama serve` is restarted. Nothing is corrupted (the store is read-only during inference; the blobs are content-addressed and verified on pull), and the judge cache/ledger live on the internal disk, so the only loss is the cell being judged at that instant - the cache-by-hash design (§7) resumes from there. Do not eject the SSD while `ollama ps` shows a model resident.

### §4. Pull models and run a one-shot prompt

Pull the minimum first; each `pull` prints the size, `ollama list` shows it afterwards:

```bash
ollama pull bge-m3                    # embedding, ~1.2 GB
ollama pull qwen2.5:7b-instruct       # judge candidate 1, ~4.7 GB, strong JSON discipline
# after the experiment, if RAM allows and the licence is acceptable to you:
# ollama pull aya-expanse:8b          # judge candidate 2, ~5 GB, best small-model coverage of hi/ar/uk/ro (CC-BY-NC - check)
# ollama pull gemma3:12b              # ~8 GB, 24 GB+ Mac
# ollama pull gemma3:27b              # ~17 GB, 32 GB+ Mac
ollama list
du -sh "$OLLAMA_MODELS"
```

One-shot from the shell:

```bash
ollama run qwen2.5:7b-instruct "Antworte nur mit JSON: {\"lang\": <ISO-Code dieses Satzes>}. Satz: 'Sie müssen hier geradeaus oder nach rechts weiterfahren.'"
```

The same via the HTTP API (this is what the scripts use; `stream:false` returns one JSON object):

```bash
curl -s localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b-instruct",
  "stream": false,
  "options": {"temperature": 0, "seed": 42, "num_ctx": 4096, "num_predict": 300},
  "format": {"type":"object","required":["same_meaning","evidence"],
             "properties":{"same_meaning":{"type":"boolean"},"evidence":{"type":"string","maxLength":200}}},
  "messages": [{"role":"user","content":
    "German: \"Sie müssen hier geradeaus oder nach rechts weiterfahren.\"\nPolish: \"Musisz tutaj jechać dalej na wprost lub w prawo.\"\nDo they state the same rule? Answer only with JSON."}]
}' | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['message']['content']); print('eval_count', r.get('eval_count'), 'eval_ns', r.get('eval_duration'))"
```

Embeddings:

```bash
curl -s localhost:11434/api/embed -d '{"model":"bge-m3","input":["Was schreibt dieses Verkehrszeichen vor?","Co nakazuje ten znak drogowy?"]}' \
  | python3 -c "import sys,json; e=json.load(sys.stdin)['embeddings']; import math; d=sum(a*b for a,b in zip(*e)); n=lambda v: math.sqrt(sum(x*x for x in v)); print('cosine', d/(n(e[0])*n(e[1])))"
```

Get the digest you will pin (full sha256, not the 12-char prefix `ollama list` shows):

```bash
curl -s localhost:11434/api/tags | python3 -c "import sys,json; [print(m['name'], m['digest'], round(m['size']/1e9,2),'GB') for m in json.load(sys.stdin)['models']]"
```

### §5. Model choice for this project's 13 locales

Locales: `de en es fr it pl ru uk tr ar hi zh` (+ `ro` in compliance modules). Honest picture, as far as the author knows on 2026-09-05 - **verify each claim against the model's own card before relying on it, and against the experiment (§6) before trusting it:**

| Locale group | Any modern 7-14B instruct model | Where it is weak |
|---|---|---|
| en es fr it | good | - |
| pl ru zh tr | good on Qwen 2.5/3, Gemma 3, Mistral Nemo; Llama 3.1 does **not** list them | pl false friends are subtle for everyone |
| uk | Qwen 2.5 does not officially list it; Gemma 3 and Aya Expanse do | models drift into Russian; the `іїєґ` file-level heuristic in the strategy ADR is the cheap guard |
| ar | Qwen 2.5, Gemma 3, Aya, Mistral Nemo list it | polarity and numerals (Eastern vs Western digits in the same cell) |
| hi | Llama 3.1, Gemma 3, Aya list it; Qwen 2.5 does not officially | register mixing (Hindi/Urdu), transliterated German sign names |
| ro | Aya Expanse lists it; Gemma 3 claims broad coverage; Qwen 2.5 does not officially | least-tested locale in this repo; treat every verdict as advisory until measured |

Recommended set, in pull order:

1. **`bge-m3`** - Tier 2; explicitly multilingual across all 13 locales. No known licence issue (MIT, to the author's knowledge - check).
2. **`qwen2.5:7b-instruct`** (or `qwen3:8b` if pulling fresh) - Tier 3 default for es/fr/it/pl/ru/tr/zh. Best JSON discipline of the small models; Apache-2.0 for the 7B (check the tag you pull).
3. **`aya-expanse:8b`** - Tier 3 for hi/ar/uk/ro, and second opinion for the two-model agreement rule. The only small model whose official list covers all 13 locales, as far as the author can tell. **CC-BY-NC**: internal QA tooling only, and that is the user's call.
4. **`gemma3:12b` / `gemma3:27b`** - escalation model if RAM allows (§2). Claims 140 languages; the 27B is the best local option for hi/ar/uk if the 8Bs fail the experiment. Google's Gemma terms apply - check.

The author is **not** certain that every tag above exists under exactly that name in the Ollama library on the day you pull; `ollama pull` is the check. If a tag is missing, `ollama search <name>` (recent Ollama) or the library website lists the current one.

### §6. Tonight's experiment: is the judge viable at all?

One evening, one model, one number per locale. **Precision on the known-good half decides viability** - a judge that flags everything is worthless, and the strategy ADR already sets the bar: seeded-set precision below ~0.7 makes the tier advisory-only for that locale.

**Known-bad set** (all real, all from this repo; ~24-30 cells):

| id | locales | defect | where the bad text lives today |
|---|---|---|---|
| `zeichen-132` | ar, pl, tr, uk | stem + correct option describe "Mofa frei" instead of "Fußgänger" 1010-53 (**live in the master now**) | `data/pilot_questions.json` as is |
| `zeichen-68` | ar (+ es, fr, pl, hi if recoverable from git history - the user can `git log -p`, the author cannot) | pre-fix text describes an obstacle-passing sign instead of Zeichen 214 | `tmp/apply_ar_fixes.py` prints the old ar text; other locales from history |
| `zeichen-04` | ar, pl, hi (pre-fix) | sign number 133 instead of 136 | as above - or synthesise by replacing 136→133 in the current translation |
| synthetic, 2-3 per locale | all 11 | (a) replace the target cell with the target cell of a *different* question in the same topic (the `zeichen-68` class); (b) swap the target's correct option text with a distractor's (answer-key breakage); (c) negate the target correct option (inversion, hand-written per locale); (d) flip one number in the stem | generated deterministically from known-good cells by the script |
| `datenschutz-*` (9 ids) | any | the historical `high_stakes` leak - **Tier 1 catches this exactly**; include one or two only to confirm the judge is not needed for it | history / synthesise by appending " - daher als high_stakes markiert." |

**Known-good set** (equal size, same locales): the *fixed* `zeichen-68` and `zeichen-04` in all locales; a random sample of `high_stakes: true` fuehrerschein cells; all of them stamped, and at least the es/fr/en ones spot-read by a human. Label them "presumed good" - if the judge flags one and a human agrees, it moves to the bad set and the count is still useful.

**Script shape** - `scripts/i18n_qa/judge_seed_eval.py` (the strategy ADR's §1 layout; stdlib only; reads the master via the same `load_master`/`source_hash` helpers as `translation_ledger.py`):

```
inputs :  scripts/i18n_qa/seed/known_bad.json   [{module,id,locale,defect,target_cell_override?}]
          scripts/i18n_qa/seed/known_good.json  [{module,id,locale}]
          scripts/i18n_qa/prompts/judge_v1.md   (rubric from the strategy ADR §5; sha256 recorded)
          --model TAG  --ollama http://localhost:11434
per cell: build prompt(de cell, target cell, core.correct) -> POST /api/chat
          options {temperature:0, seed:42, num_ctx:4096, num_predict:300}, format = strategy ADR §5 schema
          derive verdict from the booleans in code (never trust "verdict" field)
          append {module,id,locale,expected,got,confidence,evidence,model_digest,ollama_version,prompt_sha,de_sha,target_sha,ms}
            to tmp/judge_seed_log.jsonl
output :  tmp/judge_seed_report.md - per locale: n_bad, caught (recall), n_good, false_positives (FP rate),
          median seconds per cell; and the same table for confidence >= 0.7 only
```

Run:

```bash
python3 scripts/i18n_qa/judge_seed_eval.py --model qwen2.5:7b-instruct
python3 scripts/i18n_qa/judge_seed_eval.py --model aya-expanse:8b        # if pulled
cat tmp/judge_seed_report.md
```

At ~60 cells × 5-15 s that is 5-15 minutes per model (estimate). Read the report as: **FP rate on known-good ≤ ~10 % *and* recall on known-bad ≥ ~70 % per locale → viable (blocking-capable)**; FP ≤ ~10 % but low recall → advisory; FP > ~20 % → disabled for that locale regardless of recall. Record the table in the PR/card and in `scripts/i18n_qa/thresholds.json` once that file exists. Then fix `zeichen-132` in ar/pl/tr/uk and re-stamp those four cells - that is the first real output of the tier.

### §7. Determinism and receipts

A verdict is a receipt only if it records all of:

| field | how to get it |
|---|---|
| `model` and `model_digest` | `/api/tags` → `digest` (full sha256), not the tag name - tags move |
| `ollama_version` | `/api/version` |
| `prompt_sha` | `sha256(scripts/i18n_qa/prompts/judge_vN.md)` |
| `options` | `{"temperature":0,"seed":42,"num_ctx":4096,"num_predict":300}` verbatim - `num_ctx` must be explicit; Ollama's default context is small and silently truncates long bilingual prompts |
| `format` | the JSON schema (its sha256 is enough) |
| `de_sha`, `target_sha` | `translation_ledger.source_hash()` for the German; the same normalisation applied to the target cell |
| `at` | ISO-8601 UTC |

Cache key = `sha256(de_sha + target_sha + model_digest + prompt_sha + options_sha)`. Verdicts go to `data/translation_state/verdicts/<module>.jsonl` (committed; one line per receipt, append-only) - a *separate* file from the ledger, so `translation_ledger.py` stays dumb and its schema unchanged. Full prompt and raw reply go to `tmp/judge_log.jsonl` (not committed) for audit.

Why the ledger makes re-judging cheap: Tier 0 already computes `de_sha` per cell and tells you which cells changed; a sweep runner only needs to look up `(de_sha, target_sha)` against the receipt file and skip hits. A one-word German edit re-judges 11 cells, not 5,841.

Reproduction test (do once): run the same 20 cells twice with the same receipt fields; every JSON must be byte-identical. If it is not, the receipt tells you which of the six fields differed.

### §8. Runtime and cost reality (estimates, not measurements)

| job | cells | 8B Q4, 5-15 s/cell | 27B Q4, ~15-40 s/cell |
|---|---|---|---|
| seeded experiment (§6) | ~60 | 5-15 min | 15-40 min |
| all `high_stakes` fuehrerschein × 11 locales | 82 × 11 = 902 | 1.3-4 h | 4-10 h |
| the 3,284 untracked cells | 3,284 | 4.5-14 h (one to two nights) | 14-36 h |
| full fuehrerschein | 531 × 11 = 5,841 | 8-25 h | 1-3 days |
| Tier 2 embedding sweep of everything (~16k cells) | ~16,400 | minutes | - |

Electricity and wear are the only costs. Measure `eval_duration` from the first 20 calls and replace this table with real numbers before scheduling a night run.

### §9. Where it must NOT run, and what CI does instead

GitHub-hosted runners have no GPU and 7-16 GB RAM; an 8B judge there is minutes per cell or an out-of-memory. `bge-m3` on CPU would work but is not worth a runner-side Ollama install yet. CI therefore runs:

```
npm run check:data            # scripts/check_data_integrity.py  (Tier 1: structure + leaked tokens)
npm run check:translations    # scripts/translation_ledger.py check  (Tier 0: stale / untracked → exit 1)
python3 scripts/i18n_qa/verify_receipts.py --require changed,high_stakes   # to be written: every required cell has a receipt whose de_sha/target_sha match and whose model_digest+prompt_sha are on the allow-list
```

The Mac produces the receipts and they are committed with the content change. CI checks the receipts, not the model. Until `verify_receipts.py` exists, the first two lines are the whole CI story - and `check:translations` is red today until the 3,284 untracked cells are either judged or consciously stamped.

### §10. Tonight, in order

1. §1 - paste RAM / disk / SSD info into the card.
2. §3 - install, format SSD APFS, `OLLAMA_MODELS` on the SSD, `ollama serve` with the guard, `curl /api/version`.
3. §4 - `ollama pull bge-m3`, `ollama pull qwen2.5:7b-instruct`, one-shot prompt works, digest captured.
4. §6 - build the two seed files (start with the 4 live `zeichen-132` cells and the fixed `zeichen-68`/`zeichen-04` as the good half; add synthetic cases as time allows), run the eval, read the FP rate.
5. Decide per locale; fix `zeichen-132`; stamp those four; only then think about a second model.
