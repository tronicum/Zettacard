# Sovereign cloud & the DORA exit strategy — practitioner reference add-on (2026-08-16)

**Status:** Optional add-on reference document, **not a module**. The DORA/CRA B2B roadmap (`claude/dora-cra-b2b-training-roadmap-2026-08-16.md`) lists "Sovereign Cloud / exit-strategy documentation for cloud architects" as item **10 of 10** in the TAM-based build priority — *"supplementary only"*, explicitly not a full module. This document is written to that scope: no MCQ pilot, no `data/*.json` file, no module wiring. It is a reference sheet for the people who will later write that supplementary content, and it is directly usable as background for module **3A (Surviving the CISA Audit)**, whose scope already includes "exit-strategy documentation".

**Audience:** cloud architects, infrastructure leads and IT procurement staff at EU financial entities who have to *implement and document* an exit strategy — not lawyers, and not general staff.

**Relationship to the legal work already done.** The legal grounding of DORA's exit-strategy requirement is **already settled** in `docs/dora-procurement-pre-review-dossier-2026-08-16.md` (Module 2B), which verified Art. 30(3)(f) and Art. 28(8) of Regulation (EU) 2022/2554 against the Official Journal text in EN and DE, plus Art. 10 of Commission Delegated Regulation (EU) 2024/1773. **That research is not repeated here and is not re-derived.** Two findings from it are load-bearing for everything below and are cited by reference throughout:

> **(2B-A)** DORA prescribes **no** exit transition-period duration. Art. 30(3)(f) requires an *"adequate"* transition period, measured against service complexity. "At least 24 months" is a distractor in `kritische-funktionen-04`, not a rule. *(2B dossier §3, §2 item 13)*
>
> **(2B-B)** The exit strategy is an **Art. 30(3)-tier obligation only** — contracts for ICT services supporting **critical or important functions**. It is *not* in the Art. 30(2) baseline that applies to every ICT contract. *(2B dossier §4.2)*

**Method.** Everything in §2 and §3 about specific vendors and programmes was verified by live web search and page retrieval on **2026-08-16**. This area moves fast and training-data recall about it is unreliable — see §7 for a worked example of an assumption in the roadmap's own source research that is now out of date. Sources are listed inline and consolidated in §8.

**This is not legal advice.** Same standing caveat as every other dossier in this repo. Nothing here is a compliance opinion about any named vendor, and §6 exists specifically to prevent it being read as one.

---

## 1. What "sovereign cloud" actually means — and what it does not

"Sovereign cloud" is a **marketing term with no single legal definition in force**. As of 2026-08-16 there is no adopted EU instrument that defines it and grants it a certification. That matters for exit-strategy documentation: an auditor cannot be pointed at "we use a sovereign cloud" as a control, because there is no agreed referent for the phrase.

Three separate things get called "sovereign", and they carry materially different guarantees.

### 1.1 The three tiers, and what each actually buys you

| Tier | What it is | What it genuinely guarantees | What it does **not** guarantee |
|---|---|---|---|
| **A — Data residency / boundary** | Contractual + technical commitment that data (and sometimes metadata, logs, telemetry) stays in a named region, with access controls and logging. Microsoft EU Data Boundary, Google Cloud Data Boundary, most "EU region" offerings. | Where bytes sit at rest and, increasingly, where they are processed. Audit logging of administrative access. | **Nothing about jurisdiction.** A US-parented provider remains subject to US extraterritorial process regardless of where the disk is. |
| **B — Operational sovereignty (US parent, EU operations)** | EU-incorporated subsidiaries, EU-resident staff only, EU-resident leadership, separate control plane, sometimes an independent advisory board. **AWS European Sovereign Cloud**; Microsoft's Sovereign Public/Private Cloud tiers. | Who can technically touch the systems; where the operational staff sit; often physical/logical separation from the provider's other regions. Real reduction in the *practical* surface for foreign access. | **Does not sever the parent-company legal chain.** Analysts assessing both AWS's and Microsoft's 2026 offerings reach the same conclusion: sovereignty improvements *reduce* the risk but **"do not eliminate the legal basis"** for lawful-access demands under US law such as the CLOUD Act. |
| **C — Jurisdictional sovereignty (EU/EEA ownership and control)** | Provider whose ultimate controlling entity is established in the EU/EEA and which has no controlling third-country parent. StackIT, IONOS, Deutsche Telekom, plusserver, Scaleway, OVHcloud. Also partner-operated clouds where the *operator* is EU-controlled (Delos Cloud, Bleu, S3NS). | No US parent to be served with extraterritorial process for the operator's own holdings. | **Does not guarantee resilience, portability, scale, or freedom from DORA oversight.** See §4 — two EU-headquartered telcos are on the ESAs' critical-provider list. |

### 1.2 The hard fact that separates marketing from law

The clearest publicly available evidence that Tier A and Tier B do **not** deliver jurisdictional immunity is testimony, not analysis. In **July 2025**, Microsoft France's legal director told a French Senate inquiry, under oath, that he **could not guarantee** that French citizens' data hosted by Microsoft would never be transmitted to US authorities without French consent. Microsoft's own subsequent sovereignty announcements (November 2025) added controls — Data Guardian tamper-evident logging of engineer access, disconnected Azure Local, national partner clouds — but did not and could not change that legal position.

This is the single most useful factual anchor for the whole topic, because it is a provider's own statement rather than a critic's inference. Exit-strategy documentation that assumes a Tier A or Tier B offering removes third-country legal exposure is documenting an aspiration, not a control.

### 1.3 Terminology worth getting right in course copy

- **Data residency** ≠ **data sovereignty** ≠ **operational sovereignty** ≠ **jurisdictional/legal sovereignty**. Use the four terms distinctly; vendor material routinely collapses them.
- **"Sovereign"** is not a certification. **C5**, **ISO 27001**, **SecNumCloud**, **IT-Grundschutz** and the **EU Cloud Code of Conduct** are things a provider can actually hold and evidence. Ask for the certificate scope, not the adjective.
- **C5 Type 1 vs Type 2** matters and is routinely elided. Type 1 attests design of controls at a point in time; Type 2 attests operating effectiveness over a period. Several providers hold Type 1 on a *subset of services*. This is exactly the kind of detail an Art. 28(4)(d) due-diligence file needs.

---

## 2. The regulatory frame around sovereign cloud that is *not* DORA

Cloud architects planning an exit will be affected by three instruments other than DORA. None of these is re-derived legal research — each is flagged with its current status as of 2026-08-16 and should be re-verified before any production use.

### 2.1 EU Data Act (Regulation (EU) 2023/2854), Chapter VI — the switching rules

**This is the most practically important non-DORA instrument for exit planning, and it is already in force.** The Data Act became applicable across the EU on **12 September 2025**. Chapter VI (Arts. 23–31) imposes cloud-switching obligations directly on providers:

- Contractual terms must give a **maximum two-month notice period** for the customer to initiate switching (Art. 25(2)(d)).
- A **transition period of up to 30 days** after termination, extendable to a maximum of **seven months** where technically infeasible within 30 days (Arts. 25(2)(a), 25(4)).
- Contracts must **exhaustively specify** the data and digital assets that are portable (Art. 25(2)(e)).
- Providers must remove pre-commercial, commercial, technical, contractual and organisational **switching obstacles** (Arts. 23–24) and cooperate in good faith (Art. 27).
- **Switching charges (including egress fees) are cost-capped until 12 January 2027 and then prohibited entirely** (Art. 29).

**Why this matters for a DORA exit strategy:** the Data Act gives a *floor* that DORA does not. Where the 2B dossier established that DORA sets no numeric transition period (finding 2B-A), the Data Act does set outer bounds for the switching *mechanics*. These are complementary, not substitutes — the Data Act's seven-month ceiling is a maximum a provider may take, whereas DORA's "adequate" is a minimum the *entity* must be able to justify. A well-drafted exit clause should reference both. Note also that the January 2027 egress-fee prohibition removes what has historically been the largest single quantified cost line in hyperscaler exit modelling; exit cost models built before 2027 need re-baselining.

### 2.2 EUCS — still not adopted

The **European Cybersecurity Certification Scheme for Cloud Services (EUCS)** has been in preparation at ENISA since 2020 and, as of this research date, **has still not been adopted**. It remains blocked on precisely the question this document is about: whether the highest assurance level should carry sovereignty requirements (immunity from non-EU law, EU-only data storage, EU ownership). Analysts have for over a year been recommending the Commission adopt EUCS *without* the sovereignty requirements to break the deadlock.

**Practical consequence:** do not build exit or procurement documentation that depends on an EUCS level. There is nothing to cite. National schemes (**BSI C5** in Germany, **ANSSI SecNumCloud** in France) are what actually exist and are what auditors will accept today.

### 2.3 Cloud and AI Development Act (CADA) — proposed, not law

The Commission published the proposed **Cloud and AI Development Act** on **3 June 2026** as part of its Tech Sovereignty Package. Its centrepiece is a cloud sovereignty framework of **four Union Assurance Levels**, conditioning public-sector procurement on graduated security/resilience/sovereignty criteria. The top level would require that the provider is **not controlled by a third country**, holds European cybersecurity certification at "high" assurance, and retains **effective control over all software components**.

**Status: a proposal at the start of the ordinary legislative procedure.** It is not in force, the assurance-level definitions are expected to be the main battleground, and its direct addressees are public authorities rather than financial entities. It is worth tracking because it is the first EU instrument that would give "sovereign cloud" a legal definition — which would in turn give exit-strategy documentation something concrete to cite. It should **not** appear in training content as a current obligation.

---

## 3. Vendor landscape — verified 2026-08-16

Everything in this section was retrieved live on the research date. Where a claim is a **vendor self-description** rather than an independently verifiable fact, it is marked as such — this distinction is the whole point of the section.

### 3.1 Summary table

| Provider | Ultimate control | Jurisdiction tier (§1.1) | Verified certifications | On ESA CTPP list? (§4) |
|---|---|---|---|---|
| **STACKIT** | Schwarz Group (DE, private) via Schwarz Digits | C | C5, ISO 27001, TÜV SÜD *(vendor-stated)* | No |
| **IONOS** | United Internet AG (DE, listed) | C — but **non-EU data centres exist** | C5 **Type 1** (3 services, Nov 2023), BSI IT-Grundschutz (2022), ISO 27001/20000/9001/50001, PCI DSS & SOC (product-scoped) | No |
| **Open Telekom Cloud / T Cloud Public** | Deutsche Telekom AG (DE, listed; German state is an anchor shareholder) | C | C5 *(vendor-stated, "3× certification density")* | **YES — Deutsche Telekom AG designated** |
| **plusserver** | Private-equity owned (see caveat below) | C (assets), **ownership needs verification** | **BSI C5 Type II**, ISO 27001, ISO 9001, PCI DSS | No |
| **Scaleway** | Iliad Group (FR, private) | C | ISO 27001:2022, HDS; **SecNumCloud in process, not yet qualified** | No |
| **OVHcloud** | OVH Groupe SA (FR, listed) | C | **SecNumCloud qualified** (Hosted Private Cloud, 3 FR sites; Bare Metal Pod) | No |
| **Exoscale** | A1 Digital → A1 Telekom Austria Group → **América Móvil (MX) majority** | **Mixed — see §3.4** | (not independently verified today) | No |
| **AWS European Sovereign Cloud** | Amazon.com, Inc. (US) via new DE parent + 3 GmbH subsidiaries | **B** | SOC 2 Type 1, **C5 Type 1** (69 services), 7 ISO certs — as of 10 Mar 2026 | **YES — AWS EMEA SARL designated** |
| **Microsoft sovereign portfolio** | Microsoft Corp. (US); partner clouds operated by SAP (Delos) / Capgemini+Orange (Bleu) | **B**, partner clouds approach C | EU Data Boundary completed Feb 2025 | **YES — Microsoft Ireland Operations Ltd designated** |
| **Google sovereign portfolio** | Alphabet (US); S3NS is a Thales JV | **B**, S3NS approaches C | S3NS targets SecNumCloud | **YES — Google Cloud EMEA Ltd designated** |

### 3.2 German providers

**STACKIT (Schwarz Digits / Schwarz Group).** The IT division of the Schwarz Group — the retail group behind Lidl and Kaufland — announced as a division in September 2023, HQ Neckarsulm, revenue €1.9bn in FY2024/25. Currently building a very large campus near **Lübbenau, Brandenburg** (13 ha, ~200 MW planned). Cooperation with the BSI on sovereign cloud solutions since March 2025; KPN launched a STACKIT-based sovereign cloud in the Netherlands. Positions itself as "a sovereign European hyperscaler". Lists C5, ISO 27001 and TÜV SÜD.

> **Flag for exit-strategy purposes.** STACKIT's financial-services page describes the company as **"a DORA-compliant ICT service provider."** This phrasing is precisely the misconception §6.1 warns about. There is no such thing as a DORA-compliant provider in the sense that would discharge a financial entity's own obligations; DORA compliance is a property of the *financial entity's* arrangements. A provider can be *contractually capable of supporting* DORA compliance, which is a different and weaker claim. This is a good, real, citable example for a distractor.

**IONOS (United Internet AG).** Montabaur-headquartered, German-listed parent, one of the largest Gaia-X members. Verified certification detail: **C5 Type 1**, awarded 7 November 2023, scoped to **three services only** (Compute Engine, Cloud Cubes, S3 Object Storage) — not the whole platform. Also holds BSI **IT-Grundschutz** certification since September 2022. PCI DSS and SOC attestations are explicitly product-scoped, not platform-wide.

> **Nuance worth documenting:** IONOS operates data centres in **Las Vegas, Newark and Lenexa (US)** alongside its European sites. "German company" and "EU-only footprint" are not the same claim. For a critical-or-important-function workload, the Art. 30(2)(b) location clause has to name the actual regions/countries used, and the answer for IONOS depends on the product.

**Open Telekom Cloud / T Cloud Public (Deutsche Telekom / T-Systems).** Deutsche Telekom has expanded **T Cloud Public** into its flagship sovereign public cloud: 4,000+ enterprise customers, ~80% of core hyperscaler functionality available with a **100% feature-parity target by end of 2026**, and an **Industrial AI Cloud going live 4 February 2026** (claimed to raise Germany's GPU capacity by ~50%). Telekom's own claim is "fully EU compliant data processing in European data centres, strictly protected against access by third countries", with C5 certification and open standards to avoid lock-in.

> **The decisive fact for this vendor is in §4: Deutsche Telekom AG is a designated CTPP.** Selecting the German national champion does not put a financial entity outside the DORA oversight framework.
>
> *Not verified today:* the precise present relationship between the older Open Telekom Cloud (OpenStack-based) and the newer T Cloud Public, and whether OTC's historical underlying technology stack is still in place. Anyone writing content on this should verify it directly; the roadmap's source research treats "Open Telekom Cloud" as the current product name and that framing looks dated.

**plusserver.** Cologne-based, four German data centres, and the only provider in this list verified today as holding **BSI C5 Type II** (operating effectiveness over a period, not just design). ISO 27001, ISO 9001, PCI DSS. Its `pluscloud open` product runs on **OpenStack via the Sovereign Cloud Stack (SCS)** and is Gaia-X aligned — described as the first German enterprise open-source cloud on SCS. Markets "BaFin-compliant hosting & cloud" to finance and insurance.

> **Ownership caveat, and it is a real due-diligence point.** plusserver's own "about us" page does not state its ultimate owner, and public sources today are inconsistent about current ownership (historically a private-equity portfolio company). **Do not assert plusserver's ownership chain in content without a fresh companies-register check.** Under Art. 28(4)(d) this is not a nitpick: a provider whose ultimate beneficial owner is a fund, potentially non-EU, is a materially different sovereignty proposition from one owned by an EU operating group, and it can change without notice to customers.

### 3.3 Other EU providers

**Scaleway (Iliad Group, France).** French-owned, "100% European infrastructure", explicitly markets itself as "free from the US CLOUD Act". Verified: **ISO/IEC 27001:2022** and **HDS** (French health-data hosting). **SecNumCloud is in the qualification process, not yet awarded** — its own newsroom announces *entering* the process. Do not describe Scaleway as SecNumCloud-qualified. No DORA-specific or reversibility commitments were found on its public compliance pages today.

**OVHcloud (OVH Groupe SA, France).** Publicly listed, French-controlled. Holds **ANSSI SecNumCloud qualification** — the strongest sovereignty-adjacent credential actually obtainable in the EU today — for its Hosted Private Cloud offering across three French sites (Roubaix, Gravelines, Strasbourg), and more recently for its **Bare Metal Pod** platform. Note the qualification is **product- and site-scoped**, not company-wide; OVHcloud also operates outside the EU, including in North America.

### 3.4 Exoscale — and why "Swiss" is not "EU"

**Flagging this explicitly, as the task requires.** Exoscale is Swiss-founded (Geneva/Lausanne) and is frequently listed in "EU alternatives" round-ups. That framing is imprecise in a way that matters for a regulated financial entity:

1. **Switzerland is not in the EU or the EEA.** It is a third country for GDPR purposes, covered by a European Commission **adequacy decision** — which means transfers are permitted without additional safeguards, *but it is an adequacy decision, not membership*. Adequacy decisions are reviewable and have been struck down before in other contexts. DORA itself applies to the financial entity, not to Switzerland, but **Art. 29(2)** expressly directs entities to consider third-country insolvency-law and legal-framework factors in concentration-risk assessment — and a Swiss-hosted provider engages that provision where an EU-hosted one does not.
2. **Exoscale's footprint is genuinely mixed.** Verified zone list today: **DE-FRA-1 and DE-MUC-1 (Germany), AT-VIE-1 and AT-VIE-2 (Austria), BG-SOF-1 (Bulgaria), HR-ZAG-1 (Croatia)** — all EU — plus **CH-GVA-2 (Geneva) and CH-DK-2 (Zurich)** in Switzerland. An EU financial entity can run entirely within the EU zones. The point is that this has to be a *documented, contractually pinned choice* under Art. 30(2)(b), not an assumption.
3. **The ownership chain is the part most often missed.** Exoscale was acquired by **A1 Digital**, part of **A1 Telekom Austria Group** — which is itself **majority-owned by América Móvil, a Mexican group** (with Austrian state holding ÖBAG as the other significant shareholder). So the "Swiss sovereign alternative" has an Austrian intermediate parent and a Latin American ultimate controlling shareholder. That is not a criticism of the service; it is a fact that belongs in the due-diligence file, because "sovereign" was never defined as "not-American".

### 3.5 The hyperscaler "sovereign" offerings — current status

**AWS European Sovereign Cloud — LAUNCHED, and this is the biggest change since the roadmap's source research.**

- **Launched 15 January 2026**, first region in **Brandenburg, Germany**. Expansion announced for **Belgium, the Netherlands and Portugal** (no dates given).
- **90+ services** at launch across AI, compute, containers, database, networking, security, storage.
- **Structure:** a new parent company plus **three local subsidiaries incorporated in Germany as GmbHs**. Leadership are EU citizens obligated to abide by European law. An **advisory board of five** — three Amazon employees and two independent members, all European citizens and residents.
- **Claims:** all data *including all metadata* stays in the EU; "zero operational control outside of EU borders"; operated exclusively by EU residents; physical and logical separation from other AWS regions; no critical dependencies on non-EU infrastructure; Nitro System prevents AWS employee access to customer data. An emergency access path exists for authorised EU-resident AWS employees to source-code replicas.
- **Compliance milestone 10 March 2026:** SOC 2 Type 1 and **BSI C5 Type 1** reports covering **69 services**, plus seven ISO certifications (27001:2022, 27017, 27018, 27701, 22301, 20000-1, 9001).
- **Independent assessment:** the structure "depends upon trust in the local EU governance structures"; the residual risk is that AWS "could be forced under US laws like the CLOUD Act to override all the EU legal governance and controls." The advisory board provides accountability but **cannot override US legal obligations**. Analysts also note **no commitment to technology portability or reduced vendor lock-in** — directly relevant to exit planning.

**Microsoft.** Portfolio as of the November 2025 expansion:
- **EU Data Boundary** — completed February 2025; in 2026 extended to AI workloads, M365 Copilot data handling, telemetry, logs, confidential computing. In-country M365 Copilot processing in 4 countries by end-2025, +11 countries during 2026.
- **Sovereign Public Cloud** — available; **Data Guardian** (tamper-evident logging of engineer remote access) on the roadmap, not shipped.
- **Sovereign Private Cloud (Azure Local)** — scaled from 16 to hundreds of servers, SAN support, GPU support; **Microsoft 365 Local** GA from December (connected mode), **disconnected mode early 2026**.
- **National Partner Clouds** — **Delos Cloud** (Germany, SAP-operated, BSI requirements, aimed at public administration) and **Bleu** (France, Capgemini/Orange JV, ANSSI SecNumCloud requirements).
- **Residual risk, per independent assessment:** Microsoft remains a US-headquartered provider subject to extraterritorial frameworks; sovereignty improvements reduce but **"do not eliminate the legal basis"** for CLOUD Act access, across all four sovereignty domains (data, operational, technology, infrastructure). Consistent with the July 2025 Senate testimony in §1.2.

**Google.** Portfolio as currently marketed:
- **Google Cloud Data Boundary** — Tier A: regional pinning of core customer data, logged/conditioned administrative access, CMEK with optional external key storage, regional personnel access specification, optional partner supervision.
- **Google Cloud Dedicated** — dedicated infrastructure with independent operations; delivered in Europe with **Thales**, and in France through **S3NS**, a standalone French entity targeting SecNumCloud.
- **Google Distributed Cloud** — on-premises, with an **air-gapped mode** that runs independently and cannot be remotely shut down by Google (positioned for defence/national security).
- **Munich Sovereign Cloud Hub** opened November 2025; a Thales/Google Germany sovereign cloud partnership has been announced.

> **Date caution.** A German-language trade report headline states Google is targeting a sovereign cloud **in Germany by end of 2026**. That page could not be retrieved (robots.txt), so the headline is recorded but the detail is **unverified**. Treat any Google Germany date as provisional and re-check before use — this is exactly the class of announced-date that has slipped elsewhere in this market.

---

## 4. The finding that changes exit-strategy planning: who is actually a CTPP

On **18 November 2025**, the ESAs published the **first list of designated critical ICT third-party providers** under DORA Art. 31 — **19 entities**:

> Accenture plc · Amazon Web Services EMEA SARL · Bloomberg L.P. · Capgemini SE · Colt Technology Services · **Deutsche Telekom AG** · Equinix (EMEA) B.V. · Fidelity National Information Services, Inc. · Google Cloud EMEA Limited · International Business Machines Corporation · InterXion HeadQuarters B.V. · Kyndryl Inc. · LSEG Data and Risk Limited · Microsoft Ireland Operations Limited · NTT DATA Inc. · Oracle Nederland B.V. · **Orange SA** · SAP SE · Tata Consultancy Services Limited

**Three things follow, and they are the practical core of this document.**

1. **"Sovereign" and "European" do not mean "not a CTPP."** Deutsche Telekom AG and Orange SA are both designated. SAP SE — operator of Delos Cloud — is designated. Capgemini SE — half of the Bleu joint venture — is designated. A financial entity that migrates from AWS to Open Telekom Cloud/T Cloud specifically to escape CTPP-related oversight has not escaped anything; it has swapped one designated provider for another. Conversely, **StackIT, IONOS, plusserver, Scaleway, OVHcloud and Exoscale are not on the list** — which is a genuine differentiator, but see point 3.
2. **CTPP designation does not reduce the financial entity's own obligations.** The entity must still take into account risks identified by the Lead Overseer, and must still meet its own Art. 28/30 contractual and risk-management requirements. Where risks are not adequately addressed, a competent authority may require the entity to **suspend use of the service in whole or in part, or to terminate the contract in whole or in part**. That supervisory power is precisely why a *tested* exit capability, not just a documented one, is the point.
3. **Being small enough to avoid designation is not automatically good news.** The Art. 31 criteria are about systemic impact. A provider below the designation threshold sits outside ESA direct oversight — which means the financial entity gets *less* external assurance about that provider, not more, and carries correspondingly more of the diligence burden itself. This cuts directly against the intuitive reading and is worth building a scenario question around later.

---

## 5. Practical exit-strategy documentation guidance

**No new legal claims here.** This section applies the 2B dossier's already-verified requirements (findings 2B-A and 2B-B above; Art. 30(3)(f), Art. 28(8), and Art. 10 of Del. Reg. (EU) 2024/1773 on documented, periodically tested exit plans) to the vendor landscape in §3.

### 5.1 Scope first: which contracts even need one

Apply finding **2B-B** before anything else. The exit strategy is an **Art. 30(3)** obligation, triggered by the contract supporting a **critical or important function** as defined in Art. 3(22) — an impact-based test, not a contract-value or headcount test. A common and expensive failure mode is producing exit documentation for the entire vendor portfolio, which dilutes reviewer attention across dozens of immaterial SaaS tools while the two contracts that actually matter get a template. Classify first, then document.

### 5.2 What "adequate transition period" documentation should actually demonstrate

Finding **2B-A** says there is no number to comply with. That is liberating and dangerous in equal measure: it means the entity is being asked to *justify* a period, and a justification is auditable in a way that a copied number is not. Documentation that holds up should show, at minimum:

- **A derivation, not an assertion.** The period should fall out of a stated migration plan — data volume, dependency inventory, the number of interfaces to rebuild, regression-test and parallel-run duration, regulatory notification lead times — not appear as a round number in a contract with no working behind it.
- **Contractual continuity of service, not just data export.** Art. 30(3)(f) as read in 2B requires the provider to *keep providing the service* during the transition period. A clause offering a 30-day data export window is the exact vendor-pushback pattern the 2B pilot's `kritische-funktionen-04` was written to catch.
- **Interaction with the Data Act floor (§2.1).** Where the Data Act applies, the provider cannot impose more than a two-month notice period and must complete switching within 30 days (extendable to seven months). Documentation should state how the DORA-adequate period and the Data Act mechanics fit together, because a reviewer will ask.
- **Evidence of testing.** Del. Reg. (EU) 2024/1773 Art. 10 requires exit plans to be **documented and periodically tested** (read in the 2B dossier, §5 gap item 7 — available and untested in that pilot). An untested plan is a document, not a strategy. Test evidence — even a partial restore into a second provider, or a tabletop with timings — is the difference between an exit strategy and an exit intention.

### 5.3 Data portability: what to actually specify

- **Formats, named.** "Easily accessible format" is the Art. 30(2)(d) standard for return of data. Turn it into named formats in the contract (Parquet/CSV/JSON for data; documented schema; OCI images for workloads; Terraform/OpenTofu or similar for infrastructure definitions). Open, documented, non-proprietary beats "a format mutually agreed at the time".
- **Metadata, configuration and logs, not just payload data.** The AWS ESC announcement makes a point of metadata staying in the EU precisely because metadata is separately valuable. Exit inventories routinely omit IAM policy, network configuration, key material, monitoring rules and audit logs — the things that make the payload data usable. Log retention obligations frequently outlive the contract.
- **Egress cost, with a 2027 caveat.** Model it, but note that Data Act Art. 29 **prohibits switching charges from 12 January 2027**. Cost models built on current egress pricing will overstate exit cost for any exit executed after that date, and any exit clause that prices egress needs a sunset provision.
- **The proprietary-service problem is the real lock-in.** Portability of *data* is largely solved. Portability of *architecture* is not. A workload built on a single provider's managed serverless, proprietary managed database, or first-party AI services has an exit cost dominated by rebuild effort, and no amount of data-format specification touches it. The KuppingerCole assessment of AWS ESC specifically notes the absence of any technology-portability commitment. Architects should record, per critical workload, which services have a standards-based equivalent and which do not — that inventory *is* the honest transition-period derivation asked for in §5.2.

### 5.4 Exiting a hyperscaler vs. exiting a smaller EU provider

These are genuinely different exercises, and treating them identically is the most common architectural mistake in this area.

| | **Exit FROM a hyperscaler** | **Exit FROM a smaller EU-sovereign provider** |
|---|---|---|
| **Dominant risk** | Lock-in depth. Proprietary managed services, IAM model, huge data volumes, long dependency chains. | **Provider viability and capability.** Smaller balance sheet, PE or single-group ownership, narrower service catalogue, thinner regional redundancy. |
| **Likely trigger for exit** | Regulatory/supervisory action, a strategic sovereignty decision, or commercial renegotiation. Rarely sudden. | Insolvency, acquisition, strategic pivot, or the provider failing to keep pace on a needed service. **Can be sudden.** |
| **Time available** | Usually planned, with notice. | May be compressed. Art. 30(2)(d) — data access/recovery/return **on insolvency** — is the baseline clause that earns its keep here (2B dossier §4.2 flags this as an easy-to-miss Art. 30(2) content). |
| **Where to go** | An EU provider, another hyperscaler, or on-premises. Feature parity at the destination is the constraint. | Often *to* a hyperscaler, or to another EU provider. Usually easier technically where the source runs open standards (OpenStack/SCS at plusserver, Kubernetes-first stacks). |
| **Concentration risk (Art. 29)** | Substitutability is poor because the plausible alternatives are three companies. **Four of the five relevant providers are designated CTPPs** (§4). | Substitutability is nominally better, but the concentration may be *within a group* — e.g. a provider whose own infrastructure rests on a designated CTPP's colocation (Equinix and InterXion are both on the CTPP list). **Nth-party mapping is the harder problem here.** |
| **Practical tell** | The exit plan is long, expensive and well-understood. | The exit plan is short and cheap on paper — and is the one more likely to be executed under time pressure. |

**Art. 29 concentration risk is cited, not re-derived** — it is covered in the 2B dossier (§2 item 3 via Art. 28(4)(c); §5 gap item 5 notes Art. 29(2)'s third-country and insolvency-law dimension as untested) and in the earlier `dora-pilot-pre-review-dossier-2026-08-13.md`. The specific addition this document makes is the empirical one in §4: the CTPP list makes the concentration analysis checkable against a published list rather than left to judgement, and the list contains European national champions.

### 5.5 A minimum documentation set for one critical workload

Offered as a practitioner checklist, not as a compliance standard:

1. Art. 3(22) classification decision, with the impact reasoning, for the function the service supports.
2. Service inventory: every provider service consumed, marked standards-based / proprietary / no direct equivalent.
3. Named destination(s), with a stated reason each is credible — including at least one that is not the same jurisdiction tier as the incumbent.
4. Data and asset inventory: payload, metadata, configuration, keys, logs, with target formats named.
5. Derived transition-period estimate with the working shown (§5.2), reconciled against Data Act notice/transition limits (§2.1).
6. Contract mapping: which Art. 30(2)/(3) clause covers each step, and where the contract falls short of what the plan assumes.
7. Nth-party map: subcontractors and their subcontractors, checked against the CTPP list (§4), including colocation and connectivity providers.
8. Test record: what was tested, when, by whom, what broke, what the measured timings were.
9. Trigger and governance: who decides to invoke, on what signals, and to whom it is escalated.
10. Review date, and an owner who is a named person.

---

## 6. Deliberate non-assertions — and the distractors they justify

Matching the house style established in `docs/dora-procurement-pre-review-dossier-2026-08-16.md` §3. These are propositions this document **deliberately does not make**, each of which is a plausible-sounding error worth building a distractor around if this material is ever turned into questions.

**6.1 No vendor is "DORA-compliant", and no vendor certification substitutes for the entity's own exit strategy.**
This is the central non-assertion of the whole document. DORA obligations attach to the **financial entity**. A provider can hold C5, ISO 27001, SecNumCloud, EU Cloud CoC adherence and every attestation in §3, be EU-owned and EU-operated — and the entity still has to produce, maintain and **test** its own documented exit strategy under Art. 30(3)(f)/Art. 28(8). The DLA Piper reading of the CTPP designation makes the same point from the other direction: even a provider under direct ESA oversight does not discharge the entity's obligations. **A real, citable instance of the misconception exists in the wild** — STACKIT's own financial-services page calls the company "a DORA-compliant ICT service provider" (§3.2). That is a strong distractor because it is a genuine vendor claim, not a strawman.

**6.2 "Sovereign cloud" is not a certification, a legal status, or a defined term in force.**
As of 2026-08-16: EUCS is **not adopted** (§2.2) and CADA is **a proposal** (§2.3). Any content implying a learner can look up or verify a "sovereign cloud certification" is wrong today. What exists is C5, IT-Grundschutz, SecNumCloud, ISO, and the EU Cloud Code of Conduct — each with a defined, checkable scope.

**6.3 Choosing an EU or German provider does not remove DORA oversight exposure.**
Deutsche Telekom AG, Orange SA, SAP SE and Capgemini SE are all designated CTPPs (§4). "Migrate to a European provider and the CTPP problem goes away" is false and is the highest-value distractor this research produced.

**6.4 DORA does not mandate any exit transition-period duration.**
Restated from 2B finding **2B-A** — not re-derived. "Adequate" is the standard. Any specific figure (24 months, 12 months, 6 months) is wrong as a statement of DORA law. Note the interaction trap: the Data Act's 30-day/seven-month switching limits (§2.1) are *provider-side switching mechanics under a different regulation*, and presenting them as "DORA's exit timeline" would be a subtle and very plausible error.

**6.5 An exit strategy is not required for every ICT contract.**
Restated from 2B finding **2B-B** — Art. 30(3) tier only, critical or important functions. Not in the Art. 30(2) baseline.

**6.6 Data residency is not jurisdictional immunity.**
Storing data in Frankfurt under a US-parented provider does not put it beyond US extraterritorial process. Microsoft France's own sworn testimony to the French Senate in July 2025 is the cleanest evidence (§1.2), and independent 2026 assessments of both the AWS and Microsoft sovereign offerings reach the same conclusion: the legal basis for access is reduced in practice, not eliminated.

**6.7 Being absent from the CTPP list is not a mark of quality.**
It reflects systemic footprint, not resilience or suitability. It also means *less* external supervisory assurance for the entity to lean on (§4, point 3).

**6.8 "Swiss" is not "EU".**
Switzerland is a third country operating under an adequacy decision (§3.4). An "EU alternative" round-up that includes Exoscale without that qualifier is imprecise, and Art. 29(2)'s third-country considerations are engaged.

**6.9 A certification named without its scope and type is close to meaningless.**
IONOS's C5 is **Type 1** on **three named services**; plusserver's is **Type II**; AWS ESC's is **Type 1** across 69 services as of March 2026; OVHcloud's SecNumCloud is scoped to specific products and three French sites; Scaleway's SecNumCloud is **in process, not awarded**. Content that lists these as undifferentiated bullet points would teach a procurement audience the wrong habit.

**6.10 This document asserts nothing about any provider's actual suitability.**
It records what was published and verifiable on 2026-08-16. Vendor selection is the entity's decision under Art. 28(4)(d) due diligence, and vendor facts here will go stale — see §7.

---

## 7. What changed versus older assumptions — evidence that this needs re-verification

Recorded so future readers can gauge decay rate. The roadmap's underlying source research (user's Gemini export, conducted 2026-08-15, but reflecting an older market picture) framed the landscape as *"the AWS/Microsoft 'sovereign cloud' hybrid offerings"* and *"Open Telekom Cloud (T-Systems)"*. As of the research date:

1. **AWS European Sovereign Cloud is no longer a future programme — it launched 15 January 2026** in Brandenburg with 90+ services, and reached its first C5/SOC 2/ISO compliance milestone on 10 March 2026. Any content describing it as announced-but-not-launched is wrong.
2. **The first CTPP list exists** (18 November 2025, 19 entities) and includes two European telcos. Before that list, "which providers are critical" was an inference; now it is a published fact, and the answer is not the one the sovereignty framing predicts.
3. **Deutsche Telekom's flagship is T Cloud Public**, not Open Telekom Cloud, with an Industrial AI Cloud live from 4 February 2026 and a 100%-feature-parity target for end-2026. The product naming in the source research is dated.
4. **The Data Act's switching regime has been applicable since 12 September 2025**, and the egress-fee prohibition lands 12 January 2027. This is the largest single change to the economics of cloud exit in the period, and it does not appear in the source research at all.
5. **CADA was proposed on 3 June 2026** — after the source research's evident horizon — and would be the first instrument to define sovereignty tiers in law.
6. **EUCS is still stalled**, which is a non-change worth recording explicitly, because "EUCS will resolve this" has been a standing assumption in this space for several years and has not come true.

**Decay estimate:** high. Six material changes in roughly nine months. Any content derived from this document should carry a visible "verified as at" date and be re-checked before each release.

---

## 8. Source ledger (all retrieved 2026-08-16)

**Regulatory / official**
- ESAs / EBA press release, designation of CTPPs under DORA, 18 Nov 2025 — https://www.eba.europa.eu/publications-and-media/press-releases/european-supervisory-authorities-designate-critical-ict-third-party-providers-under-digital
- EIOPA, *List of designated CTPPs* (PDF, the 19 named entities) — https://www.eiopa.europa.eu/document/download/56b1ca78-5dd2-4d36-8377-47a538eb7558_en?filename=List+of+designated+CTPPs.pdf
- European Commission, *Proposal for a Cloud and AI Development Act (CADA)* — https://digital-strategy.ec.europa.eu/en/library/proposal-cloud-and-ai-development-act-cada
- ENISA, *EUCS – Cloud Services Scheme* — https://www.enisa.europa.eu/publications/eucs-cloud-service-scheme

**Legal / analyst commentary**
- Deloitte Legal, *Cloud switching under the EU Data Act* (Chapter VI mechanics, dates, Art. 29 charge phase-out) — https://www.deloittelegal.de/dl/en/services/legal/perspectives/cloud-switching-eu-data-act.html
- DLA Piper, *Designation of critical ICT third-party providers under DORA*, Nov 2025 — https://www.dlapiper.com/en-us/insights/publications/2025/11/designation-of-critical-ict-third-party-providers-under-dora
- Morgan Lewis, *DORA: EU Regulators Announce List of Critical ICT Third-Party Providers* (count: 19; date) — https://www.morganlewis.com/blogs/sourcingatmorganlewis/2025/11/dora-eu-regulators-announce-list-of-critical-ict-third-party-providers
- cep, *EU Cloud Certification at an Impasse* (EUCS status, sovereignty-requirement deadlock) — https://www.cep.eu/eu-topics/details/eu-cloud-certification-at-an-impasse.html
- Hogan Lovells / hlc, *The EU's CADA: towards a sovereignty-focused framework* (3 June 2026 proposal, four Union Assurance Levels) — https://www.hlc.com/en/publications/the-eus-cloud-and-ai-development-act-cada-towards-a-sovereigntyfocused-framework-for-cloud
- KuppingerCole, *AWS EU Sovereign Cloud Announcement January 2026* — https://www.kuppingercole.com/blog/small/aws-eu-sovereign-cloud-announcement-january-2026
- KuppingerCole, *Microsoft's Sovereign Cloud in 2026* — https://www.kuppingercole.com/blog/small/microsofts-sovereign-cloud-in-2026
- The Register, *Microsoft exec admits it 'cannot guarantee' data sovereignty* (July 2025 French Senate testimony; page returned HTTP 403 on direct fetch, headline and substance corroborated across SDxCentral, Forbes and ActuIA search results) — https://www.theregister.com/off-prem/2025/07/25/microsoft_exec_admits_it_cannot_guarantee_data_sovereignty/458553

**Vendor / primary programme sources**
- AWS press release, *AWS Launches AWS European Sovereign Cloud*, 15 Jan 2026 — https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe
- AWS Security Blog, *AWS European Sovereign Cloud achieves first compliance milestone: SOC 2 and C5 reports plus seven ISO certifications*, 10 Mar 2026 — https://aws.amazon.com/blogs/security/aws-european-sovereign-cloud-achieves-first-compliance-milestone-soc-2-and-c5-reports-plus-seven-iso-certifications
- Microsoft Azure Blog, *Microsoft strengthens sovereign cloud capabilities with new services* (Nov 2025) — https://azure.microsoft.com/en-us/blog/microsoft-strengthens-sovereign-cloud-capabilities-with-new-services/
- Microsoft On the Issues, *Microsoft completes landmark EU Data Boundary*, 26 Feb 2025 — https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/
- Google Cloud, *Sovereign Cloud from Google* (Data Boundary / Dedicated / Distributed, S3NS, Thales) — https://cloud.google.com/sovereign-cloud
- Deutsche Telekom media release, *Hyperscaler Power with European Sovereignty: T Cloud Public* — https://www.telekom.com/en/media/media-information/archive/t-cloud-public-sovereign-power-1101542
- STACKIT, *Cloud solutions for financial services* (source of the "DORA-compliant ICT service provider" claim) — https://stackit.com/en/solutions/industries/financial-services
- Wikipedia, *Schwarz Digits* (ownership, Lübbenau build-out, milestones) — https://en.wikipedia.org/wiki/Schwarz_Digits
- IONOS Group SE, *IONOS receives C5 certification for Compute Engine, Cloud Cubes and S3 Object Storage* (Type 1, 7 Nov 2023) — https://www.ionos-group.com/investor-relations/publications/announcements/ionos-receives-c5-certification-for-compute-engine-cloud-cubes-and-s3-object-storage.html
- European Cloud, *IONOS provider profile* (ownership, data-centre locations incl. US) — https://european.cloud/provider/ionos/
- plusserver, *About us* (4 German DCs, C5 Type II, OpenStack/SCS, BaFin-compliant hosting positioning) — https://www.plusserver.com/en/company/about-us/
- Scaleway, *Security and compliance* (ISO 27001:2022, HDS, SecNumCloud in process) — https://www.scaleway.com/en/security-and-compliance/
- Scaleway newsroom, *Scaleway begins the SecNumCloud qualification process* — https://www.scaleway.com/en/news/scaleway-begins-the-secnumcloud-qualification-process/
- OVHcloud, *Security and Certifications* (SecNumCloud scope: Roubaix, Gravelines, Strasbourg) — https://corporate.ovhcloud.com/en/trusted-cloud/security-certifications/
- OVHcloud newsroom, *SecNumCloud qualification of Bare Metal Pod* — https://corporate.ovhcloud.com/en/newsroom/news/secnumcloud-qualification-bare-metal-pod/
- Exoscale, *Data centers* (full zone list) — https://www.exoscale.com/datacenters/
- TelecomTV, *A1 digital acquires Swiss cloud provider Exoscale* — https://www.telecomtv.com/content/tracker/a1-digital-acquires-swiss-cloud-provider-exoscale-28170/
- Wikipedia, *A1 Telekom Austria Group* (América Móvil majority shareholding, ÖBAG stake) — https://en.wikipedia.org/wiki/A1_Telekom_Austria_Group

**Retrieved as headline only, detail unverified**
- heise online, *Google Cloud: Sovereign Cloud in Germany by end of 2026* — https://www.heise.de/en/news/Google-Cloud-Sovereign-Cloud-in-Germany-by-end-of-2026-11338389.html — **blocked by robots.txt; the date claim is recorded but not confirmed. Re-verify before use.**

---

## 9. Gap list — what this document deliberately does not cover

1. **No MCQ pilot.** Per the roadmap, this is an add-on, not a module. If questions are ever written from it, §6 is the distractor bank and §4 is the highest-value single item.
2. **No new primary-source legal work.** No EUR-Lex or Cellar retrieval was performed today. Every DORA proposition is cited from the 2B dossier. The Data Act, EUCS and CADA statements in §2 come from **secondary legal commentary** and are explicitly weaker-sourced than anything in the 2B dossier — they would need primary-source verification to the same standard before shipping.
3. **EU Cloud Code of Conduct adherence per provider was not verified.** The CoC is mentioned as a category; no provider is asserted to be an adherent, because that requires checking the public adherence register, which was not done.
4. **No pricing, SLA or performance comparison.** Deliberately out of scope; it decays faster than everything else here and invites a "which is better" reading the document is trying to avoid.
5. **Open Telekom Cloud's current technical relationship to T Cloud Public was not established** (§3.2).
6. **plusserver's current ultimate ownership was not established** (§3.2) — flagged as a due-diligence action, not guessed.
7. **Bleu (France) was not researched directly**, only via Microsoft's own description. Delos Cloud likewise.
8. **Gaia-X and Sovereign Cloud Stack** are mentioned where providers cite them but were not assessed as programmes.
9. **BaFin and other national supervisory expectations on cloud exit** (e.g. BAIT/xAIT successor guidance) are entirely untouched. For a German-market B2B audience this is a real gap and probably the highest-value next research step.
10. **Nothing here has been reviewed by a lawyer.**

---

## 10. Kurzfassung (Deutsch)

**Kernaussage.** „Souveräne Cloud" ist kein Rechtsbegriff und keine Zertifizierung, sondern derzeit überwiegend ein Marketingbegriff. Für die Exit-Strategie-Dokumentation nach DORA ist deshalb entscheidend, drei Ebenen sauber zu trennen: **Datenresidenz** (wo liegen die Daten), **operative Souveränität** (wer kann technisch zugreifen) und **jurisdiktionelle Souveränität** (welchem Recht unterliegt der beherrschende Konzern). Nur die dritte Ebene schließt den Zugriff nach ausländischem Recht aus — und genau diese Ebene erreichen die Angebote der US-Hyperscaler auch in ihren „souveränen" Varianten nicht. Der Rechtsdirektor von Microsoft Frankreich hat im Juli 2025 vor dem französischen Senat unter Eid ausgesagt, er könne **nicht garantieren**, dass Daten französischer Bürger nicht an US-Behörden übermittelt werden. Unabhängige Analysen zu AWS und Microsoft kommen 2026 übereinstimmend zu dem Ergebnis, dass die Souveränitätsmaßnahmen das Risiko zwar verringern, die **Rechtsgrundlage für einen Zugriff aber nicht beseitigen**.

**Wichtigster praktischer Befund.** Am 18. November 2025 haben die ESAs die erste Liste kritischer IKT-Drittdienstleister (CTPP) nach Art. 31 DORA veröffentlicht — **19 Unternehmen**, darunter neben Amazon, Microsoft, Google, IBM und Oracle auch die **Deutsche Telekom AG**, **Orange SA**, **SAP SE** und **Capgemini SE**. Der Wechsel zu einem europäischen Anbieter führt also **nicht** automatisch aus dem CTPP-Aufsichtsrahmen heraus. StackIT, IONOS, plusserver, Scaleway, OVHcloud und Exoscale stehen nicht auf der Liste — was allerdings auch bedeutet, dass für diese Anbieter **keine** direkte ESA-Aufsicht als zusätzliche Sicherheit zur Verfügung steht und das Finanzunternehmen die Sorgfaltspflicht vollständig selbst trägt.

**Verhältnis zu DORA.** Die rechtliche Grundlage ist im Dossier zu Modul 2B bereits primärquellengeprüft und wird hier nur referenziert: Die Exit-Strategie ist eine Pflicht **allein auf der Ebene von Art. 30 Abs. 3 Buchst. f** (kritische oder wichtige Funktionen), nicht Teil des Grundkatalogs nach Art. 30 Abs. 2. DORA schreibt **keine bestimmte Dauer** der Übergangsfrist vor; der Verordnungstext verlangt eine „angemessene" Frist. Wer eine Zahl nennt, muss sie herleiten — aus Datenvolumen, Schnittstellen, Testläufen und Meldefristen — und nicht abschreiben.

**Zusätzlich zu beachten.** Kapitel VI des **EU Data Act** (Verordnung (EU) 2023/2854) gilt seit dem **12. September 2025** und regelt den Anbieterwechsel unmittelbar: maximal zwei Monate Kündigungsfrist, Übergang grundsätzlich binnen 30 Tagen (in Ausnahmefällen bis zu sieben Monate), und ab dem **12. Januar 2027 ein vollständiges Verbot von Wechselentgelten** einschließlich Egress-Gebühren. Bestehende Exit-Kostenmodelle sind daher neu zu rechnen.

**Klarstellung (bewusste Nicht-Aussage).** **Kein Anbieter ist „DORA-konform"** in einem Sinne, der die eigenen Pflichten des Finanzunternehmens ersetzen würde — auch dann nicht, wenn er über C5, ISO 27001, SecNumCloud oder IT-Grundschutz verfügt und vollständig in EU-Eigentum steht. Die Pflicht zur dokumentierten und **regelmäßig getesteten** Exit-Strategie trifft das Finanzunternehmen selbst. Werbeaussagen wie „DORA-compliant ICT service provider" sind in diesem Sinne unzutreffend und eignen sich hervorragend als Distraktor.

---

**Reminder:** this is draft groundwork for training content. It is not legal advice, has not been reviewed by a qualified lawyer, and must not be used commercially or shipped to learners before that review. Vendor facts are accurate as at **2026-08-16** and decay quickly — see §7.

*Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall durch qualifizierte Juristen oder Wirtschaftsprüfer zu validieren.*
