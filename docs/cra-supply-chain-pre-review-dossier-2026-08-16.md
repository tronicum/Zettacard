# CRA Secure Supply Chain & Vulnerability Handling module (`cra_supply_chain`) — draft pilot content + pre-review dossier (2026-08-16)

**Status:** AI-prepared groundwork only — **NOT legal advice**. Attorney sign-off required before any commercial/production use. The draft question file exists at `data/cra_supply_chain_pilot_DRAFT.json` and is **deliberately not wired into the live app**: it is not registered in `data/build_modules.py` or `data/modules_manifest.json`, `app.js` is untouched, no build step was run, and nothing was staged or committed. The `_DRAFT` suffix keeps it out of the live build path by construction.

**Subject:** 20-question **EN-canonical** (+ DE) draft pilot for a new module, **"CRA — Secure Supply Chain & Vulnerability Handling"** (internal working name `cra_supply_chain`, roadmap module 2A, which the roadmap calls "Secure Supply Chain Coding"). Target audience: **DevSecOps engineers, CTOs and software supply-chain / security engineering staff at manufacturers of "products with digital elements"** — the people who own the build pipeline, the dependency tree and the on-call rota, not compliance officers and not the board. Schema follows `data/kartellrecht_pilot.json` field-for-field (verified programmatically: identical question-object key set **and** key order).

**Locale decision, stated explicitly so nobody "fixes" it later.** The four DORA sibling dossiers drafted this session (`dora_procurement`, `dora_executive`, `dora_register`, `dora_incident`) are all **DE-canonical**. This module is **EN-canonical by deliberate audience decision**: the roadmap targets **EN/PL/RO** for module 2A because the addressable audience is the Polish and Romanian nearshore engineering market, where English is the working language of the discipline and German is not spoken in the room. German is produced here as a **secondary** locale, to the same quality bar and checked against the German OJ language version rather than machine-translated from the English, so the module stays consistent with the project's DE+EN pilot pattern. `meta.canonical_locale` is `"en"` and `meta.canonical_locale_note` records the reason inside the data file.

**Subject-matter warning for reviewers coming from the DORA dossiers:** this module is about **Regulation (EU) 2024/2847 (Cyber Resilience Act)**, a product-safety/CE-marking instrument addressed to *manufacturers*. It shares nothing legally with DORA (Regulation (EU) 2022/2554), which is a financial-sector operational-resilience instrument addressed to *financial entities*. Only the **method** is carried over from the sibling dossiers. Where the two regimes look superficially similar — both have 24h/72h/final-report cascades — they differ in ways this module tests directly (see §4.3).

---

## 0. Method and instruments read

Every citation below was read on 2026-08-16 in the **official Official Journal text**, in both the **English and the German** language versions, retrieved from the EU Publications Office **Cellar** repository (`publications.europa.eu/resource/celex/<CELEX>`, `Accept: application/xhtml+xml`, `Accept-Language: eng` / `deu`). As all four DORA sibling dossiers recorded, `eur-lex.europa.eu` sits behind an AWS WAF JavaScript challenge in this sandbox and `WebFetch` truncates before reaching the articles; the Cellar route was used from the start and delivered complete documents in every case.

| Instrument | CELEX | OJ reference | Bytes EN / DE | What was read |
|---|---|---|---|---|
| **Regulation (EU) 2024/2847** — Cyber Resilience Act | `32024R2847` | OJ L, 2024/2847, **20.11.2024** | 711 KB / 751 KB | Recitals (incl. 76, 77); **Art. 1–3 in full**; Art. 4–12; **Art. 13, 14, 15, 16, 17 in full**; Art. 18–20, 24–26; Art. 64; **Art. 69, 70, 71 in full**; **Annex I (Parts I and II) in full**; **Annex II in full**; Annex III/IV headings; **Annex VII in full** — EN + DE |
| **Consolidated text** of the same, incorporating all corrigenda | `02024R2847-20241120` (version 000.003) | — | 381 KB / 398 KB | **Full enacting text, diffed word-by-word against the base OJ text in both languages** — EN + DE |
| **Commission Delegated Regulation (EU) 2026/881** of 11 December 2025 — terms and conditions for the cybersecurity-related grounds for delaying dissemination of notifications (the Art. 14(9) mandate) | `32026R0881` | OJ L, 2026/881, **20.4.2026** | 29 KB / 31 KB | **Art. 1–6 in full** — EN + DE |

The CELEX number was **found, not assumed**: `32024R2847` was confirmed by retrieving the document and reading its own OJ header (`L_202402847EN.000101.fmx.xml`, "REGULATION (EU) 2024/2847 … of 23 October 2024 … (Cyber Resilience Act)", OJ L series, 20.11.2024).

### 0.1 Corrigendum check — and it did not come back clean

The `dora_register` dossier established that instruments in this family get silently corrected after OJ publication, and the `dora_incident` dossier turned that into a standing probe. Run here, the probe **fires**:

| Probe | Result |
|---|---|
| `02024R2847-20241120` (EN) | **200, 381 KB — a consolidation exists** |
| `02024R2847-20241120` (DE) | **200, 398 KB — a consolidation exists** |
| `02024R2847-20250101` (control for a wrong date) | 404 |
| `02024R2956-20241202` (positive control, the known-corrected DORA register ITS) | 200, 294 KB |

**The Cyber Resilience Act has been corrected three times.** The EN consolidation lists: Corrigendum, **OJ L, 2024/90780, 5.12.2024**; Corrigendum, **OJ L, 2025/90555, 2.7.2025**; Corrigendum, **OJ L, 2025/90828, 17.10.2025**. The DE consolidation lists only two (2.7.2025 and 17.10.2025) — the 5.12.2024 corrigendum was EN-specific.

Because a corrigendum can move an answer key, I did not stop at "a consolidation exists". I **diffed the full enacting text word by word**, in both languages, base OJ text against consolidated text, with footnote markers and paragraph-numbering artefacts normalised away. **Exactly three substantive differences exist in the whole enacting text, and two of them are in this module's scope:**

| # | Provision | Base OJ text | Corrected text | Languages | Material here? |
|---|---|---|---|---|---|
| 1 | **Art. 64(10)** (derogation from the fines) | "By way of derogation from paragraphs **3 to 9**" / "Abweichend von den Absätzen **3 bis 9**" | "paragraphs **2 to 9**" / "Absätzen **2 bis 9**" | EN **and** DE | **Yes — see §4.4** |
| 2 | **Art. 13(8) DE** (vulnerability handling / support period) | "…in den Verkehr bringen und während **der erwarteten Produktlebensdauer und** des Unterstützungszeitraums…" | "…in den Verkehr bringen und während des Unterstützungszeitraums…" | **DE only** | **Yes — see §4.5** |
| 3 | Art. 67 (amendment to Directive (EU) 2020/1828) | point "69." | point "72." | EN only (DE already read 72) | No |

Everything else the diff surfaced was formatting: footnote renumbering, the signature block and ELI footer that consolidations drop, and paragraph numbers moved onto their own lines.

**All 20 questions in this pilot are written on the CORRECTED text**, and the two material corrections are flagged inside the affected questions' own explanations so a learner reading an uncorrected PDF is not left confused.

*(Caveat for the reviewer: a corrigendum published very recently could lag consolidation. Re-run this probe before any production release — see §8.6.)*

### 0.2 Level 2 status — what exists and what does not, checked rather than assumed

| Empowerment | Status as at 2026-08-16 | Consequence for this module |
|---|---|---|
| **Art. 13(24)** — Commission **may** specify by implementing act "the format and elements of the software bill of materials" | **Not exercised.** No such implementing act was found. The empowerment is discretionary ("may"), so its non-exercise is the default state, not a delay. | The SBOM format question (`cra-sbom_vulnerability-01`) is answerable from Annex I Part II point (1) and Art. 13(24) alone, and its answer does not depend on the negative finding. |
| **Art. 14(9)** — Commission **shall**, by 11 December 2025, adopt a delegated act on grounds for delaying dissemination | **Adopted, on the deadline.** Commission Delegated Regulation **(EU) 2026/881** of **11 December 2025**, OJ L, 2026/881, 20.4.2026. Read in full, EN + DE. | Read and available; **no answer key or distractor in this pilot depends on it** (see §5 gap 7). |
| **Art. 7(4)** — implementing act by 11 December 2025 specifying technical descriptions of Annex III/IV categories | Not verified either way. | Nothing in this pilot turns on Annex III/IV classification. Logged as gap 3. |
| **Art. 8(1)** — delegated acts on mandatory certification for critical products | Not verified either way. | Nothing in this pilot turns on it. Gap 3. |
| **Art. 2(5)**, **Art. 13(8) 5th subpara**, **Art. 25** — further delegated-act powers | Not verified either way; all discretionary. | Referenced in explanations only as powers, never as adopted law. |

**Discipline applied:** where I did not verify a Level 2 instrument's existence to the same standard as the CRA itself, no question's correctness depends on whether it exists. The only negative finding I assert is the SBOM implementing act, and I assert it as "not found as at 2026-08-16", inside an explanation, never as an answer key.

### 0.3 Non-legal technical standards — consulted, and quarantined

The brief asked for precision on where EU law ends and industry practice begins. The following were checked by web research (they are not EU legal instruments, so Cellar does not apply) and are used **only in explanations, as clearly-labelled factual context**. **No answer key and no distractor's wrongness depends on any of them:**

- **CycloneDX** — an OWASP project, standardised by **Ecma International as ECMA-424**, developed by Ecma TC54 (Software & System Transparency) jointly with OWASP. It is *not* an ISO standard.
- **SPDX** — a Linux Foundation project. **SPDX 2.2.1 is standardised as ISO/IEC 5962:2021** (published August 2021). **SPDX 3.0 was released in April 2024** and is *not itself* the ISO-standardised version. Note the trap this creates: "SPDX is an ISO standard" is true of 2.2.1 and misleading about 3.0.
- **VEX (Vulnerability Exploitability eXchange)** — **a concept, not a format.** It originated in the NTIA multistakeholder process. No single body maintains "the VEX specification". It is *implemented* by at least four formats: CSAF, CycloneDX, SPDX and OpenVEX. Anyone who says "send us a VEX file" is naming a category, not a schema.
- **CSAF (Common Security Advisory Framework)** — a formal specification maintained by **OASIS**; **CSAF 2.0** (November 2022) contains a dedicated **VEX profile** alongside other profiles. CSAF is one implementation of the VEX concept.
- **VDR (Vulnerability Disclosure Report)** — a practice, not a specification.
- **IEC 62443-4-1** — named in the roadmap; **not read, not cited, and not tested here** (see gap 10).

**The CRA names none of these.** Not CycloneDX, not SPDX, not VEX, not CSAF, not IEC 62443. The only textual hooks are Annex I Part II point (1) ("a commonly used and machine-readable format"), Art. 13(6) ("where appropriate in a machine-readable format") and Art. 14(8) ("where appropriate in a structured, machine-readable format that is easily automatically processable"). This is stated in `cra-sbom_vulnerability-01` and `cra-reporting-05` and is the module's single most commercially valuable correction.

### 0.4 Secondary / practical guidance — consulted and quarantined

- **European Commission, "Cyber Resilience Act — Reporting obligations"** (`digital-strategy.ec.europa.eu/en/policies/cra-reporting`). States: "As of 11 September 2026, manufacturers are required to report actively exploited vulnerabilities and severe incidents impacting the security of products with digital elements"; describes the 24h / 72h / 14-day (vulnerability) / one-month (incident) cascade; states manufacturers submit "only once through the CRA Single Reporting Platform (SRP)" to the CSIRT of their main establishment; and states the SRP "will be operational by 11 September 2026".
- **ENISA, Single Reporting Platform FAQ** (`enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions`). States the platform "is scheduled to be operational by 11 September 2026"; that manufacturers and authorised representatives of open-source stewards register via an **EU Login** account with authorisation validated by the designated CSIRT coordinator; describes automatic routing to the CSIRT coordinator and ENISA simultaneously.

**Both are consistent with the primary text on every point I checked, which is itself worth recording** — unlike the DORA "4-hour rule" secondary literature, the official CRA guidance here is accurate. Neither is a binding instrument, so under the rule in §2 neither can carry a High-confidence answer key, and **no question in this pilot is written on them**. Registration mechanics (EU Login, authorisation validation) are logged as gap 8 — operationally the first thing a DevSecOps lead will ask, and correctly excluded from the statutory question pool.

Vendor and consultancy commentary on CRA SBOM obligations was scanned and **is not cited anywhere**. As §4.2 shows, the claim that most of it repeats is precisely what this module is built to correct.

---

## 1. Why this module, and what its spine is

Three design decisions came out of the primary-source read.

1. **The spine is the SBOM-format non-requirement.** The most valuable single fact this module teaches is that the CRA does *not* mandate CycloneDX, SPDX or any other named format — it mandates three properties ("commonly used", "machine-readable", "at the very least the top-level dependencies") and reserves a discretionary power to specify more later. Every engineering team currently being sold a format by a tool vendor is being sold a convention as if it were law. `cra-sbom_vulnerability-01` is the anchor question and `cra-sbom_vulnerability-02` is its commercial twin (there is no duty to publish the SBOM at all).

2. **Article 14 is taught as two tracks that diverge at the third stage.** The vulnerability track and the severe-incident track are symmetric for 24 hours and 72 hours and then split: 14 days after a corrective or mitigating measure is *available* versus one month after *submission* of the incident notification. That is a genuine trap, it is the CRA's structural difference from the DORA cascade, and `cra-reporting-02` exists solely to test it.

3. **The transitional rule is taught as a trap, not as relief.** Art. 69(2) grandfathers the installed base; Art. 69(3) pulls Art. 14 straight back out of the grandfathering. A vendor who reads only Art. 69(2) will conclude — reasonably, and wrongly — that a 2025 product is simply out of scope. `cra-scope_dates-04` punishes exactly that reading.

Four questions are operational-trap scenarios where a competent engineering organisation does the technically sensible thing and misses a statutory duty: `cra-manufacturer_duties-02` (patch your own product and say nothing upstream), `cra-sbom_vulnerability-03` (bundle security fixes into the quarterly release, gate patches behind a support contract), `cra-sbom_vulnerability-04` (never publish fixed-vulnerability details), `cra-reporting-03` (treat a non-executed supply-chain implant as "no incident").

---

## 2. Citation ledger (primary-source verified 2026-08-16)

**Confidence rule used here** — identical to the four DORA sibling dossiers, restated so the reviewer can hold me to it:

- **"High — verbatim"** = the tested proposition is a direct restatement of wording I read in the OJ text of the cited provision, in **both** EN and DE.
- **"High — verbatim + synthesis"** = every element is verbatim, but the question combines **two or more** provisions I read separately; the reviewer should check that the *combination* is a fair statement, not the underlying text.
- **What disqualifies a claim from "High":** any of (a) the proposition rests wholly or partly on a source that is not the OJ text of a binding instrument — including Commission FAQs, ENISA guidance, national-authority notices, standards bodies and vendor summaries; (b) the proposition requires an inferential step beyond the words on the page; (c) the proposition was verified in only one language version where both exist; (d) the proposition rests on a **recital** rather than the enacting terms; (e) the proposition depends on the **absence** of an instrument I could not exhaustively enumerate. Anything hitting (a)–(e) is dropped or explicitly de-rated.
- **No question in this pilot carries a Medium or lower rating.** Questions that could not be grounded verbatim were dropped rather than written down-rated; they are logged in §6.
- **Mechanical verification performed:** every quoted string of six or more words appearing inside a question, an option or an explanation — **110 fragments, EN and DE combined** — was re-matched programmatically against the retrieved OJ / consolidated plain text after whitespace, quote-style and case normalisation. **110/110 matched exactly; 0 failures.** Six German quotations were corrected during this pass, which is why the check is worth running rather than trusting the drafting (see §4.7).

| # | Question ID | Citation (CRA = Regulation (EU) 2024/2847) | What's tested | Confidence |
|---|---|---|---|---|
| 1 | `cra-scope_dates-01` | Art. 2(1) + Art. 3(1) | Scope reaches **indirect** logical or physical connections; hardware, firmware and separately-placed components all count | High — verbatim (EN + DE) |
| 2 | `cra-scope_dates-02` | Art. 3(13) | Manufacturer = whoever markets under its name/trademark, incl. commissioned development and **free-of-charge** supply | High — verbatim (EN + DE) |
| 3 | `cra-scope_dates-03` | Art. 71(2) | **Three** application dates: 11 Dec 2027 general, Art. 14 from 11 Sept 2026, Chapter IV from 11 June 2026 | High — verbatim (EN + DE) |
| 4 | `cra-scope_dates-04` | Art. 69(2) + Art. 69(3) | Legacy products grandfathered from everything **except** Art. 14 reporting | High — verbatim (an in-text derogation, quoted in both languages) |
| 5 | `cra-scope_dates-05` | Art. 3(40), (41), (42) | The three-step vulnerability ladder; only "reliable evidence that a malicious actor has exploited it in a system without permission of the system owner" triggers Art. 14 | High — verbatim |
| 6 | `cra-manufacturer_duties-01` | Art. 13(5) | Due diligence on third-party components, **expressly including non-commercial FOSS** | High — verbatim |
| 7 | `cra-manufacturer_duties-02` | Art. 13(6) (+ Art. 3(42), Art. 14(1) in the explanation) | Upstream report + remediate + share the fix; and that this is **not** an Art. 14 CSIRT notification | High — verbatim + synthesis (two provisions; the contrast is the point) |
| 8 | `cra-manufacturer_duties-03` | Art. 13(8) subparas 1 and 3 + Art. 13(9) | Support period ≥ 5 years or expected use time if shorter; update availability ≥ 10 years or remainder of support period | High — verbatim. **DE limb depends on corrigendum OJ L, 2025/90555 — see §4.5** |
| 9 | `cra-manufacturer_duties-04` | Art. 13(2), (3), (4) + Annex VII | Risk assessment documented, updated during the support period, in the technical documentation; **clear justification required** where a requirement is disapplied | High — verbatim + synthesis |
| 10 | `cra-manufacturer_duties-05` | Art. 64(2) + Art. 64(10)(a), (b) | EUR 15 m / 2,5 % tier for Annex I + Arts. 13/14; narrow micro/small carve-out for the 24-hour early warning only | High — verbatim, **but the carve-out's operability depends on corrigendum — Tier B, see §4.4** |
| 11 | `cra-sbom_vulnerability-01` | **Annex I Part II point (1)** + Art. 13(24) + Art. 3(39) | **The anchor fact**: no format is named; "commonly used and machine-readable"; "at the very least the top-level dependencies"; Commission **may** specify later | High — verbatim (EN + DE, quoted in both) |
| 12 | `cra-sbom_vulnerability-02` | Annex II point 9 + Annex VII points 2(b) and 8 + Art. 13(25) (recital 77 in the explanation only, labelled) | No duty to publish the SBOM; technical documentation + reasoned MSA request are the only routes | High — verbatim + synthesis (three locations of one instrument; recital used only for corroboration and labelled as such) |
| 13 | `cra-sbom_vulnerability-03` | Annex I Part II points (2), (7), (8) | Remediate without delay; security updates separate from functionality updates where technically feasible; free of charge save the tailor-made/business-user carve-out | High — verbatim |
| 14 | `cra-sbom_vulnerability-04` | Annex I Part II point (4) | Public disclosure of **fixed** vulnerabilities is mandatory, triggered by update availability; the delay is a justified exception with a defined end point | High — verbatim |
| 15 | `cra-sbom_vulnerability-05` | Annex I Part II points (5), (6) + Art. 13(17) | CVD policy put in place **and enforced**; contact address; single point of contact must not be limited to automated tools | High — verbatim + synthesis |
| 16 | `cra-reporting-01` | Art. 14(1), (2)(a), (b), (7) + Art. 16(1) | 24h early warning and 72h vulnerability notification **both from becoming aware**; simultaneously to CSIRT coordinator **and** ENISA via the single reporting platform | High — verbatim (EN + DE, quoted in both) |
| 17 | `cra-reporting-02` | Art. 14(2)(c) vs Art. 14(4)(c) | **The two divergent final-report clocks** | High — verbatim (both provisions quoted in full in both languages) |
| 18 | `cra-reporting-03` | Art. 14(3), (5) + Art. 3(43), (44) | Only **severe** incidents; the two alternative severity limbs; the reach of "is capable of" | High — verbatim + synthesis |
| 19 | `cra-reporting-04` | Art. 14(7) subparas 1–4 | Main establishment = where **product-cybersecurity decisions are predominantly taken**; employee-count fallback; the four-limb cascade for non-EU manufacturers | High — verbatim |
| 20 | `cra-reporting-05` | Art. 14(6) + Art. 14(8) | Intermediate report **only on CSIRT request**; independent duty to inform impacted users, with CSIRT substitution if you fail | High — verbatim |

**Tier A — verbatim, single-instrument location, lowest review burden (14):** 1, 2, 3, 4, 5, 6, 8, 11, 13, 14, 16, 17, 19, 20.
**Tier B — verbatim but combining provisions, or depending on a corrigendum, so the reviewer should check the combination rather than the text (6):** 7, 9, 10, 12, 15, 18.
**Tier C — any claim resting on a secondary source: none.** No question's correct answer, and no distractor's wrongness, depends on a Commission FAQ, ENISA guidance, a standards body, a national-authority notice or a vendor summary. Every factual statement about CycloneDX, SPDX, VEX and CSAF sits inside an explanation, is labelled as industry context, and is arranged so that a reader who ignored it entirely would still answer correctly.

---

## 3. Deliberate non-assertions — what the distractors are built to punish

Recorded explicitly so no scale-up quietly reintroduces them.

1. **"The CRA mandates CycloneDX."** Question 11 distractor (a). It does not. It requires "a commonly used and machine-readable format". ECMA-424 is a real standardisation of CycloneDX and legally irrelevant to this requirement.
2. **"The CRA mandates SPDX because SPDX is an ISO standard."** Question 11 distractor (b). ISO/IEC 5962:2021 is real, applies to SPDX 2.2.1, and is equally irrelevant: the CRA cites no standard for the SBOM.
3. **"Whichever format you pick, you must supply the full transitive dependency tree."** Question 11 distractor (c). Annex I Part II point (1) says "at the very least the **top-level** dependencies". Deeper is good practice; the floor is top-level.
4. **"The CRA obliges you to publish or ship your SBOM."** Question 12 distractors (a), (b). It obliges you to have one in the technical documentation and to produce it to a market surveillance authority on a reasoned request. Annex II point 9 is conditional in terms. Recital 77 says so outright, and is not relied on.
5. **"You must upload the SBOM with each vulnerability notification."** Question 12 distractor (d). Nothing in Art. 14 or Art. 16 requires it.
6. **"Reporting goes to the market surveillance authority."** Question 16 distractor (b). It goes to the CSIRT designated as coordinator **and ENISA simultaneously**, via the single reporting platform. Art. 16(3) runs information the other way: CSIRTs feed the market surveillance authorities.
7. **"The 72-hour clock starts when you file the early warning."** Question 16 distractor (c) — the most dangerous single error in this module, because it is what a DORA-trained reader will assume by analogy. Both Art. 14 clocks start at **becoming aware**.
8. **"The final report is always due one month after you become aware"** / **"14 days after the 72-hour notification"** / **"one month after the early warning."** Question 17 distractors (a), (c), (d). All three are plausible recombinations; none is the rule.
9. **"Every security incident affecting the product is notifiable."** Question 18 distractor (a). Only **severe** ones, per the two limbs of Art. 14(5). Near misses are voluntary only (Art. 15(2)).
10. **"Notifiability depends on confirmed personal-data loss"** or **"on a user-count threshold."** Question 18 distractors (b), (d). Neither concept exists in Art. 14.
11. **"Merely knowing about a vulnerability triggers a 24-hour CSIRT notification."** Question 7 distractor (d). Art. 14 needs *active exploitation* (Art. 3(42)) or a *severe incident*. A known-but-not-exploited vulnerability triggers Art. 13(6) upstream reporting and Annex I Part II handling.
12. **"Fix it in your own product and you are done."** Question 7 distractor (a). Art. 13(6) creates an outward-facing duty to the component's maintainer, including sharing the fix.
13. **"Open source is somebody else's problem"** and **"unpaid open source is out of scope."** Question 6 distractors (a), (c). Art. 13(5) names non-commercial FOSS explicitly, as the integrator's problem.
14. **"You can bundle security fixes into the next feature release"** and **"you can charge for security patches."** Question 13 distractors (a), (c). Annex I Part II points (2) and (8) say the opposite, subject only to the tailor-made/business-user carve-out.
15. **"You should never publish details of fixed vulnerabilities"** and **"you must publish immediately on discovery."** Question 14 distractors (a), (b). The trigger is availability of the update; the delay is a justified exception ending when users can patch.
16. **"A bug bounty is required"** / **"security.txt is required"** / **"an automated web form is enough."** Question 15 distractors (a), (b), (c). Bug bounties appear only in recital 76 as permissive; security.txt is nowhere in the Regulation; Art. 13(17) forbids limiting the single point of contact to automated tools.
17. **"An intermediate report is due every 72 hours."** Question 20 distractor (a). Art. 14(6) makes it a supervisory request, not a standing duty — the opposite of DORA.
18. **"User communication is a commercial decision"** and **"tell users only after the final report."** Question 20 distractors (b), (c). Art. 14(8) is a duty with a CSIRT substitution mechanism attached.
19. **"Products placed on the market before 11 December 2027 are simply out of scope."** Question 4 distractor (a). Art. 69(3).
20. **"Which CSIRT you report to follows corporate registration or tax residence."** Question 19 distractors (a), (d). Art. 14(7): where product-cybersecurity decisions are predominantly taken.
21. **"CRA fines mirror the GDPR at 4 % / EUR 20 m"** and **"the CRA sets no EU-level ceiling."** Question 10 distractors (c), (d). Art. 64(2)–(4) sets three tiers: 15 m / 2,5 %, 10 m / 2 %, and 5 m / 1 %.

---

## 4. Findings where existing research / prior content is imprecise against the primary text

The task asked me to check the briefing rather than confirm it. **Seven findings, four of them material.**

### 4.1 The roadmap's two CRA dates: one is exactly right, one is right but incomplete, and a third date is missing

The roadmap (`claude/dora-cra-b2b-training-roadmap-2026-08-16.md`) states: *"Key CRA dates cited: 11 Sept 2026 (active-exploit reporting duty), 11 Dec 2027 (full CRA/SBOM duty)."* Measured against **Art. 71(2)**, verbatim in both languages:

> **EN:** *"This Regulation shall apply from 11 December 2027. However, Article 14 shall apply from 11 September 2026 and Chapter IV (Articles 35 to 51) shall apply from 11 June 2026."*
>
> **DE:** *"Diese Verordnung gilt ab dem 11. Dezember 2027. Artikel 14 gilt jedoch ab dem 11. September 2026, und Kapitel IV (Artikel 35 bis 51) gilt ab dem 11. Juni 2026."*

| Roadmap claim | Verdict |
|---|---|
| **11 December 2027 = full CRA/SBOM duty** | **Correct.** Art. 71(2) first sentence. The SBOM duty sits in Annex I Part II point (1), which becomes applicable on that date. |
| **11 September 2026 = "active-exploit reporting duty"** | **Correct on the date, incomplete on the scope.** Art. 14 applies from that date — and **Art. 14 covers two duties, not one**: actively exploited vulnerabilities (Art. 14(1)–(2)) *and* severe incidents having an impact on the security of the product (Art. 14(3)–(5)). Calling it the "active-exploit reporting duty" drops half the obligation. Art. 14(8) (informing users) also starts that day. |
| **A third date** | **Missing.** **Chapter IV (Articles 35 to 51) applies from 11 June 2026** — notification of conformity assessment bodies. Low relevance to a DevSecOps audience but it belongs in any date table a CTO is shown, because it is already in the past and it explains why notified bodies are being designated now. |

**Recommended roadmap wording, replacing the current parenthetical:** *"Key CRA dates: 11 June 2026 (Chapter IV — notification of conformity assessment bodies); 11 September 2026 (Art. 14 — reporting of actively exploited vulnerabilities **and** of severe incidents affecting product security, plus the duty to inform users); 11 December 2027 (full application, including Annex I essential requirements, SBOM, CE marking and technical documentation)."*

**And a fourth, unstated date that matters more than the third:** by **Art. 69(3)**, the Art. 14 duties reach **the whole installed base placed on the market before 11 December 2027**, notwithstanding the Art. 69(2) grandfathering. For an established vendor that is the single most expensive sentence in the Regulation, and the roadmap does not mention it at all.

### 4.2 The roadmap's module framing lists SBOM formats as if they were the subject matter — and one of the listed items is not a format

The roadmap describes module 2A as: *"Secure Supply Chain Coding (DevSecOps/CTOs; CRA Art. 14, CycloneDX vs SPDX, VEX, generate→attest→store→verify pipeline)."* Three corrections:

1. **"CycloneDX vs SPDX" is not a CRA question.** The CRA names neither. Teaching a format comparison as CRA content is exactly the blur this session's other dossiers have repeatedly corrected. The defensible framing is: *the CRA specifies properties, not a format; here are the two formats that satisfy those properties in practice, and here is why your architecture should treat the format as a swappable output stage.*
2. **VEX is a concept, not a format.** It is implemented by CSAF, CycloneDX, SPDX and OpenVEX. A module that presents "VEX" alongside "CycloneDX" and "SPDX" as three peer formats is teaching a category error. The roadmap's own sample MCQ ("correctly builds a VEX file for a non-exploitable CVE") inherits the error — there is no such thing as "a VEX file" without naming the implementing format.
3. **"CRA Art. 14" understates the module's centre of gravity.** Art. 14 is the reporting cascade. The supply-chain substance — due diligence on third-party and open-source components, upstream vulnerability reporting, the SBOM, coordinated vulnerability disclosure, secure update distribution — lives in **Art. 13 and Annex I Part II**, which the roadmap does not name. Ten of this pilot's twenty questions are unanswerable from Art. 14 alone.

**Recommended module description:** *"CRA — Secure Supply Chain & Vulnerability Handling (DevSecOps/CTOs; Art. 13 manufacturer due diligence incl. open-source components, Annex I Part II vulnerability handling and the SBOM requirement, Art. 14 reporting to the CSIRT coordinator and ENISA, and the application-date/legacy-product transitional rules). Formats (CycloneDX, SPDX) and advisory schemas (CSAF, and VEX as a concept implemented by several formats) are taught as industry practice, explicitly distinguished from CRA legal requirements."*

### 4.3 The DORA-trained reader's three false analogies — the reason this module cannot be adapted from module 5

Anyone who built or took the `dora_incident` module will carry three assumptions into the CRA and all three are wrong:

| DORA (Art. 19 + Delegated Regulation (EU) 2025/301) | CRA (Art. 14) |
|---|---|
| Initial notification: **4 hours from classification as major AND no later than 24 hours from awareness**, whichever expires first | Early warning: **24 hours from becoming aware**. There is **no classification step and no second clock**. |
| Intermediate report: **72 hours from submission of the initial notification**, mandatory, even if nothing changed | 72-hour notification runs **from becoming aware**, not from the early warning. And the thing the CRA calls an *intermediate report* (Art. 14(6)) is **not mandatory at all** — the CSIRT requests it "where necessary". |
| Final report: **one month after the (latest updated) intermediate report** | **Two different final-report clocks**: 14 days after a corrective or mitigating measure is *available* (vulnerability track) or one month after *submission of the 72-hour incident notification* (incident track). |

The recipient differs too: DORA reports go to the competent authority under Art. 46 DORA; CRA notifications go **simultaneously to the CSIRT designated as coordinator and to ENISA**, via ENISA's single reporting platform, with the CSIRTs then feeding the market surveillance authorities (Art. 16(3)). **Do not let any scale-up reuse DORA question stems here.**

### 4.4 Art. 64(10) was broken as published, and the fix changes who can be fined

As published in the OJ, **Art. 64(10)** read *"By way of derogation from paragraphs **3 to 9**, the administrative fines referred to in those paragraphs shall not apply to … (a) manufacturers that qualify as microenterprises or small enterprises with regard to any failure to meet the deadline referred to in Article 14(2), point (a), or Article 14(4), point (a); (b) any infringement of this Regulation by open-source software stewards."*

But the fines for breaching **Article 14** are in **paragraph 2**, not in paragraphs 3 to 9. On the uncorrected text, the carve-out named an Art. 14 deadline and then derogated from a range of paragraphs that does not contain the Art. 14 fine — i.e. it was **inoperative for the very case it describes**. The corrigendum changed the range to **"paragraphs 2 to 9"** in both EN and DE, which makes the carve-out work.

Two consequences: (i) **question 10 is written on the corrected text and says so in its own explanation**, and is rated Tier B for that reason; (ii) any CRA training or marketing material drafted from a PDF downloaded before mid-2025 will contain the broken version. Worth a spot-check of any third-party CRA content the business licenses.

**Note also how narrow the relief is even when it works:** it covers *only* the 24-hour early-warning deadline in Art. 14(2)(a) / 14(4)(a). Not the 72-hour notification, not the final report, and not the substance of any duty. A micro-enterprise that never reports at all is not covered.

### 4.5 The German OJ text of Art. 13(8) said something the English never did — and it has been corrected

Base German OJ text of Art. 13(8): *"Wenn sie ein Produkt mit digitalen Elementen in den Verkehr bringen und während **der erwarteten Produktlebensdauer und** des Unterstützungszeitraums stellen die Hersteller sicher, dass Schwachstellen dieses Produkts … behandelt werden."*

English, unchanged throughout: *"Manufacturers shall ensure, when placing a product with digital elements on the market, **and for the support period**, that vulnerabilities of that product … are handled effectively …"*

The German version therefore created a **second, potentially longer obligation window** ("expected product lifetime") that the English text never contained — a materially different scope for the core vulnerability-handling duty. Corrigendum **OJ L, 2025/90555 of 2.7.2025** deleted the phrase, aligning DE with EN.

This is the finding with the widest reach beyond this module: **any German-language CRA training material produced from the original OJ text teaches a wrong scope for Art. 13(8)**, and Art. 13(8) is the provision the whole support-period concept hangs from. Question 8's German explanation states the correction explicitly. Recommend a spot-check of any German CRA content already in the business's pipeline.

### 4.6 Two residual drafting defects in the CRA, noted for the reviewer, not tested

1. **Art. 16(2), second subparagraph** refers to *"the level of sensitivity of the notified information as indicated by the manufacturer under **Article 14(2), point (a)**"*. But Art. 14(2)(a) — the early warning — contains no sensitivity indication; the sensitivity indication is in Art. 14(2)**(b)**, and Art. 16(2) third subparagraph correctly refers to point (b) two sentences later. The cross-reference in the second subparagraph is wrong on its face in **both** language versions, and survives all three corrigenda. Directly parallel to the Annex I/Annex II cross-reference defect the `dora_incident` dossier found in Implementing Regulation (EU) 2025/302. **No question depends on it.**
2. **Annex VII points 2(b) and 8** both cover the software bill of materials: point 2(b) requires it as part of the vulnerability-handling process description in the technical documentation, while point 8 lists it separately as due *"where applicable, … further to a reasoned request from a market surveillance authority"*. The two are redundant at best and in tension at worst on whether the SBOM must sit in the file at all times or only be producible on request. **Question 12 is written on the safe reading** (it is in the technical documentation *and* producible on reasoned request) and asserts nothing about the tension.

### 4.7 German terminology inconsistencies inside the CRA itself, and what they cost

Three, all found during the verbatim-matching pass and all reflected in the drafted German:

1. **Art. 13(17) DE calls the single point of contact the "zentrale *Anlaufstelle*"; Annex II point 2 DE calls it the "zentrale *Kontaktstelle*."** The English says "single point of contact" in both places. Question 15's German explanation carries a short note so a learner comparing the two annexes does not conclude they are different institutions.
2. **Art. 14(6) DE contains a grammatical error in the OJ text:** *"das als Koordinator benannte CSIRT, **dass** ursprünglich die Meldung erhält"* — a relative pronoun spelled as a conjunction. Not corrected by any of the three corrigenda. Question 20's German explanation quotes only the clean part of the sentence verbatim and footnotes the defect rather than reproducing it in learner-facing prose.
3. **Art. 3(1) DE uses "Zweckbestimmung" for "intended purpose", but Art. 2(1) DE uses "bestimmungsgemäßer Zweck"** for the same English phrase. My first German draft used the Art. 3 term inside an Art. 2 quotation; the mechanical verbatim check caught it. Corrected.

Two of the six German corrections the verbatim pass forced were of this kind (a plausible synonym that is not the OJ's word); two were declension errors; one was a phrase order difference; one was the Art. 14(6) typo. **This is the argument for keeping the mechanical check in the pipeline for every locale, not just for German**, and it is why the FR/ES/IT/PL/RO expansion in §8.5 must be sourced from the respective OJ language versions rather than translated.

---

## 5. Gap list — covered by the primary sources but deliberately **not** tested by this 20-question pilot

1. **Annex I Part I in full (the thirteen product-property requirements (a)–(m)).** Read; only points (2)(a) and (2)(c) are touched, inside explanations. Secure-by-default, data minimisation, attack-surface limitation, exploitation-mitigation techniques, logging with an opt-out and secure data erasure each deserve a question. This is the largest single block of untested primary material and the obvious spine of a 40-question scale-up.
2. **The conformity-assessment machinery: Art. 27 (harmonised standards, common specifications, certification schemes), Art. 28 (EU declaration of conformity), Art. 30 (CE marking), Art. 31 (technical documentation), Art. 32 and Annex VIII (the four assessment modules).** Read in outline; untested. A CTO needs this, but it is a different module (the CRA analogue of `dora_procurement`), not a supply-chain one.
3. **Art. 7 and Annex III (important products, classes I and II); Art. 8 and Annex IV (critical products).** Read; deliberately untested, because a correct answer would need the Art. 7(4) implementing act specifying the technical descriptions of those categories, and I did not verify that act's existence to this dossier's standard. See §0.2. This is a genuine gap for a hardware/security-product audience.
4. **Art. 24 (obligations of open-source software stewards) and Art. 25 (voluntary security attestation of FOSS).** Read in full; referenced only in question 6's explanation. Art. 24(3)'s split application of Art. 14(1) versus Art. 14(3) and (8) to stewards is subtle and genuinely important to the open-source-heavy audience this module targets — a strong scale-up candidate, but it needs its own question rather than a clause.
5. **Arts. 18–23 (authorised representatives, importers, distributors; when a distributor or importer is deemed a manufacturer under Art. 22).** Read. Untested because this pilot is written for the manufacturer's engineering organisation. Art. 22 in particular (re-branding or substantially modifying someone else's product makes you the manufacturer) is a trap worth its own question in a channel/reseller-facing variant.
6. **Art. 15 (voluntary reporting) and Art. 17(4) ("[t]he mere act of notification … shall not subject the notifying natural or legal person to increased liability").** Read; both appear only inside explanations. Art. 17(4) is a genuinely reassuring fact for engineers who fear that reporting creates exposure, and would make a good stand-alone question.
7. **Commission Delegated Regulation (EU) 2026/881 in full** — the four grounds for delaying dissemination (sensitivity of the information, a 72-hour expected-mitigation window, exploit-technique risk, an ongoing coordinated vulnerability disclosure), the CSIRT-specific grounds in Art. 4, and the platform-compromise ground in Art. 5. Read in full and **deliberately untested**: it governs what the CSIRT does after you report, not what you must do, and its Art. 3(a) "72 hours" is a trap that would confuse a learner still consolidating the Art. 14 deadlines. Excellent material for an advanced annex.
8. **The practical registration and submission mechanics of the single reporting platform** (EU Login accounts, authorisation validation by the CSIRT coordinator, routing behaviour). Sourced only from the Commission and ENISA pages in §0.4, therefore Tier C under §2, therefore not tested. Recommend a **separately-labelled, separately-reviewed "practical operations" annex** with its own re-verification cadence, exactly as the `dora_register` and `dora_incident` dossiers recommended for their submission mechanics. This is the first thing a DevSecOps lead will ask and the last thing that should sit in a statutory question pool.
9. **Art. 52–63 (market surveillance, Union safeguard procedure, ADCO, compliant products presenting a significant cybersecurity risk, Art. 54(2) non-technical risk factors).** Read in outline; untested. Enforcement architecture, not engineering practice.
10. **IEC 62443-4-1, and the whole harmonised-standards landscape.** Named in the roadmap; **not read and not cited**. Once harmonised standards for the CRA are cited in the OJ under Art. 27, presumption of conformity becomes a first-class topic and this gap becomes urgent. Until then, anything said about it would be commentary.
11. **The CRA/NIS2 and CRA/AI-Act interfaces** (Art. 12 for high-risk AI systems; the pervasive cross-references to Directive (EU) 2022/2555 for CSIRTs, coordinated vulnerability disclosure, the European vulnerability database and the Cooperation Group). Read; untested. High-interest, high-oversimplification-risk; same reasoning as the sibling dossiers.
12. **National implementation.** Nothing national is asserted anywhere in this pilot. No Polish, Romanian or German authority is named. Given the roadmap's EN/PL/RO target, a national layer will eventually be wanted and will need its own sourcing.
13. **Art. 13(10) and (11)** (substantially modified software versions; public software archives) and **Art. 13(23)** (cessation of operations). Read; untested. Art. 13(23) is a good scale-up question because it is counter-intuitive: winding down a product line creates a notification duty to market surveillance authorities *and* to users.

---

## 6. Questions considered and dropped (grounding failures, logged rather than written)

Per the brief's instruction not to write anything that cannot be grounded in verbatim primary text:

- **"Which SBOM format does the CRA require?"** as a *positive* question — dropped in that form and rewritten as question 11, which tests the properties. A question whose correct answer is a format name cannot be grounded; a question whose correct answer is "none is named" can.
- **"By when must the Commission adopt the SBOM implementing act?"** — dropped. Art. 13(24) sets **no deadline** and the power is discretionary ("may"). Contrast Art. 14(9), which does set one ("By 11 December 2025") and was discharged by Delegated Regulation (EU) 2026/881. Asserting any SBOM-act timetable would be invention.
- **"Is a VEX document required to accompany an SBOM?"** — dropped. Neither VEX nor CSAF appears anywhere in the CRA. The nearest true statements are Art. 14(8)'s "where appropriate in a structured, machine-readable format that is easily automatically processable" and Art. 13(6)'s "where appropriate in a machine-readable format", both of which are taught inside explanations without asserting any schema.
- **"How deep must an SBOM go?"** as a standalone question — folded into question 11 rather than written separately, because the only verbatim answer is "at the very least the top-level dependencies" and a whole question on one clause invites over-reading.
- **"Within how long must a vulnerability be patched?"** — dropped. Annex I Part II point (2) says "without delay" and fixes no period. The commonly quoted "90 days" is industry disclosure convention (and not even a uniform one), not CRA law. Question 13 teaches "without delay" and the separate-from-functionality-updates rule instead.
- **"Which products are 'important' or 'critical'?"** — dropped, see gap 3: the answer depends on an implementing act whose existence I did not verify to this dossier's standard.
- **"Does the CRA apply to SaaS?"** — dropped. The text reaches "remote data processing solutions" as part of a product with digital elements (Art. 3(1), (2)) and recital 12 discusses the boundary, but a crisp SaaS answer requires the Art. 26 Commission guidance, which is not adopted-and-verified here. A wrong answer to this question would be commercially damaging, so it is a gap, not a guess.
- **"What is the penalty for a specific national breach?"** — dropped. Art. 64(1) leaves the rules to Member States; only the EU ceilings are asserted (question 10).
- **"Who inside the manufacturer must sign the notification?"** — dropped. The CRA names no function. Art. 13(17)'s single point of contact is user-facing, not a reporting signatory.
- **"Does the 24-hour clock pause outside business hours or over a weekend?"** — dropped. The CRA contains **no** temporal relief of any kind for Art. 14 — no weekend rule, no bank-holiday rule, nothing equivalent to Art. 5(4) of DORA's Delegated Regulation (EU) 2025/301. Saying so requires proving a negative across the whole instrument; a full-text search for "working day", "bank holiday" and "Arbeitstag" found nothing, but the module simply says nothing implying relief rather than asserting its absence.

---

## 7. Module metadata as drafted

- Module id: `cra_supply_chain` · file: `data/cra_supply_chain_pilot_DRAFT.json` (106 KB) · **20 questions** · **EN canonical + DE**
- Generator retained at `data/gen_cra_supply_chain_draft.py` (deterministic, re-runnable; runs its own integrity, schema-parity and orthography checks and exits non-zero on failure). Not referenced by any build path.
- `class: "ALL"` in meta; `class_scope: ["ALL"]` and `roles: ["all"]` on every question
- **Topic codes (4 × 5):** `scope_dates` (Scope, definitions and application dates), `manufacturer_duties` (Manufacturer obligations and support period), `sbom_vulnerability` (SBOM and vulnerability handling), `reporting` (Reporting obligations under Article 14)
- **Points:** 12 × 4 points, 8 × 3 points — matching the `kartellrecht_pilot.json` / DORA-sibling scale
- **`high_stakes: true` on 10 questions** (2, 3, 4, 7, 10, 11, 13, 16, 17, 18) — the ones where a wrong answer produces either a missed statutory deadline, a shipped non-conformity, or a false statement about scope
- **`grundstoff: true` on 4** — one anchor question per topic (1, 6, 11, 16)
- **Answer key distributed exactly 5 × a / 5 × b / 5 × c / 5 × d**; verified programmatically, as is option-set integrity (`{a,b,c,d}` in both locales), the correct-key-exists-in-both-locales check, and ID uniqueness
- **Schema parity verified programmatically** against `data/kartellrecht_pilot.json`: identical question-object key list *and* order (`id, topic, topic_code, class_scope, grundstoff, legal_basis, points, high_stakes, question_type, image_ref, correct, text, explanation, roles`)
- **German orthography verified programmatically.** The emitted file contains **611 real umlaut/eszett characters** (ä 168, ö 87, ü 281, Ä 7, Ö 1, Ü 11, ß 56). A residue scan for 34 ASCII-transliteration patterns (`fuer`, `ueber`, `muessen`, `koennen`, `waere`, `gefuehrt`, `ausschliesslich`, `faellt`, `maessig`, `groesse`, `zustaendig`, `behoerde`, `moeglich`, `spaetest`, `unverzueglich`, `gemaess`, `pruef`, `schaetz`, `vorfaelle`, `jaehrlich`, `massnahm`, `erfuell`, `haerte`, `verstoesse`, `regelmaessig`, `abhaengigkeit`, `geldbusse`, `stueckliste`, `vollstaendig`, `naechste`, `grundsaetzlich`, and others) returns **zero hits**. A second, exhaustive audit tokenised every German-language string and listed every word containing `ae`/`oe`/`ue`/`ss` without a real umlaut; after whitelisting legitimately-ASCII German words (*Abschlussbericht, Auffassung, Hauptniederlassung, Kommission, Prozess, Nutzungsdauer, dass, muss, lassen, sodass, voraussichtlich* and similar) the residue list is **empty**. Additionally: **no English-language field contains an umlaut** (0 occurrences), and `data/kartellrecht_pilot.json`'s punctuation convention is followed exactly — straight quotes only, ASCII hyphens only, no typographic quotes, en dashes or em dashes anywhere in the file, and no control characters.
- **Verbatim citation check:** 110/110 quoted legal fragments of six or more words matched the retrieved OJ text exactly (see §2).
- `meta.legal_disclaimer` carries the user's German boilerplate verbatim; `meta.legal_disclaimer_en` carries an English rendering, since EN is canonical here
- `meta.canonical_locale: "en"` with `meta.canonical_locale_note` recording that this is a deliberate audience decision, not an oversight
- `meta.renewal_months: null`, `renewal_basis: "not_specified_in_statute"` — with a note distinguishing the two genuine recurring duties in this area (ENISA's **24-monthly** technical report under Art. 17(3); the Commission's **four-yearly** evaluation under Art. 70(1)) from a training cadence, which the CRA nowhere fixes. Art. 10 asks Member States to promote re-skilling and up-skilling for manufacturers' employees but sets no frequency.
- `meta.legal_review_status` records the primary-source verification, the CELEX identifiers, the OJ references, **all three corrigenda and the two that are material**, the Delegated Regulation (EU) 2026/881 read, and points back to this dossier
- `meta.pass_rule_note` deliberately proposes no `EXAM_QUESTION_COUNT_BY_TYPE` / `MAX_ERROR_POINTS_BY_TYPE` / `EXAM_TOPIC_DRAW` values

---

## 8. Open items before this could move toward `data/cra_supply_chain_pilot.json`

1. **Human legal review, in this order of value:** first **§4.4** (Art. 64(10) and the corrigendum, on which question 10's carve-out limb depends); then **§4.5** (the German Art. 13(8) correction, on which question 8's German text depends); then Tier B questions 7, 9, 12, 15, 18; then §4.6's two drafting defects.
2. **Product decision on §4.1 and §4.2.** The roadmap's date parenthetical and its module description for 2A should both be replaced with the wording proposed there. In particular, the roadmap's own sample MCQ about "building a VEX file" should be rewritten before it becomes a question — as drafted it teaches a category error (§4.2 point 2).
3. **Decide how the module is marketed.** "CycloneDX vs SPDX" sells to an engineering buyer and it is not what the CRA says. Recommendation identical in shape to the `dora_incident` recommendation about the "4-hour rule": keep the format comparison as the marketing hook, and let the module's actual value proposition be the correction — *the CRA does not mandate a format, and here is exactly what it does mandate.*
4. **Spot-check third-party and German-language CRA material the business may license or reuse**, against §4.4 and §4.5. Content drafted from an uncorrected OJ PDF will carry both defects, and the German Art. 13(8) defect changes a scope statement rather than a footnote.
5. **Locale scope.** EN canonical + DE only. The roadmap targets **EN/PL/RO** for this module, so **Polish and Romanian are the priority additions, ahead of the DE-market languages** — the reverse of the DORA modules' priority. Both must be sourced from the **Polish and Romanian OJ language versions** of Regulation (EU) 2024/2847, not machine-translated. §4.7 is the evidence for why: six German quotations needed correction against the OJ despite being drafted by someone reading the German OJ text alongside. The load-bearing terms to get right in each language are *actively exploited vulnerability*, *severe incident*, *becoming aware*, *support period*, *placing on the market* and *software bill of materials*.
6. **Regulatory currency.** The CRA has already been corrected three times, twice materially for this module. Before any production release, re-run the consolidated-version probe in §0.1 (with the positive control) and re-confirm Art. 13(8), Art. 14 and Art. 64(10). Separately, re-check whether the **Art. 13(24) SBOM implementing act** has been adopted — if it is, question 11's explanation needs updating within days, and the module's core selling point changes shape.
7. **Role vocabulary.** All 20 questions carry `roles: ["all"]`. The app's existing role vocabulary is `all`, `all_staff`, `management`, `hr`, `it`, `finance`. This module's real audience is a product-engineering/DevSecOps role that does not exist in the vocabulary. **Five modules now** (2B, 1A, 4, 5, 2A) have audiences the vocabulary cannot express; worth resolving once as a product decision rather than per module.
8. **Module wiring.** Not done, by design: `build_modules.py`, `modules_manifest.json` and `app.js` untouched, no build run, nothing git-added. The 5/5/5/5 topic split suggests a 4- or 5-question draw touching every topic, but that is a design decision after sign-off.
9. **Decide on the two annexes** (gaps 7 and 8). The Delegated Regulation (EU) 2026/881 material and the ENISA platform mechanics are both genuinely wanted by this audience and both belong outside the statutory pool — the first because it teaches what happens after you report, the second because it is Tier C. Recommendation: one combined, separately-labelled "CRA reporting in practice" annex with an explicit "verify before each cycle" note.

---

**Reminder:** this document and the accompanying JSON are draft training-content groundwork. They are not legal advice, have not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review.
