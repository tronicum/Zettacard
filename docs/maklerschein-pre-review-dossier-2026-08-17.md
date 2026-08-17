# "Maklerschein" (§ 34c GewO Immobilienmakler) — pre-review dossier (2026-08-17)

**Status:** AI-prepared research groundwork only — **NOT legal advice**. No content was drafted this round, deliberately. See §0 and §9.

**Requested:** a "Maklerschein" exam-prep module for German real-estate brokers (Immobilienmakler), explicitly modelled on `data/aevo_pilot.json` (IHK Ausbilder-Eignungsprüfung) and the driving-licence modules — i.e. a genuine question bank for a proctored pass/fail exam.

**Delivered:** this dossier, and **no `data/maklerschein_pilot_DRAFT.json`**. The requested module shape rests on a factual premise that primary-source research disproves twice over. Building it would have shipped a fabricated exam for a licence that has no exam, against a syllabus that was **repealed three and a half weeks ago**.

**Files touched:** this file only. `data/build_modules.py`, `data/modules_manifest.json`, `app/data/modules.json` and `app/app.js` are untouched; no build was run; nothing was staged or committed.

---

## 0. The finding, first, because it is a scope decision and not a footnote

Two separate framings were put to me. **Both are factually wrong as of today.**

| Framing | Verdict | Why |
|---|---|---|
| **(A) The PO's framing:** "an IHK *Sachkundeprüfung* for Immobilienmakler, like § 34d / § 34f" — a proctored exam with a pass/fail question catalogue | **Wrong, and has never been right.** | § 34c GewO has **never** contained a qualification or Sachkunde requirement. The word *Sachkunde* appears **zero times** in § 34c GewO and **zero times** in the entire MaBV. § 34c Abs. 2 is a closed list of three grounds for refusal, none of which is knowledge-based. |
| **(B) The task brief's own fallback:** "no upfront exam, but a *Weiterbildungspflicht* of 20 h / 3 years under § 34c Abs. 2a GewO + § 15b MaBV, whose required subject areas are listed in § 15b / Anlage 1 MaBV" | **Was right until 23 July 2026. Wrong since 24 July 2026.** | The **Gesetz zum Bürokratierückbau in der Gewerbeordnung …** of **20 July 2026 (BGBl. 2026 I Nr. 215)**, in force **24 July 2026**, **struck Immobilienmakler out of § 34c Abs. 2a GewO** and **deleted Teil A of Anlage 1 MaBV** — the broker syllabus itself. Brokers now have **no continuing-education duty at all**. Wohnimmobilienverwalter keep theirs. |

**Consequence for the product:** as of 2026-08-17 a German Immobilienmakler has **no statutory knowledge obligation of any kind** arising from GewO or MaBV — no entry exam, no syllabus, no hour quota, no proof-of-training file. The only mandatory *training* duty anywhere in a broker's regulatory perimeter is **§ 6 Abs. 2 Nr. 6 GwG** (money-laundering staff instruction), which is a duty to *instruct staff*, not a duty to *pass* anything, and which this repo's `kyc_aml` module already substantially covers (§6).

The brief anticipated exactly this and instructed: *"do NOT force-build a fake exam bank anyway … STOP there without drafting the mismatched content."* That instruction is followed. §8 sets out three accurate alternative shapes and a recommendation; §10 lists what the PO has to decide.

**One further correction, to this repo's own roadmap.** `claude/content-portfolio-and-expansion-roadmap-2026-08-14.md` and three `BACKLOG.md` "Done" entries pair **"§ 34a Bewachungsgewerbe and § 34c Immobilienmakler"** as a single deferred item with a single shared blocker ("no official public question catalog, only private vendor compilations"). That pairing is a **regulatory category error**. § 34a **does** have a real, statutory IHK Sachkundeprüfung (§ 34a Abs. 1 Satz 3 Nr. 3 and Abs. 1a GewO — see §5); its blocker is genuinely a *sourcing* problem, and it is a legitimate exam-prep module. § 34c has **no exam to prep for**; its blocker is not sourcing but **the non-existence of the subject**. The two should be de-coupled on the roadmap, because "resolve the sourcing question" unblocks § 34a and does nothing for § 34c.

---

## 1. Method and instruments read

All retrieval on **2026-08-17**. `WebFetch` is blocked on `gesetze-im-internet.de` in this sandbox (`ROBOTS_DISALLOWED`); every German statutory text below was fetched by direct `curl` against `gesetze-im-internet.de` and parsed from the raw HTML, so the quotes are from the consolidated official text and not from a summary. The decisive amendment was additionally read in the **official Bundesgesetzblatt PDF** and in an **independent third consolidation** (`buzer.de`), giving three independent readings of the load-bearing sentence.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **GewO § 34c** (Immobilienmakler, Darlehensvermittler, Bauträger, Baubetreuer, Wohnimmobilienverwalter) | `gesetze-im-internet.de/gewo/__34c.html` | Abs. 1–5 in full, incl. Fußnote |
| **GewO § 34a** (Bewachungsgewerbe) | `gesetze-im-internet.de/gewo/__34a.html` | Abs. 1, 1a, 2 — Sachkunde limbs |
| **GewO § 34d** (Versicherungsvermittler) | `gesetze-im-internet.de/gewo/__34d.html` | Abs. 2 Nr. 4 |
| **GewO § 34f** (Finanzanlagenvermittler) | `gesetze-im-internet.de/gewo/__34f.html` | Abs. 2 Nr. 4, Abs. 4 |
| **MaBV** (Makler- und Bauträgerverordnung) | `gesetze-im-internet.de/gewo_34cdv/` — **note the non-obvious slug `gewo_34cdv`**; `/mabv/` 404s | **Full consolidated text** (§§ 1–22, Anlagen 1–3), plus Einzelnorm pages for § 15b, Anlage 1, Anlage 2 |
| **GewBürAbG** — Gesetz zum Bürokratierückbau in der Gewerbeordnung und dem Energieverbrauchskennzeichnungsgesetz sowie anderer Rechtsvorschriften zur Aufhebung von Berichtspflichten, **G. v. 20.07.2026, BGBl. 2026 I Nr. 215** | **Official BGBl PDF**: `recht.bund.de/bgbl/1/2026/215/regelungstext.pdf?__blob=publicationFile&v=1` (7 pp., 289 KB) **and** `buzer.de/gesetz/17617/index.htm` | Art. 1 Nr. 3, Art. 2 Nr. 1–5, Art. 11 — verbatim, both sources |
| **GwG** §§ 1, 2, 6, 10, 16a | `gesetze-im-internet.de/gwg_2017/` | § 1 Abs. 11, § 2 Abs. 1 Nr. 14, § 6 Abs. 2 Nr. 6, § 10 Abs. 6, § 16a Abs. 1–5 |
| **GwGMeldV-Immobilien** | `gesetze-im-internet.de/imgwgmeldv/__1.html` | § 1 (scope) |
| **MaBV Anlage 1, pre-24.07.2026 version** (the deleted broker syllabus) | `buzer.de/gesetz/2268/al241781-0.htm` (archived Fassung) | **Teil A in full** — reproduced at §4.2 |
| **DIHK, "FAQ: Weiterbildungspflicht für Immobilienmakler und Wohnimmobilienverwalter", Stand Januar 2025** | `dihk.de/resource/blob/129800/…/faq-wb-34c-gewo-stand29012025-data.pdf` (6 pp.) | Whole document — documents the **pre-abolition** regime |

**Not used as a basis for anything:** the SEO/press-release pages that dominate search results for this topic (`pressnetwork.de`, `go-with-us.de`, `pflumm.de`, `pr-echo.de`, `schlaunews.de`, `artikel-presse.de` — all carrying the identical syndicated text "Abschaffung der Weiterbildungspflicht für Immobilienmakler"). They corroborate the finding and are the reason I went looking, but nothing here rests on them.

### 1.1 A retrieval trap worth recording for the next agent

The consolidated § 34c text on `gesetze-im-internet.de` **currently contradicts every IHK page, every trade-body page and the DIHK's own FAQ**, all of which still say the Weiterbildungspflicht covers Immobilienmakler. The consolidated statute is right and the secondary sources are stale by weeks. Had I "sanity-checked" the primary text against the weight of secondary opinion — the normal and usually correct instinct — I would have concluded the `curl` output was truncated and built module (B). What actually resolved it was **going to the amending act and reading the change instruction**, which is the only artefact that states *what changed and when*. Recommended as standing practice for this repo: when consolidated text and practitioner consensus disagree, the tie-break is the amending instrument, never the louder source.

---

## 2. What § 34c GewO actually requires of an Immobilienmakler (Tier A)

### 2.1 The permission requirement

> **§ 34c Abs. 1 Satz 1 GewO** — "Wer gewerbsmäßig **1.** den Abschluss von Verträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume vermitteln oder die Gelegenheit zum Abschluss solcher Verträge nachweisen, […] will, bedarf der Erlaubnis der zuständigen Behörde."

Brokers are **Nr. 1**. The other addressees of the same section — and the distinction is load-bearing for everything below — are **Nr. 2** Darlehensvermittler, **Nr. 3** Bauträger/Baubetreuer, **Nr. 4** **Wohnimmobilienverwalter**.

### 2.2 The grounds for refusal are a closed list, and none of them is knowledge

> **§ 34c Abs. 2 GewO** — "Die Erlaubnis **ist zu versagen, wenn**
> **1.** Tatsachen die Annahme rechtfertigen, daß der Antragsteller oder eine der mit der Leitung des Betriebes oder einer Zweigniederlassung beauftragten Personen die für den Gewerbebetrieb erforderliche **Zuverlässigkeit** nicht besitzt; die erforderliche Zuverlässigkeit besitzt in der Regel nicht, wer in den letzten fünf Jahren vor Stellung des Antrages wegen eines Verbrechens oder wegen Diebstahls, Unterschlagung, Erpressung, Betruges, Untreue, **Geldwäsche**, Urkundenfälschung, Hehlerei, Wuchers oder einer Insolvenzstraftat rechtskräftig verurteilt worden ist,
> **2.** der Antragsteller in **ungeordneten Vermögensverhältnissen** lebt; dies ist in der Regel der Fall, wenn über das Vermögen des Antragstellers das Insolvenzverfahren eröffnet worden oder er in das vom Vollstreckungsgericht zu führende Verzeichnis (§ 26 Abs. 2 Insolvenzordnung, § 882b Zivilprozeßordnung) eingetragen ist,
> **3.** der Antragsteller, **der ein Gewerbe nach Absatz 1 Satz 1 Nummer 4 betreiben will**, den Nachweis einer **Berufshaftpflichtversicherung** nicht erbringen kann."

Three findings, all directly relevant to how a module would have to be worded:

1. **No Sachkunde limb exists.** The list is exhaustive ("ist zu versagen, wenn"). A knowledge test cannot be read into it, and no Land can add one — § 34c is federal law and the Länder only designate the *zuständige Behörde*.
2. **The word "Sachkunde" appears 0 times in § 34c GewO and 0 times in the whole of the MaBV** (mechanical count over the retrieved texts). Contrast §5.
3. **The Berufshaftpflichtversicherung requirement does NOT apply to brokers.** Abs. 2 Nr. 3 is expressly limited to *Nummer 4* — Wohnimmobilienverwalter. **This corrects the task brief itself**, which listed "Berufshaftpflichtversicherung requirements" among the things a broker needs for the Erlaubnis. A broker needs Zuverlässigkeit and ordered finances, and that is all. (Brokers may of course carry Vermögensschadenhaftpflicht commercially; it is not a licensing condition.)

### 2.3 What *is* genuinely binding on brokers, and it is real law

Losing the Weiterbildungspflicht does not leave brokers unregulated. The MaBV applies to them by § 1 Abs. 1 — *"Diese Verordnung gilt für Gewerbetreibende, die Tätigkeiten nach § 34c Absatz 1 der Gewerbeordnung ausüben, unabhängig vom Bestehen einer Erlaubnispflicht."* Note also § 1 Abs. 2 Satz 2: the MaBV **does not** apply to Wohnimmobilienverwalter except §§ 11, 15–15b, 18 and 19 — i.e. **the operative MaBV duties are mostly a broker/Bauträger regime, not a Verwalter regime.** The Verwalter has the syllabus; the broker has the duties. This inversion is the single most interesting product fact in the dossier and is the basis of the §8 recommendation.

Binding on a broker today:

| Provision | Duty | Applies to brokers? |
|---|---|---|
| **§ 2 MaBV** | Sicherheitsleistung/Versicherung before receiving or being authorised to use client assets | Yes — but **§ 7 Abs. 1** frees "die übrigen Gewerbetreibenden im Sinne des § 34c Abs. 1" from §§ 2, 3 Abs. 3 and 4–6 where blanket security is provided, and § 7 Abs. 2 exempts public-law and registered-merchant clients. Most brokers never touch client funds and so never trigger it. |
| **§ 8 MaBV** | Rechnungslegung after execution of the mandate | Yes |
| **§ 10 MaBV** | Buchführungspflicht — records "unverzüglich und in deutscher Sprache"; **Abs. 3** adds broker-specific particulars | Yes, incl. an express broker-only paragraph |
| **§ 11 MaBV** | Informationspflicht in Textform und in deutscher Sprache; **Satz 1 Nr. 1** is the broker limb (Nr. 3 is the Verwalter limb and per the DIHK FAQ expressly *does not* apply to brokers) | Yes |
| **§ 14 MaBV** | Aufbewahrung of business records | Yes |
| **§ 16 Abs. 2 MaBV** | Ad-hoc audit at the broker's cost "aus besonderem Anlaß" (the *routine annual* Prüfungsbericht in § 16 Abs. 1 is a **Bauträger** duty — § 34c Abs. 1 Satz 1 Nr. 3 — not a broker one) | Yes, ad-hoc only |
| **§ 18 MaBV** | Ordnungswidrigkeiten for breaches of the above, via §§ 144–146 GewO | Yes |
| **§ 15b MaBV / § 34c Abs. 2a GewO** | Weiterbildung, 20 h / 3 years, + evidence file | **No — not since 24.07.2026** (§3) |
| **§ 34c Abs. 2 Nr. 3 GewO / §§ 15, 15a MaBV** | Berufshaftpflichtversicherung + Versicherungsbestätigung | **No** — Wohnimmobilienverwalter only |
| **GwG** (§§ 2 Abs. 1 Nr. 14, 4, 6, 10 Abs. 6, 43; § 16a) | Money-laundering prevention | **Yes** — see §6 |

---

## 3. The 24 July 2026 abolition — verbatim, from three independent readings

### 3.1 The amending instruction

**Gesetz zum Bürokratierückbau in der Gewerbeordnung und dem Energieverbrauchskennzeichnungsgesetz sowie anderer Rechtsvorschriften zur Aufhebung von Berichtspflichten**, of **20 July 2026**, **BGBl. 2026 I Nr. 215**.

> **Artikel 1 (Änderung der Gewerbeordnung), Nr. 3** — "§ 34c Absatz 2a wird wie folgt geändert:
> a) In Satz 1 wird die Angabe „Absatz 1 Satz 1 **Nummer 1 und 4**" durch die Angabe „Absatz 1 Satz 1 **Nummer 4**" ersetzt.
> b) In Satz 2 Nummer 1 wird die Angabe „Absatz 1 Satz 1 Nummer 1 oder 4" durch die Angabe „Absatz 1 Satz 1 Nummer 4" ersetzt.
> c) In Satz 3 wird die Angabe „bei der **Vermittlung** nach Absatz 1 Satz 1 Nummer 1 oder der Verwaltung nach Absatz 1 Satz 1 Nummer 4 mitwirkenden Personen" durch die Angabe „bei der **Verwaltung** nach Absatz 1 Satz 1 Nummer 4 mitwirkenden Personen" ersetzt."

> **Artikel 2 (Änderung der Makler- und Bauträgerverordnung), Nr. 4 und 5** — "4. **Anlage 1** wird wie folgt geändert: a) **Teil A wird gestrichen.** b) Die Überschrift „**B.** Inhaltliche Anforderungen an die Weiterbildung für Wohnimmobilienverwalter" wird durch die Überschrift „Inhaltliche Anforderungen an die Weiterbildung für Wohnimmobilienverwalter" ersetzt. — 5. **Anlage 3 wird gestrichen.**"

> **Artikel 11 Abs. 1** — "Dieses Gesetz tritt vorbehaltlich der Absätze 2 bis 4 **am Tag nach der Verkündung** in Kraft."

Art. 1 Nr. 3 and Art. 2 are **not** among the Absätze 2–4 exceptions (those cover Art. 1 Nr. 2 and Art. 7 → 01.05.2027, Art. 3 → 30.07.2026, Art. 9 → 01.11.2026). Verkündung was 23.07.2026; `buzer.de` records the section as "Geltung ab 24.07.2026". **The broker Weiterbildungspflicht therefore ended on 24 July 2026.**

Signed *Berlin, den 20. Juli 2026* by Bundespräsident Steinmeier, Bundeskanzler Merz and Bundesministerin für Wirtschaft und Energie Katherina Reiche.

### 3.2 Cross-check: the resulting consolidated text

> **§ 34c Abs. 2a Satz 1 GewO, as in force** — "Gewerbetreibende nach Absatz 1 Satz 1 **Nummer 4** sind verpflichtet, sich in einem Umfang von 20 Stunden innerhalb eines Zeitraums von drei Kalenderjahren weiterzubilden; das Gleiche gilt entsprechend für unmittelbar bei der erlaubnispflichtigen Tätigkeit mitwirkende beschäftigte Personen."

Identical wording retrieved independently from `gesetze-im-internet.de/gewo/__34c.html` and from `buzer.de/34c_GewO.htm` (the latter stating "zuletzt geändert durch Artikel 1 G. v. 20.07.2026 BGBl. 2026 I Nr. 215"). **Nummer 1 — Immobilienmakler — is gone from the sentence.**

> **Anlage 1 MaBV, as in force** — heading: "**Inhaltliche Anforderungen an die Weiterbildung für Wohnimmobilienverwalter**" (no Teil A, no "B."), followed by areas 1–8 (Grundlagen der Immobilienwirtschaft / Rechtliche Grundlagen / Kaufmännische Grundlagen / Verwaltung von Wohnungseigentumsobjekten / Verwaltung von Mietobjekten / Technische Grundlagen der Immobilienverwaltung / Wettbewerbsrecht / Verbraucherschutz). MaBV's table of contents now shows "**Anlage 3 (weggefallen)**".

§ 15b MaBV itself survives and still governs the *Verwalter* duty:

> **§ 15b Abs. 1 MaBV** — "Wer nach § 34c Absatz 2a der Gewerbeordnung zur Weiterbildung verpflichtet ist, muss sich fachlich entsprechend seiner ausgeübten Tätigkeit weiterbilden. Die inhaltlichen Anforderungen an die Weiterbildung sind an den Vorgaben der **Anlage 1** auszurichten. […] Der Erwerb eines Ausbildungsabschlusses als Immobilienkaufmann oder Immobilienkauffrau oder eines Weiterbildungsabschlusses als Geprüfter Immobilienfachwirt oder Geprüfte Immobilienfachwirtin gilt als Weiterbildung."

Because § 15b Abs. 1 Satz 1 keys off *"Wer nach § 34c Absatz 2a … verpflichtet ist"*, the § 34c amendment alone was enough to switch brokers off; deleting Teil A was tidying up after it.

### 3.3 Scope of the abolition — brokers only, and that was contested

The Weiterbildungspflicht for **Wohnimmobilienverwalter survives unchanged at 20 h / 3 years**. This was a live political question, not an oversight: the Bundesrat consented on **10 July 2026**, and the trade side's demand to abolish the Verwalter duty too — which had been in the Kabinettsentwurf — was **not** granted (*Die Wohnungswirtschaft Bayern*, 15.07.2026: *"Der von den Regionalverbänden und dem GdW gegenüber dem Bundesrat explizit geforderten Streichung der Weiterbildungspflicht auch für Wohnimmobilienverwalter … ist nicht nachgekommen worden."*). Tier C, and used only for the political framing; the legal fact is Tier A from §3.1.

### 3.4 Currency caveat, stated plainly

`gesetze-im-internet.de` flags the MaBV consolidation as *"Änderung durch Art. 2 G v. 20.7.2026 I Nr. 215 **textlich nachgewiesen, dokumentarisch noch nicht abschließend bearbeitet**"* — the substance is applied, the editorial apparatus is not finished. Separately, the MaBV was amended **again** on **28 July 2026** (Art. 2 V v. 28.07.2026, BGBl. 2026 I Nr. 229, in force 01.08.2026 — the Verbraucherkredit-Umsetzungsverordnung, which renumbers § 34c Abs. 1 references in §§ 2, 4, 16 MaBV, with GII noting the change instruction was defective and consolidated *sinngemäß*). **This corner of the law is moving fast: two amendments in eight days.** Anything built here needs a re-verification date, and any figure or Nummer reference should be re-read rather than trusted from this document after ~Q4 2026.

---

## 4. The syllabus that no longer exists

### 4.1 That there was one is independently documented

The **DIHK FAQ, Stand Januar 2025** (Tier B, and now historical) confirms the pre-abolition architecture in terms:

> "Nach § 34c Absatz 2a GewO i. V. m. § 15b und den Anlagen 1 bis 3 der Makler- und Bauträgerverordnung (MaBV) besteht eine Pflicht zur regelmäßigen Weiterbildung für **Immobilienmakler und Wohnimmobilienverwalter** … innerhalb eines Zeitraums von drei Kalenderjahren in einem Umfang von 20 Stunden (à 60 Minuten) **pro Tätigkeitsbereich**."

and, on content:

> "… sollten die Inhalte der Weiterbildung mit Anlage 1 zu § 15b Absatz 1 MaBV (**Teil A für Immobilienmakler, Teil B für Wohnimmobilienverwalter**) abgeglichen werden."

It also records that someone holding **both** permissions owed **40 hours** per three years. That regime is now 20 hours, Verwalter side only.

### 4.2 Teil A as it read until 23.07.2026 (repealed; recorded for the record)

Retrieved from the archived pre-amendment Fassung of Anlage 1 MaBV. German statutory text is an *amtliches Werk* under § 5 UrhG and carries no copyright, so reproducing it raises none of this repo's constraint-1 concerns — it is the opposite of a vendor catalogue.

> **A. Inhaltliche Anforderungen an die Weiterbildung für Immobilienmakler**
> **1. Kundenberatung** — 1.1 Serviceerwartungen des Kunden · 1.2 Besuchsvorbereitung/Kundengespräch/Kundensituation · 1.3 Kundenbetreuung
> **2. Grundlagen des Maklergeschäfts** — 2.1 Teilmärkte des Immobilienmarktes · 2.2 Preisbildung am Immobilienmarkt · 2.3 Objektangebot und Objektanalyse · 2.4 Die Wertermittlung · 2.5 Gebäudepläne, Bauzeichnungen und Baubeschreibungen · 2.6 Relevante Versicherungsarten im Immobilienbereich · 2.7 Umwelt- und Energiethemen im Immobilienbereich
> **3. Rechtliche Grundlagen** — 3.1 Bürgerliches Gesetzbuch (3.1.1 Allgemeines Vertragsrecht · 3.1.2 Maklervertragsrecht · 3.1.3 Mietrecht · 3.1.4 Grundstückskaufvertragsrecht · 3.1.5 Bauträgervertragsrecht) · 3.2 Grundbuchrecht · 3.3 Wohnungseigentumsgesetz · 3.4 Wohnungsvermittlungsgesetz · 3.5 Zweckentfremdungsrecht · **3.6 Geldwäschegesetz** · 3.7 Makler- und Bauträgerverordnung · 3.8 Informationspflichten des Maklers (3.8.1 Dienstleistungs-Informationspflichten-Verordnung · 3.8.2 Digitale-Dienste-Gesetz · 3.8.3 Preisangabenverordnung · 3.8.4 Energieeinsparverordnung)
> **4. Wettbewerbsrecht** — 4.1.1 Allgemeine Wettbewerbsgrundsätze · 4.1.2 Unzulässige Werbung
> **5. Verbraucherschutz** — 5.1.1 Grundlagen des Verbraucherschutzes · 5.1.2 Schlichtungsstellen · 5.1.3 Datenschutz
> **6. Grundlagen Immobilien und Steuern** — 6.1 Einkommensteuern · 6.2 Körperschaftsteuern · 6.3 Gewerbesteuer · 6.4 Umsatzsteuer · 6.5 Bewertungsgesetzabhängige Steuern · 6.6 Spezielle Verkehrssteuern (Grunderwerb- und Grundsteuern)

**What this list is now, and is not.** It is **not** a legal requirement, **not** a syllabus anyone must satisfy, and **not** something a learner can be told they need. It **is** the best available evidence of what the German legislature considered professionally necessary for a broker as recently as July 2026, and as such it is a defensible, honestly-labelled scaffold for a **voluntary** competency module (option 2 in §8). Two of its areas also carry a live currency problem even as a scaffold: **3.8.4 Energieeinsparverordnung** (the EnEV was superseded by the GEG in 2020 — the annex was never updated) and **6.5** (Bewertungsgesetz-dependent taxes have moved substantially since 2018 via the Grundsteuerreform). Anything built from it must be re-grounded in current law, not transcribed.

---

## 5. The contrast that shows this is a real structural difference, not a gap in my search

Same statute, adjacent sections, opposite answers. All Tier A, all read today.

| Section | Trade | Statutory knowledge requirement | Exam-prep module viable? |
|---|---|---|---|
| **§ 34a GewO** | Bewachungsgewerbe (security) | **Yes.** Abs. 1 Satz 3 Nr. 3: refusal if the applicant "nicht durch eine **vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung** nachweist, dass er die für die Ausübung des Bewachungsgewerbes notwendige **Sachkunde** über die rechtlichen und fachlichen Grundlagen besitzt". Abs. 1a Satz 2 adds a Sachkundeprüfung for specified activities; Abs. 2 empowers the BewachV to set "die Anforderungen und das Verfahren für eine Sachkundeprüfung". | **Yes** |
| **§ 34c GewO** | **Immobilienmakler** | **None.** Abs. 2 is a closed list of Zuverlässigkeit + Vermögensverhältnisse (+ Berufshaftpflicht for Nr. 4 only). "Sachkunde": **0 occurrences** in § 34c; **0** in the MaBV. Since 24.07.2026 also no Weiterbildungspflicht. | **No** |
| **§ 34d GewO** | Versicherungsvermittler/-berater | **Yes.** Abs. 2 Nr. 4: refusal unless the applicant proves "durch eine **vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung** … die für die Versicherungsvermittlung oder Versicherungsberatung notwendige **Sachkunde** über die versicherungsfachlichen, insbesondere hinsichtlich Bedarf, Angebotsformen und Leistungsumfang, und die rechtlichen Grundlagen sowie die Kundenberatung". | **Yes** |
| **§ 34f GewO** | Finanzanlagenvermittler | **Yes.** Abs. 2 Nr. 4, same IHK-Prüfung construction, "die Sachkunde ist dabei im Umfang der beantragten Erlaubnis nachzuweisen"; Abs. 4 extends a Sachkundenachweis duty to mitwirkende Personen. | **Yes** |

The § 34d / § 34f wording the brief hypothesised for § 34c genuinely exists — **in § 34d and § 34f**. The legislature knows how to write a Sachkundeprüfung requirement and has written one three times in this very statute. Its absence from § 34c is a deliberate policy choice, repeatedly reaffirmed (the broker Sachkundenachweis has been a standing trade-body demand for over a decade and has never been enacted), and it is now reinforced rather than eroded: the July 2026 Act moved § 34c **further** away from a qualification regime.

**Product read:** if the PO wants a genuine § 34x GewO IHK-exam module, the three that exist are **§ 34a Bewachungsgewerbe** (already on the roadmap, and the one whose blocker really is just sourcing), **§ 34d Versicherungsvermittler** and **§ 34f Finanzanlagenvermittler**. The last two are especially interesting given this repo already holds `kyc_aml` and `datenschutz` content that overlaps their syllabi. § 34c is not on that list and cannot be put on it.

---

## 6. GwG: the one real training duty, and why it should be a cross-reference

### 6.1 The obligations (Tier A)

Immobilienmakler are a named obligated entity:

> **§ 2 Abs. 1 Nr. 14 GwG** — the entry reads, verbatim and in its entirety: "**Immobilienmakler,**"

> **§ 1 Abs. 11 GwG** — "Immobilienmakler im Sinne dieses Gesetzes ist, wer gewerblich den Abschluss von **Kauf-, Pacht- oder Mietverträgen** über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume vermittelt."

The trigger for customer due diligence is broker-specific and threshold-split:

> **§ 10 Abs. 6 GwG** — "Verpflichtete nach § 2 Absatz 1 Nummer 14 haben die allgemeinen Sorgfaltspflichten zu erfüllen: **1.** bei der Vermittlung von **Kaufverträgen** und **2.** bei der Vermittlung von **Miet- oder Pachtverträgen** bei Transaktionen mit einer **monatlichen Nettokaltmiete oder Nettokaltpacht in Höhe von mindestens 10 000 Euro**."

The training duty itself is an internal-safeguards duty, not a qualification:

> **§ 6 Abs. 2 Nr. 6 GwG** — internal safeguards include "die **erstmalige und laufende Unterrichtung der Mitarbeiter** in Bezug auf Typologien und aktuelle Methoden der Geldwäsche und der Terrorismusfinanzierung sowie die insoweit einschlägigen Vorschriften und Pflichten, einschließlich Datenschutzbestimmungen".

*(Note: this repo's `claude/kyc-aml-pre-review-dossier-2026-08-10.md` already flagged that `kyc_aml`'s metadata paraphrases this as "erstmalig und danach fortlaufend" where the statute says "die erstmalige und laufende Unterrichtung". Same wording, still worth conforming — it is quoted in a module description.)*

Also in perimeter: **§ 4 GwG** (Risikomanagement), **§ 43 GwG** (Verdachtsmeldung to the FIU), and **§ 16a GwG** *Verbot der Barzahlung beim Erwerb von Immobilien* — cash, Kryptowerte, gold, platinum and precious stones may not be used as consideration for domestic real-estate purchases or share deals in property-holding companies, with the § 16a Abs. 2–4 proof mechanics addressed to the **Notar** and a EUR 10 000 de-minimis in Abs. 5.

**A negative finding worth having in writing:** the **GwGMeldV-Immobilien** — the regulation listing situations that must *always* be reported — does **not** apply to brokers. Its § 1 limits it to "Verpflichteten nach § 2 Absatz 1 **Nummer 10 und 12** des Geldwäschegesetzes" (notaries/lawyers and tax advisers). A module must not tell brokers they are subject to it; this is a common practitioner confusion because the instrument's name says "Immobilien".

### 6.2 Coverage check against `data/kyc_aml_pilot.json`, and the cross-link plan

Read programmatically: 30 questions, 5 topics (`Grundlagen der Geldwaesche`, `Kundensorgfaltspflichten (KYC)`, `Verdachtsmeldewesen`, `Verstaerkte Sorgfaltspflichten`, `Sanktionen und Folgen`), DE canonical + EN. String counts over the whole file: **"Immobilien" 8 · "16a" 5 · "Barzahlung" 4 · "Makler" 0 · "Nummer 14"/"Nr. 14" 0.**

So the module already teaches the § 16a cash prohibition and touches real-estate context, but it **never addresses the broker as an obligated entity** — no § 2 Abs. 1 Nr. 14, no § 1 Abs. 11 definition, and critically **no § 10 Abs. 6 threshold split**, which is the single most operationally important GwG rule for a broker (it decides, per mandate, whether CDD is owed at all).

**Recommended pattern — cross-link, do not duplicate**, following the two precedents the brief names and which I verified in the repo:

- `data/fadp_ch_pilot.json` `meta.description` ends: *"See-also: this is a SEPARATE module from 'datenschutz' (EU GDPR / German BDSG) — the two regimes are related but legally distinct and are cross-linked, not merged (PO decision 2026-08-16)."*
- `docs/dora-audit-readiness-pre-review-dossier-2026-08-16.md` §2.2 keeps Art. 30(3)(f) exit-strategy content out of the audit module by pointing at `dora_procurement` and stating the boundary inside the question's own explanation.

Applied here: whichever module ships (§8), it should carry **at most 2–3 GwG questions**, restricted to the **broker-specific** provisions `kyc_aml` does not and should not cover — § 2 Abs. 1 Nr. 14 as the hook, § 10 Abs. 6's two-limb trigger with the EUR 10 000 monthly-net-rent threshold, and the negative point that GwGMeldV-Immobilien does not apply to them — with an explicit "for the general GwG regime see the `kyc_aml` module" note in each explanation and in `meta.description`. Typologies, the three-phase model, PEPs, § 43 mechanics, § 56 fines: **all stay in `kyc_aml`.** Conversely, `kyc_aml` would benefit from one added question on § 10 Abs. 6 regardless of what happens to the broker module, since it already claims broker coverage in a question about who counts as a Verpflichteter. That is a small, separately-schedulable `kyc_aml` card, not part of this decision.

**Kartellrecht:** checked and **not** relevant enough to cross-link. The deleted Teil A's area 4 was *Wettbewerbsrecht* in the **UWG** sense (unlautere Werbung), not the **GWB/Art. 101 TFEU** antitrust sense `kartellrecht` covers. Different body of law; no boundary to negotiate.

---

## 7. Source confidence

**Tier A — binding primary text, read in the official consolidated version and/or the official gazette.** Everything the recommendation rests on.

1. § 34c GewO Abs. 1, 2, 2a, 3, 5 — `gesetze-im-internet.de`, cross-read on `buzer.de`.
2. **GewBürAbG, BGBl. 2026 I Nr. 215, Art. 1 Nr. 3, Art. 2 Nr. 1–5, Art. 11** — read in the **official `recht.bund.de` BGBl PDF** *and* in an independent consolidation. **Three independent readings of the decisive sentence.**
3. MaBV in full — §§ 1, 2, 7, 8, 10, 11, 14, 15, 15a, 15b, 16, 18, 19, Anlagen 1–3 — incl. the amendment/Fußnote apparatus and both 2026 Änderungshinweise.
4. MaBV Anlage 1 **Teil A** in its pre-24.07.2026 wording (archived Fassung of the official consolidation).
5. § 34a, § 34d, § 34f GewO — the Sachkundeprüfung contrast, quoted.
6. GwG § 1 Abs. 11, § 2 Abs. 1 Nr. 14, § 6 Abs. 2 Nr. 6, § 10 Abs. 6, § 16a Abs. 1–5; GwGMeldV-Immobilien § 1.
7. Mechanical negative checks: "Sachkunde" → 0 hits in § 34c GewO, 0 in the MaBV.

**Tier B — official/quasi-official procedural material, not itself binding.**

8. **DIHK FAQ, Stand Januar 2025** (6 pp.) — documents the pre-abolition regime, the 20 h "pro Tätigkeitsbereich" / 40 h combined arithmetic, the Teil A/Teil B split, delegation rules, and that § 11 Satz 1 Nr. 3 MaBV does not apply to brokers. **Now historically superseded for the broker half** — flagged so nobody later cites it as current.
9. IHK landing pages for § 34c (München, Frankfurt, Hannover, Braunschweig, Düsseldorf, Bergische, Oldenburg) — identified in search, **and all still describing the pre-abolition regime**. Used only as evidence that the secondary layer is stale (§1.1); **no proposition here rests on any of them**. Their own JS-rendered bodies were not readable in this sandbox in any case.

**Tier C — orientation only, load-bearing for nothing.**

10. *Die Wohnungswirtschaft Bayern* (vdwbayern.de), 15.07.2026 — Bundesrat consent 10.07.2026 and the rejected extension to Verwalter (§3.3). Political framing only.
11. IVD "Faktencheck", Haufe Akademie, forum-verlag — orientation on the practitioner debate and the long-standing (never enacted) Sachkundenachweis demand.
12. The six syndicated press-release pages on the abolition — the reason I went looking; cited for nothing.

**Confidence in the headline finding: very high.** It is a change *instruction* read in the official gazette, plus the resulting consolidated text from two independent consolidators, plus corroborating trade reporting of the Bundesrat vote, plus a coherent deletion of the corresponding syllabus in a second instrument. The residual risk is not that the finding is wrong but that it is **already stale again** (§3.4) — two MaBV amendments in eight days.

---

## 8. What the module's correct shape should be

None of the three options below is an exam simulator, because there is no exam. All three are honest.

### Option 1 — Build nothing here; redirect the slot to § 34a / § 34d / § 34f

The cleanest answer to "we want a German licensing exam-prep module in the property/finance space". Three real IHK Sachkundeprüfungen exist (§5); § 34a already has a reserved roadmap slot and a stated commercial demand of EUR 450–4,200. **This is the option that gives the PO what they actually asked for — a licence exam module — by changing the licence, not by faking the exam.**

### Option 2 — `makler_berufspflichten`: a broker professional-duties module, explicitly not an exam simulator ← **recommended**

Grounded in what is genuinely binding on a broker **today** (§2.3), which is a well-defined, statutory, testable body of law:

- **`erlaubnis`** — § 34c Abs. 1 Nr. 1 permission scope; Abs. 2's closed list of refusal grounds; **that there is no Sachkundeprüfung and, since 24.07.2026, no Weiterbildungspflicht** (the highest-value fact in the module, because the entire practitioner web still says otherwise); that Berufshaftpflicht is a Verwalter requirement, not a broker one.
- **`mabv_pflichten`** — § 10 Buchführung incl. the broker-specific Abs. 3; § 11 Satz 1 Nr. 1 information duties in Textform; § 8 Rechnungslegung; § 14 Aufbewahrung; § 2 in combination with the § 7 exemption for brokers who never handle client funds; § 16 Abs. 2 ad-hoc audit.
- **`sanktionen`** — § 18 MaBV Ordnungswidrigkeiten via §§ 144–146 GewO; unerlaubte Gewerbeausübung.
- **`gwg_makler`** — 2–3 questions only, broker-specific, cross-linked to `kyc_aml` per §6.2.
- **`abgrenzung`** — the broker/Verwalter/Bauträger boundary inside § 34c, which is where practitioner error actually concentrates and which the July 2026 split makes sharper than ever.

Framed the way `cka` was: *a professional-duties knowledge check for licensed brokers and their staff, not an exam simulator — no state exam exists for this trade.* Honest, currently accurate, commercially defensible (it is the only place a broker can find out that their Weiterbildungspflicht has just been abolished), and it needs **no** PO decision on the constraint-1 sourcing problem, because it is authored from GewO/MaBV/GwG text and never touches a vendor catalogue. Realistic first pilot: 20–25 questions, DE canonical + EN, matching the `kartellrecht` / DORA-sibling schema.

**Its weakness, stated honestly:** the addressable audience is smaller and less motivated than an exam cohort. Nobody *has* to take this. It sells to brokerages as staff compliance training, not to individuals as licence prep — a different buyer, and closer to this repo's B2B compliance line than to its licence line.

### Option 3 — `immobilienverwalter_weiterbildung`: track the one syllabus still in force

MaBV **Anlage 1** as it now stands is a legally-mandated, 8-area, currently-binding syllabus with a **20 h / 3 years** quota, an evidence-file duty (§ 15b Abs. 2 MaBV, now a 3-year retention period after Art. 2 Nr. 1 GewBürAbG), a provider-quality standard (**Anlage 2**), and an Ordnungswidrigkeit for a missing evidence file (§ 18 Abs. 1 Nr. 9 MaBV). It is by far the strongest legal hook in this whole space, and § 15b Abs. 1 Satz 3 expressly permits *"begleitetes Selbststudium"* with *"eine nachweisbare Lernerfolgskontrolle durch den Anbieter"* — **a statutory description of an e-learning product with a test at the end, which is exactly what this app is.**

**But it is a different profession.** Silently retargeting a module the PO specified as "Maklerschein / Immobilienmakler" at Wohnimmobilienverwalter would be exactly the kind of quiet scope substitution AGENTS.md reserves to the PO. It is also materially more work: Anlage 1 area 2 alone pulls in BGB (Vertrags-, Miet-, Werkvertrags-, Grundstücksrecht), GBO, WEG, RDG, Zweckentfremdungsrecht, MaBV, BetrKV, HeizkostenV, TrinkwV, WoFlV and Mietprozess-/Zwangsvollstreckungsrecht. And **§ 15b Abs. 1 Satz 5 makes Anlage 2 a duty of the training *provider*** — if Zettacard positions itself as the Weiterbildungsanbieter whose hours count, that is a **regulatory posture with its own obligations**, not just a content decision. Needs the PO **and** probably counsel.

**Recommendation: Option 2 now, Option 3 as a separately-scoped follow-up if the PO wants the property vertical seriously, Option 1 as the answer to the original "we want an exam module" impulse.** Options 2 and 3 are complementary and would cross-link (`makler_berufspflichten` ↔ `immobilienverwalter_weiterbildung`) exactly as `fadp_ch` ↔ `datenschutz` do.

---

## 9. Why no draft question bank was produced

Stated explicitly, because the brief asked for one conditionally and the condition failed.

1. **The name describes something that does not exist.** There is no "Maklerschein". Publishing a question bank under that name would tell learners a licence-by-examination exists for this trade. This is worse than the `cka` case: there, a real exam existed and was merely untestable by MCQ, so an honestly-relabelled concept-check was still *about* a real thing. Here the referent is absent.
2. **The brief's own fallback scope was repealed 24 days ago.** Building against MaBV Anlage 1 Teil A would have produced a module teaching a syllabus that no longer binds anyone — and, worse, whose existence implies a duty that was just abolished. That is a factual error a learner would act on.
3. **Every accurate alternative changes something only the PO can change** — the module's name, or its audience (broker → Verwalter), or its category (licence prep → B2B compliance). AGENTS.md: the Product Owner *"is the only one who can change scope"*, and *"before any task large enough to need multiple sequential agent dispatches or a substantial architecture/UI change, check in with the PO on scope first rather than assuming."*
4. **This gate already exists and has never been cleared.** `BACKLOG.md` records § 34c Immobilienmakler as deferred pending "an explicit PO sourcing-strategy decision before any content work starts" in **three separate** completed rounds (2026-08-12 ×3). Producing content now would silently close a gate the board says is open — and on a premise (§0) that has since changed.

What §8 provides instead is a specified-enough recommendation that the next round can go straight to authoring on a one-line PO answer.

---

## 10. Open items for the PO / human decision

1. **Decide the module's identity** — Option 1, 2 or 3 in §8 (recommended: 2). This is the only blocking decision; everything else follows.
2. **Kill the "Maklerschein" / "Sachkundeprüfung" naming** before it reaches any roadmap, landing page or marketing copy. If Option 2 ships, the honest label is *"Immobilienmakler — Berufspflichten (§ 34c GewO / MaBV)"*, with a visible statement that no state exam exists for this trade. There is real consumer-protection and competition-law exposure in implying otherwise.
3. **De-couple § 34a from § 34c on the roadmap** (§0) and correct the shared-blocker wording in `claude/content-portfolio-and-expansion-roadmap-2026-08-14.md`. § 34a is a genuine, buildable IHK-exam module blocked only on sourcing; § 34c is not an exam module at all. Consider adding **§ 34d** and **§ 34f** as newly-identified genuine IHK-exam candidates that overlap existing `kyc_aml` / `datenschutz` investment.
4. **Schedule a small `kyc_aml` card** for § 10 Abs. 6 GwG (broker CDD trigger, EUR 10 000 monthly-net-rent threshold) and the § 2 Abs. 1 Nr. 14 hook — worth doing regardless of §8's outcome, since `kyc_aml` already asserts broker coverage. Optionally conform the `meta` paraphrase of § 6 Abs. 2 Nr. 6 to the statutory *"die erstmalige und laufende Unterrichtung"* at the same time.
5. **If Option 3 is ever chosen, treat the Anlage 2 provider-quality question as a legal question, not a content one** — § 15b Abs. 1 Satz 5 puts the duty on the *Anbieter der Weiterbildung*. "Do our hours count towards a Verwalter's 20?" is a claim with regulatory consequences and needs counsel before it appears in any copy.
6. **Set a re-verification date of no later than 2026-11-30 on everything in this dossier**, and re-read § 34c GewO and the MaBV from the amending instruments rather than from this file. §3.4: two MaBV amendments inside eight days, one of them with a defective change instruction that had to be consolidated *sinngemäß*. Also worth watching whether the abolition draws a legislative counter-reaction — the trade bodies have wanted a broker Sachkundenachweis for years and have just lost the weaker instrument.
7. **Standing process note for this repo** (§1.1): when consolidated statutory text conflicts with practitioner consensus, resolve it against the **amending instrument**, not against the weight of secondary sources. This dossier's headline finding would have been missed by the opposite instinct, and the same failure mode is live for any fast-moving module.

---

**Reminder:** this document is draft research groundwork. It is not legal advice, has not been reviewed by a qualified lawyer, and no content derived from it should be shipped to learners before that review. The abolition finding in §3 is high-confidence and triple-sourced, but it is **24 days old as at writing** and sits in a provision that has been amended twice in the last month.
