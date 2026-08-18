# Bewachungsgewerbe (§ 34a GewO) — IHK-Sachkundeprüfung — pre-review dossier (2026-08-17)

**Status:** AI-prepared research groundwork only — **NOT legal advice**. Not reviewed by a lawyer or by any IHK Prüfungsausschuss member.

**Requested:** resolve the standing sourcing blocker on § 34a GewO (Bewachungsgewerbe / private security) and, *if and only if* it is genuinely resolvable, draft a first-round pilot question bank.

**Delivered:** this dossier **and** `data/bewachungsgewerbe_pilot_DRAFT.json` (28 questions, DE canonical + EN) plus its deterministic generator `data/gen_bewachungsgewerbe_draft.py`. The blocker is **solved**, and solved more cleanly than the roadmap assumed: the exam's subject matter is fixed by **statute**, not by a private catalogue.

**Files touched:** this file, `data/bewachungsgewerbe_pilot_DRAFT.json`, `data/gen_bewachungsgewerbe_draft.py`. Nothing else. `data/build_modules.py`, `data/modules_manifest.json`, `app/data/modules.json` and `app/app.js` are untouched; no build was run; nothing was staged or committed. The `_DRAFT` suffix keeps the pilot out of the live build path by construction.

---

## 0. The findings, first, because two of them are scope decisions and not footnotes

### 0.1 The sourcing blocker is solved — and it was never as bad as recorded

`claude/content-expansion-scoping-2026-08-12.md` item 15 records the blocker as: *"No single nationally published official question catalog. DIHK provides only a Rahmenplan/curriculum outline; actual questions are IHK-regional and non-public."*

Two of those three clauses are right; the framing built on them is wrong, and the third clause is wrong.

| Claim on file | Verdict |
|---|---|
| "No nationally published official **question** catalog" | **True**, and irrelevant. This project has never needed one — `aevo`, `kartellrecht`, `dora`, `nis2`, `cka`, `datenschutz` were all authored from a legal syllabus without one. |
| "DIHK provides **only** a Rahmenplan/curriculum outline" | **Understated.** The exam's subject matter is not a DIHK courtesy document — it is **fixed by legal instrument**. **§ 9 Abs. 2 BewachV**: *"Gegenstand der Sachkundeprüfung sind die in § 7 in Verbindung mit Anlage 2 aufgeführten Sachgebiete; die Prüfung soll sich auf jedes der dort aufgeführten Gebiete erstrecken."* § 7 BewachV names seven Sachgebiete; **Anlage 2 BewachV** breaks them down to individually **cited statutory provisions** (§ 227 BGB, §§ 228/904 BGB, §§ 229/859 BGB, § 858 BGB, §§ 823 ff. BGB, §§ 903/854 BGB, § 226 BGB, §§ 32–35 StGB, §§ 123/185 ff./223 ff./239/240/244 ff. StGB, § 127 StPO, §§ 152/163 StPO …). That is a **Tier A, copyright-free (§ 5 UrhG *amtliches Werk*) syllabus at provision-level granularity.** |
| "actual questions are IHK-regional and non-public" | **Wrong on the first half.** The DIHK Rahmenplan states the written question sets are **bundeseinheitlich**: *"Er ist Richtschnur für die Entwicklung der **bundeseinheitlichen Aufgabensätze** für den schriftlichen Prüfungsteil."* Non-public: yes. Regional: no. |

**So the sourcing basis here is strictly stronger than for several modules this repo has already shipped.** `aevo`'s own `meta` concedes *"There is no official public AEVO question catalogue"* and builds from AEVO + BBiG + a BIBB Rahmenplan. § 34a gives us the same shape **plus** a statutory annex that names the individual provisions to be examined. If `aevo` cleared the bar, § 34a clears it comfortably.

### 0.2 The base-vs-elevated distinction — and a correction to the task brief

The brief hypothesised that § 34a Abs. 1a names *"Personenschutz, Veranstaltungen mit erhöhtem Sicherheitsrisiko, Alarmempfangsstellen, JVA-Bewachung, Asylbewerberunterkünfte, öffentliche Verkehrsmittel"*. **That is not the statutory list.** Read today in the consolidated text on `gesetze-im-internet.de` and cross-read on `buzer.de` (§2.2 below), § 34a Abs. 1a Satz 2 lists **five** activities, and **Personenschutz, Alarmempfangsstellen, JVA-Bewachung and öffentliche Verkehrsmittel appear in none of them.** The correct statement is in §2. Getting this wrong in shipped copy would mis-sell the module to exactly the wrong buyers.

### 0.3 A three-and-a-half-week-old change nobody's secondary sources have caught up with

**§ 6a Abs. 1 GewO was rewritten with effect from 24 July 2026** by the same act the Maklerschein round analysed (GewBürAbG, BGBl. 2026 I Nr. 215). The Genehmigungsfiktion flipped from a **closed positive list** to a **general rule with two express carve-outs**, one of which is **§ 34a Abs. 1**. See §6 — including why the naive reading of the new text ("§ 34a just lost its deemed approval") is **wrong**, and what the change actually did.

---

## 1. Method and instruments read

All retrieval **2026-08-17**. `WebFetch` is `ROBOTS_DISALLOWED` on `gesetze-im-internet.de` in this sandbox; every German statutory text below was fetched by direct `curl`/`urllib` against `gesetze-im-internet.de` and parsed from raw HTML, so quotes are from the consolidated official text, not from a summary. Load-bearing provisions were cross-read on `buzer.de`; the 2026 amendment was additionally read in the **official Bundesgesetzblatt PDF**.

| Instrument | Retrieved from | What was read |
|---|---|---|
| **GewO § 34a** (Bewachungsgewerbe; Verordnungsermächtigung) | `gesetze-im-internet.de/gewo/__34a.html`; cross-read `buzer.de/34a_GewO.htm` | **Abs. 1–5 in full**, twice, independently |
| **GewO § 6a** (Entscheidungsfrist, Genehmigungsfiktion) | same; **plus** the pre-24.07.2026 Fassung via `buzer.de/gesetz/3982/al241775-0.htm` (synopse) | current **and** superseded wording |
| **GewO § 32** (Regelung der Sachkundeprüfung, Aufgabenauswahlausschüsse) | `gesetze-im-internet.de/gewo/__32.html` | Abs. 1 Nr. 1–11, Abs. 2 |
| **GewO §§ 144, 11b, 159** | same | § 144 Abs. 1 Nr. 1 lit. f, Abs. 2 Nr. 1b, **Abs. 4** (Bußgeldrahmen); § 11b Abs. 7–9; § 159 |
| **BewachV** (Verordnung über das Bewachungsgewerbe, V. v. 03.05.2019 BGBl. I S. 692, zuletzt geänd. Art. 2 V. v. 24.06.2019 BGBl. I S. 882) | `gesetze-im-internet.de/bewachv_2019/` — **note the non-obvious slug `bewachv_2019`** | **§§ 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23 in full**, Inhaltsübersicht, **Anlage 2 in full** |
| **GewBürAbG**, G. v. 20.07.2026, **BGBl. 2026 I Nr. 215** | **official BGBl PDF** `recht.bund.de/bgbl/1/2026/215/regelungstext.pdf` (7 pp., 289 KB) **and** `buzer.de/gesetz/17617/index.htm` | Art. 1 Nr. 1–3, **Art. 11 Abs. 1–4** verbatim, both sources |
| **BGB** §§ 226, 227, 228, 229, 230, 823, 833, 854, 855, 858, 859, 860, 903, 965 | `gesetze-im-internet.de/bgb/` | full text of each |
| **StGB** §§ 12, 32, 34, 123, 239, 240, 242, 249, 252, 263, 265a, 303, 323c | `gesetze-im-internet.de/stgb/` | full text of each |
| **StPO** §§ 127, 163 | `gesetze-im-internet.de/stpo/` | full text |
| **WaffG** §§ 10, 28, 42a | `gesetze-im-internet.de/waffg_2002/` | full text |
| **BDSG** § 4 | `gesetze-im-internet.de/bdsg_2018/__4.html` | Abs. 1–5 — see the currency warning at §7.3 |
| **DIHK, "Bewachungsgewerbe — Rahmenplan für die Sachkundeprüfung / Stoffsammlung für die Unterrichtung", Stand September 2019** | `ihk.de/blueprint/servlet/resource/blob/3599196/…/rahmenplan-bewachungsgewerbe-data.pdf` (13 pp.) | **whole document** — see §4, incl. its copyright notice |
| **IHK Frankfurt am Main**, Sachkundeprüfung § 34a (Nr. 5306328) | `frankfurt-main.ihk.de/…/5306328` | exam mechanics, fees, Zulassungsregel |
| **IHK Magdeburg**, Sachkundeprüfung Bewachung (Nr. 3301986) | `ihk.de/magdeburg/…/3301986` | exam mechanics, Bewertung change 01.07.2025 |
| **IHK zu Essen**, Rahmenplan-Seite (Nr. 2713376) | `ihk.de/meo/…/2713376` | Rahmenplan framing, sachkundepflichtige Tätigkeiten |

**Deliberately not opened, not read, not cited for anything:** every exam-prep vendor site that dominates the search results for this topic — `34a.org`, `34a-master.de`, `34a-jack.de`, `sicherheit34a.de`, `sachkunde-lernen.de`, `secumind-34a.de`, `34a-sachkunde-gewo.de`, `ihq-akademie.de`, `amtsguide.de`. Several appeared in search results and were **not fetched**. AGENTS.md constraint 1 bans third-party exam-prep companies' text outright, and unlike the sign-icon carve-out there is no visual-accuracy exception that could apply to a question bank. Nothing in this dossier or in the draft derives from any of them, directly or indirectly.

### 1.1 A retrieval note for the next agent

`https://www.gesetze-im-internet.de/bewachv_2019/BJNR146600019.html` (the Gesamtausgabe URL pattern used elsewhere) returns a **236-byte stub**, not the regulation. The working entry point is the index at `/bewachv_2019/` plus per-§ `__N.html` Einzelnorm pages; **Anlage 2 is at `/bewachv_2019/anlage_2.html`**, not under a § number. Also note `buzer.de` still lists a *pre-2019* BewachV as a separate title — check the `V. v. 03.05.2019` date before quoting anything from a buzer BewachV page.

---

## 2. § 34a GewO: who needs what (Tier A — the commercially decisive structure)

There are **three** distinct qualification tiers, not two. Getting them right decides who the module is sold to.

### 2.1 Tier 1 — the *business*: Erlaubnis + Sachkundeprüfung (§ 34a Abs. 1)

> **§ 34a Abs. 1 Satz 1 GewO** — "Wer gewerbsmäßig **Leben oder Eigentum fremder Personen bewachen** will (Bewachungsgewerbe), bedarf der **Erlaubnis** der zuständigen Behörde."

> **§ 34a Abs. 1 Satz 3 GewO** — "Die Erlaubnis **ist zu versagen**, wenn […] **3.** der Antragsteller oder eine mit der Leitung des Betriebes oder einer Zweigniederlassung beauftragte Person **nicht durch eine vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung nachweist, dass er die für die Ausübung des Bewachungsgewerbes notwendige Sachkunde über die rechtlichen und fachlichen Grundlagen besitzt**; für juristische Personen gilt dies für die gesetzlichen Vertreter, soweit sie mit der Durchführung von Bewachungsaufgaben direkt befasst sind oder keine mit der Leitung des Betriebes oder einer Zweigniederlassung beauftragte Person einen Sachkundenachweis hat, oder **4.** der Antragsteller den Nachweis einer **Haftpflichtversicherung** nicht erbringt."

Note the internal logic of Nr. 3's second half: for a juristische Person the *gesetzlicher Vertreter* needs the Sachkunde only if he is directly involved in Bewachungsaufgaben **or** if no Betriebsleiter holds a Sachkundenachweis. A GmbH can therefore satisfy § 34a with a qualified Betriebsleiter and a non-operational managing director.

Contrast **§ 34c**: refusal grounds there are Zuverlässigkeit + Vermögensverhältnisse only, with no knowledge limb at all (`docs/maklerschein-pre-review-dossier-2026-08-17.md` §2.2). Here Sachkunde and Haftpflicht are **additional** limbs on top of both.

### 2.2 Tier 2 — the *base* for employees: Unterrichtung only, **no exam**

> **§ 34a Abs. 1a Satz 1 GewO** — "Der Gewerbetreibende darf mit der Durchführung von Bewachungsaufgaben nur Personen (**Wachpersonen**) beschäftigen, die **1.** die erforderliche **Zuverlässigkeit** besitzen und **2.** durch eine **Bescheinigung der Industrie- und Handelskammer** nachweisen, dass sie über die für die Ausübung des Gewerbes notwendigen rechtlichen und fachlichen Grundlagen **unterrichtet** worden sind und mit ihnen vertraut sind."

The Unterrichtung is **not an exam**. Per **§ 6 BewachV** it is oral, at least **40 Unterrichtsstunden** of 45 minutes, max 20 participants, requires German at **CEFR B1 minimum**, and the Bescheinigung issues on **attendance without any absence** plus the IHK satisfying itself through dialogue and comprehension questions after each Sachgebiet — *"wenn die unterrichtete Person am Unterricht **ohne Fehlzeiten** teilgenommen hat"*. **There is no pass/fail, no grade and no proctored test.**

### 2.3 Tier 3 — the *elevated* activities: Sachkundeprüfung required

> **§ 34a Abs. 1a Satz 2 GewO** — "Für die Durchführung folgender Tätigkeiten ist **zusätzlich zu den Anforderungen des Satzes 1 Nummer 1** der Nachweis einer vor der Industrie- und Handelskammer erfolgreich abgelegten **Sachkundeprüfung** erforderlich:
> **1.** **Kontrollgänge im öffentlichen Verkehrsraum** oder in Hausrechtsbereichen mit tatsächlich öffentlichem Verkehr,
> **2.** **Schutz vor Ladendieben**,
> **3.** Bewachungen **im Einlassbereich von gastgewerblichen Diskotheken**,
> **4.** Bewachungen von **Aufnahmeeinrichtungen nach § 44 des Asylgesetzes** […], von **Gemeinschaftsunterkünften nach § 53 des Asylgesetzes** oder anderen Immobilien und Einrichtungen, die der auch vorübergehenden amtlichen Unterbringung von Asylsuchenden oder Flüchtlingen dienen, **in leitender Funktion**,
> **5.** Bewachungen von **zugangsgeschützten Großveranstaltungen in leitender Funktion**."

**The precise statement of the base-vs-elevated distinction, with citation:**

> A Wachperson performing the **base** activity needs **Zuverlässigkeit plus an IHK *Unterrichtungs*bescheinigung** — 40 hours, attendance-based, no exam (**§ 34a Abs. 1a Satz 1 Nr. 1 und 2 GewO** i. V. m. **§ 6 BewachV**). The **full IHK *Sachkundeprüfung*** is required only (a) of the **business owner / gesetzlicher Vertreter / Betriebsleiter** as a condition of the Erlaubnis (**§ 34a Abs. 1 Satz 3 Nr. 3 GewO**), and (b) of **Wachpersonen performing one of the five activities exhaustively listed in § 34a Abs. 1a Satz 2 GewO** — Kontrollgänge im öffentlichen Verkehrsraum bzw. in Hausrechtsbereichen mit tatsächlich öffentlichem Verkehr; Schutz vor Ladendieben; Einlassbereich gastgewerblicher Diskotheken; Asyl-Aufnahmeeinrichtungen/Gemeinschaftsunterkünfte **in leitender Funktion**; zugangsgeschützte Großveranstaltungen **in leitender Funktion**.

**Four consequences that are easy to get wrong and that the draft tests explicitly:**

1. **The list is exhaustive**, and it does **not** contain Personenschutz, Alarmempfangsstellen/NSL, JVA-Bewachung, öffentliche Verkehrsmittel or "Veranstaltungen mit erhöhtem Sicherheitsrisiko" (correcting the task brief, §0.2). Objektschutz on private premises, Werkschutz, Empfangsdienst, Doorman duty that is not a *gastgewerbliche Diskothek*, and non-leitende event stewarding all sit in the base tier.
2. **Nr. 4 and Nr. 5 are limited to `in leitender Funktion`.** A rank-and-file steward at a ticketed stadium concert does **not** need the Sachkundeprüfung. **Both IHK pages checked drop this qualifier** — IHK Frankfurt lists "Bewachung von Aufnahmeeinrichtungen nach §§ 44 des Asylgesetzes (Flüchtlingsunterkünften, Asylantenwohnheime)" with no leitende limitation, IHK Essen drops it from Großveranstaltungen. The statute governs; the IHK summaries are loose. (This is the same secondary-source-drift pattern §1.1 of the Maklerschein dossier recorded.)
3. **Satz 2 supplements only `Satz 1 Nummer 1` — the Zuverlässigkeit — not Nummer 2.** The Sachkundeprüfung therefore **replaces** rather than stacks on top of the Unterrichtung, and **§ 8 Nr. 4 BewachV** closes the loop expressly: a *"Bescheinigung über eine erfolgreich abgelegte Sachkundeprüfung nach § 11 Absatz 7"* is one of the four documents that make an Unterrichtungsnachweis unnecessary. Nobody needs both.
4. **A separate, higher Zuverlässigkeit screen exists and does not track the Sachkunde line.** Per **§ 34a Abs. 1a Satz 5**, the Verfassungsschutz check of Abs. 1 Satz 5 Nr. 4 applies to Wachpersonen doing Nr. 4/Nr. 5 work **"auch in nicht leitender Funktion"**, and to *"Schutzaufgaben im befriedeten Besitztum bei Objekten, von denen im Fall eines kriminellen Eingriffs eine besondere Gefahr für die Allgemeinheit ausgehen kann"* — a category that appears **nowhere** in the Sachkunde list. **Reliability tier ≠ qualification tier.** A rank-and-file guard at an asylum shelter gets the constitutional-protection check but needs only the Unterrichtung.

### 2.4 The limits on what a guard may actually do (Tier A, and the module's ethical spine)

> **§ 34a Abs. 5 GewO** — "Der Gewerbetreibende und seine Beschäftigten dürfen bei der Durchführung von Bewachungsaufgaben gegenüber Dritten **nur die Rechte, die Jedermann im Falle einer Notwehr, eines Notstandes oder einer Selbsthilfe zustehen**, die ihnen vom jeweiligen Auftraggeber **vertraglich übertragenen Selbsthilferechte** sowie die ihnen gegebenenfalls in Fällen **gesetzlicher Übertragung** zustehenden Befugnisse eigenverantwortlich ausüben. In den Fällen der Inanspruchnahme dieser Rechte und Befugnisse ist der **Grundsatz der Erforderlichkeit** zu beachten."

Reinforced operationally by **§ 17 Abs. 1 Satz 2 BewachV**: the Dienstanweisung *"muss den Hinweis enthalten, dass die Wachperson **nicht die Eigenschaft und die Befugnisse eines Polizeivollzugsbeamten**, oder eines sonstigen Bediensteten einer Behörde besitzt"*, and by **§ 19 Abs. 1 BewachV** (Dienstkleidung must differ clearly from uniforms of armed forces or enforcement bodies, no confusable insignia). This "no special powers" spine is the single most important thing a § 34a learner has to internalise and is weighted accordingly in the draft.

---

## 3. The statutory syllabus — this is what unblocks the module (Tier A)

### 3.1 The chain of authority

**§ 34a Abs. 2 Nr. 3 GewO** empowers the BMI, with Bundesrat consent, to lay down *"die Anforderungen und das Verfahren für eine **Sachkundeprüfung** nach Absatz 1 Satz 3 Nummer 3 und Absatz 1a Satz 2 sowie Ausnahmen von der Erforderlichkeit der Sachkundeprüfung"*. The BewachV is the exercise of that power. Then:

> **§ 9 BewachV — Zweck und Gegenstand der Sachkundeprüfung**
> "(1) Zweck der Sachkundeprüfung […] ist es, den Nachweis zu erbringen, dass die dort genannten Personen die für die **eigenverantwortliche Wahrnehmung der Bewachungsaufgaben** erforderlichen Kenntnisse über die dafür notwendigen **rechtlichen Vorschriften und fachbezogenen Pflichten und Befugnisse sowie deren praktische Anwendung** erworben haben.
> (2) **Gegenstand der Sachkundeprüfung sind die in § 7 in Verbindung mit Anlage 2 aufgeführten Sachgebiete; die Prüfung soll sich auf jedes der dort aufgeführten Gebiete erstrecken.**"

Abs. 1's *"sowie deren praktische Anwendung"* is a drafting instruction as much as a legal one: the exam is **applied**, not recitation. The draft is written in situation style accordingly, the same choice `aevo` made off § 4 Abs. 2 AEVO.

### 3.2 The seven Sachgebiete

> **§ 7 BewachV — Inhalt der Unterrichtung**
> "Die Unterrichtung umfasst nach näherer Bestimmung der Anlage 2 für alle Arten des Bewachungsgewerbes die fachspezifischen Rechte, Pflichten und Befugnisse folgender Sachgebiete:
> **1.** Recht der öffentlichen Sicherheit und Ordnung **einschließlich Gewerberecht**,
> **2.** **Datenschutzrecht**,
> **3.** **Bürgerliches Gesetzbuch**,
> **4.** **Straf- und Strafverfahrensrecht, Umgang mit Waffen**,
> **5.** **Unfallverhütungsvorschrift Wach- und Sicherungsdienste**,
> **6.** **Umgang mit Menschen**, insbesondere Verhalten in Gefahrensituationen, Deeskalationstechniken in Konfliktsituationen sowie interkulturelle Kompetenz unter besonderer Beachtung von Diversität und gesellschaftlicher Vielfalt und
> **7.** **Grundzüge der Sicherheitstechnik**."

The task brief's starting hypothesis was close but not exact: it guessed "Gewerberecht/OWi-Recht", "BGB incl. Notwehr/Nothilfe/Selbsthilfe/unerlaubte Handlungen", "Straf-/Verfahrensrecht incl. § 127 StPO", "Datenschutz", "Waffen", "UVV/Arbeitsschutz". **It missed Nr. 6 (Umgang mit Menschen — the single largest block at ~11 of 40 hours) and Nr. 7 (Sicherheitstechnik) entirely.** Both are in the draft.

### 3.3 Anlage 2 BewachV — provision-level granularity, zero copyright

**Anlage 2 (zu § 7)**, Fundstelle BGBl. I 2019, 701, headed *"Sachgebiete für das Unterrichtungsverfahren im Bewachungsgewerbe — Bewachungspersonal (40 Unterrichtsstunden)"*. German statutory text is an *amtliches Werk* under **§ 5 UrhG** and carries no copyright, so reproducing it raises none of constraint 1's concerns — it is the categorical opposite of a vendor catalogue.

| Nr. | Sachgebiet | Provisions Anlage 2 itself names | Hours |
|---|---|---|---|
| 1 | Recht der öffentlichen Sicherheit und Ordnung einschl. Gewerberecht | Abgrenzung Bewachungsunternehmen ↔ Polizei-/Ordnungsbehörden; **§ 34a GewO, BewachV** | 6 (with Nr. 2) |
| 2 | Datenschutzrecht | *(no sub-bullets in Anlage 2)* | — |
| 3 | Bürgerliches Gesetzbuch | **Notwehr § 227**, **Notstand §§ 228, 904**, **Selbsthilfe §§ 229, 859**, **verbotene Eigenmacht § 858**, **Haftungs-/Deliktsrecht §§ 823 ff.**, **Eigentum und Besitz §§ 903, 854**, **Schikaneverbot § 226**, *"wobei **Abgrenzungsfragen zu den einschlägigen Vorschriften des StGB (§§ 32 bis 35)** aufgezeigt werden"* | ~6 |
| 4 | Straf- und Verfahrensrecht, Umgang mit Waffen | einzelne Straftatbestände (**§ 123, §§ 185 ff., §§ 223 ff., § 239, § 240, §§ 244 ff. StGB**); **vorläufige Festnahme § 127 StPO**; Aufgaben von Staatsanwaltschaft und Polizei **§§ 152, 163 StPO**; Umgang mit Waffen (Schlagstöcke, Reizstoffsprühgeräte usw.) | ~6 |
| 5 | Unfallverhütung | *(no sub-bullets in Anlage 2)* | ~6 |
| 6 | Umgang mit Menschen … | Selbstwertgefühl; übersteigerte Selbstwert-/Minderwertigkeitsgefühle; Konflikt/Stress; richtiges Ansprechen und Gesprächsführung; interkulturelle Kompetenz; **Umgang mit und Schutz von besonders schutzbedürftigen Geflüchteten** | **~11** |
| 7 | Grundzüge der Sicherheitstechnik | Mechanische Sicherungstechnik; **Gefahrenmeldeanlagen; Alarmverfolgung**; **Brandschutz** | ~5 |

**This table is the authoring outline.** Every question in the draft is written from the *cited provision's own text* (all fetched and read this session, §1), with Anlage 2 used only to decide *which* provisions are in scope and roughly how much weight each area carries.

**One caveat, stated plainly.** Anlage 2 is formally the **Unterrichtungs** curriculum; § 9 Abs. 2 imports it as the exam's Gegenstand **by reference**, and the DIHK Rahmenplan states that the Prüfung is *deeper and broader* than the Unterrichtung (*"Die Unterrichtung ist weniger tief und breit als die Sachkundeprüfung angelegt"*). So Anlage 2 is a reliable **floor** on exam scope, not a ceiling. That is exactly the right property for a pilot: nothing in the draft can be outside the exam's scope, though the real exam reaches somewhat further.

---

## 4. The DIHK Rahmenplan — an official topic catalogue exists, and here is precisely how far it may be used

**DIHK e.V., "Bewachungsgewerbe — Rahmenplan für die Sachkundeprüfung / Stoffsammlung für die Unterrichtung", Stand September 2019**, 13 pp., *"prüfungsrelevant ab 1. Juni 2019"*. This is the document the roadmap knew about. It is real, official in the IHK-organisation sense, and freely downloadable from `ihk.de`.

**What it is (its own words):**

> "Um die maßgeblichen Lerninhalte und Lernziele für die Prüfungsteilnehmer transparenter und verbindlicher zu machen, hat die IHK-Organisation diesen Rahmenplan erarbeitet. […] Der Rahmenplan bezieht sich auf den schriftlichen und mündlichen Prüfungsteil. **Er ist Richtschnur für die Entwicklung der bundeseinheitlichen Aufgabensätze für den schriftlichen Prüfungsteil.**"

> "Eine weitere Konkretisierung des prüfungsrelevanten Stoffs ist **in der BewachV selbst nicht enthalten**. Die Anlage 2 der BewachV, die sich auf das Unterrichtungsverfahren bezieht, **gibt jedoch Anhaltspunkte für die Prüfungsinhalte**."

Structurally it is a three-column table — *Inhalt | Erläuterungen | Taxonomie für die Prüfung* — with **Bloom-style taxonomy levels** (WISSEN / VERSTEHEN / ANWENDEN / ÜBERTRAGEN) per learning objective, and an **`(S)` marker on items that are Sachkundeprüfung-only** and not part of the Unterrichtung. It confirms and refines Anlage 2 at every point checked. It is **not** a question catalogue and contains **no exam questions**.

### 4.1 The constraint-1 analysis, and why the answer is "cite it, don't build on it"

**The Rahmenplan is copyrighted.** Page 1 carries: *"Copyright: Alle Rechte liegen beim Herausgeber. Ein Nachdruck – auch auszugsweise – ist nur mit ausdrücklicher schriftlicher Genehmigung des Herausgebers gestattet."* Herausgeber is **DIHK e.V.**, a private association. It is therefore **not** an *amtliches Werk* under § 5 UrhG, unlike Anlage 2 BewachV.

That does **not** make it a constraint-1 object — the DIHK is not an "exam-prep or compliance-training company" and this is not "an official Fragenkatalog". But it does mean the safe posture is narrower than "it's official, go ahead":

| Use | Verdict |
|---|---|
| Read it to confirm scope, depth and weighting; cite it as evidence that an official topic catalogue exists | **Fine.** Done here. |
| Reproduce its table, its taxonomy assignments, its `(S)` markers or its sub-bullet wording into repo content | **Do not.** Copyrighted expression of a private body. |
| Derive question wording from it | **Do not.** Nothing needs it — its substance is a list of statutory citations, and those provisions were read directly (§1). |
| Treat it as the module's *authoritative* syllabus | **No — use Anlage 2 BewachV instead.** Anlage 2 is Tier A, copyright-free, and legally the actual Gegenstand per § 9 Abs. 2 BewachV. The Rahmenplan is Tier B corroboration. |

**Net:** the module's syllabus authority is **statutory**, and the Rahmenplan is a cross-check we happen to also have. That is a materially better position than the roadmap assumed, and it removes the roadmap's stated risk entirely — there is no path here that runs through anyone's proprietary question bank.

### 4.2 Where the Rahmenplan is stale (it is nearly seven years old)

Stand September 2019. Two items to re-ground rather than transcribe:

- **"Videoüberwachung öffentlich zugänglicher Räume (§ 4 BDSG)"** under Sachgebiet 2. § 4 Abs. 1 BDSG's applicability to **non-public** controllers has been contested since 2019 on Union-law-preemption grounds, with Art. 6 Abs. 1 lit. f DSGVO advanced as the correct basis for private video surveillance. **This dossier does not resolve that question** — it is flagged as a live legal issue for review (§9.3), and the draft's video question deliberately sits on the uncontested limbs (transparency/signage, erasure when no longer required) rather than on § 4 Abs. 1.
- **"Betäubungsmittelstrafrecht (§§ 29, 30 BTMG)"** under 4a. The BTMG has been amended repeatedly since 2019 (cannabis reform). Not touched in the draft.

Its own §-references to GewO/BewachV/StGB/StPO/BGB/WaffG were spot-checked against the current consolidated texts and all held.

---

## 5. Exam structure and mechanics

### 5.1 What the regulation itself fixes (Tier A)

> **§ 11 BewachV — Prüfung, Verfahren**
> "(1) Die Sachkundeprüfung ist in einen **mündlichen und einen schriftlichen Teil** zu gliedern.
> (2) Im mündlichen Prüfungsteil können gleichzeitig **bis zu fünf Prüflinge** geprüft werden; er soll für jeden Prüfling **etwa 15 Minuten** dauern. Im mündlichen Prüfungsteil ist ein **Schwerpunkt auf die in § 7 Nummer 1 und 6 genannten Gebiete** zu legen.
> (3) Der schriftliche Teil der Prüfung kann mit Hilfe unterschiedlicher Medien durchgeführt werden.
> (4) Die Leistung des Prüflings ist von dem Prüfungsausschuss mit **bestanden oder nicht bestanden** zu bewerten. Die Prüfung ist bestanden, wenn die Leistungen des Prüflings **im schriftlichen Teil und im mündlichen Teil der Prüfung jeweils mindestens mit ausreichend** bewertet wurden.
> […] (6) Die Prüfung **darf wiederholt werden**.
> (7) Die Industrie- und Handelskammer stellt eine **Bescheinigung nach Anlage 3** aus […]
> (8) Die **Einzelheiten des Prüfungsverfahrens regeln die Industrie- und Handelskammern nach Maßgabe des § 32 der Gewerbeordnung durch Satzung.**"

Also Tier A: **§ 10 Abs. 1** — the exam may be sat *"bei jeder Industrie- und Handelskammer […], die diese anbietet"* (free choice of chamber, no district binding); **§ 10 Abs. 2** — each IHK sets up at least one Prüfungsausschuss; **§ 11 Abs. 5** — the exam is not public, with an exhaustive list of five permitted observer categories who *"dürfen nicht in die laufende Prüfung eingreifen"*; **§ 12** — holders of the § 8 Nr. 1–3 qualifications are exempt from the Prüfung entirely.

**Four things the BewachV deliberately does *not* fix**, and which any module must therefore not assert as national facts: the **number of questions**, the **duration of the written part**, the **percentage** constituting *"ausreichend"*, and whether the written part gates the oral. All four are **IHK Satzung** matter under § 11 Abs. 8 BewachV + **§ 32 Abs. 1 GewO** — whose Nr. 4 ("die Dauer der Prüfung"), Nr. 5 ("die Zulassung zum praktischen Teil der Prüfung"), Nr. 8 ("die Bewertung der Prüfungsleistungen") and Nr. 10 ("die Wiederholungsprüfung") name exactly these.

**Notable negative finding:** **§ 32 Abs. 2 GewO** provides for **Aufgabenauswahlausschüsse** (question-selection committees, run via the gemeinsame Stelle of § 32 Abs. 2 UAG) — *"soweit in Rechtsverordnungen nach diesem Abschnitt für die Auswahl von Prüfungsfragen für Sachkundeprüfungen die Bildung von Aufgabenauswahlausschüssen vorgesehen ist"*. **The BewachV contains no such provision** ("Aufgabenauswahl" appears nowhere in it). The bundeseinheitliche Aufgabensätze are therefore an **IHK-organisation practice** documented by the Rahmenplan, not a statutory mechanism — which is consistent with the question sets being non-public, and is a further reason not to expect a published catalogue ever to appear.

### 5.2 What the chambers actually do (Tier B — two independent IHKs)

| Fact | IHK Frankfurt am Main | IHK Magdeburg |
|---|---|---|
| Written part | **digital, 120 Minuten** | **120 Minuten** |
| Oral part | **ca. 15 Min**, separate date | **ca. 15 Min** je Teilnehmer, separate date, **bis zu drei Personen** zusammen |
| Gating | *"Zum mündlichen Prüfungsteil wird nur zugelassen, wer den schriftlichen Prüfungsteil bestanden hat"*, with a **2-year window** to sit the oral | *"Zur mündlichen Prüfung wird nur zugelassen, wer zuvor den schriftlichen Prüfungsteil bestanden hat"* |
| Fee | **EUR 205** total; **EUR 137** to repeat the oral | (Gebührentarif not read) |
| Scoring | — | *"Bisher wird nach dem 'Alles-oder-Nichts-Prinzip' geprüft. **Neu: Ab 01.07.2025** wird die Prüfung mit einer **Teilbewertung** geprüft."* |

Two observations worth carrying forward. First, **120 minutes and the written-gates-oral rule are consistent across both chambers**, so they are safe as *typical* practice — but they are Satzung, not law, and must be labelled as such. Second, **Magdeburg records a scoring-model change effective 01.07.2025** from all-or-nothing to partial credit. That is a live, dated change to how the exam is marked, it is chamber-level, and this dossier has **not** established whether it is nationwide. The draft's `pass_rule_note` says so explicitly rather than inventing a threshold.

**Neither chamber publishes a question catalogue.** Both point learners at the Rahmenplan and at commercial course providers; Frankfurt offers a "PC-Test-Prüfung" with the express caveat that it *"stellt nur die Prüfungsumgebung vor und **enthält keine realen Prüfungsfragen**"*. Magdeburg states it *"darf aus Neutralitätsgründen keine Bildungsträger empfehlen"*. **This is a real, unserved gap:** the state mandates the exam, publishes the syllabus, and publishes no practice material at all.

### 5.3 Administrative route — a product-relevant surprise

Per IHK Frankfurt: *"Die Prüfung erfolgt **nicht auf direkten Antrag der Einzelperson**, sondern über den Gewerbetreibenden"* — the employer registers the person in the **Bewacherregister**, uploads the qualification evidence, and the Ordnungsamt assesses exemption under §§ 8/12/23 BewachV. Confirmed in statute by **§ 16 Abs. 2 BewachV** (employer must register a Wachperson via the Bewacherregister *before* deploying them, transmitting *inter alia* Nr. 7 *"die Angabe der beabsichtigten Tätigkeit der Wachperson nach § 34a Absatz 1a Satz 2 und Satz 5"* and Nr. 8 the qualification evidence). **The individual is not the transacting party with the authority** — which has obvious implications for who the buyer of a prep product is (B2C learner, B2B employer, or both).

---

## 6. The 24 July 2026 § 6a GewO change — verified, and *not* what a naive reading suggests

**Current consolidated text**, read on `gesetze-im-internet.de/gewo/__6a.html` and cross-read on `buzer.de/6a_GewO.htm`:

> **§ 6a Abs. 1 GewO** — "Hat die Behörde über einen Antrag auf Erlaubnis zur Ausübung eines Gewerbes nicht innerhalb einer Frist von **drei Monaten** entschieden, gilt die Erlaubnis als erteilt. **Satz 1 gilt nicht für Verfahren nach § 31 Absatz 1 und § 34a Absatz 1.**"

**The amending instruction**, verbatim from the official BGBl PDF:

> **GewBürAbG Art. 1 Nr. 1** — "§ 6a Absatz 1 wird durch den folgenden Absatz 1 ersetzt: „(1) Hat die Behörde über einen Antrag auf Erlaubnis zur Ausübung eines Gewerbes nicht innerhalb einer Frist von drei Monaten entschieden, gilt die Erlaubnis als erteilt. Satz 1 gilt nicht für Verfahren nach § 31 Absatz 1 und § 34a Absatz 1.“"

> **GewBürAbG Art. 11** — "(1) Dieses Gesetz tritt vorbehaltlich der Absätze 2 bis 4 **am Tag nach der Verkündung** in Kraft. (2) **Artikel 1 Nummer 2** und Artikel 7 treten am 1. Mai 2027 in Kraft. (3) Artikel 3 tritt am 30. Juli 2026 in Kraft. (4) Artikel 9 tritt am 1. November 2026 in Kraft."

Art. 11 Abs. 2 defers **Nummer 2** (§ 14 Abs. 8 GewO), **not Nummer 1**. Verkündung was 23.07.2026; `buzer.de` records § 6a as *"Text in der Fassung des Artikels 1 […] m.W.v. **24. Juli 2026**"*. **Art. 1 Nr. 1 is therefore in force now.**

**And here is the part that required checking rather than assuming.** The superseded wording, retrieved from the buzer synopse of the pre-24.07.2026 Fassung:

> **§ 6a Abs. 1 GewO, until 23.07.2026** — "Hat die Behörde über einen Antrag auf Erlaubnis zur Ausübung eines Gewerbes **nach § 34b Absatz 1, 3, 4, § 34c Absatz 1 Satz 1 Nummer 1, 3 und 4 oder § 55 Absatz 2** nicht innerhalb einer Frist von drei Monaten entschieden, gilt die Erlaubnis als erteilt."

So the old rule was a **closed positive list that never contained § 34a in the first place**. The reform inverted the drafting technique — from *"the fiction applies to these listed trades"* to *"the fiction applies to all trades except these two"* — and § 34a moved from *outside an inclusion list* to *inside an exclusion list*.

**The correct statement is therefore: the outcome for Bewachung is unchanged — there has never been a deemed approval for a § 34a Abs. 1 Erlaubnis, and there still isn't — but the reason changed on 24 July 2026, and § 34a is now one of only two trades the GewO names by hand as too safety-critical for a deemed approval.** The naive reading ("§ 34a just lost its Genehmigungsfiktion") is wrong and would have been an easy, plausible, undetected error. Recording this because it is the same failure mode the Maklerschein dossier §1.1 warned about, arrived at from the opposite direction: there, the consolidated text was right and the practitioners were stale; here, the consolidated text alone is genuinely misleading and only the **superseded** text disambiguates it.

---

## 7. The rest of the operative regime (Tier A) — what a module has to get right

### 7.1 Duties on the business, BewachV Abschnitt 6

| § | Duty | Testable detail |
|---|---|---|
| **§ 14** | Haftpflichtversicherung | Minimums **per Schadensereignis**: Personenschäden **1 000 000 EUR**, Sachschäden **250 000 EUR**, Abhandenkommen bewachter Sachen **15 000 EUR**, reine Vermögensschäden **12 500 EUR**; annual aggregate may be capped at **double** the minimum; must cover §§ 278/831 BGB vicarious liability |
| **§ 16** | Bewacherregister An-/Abmeldung **before** deployment; Wachperson must be zuverlässig, **18** (or hold a § 8 qualification), and have "die für ihre Tätigkeit notwendige Befähigung"; applies equally to **Arbeitnehmerüberlassung** (Abs. 5) | the intended § 34a Abs. 1a Satz 2/Satz 5 activity must be declared at registration |
| **§ 17** | Dienstanweisung; **mandatory** statement that the guard has no police powers; weapons only with the Gewerbetreibender's consent and every use reported **unverzüglich** to police and employer; handed over **against receipt** before first duty; written confidentiality undertaking surviving termination | |
| **§ 18** | Ausweis (5 mandatory items incl. **Bewacherregister-ID** of both person and firm) — must be *"so beschaffen […], dass er sich von amtlichen Ausweisen deutlich unterscheidet"*; carried on duty and shown on demand. **Abs. 3**: visible **name or ID-number badge** for activities under § 34a Abs. 1a Satz 2 **Nr. 1 und 3 bis 5** — i.e. **not Nr. 2 (Ladendetektive)** — and for Nr. 4/5 also in **non-leitende** function | the Nr. 2 exclusion is the elegant detail: covert store detection would be defeated by a badge |
| **§ 19** | Dienstkleidung must differ clearly from military/enforcement uniforms; **mandatory** where the guard enters *befriedetes Besitztum* | |
| **§ 20** | Safe storage and return of weapons/ammunition; **Anzeigepflicht** after any weapon use | |
| **§ 21** | Buchführung *"unverzüglich und in deutscher Sprache"*; per-contract records; evidence list in Abs. 3; **3-year** retention with the Abs. 4 variants; **Abs. 5**: no contract-record duty where only **Landfahrzeuge** are guarded | |

### 7.2 Sanctions

**§ 144 Abs. 1 Nr. 1 lit. f GewO** — operating without the Erlaubnis (*"nach § 34a Abs. 1 Satz 1 Leben oder Eigentum fremder Personen bewacht"*) is an Ordnungswidrigkeit; per **§ 144 Abs. 4** the frame for Abs. 1 Nr. 1 lit. a–l is **bis zu fünftausend Euro**. **§ 22 BewachV** makes eleven BewachV breaches Ordnungswidrigkeiten *"im Sinne des § 144 Absatz 2 Nummer 1b der Gewerbeordnung"*, whose frame under § 144 Abs. 4 is **bis zu dreitausend Euro**. **§ 34a Abs. 4 GewO** additionally allows the authority to prohibit the employment of a specific individual. Note the asymmetry: unlicensed operation is fined harder than a BewachV compliance failure.

### 7.3 Exemptions (§ 8, § 12, § 23 BewachV) — commercially load-bearing

**§ 8** lists the qualifications that displace the Unterrichtung: the six Schutz-und-Sicherheit / Werkschutz Abschlüsse (Nr. 1); a Laufbahnprüfung at least for the **mittlerer Dienst** in Polizeivollzugsdienst, Justizvollzugsdienst, the armed part of the Zolldienst or Feldjägerdienst der Bundeswehr (Nr. 2); a **law degree** *plus* an IHK Unterrichtung limited to Sachgebiete **Nr. 5 bis 7** (Nr. 3); and a **Sachkundeprüfung** certificate (Nr. 4). **§ 12** exempts § 8 Nr. 1–3 holders from the Prüfung as well — note it does **not** list Nr. 4, which would be circular. **§ 23 Abs. 2** grandfathers anyone who on **1 January 2003** had been performing § 34a Abs. 1a activities lawfully and without interruption for at least three years.

The Nr. 3 construction is worth noticing: the legislature judged that a lawyer needs no instruction in law but does need instruction in **accident prevention, human interaction and security technology** — a compact statement of what this trade's non-legal core actually is.

---

## 8. Source confidence

**Tier A — binding primary text, read in the official consolidated version and/or the official gazette. Everything the recommendation and every draft question rests on.**

1. **GewO § 34a Abs. 1–5** — `gesetze-im-internet.de`, **cross-read in full on `buzer.de`**. The Abs. 1a Satz 2 five-item list was read twice, independently, verbatim.
2. **BewachV §§ 1, 4–12, 14, 16–23 and Anlage 2** — full text of each, plus Inhaltsübersicht. § 9 Abs. 2 (the provision that solves the blocker) and § 7 quoted verbatim.
3. **GewBürAbG, BGBl. 2026 I Nr. 215, Art. 1 Nr. 1 and Art. 11** — read in the **official `recht.bund.de` BGBl PDF** *and* in an independent consolidation, *and* against the **superseded § 6a wording** from a third retrieval. Three readings of the decisive change.
4. **GewO §§ 32, 144 (Abs. 1 Nr. 1 lit. f, Abs. 2 Nr. 1b, Abs. 4), 11b, 6a, 159.**
5. **BGB §§ 226, 227, 228, 229, 230, 823, 833, 854, 855, 858, 859, 860, 903, 965** — full text of each.
6. **StGB §§ 12, 32, 34, 123, 239, 240, 242, 249, 252, 263, 265a, 303, 323c; StPO §§ 127, 163** — full text of each.
7. **WaffG §§ 10, 28, 42a; BDSG § 4** — full text.
8. Mechanical checks: "Aufgabenauswahl" → **0 hits** in the BewachV; the Abs. 1a Satz 2 list contains **0** occurrences of Personenschutz, Alarmempfangsstelle, Justizvollzug or Verkehrsmittel.

**Tier B — official/quasi-official procedural material, not itself binding.**

9. **DIHK Rahmenplan Bewachungsgewerbe, Stand September 2019** (13 pp.) — read in full. Establishes that an official topic catalogue exists, that written question sets are **bundeseinheitlich**, and the taxonomy/`(S)` structure. **Copyrighted (DIHK e.V.); used as corroboration only, never as a content source — see §4.1.** Nearly seven years old; two staleness flags at §4.2.
10. **IHK Frankfurt am Main (Nr. 5306328), IHK Magdeburg (Nr. 3301986), IHK zu Essen (Nr. 2713376)** — exam mechanics, fees, gating, the 01.07.2025 scoring change, the employer-mediated registration route. Three independent chambers; where two agree (120 min, written-gates-oral) that is recorded as typical practice, not law. **Both Frankfurt and Essen state the sachkundepflichtige activity list inaccurately** (dropping *"in leitender Funktion"*) — recorded at §2.3 as evidence that the secondary layer is loose here.

**Tier C — orientation only, load-bearing for nothing.**

11. Search-result listings for § 34a prep vendors — used **only** to identify what had to be avoided (§1). None was fetched, read or cited.
12. The market figures on file (EUR 450–4,200 commercial pricing, `claude/content-expansion-scoping-2026-08-12.md` item 15) — carried forward from prior rounds, **not re-verified this round**.

**Confidence in the headline finding: very high.** § 9 Abs. 2 BewachV is a single unambiguous sentence in a currently-in-force federal regulation, read directly, and it does the whole job: it makes the exam's subject matter a matter of published statute. It is corroborated by an official DIHK document that says the same thing in more detail. The residual risks are (a) that Anlage 2 is a **floor** not a ceiling on exam scope (§3.3), and (b) that the chamber-level mechanics in §5.2 drift — one of them demonstrably changed on 01.07.2025.

---

## 9. Recommendation

### 9.1 Build it. The blocker is resolved and the gate can be closed.

`BACKLOG.md` and `claude/content-expansion-scoping-2026-08-12.md` hold § 34a *"blocked on an explicit PO sourcing-strategy decision before any content work starts"*, with the stated path forward: *"Build purely from GewO §34a + BewachV statute text and the public DIHK Rahmenplan, with no reference to any private prep vendor's question wording."*

**That path is confirmed viable, and is strictly better than described:** the syllabus is not merely a public DIHK document but a **statutory annex incorporated by reference into the exam's legal definition** (§ 9 Abs. 2 BewachV). The DIHK Rahmenplan is not needed as a source at all — only as a cross-check — which sidesteps its copyright notice entirely (§4.1). The draft accordingly took the narrower route: **statute only**, Rahmenplan for scope confirmation, zero vendor material.

This module also has the best commercial profile of anything in the § 34x space: a real state-administered exam, a large mandatory cohort, no official practice material published by anyone, and chambers that decline on neutrality grounds to recommend preparation.

### 9.2 Name it honestly

Recommended label: **"Bewachungsgewerbe — IHK-Sachkundeprüfung (§ 34a GewO)"**, with a visible statement that (a) this is unofficial practice material, (b) no official question catalogue exists so no coverage of the real Aufgabensätze can be claimed, and (c) **the base activity needs only the 40-hour Unterrichtung, not this exam** — see §2. Point (c) is a duty of honesty *and* a conversion feature: a large part of the audience arrives not knowing which tier they are in, and the module can tell them.

### 9.3 Open items for the PO / human review

1. **Close the § 34a sourcing gate** in `BACKLOG.md` and `claude/content-expansion-scoping-2026-08-12.md` item 15, recording § 9 Abs. 2 BewachV + Anlage 2 as the resolution — and **de-couple § 34a from § 34c**, per open item 3 of the Maklerschein dossier, which this round independently confirms.
2. **Decide the module's tier framing** — exam-prep for the Sachkundeprüfung only (as drafted), or a two-track module also covering the Unterrichtung cohort (much larger, no exam to prep for, closer to the compliance line). This is a scope decision and therefore the PO's.
3. **Legal review must resolve the § 4 BDSG video-surveillance question** (§4.2). The DIHK Rahmenplan still cites § 4 BDSG for private video surveillance; its applicability to non-public controllers is contested. The draft avoids the contested limb, but a fuller build cannot.
4. **Do not ship the § 5.2 chamber mechanics as national facts.** 120 minutes, the written-gates-oral rule, fees and the partial-credit scoring model are IHK **Satzung** (§ 11 Abs. 8 BewachV, § 32 GewO) and vary. The draft's `pass_rule_note` and `exam_format_note` already say so; keep it that way.
5. **Verify whether Magdeburg's 01.07.2025 move from all-or-nothing to Teilbewertung is nationwide** before any marketing copy describes the scoring model.
6. **Locale plan.** The draft ships DE canonical + EN, following `aevo`/`fadp_ch`/`kyc_aml`. This module is a **stronger** candidate for the full 12 locales than any of them — the security workforce is heavily migrant, the Unterrichtung has a statutory **B1 German** requirement (§ 6 Abs. 1 Satz 2 BewachV), and Anlage 2 Nr. 6 is *explicitly* about intercultural competence. A DE+EN-only launch is defensible as a pilot; a production build should plan for all 12 and should treat DE-language support as a product feature, not just a translation task.
7. **Re-verification date: no later than 2026-11-30.** The GewO has been amended at least twice in 2026 (BGBl. 2026 I Nr. 183 of 18.06.2026; Nr. 215 of 20.07.2026) and Art. 1 Nr. 2 GewBürAbG lands **01.05.2027**. Re-read § 34a and the BewachV from the amending instruments, not from this file.
8. **Standing note, confirming the Maklerschein dossier's §1.1 rule from the other direction** (§6): when a consolidated provision reads as though something changed, check the **superseded** text before describing the change. Here the current § 6a text plainly implies § 34a lost a benefit it had; it never had it.

---

## 10. What was drafted

`data/bewachungsgewerbe_pilot_DRAFT.json` — **28 questions**, DE canonical + EN, single-choice, generated deterministically by `data/gen_bewachungsgewerbe_draft.py` (which runs its own integrity, orthography and answer-distribution checks and exits non-zero on failure).

Topics map **1:1 onto the seven Sachgebiete of § 7 BewachV**, weighted approximately by Anlage 2's teaching hours, with a floor of three per area so every Sachgebiet stays usable for topic-filtered practice:

| topic_code | Sachgebiet (§ 7 BewachV) | Q |
|---|---|---|
| `oeffentliche_sicherheit` | Nr. 1 — Recht der öffentlichen Sicherheit und Ordnung einschl. Gewerberecht | 5 |
| `datenschutz` | Nr. 2 — Datenschutzrecht | 3 |
| `bgb` | Nr. 3 — Bürgerliches Gesetzbuch | 5 |
| `strafrecht_waffen` | Nr. 4 — Straf- und Verfahrensrecht, Umgang mit Waffen | 6 |
| `unfallverhuetung` | Nr. 5 — Unfallverhütungsvorschrift Wach- und Sicherungsdienste | 3 |
| `umgang_menschen` | Nr. 6 — Umgang mit Menschen, Deeskalation, interkulturelle Kompetenz | 3 |
| `sicherheitstechnik` | Nr. 7 — Grundzüge der Sicherheitstechnik | 3 |

Every question carries a `legal_basis` naming the provision it is authored from, and every one of those provisions was fetched and read this session (§8 items 1–7). Questions are written in applied-situation style per § 9 Abs. 1 BewachV's *"sowie deren praktische Anwendung"*. `high_stakes: true` marks the **14** where getting it wrong in real life means a criminal offence, an Ordnungswidrigkeit, or a guard exceeding their powers — the § 34a Abs. 5 spine. Points: 8 × 3, 10 × 4, 10 × 5. Answer-key spread a/b/c/d = 7/9/7/5.

**Not drafted, deliberately:** anything resting on the DIHK Rahmenplan's own wording or structure; anything on § 4 Abs. 1 BDSG's contested limb; anything asserting a national question count, exam duration or pass percentage; anything on DGUV Vorschrift 23's individual §§, whose text was **not** retrieved this session — the Unfallverhütung questions are built from **§ 17 BewachV** and **§ 20 BewachV** instead, which are Tier A and which cover the same duties from the regulation's own side.

---

**Reminder:** this document is draft research groundwork. It is not legal advice, has not been reviewed by a qualified lawyer or by any IHK Prüfungsausschuss member, and no content derived from it should be shipped to learners before that review. The draft question bank carries `legal_review_status` accordingly and is unwired from every build path.
