# DORA Art. 30 procurement module (`dora_procurement`) — draft pilot content + pre-review dossier (2026-08-16)

**Status:** AI-prepared groundwork only — **NOT legal advice**. Attorney sign-off required before any commercial/production use. The draft question file exists at `data/dora_procurement_pilot_DRAFT.json` and is **deliberately not wired into the live app**: it is not registered in `data/build_modules.py` or `data/modules_manifest.json`, no build step was run, and nothing was staged or committed.

**Subject:** 20-question DE/EN draft pilot for a new module, **"DORA Art. 30 — IKT-Drittparteienrisiko und Beschaffung"** (internal working name `dora_procurement`). Target audience: IT procurement, vendor management, and in-house legal at EU financial entities who negotiate contracts with ICT service providers (cloud, SaaS, software houses). Schema follows `data/kartellrecht_pilot.json` field-for-field (verified: identical question-object key set and key order). Same pilot-then-scale discipline as `kartellrecht_pilot.json`, `kyc_aml_pilot.json`, `lksg_pilot.json`, `dora_pilot.json`: 20 questions DE/EN pilot → 40 questions/12 locales only after sign-off.

**Method — and how it differs from the 2026-08-13 DORA dossier.** The predecessor dossier `dora-pilot-pre-review-dossier-2026-08-13.md` verified its citations **only against secondary legal-analysis sources** (Springlex, regulation-dora.eu, digital-operational-resilience-act.com) and explicitly recommended a primary-source re-check. **That re-check was performed for this module.** Every citation below was read on 2026-08-16 in the **official Official Journal text**, in both the English and the German language versions, and in the two relevant Level 2 delegated regulations in full:

| Instrument | CELEX | OJ reference | What it is |
|---|---|---|---|
| Regulation (EU) 2022/2554 (DORA) | `32022R2554` | OJ L 333, 27.12.2022, p. 1 | Base regulation (Art. 3, 28, 29, 30 read verbatim, EN + DE) |
| Commission Delegated Regulation (EU) 2024/1773 | `32024R1773` | OJ L, 25.6.2024 | RTS under the **Art. 28(10)** mandate — detailed content of the policy on ICT services supporting critical or important functions. **Art. 8 "Contractual clauses", Art. 9 "Monitoring", Art. 10 "Exit"** read in full |
| Commission Delegated Regulation (EU) 2025/532 | `32025R0532` | OJ L, 2.7.2025 | RTS under the **Art. 30(5)** mandate — elements to determine and assess when subcontracting ICT services supporting critical or important functions. **All 7 articles read in full** |

**Retrieval note (methodological transparency).** The `eur-lex.europa.eu` web UI is behind an AWS WAF JavaScript challenge and returned HTTP 202 with an empty body to every direct request; the WebFetch path reached the page but only rendered the recitals, not the enacting articles. The article text was therefore retrieved from **`publications.europa.eu/resource/celex/<CELEX>`** — the EU Publications Office **Cellar** repository, which is the authoritative machine-readable source serving the same Official Journal document that EUR-Lex renders. Content-type `application/xhtml+xml`, `Accept-Language: eng` and `deu`. This is a primary source, not a mirror or a summary, but a reviewer who wants belt-and-braces can re-confirm against the EUR-Lex HTML in a normal browser.

**Level 2 answer to the open question in the 2026-08-13 dossier:** yes, a finalised RTS specifically elaborating Art. 30 contractual content **does** exist, and there are in fact **two** relevant instruments, both adopted and published, not drafts. This is exactly the RTS-level detail the previous dossier flagged as typically missing from secondary sources.

---

## 1. Why this module

The shipped `dora` module treats third-party risk as one topic out of five (`drittparteien-01` … `-04`, four questions). That is right for an all-staff awareness module under Art. 13(6), but it is far too shallow for the audience this module targets: the people who actually sit across the table from a hyperscaler's contracts team. Art. 30 is unusual among compliance obligations in that it is **directly operationalisable as a clause checklist** — the regulation names the required contract contents letter by letter — which makes it unusually well-suited to scenario-based assessment.

Three design decisions follow from the primary-source read:

1. **The Art. 30(2) / Art. 30(3) tier split is the spine of the module.** It is the single most legally load-bearing distinction here, and it is the one most often blurred in secondary material (including, as noted in §4 below, in this project's own shipped content). Two questions test it head-on (`pflichtklauseln-01`, `kritische-funktionen-02`), both marked `high_stakes`.
2. **Four questions are vendor-pushback scenarios** (`kritische-funktionen-03`, `kritische-funktionen-04`, `auditrechte-03`, `subunternehmer-02`), matching the project's established scenario style and the real friction points procurement teams hit: best-effort SLAs, 30-day-export-only "exit", certification-instead-of-audit, and free subcontractor substitution.
3. **Level 2 detail is included where it changes the answer.** The certification-versus-audit question is unanswerable from the base regulation alone; Art. 8 of Delegated Regulation (EU) 2024/1773 is what actually resolves it. Same for subcontractor change control (Art. 5 of 2025/532).

## 2. Citation ledger (primary-source verified 2026-08-16)

Confidence scale used here is stricter than the 2026-08-13 dossier's, because the sourcing is stronger. **"High — verbatim"** means the tested proposition is a direct restatement of wording I read in the OJ text of the cited provision, in both EN and DE. **"High — verbatim + synthesis"** means every element is verbatim but the question combines two provisions I read. **"Medium"** would mean inference beyond the text — **no question in this pilot carries a Medium or lower rating**, because questions I could not ground verbatim were dropped rather than written (see §5).

| # | Question ID | Citation | What's tested | Confidence |
|---|---|---|---|---|
| 1 | `grundsaetze-01` | Art. 30(1) Reg. (EU) 2022/2554 | Rights/obligations clearly allocated and set out in writing; full contract includes the SLAs; documented in **one** written document available on paper or in another downloadable, durable and accessible format | High — verbatim |
| 2 | `grundsaetze-02` | Art. 28(1)(a) Reg. (EU) 2022/2554 | Financial entity remains **"at all times" fully responsible**; outsourcing does not transfer regulatory responsibility | High — verbatim |
| 3 | `grundsaetze-03` | Art. 28(4) Reg. (EU) 2022/2554 | The five mandatory pre-contract steps (CIF assessment, supervisory conditions, all relevant risks incl. concentration risk per Art. 29, due diligence/suitability, conflicts of interest) | High — verbatim (all five points (a)–(e) read) |
| 4 | `grundsaetze-04` | Art. 30(4) Reg. (EU) 2022/2554 | Public-authority standard contractual clauses: parties shall **"consider"** their use — a duty to engage, not to adopt | High — verbatim; the DE text ("erwägen") confirms the EN "consider" |
| 5 | `pflichtklauseln-01` | Art. 30(2) Reg. (EU) 2022/2554 | The nine-point baseline catalogue applies to **all** ICT service contracts, not only critical ones | High — verbatim (chapeau of Art. 30(2) is unqualified) |
| 6 | `pflichtklauseln-02` | Art. 30(2)(b) Reg. (EU) 2022/2554 | Locations at **region/country** granularity, incl. storage location, incl. subcontracted parts, plus advance notification of envisaged location change | High — verbatim; the regulation defines its own granularity ("namely the regions or countries") |
| 7 | `pflichtklauseln-03` | Art. 30(2)(f) Reg. (EU) 2022/2554 | ICT incident assistance **at no additional cost, or at a cost determined ex-ante** — the two-model structure | High — verbatim |
| 8 | `pflichtklauseln-04` | Art. 30(2)(d) Reg. (EU) 2022/2554 | Access, recovery and return of personal and non-personal data in an **easily accessible format**, on insolvency / resolution / discontinuation / termination | High — verbatim |
| 9 | `pflichtklauseln-05` | Art. 30(2)(i) + Art. 13(6) Reg. (EU) 2022/2554 | Contract must set conditions for the **provider's participation in the entity's** awareness/resilience training (direction of the obligation is the tested point) | High — verbatim (Art. 30(2)(i) cross-refers to Art. 13(6) on its face) |
| 10 | `kritische-funktionen-01` | Art. 3(22) Reg. (EU) 2022/2554 | Legal definition of "critical or important function" — impact-based, not value/headcount-based; and its independence from the Art. 3(23)/Art. 31 **CTPP** designation | High — verbatim (both definitions read side by side) |
| 11 | `kritische-funktionen-02` | Art. 30(2) and (3) Reg. (EU) 2022/2554 | **The tier split.** Which contents are Art. 30(3)-only (audit rights, exit strategy, contingency plans, precise SLA targets) versus baseline | High — verbatim (full enumeration of both paragraphs read; see §4) |
| 12 | `kritische-funktionen-03` | Art. 30(3)(a) Reg. (EU) 2022/2554 | **Precise quantitative and qualitative performance targets** required for CIF contracts; best-effort SLA insufficient; DORA prescribes no specific availability figure | High — verbatim, incl. the stated purpose clause (effective monitoring / corrective action without undue delay) |
| 13 | `kritische-funktionen-04` | Art. 30(3)(f) + Art. 28(8) Reg. (EU) 2022/2554 | Exit strategy = **mandatory adequate transition period with continued service provision**, not merely a data export; "adequate" is relative, no fixed duration in the text | High — verbatim + synthesis (Art. 28(8) read separately for the exit-plan quality requirements) |
| 14 | `auditrechte-01` | Art. 30(3)(e)(i) Reg. (EU) 2022/2554 | Three right-holders (entity, appointed third party, competent authority); on-site copy right; anti-hollowing-out clause | High — verbatim |
| 15 | `auditrechte-02` | Art. 30(3)(e)(i)–(ii) + Art. 28(6) Reg. (EU) 2022/2554 | **What "unrestricted" actually means** — see §4 for the full finding | High — verbatim + synthesis (three provisions read) |
| 16 | `auditrechte-03` | Art. 30(3)(e) DORA + **Art. 8(2)–(3) Del. Reg. (EU) 2024/1773** | Certifications/provider audit reports are permissible assurance methods under conditions; **no sole reliance over time**; entity must retain contractual right to individual and pooled audits at its discretion | High — verbatim (Art. 8 read in full; the four methods and the eight conditions are enumerated in the RTS) |
| 17 | `auditrechte-04` | Art. 30(3) subpara. 2 + Art. 3(60) Reg. (EU) 2022/2554 | **Microenterprise-only** derogation allowing delegation of audit rights to a provider-appointed independent third party; precise microenterprise definition (<10 persons, ≤ EUR 2m, excl. trading venues/CCPs/TRs/CSDs) | High — verbatim (derogation subparagraph and Art. 3(60) both read) |
| 18 | `subunternehmer-01` | Art. 30(2)(a) DORA + **Art. 3(1) Del. Reg. (EU) 2025/532** | Contract must state **whether** CIF subcontracting is permitted and on what conditions; silence is not an option; the ten pre-contract conditions in the RTS | High — verbatim (all ten points (a)–(j) of RTS Art. 3(1) read) |
| 19 | `subunternehmer-02` | **Art. 5 Del. Reg. (EU) 2025/532** + Art. 30(5) DORA | Material subcontracting changes: inform well in time → reasonable notice period → **approve-or-object before implementation**; plus the Art. 6 termination right | High — verbatim (RTS Art. 5 and Art. 6 read in full) |
| 20 | `subunternehmer-03` | **Art. 3(1)(d) and Art. 4(1)(j) Del. Reg. (EU) 2025/532** + Art. 30(3)(e) DORA | Subcontractor must grant the entity and competent/resolution authorities the **same** access/inspection/audit rights; pass-through via the contract chain, no direct contract needed | High — verbatim (both RTS provisions cross-refer expressly to Art. 30(3)(e) DORA) |

**Tier A (verbatim single-provision reads, lowest review burden):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 17, 18.
**Tier B (verbatim but combining two or more provisions — reviewer should confirm the combination is a fair statement, not the underlying text):** 11, 13, 15, 16, 19, 20.
**Tier C (numeric/procedural claims sourced only from secondary summaries):** **none.** This pilot contains no hour-counts, deadlines, or dates of the kind that made items 10, 11 and 15 of the 2026-08-13 dossier the highest-risk entries. The only numbers asserted anywhere are the microenterprise thresholds in `auditrechte-04`, taken verbatim from Art. 3(60).

## 3. Deliberate non-assertions (things the questions are careful *not* to say)

These are places where a plausible-sounding claim would have been wrong, and the distractors are built to punish it:

- **DORA does not prescribe an availability percentage.** `kritische-funktionen-03` has "99.9% minimum for core banking systems" as a distractor precisely because that is a common and false intuition. The requirement is a property of the clause (precise, quantitative *and* qualitative), not a level.
- **DORA does not prescribe an exit transition-period duration.** `kritische-funktionen-04` has "at least 24 months" as a distractor. The text says "adequate", measured against service complexity.
- **DORA does not mandate use of standard contractual clauses.** `grundsaetze-04` tests the "consider" wording specifically.
- **Incident assistance need not be free.** `pflichtklauseln-03` includes "must always be entirely free of charge" as a distractor; Art. 30(2)(f) permits ex-ante determined cost.
- **The general SME 250-employee threshold does not apply.** `auditrechte-04` includes it as a distractor against the Art. 3(60) microenterprise definition.

## 4. Findings where existing research/content is imprecise against the actual regulation text

This is the section the task specifically asked for, and there are three real findings.

### 4.1 The "unrestricted audit and access right" claim — literally supported, materially over-read

The prior Gemini-generated market research claims financial entities get an "unrestricted audit and access right". **The word is genuinely in the regulation** — Art. 30(3)(e)(i) EN reads "unrestricted rights of access, inspection and audit", DE "uneingeschränkte Zugangs-, Inspektions- und Auditrechte". So the claim is not fabricated. But as a standalone statement it is materially misleading in **four** ways, all visible in the primary text:

1. **It is a critical-tier right, not a general one.** It sits in Art. 30(3), which applies only to contracts on ICT services supporting critical or important functions. There is no audit right at all in the Art. 30(2) baseline. A blanket "DORA gives you unrestricted audit rights over ICT vendors" is wrong for the majority of a typical vendor portfolio.
2. **"Unrestricted" is defined by its own closing clause, and that clause is narrower than the adjective sounds.** The provision continues: "the effective exercise of which is not impeded or limited by other contractual arrangements or implementation policies." The target is *contractual hollowing-out* — granting an audit right on page 4 and neutering it via a security policy on page 40. It is not a warrant for unannounced entry.
3. **The very next sub-point authorises a negotiated alternative.** Art. 30(3)(e)(ii) grants "the right to agree on **alternative assurance levels** if other clients' rights are affected." That is an express carve-out, drafted into the same list, and it is exactly the ground a multi-tenant cloud provider stands on. Any training that presents the audit right as absolute will get contradicted in the first real negotiation.
4. **The entity's own exercise of the right is constrained by Art. 28(6).** Financial entities "shall, on the basis of a risk-based approach, **pre-determine the frequency** of audits and inspections as well as the areas to be audited", adhering to commonly accepted audit standards. The right must be exercised in a planned, risk-based way — which is close to the opposite of "unrestricted" in colloquial usage.

Plus a fifth, narrower point: Art. 30(3) subparagraph 2 lets a **microenterprise** financial entity delegate those rights entirely to an independent third party appointed *by the provider*.

`auditrechte-02` is written specifically to correct this, and `auditrechte-01` states the right accurately without overstating it. **Recommendation: the phrase "unrestricted audit and access right" should not be used in marketing or course copy without the Art. 30(3)(e)(ii) and Art. 28(6) qualifiers attached.**

### 4.2 The Art. 30(2) baseline is commonly described with Art. 30(3) contents folded in

Several widely circulated summaries — and the framing in the brief for this module — describe the Art. 30(2) baseline as including "service levels with precise targets", "audit rights", and "exit strategies". **None of those three is in Art. 30(2).** Reading the enumerations directly:

- Art. 30(2)(e) requires only "service level descriptions, including updates and revisions thereof". The words "precise quantitative and qualitative performance targets" appear in **Art. 30(3)(a)**, critical tier only.
- **Audit rights do not appear in Art. 30(2) at all.** They are Art. 30(3)(e).
- **Exit strategies do not appear in Art. 30(2) at all.** They are Art. 30(3)(f). (Exit strategies are separately required by **Art. 28(8)**, but again only "for ICT services supporting critical or important functions".)
- Relatedly, the *termination circumstances* often attributed to Art. 30 are in **Art. 28(7)**; Art. 30(2)(h) covers only termination rights and minimum notice periods as a contract content.

What Art. 30(2) *does* contain that is easy to miss: (d) data access/recovery/return on insolvency, and (i) the provider's participation in the entity's training programmes. Both are tested here (`pflichtklauseln-04`, `-05`).

### 4.3 This project's own shipped DORA content carries the same blur — worth a correction pass

Not a defect in this new module, but found while checking, and it affects live content:

- `data/dora_pilot.json`, question `dora-drittparteien-02`, states that Art. 30 requires "eine klare Leistungsbeschreibung, Auditrechte, Bedingungen für Unter-Auslagerung sowie Exit-Strategien" as generic Art. 30 minimum contract elements, with no tier qualifier. Per §4.2 that is imprecise: audit rights and exit strategies are Art. 30(3) only. The answer key is not wrong (the option is still the best of four), but the explanation should gain a tier qualifier.
- `data/dora_course.json`, lesson section `dora-l5-s1`, contains the same sentence in prose form (DE and EN).
- **Terminology drift:** the official German OJ text uses **"IKT-Drittdienstleister"**; the shipped `dora_pilot.json` uses "IKT-Drittanbieter" throughout. The official DE heading for Art. 30 is "Wesentliche Vertragsbestimmungen", and the official DE term for SLAs in this article is "Dienstleistungsgüte". This draft uses the official terminology; the shipped module does not. Aligning them is a small but worthwhile consistency fix, and it matters for a B2B audience that will read the German regulation alongside the course.

These are logged here rather than fixed, since changing shipped content is out of scope for this task and should be a deliberate, separately reviewed edit.

## 5. Gap list — covered by Art. 30 but **not** tested by this 20-question pilot

Written out explicitly so nothing is silently assumed to be covered:

1. **Art. 30(3)(b)** — notice periods and the provider's reporting obligations on developments that might materially impact its ability to deliver. Mentioned inside the `kritische-funktionen-02` enumeration but has no dedicated question.
2. **Art. 30(3)(c)** — the requirement that the provider implement **and test** business contingency plans and maintain ICT security measures, tools and policies. Same status: enumerated, not separately tested. A strong candidate for the 40-question scale-up.
3. **Art. 30(3)(d)** — the provider's obligation to participate and fully cooperate in the entity's **TLPT** under Art. 26–27. Not tested; it sits at the seam between this module and the shipped `dora` module's testing topic, and duplicating it here risks inconsistency between the two modules' framing.
4. **Art. 28(3) — the Register of Information.** Deliberately excluded: it is already covered by `dora-drittparteien-01` in the shipped module, and the ITS templates under Art. 28(9) were not read for this dossier.
5. **Art. 29 concentration risk** in its own right. Referenced inside `grundsaetze-03` via Art. 28(4)(c) but not tested directly; Art. 29(2)'s third-country/insolvency-law considerations are untested.
6. **Art. 31–44 CTPP Oversight Framework.** Out of scope by design — this is a contracting module. `kritische-funktionen-01` tests only the CIF/CTPP *distinction*, not the oversight mechanics.
7. **Delegated Regulation (EU) 2024/1773 Art. 1–7 and 9–10** — governance, life-cycle phases, ex-ante risk assessment, due diligence, conflicts of interest, monitoring, exit planning. Only Art. 8 is tested. Art. 9 (monitoring measures, KPIs, contractual penalties where appropriate) and Art. 10 (documented, periodically tested exit plans) are read and available for the scale-up.
8. **Delegated Regulation (EU) 2025/532 Art. 1 and 2** — the twelve complexity factors and the group-level consistency obligation. Read, not tested.
9. **National/BaFin layer.** Entirely untested. This module covers the EU instrument only; German supervisory practice on ICT contracting is not addressed.
10. **Interaction with GDPR Art. 28 processor contracts.** A genuinely important practical question for this exact audience (the two clause catalogues overlap but are not congruent) — **deliberately not written**, because answering it accurately requires reading GDPR Art. 28 to the same primary-source standard, which was not done today. Flagged rather than guessed.

## 6. Open items before this could move toward `data/dora_procurement_pilot.json`

1. **Human legal review.** This is a first AI pass with strong sourcing, not a lawyer's pass. The highest-value use of a reviewer's time is Tier B (items 11, 13, 15, 16, 19, 20) — the questions that combine provisions — and specifically §4.1, since the audit-rights framing is the module's most commercially quoted claim.
2. **Decide whether to correct the shipped `dora` module** per §4.3 (tier qualifier + "IKT-Drittdienstleister" terminology). Separate, explicit change.
3. **Role vocabulary.** All 20 questions carry `roles: ["all"]`, matching the `kartellrecht_pilot.json` convention. The app's existing role vocabulary across `*_pilot.json` is `all`, `all_staff`, `management`, `hr`, `it`, `finance` — there is **no** `procurement`, `vendor_management`, or `legal` role. Given this module's audience, adding those role values is worth a product decision; it would need a matching change wherever roles are consumed.
4. **Module wiring.** Not done, by design: `build_modules.py`, `modules_manifest.json`, and `app.js` are untouched, no build was run, and nothing was git-added. Wiring should be a separate, explicit step after sign-off, at which point `pass_rule_note` and the per-module exam config (`EXAM_QUESTION_COUNT_BY_TYPE`, `MAX_ERROR_POINTS_BY_TYPE`, `EXAM_TIME_LIMIT_MS_BY_TYPE`, `EXAM_TOPIC_DRAW`) need real values — 5 topics with a 5/5/4/4/3 distribution suggests a 5-question draw touching every topic, but that is a design decision, not a legal one.
5. **Locale scope.** DE canonical + EN only, per the pilot-first convention. The 12-locale expansion happens only after sign-off. Note for translators: the official OJ terminology differs meaningfully between language versions and should be sourced from the OJ version of each target language, not machine-translated from the DE.
6. **Regulatory currency.** Both delegated regulations were adopted recently (2024/1773 in March 2024, 2025/532 in March 2025). Before any production release, re-confirm no further Art. 30-relevant Level 2 act or ESA guidance has landed since 2026-08-16.

## 7. Module metadata as drafted

- Module id: `dora_procurement` · file: `data/dora_procurement_pilot_DRAFT.json` · 20 questions · DE canonical + EN
- `class_scope: ["ALL"]` on every question; `class: "ALL"` in meta
- Topic codes (5): `grundsaetze` (4), `pflichtklauseln` (5), `kritische_funktionen` (4), `auditrechte` (4), `subunternehmer` (3)
- Points: 3–4 (11 × 4 points, 9 × 3 points), matching the `kartellrecht_pilot.json` scale
- `high_stakes: true` on 10 questions — the tier-split, audit-rights and vendor-pushback items
- `grundstoff: true` on one anchor question per topic
- Answer key distributed 5×a / 5×b / 5×c / 5×d (the first draft was 19/20 "b"; positions were permuted and all in-explanation option references were remapped and re-verified)
- `meta.legal_disclaimer` carries the required text verbatim: *"Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall durch qualifizierte Juristen oder Wirtschaftsprüfer zu validieren."*
- `meta.legal_review_status` records the primary-source verification and points back to this dossier

---

**Reminder:** this document and the accompanying JSON are draft training-content groundwork. They are not legal advice, have not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review.
