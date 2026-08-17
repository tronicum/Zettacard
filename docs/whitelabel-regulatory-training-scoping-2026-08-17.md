# Whitelabel regulatory-training course line — architecture scoping (2026-08-17)

**Status:** first architecture pass for PO review. **Scoping only — no content, no question text, no lesson copy.**
The PO has said explicitly that detail follows later; authoring anything now would be premature.

**Working title of the line:** "Risiken und Regulierung" — broad regulatory/digital-risk training assembled per
audience, sold under a separate (TBD) brand to the financial industry and its supplier chain, while the same
underlying MCQ banks remain sellable as Zettacard-branded premium content in this app.

**Everything factual below about the codebase was verified in this repo on 2026-08-17.** Where a number is a
count I made, the method is stated so it can be re-run. Where something is a legal claim, it is marked as
inheriting the existing dossier discipline and *not* as verified here.

---

## 0. Contents

- §1 What already exists (verified inventory) — read this before designing anything
- §2 The honesty constraint, as a schema field, not a tone of voice
- §3 Tagging model: `regime` × `branche` × `exposure`
- §4 Bundles: recombination at **build time**, not runtime — and why that is forced
- §5 Scheduling model: one lesson pool, 1-week and 1-day formats (worked example with numbers)
- §6 The PDF gap — recommendation
- §7 The whitelabel/branding split — honest engineering scope
- §8 Premium/gating — content-model implications only
- §9 The Romanian locale gap, as a decision with three priced options
- §10 Punch list: decisions the PO owes before authoring starts
- §11 Appendix: exact files and line anchors

---

## 1. What already exists (verified inventory)

### 1.1 Question banks

`data/build_modules.py` builds 21 modules (`BUILT_MODULES`, line 53); `app/data/` contains 25 built module
directories, **2,258 questions total**. The regulatory/compliance subset relevant to this line:

| Module | Q | Content locales | Has course | Canonical |
|---|---:|---:|---|---|
| `dora` | 20 | de, en | ✅ | de |
| `nis2` | 20 | de, en | ✅ | de |
| `datenschutz` (GDPR/BDSG) | 40 | 12 | ✅ | de |
| `kyc_aml` (GwG) | 30 | de, en | ✅ | de |
| `kartellrecht` | 30 | de, en | ✅ | de |
| `ki_act` (EU AI Act) | 40 | 12 | ✅ | de |
| `it_sicherheit` | 64 | 12 | ✅ | de |
| `hinweisgeberschutz` | 40 | 12 | ✅ | de |
| `arbeitssicherheit` | 40 | 12 | ✅ | de |
| `lksg` | 30 | de, en | ❌ | de |
| `fadp_ch` | 40 | de, en | ❌ | de |
| **Total wired** | **394** | | | |

Authored but **not wired into `build_modules.py` and not in `app/data/`** (6 × 20 Q = 120 questions):
`cra_supply_chain_pilot_DRAFT.json` (EN-canonical, en/de, topics `manufacturer_duties` / `reporting` /
`sbom_vulnerability` / `scope_dates`), `dora_executive`, `dora_incident`, `dora_procurement`, `dora_register`,
`dora_audit_readiness` (all DE-canonical, de/en). Each has a pre-review dossier in `docs/`. **These are the
raw material for this line and they are currently shelf-ware** — wiring them is a prerequisite, not part of
this design.

Question record shape (verified against `data/dora_pilot.json`): `id`, `topic`, `topic_code`, `legal_basis`,
`points`, `correct`, `class_scope`, `grundstoff`, `high_stakes`, `question_type`, `image_ref`, `roles`, plus
per-locale `text`/`explanation` which `split_module()` fans out into `app/data/<m>/locales/<lang>.json`.

### 1.2 Course layer

11 modules ship a `course.json` (`aevo`, `arbeitssicherheit`, `cka`, `datenschutz`, `dora`, `hinweisgeberschutz`,
`it_sicherheit`, `kartellrecht`, `ki_act`, `kyc_aml`, `nis2`). Across all `data/*_course.json`:

- **60 lessons**: 41 `primer`, 9 `checkpoint`, 5 `scenario`, 3 `lab`, 2 `guidance`
- **124 sections**: 56 `prose`, 29 `worked_example`, 28 `callout`, 11 `decision_flow`, **0 `media`**
- `completion_rule`: 46 × `quiz_pass:0.7`, 9 × `quiz_pass:0.8`, 5 × `read`
- **All 124 sections carry `"license_ref": "CC-BY-NC-SA-4.0"`** — see §7.4, this is load-bearing
- Lesson length today: compliance courses run 12–25 min/lesson (`kyc_aml` = 6 lessons, 83 min total);
  `cka` is the outlier at 40–75 min/lesson, 570 min total, and is the only course with a `cadence_hint`
  (`"4 weeks, ~2.5 h of course time per week plus your own hands-on lab practice"` — free text, display-only)
- `cka` is also the only course with a course-level `locales` array (`en, de, ja, zh`) distinct from its
  module's — precedent that matters for §9

Runtime: `app/app.js:4722 renderCourseView()` lists lessons grouped under `units[]` headings, filtered to
`primer | checkpoint | scenario | guidance`; `openCourseLesson()` walks sections one at a time; on the last
section `related[]` renders **as prose only** (`app.js:4864–4874`) — no `href`, no link, no download.

**`app.js:4740` hardcodes `core.courses && core.courses[0]`.** The `courses[]` array-of-one that the v1 design
doc deliberately left extensible has no runtime consumer for a second element yet. §5 depends on this.

### 1.3 Media sections (landed 2026-08-17)

`section_kind: "media"` with `media.type ∈ youtube | video_mp4 | image | slideshow`. Facts stay in
`course.json`, `alt_text`/`caption` split into `course_locales/*.json`. `media.license` is **mandatory** and the
build hard-fails without it. No shipped course uses it yet. **There is no `pdf` or `document` type** — see §6.

The `media.license` enforcement is the pattern to copy for every new mandatory field in this design: a build-time
hard fail in `data/build_modules.py`, not a convention in a doc.

### 1.4 Locales

**12 UI locales, confirmed**: `de, en, uk, pl, ar, zh, hi, tr, fr, ru, es, it` — the same list appears in
`app.js:502 LANG_PICKER_LABEL`, in the two `<select>` blocks in `app/app.html` (lines 64–75 and 132–143), and as
`fs_locales`/`ang_locales`/etc. in `build_modules.py`'s `main()`. `RTL_LANGS = new Set(["ar"])` (`app.js:495`).
**`ro` is not among them.** `pl`, `es` are.

Counted by walking every `const *_STRINGS = { … }` object literal in `app/app.js` and counting depth-1 keys per
locale: **14 string blocks, 198 keys per locale, 2,186 translated string instances today.** One block
(`PRACTICE_QUIZ_STRINGS`, 19 keys) is DE/EN-only; the other 13 are full 12-locale. Largest single block:
`CERT_STRINGS`, 52 keys. → **a 13th locale needs 179 new UI strings** (see §9).

### 1.5 Branding, theming, gating — what exists and what does not

| Capability | State today |
|---|---|
| Design tokens | ✅ `app/styles.css:1` `:root` with ~27 CSS custom properties; light theme via `[data-theme="light"]` at line 34 |
| Brand parameterization | ❌ none. **107 hardcoded "Zettacard" occurrences across 11 non-content files** (`app.js`, `app.html`, `index.html`, `get-app.html`, `manifest.json`, `service-worker.js`, `app/legal/{quellen,trademarks}.html`, `netlify/functions/{issue-badge,get-badge,sign-credential}`) |
| Second build/deploy target | ❌ `netlify.toml` has `publish = "app"`, `command = "true"` — one site, one origin |
| Service worker | `CACHE_NAME = "zettacard-v7"`, a 10-entry `ASSETS` precache list — **per-origin**, so two brands on one origin would fight over it |
| Content visibility flag | ⚠️ partial: `feature_flag` on a manifest entry + `isFeatureEnabled()` (`app.js:1138`), fail-closed, used today only by `cka`. Overridable per-device via `?ff_<name>=on` → **visibility, not entitlement** |
| Payment / access gating | ❌ none, and deliberately deferred by the PO |
| PDF | ⚠️ only `printCertificateAsPdf()` (`app.js:2888`): hidden iframe + `window.print()`. No PDF library. The app has **zero third-party JS** (a stated constraint) |
| Badge issuer | `issuer: { type: "Profile", id: ISSUER_URL, name: "Zettacard" }` hardcoded at `netlify/functions/issue-badge.mjs:193`; `ISSUER_URL = process.env.URL || "https://zettacard.netlify.app"` (line 66) |
| Content licence | **`CC BY-NC-SA 4.0` on every pilot's `meta.license` and every one of the 124 course sections' `license_ref`** |

---

## 2. The honesty constraint, expressed as schema

The prior review in this session flagged that **DORA Art. 2 does not name real-estate brokers, and NIS2's
sector annexes do not either.** Consultants and auditors are likewise not addressees of DORA as such. The
commercially attractive framing ("DORA training for Immobilienmakler") is therefore an over-claim if it implies
a direct legal duty.

Prose discipline alone will not hold this across N audiences × M regimes × 4 languages authored by different
agents. Make it structural:

1. **`exposure` is a required enum on every audience mapping** (§3.2), with four values that force the author to
   pick a truthful one.
2. **`exposure_basis` is required whenever `exposure != "direct"`**, and the build hard-fails without it — same
   mechanism as `media.license`. It is one sentence naming *what actually creates the relevance* (a contract
   clause, a tender requirement, a client's obligation), which is exactly the sentence marketing copy tends to
   drop.
3. **Every bundle's lesson 1 is a mandatory exposure lesson.** `bundle.exposure_summary_key` points at a prose
   block that must exist in the canonical locale or the build fails. Content is the PO's later; the *slot* is
   architecture now. This mirrors the existing precedent where `dora-l1.related` carries the NIS2 lex-specialis
   warning structurally rather than trusting prose luck.
4. Existing dossier discipline is inherited unchanged: `legal_review_status`, primary-source (EUR-Lex/OJ)
   verification, the German + English disclaimer already carried in `cra_supply_chain_pilot_DRAFT.json`'s meta.
   **No legal claim in this doc has been verified here** — the Art. 2 / NIS2-annex points above are restated
   from the session's prior review and need the same dossier pass every other module got.

---

## 3. Tagging model

### 3.1 `regime` stays the module boundary — do not retag

One module = one `exam_type` = one directory = one question pool = one licensing boundary = one offline-cache
unit. That invariant is load-bearing in three separate places (`offlineAssetUrls()`, the licence-isolation rule,
and the "no cross-module content injection" decision). **A regime is a module. Do not introduce a second,
competing regime axis inside a module.**

Add to each pilot's `meta` (locale-independent, cheap, backfillable in one pass over 11 files):

```jsonc
"regime": {
  "id": "dora",                                  // closed vocab, see below
  "instrument": "Regulation (EU) 2022/2554",
  "celex": "32022R2554",
  "scope_article": "Art. 2",                     // where the addressee list lives - the honesty anchor
  "families": ["ict-risk", "operational-resilience"]   // for cross-regime bundle selection
}
```

Closed vocabulary for `regime.id` (extend by PR, never ad-hoc):
`dora · nis2 · cra · gdpr · gwg_aml · kartellrecht · ki_act · hinweisgeberschutz · arbeitsschutz · lksg ·
mica · fadp_ch`.

Note the deliberate decoupling of `regime.id` from `exam_type`: `datenschutz` carries `regime.id: "gdpr"`,
`kyc_aml` carries `gwg_aml`. That lets a bundle say "include the GDPR regime" without knowing this repo's
German module naming history.

### 3.2 `branche` / audience — the new axis, with exposure attached

Do **not** reuse the existing per-question `roles` field (`"all" | "all_staff" | "hr" | "it" | "management"`).
`roles` is *job function inside one employer*; `branche` is *what kind of employer*. A DORA question can be
`roles: ["it"]` and simultaneously `context_only` for a brokerage. Conflating them would silently destroy the
existing role filter (`ROLE_FILTER_STRINGS`, `app.js:1040`).

```jsonc
"audience_relevance": [
  {
    "branche": "immobilienmakler",
    "exposure": "indirect_contractual",
    "exposure_basis": "Not an addressee of the instrument's own scope article. Relevance arises only where the firm acts as a service provider to a regulated financial entity and the obligation is passed down contractually.",
    "weight": "core"
  },
  { "branche": "wirtschaftspruefer", "exposure": "direct", "weight": "core" },
  { "branche": "berater", "exposure": "indirect_market",
    "exposure_basis": "No statutory duty; arises as a client/tender expectation when advising in-scope entities.",
    "weight": "elective" }
]
```

**`branche` closed vocabulary** (PO to finalise — punch-list item 2):
`immobilienmakler · berater · wirtschaftspruefer · outsourcing_contractor · crypto_hub_devsecops ·
it_procurement · executive · all_staff`.

**`exposure` closed vocabulary — 4 values, and the whole point of this design:**

| value | meaning | marketing may say |
|---|---|---|
| `direct` | the learner's employer is a named addressee of the instrument | "applies to you" |
| `indirect_contractual` | bound through a contract with a regulated entity (flow-down clauses) | "your client's obligation becomes your contract" |
| `indirect_market` | no legal duty; a tender / audit / client expectation | "expected of you commercially" |
| `context_only` | background so the learner understands the client's world; explicitly no duty | "so you can talk to your client" — never "you must" |

**`weight`**: `core | elective | omit`. Drives §5's core/elective split and lets one lesson be core for auditors
and elective for brokers without a second copy.

### 3.3 Where the tags live: three levels, defaults inherited

Tagging 394 existing questions individually is a needless pass. Use inheritance:

1. **Module `meta.default_audience_relevance`** — the honest default for the whole pool. One edit per module.
2. **Lesson `audience_relevance`** — overrides the module default for that lesson. This is where most real
   authoring happens, ~8 lessons per bundle.
3. **Question `audience_relevance`** — override **only where a question would be actively misleading** for an
   audience. This is not optional polish: a question whose correct answer is a 4-hour notification deadline is
   *false as stated* for a `context_only` audience, and must be excluded from that bundle rather than
   re-explained. The build should report, per bundle, how many questions were pulled in on the module default vs.
   an explicit override, so "nobody checked" is visible in review.

Resolution order for a bundle: question override → lesson → module default. A question whose resolved
`exposure` is weaker than the bundle's declared `min_exposure` is excluded (and counted in the build log).

---

## 4. Bundles: recombination at build time, not runtime

### 4.1 The constraint that decides this

Runtime cross-module content loading is **already ruled out** by the existing course-layer design, for three
reasons that all still apply here and are not stylistic:

1. **Correctness.** The DORA/NIS2 lex-specialis carve-out means injecting NIS2's reporting cascade into a DORA
   lesson teaches a deadline that does not bind that learner. This new line multiplies exactly that hazard
   across more regimes and more audiences.
2. **Offline-first.** `offlineAssetUrls()` (`app.js:1571`) caches exactly one module's `core.json` + one locale
   file (+ primers/course/media extras). Runtime composition would need a dependency walk it has no concept of.
3. **Licence isolation.** One module = one licensing boundary; content that never crosses a boundary can never
   propagate a share-alike obligation sideways. §7.4 makes this urgent, not theoretical.

**So: compose bundles in the build, and let the runtime keep seeing one ordinary module.** A compiled bundle is
indistinguishable at runtime from `dora` or `kyc_aml`. **Zero `app.js` changes are required for the tagging and
recombination half of this design** — which is the single biggest reason to prefer it.

### 4.2 The bundle file

New authored file, `data/bundles/<bundle_id>.json`:

```jsonc
{
  "bundle_id": "riskreg_immobilien_de",
  "channel": "riskreg",                    // which distribution brand ships it (§7)
  "audience": "immobilienmakler",
  "canonical_locale": "de",
  "locales": ["de", "en"],
  "access_tier": "premium",                // §8 - a label, not enforcement
  "min_exposure": "indirect_contractual",  // anything weaker is excluded, with a build count
  "exposure_summary_key": "riskreg_immobilien_de-exposure",   // MANDATORY - §2.3
  "schedule_profile": "week-5x60",         // §5

  "include": [
    { "regime": "dora",  "from_module": "dora",
      "lessons":   ["dora-l1", "dora-l5"],
      "questions": { "topic_codes": ["grundlagen", "drittparteien"], "max": 8 } },
    { "regime": "gdpr",  "from_module": "datenschutz",
      "lessons":   ["datenschutz-l2"],
      "questions": { "topic_codes": ["betroffenenrechte"], "max": 6 } },
    { "regime": "gwg_aml", "from_module": "kyc_aml",
      "lessons":   ["kyc_aml-l1"],
      "questions": { "topic_codes": ["sorgfaltspflichten"], "max": 6 } }
  ]
}
```

`split_bundle()` in `data/build_modules.py` (folded in, **not** a new script — the repo has been burned twice by
sibling build scripts silently dropping each other's output) emits an ordinary module directory:

```
app/data/riskreg_immobilien_de/core.json          <- questions, each carrying provenance
app/data/riskreg_immobilien_de/locales/{de,en}.json
app/data/riskreg_immobilien_de/course.json        <- lessons, re-ordered, unit-grouped per §5
app/data/riskreg_immobilien_de/course_locales/{de,en}.json
```

Every compiled record carries provenance so nothing is orphaned:

```jsonc
{ "id": "riskreg_immobilien_de-dora-grundlagen-01",
  "source_module": "dora", "source_id": "dora-grundlagen-01",
  "regime": "dora", "license_ref": "CC-BY-NC-SA-4.0",
  "resolved_exposure": "indirect_contractual", "…": "…" }
```

Build must also: rewrite `meta.app` (today `"Zettacard / dora-lernmodul"` — wrong on a whitelabel bundle),
compute the bundle's effective licence as the union of its parts and **refuse a combination it cannot reconcile**
(§7.4), and fail if `exposure_summary_key` has no canonical-locale text.

**Accepted cost:** compiled bundles duplicate bytes. A bundle of 8 lessons + ~30 questions × 4 locales is a few
hundred KB; `app/data/` already holds 2,258 questions × up to 12 locales. Not a real problem at this scale, and
the alternative costs correctness.

**Accepted cost 2:** every bundle is a `modules.json` entry, so N audiences × 2 schedule formats × M languages
multiplies the module picker. §7 resolves this: the whitelabel brand's picker shows only its own bundles.

### 4.3 The clean answer to "one source, two products"

| | Zettacard-branded premium | Whitelabel course product |
|---|---|---|
| What ships | the **regime modules** (`dora`, `nis2`, `datenschutz`, …) | the **compiled bundles** |
| Experience | MCQ / flashcards / exam sim, existing chrome | full course: video, prose, handouts, checkpoints |
| Course layer | existing per-module course, or suppressed | the assembled per-audience course |
| Assembly | none — modules already exist | `split_bundle()` |
| Authored content duplicated | **none** | **none** |

Only the *assembly configuration* differs. That is the property the PO asked for.

---

## 5. Scheduling: one lesson pool → 1-week and 1-day formats

### 5.1 Unit granularity

Set the **content unit = one lesson = 45–60 min**, and treat 50 min as the authoring target. Rationale:

- The existing compliance courses author 12–25 min lessons; `cka` authors 40–75. A 50-min unit is inside the
  proven range and is the natural size of a classroom block (50 + 10 min break).
- `estimated_minutes` already exists on every lesson and is authored, not computed. **Keep it the single source
  of truth for duration.** A schedule profile must never re-time a lesson; it only *groups lesson ids*.
- A unit at this size survives both formats: it is one sitting for the self-paced learner and one block for the
  instructor.

### 5.2 Schedule profiles

Add to the course object (locale-independent except the label):

```jsonc
"session_length_minutes": 50,
"schedule_profiles": [
  { "profile_id": "week-5x60", "kind": "self_paced",
    "label": { "de": "…", "en": "…" },
    "days": [
      { "day": 1, "lessons": ["b-l1"], "target_minutes": 60 },
      { "day": 2, "lessons": ["b-l2"], "target_minutes": 60 }
    ] },
  { "profile_id": "intensive-1day", "kind": "instructor_led",
    "label": { "de": "…", "en": "…" },
    "blocks": [
      { "block": 1, "lessons": ["b-l1", "b-l2"], "break_after_minutes": 15 },
      { "block": 2, "lessons": ["b-l3"],         "break_after_minutes": 45 }
    ] }
]
```

Build-time rules:
- a lesson appears at most once per profile;
- the union of a profile's lesson refs must equal the course's `weight: "core"` lessons — a missing core lesson
  is a hard fail, an extra elective is fine;
- sum of referenced `estimated_minutes` + breaks is computed and written back as `profile.total_minutes` so the
  marketing claim ("7-hour intensive") is derived from content, not asserted.

### 5.3 Worked example — 5 core + 3 elective units of ~50 min

| | `week-5x60` (self-paced) | `intensive-1day` (instructor-led) |
|---|---|---|
| Core lessons | 5 × 50 min = **250 min**, one per weekday | same 5 × 50 = **250 min**, back to back |
| Audience electives | days 6–7, optional | +2 × 50 = **100 min** |
| MCQ checkpoint | ~10 min at the end of each day = 50 min | one 30-min checkpoint at the end |
| Breaks | n/a (self-paced) | 2 × 15 + 45 lunch = **75 min** |
| **Elapsed** | 5 × ~60 min = **5 h across 5 days** | 250 + 100 + 30 + 75 = **455 min ≈ 7 h 35** |
| Lean variant (no electives) | 5 h | 250 + 30 + 45 = **325 min ≈ 5 h 25** |

**Both PO targets are satisfied by a single pool of 8 units per audience bundle: 5 core (shared across all
Branchen) + 3 audience-specific electives.** The 4–8 h intensive window is hit at both ends by including or
dropping electives; the 1 h/day week track is the same 5 core units, one per day, with the electives offered as
optional days 6–7.

Note the arithmetic the PO should see: **5 × 1 h ≠ 8 h.** "Same content, two formats" only works if the day
format has *more* content than the week format, or the week format runs longer than 5 days. The core/elective
split is the mechanism that makes that honest rather than a marketing fudge. If the PO wants literally identical
content in both, the intensive lands at ~5 h 25 and the "up to 8 hours" claim has to go.

### 5.4 What this costs in the app

- **Zero-code path (recommended for v1):** the course view already renders `units[]` as headings. Emit
  `unit_kind: "day"` (week track) or `unit_kind: "block"` (intensive) and the existing UI groups correctly with
  no change. Compile the two formats as **two courses in the same module's `courses[]` array** — the
  array-of-one the v1 design deliberately left extensible.
- **The one real app change:** `app.js:4740` hardcodes `courses[0]`. Supporting two schedule formats in one
  module needs a format picker → one small modal + ~4 new strings × N locales + a `courses[]` selector.
  Small, but not free, and it is the *only* app-side change §4/§5 require.
- **Cheapest possible alternative:** compile `…_week` and `…_intensive` as two separate modules. Zero app
  change, at the cost of two picker entries and duplicated bytes. Reasonable for a pilot, ugly at scale.

---

## 6. The PDF gap — recommendation

### 6.1 What was actually checked

- `section_kind: "media"` supports `youtube | video_mp4 | image | slideshow`. **No `pdf`, no `document`.**
- `related[]` renders as prose only (`app.js:4864–4874`). **There is no download-link mechanism in the course
  layer at all** — no `href`, no attachment, nothing.
- The *only* PDF path in the app is `printCertificateAsPdf()` (`app.js:2888`): build an HTML document in a
  hidden iframe, call `contentWindow.print()`, let the browser's "Save as PDF" do the rest. No PDF library.
- The app has **zero third-party JS**, stated as a constraint and re-affirmed when the media carousel was
  hand-rolled rather than taking a dependency.

### 6.2 Recommendation: do **not** render PDFs inline. Do two cheaper things.

**Rejected — `media.type: "pdf"` with inline rendering.** `<embed>`/`<iframe>` PDF viewing is inconsistent
across browsers and poor on mobile (the app's primary form factor); doing it properly means pdf.js, which is
~1 MB of third-party JS and breaks the zero-dependency rule for one section type. It is also offline-hostile if
the asset is remote.

**Recommended (a) — a new `section_kind: "handout"`: a download affordance with metadata, not a viewer.**

```jsonc
{ "section_id": "b-l3-s4", "order": 3, "section_kind": "handout",
  "handout": {
    "src": "assets/handouts/art30-checkliste-de.pdf",   // same-origin ⇒ SW-precacheable, like local images
    "mime": "application/pdf",
    "pages": 4, "bytes": 214000,
    "lang": "de",                                        // a PDF is per-language, unlike a diagram
    "license": "Zettacard original",                     // mandatory, same rule as media.license
    "commercial_use": true,                              // §7.4 - needed for the whitelabel channel
    "title":       { "de": "…", "en": "…" },            // split into course_locales
    "description": { "de": "…", "en": "…" }
  } }
```

Cost: ~30 lines in `app.js`, 3–4 new `COURSE_STRINGS` keys × 12 locales, a `split_handout()` validator in
`build_modules.py`, and one `offlineAssetUrls()` addition. Follow the mp4 decision's shape for hosting: a
same-origin `assets/handouts/…` path is precacheable and works offline; an external `https://` URL is not and
should get the same offline notice the media sections already render.

**Recommended (b) — generate handouts from lesson prose using the existing print path.** For "give me a PDF of
what we just covered", reuse `printCertificateAsPdf()`'s iframe-and-print pattern against the lesson's own
sections. No binary asset, no licensing question, works offline, no new dependency, and it stays automatically
in sync with the content. This is very likely what "PDF" means for most of the requirement.

**Open question for the PO (punch-list item 8):** "PDF" here is at least three different artifacts —
(i) a branded slide deck for the *trainer*, (ii) a learner handout/checklist, (iii) a certificate of
attendance. (iii) largely exists (certificate HTML + print-to-PDF + signed Open Badge). (ii) is (b). Only (i)
genuinely needs (a).

---

## 7. Whitelabel / branding split — honest engineering scope

**This is real net-new engineering.** The app has design tokens but no brand parameterization: 107 hardcoded
"Zettacard" occurrences across 11 non-content files, one Netlify publish target, a per-origin service worker and
web-app manifest, and a hardcoded badge issuer.

### 7.1 The mechanism: `app/brand.json`, loaded before first render

```jsonc
{
  "brand_id": "riskreg",
  "name": "…",  "domain": "…",
  "logo": "icons/riskreg.svg",
  "theme": { "--accent": "#…", "--bg": "#…", "--card": "#…" },   // CSS custom-property overrides only
  "modules": ["riskreg_immobilien_de", "riskreg_wp_en"],          // allowlist - the picker shows only these
  "ui_locales": ["en", "de", "pl", "es", "ro"],
  "badge_issuer": { "name": "…", "url": "…", "key_id": "…" },
  "legal": { "impressum_url": "…", "privacy_url": "…" },
  "features": { "certificates": true, "exam_sim": false }
}
```

Theming is genuinely cheap **because** `styles.css` is already fully tokenized (`:root` + `[data-theme]`) —
a brand override is a handful of custom-property assignments injected before first paint, the same trick the
existing anti-flash theme script in `app.html` already uses.

### 7.2 The delivery model: a second publish target, not runtime multi-tenancy

Do **not** serve two brands from one origin. The service-worker cache and the web-app manifest are per-origin;
two brands would collide on `CACHE_NAME`, on the install prompt, and on precached shell assets.

Instead: a new build step (`scripts/build_brand.py` or a `build_modules.py` sibling target) copies `app/` into
`dist/<brand_id>/`, overwrites `brand.json`, `manifest.json`, the SW's `CACHE_NAME`/`ASSETS`, `icons/`, the legal
pages and `index.html`, and prunes `data/` to the brand's module allowlist. A second Netlify site publishes
`dist/riskreg/` on the new domain. Zettacard's own site is untouched.

### 7.3 Scope, chunked honestly

| # | Work | Size | Notes |
|---|---|---|---|
| 1 | Brand-token extraction: `brand.json` loader; parameterize `app.html` title/h1/meta, `manifest.json`, SW `CACHE_NAME`+`ASSETS`, `UI_STRINGS.*.title` (12 locales), the certificate chrome in `CERT_STRINGS` (52 keys is the biggest block and it names the issuer), `index.html`/`get-app.html`, `app/legal/*` | **M** | 107 occurrences; maybe 30 actually matter |
| 2 | Module allowlist + picker filter | **S** | `feature_flag`'s filter at `app.js:1773` is the precedent; ~5 lines |
| 3 | Theme override injection | **S** | tokens already exist |
| 4 | Second build target + second Netlify site + domain/DNS/TLS | **S–M** | mostly config; new `dist/` tree changes `.gitignore` and deploy story |
| 5 | `split_bundle()` in `build_modules.py` | **M** | §4; the largest single new code artifact, and it is all Python, not app code |
| 6 | Two-schedule-format support (`courses[]` picker) | **S** | §5.4; skippable in v1 |
| 7 | `section_kind: "handout"` | **S** | §6 |
| 8 | **Per-brand badge/credential identity** | **M, and the risky one** | `issuer.name: "Zettacard"` is baked into `issue-badge.mjs:193`. A whitelabel badge signed by Zettacard's key and naming Zettacard is either brand leakage or misattribution. Needs a per-brand issuer profile, probably a per-brand key + JWKS path, and a decision about whether one legal entity issues for both brands |
| 9 | **Legal/licensing for the new domain** | **M, non-code** | own Impressum + Datenschutzerklärung; §7.4 |

Nothing here is architecturally scary. Items 8 and 9 are the ones that can actually block a launch.

### 7.4 The blocker nobody has flagged yet: the content licence

**Every pilot's `meta.license` is `CC BY-NC-SA 4.0`, and all 124 course sections carry
`license_ref: "CC-BY-NC-SA-4.0"`.** The `-NC-` is *NonCommercial*. Two consequences:

1. **Selling this content commercially contradicts what the repo currently says about it.** Presumably the PO is
   sole rightsholder and can dual-license (the existing `license_note` even says "Commercial reuse needs a
   separate arrangement" — i.e. with the PO). But that has to be *done*: a decision, and then a mechanical pass
   over `meta.license`/`license_note` on every reused pilot and `license_ref` on every reused section. Until
   then, a commercial whitelabel product built from these files is inconsistent with its own metadata.
2. **`ShareAlike` on any third-party-derived fragment would propagate into the commercial product.** This is
   exactly why §4.1 keeps licences travelling with compiled fragments and why `split_bundle()` should compute
   the effective licence and refuse an irreconcilable mix.
3. Same issue one level down for media: `media.license` is a free-text human label today. `"CC BY 4.0"` is
   commercially fine, `"CC BY-NC 4.0"` is not, and nothing can tell them apart mechanically. **Add a required
   boolean `commercial_use` alongside `media.license` and `handout.license`**, and have the whitelabel build
   target refuse any asset with `commercial_use: false`. Cheap now, unpleasant to retrofit after 200 videos.

---

## 8. Premium / gating — content-model implications only

Per the PO, the payment/checkout mechanism is deliberately deferred. Only the content model is designed here.

**Fields:**

```jsonc
// modules.json entry, course, lesson, or question
"access_tier": "free" | "premium" | "channel_only",
"channels": ["zettacard", "riskreg"]
```

`access_tier` is inherited downward (module → course → lesson → question) with the most specific winning, same
resolution style as §3.3.

**And now the honest part.** All content is static JSON, served from a CDN, precached by a service worker.
Anything the app can render, a determined user can `curl`. `feature_flag`/`isFeatureEnabled()` is fail-closed by
default but is overridable per-device with `?ff_<name>=on`, stored in `localStorage` — that is a **visibility
switch, not an entitlement check**, and the code's own comments say as much.

Therefore: **`access_tier` is a merchandising and assembly label, not enforcement.** The two real options are

- **(a) build-time exclusion** — premium content simply is not in the publish tree the free audience gets. The
  §4 bundle model gives this for free: a bundle exists only in its brand's `dist/` directory. Nothing to
  bypass, because nothing is served.
- **(b) server-delivered content behind auth** — real enforcement, but it breaks offline-first precaching,
  which is a stated product constraint and the reason this app has no backend for content today.

**Recommendation: (a), and say so out loud.** In this architecture the strongest available paywall is *build-time
exclusion*, not a runtime flag. For Zettacard-branded premium MCQ inside the free app, that means the honest
options are: ship it and mark it premium (visibility only, trivially bypassable), or keep the premium pool in a
separate origin/build. Which of those is acceptable is a PO decision (punch-list item 11) — and it is a
*product* decision, not something the schema can paper over.

---

## 9. The Romanian locale gap — a decision, priced three ways

### 9.1 The measured facts

`ro` is not one of the app's 12 UI locales. Adding it app-wide means:

| What | Count |
|---|---|
| UI strings in `app/app.js` (13 of 14 `*_STRINGS` blocks are 12-locale; `PRACTICE_QUIZ_STRINGS` is DE/EN-only) | **179 new strings** |
| — of which `CERT_STRINGS` alone | 52 |
| `LANG_PICKER_LABEL` entry (`app.js:502`) | 1 |
| `<option>` in `app/app.html` (two separate `<select>` blocks: UI language, certificate language) | 2 |
| `modules_manifest.json` module labels | 25 objects |
| `modules_manifest.json` scope-option labels | 34 objects |
| `modules_manifest.json` module intro steps | 10 (DE/EN-only today; falls back to EN) |
| Per-module content: `locales/ro.json` + `course_locales/ro.json` | per module in scope |
| RTL work | none (`ro` is LTR) |
| `detectBrowserLang()` | works automatically once `UI_STRINGS.ro` exists |

### 9.2 The finding that kills the naive "narrow alternative"

**`app/data/cka/locales/ja.json` and `app/data/cka/course_locales/ja.json` exist and ship — and are
unreachable.** `state.lang` is gated by `if (savedLang && UI_STRINGS[savedLang])` (`app.js:6782`) and
`detectBrowserLang()` only returns a language present in `UI_STRINGS` (`app.js:515`). Content locale is always
derived from `state.lang` with *downward* fallback only (`app.js:1500–1540`); there is no independent
content-language selector. So a content locale that is not a UI locale is dead weight today.

That is the precedent for "Romanian for this course line's content only": **it does not work as-is.** It needs at
minimum a `UI_STRINGS.ro` entry plus a picker option — or a deliberate split of the UI-language and
content-language gates.

### 9.3 Three options

| | Option A: full 13th UI locale | Option B: RO in `UI_STRINGS`, offered only in the whitelabel brand's picker | Option C: split content-language from UI-language |
|---|---|---|---|
| UI strings to translate | 179 | 179 (they live in the shared `app.js`) | ~0 |
| App code change | none beyond strings + 2 `<option>`s | `brand.ui_locales` filter on the picker (§7.1) | **new**: a `CONTENT_LANGS` set, a content-language selector, and a "showing X because RO isn't translated" notice |
| Zettacard picker shows RO | yes — with content only 1–2 modules deep | no | yes, as a *content* language |
| Fixes the stranded `ja` content | no | no | **yes** |
| Verdict | cleanest, most work, and awkward until RO content exists app-wide | **recommended for a first launch** — the strings get written once, exposure is controlled per brand | architecturally the nicest and the only one that avoids the 179 strings, but it is net-new UI/UX with a fallback-notice design attached |

**Recommendation: Option B**, with Option C noted as the right follow-up if a second content-only language ever
appears (`ja` already makes it two). Under Option B, RO content for the course line lives in the bundle's own
`locales/ro.json` / `course_locales/ro.json`, and `brand.ui_locales` keeps RO out of the Zettacard-branded
picker until there is a reason for it to be there.

Note also that the PO's stated language set for this line (**EN + RO + PL + ES**) and the existing B2B roadmap's
set (EN, DE, FR, ES, IT, PL, RO) do not match. Punch-list item 3.

---

## 10. Punch list — decisions needed before any content is authored

1. **Domain and brand identity.** Name, domain, logo, colour tokens for the whitelabel line. Blocks §7 items
   1–4 entirely; everything else can proceed without it.
2. **Final `branche` vocabulary.** The four named (Immobilienmakler, Berater, Wirtschaftsprüfer,
   outsourcing/contractor) plus the crypto-hub audience — is that the closed list, or is it open-ended? Each
   `branche` costs ~3 elective units of authoring; the 5 core units are shared.
3. **Final language set per audience,** and reconciliation with the existing roadmap's 7-language plan.
   Concretely: is it EN+RO+PL+ES for this line, or the roadmap's EN/DE/FR/ES/IT/PL/RO?
4. **Reuse vs. re-author per regime.** 394 wired questions + 120 authored-but-unwired exist. The unwired 120
   (`cra_supply_chain` + 5 DORA sub-modules) are the closest match to this line's audience and are currently
   shelf-ware. Wire them first, or author fresh?
5. **Do the existing GDPR (`datenschutz`) and GwG/AML (`kyc_aml`) modules get folded into bundles, or stay
   standalone?** Recommendation: folded in via `include` — they need no re-authoring, only audience tagging.
   Note `datenschutz` already has 12 content locales while `kyc_aml` has 2; a bundle mixing them inherits the
   *narrower* locale set.
6. **Exposure classification per (audience × regime).** This is the PO's call, not an authoring agent's, and it
   is the single highest-risk item in the whole line. It needs the same primary-source dossier pass every other
   module got — including re-verifying the Art. 2 / NIS2-annex points that triggered this reframe.
7. **Core/elective split.** Confirm 5 core + 3 elective units of ~50 min (§5.3), or state the real target
   durations. If "identical content in both formats" is a hard requirement, the intensive is ~5 h 25 and the
   "up to 8 hours" claim goes.
8. **What "PDF" means:** trainer slide deck (needs the new `handout` section kind), learner handout (generate
   from prose, nearly free), or attendance certificate (largely exists).
9. **Whitelabel engineering budget.** §7.3 items 1–7 are S/M and mostly mechanical. Items 8 (per-brand badge
   issuer identity + keys) and 9 (Impressum, Datenschutzerklärung, licence relicensing) are the ones that can
   block a launch. Approve or defer explicitly.
10. **Relicense the reused content for commercial use** (§7.4). All 11 candidate modules and all 124 course
    sections currently say NonCommercial. Nothing else in this design is blocked by it, but shipping is.
11. **Premium inside Zettacard: visibility or exclusion?** Ship premium MCQ in the free app marked
    `access_tier: "premium"` (bypassable), or keep it out of the free build entirely (§8). This is the only
    part of the deferred paywall question that the content model cannot avoid answering.
12. **Two schedule formats: one module with two courses, or two modules?** The former needs the `courses[0]`
    change at `app.js:4740`; the latter needs nothing but duplicates a picker entry.
13. **Romanian: option A, B or C** (§9.3).
14. **`commercial_use` on media/handout licences** — approve adding it as a required field now, before any
    video library exists (§7.4.3).

---

## 11. Appendix — verified anchors

**Schema / build**
`data/build_modules.py` — `CORE_FIELDS` :34, `BUILT_MODULES` :53, `split_module()` :62, `MEDIA_TYPES` :145,
`_norm_media_facts()` :212, `split_course()` :261, `main()` :384
`data/modules_manifest.json` — 25 module entries; `hasCourse` flags; `feature_flag` on `cka` :1184
`data/dora_pilot.json`, `data/dora_course.json`, `data/cka_course.json` (`cadence_hint`, course-level `locales`)
`data/{cra_supply_chain,dora_executive,dora_incident,dora_procurement,dora_register,dora_audit_readiness}_pilot_DRAFT.json`

**Runtime**
`app/app.js` — `RTL_LANGS` :495, `LANG_PICKER_LABEL` :502, `detectBrowserLang()` :510,
`isFeatureEnabled()` :1138, feature-flag deep link :1156, picker filter :1773,
locale fallback / `contentLangFallback` :1500–1540, `offlineAssetUrls()` :1571,
`printCertificateAsPdf()` :2888, `renderCourseMedia()` :4544, `courses[0]` :4740,
`renderCourseView()` :4722, related-as-prose :4864, `COURSE_STRINGS` :4595, UI-locale gate :6782
`app/app.html` — brand strings :6/:14/:31, language `<select>`s :64–75 and :132–143, course view :287
`app/styles.css` — `:root` tokens :1–27, `[data-theme="light"]` :34
`app/service-worker.js` — `CACHE_NAME` :62, `ASSETS` :63
`netlify/functions/issue-badge.mjs` — `ISSUER_URL` :66, hardcoded `issuer.name` :193
`netlify.toml` — `publish = "app"`, single site

**Docs**
`docs/course-media-sections.md` (media layer, landed 2026-08-17)
`docs/{cra-supply-chain,dora-audit-readiness,dora-executive,dora-incident,dora-procurement,dora-register}-pre-review-dossier-2026-08-16.md`
`docs/business-team-features-scoping.md` (B2B backend options), `docs/paid-verifiable-certificates-scoping.md`,
`docs/open-badges-signing-scoping.md`
Project docs: `claude/modular-course-architecture-v1-2026-08-15.md` (the v1 course-layer design this builds on),
`claude/dora-cra-b2b-training-roadmap-2026-08-16.md` (the 9-module B2B roadmap and its language plan),
`claude/dora-nis2-module-scoping-2026-08-13.md`, `claude/dora-pilot-pre-review-dossier-2026-08-13.md`

**Counting methods, so they can be re-run**
UI strings: brace-matched every `const *_STRINGS = {…}` in `app/app.js`, counted depth-1 keys per locale
→ 14 blocks, 198 keys/locale, 179 in the 12-locale blocks, 2,186 instances total.
Brand coupling: `grep -rn "Zettacard"` over `app/` + `netlify/` + `netlify.toml`, excluding `app/data/`
→ 107 hits in 11 files.
Sections/lessons: `grep -ho '"section_kind": "…"' data/*_course.json | sort | uniq -c` → 124 sections,
60 lessons, 0 media.
