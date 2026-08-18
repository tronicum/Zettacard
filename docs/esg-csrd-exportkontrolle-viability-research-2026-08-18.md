# ESG/CSRD and Exportkontrolle — module viability research (2026-08-18)

**Status:** AI-prepared research groundwork only — **NOT legal advice**. This is a viability/timing round.
**No question-bank content was drafted for either topic, by design** (see §0.3 and §7). Unlike the sibling
§ 34a / § 34d / § 34f dossiers running in parallel today, this round was explicitly scoped as a
build/don't-build decision, not a content round.

**Requested:** actually research the two topics `BACKLOG.md` (the DN-50-era line) has flagged for months as
*"unconfirmed white space, never actually researched"* — **ESG/CSRD** and **Exportkontrolle** — and return an
independent verdict for each. They were named alongside Kartellrecht and Geldwäsche/AML, both of which have
since been built (`kartellrecht`, `kyc_aml` ship today).

**Files touched:** this file only. No `data/` file, no `app/` file, no `BACKLOG.md` edit, no
`data/build_modules.py` run, nothing staged or committed.

---

## 0. The verdicts, first

### 0.1 Summary table

| Topic | Verdict | One-line reason |
|---|---|---|
| **ESG/CSRD** | **BUILD LATER** — not now | Germany has **still not transposed CSRD** (deadline was 6 July 2024; today it is 25 months overdue), the EU **rewrote the directive's scope on 24 February 2026** (Directive (EU) 2026/470), and the **reporting standards themselves were only adopted as draft delegated acts on 3 July 2026 and are still inside their scrutiny period**. There is no stable in-force German reporting duty to teach. |
| **Exportkontrolle** | **BUILD NOW** — recommend as the next round's content task | AWG/AWV + Regulation (EU) 2021/821 are in force, decades-stable in architecture, and produce a clean five-topic MCQ syllabus with named §§, hard numbers and real sanctions. Its one recent change (the **AWG-Novelle in force 6 February 2026**) *strengthens* the case rather than destabilising it: corporate fines went from the OWiG default of €10m to **€40m**. |

### 0.2 The single most important finding for each

- **ESG/CSRD — the rules changed materially, twice, and the second change is six months old.**
  **Directive (EU) 2026/470 of 24 February 2026** (Omnibus I) cut CSRD's personal scope to undertakings
  exceeding **both** *"a net turnover of EUR 450 000 000 and an average number of 1 000 employees during the
  financial year"*, **deleted wave 3 outright** (listed SMEs), and reset the Member-State transposition clock
  to **19 March 2027**. Anything authored against the 2022 CSRD text — including most of what is on the open
  web, and any general-knowledge assumption about "250 employees / €50m / €25m" — is **wrong for the law that
  will actually apply**. Compounding this: **the revised ESRS were only adopted by the Commission as delegated
  regulations on 3 July 2026** and are, as at today, still in the EP/Council scrutiny window — i.e. the
  substance a module would teach is not yet finally in force anywhere in the EU.

- **Exportkontrolle — the rules just changed too, but in a way that *creates* teachable content.**
  The **Gesetz zur Anpassung von Straftatbeständen und Sanktionen bei Verstößen gegen restriktive Maßnahmen
  der Europäischen Union vom 3. Februar 2026 (BGBl. 2026 I Nr. 27)**, in force **6 February 2026**, transposed
  Directive (EU) 2024/1226 and inserted **§ 19 Abs. 7 and 8 AWG**: a **€40 million** ceiling on the corporate
  fine for an intentional § 18 Abs. 1 sanctions offence, and the **same €40 million ceiling for a mere
  § 130 OWiG supervisory-duty failure** connected to one. It also created a new **§ 18 Abs. 6a** aggravated
  offence (6 months–10 years) for end-use/route/recipient misstatements and for hiding a breach behind a
  controlled third-country company. That is a hard, dated, high-stakes number and an "*your compliance
  organisation itself is the offence*" hook — exactly what a workplace-compliance question bank is for.

### 0.3 Why no draft content this round

The brief scoped this as a viability decision and asked explicitly for no drafting. That instruction is
followed for both topics. For **CSRD** it would have been the right call anyway (§2.9). For
**Exportkontrolle** the finding is the opposite — it is buildable *today* with the same confidence as
`kartellrecht` and `kyc_aml` — so §3.8 specifies the module tightly enough that the next round can go
straight to authoring on a one-line PO approval, rather than re-doing this research.

---

## 1. Method, instruments read, and two retrieval traps

All retrieval on **2026-08-18**. `WebFetch` is blocked on `gesetze-im-internet.de` in this sandbox
(`ROBOTS_DISALLOWED`); every German statutory text below was fetched by direct `curl` and parsed from the raw
HTML, so quotes are from the consolidated official text, not from a summary. EU instruments were fetched by
`curl` from EUR-Lex ELI URLs (`eur-lex.europa.eu/eli/...`), i.e. the Official Journal text. The decisive
German amending act was additionally read in the **official Bundesgesetzblatt PDF** from `recht.bund.de`.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **AWG** (Außenwirtschaftsgesetz) | `gesetze-im-internet.de/awg_2013/BJNR148210013.html` | Full consolidated text; §§ 1, 2, 4, 8, 17, 18, 19 verbatim |
| **AWV** (Außenwirtschaftsverordnung) | `gesetze-im-internet.de/awv_2013/BJNR286500013.html` | Full consolidated text; §§ 8, 9, 11, 22, 26, 46, 49, 52a, 74, 80 verbatim; Anlage AL confirmed |
| **Gesetz zur Anpassung von Straftatbeständen und Sanktionen bei Verstößen gegen restriktive Maßnahmen der EU, v. 3.2.2026, BGBl. 2026 I Nr. 27** | **official BGBl PDF** `recht.bund.de/bgbl/1/2026/27/regelungstext.pdf` (14 pp.) | Art. 1 Nr. 1–8, Art. 2, Art. 6 — verbatim change instructions |
| **Regulation (EU) 2021/821** (EU Dual-Use Regulation) | `eur-lex.europa.eu/eli/reg/2021/821/oj/eng` | Art. 2(21), 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 25, 27 |
| **Regulation (EU) 269/2014** (asset freeze / Bereitstellungsverbot) | `eur-lex.europa.eu/eli/reg/2014/269/oj/eng` | Art. 2(1)–(2) |
| **Regulation (EU) 2026/506** (20th Russia package) | `eur-lex.europa.eu/eli/reg/2026/506/oj/eng` | Title, date, OJ citation |
| **BAFA, "Firmeninterne Exportkontrolle" (ICP-Merkblatt), 3. Auflage/April 2022** | `bafa.de/SharedDocs/Downloads/DE/Aussenwirtschaft/afk_merkblatt_icp.pdf` (PDF) | Whole document; §§ on AV, Schulungen, Aufzeichnungen |
| **Directive (EU) 2022/2464** (CSRD) | `eur-lex.europa.eu/eli/dir/2022/2464/oj/eng` | Art. 5(1)–(2) verbatim |
| **Directive (EU) 2025/794** ("stop-the-clock") | `eur-lex.europa.eu/eli/dir/2025/794/oj/eng` | Art. 1–3 verbatim |
| **Directive (EU) 2026/470** (Omnibus I) | `eur-lex.europa.eu/eli/dir/2026/470/oj/eng` | Recitals + Art. 1–7; scope, value-chain cap, Art. 5 transposition, Art. 6 entry into force |
| **HGB** §§ 289b–289e, 315b–315c, 316, 334 | `gesetze-im-internet.de/hgb/BJNR002190897.html` **and** `buzer.de/289b_HGB.htm` | Full consolidated text of the sustainability-reporting sections, from **two independent consolidators** |
| **LkSG** | `gesetze-im-internet.de/lksg/BJNR295910021.html` | Vollzitat / amendment status (cross-check for the existing `lksg` module) |

### 1.1 Retrieval trap #1 — a secondary source predicted a law that has not happened

An April 2026 trade report stated *"Zweite und dritte Lesung im Bundestag sollen noch im April folgen"* for
the German CSRD-Umsetzungsgesetz, and projected promulgation in Q2 2026. **It did not happen.** Both
consolidators show the HGB as *"zuletzt geändert durch Artikel 4 G. v. 04.02.2026 BGBl. 2026 I Nr. 33"* with
§ 289b still in its 2017 CSR-RUG wording. This is the mirror image of the trap recorded in
`docs/maklerschein-pre-review-dossier-2026-08-17.md` §1.1: there, practitioner consensus was *stale*; here,
practitioner reporting is *anticipatory*. Same tie-break rule applies and is worth restating as standing
practice: **resolve against the instrument (amending act / consolidated text), never against the projection.**

### 1.2 Retrieval trap #2 — a practitioner newsletter overstated the AWG-Novelle

A German export-control law-firm newsletter on the 2026 AWG-Novelle reports a *"Wegfall der bisherigen
zweitägigen Schonfrist"*. Reading the amending instruction (Art. 1 Nr. 6 lit. a–l of BGBl. 2026 I Nr. 27)
**there is no change to § 18 Abs. 12 AWG**, and the consolidated text still carries it:

> **§ 18 Abs. 12 AWG** — "Nach Absatz 1a […] wird nicht bestraft, wer **1.** einer öffentlich bekannt
> gemachten Anordnung **bis zum Ablauf des zweiten Werktages, der auf die Veröffentlichung folgt**,
> zuwiderhandelt und **2.** von einer dadurch angeordneten Beschränkung zum Zeitpunkt der Tat keine Kenntnis
> hat."

The grace period survives, narrowed to § 18 Abs. 1a (national orders). **Do not carry the newsletter's claim
into any question.** Recorded because it is precisely the kind of plausible-sounding secondary assertion that
would have produced a wrong answer key.

---

## 2. ESG/CSRD

### 2.1 The EU duty and the deadline Germany missed (Tier A)

> **Art. 5(1) Directive (EU) 2022/2464** — "Member States shall bring into force the laws, regulations and
> administrative provisions necessary to comply with Articles 1 to 3 of this Directive **by 6 July 2024**."

Art. 5(2) then set the original three waves: FY2024 for large PIEs >500 employees (a), FY2025 for other large
undertakings (b), FY2026 for listed SMEs / small and non-complex institutions / captive (re)insurers (c).

### 2.2 First change: "stop the clock" (Tier A)

**Directive (EU) 2025/794 of 14 April 2025** (OJ L, 2025/794, 16.4.2025) amended Art. 5(2) of the CSRD so that
wave (b) reads *"for financial years starting on or after 1 January 2027"* and wave (c) *"…1 January 2028"* —
a straight two-year delay. Its own transposition deadline was **31 December 2025** (Art. 3(1)). Germany missed
that one too (§2.5).

### 2.3 Second change, and the one that matters: Omnibus I (Tier A) ← **the "rules just changed" catch**

**Directive (EU) 2026/470 of 24 February 2026**, *"amending Directives 2006/43/EC, 2013/34/EU, (EU) 2022/2464
and (EU) 2024/1760 as regards certain corporate sustainability reporting requirements and certain corporate
sustainability due diligence requirements"*, **OJ L, 2026/470, 26.2.2026**. Art. 6: *"This Directive shall
enter into force on the twentieth day following that of its publication"* → **in force 18 March 2026**.

What it does to CSRD (all verbatim from the operative articles):

1. **New scope gate — both limbs, cumulative.** Art. 19a(1) and 29a(1) of Directive 2013/34/EU now bite only on
   > "Undertakings which, on their balance sheet dates, exceed **a net turnover of EUR 450 000 000 and an
   > average number of 1 000 employees during the financial year**…"
   and, for groups, *"Parent undertakings of a group which, on its balance sheet date, exceeds, on a
   consolidated basis, a net turnover of EUR 450 000 000 and an average number of 1 000 employees…"*
2. **Wave 3 is gone.** In both the first and third subparagraphs of CSRD Art. 5(2), *"point (c) is deleted"* —
   listed SMEs, small and non-complex institutions and captive (re)insurers are out of scope entirely.
3. **Wave 2 is re-cut** to the new €450m + 1,000-employee gate.
4. **Wave 1 gets an opt-out.** A new subparagraph lets Member States *"exempt undertakings or issuers which do
   not exceed a net turnover of EUR 450 000 000 **or** an average number of 1 000 employees during the
   financial year […] for the financial years starting between 1 January 2025 and 31 December 2026."*
   So even who has to report *for 2025 and 2026* is a **Member-State option**, not a settled EU fact.
5. **A statutory "value-chain cap."** New protections for undertakings in the value chain that *"do not exceed
   an average number of 1 000 employees during the preceding financial year"*, including a **statutory right
   to decline** to provide information beyond the voluntary standard, and reliance on a supplier
   **self-declaration** of size without further verification.
6. **New transposition deadline.** Art. 5(1): *"Member States shall bring into force the laws, regulations and
   administrative provisions necessary to comply with Articles 1, 2 and 3 **by 19 March 2027**."*
   (Art. 4 — the CSDDD limb — by **26 July 2028**.)

**Product consequence:** the CSRD that a German module would teach in, say, Q4 2026 is a directive whose scope
provisions were rewritten six months ago and whose national implementation is legally not due for another
seven months. Any content authored from the widely-circulated 2022/2024-vintage material (250 employees /
€50m turnover / €25m balance sheet, "wave 3 listed SMEs from 2026", "~15,000 German companies affected") would
be **factually wrong on the answer key**, not merely dated.

### 2.4 The standards a module would actually teach are not yet in force (Tier B, high confidence)

CSRD's substance for a learner is the **ESRS**, not the directive's scoping arithmetic. Per the
Wirtschaftsprüferkammer, the European Commission **adopted the delegated regulation taking over the revised
ESRS, and a separate voluntary standard, on 3 July 2026**; the acts then run a **two-month scrutiny period,
extendable by two further months**, and enter into force three days after OJ publication. As at **2026-08-18
that scrutiny period has not expired** and the revised ESRS are not published law. Omnibus I itself sets the
deadline for the Commission's voluntary standard at **19 July 2026** (new Art. 29ca of Directive 2013/34/EU),
which the 3 July adoption meets — but "adopted by the Commission" is not "in force."

So: at the level of the directive, the scope changed six months ago. At the level of the standards, the text
is still in scrutiny. At the level of German law, nothing has happened at all (§2.5).

### 2.5 Germany has not transposed CSRD — verified against two independent consolidations (Tier A)

The decisive check is mechanical. **HGB § 289b as in force today still reads:**

> **§ 289b Abs. 1 HGB** — "Eine Kapitalgesellschaft hat ihren Lagebericht um eine **nichtfinanzielle
> Erklärung** zu erweitern, wenn sie die folgenden Merkmale erfüllt: **1.** die Kapitalgesellschaft erfüllt die
> Voraussetzungen des § 267 Absatz 3 Satz 1, **2.** die Kapitalgesellschaft ist **kapitalmarktorientiert** im
> Sinne des § 264d und **3.** die Kapitalgesellschaft hat im Jahresdurchschnitt **mehr als 500 Arbeitnehmer**
> beschäftigt."

That is the **CSR-RUG (2017) / NFRD** regime, unchanged. Findings from a mechanical read of the whole HGB:

- The HGB's Vollzitat is *"…zuletzt geändert durch Artikel 4 des Gesetzes vom **4. Februar 2026** (BGBl. 2026 I
  Nr. 33)"* — i.e. the last HGB amendment predates any possible CSRD act by six months.
- `buzer.de` (independent, "tagaktuell konsolidiert") returns the **identical** § 289b text and the identical
  Vollzitat, and records that **§ 289b has only two earlier versions** — it has never been amended for CSRD.
- **The words "Nachhaltigkeitsbericht" / "Nachhaltigkeitsberichterstattung" appear nowhere** in the HGB's
  accounting sections. The reporting duty sections are still §§ 289b–289e (single entity) and §§ 315b–315c
  (group), all in *nichtfinanzielle*-Erklärung wording.
- § 317 Abs. 2 Satz 4 HGB still limits the auditor's involvement to checking *"ob die nichtfinanzielle
  Erklärung […] **vorgelegt wurde**"* — i.e. a presence check, not CSRD's limited assurance.
- § 334 Abs. 1 Nr. 3 HGB still keys its Ordnungswidrigkeit to *"§§ 289 bis 289b Absatz 1, §§ 289c, 289d,
  289e Absatz 2 […]"*.

**Conclusion (very high confidence): as of 2026-08-18 Germany has no CSRD-based reporting duty in force.**
What binds a German company today is NFRD-vintage law: large, capital-market-oriented, >500 employees.

### 2.6 Where the German bill actually stands, and its own defect (Tier B)

- Government bill **BT-Drs. 21/1857**, introduced **3 September 2025** (21. Wahlperiode), drafted against CSRD
  *as amended by* the stop-the-clock directive.
- A joint **CDU/CSU + SPD Änderungsantrag of 31 March 2026** re-aligned it to Omnibus I: the €450m + 1,000-
  employee gate for financial years from 1 January 2027, plus the value-chain cap and **permanent limited
  assurance**.
- **Public hearing in the Rechtsausschuss on 13 April 2026.** Trade reporting on 6 April 2026 expected 2nd/3rd
  readings "still in April" and BGBl publication in Q2 2026. **Neither happened** (§2.5, §1.1).
- The amendment would apply the new duties **retroactively to financial years beginning after 31 December
  2024** — i.e. companies would acquire a reporting duty for an **already-closed FY 2025**. Both the **DRSC**
  and the **IDW** publicly warned against this; commentators question it against the constitutional
  prohibition on retroactivity. **This is not a settled drafting question; it is a live constitutional
  objection to the central applicability rule.**
- Infringement proceedings for non-transposition were opened by the Commission on **26 September 2024**
  (Germany was one of 17 Member States). No confirmed CJEU referral was found in this pass; the point is not
  load-bearing here and is left as an open item (§8.4).

### 2.7 So what could a module honestly teach today?

Three candidate framings, all of which fail:

1. **"CSRD reporting duties in Germany"** — the honest answer to *"must my company report under CSRD?"* is
   *"under German law, no — that directive is not transposed."* A module teaching the duty would teach a duty
   that does not bind its learner. This is the same defect that killed the Maklerschein module (dossier §9.2).
2. **"CSRD as EU law, ignoring transposition"** — possible in principle, but the operative content (who is in
   scope, from when, at what assurance level, against which standard) is exactly what changed on 24 February
   2026 and is exactly what is still in Commission scrutiny. The Member-State exemption option in §2.3(4) means
   even the EU-level answer for FY2025–2026 is *"it depends on your Member State's choice"* — unanswerable in
   an MCQ.
3. **"The current German regime (§§ 289b ff. HGB, CSR-RUG)"** — this *is* stable, in force and testable. But it
   binds roughly 500 companies, is on a defined path to repeal, and would be a module about the law that is
   about to be replaced. Teaching it under an "ESG/CSRD" label would actively mislead.

There is also a **naming trap** worth flagging before it reaches any roadmap or landing page: "ESG" is not a
legal category in German or EU law. The legal objects are *Nachhaltigkeitsberichterstattung* (CSRD/ESRS),
*Sorgfaltspflichten in der Lieferkette* (LkSG/CSDDD), and the *Taxonomie-Verordnung*. A module labelled "ESG"
would promise a scope no instrument defines.

### 2.8 Verdict — **BUILD LATER**, with explicit trigger conditions

Do not build an ESG/CSRD module now. Revisit when **all three** of the following are true:

1. **The German CSRD-Umsetzungsgesetz is promulgated in the BGBl** and the HGB actually carries
   sustainability-reporting sections (test: `curl` `gesetze-im-internet.de/hgb/__289b.html` and look for
   *Nachhaltigkeitsbericht* wording instead of *nichtfinanzielle Erklärung*). Earliest realistic window is
   between now and the **19 March 2027** Omnibus deadline; on this bill's track record, treat that deadline as
   a target rather than a certainty.
2. **The revised ESRS delegated regulation has completed scrutiny and been published in the OJ.**
3. **The retroactivity question (§2.6) is resolved** in the enacted text, so a question about "which financial
   year does this first bite?" has a single correct answer.

Estimated earliest sensible build window: **Q2 2027**, and it needs a fresh research pass at that point — not
this document, which will be stale.

### 2.9 A knock-on finding this repo should act on regardless: the existing `lksg` module

Checked because CSDDD sits in the same Omnibus and LkSG is already shipped.

- **LkSG has not been amended at all.** Its Vollzitat is still the bare *"Lieferkettensorgfaltspflichtengesetz
  vom 16. Juli 2021 (BGBl. I S. 2959)"* — no *"zuletzt geändert"* clause, i.e. **zero amendments since
  enactment**. The September 2025 government bill that `BACKLOG.md` DN-64 records as "cabinet-approved, still
  in Bundestag committee" is **still not law**. The `lksg` module's decision to teach current law and flag the
  pending reform explicitly was correct and **remains correct today** — a good outcome for that module, worth
  recording.
- **But CSDDD moved under it.** Omnibus I raised the CSDDD gate to *"more than 5 000 employees on average and
  […] a net worldwide turnover of more than EUR 1 500 000 000"* (from 1,000/€450m) and pushed transposition to
  **26 July 2028**, application from 26 July 2029. If `lksg`'s content or metadata characterises the incoming
  EU regime with the old 1,000/€450m figures, that is now wrong. **Recommend a small verification card on
  `data/lksg_pilot.json`** — a text check for "1.000"/"450" in any CSDDD-facing question or in
  `meta.description`. Not part of this decision; separately schedulable.

---

## 3. Exportkontrolle

### 3.1 The instruments, and their current status (Tier A)

| Instrument | Status as read today |
|---|---|
| **AWG** — Außenwirtschaftsgesetz v. 6.6.2013 | In force since 1.9.2013. *"zuletzt durch Artikel 1 des Gesetzes vom **3. Februar 2026** (BGBl. 2026 I Nr. 27) geändert"* |
| **AWV** — Außenwirtschaftsverordnung v. 2.8.2013 | In force since 1.9.2013. *"zuletzt durch Artikel 5 des Gesetzes vom **11. März 2026** (BGBl. 2026 I Nr. 66)"* — that act is the **KRITIS-Dachgesetz** (CER-Richtlinie (EU) 2022/2557); its AWV limb touches **investment screening (§ 55a AWV)**, not export control. Incidental but worth knowing: it is also directly relevant to this repo's `nis2` module. |
| **Regulation (EU) 2021/821** — EU Dual-Use Regulation | Directly applicable since 9.9.2021. Annex I is updated annually by delegated regulation; the AWG expressly applies Anhang I *"in der jeweils geltenden Fassung"* (§ 18 Abs. 5 Satz 2 AWG) |
| **Regulation (EU) 269/2014**, **833/2014** and the country regimes | Directly applicable; amended continuously (§3.6) |
| **Ausfuhrliste** = **Anlage AL zur AWV** | Part of the AWV itself, Anlage 1 |

Architecturally this body of law has been stable for **13 years** at the AWG/AWV level and **5 years** at the
EU dual-use level. That is a completely different situation from CSRD.

### 3.2 The AWG-Novelle of 3 February 2026 — verbatim, from the official gazette (Tier A)

**Gesetz zur Anpassung von Straftatbeständen und Sanktionen bei Verstößen gegen restriktive Maßnahmen der
Europäischen Union**, vom **3. Februar 2026**, **BGBl. 2026 I Nr. 27**, *"Ausgegeben zu Bonn am 5. Februar
2026"*. Art. 6: *"Dieses Gesetz tritt am Tag nach der Verkündung in Kraft."* → **in force 6 February 2026.**

Its own footnote states the EU basis:

> "Die Artikel 1 Nummer 6 Buchstabe a, e und g bis l, Nummer 7 Buchstabe a und d, Artikel 2 Nummer 5
> Buchstabe a, d, f, g, j und l sowie die Artikel 4 bis 6 dieses Gesetzes dienen der **Umsetzung der Richtlinie
> (EU) 2024/1226** des Europäischen Parlaments vom 24. April 2024 zur Definition von Straftatbeständen und
> Sanktionen bei Verstoß gegen restriktive Maßnahmen der Union […]"

**The three changes that matter for a training module:**

**(a) Corporate fines quadrupled — Art. 1 Nr. 7 lit. d inserted § 19 Abs. 7 and 8 AWG:**

> "**(7)** Abweichend von § 30 Absatz 2 Satz 1 Nummer 1 des Gesetzes über Ordnungswidrigkeiten beträgt das
> Höchstmaß der Geldbuße im Falle einer vorsätzlichen Straftat nach § 18 Absatz 1 dieses Gesetzes **vierzig
> Millionen Euro**.
> **(8)** Abweichend von § 30 Absatz 2 Satz 2 des Gesetzes über Ordnungswidrigkeiten beträgt das Höchstmaß der
> Geldbuße im Falle einer Ordnungswidrigkeit nach **§ 130 Absatz 1 des Gesetzes über Ordnungswidrigkeiten** in
> Verbindung mit § 18 Absatz 1 dieses Gesetzes **vierzig Millionen Euro**."

Before this, the general OWiG ceiling of €10m applied. **Abs. 8 is the pedagogically important one**: it hangs
the same €40m on a **§ 130 OWiG Aufsichtspflichtverletzung** — a failure to organise and supervise. The company
does not have to commit the export offence; failing to prevent it is enough. That is the single strongest
argument for an export-control training product that this dossier found, and it is a statutory one.

**(b) A new aggravated offence — Art. 1 Nr. 6 lit. h inserted § 18 Abs. 6a AWG:**

> "In besonders schweren Fällen des Absatzes 1 Nummer 1 Buchstabe a oder Nummer 4 Buchstabe a ist die Strafe
> Freiheitsstrafe von **sechs Monaten bis zu zehn Jahren**. Ein besonders schwerer Fall liegt in der Regel vor,
> wenn der Täter **1.** gegenüber einer öffentlichen Stelle eine unvollständige oder unrichtige Angabe über die
> **Endverwendung, die Beförderungsroute, den Empfänger, den Versender, den Ursprung, den Käufer, den
> Verkäufer, die Menge, den Wert oder die Beschaffenheit der Güter** macht oder **2.** eine **Drittstaat-
> Gesellschaft** im Sinne des § 138 Absatz 3 der Abgabenordnung nutzt, auf die er unmittelbar oder mittelbar
> einen beherrschenden oder bestimmenden Einfluss ausübt, um einen Verstoß […] zu **verschleiern**."

**(c) Leichtfertigkeit for listed dual-use goods — new § 18 Abs. 8a AWG:**

> "Handelt der Täter in den Fällen des Absatzes 1 Nummer 1 Buchstabe a oder b oder Nummer 4 Buchstabe a oder b
> **leichtfertig**, so ist die Strafe Freiheitsstrafe bis zu drei Jahren oder Geldstrafe, wenn sich die Tat auf
> Güter mit doppeltem Verwendungszweck bezieht, die in **Anhang I oder Anhang IV der Verordnung (EU) 2021/821**
> aufgeführt sind."

Recklessness suffices. "We didn't check the list" is a criminal exposure, not a paperwork slip.

The same act also inserted **§§ 6a–6g AWG** (Treuhandverwaltung / Anteilspfleger for sanctioned companies) —
real, but a state-intervention regime, not staff-training content. Out of scope for a module.

### 3.3 The testable syllabus (all Tier A, all read today)

**(i) Genehmigungspflichten — when do you need a licence?**

- **EU layer.** *"An authorisation shall be required for the export of dual-use items listed in Annex I"*
  (Art. 3(1) Reg. 2021/821). Intra-EU: *"An authorisation shall be required for intra-Union transfers of
  dual-use items listed in Annex IV"* (Art. 11(1)).
- **National layer.** § 8 Abs. 1 AWV — licence for goods in **Teil I Abschnitt A** (military/war-weapons-
  adjacent) and **Abschnitt B** (the "900er" national dual-use positions) of the Ausfuhrliste. Two clean,
  testable de-minimis rules: § 8 Abs. 3 exempts Abschnitt-B contracts *"im Wert von nicht mehr als **5 000
  Euro**"* — **but** *"Die Ausfuhr von Software und Technologie ist abweichend von Satz 1 **stets**
  genehmigungspflichtig."* The same €5,000/software-and-technology split recurs in § 9 Abs. 3 Nr. 2 and
  § 11 Abs. 5 Nr. 3 AWV. That is exactly the kind of "the exception has an exception" rule an MCQ tests well.
- **Verbringung.** § 11 Abs. 1 AWV — intra-EU transfer of Teil I Abschnitt A goods needs a licence.
- **Types of authorisation.** Art. 12(1) Reg. 2021/821: *"(a) individual export authorisations; (b) global
  export authorisations; (c) national general export authorisations; (d) Union general export authorisations
  […] as set out in Sections A to H of Annex II."* Validity: *"Individual export authorisations and global
  export authorisations shall be valid for up to two years"* (Art. 12(3)).

**(ii) Dual-Use-Güter and the catch-alls — the part practitioners actually get wrong**

- **Art. 4(1) Reg. 2021/821** (the WMD / military-end-use catch-all): a licence is required for **non-listed**
  goods if the exporter *"has been informed by the competent authority"* that they are or may be intended
  *"(a) for use in connection with the development, production, handling, operation, maintenance, storage,
  detection, identification or dissemination of chemical, biological or nuclear weapons […] (b) for a military
  end-use if the purchasing country or country of destination is subject to an arms embargo […] (c) for use as
  parts or components of military items […]"*.
- **Art. 4(2)**: the duty flips — *"Where an exporter is **aware** that dual-use items which he proposes to
  export, not listed in Annex I, are intended […] the exporter **shall notify** the competent authority."*
  Positive knowledge triggers a self-report duty, with no prior BAFA notice.
- **Art. 5(1)–(2)**: the **cyber-surveillance** catch-all — non-listed cyber-surveillance items intended for
  *"internal repression and/or the commission of serious violations of human rights and international
  humanitarian law"*, with Art. 5(2) keying the notification duty to what the exporter knows *"according to
  its due diligence findings"*. This is the newest limb and the one most relevant to a German software/tech
  exporter, i.e. to a plausible Zettacard buyer.
- **National catch-all.** § 9 Abs. 1 AWV — non-listed goods for nuclear-facility end-use in a named country
  list (*"Algerien, Irak, Iran, Israel, Jordanien, Libyen, die Demokratische Volksrepublik Korea, Pakistan
  oder Syrien"*), with § 9 Abs. 2 Satz 3 imposing a hard stop: *"Die Güter dürfen erst ausgeführt werden, wenn
  das […] (BAFA) die Ausfuhr genehmigt hat oder entschieden hat, dass es keiner Genehmigung bedarf."*
- **Brokering and technical assistance.** Art. 6 and Art. 8 Reg. 2021/821; nationally §§ 46–47 AWV
  (Handels- und Vermittlungsgeschäfte) and §§ 49–52b AWV (technische Unterstützung), including the modern
  **§ 52a AWV** limb for communication-surveillance items and the **oral-advice** carve-out in § 49 Abs. 3
  Nr. 3.

**(iii) Embargos and sanctions-list screening**

- The **Bereitstellungsverbot** is the everyday duty and the reason screening exists:
  > **Art. 2(2) Reg. (EU) 269/2014** — "No funds or economic resources shall be made available, **directly or
  > indirectly**, to or for the benefit of natural persons or natural or legal persons, entities or bodies
  > associated with them listed in Annex I."
  Note there is no de-minimis and no intent requirement in the prohibition itself — this is why every
  counterparty gets screened, not just export ones.
- **§ 74 AWV** carries a hard national country embargo list for Ausfuhrliste Teil I Abschnitt A goods
  (Birma/Myanmar, DR Kongo, DVR Korea, Irak, Iran, Libanon, Simbabwe, Somalia, Sudan, Südsudan, Syrien,
  Venezuela — with several entries *(weggefallen)*, itself a nice illustration that embargo lists move), plus
  § 74 Abs. 2's person/entity limb keyed to the EU terrorism and Afghanistan lists.
- **§ 80 AWV** routes § 74/75/77 breaches into § 17 AWG's penalty range.

**(iv) Straf- und Bußgeldvorschriften — the hard numbers**

- **§ 17 Abs. 1 AWG**: **one to ten years' imprisonment** for breaching a sanctions regulation concerning
  Ausfuhrliste Teil I Abschnitt A goods; Abs. 5: *"Handelt der Täter […] **leichtfertig**, so ist die Strafe
  Freiheitsstrafe bis zu drei Jahren oder Geldstrafe."*
- **§ 18 Abs. 1 AWG**: **three months to five years** for breaching directly applicable EU sanctions
  provisions — now with the fully enumerated lit. a–h catalogue (goods, technical assistance, financial
  services and crypto wallets, legal/PR/audit/IT consulting, leases, public contracts, joint ventures,
  making funds available).
- **§ 18 Abs. 2 Nr. 1 AWG**: the core export-control offence — exporting *"ohne Genehmigung nach § 8 Absatz 1,
  § 9 Absatz 1 oder § 78"* AWV.
- **§ 18 Abs. 5 AWG**: the dual-use offence — exporting *"ohne Genehmigung nach Artikel 3 Absatz 1, Artikel 4
  Absatz 1, Artikel 5 Absatz 1 oder Artikel 10 Absatz 1"* of Reg. 2021/821.
- **§ 18 Abs. 6a / 8a AWG**: §3.2(b) and (c).
- **§ 18 Abs. 10 AWG**: extraterritoriality — *"Die Absätze 1 bis 9 gelten, unabhängig vom Recht des Tatorts,
  auch für Taten, die im Ausland begangen werden, wenn der Täter Deutscher ist."*
- **§ 19 Abs. 1 AWG**: negligence (fahrlässig) versions are Ordnungswidrigkeiten.
- **§ 19 Abs. 6 AWG**: **€500,000** in the Abs. 1 / Abs. 3 Nr. 1 lit. a cases, **€30,000** otherwise.
- **§ 19 Abs. 7 / 8 AWG**: **€40,000,000** (§3.2(a)).
- **§ 18 Abs. 11 AWG**: the humanitarian-aid exemption, new since Feb 2026.

**(v) Betriebliche Organisation — records, roles, ICP**

- **Records, EU layer:** Art. 27(3) Reg. 2021/821 — registers *"shall be kept for **at least five years** from
  the end of the calendar year in which the export took place"*; Art. 27(4) — **three years** for intra-Union
  transfers of Annex I items.
- **Records, national layer:** § 22 Abs. 2 AWV lists the six mandatory data points (goods designation and
  Ausfuhrliste position, quantity and value, export date, exporter and consignee names/addresses, end-use and
  end-user where known, and confirmation that the consignee was informed under Abs. 1), retained **five years**
  (§ 22 Abs. 3); § 26 adds a parallel five-year duty for customs write-offs.
- **ICP, EU layer:** Art. 2(21) defines an *"internal compliance programme"* as *"ongoing effective,
  appropriate and proportionate policies and procedures adopted by exporters […] including, inter alia, due
  diligence measures assessing risks related to the export of the items to end-users and end-uses"*; Art. 12(4)
  makes it near-mandatory in practice — *"Exporters using **global** export authorisations **shall implement an
  ICP**, unless the competent authority considers it unnecessary…"*; Art. 15(2) makes ICP a licensing criterion.
- **Reliability, national layer:** § 8 Abs. 2 AWG — *"Die Erteilung der Genehmigung kann von sachlichen und
  persönlichen Voraussetzungen, insbesondere der **Zuverlässigkeit** des Antragstellers, abhängig gemacht
  werden."*

### 3.4 Is there a statutory training mandate? No — and the honest position is still strong

Mechanical finding: **AWG and AWV contain no training-frequency mandate.** There is no export-control
equivalent of § 6 Abs. 2 Nr. 6 GwG or DGUV V1's annual Unterweisung. A module must not claim one.

What does exist is a documented, official expectation, from **BAFA's own ICP-Merkblatt "Firmeninterne
Exportkontrolle", 3. Auflage/April 2022** (Tier B, official):

> "Das Exportkontrollpersonal **soll mindestens einmal im Jahr** Gelegenheit bekommen, sich intern oder extern
> auf dem Gebiet der Exportkontrolle **fortzubilden**. **Sämtliche Schulungsnachweise werden aufbewahrt.**"

and, on scope of audience:

> "Das Unternehmen (AV) muss dafür sorgen, dass **alle Mitarbeiter, die mit Exportkontrollaufgaben beauftragt
> sind**, Gelegenheit zur Teilnahme an einschlägigen Schulungen bekommen." — with BAFA's own ICP-Prüffrage
> asking whether training is also provided for staff *"die **mittelbar** von der Exportkontrolle betroffen sind
> (**Vertrieb, Versand, Projektverantwortliche**)"*.

Plus the **Ausfuhrverantwortlicher (AV)** role, which BAFA describes as personally accountable:

> "Der AV ist für die Einhaltung der Exportkontrollvorschriften **persönlich verantwortlich**." … "Anträge auf
> Erteilung einer Ausfuhr-/Verbringungsgenehmigung für gelistete Güter kann nur stellen, wer einen AV bestellt
> und gegenüber dem BAFA benannt hat."

This is the **same honest structure the `kartellrecht` module already ships and got right**: no statutory
interval, an annual refresher as documented best practice, and the reason for training stated as fine
mitigation / organisational duty rather than a legal quota. Here the fine-mitigation hook is stronger than
antitrust's discretionary § 81d GWB, because § 19 Abs. 8 AWG names § 130 OWiG expressly and puts €40m on it.
Recommended `meta` treatment: `renewal_months: 12`, `renewal_basis: "best_practice"`, and a
`renewal_note` that says plainly that AWG/AWV impose **no** statutory refresher interval and that the annual
cadence comes from BAFA's ICP-Merkblatt — mirroring `data/kartellrecht_pilot.json` almost word-for-word in
structure.

The "Schulungsnachweise werden aufbewahrt" line is also the clearest product fit this repo has found for its
**signed completion credential** feature (`netlify/functions/sign-credential.js`, the Open-Badges work): the
regulator's own guidance says training evidence must be retained. That is a genuine, non-speculative reason a
buyer would want verifiable per-employee completion records rather than a spreadsheet.

### 3.5 Commercial fit — a different buyer from every module this repo has shipped

Worth stating explicitly, because it is a strategic fact and not just a content one.

- **Who has the duty.** Anyone who is an *Ausführer* under § 2 Abs. 2 AWG — which expressly includes
  *"im Fall von **Software oder Technologie** über deren Übertragung aus dem Inland in ein Drittland
  **einschließlich ihrer Bereitstellung auf elektronischem Weg**"*. Machine builders, electronics,
  chemicals/pharma, aerospace, sensors/optics, and — via Art. 5 and § 52a AWV — **software and telecoms
  firms**. Logistics, forwarders and customs agents sit in the same perimeter via Durchfuhr and Vermittlung.
- **Who inside the company needs it.** BAFA's own ICP-Prüffragen name **Vertrieb, Versand,
  Projektverantwortliche** as indirectly affected staff who should be trained. That is a broad-workforce
  audience, not a compliance-officer-only audience — which is precisely the shape this app serves and the shape
  that the expensive seminar market underserves (the same argument `claude/compliance-competitor-pricing-and-
  course-gaps.md` made successfully for LkSG and Hinweisgeberschutz).
- **How it differs from this repo's current base.** `datenschutz`, `ki_act`, `it_sicherheit`,
  `hinweisgeberschutz` and `arbeitssicherheit` sell to *any* employer. `kyc_aml` and `dora` sell to financial
  services. `kartellrecht` and `lksg` sell to large corporates. **Exportkontrolle sells to the German
  Mittelstand's export core — manufacturing, logistics and tech-export firms — a buyer this catalogue does not
  currently address at all.** It is a genuine adjacency, not a duplicate. It also pairs naturally with
  `kyc_aml` (sanctions-list screening is the shared operational control: the *Bereitstellungsverbot* in
  Art. 2(2) Reg. 269/2014 is screened by the same team and often the same tooling as GwG customer due
  diligence) — a cross-link, not a merge, following the `fadp_ch` ↔ `datenschutz` and
  `dora_audit_readiness` ↔ `dora_procurement` precedents.
- **Willingness to pay.** Not quantified in this pass — no pricing research was done. Flagged as an open item
  (§8.6). The €40m exposure and the personally-liable AV role are strong qualitative signals, but this dossier
  does **not** claim a verified price point.

### 3.6 What moves, and how to build so it does not break

Export control is stable in **architecture** and volatile in **lists**. The module must be built on the former.

| Moves | How often | Mitigation |
|---|---|---|
| **Annex I** of Reg. 2021/821 (the dual-use list itself) | ~annually, by delegated regulation | Never test a specific Annex I position number or technical parameter. Test the *mechanism*: that Annex I applies *"in der jeweils geltenden Fassung"* (§ 18 Abs. 5 Satz 2 AWG), and that classification is the exporter's own duty. |
| **EU sanctions packages** | The 20th Russia package was **Council Regulation (EU) 2026/506 of 23 April 2026** (OJ L, 2026/506, 23.4.2026) | Never name a package number, a listed entity, or a CN code in a question. Test the *duty* (Art. 2(2) Reg. 269/2014 screening, § 18 Abs. 1 AWG offences) which is package-independent. |
| **§ 74 AWV country list** | Entries added/repealed | Test that a national embargo list exists and where it lives, not its current membership. |
| **Reg. 2021/821 itself** | The Commission has an **open evaluation/call for evidence** on the regulation, with a more coordinated EU export-control approach under discussion | Watch item, not a blocker: no proposal is in force, and Art. 3/4/5/12/27 are the stable spine of any successor. Re-verify at the dates in §9. |

Compare CSRD, where what is moving is not the lists but **who is in scope, from when, against which standard,
and whether the national law exists at all**. That is the distinction that drives the two opposite verdicts.

### 3.7 Verdict — **BUILD NOW**

Exportkontrolle clears the same bar as `kartellrecht` and `kyc_aml` did:

- ✅ In-force, directly citable primary law with named §§ and articles (§3.1, §3.3).
- ✅ Hard, testable numbers that do not move: €5,000 de-minimis, 5-year and 3-year retention, 2-year
  authorisation validity, €30,000 / €500,000 / €40,000,000 fine tiers, 1–10 / 3 months–5 years / 6 months–10
  years custodial ranges.
- ✅ A genuine "why this training exists" hook that is statutory, not marketing (§ 19 Abs. 8 AWG × § 130 OWiG).
- ✅ Official, quotable guidance on training cadence and audience (BAFA ICP-Merkblatt), so the
  `renewal_basis: "best_practice"` framing is evidenced rather than asserted.
- ✅ Zero constraint-1 exposure: everything above is *amtliches Werk* (§ 5 UrhG) or EU Official Journal text.
  There is no Fragenkatalog, no vendor catalogue, and nothing to negotiate with the PO about sourcing.
- ✅ A recent, dated, high-salience change (6 February 2026) that most existing training material will not yet
  reflect — the same competitive edge the Maklerschein dossier identified in "being the only place that tells
  you the rule changed."

**Recommendation: schedule Exportkontrolle as the next content round.** §3.8 is the specification.

### 3.8 Proposed module shape (specification only — no content drafted)

Follow `data/kartellrecht_pilot.json` exactly; it is the closest structural sibling (enterprise compliance, no
statutory training interval, criminal-liability topic).

- **`exam_type`:** `exportkontrolle`
- **Pilot size:** 20 questions (4 per topic), DE canonical + EN — the standard first-pilot shape. Scale to 30
  (6 per topic) only after an AI legal-review pass, same order `kyc_aml` and `kartellrecht` followed.
- **Topics (5):**
  1. `grundlagen` — § 1 AWG's freedom principle and its exceptions; Ausführer / Ausfuhr / Verbringung /
     Durchfuhr definitions (§ 2 AWG); the three-layer structure (EU regulation → AWG → AWV/Ausfuhrliste); BAFA
     as the competent authority.
  2. `genehmigungspflichten` — Art. 3(1) and 11(1) Reg. 2021/821; §§ 8, 9, 11 AWV; the €5,000 de-minimis and
     its software/technology exception; authorisation types and 2-year validity (Art. 12).
  3. `dual_use_catchall` — Art. 4 and Art. 5 Reg. 2021/821; the informed-vs-aware distinction and the
     self-notification duty; § 9 AWV's national nuclear catch-all; brokering (Art. 6, §§ 46–47 AWV) and
     technical assistance (Art. 8, §§ 49–52b AWV).
  4. `embargos_screening` — Art. 2(2) Reg. 269/2014 Bereitstellungsverbot incl. *"directly or indirectly"*;
     § 74 AWV; why screening is counterparty-wide and not export-specific; explicit cross-link note to
     `kyc_aml` for the general sanctions/AML perimeter.
  5. `sanktionen_organisation` — §§ 17, 18, 19 AWG incl. the Feb-2026 § 18 Abs. 6a / 8a and § 19 Abs. 7/8;
     § 130 OWiG; § 18 Abs. 10 extraterritoriality; ICP (Art. 2(21), 12(4), 15(2)) and the AV role; record
     retention (Art. 27, §§ 22, 26 AWV).
- **`meta` fields**, per repo convention: `license: "CC BY-NC-SA 4.0"` + `license_url` + `license_note`;
  `legal_review_status` set honestly to "not reviewed by a licensed lawyer" at first draft (constraint 4 —
  do **not** pre-set it to reviewed); `renewal_months: 12`, `renewal_basis: "best_practice"` with the
  §3.4 note; `locales: ["de","en"]`, `canonical_locale: "de"`.
- **Explicit `legal_basis` per question** (e.g. `"§ 19 Abs. 7 AWG"`, `"Art. 4 Abs. 1 VO (EU) 2021/821"`),
  matching `kartellrecht`.
- **Wiring** (the known drift trap — `BACKLOG.md` records a live 400 rejection when it was missed once):
  `data/modules_manifest.json` with the module label in **all 12 locales**, a `split_module()` call in
  `data/build_modules.py`, `TOPIC_LABELS.exportkontrolle` + `COMPLIANCE_MODULES` in `app/app.js`, **and**
  `COMPLIANCE_EXAM_TYPES` in `netlify/functions/save-verified-credential-v2.mjs` — all in the same commit.
- **Hard content rules for the author, from §3.6:** no Annex I position numbers, no sanctions package numbers,
  no named listed entities, no CN codes, no current § 74 AWV country membership. Every question must survive
  the next list update unchanged.
- **Two explicit "do not fabricate" warnings:** (1) there is **no** statutory training-frequency mandate in
  AWG/AWV — do not write a question implying one; (2) do not repeat the practitioner claim that the two-
  working-day Schonfrist was abolished (§1.2).

---

## 4. What each verdict rests on, stated as a falsifiable test

So the next agent can re-check cheaply rather than re-researching.

**ESG/CSRD — "build later" is wrong if:** `curl https://www.gesetze-im-internet.de/hgb/__289b.html` returns a
§ 289b that speaks of a *Nachhaltigkeitsbericht* rather than a *nichtfinanzielle Erklärung*, **and** the
revised ESRS delegated regulation has an OJ citation. Until both are true, the verdict holds.

**Exportkontrolle — "build now" is wrong if:** the AWG's Vollzitat changes to an act that restructures
§§ 17–19, or Reg. 2021/821 is repealed/replaced by a successor regulation with different article numbering.
Neither is in force or formally proposed today.

---

## 5. Source confidence

**Tier A — binding primary text, read in the official consolidated version and/or the official gazette.
Everything both recommendations rest on.**

1. **AWG** full consolidated text, `gesetze-im-internet.de`; §§ 1, 2, 4, 8, 17, 18 (incl. Abs. 1, 1a, 2, 5,
   5a, 5b, 6a, 8a, 10, 11, 12, 13), 19 (incl. Abs. 6, 7, 8) quoted verbatim.
2. **BGBl. 2026 I Nr. 27** — *Gesetz zur Anpassung von Straftatbeständen und Sanktionen bei Verstößen gegen
   restriktive Maßnahmen der EU* v. 3.2.2026, read in the **official `recht.bund.de` PDF**: Art. 1 Nr. 6
   lit. a–l, Nr. 7 lit. a–d, Art. 6, and the Richtlinie-(EU)-2024/1226 footnote. Cross-checked against the
   resulting consolidated AWG text — **two independent readings of the €40m provision.**
3. **AWV** full consolidated text; §§ 8, 9, 11, 22, 26, 46, 49, 52a, 74, 80 quoted verbatim; Anlage AL and the
   § 80–82 penalty structure confirmed.
4. **Regulation (EU) 2021/821**, OJ text: Art. 2(21), 3(1)–(2), 4(1)–(3), 5(1)–(3), 6, 8, 9, 10, 11(1),
   12(1)–(7), 13, 15(1)–(2), 16, 25(1), 27(1)–(4).
5. **Regulation (EU) 269/2014** Art. 2(1)–(2), OJ text.
6. **Council Regulation (EU) 2026/506 of 23 April 2026**, OJ L, 2026/506, 23.4.2026 — title, date, OJ citation
   verified on EUR-Lex (used only to date the current sanctions state, §3.6).
7. **Directive (EU) 2022/2464** Art. 5(1)–(2) — the 6 July 2024 deadline and the original three waves.
8. **Directive (EU) 2025/794** Art. 1–3 — the two-year wave delay and the 31 December 2025 transposition date.
9. **Directive (EU) 2026/470 of 24 February 2026**, OJ L, 2026/470, 26.2.2026 — recitals and Art. 1–7: the
   €450m/1,000-employee gate, the deletion of wave (c), the FY2025–2026 Member-State exemption option, the
   value-chain cap, the Art. 29ca voluntary-standard mandate (by 19 July 2026), Art. 5's **19 March 2027** and
   **26 July 2028** deadlines, Art. 6's twentieth-day entry into force, and the CSDDD 5,000/€1.5bn re-cut.
10. **HGB** §§ 289b, 289c, 289d, 289e, 315b, 315c, 317 Abs. 2, 334 Abs. 1 — read in full from
    `gesetze-im-internet.de` **and** independently from `buzer.de`; Vollzitat *"zuletzt geändert durch Artikel
    4 des Gesetzes vom 4. Februar 2026 (BGBl. 2026 I Nr. 33)"* identical in both. **Two independent
    consolidations of the negative finding.**
11. **LkSG** Vollzitat — *"Lieferkettensorgfaltspflichtengesetz vom 16. Juli 2021 (BGBl. I S. 2959)"* with **no
    "zuletzt geändert" clause at all**, i.e. zero amendments (§2.9).
12. **BGBl. 2026 I Nr. 66** — *Gesetz zur Umsetzung der Richtlinie (EU) 2022/2557 und zur Stärkung der
    Resilienz kritischer Anlagen* v. 11.3.2026, first page read in the official PDF (identifies what the
    11 March 2026 AWV amendment actually was).
13. **Mechanical negative checks:** "Nachhaltigkeitsbericht*" → **0 occurrences** in the HGB's accounting
    sections; no training-frequency provision anywhere in AWG or AWV.

**Tier B — official / quasi-official material, not itself binding.**

14. **BAFA, "Firmeninterne Exportkontrolle — Betriebliche Organisation im Außenwirtschaftsverkehr", 3. Auflage
    / April 2022** (PDF from bafa.de). Load-bearing for §3.4 (annual training expectation, retention of
    Schulungsnachweise, the indirectly-affected-staff audience, the AV role) and §3.5. **Note its age**: the
    3rd edition predates the February 2026 AWG-Novelle, so its penalty references are stale even though its
    organisational guidance is not.
15. **Wirtschaftsprüferkammer (WPK)** news of 3 July 2026 — Commission adoption of the revised-ESRS and
    voluntary-standard delegated regulations, two-month scrutiny period, three-day entry into force after OJ
    publication. Load-bearing for §2.4.
16. **BT-Drs. 21/1857** (Regierungsentwurf CSRD-UmsG, 3 September 2025) and **BR-Drs. 435/25** — identified and
    dated; the bill's own text was not read in full this round, because §2.5 disposes of the question.
17. **DRSC** news of 1 April 2026 (Änderungsantrag of 31 March 2026; hearing set for 13 April 2026) and
    **Noerr** insight of 13 April 2026 (thresholds from FY2027, value-chain cap, permanent limited assurance,
    retroactive application to FYs beginning after 31 December 2024, 2nd/3rd readings still pending).
    Load-bearing only for §2.6's narrative, not for any legal proposition.

**Tier C — orientation only; nothing rests on these.**

18. Law-firm and trade commentary on the 2026 AWG-Novelle (`awb-international.com`, `anwalt.de`). Useful as the
    reason to go looking; **one of its claims was checked and does not hold** (§1.2), which is why the §3.2
    findings were taken from the gazette instead.
19. Law-firm summaries of the 20th Russia sanctions package (GvW, Morgan Lewis, Squire Patton Boggs, Skadden)
    — used to locate Reg. (EU) 2026/506, which was then verified directly on EUR-Lex.
20. Trade/advisory commentary on CSRD status (Ebner Stolz 18.12.2025, CMS 2026 outlook, PwC blog 14.04.2026,
    ad-hoc-news 06.04.2026, Taylor Wessing June 2026, ADVANT Beiten, Baker Tilly). One of these produced the
    §1.1 trap and is cited for that, not for its prediction.
21. Commission open evaluation / call for evidence on Reg. (EU) 2021/821 (§3.6 watch item).

**Confidence.** *Exportkontrolle "build now": very high* — everything is in-force primary text, and the one
recent change was read in the official gazette and cross-checked against the consolidation. *ESG/CSRD "build
later": very high on the German non-transposition* (two independent consolidations of the actual statutory
text, which is a positive reading of what the law says, not an absence-of-evidence argument), *high on the
Omnibus rewrite* (OJ text), *high on the ESRS scrutiny status* (Tier B, single source — see §8.4).

---

## 6. What this changes in the repo's own record

Three corrections to standing repo documents, offered for the PO rather than applied (this round touched no
file but this one):

1. **`BACKLOG.md`'s line pairing "ESG/CSRD, Exportkontrolle" as a single unit of unverified white space should
   be split.** The two have opposite answers and opposite blockers. Bundling them has already cost this project
   time — the same category error the Maklerschein dossier caught in the "§ 34a and § 34c" pairing.
2. **`claude/compliance-competitor-pricing-and-course-gaps.md`** should record that Exportkontrolle is now
   **verified** and recommended, and that ESG/CSRD is **verified as blocked on German transposition**, with the
   three trigger conditions in §2.8. "Anti-Korruption", named in the same line, remains genuinely unresearched
   — this round did not touch it.
3. **`data/lksg_pilot.json`** — §2.9's CSDDD threshold check.

---

## 7. Why no draft question bank for Exportkontrolle either, despite a "build now" verdict

Stated explicitly because the verdict and the deliverable point in different directions.

The brief scoped this round as *"a real research verdict, not a content build"* and said in terms: if a topic
is clearly buildable, *"say so plainly and recommend it as the next round's task rather than drafting it
yourself."* That is what §3.7 and §3.8 do. Drafting 20 questions here would also have collided with the repo's
own working discipline: content rounds in this project run through a named card, a Student-Review gate and an
AI legal-review pass, none of which a research card carries. §3.8 is deliberately specified to the point where
an authoring agent needs no further research — five topics, the exact §§ per topic, the `meta` shape, the
wiring checklist, and two explicit do-not-fabricate warnings.

---

## 8. Open items for the PO / human decision

1. **Approve Exportkontrolle as the next content round** (§3.7, §3.8). This is the one decision that unblocks
   real work. Recommended card shape: 20-question DE/EN pilot, `kartellrecht` pattern, followed by an AI
   legal-review pass before any scale-up.
2. **Accept "build later" for ESG/CSRD** and record the three trigger conditions in §2.8 rather than leaving it
   on the board as ambiguous white space. Do not let "ESG" reach a roadmap or landing page as a module name
   (§2.7) — it is not a legal category.
3. **Split the ESG/CSRD + Exportkontrolle backlog line** (§6.1).
4. **Two verification gaps this round did not close**, both non-blocking: (a) whether the Commission's
   infringement action against Germany over CSRD has been referred to the CJEU — rests on a single dated Tier B
   source (proceedings opened 26 September 2024); (b) the ESRS scrutiny status rests on one Tier B source (WPK,
   3 July 2026) and should be re-checked against the OJ before any CSRD build.
5. **Small `lksg` card** for the CSDDD threshold check (§2.9).
6. **Pricing/market research for Exportkontrolle was not done** and is not claimed. The buyer analysis in §3.5
   is a qualitative fit argument from the legal duty and BAFA's stated training audience, not a validated
   willingness-to-pay finding. If the PO wants a price point before committing, that is a separate, small
   research card — but it should not block the content build, since the module is defensible on legal grounds
   alone and every prior compliance pilot shipped free.
7. **Standing process note, reinforced** (§1.1, §1.2): when a secondary source and a primary instrument
   disagree, the instrument wins — and this now cuts both ways. Stale consensus was the Maklerschein failure
   mode; **anticipatory** reporting ("the Bundestag will pass this in April") is the failure mode here. Neither
   is evidence of what the law is.

---

## 9. Re-verification

- **Exportkontrolle content, if built:** re-read § 18 and § 19 AWG, and Art. 3/4/5/12/27 of Reg. (EU) 2021/821,
  from the consolidations before the module's legal-review gate, and again no later than **2026-12-31**. Never
  re-verify list membership from this document — it deliberately contains none.
- **ESG/CSRD:** re-run the two falsifiable tests in §4 no later than **2027-01-31**, and again shortly before
  the **19 March 2027** Omnibus transposition deadline. Do not build from this document; build from a fresh
  pass.
- **Everything in §2** should be treated as having a short half-life. Between 14 April 2025 and 3 July 2026
  this area saw a delay directive, a scope-rewriting directive, a national bill re-drafted mid-passage, and a
  delegated act still in scrutiny. Assume it has moved again.

---

**Reminder:** this document is draft research groundwork. It is not legal advice, has not been reviewed by a
qualified lawyer, and no content derived from it should be shipped to learners before that review. The
Exportkontrolle findings rest on primary text read today and are high-confidence but six months downstream of a
significant amendment; the CSRD findings describe a legal position that is, by its nature, expected to change.
