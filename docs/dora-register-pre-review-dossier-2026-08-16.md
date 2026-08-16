# DORA Art. 28 Informationsregister module (`dora_register`) — draft pilot content + pre-review dossier (2026-08-16)

**Status:** AI-prepared groundwork only — **NOT legal advice**. Attorney sign-off required before any commercial/production use. The draft question file exists at `data/dora_register_pilot_DRAFT.json` and is **deliberately not wired into the live app**: it is not registered in `data/build_modules.py` or `data/modules_manifest.json`, no build step was run, and nothing was staged or committed.

**Subject:** 20-question DE/EN draft pilot for a new module, **"DORA Art. 28 — Informationsregister"** / *DORA Information Register* (internal working name `dora_register`, roadmap module 4, the user's #3 TAM priority). Target audience: **compliance officers, IT-controlling and PMO/programme staff at EU financial entities who personally have to build, maintain and hand over the Register of Information** — not people who need to know it exists. Schema follows `data/kartellrecht_pilot.json` field-for-field (verified programmatically: identical question-object key set **and** key order). Same pilot-then-scale discipline as the two sibling modules drafted this session (`dora_procurement`, `dora_executive`): 20 questions DE/EN → 40 questions / wider locale set only after sign-off.

**Method.** Every citation below was read on 2026-08-16 in the **official Official Journal text**, in both the **English and the German** language versions, retrieved from the EU Publications Office **Cellar** repository (`publications.europa.eu/resource/celex/<CELEX>`, `Accept: application/xhtml+xml`, `Accept-Language: eng` / `deu`). As the two sibling dossiers recorded, `eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge in this sandbox and `WebFetch` truncates inside the recitals; the Cellar route was used from the start and delivered complete documents (DORA 747 KB EN / 784 KB DE; the ITS 466 KB EN / 476 KB DE).

| Instrument | CELEX | OJ reference | What was read |
|---|---|---|---|
| Regulation (EU) 2022/2554 (DORA) | `32022R2554` | OJ L 333, 27.12.2022, p. 1 | Art. 2(1)–(4), Art. 3(20)–(23), Art. 8(1), Art. 16(1), **Art. 28 in full (1)–(10)**, Art. 29, Art. 31(1)–(11) — EN + DE |
| Commission Implementing Regulation (EU) 2024/2956 | `32024R2956` | OJ L, 2.12.2024 | **The ITS under the Art. 28(9) mandate.** Recitals 1–15, Art. 1–7, **Annex I Parts 1 and 2 in full (all 15 templates, every column instruction)**, Annexes II, III, IV — EN + DE |
| Corrigendum to (EU) 2024/2956 | via consolidated `02024R2956-20241202` | OJ L, 2025/90725, 19.9.2025 | Read through the Publications Office consolidation (EN + DE), which carries the `►C1` change markers; corroborated against the corrigendum PDF |

**Adoption status — confirmed, not assumed.** The task brief asked me to verify rather than assume that the ITS is in force. It is. **Commission Implementing Regulation (EU) 2024/2956 of 29 November 2024** is an adopted, published implementing act, "laying down implementing technical standards for the application of Regulation (EU) 2022/2554 … with regard to standard templates for the register of information", citing "in particular Article 28(9), second subparagraph, thereof". Art. 7 provides entry into force on the twentieth day following publication, and the closing formula reads *"This Regulation shall be binding in its entirety and directly applicable in all Member States."* It is **not** an RTS, **not** a draft, and **not** an ESA guideline — a distinction question 5 tests directly, because secondary material routinely mislabels it.

**One correction to the instrument's own text.** The ITS was corrected by a corrigendum published in **OJ L, 2025/90725 of 19.9.2025**. Read through the consolidated version in both EN and DE, the corrigendum: (i) simplifies the code-type construction in column `B_05.01.0020`; (ii) fixes the cross-reference in `B_05.01.0090` from `B_05.01.0070` to `B_05.01.0100`; (iii) **renumbers the columns of template `B_06.01`** — the original OJ text jumped from `…0040` to `…0060`, so `Criticality or importance assessment` is now `B_06.01.0050`, not `B_06.01.0060`, and every following column shifts down by one; (iv) corrects the option number of "Assessment not performed" in `B_07.01.0110` from `7.` to `3.`. This matters commercially, not just editorially: **any data model or vendor template built from the December 2024 OJ text carries wrong `B_06.01` column codes.** Question 15 is written on the corrected numbering and says so in its explanation.

*(Residual drafting inconsistency, noted but not tested: even in the corrected consolidated text, the `B_99.01` cross-reference table still points at `B_06.01.0110` for "Impact of discontinuing the function", while the corrected `B_06.01` template now ends at `…0100`. Flagged for the reviewer; no question depends on it.)*

---

## 1. Why this module, and why it is not a re-run of the shipped `dora` module

The shipped general-staff module covers the register in exactly one question — `dora-drittparteien-01`, 2 points, `grundstoff`, not `high_stakes` — whose whole content is "financial entities must keep a Register of Information covering all contractual arrangements with ICT third-party providers", with a one-sentence explanation. That is the right depth for an all-staff awareness module under Art. 13(6). It is not remotely enough for the audience here, and there is no overlap risk: **none of the 20 questions in this pilot can be answered from what `dora_pilot.json` teaches**, and 16 of them cannot be answered from the base Regulation at all — they need the ITS.

Three design decisions came out of the primary-source read:

1. **The spine of the module is the gap between what Art. 28(3) says and what the register programme actually has to do.** The base Regulation gives you four sentences. The ITS gives you 15 templates, four relational keys, a rank system, and roughly 120 column instructions with three levels of conditional mandatoriness. A module that stays at the Art. 28(3) level teaches nothing operational; a module that only teaches templates leaves the learner unable to answer a supervisor's "on what basis?".
2. **The single highest-value correction this module can make is the "annual submission" framing** — see §4.1. It is wrong in the project's own roadmap doc, it is wrong in most vendor marketing, and it is exactly the kind of thing a Big-4 auditor will ask a compliance officer to cite chapter and verse for. Question 2 is built entirely around it and is `high_stakes`.
3. **Four questions are operational-trap scenarios** (`registerstruktur-04` multi-country data locations, `lieferkette-02` three-tier chain, `lieferkette-04` intra-group first-extra-group-subcontractor, `funktionen-04` "our SOC report counts as our audit"). These are the four places where a register that looks finished is actually defective, and all four are answerable only from the Annex I instructions.

## 2. Citation ledger (primary-source verified 2026-08-16)

**Confidence rule used here** — identical to the `dora_procurement` dossier, stated so the reviewer can hold me to it:

- **"High — verbatim"** = the tested proposition is a direct restatement of wording I read in the OJ text of the cited provision, in **both** EN and DE.
- **"High — verbatim + synthesis"** = every element is verbatim, but the question combines **two or more** provisions I read separately; the reviewer should check that the *combination* is a fair statement, not the underlying text.
- **What disqualifies a claim from "High":** any of (a) the proposition rests wholly or partly on a source that is not the OJ text of a binding instrument — including ESA Q&As, FAQs, national-authority notices and vendor summaries; (b) the proposition requires an inferential step beyond the words on the page (legal characterisation, gap-filling, "this implies"); (c) the proposition was verified in only one language version where both exist; (d) the proposition rests on a **recital** rather than the enacting terms. Anything hitting (a)–(d) is either dropped or explicitly de-rated.
- **No question in this pilot carries a Medium or lower rating**, because questions that could not be grounded verbatim were dropped rather than written down-rated. They are logged in §6.

| # | Question ID | Citation | What's tested | Confidence |
|---|---|---|---|---|
| 1 | `registerpflicht-01` | Art. 28(3) subparas 1–2 DORA | Register covers **all** ICT service arrangements, not only critical ones; maintained at entity **and** sub-consolidated **and** consolidated level; criticality governs documentation, not inclusion | High — verbatim (EN + DE) |
| 2 | `registerpflicht-02` | Art. 28(3) subparas 3, 4, 5 DORA (+ Art. 31(10) in the explanation) | **The three separate supervisory duties**, and that none of them is an express annual full-register submission — see §4.1 | High — verbatim + synthesis (three subparagraphs read verbatim in both languages) |
| 3 | `registerpflicht-03` | Art. 16(1) subpara 1 + Art. 28(2) + Art. 28(3) DORA (+ Art. 2(3)(e)) | Simplified-framework entities and microenterprises are **not** exempt from the register; the Art. 28(2) carve-out is deliberately absent from Art. 28(3) | High — verbatim + synthesis (the argument is an in-text contrast between two paragraphs of the same article) |
| 4 | `registerpflicht-04` | Art. 28(3) subpara 5 DORA (+ Art. 8(1) in the explanation) | Two notification triggers, one of them non-contractual: a function **becoming** critical or important | High — verbatim |
| 5 | `registerstruktur-01` | Art. 28(9) DORA; Implementing Reg. (EU) 2024/2956, title, citation clause, Art. 7, closing formula | Instrument type (ITS not RTS not guideline), adoption date, direct applicability; Art. 28(10) distinguished | High — verbatim |
| 6 | `registerstruktur-02` | Art. 3(1) and Art. 5(1)(a)–(o), Art. 5(2) ITS | Templates are mandatory **for maintaining and updating**, not only for reporting; **15** templates; own additional fields expressly permitted | High — verbatim (the count of 15 is a direct count of the enumerated points (a)–(o), not an external figure) |
| 7 | `registerstruktur-03` | Art. 3(2)(a)–(b) ITS + Annex I, B_05.02 scope list | **The scope asymmetry**: all direct providers vs. only CIF-underpinning subcontractors — see §4.2 | High — verbatim + synthesis (Art. 3(2) and the B_05.02 instructions read together) |
| 8 | `registerstruktur-04` | Art. 4(1)–(3) ITS + Annex I, B_02.02.0150/0160 | One value per data element; extra **rows**, never comma-lists or extra columns | High — verbatim |
| 9 | `lieferkette-01` | Art. 1(2)–(3) and Art. 2 ITS + Annex I, B_05.02 | Definition and mechanics of `rank`; rank ≠ criticality; equal positions share a rank | High — verbatim |
| 10 | `lieferkette-02` | Annex I, B_02.01 chapeau and B_05.02 instructions ITS | Three-tier chain: shared contract reference number and service type, ranks 1/2/3, mandatory back-reference to the recipient at rank *n*−1, **no** reference number for provider-to-subcontractor arrangements | High — verbatim + synthesis (two template instruction blocks) |
| 11 | `lieferkette-03` | Art. 3(5)–(6) ITS + Annex I, B_05.01.0020 | LEI/EUID duty extends **through** the direct provider to CIF-underpinning subcontractors; non-EU legal persons: **LEI only** | High — verbatim |
| 12 | `lieferkette-04` | Annex I, B_05.02 scope point (d) ITS (+ B_02.03, B_07.01, recital 5) | The intra-group rule: **at least the first extra-group subcontractor even where the service is non-critical** — see §4.3 | High — verbatim + synthesis (the operative sentence is verbatim; recital 5 is used only for the rationale, flagged in the explanation) |
| 13 | `funktionen-01` | Art. 3(22) and Art. 3(23) DORA | CIF is impact-based, not spend/headcount/GDPR-based; CIF classification (entity's own) vs. CTPP designation (ESAs', Art. 31) | High — verbatim (EN + DE, both definitions read side by side) |
| 14 | `funktionen-02` | Annex I, B_06.01 instructions ITS (+ Annex II, recital 8) | Function identifier is unique per **LEI × licenced activity × function name**; the ITS's own worked example | High — verbatim |
| 15 | `funktionen-03` | Annex I, B_06.01 ITS **as corrected by OJ L, 2025/90725** | Three-option closed list incl. "Assessment not performed"; `9999-12-31` explicit-nil convention; RTO/RPO in whole hours with `1`/`0` conventions | High — verbatim (read in both the original OJ and the corrected consolidated text, EN + DE) |
| 16 | `funktionen-04` | Annex I, B_07.01.0070 ITS (+ B_07.01.0050/0080/0110) | **What the "date of last audit" column excludes**: third-party certifications, provider internal audit reports, annual monitoring dates, risk-assessment review dates | High — verbatim (the exclusion is an express sentence in the instruction, not an inference) |
| 17 | `datenqualitaet-01` | Art. 3(3)–(4) ITS (+ recital 12) | The six data-quality principles, verbatim and in order; regular review + prompt correction duty | High — verbatim |
| 18 | `datenqualitaet-02` | Art. 6(1)–(2) and Art. 3(3) subpara 2 ITS; **recital 2** | Group registers: parent scopes it, sub-consolidated/consolidated register covers all financial entities *and* ICT intra-group service providers; a single register is possible but does not transfer the obligation | High — verbatim + synthesis, **with an express recital caveat**: the single-register *option* is stated in recital 2, and the question's explanation says so. The answer key does not depend on the recital — Art. 6(2) and Art. 3(3) subpara 2 alone dispose of distractors (a), (b) and (d) |
| 19 | `datenqualitaet-03` | Annex III ITS (+ Art. 3(21) DORA) | Closed list **S01–S19**, identifier only; three separate cloud codes; S13 excludes SaaS; analogue telephony excluded | High — verbatim (the count of 19 is stated in Annex III's own opening sentence: "only the identifier (from S01 to S19)") |
| 20 | `datenqualitaet-04` | Annex I, B_02.01 and B_02.02 instructions ITS | **Conditional mandatoriness**: B_02.01 unconditional for every contract; notice periods / governing law / country of provision / storage flag only "mandatory if the ICT service is supporting a critical or important function" | High — verbatim |

**Tier A — verbatim, single instrument-location, lowest review burden (14):** 1, 4, 5, 6, 8, 9, 11, 13, 14, 15, 16, 17, 19, 20.
**Tier B — verbatim but combining provisions; reviewer should check the combination, not the text (6):** 2, 3, 7, 10, 12, 18.
**Tier C — any claim resting on a secondary source: none.** No question's correct answer, and no distractor's wrongness, depends on an ESA FAQ, a national-authority notice or a vendor summary.

**Secondary/practical-guidance source consulted but deliberately quarantined.** The ESAs' *DORA Register of Information reporting FAQ* (version 14 February 2025, hosted on the EBA website) states that in 2025 registers were to be submitted by 30 April 2025 with a 31 March 2025 reference date, and that **from 2026 the deadline is 31 March each year with a reference date of 31 December of the preceding year**, in **plain-CSV** files delivered as `.zip` per ESA naming conventions; national notices (e.g. DNB's "Reporting DORA registers of information in March 2026", CSSF's eDesk opening on 11 February 2026) are consistent with this. This is **operational supervisory guidance, not law**, and it is used in this dossier and in exactly one question explanation (question 2, labelled *"Praxishinweis, kein Verordnungsinhalt" / "Practice note, not law"*) purely to stop learners concluding that "no annual submission duty in the text" means "nobody will ask you for the register in March". **No question's correct answer depends on it**, and it is therefore Tier C-free by construction.

## 3. Deliberate non-assertions — what the distractors are built to punish

Recorded explicitly so no scale-up quietly reintroduces them.

1. **"DORA Art. 28(3) requires annual submission of the full register."** It does not say that. Question 2's distractor (a) is exactly this sentence. See §4.1.
2. **"The register only covers critical or important functions."** Question 1 distractor (b). Art. 28(3) subpara 1 says "all contractual arrangements".
3. **"Small entities under the simplified framework are exempt."** Question 3 distractors (a) and (b). Art. 16(1) disapplies Articles 5–15 only.
4. **"The 250-employee SME threshold matters here."** Question 3 distractor (d). It appears nowhere in Art. 28.
5. **"Every subcontractor at every tier must be in the register."** Question 7 distractor (a). Only CIF-underpinning ones — but for those, without a depth limit.
6. **"Subcontractors aren't in the register because there's no contract with them."** Question 7 distractor (d) — the mirror-image error, and the more common one in first-year programmes.
7. **"Intra-group arrangements are out of register scope."** Question 12 distractor (c). They get their own reconciliation template (B_02.03) *and* an extra-strict subcontractor rule.
8. **"A received SOC 2 / ISAE 3402 report is our last audit date."** Question 16 distractors (a) and (c). The instruction excludes this in terms.
9. **"Leave the criticality field blank if we haven't assessed it."** Question 15 distractors (b) and (c). The closed list has an explicit "Assessment not performed" value, and the date field has an explicit `9999-12-31` nil.
10. **"The ITS prescribes a file format."** It prescribes none — no occurrence of "CSV", "XBRL", "zip", "XML" or "Excel" anywhere in the instrument. Stated in question 8's explanation.
11. **"There is a defined total field count for the register."** There is not — see §4.4. No question asserts one.
12. **"Criticality decides whether a contract goes in the register."** Question 20's whole point: it decides *how many fields* per contract, not *whether*.

## 4. Findings where existing research / shipped content is imprecise against the primary text

The task asked me to check the brief rather than confirm it. Four findings, one of them material.

### 4.1 The roadmap's "annual mandatory register submission" is not what Art. 28(3) says — and this is the module's most valuable correction

The project's roadmap doc `claude/dora-cra-b2b-training-roadmap-2026-08-16.md` frames module 4 as *"annual mandatory register submission, Nth-party/subcontractor chain mapping, critical-vs-non-critical function classification"*. Two of those three hold up cleanly (see §4.2, §4.3). The first does not, as a statement of what the Regulation requires.

**What Art. 28(3) actually contains, read in full, EN and DE:**

- **Subpara 1** — maintain and update the register, at entity, sub-consolidated and consolidated levels, for **all** ICT service arrangements.
- **Subpara 2** — document the arrangements appropriately, **distinguishing** CIF-supporting from non-CIF-supporting ones.
- **Subpara 3 — the only "yearly" duty in the paragraph, and it is not the register:** *"Financial entities shall report **at least yearly** to the competent authorities on **the number of new arrangements** on the use of ICT services, **the categories** of ICT third-party service providers, **the type** of contractual arrangements and **the ICT services and functions** which are being provided."* DE: *"Finanzunternehmen erstatten den zuständigen Behörden **mindestens einmal jährlich Bericht zur Anzahl neuer Vereinbarungen** …"*. This is a **four-item aggregate report**, not the register. Art. 31(10) confirms the design: competent authorities transmit *"the reports referred to in Article 28(3), third subparagraph"* to the Oversight Forum "on a yearly and aggregated basis".
- **Subpara 4** — *"Financial entities shall make available to the competent authority, **upon its request**, the full register of information or, as requested, specified sections thereof …"*. On request. Not on a calendar.
- **Subpara 5** — timely notification of planned CIF arrangements and of a function **becoming** critical or important.

**Full-text negative checks performed on the primary texts:**

| Check | Result |
|---|---|
| `"register of information"` in the DORA enacting terms | 3 hits — Art. 28(3) subpara 1, Art. 28(3) subpara 4, Art. 28(9). **None imposes an annual submission of the full register.** (Plus 2 recital hits, 149 and 219; recital 149 likewise says supervisors "should be able to request the full register".) |
| `"at least yearly"` in DORA | 7 hits, all located: Art. 8(1), Art. 8(2), Art. 8(7), Art. 11(6)(a), Art. 13(5), Art. 24(6), Art. 28(3) subpara 3. The Art. 28 hit is the aggregate report, **not** the register. |
| `"annual"` / `"yearly"` in Implementing Reg. (EU) 2024/2956 | 9 hits, none of them a submission cadence: recital 1 (the ESAs' **annual CTPP designation** process), `B_01.02` (total assets from the annual financial statement), the `B_02.01.0050` / `B_05.01.0100` **annual expense** columns, and the `B_07.01.0070` instruction that expressly **excludes** "the annual monitoring date of the arrangement" from the audit-date column. |
| `"31 March"`, `"30 April"`, `"deadline"`, `"shall submit"` in the ITS | **0 hits.** |
| `"CSV"`, `"XBRL"`, `"zip"`, `"XML"`, `"Excel"`, `"xlsx"` in the ITS | **0 hits.** |

**Conclusion.** The annual full-register collection is real — competent authorities do run it, on a 31 March cycle from 2026 with a 31 December reference date (ESA FAQ, secondary) — but its legal footing is Art. 28(3) subpara 4's "upon its request" plus the ESAs'/NCAs' reporting arrangements, **not** an express periodic-submission rule in DORA or in the ITS. **Recommended wording for marketing and course copy:** "the annual register submission your supervisor runs" — never "the annual submission DORA requires in Art. 28(3)". A compliance officer trained on the second phrasing will cite a provision that does not say it, in front of an auditor, which is the precise failure mode this module exists to prevent. Question 2 is built on this and is `high_stakes`; the correct answer is the option that enumerates all three duties.

### 4.2 "Nth-party / subcontractor chain mapping" is right, but the roadmap omits the scope filter that halves the work

The roadmap's second bullet is accurate as far as it goes, but a programme scoped from that phrase alone will over-build. Art. 3(2) ITS sets **two requirements of different breadth**: point (a) "the relevant information in relation to **all** the ICT services provided by **direct** ICT third-party providers"; point (b) "information on **all subcontractors that effectively underpin ICT services supporting critical or important functions or material parts thereof**". The Annex I B_05.02 instructions define "effectively underpin" as "all the subcontractors providing ICT services whose disruption would impair the security or the continuity of the service provision", and recital 6 confirms that the drafters deliberately limited subcontractor recording to that set to keep the exercise proportionate.

So: **direct providers — everything; subcontractors — CIF chains only, but those to unlimited depth.** Both common project scopings ("map the whole supply base" and "map tier 1 only") are wrong, in opposite directions. Question 7 tests this and is `high_stakes`.

### 4.3 "Critical-vs-non-critical function classification" holds up — with one addition the roadmap does not mention

Verified: Art. 3(22) DORA is impact-based and the classification is the entity's own, distinct from the ESAs' Art. 31 CTPP designation (Art. 3(23)). The ITS operationalises it in `B_06.01` (three-option assessment column plus `9999-12-31` nil-date) and `B_07.01` (CIF-only assessment template).

What the roadmap misses is that the classification has a **statutory review cadence that is genuinely annual** and is *not* the register submission: **Art. 8(1) DORA** requires entities to *"review as needed, and at least yearly, the adequacy of this classification and of any relevant documentation"* for all ICT supported business functions. That is the annual duty in this area that the text actually contains, and it is a much better hook for the "annual pain point" sales argument than the submission framing in §4.1. It is cited in question 4's explanation.

### 4.4 The shipped `dora_pilot.json` register question survives — but is thin in three specific ways

`dora-drittparteien-01` in `data/dora_pilot.json` asks what entities must maintain and keep current, with correct answer (b) "Ein Informationsregister (Register of Information) über alle vertraglichen Vereinbarungen mit IKT-Drittanbietern". **The answer key is correct and the option is a fair paraphrase of Art. 28(3) subpara 1** — including the "über alle" scope, which is the part most summaries get wrong. Distractor (d) ("a register only for non-EU providers") is a good one. No correction to the key is needed. Three refinements are worth logging:

1. **The explanation omits the three-level requirement.** It reads only "Art. 28 Abs. 3 verlangt ein aktuell gehaltenes Register aller IKT-Drittanbieter-Verträge". The DE OJ text says the register is kept *"auf Unternehmensebene sowie auf teilkonsolidierter und konsolidierter Ebene"*. For a general-staff module that omission is defensible; for consistency with this module it is worth one clause.
2. **Terminology drift, same finding as the `dora_procurement` dossier §4.3.** The official DE OJ term throughout Art. 28 and throughout Implementing Reg. (EU) 2024/2956 is **"IKT-Drittdienstleister"**; the shipped `dora_pilot.json` uses "IKT-Drittanbieter". The official DE term for the register is **"Informationsregister"** (which the shipped question does use). This draft uses OJ terminology throughout.
3. **The explanation's "eine zentrale Grundlage für die aufsichtliche Überwachung" is right but under-specific**, and could cheaply name the actual mechanism now that it is verified: ITS recital 1 states the register's information is essential for the entity's own ICT risk management, for supervision by competent authorities, for the Lead Overseer's oversight, **and for the ESAs' annual CTPP designation process**.

These are logged, not fixed — changing shipped content is out of scope here and should be a separate, deliberately reviewed edit.

### 4.5 Field-count and template-count claims in circulation

There is **no total field count stated anywhere in Implementing Regulation (EU) 2024/2956**, and any "the register has N fields" figure in vendor material is a count somebody performed, not a regulatory figure. Two counts *are* defensible and both are used in this pilot:

- **15 templates** — a direct count of Art. 5(1) points (a) to (o), which name them individually (question 6).
- **19 ICT service types (S01–S19)** — stated in Annex III's own opening sentence (question 19).

For the record, a programmatic count of distinct column codes in the corrected consolidated text gives 123 across all 15 templates, but that figure is fragile (it includes the `B_99.01` row codes, and is inflated by the residual `B_06.01.0110` cross-reference noted above), so **no question asserts it** and neither should any course copy.

## 5. Gap list — covered by the primary sources but deliberately **not** tested by this 20-question pilot

1. **Templates `B_01.03` (branches), `B_03.01`, `B_03.02`, `B_03.03` (signing entities) and `B_04.01` (entities using the services).** Read in full; not tested. Together they are the register's "who signed what for whom" layer, and the sub-consolidated case where the signing entity is not the using entity is a genuine trap. Prime candidates for the 40-question scale-up.
2. **Template `B_99.01` in its own right.** Read; only referenced inside other explanations. The obligation to publish your own definitions of "Low/Medium/High" is unusual and worth a dedicated question later.
3. **Annex II (licenced activities per entity type) and Annex IV (how to report total assets per entity type).** Both read in full; both are sector-specific lookup annexes, and testing them properly means testing 22 entity types. Referenced in question 14's explanation only.
4. **The 22-value closed list of entity types in `B_01.01.0040` / `B_01.02.0040`,** and the "other financial entity" fallback for a holding company that maintains a group register without itself being a financial entity. Read; untested.
5. **`B_02.02.0090` termination-reason closed list** (6 options, including "termination following a request by a competent authority"). Read; untested. It is a good scale-up item because it is the register's only backward-looking enforcement signal.
6. **Art. 29 DORA concentration-risk assessment.** Not tested. The register feeds it (`B_07.01` substitutability mirrors the Art. 31(2)(d) parameters almost word for word), but the assessment itself belongs to a risk module, and the sibling `dora_procurement` pilot already flags Art. 29 as its own gap.
7. **Art. 31–44 CTPP oversight mechanics.** Out of scope by design. Question 13 tests only the CIF/CTPP *distinction*.
8. **The ESA submission mechanics** — 31 March cycle, 31 December reference date, plain-CSV in `.zip`, national portals (DNB, CSSF, BaFin). **Deliberately untested**, because a correct answer would rest wholly on secondary guidance and would therefore be Tier C under the rule in §2. If the product owner wants this taught — and for this audience there is a real argument that it must be — it should be a **clearly separated, explicitly-labelled "supervisory practice" section** with its own review and its own currency-check cadence, not mixed into the statutory question pool.
9. **National implementation and supervisory specifics.** Nothing German-, Polish- or Romanian-specific is asserted anywhere in this pilot, even though the roadmap targets DE/EN/PL/RO for this module. That is the safe state; PL/RO localisation will need a national-notice layer that this dossier does not cover.
10. **Interaction with the Art. 30 contract-content catalogue.** Several register columns (notice periods, governing law, data locations, exit plan existence) are effectively evidence that the Art. 30 clauses were negotiated. That linkage is real and commercially interesting, but module 2B owns Art. 30 and this pilot deliberately stays inside the register's own instructions to avoid two modules teaching the same clause differently.
11. **Delegated Regulation (EU) 2025/532 (subcontracting RTS).** Read for the sibling `dora_procurement` dossier, **not re-read for this one**, and therefore not cited here even though its subcontracting-chain concepts sit adjacent to `B_05.02`. Flagged rather than assumed.

## 6. Questions considered and dropped (grounding failures, logged rather than written)

Per the brief's instruction not to write anything I cannot ground in verbatim primary text:

- **"By when must the register be submitted?"** — dropped. Any correct answer is ESA/NCA guidance, not regulation. Became gap 8 and, in inverted form, question 2.
- **"In what file format is the register submitted?"** — dropped, same reason. The ITS is silent; the point survives only as a negative statement inside question 8's explanation.
- **"How many data fields does the register contain?"** — dropped. No such figure exists in the instrument; see §4.4.
- **"How deep must subcontractor mapping go in tiers?"** — dropped as a *numeric* question. The ITS sets a functional test ("effectively underpin"), not a tier limit; the functional test is tested instead in questions 7 and 10.
- **"What penalty applies for a defective register?"** — dropped. DORA sets no EU-wide amount (established in the `dora_executive` dossier §3.1/§3.3 and not re-litigated here); anything specific would be national law not read today.
- **"Does the ECB/SSM impose additional register requirements for significant institutions?"** — dropped. Not read; would be Tier C.

## 7. Module metadata as drafted

- Module id: `dora_register` · file: `data/dora_register_pilot_DRAFT.json` · **20 questions** · DE canonical + EN
- `class: "ALL"` in meta; `class_scope: ["ALL"]` and `roles: ["all"]` on every question
- **Topic codes (5 × 4):** `registerpflicht` (Registerpflicht und Meldewege), `registerstruktur` (Aufbau und Vorlagen des Informationsregisters), `lieferkette` (IKT-Dienstleistungskette und Unterauftragnehmer), `funktionsklassifizierung` (Funktionsklassifizierung und Bewertung), `datenqualitaet` (Datenqualität, Identifikatoren und Konsolidierung)
- **Points:** 12 × 4 points, 8 × 3 points — matching the `kartellrecht_pilot.json` scale
- **`high_stakes: true` on 8 questions** (2, 3, 7, 10, 12, 15, 16, 20) — the ones where a wrong answer produces either a false statement to a supervisor or a structurally defective register
- **`grundstoff: true` on 5** — one anchor question per topic (1, 5, 9, 13, 17)
- **Answer key distributed exactly 5 × a / 5 × b / 5 × c / 5 × d**; verified programmatically, as is the option-set integrity (`{a,b,c,d}` in both locales) and the ID uniqueness
- **Schema parity verified programmatically** against `data/kartellrecht_pilot.json`: identical question-object key list *and* order
- `meta.legal_disclaimer` carries the user's boilerplate verbatim: *"Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall durch qualifizierte Juristen oder Wirtschaftsprüfer zu validieren."*
- `meta.renewal_months: null`, `renewal_basis: "not_specified_in_statute"` — with a note distinguishing the two genuine yearly duties in the text (Art. 28(3) subpara 3 aggregate report; Art. 8(1) classification review) from a training cadence, which neither instrument fixes
- `meta.legal_review_status` records the primary-source verification, names the CELEX identifiers and the corrigendum, and points back to this dossier

## 8. Open items before this could move toward `data/dora_register_pilot.json`

1. **Human legal review.** Highest-value use of a reviewer's hour, in order: **§4.1** (the annual-submission finding — it is the module's commercial hook and its biggest correction), then Tier B questions 2, 3, 7, 10, 12, 18, then question 18's recital-based element.
2. **Product decision on §4.1's downstream effect.** If any existing marketing, roadmap copy or course prose says "DORA requires annual submission of the register", it should be reworded. The roadmap doc `claude/dora-cra-b2b-training-roadmap-2026-08-16.md` is the source of the phrasing in this project and is the place to fix it.
3. **Decide whether to teach the supervisory submission mechanics at all** (gap 8). Recommendation: yes, but in a separately-labelled, separately-reviewed practice annex with an explicit "verify before each cycle" note — never inside the statutory question pool.
4. **Decide whether to correct the shipped `dora` module** per §4.4 (three-level clause + "IKT-Drittdienstleister" terminology). Same decision as the `dora_procurement` dossier raised; doing both at once is cheaper.
5. **Role vocabulary.** All 20 questions carry `roles: ["all"]`. The app's existing role vocabulary is `all`, `all_staff`, `management`, `hr`, `it`, `finance` — there is no `compliance`, `controlling` or `pmo`. Three modules now (2B, 1A, 4) have audiences the vocabulary cannot express; worth resolving once, as a product decision, rather than per module.
6. **Module wiring.** Not done, by design: `build_modules.py`, `modules_manifest.json` and `app.js` untouched, no build run, nothing git-added. `pass_rule_note` proposes no exam-config numbers; the 4/4/4/4/4 topic split suggests a 5-question draw touching every topic, but that is a design decision.
7. **Locale scope.** DE canonical + EN only. The roadmap targets DE/EN/PL/RO for this module; PL and RO must be sourced from the **Polish and Romanian OJ versions** of both instruments, not machine-translated from the DE — the ITS column names in particular are legally defined terms in each language version.
8. **Regulatory currency.** The ITS is recent and has already been corrected once (Sept 2025). Before any production release, re-confirm that no further corrigendum, amending implementing regulation or ESA reporting-framework change has landed since 2026-08-16 — and specifically re-check the `B_06.01` column numbering, which is the item most likely to move again.

---

**Reminder:** this document and the accompanying JSON are draft training-content groundwork. They are not legal advice, have not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review.
