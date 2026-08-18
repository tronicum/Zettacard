# Finanzanlagenvermittler (§ 34f GewO) — IHK-Sachkundeprüfung "Geprüfter Finanzanlagenfachmann/-frau IHK" — pre-review dossier (2026-08-17)

**Status:** AI-prepared research groundwork only — **NOT legal advice**. Not reviewed by a lawyer, by BaFin, or by any IHK Prüfungsausschuss or Aufgabenauswahlausschuss member.

**Requested:** research § 34f GewO and the FinVermV, confirm the real syllabus areas, check whether the sourcing situation is solvable, and — *if and only if* it is — draft a first-round pilot question bank.

**Delivered:** this dossier **and** `data/finanzanlagenvermittler_pilot_DRAFT.json` (30 questions, DE canonical + EN) plus its deterministic generator `data/gen_finanzanlagenvermittler_draft.py`. **The sourcing blocker is solved, and solved more cleanly than for any other exam module this repo has attempted.** The syllabus is not a trade-body courtesy document: it is **Anlage 1 to the FinVermV**, a statutory annex, and § 1 Abs. 2 FinVermV makes it the binding content specification of the exam. Copyright-free under § 5 UrhG.

**Files touched:** this file, `data/finanzanlagenvermittler_pilot_DRAFT.json`, `data/gen_finanzanlagenvermittler_draft.py`. Nothing else. `data/build_modules.py`, `data/modules_manifest.json`, `app/data/modules.json` and `app/app.js` are untouched; no build was run; nothing was staged or committed. The `_DRAFT` filename suffix keeps the pilot out of the live build path by construction.

---

## 0. The findings, first, because three of them correct the task brief

### 0.1 The sourcing blocker is solved — by a statutory annex, not by a Rahmenplan

`docs/maklerschein-pre-review-dossier-2026-08-17.md` §5 identified § 34f as a genuine IHK-exam candidate on the strength of § 34f Abs. 2 Nr. 4 GewO alone. That was right, and the position is stronger than it looked:

| Question | Answer |
|---|---|
| Is there a real, statutory, pass/fail exam? | **Yes.** § 34f Abs. 2 Nr. 4 GewO makes an IHK-Prüfung a condition of the Erlaubnis; § 3 Abs. 7 FinVermV grades it "bestanden"/"nicht bestanden" with a 50 % threshold per examined area. |
| Is the exam's subject matter fixed by a legal instrument? | **Yes, twice over.** § 1 Abs. 1 FinVermV names the Gebiete; § 1 Abs. 2 FinVermV: *"Die Einzelheiten der inhaltlichen Anforderungen an die Sachkundeprüfung bestimmen sich nach der **Anlage 1**."* Anlage 1 is a five-area, three-level syllabus running to ~90 numbered items. |
| Is that syllabus copyright-encumbered? | **No.** It is an annex to a Rechtsverordnung — an *amtliches Werk* under § 5 UrhG. Reproducing and authoring against it raises none of AGENTS.md constraint 1's concerns; it is the opposite of a vendor catalogue. |
| Is there an official public **question** catalogue? | **No — and the statute says so.** § 3 Abs. 3 Satz 7 FinVermV: *"Die Prüfungsaufgaben werden nach der Prüfung **nicht veröffentlicht**; sie stehen den Prüflingen nur während der Prüfungen zur Verfügung."* |
| Are the question sets regional? | **No.** § 3 Abs. 3 Satz 1 FinVermV: selection is made by *"ein nach Maßgabe des § 32 Absatz 2 der Gewerbeordnung eingerichteter **bundesweit einheitlich tätiger Aufgabenauswahlausschuss**"* — seven members, composition fixed by Satz 4. |

Compare the two nearest precedents in this repo. `aevo_pilot.json`'s own meta concedes *"There is no official public AEVO question catalogue"* and builds from AEVO + BBiG + a BIBB Rahmenplan. `bewachungsgewerbe_pilot_DRAFT.json` (this round's sibling) rests on § 9 Abs. 2 BewachV pointing at § 7 + Anlage 2 BewachV. **§ 34f is the strongest of the three**: the syllabus annex is more granular than BewachV Anlage 2, and the non-publication of questions is stated *in the regulation itself* rather than inferred from IHK practice. If `aevo` cleared the bar, § 34f clears it by a wide margin.

### 0.2 The scope split is real and high-value — but it is **not** in Abs. 5, and it is **three**-way, not two-way

The task brief states: *"the Abs. 5 scope split — § 34f Vermittler deal specifically in Anlage 2 Abs. 1 Nr. 1 (offene/geschlossene Investmentvermögen) vs Nr. 2 (Vermögensanlagen i.S.d. VermAnlG)"*. **Three errors in one sentence**, all corrected in §3 below:

1. **Wrong provision.** § 34f **Abs. 5** GewO is the *Registrierungspflicht* in the Vermittlerregister nach § 11a Abs. 1 GewO. It is *related* to the scope split — the entry must be made *"entsprechend dem Umfang der Erlaubnis"*, and § 6 Nr. 4 FinVermV makes *"der Umfang der Erlaubnis nach § 34f Absatz 1 Satz 1 Nummer 1 bis 3"* a stored register field — but it does not create the split.
2. **Wrong count and wrong grouping.** The split is created by **§ 34f Abs. 1 Satz 1 Nr. 1, 2 und 3** in combination with **§ 34f Abs. 1 Satz 3**, and it is **three-way**: Nr. 1 = *offene* Investmentvermögen, Nr. 2 = *geschlossene* Investmentvermögen, Nr. 3 = Vermögensanlagen i. S. d. § 1 Abs. 2 VermAnlG. Offene and geschlossene Investmentvermögen are **separate categories**, not one bundled category.
3. **"Anlage 2"** in the brief appears to be a slip for the GewO paragraph itself; FinVermV **Anlage 2** is the *Bescheinigung* template — which, usefully, spells the three-way split out in its own title (§3.1).

**The brief was also wrong about the documentation duties.** It refers to *"§ 34f Abs. 5/6 GewO's Beratungsprotokoll-style duties"*. § 34f Abs. 5 and Abs. 6 GewO are both **register duties** (Abs. 5 the Gewerbetreibender's own entry, Abs. 6 the entry of directly-involved staff). The advice-documentation duties live in the FinVermV — §§ 16, 18, 18a, 22, 23 — and the **Beratungsprotokoll no longer exists**: it was replaced by the **Geeignetheitserklärung** (§ 18 FinVermV) with effect from 1 August 2020. Shipping "Beratungsprotokoll" in learner-facing copy would teach a six-year-dead instrument.

### 0.3 "Anlegerpsychologie" is **not** in the statutory syllabus — verified mechanically, not assumed

The brief asks for *"Grundlagen der Anlegerpsychologie/Risikoaufklärung if genuinely part of the statutory syllabus (verify, don't assume)"*. Verified over the retrieved text of Anlage 1 FinVermV:

> **"Anlegerpsychologie": 0 occurrences. "Psychologie": 0. "Risikoaufklärung": 0. "Behavioral": 0.**

What *is* there is (a) **Anlage 1 Nr. 1 Kundenberatung** — a behaviour-and-process area (Serviceerwartungen, Besuchsvorbereitung, Kundengespräch, Erstellung eines Kundenprofils, Kundenbedarf und anlegergerechte Lösungen, Gesprächsführung und Systematik, Kundenbetreuung), which is a *sales-conversation* syllabus, not a psychology syllabus; and (b) **"Chancen, Risiken und Haftung"** as a recurring sub-area of each of the three product categories (Anlage 1 Nr. 3.4, 4.3, 5.2), which is *product* risk, backed by the hard information duty in § 13 FinVermV. **The draft therefore contains no "investor psychology" content.** Anything of that flavour in a competitor product is that vendor's own addition, not the statutory syllabus.

---

## 1. Method and instruments read

All retrieval **2026-08-17**. `WebFetch` is `ROBOTS_DISALLOWED` on `gesetze-im-internet.de` in this sandbox; every German statutory text below was fetched by direct `curl` against `gesetze-im-internet.de` and parsed from raw HTML, so the quotes are from the consolidated official text and not from a summary. Load-bearing provisions were cross-read on `buzer.de`.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **GewO § 34f** (Finanzanlagenvermittler) | `gesetze-im-internet.de/gewo/__34f.html`; cross-read `buzer.de/34f_GewO.htm` | **Abs. 1–6 in full**, twice, independently |
| **GewO § 34h** (Honorar-Finanzanlagenberater) | `gesetze-im-internet.de/gewo/__34h.html` | Abs. 1–3 in full |
| **GewO § 34g** (Verordnungsermächtigung) | same | Abs. 1 Satz 1–2, Abs. 2 Nr. 1–7 |
| **GewO § 11a** (Vermittlerregister) | same | Abs. 1, 2, 3a, 5, 7, 8 |
| **GewO § 32** (Sachkundeprüfungen, Aufgabenauswahlausschüsse) | same | Abs. 2 |
| **GewO § 144** (Ordnungswidrigkeiten) | same | Abs. 1 Nr. 1 lit. m/n, Abs. 2 Nr. 5, 6, 8, 9, **Abs. 4** (Bußgeldrahmen) |
| **FinVermV** (Verordnung über die Finanzanlagenvermittlung, V. v. 02.05.2012 BGBl. I S. 1006, zuletzt geänd. Art. 9 V. v. 11.12.2024 BGBl. 2024 I Nr. 411) | `gesetze-im-internet.de/finvermv/` — **note the short slug `finvermv`**; `finvermv_2012` and the `BJNR…` Gesamtausgabe pattern both 404 | **Inhaltsübersicht, §§ 1, 2, 3, 4, 6, 7, 9, 11, 11a, 12, 12a, 13, 14, 15, 16, 17, 18, 18a, 19, 20, 22, 23, 24, 26 in full**, plus **Anlage 1 in full** |
| **FinVermV Anlage 1** (zu § 1 Abs. 2) — *Inhaltliche Anforderungen an die Sachkundeprüfung*, Fundstelle BGBl. I 2012, 1015–1017 | `gesetze-im-internet.de/finvermv/anlage_1.html` | **complete, all five areas, all three levels** — reproduced at §2.2 |
| **VermAnlG** §§ 1, 2a, 13 | `gesetze-im-internet.de/vermanlg/` | § 1 Abs. 1–3, § 2a Abs. 1–5, § 13 Abs. 1–3 |
| **KAGB** § 1 | `gesetze-im-internet.de/kagb/__1.html` | Abs. 4, 5, 6 |
| **KWG** § 2 | `gesetze-im-internet.de/kredwg/__2.html` | **Abs. 6 Satz 1 Nr. 8** — the Bereichsausnahme § 34f Abs. 1 Satz 1 keys off |
| **GwG** §§ 1, 2 | `gesetze-im-internet.de/gwg_2017/` | § 2 Abs. 1 Nr. 1–16 in full; **§ 1 Abs. 24** (Finanzunternehmen) — the decisive provision, §5 |
| **GwG, full consolidated text** | `gesetze-im-internet.de/gwg_2017/BJNR182210017.html` (476 KB) | **mechanical whole-Act string counts** — see §5.1 |
| **HGB** §§ 171, 172 | `gesetze-im-internet.de/hgb/` | full text of each |
| **DIHK, "Geprüfter Finanzanlagenfachmann IHK / Geprüfte Finanzanlagenfachfrau IHK — Rahmenplan", Stand Oktober 2023** | `dihk.de/resource/blob/32540/…/recht-rahmenplan-gepruefte-finanzanlagenfachleute-2023-data.pdf` | **copyright notice and top-level headings only** — see §4 |
| **IHK "Wichtige Hinweise zur Sachkundeprüfung Finanzanlagenfachmann"** | `ihk.de/blueprint/servlet/resource/blob/6335480/…/hinweise-zur-pruefung-data.pdf` | exam mechanics: durations, thresholds, category coupling |
| **IHK München und Oberbayern, Merkblatt "Berufspflichten §§ 34f/34h GewO"** | `ihk-muenchen.de/ihk/documents/…/merkblatt_34fh_berufspflichten.pdf` | duty list, retention period, audit deadline |

**Deliberately not opened, not read, not cited for anything:** the exam-prep vendor sites that appear in the search results for this topic, including the `prüfungsfragen.biz` "Prüfungsfragen IHK-Sachkundeprüfung §34d, §34f, §34i GewO" product page that surfaced as the eighth hit on the very first search. AGENTS.md constraint 1 bans third-party exam-prep companies' text outright, and unlike the sign-icon carve-out there is no visual-accuracy exception that could apply to a question bank. Nothing in this dossier or in the draft derives from any of them, directly or indirectly.

### 1.1 Retrieval notes for the next agent

- The FinVermV slug on `gesetze-im-internet.de` is **`finvermv`** — not `finvermv_2012`, not `finanzanlagenvermittlungsverordnung`. The `BJNR…` Gesamtausgabe URL pattern used for other instruments **404s** here; use the `/finvermv/` index plus `__N.html` Einzelnorm pages. **Anlage 1 is at `/finvermv/anlage_1.html`**, not under a § number.
- Several Einzelnorm pages (`__14.html`, `__34h.html` on the GewO) are served in a markup variant that defeats the `<div class="jnhtml">…</div></div>` extraction regex the Maklerschein/Bewachungsgewerbe rounds used; they return **empty output rather than an error**. Falling back to a plain tag-strip recovers them. An empty parse from `gesetze-im-internet.de` should be treated as a **parser failure, never as an empty provision**.
- Several `ihk.de` regional sub-pages return **HTTP 403** to `WebFetch` while their linked PDFs on the same host fetch fine. Go for the PDF.

---

## 2. The exam: what it is, and what the law fixes about it (Tier A)

### 2.1 The chain of authority

**§ 34f Abs. 2 Nr. 4 GewO** creates the requirement; **§ 34g Abs. 2 Nr. 3 GewO** empowers the FinVermV to set *"die Inhalte und das Verfahren für die Sachkundeprüfung nach § 34f Absatz 2 Nummer 4"*; **§ 1 FinVermV** sets the content; **Anlage 1 FinVermV** sets the detail; **§ 3 FinVermV** sets the procedure.

> **§ 34f Abs. 2 GewO** — "Die Erlaubnis **ist zu versagen**, wenn […] **4.** der Antragsteller nicht durch eine **vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung** nachweist, dass er die für die Vermittlung von und Beratung über Finanzanlagen im Sinne des Absatzes 1 Satz 1 notwendige **Sachkunde über die fachlichen und rechtlichen Grundlagen sowie über die Kundenberatung** besitzt; **die Sachkunde ist dabei im Umfang der beantragten Erlaubnis nachzuweisen**."

The other three refusal grounds, for completeness and because the draft tests the contrast with § 34c: **Nr. 1** Zuverlässigkeit (same 5-year conviction catalogue as § 34a/§ 34c, Geldwäsche included), **Nr. 2** ungeordnete Vermögensverhältnisse, **Nr. 3** Nachweis einer **Berufshaftpflichtversicherung**. Unlike § 34c — where the Berufshaftpflicht limb applies only to Wohnimmobilienverwalter (`docs/maklerschein-pre-review-dossier-2026-08-17.md` §2.2) — **here it applies to every applicant**, and § 9 Abs. 2 FinVermV fixes the minimum sums at **1 276 000 EUR je Versicherungsfall / 1 919 000 EUR für alle Versicherungsfälle eines Jahres, expressly *"unabhängig vom Umfang der Erlaubnis"***.

The staff limb:

> **§ 34f Abs. 4 Satz 1 GewO** — "Gewerbetreibende nach Absatz 1 dürfen direkt bei der Beratung und Vermittlung mitwirkende Personen **nur beschäftigen, wenn sie sicherstellen, dass diese Personen über einen Sachkundenachweis nach Absatz 2 Nummer 4 verfügen** und geprüft haben, ob sie zuverlässig sind."

**This is the commercially decisive sentence for module sizing.** Unlike § 34a — where the rank-and-file Wachperson needs only an attendance-based *Unterrichtung* and the exam is confined to the owner plus five listed elevated activities (`docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md` §2.2/2.3) — **§ 34f has no base tier.** Every person directly involved in advice or intermediation needs the *same* Sachkundenachweis as the licence holder. The addressable population is the whole distribution force, not just principals.

### 2.2 Anlage 1 FinVermV — the statutory syllabus, top two levels

Reproduced from the official consolidation. German statutory text is an *amtliches Werk* under § 5 UrhG and carries no copyright.

> **Anlage 1 (zu § 1 Absatz 2) — Inhaltliche Anforderungen an die Sachkundeprüfung**
> **1. Kundenberatung** — 1.1 Serviceerwartungen des Kunden · 1.2 Besuchsvorbereitung/Kundenkontakte · 1.3 Kundengespräch (1.3.1 Kundensituation · 1.3.2 Erstellung eines Kundenprofils · 1.3.3 Kundenbedarf und anlegergerechte Lösungen · 1.3.4 Gesprächsführung und Systematik) · 1.4 Kundenbetreuung
> **2. Kenntnisse für Beratung und Vertrieb von Finanzanlageprodukten** — 2.1 Wirtschaftliche Grundlagen · 2.2 Grundlagen über Finanzinstrumente und Kategorien von Finanzanlagen (2.2.1 Geldanlageformen · 2.2.2 Nichtbörsennotierte Finanzanlageprodukte · 2.2.3 Börsennotierte Finanzanlageprodukte · **2.2.4 Nachhaltigkeitskriterien für Finanzanlageprodukte**) · 2.3 Allgemeine rechtliche Grundlagen (2.3.1 Vertragsrecht · 2.3.2 Geschäftsfähigkeit) · **2.4 Rechtliche Grundlagen für Finanzanlagenberatung und -vermittlung sowie Honorar-Finanzanlagenberatung** (2.4.1 Wertpapierhandelsgesetz · **2.4.2 Finanzanlagenvermittlungsverordnung**, broken out into 2.4.2.1 Statusbezogene Informationspflichten · 2.4.2.2 Einholung von Informationen über den Kunden · 2.4.2.3 Pflicht zur Empfehlung geeigneter Finanzanlagen · 2.4.2.4 Offenlegung von Zuwendungen · 2.4.2.5 Kurzinformationsblatt · 2.4.2.6 Informationen über Risiken, Kosten, Nebenkosten · 2.4.2.7 Anfertigung einer Geeignetheitserklärung · 2.4.2.8 Vermeidung, Regelung und Offenlegung von Interessenkonflikten, Vergütung · 2.4.2.9 Aufzeichnung telefonischer Vermittlungs- und Beratungsgespräche und sonstiger elektronischer Kommunikation · 2.4.3 Kreditwesengesetz · **2.4.4 Geldwäschegesetz** · 2.4.5 Finanzmarktrichtlinie) · 2.5 Vermittlerrecht (2.5.1 Rechtsstellung · 2.5.2 Berufsvereinigungen/Berufsverbände · 2.5.3 Arbeitnehmervertretungen) · 2.6 Wettbewerbsrecht (2.6.1 Allgemeine Wettbewerbsgrundsätze · 2.6.2 Unzulässige Werbung) · 2.7 Verbraucherschutz (2.7.1 Grundlagen des Verbraucherschutzes · 2.7.2 Schlichtungsstellen · **2.7.3 Datenschutz**)
> **3. Offene Investmentvermögen** — 3.1 Märkte für Finanzanlagen (Geld-/Renten-/Aktienmarkt) · 3.2 Konzept offener Fonds · 3.3 Fondsarten (17 named types, incl. ETFs, Publikumsinvestmentvermögen, Spezial-AIF, Anteilsklassen) · **3.4 Chancen, Risiken und Haftung** · 3.5 Kapitalanlagegesetzbuch · 3.6 Steuerliche Behandlung · 3.7 Depotkonten · 3.8 Staatliche Förderung · 3.9 Anlageprogramme · 3.10 Rating und Ranking
> **4. Geschlossene Investmentvermögen** — 4.1 Vertragsbeziehungen, Funktionsweise und Struktur · 4.2 Arten (Immobilien-, Projektentwicklungs-, Medien-, Schiffs-, Container-, Private-Equity-, Flugzeug-, Leasing-, Policen-, Umwelt-, Infrastruktur-/Blind-Pool-/Zweitmarktfonds) · **4.3 Chancen, Risiken und Haftung** · 4.4 Fachbegriffe · 4.5 Rechtliche Grundlagen (KAGB, BGB, HGB, **Kommanditgesellschaft**, GmbHG) · 4.6 Steuerliche Behandlung · 4.7 Auflösung stiller Reserven
> **5. Vermögensanlagen im Sinne des § 1 Absatz 2 des Vermögensanlagengesetzes** — 5.1 Anlageformen (5.1.1 Genussrechte · 5.1.2 Stille Beteiligungen · 5.1.3 Namensschuldverschreibungen · 5.1.4 Genossenschaftsanteile · 5.1.5 Weitere Vermögensanlagen) · **5.2 Chancen, Risiken und Haftung** · 5.3 Fachbegriffe · 5.4 Rechtliche Grundlagen (VermAnlG, BGB, HGB, GmbHG, GenG) · 5.5 Steuerliche Behandlung

**Areas 3, 4 and 5 map exactly onto § 34f Abs. 1 Satz 1 Nr. 1, 2 and 3.** Areas 1 and 2 are the shared base every candidate takes regardless of scope. The draft's five topics are this list, 1:1 — the same discipline `bewachungsgewerbe_pilot_DRAFT.json` applies to § 7 BewachV.

### 2.3 A currency defect in Anlage 1 itself, worth recording

Anlage 1's Fundstelle is **BGBl. I 2012, 1015–1017**, and area 5.1 enumerates only *Genussrechte, stille Beteiligungen, Namensschuldverschreibungen, Genossenschaftsanteile* and a catch-all *"weitere Vermögensanlagen"*. But § 1 Abs. 2 VermAnlG has since grown to **eight** numbered categories, and the two that dominate today's market — **partiarische Darlehen (Nr. 3)** and **Nachrangdarlehen (Nr. 4)** — were inserted by the Kleinanlegerschutzgesetz in 2015, *three years after Anlage 1 was drafted*. **"Nachrangdarlehen" appears 0 times in Anlage 1.** They are examinable via 5.1.5 and via the express reference in the area heading to *"§ 1 Absatz 2 des Vermögensanlagengesetzes"*, but a module that transcribed Anlage 1's 5.1 list literally would miss them. The draft therefore anchors area 5 on **§ 1 Abs. 2 VermAnlG's current eight-item list**, not on Anlage 1's frozen five. Same failure mode the Maklerschein dossier flagged for MaBV Anlage 1's "Energieeinsparverordnung" (§4.2 there): a statutory syllabus annex is authoritative on *scope*, not automatically current on *substance*.

### 2.4 Exam procedure — what § 3 FinVermV fixes, and what it leaves to the IHKs

Fixed by federal law (Tier A):

| Point | Provision |
|---|---|
| Two parts: written + practical; **the practical part may only be sat after passing the written part** | § 3 Abs. 1 |
| Written part covers the § 1 Abs. 1 Nr. 1 areas, *"anhand praxisbezogener Aufgaben und in einem ausgewogenen Verhältnis zueinander"* | § 3 Abs. 2 Satz 1–2 |
| Written part may be sat by any medium | § 3 Abs. 2 Satz 3 |
| Practical part = **Simulation eines Kundenberatungsgesprächs**, one candidate at a time | § 3 Abs. 4 |
| Practical part **falls away entirely** in three cases (§3.3 below) | § 3 Abs. 5 |
| Grading is **bestanden/nicht bestanden** only; pass requires **≥ 50 % of attainable points in each examined written area *and* ≥ 50 % in the practical part** | § 3 Abs. 7 |
| The exam is **not public**, with five categories of permitted observers who may not intervene | § 3 Abs. 6 |
| The exam may be sat at **any IHK that offers it** — no district binding | § 2 Abs. 1 |
| The IHK issues a Bescheinigung nach **Anlage 2**, **stating which of the three areas the written part covered** | § 3 Abs. 8 Satz 1–2 |
| Federal, non-public question selection by a 7-member Aufgabenauswahlausschuss | § 3 Abs. 3 |

**Deliberately left to Kammer-Satzung** by § 3 Abs. 9 i. V. m. § 32 Abs. 1 Satz 2 GewO: number of questions, duration, question format, fees, retake mechanics. One IHK information sheet (Tier B) gives **165 minutes maximum for all categories — Basisteil 30 min plus 45 min per category, including a 20-minute break — and ca. 20 minutes for the role-play**. That is typical Kammer practice, **not** federal law, and the draft's `exam_format_note` says so explicitly.

**The draft invents no pass rule.** It records § 3 Abs. 7's 50 %-per-area rule as the statutory one, and stops there.

---

## 3. The scope split, stated precisely — the single highest-value finding

### 3.1 The three categories and the restriction power

> **§ 34f Abs. 1 Satz 1 GewO** — "Wer im Umfang der Bereichsausnahmen des § 2 Absatz 6 Satz 1 Nummer 8 des Kreditwesengesetzes oder des § 3 Absatz 1 Satz 1 Nummer 11 des Wertpapierinstitutsgesetzes gewerbsmäßig zu
> **1.** Anteilen oder Aktien an inländischen **offenen** Investmentvermögen, offenen EU-Investmentvermögen oder ausländischen offenen Investmentvermögen, die nach dem Kapitalanlagegesetzbuch vertrieben werden dürfen,
> **2.** Anteilen oder Aktien an inländischen **geschlossenen** Investmentvermögen, geschlossenen EU-Investmentvermögen oder ausländischen geschlossenen Investmentvermögen, die nach dem Kapitalanlagegesetzbuch vertrieben werden dürfen,
> **3.** **Vermögensanlagen im Sinne des § 1 Absatz 2 des Vermögensanlagengesetzes**
> Anlagevermittlung im Sinne des § 1 Absatz 1a Nummer 1 des Kreditwesengesetzes […] oder Anlageberatung im Sinne des § 1 Absatz 1a Nummer 1a des Kreditwesengesetzes […] erbringen will (**Finanzanlagenvermittler**), bedarf der Erlaubnis der zuständigen Behörde."

> **§ 34f Abs. 1 Satz 3 GewO** — "Die Erlaubnis nach Satz 1 **kann auf die Anlageberatung zu und die Vermittlung von Verträgen über den Erwerb von einzelnen Kategorien von Finanzanlagen nach Nummer 1, 2 oder 3 beschränkt werden**."

> **§ 34f Abs. 2 Nr. 4 Halbsatz 2 GewO** — "**die Sachkunde ist dabei im Umfang der beantragten Erlaubnis nachzuweisen**."

The categories are anchored in the KAGB: **offen** = OGAW plus AIF satisfying Art. 1 Abs. 2 der Delegierten Verordnung (EU) Nr. 694/2014 (**§ 1 Abs. 4 KAGB**); **geschlossen** is defined purely negatively — **§ 1 Abs. 5 KAGB**: *"Geschlossene AIF sind alle AIF, die keine offenen AIF sind."*

**And the split is written into the certificate itself.** FinVermV **Anlage 2**'s own title reads: *"Bescheinigung über die erfolgreiche Ablegung der Sachkundeprüfung „Geprüfter Finanzanlagenfachmann/Geprüfte Finanzanlagenfachfrau IHK" nach § 34f Absatz 2 Nummer 4 […] in Verbindung mit § 34f Absatz 1 Satz 1 **Nummer 1** der Gewerbeordnung (**offene Investmentvermögen**)/ § 34f Absatz 1 Satz 1 **Nummer 2** der Gewerbeordnung (**geschlossene Investmentvermögen**)/ § 34f Absatz 1 Satz 1 **Nummer 3** der Gewerbeordnung (**Vermögensanlagen im Sinne des § 1 Absatz 2 des Vermögensanlagengesetzes**)"*.

### 3.2 The asymmetric coupling — the part practitioners get wrong

The three categories are **not** freely combinable. **§ 3 Abs. 2 Satz 5–7 FinVermV**:

> "Der schriftliche Teil der Prüfung **kann auf Antrag des Prüflings** auf die einzelnen Kategorien von Finanzanlagen nach Satz 4 Nummer 1, 2 oder Nummer 3 **beschränkt werden**. In diesem Fall muss der schriftliche Teil der Prüfung diejenigen in Satz 4 Nummer 1, 2 oder Nummer 3 genannten Bereiche umfassen, für die eine Erlaubnis nach § 34f Absatz 1 Satz 1 Nummer 1, 2 oder Nummer 3 in Verbindung mit Satz 3 […] beantragt wird. **Für eine Erlaubnis nach § 34f Absatz 1 Satz 1 Nummer 3 in Verbindung mit Satz 3 […] muss der schriftliche Teil der Prüfung zusätzlich die in Satz 4 Nummer 2 genannten Bereiche umfassen.**"

**Stated as a rule:** a candidate may sit the written part for **Nr. 1 alone**, or for **Nr. 2 alone**, but **never for Nr. 3 alone** — an application for a **Nr. 3 (Vermögensanlagen)** licence forces the written part to cover the **Nr. 2 (geschlossene Investmentvermögen)** areas as well. The coupling runs **one way only**: Nr. 2 does *not* drag in Nr. 3.

Independently corroborated in IHK candidate information (Tier B), which states of the three written categories: *"Kategorie 3: **Nur in Verbindung mit Kategorie 2 möglich!**"* — Kammer practice matching the regulation exactly, which is worth noting because the § 34a round found the opposite pattern (IHK summaries silently dropping a statutory qualifier).

### 3.3 What the scope split determines in practice

| Consequence | Provision |
|---|---|
| **What may be sold.** A Nr. 1-only licence holder advising on a Nachrangdarlehen or a closed-end fund is acting **without the required Erlaubnis** — an OWi under § 144 Abs. 1 Nr. 1 lit. m GewO, punishable by **up to EUR 50 000** (§ 144 Abs. 4 GewO). Note the asymmetry in the fine schedule: unlicensed § 34f/§ 34h activity attracts EUR 50 000, while breaches of the FinVermV conduct rules (§ 144 Abs. 2 Nr. 6) and of the registration duty (Nr. 8/9) attract **EUR 5 000**. | § 34f Abs. 1 Satz 1/3; § 144 Abs. 1 Nr. 1 lit. m, Abs. 2 Nr. 6, 8, 9, Abs. 4 GewO |
| **What must be examined.** § 34f Abs. 2 Nr. 4 Hs. 2 + § 3 Abs. 2 Satz 5–7 FinVermV. | see §3.2 |
| **What is on the certificate.** § 3 Abs. 8 Satz 2 FinVermV: the Bescheinigung must state which areas were examined. | § 3 Abs. 8 |
| **What is in the public register.** § 6 Nr. 4 FinVermV stores *"der Umfang der Erlaubnis nach § 34f Absatz 1 Satz 1 Nummer 1 bis 3"*; § 11a Abs. 1 Satz 3 GewO states the register's purpose as letting the public verify *"die Zulassung sowie **des Umfangs der zugelassenen Tätigkeit**"*. | § 34f Abs. 5 GewO; §§ 6, 7 FinVermV |
| **What must be told to the investor, unprompted, before the first advice.** § 12 Abs. 1 Nr. 3 lit. a FinVermV requires disclosure in Textform of whether one is registered *"als Finanzanlagenvermittler mit einer Erlaubnis nach § 34f Absatz 1 Satz 1 **Nummer 1, 2 oder Nummer 3**"*, plus Nr. 3a how to verify it and Nr. 5 the registration number. | § 12 Abs. 1 FinVermV |

**The scope split is therefore not a licensing technicality — it is a disclosure obligation, a register field, a certificate field and a EUR 50 000 boundary at once.** It is the highest-value single topic in the module, and the draft weights it accordingly. This repeats the pattern the Bewachungsgewerbe and DORA rounds found: scope boundaries are consistently where this project's exam-module dossiers land their most useful findings.

### 3.4 A genuine, and generous, exemption practitioners under-use

**§ 3 Abs. 5 FinVermV** drops the practical part altogether in three cases:

1. a **Nr. 1-only** exam, where the candidate already holds a **§ 34d Abs. 1 oder 2 GewO** insurance-intermediary licence, or a § 34d Abs. 5 Satz 1 Nr. 4 Sachkundenachweis (or an equivalent under § 27 VersVermV);
2. a **Folgeprüfung** extending an already-restricted § 34f/§ 34h licence to a further category — i.e. **you only ever do the customer-conversation role-play once**;
3. holding a **§ 34i Abs. 2 Nr. 4 GewO** (Immobiliardarlehensvermittler) Sachkundenachweis.

**§ 4 FinVermV** additionally treats **thirteen** named qualifications as equivalent to the whole exam (Bankfachwirt, Investment-Fachwirt, Fachwirt für Finanzberatung, Bank-/Sparkassenkaufmann, Investmentfondskaufmann, and others), and **§ 4 Abs. 2** recognises a mathematics, economics or law degree **plus, as a rule, three years' relevant experience**. A meaningful share of any real cohort never sits this exam at all — a product-positioning fact, not just a legal one.

---

## 4. The DIHK Rahmenplan — used as a scope cross-check only, exactly as the § 34a round did

A public DIHK Rahmenplan exists: **"Geprüfter Finanzanlagenfachmann IHK / Geprüfte Finanzanlagenfachfrau IHK", Stand Oktober 2023**, updated by the responsible *Sachverständigengremium*. It carries an express reservation of rights:

> "**Copyright:** Alle Rechte liegen beim Herausgeber. Ein Nachdruck – auch auszugsweise – ist nur mit ausdrücklicher schriftlicher Genehmigung des Herausgebers gestattet."

**Handling, matching the precedent set by `docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md` for the copyrighted DIHK § 34a Rahmenplan:** the document was opened **once**, only its **copyright notice, its Stand date, and its five top-level headings** were extracted, and **no learning objective, no sub-item wording, no phrasing and no ordering below level 1 was read into this dossier or into the draft.** It is cited here for exactly one proposition and no other.

That proposition is: **the Rahmenplan's five top-level areas are identical to Anlage 1 FinVermV's five top-level areas** — 1. Kundenberatung · 2. Kenntnisse für Beratung und Vertrieb von Finanzanlageprodukten · 3. Offene Investmentvermögen · 4. Geschlossene Investmentvermögen · 5. Vermögensanlagen (§ 1 Abs. 2 VermAnlG). The Rahmenplan describes itself as forming *"die Grundlage für die Erstellung von lernzielorientierten Prüfungsaufgaben"*.

**Two conclusions.** First, **the copyrighted document adds no scope this project needs**: the statutory annex already gives the same five areas at three levels of depth, free of copyright, so there is no temptation and no reason to go near the Rahmenplan's own text. Second, the cross-check **confirms** that authoring from Anlage 1 targets the right subject matter. That is the entire value of the exercise, and it is complete.

Also worth recording as a small correction to the § 34a analogy: unlike the § 34a Rahmenplan, this one does **not** state that the written question sets are bundeseinheitlich or non-public — but that costs nothing here, because for § 34f **both facts are in the regulation** (§ 3 Abs. 3 Satz 1 and Satz 7 FinVermV). The § 34f sourcing case therefore rests on **no** trade-body document at all.

---

## 5. Geldwäscheprävention: the brief's premise is half-wrong, and the correction matters

### 5.1 Finanzanlagenvermittler are **not** named in § 2 GwG

The task brief asks me to *"confirm the exact GwG provision number that names them"* in § 2. Verified mechanically over the **complete consolidated GwG** (311 000 characters of extracted text):

> **"Finanzanlagenvermittler": 1 occurrence in the entire Act. "34f": 1 occurrence. Both are the same sentence — and it is not in § 2.**

**§ 2 Abs. 1 GwG's sixteen-item list of Verpflichtete does not mention them.** Nor could it: § 2 Abs. 1 Nr. 2 covers Finanzdienstleistungsinstitute *"mit Ausnahme der in § 2 Absatz 6 Satz 1 **Nummer 3 bis 10** […] des Kreditwesengesetzes genannten Unternehmen"*, and § 2 Abs. 6 Satz 1 **Nr. 8** KWG is precisely the Bereichsausnahme that § 34f Abs. 1 Satz 1 GewO keys off. A § 34f Vermittler is expressly carved *out* of the Nr. 2 route.

### 5.2 They are Verpflichtete by a two-step route, **with a carve-out** (Tier A)

The single occurrence is in the GwG's **own** definition of *Finanzunternehmen*:

> **§ 1 Abs. 24 GwG** — "Finanzunternehmen im Sinne dieses Gesetzes ist ein Unternehmen, dessen **Haupttätigkeit** darin besteht, […] **4. Finanzanlagenvermittler nach § 34f Absatz 1 Satz 1 der Gewerbeordnung** und Honorar-Finanzanlagenberater nach § 34h Absatz 1 Satz 1 der Gewerbeordnung **zu sein, es sei denn, die Vermittlung oder Beratung bezieht sich ausschließlich auf Anlagen, die von Verpflichteten nach diesem Gesetz vertrieben oder emittiert werden**, […]"

which then feeds:

> **§ 2 Abs. 1 Nr. 6 GwG** — "**Finanzunternehmen** sowie im Inland gelegene Zweigstellen und Zweigniederlassungen von Finanzunternehmen mit Sitz im Ausland, soweit sie nicht bereits von den Nummern 1 bis 5, 7, 9, 10, 12 oder 13 erfasst sind,"

**The precise statement, and it is a two-limbed conditional, not a status:**

> A Finanzanlagenvermittler nach § 34f Abs. 1 Satz 1 GewO is a GwG-Verpflichteter **via § 2 Abs. 1 Nr. 6 GwG in Verbindung mit § 1 Abs. 24 Nr. 4 GwG** — **unless** the intermediation or advice relates **exclusively** to investments distributed or issued by entities that are themselves Verpflichtete under the GwG, in which case the exception in § 1 Abs. 24 Nr. 4 GwG applies and the Vermittler is not a Finanzunternehmen and therefore **not** a Verpflichteter.

**Why this is the module's most practically useful GwG fact, and why it correlates with the scope split.** Kapitalverwaltungsgesellschaften are Verpflichtete under § 2 Abs. 1 Nr. 9 GwG and Kreditinstitute under Nr. 1. A Vermittler whose entire book is open-ended KVG funds (a pure **Nr. 1** licence) will typically fall inside the exception and owe **nothing** under the GwG. A Vermittler placing **Nr. 3** Vermögensanlagen — Nachrangdarlehen, Genussrechte, stille Beteiligungen from ordinary corporate issuers who are *not* GwG-Verpflichtete — falls outside the exception and carries the **full** § 4/§ 6/§ 10 ff. apparatus. **The § 34f licence category and the GwG obligation status track each other.** Independently consistent with the IHK München Merkblatt on §§ 34f/34h Berufspflichten (Tier B), which lists the FinVermV conduct duties in detail and **does not mention the GwG at all** — which would be an odd omission for a universal duty and is exactly what one expects of a conditional one.

**Two things a module must therefore *not* say:** that Finanzanlagenvermittler are listed in § 2 GwG (they are not), and that they are unconditionally Verpflichtete (they are not). **Anlage 1 Nr. 2.4.4 puts "Geldwäschegesetz" on the syllabus regardless** — so the topic is examinable, but the correct answer is the conditional one.

### 5.3 Coverage check against `data/kyc_aml_pilot.json`, and the cross-link plan

Read programmatically: **30 questions, 5 topics** (`Grundlagen der Geldwaesche`, `Kundensorgfaltspflichten (KYC)`, `Verdachtsmeldewesen`, `Verstaerkte Sorgfaltspflichten`, `Sanktionen und Folgen`), DE canonical + EN, `legal_basis` values spanning **§§ 2 Abs. 1, 4, 5, 7, 10, 11, 12, 15, 16a, 18, 20, 27, 43, 45, 46, 47, 56 GwG**, plus § 261 StGB and § 25h KWG. String counts over the whole file:

> **"34f" 0 · "Finanzanlagen" 0 · "Finanzunternehmen" 0 · "Abs. 24"/"Absatz 24" 0 · "Anlagevermittlung" 0 · "Anlageberatung" 0 · "Vermögensanlage" 0 · "Investmentvermögen" 0.**

So `kyc_aml` teaches the general GwG regime thoroughly and **has no contact whatever** with the § 1 Abs. 24 Nr. 4 / § 2 Abs. 1 Nr. 6 route. There is nothing to duplicate and a clean boundary to draw.

**Recommended pattern — cross-link, do not duplicate**, following the precedent the Maklerschein round set for its 2–3 broker GwG questions and `fadp_ch` set in its `meta.description`:

- The draft carries **exactly two GwG questions**, both restricted to the § 34f-specific hook: (a) the § 2 Abs. 1 Nr. 6 i. V. m. § 1 Abs. 24 Nr. 4 route *including its exception*, and (b) the negative point that § 2 GwG's list does not name Finanzanlagenvermittler. Both explanations end with an explicit pointer to `kyc_aml`, and `meta.related_modules` states the boundary.
- **Everything else stays in `kyc_aml`**: the three-phase model, § 10 Sorgfaltspflichten mechanics, PEPs, verstärkte Sorgfaltspflichten, § 43 Verdachtsmeldung, § 56 Bußgelder, § 16a cash prohibition.
- Conversely, `kyc_aml` would benefit from **one** added question on § 1 Abs. 24 Nr. 4 / § 2 Abs. 1 Nr. 6, since its existing § 2 Abs. 1 question presents the Verpflichteten list as the whole answer and the Finanzunternehmen route is a genuine second door. That is a small, separately-schedulable `kyc_aml` card, not part of this decision — and it sits neatly alongside the § 10 Abs. 6 GwG card the Maklerschein round already proposed.

### 5.4 Coverage check against `data/datenschutz_pilot.json`

Read programmatically: **40 questions, 5 topics**, GDPR/BDSG general. String counts: **"34f" 0 · "Finanzanlage" 0 · "Aufzeichnung" 0 · "Beratungsgespräch" 0 · "zehn Jahre" 0.**

Anlage 1 Nr. 2.7.3 puts *Datenschutz* on the § 34f syllabus, and the § 34f-specific data-protection problem is a real and unusual one: **§ 18a FinVermV compels recording of every advice-related phone call and electronic communication**, permits processing the personal data the investor discloses in them, requires prior notice to investor *and* staff, **bars telephone/electronic advice entirely if the investor objects** (Abs. 3 Satz 2), restricts evaluation to four enumerated purposes and **expressly forbids using the recordings to monitor employees** (Abs. 5 Satz 1), gives the investor a copy right (Abs. 6 Satz 1), and mandates deletion after the § 23 retention period with the deletion itself documented (Abs. 6 Satz 2–3).

The draft carries **one** question on this, in the `beratung_vertrieb` topic, with `meta.related_modules` pointing at `datenschutz` for the general GDPR principles, data-subject rights and sanctions — the same shape `bewachungsgewerbe_pilot_DRAFT.json` used for its § 4 BDSG video-surveillance slice.

---

## 6. A drafting defect inside the FinVermV, found and worked around

**§ 23 Satz 1 FinVermV** (the duty): *"Die Aufzeichnungen nach § 18a Absatz 1 Satz 1 und Absatz 4 sowie die in § 22 genannten Unterlagen sind **zehn Jahre** auf einem dauerhaften Datenträger vorzuhalten […]"*

**§ 26 Abs. 1 Nr. 18 FinVermV** (the sanction for breaching it): *"… entgegen § 23 Satz 1 eine Unterlage nicht, nicht in der vorgeschriebenen Weise oder nicht **mindestens fünf Jahre** aufbewahrt"*

The sanction provision still carries the **pre-amendment five-year figure** while the duty provision says ten. Confirmed identical on **two independent consolidations** (`gesetze-im-internet.de` and `buzer.de`), so this is the enacted text and not a transcription error on either site. The IHK München Berufspflichten-Merkblatt (Tier B) states **ten years**, consistent with § 23.

**Handling in the draft:** the retention question tests **§ 23 Satz 1 — ten years, running from the end of the calendar year in which the last recordable event for that mandate occurred** — because § 23 is the duty and § 26 is merely its (imperfectly updated) sanction. The explanation flags the discrepancy rather than hiding it, and **no question tests the § 26 Abs. 1 Nr. 18 limb**. Flagged here as an open item for legal review (§9).

---

## 7. Source confidence

**Tier A — binding primary text, read in the official consolidated version.** Everything the draft rests on.

1. **GewO § 34f Abs. 1–6** in full — `gesetze-im-internet.de`, cross-read on `buzer.de`. The load-bearing sentences (Abs. 1 Satz 1 Nr. 1–3, Abs. 1 Satz 3, Abs. 2 Nr. 4, Abs. 4 Satz 1) read twice, independently.
2. **FinVermV §§ 1, 2, 3, 4, 6, 7, 9, 11, 11a, 12, 12a, 13, 14, 15, 16, 17, 18, 18a, 19, 20, 22, 23, 24, 26** in full.
3. **FinVermV Anlage 1** in full — the statutory syllabus, and the reason this module is buildable at all.
4. **FinVermV Anlage 2** title — the three-way category split written into the certificate.
5. **GewO §§ 11a, 32 Abs. 2, 34g, 34h, 144** (incl. Abs. 4 Bußgeldrahmen).
6. **KAGB § 1 Abs. 4, 5, 6**; **KWG § 2 Abs. 6 Satz 1 Nr. 8**; **VermAnlG §§ 1 Abs. 2, 2a, 13**; **HGB §§ 171, 172**.
7. **GwG § 1 Abs. 24 Nr. 4** and **§ 2 Abs. 1** in full, plus **mechanical whole-Act string counts** establishing that "Finanzanlagenvermittler" and "34f" each occur exactly once in the GwG and that the occurrence is § 1 Abs. 24 Nr. 4, not § 2.
8. **Mechanical negative checks** over Anlage 1 FinVermV: "Anlegerpsychologie" → 0, "Psychologie" → 0, "Risikoaufklärung" → 0, "Nachrangdarlehen" → 0.
9. **Cross-consolidation confirmation** of the § 23 / § 26 Abs. 1 Nr. 18 retention-period discrepancy on two independent sites.

**Tier B — official/quasi-official procedural material, not itself binding.**

10. **IHK "Wichtige Hinweise zur Sachkundeprüfung Finanzanlagenfachmann"** — written part max. 165 min (Basisteil 30 + 3 × 45, incl. a 20-min break), ≥ 50 % per applied category, role-play ca. 20 min, usually the day after the written part, and *"Kategorie 3: Nur in Verbindung mit Kategorie 2 möglich!"* — an independent practice-side confirmation of § 3 Abs. 2 Satz 7 FinVermV. **Kammer practice, not federal law**; used only for the `exam_format_note` and labelled as such there.
11. **IHK München und Oberbayern, Merkblatt Berufspflichten §§ 34f/34h GewO** — duty inventory, ten-year retention, audit report due 31 December of the following year; **no mention of the GwG**, consistent with §5.2's conditional finding.
12. **DIHK Rahmenplan, Stand Oktober 2023** — **copyright notice, Stand date and five top-level headings only** (§4). Cited for one proposition: the top-level scope matches Anlage 1 FinVermV. **No content derived.**

**Tier C — orientation only, load-bearing for nothing.**

13. A law-firm client briefing on the 2. FinVermVÄndV (V. v. 09.10.2019 BGBl. I S. 1434, in force 01.08.2020) confirming *"das bisherige Beratungsprotokoll [wird] durch eine Geeignetheitserklärung nach § 18 FinVermV ersetzt"* and that § 18a taping was *"neu eingefügt"*. Corroborates §0.2's correction; the current § 18 and § 18a texts are Tier A and stand on their own, and `buzer.de` independently records that § 18 has exactly one earlier Fassung.
14. IHK regional landing pages surfaced in search (Nürnberg, Frankfurt, Rhein-Neckar, Berlin, Kassel-Marburg, Ostwestfalen, Düsseldorf, Hannover, Köln, Leipzig, Gera, Stuttgart) — several returned HTTP 403 and were not read. **No proposition rests on any of them.**

**Confidence in the headline findings: high.** §0.1 (blocker solved), §3 (scope split incl. the asymmetric Nr. 3 → Nr. 2 coupling) and §5 (GwG route and its carve-out) are all direct quotations from consolidated federal instruments, two of the three cross-read on a second consolidator, and §3.2 additionally corroborated from the practice side. The residual risks are **currency** (§9.1) rather than accuracy.

---

## 8. What was drafted, and how it is scoped

`data/finanzanlagenvermittler_pilot_DRAFT.json` — **30 questions, DE canonical + EN**, generated deterministically by `data/gen_finanzanlagenvermittler_draft.py`. Five topics, **1:1 with Anlage 1 FinVermV's five areas**:

| Topic | Anlage 1 area | Questions | Rationale |
|---|---|---|---|
| `kundenberatung` | 1. Kundenberatung | 4 | Deliberately light. § 3 Abs. 4 FinVermV makes this the **practical** part — a role-play — which MCQ tests badly. The four questions here test the *legally hard* edges of the advice process (§§ 11, 11a Abs. 3, 13, 16 Abs. 3), not conversational technique. |
| `beratung_vertrieb` | 2. Kenntnisse für Beratung und Vertrieb | 13 | The shared legal base every candidate sits regardless of scope: the Erlaubnis and its three-way split, the Sachkunde and staff limbs, the register, and the whole FinVermV conduct-and-documentation apparatus, plus the two GwG questions and the one Datenschutz question. |
| `offene_investmentvermoegen` | 3. Offene Investmentvermögen | 5 | § 34f Abs. 1 Satz 1 Nr. 1 category. |
| `geschlossene_investmentvermoegen` | 4. Geschlossene Investmentvermögen | 4 | § 34f Abs. 1 Satz 1 Nr. 2 category. |
| `vermoegensanlagen` | 5. Vermögensanlagen (§ 1 Abs. 2 VermAnlG) | 4 | § 34f Abs. 1 Satz 1 Nr. 3 category. |

**Weighting, stated honestly as a judgement call and not as a documented fact about the real exam.** § 3 Abs. 2 Satz 2 FinVermV requires the § 1 Abs. 1 Nr. 1 areas to be examined *"in einem ausgewogenen Verhältnis zueinander"* and no authority publishes a question distribution. Areas 1 and 2 are weighted up because **every** candidate sits them irrespective of which categories they apply for, whereas each of areas 3–5 is sat only by the subset applying for that category. The `topic_weighting_note` in the file says exactly this.

**Every question carries a `legal_basis` naming a specific provision**, and the `high_stakes`/5-point flag marks the questions where an error in practice is an Ordnungswidrigkeit, an act outside one's Erlaubnis, or a breach of an investor-protection duty — the scope split, the staff Sachkunde limb, the § 20 client-money prohibition, the Geeignetheit/Angemessenheit distinction, the § 18a objection rule and the GwG status.

**What the draft explicitly does not do:** claim to reproduce, predict or cover the real exam (§ 3 Abs. 3 Satz 7 FinVermV makes the real questions non-public by law); invent a pass rule beyond § 3 Abs. 7's statutory 50 %-per-area; present Kammer-specific timings as federal law; test the defective § 26 Abs. 1 Nr. 18 retention limb; or carry any "Anlegerpsychologie" content (§0.3).

**Locales.** DE + EN first, per the established pattern (`aevo_pilot.json`, `fadp_ch_pilot.json`, `kyc_aml_pilot.json`, `bewachungsgewerbe_pilot_DRAFT.json`). Unlike the § 34a module — where the sibling dossier argued the migrant-heavy workforce makes all 12 locales a strong fit — this cohort sits a German-language proctored exam involving German tax and company law, and a 12-locale build should be a deliberate PO decision rather than an assumption. AGENTS.md constraint 5's 12-locale requirement applies to UI strings and topic labels regardless, and would apply to this module's content the moment it is wired in.

---

## 9. Open items for the PO / human decision

### 9.1 Re-verification

1. **Set a re-verification date of no later than 2026-11-30.** The FinVermV was last amended by **Art. 9 V. v. 11.12.2024 (BGBl. 2024 I Nr. 411)** and is stable, but the surrounding statutes are not: the GewO was amended on **20.07.2026 (BGBl. 2026 I Nr. 215)** and the GwG on **29.06.2026 (BGBl. 2026 I Nr. 197)**, both within the last eight weeks. Re-read § 34f GewO, § 1 Abs. 24 GwG and § 2 Abs. 1 GwG **from the amending instruments**, per the standing process note the Maklerschein round established (`docs/maklerschein-pre-review-dossier-2026-08-17.md` §1.1 and open item 7).
2. **Watch the supervision question.** Moving § 34f supervision from the Gewerbeämter/IHKs to BaFin has been proposed repeatedly and has never been enacted; if it ever is, the § 24 FinVermV audit regime and the § 11a register architecture both change. Not currently in force and nothing in the draft assumes otherwise.

### 9.2 Legal review

3. **Have counsel confirm the §5.2 GwG conditional** before any of it reaches learners. It is a statutory reading, well-supported, but it is the kind of conclusion ("you may owe nothing under the GwG") where being wrong is expensive. The two GwG questions in the draft are the ones to review first.
4. **Flag the § 23 / § 26 Abs. 1 Nr. 18 discrepancy** (§6) to whoever reviews. The draft's answer (ten years) is right on any reading, but the reviewer should know the tension is there and is in the enacted text.
5. **Anlage 1's frozen 2012 substance** (§2.3) needs a systematic pass, not just the VermAnlG spot-fix the draft applies. Areas 3.6 and 4.6/5.5 (Steuerliche Behandlung) in particular reference a tax landscape that has moved considerably — the Investmentsteuerreform 2018 alone. **The draft deliberately contains no tax questions for this reason**, which is a real coverage gap against the statutory syllabus and should be closed by someone competent in the tax law rather than papered over.

### 9.3 Scope and roadmap

6. **Decide the locale target** (§8) — DE+EN pilot as drafted, or plan for all 12 from the start.
7. **Correct the roadmap.** `claude/content-portfolio-and-expansion-roadmap-2026-08-14.md` and the related `BACKLOG.md` entries should now record **three** genuine § 34x IHK-exam modules, all drafted on 2026-08-17 in parallel rounds — **§ 34a** (`docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md`), **§ 34d** (`docs/versicherungsvermittler-pre-review-dossier-2026-08-17.md`), **§ 34f** (this dossier) — and should carry the Maklerschein round's de-coupling of § 34c from that group. **Worth a small follow-up card: the § 34d and § 34f modules interlock by statute** and neither round could see the other's output while running. § 3 Abs. 5 Nr. 1 FinVermV drops the practical part of the § 34f exam for a Nr.-1-only candidate who already holds a § 34d licence or § 34d Abs. 5 Satz 1 Nr. 4 Sachkundenachweis; § 12 Abs. 2 FinVermV lets § 15 VersVermV's status disclosure satisfy § 12 Abs. 1 for someone holding both. A `related_modules` cross-link in **both** files, plus one question on each side about the dual-licence case, would be cheap and is genuinely exam-relevant. This module's `meta.related_modules` currently cross-links `kyc_aml`, `datenschutz` and `bewachungsgewerbe` but **not** `versicherungsvermittler`, because that draft did not exist when this one was generated.
8. **Schedule the small `kyc_aml` card** for § 1 Abs. 24 Nr. 4 / § 2 Abs. 1 Nr. 6 GwG (§5.3), alongside the § 10 Abs. 6 GwG card the Maklerschein round proposed.
9. **Do not wire this module in until items 3–5 are closed.** The `_DRAFT` suffix keeps it out of the build path; leave it there.

---

**Reminder:** this document is draft research groundwork. It is not legal advice, has not been reviewed by a qualified lawyer, and no content derived from it should be shipped to learners before that review. Nothing here was sourced from any exam-prep vendor's material, and the one copyrighted document consulted (§4) was used solely to confirm that the copyright-free statutory annex already covers the required scope.
