# DORA audit-readiness module (`dora_audit_readiness`) — draft pilot content + pre-review dossier (2026-08-16)

**Status:** AI-prepared groundwork only — **NOT legal advice**. Attorney sign-off required before any commercial/production use. The draft question file exists at `data/dora_audit_readiness_pilot_DRAFT.json` and is **deliberately not wired into the live app**: it is not registered in `data/build_modules.py` or `data/modules_manifest.json`, `app.js` is untouched, no build step was run, and nothing was staged or committed. The `_DRAFT` suffix keeps it out of the live build path by construction.

**Subject:** 20-question **DE-canonical** (+ EN) draft pilot for a new module, working name `dora_audit_readiness` — **"Surviving the DORA Audit: Testing, Evidence, and ISO 27001 Alignment"** (roadmap module 3A, which the roadmap calls *"Surviving the CISA Audit"*). Target audience: **internal audit functions, CISOs and audit-preparation staff at EU financial entities who have to actually produce evidence for a DORA compliance audit** — an internal audit, a Big 4 external audit, or a supervisory examination. Not the board, not procurement, not the SOC. Schema follows `data/kartellrecht_pilot.json` field-for-field (verified programmatically: identical question-object key set **and** key order).

**Locale decision.** DE canonical + EN, matching the four DORA sibling draft modules (`dora_procurement`, `dora_executive`, `dora_register`, `dora_incident`) and the roadmap, which targets **DE/EN** for module 3A. (Only `cra_supply_chain` is EN-canonical, and for a stated audience reason.)

---

## 0. The acronym problem, dealt with first because it is a naming decision, not a footnote

The roadmap calls this module **"Surviving the CISA Audit"**. That title is ambiguous to the point of being unusable in a learner-facing product, and the ambiguity was checked rather than assumed.

| Reading | What it actually is | Status here |
|---|---|---|
| **ISACA's "Certified Information Systems Auditor" (CISA)** | A **professional credential for individuals**, issued by ISACA. It is what a large share of internal auditors and Big 4 IT-audit staff hold, and the roadmap's own "certification/buzzword landscape" section lists it alongside CRISC as *"DORA-adjacent professional certs Big 4 auditors actually hold"*. | **This is the meaning the roadmap intends.** The module is aimed at the people who hold or are preparing for that credential and who sit on internal-audit / CISO teams. |
| **The US "Cybersecurity and Infrastructure Security Agency" (CISA)** | A **United States federal agency**. It has **no role whatsoever** under DORA, is not a competent authority under Art. 46, and appears nowhere in Regulation (EU) 2022/2554 or in Delegated Regulation (EU) 2025/1190. | **Wrong reading.** A German- or English-speaking EU learner searching "CISA audit" will land on the US agency more often than on ISACA. |
| **An alleged EU "Critical Entities Resilience" usage of "CISA"** | **Not substantiated.** The EU instrument on the resilience of critical entities is **Directive (EU) 2022/2557**, whose established short form in EU and practitioner usage is **CER**, not CISA. I found no EU-institutional source using "CISA" for it. | **Recorded as a correction to the task brief**, which suggested this third usage. It is not a real acronym collision; the real collision is the two above. |

**Recommendation, and it is a product decision, not a legal one:** drop the acronym from any learner-facing title. Proposed title: **"DORA Audit Readiness — Testing, Evidence and ISO 27001 Alignment"**, with *"for CISA/CRISC-holding internal auditors"* usable in marketing copy where the audience is unambiguous. The acronym decision is recorded inside the data file as `meta.acronym_note` so it cannot be lost in a rename.

**A second, smaller correction to the same roadmap paragraph:** the roadmap lists *"CISA, CRISC (both ISACA), ISO/IEC 27001:2022 as baseline"* as though all three were personal credentials held by auditors. **ISO/IEC 27001 is a standard certifying an organisation's information security management system, not a person.** (There are personal "ISO 27001 Lead Auditor / Lead Implementer" qualifications, but those are training-provider credentials, not the standard itself.) Putting the three in one list is a category error that this module must not repeat, because it is the seed of exactly the confusion §4.3 is written to prevent.

---

## 1. Method and instruments read

Every citation below was read on 2026-08-16 in the **official Official Journal text**, in both the **English and the German** language versions, retrieved from the EU Publications Office **Cellar** repository (`publications.europa.eu/resource/celex/<CELEX>`, `Accept: application/xhtml+xml`, `Accept-Language: eng` / `deu`). As all five sibling dossiers recorded, `eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge in this sandbox and `WebFetch` truncates before reaching the articles; the Cellar route was used **from the start** and delivered complete documents in every case.

| Instrument | CELEX | OJ reference | Bytes EN / DE | What was read |
|---|---|---|---|---|
| **Regulation (EU) 2022/2554** (DORA) | `32022R2554` | OJ L 333, 27.12.2022, p. 1 | 747 KB / 784 KB | Recitals 42–44, 47; Art. 3(17), 3(22), 3(60); Art. 4; **Art. 6 in full**; **Art. 11 in full**; **Art. 16(1)**; **Art. 24, 25, 26, 27 in full**; Art. 40(4); Art. 46 — EN + DE |
| **Commission Delegated Regulation (EU) 2025/1190** of 13 February 2025 — RTS on TLPT (the Art. 26(11) mandate) | `32025R1190` | OJ L, **2025/1190, 18.6.2025** | 305 KB / 314 KB | **Recitals in full**; **Art. 1–17 in full**; Annex VII and Annex VIII — EN + DE |

### 1.1 The Level 2 question, answered by finding the instrument rather than assuming it does not exist

The brief asked whether a finalised RTS/ITS exists for TLPT under Art. 26(11)/27(1). **It does, it is adopted, and it is substantial.**

- **Commission Delegated Regulation (EU) 2025/1190** of 13 February 2025, published in **OJ L, 2025/1190 of 18 June 2025**, cites in its own preamble *"Regulation (EU) 2022/2554 … and in particular Article 26(11), fourth subparagraph thereof"*. Its title discharges all four limbs of the Art. 26(11) mandate: the criteria for identifying entities required to perform TLPT; the requirements and standards governing the use of internal testers; the requirements on scope, testing methodology and approach per phase and on results/closure/remediation; and the supervisory cooperation needed for implementation and mutual recognition.
- **Adopted status confirmed, not inferred:** the instrument closes with *"Diese Verordnung ist in allen ihren Teilen verbindlich und gilt unmittelbar in jedem Mitgliedstaat"* / *"This Regulation shall be binding in its entirety and directly applicable in all Member States"*, signed **Brussels, 13 February 2025**, and Art. 17 provides for entry into force on the twentieth day following OJ publication. It is not a draft, a consultation paper or an ESA final report.
- **There is no separate ITS** under Art. 26(11)/27(1). The mandate is an RTS mandate; the tester requirements in Art. 27(1) DORA are directly applicable and are supplemented by Art. 7 of the RTS, not by a distinct instrument.

**Note on the drafting history, kept out of the question pool:** the ESAs' Final Report `JC 2024-29` on this RTS is the public draft that preceded the delegated act. It is **not cited anywhere in this module** — the adopted instrument is available and there is no reason to rest anything on the draft.

### 1.2 Corrigendum / amendment check, with a positive control

The `dora_register` dossier established that Level 2 instruments in this family get silently corrected after OJ publication, and the `cra_supply_chain` dossier found three corrigenda by running the probe. Run here:

| Consolidated-version probe | Result |
|---|---|
| `02024R2956-20241202` (positive control — known-corrected DORA register ITS) | **200, 294 KB — consolidation exists** |
| `02025R1190-20250701` | 404 |
| `02025R1190-20250708` | 404 |
| `02025R1190-20260101` | 404 |
| `02022R2554-20230116` | 404 |
| `02022R2554-20250117` | 404 |

Because the control returns a consolidation and none of the probes for the two instruments used here does, **no amendment or corrigendum has been applied to Regulation (EU) 2022/2554 or to Delegated Regulation (EU) 2025/1190 as at 2026-08-16.** *(Caveat: absence of a consolidated version is strong but not conclusive evidence; a very recent corrigendum could lag consolidation. Re-run before any production release — see §8.6.)*

### 1.3 Non-legal frameworks and standards — consulted and quarantined

Two bodies of material matter to this audience and **neither is EU law**. Both are used only inside explanations, clearly labelled, and **no answer key and no distractor's wrongness depends on either**.

**TIBER-EU.** Researched by web sources because it is not in any legal database. It is the **Threat Intelligence-based Ethical Red Teaming framework published by the European Central Bank on 2 May 2018**, described by the ECB at publication as *"the first Europe-wide framework for controlled and bespoke tests against cyber attacks in the financial market"*, with the ECB stating expressly that *"it is up to the relevant authorities and the entities themselves to determine if and when TIBER-EU based tests are performed"*. The Eurosystem **updated TIBER-EU in February 2025 to align it with DORA's TLPT RTS**, and the ECB has since published a TIBER-EU SSM implementation guide for significant institutions (November 2025). **TIBER-EU is a central-bank framework, not a Union legal act.** Its precise legal relationship to DORA is set out in §4.2 and is the subject of question 20.

**ISO/IEC 27001:2022.** **Copyrighted and not available through any public legal database.** Handled under a strict rule stated here so a reviewer can hold me to it:

- **No ISO control text is quoted, paraphrased closely, or reproduced anywhere** in the dossier or in the JSON file. There is not one sentence of ISO wording in either artefact.
- Annex A control **identifiers and their well-known short titles** (e.g. "A.5.1 policies for information security") are used ubiquitously in public compliance literature and are not themselves the protected expression, so referencing them is safe — but **this pilot does not in fact reference a single one**, because no question needed it. The ISO question is grounded entirely in DORA's own text.
- The structural facts used (ISO/IEC 27001:2022 was published in October 2022; Annex A restructures the controls into four themes) come from secondary summaries and appear nowhere in the question pool.
- The mapping is framed only at a **structural/topical** level: *an organisation already certified to ISO/IEC 27001 will have built structures, evidence and review routines that address related ground for part of what DORA requires.* It is never framed as equivalence. See §3.1.

Vendor and consultancy "ISO 27001 to DORA mapping" material was scanned and **is not cited anywhere**. As §4.3 shows, the claim most of it implies is precisely what this module is built to correct.

---

## 2. Why this module, and where its boundaries are

### 2.1 The spine

Three design decisions came out of the primary-source read.

1. **The spine is the two-regime split inside Chapter IV.** DORA does not have "a testing requirement". It has **two**, with different addressees, different frequencies and different tester rules:
   - the **baseline programme** (Art. 24–25), binding on **every** financial entity that is not a microenterprise, with a **yearly** floor for systems supporting critical or important functions (Art. 24(6)); and
   - **TLPT** (Art. 26–27), binding only on a **small identified population**, at least every **3 years**, with supervisory validation of scope, supervisory approval of internal testers, and a mandatory external threat-intelligence provider.

   Almost every practitioner error in this area is a transfer of a rule from one regime to the other. Questions 2, 6, 11 and 12 exist to make the split explicit and permanent.

2. **Evidence is taught as a set of named artefacts, not as a virtue.** DORA and the RTS name, in terms, what has to exist and be producible: internal validation methodologies (Art. 24(5)), the scope specification document approved by the **management body** (RTS Art. 9(6)), the summary of relevant findings and the documentation demonstrating conformity of the test (Art. 26(6)), the five-element remediation plan (RTS Art. 13(2)), the internal-tester policy and its disclosure in three specific documents (RTS Art. 15(1) and (3)), and the attestation and its contents (Art. 26(7), RTS Art. 14 and Annex VIII). Nine of the twenty questions are answerable only by knowing an artefact exists.

3. **Three questions are audit-trap scenarios** where a competent organisation does the operationally sensible thing and still fails: question 3 (tickets opened and closed, no validation methodology), question 8 (test the mirror environment because production is risky), question 18 (rest on the ISO 27001 certificate). These are the three places a Big 4 auditor or a supervisory examiner opens the file first.

### 2.2 Boundaries against the sibling modules — checked question by question, not assumed

| Sibling | What it already tests | How this module stays clear |
|---|---|---|
| **`dora_executive`** (module 1A) | Board governance under Art. 5, **including Art. 5(2)(f)** — approval and periodic review of ICT internal audit plans, ICT audits and material modifications, read together with **Art. 6(6) and 6(7)** (framework subject to regular internal audit; formal follow-up for critical findings). Also **Art. 6(5)** (yearly review cadence and its triggers). | This module **does not re-test Art. 5(2)(f), Art. 6(5) or Art. 6(7)**. Question 15 goes to a different half of the same neighbourhood: **Art. 6(4)** (three-lines-of-defence segregation and independence of the ICT risk management, control and internal audit functions — untested anywhere) and the **auditor-competence limb of Art. 6(6)** (*sufficient knowledge, skills and expertise in ICT risk, as well as appropriate independence*), which the executive dossier's item 10 touches only from the board's approval standpoint. The boundary is stated inside question 15's own German explanation so a learner taking both modules is not confused. **This is the closest overlap in the module and is flagged for the reviewer in §8.1.** |
| **`dora_procurement`** (module 2B) | Art. 30 contract contents, the Art. 30(2)/30(3) tier split, **audit rights over vendors (Art. 30(3)(e))**, certifications as vendor-assurance methods (Art. 8 Del. Reg. (EU) 2024/1773), subcontracting, and **exit strategy (Art. 30(3)(f) + Art. 28(8))**. | **No question here touches Art. 28 or Art. 30.** Third-party providers appear only where Chapter IV itself reaches them: Art. 26(3)–(4) (participation in a TLPT, pooled testing, retained responsibility) — question 9. **Exit-strategy documentation is deliberately not tested here at all**; see §4.1. |
| **`dora_incident`** (module 5) | Art. 17–20 and the three Level 2 instruments on incident classification, deadlines, content and templates. | **No question here touches Chapter III.** The only contact point is that Art. 6(5) lists major incidents as a framework-review trigger, and that is left to the executive module. |
| **`dora_register`** (module 4) | The Art. 28(3) information register and ITS (EU) 2024/2956. | No contact. |
| **Roadmap module 6, "TLPT & Advanced Resilience Testing"** | Planned as a separate elite/EN-only premium module. | **This is a genuine, unresolved boundary problem and it is a product decision, not a legal one — see §4.4.** |

---

## 3. Citation ledger (primary-source verified 2026-08-16)

**Confidence rule used here** — identical to the five sibling dossiers, restated so the reviewer can hold me to it:

- **"High — verbatim"** = the tested proposition is a direct restatement of wording I read in the OJ text of the cited provision, in **both** EN and DE.
- **"High — verbatim + synthesis"** = every element is verbatim, but the question combines **two or more** provisions I read separately; the reviewer should check that the *combination* is a fair statement, not the underlying text.
- **What disqualifies a claim from "High":** any of (a) the proposition rests wholly or partly on a source that is not the OJ text of a binding instrument — including ECB frameworks, ESA final reports, ISO standards, national-authority notices and vendor summaries; (b) the proposition requires an inferential step beyond the words on the page; (c) the proposition was verified in only one language version where both exist; (d) the proposition rests on a **recital** rather than the enacting terms; (e) the proposition depends on the **absence** of an instrument I could not exhaustively enumerate. Anything hitting (a)–(e) is dropped or explicitly de-rated.
- **No question in this pilot carries a Medium or lower rating.** Questions that could not be grounded verbatim were dropped rather than written down-rated; they are logged in §6.
- **Mechanical verification performed:** every quoted string of six or more words appearing inside a question, an option or an explanation — **81 fragments, DE and EN combined** — was re-matched programmatically against the retrieved OJ plain text after whitespace, quote-style and case normalisation. **81/81 matched exactly; 0 failures.** Breakdown by source: 29 DORA DE, 29 DORA EN, 11 RTS DE, 12 RTS EN. Two German/English pairs were corrected during this pass (a trailing full stop written where the OJ has a colon), which is why the check is worth running rather than trusting the drafting.

| # | Question ID | Citation (DORA = Reg. (EU) 2022/2554; RTS = Del. Reg. (EU) 2025/1190) | What's tested | Confidence |
|---|---|---|---|---|
| 1 | `dora-audit-testprogramm-01` | Art. 24(1), (2) DORA | The testing programme is an **integral part of the Art. 6 framework**, established/maintained/reviewed, comprising the Art. 25/26 range of assessments | High — verbatim (EN + DE) |
| 2 | `dora-audit-testprogramm-02` | Art. 24(6) DORA | **At least yearly** appropriate tests on **all** ICT systems and applications supporting critical or important functions — and its independence from the 3-year TLPT cycle | High — verbatim |
| 3 | `dora-audit-testprogramm-03` | Art. 24(5) DORA | Scenario: closed tickets are not enough. Prioritise/classify/remedy procedures **and** internal validation methodologies to ascertain that gaps are **fully addressed** | High — verbatim |
| 4 | `dora-audit-testprogramm-04` | Art. 25(1) + Art. 25(2) DORA | The open ("such as") list, incl. **physical security reviews** and **questionnaires**; source code review only **"where feasible"**; CSD/CCP pre-deployment vulnerability assessments | High — verbatim + synthesis (two paragraphs of one Article) |
| 5 | `dora-audit-testprogramm-05` | Art. 11(6)(a) + Art. 11(6) subpara 2 + Art. 11(3) DORA | BCP and response/recovery plan testing **at least yearly and on substantive changes**; cyber-attack and switchover scenarios mandatory for non-microenterprises; response/recovery plans subject to **independent internal audit reviews** | High — verbatim + synthesis |
| 6 | `dora-audit-tlpt_scoping-01` | Art. 26(1) read with Art. 26(8) subpara 3, Art. 16(1) subpara 1, Art. 3(60) DORA | **The scoping anchor**: only entities identified by the competent authority; at least every 3 years; authority may reduce **or increase**; Art. 16(1) entities and microenterprises excluded | High — verbatim (the whole of Art. 26(1) quoted in both languages) |
| 7 | `dora-audit-tlpt_scoping-02` | Art. 2(1), (2) RTS | The identification mechanism: a two-part criteria catalogue **plus** a **rebuttable** presumptive list ("unless the assessment … does not justify") | High — verbatim (chapeau of Art. 2(2) quoted in both languages) |
| 8 | `dora-audit-tlpt_scoping-03` | Art. 26(2) subparas 1 and 3 DORA (+ RTS Art. 9(6) in the explanation) | **Live production systems**, several or all CIFs; scope proposed by the entity and **validated by the competent authorities** | High — verbatim |
| 9 | `dora-audit-tlpt_scoping-04` | Art. 26(3), (4) DORA | Provider participation; **retained full responsibility**; the pooled-testing route and that pooled testing **counts as** the participants' TLPT | High — verbatim |
| 10 | `dora-audit-tlpt_scoping-05` | Art. 9(2), 9(6), 11(5) RTS | 3-month initiation information; 6-month scope specification document **approved by the management body**; active red team phase **at least 12 weeks** | High — verbatim |
| 11 | `dora-audit-tester_governance-01` | Art. 24(4) DORA | Independent parties, **internal or external**; internal testers require dedicated resources and conflict-of-interest avoidance throughout design and execution | High — verbatim |
| 12 | `dora-audit-tester_governance-02` | Art. 26(8) subparas 1 and 2 DORA | External tester **every three tests**; and the **absolute** external-only rule for significant credit institutions | High — verbatim |
| 13 | `dora-audit-tester_governance-03` | Art. 27(2)(a), (b), (c) DORA | The three additional internal-tester conditions, incl. that the **threat intelligence provider is external to the entity** | High — verbatim |
| 14 | `dora-audit-tester_governance-04` | Art. 27(1)(a)–(e) DORA | The five tester requirements; **point (c) is an alternative, not a mandate**; indemnity insurance is not optional; DORA names **no** certification | High — verbatim |
| 15 | `dora-audit-tester_governance-05` | Art. 6(4) + Art. 6(6) DORA | Three-lines-of-defence segregation and independence; **auditor competence and independence**; frequency/focus commensurate to ICT risk | High — verbatim + synthesis (two paragraphs; boundary against `dora_executive` stated in the explanation) |
| 16 | `dora-audit-nachweise_audit-01` | Art. 26(6), (7) DORA (+ RTS Art. 14 / Annex VIII in the explanation) | **The evidence anchor**: what goes to the authority; the attestation is for **mutual recognition**, not a compliance certificate; responsibility is **not** shifted | High — verbatim |
| 17 | `dora-audit-nachweise_audit-02` | Art. 13(1), (2) RTS | The 8-week clock and the **five mandatory remediation-plan elements**, incl. root-cause analysis and named owners | High — verbatim (all five points quoted in both languages) |
| 18 | `dora-audit-nachweise_audit-03` | Art. 6, Arts. 24–27 and Art. 40(4) subpara 2 DORA | **The ISO 27001 question**: no certification-equivalence and no presumption of conformity exists in DORA; the only two certification references in the enacting terms and what they actually address | High — verbatim + synthesis, **supported by a full-text negative check** (see §3.1) |
| 19 | `dora-audit-nachweise_audit-04` | Art. 15(1), (3) RTS | Internal-tester policy contents (documented and periodically reviewed; test lead + at least two members; 12-month prior employment) and the **three documents** the use of internal testers must be stated in | High — verbatim |
| 20 | `dora-audit-nachweise_audit-05` | **Art. 26(11) subpara 1 DORA** (+ RTS recital 1, labelled, for corroboration) | **The TIBER-EU question**: DORA binds the **ESAs** to draft in accordance with TIBER-EU; it does not bind entities to test according to it | High — verbatim on the enacting text; recital used only as corroboration and labelled as such |

**Tier A — verbatim, single-provision, lowest review burden (13):** 1, 2, 3, 6, 8, 9, 10, 11, 12, 13, 14, 17, 19.
**Tier B — verbatim but combining provisions, or turning on a boundary the reviewer should confirm (7):** 4, 5, 7, 15, 16, 18, 20.
**Tier C — any claim resting on a secondary source: none.** No question's correct answer, and no distractor's wrongness, depends on the TIBER-EU framework documents, the ECB press releases, the ESAs' final report `JC 2024-29`, ISO/IEC 27001, or any vendor or consultancy summary. Every factual statement about TIBER-EU's ownership and history sits inside question 20's explanation, is labelled *"Hintergrundinformation, nicht Rechtsgrundlage"* / *"Background, not legal basis"*, and is arranged so that a reader who ignored it entirely would still answer correctly.

### 3.1 The negative check behind question 18, stated so it can be re-run

Question 18 is the only question in this pilot whose correct answer depends partly on something **not** being in the text. That is a category (e) risk under the confidence rule, so the check was made exhaustive and mechanical rather than impressionistic:

| Search | DORA EN | DORA DE | RTS EN | RTS DE |
|---|---|---|---|---|
| `ISO` (as a standalone token or in `ISO/IEC`) | **0** | **0** | **0** | **0** |
| `certification` / `Zertifizierung` (enacting terms) | **2 locations** | **2 locations** | 1 (Art. 7(1)(a), tester CVs) | 1 (same) |
| `presumption of conformity` / `Konformitätsvermutung` | **0** | **0** | **0** | **0** |
| `harmonised standard` / `harmonisierte Norm` | **0** | **0** | **0** | **0** |

The **two** certification locations in DORA's enacting terms are:

1. **Art. 27(1)(c)** — testers *"are certified by an accreditation body in a Member State **or** adhere to formal codes of conduct or ethical frameworks"* / *"von einer Akkreditierungsstelle in einem Mitgliedstaat zertifiziert wurden **oder** formale Verhaltenskodizes oder ethische Rahmenregelungen einhalten"*. This is about the **tester**, not the entity, and it is disjunctive.
2. **Art. 40(4), second subparagraph** — *"For the purposes of fulfilling the oversight activities, the Lead Overseer may take into consideration any relevant third-party certifications and ICT third-party internal or external audit reports made available by the critical ICT third-party service provider."* / *"Die federführende Überwachungsbehörde kann zur Erfüllung der Überwachungstätigkeiten alle einschlägigen Zertifizierungen Dritter und interne oder externe IKT-Prüfungsberichte Dritter berücksichtigen, die von dem kritischen IKT-Drittdienstleister zur Verfügung gestellt werden."* This is about a **critical ICT third-party service provider** under Oversight, not about a financial entity's own compliance, and the verb is **"may take into consideration"**, not "shall accept".

There is a **third** certification-adjacent provision, and it is worth naming because it is the one most often mis-cited in this argument: **Art. 8 of Commission Delegated Regulation (EU) 2024/1773** permits certifications and provider audit reports as **assurance methods for auditing an ICT vendor**, subject to conditions and expressly prohibiting sole reliance over time. That was read and verified by the `dora_procurement` dossier (its question 16). It concerns **how a financial entity assures itself about a vendor**, not how it demonstrates its own compliance to a supervisor — and it is not re-tested here.

**Conclusion, stated as precisely as the text allows:** DORA says **nothing at all** about existing certifications of the financial entity itself. There is no equivalence rule, no presumption of conformity, no partial credit, and no exemption. The nearest analogue in adjacent EU law — the presumption of conformity through harmonised standards — is a **product-law** mechanism (the Cyber Resilience Act uses it) and is structurally absent from DORA, which is a supervisory instrument addressed to regulated entities.

---

## 4. Findings where existing research / prior content is imprecise against the primary text

The task asked me to check the briefing rather than confirm it. **Six findings, four of them material.**

### 4.1 The roadmap's module 3A description is three items long and one of them belongs to another module

The roadmap describes 3A as: *"Surviving the CISA Audit (internal audit/CISO; **ISO27001-to-DORA gap mapping, evidence packaging, exit-strategy documentation**)."* Checked item by item:

| Roadmap item | Verdict |
|---|---|
| **"evidence packaging"** | **Correct, and better supported than the roadmap knows.** The RTS names artefacts, owners and clocks with unusual precision (Art. 9(2), 9(6), 12(2), 12(4), 12(7), 13(1)–(2), 14, 15(1), 15(3)). Nine of this pilot's twenty questions sit here. This is the module's strongest commercial ground. |
| **"ISO27001-to-DORA gap mapping"** | **Correct as an internal working method, dangerous as a value proposition.** See §4.3. A gap map is a perfectly sensible way for a certified organisation to organise its DORA programme; what it must never be sold as is a compliance shortcut. And because ISO's control text is copyrighted, a Zettacard module cannot teach the mapping at control-text level at all — only at the structural level of "these DORA duties have no ISO counterpart at all". |
| **"exit-strategy documentation"** | **Belongs to Module 2B, not here — flagged explicitly, as the brief required.** Exit strategy is an **Art. 30(3)(f)** obligation, read with **Art. 28(8)**, i.e. it sits in Chapter V (ICT third-party risk), not Chapter IV (testing). It is already tested by `dora_procurement` question 13 (`kritische-funktionen-04`), whose dossier established the two load-bearing facts: DORA prescribes **no** transition-period duration (it requires an *"adequate"* period), and the duty is **Art. 30(3)-tier only**, i.e. it does not reach the Art. 30(2) baseline that applies to every ICT contract. There is also now a separate practitioner add-on at `docs/sovereign-cloud-exit-strategy-addon-2026-08-16.md`, scoped to the same material. **Nothing in this pilot's 20 questions touches Art. 28 or Art. 30.** Re-testing it here would have produced the exact duplication the roadmap's own module boundaries are meant to prevent. |

**Recommended roadmap wording, replacing the current parenthetical:** *"3A. DORA Audit Readiness (internal audit/CISO; Chapter IV resilience testing — the Art. 24–25 baseline programme and the Art. 26–27 TLPT regime under Delegated Regulation (EU) 2025/1190; evidence artefacts and the remediation-plan requirements; internal-audit independence under Art. 6(4)/6(6); and the precise, non-equivalent relationship between an existing ISO/IEC 27001 certification and DORA compliance). Exit-strategy documentation is covered by module 2B and is not repeated here."*

### 4.2 The TIBER-EU relationship, stated precisely — and it is not what "the core buzzword for DORA Pillar 4" implies

The roadmap lists **TIBER-EU** as *"the core buzzword for DORA Pillar 4 (resilience testing / TLPT)"*. That is accurate as a marketing observation and misleading as a statement of obligation. The precise position, verified in enacting text:

**The only reference to TIBER-EU in DORA's enacting terms is Art. 26(11), first subparagraph:**

> **EN:** *"The ESAs shall, in agreement with the ECB, develop joint draft regulatory technical standards **in accordance with the TIBER-EU framework** in order to specify further: …"*
>
> **DE:** *"Die ESA arbeiten im Einvernehmen mit der EZB **im Einklang mit dem TIBER-EU-Rahmen** gemeinsame Entwürfe technischer Regulierungsstandards aus, in denen Folgendes präzisiert wird: …"*

**Read the addressee.** That sentence binds **the European Supervisory Authorities in their rule-making**. It does not bind a financial entity in its testing. There is **no provision anywhere in DORA obliging a financial entity to follow the TIBER-EU methodology.**

**The RTS then says so in terms, in recital 1** (labelled as a recital, used only for corroboration, and the reason question 20's answer key rests on Art. 26(11) instead):

> **EN:** *"This Regulation has been drafted in accordance with the TIBER-EU framework and mirrors the methodology, process and structure of threat-led penetration testing (TLPT) as described in TIBER-EU. Financial entities subject to TLPT **may** refer to and apply the TIBER-EU framework, or one of its national implementations, **in as much as** that framework or implementation **is consistent with** the requirements set out in Articles 26 and 27 of Regulation (EU) 2022/2554 and this Regulation."*
>
> **DE:** *"Diese Verordnung wurde im Einklang mit dem TIBER-EU-Rahmen ausgearbeitet und spiegelt die Methodik, das Verfahren und die Struktur bedrohungsorientierter Penetrationstests … wider. Finanzunternehmen, die zur Durchführung von TLPT verpflichtet sind, **können** sich auf den TIBER-EU-Rahmen oder eine seiner nationalen Umsetzungen beziehen und diesen Rahmen oder die nationale Umsetzung anwenden, **sofern** dieser Rahmen oder die Umsetzung mit den Anforderungen der Artikel 26 und 27 der Verordnung (EU) 2022/2554 und der vorliegenden Verordnung **im Einklang steht**."*

**The precise answer, in one sentence:** *DORA does not legally mandate the TIBER-EU methodology. It mandates the ESAs to build the RTS in accordance with TIBER-EU, with the result that the legally binding methodology in Delegated Regulation (EU) 2025/1190 deliberately mirrors TIBER-EU; applying TIBER-EU or a national TIBER implementation is expressly permitted and, where consistent, satisfies the law — but the legal yardstick is Arts. 26/27 DORA and the Delegated Regulation, never the framework document.*

That distinction is not academic. The RTS **is** a near-mirror of TIBER-EU: it imports the control team, the blue team, the threat intelligence provider and the testers-as-red-team, and creates a "TLPT cyber team" (TCT) at the authority explicitly mirroring TIBER-EU's cyber teams (recitals 5–8). In practice most entities will be told by their national TLPT authority to use a national TIBER implementation. But **the legal duty runs to the Delegated Regulation**, and a firm that documents its test against the TIBER-EU framework document alone has evidenced conformity with a guidance document, not with the law.

**Recommended roadmap wording:** replace *"TIBER-EU: the core buzzword for DORA Pillar 4"* with *"TIBER-EU: the ECB/Eurosystem framework that DORA's TLPT regime was built to mirror (Art. 26(11) DORA obliges the ESAs to draft the RTS in accordance with it). Binding law is Arts. 26–27 DORA + Delegated Regulation (EU) 2025/1190; TIBER-EU and its national implementations may be applied where consistent with those."*

### 4.3 "ISO 27001 as baseline" is the single most commercially dangerous phrase in the roadmap

The roadmap lists ISO/IEC 27001:2022 *"as baseline"* among the credentials Big 4 auditors hold, and frames module 3A around "ISO27001-to-DORA gap mapping". Two corrections, one of them already made in §0 (it is not a personal credential), and one that goes to the module's core:

**There is no such thing as a DORA compliance credit for an ISO/IEC 27001 certificate.** §3.1 sets out the mechanical check. In summary: DORA never mentions ISO, contains no presumption of conformity, no equivalence clause, and no exemption keyed to any certification. The two certification references in its enacting terms address a **TLPT tester's suitability** and **a critical ICT third-party provider under Oversight**. Neither is about the entity's own compliance.

**What is true, and is what the module actually teaches:**

- An organisation running a certified ISMS will already have management-system machinery — documented policies, risk assessment, internal audit, management review, corrective action, competence records — that overlaps **topically** with what DORA requires, and that overlap makes DORA evidence cheaper to produce. That is a real, sellable benefit and it is stated in question 18's explanation in exactly those terms.
- The overlap is **partial and asymmetric**, and the module's value is naming the parts with no ISO counterpart at all. On the primary text: **Art. 24(6)**'s yearly floor for *all* systems supporting critical or important functions; the whole of **Art. 26** (TLPT scoping by the supervisor, live production systems, supervisory validation of scope, the 12-week active phase); **Art. 27**'s tester regime including the external threat-intelligence rule; **Art. 26(6)–(7)**'s submission and attestation mechanics; and the **Art. 13(2) RTS** remediation-plan contents. None of these has anything to answer to it in a general-purpose ISMS standard, and no amount of gap-mapping produces them.
- **A certificate is not a defence and cannot be presented as one.** The correct framing for a supervisory conversation is: *here is our Art. 24 testing programme, here is the Art. 24(6) evidence, here is the Art. 24(5) validation methodology, here is the Art. 6(6) internal audit* — with the ISMS as the filing system, not the answer.

Question 18 is built to punish the opposite framing, and its three wrong options are the three real-world versions of the mistake: "the certificate evidences conformity with Art. 6", "certified entities are exempt from Art. 26", and "DORA has a presumption of conformity like product safety law".

### 4.4 The roadmap has two modules covering TLPT and has not decided where the line is

The roadmap lists **3A** (this module) and, separately, **module 6, "TLPT & Advanced Resilience Testing (elite security teams, TIBER-EU). Language: EN only. Niche/premium-consulting framing, low volume."**

Ten of this pilot's twenty questions are about TLPT — because **an internal auditor at an in-scope entity cannot prepare an audit file without knowing the TLPT scoping rule, the tester rules and the closure artefacts.** That is not scope creep; it is what the audience needs. But it does mean that after this module ships, a separate module 6 has to justify itself on depth this one does not reach.

**Recommendation (product decision, flagged not taken):** the honest line is **audit perspective versus execution perspective**. 3A teaches *what must exist, who signs it, when it is due and what the auditor will ask for*. Module 6, if built, should teach *how to run the test* — the phase mechanics of RTS Arts. 9–12, scenario selection under Art. 10(3)–(4), leg-ups, detection handling under Art. 11(9), the purple-teaming fallback under Art. 11(10), the replay exercise, and the Annex I–VIII document templates. Framed that way the two do not collide. Framed as "3A: TLPT overview / 6: TLPT deep dive" they will, and the low-volume module is the one that loses.

### 4.5 Four German-language defects in the primary texts, three of which affect this audience directly

Found during the verbatim-matching pass; all four are in the OJ text, none is a drafting error of mine.

1. **RTS Art. 15(1), second subparagraph, point (c) DE calls the internal team's leader a *"Testmanager"*.** The EN reads *"a test lead"*. But **Art. 3 of the same Regulation defines *"Testmanager"* as the officers of the TLPT **authority*** (*"Ein TCT setzt sich aus Testmanagern zusammen, die mit der Beaufsichtigung eines einzelnen TLPT betraut sind"*), and the German text uses that meaning in all 35 other places. **In the German version the same word therefore denotes the supervisor's test manager everywhere except in Art. 15(1)(c), where it denotes the tested entity's own internal test lead.** For a module about who is independent from whom, that is not a cosmetic issue. Question 19's German option deliberately uses **"Testleiter"** and its explanation carries an explicit note.
2. **RTS Art. 9(6) DE says *"legt den Testleitern … vor"* where the EN says *"submit to the test managers"*.** *"Testleiter"* occurs exactly once in the whole German text, here. So the German version manages to use two different words for the authority's test managers and to reuse one of them for the entity's internal test lead. Same note, same question.
3. **DORA Art. 26(6) DE has a number-agreement error in the OJ text**: *"…die Unterlagen vor, mit denen belegt wird, dass **der TLPT** anforderungsgemäß **durchgeführt wurden**"* — singular article, plural verb. Not corrected by any consolidation (none exists). Question 16 quotes the sentence verbatim because it is the operative evidence rule, and the defect is harmless to meaning; it is recorded here so a reviewer does not think the quotation was mistyped.
4. **DORA Art. 26(7), second sentence: the DE is narrower than the EN.** EN: *"The financial entity shall notify the relevant competent authority of the attestation, the summary of the relevant findings and **the remediation plans**."* DE: *"…die Bescheinigung, die Zusammenfassung der maßgeblichen Ergebnisse und **die Abhilfemaßnahmen**."* The German says you notify the **measures**; the English says you notify the **plans**. Art. 26(6) DE gets it right (*"die Pläne mit Abhilfemaßnahmen"*), so the divergence is confined to one sentence. **No question depends on it**, and question 16 is written on Art. 26(6) plus the attestation limb of 26(7), avoiding the loose sentence. Flagged in case it ever moves.

### 4.6 Two things the sibling dossiers said about this area, checked

- The **`dora_executive` dossier** recorded Art. 6(6) and 6(7) as read and tested them from the board's approval standpoint (its item 10, Art. 5(2)(f)). **That reading is confirmed and is not disturbed here.** What the executive dossier did **not** reach is **Art. 6(4)** — the three-lines-of-defence segregation requirement — which is arguably the single most important structural provision for this module's audience, since it is the textual basis for internal audit not owning the ICT risk it audits. Question 15 closes that gap.
- The **2026-08-13 `dora` dossier** and the shipped general-staff `dora` module contain **no testing content at all** beyond awareness level. There is therefore **no shipped content to correct** in this area — unlike modules 5 and 2B, this dossier raises **no** correction against `data/dora_pilot.json`. (The separate German-orthography defect in that file, first raised by the `dora_incident` dossier §4.2, still stands and is still not fixed; this module's file uses proper orthography throughout — see §7.)

---

## 5. Gap list — covered by the primary sources but deliberately **not** tested by this 20-question pilot

1. **The whole phase mechanics of the RTS: Arts. 9–12 in operational detail.** Read in full; only the outer deadlines (Art. 9(2), 9(6), 11(5), 12(7)) and the closure/remediation outputs are tested. Untested: threat-intelligence analysis and scenario selection (**Art. 10**, including the rule that at least **three** scenarios are selected and that **no more than one** may be non-threat-led); the red team test plan and leg-ups (**Art. 11(1)–(3), (8)**); weekly progress reporting (**Art. 11(7)**); detection handling (**Art. 11(9)**); suspension and the limited purple-teaming fallback (**Art. 11(10)**); the replay and purple-teaming exercises and the mutual feedback round (**Art. 12(5)–(6)**). **This is the largest single block of untested primary material and is the natural spine of roadmap module 6** — see §4.4.
2. **RTS Annexes I–VIII in their entirety** (project charter, scope specification document, targeted threat intelligence report, red team test plan, red team test report, blue team test report, summary findings report, attestation). Read in outline; referenced only by number. A "populate the annex correctly" exercise is the obvious premium add-on for this audience and needs its own review pass.
3. **RTS Art. 5 (risk management by the control team) and Art. 6 (risk management measures).** Read; untested. Art. 5(1)'s enumeration of the risks to be assessed before testing live production systems, and Art. 5(3)'s exceptional-circumstances mechanism, are strong scale-up candidates and are directly relevant to an auditor asking "how did you satisfy yourself that this test was safe?".
4. **RTS Art. 7(1) in detail** — the concrete tester and threat-intelligence-provider qualification floors (years of experience, minimum team composition, at least three references for the TI provider and five for the testers, restoration procedures including command-and-control deactivation and backdoor removal, and the list of prohibited activities). Read in full; question 14 tests the DORA Art. 27(1) layer above it and the explanation only names the RTS as adding detail. Art. 7(2)'s exceptional-circumstances derogation is genuinely important commercially and is untested.
5. **RTS Art. 16 (cooperation and mutual recognition) in full**, including the host-authority observer mechanism, the 20-working-day window and the lead-authority rules for joint and pooled TLPTs. Read; only touched inside question 9's explanation. Relevant to any cross-border group and a good candidate for a group-audit variant.
6. **RTS Arts. 3, 4, 8** (TLPT cyber teams and test managers; the entity's organisational arrangements including need-to-know and blue-team handling; the specificities of pooled and joint TLPTs). Read; untested.
7. **Art. 6(8)–(9) DORA (digital operational resilience strategy contents, multi-vendor strategy)** and **Art. 6(10)** (outsourcing compliance-verification tasks). Read; **deliberately left to `dora_executive`**, which tests Art. 6(8) as item 7 and Art. 6(10) as item 3.
8. **Arts. 7–10 and 12–15 DORA** (ICT systems and tools; identification; protection and prevention; detection; backup and restoration; learning and evolving; communication) and **Delegated Regulation (EU) 2024/1774**, the RTS on ICT risk management tools. **Not read for this dossier and not cited.** This is the largest untested area of DORA for an audit audience and would be a fourth or fifth DORA module in its own right; it is named here so nobody assumes it was covered.
9. **Art. 16(2)–(4) DORA** (what entities on the simplified framework must do instead, and their own review and reporting duties). Read only as far as Art. 16(1); the simplified regime's own testing expectations are untested and would matter to a small-entity audit audience.
10. **Art. 46 DORA and the supervisory architecture** (which authority is competent for which entity type, and the interaction with a single national TLPT authority designated under Art. 26(9) or a delegation under Art. 26(10)). Read; only the existence of the designated authority is used. Nothing national is asserted anywhere in this pilot.
11. **Penalties for defective testing or evidence.** Not tested. DORA sets no EU-wide amount for financial entities — established in the `dora_executive` dossier §3.1/§3.3 and not re-litigated here — and anything specific would be national law not read today. In particular the roadmap's *"penalties up to 10% of annual revenue"* is a **Romanian national implementing figure**, not a DORA figure, and is not repeated anywhere in this module.
12. **ISO/IEC 27001 control-level mapping.** Deliberately and permanently out of scope for copyright reasons (§1.3). Even after legal review, this module should never contain an ISO-control-to-DORA-article table reproducing ISO wording. A DORA-side table naming duties with **no** ISO counterpart is safe and is the useful half anyway.
13. **The ESAs' final report `JC 2024-29` and the ECB's TIBER-EU documents and SSM implementation guide.** Consulted for background only; not cited, not tested, Tier C by construction. If the product owner wants TIBER-EU procedure taught, it belongs in a separately-labelled, separately-reviewed practice annex with its own re-verification cadence — the same recommendation the `dora_register`, `dora_incident` and `cra_supply_chain` dossiers made for their own practice material.

---

## 6. Questions considered and dropped (grounding failures, logged rather than written)

Per the brief's instruction not to write anything that cannot be grounded in verbatim primary text:

- **"Which ISO 27001 Annex A controls map to DORA Art. 24?"** — dropped, and permanently. Answering it requires reproducing or closely paraphrasing copyrighted control text. Rewritten as question 18, which is grounded entirely in DORA's own silence about certifications and is a better question anyway.
- **"Does an ISO 27001 certificate reduce the frequency of DORA testing?"** — dropped as a separate question. The honest answer is "DORA contains nothing that could produce such a reduction", which is the same negative finding question 18 already carries; a second question on one negative invites over-reading.
- **"How long must TLPT evidence be retained?"** — dropped. **Neither DORA nor the RTS states a retention period for TLPT documentation.** RTS Art. 7(2) requires the control team to *"keep record of"* the tester-compliance documentation and Art. 26(6) DORA requires documentation to be *provided*, but no instrument fixes a period. Any figure would come from national bookkeeping or supervisory law not read today. This is the single most-asked practical question from this audience and it is a gap, not a guess.
- **"In what format / through which portal is the TLPT summary submitted?"** — dropped. The RTS prescribes contents (Annexes VII, VIII) and addressees, not a channel or a format.
- **"How many days may elapse between the red team test report and remediation completion?"** — dropped. RTS Art. 13 fixes the **8-week deadline for submitting the plan** and requires the plan to state *"ihres voraussichtlichen Abschlusses"* / *"their … expected completion"*, but **fixes no completion deadline**. Question 17 teaches the submission clock and the five plan elements instead. Asserting a remediation deadline would be invention.
- **"Which entities are 'significant credit institutions' for the purposes of Art. 26(8)?"** — partly dropped. Question 12 states the consequence and cites the definitional route (Art. 6(4) of Regulation (EU) No 1024/2013) without teaching the SSM significance criteria, which live in an instrument not read today.
- **"Must the audit function be independent of the CISO?"** — dropped in that form. Art. 6(4) requires segregation and independence of the ICT risk management, control and internal audit functions "according to the three lines of defence model, or an internal risk management and control model", but names **no** function and prescribes **no** reporting line. Question 15 states what the text states; anything about the CISO specifically would be inference.
- **"Can a Big 4 external audit substitute for the Art. 6(6) internal audit?"** — dropped. Art. 6(6) requires internal audit "by auditors" meeting competence and independence requirements and is silent on whether the function may be sourced externally; Art. 6(10) permits outsourcing of compliance-verification tasks for the framework generally, which is a different provision and is tested by `dora_executive`. A crisp answer would need a reading, so it is a gap.
- **"What happens if the TLPT authority refuses to issue the attestation?"** — dropped. RTS Art. 5(1) mentions lack of compliance resulting in the attestation not being issued as a **risk to be assessed**, but neither instrument states a consequence. Nothing in this pilot asserts one.
- **"Does the 3-year TLPT clock run from the test or from the attestation?"** — dropped. Art. 26(1) says "at least every 3 years" and fixes no anchor event. Saying either would be invention.

---

## 7. Module metadata as drafted

- Module id: `dora_audit_readiness` · file: `data/dora_audit_readiness_pilot_DRAFT.json` (95 KB) · **20 questions** · **DE canonical + EN**
- Generator retained at `data/gen_dora_audit_readiness_draft.py` (deterministic, re-runnable; runs its own integrity, schema-parity, punctuation and orthography checks and exits non-zero on failure). Not referenced by any build path.
- `class: "ALL"` in meta; `class_scope: ["ALL"]` and `roles: ["all"]` on every question
- **Topic codes (4 × 5):** `testprogramm` (Testprogramm und allgemeine Testanforderungen), `tlpt_scoping` (TLPT: Anwendungsbereich, Häufigkeit und Testumfang), `tester_governance` (Tester, Unabhängigkeit und interne Revision), `nachweise_audit` (Nachweise, Dokumentation und Auditvorbereitung)
- **Points:** 12 × 4 points, 8 × 3 points — matching the `kartellrecht_pilot.json` / DORA-sibling scale
- **`high_stakes: true` on 10 questions** (2, 3, 6, 8, 12, 13, 16, 17, 18, 20) — the ones where a wrong answer produces either a missed statutory duty, a defective evidence file, or a false statement to a supervisor
- **`grundstoff: true` on 4** — one anchor question per topic (1, 6, 11, 16)
- **Answer key distributed exactly 5 × a / 5 × b / 5 × c / 5 × d**; verified programmatically, as is option-set integrity (`{a,b,c,d}` in both locales), the correct-key-exists-in-both-locales check, and ID uniqueness
- **Schema parity verified programmatically** against `data/kartellrecht_pilot.json`: identical question-object key list *and* order (`id, topic, topic_code, class_scope, grundstoff, legal_basis, points, high_stakes, question_type, image_ref, correct, text, explanation, roles`)
- **German orthography verified programmatically.** The emitted file contains **568 real umlaut/eszett characters** in total (ä 204, ö 68, ü 228, Ä 3, Ö 0, Ü 7, ß 58), of which **565 sit in the German question, option, explanation and topic fields** and 3 in German-language `meta` fields. An independent re-count over the raw file bytes, run separately from the generator's own check, returns the same figure. A residue scan for **48** ASCII-transliteration patterns (`fuer`, `ueber`, `muessen`, `koennen`, `waere`, `gefuehrt`, `ausschliesslich`, `faellt`, `maessig`, `groesse`, `zustaendig`, `behoerde`, `moeglich`, `spaetest`, `unverzueglich`, `gemaess`, `pruef`, `schaetz`, `vorfaelle`, `jaehrlich`, `massnahm`, `erfuell`, `haerte`, `verstoesse`, `regelmaessig`, `abhaengigkeit`, `geldbusse`, `vollstaendig`, `naechste`, `grundsaetzlich`, `durchfuehr`, `beruecksichtig`, `haeufigkeit`, `unabhaengig`, `maengel`, `schwaech`, `ueberprue`, `aenderung`, `loesung`, `auszufuehr`, `ergaenz`, `traeger`, `waehrend`, `nachtraeglich` and others) returns **zero hits**. A second, exhaustive audit tokenised every German-language string and listed every word containing `ae`/`oe`/`ue`/`ss` without a real umlaut; after whitelisting legitimately-ASCII German words (*dass, muss, Prozess, Abschlussbericht, Auffassung, voraussichtlich, Ressourcen, Fachkenntnisse, Klassifizierung, Regulierungsstandard, Zusammenfassung, Interessenkonflikte, Mindestdauer* and similar) and the English loanwords the RTS itself uses in German (*Blue Team, Red Team, Purple Teaming, Cyber, Charter*), the residue list is **empty**. Additionally: **no English-language field contains an umlaut** (0 occurrences), and `data/kartellrecht_pilot.json`'s punctuation convention is followed exactly — straight quotes only, ASCII hyphens only, no typographic quotes, no German low quotes, no en dashes or em dashes anywhere in the file, no non-breaking spaces, and no control characters.
- **Verbatim citation check:** **81/81** quoted legal fragments of six or more words matched the retrieved OJ text exactly (29 DORA DE, 29 DORA EN, 11 RTS DE, 12 RTS EN) — see §3.
- `meta.legal_disclaimer` carries the user's German boilerplate verbatim; `meta.legal_disclaimer_en` carries an English rendering
- `meta.acronym_note` records the CISA analysis in §0 inside the data file, so a rename cannot lose it
- `meta.renewal_months: null`, `renewal_basis: "not_specified_in_statute"` — with a note distinguishing the four genuine recurring duties in this area (yearly tests on CIF-supporting systems, Art. 24(6); yearly BCP/response-and-recovery testing, Art. 11(6)(a); yearly documentation and review of the framework, Art. 6(5); and TLPT at least every 3 years for identified entities, Art. 26(1)) from a training cadence, which neither instrument fixes
- `meta.legal_review_status` records the primary-source verification, both CELEX identifiers and OJ references, the negative corrigendum finding **with its positive control**, the ISO/certification negative check, the TIBER-EU characterisation, and points back to this dossier
- `meta.pass_rule_note` deliberately proposes no `EXAM_QUESTION_COUNT_BY_TYPE` / `MAX_ERROR_POINTS_BY_TYPE` / `EXAM_TOPIC_DRAW` values

---

## 8. Open items before this could move toward `data/dora_audit_readiness_pilot.json`

1. **Human legal review, in this order of value:** first **question 15's boundary against `dora_executive`** — it is the only place in the whole draft batch where two modules touch the same Article, and a reviewer should confirm the split (Art. 6(4) + the auditor-competence limb of 6(6) here; Art. 5(2)(f) + 6(6)/6(7) there) is a clean one rather than a duplication; then **question 18** and the §3.1 negative check, because it is the module's commercial core and its one claim that rests partly on an absence; then **question 20** and §4.2's characterisation of the TIBER-EU relationship; then the remaining Tier B questions 4, 5, 7, 16.
2. **Product decision on the module title (§0).** "Surviving the CISA Audit" should not ship. Recommended: "DORA Audit Readiness — Testing, Evidence and ISO 27001 Alignment", with the acronym confined to marketing copy where the audience is unambiguous. The roadmap's "ISO/IEC 27001:2022 as baseline" line in the credential list should be corrected in the same pass — it is a standard, not a personal credential.
3. **Product decision on §4.1 and §4.3.** The roadmap's 3A description should be replaced with the wording proposed at the end of §4.1, and **"exit-strategy documentation" removed from it** — that material is Module 2B's and now also has its own practitioner add-on. Separately: whoever writes the sales copy needs to be told, in writing, that "we map your ISO 27001 to DORA" must never become "your ISO 27001 gets you most of the way to DORA". The defensible pitch is the inverse and it is stronger: *here is precisely what your certificate does not cover, and here is the evidence a supervisor will ask for that your ISMS has never had to produce.*
4. **Product decision on §4.4 — the 3A / module 6 boundary.** Recommended split: 3A = audit perspective (what must exist, who signs, when due); module 6 = execution perspective (RTS Arts. 9–12 phase mechanics and the Annexes). Decide before either is marketed, because as currently described they sell against each other.
5. **Locale scope.** DE canonical + EN only, matching the roadmap's DE/EN target for 3A. If FR/ES/IT are ever added, they must be sourced from the **French, Spanish and Italian OJ language versions of both instruments**, not machine-translated. §4.5 is the evidence for why: the German version of the RTS alone contains two role-naming defects that a translator working from the English would silently "fix" into something the OJ does not say. The load-bearing terms to get right in each language are *threat-led penetration testing*, *test manager* versus *test lead*, *control team*, *scope specification document*, *attestation*, *remediation plan* and *internal validation methodologies*.
6. **Regulatory currency.** Delegated Regulation (EU) 2025/1190 is barely a year old and this family of Level 2 acts does get corrected after publication (the `dora_register` and `cra_supply_chain` dossiers both found corrigenda). Before any production release, re-run the consolidated-version probe in §1.2 **with the same positive control** and re-confirm RTS Arts. 2, 9, 11, 13 and 15, which carry every figure in this module. Separately, re-check whether the ECB has updated TIBER-EU again — question 20's explanation names the 2025 alignment and the November 2025 SSM implementation guide as background and would need a one-line refresh.
7. **Role vocabulary.** All 20 questions carry `roles: ["all"]`. The app's existing role vocabulary is `all`, `all_staff`, `management`, `hr`, `it`, `finance`. This module's real audience is an internal-audit / assurance role that does not exist in the vocabulary. **Six modules now** (2B, 1A, 4, 5, 2A, 3A) have audiences the vocabulary cannot express; this is well past the point where it should be resolved once as a product decision rather than per module.
8. **Module wiring.** Not done, by design: `build_modules.py`, `modules_manifest.json` and `app.js` untouched, no build run, nothing git-added. The 5/5/5/5 topic split suggests a 4- or 5-question draw touching every topic, but that is a design decision after sign-off.
9. **Decide on the two annexes** (gaps 1/2 and gap 13). The RTS phase mechanics plus Annexes I–VIII, and the TIBER-EU procedural material, are both genuinely wanted by this audience. The first is module 6's substance if module 6 is built (§4.4); the second belongs outside the statutory pool in a separately-labelled practice annex with an explicit "verify before each cycle" note, exactly as the three earlier dossiers recommended for their own practice material.
10. **Open the retention question with counsel (gap 3 in §6).** "How long do we keep TLPT evidence?" is the first thing this audience asks and neither instrument answers it. A short, separately-sourced national note (DE at minimum) would be disproportionately valuable relative to its length — but it is national law, not DORA, and must be labelled as such.

---

**Reminder:** this document and the accompanying JSON are draft training-content groundwork. They are not legal advice, have not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review.
