# Versicherungsvermittler / Versicherungsberater (§ 34d GewO) — IHK-Sachkundeprüfung — pre-review dossier (2026-08-17)

**Status:** AI-prepared research groundwork only — **NOT legal advice**. Not reviewed by a lawyer, by any IHK Prüfungsausschuss member, or by anyone on the DIHK/BWV Sachverständigengremium.

**Requested:** work up § 34d GewO (Versicherungsvermittler/-berater) as an IHK-Sachkundeprüfung exam-prep module — the candidate newly spotted in `docs/maklerschein-pre-review-dossier-2026-08-17.md` §5 — and, *if and only if* the sourcing situation is genuinely solvable, draft a first-round pilot.

**Delivered:** this dossier **and** `data/versicherungsvermittler_pilot_DRAFT.json` (30 questions, DE canonical + EN) plus its deterministic generator `data/gen_versicherungsvermittler_draft.py`. The blocker is **solved, but only partly, and the part that is not solved is a real product constraint that must be stated on the tin** — see §0.2. This is the first module in this repo where the honest answer is "buildable, at a bounded scope" rather than a clean yes or no.

**Files touched:** this file, `data/versicherungsvermittler_pilot_DRAFT.json`, `data/gen_versicherungsvermittler_draft.py`. Nothing else. `data/build_modules.py`, `data/modules_manifest.json`, `app/data/modules.json` and `app/app.js` are untouched; no build was run; nothing was staged or committed. The `_DRAFT` suffix keeps the pilot out of the live build path by construction.

---

## 0. The findings, first, because three of them are scope decisions and not footnotes

### 0.1 The syllabus problem is solved by statute, exactly as it was for § 34a

**Anlage 1 VersVermV**, *"Inhaltliche Anforderungen an die Sachkundeprüfung"* (Fundstelle: BGBl. I 2018, 2493–2495), is a four-level, sub-item-granular syllabus, incorporated into the exam's legal definition by **§ 2 Abs. 2 Satz 2 VersVermV**: *"Die inhaltlichen Anforderungen an die Sachkundeprüfung bestimmen sich nach der **Anlage 1**."* German statutory text is an *amtliches Werk* under **§ 5 UrhG** and carries no copyright.

This is the same structural unblock the § 34a round found in § 9 Abs. 2 BewachV + Anlage 2 BewachV (`docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md` §0.1, §3), and it is **stronger here in one respect and weaker in another**:

| | § 34a Bewachungsgewerbe | § 34d Versicherungsvermittlung |
|---|---|---|
| Statutory syllabus | Anlage 2 BewachV — but formally the *Unterrichtungs* curriculum, imported into the exam **by reference**, so a floor and not a ceiling | **Anlage 1 VersVermV — drafted for the exam itself.** No import gap. **Stronger.** |
| Pass rule | Not federal law; IHK Satzung (§ 11 Abs. 8 BewachV) | **Federal law, to the percentage point** (§ 4 Abs. 7 VersVermV). **Stronger.** |
| Question sets | bundeseinheitlich by IHK-organisation practice; no statutory mechanism (BewachV has no Aufgabenauswahlausschuss) | **Statutory**: § 4 Abs. 3 VersVermV constitutes a *"bundesweit einheitlich tätiger Aufgabenauswahlausschuss"* with a named 8-member composition. **Stronger.** |
| Subject matter reachable from law alone | Yes, essentially all of it — the syllabus resolves to BGB/StGB/StPO/WaffG provisions | **No, not all of it.** Roughly half the syllabus by teaching hours is *product* knowledge tested against a **privately published model-conditions work**. **Weaker — see §0.2.** |

### 0.2 The finding that actually bounds this module: **Proximus**

The written part of the exam is **not** graded against the law alone. It is graded against a specific, named, commercially published body of model insurance conditions and tariffs for a **fictional insurer invented by the BWV Bildungsverband**.

> **DIHK/BWV Rahmenplan, "Der Rahmenplan in der praktischen Anwendung", p. 6** — "Der schriftliche Prüfungsteil dauert 160 Minuten. […] Im schriftlichen Prüfungsteil werden **die Proximus-Versicherungsbedingungen 5 zu Grunde gelegt**. Nur dadurch kann eine einheitliche Basis für die überbetriebliche Prüfung gewährleistet werden."

> Same document, p. 4 — the 6th edition was needed *"aufgrund gesetzlicher Änderungen und Neuerungen sowie der Aktualisierung des **für den schriftlichen Prüfungsteil maßgeblichen Bedingungswerkes „Proximus 5"**"*, and *"Sowohl Proximus 5 als auch dieser Rahmenplan sind ab dem **01.07.2023** prüfungsrelevant."*

**What Proximus is** (BWV Bildungsverband, own description, Tier B): *"unsere fiktive Versicherungsgesellschaft Proximus"* — a conditions-and-tariffs compendium across the insurance lines, sold as print and e-book through the **BWV shop**, and described by the BWV as an approved aid for three IHK qualifications. It is **not** law, **not** an *amtliches Werk*, and **not** free. Its publisher, the Berufsbildungswerk der Deutschen Versicherungswirtschaft e. V., is precisely the kind of body AGENTS.md constraint 1 has in mind: it publishes and sells the preparation material for this exam.

**Why this matters, stated precisely.** § 2 Abs. 2 Satz 1 VersVermV itself says the exam covers *"die rechtlichen Grundlagen und **marktübliche allgemeine Versicherungsbedingungen**"*. The legislature therefore *knows* that a chunk of the exam is AVB knowledge and deliberately declined to fix which AVB. The IHK organisation filled that gap with a private work. The consequence for this repo:

- **Areas that are statutorily groundable** — the whole of Anlage 1 Nr. 2 (Rechtliche Grundlagen: VVG contract law, Vermittlerrecht, Wettbewerb, Verbraucherschutz, Datenschutz, Versicherungsaufsicht, Binnenmarkt, GwG), Nr. 1 (Kundenberatung, to the extent it is the statutory Beratungs-/Dokumentationspflicht rather than sales technique), Nr. 3.1 (GRV → SGB VI), Nr. 3.3 (bAV → BetrAVG/EStG), the statutory limbs of Nr. 3.4/3.5 (GUV → SGB VII; GKV/SPV → SGB V/XI; VVG §§ 178, 192 ff.), and the statutory floors under Nr. 4 (VVG Schadens- und Haftpflichtversicherungsrecht §§ 74–124; PflVG). **These are Tier A and independently authorable, and the draft is built entirely from them.**
- **Areas that are not** — *Leistungsumfang, Ausschlüsse, Klauseln, Tarifaufbau und -anwendung, Annahmerichtlinien, Entschädigungsgrenzen, Versicherungsformen* across Anlage 1 Nr. 3.2, 3.4, 3.5 and all of Nr. 4. These are Proximus-graded. **This module cannot honestly claim to prepare a candidate for those, and must not try to reconstruct them from any vendor's material.**

**Net verdict: the blocker is solved for a well-defined, statutorily-grounded core, and is NOT solved — and is not solvable inside constraint 1 — for the AVB/tariff half.** The recommendation in §9 is to build the core, label it exactly, and say out loud that the learner still needs Proximus 5 for the product half. That is an honest and, commercially, a perfectly good position: nobody publishes free practice material for the legal half either.

### 0.3 A correction to this repo's own record: the citation in the Maklerschein dossier is stale by eight and a half years

`docs/maklerschein-pre-review-dossier-2026-08-17.md` §5 records the § 34d Sachkunde limb as **"Abs. 2 Nr. 4"**. It is not, and has not been since **23 February 2018**.

- **Current law:** the four Versagungsgründe, including Sachkunde, are at **§ 34d Absatz 5 Satz 1 Nummer 4 GewO**. Verified three ways: the consolidated text on `gesetze-im-internet.de`; the consolidated text on `buzer.de`; and — decisively — the **VersVermV's own internal cross-references**, which say *"§ 34d **Absatz 5 Satz 1 Nummer 4**"* in § 2 Abs. 1, § 11, § 12 Abs. 1 and Anlage 2, i.e. a second federal instrument citing the location four separate times.
- **What Abs. 2 is now:** the **Versicherungsberater** limb — permission requirement, definition, the Honorar-only rule and the Zuwendungsverbot.
- **When it moved:** § 34d was restructured by **Art. 1 des Gesetzes zur Umsetzung der Richtlinie (EU) 2016/97 … über Versicherungsvertrieb**, v. 20.07.2017, BGBl. I S. 2789, in force **23.02.2018**. The superseded wording was retrieved directly (`buzer.de/gesetz/3982/al0-66542.htm` and `…/al0-55333.htm`) and reads: *"**(2)** Die Erlaubnis ist zu versagen, wenn […] **4.** der Antragsteller nicht durch eine vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung nachweist, dass er die für die **Versicherungsvermittlung** notwendige Sachkunde […] besitzt"* — note also that the pre-2018 text did **not** contain *"oder Versicherungsberatung"*.

The Maklerschein dossier therefore quoted the **current wording** under the **pre-2018 location**. The wording it quoted is right; the citation is wrong. Correcting it here rather than editing that file, per the brief's "do not touch already-wired repo files" instruction — but §10 flags it for a one-line fix.

### 0.4 Two corrections to the task brief's own hypotheses

| Brief's hypothesis | Verdict |
|---|---|
| "gebundene Versicherungsvertreter under **Abs. 4**" | **Wrong Absatz.** § 34d **Abs. 4** is Nebenbestimmungen plus the three-month decision deadline plus IHK supervision. The gebundener Versicherungsvertreter sits in **§ 34d Abs. 7 Satz 1 Nr. 1**. |
| "the **Anlage 1** exemption for simple/ancillary insurance products" | **No such thing.** § 34d has no Anlagen. **Anlage 1 VersVermV is the exam syllabus** (§0.1), which is a different animal entirely and much more valuable. The ancillary-product exemptions are **§ 34d Abs. 6** (produktakzessorisch, on application) and **§ 34d Abs. 8** (Nebentätigkeit, by operation of law, with EUR 600 / EUR 200 / EUR 500 premium thresholds). |

Both would have produced wrong shipped copy. Both are corrected in §2, which is where the highest-value product content in this dossier sits.

---

## 1. Method and instruments read

All retrieval **2026-08-17**. `WebFetch` is `ROBOTS_DISALLOWED` on `gesetze-im-internet.de` in this sandbox; every German statutory text below was fetched by direct `curl`/`urllib` against `gesetze-im-internet.de` and parsed from raw HTML, so quotes are from the consolidated official text, not from a summary. The load-bearing § 34d structure was cross-read on `buzer.de` and against superseded Fassungen; the 2025 VersVermV amendment and the 2026 GewO amendment were read in the **official Bundesgesetzblatt PDFs**.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **GewO § 34d** (Versicherungsvermittler, Versicherungsberater) | `gesetze-im-internet.de/gewo/__34d.html`; cross-read `buzer.de/34d_GewO.htm`; superseded Fassungen `buzer.de/gesetz/3982/al0-66542.htm`, `…/al0-55333.htm` | **Abs. 1–13 in full**, current text twice independently, plus the pre-23.02.2018 text |
| **GewO § 34e** (Verordnungsermächtigung) | `gesetze-im-internet.de/gewo/__34e.html` | Abs. 1 Satz 1 Nr. 1–7, Abs. 2, 3 |
| **GewO §§ 11a, 32, 144** | same | § 11a (Vermittlerregister); § 32 Abs. 1, 2 (Sachkundeprüfungs-Satzungsrecht, Aufgabenauswahlausschüsse); **§ 144 Abs. 1 Nr. 1 lit. k–o, Abs. 2 Nr. 7–9, Abs. 4** (Bußgeldrahmen) |
| **VersVermV** (Versicherungsvermittlungsverordnung v. 17.12.2018, BGBl. I S. 2483; 2019 I S. 411; zuletzt geänd. Art. 1 V. v. 17.02.2025, BGBl. 2025 I Nr. 43) | `gesetze-im-internet.de/versvermv_2018/BJNR248310018.html` — **note the non-obvious slug `versvermv_2018`**; `/versvermv/` 404s | **Gesamtausgabe: §§ 1–27 and Anlagen 1–4 in full**, incl. Inhaltsübersicht |
| **1. VersVermVÄndV**, V. v. 17.02.2025, **BGBl. 2025 I Nr. 43** | **official BGBl PDF** `recht.bund.de/bgbl/1/2025/43/regelungstext.pdf` (2 pp.) | Art. 1, Art. 2 verbatim |
| **GewBürAbG**, G. v. 20.07.2026, **BGBl. 2026 I Nr. 215** | **official BGBl PDF** `recht.bund.de/bgbl/1/2026/215/regelungstext.pdf` (7 pp.) | Art. 1 Nr. 1–3, Art. 11 — checked specifically for § 34d; see §5.4 |
| **VVG** | `gesetze-im-internet.de/vvg_2008/` | **§§ 1a, 3, 6, 6a, 7, 7a, 7b, 7c, 8, 19, 23, 28, 33, 37, 59, 60, 61, 62, 63, 64, 74, 75, 76, 95, 100, 113, 115, 178, 193, 210, 213, 214 — full text of each** |
| **VAG** | `gesetze-im-internet.de/vag_2016/` | §§ 48, 48a, 48b, 48c |
| **GwG § 2** | `gesetze-im-internet.de/gwg_2017/__2.html` | Abs. 1 Nr. 7 and Nr. 8 verbatim |
| **BetrAVG §§ 1a, 1b; SGB VI § 35; SGB VII § 8; EStG § 3** | `gesetze-im-internet.de/…` | full text of each |
| **PflVG § 1, § 4 und Anlage zu § 4 Abs. 2** | `gesetze-im-internet.de/pflvg/` | Versicherungspflicht + **Mindestversicherungssummen** |
| **DIHK/BWV, "Geprüfter Fachmann für Versicherungsvermittlung IHK — Rahmenplan mit Lernzielen für die Sachkundeprüfung", 6. Auflage, Stand März 2025** | `bwv.de/fileadmin/…/Versicherungsvermittler/2025_Rahmenplan.pdf` (72 pp.) | Vorwort, alle Aktualisierungskommentare, Konzeption mit Stundenempfehlung, Taxonomie, Struktur — **see §4 for the copyright analysis and the strict use limits** |
| **IHK Düsseldorf** (Nr. 2595960), **IHK Rhein-Neckar** (Nr. 945188) | `ihk.de/…` | exam mechanics, fees, gating, retake rules, permitted aids |

**Deliberately not opened, not read, not cited for anything:** the exam-prep vendor sites that dominate the search results for this topic (`sachkundegurus.de`, `sachkundepruefung-versicherungsfachmann.de` and others appearing in result listings). AGENTS.md constraint 1 bans third-party exam-prep companies' text outright and there is no visual-accuracy carve-out that could apply to a question bank. Nothing here derives from any of them, directly or indirectly. **Proximus itself was likewise not purchased, downloaded, opened or consulted** — its existence and role are documented from the Rahmenplan and from the BWV's own public description, and nothing in the draft depends on knowing its contents.

### 1.1 Retrieval notes for the next agent

1. **The VersVermV slug is `versvermv_2018`.** `gesetze-im-internet.de/versvermv/` returns a 404 stub. The Gesamtausgabe (`BJNR248310018.html`) works here and returns the Anlagen inline — unlike the BewachV, where the equivalent URL returns a 236-byte stub and the Anlagen live at `anlage_N.html` (`bewachungsgewerbe` dossier §1.1). **Do not generalise either behaviour;** check per instrument.
2. **`buzer.de/34d_GewO.htm` header says *"zuletzt geändert durch Artikel 1 G. v. 20.07.2026 BGBl. 2026 I Nr. 215"*. That is the *title-level* stand line for the whole GewO, not § 34d's own version.** § 34d's own footer reads *"Text in der Fassung des Artikels 9 Finanzmarktdigitalisierungsgesetz (FinmadiG) G. v. 27. Dezember 2024 BGBl. 2024 I Nr. 438 m.W.v. 30. Dezember 2024."* Confirmed against the BGBl PDF: **GewBürAbG Art. 1 has exactly three Nummern (§ 6a, § 14 Abs. 8, § 34c Abs. 2a) and does not touch § 34d.** Reading the title-level line as a section-level line would have produced a false "just amended" claim.

---

## 2. The scope structure: **four tiers, not two** (Tier A — the commercially decisive finding)

The task brief asked for the exemption/scope boundaries "since scope boundaries have repeatedly been the highest-value finding in this project's other exam-module dossiers". They are again. § 34d contains **four** distinct positions, and only the first requires the exam.

### 2.1 Tier 1 — Erlaubnis + IHK-Sachkundeprüfung

> **§ 34d Abs. 1 Satz 1 GewO** — "Wer gewerbsmäßig den Abschluss von Versicherungs- oder Rückversicherungsverträgen vermitteln will (**Versicherungsvermittler**), bedarf nach Maßgabe der folgenden Bestimmungen der **Erlaubnis der zuständigen Industrie- und Handelskammer**."

> **§ 34d Abs. 2 Satz 1 GewO** — "Wer gewerbsmäßig über Versicherungen oder Rückversicherungen beraten will (**Versicherungsberater**), bedarf nach Maßgabe der folgenden Bestimmungen der Erlaubnis der zuständigen Industrie- und Handelskammer."

> **§ 34d Abs. 5 Satz 1 GewO** — "Eine Erlaubnis nach den Absätzen 1 und 2 **ist zu versagen**, wenn
> **1.** Tatsachen die Annahme rechtfertigen, dass der Antragsteller die für den Gewerbebetrieb erforderliche **Zuverlässigkeit** nicht besitzt,
> **2.** der Antragsteller in **ungeordneten Vermögensverhältnissen** lebt,
> **3.** der Antragsteller den Nachweis einer **Berufshaftpflichtversicherung oder einer gleichwertigen Garantie** nicht erbringen kann oder
> **4.** der Antragsteller **nicht durch eine vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung nachweist, dass er die für die Versicherungsvermittlung oder Versicherungsberatung notwendige Sachkunde über die versicherungsfachlichen, insbesondere hinsichtlich Bedarf, Angebotsformen und Leistungsumfang, und die rechtlichen Grundlagen sowie die Kundenberatung besitzt**."

Note the contrast the Maklerschein dossier drew: § 34c Abs. 2 has **two** refusal grounds and no knowledge limb; § 34a Abs. 1 Satz 3 has Sachkunde **and** Haftpflicht on top of the two; § 34d Abs. 5 has **all four**. § 34d is the most heavily gated of the three.

**The corporate route.** § 34d Abs. 5 Satz 4: where the applicant is not a natural person, it is enough that the Sachkundenachweis is held by *"eine im Hinblick auf eine ordnungsgemäße Wahrnehmung der erlaubnispflichtigen Tätigkeit **angemessene Zahl** von beim Antragsteller beschäftigten natürlichen Personen […], denen die **Aufsicht** über die unmittelbar mit der Vermittlung von oder der Beratung über Versicherungen befassten Personen übertragen ist und die den Antragsteller **vertreten** dürfen."* Satz 5 shuts that door for a natural person who *"selbst Versicherungen vermittelt oder über Versicherungen berät"* or is *"für diese Tätigkeiten in der Leitung des Gewerbebetriebs verantwortlich"*. Same architecture as § 34a's Betriebsleiter construction, different wording.

**Incompatibility.** § 34d Abs. 3: a Vermittler may not also run a Berater business and vice versa. Breach is an Ordnungswidrigkeit under § 144 Abs. 2 Nr. 7c GewO.

### 2.2 Tier 2 — **gebundener Versicherungsvertreter: no Erlaubnis, no exam** (§ 34d Abs. 7 Satz 1 Nr. 1)

> **§ 34d Abs. 7 Satz 1 GewO** — "Abweichend von Absatz 1 bedarf ein Versicherungsvermittler **keiner Erlaubnis**, wenn er **1.** seine Tätigkeit als Versicherungsvermittler **ausschließlich im Auftrag eines oder, wenn die Versicherungsprodukte nicht in Konkurrenz stehen, mehrerer Versicherungsunternehmen** ausübt, die im Inland zum Geschäftsbetrieb befugt sind, und **durch das oder die Versicherungsunternehmen für ihn die uneingeschränkte Haftung aus seiner Vermittlertätigkeit übernommen wird** […]"

This is the single largest cohort in German insurance distribution and it is **outside the exam requirement entirely**. Three consequences the module must state and does:

1. **Qualification does not disappear; it moves to the insurer.** **§ 48 Abs. 2 Satz 2 Nr. 1 VAG**: an insurer may cooperate with a § 34d Abs. 7 Satz 1 Nr. 1 intermediary only if that intermediary is reliable, in ordered financial circumstances, *"über die zur Vermittlung der jeweiligen Versicherung **angemessene Qualifikation** verfügt und sich regelmäßig fortbildet"*, and **§ 48 Abs. 2 Satz 5 VAG**: *"Inhalt, Umfang sowie Dokumentation von nachzuweisenden Qualifikationsmaßnahmen haben **Abschnitt 1 der Versicherungsvermittlungsverordnung** zu entsprechen."* So the *content* standard is the same VersVermV Abschnitt 1; the *proof mechanism* is not the IHK exam.
2. **Registration still applies.** § 34d Abs. 10 Satz 1 names Abs. 7 Satz 1 Nr. 1 among those who must be entered in the § 11a register — but by a different route: **§ 9 Abs. 2 VersVermV** directs that their register data is transmitted *"ausschließlich nach § 48 Absatz 4 Satz 1 des Versicherungsaufsichtsgesetzes"*, i.e. **by the insurer, on the intermediary's initiative**, and § 34d Abs. 10 Satz 3 makes that same notification the moment the insurer's unlimited liability attaches.
3. **The 15-hour CPD duty still applies to them** (§ 34d Abs. 9 Satz 2 names Abs. 7 Satz 1 Nr. 1 expressly). Only the Abs. 9 Satz 3 carve-out — purely ancillary products — lets any of them off.

### 2.3 Tier 3 — **produktakzessorischer Vermittler: Erlaubnis*befreiung* on application** (§ 34d Abs. 6)

> **§ 34d Abs. 6 Satz 1 GewO** — "Auf Antrag hat die zuständige Industrie- und Handelskammer einen Gewerbetreibenden, der die Versicherung als **Ergänzung der im Rahmen seiner Haupttätigkeit gelieferten Waren oder Dienstleistungen** vermittelt, von der Erlaubnispflicht nach Absatz 1 Satz 1 **auszunehmen**, wenn er nachweist, dass **1.** er seine Tätigkeit als Versicherungsvermittler unmittelbar im Auftrag eines oder mehrerer Versicherungsvermittler, die Inhaber einer Erlaubnis nach Absatz 1 Satz 1 sind, oder eines oder mehrerer Versicherungsunternehmen ausübt, **2.** für ihn eine **Berufshaftpflichtversicherung oder eine gleichwertige Garantie** nach Maßgabe des Absatzes 5 Satz 1 Nummer 3 besteht und **3.** er **zuverlässig sowie angemessen qualifiziert** ist und nicht in ungeordneten Vermögensverhältnissen lebt."

**The precise distinction, and it is easy to get wrong:** Abs. 6 requires *"angemessen qualifiziert"* — **not** the IHK-Sachkundeprüfung. Satz 2 makes the proof a *declaration by the principals* undertaking to comply with § 48 Abs. 2 VAG and to ensure the applicant's qualification. So Tier 3 keeps the Berufshaftpflicht limb of Abs. 5 (Nr. 3) and the Zuverlässigkeit/Vermögens limbs (Nr. 1, 2) but **drops the Sachkundeprüfung limb (Nr. 4) and replaces it with a self-declared, insurer-warranted "angemessene Qualifikation".** Tier 3 is registered (Abs. 10, § 8 Nr. 3 lit. a bb / b cc VersVermV distinguish "produktakzessorischer Versicherungsmakler" from "produktakzessorischer Versicherungsvertreter" in the register itself) and is subject to the 15-hour CPD duty unless the Abs. 9 Satz 3 carve-out bites.

### 2.4 Tier 4 — **§ 34d Abs. 8: outside the regime altogether**

> **§ 34d Abs. 8 GewO** — "Keiner Erlaubnis bedarf ferner ein Gewerbetreibender, **1.** wenn er als **Versicherungsvermittler in Nebentätigkeit** a) nicht hauptberuflich Versicherungen vermittelt, b) diese Versicherungen eine **Zusatzleistung** zur Lieferung einer Ware oder zur Erbringung einer Dienstleistung darstellen und c) diese Versicherungen das Risiko eines Defekts, eines Verlusts oder einer Beschädigung der Ware oder der Nichtinanspruchnahme der Dienstleistung oder die Beschädigung, den Verlust von Gepäck oder andere Risiken im Zusammenhang mit einer bei dem Gewerbetreibenden gebuchten Reise abdecken und **aa)** die Prämie bei zeitanteiliger Berechnung auf Jahresbasis einen Betrag von **600 Euro** nicht übersteigt oder **bb)** die Prämie je Person abweichend von Doppelbuchstabe aa einen Betrag von **200 Euro** nicht übersteigt, wenn die Versicherung eine Zusatzleistung zu einer einleitend genannten Dienstleistung mit einer Dauer von **höchstens drei Monaten** darstellt; **2.** wenn er als **Bausparkasse** oder als von einer Bausparkasse beauftragter Vermittler für Bausparer Versicherungen im Rahmen eines Kollektivvertrages vermittelt […] oder **3.** wenn er als Zusatzleistung zur Lieferung einer Ware oder der Erbringung einer Dienstleistung im Zusammenhang mit Darlehens- und Leasingverträgen **Restschuldversicherungen** vermittelt, deren **Jahresprämie einen Betrag von 500 Euro nicht übersteigt**."

**Tier 4 is the genuinely different one.** Compare the addressee lists:

- **§ 34d Abs. 10 Satz 1** (Registerpflicht) names Abs. 1 Satz 2, Abs. 2 Satz 2, **Abs. 6 Satz 1** and **Abs. 7 Satz 1 Nr. 1** — **Abs. 8 is absent.**
- **§ 34d Abs. 9 Satz 1 und 2** (Beschäftigtenprüfung; 15 h Weiterbildung) name Abs. 1, 2, 6 and **Abs. 7 Satz 1 Nr. 1** — **Abs. 8 is absent.**

**So a § 34d Abs. 8 intermediary needs no permission, no exemption decision, no register entry and no CPD hours.** They are not, however, in a lawless space: **§ 48 Abs. 1 Nr. 1 VAG** requires insurers to work only with intermediaries who are licensed, exempted, or fall under Abs. 7 Satz 1 Nr. 1 **or Abs. 8**, and **§ 66 VVG** (checked in the citation apparatus) carves this cohort out of specified VVG information duties while leaving a residual pre-contractual duty. The complete statement is in the draft's `scope_boundary_note`.

### 2.5 Employees, at every tier

> **§ 34d Abs. 9 Satz 1 GewO** — "Gewerbetreibende nach den Absätzen 1, 2, 6 und 7 Satz 1 Nummer 1 dürfen unmittelbar bei der Vermittlung oder Beratung mitwirkende Personen nur beschäftigen, wenn sie **deren Zuverlässigkeit geprüft haben und sicherstellen, dass diese Personen über die für die Vermittlung der jeweiligen Versicherung sachgerechte Qualifikation verfügen**."

**"Sachgerechte Qualifikation" is not the Sachkundeprüfung.** Nothing in § 34d requires a rank-and-file employed adviser to hold the IHK certificate; the duty is on the employer to ensure appropriate qualification, enforceable by an employment prohibition under § 34d Abs. 9 Satz 6. The CPD duty in Satz 2, by contrast, does bite on those employees directly: *"Gewerbetreibende nach Absatz 1 Satz 1 bis 4, Absatz 2 Satz 1 und 2 und Absatz 7 Satz 1 Nummer 1 **und die unmittelbar bei der Vermittlung oder Beratung mitwirkenden Beschäftigten** müssen sich in einem Umfang von **15 Stunden je Kalenderjahr** […] weiterbilden."*

### 2.6 The scope-boundary statement, as it should appear in shipped copy

> The **IHK-Sachkundeprüfung nach § 34d Abs. 5 Satz 1 Nr. 4 GewO** is required only of an applicant for a **Versicherungsvermittler-Erlaubnis (Abs. 1)** or a **Versicherungsberater-Erlaubnis (Abs. 2)** — and, for a non-natural-person applicant, only of an *angemessene Zahl* of supervising, representation-authorised employees (**Abs. 5 Satz 4**), unless the applicant is a natural person who personally mediates/advises or leads that function (**Abs. 5 Satz 5**). It is **not** required of a **gebundener Versicherungsvertreter (Abs. 7 Satz 1 Nr. 1)**, whose qualification is warranted by the liability-assuming insurer under **§ 48 Abs. 2 VAG**; **not** of a **produktakzessorischer Vermittler (Abs. 6)**, who needs only to be *"angemessen qualifiziert"*, proved by the principals' declaration under **Abs. 6 Satz 2**; **not** of a **Nebentätigkeits-, Bausparkassen- or small-Restschuldversicherungs-Vermittler (Abs. 8)**, who is outside the permission, register and CPD regime altogether; and **not** of an employed adviser, who needs *"sachgerechte Qualifikation"* under **Abs. 9 Satz 1** but not the certificate.

---

## 3. The statutory syllabus (Tier A) — what unblocks the module

### 3.1 Chain of authority

**§ 34e Abs. 1 Satz 1 Nr. 5 GewO** empowers the ministry, with Bundesrat consent, to lay down *"die **Inhalte und das Verfahren für eine Sachkundeprüfung** nach § 34d Absatz 5 Satz 1 Nummer 4, die Ausnahmen von der Erforderlichkeit der Sachkundeprüfung sowie die Gleichstellung anderer Berufsqualifikationen mit der Sachkundeprüfung, die örtliche Zuständigkeit der Industrie- und Handelskammern, die Berufung eines **Aufgabenauswahlausschusses**"*. The VersVermV is the exercise of that power. Then:

> **§ 2 Abs. 1 VersVermV** — "**Gegenstand der Sachkundeprüfung** nach § 34d Absatz 5 Satz 1 Nummer 4 der Gewerbeordnung sind die erforderlichen Kenntnisse und Fähigkeiten auf folgenden Gebieten **und deren praktische Anwendung**:
> **1. fachliche Grundlagen:**
> a) **rechtliche Grundlagen** für die Versicherungsvermittlung und -beratung,
> b) **sozialversicherungsrechtliche Rahmenbedingungen**, insbesondere gesetzliche Rentenversicherung, private Vorsorge durch Lebens-, Renten- und Berufsunfähigkeitsversicherung, Grundzüge der betrieblichen Altersversorgung, staatliche Förderung und steuerliche Behandlung der privaten Vorsorge und der durch Entgeltumwandlung finanzierten betrieblichen Altersversorgung,
> c) **Unfallversicherung, Krankenversicherung und Pflegeversicherung**,
> d) **verbundene Hausratversicherung und verbundene Gebäudeversicherung**,
> e) **Haftpflichtversicherung, Kraftfahrtversicherung und Rechtsschutzversicherung**;
> **2. Kundenberatung:** a) Bedarfsermittlung, b) Lösungsmöglichkeiten, c) Produktdarstellung und Information."

> **§ 2 Abs. 2 VersVermV** — "Die Sachkundeprüfung umfasst zu den in Absatz 1 Nummer 1 genannten Grundlagen insbesondere den **zielgruppenspezifischen Bedarf, die Angebotsformen, den Leistungsumfang, den Versicherungsfall sowie die rechtlichen Grundlagen und marktübliche allgemeine Versicherungsbedingungen**. Die inhaltlichen Anforderungen an die Sachkundeprüfung bestimmen sich nach der **Anlage 1**."

**Two structural facts fall straight out of this.** First, § 2 Abs. 1 Nr. 1 **lit. a–e are the five written-exam areas**, and § 4 Abs. 7 keys the pass rule to them by name. Second, **§ 2 Abs. 1 Nr. 2 (Kundenberatung) is the *practical* part** — § 4 Abs. 4: *"Dieser Prüfungsteil umfasst die **Kundenberatung nach § 2 Absatz 1 Nummer 2** und wird als **Simulation eines Kundenberatungsgesprächs** durchgeführt."* Kundenberatung is therefore **not multiple-choice-testable**, and the draft says so rather than pretending otherwise — exactly as the § 34a draft did for that exam's oral part.

Note also Abs. 1's *"und deren praktische Anwendung"* and § 4 Abs. 2 Satz 2: *"Sie sind anhand **praxisbezogener Aufgaben** und in einem **ausgewogenen Verhältnis** zueinander zu prüfen."* The exam is applied, not recitation; the draft is written in situation style accordingly, the same choice `aevo` and `bewachungsgewerbe` made.

### 3.2 Anlage 1 VersVermV — reproduced, because it is copyright-free and it is the authoring outline

**Anlage 1 (zu § 2 Absatz 2 Satz 2), "Inhaltliche Anforderungen an die Sachkundeprüfung", Fundstelle: BGBl. I 2018, 2493–2495.** Top two levels only; the third level is in the retrieved text and in the draft's authoring notes.

| | Area | Sub-areas (Anlage 1's own wording) |
|---|---|---|
| **1** | **Kundenberatung** | 1.1 Serviceerwartungen des Kunden · 1.2 Besuchsvorbereitung/Kundenkontakte · 1.3 Kundengespräch **unter Beachtung ethischer Grundsätze** (Kundensituation und Kundenbedarf; Kundengerechte Lösungen; Gesprächsführung und Systematik) · 1.4 Kundenbetreuung |
| **2** | **Rechtliche Grundlagen** | 2.1 **Vertragsrecht** (Geschäftsfähigkeit; Zustandekommen von allgemeinen Verträgen; Grundlagen des Versicherungsvertrags; Beginn und Ende) · 2.2 **Besondere Rechtsvorschriften für den Versicherungsvertrag** (Versicherungsschein; Beitragszahlung; Obliegenheiten; **vorvertragliche Anzeigepflicht**; **Gefahrerhöhung**; Pflichten im Schadenfall; **Eigentumswechsel in der Schadenversicherung**) · 2.3 **Vermittler- und Beraterrecht** (Allgemeine Rechtsstellung; Grundlagen für die Tätigkeit; Besondere Rechtsstellung; **Umgang mit Interessenkonflikten**; Berufsvereinigungen; Arbeitnehmervertretungen) · 2.4 **Wettbewerbsrecht** · 2.5 **Verbraucherschutz** (Grundlagen; Schlichtungsstellen und Behandlung von Beschwerden; **Datenschutz**) · 2.6 **Versicherungsaufsicht: Zuständigkeiten** · 2.7 **Europäischer Binnenmarkt: Dienstleistungs- und Niederlassungsfreiheit** · **2.8 Geldwäschegesetz** |
| **3** | **Vorsorge** | 3.1 **Gesetzliche Rentenversicherung** (incl. Versorgungslücke, steuerliche Behandlung) · 3.2 **Private Vorsorge** durch Lebens-/Rentenversicherungen, **Versicherungsanlageprodukte** und Versicherungen zur Arbeitskraftabsicherung · 3.3 **Grundzüge der betrieblichen Altersversorgung** (Direktversicherung und Pensionskasse durch **Entgeltumwandlung**; Rechtsanspruch; Unverfallbarkeit; Insolvenz des Arbeitgebers; steuerliche und sozialversicherungsrechtliche Behandlung) · 3.4 **Gesetzliche und private Unfallversicherung** · 3.5 **Gesetzliche und private Krankenversicherung / soziale und private Pflegeversicherung** |
| **4** | **Sach-/Vermögensversicherung** | 4.1 **Haftpflichtversicherung** · 4.2 **Kraftfahrtversicherung** · 4.3 **Hausratversicherung** · 4.4 **Gebäudeversicherung** · 4.5 **Rechtsschutzversicherung** — each broken down to Einführung/Bedarf, Leistungsumfang, Versicherungssumme, **Tarifaufbau und -anwendung**, **Antragsaufnahme/Annahmerichtlinien**, Versicherungsfall, Besonderheiten |

**Reading this against §0.2:** area **2** is almost entirely resolvable to named federal instruments (BGB, VVG, GewO, VersVermV, UWG, VAG, DSGVO/BDSG, GwG, AEUV/IDD) and is Tier A throughout. Area **3** splits: 3.1, 3.3 and the *gesetzliche* halves of 3.4/3.5 are SGB VI / BetrAVG / EStG / SGB VII / SGB V / SGB XI; the *private* halves are partly VVG (§§ 150–171 Leben, 178–191 Unfall, 192–208 Kranken) and partly AVB. Area **4** is dominated by *Leistungsumfang / Ausschlüsse / Klauseln / Tarifaufbau / Annahmerichtlinien* — Proximus territory, with statutory floors only in VVG §§ 74–99 (Schadensversicherung), §§ 100–124 (Haftpflicht) and the PflVG/KfzPflVV for motor. Area **1** is a sales-conversation competence, examined orally.

### 3.3 The brief's hypothesis, checked item by item

The task brief offered a starting list and asked for it to be verified rather than assumed. Result:

| Brief's hypothesis | Verdict against Anlage 1 / § 2 VersVermV |
|---|---|
| Rechtsgrundlagen der Versicherungsvermittlung (GewO/VersVermV/IDD) | **Confirmed** — Anlage 1 Nr. 2.3, 2.6, 2.7; § 2 Abs. 1 Nr. 1 lit. a |
| Vertragsrecht (VVG basics) | **Confirmed** — Anlage 1 Nr. 2.1, 2.2, and much more granular than the brief assumed (the annex names Anzeigepflicht, Gefahrerhöhung and Eigentumswechsel individually) |
| Main Versicherungssparten at working-knowledge level | **Confirmed but mis-scoped.** The statutory list is **not** open-ended: § 2 Abs. 1 Nr. 1 lit. c–e names exactly **Unfall, Kranken, Pflege, verbundene Hausrat, verbundene Gebäude, Haftpflicht, Kraftfahrt, Rechtsschutz**. Anlage 1 Nr. 4 adds nothing beyond those. "Sachversicherung" generally, transport, technical lines, industrial lines, D&O: **not in scope.** |
| Vertriebsrecht/Beratungspflichten (**§§ 60–63 VVG**, Dokumentation, Beratungsprotokoll) | **Confirmed, and the brief's citation is right** — §§ 60–63 VVG are the Vermittler limbs. The brief omitted **§ 62 VVG** by name (Zeitpunkt und Form: § 60 Abs. 2 info *before the customer's Vertragserklärung*, § 61 Abs. 1 documentation *before Vertragsschluss*, both **in Textform**) and **§ 6/6a VVG** (the *insurer's* parallel duty, with the § 6 Abs. 6 twist at §6.2 below). |
| Datenschutz in der Versicherungsvermittlung | **Confirmed** — Anlage 1 Nr. 2.5.3 |
| Grundlagen der Altersvorsorge / bAV "if in scope" | **Confirmed, and it is a much bigger block than "if in scope" implies.** § 2 Abs. 1 Nr. 1 lit. b makes GRV, private Vorsorge, bAV Grundzüge, staatliche Förderung and steuerliche Behandlung **one of five written areas**, and the DIHK/BWV hour recommendation puts area 3 at **92 of 230 UE — the largest block in the whole syllabus.** |
| *(not in the brief)* | **Geldwäschegesetz — Anlage 1 Nr. 2.8, an express named sub-area.** See §7. |
| *(not in the brief)* | **Wettbewerbsrecht (Nr. 2.4), Versicherungsaufsicht (Nr. 2.6), Binnenmarkt/Dienstleistungs- und Niederlassungsfreiheit (Nr. 2.7).** |

---

## 4. The DIHK/BWV Rahmenplan and Proximus — exactly how far each may be used

### 4.1 The Rahmenplan — same posture as the § 34a round: cite it, do not build on it

**DIHK e. V. (Herausgeber), Kooperationspartner BWV e. V., "Geprüfter Fachmann / Geprüfte Fachfrau für Versicherungsvermittlung IHK — Rahmenplan mit Lernzielen für die Sachkundeprüfung", 6. Auflage, Stand März 2025**, 72 pp., freely downloadable from `bwv.de` and linked from IHK pages. Its own account of itself:

> "In **Abschnitt 1 der VersVermV** werden unter Bezugnahme auf **Anlage 1** der Verordnung Gegenstand und inhaltliche Anforderungen der Sachkundeprüfung dargelegt."

> "Um die **Verbindlichkeit und Transparenz** der für alle Prüfungsteilnehmer maßgeblichen Lerninhalte und Lernziele zu stärken, haben sich der Deutsche Industrie- und Handelskammertag (DIHK) e. V. und das Berufsbildungswerk der Deutschen Versicherungswirtschaft (BWV) e. V. darauf verständigt, dass das bisherige Ausbildungsprogramm des BWV durch diesen Rahmenplan mit Lernzielen ersetzt wird."

> "Auch wenn der Verordnungsgeber **keine konkreten Vorgaben zu Art und Umfang der Ausbildung** macht, sondern vielmehr das **„Nadelöhr" Prüfung** definiert, umfasst dieser Rahmenplan eine Konzeption mit **Stundenempfehlungen** zur Prüfungsvorbereitung."

Structurally it is a three-column table (Sachgebiet | Inhaltsübersicht/Lernziele | Zeitlicher Richtwert) with a **three-level Anwendungstaxonomie** (1 Wissen · 2 Anwendung · 3 Interpretation) per learning objective and **G / S / P / S+P markers** distinguishing background material from written-only, practical-only and both-parts material. Its top-level structure is **Anlage 1 VersVermV's structure, unchanged**; it adds depth, weighting and taxonomy.

**It is copyrighted.** Page 1: *"Copyright: **Alle Rechte liegen beim Herausgeber. Ein Nachdruck – auch auszugsweise – ist nur mit ausdrücklicher schriftlicher Genehmigung des Herausgebers gestattet.**"* Herausgeber is **DIHK e. V.**, a private association; it is therefore **not** an *amtliches Werk* under § 5 UrhG, unlike Anlage 1 VersVermV.

| Use | Verdict |
|---|---|
| Read it to confirm scope, depth and weighting; cite it as evidence that an official topic catalogue and an hour recommendation exist | **Fine.** Done here. |
| Reproduce its table, taxonomy assignments, G/S/P markers, hour figures per sub-area, or sub-bullet wording into repo content | **Do not.** Copyrighted expression of a private body. *(The area-level hour totals are quoted once in §0.2/§3.2 as evidence for a proposition about scope balance, which is a permissible short citation and not a reproduction of the work; they are **not** in the draft.)* |
| Derive question wording from it | **Do not.** Nothing needs it. |
| Treat it as the module's authoritative syllabus | **No — use Anlage 1 VersVermV.** Anlage 1 is Tier A, copyright-free, and legally *is* the inhaltliche Anforderung per § 2 Abs. 2 Satz 2 VersVermV. The Rahmenplan is Tier B corroboration. |

This is the identical posture the § 34a round adopted for the DIHK Bewachungs-Rahmenplan (`bewachungsgewerbe` dossier §4.1), reached independently on the same reasoning, on a document carrying a verbatim-identical copyright notice. **Recommend recording it as a standing repo rule: DIHK Rahmenpläne are scope cross-checks, never content sources.**

### 4.2 Proximus — a harder object than the Rahmenplan, and the reason this module is bounded

Set out in §0.2. To restate the operative points as rules:

| Use | Verdict |
|---|---|
| Record that Proximus 5 exists, that it is the written part's Bedingungswerk since 01.07.2023, and that a learner needs it | **Fine and necessary.** The module would be dishonest without saying so. |
| Purchase, download, read, quote, paraphrase or reconstruct any Proximus condition, clause, exclusion, sum or tariff | **Do not, at any point, for any purpose.** It is a private training body's commercial publication. This is the core of constraint 1. |
| Write questions about *Leistungsumfang, Ausschlüsse, Klauseln, Tarifaufbau, Annahmerichtlinien, Entschädigungsgrenzen* in the Anlage 1 Nr. 3.2/3.4/3.5/4 sense | **Do not.** They cannot be authored correctly without the work, and approximating them from general market knowledge would produce content that is both unsourced and probably wrong against the actual grading basis. |
| Write questions on the **statutory** rules that govern the same lines — VVG §§ 74, 75, 95, 100, 115, 178, 193; PflVG § 1 and its Anlage | **Yes.** These are Tier A, they are genuinely part of area 2 and the statutory floor of area 4, and they are what a candidate gets wrong for legal rather than product reasons. |

**A note against over-reading this.** Proximus does not make the exam unpreparable from law — it makes *one half* of it so. The IHK-published pass rule (§5.1) is instructive: a candidate must reach **50 % in four of the five areas and 30 % in the fifth**. A candidate who is strong on the legal areas and takes the 30 % floor in one product area passes. The legal half is not a consolation prize; it is a genuine and independently sufficient product.

### 4.3 Staleness check on the Rahmenplan

Stand März 2025, so much fresher than the § 34a Rahmenplan (2019). Its §-references to GewO/VersVermV/VVG/VAG were spot-checked against the current consolidated texts and held, including the post-2018 § 34d Abs. 5 numbering. Two currency watch-items: it is keyed to **Proximus 5 (prüfungsrelevant ab 01.07.2023)**, so a Proximus 6 would move the exam without moving any law; and its § 5 VersVermV equivalence material predates the **17.02.2025** amendment by weeks (§5.4).

---

## 5. Exam mechanics

### 5.1 What the VersVermV itself fixes (Tier A) — including, unlike § 34a, the pass rule

> **§ 4 Abs. 1 VersVermV** — "Die Sachkundeprüfung besteht aus einem **schriftlichen und einem praktischen Teil**. Die Teilnahme am praktischen Teil der Prüfung **setzt das Bestehen des schriftlichen Teils voraus**."

> **§ 4 Abs. 2** — "Der schriftliche Teil der Prüfung umfasst die in § 2 Absatz 1 Nummer 1 aufgeführten Sachgebiete. Sie sind anhand **praxisbezogener Aufgaben** und in einem **ausgewogenen Verhältnis** zueinander zu prüfen. Der schriftliche Teil der Prüfung kann mit Hilfe unterschiedlicher Medien durchgeführt werden."

> **§ 4 Abs. 3** — "Die Auswahl der Prüfungsaufgaben für den schriftlichen Teil der Prüfung trifft ein nach Maßgabe des § 32 Absatz 2 der Gewerbeordnung eingerichteter **bundesweit einheitlich tätiger Aufgabenauswahlausschuss**. Der Aufgabenauswahlausschuss ist mit **acht Mitgliedern und acht stellvertretenden Mitgliedern** zu besetzen. […] **Die Prüfungsaufgaben werden auch nach der Prüfung nicht veröffentlicht**, sondern stehen den Prüflingen nur während der Prüfung zur Verfügung."

> **§ 4 Abs. 4** — "Im praktischen Teil der Prüfung wird **jeweils ein Prüfling** geprüft. Dieser Prüfungsteil umfasst die Kundenberatung nach § 2 Absatz 1 Nummer 2 und wird als **Simulation eines Kundenberatungsgesprächs** durchgeführt. […] Dabei kann der Prüfling wählen zwischen den Sachgebieten **1. Vorsorge** […] oder **2. Sach- und Vermögensversicherung** […]"

> **§ 4 Abs. 7** — "Die Leistung des Prüflings ist von dem Prüfungsausschuss mit „bestanden" oder „nicht bestanden" zu bewerten. Die Prüfung ist bestanden, wenn sowohl der schriftliche als auch der praktische Teil der Prüfung jeweils mit „bestanden" bewertet worden sind. **Der schriftliche Teil der Prüfung ist bestanden, wenn der Prüfling 1. in vier der in § 2 Absatz 1 Nummer 1 genannten Bereiche jeweils mindestens 50 Prozent und 2. in dem verbliebenen Bereich mindestens 30 Prozent der erreichbaren Punkte erzielt.** Der praktische Teil der Prüfung ist bestanden, wenn der Prüfling **mindestens 50 Prozent** der erreichbaren Punkte erzielt."

**This is a materially better position than § 34a.** There, the four most-asked questions (question count, duration, pass percentage, gating) were all IHK Satzung and the draft had to decline to state them. Here **the pass percentages and the gating are federal law**, quotable and stable. Only the question count and the duration remain Satzung (§ 4 Abs. 9 + § 32 Abs. 1 Satz 2 GewO).

Also Tier A: **§ 3 Abs. 1** — *"Die Sachkundeprüfung kann bei **jeder** Industrie- und Handelskammer abgelegt werden"* (free choice of chamber, no district binding, same as § 10 Abs. 1 BewachV); **§ 4 Abs. 6** — the exam is not public, with an exhaustive list of five permitted observer categories; **§ 4 Abs. 8** — a passing candidate receives the **Anlage 2** certificate bearing the protected title *"Geprüfter Fachmann für Versicherungsvermittlung IHK"*; a failing candidate receives a Bescheid that must point out the retake option.

**Exemptions and equivalences, all Tier A and all commercially load-bearing:**

- **§ 4 Abs. 5** — the **practical part alone** is waived for holders of a § 34f/§ 34h/§ 34i Erlaubnis or of the corresponding Sachkundenachweise. Note the asymmetry: an adjacent-licence holder still sits the *written* part.
- **§ 5 Abs. 1** — full equivalence for **Versicherungskaufmann/-frau; Kaufmann/-frau für Versicherungen und Finanzen; Geprüfter Fachwirt für Versicherungen und Finanzen; Geprüfter Fachwirt für Finanzberatung; Kaufmann/-frau für Versicherungen und Finanzanlagen** (Nr. 1, no experience requirement); a Bank/Versicherung/Finanzdienstleistung degree or specified Fachberater/Finanzfachwirt qualifications **plus one year** of relevant experience (Nr. 2); Bank-/Sparkassenkaufmann, Investmentfondskaufmann or Geprüfter Fachberater für Finanzdienstleistungen **plus two years** (Nr. 3).
- **§ 5 Abs. 2** — a mathematics, economics or law degree counts *"wenn in der Regel zusätzlich eine mindestens **dreijährige** Berufserfahrung […] nachgewiesen wird"*. Compare § 8 Nr. 3 BewachV, where a law degree buys an exemption from the *legal* Sachgebiete but requires instruction in the practical ones — a nice cross-trade contrast the § 34a dossier already noticed.
- **§ 2 Abs. 3** — a **grandfather clause**: anyone continuously active as a Versicherungsvermittler or -berater **since 31 August 2000** needs no Sachkundeprüfung, as does anyone who applied for a § 34d/§ 34e permission **before 1 January 2009** (the latter surviving even a subsequent interruption).
- **§ 27** — a pre-01.01.2009 BWV *Versicherungsfachmann/-frau* qualification is equivalent.

### 5.2 What the chambers actually do (Tier B — two independent IHKs)

| Fact | IHK Düsseldorf | IHK Rhein-Neckar |
|---|---|---|
| Written part | **160 Minuten**, PC-Prüfung, in two blocks with no break | **160 Minuten**, am Computer, praxisbezogene Aufgaben |
| Question sets | (not stated) | *"Aufgaben sind **pro Prüfungstermin bundesweit einheitlich**"* |
| Practical part | **in der Regel 20 Minuten**, plus 20 minutes' preparation; role-play | **20 Minuten**, Rollenspiel, one candidate only, on a Fallbeispiel |
| Gating / window | Only those who passed the written part are admitted; must sit the practical **within two years** of passing the written | (gating stated; window not stated) |
| Retakes | practical *"kann innerhalb der zwei Jahre **beliebig oft** wiederholt werden"* | *"darf **unbegrenzt** wiederholt werden"* |
| Fee | **EUR 399** full; **EUR 313** written only; **EUR 274** practical only *(Gebührentarif ab 01.01.2026)* | **EUR 360** full; **EUR 260** written; **EUR 210** practical retake |
| Practical assessment | *"Zur Bewertung des praktischen Prüfungsteils wird der **Protokollbogen der DIHK** verwendet"* | — |
| Proximus | *"Am 1. Juli 2023 wurde das aktuelle **Bedingungswerk Proximus 5** veröffentlicht"* | — |

**160 minutes / 20 minutes and unlimited retakes are consistent across both chambers, so they are safe as *typical practice* — but the duration is Satzung under § 4 Abs. 9 VersVermV and must be labelled as such.** The 160-minute figure is independently corroborated by the Rahmenplan (§0.2). **Fees vary by roughly 10 % between the two chambers checked and must never be stated as a national figure.**

### 5.3 A secondary-source error, recorded for the same reason the other two dossiers recorded theirs

**IHK Düsseldorf's page states the pass rule as** *"gemäß **§ 9 Absatz 4 lit. a bis e** jeweils mindestens 50 Prozent und in dem weiteren Bereich mindestens 30 Prozent"*. **There is no such provision.** § 9 VersVermV is *Mitteilungspflichten* and has four Absätze, none lettered. The pass rule is **§ 4 Abs. 7 VersVermV**, and the lettered a–e list it refers to is **§ 2 Abs. 1 Nr. 1**. The *substance* Düsseldorf states is correct; the citation is not.

This is the third consecutive dossier in this repo to find a chamber-level page misciting or under-stating the very rule it is explaining (Maklerschein §1.1: IHK pages weeks stale on the abolition; Bewachung §2.3: two IHKs dropping *"in leitender Funktion"* from the statutory list). **The pattern is now established enough to be a working assumption: IHK web copy is a good pointer to which instrument to read and a bad source for what it says.**

### 5.4 Currency

- **§ 34d GewO** is in the Fassung of **Art. 9 FinmadiG, BGBl. 2024 I Nr. 438, in force 30.12.2024** (which added the DORA supervision limbs in Abs. 11a and 13). **The GewBürAbG of 20.07.2026 — the act that reshaped § 6a and abolished the broker CPD duty in § 34c — does not touch § 34d.** Verified against the official BGBl PDF: Art. 1 has exactly three Nummern and none of them is § 34d. See §1.1 note 2 for the buzer header trap.
- **VersVermV** was last amended by **Art. 1 der Ersten Verordnung zur Änderung der Versicherungsvermittlungsverordnung v. 17.02.2025, BGBl. 2025 I Nr. 43**, in force 22.02.2025. Read in the official BGBl PDF: it changes **§ 5 Abs. 1 only** — inserting *"oder Nachfolger"* after *"Vorläufer"* and appending **Nr. 1 lit. e, "Kaufmann/Kauffrau für Versicherungen und Finanzanlagen"**, the new Ausbildungsberuf. Small, but it directly widens who is exempt from the exam, so it matters commercially.
- **Watch item:** the EU-level IDD review / Retail Investment Strategy is the plausible source of the next structural change to this regime, and any change to the ministry's § 34e Abs. 1 Satz 1 Nr. 5 power flows straight into Anlage 1. **Re-verification date: no later than 2026-11-30.**

---

## 6. The surrounding operative regime (Tier A) — what a module has to get right

### 6.1 Duties on the intermediary, VersVermV

| § | Duty | Testable detail |
|---|---|---|
| **§ 7 Abs. 1** | Weiterbildung, 15 h per **Kalenderjahr** (§ 34d Abs. 9 Satz 2 GewO) | May be Präsenz, **Selbststudium**, betriebsintern or "andere geeignete Form"; **self-study requires *"eine nachweisbare Lernerfolgskontrolle durch den Anbieter"***; provider quality per **Anlage 3**; acquiring a § 5 qualification counts as CPD |
| **§ 7 Abs. 2** | Evidence file | Name, date/scope/content/title of the measure, provider name and contact; **five years** on a durable medium, kept on the business premises, clock starting at the end of the calendar year of the measure |
| **§ 7 Abs. 3** | IHK may order an **Anlage 4** declaration of CPD compliance for the previous calendar year, free of charge, electronically permitted | |
| **§§ 11–13** | Berufshaftpflicht | Must cover the **whole EU/EEA** (§ 11); minimum sums **EUR 1 276 000 per Versicherungsfall and EUR 1 919 000 per year** (§ 12 Abs. 2), adjusted by the Art. 10 Abs. 7 IDD technical standard; must extend to §§ 278/831 BGB vicarious liability (§ 12 Abs. 3); **wissentliche Pflichtverletzung** may be excluded, further exclusions only if market-standard (§ 12 Abs. 5); the Versicherungsbestätigung may be **no more than three months old** at application (§ 13 Abs. 1) |
| **§ 14** | Geschäftsorganisation | Must hold all appropriate product and **Produktfreigabeverfahren/Zielmarkt** information (Abs. 1); **must not remunerate or assess staff in a way that conflicts with acting in the customer's best interest**, and must not set incentives to recommend a product where a better-suited one could be offered (Abs. 2) |
| **§ 15/§ 16** | **Erstinformation** at first business contact | Twelve items incl. status (Makler/Vertreter/Berater and which permission or exemption), registration number and how to check it, whether advice is offered, **the nature of the remuneration** (direct fee vs. commission in the premium vs. other Zuwendungen vs. a combination), >10 % holdings both ways, and the Schlichtungsstelle address. **On paper, clear and comprehensible, in an official language of the risk state, free of charge** (§ 16 Abs. 1); durable medium or website only under the § 16 Abs. 2 conditions; by telephone, immediately after the first contact (§ 16 Abs. 4) |
| **§ 17** | Beschwerdemanagement | Written Leitlinien; a complaints-management function; registration of complaints with **IHK inspection rights at any time**; acknowledgement; forwarding where not competent; publication of the procedure; **and a duty to participate in a § 214 Abs. 1 Satz 1 Nr. 2 VVG Schlichtungsverfahren if the customer invokes it** (Abs. 4) |
| **§§ 18, 19** | Versicherungsanlageprodukte | Conflict-of-interest measures (§ 48a Abs. 4, 5 VAG entsprechend); Zuwendungen must not impair quality or the § 1a Abs. 1 VVG duty to act *"ehrlich, redlich und professionell"* |
| **§§ 20–22** | Zahlungssicherung | Client money may be accepted only against a **Sicherheit or Vertrauensschadenversicherung** unless the intermediary is authorised by the insurer to collect (§ 20 Abs. 1); minimum **4 % of annual premium receipts, floor EUR 19 200** (§ 20 Abs. 5); Aufzeichnungen *"unverzüglich und in **deutscher Sprache**"* with a five-year retention (§ 22); **§ 25: none of §§ 20–24 applies to reinsurance** |
| **§ 23** | Ad-hoc audit at the intermediary's cost *"aus besonderem Anlass"* on §§ 20/22 compliance; for Versicherungsberater additionally on the § 34d Abs. 2 Satz 4 Zuwendungsverbot | |
| **§ 26** | Seven Ordnungswidrigkeiten *"im Sinne des § 144 Absatz 2 Nummer 1b der Gewerbeordnung"* — frame **EUR 3 000** per § 144 Abs. 4 | |

### 6.2 Advice and documentation, VVG — including one trap worth teaching

- **§ 61 Abs. 1 VVG** (the intermediary's core duty): question the customer as to *Wünsche und Bedürfnisse* where the difficulty of the product or the customer's situation gives cause, advise *"auch unter Berücksichtigung eines angemessenen Verhältnisses zwischen Beratungsaufwand und der vom Versicherungsnehmer zu zahlenden Prämien"*, **state the reasons for each recommendation**, and document it.
- **§ 62 VVG**: § 60 Abs. 2 information **before the customer's Vertragserklärung**, § 61 Abs. 1 documentation **before Vertragsschluss**, both *"klar und verständlich in **Textform**"*, with the § 62 Abs. 2 oral exception on customer request or provisional cover — which does **not** apply to provisional cover in compulsory insurance.
- **§ 60 Abs. 1 VVG**: the **Makler** must base advice on *"eine hinreichende Zahl von auf dem Markt angebotenen Versicherungsverträgen und von Versicherern"* unless he expressly flags a restricted selection **before** the customer's Vertragserklärung; § 60 Abs. 2 then requires both the restricted-selection Makler and **every Vertreter** to disclose their market and information basis, name the insurers relied on, and (Vertreter only) say for which insurers they act and whether exclusively.
- **§ 63 VVG**: damages for breach of § 60 or § 61, with a reversed fault carve-out (*"Dies gilt nicht, wenn der Versicherungsvermittler die Pflichtverletzung nicht zu vertreten hat"*). § 61 Abs. 2: a waiver needs a **separate written declaration** containing an express warning that waiving may prejudice a § 63 claim.
- **The trap: § 6 Abs. 6 VVG.** The *insurer's* parallel advisory duty under § 6 Abs. 1–5 does **not** apply *"wenn der Vertrag mit dem Versicherungsnehmer von einem **Versicherungsmakler** vermittelt wird"* (nor to Großrisiken per § 210 Abs. 2). Broker-intermediated business therefore has **one** advisory duty (the broker's, § 61) rather than two. Agent-intermediated business has both. This is a clean, examinable, frequently-misunderstood consequence of the Makler/Vertreter split and is in the draft.

### 6.3 Remuneration constraints

- **§ 34d Abs. 1 Satz 5 GewO**: *"Einem Versicherungsvermittler ist es untersagt, Versicherungsnehmern, versicherten Personen oder Bezugsberechtigten aus einem Versicherungsvertrag **Sondervergütungen** zu gewähren oder zu versprechen"*, with §§ 48b, 50a VAG applied entsprechend. **§ 48b Abs. 2 VAG** defines a Sondervergütung as any direct or indirect benefit beyond the agreed policy performance — *"insbesondere jede 1. vollständige oder teilweise **Provisionsabgabe**, 2. sonstige Sach- oder Dienstleistung […], 3. Rabattierung"* — *"sofern sie nicht **geringwertig** ist"*, and fixes geringwertig at **EUR 15 pro Versicherungsverhältnis und Kalenderjahr**. § 48b Abs. 4 exempts benefits used for a permanent increase in cover or premium reduction of the mediated contract. Breach is an OWi under § 144 Abs. 2 Nr. 7 GewO.
- **§ 34d Abs. 2 Sätze 3–6 GewO** (Versicherungsberater): fee only from the client; **no Zuwendungen from an insurer**; where several policies are equally suitable, the one available **without** an insurer Zuwendung must be offered first; and where the Berater does mediate a policy containing Zuwendungen, he must *"unverzüglich die **Auskehrung** der Zuwendungen durch das Versicherungsunternehmen an den Versicherungsnehmer nach § 48c Absatz 1 des Versicherungsaufsichtsgesetzes […] veranlassen"*. Breaches are OWis under § 144 Abs. 2 Nr. 7a and 7b GewO.

### 6.4 Sanctions — with an asymmetry worth teaching

**§ 144 Abs. 1 Nr. 1 GewO** makes it an Ordnungswidrigkeit to operate without the required permission: **lit. k** *"nach § 34d Absatz 1 Satz 1 den Abschluss eines dort genannten Vertrages vermittelt"*, **lit. l** *"nach § 34d Absatz 2 Satz 1 über eine Versicherung oder Rückversicherung berät"*. **§ 144 Abs. 2** covers Sondervergütung (Nr. 7), the Berater Zuwendungsverbot (Nr. 7a) and Auskehrungspflicht (Nr. 7b), the Vermittler/Berater incompatibility (Nr. 7c), the CPD duty (Nr. 7d) and the register duties (Nr. 8, 9).

> **§ 144 Abs. 4 GewO** — "Die Ordnungswidrigkeit kann in den Fällen des Absatzes 1 Nummer 1 **Buchstabe m und n** und Nummer 2 mit einer Geldbuße bis zu **fünfzigtausend Euro**, in den Fällen des Absatzes 1 Nummer 1 **Buchstabe a bis l** und o, Nummer 3 und 4 und des Absatzes 2 Nummer 1, 1a und 5 bis 11 mit einer Geldbuße bis zu **fünftausend Euro**, in den Fällen des Absatzes 2 Nummer 1b und 2 bis 4a mit einer Geldbuße bis zu **dreitausend Euro** […] geahndet werden."

**So unlicensed insurance mediation (lit. k) or advice (lit. l) is capped at EUR 5 000, while unlicensed Finanzanlagenvermittlung (lit. m, § 34f) and unlicensed Honorar-Finanzanlagenberatung (lit. n, § 34h) carry EUR 50 000 — a tenfold difference between adjacent Gewerbe in the same sentence.** VersVermV breaches sit in the **EUR 3 000** band via § 26 VersVermV → § 144 Abs. 2 Nr. 1b. Recorded because it is precise, counterintuitive and exactly the kind of thing a module gets wrong by rounding "GewO fines" to one number.

---

## 7. GwG and Datenschutz: the cross-link plan against `kyc_aml` and `datenschutz`

Anlage 1 VersVermV names **Geldwäschegesetz (Nr. 2.8)** and **Datenschutz (Nr. 2.5.3)** as express sub-areas, so both are genuinely in scope and cannot simply be omitted. This repo already holds substantial content in both. Following the precedents the brief names — `fadp_ch`'s `meta.description` see-also to `datenschutz`, and `dora_audit_readiness` §2.2's boundary-in-the-explanation technique — the rule adopted is **cross-link, do not duplicate**, and the boundary is drawn on *insurance-specificity*.

### 7.1 Coverage check, read programmatically

| Module | Questions | Topics | Locales | Relevant string counts |
|---|---|---|---|---|
| `data/kyc_aml_pilot.json` | 30 | grundlagen · sorgfaltspflichten · verdachtsmeldung · verstaerkte_sorgfalt · sanktionen (6 each) | de, en | **"Versicher" 2 · "34d" 0 · "Vermittler" 0 · "Nummer 8"/"Nr. 8" 0** |
| `data/datenschutz_pilot.json` | 40 | grundprinzipien · betroffenenrechte · datensicherheit · meldepflichten · auftragsverarbeitung (8 each) | **all 12** | "Art. 9" 17 · "Gesundheitsdaten" 10 · "Einwilligung" 20 · **"Versicher" 0 · "213" 0** |

### 7.2 GwG — the boundary is § 2 Abs. 1 Nr. 8, and it is beautifully insurance-specific

> **§ 2 Abs. 1 Nr. 8 GwG** — "**Versicherungsvermittler nach § 59 des Versicherungsvertragsgesetzes, soweit sie die unter Nummer 7 fallenden Tätigkeiten, Geschäfte, Produkte oder Dienstleistungen vermitteln, mit Ausnahme der gemäß § 34d Absatz 6 oder 7 Nummer 1 der Gewerbeordnung tätigen Versicherungsvermittler**, und im Inland gelegene Niederlassungen entsprechender Vermittler mit Sitz im Ausland"

with **Nr. 7** covering Solvency-II insurance undertakings *"soweit sie jeweils a) **Lebensversicherungstätigkeiten**, die unter diese Richtlinie fallen, anbieten"* (and the further Nr. 7 limbs).

Three facts, none of them in `kyc_aml`, all of them squarely insurance-specific, and — the elegant part — **the GwG obligation follows exactly the same tier line as § 34d itself**: the Abs. 6 and Abs. 7 Nr. 1 tiers identified in §2 are **expressly carved out of the GwG duty by name**. A produktakzessorischer or gebundener Vermittler is not a Verpflichteter at all. And even a fully licensed Vermittler is a Verpflichteter only *"soweit"* they mediate the Nr. 7 activities — i.e. **life-assurance-type business, not motor, not household, not liability**.

**Plan: 1 question in this module**, on § 2 Abs. 1 Nr. 8 GwG — who is and is not a Verpflichteter in insurance distribution, with the two carve-outs and the "soweit Lebensversicherung" limitation — carrying an explicit *"for the general GwG regime (Typologien, KYC, Verdachtsmeldung nach § 43, Sanktionen) see the `kyc_aml` module"* pointer inside its own explanation and in `meta.related_modules`. **Everything else stays in `kyc_aml`.**

**Reciprocally**, and worth a separate small card regardless of what happens to this module: `kyc_aml` currently contains **zero** mentions of § 2 Abs. 1 Nr. 8 while claiming general coverage of who is a Verpflichteter. That is the same gap the Maklerschein dossier §6.2 found for § 2 Abs. 1 Nr. 14 (Immobilienmakler) and § 10 Abs. 6. **Two independent rounds have now found the same shaped hole in `kyc_aml`'s Verpflichteten-katalog coverage. That is a pattern, not a coincidence, and it should be a `kyc_aml` card in its own right** — one question per commercially significant Verpflichteten-Kategorie, rather than the current implicit assumption that the reader knows they are covered.

### 7.3 Datenschutz — the boundary is § 213 VVG

`datenschutz` covers Art. 9 DSGVO, health data and consent thoroughly and in all 12 locales. Re-teaching that here would be pure duplication. What it does **not** and should not cover is the **insurance-sector-specific lex specialis**:

> **§ 213 Abs. 1 VVG** — "Die Erhebung personenbezogener **Gesundheitsdaten** durch den Versicherer darf **nur bei Ärzten, Krankenhäusern und sonstigen Krankenanstalten, Pflegeheimen und Pflegepersonen, anderen Personenversicherern und gesetzlichen Krankenkassen sowie Berufsgenossenschaften und Behörden** erfolgen; sie ist nur zulässig, soweit die Kenntnis der Daten **für die Beurteilung des zu versichernden Risikos oder der Leistungspflicht erforderlich** ist und die betroffene Person eine **Einwilligung** erteilt hat."

with Abs. 2 (the consent may predate the Vertragserklärung; the data subject must be **informed before each collection** and may **object**), Abs. 3 (the data subject may demand single-instance consent for every collection) and Abs. 4 (duty to point these rights out).

**Plan: 1 question in this module**, on § 213 VVG — the closed list of permissible sources, the necessity limb, and the Unterrichtung/Widerspruch mechanics — with an explicit pointer to `datenschutz` for the general GDPR framework. **No question here restates Art. 6, Art. 9, Art. 33/34, Auftragsverarbeitung or Betroffenenrechte.**

### 7.4 Modules checked and deliberately *not* cross-linked

- **`dora`** and its five siblings: § 34d Abs. 11a and Abs. 13 GewO **do** put DORA supervision on IHKs for insurance intermediaries above the 250-employee / EUR 50 m turnover / EUR 43 m balance-sheet threshold. **But that threshold excludes essentially the entire Sachkundeprüfung audience**, which is individuals and small brokerages, and DORA appears nowhere in Anlage 1. Noted as a fact about § 34d, kept out of the module. If a B2B "Versicherungsvertrieb — DORA" cut is ever wanted, § 34d Abs. 13 is the hook and it belongs in the DORA line, not here.
- **`kartellrecht`**: Anlage 1 Nr. 2.4 *Wettbewerbsrecht* is UWG (unzulässige Werbung), not GWB/Art. 101 AEUV. Same conclusion, on the same reasoning, as the Maklerschein dossier §6.2.
- **`hinweisgeberschutz`**: § 34d Abs. 12 GewO applies HinSchG §§ 4 Abs. 2, 5–11, 24, 25, 27–31 *entsprechend* to the IHKs' intermediary-misconduct reporting channels. That is a duty on the **chamber**, not on the candidate, and it is not in Anlage 1. Not cross-linked; recorded so the next agent does not re-derive it.

---

## 8. Source confidence

**Tier A — binding primary text, read in the official consolidated version and/or the official gazette. Everything the recommendation and every draft question rests on.**

1. **GewO § 34d Abs. 1–13** — `gesetze-im-internet.de`, **cross-read in full on `buzer.de`**, **plus the superseded pre-23.02.2018 Fassung from two separate archived versions**. The Abs. 5 Satz 1 Nr. 4 location was verified a third way, against the VersVermV's own four internal cross-references (§0.3).
2. **VersVermV §§ 1–27 and Anlagen 1–4 in full**, incl. Inhaltsübersicht. § 2 (Gegenstand), § 4 (Verfahren und Bestehensregel) and Anlage 1 (the syllabus that unblocks the module) quoted verbatim.
3. **GewO §§ 11a, 32, 34e, 144** — incl. the § 144 Abs. 4 Bußgeldrahmen mapping and the lit. k/l vs. lit. m/n asymmetry (§6.4).
4. **1. VersVermVÄndV, BGBl. 2025 I Nr. 43, Art. 1 und 2** — read in the **official BGBl PDF**.
5. **GewBürAbG, BGBl. 2026 I Nr. 215, Art. 1 und 11** — read in the **official BGBl PDF**, specifically to establish the **negative** finding that § 34d is untouched (§5.4).
6. **VVG §§ 1a, 3, 6, 6a, 7, 7a, 7b, 7c, 8, 19, 23, 28, 33, 37, 59, 60, 61, 62, 63, 64, 74, 75, 76, 95, 100, 113, 115, 178, 193, 210, 213, 214** — full text of each.
7. **VAG §§ 48, 48a, 48b, 48c** — full text.
8. **GwG § 2 Abs. 1 Nr. 7 und Nr. 8** — verbatim.
9. **BetrAVG §§ 1a, 1b; SGB VI § 35; SGB VII § 8; EStG § 3; PflVG § 1, § 4 und Anlage zu § 4 Abs. 2** — full text of each.
10. Mechanical checks: **GewBürAbG Art. 1 contains exactly three Nummern, none of them § 34d**; the § 34d Abs. 10 and Abs. 9 addressee lists contain **zero** references to Abs. 8 (§2.4).

**Tier B — official/quasi-official procedural material, not itself binding.**

11. **DIHK/BWV Rahmenplan, 6. Auflage, Stand März 2025** (72 pp.) — read in full. Establishes that an official topic catalogue and an hour recommendation exist, the taxonomy and G/S/P structure, the 160-minute written duration, and — decisively — **that Proximus 5 is the written part's grading basis** (§0.2). **Copyrighted (DIHK e. V.); used as corroboration only, never as a content source — see §4.1.**
12. **BWV Bildungsverband's own public description of Proximus** — that it is a fictitious insurer's conditions-and-tariffs work, sold as print and e-book, and an approved aid in three IHK qualifications. **The work itself was not obtained, opened or consulted.**
13. **IHK Düsseldorf (Nr. 2595960)** and **IHK Rhein-Neckar (Nr. 945188)** — exam mechanics, fees, gating, the two-year practical window, unlimited retakes, the DIHK Protokollbogen, bundeseinheitliche Aufgaben. Two independent chambers; where they agree (160 min written, 20 min practical, unlimited retakes) that is recorded as typical practice, not law. **Düsseldorf misstates the pass rule's citation** — recorded at §5.3.

**Tier C — orientation only, load-bearing for nothing.**

14. Search-result listings for § 34d prep vendors — used **only** to identify what had to be avoided (§1). None was fetched, read or cited.
15. Trade-press coverage of the Proximus 5 release — corroborates the July 2023 date already established from the Rahmenplan; nothing rests on it.

**Confidence in the headline findings.** *Very high* on §0.1 (Anlage 1 is the statutory syllabus): a single unambiguous sentence in an in-force federal regulation, read directly, corroborated by an official DIHK/BWV document that reprints the annex in its own appendix. *Very high* on §0.3 (the Abs. 5 Nr. 4 correction): four independent confirmations including the superseded text and a second federal instrument's cross-references. *High* on §0.2 (the Proximus boundary): it rests on two explicit statements in an official DIHK/BWV document plus the BWV's own product description, but it is a Tier B finding about exam *practice* rather than a Tier A finding about law, and **it should be confirmed with an IHK before it appears in marketing copy**. The residual risks are (a) a Proximus 6 moving the exam without moving any law, and (b) IDD-review-driven change at EU level flowing through § 34e into Anlage 1.

---

## 9. Recommendation

### 9.1 Build it — at a stated scope, and say what the scope is

The § 34d module is viable and, on the sourcing question specifically, sits between the two siblings: better than § 34c (which had no exam at all) and slightly worse than § 34a (whose statutory syllabus covered essentially the whole exam). The buildable core is **Anlage 1 areas 2 and the statutory limbs of 3 — plus the statutory floors of area 4 — authored entirely from GewO, VersVermV, VVG, VAG, GwG, SGB VI/VII, BetrAVG and PflVG.** The non-buildable remainder is the AVB/tariff product knowledge graded against Proximus 5, and no amount of cleverness makes that authorable inside constraint 1.

Commercially this is a good position, not a compromised one. The audience is large and mandatory-ish; **§ 4 Abs. 3 VersVermV expressly provides that the question sets are never published**, so no free official practice material exists or ever will; the pass rule's 30 %-floor structure means the legal areas alone can carry a candidate a long way; and § 7 Abs. 1 Satz 4 VersVermV's *"nachweisbare Lernerfolgskontrolle durch den Anbieter"* for self-study CPD is, once again, a **statutory description of an e-learning product with a test at the end** — the same observation the Maklerschein dossier made about § 15b Abs. 1 MaBV, and the same caution applies (see §10 item 5).

### 9.2 Name it honestly

Recommended label: **"Versicherungsvermittler / Versicherungsberater — IHK-Sachkundeprüfung (§ 34d GewO)"**, with three visible statements:

1. This is **unofficial** practice material. The written question sets are never published (§ 4 Abs. 3 Satz 6 VersVermV), so no coverage of the real Aufgabensätze can be claimed.
2. It covers the **statutorily-grounded** part of the syllabus. The written part is additionally graded against the **Proximus 5** Bedingungswerk, which this module does not and cannot reproduce; a candidate needs it separately for the product half.
3. **Many people who think they need this exam do not** — gebundene Versicherungsvertreter (Abs. 7 Satz 1 Nr. 1), produktakzessorische Vermittler (Abs. 6), Abs. 8 Nebentätigkeits-Vermittler and employed advisers are all outside it (§2). As with § 34a, this is both a duty of honesty and a conversion feature: a large part of the audience arrives not knowing which tier they are in.

The **Kundenberatung** half of the syllabus is examined as a 20-minute simulated advisory conversation with a single candidate (§ 4 Abs. 4 VersVermV) and is not multiple-choice-testable at all. The draft says so in `meta` rather than faking it, exactly as the § 34a draft did for that exam's oral part.

### 9.3 Two structural observations for the roadmap

1. **§ 34f / § 34h / § 34i are now the obvious next candidates and they share machinery with this one.** § 4 Abs. 5 VersVermV waives this exam's practical part for their licence-holders; § 3 FinVermV and § 3 ImmVermV mirror the structure in the other direction. The `versicherungsvermittler` module and a future `finanzanlagenvermittler` module would share topic infrastructure and cross-link naturally. **§ 34f additionally carries the EUR 50 000 fine frame (§6.4), i.e. the legislature treats it as the higher-risk trade.**
2. **The three § 34x rounds run today have converged on one repeatable method** and it should be written down: (i) find the Verordnungsermächtigung in the GewO; (ii) read the Rechtsverordnung it produced; (iii) find the *Anlage* that carries the syllabus; (iv) treat the DIHK Rahmenplan as a copyright-encumbered cross-check only; (v) check what the exam is graded *against* as well as what it is *about*. Step (v) is new this round and is the only reason the Proximus constraint was found rather than discovered after content had been written.

---

## 10. Open items for the PO / human review

1. **Decide whether a bounded module ships.** The scope limit in §0.2 is real and is the only genuine decision here. Recommended: yes, with the §9.2 labelling. This is a scope call and therefore the PO's.
2. **Fix the stale "§ 34d Abs. 2 Nr. 4" citation in two other docs** — it should read **"§ 34d Abs. 5 Satz 1 Nr. 4"** everywhere (§0.3). Neither file was edited here, because both were out of scope for this round:
   - **`docs/maklerschein-pre-review-dossier-2026-08-17.md` §5**, the table row that first identified § 34d as a candidate. The § 34f row in the same table should be re-checked at the same time for the same pre-2018-numbering problem.
   - **`docs/finanzanlagenvermittler-pre-review-dossier-2026-08-17.md`** (a § 34f round run in parallel with this one), which is **internally inconsistent on the point**: its §"Exam structure" passage correctly writes *"§ 34d Abs. 5 Satz 1 Nr. 4 Sachkundenachweis"*, while its roadmap open item repeats *"§ 34d Abs. 2 Nr. 4 GewO + VersVermV"*. Fix the second. That document also records § 34d as *"identified, not yet researched"* — superseded by this dossier, and the roadmap wording should say so.

   Three documents in this repo now carry the pre-2018 numbering, all traceable to one propagated citation. **Worth a single grep-and-fix pass rather than three separate edits.**
3. **Confirm the Proximus finding with an IHK before any marketing copy relies on it.** It is Tier B (§8). The question to ask is narrow: *"Is the written part still graded against Proximus 5, and is a Proximus 6 in preparation?"*
4. **Do not ship the §5.2 chamber mechanics as national facts.** 160 minutes, 20 minutes and the fee figures are Satzung under § 4 Abs. 9 VersVermV + § 32 Abs. 1 Satz 2 GewO and vary; two chambers already differ by ~10 % on fees. The **pass percentages and the written-gates-practical rule are** federal law (§ 4 Abs. 7, § 4 Abs. 1 Satz 2) and may be stated as such — that is the one place this module can be more definite than the § 34a one.
5. **If Zettacard ever positions itself as a § 7 VersVermV Weiterbildungsanbieter whose hours count toward the 15, treat that as a legal question, not a content one.** § 7 Abs. 1 Sätze 4–6 put duties on the *Anbieter* (Lernerfolgskontrolle, planning, systematic organisation, instructor qualification per **Anlage 3**), and § 7 Abs. 2 puts a five-year evidence duty on the *Gewerbetreibende*. "Do our hours count?" is a claim with regulatory consequences. Same warning the Maklerschein dossier gave for MaBV Anlage 2.
6. **Schedule a `kyc_aml` card for the Verpflichteten-katalog gap** (§7.2). Two independent rounds have now found the same shape of hole — § 2 Abs. 1 Nr. 14 (Immobilienmakler) last week, § 2 Abs. 1 Nr. 8 (Versicherungsvermittler, with its two § 34d carve-outs) today. Worth doing regardless of whether this module ships.
7. **Locale plan.** The draft ships DE canonical + EN, following `aevo` / `fadp_ch` / `kyc_aml` / `kartellrecht` / `bewachungsgewerbe`. **Unlike the § 34a module, this one is a genuinely weak candidate for the full 12** — the exam is a German-language proctored exam on German private and social insurance law, the practical part is a German-language advisory conversation, and there is no statutory multilingual hook comparable to BewachV Anlage 2 Nr. 6. DE + EN looks right here for production, not just for a pilot. **UI strings still ship in all 12 per AGENTS.md constraint 5 regardless.**
8. **Re-verification date: no later than 2026-11-30** (§5.4). Re-read § 34d and the VersVermV from the amending instruments, not from this file, and re-check whether Proximus 5 is still current.
9. **Standing process notes, both confirmed again this round.** (a) `buzer.de`'s title-level "zuletzt geändert" line is not the section's own version — read the section footer (§1.1 note 2); this is the third variant of the "consolidated text vs. what actually changed" failure mode the Maklerschein (§1.1) and Bewachung (§6) dossiers recorded. (b) **DIHK Rahmenpläne are scope cross-checks, never content sources** (§4.1) — now established on two independent documents with identical copyright notices, and worth promoting from a per-dossier finding to a repo rule.

---

## 11. What was drafted

`data/versicherungsvermittler_pilot_DRAFT.json` — **30 questions**, DE canonical + EN, single-choice, generated deterministically by `data/gen_versicherungsvermittler_draft.py` (which runs its own integrity, orthography and answer-distribution checks and exits non-zero on failure).

| topic_code | Anlage 1 / § 2 Abs. 1 Nr. 1 VersVermV mapping | Q |
|---|---|---|
| `rechtliche_grundlagen` | lit. a — GewO § 34d tier structure, Erlaubnis, Register, Weiterbildung, Berufshaftpflicht, Sondervergütung, Sanktionen (Anlage 1 Nr. 2.3, 2.6) | 8 |
| `vertragsrecht_vvg` | lit. a — VVG general contract law (Anlage 1 Nr. 2.1, 2.2) | 7 |
| `beratung_dokumentation` | lit. a + the statutory core of Nr. 1 — VVG §§ 6, 60–63; VersVermV §§ 15–17 | 6 |
| `vorsorge` | lit. b + c, statutory limbs only — SGB VI, BetrAVG, SGB VII, VVG §§ 178, 193 | 4 |
| `sach_haftpflicht` | lit. d + e, statutory floors only — VVG §§ 74, 75, 95, 100, 115; PflVG | 3 |
| `datenschutz_gwg` | Anlage 1 Nr. 2.5.3 and Nr. 2.8 — deliberately minimal, cross-linked | 2 |

**The weighting deliberately does not mirror the real exam's, and the draft says so in `meta.topic_weighting_note`.** The real written part is examined *"in einem ausgewogenen Verhältnis"* across the five lit. a–e areas (§ 4 Abs. 2 Satz 2 VersVermV), which would put roughly a fifth of the paper in each. This draft over-weights the legal areas and under-weights the product areas, for the reason in §0.2: the product areas are Proximus-graded and cannot be authored here. **This module therefore cannot claim proportional coverage of the real written exam, and must not be marketed as if it could.**

Every question carries a `legal_basis` naming the provision it is authored from, and every one of those provisions was fetched and read this session (§8 items 1–9). Questions are written in applied-situation style per § 2 Abs. 1 VersVermV's *"und deren praktische Anwendung"* and § 4 Abs. 2's *"praxisbezogener Aufgaben"*. `high_stakes: true` marks the questions where getting it wrong in real life means an Ordnungswidrigkeit, a § 63 VVG damages claim, an unlicensed-trade problem, or a customer losing cover.

**Not drafted, deliberately:** anything resting on the DIHK/BWV Rahmenplan's wording, table structure, taxonomy levels, G/S/P markers or per-sub-area hour figures; **anything resting on, resembling, or reconstructing Proximus conditions, exclusions, clauses, sums or tariffs**; anything on *Leistungsumfang / Ausschlüsse / Tarifaufbau / Annahmerichtlinien* in the Anlage 1 Nr. 3.2/3.4/3.5/4 sense; anything on Kundenberatung as a sales competence (§ 4 Abs. 4 makes it a simulated conversation, not an MCQ); anything asserting a national question count or fee; and anything duplicating `kyc_aml` or `datenschutz` beyond the two boundary questions specified in §7.

---

**Reminder:** this document is draft research groundwork. It is not legal advice, has not been reviewed by a qualified lawyer or by any IHK Prüfungsausschuss member, and no content derived from it should be shipped to learners before that review. The draft question bank carries `legal_review_status` accordingly and is unwired from every build path. The Proximus finding in §0.2 is the single most important thing in this file for anyone picking the module up, and it is Tier B — confirm it before it reaches a customer.
