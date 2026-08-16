# DORA Art. 17-20 Vorfallmeldung module (`dora_incident`) — draft pilot content + pre-review dossier (2026-08-16)

**Status:** AI-prepared groundwork only — **NOT legal advice**. Attorney sign-off required before any commercial/production use. The draft question file exists at `data/dora_incident_pilot_DRAFT.json` and is **deliberately not wired into the live app**: it is not registered in `data/build_modules.py` or `data/modules_manifest.json`, `app.js` is untouched, no build step was run, and nothing was staged or committed. The `_DRAFT` suffix keeps it out of the live build path by construction.

**Subject:** 20-question DE/EN draft pilot for a new module, **"DORA Art. 17-20 — Meldung von IKT-Vorfällen"** / *DORA Incident Reporting* (internal working name `dora_incident`, roadmap module 5). Target audience: **IT operations, helpdesk/SOC staff and incident managers at EU financial entities who personally classify incidents and hit the clock** — not general staff, and not the management body. Schema follows `data/kartellrecht_pilot.json` field-for-field (verified programmatically: identical question-object key set **and** key order). Same pilot-then-scale discipline as the three sibling modules drafted this session (`dora_procurement`, `dora_executive`, `dora_register`): 20 questions DE/EN → 40 questions / wider locale set only after sign-off.

**This module exists to close a specific, named gap.** Both the 2026-08-13 `dora` dossier and the 2026-08-16 `dora_executive` dossier flagged the "4-hour rule" / initial-intermediate-final timings as **Tier C — sourced only from secondary summaries, never verified against Level 2 primary text**. That verification has now been performed, in full, in both language versions. **The Tier C flag is closed, and the secondary summaries turn out to have been materially incomplete** — see §4.

---

## 0. Method and instruments read

Every citation below was read on 2026-08-16 in the **official Official Journal text**, in both the **English and the German** language versions, retrieved from the EU Publications Office **Cellar** repository (`publications.europa.eu/resource/celex/<CELEX>`, `Accept: application/xhtml+xml`, `Accept-Language: eng` / `deu`). As all three sibling dossiers recorded, `eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge in this sandbox and `WebFetch` truncates inside the recitals; the Cellar route was used from the start and delivered complete documents in every case.

| Instrument | CELEX | OJ reference | Bytes EN / DE | What was read |
|---|---|---|---|---|
| Regulation (EU) 2022/2554 (DORA) | `32022R2554` | OJ L 333, 27.12.2022, p. 1 | 747 KB / 784 KB | Art. 3(8)–(14), (22); Art. 4(2); **Art. 16(1)**; **Art. 17, 18, 19, 20 in full**; Art. 21, 22, 23; Art. 46 — EN + DE |
| Commission Delegated Regulation (EU) **2024/1772** of 13 March 2024 (RTS — classification criteria, materiality thresholds) | `32024R1772` | OJ L, 2024/1772, 25.6.2024 | 90 KB / 93 KB | Recitals 1–18, **Art. 1–13 in full** — EN + DE |
| Commission Delegated Regulation (EU) **2025/301** of 23 October 2024 (RTS — content **and time limits** of initial notification, intermediate and final reports, and content of voluntary cyber-threat notifications) | `32025R0301` | OJ L, 2025/301, 20.2.2025 | 57 KB / 58 KB | Recitals 1–9, **Art. 1–7 in full** — EN + DE |
| Commission Implementing Regulation (EU) **2025/302** of 23 October 2024 (ITS — standard forms, templates and procedures) | `32025R0302` | OJ L, 2025/302, 20.2.2025 | 562 KB / 573 KB | Recitals, **Art. 1–9 in full**, **Annex I** (all fields), **Annex II** (data glossary, the fields used here), Annex III/IV headers — EN + DE |

### 0.1 Which Level 2 instrument holds what — and the mandate chain, confirmed in the citation clauses

The task brief asked me to find the *correct* Level 2 instruments rather than assume. There are **three**, not two, and the deadlines are in the one the sibling dossiers never named:

- **RTS (EU) 2024/1772** cites *"Article 18(4), third subparagraph"* DORA. It contains **the classification criteria, the materiality thresholds, and the definition of a major incident** — and **no reporting deadline whatsoever**.
- **RTS (EU) 2025/301** cites *"Article 20, third subparagraph"* DORA. It contains **the content of each of the three reports and — uniquely — the actual time limits.** Art. 20, first para, point (a)(ii) DORA is the mandate to *"determine the time limits for the initial notification and for each report referred to in Article 19(4)"*, and this is the instrument that discharges it.
- **ITS (EU) 2025/302** cites *"Article 20, fourth paragraph"* DORA, discharging the Art. 20(b) mandate for *"standard forms, templates and procedures"*. It contains the single reporting template (Annex I), the data glossary (Annex II), the cyber-threat template and glossary (Annexes III/IV), and procedural rules on secure channels, joint submission, reclassification, outsourcing and aggregated reporting.

**The brief's hypothesis was right and is now confirmed in text: the hour figures live in Level 2, not in the base Regulation.** Full-text negative check, run on the enacting text of Regulation (EU) 2022/2554 in **both** language versions:

| String searched | DORA EN | DORA DE | RTS 2024/1772 | RTS 2025/301 | ITS 2025/302 |
|---|---|---|---|---|---|
| `four hours` / `vier Stunden` | **0** | **0** | 0 | **2** | 0 |
| `24 hours` / `24 Stunden` | **0** | **0** | 1 (a *classification threshold*, not a deadline) | 2 | 0 |
| `72 hours` / `72 Stunden` | **0** | **0** | 0 | 1 | 0 |
| `one month` / `einen Monat` | 1 (Art. 31 CTPP designation — unrelated) | 1 (same) | 0 | 1 | 0 |

**Regulation (EU) 2022/2554 contains no hour-based incident-reporting deadline at all.** Art. 19(4) says only that the three submissions are made *"within the time limits to be laid down in accordance with Article 20, first paragraph, point (a), point (ii)"*. Anyone who cites "Art. 19 DORA" for the 4-hour figure is citing a provision that does not contain it.

### 0.2 Adoption and currency status — confirmed, not assumed

All three Level 2 instruments are **adopted, published, in force and directly applicable**. Each closes with *"This Regulation shall be binding in its entirety and directly applicable in all Member States"* and enters into force on the twentieth day following OJ publication (RTS 2024/1772 Art. 13; RTS 2025/301 Art. 7; ITS 2025/302 Art. 9). None is a draft, a guideline or an ESA consultation paper.

**Amendment/corrigendum check, with a positive control.** The `dora_register` sibling dossier found that its own ITS ((EU) 2024/2956) had been corrected by a corrigendum, and that the correction is visible through the Publications Office consolidation. I used the same route here, deliberately including that known-corrected instrument as a control:

| Consolidated-version probe | Result |
|---|---|
| `02024R2956-20241202` (control — known corrigendum) | **200, 294 KB** — consolidation exists |
| `02024R1772-20240715` | **404** |
| `02025R0301-20250312` | **404** |
| `02025R0302-20250312` | **404** |

Because the control returns a consolidation and the three incident instruments do not, **no amendment or corrigendum has been applied to Delegated Regulation (EU) 2024/1772, Delegated Regulation (EU) 2025/301 or Implementing Regulation (EU) 2025/302 as at 2026-08-16.** *(Caveat for the reviewer: absence of a consolidated version is strong but not conclusive evidence; a corrigendum published very recently could lag consolidation. Re-check before any production release — see §8.8.)*

### 0.3 Secondary / practical-guidance sources — consulted and quarantined

- **EBA Single Rulebook Q&A `2025_7613`, "Classification of phishing-attacks as a reportable major ICT-related incident"** (submitted by **BaFin** 04/11/2025, **Final Q&A published 06/02/2026**, on DORA Art. 3(8) and Arts. 6, 8, 9 of Delegated Regulation (EU) 2024/1772). Substance: phishing confined to a client's private sphere, not affecting the financial entity's own or its providers' services, is **not** an ICT-related incident under DORA and cannot trigger major-incident reporting; where the entity itself is targeted (phishing at employees, campaigns affecting its services) it may be an ICT-related incident and, if thresholds are met, a major one. This is genuinely useful for a SOC audience and is **the only secondary source in this dossier**. It is an ESA Q&A, i.e. **not a binding instrument**, so under the rule in §2 it cannot carry a High-confidence answer key. **No question in this pilot is written on it, and no answer key or distractor depends on it.** It is recorded here and in §5 gap 6 as a candidate for a separately-labelled practice annex.
- A web scan for the "4-hour rule" surfaced only vendor and law-firm commentary (regulation-dora.eu, Springlex, various consultancies). **None of it is cited.** As §4 shows, the branding those sources popularised is precisely the imprecision this module corrects.

---

## 1. Why this module, and why it does not repeat the shipped `dora` module

The shipped general-staff module (`data/dora_pilot.json`) devotes four questions to `meldepflichten`. They are the right depth for an Art. 13(6) all-staff awareness course and they are **not** enough for this audience — and, more importantly, **two of the four are imprecise or wrong when measured against the Level 2 text that has now been read** (see §4.2). The overlap risk is therefore inverted: the problem is not duplication, it is that the shipped module currently teaches an anchor point that the RTS does not use.

Three design decisions came out of the primary-source read:

1. **The spine of the module is the two-limbed initial-notification deadline** — because it is the single most commercially valuable fact the module teaches, because every secondary summary in circulation states it with one limb missing, and because the ITS reporting template makes both limbs individually auditable by the supervisor (fields 2.2 and 2.3). Four of the five `meldefristen` questions and one `meldeinhalt` question orbit it.
2. **Classification is taught as a structured gate test, not as a list of criteria.** Art. 8(1) RTS 2024/1772 is a two-stage construction — a mandatory critical-services gate, then *either* one specific threshold alone *or* two of the rest — and a learner who has memorised "six criteria in Art. 18(1)" cannot apply it. Question `klassifizierung-01` tests the structure and `klassifizierung-04` tests the case where the structure produces a counter-intuitive result.
3. **Four questions are operational-trap scenarios** (`vorfallmanagement-03` ticket closed without root cause, `klassifizierung-04` intrusion with no service impact, `klassifizierung-05` recurring low-severity outages, `meldeinhalt-01` "we can't report, we don't know the cause yet"). These are the four places where a competent SOC does the technically right thing and misses a statutory duty, and all four are answerable only from Level 2 text.

---

## 2. Citation ledger (primary-source verified 2026-08-16)

**Confidence rule used here** — identical to the `dora_procurement` and `dora_register` dossiers, restated so the reviewer can hold me to it:

- **"High — verbatim"** = the tested proposition is a direct restatement of wording I read in the OJ text of the cited provision, in **both** EN and DE.
- **"High — verbatim + synthesis"** = every element is verbatim, but the question combines **two or more** provisions I read separately; the reviewer should check that the *combination* is a fair statement, not the underlying text.
- **What disqualifies a claim from "High":** any of (a) the proposition rests wholly or partly on a source that is not the OJ text of a binding instrument — including ESA Q&As, FAQs, national-authority notices and vendor summaries; (b) the proposition requires an inferential step beyond the words on the page (legal characterisation, gap-filling, "this implies"); (c) the proposition was verified in only one language version where both exist; (d) the proposition rests on a **recital** rather than the enacting terms. Anything hitting (a)–(d) is either dropped or explicitly de-rated.
- **No question in this pilot carries a Medium or lower rating**, because questions that could not be grounded verbatim were dropped rather than written down-rated. They are logged in §6.
- **Mechanical verification performed:** 20 verbatim strings quoted in the question explanations (10 DE, 10 EN, spread across all four instruments) were re-matched programmatically against the retrieved OJ plain text after whitespace normalisation. **20/20 matched exactly; 0 failures.**

| # | Question ID | Citation | What's tested | Confidence |
|---|---|---|---|---|
| 1 | `vorfallmanagement-01` | Art. 17(1), (2) DORA | Recording duty covers **all** ICT-related incidents **and** all significant cyber threats — far wider than the reporting duty | High — verbatim (EN + DE) |
| 2 | `vorfallmanagement-02` | Art. 17(3)(a)–(f) DORA | Required contents of the incident-management process; classification logic must be built in ex ante, per the Art. 18(1) criteria | High — verbatim |
| 3 | `vorfallmanagement-03` | Art. 17(2) DORA | Scenario: restoration ≠ follow-up. Root causes must be identified, documented **and addressed** to prevent recurrence | High — verbatim |
| 4 | `vorfallmanagement-04` | Art. 16(1) subpara 1 DORA + Art. 8(2) final subpara RTS 2024/1772 | Simplified-framework entities: Chapter III applies **unchanged**; the only express relief is the recurring-incident carve-out | High — verbatim + synthesis (an in-text contrast between two instruments) |
| 5 | `vorfallmanagement-05` | Art. 19(3) subparas 1–2 DORA | Client-information duty: own trigger (financial interests), own clock (*without undue delay* on awareness), independent of the supervisory report | High — verbatim (EN + DE) |
| 6 | `klassifizierung-01` | Art. 8(1)(a), (b) RTS 2024/1772 (referencing its own Arts. 6 and 9) | **The gate test**: critical-services gate + [9(5)(b) alone OR 2+ of the other thresholds]; the gate does not count as one of the two | High — verbatim (the option restates Art. 8(1) including its internal cross-references) |
| 7 | `klassifizierung-02` | Art. 9(3) + Art. 3(1), (2) RTS 2024/1772 | Duration > 24 h / downtime > 2 h for CIF-supporting ICT services; how each is measured; estimates mandatory where resolution is open | High — verbatim |
| 8 | `klassifizierung-03` | Art. 9(1)(a)–(f), Art. 9(6) RTS 2024/1772 | The six alternative client/counterpart/transaction conditions incl. the 100 000-client absolute and the 30 % counterpart figure; EUR 100 000 economic threshold distinguished | High — verbatim |
| 9 | `klassifizierung-04` | Art. 6(c) + Art. 9(5)(b) + Art. 8(1)(a) RTS 2024/1772 (recital 10 in the explanation only) | Intrusion with **no** downtime, **no** client impact and **no** economic threshold can already be major | High — verbatim + synthesis (three provisions of one instrument; recital used only for rationale and labelled as such) |
| 10 | `klassifizierung-05` | Art. 8(2)(a)–(c) RTS 2024/1772 + Art. 3 ITS 2025/302 | Recurring incidents: ≥2 in 6 months, same apparent root cause, collectively meeting Art. 8(1); **monthly** assessment; aggregated form; microenterprise/Art. 16(1) carve-out | High — verbatim |
| 11 | `meldefristen-01` | **Art. 5(1)(a) RTS 2025/301** + Art. 19(4), Art. 20 first para (a)(ii) DORA | **The core fact**: as early as possible, in any case within 4 h of classification **and** no later than 24 h from becoming aware | High — verbatim (EN + DE, quoted in both in the explanation) |
| 12 | `meldefristen-02` | Art. 5(1)(a) read with Art. 5(2) RTS 2025/301 | The arithmetic case where the 24-hour limb binds and only 2 hours remain after classification | High on the text, **Medium-High on the cumulative reading** — see §4.1.3. Flagged Tier B; the single highest-value reviewer item |
| 13 | `meldefristen-03` | Art. 5(2) RTS 2025/301 | Late classification (day 4): duty does not lapse; 4 h from classification. Explanation warns this is not a licence to classify late (fields 2.2/2.3 expose the gap) | High — verbatim |
| 14 | `meldefristen-04` | Art. 5(1)(b), (c) RTS 2025/301 + Art. 19(4)(b), (c) DORA | Intermediate anchored to **submission of the initial notification**, not classification, and due **even without a status change**; final anchored to the (latest updated) intermediate | High — verbatim |
| 15 | `meldefristen-05` | Art. 5(4), (5), (6) RTS 2025/301 | Weekend/bank-holiday extension to **noon** of the next working day, and the credit-institution / CCP / trading-venue / NIS2 carve-out for initial and intermediate reports | High — verbatim |
| 16 | `meldeinhalt-01` | Art. 2(a)–(j) and Art. 4(a) RTS 2025/301 + Art. 1(3) ITS 2025/302 (recital 2 in the explanation only) | Root-cause analysis is **not** initial-notification content; estimates are mandatory where accurate data are unavailable | High — verbatim + synthesis (two instruments; recital labelled) |
| 17 | `meldeinhalt-02` | Art. 5(3) RTS 2025/301 + Art. 4(1), (2) ITS 2025/302 (+ Art. 19(1) subpara 4, Art. 19(6) DORA) | Missed deadline → notify **within** the deadline, with reasons; secure-channel failure → other secure means by agreement + later resubmission; addressee stays the NCA | High — verbatim + synthesis |
| 18 | `meldeinhalt-03` | ITS 2025/302 Annex I fields 2.2/2.3 and Annex II glossary entries | Both the awareness timestamp **and** the classification timestamp are mandatory in the initial notification, ISO 8601 UTC — which is what makes both limbs auditable | High — verbatim (EN + DE glossary entries quoted) |
| 19 | `meldeinhalt-04` | Art. 19(5) DORA + Art. 6(1)–(3), Art. 7(1), (2) ITS 2025/302 | Outsourced reporting: permitted, entity **remains fully responsible**, notification duties, aggregated-report conditions and the significant-CI/venue/CCP exclusion | High — verbatim + synthesis (EN + DE) |
| 20 | `meldeinhalt-05` | Art. 5 ITS 2025/302 + Art. 2(i) RTS 2025/301 | Reclassification is a **retrospective** test ("at no time fulfilled"), not "the incident is over" or "the estimate turned out lower" | High — verbatim |

**Tier A — verbatim, single instrument-location, lowest review burden (14):** 1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 14, 15, 18, 20.
**Tier B — verbatim but combining provisions or requiring a reading; reviewer should check the combination, not the text (6):** 4, 9, 12, 16, 17, 19.
**Tier C — any claim resting on a secondary source: none.** No question's correct answer, and no distractor's wrongness, depends on an ESA Q&A, an FAQ, a national-authority notice or a vendor summary. **This closes the Tier C flag carried by the 2026-08-13 `dora` dossier and repeated in the `dora_executive` dossier §4/§6.1.**

---

## 3. Deliberate non-assertions — what the distractors are built to punish

Recorded explicitly so no scale-up quietly reintroduces them.

1. **"The 4-hour clock starts at detection / first alert."** Question 11 distractor (a). It starts at classification — *but see 2.*
2. **"4 hours from classification is the whole rule."** Question 11 distractor (b) — the *more dangerous* error, because it is what almost every secondary summary says, and because it silently deletes the 24-hour outer limit that in the common case binds first. See §4.1.
3. **"The 72-hour intermediate deadline runs from classification."** Question 14 distractor (a). It runs from **submission of the initial notification**. This distractor is worded to match the shipped `dora` module's current text — see §4.2.
4. **"The one-month final-report deadline runs from the incident."** Also question 14 distractor (a). It runs from the intermediate report, or the latest updated intermediate report.
5. **"No intermediate report is due if nothing has changed."** Question 14. Art. 5(1)(b) RTS says the opposite in terms: *"auch wenn sich … der Status oder die Handhabung des Vorfalls nicht geändert hat"*.
6. **"Missing the deadline once classification slipped past 24 hours means there is nothing left to do."** Question 13 distractor (b). Art. 5(2) expressly governs that case.
7. **"An incident with no downtime and no affected clients cannot be major."** Question 9 distractor (b). Art. 6(c) + Art. 9(5)(b) + Art. 8(1)(a) dispose of it.
8. **"Two of the six Art. 18(1) DORA criteria make an incident major."** Question 6 distractor (a). The test is Art. 8(1) RTS, and the critical-services element is a gate, not a countable criterion.
9. **"You cannot report before you know the root cause."** Question 16 distractors (a) and (b). Art. 2 RTS 2025/301 does not ask for it; Art. 4 does, for the final report.
10. **"Uncertainty justifies delay."** Questions 7 and 16. Estimates are expressly mandated (Art. 3(1) third subpara and Art. 9(1) second subpara RTS 2024/1772; Art. 1(3) ITS 2025/302).
11. **"Reclassify to non-major once the incident is resolved / turned out cheaper."** Question 20 distractors (a) and (c). The test is "at no time fulfilled".
12. **"Small / simplified-framework entities have easier reporting deadlines."** Question 4 distractors (b) and (c). Art. 16(1) disapplies Arts. 5–15 only.
13. **"Outsourcing the reporting transfers the responsibility."** Question 19 distractor (c). Art. 19(5) second sentence.
14. **"Every major incident requires client notification."** Question 5 distractor (d). Art. 19(3) has its own trigger.
15. **"The weekend rule is available to everyone."** Question 15 distractor (a). Art. 5(5) removes it from banks, CCPs, trading-venue operators and NIS2 essential/important entities for the initial and intermediate reports.

---

## 4. Findings where existing research / shipped content is imprecise against the primary text

The task asked me to check the briefing rather than confirm it. Five findings, two of them material.

### 4.1 The roadmap's "timing starts at formal Major Incident classification, not first alert" is **half right, and the missing half is the half that usually bites**

The project roadmap (`claude/dora-cra-b2b-training-roadmap-2026-08-16.md`) describes module 5 as: *"3-stage notification — initial/intermediate/final — timing starts at formal Major Incident classification, not first alert"*. Measured against Art. 5 of Delegated Regulation (EU) 2025/301, that sentence is **correct about stage 1's primary anchor, incomplete about stage 1's outer limit, and wrong about stages 2 and 3.**

#### 4.1.1 The verbatim text

**Art. 5(1)(a), DE (OJ, verified verbatim):**
> *"bei der Erstmeldung: so früh wie möglich, in jedem Fall aber **innerhalb von vier Stunden nach Einstufung** des IKT-bezogenen Vorfalls als schwerwiegend **und spätestens 24 Stunden nach dem Zeitpunkt, zu dem das Finanzunternehmen Kenntnis von dem IKT-bezogenen Vorfall erlangt hat**"*

**Art. 5(1)(a), EN (OJ, verified verbatim):**
> *"for the initial report: as early as possible, but in any case, **within four hours from the classification** of the ICT-related incident as a major ICT-related incident **and no later than 24 hours from the moment the financial entity has become aware** of the ICT-related incident"*

**Art. 5(2), DE (OJ, verified verbatim):**
> *"Hat das Finanzunternehmen einen IKT-bezogenen Vorfall **nicht innerhalb von 24 Stunden** nach dem Zeitpunkt, zu dem es Kenntnis von dem IKT-bezogenen Vorfall erlangt hat, sondern erst zu einem späteren Zeitpunkt als schwerwiegend eingestuft, übermittelt es die Erstmeldung **innerhalb von vier Stunden**, nachdem es den IKT-bezogenen Vorfall als schwerwiegend eingestuft hat."*

#### 4.1.2 The answer to the question the brief asked, stated precisely

> **There is not one clock. There are two, running from two different events, and the initial notification is due when the *first* of them expires.**
>
> - **Clock A** starts at **formal classification of the incident as major**, and runs **4 hours**.
> - **Clock B** starts at **the moment the financial entity became aware of the incident** (the ITS glossary defines the reported "date and time of detection" as exactly this: *"Datum und Uhrzeit der Kenntnisnahme des IKT-bezogenen Vorfalls durch das Finanzunternehmen"* / *"Date and time at which the financial entity has become aware of the ICT-related incident"*), and runs **24 hours**.
> - **Only where classification happens later than 24 hours after awareness does Clock B drop away and Clock A alone govern** — that is what Art. 5(2) is for, and it is the *only* case in which "timing starts at classification" is a complete statement of the rule.

So the roadmap's framing is safe **only** in the late-classification case and misleading in the ordinary one. In the ordinary case — a SOC that becomes aware in the morning and classifies during the day — **the earlier of the two deadlines is very often Clock B**, and a team trained on "you get 4 hours from classification" will file late while believing it is early. Worked example, tested as question 12: aware Monday 08:00, classified Tuesday 06:00 → Clock A expires Tuesday 10:00, Clock B expires Tuesday 08:00, **the notification is due Tuesday 08:00 — two hours after classification, not four.**

#### 4.1.3 The one interpretive step, flagged honestly

The two limbs are joined by *"und"* / *"and"*, which on its face makes them cumulative, so the earlier-expiring limb governs. Art. 5(2) corroborates that reading: it exists precisely to restore Clock A for the case where Clock B has already run out, and would be redundant if Clock B were subordinate. **That is a reading of the wording, not a quotation of it**, so question 12 is Tier B and is named in §8 as the highest-value item for a lawyer's hour. Questions 11 and 13 do **not** depend on it — they quote the two limbs and Art. 5(2) respectively without resolving their interaction.

#### 4.1.4 The roadmap's "timing starts at classification" is simply wrong for stages 2 and 3

Neither the intermediate nor the final report is anchored to classification at all:

- **Intermediate: 72 hours from *submission of the initial notification*** — *"spätestens 72 Stunden nach Übermittlung der Erstmeldung"* — and expressly due **even where the status or handling of the incident has not changed**, notwithstanding the wording of Art. 19(4)(b) DORA. Updated intermediate reports are due *without undue delay* and in any event once regular activities have been recovered.
- **Final: no later than one month after the intermediate report, or, where applicable, after the latest updated intermediate report.** Not one month from the incident, not from detection, not from classification.

**Recommended roadmap wording, replacing the current sentence:** *"3-stage notification — initial / intermediate / final. The initial notification is due within 4 hours of classification as major AND no later than 24 hours from becoming aware of the incident, whichever comes first; the intermediate report within 72 hours of submitting the initial notification, even if nothing has changed; the final report within one month of the (latest updated) intermediate report."*

### 4.2 The shipped `dora_pilot.json` incident content: one answer key survives, one option statement is factually wrong, and one explanation mischaracterises the law

The shipped general-staff module carries four `meldepflichten` questions. Assessed against the now-verified Level 2 text:

| Shipped question | Verdict |
|---|---|
| `dora-meldepflichten-01` (Art. 18 + RTS 2024/1772, classification criteria) | **Key correct, depth thin.** Option (b) fairly paraphrases the Art. 18(1) criteria list and "not a single metric" is right. It does not convey that the operative test is the Art. 8(1) RTS gate construction. Defensible for an awareness module; no correction needed. |
| `dora-meldepflichten-02` (initial deadline; correct answer (a) "within 4 hours of classification") | **Key survives as best-of-four; the option text is materially incomplete and the explanation is wrong in its characterisation.** The option omits the 24-hour-from-awareness limb entirely. The explanation states *"Die Uhr beginnt mit der Klassifizierung, nicht mit der Entdeckung — die Klassifizierung selbst soll aber ohne schuldhaftes Zögern erfolgen (in der Praxis meist binnen rund 24 Stunden nach Entdeckung)"*. **The 24 hours is not a practice norm about when to classify. It is a binding outer limit on when to *report*, laid down in Art. 5(1)(a) of Delegated Regulation (EU) 2025/301.** Recommend rewriting option (a) and the explanation; the module's own `PRUEFHINWEIS` already invites exactly this. |
| `dora-meldepflichten-03` (correct answer (a) "intermediate within 72 hours **of classification**, final within one month of the intermediate") | **The option statement is factually wrong on the anchor.** Art. 5(1)(b) RTS 2025/301: *72 hours from submission of the initial notification*. The final-report half is right but omits *"or the latest updated intermediate report"*, and the option does not carry the "even where nothing has changed" rule. The answer key still selects the least-wrong option, which is precisely the failure mode a Big-4 auditor exposes. **Recommend correcting the option text.** |
| `dora-meldepflichten-04` (recipient + voluntary cyber-threat notification) | **Correct and holds up.** Art. 19(1) (report to the relevant competent authority under Art. 46) and Art. 19(2) (voluntary notification of significant cyber threats) both verified. The BaFin example is a national illustration, not an assertion about DORA. |

**Two of the four therefore need a wording edit before the shipped module can be considered accurate on this topic.** Changing shipped content is out of scope for this task and is logged, not done — see §8.4.

*(Separate, non-legal observation on the same file: `data/dora_pilot.json` writes its entire German text in ASCII transliteration — "Vorfaelle", "zustaendige", "Ausschliesslich", "gestuetzt". `data/kartellrecht_pilot.json` and this draft both use proper orthography. That is a content-quality inconsistency worth resolving in the same edit pass, but it is a separate decision from the legal corrections above.)*

### 4.3 The "4-hour rule" as a branded concept has no home in DORA and only a partial home in the RTS

The phrase does not appear in any of the four instruments. What exists is a compound deadline in one sub-point of one Article of one delegated regulation. Two consequences for course and marketing copy:

1. **Never cite "Art. 19 DORA" for the 4 hours.** Art. 19(4) delegates the timing question outward in terms. The correct citation is **Art. 5(1)(a) of Commission Delegated Regulation (EU) 2025/301**, with Art. 19(4) and Art. 20, first para, point (a)(ii) DORA as the mandate chain.
2. **Never sell the module as "the 4-hour rule" without the second limb.** The commercially defensible pitch is the opposite: *the reason you need this training is that the rule everyone calls "the 4-hour rule" has a second deadline in it that most summaries drop.*

### 4.4 What the sibling dossiers said about this area, checked

- The **2026-08-13 `dora` dossier** flagged the deadlines Tier C and asked for a primary-source re-check. **Done; the flag is closed.** Its instinct was right: the secondary summaries it relied on were incomplete in exactly the way described in §4.1.
- The **`dora_executive` dossier §6.1** named *"Art. 19 + RTS 2024/1772, RTS 2025/301"* as the home of the deadlines and referred module 5 to them. **Partly right, and one instrument short.** RTS 2024/1772 contains no deadline of any kind; RTS 2025/301 contains all of them; and **Implementing Regulation (EU) 2025/302, which neither sibling dossier names, contains the template, the mandatory timestamp fields, and the procedural rules (secure channels, joint submission, reclassification, outsourcing notification, aggregated reporting)** that make the deadlines operable. Six of this pilot's twenty questions are unanswerable without it.
- The **`dora_register` dossier**'s methodological finding — that a Level 2 instrument in this area had been silently corrected after publication — is what motivated the positive-control corrigendum check in §0.2. That check came back clean for all three incident instruments.

### 4.5 A residual drafting defect in the ITS, noted for the reviewer

**Art. 5 of Implementing Regulation (EU) 2025/302** (reclassification) instructs entities to provide the information *"in der Vorlage in **Anhang II** dieser Verordnung"* / *"in the template laid down in **Annex II** to this Regulation"*. But Annex II is the **data glossary and instructions**; the reporting template is **Annex I** (Art. 1(1) says so expressly, and Art. 1(5) tells entities to follow "the data glossary and instructions set out in Annex II" when completing the Annex I template). The cross-reference in Art. 5 is therefore wrong on its face in **both** language versions. The intent is unambiguous — reclassification is reported through the Annex I template, using the "type of submission" field, whose closed choice list in Annex II includes *"major incident reclassified as non-major"*, plus "other information". **Question 20 is written on the intent and states the defect explicitly in its own explanation.** No answer depends on it. Flagged in case a corrigendum lands later (compare the `B_06.01` renumbering the `dora_register` dossier found in the register ITS).

---

## 5. Gap list — covered by the primary sources but deliberately **not** tested by this 20-question pilot

1. **The full Annex I / Annex II field catalogue.** Only fields 1.1, 2.2, 2.3 and the 2.5 criteria list are touched. The intermediate-report block (3.1–3.x: affected clients/counterparts counts and percentages, functional areas, infrastructure components, indicators of compromise, reporting to other authorities) and the final-report block are read but untested. Prime material for the 40-question scale-up, and the natural home for a "fill the template correctly" exercise.
2. **Annexes III and IV (voluntary significant-cyber-threat template and glossary) and Art. 6 RTS 2025/301 (content of the voluntary notification).** Read; only the *existence* of the voluntary channel is touched, and only inside question 5's neighbourhood. Deliberately left out because voluntary notification is a policy decision above SOC pay grade; better as a management-facing add-on.
3. **Art. 10 RTS 2024/1772 (high materiality thresholds for significant cyber threats).** Read in full; untested. It is a three-condition cumulative test with its own sub-criteria and deserves its own question rather than a footnote.
4. **Art. 7 RTS 2024/1772 (economic impact: the eight includable cost categories and the three expressly excluded ones — general maintenance, post-incident enhancements, insurance premiums).** Read; only the EUR 100 000 figure is used, in question 8's explanation. The exclusion list is a genuinely good scale-up question because it is counter-intuitive.
5. **Art. 2 RTS 2024/1772 (reputational impact) and Art. 4 (geographical spread) in their own right.** Read; referenced only as thresholds in question 8's neighbourhood.
6. **The phishing scoping question** (EBA Q&A `2025_7613`, §0.3). Highly relevant to a helpdesk/SOC audience and deliberately **not** tested, because a correct answer would rest on an ESA Q&A and would therefore be Tier C under the rule in §2. If the product owner wants it — and there is a real argument that this audience needs it — it belongs in a **separately-labelled, separately-reviewed "supervisory practice" annex** with its own currency-check cadence, exactly as recommended for the register module's submission mechanics.
7. **Art. 23 DORA — operational or security payment-related incidents.** Read: Chapter III applies equally to (major) operational or security payment-related incidents for credit institutions, payment institutions, account information service providers and e-money institutions. Untested because doing it properly means teaching the parallel Art. 3(9)/(11) definitions and the PSD2 heritage, which is a payments-specific module.
8. **Art. 19(1) subparas 2–3 and Art. 19(6)–(8) DORA — the supervisory routing layer** (single competent authority where several supervise; significant credit institutions reporting via the national authority which forwards to the ECB; onward distribution to EBA/ESMA/EIOPA, ECB, NIS2 CSIRTs, resolution authorities/SRB; cross-border relevance assessment; the CSD host-Member-State rule). Read; only the "addressee stays the NCA" point survives, inside question 17's explanation. This is supervisory architecture, not SOC procedure.
9. **Art. 21 (single EU Hub feasibility report) and Art. 22 (supervisory feedback; annual anonymised ESA reporting).** Read; untested. Art. 22(1)'s closing sentence — entities *"remain fully responsible for the handling and for consequences of the ICT-related incidents reported"* despite supervisory feedback — is a good scale-up item.
10. **Art. 2 ITS 2025/302 (joint submission of two or all three reports where regular activities have recovered or root-cause analysis is complete, provided the Art. 5 time limits are met).** Read; untested, though it is genuinely useful operationally. Deliberately omitted to keep the deadline topic focused on the anchors rather than on optimisations.
11. **Any national implementation or supervisory-portal specifics** (BaFin MVP portal, KNF, BNR/ASF, CSSF eDesk). Nothing national is asserted anywhere in this pilot — the only national reference in the whole draft is that the addressee is "the competent authority", quoting Art. 19(1). That is the safe state; the roadmap targets DE/EN/FR/ES/IT for this module and a national layer would need its own sourcing.
12. **The DORA/NIS2 relationship.** Art. 5(5) RTS 2025/301 borrows the NIS2 essential/important-entity classification, and recital 1 says the time limits should be "at least equivalent in effect" to NIS2's. The interaction is real, high-interest and high-oversimplification-risk; the same reasoning as the two earlier dossiers applies, and it is left out.
13. **Penalties for late or defective reporting.** Not tested. DORA sets no EU-wide amount (established in the `dora_executive` dossier §3.1/§3.3 and not re-litigated here), and anything specific would be national law not read today.

---

## 6. Questions considered and dropped (grounding failures, logged rather than written)

Per the brief's instruction not to write anything that cannot be grounded in verbatim primary text:

- **"How quickly must an incident be classified after detection?"** — dropped. **There is no classification deadline anywhere in the four instruments.** Art. 17(3)(b) DORA requires classification *procedures*; Art. 5(1)(a)/(2) RTS 2025/301 attach consequences to when classification happens but set no independent limit on it. The nearest true statement — that a late classification shortens nothing but is fully visible via template fields 2.2/2.3 — is taught inside question 13's explanation instead. **The commonly repeated "classify within 24 hours" is not a rule; it is the reporting outer limit misread as a classification limit.**
- **"Is phishing a reportable incident?"** — dropped as a question; it would rest on the EBA Q&A. Became gap 6.
- **"In what file format / through which portal is the report submitted?"** — dropped. The ITS requires "secure electronic channels as made available by their competent authority" and prescribes no format; anything more specific is national supervisory practice.
- **"How many data fields does the reporting template have?"** — dropped. No such figure is stated in the ITS, and a self-performed count is not a regulatory figure. Same discipline as the `dora_register` dossier §4.5.
- **"What happens if you report an incident that turns out not to be major?"** — partly dropped. The reclassification mechanics are tested (question 20); the *consequences* of an over-report are not addressed anywhere in the four instruments and no question asserts any.
- **"Does the 4-hour clock pause overnight / outside business hours?"** — dropped as a general question. The only temporal relief in the text is the weekend/bank-holiday rule of Art. 5(4) with its Art. 5(5)/(6) carve-outs, which is tested as question 15. There is no night-time or out-of-hours suspension, and the module says nothing implying one.
- **"Who inside the entity must sign off the classification?"** — dropped. Art. 17(3)(c) requires roles and responsibilities to be assigned but names no function; anything more would be invented.

---

## 7. Module metadata as drafted

- Module id: `dora_incident` · file: `data/dora_incident_pilot_DRAFT.json` · **20 questions** · DE canonical + EN
- Generator retained at `data/gen_dora_incident_draft.py` (deterministic, re-runnable, runs its own integrity and orthography checks and exits non-zero on failure). Not referenced by any build path.
- `class: "ALL"` in meta; `class_scope: ["ALL"]` and `roles: ["all"]` on every question
- **Topic codes (4 × 5):** `vorfallmanagement` (Vorfallmanagement und Erkennung), `klassifizierung` (Klassifizierung und Wesentlichkeitsschwellen), `meldefristen` (Meldefristen und Meldekaskade), `meldeinhalt` (Meldeinhalte, Vorlagen und Verfahren)
- **Points:** 12 × 4 points, 8 × 3 points — matching the `kartellrecht_pilot.json` / `dora_register` scale
- **`high_stakes: true` on 10 questions** (5, 6, 9, 11, 12, 14, 15, 16, 19, 20) — the ones where a wrong answer produces either a missed statutory deadline or a false statement to a supervisor
- **`grundstoff: true` on 4** — one anchor question per topic (1, 6, 11, 16)
- **Answer key distributed exactly 5 × a / 5 × b / 5 × c / 5 × d**; verified programmatically, as is option-set integrity (`{a,b,c,d}` in both locales), the correct-key-exists-in-both-locales check, and ID uniqueness
- **Schema parity verified programmatically** against `data/kartellrecht_pilot.json`: identical question-object key list *and* order
- **German orthography verified programmatically.** The emitted file contains **415 real umlaut/eszett characters** (ä/ö/ü/Ä/Ö/Ü/ß). A residue scan for ASCII-transliteration patterns (`fuer`, `ueber`, `muessen`, `koennen`, `waere`, `gefuehrt`, `ausschliesslich`, `faellt`, plus `maessig`, `groesse`, `zustaendig`, `behoerde`, `moeglich`, `spaetest`, `unverzueglich`, `gemaess`, `pruef`, `schaetz`, `vorfaelle`, `jaehrlich`, `massnahm`, `erfuell`) returns **zero hits**. A second, exhaustive audit tokenised every German-language string and listed every word containing `ae`/`oe`/`ue`/`ss` without a real umlaut: the only survivors are legitimately ASCII German words (*Dauer, dauert, gedauert, Datenquellen, genaue, Konsequenz*, plus correct `ss` words such as *Prozess, Beschluss, dass, muss, abgeschlossen, Wesentlichkeitsschwelle*). Additionally: **no English-language field contains an umlaut**, and `data/kartellrecht_pilot.json`'s punctuation convention (straight quotes, ASCII hyphens, no typographic dashes) is followed exactly.
- `meta.legal_disclaimer` carries the user's boilerplate verbatim: *"Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall durch qualifizierte Juristen oder Wirtschaftsprüfer zu validieren."*
- `meta.renewal_months: null`, `renewal_basis: "not_specified_in_statute"` — with a note distinguishing the two genuine recurring duties in this area (the **monthly** recurring-incident assessment under Art. 8(2) RTS 2024/1772; the **yearly** ESA aggregate reporting under Art. 22(2) DORA) from a training cadence, which none of the four instruments fixes
- `meta.legal_review_status` records the primary-source verification, names all four CELEX identifiers and OJ references, records the negative corrigendum finding, and points back to this dossier
- `meta.pass_rule_note` deliberately proposes no `EXAM_QUESTION_COUNT_BY_TYPE` / `MAX_ERROR_POINTS_BY_TYPE` / `EXAM_TOPIC_DRAW` values

---

## 8. Open items before this could move toward `data/dora_incident_pilot.json`

1. **Human legal review, in this order of value:** first **§4.1.3** — the cumulative reading of the two limbs of Art. 5(1)(a), which is the module's commercial core and its one genuine interpretive step, and on which question 12 alone depends; then Tier B questions 4, 9, 16, 17, 19; then §4.5 (the ITS Art. 5 cross-reference defect).
2. **Product decision on §4.1's downstream effect.** The roadmap sentence describing module 5 should be replaced with the wording proposed at the end of §4.1.4. Any marketing copy that says "the 4-hour rule" without the 24-hour limb should be reworded — the second limb is a better sales argument than the first.
3. **Decide whether the module should be *named* after the 4-hour rule at all.** The roadmap calls it "Incident Reporting & the 4-hour rule". That title sells, and it also repeats the imprecision. Recommendation: keep the phrase in marketing as the hook, but never in a question, an explanation, or a citation.
4. **Correct the shipped `dora` module per §4.2** — `dora-meldepflichten-02` (option text + explanation) and `dora-meldepflichten-03` (option text). This is now the fourth module dossier to raise a correction against shipped content; batching them into one deliberately-reviewed edit is cheaper than four separate passes. The German-orthography inconsistency in the same file should ride along.
5. **Role vocabulary.** All 20 questions carry `roles: ["all"]`. The app's existing role vocabulary is `all`, `all_staff`, `management`, `hr`, `it`, `finance`. This module's real audience is `it` plus a SOC/incident-manager role that does not exist. Four modules now (2B, 1A, 4, 5) have audiences the vocabulary cannot express; worth resolving once as a product decision rather than per module.
6. **Module wiring.** Not done, by design: `build_modules.py`, `modules_manifest.json` and `app.js` untouched, no build run, nothing git-added. The 5/5/5/5 topic split suggests a 4- or 5-question draw touching every topic, but that is a design decision after sign-off.
7. **Locale scope.** DE canonical + EN only. The roadmap targets DE/EN/FR/ES/IT for this module. FR, ES and IT must be sourced from the **French, Spanish and Italian OJ versions** of all four instruments, not machine-translated from the DE — "Einstufung"/"classification", "Kenntnisnahme"/"become aware" and "Übermittlung"/"submission" are the three load-bearing terms in the deadline rule and each is a legally defined expression in every language version.
8. **Regulatory currency.** The two 2025 instruments are recent, and the sibling `dora_register` dossier established that this family of Level 2 acts does get corrected after publication. Before any production release, re-run the consolidated-version probe in §0.2 (with the same positive control) and re-confirm that Art. 5 of Delegated Regulation (EU) 2025/301 is unamended. If any part of this module ever moves, it will be that Article.
9. **Decide on the practice annex** (gap 6 / §0.3). The phishing-scoping Q&A is exactly the kind of question a helpdesk asks on day one. Recommendation: yes, but in a separately-labelled, separately-reviewed annex with an explicit "verify before each cycle" note — never inside the statutory question pool.

---

**Reminder:** this document and the accompanying JSON are draft training-content groundwork. They are not legal advice, have not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review.
