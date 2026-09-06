# data-rules.md — how Zettacard content is stored, authored, verified and published

This file is identical in `Zettacard/` and `zettacard-kb/`. If you change it in
one repo, copy it to the other in the same change. It is the rulebook both repos
answer to; `AGENTS.md` points here rather than restating it.

Last changed 2026-09-06.

---

## 1. Which repo is the master

**The two repos own different things, and each is authoritative for its own
(PO, 2026-09-06):**

| Repo | Authoritative for | Not authoritative for |
|---|---|---|
| **`zettacard-kb`** | **content** — questions, explanations, every locale, provenance, defects, rights | app code |
| **`Zettacard`** | **app code** — `app.js`, `styles.css`, `service-worker.js`, HTML, assets, `build_modules.py`, deploy config | content |

Content flows one way, app code the other. `src/export_to_zettacard.py` is the
content direction: it writes the master files in `Zettacard/data/` that
`build_modules.py` already expects, so nothing in the app repo has to change to
consume it. Publishing happens from `Zettacard`, as it always has.

This reverses the arrangement that held until 2026-09-06, when `zettacard-kb` was
a read-only citation index and `Zettacard/data/*_pilot.json` held the masters.
**Do not follow older instructions that say otherwise**, in either repo's history,
in an older ADR, or in a stale README.

The pipeline, in one line:

```
zettacard-kb (authored, reviewed, versioned)  ->  Zettacard/data/  ->  Zettacard/app/data/  ->  zettacard.de
```

Everything downstream of the first arrow is **generated output**. Consequences, in
the order they will bite you:

1. **A content fix goes into `zettacard-kb`.** Never into `Zettacard/data/`, never
   into `Zettacard/app/data/`. Both are regenerated; a fix applied there is
   overwritten on the next build and is, by definition, lost work.
2. **Nothing is published that has not passed the review gate** (§4).
3. **`app/data/**` is disposable and always has been** — `build_modules.py` calls
   `shutil.rmtree()` on each module's `locales/` before regenerating it, so a
   locale that exists only as generated output, and is not listed in that script's
   `fs_locales`/`compliance_locales` arrays, is deleted with nothing to rebuild it
   from. Romanian was nearly lost this way. `Zettacard/data/` is now disposable in
   the same sense. The durable copy is in the KB.

---

## 2. The reference architecture: HugoFara/boating-licence

**It is a reference for how someone else stores this kind of data. It is not a
specification we conform to.** We define our own dataset rules — they are in § 3a
below. Read his repo to learn from it, then decide deliberately what to take and
what to leave; adopting a pattern because he has it is as wrong as ignoring one
because he has it.

**Read the actual repository before designing any part of the content pipeline** —
not this summary, and not a README's paraphrase of it. Clone it and read, at
minimum:

| File | What to take from it |
|---|---|
| `src/sources.py` | the approved-source registry and its per-source licence note |
| `src/staleness.py` | fingerprinting, the lockfile, and graded drift |
| `src/questions/schema.py` | the review gate and the export gate |
| `src/countries/base.py` | `source` / `url` / `as_of` / `volatile` on every fact |
| `run.py` | the stage vocabulary: build → questions → draft → review → web |

The summary below tells you what to look for. It does not save you the reading.

What that repo actually does, and what we are copying:

- **The repo is the master and generates the published site.** Its `web/` tree is
  built output — committed, but derived. There is no separate "real" content
  living somewhere else.
- **An approved source registry.** Every upstream source is a declared entry with
  a stable id, a canonical URL, a `kind`, and a **licence note carried into every
  unit derived from it**. Nothing is ingested that is not registered.
- **A blessed lockfile.** `data/sources.lock.json` pins a fingerprint per source:
  the source's own version marker (a consolidation date, a "Stand", a catalogue
  edition) **plus a SHA-256 of the fetched bytes** — because a digest catches
  editorial changes that a version string never bumps.
- **Drift is graded, and the grades have teeth.** Law-grade sources (primary
  legislation, official catalogues) drifting is **significant**: a derived question
  may now be wrong, and the check exits non-zero. Reference-grade sources
  (encyclopaedic prose) are **advisory**: reported, never fatal. Copy the
  asymmetry — do not grade everything the same.
- **Every fact carries `source`, `url` and `as_of`** — the ISO date the fact was
  actually verified against that URL — and is authored from that source,
  **never from memory**. Facts known to drift (fees, age limits, validity periods)
  are marked `volatile` so they are re-verified first.
- **Honest defaults.** Difficulty defaults to `unrated`, not `medium`. Source grade
  defaults to `unverified`, not `law`. A field is populated only once something
  actually determined it.

---

## 3. Source registry and grading

Every source a question is derived from is registered, with a licence note, and
graded:

| Grade | Meaning | Evidence required | Drift behaviour |
|---|---|---|---|
| `law` | Primary legislation or an official catalogue, fetched and hashed | source URL **and** fetched, hashed text | **fatal** — derived questions may now be wrong; the check exits non-zero |
| `reference` | Authoritative secondary source (official guidance, encyclopaedic prose) | source URL **and** fetched, hashed text | advisory — reported, never fatal |
| `unverified` | No source URL mapped, or mapped but never fetched | none; this is the default | n/a |

A URL alone never earns `law` or `reference`. The whole point of the grade is that
upstream change becomes *detectable*, and that requires stored bytes to compare
against. The lockfile is `data/citations.lock.json` in `zettacard-kb`; it grows a
per-citation source URL and fetched-text hash rather than being replaced.

## 3a. Our dataset rules

These are ours. Where they differ from HugoFara/boating-licence the difference is
deliberate and the reason is stated.

### What we take from him, and why

| His pattern | We | Why |
|---|---|---|
| Lockfile pins each source's own version marker **plus** a SHA-256 of fetched bytes | **adopt** | a digest catches editorial change a version string never bumps |
| `legal_version` is heterogeneous and **not normalised** (a BGBl amendment string, an ISO date, an HTTP `Last-Modified`, a corpus pin) | **adopt** | normalising it destroys information; the digest does the real work |
| Graded drift: law-grade loud, reference-grade advisory | **adopt** | see § 3 |
| `source` / `url` / `as_of` on every fact, authored from the source not from memory | **adopt** | this is the discipline, not the format |
| Honest defaults — `unrated`, `unverified`, `pending` | **adopt** | see ADR-0003 |
| Verdicts as **committed data files**, separate from the content | **adopt, our own layout** | a verdict in its own file is a reviewable git object; a verdict inside the content line can be rewritten by a content edit. Ours live at `content/<module>/verdicts/<locale>.jsonl`, append-only |
| Distinguishes languages with officially-published law to ground against | **adopt as a separate axis** — see below | |
| **Export gate: only approved content publishes** | **reject** | correct for a curated product; wrong for a free openly-licensed study aid with 19,391 unreviewed cells. See ADR-0003 — for us verification is a label, not a wall |

### Two axes, not one: exam tier and groundedness

Our locale `tier` answers *where does the learner sit the exam*. His
`GROUNDED_LANGS` answers *what could the author check the text against*. They are
different questions and they disagree in both directions:

| | grounded | ungrounded |
|---|---|---|
| **official exam language** | e.g. German source, French where official texts exist | **Arabic** — a candidate may sit the Theorieprüfung in it, but there is no official Arabic StVO to check against. The worst cell in the matrix |
| **study aid** | — | English, Bavarian, Persian, Japanese … |

So a unit carries **both**: `tier` (from § 7) and `grounded` (derived from the
source registry — a locale is grounded for a module when at least one registered
source for that module exists officially in that language).

This is not bookkeeping. It changes the reviewer's brief: on a grounded locale a
reviewer can be handed the official text and told to check against it; on an
ungrounded locale they are doing translation revision and **must not** be asked to
"verify against the law", because there is nothing to verify against. The card
label must say which kind of review happened, or it overstates what was done.

### Citations: the gradable unit is the source, not the anchor

A citation is a **source id plus an anchor into it**. The anchor syntax is
per-source and is not normalised:

| Source kind | Anchor example |
|---|---|
| statute | `§ 8 Abs. 1 StVO`, `Art. 6 DSGVO` |
| official catalogue | `ELWIS Fragenkatalog SBF Binnen, Stand 01.08.2023 (Frage 137)` |

Grading applies to the **source**, once, on fetched and hashed bytes. Anchors are
validated by a per-source rule that checks the anchor points somewhere inside the
graded source. This is why the 515 Sportboot questions are not 515 grading jobs:
they are one source registration plus an anchor check.

Consequence worth stating plainly: our current data has 515 distinct "citations"
for 515 questions because the anchor was baked into the citation string. That is a
shape defect, not 515 sources.

### Inherited data is unverified data

`sportboot_binnen` and `sportboot_see` (515 questions) were ingested through
HugoFara's pipeline and **have never been checked against the primary ELWIS PDF by
us**. His lockfile says the catalogue was still at edition 2023-08 as of his bless
on 2026-05-30, and our data is pinned to the same edition. That is evidence that
*the catalogue* had not moved. It is **not** evidence that our 515 cells match it,
nor that it has not moved since, nor that his fetcher read the right document.

Until our own lockfile holds our own digest of bytes we fetched, those citations
stay `unverified`. Re-verification is a **bytes-against-bytes diff** — source work,
not review work — and it is the cheapest possible proof that our source registry
functions, so it goes first. The *explanations* on those modules are ours, ~90
words each, with no catalogue to diff against: those are review work, in German
first, because under § 5 Abs. 2 UrhG they are the only part of those modules where
we can be wrong in our own words.

### Licence policy: which modules get which terms

**Standing positioning line, to be carried wherever the product is described:**

> Zettacard ist kein amtlicher Prüfungssimulator. Original-Lerninhalte,
> CC BY-NC-SA 4.0.

That is the default. There are two deliberate exceptions: ND for compliance, and
per-source non-NC sub-content (below).

| Content | Terms | Why |
|---|---|---|
| Exam-prep modules (Führerschein, Motorrad, LKW, Bus, Angelschein, Sportboot, AEVO, CKA, the Gewerbe/Vermittler modules) | **CC BY-NC-SA 4.0** | original learning content; share-alike keeps derivatives open |
| **Workplace-compliance modules** | **CC BY-NC-ND 4.0** | *NoDerivatives.* A compliance course is evidence that a duty was discharged. A modified derivative circulating under the same name, with an altered answer key or a softened obligation, is a liability — for the learner relying on it and for us. ND removes the permission to distribute modified versions. |
| Sportboot question/option TEXT | not ours to license — § 5 Abs. 2 UrhG (see below) | verbatim official catalogue text |

The compliance set, explicitly: `datenschutz`, `arbeitssicherheit`,
`it_sicherheit`, `ki_act`, `nis2`, `dora` and every `dora_*` variant,
`kartellrecht`, `kyc_aml`, `hinweisgeberschutz`, `fadp_ch`, `cra_supply_chain`,
`lksg`. A new module is compliance if it trains a legal obligation someone must be
able to show they met — not merely because it cites a statute; the Führerschein
modules cite the StVO throughout and are not compliance.

Note the interaction: SA and ND are **incompatible**. Content cannot be remixed
across the two sets and redistributed. Keep the boundary at the module.

**Status as of 2026-09-06: this is the policy, not yet the data.** The compliance
modules' `meta.license` fields still read `CC BY-NC-SA 4.0`, in both the masters
and everything generated from them, and `app/legal/quellen.html` does not state it.
Changing them is a content change and must go through the normal path — it has not
been done.

### Sub-content may carry its own, non-NC terms (PO decision, 2026-09-06)

**The module licence is the licence of what we wrote. It is not a claim over
material we incorporated under someone else's terms.** Where a module includes
sub-content that arrives under a licence of its own — including a licence with no
NC clause, or one whose share-alike we cannot satisfy at module level — that
sub-content keeps its own terms, is **marked at the point of use**, and gets a row
in `app/legal/quellen.html` linking to the source and naming its licence.

This is what makes the THW pack possible. THWiki text is **CC BY-SA 4.0**
(`https://thwiki.org/t=THWiki:Urheberrecht`), and BY-SA share-alike cannot be
satisfied by redistributing under BY-NC-SA, because NC is an added restriction.
Rather than relicense a whole module or refuse the source, the rule is:

- The **module** stays CC BY-NC-SA 4.0 for the parts we authored.
- Any **incorporated BY-SA passage** is attributed and stays BY-SA, and is marked
  as such where it appears. It is a quoted, attributed component, not something we
  sublicense.
- The **register carries the row**: source, licence, URL, and what was taken.
- If a module ever reaches the point where the BY-SA material is no longer a
  component but the substance of it, that module is BY-SA, not BY-NC-SA. Say so
  rather than let the ratio drift.

Three things this decision does **not** change:

1. **§ 11 constraint 1 still stands.** Third-party exam-prep catalogues —
   thw-trainer.de, thw-theorie.de, any Fahrschul-Verlag — remain off limits
   whatever their licence, because the objection there is not the licence.
2. **Per-image licences are per image.** THWiki images are individually tagged
   `cc-by-nc-sa 3.0`, plain `copyright`, `copyright:thwhs`, `thw` or `thw-pd`
   (`https://thwiki.org/t=THWiki:Hilfe_zu_Bildern`). There is no wiki-wide image
   licence, so no image may be used on the strength of the text licence.
3. **Compliance modules are still ND.** ND and BY-SA cannot be mixed at all, so a
   compliance module takes no BY-SA sub-content. This exemption is for
   `exam_prep` and `fun_translation` only.

The THW pack is therefore authored from Dienstvorschriften, UVV, the THW-Gesetz
and any official curriculum whose terms permit it (PO decision, 2026-09-06), with
THWiki available as an attributed, marked component where it genuinely adds
something we cannot get from the primary source.

### The public source register: `app/legal/quellen.html`

Zettacard already has a per-source register, published at
`https://zettacard.de/legal/quellen` (`Zettacard/app/legal/quellen.html`). It is
the public, human-facing answer to "where did this come from and under what
terms", organised by jurisdiction, with a `Body / Licence / Note` row per source.

Two facts about it as of 2026-09-06:

- **It is the register of record, and every new source must be added to it.**
  Recording provenance only in a module's JSON `meta` is not enough; licensing
  provenance has to stay visible in one place.
- **It is hand-maintained HTML, and most rows state no licence at all.** Rows for
  BaFin, BSI, DGUV, BIBB, IHK/HWK, Fedlex (CH), EDÖB and Wikimedia Commons carry a
  note but no licence string. That is the same `unverified` condition as an
  ungraded citation, and it should be treated as a gap rather than as consent.

The KB's source registry (ADR-0001 follow-up 5) is the machine-readable version of
this page and must not become a second, diverging copy: the page should eventually
be **generated from** the registry, the way boating-licence generates its docs.
Until then, a change to one is a change to both.

Rows that already carry real terms, and the constraints they impose:

| Source | Terms as published | What it constrains |
|---|---|---|
| ELWIS / WSV / BMDV Fragenkatalog | § 5 Abs. 2 UrhG amtliches Werk — *wortgleich zu zitieren* | the Sportboot question/option text may be reused **unmodified, with citation to www.elwis.de**. Editing that text steps outside the permission — see below |
| Wikimedia Commons sign SVGs | gemeinfrei, § 5 Abs. 1 UrhG (amtliches Werk mit regelndem Inhalt) | free reuse; a faithful redraw carries no derivative-work risk |
| Légifrance / DILA LEGI | Licence Ouverte / Etalab 2.0, attribution required | planned boating modules must attribute |
| COLREG 1972 | public domain, 17 USC § 105 | free reuse |
| THWiki (thwiki.org), **text** | CC BY-SA 4.0 | usable as marked, attributed sub-content in `exam_prep` / `fun_translation` modules only; never in a compliance (ND) module; attribution and a link are mandatory |
| THWiki (thwiki.org), **images** | per image: `cc-by-nc-sa 3.0`, `copyright`, `copyright:thwhs`, `thw`, `thw-pd` | no wiki-wide image licence — each image must be checked individually before use |

### Amtliches Werk: what is ours in the Sportboot modules, and what is not

`sportboot_binnen` and `sportboot_see` (515 questions) carry **verbatim official
WSV/BMDV ELWIS Fragenkatalog** German text. Split the module in three, because the
three parts have different owners:

| Part | Whose | Terms |
|---|---|---|
| German question and option **text** | **not ours** | § 5 Abs. 2 UrhG amtliches Werk — free reuse, but *wortgleich* and with citation to www.elwis.de |
| **Translations** of that text | **ours** | our own work product |
| **Explanations** and the data structuring | **ours** | CC BY-NC-SA 4.0 |

So the module-level licence line must not read as if we license the German text.
We do not own it and cannot license it. What we license in those modules is the
translations, the explanations and the structuring.

**Consequences for the "fix it in the KB" rule.** The German question and option
text of those two modules is the one place the general rule does not apply:
**do not hand-edit it.** If the catalogue text is wrong, the fix is to re-ingest
the current official catalogue. Fixes to explanations and translations are normal
KB work.

**Is translating it permitted? Yes — checked against the statute, 2026-09-06.**
§ 5 Abs. 2 UrhG applies "§ 62 Abs. 1 **bis 3** und § 63 Abs. 1 und 2 entsprechend",
and § 62 Abs. 2 expressly permits translations: *"Zulässig sind Übersetzungen und
solche Änderungen des Werkes, die einen Auszug … darstellen, soweit sie für die
Benutzung erforderlich sind."* So the Änderungsverbot does **not** bar translating
an amtliches Werk. The Quellenangabe duty (§ 63) still applies: cite www.elwis.de.
An earlier version of this file flagged this as unresolved; it is resolved.

**Can we then license our translations CC BY-NC-SA? Genuinely unsettled — do not
assert either way.** Three separable layers, and conflating them is the error:

| Layer | Status |
|---|---|
| the German ELWIS text | **gemeinfrei** — § 5 Abs. 2, no copyright, but Änderungsverbot + Quellenangabe apply |
| our translations of it | § 3 UrhG protects "Übersetzungen … die **persönliche geistige Schöpfungen des Bearbeiters** sind … wie selbständige Werke". Protection therefore turns on whether our translation clears Schöpfungshöhe. For short, factual, single-correct-answer catalogue items that is **marginal at best**, item by item |
| our explanations, and the collection | the explanations are plainly ours. The *collection* may separately attract § 4 (Datenbankwerk) or § 87a ff. (sui generis database right) regardless of any single item |

"The source is gemeinfrei, therefore the translation is gemeinfrei" does not follow
— § 3 exists precisely for that case. But neither does "we translated it, therefore
we own it": a faithful rendering of a factual sentence may simply not be a
protectable Schöpfung. **Until a qualified lawyer rules on Schöpfungshöhe here,
do not claim CC BY-NC-SA over the Sportboot question and option text in any
language, and do not claim it is public domain either.** Publish the ELWIS
citation, license the explanations, and say nothing more.

This file is not legal advice. It records the terms as the project has published
them and the questions it has not yet answered.

### Two modules currently have no licence at all

`cka` (131 questions, authored, live) and `dora_audit_readiness` (draft) have
`license: null` in their `rights` block. That is a gap, not a permission. Set terms
before redistributing either.

Licence notes are recorded **per module and per source, never normalised**.
Zettacard's own content is mostly CC BY-NC-SA 4.0, but the Sportboot modules credit
an official ELWIS Fragenkatalog and MIT-licensed tooling, and the planned
France/Switzerland boating modules ship CC BY-SA 4.0. Silently relabelling any of
these to the house default is a licensing defect, not a tidy-up.

---

## 3b. Module kinds

Every module carries `module_kind`, because licence policy, review priority and
picker placement all key off it — and off it, not off the module's name.

| `module_kind` | What it is | Licence | Notes |
|---|---|---|---|
| `exam_prep` | German exam preparation (Führerschein, Angelschein, Sportboot, AEVO, CKA, the Gewerbe/Vermittler modules) | CC BY-NC-SA 4.0 | the default |
| `compliance` | workplace-compliance training someone must be able to show they completed | **CC BY-NC-ND 4.0** | see § 3 |
| `fun_translation` | another country's road rules, in German and English, as a curiosity and comparison object | CC BY-NC-SA 4.0 | see `docs/fun-translations-world-licences.md` |

### `fun_translation` — the rules that are specific to it

- **`de` and `en` only.** These modules are outside the 15-locale set and must
  never be counted as locale-coverage gaps.
- **Authored from the primary law of that jurisdiction, never from its driver
  handbook.** A handbook is a compiled authored work; translating one is a
  derivative of the whole thing, which is precisely what § 11 constraint 1
  forbids us from doing with the Fragenkatalog. A handbook may be read for
  *coverage* — which topics the exam asks about — and never for text.
- Note that "US government works are public domain" is **17 USC § 105, federal
  works only**. A US state's works are not automatically public domain. The same
  caution applies to every jurisdiction until its own terms have been fetched and
  recorded.
- **Identification is mandatory**, in both locales, on the module intro and
  before the first question: the module teaches another country's rules, is not a
  German licence, is not that country's official exam, and confers nothing. A
  `fun_translation` module never sits in a picker beside the German licence
  modules without that label visible.
- `legal_basis` cites that jurisdiction's law in that jurisdiction's own citation
  style, untranslated.
- Tag each card with its rule family (priority, speed, overtaking, parking,
  alcohol, lighting, turning). These modules are the corpus for the universal
  differential rulebook the PO has scheduled for Easter 2027 or later; tagging as
  we go means it can be generated rather than re-authored.

## 4. The review gate, and the export gate downstream of it

Every content unit carries `review_status`:

| Status | Set by | Export-eligible |
|---|---|---|
| `pending` | the default for anything newly authored or drafted | **no** |
| `auto_approved` | a deterministic generator, where the generator itself is the guarantee | yes |
| `approved` | a human who reviewed the unit | yes |
| `rejected` | a human who reviewed the unit and refused it | **no** |

**Only `auto_approved` and `approved` reach the published build.** Everything else
is invisible to it. This is the piece Zettacard has never had, and it is the point:
*verified* must be a state a human moved a card into, not an adjective someone put
in a commit message.

New content lands `pending`. LLM-drafted content lands `pending` — always, with no
exception for "it looks fine". A generator may only claim `auto_approved` when the
output is a deterministic function of already-approved input.

---

## 5. What "verified" means — three different things

Conflating these is the main way this goes wrong.

| Question | Field | Moves how |
|---|---|---|
| Has a human reviewed this card? | `review_status` | only by a human approving it, or a deterministic generator declaring `auto_approved` |
| Is the cited law still what it was? | source grade + lockfile digest | only by re-fetching and re-hashing the source |
| Is this translation current for its German? | `source_hash` | automatically — the moment the German cell changes |

None of the three implies the others. A card can be human-approved and cite a
statute amended last week. Never report one as if it covered another.

---

## 6. Hashing, and the one recipe that must not drift

`source_hash` is SHA-256 over a canonical JSON payload of the **German** cell only:
`{question, options, explanation, correct}`, `sort_keys=True`, `ensure_ascii=False`.

`correct` is included deliberately: if the answer key moves, an existing
translation may make the wrong option read as right.

Two implementations compute it — `zettacard-kb/src/ingest_content.py` and
`Zettacard/scripts/translation_ledger.py` — and they must agree byte for byte. It
is the join key between the repos and the staleness trigger for translations *and*
for TTS media. If the recipes diverge, both keep working and quietly disagree about
which content is current, which is the exact failure both systems exist to prevent.
`zettacard-kb/tests/test_hash_parity.py` is what stops that; run it before shipping
anything that touches hashing.

Per-locale hashes cover `{question, options, explanation}` for that locale.

---

## 7. Locale tiers — a legal distinction, not a label

For the German driving-theory exam, **twelve languages are official exam
languages**: `en, fr, el, it, pl, pt, ro, ru, hr, es, tr` and Modern Standard
Arabic. A candidate may sit the real Theorieprüfung in them, so our translation is
a rehearsal of the actual exam paper and must match German exam register. Verified
against ADAC and TÜV/DEKRA sources, 2026-09-05.

Every other locale (Bavarian, Persian, Hebrew, Levantine Arabic, Japanese, Korean,
…) is a **study aid**: the learner still sits the exam in German, and may be shown
the German term alongside the translation.

Non-driving modules have no foreign-language state exam, so their locales are
graded plainly as `translation`. German is `canonical` everywhere.

Take the live locale list from `build_modules.py`'s `fs_locales` /
`compliance_locales`, never from prose in a README.

---

## 8. Distractors are deliberately not literal translations

Wrong options are rendered freely so they read naturally in the target language.
A checker that flags "this option is not an equivalent of the German" flags
hundreds of *correct* entries — this was measured twice, at 421 and then 715 false
positives, and the approach was abandoned.

**Never "fix" a freely-rendered distractor into a literal one.** Only the correct
option, the question stem and the explanation carry an equivalence obligation.

---

## 9. Media: on the SSD, referenced by deterministic UUID

TTS audio (Ogg Opus, plus an AAC/M4A fallback — Safari plays Opus only in an Ogg
container, only from 18.4, never in WebM or MP4) and SRT subtitle tracks are
**never committed to either repo**. They live on an external SSD and are addressed
by deterministic UUIDv5:

```
key  = "<module>/<question_id>/<locale>/<kind>/<variant>"
uuid = uuid5(4e94d4ee-7ee3-5e01-a986-9006e4c2dea2, key)
```

The namespace was minted 2026-09-06 as `uuid5(NAMESPACE_DNS, "media.zettacard.de")`
so it is itself reproducible. It is now **immutable** — changing it orphans every
file on the disk.

Deterministic rather than random-plus-registry, so any checkout can compute any
object's UUID with no network and no registry, and a lost manifest is fully
regenerable from the content store. Files are sharded `<aa>/<uuid>.<ext>`.

**The SSD path is always configuration** (`--media-root` / `ZETTACARD_MEDIA_ROOT`),
never a constant in a script. Embedding a `/Volumes/...` path is a review-blocking
defect.

A reference is a promise, not a possession. This is only acceptable because every
referenced object is regenerable from the content store plus the TTS pipeline —
the SSD is a cache of expensive computation. **Anything that cannot be regenerated
— hand-recorded audio, hand-corrected splices, hand-timed subtitles — must never
live only on the SSD**, and no such asset may be created until it has a
backed-up home.

Media staleness is the same test as translation staleness: an object whose
`generated_against` no longer equals the current `source_hash` is stale.

---

## 8a. Answer roles — every option has a job

Full reasoning in `docs/adr/ADR-0006` Amendment 1. Every option on the German
canonical cell carries a role, inherited by every locale:

| Role | Meaning | Count |
|---|---|---|
| `richtig` | correct; the set must equal `meta.correct` exactly | 1, or 2+ multi-select |
| `irreführend` | **the trap** — the option a half-knowing learner actually picks | **exactly 1** |
| `plausibel` | wrong but reasonable; not the specific trap | the remainder |
| `abwegig` | clearly wrong to anyone who read the chapter | **at most 1** |

`irreführend` is a *named misconception*, not merely a hard distractor: the
neighbouring rule, the pre-amendment rule, the rule from another country, the
intuitive-but-wrong answer. Defensibly wrong, genuinely tempting.

Why it is enforced: it makes "this question tests nothing" checkable. A card with
no trap is answered correctly by anyone who skimmed the chapter. DEF-0001's absurd
option and total absence of a trap is the shape this rule catches.

**This qualifies § 8.** Distractors are still rendered freely and must never be
"corrected" toward the German — but the `irreführend` option must keep its **trap
function** in translation. Reword it however reads best; do not turn it into
something obviously wrong. That destroys the one option doing diagnostic work.

A question for which no `irreführend` option can honestly be written is a
**finding**, not a labelling failure: the question does not discriminate. It goes
to the reviewer pack as an authoring candidate and is never force-fitted.

Labelling the catalogue is milestone 0.11.

## 9a. Defects, and the cascade

Full reasoning in `docs/adr/ADR-0004-defects-and-derived-invalidation.md`. The
rules:

- Every defect is appended to `data/defects/<module>.jsonl`, append-only, with
  evidence, severity, the before/after `source_hash`, and what it invalidated.
  A defect that is only fixed and not recorded cannot be searched for as a class.
- **A defect in the canonical German cell cascades to everything derived from it;
  a defect in a derived cell does not.** Fix the canonical cell and let the hash
  do the invalidation. Never patch a translation to match a corrected German
  without re-drafting it, and never hand-edit `source_hash` to make a report go
  green.
- **A faithful translation of a wrong source is still wrong.** Cascades
  invalidate derived cells regardless of their own quality or review status.
- **Approvals never survive a cascade.** The approval record stays as history
  (it is the § 3 UrhG evidence for the version it approved); the status returns
  to `pending`. There is no "the change was small" exemption.
- **A cell with no `against_source_hash` is not a current cell** — its currency is
  unknown, and nothing reports it as stale. Do not read "no stale drafts" as
  "everything is current" until provenance backfill lands.

Defect classes: `answer_key`, `factual`, `citation`, `structural`, `translation`,
`staleness`. The first two cascade.

Do not quote a defect count as a quality metric. It measures defects *found*.

## 10. Verification discipline

- **Do not trust a self-report.** For anything visual or otherwise subjective,
  independently re-render and look at it yourself. This project's history has
  caught agents wrong about their own fix two and three rounds running.
- **An agent claiming full coverage is a claim, not a result.** Four parallel
  agents each reported reading all 531 questions in their locale; all four missed
  the same card. Spot-check with a script, over a key the agent had no reason to
  expect.
- **Test the control a real user must touch, not the state behind it.** A language
  switch was broken for every non-German locale on staging while three automated
  passes said it worked — they set the `<select>` through `page.evaluate` and never
  opened the menu the user has to open. If a user must click it, the test clicks it.
- **A green deploy is not proof.** Fetch the changed file's live URL and check the
  bytes.

---

## 11. Standing constraints that predate this file

These are unchanged and non-negotiable; they came out of legal analysis.

1. **Never source or paraphrase from the official Fragenkatalog** (current or old),
   or from any third-party exam-prep or compliance-training company's text.
   Generate original content from primary legal sources and from law-published sign
   specs (StVO Anlage 1–4).
2. **Track legal changes, not proprietary catalogue changes.** Never build a
   pipeline that syncs against someone else's compiled catalogue.
3. **Every content file ships with its real licence attached** (§3).
4. **No content has been reviewed by a legal professional.** Every unit carries
   `legal_review_status` saying so. Do not silently upgrade it — and note that this
   is a *fourth* sense of "verified", separate from all three in §5.
5. **Offline-first.** Output stays flat static JSON suitable for service-worker
   precaching. No feature may require a live backend call to serve content.
