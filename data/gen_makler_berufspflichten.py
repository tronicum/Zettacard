#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator for data/makler_berufspflichten_pilot_DRAFT.json - "Immobilienmakler
- Berufspflichten (§ 34c GewO / MaBV)".

WHAT THIS MODULE IS (and is not): a professional-duties KNOWLEDGE CHECK for
licensed German real-estate brokers (Immobilienmakler, § 34c Abs. 1 Satz 1
Nr. 1 GewO) and their staff. It is deliberately NOT an exam simulator, framed
the same way data/cka_pilot.json is framed, because THERE IS NO STATE EXAM FOR
THIS TRADE: § 34c GewO has never contained a Sachkunde- or Prüfungs-
requirement, and the fallback Weiterbildungspflicht that used to apply to
brokers was repealed with effect from 24.07.2026. See docs/maklerschein-pre-
review-dossier-2026-08-17.md for the full finding.

DRAFT STATUS: filename carries the _DRAFT suffix on purpose. This module is
deliberately NOT registered in data/build_modules.py, data/modules_manifest.json
or app/data/modules.json, and app/app.js is untouched. Content-drafting round
only; a human review pass comes before anything ships. Same pipeline as the
DORA/CRA draft modules.

SOURCING (AGENTS.md constraint 1 - original synthesis from primary legal text
only; no exam-prep or compliance-training vendor's catalogue, question wording,
explanations or structure was read into or paraphrased into this file):

  Tier A (binding primary text, re-verified by direct curl against
  gesetze-im-internet.de on 2026-08-17 for THIS build - WebFetch is
  ROBOTS_DISALLOWED on that host in this sandbox, and the dossier's own
  citations were re-checked rather than trusted, per this repo's standing QA
  practice from the aevo / fadp_ch authoring rounds):
    - GewO § 34c (Immobilienmakler, Darlehensvermittler, Bauträger,
      Baubetreuer, Wohnimmobilienverwalter), Abs. 1-5 read in full
      https://www.gesetze-im-internet.de/gewo/__34c.html
      Vollzitat as retrieved: "Gewerbeordnung in der Fassung der Bekanntmachung
      vom 22. Februar 1999 (BGBl. I S. 202), die zuletzt durch Artikel 1 des
      Gesetzes vom 20. Juli 2026 (BGBl. 2026 I Nr. 215) geändert worden ist"
    - GewO §§ 144, 145, 146 (Bußgeldvorschriften)
    - MaBV (Makler- und Bauträgerverordnung) §§ 1, 2, 3, 7, 8, 10, 11, 14, 15,
      15a, 15b, 16, 18, 19 and Anlagen 1-2 (Anlage 3 confirmed "(weggefallen)")
      NOTE THE NON-OBVIOUS URL SLUG: /gewo_34cdv/, NOT /mabv/ (which 404s).
      https://www.gesetze-im-internet.de/gewo_34cdv/__10.html etc.
      Vollzitat as retrieved: "Makler- und Bauträgerverordnung in der Fassung
      der Bekanntmachung vom 7. November 1990 (BGBl. I S. 2479), die zuletzt
      durch Artikel 2 der Verordnung vom 28. Juli 2026 (BGBl. 2026 I Nr. 229)
      geändert worden ist"
    - GwG §§ 1 Abs. 11, 2 Abs. 1 Nr. 14, 6 Abs. 2 Nr. 6, 10 Abs. 6, 16a
    - GwGMeldV-Immobilien § 1 (negative finding: scope limited to § 2 Abs. 1
      Nr. 10 und 12 GwG, i.e. NOT brokers)
    - GModG (formerly GEG) §§ 80, 87 - see the currency note below

  Tier B (official/quasi-official, not binding, labelled as such wherever it
  matters): DIHK "FAQ: Weiterbildungspflicht für Immobilienmakler und
  Wohnimmobilienverwalter", Stand Januar 2025 - now HISTORICALLY SUPERSEDED for
  the broker half. Not load-bearing for any answer key in this file.

CURRENCY FINDINGS FROM THIS BUILD'S OWN RE-VERIFICATION (both new relative to
the dossier, both recorded because they change wording):
  1. GEG -> GModG. The Gebäudeenergiegesetz has been RENAMED to
     "Gebäudemodernisierungsgesetz (GModG)" - full title "Gesetz zur Einsparung
     von Energie und zur Modernisierung der Wärmeversorgung in Gebäuden" - by
     Art. 1 Nr. 1 G v. 23.07.2026 (BGBl. 2026 I Nr. 226), with effect from
     29.07.2026 (gesetze-im-internet.de records: 'Überschrift: IdF d. Art. 1
     Nr. 1 G v. 23.7.2026 I Nr. 226 mWv 29.7.2026'). The URL slug is still
     /geg/. The dossier (§4.2) correctly said "use GEG, not EnEV"; as of this
     build the correct short form is GModG. Cited here as
     "GModG (bis 28.07.2026: GEG)".
  2. § 1 Abs. 2 Satz 2 MaBV is MORE precise than the dossier's paraphrase
     ("§§ 11, 15-15b, 18 und 19"): the actual text carves in "§§ 11, 15 bis
     15b, 18 Absatz 1 Nummer 7, 9 und 10, Absatz 2 und 3 sowie § 19".

Run from data/:  python3 gen_makler_berufspflichten.py
Do NOT run build_modules.py for this file - it is a draft.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "makler_berufspflichten_pilot_DRAFT.json")

TOPICS = {
    "erlaubnis": "Erlaubnis nach § 34c GewO",
    "mabv_pflichten": "Berufspflichten nach der MaBV",
    "sanktionen": "Ordnungswidrigkeiten und Sanktionen",
    "gwg_makler": "Geldwäscherecht: maklerspezifische Pflichten",
    "abgrenzung": "Abgrenzung der vier Erlaubnistatbestände",
}

TOPIC_LABELS_EN = {
    "erlaubnis": "Permission under § 34c GewO",
    "mabv_pflichten": "Professional duties under the MaBV",
    "sanktionen": "Administrative offences and sanctions",
    "gwg_makler": "Anti-money-laundering: broker-specific duties",
    "abgrenzung": "Telling the four permission limbs apart",
}

# Standing pointer sentence appended to every gwg_makler explanation, mirroring
# the fadp_ch <-> datenschutz and dora_audit_readiness <-> dora_procurement
# precedents: cross-link, never duplicate.
KYC_POINTER_DE = (
    " Für das allgemeine Geldwäscheregime - Typologien, Drei-Phasen-Modell, "
    "politisch exponierte Personen, Mechanik der Verdachtsmeldung nach § 43 GwG "
    "und Bußgeldrahmen - siehe das Modul 'kyc_aml'; dieses Modul behandelt nur "
    "die maklerspezifischen Vorschriften und dupliziert 'kyc_aml' bewusst nicht."
)
KYC_POINTER_EN = (
    " For the general anti-money-laundering regime - typologies, the three-phase "
    "model, politically exposed persons, the mechanics of a suspicious activity "
    "report under § 43 GwG and the fine ranges - see the 'kyc_aml' module; this "
    "module deliberately covers only the broker-specific provisions and does not "
    "duplicate 'kyc_aml'."
)

Q = []


def q(topic_code, num, legal_basis, points, high_stakes, roles, correct,
      de_q, de_opts, en_q, en_opts, de_expl, en_expl):
    Q.append({
        "id": f"makler_berufspflichten-{topic_code}-{num:02d}",
        "topic": TOPICS[topic_code],
        "topic_code": topic_code,
        "class_scope": ["ALL"],
        "grundstoff": True,
        "legal_basis": legal_basis,
        "points": points,
        "high_stakes": high_stakes,
        "question_type": "single_choice",
        "image_ref": None,
        "correct": [correct],
        "roles": roles,
        "text": {
            "de": {"question": de_q, "options": de_opts},
            "en": {"question": en_q, "options": en_opts},
        },
        "explanation": {"de": de_expl, "en": en_expl},
    })


# ===========================================================================
# Topic 1: erlaubnis - § 34c GewO
# ===========================================================================

q("erlaubnis", 1, "§ 34c Abs. 1 Satz 1 Nr. 1 GewO", 4, True, ["all"], "c",
  "Welche Tätigkeit ist genau der Erlaubnistatbestand des Immobilienmaklers nach § 34c Absatz 1 Satz 1 Nummer 1 GewO?",
  {
    "a": "Das gewerbsmäßige Bewerten von Grundstücken und Gebäuden",
    "b": "Das gewerbsmäßige Verwalten fremder Wohnimmobilien",
    "c": "Das gewerbsmäßige Vermitteln des Abschlusses von Verträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume oder das Nachweisen der Gelegenheit zum Abschluss solcher Verträge",
    "d": "Das gewerbsmäßige Vorbereiten und Durchführen von Bauvorhaben im eigenen Namen",
  },
  "Which activity is precisely the real-estate broker's permission limb under § 34c(1) sentence 1 no. 1 GewO?",
  {
    "a": "Commercially valuing land and buildings",
    "b": "Commercially managing residential property for others",
    "c": "Commercially brokering the conclusion of contracts on land, rights equivalent to land, commercial premises or residential premises, or providing the opportunity to conclude such contracts",
    "d": "Commercially preparing and carrying out construction projects in one's own name",
  },
  "§ 34c Abs. 1 Satz 1 Nr. 1 GewO erfasst wortlautgetreu, wer gewerbsmäßig „den Abschluss von Verträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume vermitteln oder die Gelegenheit zum Abschluss solcher Verträge nachweisen“ will. Erfasst sind damit beide klassischen Maklerleistungen: die Vermittlung UND der bloße Nachweis. Antwort b ist Nummer 4 (Wohnimmobilienverwalter), Antwort d ist Nummer 3 Buchstabe a (Bauträger). Die reine Wertermittlung ist in § 34c GewO überhaupt nicht als Erlaubnistatbestand genannt - sie ist gewerberechtlich erlaubnisfrei (Sachverständigenbestellungen nach § 36 GewO sind etwas anderes). Nach § 34c Abs. 1 Satz 2 GewO kann die Erlaubnis inhaltlich beschränkt und mit Auflagen verbunden werden, auch nachträglich.",
  "§ 34c(1) sentence 1 no. 1 GewO covers, in its own words, anyone who commercially intends to \"broker the conclusion of contracts on land, rights equivalent to land, commercial premises or residential premises, or provide the opportunity to conclude such contracts\". Both classic broker services are therefore caught: brokering AND the bare introduction/referral. Answer b is no. 4 (residential property manager), answer d is no. 3(a) (property developer). Pure valuation work is not a permission limb in § 34c GewO at all - it needs no trade permission (public appointment as an expert under § 36 GewO is a different matter). Under § 34c(1) sentence 2 GewO the permission may be limited in substance and made subject to conditions, including subsequently."),

q("erlaubnis", 2, "§ 34c Abs. 2 GewO", 5, True, ["all"], "d",
  "Ein Bewerber um die Maklererlaubnis fragt, wie er den erforderlichen Sachkundenachweis erbringt. Was ist die zutreffende Antwort?",
  {
    "a": "Durch eine Sachkundeprüfung vor der Industrie- und Handelskammer, wie bei Versicherungsvermittlern",
    "b": "Durch einen Berufsabschluss als Immobilienkaufmann oder eine gleichwertige Qualifikation",
    "c": "Durch eine Sachkundeprüfung, deren Einzelheiten die Länder festlegen",
    "d": "Es gibt für Immobilienmakler keinen Sachkundenachweis - § 34c Absatz 2 GewO enthält eine abschließende Aufzählung von Versagungsgründen, in der Sachkunde nicht vorkommt",
  },
  "An applicant for a broker permission asks how to furnish the required proof of professional competence (Sachkundenachweis). What is the correct answer?",
  {
    "a": "By a competence examination before the Chamber of Industry and Commerce, as for insurance intermediaries",
    "b": "By a vocational qualification as Immobilienkaufmann or an equivalent qualification",
    "c": "By a competence examination whose details are set by the Länder",
    "d": "There is no competence requirement for real-estate brokers at all - § 34c(2) GewO contains an exhaustive list of grounds for refusal, and competence is not among them",
  },
  "Das ist die für die Praxis wertvollste Aussage dieses Moduls, weil nahezu die gesamte Sekundärliteratur - IHK-Seiten, Verbandsseiten, Ratgeberportale - das Gegenteil suggeriert. § 34c Abs. 2 GewO lautet „Die Erlaubnis ist zu versagen, wenn“ und nennt danach genau drei Gründe: fehlende Zuverlässigkeit (Nr. 1), ungeordnete Vermögensverhältnisse (Nr. 2) und - nur für Wohnimmobilienverwalter nach Absatz 1 Satz 1 Nummer 4 - der fehlende Nachweis einer Berufshaftpflichtversicherung (Nr. 3). Die Formulierung „ist zu versagen, wenn“ macht die Aufzählung abschließend; ein Wissenstest lässt sich nicht hineinlesen. Der Begriff „Sachkunde“ kommt in § 34c GewO nicht ein einziges Mal vor und in der gesamten MaBV ebenfalls nicht (mechanische Prüfung der abgerufenen Texte am 17.08.2026). Zum Vergleich: § 34d Abs. 2 Nr. 4 GewO (Versicherungsvermittler) und § 34f Abs. 2 Nr. 4 GewO (Finanzanlagenvermittler) verlangen ausdrücklich eine „vor der Industrie- und Handelskammer erfolgreich abgelegte Prüfung“ - der Gesetzgeber kann eine Sachkundeprüfung also schreiben und hat es in derselben Vorschriftenfamilie dreimal getan. Ihr Fehlen in § 34c GewO ist eine bewusste Entscheidung. Antwort c ist zusätzlich falsch, weil § 34c GewO Bundesrecht ist und die Länder lediglich die zuständige Behörde bestimmen.",
  "This is the single most valuable proposition in this module, because virtually the whole secondary layer - chamber pages, trade-body pages, advice portals - suggests the opposite. § 34c(2) GewO reads \"the permission must be refused if\" and then lists exactly three grounds: lack of reliability (no. 1), disordered financial circumstances (no. 2) and - only for residential property managers under (1) sentence 1 no. 4 - failure to prove professional indemnity insurance (no. 3). The phrase \"must be refused if\" makes the list exhaustive; a knowledge test cannot be read into it. The word \"Sachkunde\" does not appear once in § 34c GewO, nor anywhere in the MaBV (mechanical check over the texts retrieved on 2026-08-17). By contrast, § 34d(2) no. 4 GewO (insurance intermediaries) and § 34f(2) no. 4 GewO (financial investment intermediaries) expressly require an \"examination successfully passed before the Chamber of Industry and Commerce\" - so the legislature knows how to write a competence-examination requirement and has done so three times in the same family of provisions. Its absence from § 34c GewO is a deliberate choice. Answer c is additionally wrong because § 34c GewO is federal law; the Länder only designate the competent authority."),

q("erlaubnis", 3, "§ 34c Abs. 2 Nr. 3 GewO; §§ 15, 15a MaBV", 5, True, ["management"], "b",
  "Die Erlaubnisbehörde fordert von einem reinen Immobilienmakler (nur Vermittlung und Nachweis) den Nachweis einer Berufshaftpflichtversicherung. Wie ist das rechtlich zu bewerten?",
  {
    "a": "Zu Recht - jeder Gewerbetreibende nach § 34c GewO muss eine Berufshaftpflichtversicherung nachweisen",
    "b": "Zu Unrecht - § 34c Absatz 2 Nummer 3 GewO ist ausdrücklich auf Gewerbetreibende nach Absatz 1 Satz 1 Nummer 4 (Wohnimmobilienverwalter) beschränkt",
    "c": "Zu Recht, allerdings erst ab einem Jahresumsatz von 500 000 Euro",
    "d": "Zu Unrecht, weil die Versicherungspflicht nur Bauträger nach Nummer 3 trifft",
  },
  "The licensing authority demands proof of professional indemnity insurance from a pure real-estate broker (brokering and referral only). Is that lawful?",
  {
    "a": "Yes - every trader under § 34c GewO must prove professional indemnity insurance",
    "b": "No - § 34c(2) no. 3 GewO is expressly limited to traders under (1) sentence 1 no. 4 (residential property managers)",
    "c": "Yes, but only above annual turnover of EUR 500,000",
    "d": "No, because the insurance duty applies only to property developers under no. 3",
  },
  "§ 34c Abs. 2 Nr. 3 GewO versagt die Erlaubnis, wenn „der Antragsteller, der ein Gewerbe nach Absatz 1 Satz 1 Nummer 4 betreiben will, den Nachweis einer Berufshaftpflichtversicherung nicht erbringen kann“. Der Relativsatz beschränkt den Versagungsgrund ausdrücklich auf Nummer 4, also auf Wohnimmobilienverwalter. Ein Makler nach Nummer 1 braucht nur Zuverlässigkeit und geordnete Vermögensverhältnisse - das ist alles. Die Ausgestaltung der Verwalter-Pflichtversicherung steht in §§ 15, 15a MaBV: Mindestversicherungssumme 500 000 Euro je Versicherungsfall und 1 000 000 Euro für alle Versicherungsfälle eines Jahres (§ 15 Abs. 2 MaBV), Versicherungsbestätigung bei Antragstellung nicht älter als drei Monate (§ 15a Abs. 1 MaBV). Praxishinweis, der die Rechtsfrage nicht berührt: viele Makler unterhalten freiwillig eine Vermögensschaden-Haftpflichtversicherung; das ist kaufmännisch sinnvoll, aber keine Erlaubnisvoraussetzung. Antwort d ist ebenfalls falsch - Bauträger nach Nummer 3 unterliegen keiner Pflichtversicherung nach § 34c Abs. 2 GewO, sondern den Sicherungspflichten der §§ 2 bis 7 MaBV.",
  "§ 34c(2) no. 3 GewO refuses the permission where \"the applicant, who intends to carry on a trade under (1) sentence 1 no. 4, cannot furnish proof of professional indemnity insurance\". The relative clause expressly confines the ground for refusal to no. 4, i.e. residential property managers. A broker under no. 1 needs only reliability and ordered financial circumstances - that is the whole list. The detail of the manager's compulsory insurance is in §§ 15, 15a MaBV: minimum sum insured EUR 500,000 per claim and EUR 1,000,000 for all claims in a year (§ 15(2) MaBV), and the insurer's confirmation must be no more than three months old at the time of application (§ 15a(1) MaBV). A practice note that does not affect the legal question: many brokers voluntarily carry pecuniary-loss liability cover; that is commercially sensible but not a licensing condition. Answer d is also wrong - developers under no. 3 are not subject to compulsory insurance under § 34c(2) GewO but to the client-asset security duties of §§ 2 to 7 MaBV."),

q("erlaubnis", 4, "§ 34c Abs. 2a GewO idF d. Art. 1 Nr. 3 GewBürAbG v. 20.07.2026 (BGBl. 2026 I Nr. 215)", 5, True, ["all"], "c",
  "Welche Weiterbildungspflicht trifft einen Immobilienmakler nach § 34c Absatz 2a GewO im aktuell geltenden Recht (Stand 17.08.2026)?",
  {
    "a": "20 Stunden in drei Kalenderjahren, wie bisher",
    "b": "20 Stunden pro Kalenderjahr",
    "c": "Keine - Absatz 2a erfasst seit dem 24.07.2026 nur noch Gewerbetreibende nach Absatz 1 Satz 1 Nummer 4 (Wohnimmobilienverwalter)",
    "d": "40 Stunden in drei Kalenderjahren, wenn er auch verwaltet",
  },
  "Which continuing-education duty applies to a real-estate broker under § 34c(2a) GewO as the law currently stands (as at 2026-08-17)?",
  {
    "a": "20 hours in three calendar years, as before",
    "b": "20 hours per calendar year",
    "c": "None - since 24 July 2026, (2a) covers only traders under (1) sentence 1 no. 4 (residential property managers)",
    "d": "40 hours in three calendar years if he also manages property",
  },
  "Das Gesetz zum Bürokratierückbau in der Gewerbeordnung und dem Energieverbrauchskennzeichnungsgesetz sowie anderer Rechtsvorschriften zur Aufhebung von Berichtspflichten vom 20.07.2026 (BGBl. 2026 I Nr. 215) hat in Artikel 1 Nummer 3 in § 34c Absatz 2a Satz 1 GewO die Angabe „Absatz 1 Satz 1 Nummer 1 und 4“ durch „Absatz 1 Satz 1 Nummer 4“ ersetzt. Nach Artikel 11 Absatz 1 trat die Änderung am Tag nach der Verkündung in Kraft, also am 24.07.2026. Der konsolidierte Text lautet seither: „Gewerbetreibende nach Absatz 1 Satz 1 Nummer 4 sind verpflichtet, sich in einem Umfang von 20 Stunden innerhalb eines Zeitraums von drei Kalenderjahren weiterzubilden“ - Nummer 1, der Makler, ist aus dem Satz verschwunden (am 17.08.2026 unmittelbar am konsolidierten Text nachgeprüft). Artikel 2 Nummer 4 desselben Gesetzes hat zusätzlich Teil A der Anlage 1 MaBV, also den Makler-Lehrplan selbst, gestrichen; die Anlage trägt heute nur noch die Überschrift „Inhaltliche Anforderungen an die Weiterbildung für Wohnimmobilienverwalter“, und Anlage 3 MaBV ist „(weggefallen)“. WICHTIG für die eigene Praxis: IHK-Seiten, Verbandsinformationen und die DIHK-FAQ (Stand Januar 2025) beschreiben durchweg noch den alten Rechtszustand. Wenn konsolidierter Gesetzestext und Praktikerkonsens auseinanderfallen, entscheidet das Änderungsgesetz, nicht die lautere Quelle. Für Wohnimmobilienverwalter besteht die Pflicht unverändert weiter - siehe das Modul 'immobilienverwalter_weiterbildung'.",
  "The Act on cutting bureaucracy in the Trade Regulation Act and the Energy Consumption Labelling Act and other provisions repealing reporting duties, of 20 July 2026 (BGBl. 2026 I no. 215), replaced in Article 1 no. 3 the reference \"(1) sentence 1 nos. 1 and 4\" in § 34c(2a) sentence 1 GewO with \"(1) sentence 1 no. 4\". Under Article 11(1) the change entered into force on the day after promulgation, i.e. 24 July 2026. The consolidated text now reads: \"Traders under (1) sentence 1 no. 4 are obliged to undertake 20 hours of continuing education within a period of three calendar years\" - no. 1, the broker, has disappeared from the sentence (verified directly against the consolidated text on 2026-08-17). Article 2 no. 4 of the same Act additionally deleted Part A of Annex 1 MaBV, i.e. the broker syllabus itself; the annex is now headed simply \"Content requirements for the continuing education of residential property managers\", and Annex 3 MaBV is \"(repealed)\". IMPORTANT in practice: chamber pages, trade-body information and the DIHK FAQ (as at January 2025) all still describe the old position. Where consolidated statutory text and practitioner consensus diverge, the amending instrument decides, not the louder source. For residential property managers the duty continues unchanged - see the 'immobilienverwalter_weiterbildung' module."),

q("erlaubnis", 5, "§ 34c Abs. 2 Nr. 1 und 2 GewO", 4, False, ["management"], "b",
  "Welcher Umstand begründet nach § 34c Absatz 2 GewO in der Regel das Fehlen der erforderlichen Zuverlässigkeit?",
  {
    "a": "Eine Verurteilung wegen einer Verkehrsordnungswidrigkeit in den letzten fünf Jahren",
    "b": "Eine rechtskräftige Verurteilung in den letzten fünf Jahren vor Antragstellung wegen eines Verbrechens oder wegen Diebstahls, Unterschlagung, Erpressung, Betruges, Untreue, Geldwäsche, Urkundenfälschung, Hehlerei, Wuchers oder einer Insolvenzstraftat",
    "c": "Jede Eintragung im Gewerbezentralregister",
    "d": "Das Fehlen einer kaufmännischen Berufsausbildung",
  },
  "Which circumstance, as a rule, establishes a lack of the required reliability under § 34c(2) GewO?",
  {
    "a": "A conviction for a road-traffic administrative offence within the last five years",
    "b": "A final conviction within the five years before the application for a serious criminal offence (Verbrechen) or for theft, embezzlement, extortion, fraud, breach of trust, money laundering, forgery of documents, handling stolen goods, usury or an insolvency offence",
    "c": "Any entry in the central trade register",
    "d": "The absence of a commercial vocational qualification",
  },
  "§ 34c Abs. 2 Nr. 1 GewO enthält eine Regelvermutung mit einem geschlossenen Deliktskatalog: „die erforderliche Zuverlässigkeit besitzt in der Regel nicht, wer in den letzten fünf Jahren vor Stellung des Antrages wegen eines Verbrechens oder wegen Diebstahls, Unterschlagung, Erpressung, Betruges, Untreue, Geldwäsche, Urkundenfälschung, Hehlerei, Wuchers oder einer Insolvenzstraftat rechtskräftig verurteilt worden ist“. Die Vermutung erfasst nicht nur den Antragsteller, sondern auch „eine der mit der Leitung des Betriebes oder einer Zweigniederlassung beauftragten Personen“ - bei Gesellschaften ist also die Geschäftsführungsebene mitzuprüfen. Nummer 2 betrifft ungeordnete Vermögensverhältnisse und ist ebenfalls mit einer Regelvermutung ausgestattet: sie liegen in der Regel vor, wenn das Insolvenzverfahren über das Vermögen des Antragstellers eröffnet wurde oder er im Verzeichnis des Vollstreckungsgerichts nach § 26 Abs. 2 InsO oder § 882b ZPO eingetragen ist. Antwort d beschreibt gerade das, was § 34c GewO NICHT verlangt (siehe die Frage zum Sachkundenachweis).",
  "§ 34c(2) no. 1 GewO contains a rule-of-thumb presumption with a closed list of offences: \"as a rule, the required reliability is not possessed by anyone who, within the five years before the application was made, has been finally convicted of a serious criminal offence or of theft, embezzlement, extortion, fraud, breach of trust, money laundering, forgery of documents, handling stolen goods, usury or an insolvency offence\". The presumption covers not only the applicant but also \"any of the persons entrusted with the management of the business or of a branch\" - so for companies the management tier must be screened too. No. 2 concerns disordered financial circumstances and also carries a presumption: as a rule these exist where insolvency proceedings have been opened over the applicant's assets or the applicant is entered in the enforcement court's register under § 26(2) InsO or § 882b ZPO. Answer d describes precisely what § 34c GewO does NOT require (see the question on proof of competence)."),

q("erlaubnis", 6, "§ 34c Abs. 5 Nr. 4 GewO; § 481 BGB", 3, False, ["all"], "a",
  "Für welche Vermittlungstätigkeit gilt die Erlaubnispflicht des § 34c Absatz 1 GewO nach Absatz 5 ausdrücklich NICHT?",
  {
    "a": "Für den Nachweis oder die Vermittlung der Teilzeitnutzung von Wohngebäuden im Sinne des § 481 BGB",
    "b": "Für die Vermittlung von Ferienwohnungen an Urlaubsgäste",
    "c": "Für die Vermittlung von Gewerberäumen an eingetragene Kaufleute",
    "d": "Für die Vermittlung von Grundstücken unterhalb eines Kaufpreises von 100 000 Euro",
  },
  "For which brokerage activity does the permission requirement of § 34c(1) GewO expressly NOT apply under (5)?",
  {
    "a": "For introducing or brokering timeshare use of residential buildings within the meaning of § 481 BGB",
    "b": "For brokering holiday flats to holidaymakers",
    "c": "For brokering commercial premises to registered merchants",
    "d": "For brokering land below a purchase price of EUR 100,000",
  },
  "§ 34c Abs. 5 GewO nimmt vier Fallgruppen aus, darunter Nummer 4: „Verträge, soweit Teilzeitnutzung von Wohngebäuden im Sinne des § 481 des Bürgerlichen Gesetzbuches gemäß Absatz 1 Satz 1 Nr. 1 nachgewiesen oder vermittelt wird“ - Timesharing also. Die übrigen drei Ausnahmen betreffen beaufsichtigte Finanzunternehmen (Nr. 1, 1a: Kreditinstitute mit Erlaubnis nach § 32 Abs. 1 KWG, Wertpapierinstitute, Kapitalverwaltungsgesellschaften), Absatzfinanzierung eigener Warenverkäufe (Nr. 2) und die Interbanken-Darlehensvermittlung nach § 53b Abs. 7 KWG (Nr. 3). Keine Ausnahme knüpft an einen Kaufpreis, eine Objektart oder die Kaufmannseigenschaft des Auftraggebers an - Antwort d gibt es also nicht. Achtung, häufige Verwechslung: die Kaufmannseigenschaft des Auftraggebers spielt eine Rolle, aber an anderer Stelle - § 7 Abs. 2 MaBV lässt einen Verzicht auf die Sicherungsvorschriften zu, wenn der Auftraggeber eine juristische Person des öffentlichen Rechts oder ein eingetragener Kaufmann ist. Das ist eine Befreiung von MaBV-Pflichten, nicht von der Erlaubnispflicht.",
  "§ 34c(5) GewO exempts four groups of cases, including no. 4: \"contracts, in so far as timeshare use of residential buildings within the meaning of § 481 BGB is introduced or brokered under (1) sentence 1 no. 1\" - i.e. timesharing. The other three exemptions concern supervised financial undertakings (nos. 1, 1a: credit institutions licensed under § 32(1) KWG, securities institutions, capital management companies), sales financing of the trader's own goods (no. 2) and interbank loan brokerage under § 53b(7) KWG (no. 3). No exemption turns on a purchase price, a property type or the client's merchant status - so answer d does not exist. A frequent confusion: the client's merchant status does matter, but elsewhere - § 7(2) MaBV permits a waiver of the client-asset security provisions where the client is a public-law legal person or a registered merchant. That is an exemption from MaBV duties, not from the permission requirement."),


# ===========================================================================
# Topic 2: mabv_pflichten
# ===========================================================================

q("mabv_pflichten", 1, "§ 1 Abs. 1 und Abs. 2 Satz 2 MaBV", 5, True, ["management"], "c",
  "Wie ist der Anwendungsbereich der MaBV nach § 1 MaBV zugeschnitten?",
  {
    "a": "Die MaBV gilt nur für Gewerbetreibende, die tatsächlich eine Erlaubnis nach § 34c GewO besitzen",
    "b": "Die MaBV gilt für alle Gewerbetreibenden nach § 34c Absatz 1 GewO in gleichem Umfang",
    "c": "Die MaBV gilt für alle Tätigkeiten nach § 34c Absatz 1 GewO unabhängig vom Bestehen einer Erlaubnispflicht, für Wohnimmobilienverwalter aber nur mit einem ausdrücklich aufgezählten Teil ihrer Vorschriften",
    "d": "Die MaBV gilt ausschließlich für Bauträger und Baubetreuer",
  },
  "How is the MaBV's scope of application framed by § 1 MaBV?",
  {
    "a": "The MaBV applies only to traders who actually hold a permission under § 34c GewO",
    "b": "The MaBV applies to all traders under § 34c(1) GewO to the same extent",
    "c": "The MaBV applies to all activities under § 34c(1) GewO regardless of whether a permission is required, but to residential property managers only through an expressly listed subset of its provisions",
    "d": "The MaBV applies exclusively to property developers and construction supervisors",
  },
  "§ 1 Abs. 1 MaBV: „Diese Verordnung gilt für Gewerbetreibende, die Tätigkeiten nach § 34c Absatz 1 der Gewerbeordnung ausüben, unabhängig vom Bestehen einer Erlaubnispflicht.“ Der Zusatz ist wichtig: wer die Tätigkeit ausübt, ist an die MaBV gebunden, auch wenn er - etwa nach § 34c Abs. 5 GewO - keiner Erlaubnis bedarf. § 1 Abs. 2 Satz 2 MaBV nimmt Wohnimmobilienverwalter dann wieder weitgehend aus: die Verordnung gilt für sie nicht, „mit Ausnahme der §§ 11, 15 bis 15b, 18 Absatz 1 Nummer 7, 9 und 10, Absatz 2 und 3 sowie § 19 dieser Verordnung“. Daraus folgt eine bemerkenswerte Umkehrung, die man sich merken sollte: die operativen MaBV-Pflichten - Sicherungspflichten, Buchführung, Aufbewahrung, Rechnungslegung, Prüfungen - sind im Kern ein Makler- und Bauträgerregime, kein Verwalterregime. Der Verwalter hat dafür den Weiterbildungslehrplan (Anlage 1) und die Pflichtversicherung, die dem Makler gerade nicht auferlegt sind. Zwei benachbarte Erlaubnistatbestände, zwei völlig unterschiedliche Pflichtenbündel.",
  "§ 1(1) MaBV: \"This Regulation applies to traders who carry on activities under § 34c(1) of the Trade Regulation Act, irrespective of whether a permission is required.\" The rider matters: anyone carrying on the activity is bound by the MaBV even if - for example under § 34c(5) GewO - no permission is needed. § 1(2) sentence 2 MaBV then largely carves residential property managers back out: the Regulation does not apply to them \"with the exception of §§ 11, 15 to 15b, 18(1) nos. 7, 9 and 10, (2) and (3), and § 19 of this Regulation\". That produces a striking inversion worth remembering: the operative MaBV duties - client-asset security, bookkeeping, retention, accounting, audits - are essentially a broker/developer regime, not a manager regime. The manager instead has the continuing-education syllabus (Annex 1) and the compulsory insurance, neither of which is imposed on the broker. Two adjacent permission limbs, two completely different bundles of duties."),

q("mabv_pflichten", 2, "§ 10 Abs. 1 MaBV", 4, False, ["all"], "b",
  "Ab welchem Zeitpunkt und in welcher Form muss ein Makler die Aufzeichnungen nach § 10 MaBV führen?",
  {
    "a": "Ab Abschluss des vermittelten Vertrages, in beliebiger Sprache",
    "b": "Von der Annahme des Auftrages an, unverzüglich und in deutscher Sprache",
    "c": "Erst auf Verlangen der zuständigen Behörde",
    "d": "Zum Ende jedes Kalenderjahres im Rahmen der Bilanzierung",
  },
  "From what point in time, and in what form, must a broker keep the records required by § 10 MaBV?",
  {
    "a": "From conclusion of the brokered contract, in any language",
    "b": "From acceptance of the mandate onwards, without delay and in German",
    "c": "Only on request by the competent authority",
    "d": "At the end of each calendar year as part of preparing the annual accounts",
  },
  "§ 10 Abs. 1 MaBV: „Der Gewerbetreibende hat von der Annahme des Auftrages an nach Maßgabe der folgenden Vorschriften Aufzeichnungen zu machen sowie Unterlagen und Belege übersichtlich zu sammeln. Die Aufzeichnungen sind unverzüglich und in deutscher Sprache vorzunehmen.“ Drei Merkmale sind prüfungs- und aufsichtsrelevant: der Startzeitpunkt ist die Auftragsannahme (nicht der Vertragsschluss über das Objekt), die Aufzeichnung muss unverzüglich erfolgen (nicht nachträglich rekonstruiert werden), und sie muss in deutscher Sprache erfolgen. Die Pflicht tritt nach § 10 Abs. 6 MaBV neben andere Aufzeichnungs- und Buchführungspflichten, insbesondere die handels- und steuerrechtlichen - sie ersetzt sie nicht. Ein Verstoß gegen § 10 Abs. 1 bis 5 MaBV ist nach § 18 Abs. 1 Nr. 6 MaBV eine Ordnungswidrigkeit.",
  "§ 10(1) MaBV: \"From acceptance of the mandate onwards, the trader must make records in accordance with the following provisions and collect documents and vouchers in an orderly manner. The records must be made without delay and in the German language.\" Three features matter for supervision: the start point is acceptance of the mandate (not conclusion of the contract about the property), the record must be made without delay (not reconstructed afterwards), and it must be in German. Under § 10(6) MaBV the duty sits alongside other record-keeping and bookkeeping duties, in particular those under commercial and tax law - it does not replace them. A breach of § 10(1) to (5) MaBV is an administrative offence under § 18(1) no. 6 MaBV."),

q("mabv_pflichten", 3, "§ 10 Abs. 3 Nr. 1 MaBV", 4, False, ["all"], "d",
  "§ 10 Absatz 3 MaBV verlangt von Gewerbetreibenden nach § 34c Absatz 1 Satz 1 Nummer 1 GewO zusätzliche Angaben. Welche Angabe gehört bei der Vermittlung eines Grundstückskaufs dazu?",
  {
    "a": "Der Beleihungswert nach Einschätzung des Maklers",
    "b": "Die Bonitätsauskunft über den Erwerbsinteressenten",
    "c": "Der voraussichtliche Grunderwerbsteuerbetrag",
    "d": "Die Höhe der Kaufpreisforderung einschließlich zu übernehmender Belastungen sowie Name, Vorname und Anschrift des Veräußerers",
  },
  "§ 10(3) MaBV requires additional particulars from traders under § 34c(1) sentence 1 no. 1 GewO. Which particular belongs there when brokering a sale of land?",
  {
    "a": "The mortgage lending value as estimated by the broker",
    "b": "A credit report on the prospective purchaser",
    "c": "The expected amount of real-property transfer tax",
    "d": "The amount of the purchase price claimed including encumbrances to be assumed, plus the seller's surname, first name and address",
  },
  "§ 10 Abs. 3 MaBV ist der maklerspezifische Absatz: er gilt ausdrücklich nur für Gewerbetreibende im Sinne des § 34c Absatz 1 Satz 1 Nummer 1 GewO und verlangt, soweit im Einzelfall in Betracht kommend, bei der Vermittlung von Erwerbsverträgen über Grundstücke oder grundstücksgleiche Rechte (Nr. 1): „Lage, Größe und Nutzungsmöglichkeit des Grundstücks, Art, Alter und Zustand des Gebäudes, Ausstattung, Wohn- und Nutzfläche, Zahl der Zimmer, Höhe der Kaufpreisforderung einschließlich zu übernehmender Belastungen, Name, Vorname und Anschrift des Veräußerers“. Für Nutzungsverträge über Grundstücke (Nr. 2) und über gewerbliche Räume oder Wohnräume (Nr. 3) sind die Kataloge ähnlich aufgebaut, treten aber an die Stelle der Kaufpreisforderung mit der Höhe der Mietforderung und gegebenenfalls Baukostenzuschuss, Kaution, Mietvorauszahlung, Mieterdarlehen oder Abstandssumme. Bonität, Beleihungswert und Steuerbeträge kommen im Katalog nicht vor; das sind - je nachdem - Vertrags-, Bank- oder Steuerthemen, keine MaBV-Aufzeichnungspflichten.",
  "§ 10(3) MaBV is the broker-specific paragraph: it applies expressly only to traders within the meaning of § 34c(1) sentence 1 no. 1 GewO and requires, in so far as relevant in the individual case, for brokering acquisition contracts over land or rights equivalent to land (no. 1): \"location, size and permitted use of the plot, type, age and condition of the building, fittings, living and usable floor area, number of rooms, the amount of the purchase price claimed including encumbrances to be assumed, and the seller's surname, first name and address\". The catalogues for use contracts over land (no. 2) and over commercial or residential premises (no. 3) are similarly built, but the purchase price claim is replaced by the amount of rent claimed and, where applicable, any construction-cost contribution, deposit, advance rent, tenant loan or key-money sum. Creditworthiness, mortgage lending value and tax amounts do not appear in the catalogue at all; those are contract, banking or tax matters, not MaBV record-keeping duties."),

q("mabv_pflichten", 4, "§ 11 Satz 1 Nr. 1 MaBV", 5, True, ["all"], "b",
  "In welcher Form und zu welchem Zeitpunkt muss ein Makler seine Informationspflichten nach § 11 Satz 1 Nummer 1 MaBV erfüllen?",
  {
    "a": "Mündlich, spätestens bei Vertragsschluss",
    "b": "In Textform und in deutscher Sprache; Entgelt und Vertragsdauer unmittelbar nach Annahme des Auftrags, die übrigen Angaben spätestens bei Aufnahme der Vertragsverhandlungen",
    "c": "In notariell beurkundeter Form vor Beginn der Tätigkeit",
    "d": "In Textform, aber erst auf ausdrückliche Anfrage des Auftraggebers",
  },
  "In what form and at what time must a broker discharge the information duties under § 11 sentence 1 no. 1 MaBV?",
  {
    "a": "Orally, at the latest on conclusion of the contract",
    "b": "In text form and in German; fee and contract duration immediately after acceptance of the mandate, the remaining particulars at the latest when contract negotiations begin",
    "c": "In notarially recorded form before starting work",
    "d": "In text form, but only on the client's express request",
  },
  "§ 11 Satz 1 MaBV verlangt einheitlich „in Textform und in deutscher Sprache“ und teilt die maklerspezifische Nummer 1 in zwei Zeitstufen: Buchstabe a - unmittelbar nach der Annahme des Auftrags die Angaben nach § 10 Absatz 2 Nummer 2 Buchstabe a und f, also das vom Auftraggeber zu entrichtende Entgelt (Wohnungsvermittler in einem Bruchteil oder Vielfachen der Monatsmiete) und die Vertragsdauer; Buchstabe b - spätestens bei Aufnahme der Vertragsverhandlungen über den vermittelten oder nachgewiesenen Vertragsgegenstand die Angaben nach § 10 Absatz 2 Nummer 2 Buchstabe b bis e und Absatz 3 Nummer 1 bis 3, also die objektbezogenen Angaben. Textform bedeutet § 126b BGB: lesbare Erklärung auf einem dauerhaften Datenträger, Nennung des Erklärenden - E-Mail oder PDF genügen, eine Unterschrift ist nicht erforderlich. Nach § 11 Satz 3 MaBV kann ein Auftraggeber, der natürliche Person ist, die Übermittlung in der Amtssprache seines EU-/EWR-Wohnsitzstaates verlangen. Achtung Abgrenzung: § 11 Satz 1 Nummer 3 MaBV - Auskunft über Qualifikation und Weiterbildung auf Anfrage - ist die Verwalter-Variante und gilt für Makler nicht. Ein Verstoß gegen § 11 Satz 1 Nummer 1 ist nach § 18 Abs. 1 Nr. 7 MaBV bußgeldbewehrt.",
  "§ 11 sentence 1 MaBV uniformly requires \"in text form and in the German language\" and splits the broker-specific no. 1 into two time stages: (a) immediately after acceptance of the mandate, the particulars under § 10(2) no. 2(a) and (f), i.e. the fee payable by the client (flat-letting agents must state it as a fraction or multiple of the monthly rent) and the duration of the contract; (b) at the latest when contract negotiations over the brokered or introduced subject matter begin, the particulars under § 10(2) no. 2(b) to (e) and (3) nos. 1 to 3, i.e. the property-related particulars. Text form means § 126b BGB: a legible declaration on a durable medium naming the declarant - e-mail or PDF suffices, no signature is needed. Under § 11 sentence 3 MaBV a client who is a natural person may demand transmission in the official language of their EU/EEA state of residence. Note the boundary: § 11 sentence 1 no. 3 MaBV - information about qualifications and continuing education on request - is the manager variant and does not apply to brokers. A breach of § 11 sentence 1 no. 1 is subject to a fine under § 18(1) no. 7 MaBV."),

q("mabv_pflichten", 5, "§ 14 Abs. 1 MaBV", 4, False, ["all"], "c",
  "Wie lange und wo sind die Geschäftsunterlagen nach § 14 Absatz 1 MaBV aufzubewahren, und wann beginnt die Frist?",
  {
    "a": "Zehn Jahre, beginnend mit dem Tag der Auftragsannahme",
    "b": "Drei Jahre in digitaler Form, beginnend mit dem Vertragsschluss",
    "c": "Fünf Jahre in den Geschäftsräumen, beginnend mit dem Schluss des Kalenderjahres, in dem der letzte aufzeichnungspflichtige Vorgang für den jeweiligen Auftrag angefallen ist",
    "d": "Sechs Jahre, beginnend mit der Rechnungslegung nach § 8 MaBV",
  },
  "How long and where must business records be kept under § 14(1) MaBV, and when does the period start?",
  {
    "a": "Ten years, starting on the day the mandate was accepted",
    "b": "Three years in digital form, starting on conclusion of the contract",
    "c": "Five years on the business premises, starting at the end of the calendar year in which the last event requiring a record for that mandate occurred",
    "d": "Six years, starting with the rendering of account under § 8 MaBV",
  },
  "§ 14 Abs. 1 MaBV: „Die in § 10 bezeichneten Geschäftsunterlagen sind 5 Jahre in den Geschäftsräumen aufzubewahren. Die Aufbewahrungsfrist beginnt mit dem Schluss des Kalenderjahres, in dem der letzte aufzeichnungspflichtige Vorgang für den jeweiligen Auftrag angefallen ist. Vorschriften, die eine längere Frist bestimmen, bleiben unberührt.“ Der letzte Satz ist praktisch entscheidend: die handels- und steuerrechtlichen Aufbewahrungsfristen (§ 257 HGB, § 147 AO) laufen daneben und sind teilweise länger; die MaBV setzt einen Mindeststandard, keine Obergrenze. § 14 Abs. 2 MaBV erlaubt die Aufbewahrung als verkleinerte Wiedergabe, wenn die Übereinstimmung mit der Urschrift gesichert ist; auf Verlangen der Behörde sind auf eigene Kosten lesbare Reproduktionen vorzulegen und bei Prüfungen in den Geschäftsräumen Lesegeräte bereitzuhalten. Nicht zu verwechseln mit der Drei-Jahres-Frist: die gilt nach § 15b Abs. 2 Satz 3 MaBV für Weiterbildungsnachweise und betrifft ausschließlich Wohnimmobilienverwalter. Ein Verstoß gegen § 14 Abs. 1 Satz 1 ist nach § 18 Abs. 1 Nr. 8 MaBV eine Ordnungswidrigkeit.",
  "§ 14(1) MaBV: \"The business records referred to in § 10 must be kept for 5 years on the business premises. The retention period begins at the end of the calendar year in which the last event requiring a record for the mandate in question occurred. Provisions setting a longer period remain unaffected.\" The last sentence is decisive in practice: the commercial and tax retention periods (§ 257 HGB, § 147 AO) run alongside and are partly longer; the MaBV sets a floor, not a ceiling. § 14(2) MaBV permits retention as a reduced-size reproduction where conformity with the original is assured; on the authority's request legible reproductions must be produced at the trader's own cost, and reading devices kept available for on-site inspections. Do not confuse this with the three-year period: that applies under § 15b(2) sentence 3 MaBV to continuing-education records and concerns residential property managers only. A breach of § 14(1) sentence 1 is an administrative offence under § 18(1) no. 8 MaBV."),

q("mabv_pflichten", 6, "§ 8 MaBV; § 259 BGB", 3, False, ["all"], "b",
  "Wann muss ein Makler nach § 8 MaBV Rechnung legen, und wann entfällt diese Pflicht?",
  {
    "a": "Immer nach Beendigung des Auftrages; ein Verzicht ist unwirksam",
    "b": "Nur wenn er zur Ausführung des Auftrages Vermögenswerte des Auftraggebers erhalten oder verwendet hat; sie entfällt bei schriftlichem Verzicht nach Auftragsende oder bei einer Festpreisleistung",
    "c": "Nur auf Verlangen der zuständigen Behörde",
    "d": "Jährlich zum 31. Dezember, unabhängig vom Auftragsstand",
  },
  "When must a broker render account under § 8 MaBV, and when does that duty fall away?",
  {
    "a": "Always after the mandate ends; a waiver is ineffective",
    "b": "Only where he has received or used the client's assets to carry out the mandate; it falls away on a written waiver after the mandate ends, or where a fixed-price service is to be provided from those assets",
    "c": "Only on request by the competent authority",
    "d": "Annually on 31 December, regardless of the state of the mandate",
  },
  "§ 8 Abs. 1 MaBV knüpft die Rechnungslegungspflicht an eine Bedingung: „Hat der Gewerbetreibende zur Ausführung des Auftrages Vermögenswerte des Auftraggebers erhalten oder verwendet, so hat er dem Auftraggeber nach Beendigung des Auftrages über die Verwendung dieser Vermögenswerte Rechnung zu legen. § 259 des Bürgerlichen Gesetzbuchs ist anzuwenden.“ § 259 BGB gibt den Inhalt vor: geordnete Zusammenstellung der Einnahmen und Ausgaben, Vorlage von Belegen, soweit sie erteilt zu werden pflegen. § 8 Abs. 2 MaBV lässt die Pflicht in zwei Fällen entfallen: schriftlicher Verzicht des Auftraggebers NACH Beendigung des Auftrages, oder wenn der Gewerbetreibende mit den Vermögenswerten eine Leistung zu einem Festpreis zu erbringen hat. Der Zeitpunkt des Verzichts ist entscheidend - ein vorab in AGB erklärter Verzicht erfüllt § 8 Abs. 2 MaBV nicht. Für die meisten Makler läuft § 8 MaBV ohnehin leer, weil sie keine Vermögenswerte des Auftraggebers entgegennehmen.",
  "§ 8(1) MaBV makes the duty to render account conditional: \"Where the trader has received or used the client's assets in order to carry out the mandate, he must render account to the client after the mandate ends on the use of those assets. § 259 BGB applies.\" § 259 BGB prescribes the content: an orderly statement of receipts and expenditure, with vouchers produced in so far as vouchers are customarily issued. § 8(2) MaBV removes the duty in two cases: a written waiver by the client AFTER the mandate has ended, or where the trader is to provide a service at a fixed price out of those assets. The timing of the waiver is decisive - a waiver declared in advance in standard terms does not satisfy § 8(2) MaBV. For most brokers § 8 MaBV is inoperative anyway, because they never receive client assets."),

q("mabv_pflichten", 7, "§ 2 Abs. 1 MaBV; § 7 Abs. 1 und 2 MaBV", 4, False, ["management"], "c",
  "Ein Makler soll für einen Auftraggeber eine Mietkaution treuhänderisch entgegennehmen. Was verlangt die MaBV?",
  {
    "a": "Nichts - die Sicherungsvorschriften der MaBV gelten nur für Bauträger",
    "b": "Eine Anzeige an die zuständige Behörde vor Entgegennahme",
    "c": "Vor Entgegennahme oder Ermächtigung zur Verwendung ist in Höhe dieser Vermögenswerte Sicherheit zu leisten oder eine geeignete Versicherung abzuschließen; § 7 MaBV lässt stattdessen eine Blankosicherheit oder - bei bestimmten Auftraggebern - einen Verzicht zu",
    "d": "Eine notarielle Verwahrung ist zwingend",
  },
  "A broker is to hold a rent deposit on trust for a client. What does the MaBV require?",
  {
    "a": "Nothing - the MaBV's security provisions apply only to property developers",
    "b": "Notification to the competent authority before receipt",
    "c": "Before receiving the assets or being authorised to use them, security must be provided or suitable insurance taken out in the amount of those assets; § 7 MaBV instead allows blanket security or - for certain clients - a waiver",
    "d": "Notarial escrow is mandatory",
  },
  "§ 2 Abs. 1 Satz 1 MaBV: „Bevor der Gewerbetreibende zur Ausführung des Auftrages Vermögenswerte des Auftraggebers erhält oder zu deren Verwendung ermächtigt wird, hat er dem Auftraggeber in Höhe dieser Vermögenswerte Sicherheit zu leisten oder eine zu diesem Zweck geeignete Versicherung abzuschließen.“ Gesichert werden nach Satz 2 Schadensersatzansprüche wegen vorsätzlich begangener unerlaubter Handlungen gegen diese Vermögenswerte. Die Sicherheit kann nach § 2 Abs. 2 MaBV nur durch Bürgschaft geleistet werden, und zwar nur durch Körperschaften des öffentlichen Rechts mit Sitz im Geltungsbereich der Verordnung, im Inland befugte Kreditinstitute oder zur Bürgschaftsversicherung befugte Versicherer, mit Verzicht auf die Einrede der Vorausklage. § 7 Abs. 1 MaBV stellt „die übrigen Gewerbetreibenden im Sinne des § 34c Abs. 1 der Gewerbeordnung“ - also insbesondere Makler - von § 2, § 3 Abs. 3 und §§ 4 bis 6 frei, sofern sie Sicherheit für alle etwaigen Rückgewähr- oder Auszahlungsansprüche geleistet haben. § 7 Abs. 2 MaBV erlaubt zusätzlich einen Verzicht in gesonderter Urkunde, wenn der Auftraggeber eine juristische Person des öffentlichen Rechts, ein öffentlich-rechtliches Sondervermögen oder ein im Handels- oder Genossenschaftsregister eingetragener Kaufmann ist; die Kaufmannseigenschaft ist durch Registerauszug nachzuweisen. Praktisch bedeutet das: die meisten Makler berühren §§ 2 bis 7 MaBV nie, weil sie keine Auftraggebergelder anfassen - wer es doch tut, muss sie genau lesen.",
  "§ 2(1) sentence 1 MaBV: \"Before the trader receives the client's assets in order to carry out the mandate, or is authorised to use them, he must provide security to the client in the amount of those assets or take out insurance suitable for that purpose.\" Sentence 2 specifies what is secured: damages claims for intentional torts directed against those assets. Under § 2(2) MaBV the security may only be given by way of guarantee, and only by public-law corporations seated within the Regulation's territory, credit institutions authorised to operate domestically, or insurers authorised to write guarantee insurance, with a waiver of the defence of failure to pursue the principal debtor. § 7(1) MaBV exempts \"the remaining traders within the meaning of § 34c(1) of the Trade Regulation Act\" - i.e. brokers in particular - from § 2, § 3(3) and §§ 4 to 6, provided they have given security for all possible claims to restitution or payment out. § 7(2) MaBV additionally permits a waiver in a separate document where the client is a public-law legal person, a public-law special fund, or a merchant registered in the commercial or cooperative register; merchant status must be evidenced by a register extract. In practice: most brokers never touch §§ 2 to 7 MaBV because they never handle client money - those who do must read them closely."),

q("mabv_pflichten", 8, "§ 16 Abs. 1 und 2 MaBV", 5, True, ["management"], "c",
  "Welche Prüfungspflicht nach § 16 MaBV trifft einen Immobilienmakler?",
  {
    "a": "Eine jährliche Prüfung mit Übermittlung des Prüfungsberichts bis zum 31. Dezember des Folgejahres",
    "b": "Eine Prüfung alle drei Jahre durch einen Wirtschaftsprüfer",
    "c": "Keine regelmäßige Prüfung - die Behörde kann ihn aber aus besonderem Anlass auf seine Kosten außerordentlich prüfen lassen",
    "d": "Gar keine - § 16 MaBV gilt nur für Wohnimmobilienverwalter",
  },
  "Which audit duty under § 16 MaBV applies to a real-estate broker?",
  {
    "a": "An annual audit with the audit report submitted by 31 December of the following year",
    "b": "An audit every three years by a statutory auditor",
    "c": "No routine audit - but the authority may have him audited ad hoc at his own cost where there is special cause",
    "d": "None at all - § 16 MaBV applies only to residential property managers",
  },
  "Die Trennung in § 16 MaBV ist scharf und wird in der Praxis oft verwechselt. § 16 Abs. 1 MaBV richtet sich ausdrücklich an „Gewerbetreibende im Sinne des § 34c Absatz 1 Satz 1 Nummer 3 der Gewerbeordnung“ - also Bauträger und Baubetreuer: sie müssen die Einhaltung der §§ 2 bis 14 MaBV für jedes Kalenderjahr auf eigene Kosten prüfen lassen und den Prüfungsbericht bis spätestens 31. Dezember des Folgejahres übermitteln (bzw. eine Negativerklärung, wenn keine erlaubnispflichtige Tätigkeit ausgeübt wurde). § 16 Abs. 2 MaBV richtet sich dagegen an alle „Gewerbetreibende im Sinne des § 34c Abs. 1 der Gewerbeordnung“: die zuständige Behörde ist befugt, sie auf deren Kosten „aus besonderem Anlaß im Rahmen einer außerordentlichen Prüfung durch einen geeigneten Prüfer überprüfen zu lassen“, wobei die Behörde den Prüfer bestimmt. Der Makler hat also keine turnusmäßige, wohl aber eine anlassbezogene Prüfungslast. Geeignete Prüfer sind nach § 16 Abs. 3 MaBV grundsätzlich Wirtschaftsprüfer, vereidigte Buchprüfer und entsprechende Gesellschaften sowie qualifizierte Prüfungsverbände; für Makler nach § 34c Absatz 1 Nummer 1 GewO können mit der Prüfung nach Absatz 2 auch andere öffentlich bestellte oder zugelassene, hinreichend vorgebildete Personen betraut werden. Befangene Personen sind ungeeignet. Antwort d ist falsch: § 16 MaBV steht nicht in der Liste des § 1 Abs. 2 Satz 2 MaBV und gilt für Verwalter gerade NICHT.",
  "The division in § 16 MaBV is sharp and often confused in practice. § 16(1) MaBV addresses expressly \"traders within the meaning of § 34c(1) sentence 1 no. 3 of the Trade Regulation Act\" - i.e. property developers and construction supervisors: they must have compliance with §§ 2 to 14 MaBV audited at their own cost for each calendar year and submit the audit report by 31 December of the following year (or a negative declaration if no activity requiring a permission was carried on). § 16(2) MaBV, by contrast, addresses all \"traders within the meaning of § 34c(1) of the Trade Regulation Act\": the competent authority is empowered to have them audited at their own cost \"where there is special cause, by way of an extraordinary audit by a suitable auditor\", the authority choosing the auditor. So the broker has no periodic audit burden but does have an event-driven one. Suitable auditors under § 16(3) MaBV are in principle statutory auditors, sworn accountants and corresponding firms, plus qualified audit associations; for brokers under § 34c(1) no. 1 GewO the (2) audit may also be entrusted to other publicly appointed or licensed persons with adequate training and experience. Persons open to concerns of bias are unsuitable. Answer d is wrong: § 16 MaBV is not in the list in § 1(2) sentence 2 MaBV and therefore does NOT apply to managers."),


# ===========================================================================
# Topic 3: sanktionen
# ===========================================================================

q("sanktionen", 1, "§ 18 Abs. 1 MaBV; § 144 Abs. 2 Nr. 6 und Abs. 4 GewO", 4, True, ["management"], "b",
  "Ein Makler hat über zwei Jahre keine Aufzeichnungen nach § 10 MaBV geführt. Welche Sanktion droht?",
  {
    "a": "Nur ein Hinweis der Behörde; Aufzeichnungsverstöße sind nicht bußgeldbewehrt",
    "b": "Eine Ordnungswidrigkeit nach § 18 Absatz 1 Nummer 6 MaBV im Sinne des § 144 Absatz 2 Nummer 6 GewO, mit einer Geldbuße bis zu fünftausend Euro",
    "c": "Eine Freiheitsstrafe bis zu einem Jahr",
    "d": "Eine Geldbuße bis zu fünfzigtausend Euro",
  },
  "A broker has kept no records under § 10 MaBV for two years. What sanction is in prospect?",
  {
    "a": "Only a warning from the authority; record-keeping breaches carry no fine",
    "b": "An administrative offence under § 18(1) no. 6 MaBV within the meaning of § 144(2) no. 6 GewO, with a fine of up to five thousand euros",
    "c": "A custodial sentence of up to one year",
    "d": "A fine of up to fifty thousand euros",
  },
  "§ 18 Abs. 1 MaBV listet elf Tatbestände und ordnet sie ausdrücklich als Ordnungswidrigkeit „im Sinne des § 144 Abs. 2 Nr. 6 der Gewerbeordnung“ ein. Nummer 6 erfasst, wer „entgegen § 10 Abs. 1 bis 5 erforderliche Aufzeichnungen nicht, nicht richtig, nicht vollständig, nicht ordnungsgemäß oder nicht rechtzeitig macht oder Unterlagen oder Belege nicht oder nicht übersichtlich sammelt“. Den Bußgeldrahmen liefert § 144 Abs. 4 GewO: für die Fälle des Absatzes 2 Nummer 5 bis 11 - dort steht Nummer 6 - eine Geldbuße bis zu fünftausend Euro. Die fünfzigtausend Euro des § 144 Abs. 4 GewO gelten nur für Absatz 1 Nummer 1 Buchstabe m und n sowie Nummer 2 (Anlageberatung/-vermittlung, Bewachung auf Seeschiffen) und sind hier nicht einschlägig. § 18 Abs. 2 und 3 MaBV verweisen für dieselben Handlungen im Reisegewerbe auf § 145 Abs. 2 Nr. 9 GewO und im Messe-, Ausstellungs- oder Marktgewerbe auf § 146 Abs. 2 Nr. 11a GewO. Eine Kriminalstrafe sieht die MaBV nicht vor. Neben dem Bußgeld steht die gewerberechtliche Ebene: Auflagen nach § 34c Abs. 1 Satz 2 GewO und im Extremfall der Widerruf der Erlaubnis.",
  "§ 18(1) MaBV lists eleven offences and classifies them expressly as administrative offences \"within the meaning of § 144(2) no. 6 of the Trade Regulation Act\". No. 6 catches anyone who \"contrary to § 10(1) to (5) fails to make required records, or makes them incorrectly, incompletely, improperly or late, or fails to collect documents or vouchers, or fails to collect them in an orderly manner\". The fine range comes from § 144(4) GewO: for cases under (2) nos. 5 to 11 - which is where no. 6 sits - a fine of up to five thousand euros. The fifty thousand euros in § 144(4) GewO applies only to (1) no. 1(m) and (n) and no. 2 (investment advice/brokerage, guarding on seagoing vessels) and is not relevant here. § 18(2) and (3) MaBV route the same acts committed in itinerant trade to § 145(2) no. 9 GewO and in fair, exhibition or market trade to § 146(2) no. 11a GewO. The MaBV provides for no criminal penalty. Alongside the fine sits the trade-law level: conditions under § 34c(1) sentence 2 GewO and, in an extreme case, revocation of the permission."),

q("sanktionen", 2, "§ 144 Abs. 1 Nr. 1 Buchst. h und Abs. 4 GewO", 4, True, ["management"], "b",
  "Jemand vermittelt gewerbsmäßig Wohnungskaufverträge, ohne die Erlaubnis nach § 34c GewO beantragt zu haben. Wie ist das sanktioniert?",
  {
    "a": "Als Straftat nach § 148 GewO mit Freiheitsstrafe",
    "b": "Als Ordnungswidrigkeit nach § 144 Absatz 1 Nummer 1 Buchstabe h GewO mit einer Geldbuße bis zu fünftausend Euro",
    "c": "Gar nicht - erlaubnisfreie Vermittlung ist nur zivilrechtlich riskant",
    "d": "Als Ordnungswidrigkeit mit einer Geldbuße bis zu fünfzigtausend Euro",
  },
  "Someone commercially brokers flat purchase contracts without having applied for the § 34c GewO permission. How is that sanctioned?",
  {
    "a": "As a criminal offence under § 148 GewO with a custodial sentence",
    "b": "As an administrative offence under § 144(1) no. 1(h) GewO with a fine of up to five thousand euros",
    "c": "Not at all - unlicensed brokerage carries only civil-law risk",
    "d": "As an administrative offence with a fine of up to fifty thousand euros",
  },
  "§ 144 Abs. 1 Nr. 1 GewO stellt die Ausübung erlaubnisbedürftiger Gewerbe ohne Erlaubnis unter Bußgeld und listet die Erlaubnistatbestände buchstabenweise auf. Buchstabe h erfasst, wer „nach § 34c Absatz 1 Satz 1 Nummer 1 oder Nummer 2 den Abschluß von Verträgen der dort bezeichneten Art vermittelt oder die Gelegenheit hierzu nachweist“ - also die unerlaubte Makler- und Darlehensvermittlertätigkeit. Buchstabe i betrifft Bauvorhaben nach Nummer 3, Buchstabe j die Wohnimmobilienverwaltung nach Nummer 4. Erfasst sind Vorsatz und Fahrlässigkeit. Der Rahmen folgt aus § 144 Abs. 4 GewO: für Absatz 1 Nummer 1 Buchstabe a bis l und o bis zu fünftausend Euro. Zusätzlich kommt die gewerberechtliche Untersagung in Betracht, und zivilrechtlich ist die Provisionsforderung eines Maklers ohne Erlaubnis angreifbar - das ist aber eine Frage des Einzelfalls und nicht Gegenstand des § 144 GewO. Antwort a ist falsch: § 34c GewO ist nicht strafbewehrt; § 148 GewO betrifft andere Tatbestände.",
  "§ 144(1) no. 1 GewO subjects carrying on a permission-requiring trade without a permission to a fine and lists the permission limbs letter by letter. Letter (h) catches anyone who \"under § 34c(1) sentence 1 no. 1 or no. 2 brokers the conclusion of contracts of the kind described there or provides the opportunity to do so\" - i.e. unlicensed broker and loan-brokerage activity. Letter (i) concerns construction projects under no. 3, letter (j) residential property management under no. 4. Both intent and negligence are covered. The range follows from § 144(4) GewO: for (1) no. 1 letters (a) to (l) and (o), up to five thousand euros. A trade prohibition may also be considered, and in civil law an unlicensed broker's commission claim is open to challenge - but that turns on the individual case and is not a matter for § 144 GewO. Answer a is wrong: § 34c GewO carries no criminal penalty; § 148 GewO concerns different offences."),

q("sanktionen", 3, "§ 18 Abs. 1 Nr. 9 MaBV; § 15b Abs. 2 Satz 3 MaBV", 4, False, ["management"], "d",
  "Kann ein Immobilienmakler seit dem 24.07.2026 noch die Ordnungswidrigkeit nach § 18 Absatz 1 Nummer 9 MaBV (fehlender Weiterbildungsnachweis) begehen?",
  {
    "a": "Ja, unverändert",
    "b": "Ja, aber nur bei vorsätzlichem Handeln",
    "c": "Ja, mit halbiertem Bußgeldrahmen",
    "d": "Nein - der Tatbestand knüpft an § 15b Absatz 2 Satz 3 MaBV an, und die Weiterbildungspflicht trifft nach § 34c Absatz 2a GewO nur noch Wohnimmobilienverwalter",
  },
  "Since 24 July 2026, can a real-estate broker still commit the administrative offence under § 18(1) no. 9 MaBV (missing continuing-education record)?",
  {
    "a": "Yes, unchanged",
    "b": "Yes, but only where acting intentionally",
    "c": "Yes, with the fine range halved",
    "d": "No - the offence hooks onto § 15b(2) sentence 3 MaBV, and under § 34c(2a) GewO the continuing-education duty now applies only to residential property managers",
  },
  "§ 18 Abs. 1 Nr. 9 MaBV erfasst, wer „entgegen § 15b Absatz 2 Satz 3 einen Nachweis oder eine Unterlage nicht oder nicht mindestens drei Jahre aufbewahrt“. Die Nachweispflicht des § 15b Abs. 2 MaBV trifft aber nur „die zur Weiterbildung verpflichteten Gewerbetreibenden“, und wer das ist, bestimmt § 15b Abs. 1 Satz 1 MaBV durch Rückverweis: „Wer nach § 34c Absatz 2a der Gewerbeordnung zur Weiterbildung verpflichtet ist“. Da § 34c Abs. 2a GewO seit dem 24.07.2026 nur noch Gewerbetreibende nach Absatz 1 Satz 1 Nummer 4 nennt, kann ein reiner Makler den Tatbestand nicht mehr erfüllen - die Kette bricht schon an der ersten Verweisung. Genau deshalb war die Streichung des Teils A der Anlage 1 MaBV (Art. 2 Nr. 4 GewBürAbG) nur Folgearbeit: die eigentliche Abschaffung geschah über § 34c Abs. 2a GewO. Wer sowohl Makler als auch Wohnimmobilienverwalter ist, bleibt für den Verwalterteil selbstverständlich in der Pflicht - dann sind Nachweise nach § 15b Abs. 2 MaBV weiterhin drei Jahre auf einem dauerhaften Datenträger oder in digitaler Form vorzuhalten, gerechnet ab dem Ende des Kalenderjahres der Maßnahme.",
  "§ 18(1) no. 9 MaBV catches anyone who \"contrary to § 15b(2) sentence 3 fails to keep a record or document, or fails to keep it for at least three years\". But the record-keeping duty in § 15b(2) MaBV binds only \"traders subject to the continuing-education duty\", and who that is is determined by § 15b(1) sentence 1 MaBV via a back-reference: \"Whoever is obliged to undertake continuing education under § 34c(2a) of the Trade Regulation Act\". Since § 34c(2a) GewO has, from 24 July 2026, named only traders under (1) sentence 1 no. 4, a pure broker can no longer satisfy the offence - the chain breaks at the very first reference. That is precisely why deleting Part A of Annex 1 MaBV (Art. 2 no. 4 GewBürAbG) was merely consequential tidying: the actual abolition happened through § 34c(2a) GewO. Anyone who is both broker and residential property manager of course remains bound for the manager side - records must then still be kept under § 15b(2) MaBV for three years on a durable medium or in digital form, counted from the end of the calendar year of the training."),


# ===========================================================================
# Topic 4: gwg_makler - deliberately only 3 questions, broker-specific only
# ===========================================================================

q("gwg_makler", 1, "§ 2 Abs. 1 Nr. 14 GwG; § 1 Abs. 11 GwG", 4, True, ["all"], "c",
  "Wer ist „Immobilienmakler“ im Sinne des Geldwäschegesetzes?",
  {
    "a": "Nur wer eine Erlaubnis nach § 34c Absatz 1 Satz 1 Nummer 1 GewO besitzt",
    "b": "Nur wer Kaufverträge über Grundstücke vermittelt",
    "c": "Wer gewerblich den Abschluss von Kauf-, Pacht- oder Mietverträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume vermittelt",
    "d": "Jeder Gewerbetreibende nach § 34c Absatz 1 GewO, also auch Bauträger und Wohnimmobilienverwalter",
  },
  "Who is a \"real-estate agent\" (Immobilienmakler) within the meaning of the Money Laundering Act?",
  {
    "a": "Only someone holding a permission under § 34c(1) sentence 1 no. 1 GewO",
    "b": "Only someone brokering purchase contracts over land",
    "c": "Anyone who commercially brokers the conclusion of purchase, lease or tenancy contracts over land, rights equivalent to land, commercial premises or residential premises",
    "d": "Every trader under § 34c(1) GewO, i.e. including developers and residential property managers",
  },
  "§ 2 Abs. 1 Nr. 14 GwG nennt als Verpflichtete schlicht „Immobilienmakler,“ und § 1 Abs. 11 GwG definiert den Begriff eigenständig: „Immobilienmakler im Sinne dieses Gesetzes ist, wer gewerblich den Abschluss von Kauf-, Pacht- oder Mietverträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume vermittelt.“ Zwei Beobachtungen sind praktisch wichtig. Erstens ist die GwG-Definition weiter als der erste Reflex: sie erfasst neben Kaufverträgen ausdrücklich auch Pacht- und Mietverträge. Zweitens knüpft sie an die TÄTIGKEIT an, nicht an den Besitz einer Erlaubnis - Antwort a greift zu kurz. Antwort d überdehnt: Bauträger und Wohnimmobilienverwalter sind über § 1 Abs. 11 GwG nicht erfasst, sie können allenfalls über andere Nummern des § 2 Abs. 1 GwG hineinfallen. Wer Verpflichteter ist, schuldet unter anderem ein Risikomanagement nach § 4 GwG und interne Sicherungsmaßnahmen nach § 6 GwG - darunter nach § 6 Abs. 2 Nr. 6 GwG „die erstmalige und laufende Unterrichtung der Mitarbeiter“ über Typologien und Methoden der Geldwäsche und Terrorismusfinanzierung. Das ist eine Unterrichtungspflicht, keine Prüfungspflicht: sie verlangt, Personal zu schulen, nicht einen Test zu bestehen." + KYC_POINTER_DE,
  "§ 2(1) no. 14 GwG names as an obliged entity simply \"Immobilienmakler,\" and § 1(11) GwG defines the term autonomously: \"A real-estate agent within the meaning of this Act is anyone who commercially brokers the conclusion of purchase, lease or tenancy contracts over land, rights equivalent to land, commercial premises or residential premises.\" Two observations matter in practice. First, the GwG definition is wider than the first reflex suggests: alongside purchase contracts it expressly covers lease and tenancy contracts. Second, it hooks onto the ACTIVITY, not on holding a permission - answer a is too narrow. Answer d overreaches: developers and residential property managers are not caught by § 1(11) GwG; at most they may fall under other numbers of § 2(1) GwG. An obliged entity owes, among other things, risk management under § 4 GwG and internal safeguards under § 6 GwG - including, under § 6(2) no. 6 GwG, \"the initial and ongoing instruction of staff\" on typologies and current methods of money laundering and terrorist financing. That is a duty to instruct, not a duty to pass anything: it requires training staff, not passing a test." + KYC_POINTER_EN),

q("gwg_makler", 2, "§ 10 Abs. 6 GwG", 5, True, ["all"], "d",
  "Bei welchen Vermittlungsgeschäften muss ein Immobilienmakler nach § 10 Absatz 6 GwG die allgemeinen Sorgfaltspflichten erfüllen?",
  {
    "a": "Bei allen Vermittlungen ab einem Transaktionswert von 10 000 Euro",
    "b": "Nur bei der Vermittlung von Kaufverträgen, unabhängig vom Wert",
    "c": "Bei allen Kauf-, Miet- und Pachtvermittlungen ohne Schwelle",
    "d": "Bei der Vermittlung von Kaufverträgen immer, bei der Vermittlung von Miet- oder Pachtverträgen nur bei einer monatlichen Nettokaltmiete oder Nettokaltpacht von mindestens 10 000 Euro",
  },
  "In which brokerage transactions must a real-estate agent perform the general customer due diligence duties under § 10(6) GwG?",
  {
    "a": "In all brokerage from a transaction value of EUR 10,000 upwards",
    "b": "Only when brokering purchase contracts, regardless of value",
    "c": "In all purchase, tenancy and lease brokerage, with no threshold",
    "d": "Always when brokering purchase contracts; when brokering tenancy or lease contracts only where the monthly net cold rent or net cold lease payment is at least EUR 10,000",
  },
  "§ 10 Abs. 6 GwG ist die betrieblich wichtigste Geldwäschevorschrift für einen Makler, weil sie pro Mandat darüber entscheidet, ob überhaupt Sorgfaltspflichten anfallen: „Verpflichtete nach § 2 Absatz 1 Nummer 14 haben die allgemeinen Sorgfaltspflichten zu erfüllen: 1. bei der Vermittlung von Kaufverträgen und 2. bei der Vermittlung von Miet- oder Pachtverträgen bei Transaktionen mit einer monatlichen Nettokaltmiete oder Nettokaltpacht in Höhe von mindestens 10 000 Euro.“ Die Schwelle ist also zweifach spezifiziert - sie bezieht sich auf die MONATLICHE Miete oder Pacht und auf die NETTOKALT-Größe, nicht auf den Gesamtwert des Vertrages, nicht auf die Warmmiete und nicht auf die Provision. Bei Kaufverträgen gibt es keine Schwelle: die Sorgfaltspflichten greifen immer. Zu beachten ist auch die zeitliche Einordnung: die Identifizierung ist bei Immobilienmaklern nach der Systematik des GwG spätestens dann durchzuführen, wenn ein ernsthaftes Interesse der Vertragsparteien am Geschäftsabschluss feststeht - Praxisfragen dazu gehören in eine geldwäscherechtliche Verfahrensanweisung, nicht in dieses Modul. Ebenfalls im Perimeter: § 16a GwG, das Verbot, die Gegenleistung beim Erwerb inländischer Immobilien in Bargeld, Kryptowerten, Gold, Platin oder Edelsteinen zu erbringen; die Nachweis- und Prüfmechanik der Absätze 2 bis 4 richtet sich an den Notar, und Absatz 5 enthält eine 10 000-Euro-Bagatellgrenze." + KYC_POINTER_DE,
  "§ 10(6) GwG is the operationally most important anti-money-laundering provision for a broker, because it decides mandate by mandate whether any due diligence is owed at all: \"Obliged entities under § 2(1) no. 14 must perform the general due diligence duties: 1. when brokering purchase contracts, and 2. when brokering tenancy or lease contracts, in transactions with a monthly net cold rent or net cold lease payment of at least EUR 10,000.\" The threshold is therefore doubly specified - it refers to the MONTHLY rent or lease payment and to the NET COLD figure, not to the total value of the contract, not to the rent inclusive of heating, and not to the commission. For purchase contracts there is no threshold: due diligence always applies. Timing also matters: for real-estate agents, identification must under the GwG's scheme be carried out at the latest once the parties' serious interest in concluding the transaction is established - practical questions about that belong in an AML procedures manual, not in this module. Also in the perimeter: § 16a GwG, the prohibition on rendering the consideration for the acquisition of domestic real estate in cash, crypto assets, gold, platinum or precious stones; the proof and verification mechanics of (2) to (4) are addressed to the notary, and (5) contains a EUR 10,000 de-minimis." + KYC_POINTER_EN),

q("gwg_makler", 3, "§ 1 GwGMeldV-Immobilien; § 43 Abs. 1 GwG", 4, True, ["all"], "b",
  "Gilt die Geldwäschegesetzmeldepflichtverordnung-Immobilien (GwGMeldV-Immobilien) für Immobilienmakler?",
  {
    "a": "Ja - der Name der Verordnung bezeichnet gerade den Immobilienmakler als Adressaten",
    "b": "Nein - § 1 GwGMeldV-Immobilien beschränkt sie auf Verpflichtete nach § 2 Absatz 1 Nummer 10 und 12 GwG",
    "c": "Ja, aber nur bei Kaufverträgen über 150 000 Euro",
    "d": "Nur für Makler, die zugleich Wohnimmobilienverwalter sind",
  },
  "Does the Money Laundering Reporting Obligation Regulation for Real Estate (GwGMeldV-Immobilien) apply to real-estate agents?",
  {
    "a": "Yes - the Regulation's name identifies the real-estate agent as its addressee",
    "b": "No - § 1 GwGMeldV-Immobilien confines it to obliged entities under § 2(1) nos. 10 and 12 GwG",
    "c": "Yes, but only for purchase contracts above EUR 150,000",
    "d": "Only for agents who are also residential property managers",
  },
  "Das ist eine der häufigsten Verwechslungen in der Maklerpraxis, und sie entsteht allein aus dem Namen der Verordnung. § 1 GwGMeldV-Immobilien sagt selbst, für wen sie gilt: „Diese Verordnung bestimmt in den §§ 3 bis 6 Sachverhalte bei Erwerbsvorgängen nach § 1 des Grunderwerbsteuergesetzes, die von Verpflichteten nach § 2 Absatz 1 Nummer 10 und 12 des Geldwäschegesetzes stets nach § 43 Absatz 1 des Geldwäschegesetzes zu melden sind.“ § 2 Absatz 1 Nummer 10 GwG erfasst Notare und Rechtsanwälte, Nummer 12 Wirtschaftsprüfer, vereidigte Buchprüfer, Steuerberater und Steuerbevollmächtigte. Immobilienmakler sind Nummer 14 und in § 1 GwGMeldV-Immobilien nicht genannt - die Verordnung begründet für sie also keine Katalog-Meldepflichten. Satz 2 stellt zudem klar, dass sie auch für ihre Adressaten keine eigenständigen Ermittlungspflichten schafft. Was für den Makler unverändert gilt: die allgemeine Verdachtsmeldepflicht des § 43 Absatz 1 GwG bei Vorliegen der dortigen Voraussetzungen. Der Unterschied ist also nicht „meldepflichtig oder nicht“, sondern „automatischer Katalogfall oder eigene Verdachtsbewertung“." + KYC_POINTER_DE,
  "This is one of the most common confusions in broker practice, and it arises purely from the Regulation's name. § 1 GwGMeldV-Immobilien states for itself whom it binds: \"This Regulation determines, in §§ 3 to 6, situations arising in acquisition transactions under § 1 of the Real Property Transfer Tax Act which obliged entities under § 2(1) nos. 10 and 12 of the Money Laundering Act must always report under § 43(1) of the Money Laundering Act.\" § 2(1) no. 10 GwG covers notaries and lawyers, no. 12 statutory auditors, sworn accountants, tax advisers and tax agents. Real-estate agents are no. 14 and are not named in § 1 GwGMeldV-Immobilien - so the Regulation creates no catalogue reporting duties for them. Sentence 2 also makes clear that even for its own addressees it creates no independent duties to investigate facts. What continues to apply to the agent unchanged: the general suspicious-activity reporting duty under § 43(1) GwG where its conditions are met. The difference is therefore not \"reportable or not\" but \"automatic catalogue case or own assessment of suspicion\"." + KYC_POINTER_EN),


# ===========================================================================
# Topic 5: abgrenzung
# ===========================================================================

q("abgrenzung", 1, "§ 34c Abs. 1 Satz 1 Nr. 1 bis 4 GewO", 4, False, ["all"], "a",
  "Ordnen Sie richtig zu: welche Nummer des § 34c Absatz 1 Satz 1 GewO betrifft welche Tätigkeit?",
  {
    "a": "Nr. 1 Immobilienmakler, Nr. 2 Darlehensvermittler, Nr. 3 Bauträger und Baubetreuer, Nr. 4 Wohnimmobilienverwalter",
    "b": "Nr. 1 Immobilienmakler, Nr. 2 Wohnimmobilienverwalter, Nr. 3 Darlehensvermittler, Nr. 4 Bauträger",
    "c": "Nr. 1 Bauträger, Nr. 2 Baubetreuer, Nr. 3 Immobilienmakler, Nr. 4 Wohnimmobilienverwalter",
    "d": "Nr. 1 Immobilienmakler, Nr. 2 Bauträger, Nr. 3 Wohnimmobilienverwalter, Nr. 4 Darlehensvermittler",
  },
  "Match correctly: which number of § 34c(1) sentence 1 GewO covers which activity?",
  {
    "a": "No. 1 real-estate broker, no. 2 loan intermediary, no. 3 property developer and construction supervisor, no. 4 residential property manager",
    "b": "No. 1 real-estate broker, no. 2 residential property manager, no. 3 loan intermediary, no. 4 property developer",
    "c": "No. 1 property developer, no. 2 construction supervisor, no. 3 real-estate broker, no. 4 residential property manager",
    "d": "No. 1 real-estate broker, no. 2 property developer, no. 3 residential property manager, no. 4 loan intermediary",
  },
  "Die Reihenfolge ist nicht kosmetisch, sondern die Grundlage jeder Zuordnung von Pflichten in GewO und MaBV. § 34c Abs. 1 Satz 1 GewO: Nummer 1 Vermittlung/Nachweis von Verträgen über Grundstücke, grundstücksgleiche Rechte, gewerbliche Räume oder Wohnräume (Immobilienmakler); Nummer 2 Vermittlung/Nachweis von Darlehensverträgen mit Ausnahme der Verträge im Sinne des § 34i Abs. 1 Satz 1 GewO (Immobiliar-Verbraucherdarlehen fallen also unter § 34i, nicht unter § 34c); Nummer 3 Bauvorhaben - Buchstabe a als Bauherr im eigenen Namen unter Verwendung von Erwerber-/Nutzergeldern (Bauträger), Buchstabe b als Baubetreuer im fremden Namen für fremde Rechnung; Nummer 4 Verwaltung des gemeinschaftlichen Eigentums von Wohnungseigentümern oder von Mietverhältnissen über Wohnräume für Dritte (Wohnimmobilienverwalter). Praktisch hängt an dieser Nummerierung fast alles: § 34c Abs. 2 Nr. 3 GewO (Berufshaftpflicht) nur Nr. 4, § 34c Abs. 2a GewO (Weiterbildung) seit dem 24.07.2026 nur Nr. 4, § 10 Abs. 3 MaBV nur Nr. 1, § 10 Abs. 4 und § 16 Abs. 1 MaBV nur Nr. 3, § 11 Satz 1 Nr. 1 MaBV nur Nr. 1 und Nr. 3 MaBV nur Nr. 4. Wer die Nummern verwechselt, verwechselt zwangsläufig die Pflichten.",
  "The order is not cosmetic; it is the basis of every allocation of duties in the GewO and the MaBV. § 34c(1) sentence 1 GewO: no. 1 brokering/introducing contracts over land, rights equivalent to land, commercial premises or residential premises (real-estate broker); no. 2 brokering/introducing loan contracts, excluding contracts within the meaning of § 34i(1) sentence 1 GewO (so residential consumer mortgage credit falls under § 34i, not § 34c); no. 3 construction projects - letter (a) as developer in one's own name using purchasers'/users' funds, letter (b) as construction supervisor in another's name and for another's account; no. 4 managing the common property of apartment owners, or tenancies over residential premises for third parties (residential property manager). Almost everything hangs off this numbering in practice: § 34c(2) no. 3 GewO (professional indemnity insurance) only no. 4; § 34c(2a) GewO (continuing education) since 24 July 2026 only no. 4; § 10(3) MaBV only no. 1; § 10(4) and § 16(1) MaBV only no. 3; § 11 sentence 1 no. 1 MaBV only no. 1 and § 11 sentence 1 no. 3 MaBV only no. 4. Confuse the numbers and you necessarily confuse the duties."),

q("abgrenzung", 2, "§ 34c Abs. 1 Satz 1 Nr. 4 GewO; § 1 Abs. 2, 3, 5 und 6 WEG; § 549 BGB", 4, True, ["management"], "c",
  "Welche Verwaltungstätigkeit fällt NICHT unter den Erlaubnistatbestand des Wohnimmobilienverwalters nach § 34c Absatz 1 Satz 1 Nummer 4 GewO?",
  {
    "a": "Die Verwaltung des gemeinschaftlichen Eigentums einer Wohnungseigentümergemeinschaft",
    "b": "Die Verwaltung von Mietverhältnissen über Wohnräume für einen dritten Eigentümer",
    "c": "Die Verwaltung ausschließlich gewerblich vermieteter Büroflächen für einen dritten Eigentümer",
    "d": "Die Verwaltung des gemeinschaftlichen Eigentums einschließlich Teileigentum im Sinne des § 1 Absatz 3 und 6 WEG",
  },
  "Which management activity does NOT fall under the residential property manager's permission limb in § 34c(1) sentence 1 no. 4 GewO?",
  {
    "a": "Managing the common property of a community of apartment owners",
    "b": "Managing tenancies over residential premises for a third-party owner",
    "c": "Managing exclusively commercially let office space for a third-party owner",
    "d": "Managing common property including part-ownership within the meaning of § 1(3) and (6) WEG",
  },
  "§ 34c Abs. 1 Satz 1 Nr. 4 GewO nennt zwei Alternativen, und beide sind wohnungsbezogen: „das gemeinschaftliche Eigentum von Wohnungseigentümern im Sinne des § 1 Absatz 2, 3, 5 und 6 des Wohnungseigentumsgesetzes oder für Dritte Mietverhältnisse über Wohnräume im Sinne des § 549 des Bürgerlichen Gesetzbuchs verwalten“. Die WEG-Alternative erfasst über § 1 Abs. 3 und 6 WEG auch Teileigentum, also nicht zu Wohnzwecken dienende Räume - aber eben nur, soweit sie Teil einer Wohnungseigentumsanlage sind. Die Mietverwaltungsalternative ist dagegen ausdrücklich auf Wohnräume im Sinne des § 549 BGB begrenzt. Wer für einen Dritten ausschließlich Gewerbeflächen verwaltet, die nicht Teil einer Wohnungseigentumsanlage sind, betreibt daher kein erlaubnispflichtiges Gewerbe nach § 34c GewO - und unterliegt konsequent auch nicht der Weiterbildungspflicht des § 34c Abs. 2a GewO oder der Pflichtversicherung nach § 34c Abs. 2 Nr. 3 GewO. Diese Grenze ist unangenehm scharf: eine gemischt genutzte Anlage, ein einzelnes vermietetes Wohnungspaket im Portfolio, und die Erlaubnispflicht ist wieder da.",
  "§ 34c(1) sentence 1 no. 4 GewO names two alternatives, and both are residential in character: \"managing the common property of apartment owners within the meaning of § 1(2), (3), (5) and (6) of the Condominium Act, or managing tenancies over residential premises within the meaning of § 549 BGB for third parties\". Via § 1(3) and (6) WEG the condominium alternative also covers part-ownership, i.e. rooms not serving residential purposes - but only in so far as they form part of a condominium scheme. The tenancy-management alternative, by contrast, is expressly limited to residential premises within the meaning of § 549 BGB. Anyone who manages, for a third party, exclusively commercial space that is not part of a condominium scheme is therefore not carrying on a trade requiring a permission under § 34c GewO - and consequently is not subject to the continuing-education duty in § 34c(2a) GewO or the compulsory insurance under § 34c(2) no. 3 GewO either. The boundary is uncomfortably sharp: one mixed-use scheme, one let residential package in the portfolio, and the permission requirement is back."),

q("abgrenzung", 3, "§ 34c Abs. 1 Satz 1 Nr. 1 und 4 GewO; § 34c Abs. 2 Nr. 3 und Abs. 2a GewO", 5, True, ["management"], "d",
  "Ein Maklerbüro erweitert sein Angebot und übernimmt künftig auch die WEG-Verwaltung mehrerer Anlagen. Was ändert sich rechtlich?",
  {
    "a": "Nichts - die bestehende Erlaubnis nach § 34c GewO deckt alle Tätigkeiten der Vorschrift ab",
    "b": "Es ist lediglich eine Anzeige der erweiterten Tätigkeit erforderlich",
    "c": "Es entsteht eine Weiterbildungspflicht von 40 Stunden in drei Kalenderjahren, weil zwei Tätigkeitsbereiche vorliegen",
    "d": "Es wird eine Erlaubnis nach Nummer 4 benötigt; damit kommen zusätzlich die Berufshaftpflichtversicherung nach § 34c Absatz 2 Nummer 3 GewO und die Weiterbildungspflicht von 20 Stunden in drei Kalenderjahren nach § 34c Absatz 2a GewO hinzu",
  },
  "A brokerage expands its offering and will in future also take on condominium management for several schemes. What changes legally?",
  {
    "a": "Nothing - the existing § 34c GewO permission covers all activities in the provision",
    "b": "Only a notification of the expanded activity is required",
    "c": "A continuing-education duty of 40 hours in three calendar years arises, because there are now two fields of activity",
    "d": "A permission under no. 4 is needed; that additionally brings professional indemnity insurance under § 34c(2) no. 3 GewO and the 20-hour / three-calendar-year continuing-education duty under § 34c(2a) GewO",
  },
  "Die Erlaubnis nach § 34c Abs. 1 GewO ist tätigkeitsbezogen, nicht personenbezogen: sie wird für den jeweiligen Erlaubnistatbestand erteilt, und wer eine weitere Nummer aufnimmt, braucht die Erlaubnis dafür. Das ist ein durchaus häufiger Fall - Maklerbüros mit angeschlossener Verwaltung sind Alltag - und genau deshalb muss die Grenze sauber gezogen werden. Mit der Nummer 4 kommen zwei Pflichten hinzu, die den Makler als Makler nicht treffen: der Nachweis einer Berufshaftpflichtversicherung nach § 34c Abs. 2 Nr. 3 GewO (ausgestaltet in §§ 15, 15a MaBV, Mindestversicherungssumme 500 000 Euro je Versicherungsfall und 1 000 000 Euro je Jahr) und die Weiterbildungspflicht nach § 34c Abs. 2a GewO. Warum 20 und nicht 40 Stunden? Unter dem alten Recht galt die Pflicht für Nummer 1 UND Nummer 4, und die DIHK rechnete für Inhaber beider Erlaubnisse mit 20 Stunden „pro Tätigkeitsbereich“, also 40 Stunden zusammen. Seit dem 24.07.2026 ist die Maklerseite entfallen; es bleibt der Verwalterbereich mit 20 Stunden in drei Kalenderjahren. Antwort c beschreibt also exakt den überholten Rechtszustand - eine der wahrscheinlichsten Fehlannahmen in dieser Materie. Für die Verwalterseite siehe das Modul 'immobilienverwalter_weiterbildung'.",
  "The permission under § 34c(1) GewO is activity-based, not person-based: it is granted for the particular permission limb, and anyone taking up a further number needs the permission for it. This is a genuinely common case - brokerages with an attached management arm are everyday practice - and that is exactly why the boundary has to be drawn cleanly. Number 4 brings two duties that do not bind the broker qua broker: proof of professional indemnity insurance under § 34c(2) no. 3 GewO (fleshed out in §§ 15, 15a MaBV, minimum sum insured EUR 500,000 per claim and EUR 1,000,000 per year) and the continuing-education duty under § 34c(2a) GewO. Why 20 and not 40 hours? Under the old law the duty applied to no. 1 AND no. 4, and the DIHK calculated 20 hours \"per field of activity\" for holders of both permissions, i.e. 40 hours combined. Since 24 July 2026 the broker side has fallen away; what remains is the manager field with 20 hours in three calendar years. Answer c therefore describes precisely the superseded position - one of the likeliest false assumptions in this area. For the manager side see the 'immobilienverwalter_weiterbildung' module."),

q("abgrenzung", 4, "§ 1 Abs. 2 Satz 2 MaBV; § 11 Satz 1 Nr. 3 MaBV", 4, False, ["management"], "b",
  "Ein Gewerbetreibender hat Erlaubnisse nach § 34c Absatz 1 Satz 1 Nummer 1 und Nummer 4 GewO. Welche MaBV-Vorschriften gelten für seine Verwaltertätigkeit?",
  {
    "a": "Alle MaBV-Vorschriften, weil er auch Makler ist",
    "b": "Nur §§ 11, 15 bis 15b, 18 Absatz 1 Nummer 7, 9 und 10, Absatz 2 und 3 sowie § 19 MaBV",
    "c": "Nur § 15b MaBV",
    "d": "Keine - für Wohnimmobilienverwalter gilt die MaBV überhaupt nicht",
  },
  "A trader holds permissions under § 34c(1) sentence 1 nos. 1 and 4 GewO. Which MaBV provisions apply to his management activity?",
  {
    "a": "All MaBV provisions, because he is also a broker",
    "b": "Only §§ 11, 15 to 15b, 18(1) nos. 7, 9 and 10, (2) and (3), and § 19 MaBV",
    "c": "Only § 15b MaBV",
    "d": "None - the MaBV does not apply to residential property managers at all",
  },
  "§ 1 Abs. 2 Satz 2 MaBV bestimmt punktgenau: die Verordnung „gilt zudem nicht für Gewerbetreibende, die als Wohnimmobilienverwalter nach § 34c Absatz 1 Satz 1 Nummer 4 der Gewerbeordnung tätig sind, mit Ausnahme der §§ 11, 15 bis 15b, 18 Absatz 1 Nummer 7, 9 und 10, Absatz 2 und 3 sowie § 19 dieser Verordnung“. Für die Verwaltertätigkeit gilt also ein sehr schmaler Kern: die Informationspflicht des § 11 (für Verwalter über Satz 1 Nummer 3 - auf Anfrage unverzüglich Angaben über berufsspezifische Qualifikationen und die in den letzten drei Kalenderjahren absolvierten Weiterbildungsmaßnahmen, wobei ein Verweis auf die eigene Internetseite genügt), die Versicherungs- und Weiterbildungsvorschriften §§ 15 bis 15b, die zugehörigen Bußgeldtatbestände und § 19 zur grenzüberschreitenden Dienstleistungserbringung. Buchführung nach § 10, Aufbewahrung nach § 14, Rechnungslegung nach § 8, Sicherungspflichten nach §§ 2 bis 7 und Prüfungen nach § 16 gelten für die Verwaltertätigkeit NICHT. Wichtig für den Doppelerlaubnisinhaber: die Trennung verläuft nach Tätigkeit, nicht nach Person. Dieselbe Firma unterliegt für ihre Maklermandate dem vollen MaBV-Pflichtenprogramm und für ihre Verwaltermandate nur dem schmalen Kern - das erfordert getrennte Prozesse und getrennte Aktenführung, nicht einen gemeinsamen Mindeststandard.",
  "§ 1(2) sentence 2 MaBV is precise: the Regulation \"also does not apply to traders acting as residential property managers under § 34c(1) sentence 1 no. 4 of the Trade Regulation Act, with the exception of §§ 11, 15 to 15b, 18(1) nos. 7, 9 and 10, (2) and (3), and § 19 of this Regulation\". So a very narrow core applies to the management activity: the information duty in § 11 (for managers via sentence 1 no. 3 - on request, without delay, particulars of profession-specific qualifications and the continuing education completed in the last three calendar years, where a reference to the trader's own website suffices), the insurance and continuing-education provisions in §§ 15 to 15b, the corresponding fine provisions, and § 19 on cross-border provision of services. Bookkeeping under § 10, retention under § 14, rendering of account under § 8, client-asset security under §§ 2 to 7 and audits under § 16 do NOT apply to the management activity. Important for a holder of both permissions: the split runs by activity, not by person. The same firm is subject to the full MaBV programme for its brokerage mandates and only to the narrow core for its management mandates - which calls for separate processes and separate files, not a single common minimum standard."),


# ===========================================================================

NO_QUOTA_NOTE_DE = (
    "Dieses Modul ist Lern- und Übungsmaterial und stellt keine anrechenbaren "
    "Weiterbildungsstunden aus. Für Immobilienmakler besteht seit dem 24.07.2026 "
    "ohnehin keine gewerberechtliche Weiterbildungspflicht mehr (§ 34c Absatz 2a "
    "GewO erfasst nur noch Gewerbetreibende nach Absatz 1 Satz 1 Nummer 4). Wer "
    "zugleich eine Erlaubnis als Wohnimmobilienverwalter hält, bleibt für diesen "
    "Tätigkeitsbereich weiterbildungspflichtig; das Absolvieren dieses oder des "
    "Schwestermoduls 'immobilienverwalter_weiterbildung' zählt NICHT auf die "
    "gesetzliche Pflicht von 20 Stunden in drei Kalenderjahren an, weil diese eine "
    "Weiterbildung bei einem Anbieter verlangt, der die Anforderungen der Anlage 2 "
    "MaBV erfüllt. Zettacard ist kein Weiterbildungsanbieter im Sinne des § 15b "
    "Absatz 1 Satz 5 MaBV."
)
NO_QUOTA_NOTE_EN = (
    "This module is study and practice material and does not issue counted "
    "Weiterbildungsstunden. For real-estate brokers there is in any event no trade-law "
    "continuing-education duty at all since 24 July 2026 (§ 34c(2a) GewO now covers only "
    "traders under (1) sentence 1 no. 4). Anyone who also holds a residential property "
    "manager permission remains subject to the duty for that field of activity; completing "
    "this module or the sibling module 'immobilienverwalter_weiterbildung' does NOT count "
    "toward the statutory 20-hour / three-calendar-year Weiterbildungspflicht, which requires "
    "training from a provider meeting MaBV Anlage 2's requirements. Zettacard is not a "
    "Weiterbildungsanbieter within the meaning of § 15b(1) sentence 5 MaBV."
)

META = {
    "app": "Zettacard / makler-berufspflichten-lernmodul",
    "version": "0.1-DRAFT",
    "generated": "2026-08-17",
    "generator": "authored:claude-opus/2026-08-17 (data/gen_makler_berufspflichten.py)",
    "title_de": "Immobilienmakler - Berufspflichten (§ 34c GewO / MaBV)",
    "title_en": "Real-estate brokers - professional duties (§ 34c GewO / MaBV)",
    "description": (
        "DRAFT question bank for a professional-duties KNOWLEDGE CHECK for licensed German "
        "real-estate brokers (Immobilienmakler, § 34c Abs. 1 Satz 1 Nr. 1 GewO) and their "
        "staff. READ THIS FIRST, because it is the module's most important fact and the "
        "reason the module is shaped this way: THERE IS NO STATE EXAM AND NO SACHKUNDE-"
        "PRUEFUNG FOR THIS TRADE. § 34c GewO has never contained a qualification or "
        "competence requirement - the word 'Sachkunde' appears zero times in § 34c GewO and "
        "zero times in the whole MaBV - and § 34c Abs. 2 GewO is an exhaustive list of three "
        "grounds for refusal (Zuverlaessigkeit, geordnete Vermoegensverhaeltnisse, and "
        "Berufshaftpflicht for Wohnimmobilienverwalter only). The fallback continuing-"
        "education duty that used to apply to brokers was REPEALED with effect from "
        "24.07.2026 by Art. 1 Nr. 3 of the Gesetz zum Buerokratierueckbau in der "
        "Gewerbeordnung ... of 20.07.2026 (BGBl. 2026 I Nr. 215), which struck brokers out of "
        "§ 34c Abs. 2a GewO; Art. 2 Nr. 4 of the same Act deleted Teil A of MaBV Anlage 1, the "
        "broker syllabus itself. This module is therefore explicitly framed like this repo's "
        "'cka' module - a knowledge check, not an exam simulator - because there is no exam to "
        "simulate. Note that virtually the entire practitioner web (IHK pages, trade-body pages, "
        "the DIHK's own FAQ as at January 2025) still says otherwise as at this writing; the "
        "consolidated statute is right and the secondary layer is stale. Five topics: erlaubnis "
        "(§ 34c GewO permission scope and refusal grounds), mabv_pflichten (MaBV §§ 1, 2, 7, 8, "
        "10, 11, 14, 16 professional duties), sanktionen (§ 18 MaBV via §§ 144-146 GewO), "
        "gwg_makler (three broker-specific AML questions only) and abgrenzung (the boundary "
        "between the four § 34c permission limbs). WHAT THIS MODULE DOES NOT CLAIM: it is study "
        "and practice material and issues no counted Weiterbildungsstunden - see "
        "meta.no_quota_disclaimer. Content is independently phrased and grounded directly in "
        "GewO, MaBV, GwG and GwGMeldV-Immobilien text retrieved from gesetze-im-internet.de, NOT "
        "sourced or paraphrased from any exam-prep or compliance-training vendor's question "
        "catalogue, explanations or wording. See-also: this is a SEPARATE module from "
        "'immobilienverwalter_weiterbildung' (Wohnimmobilienverwalter, § 34c Abs. 1 Satz 1 Nr. 4 "
        "GewO, MaBV Anlage 1) - the two trades sit in the same statutory provision but are "
        "legally distinct scopes with almost inverted duty sets, and they are cross-linked, not "
        "merged (PO decision 2026-08-17, same pattern as fadp_ch <-> datenschutz). Holding a "
        "broker permission and a Wohnimmobilienverwalter permission concurrently is a real and "
        "common case - under the pre-24.07.2026 regime the DIHK FAQ recorded such a person as "
        "owing 40 combined hours of continuing education, 20 per field of activity - and a "
        "practitioner in that position should work through both modules. For the general "
        "Geldwaesche regime see the 'kyc_aml' module; this module deliberately covers only the "
        "broker-specific GwG provisions kyc_aml does not."
    ),
    "class": "ALL",
    "locales": ["de", "en"],
    "canonical_locale": "de",
    "locale_note": (
        "DE is canonical and EN is a full parallel translation. The remaining ten locales this "
        "app carries (uk, pl, ar, zh, hi, tr, fr, ru, es, it) are tracked as a follow-up for the "
        "question bank itself, same launch pattern as fadp_ch / aevo / kyc_aml / kartellrecht / "
        "dora / nis2 - this is German trade law with no realistic non-DE/EN demand for the "
        "question text. UI strings (module label, topic labels, module card) DO ship in all 12 "
        "locales per AGENTS.md constraint 5, and are NOT part of this draft round."
    ),
    "orthography_note": (
        "Deutsches Standarddeutsch mit echten Unicode-Umlauten und Eszett (ä/ö/ü/ß) - keine "
        "ASCII-Ersatzschreibung. Statutory quotations preserve the source text's own older "
        "orthography where it occurs (e.g. 'Abschluß', 'daß', 'aus besonderem Anlaß' in the "
        "pre-1996 parts of the MaBV) rather than silently modernising a quotation."
    ),
    "exam_format_note": (
        "ES GIBT KEINE PRUEFUNG. Für das Gewerbe des Immobilienmaklers nach § 34c Absatz 1 Satz 1 "
        "Nummer 1 GewO existiert weder eine staatliche noch eine Kammerprüfung, weder ein "
        "Sachkundenachweis noch - seit dem 24.07.2026 - eine Weiterbildungspflicht. Dieses Modul "
        "ist deshalb bewusst kein Prüfungssimulator, sondern ein Wissenscheck über die "
        "tatsächlich bindenden Berufspflichten, genauso gerahmt wie das Modul 'cka' in diesem "
        "Repository. Wer eine echte Kammerprüfung im § 34x-GewO-Umfeld sucht: § 34a GewO "
        "(Bewachungsgewerbe), § 34d GewO (Versicherungsvermittler) und § 34f GewO "
        "(Finanzanlagenvermittler) enthalten jeweils eine ausdrückliche Sachkundeprüfung vor der "
        "IHK. § 34c GewO enthält keine und hat nie eine enthalten."
    ),
    "no_quota_disclaimer": {
        "de": NO_QUOTA_NOTE_DE,
        "en": NO_QUOTA_NOTE_EN,
    },
    "certificate_copy_note": (
        "If and when a course layer or completion certificate is built for this module, its copy "
        "must repeat meta.no_quota_disclaimer verbatim in substance and must NOT use the words "
        "Weiterbildungsnachweis, Weiterbildungsstunden, zertifiziert, Sachkundenachweis or any "
        "formulation implying that completion satisfies a statutory duty. For brokers there is no "
        "statutory duty to satisfy; for anyone who also holds a Nr. 4 permission, § 15b Abs. 1 "
        "Satz 5 MaBV puts the Anlage-2 quality obligation on the Weiterbildungsanbieter, a "
        "regulatory posture Zettacard has not taken on. PO instruction 2026-08-17."
    ),
    "point_system": (
        "3-5 points per question, matching this app's existing compliance modules. 5 points marks "
        "the points where getting it wrong has direct regulatory consequences: the non-existence "
        "of a Sachkundenachweis, the broker/Verwalter split of the Berufshaftpflicht and "
        "Weiterbildung duties, the § 11 MaBV Textform/timing duty, the § 16 MaBV audit split, the "
        "§ 10 Abs. 6 GwG threshold, and the effect of taking on a Nr. 4 permission."
    ),
    "pass_rule_note": (
        "DRAFT: no EXAM_QUESTION_COUNT_BY_TYPE / MAX_ERROR_POINTS_BY_TYPE / "
        "EXAM_TIME_LIMIT_MS_BY_TYPE / EXAM_TOPIC_DRAW values are proposed. There is no real exam "
        "to model a pass mark on (see exam_format_note), so any threshold would be a pure product "
        "decision and is deliberately left to a design pass after legal review. This module is NOT "
        "registered in data/build_modules.py, data/modules_manifest.json or app/data/modules.json, "
        "and app/app.js is untouched."
    ),
    "legal_review_status": (
        "AI-prepared DRAFT, 2026-08-17, NOT reviewed by a qualified lawyer and NOT to be shipped "
        "to learners before that review. Primary sources re-verified for this build by direct curl "
        "against gesetze-im-internet.de on 2026-08-17 (WebFetch is ROBOTS_DISALLOWED on that host "
        "in this sandbox): GewO § 34c Abs. 1-5 in full and §§ 144-146; MaBV (slug /gewo_34cdv/, "
        "NOT /mabv/) §§ 1, 2, 3, 7, 8, 10, 11, 14, 15, 15a, 15b, 16, 18, 19 and Anlagen 1-2, with "
        "Anlage 3 confirmed '(weggefallen)'; GwG §§ 1 Abs. 11, 2 Abs. 1 Nr. 14, 6 Abs. 2 Nr. 6, 10 "
        "Abs. 6, 16a; GwGMeldV-Immobilien § 1. Currency as retrieved: GewO 'zuletzt durch Artikel 1 "
        "des Gesetzes vom 20. Juli 2026 (BGBl. 2026 I Nr. 215)'; MaBV 'zuletzt durch Artikel 2 der "
        "Verordnung vom 28. Juli 2026 (BGBl. 2026 I Nr. 229)', with gesetze-im-internet.de flagging "
        "the Art. 2 G v. 20.7.2026 change as 'textlich nachgewiesen, dokumentarisch noch nicht "
        "abschliessend bearbeitet'. Mechanical negative checks re-run for this build: 'Sachkunde' -> "
        "0 hits in § 34c GewO, 0 hits in the MaBV; 'Makler' -> 0 hits in § 1 GwGMeldV-Immobilien. "
        "THIS CORNER OF THE LAW IS MOVING FAST - the MaBV was amended twice inside eight days in "
        "July 2026, one of those changes with a defective change instruction that had to be "
        "consolidated 'sinngemaess' (see the Fussnoten to §§ 2 and 16 MaBV). Set a re-verification "
        "date of no later than 2026-11-30 and re-read § 34c GewO and the MaBV from the amending "
        "instruments, not from this file. Background and the full citation ledger: "
        "docs/maklerschein-pre-review-dossier-2026-08-17.md."
    ),
    "sources": {
        "tier_a_binding": [
            "Gewerbeordnung (GewO) § 34c - https://www.gesetze-im-internet.de/gewo/__34c.html (Abs. 1-5 in full, incl. Fussnote)",
            "Gewerbeordnung (GewO) §§ 144, 145, 146 - https://www.gesetze-im-internet.de/gewo/__144.html (Bussgeldrahmen: Abs. 4)",
            "Makler- und Bauträgerverordnung (MaBV) - https://www.gesetze-im-internet.de/gewo_34cdv/ - NOTE the non-obvious slug 'gewo_34cdv'; '/mabv/' 404s. §§ 1, 2, 3, 7, 8, 10, 11, 14, 15, 15a, 15b, 16, 18, 19 and Anlagen 1-2 read; Anlage 3 confirmed '(weggefallen)'",
            "Gesetz zum Bürokratierückbau in der Gewerbeordnung und dem Energieverbrauchskennzeichnungsgesetz sowie anderer Rechtsvorschriften zur Aufhebung von Berichtspflichten, G. v. 20.07.2026, BGBl. 2026 I Nr. 215 - Art. 1 Nr. 3, Art. 2 Nr. 4 und 5, Art. 11; official BGBl PDF at recht.bund.de/bgbl/1/2026/215/regelungstext.pdf. Effect on § 34c Abs. 2a GewO re-verified against the consolidated text on 2026-08-17.",
            "Geldwäschegesetz (GwG) §§ 1 Abs. 11, 2 Abs. 1 Nr. 14, 6 Abs. 2 Nr. 6, 10 Abs. 6, 16a - https://www.gesetze-im-internet.de/gwg_2017/",
            "GwGMeldV-Immobilien § 1 - https://www.gesetze-im-internet.de/imgwgmeldv/__1.html (negative finding: scope limited to § 2 Abs. 1 Nr. 10 und 12 GwG)",
            "GewO §§ 34a, 34d, 34f - read for the Sachkundeprüfung contrast quoted in the erlaubnis topic",
        ],
        "tier_b_official_not_binding": [
            "DIHK, 'FAQ: Weiterbildungspflicht für Immobilienmakler und Wohnimmobilienverwalter', Stand Januar 2025 - HISTORICALLY SUPERSEDED for the broker half since 24.07.2026. Cited in this module only for the 20-hours-per-field / 40-hours-combined arithmetic under the OLD regime, and expressly labelled as the superseded position wherever it appears. No answer key rests on it.",
        ],
        "tier_c_orientation_only": [
            "IHK and trade-body landing pages for § 34c GewO - all still describing the pre-abolition regime as at 2026-08-17. Used only as evidence that the secondary layer is stale; nothing here rests on them.",
        ],
        "note": (
            "No exam-prep, e-learning or compliance-training vendor's course text, question "
            "wording, explanations or structure was read into, copied into, or paraphrased into "
            "this module (AGENTS.md constraint 1). German statutory text is an amtliches Werk "
            "under § 5 UrhG and carries no copyright, so the verbatim statutory quotations in "
            "the explanations raise none of that constraint's concerns - they are the opposite "
            "of a vendor catalogue."
        ),
    },
    "related_modules": [
        {
            "exam_type": "immobilienverwalter_weiterbildung",
            "relation": "see_also",
            "de": "Das Modul 'immobilienverwalter_weiterbildung' behandelt den Wohnimmobilienverwalter nach § 34c Absatz 1 Satz 1 Nummer 4 GewO und die acht Themengebiete der Anlage 1 MaBV. Makler und Wohnimmobilienverwalter stehen in derselben Vorschrift, sind aber rechtlich eigenständige Erlaubnistatbestände mit nahezu umgekehrten Pflichtenbündeln - sie werden deshalb verlinkt und nicht zusammengeführt. Wer beide Erlaubnisse hält - ein realer und häufiger Fall; die DIHK-FAQ rechnete für solche Doppelerlaubnisinhaber unter dem bis zum 23.07.2026 geltenden Recht mit 40 Stunden Weiterbildung insgesamt, 20 je Tätigkeitsbereich -, sollte beide Module absolvieren.",
            "en": "The 'immobilienverwalter_weiterbildung' module covers the residential property manager under § 34c(1) sentence 1 no. 4 GewO and the eight topic areas of MaBV Anlage 1. Brokers and residential property managers sit in the same provision but are legally distinct permission limbs with almost inverted duty sets - so they are cross-linked, not merged. Anyone holding both permissions - a real and common case; under the law in force until 23 July 2026 the DIHK FAQ recorded such holders as owing 40 hours of continuing education in total, 20 per field of activity - should work through both modules.",
        },
        {
            "exam_type": "kyc_aml",
            "relation": "see_also",
            "de": "Das Modul 'kyc_aml' behandelt das allgemeine Geldwäscheregime: Typologien, Drei-Phasen-Modell, politisch exponierte Personen, Verdachtsmeldewesen nach § 43 GwG, verstärkte Sorgfaltspflichten und Sanktionen. Dieses Modul beschränkt sich bewusst auf die drei maklerspezifischen Vorschriften, die 'kyc_aml' nicht abdeckt (§ 2 Abs. 1 Nr. 14 GwG, § 1 Abs. 11 GwG, § 10 Abs. 6 GwG und die Nichtanwendbarkeit der GwGMeldV-Immobilien) und dupliziert 'kyc_aml' nicht.",
            "en": "The 'kyc_aml' module covers the general anti-money-laundering regime: typologies, the three-phase model, politically exposed persons, suspicious activity reporting under § 43 GwG, enhanced due diligence and sanctions. This module deliberately restricts itself to the three broker-specific provisions 'kyc_aml' does not cover (§ 2(1) no. 14 GwG, § 1(11) GwG, § 10(6) GwG and the inapplicability of the GwGMeldV-Immobilien) and does not duplicate 'kyc_aml'.",
        },
    ],
    "license": "CC BY-NC-SA 4.0",
    "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "license_note": (
        "Attribution-NonCommercial-ShareAlike: free to use, adapt, and redistribute for "
        "non-commercial training purposes, with credit and under the same license. Commercial "
        "reuse needs a separate arrangement."
    ),
    "renewal_months": None,
    "renewal_basis": "no_statutory_duty",
    "renewal_note": (
        "Deliberately null, and the reason is the module's headline finding rather than an "
        "oversight. Since 24.07.2026 a German Immobilienmakler has NO statutory continuing-"
        "education duty at all: § 34c Abs. 2a GewO now covers only Gewerbetreibende nach Absatz 1 "
        "Satz 1 Nummer 4 (Wohnimmobilienverwalter). Putting a renewal interval here would imply a "
        "recurring statutory obligation that does not exist. The only genuinely recurring training-"
        "adjacent duty in a broker's perimeter is § 6 Abs. 2 Nr. 6 GwG, 'die erstmalige und "
        "laufende Unterrichtung der Mitarbeiter' on money-laundering typologies and methods - a "
        "duty to instruct staff on an ongoing basis, with no statutory frequency and no test to "
        "pass; an annual AML refresher is a practice convention, not a statutory number. See the "
        "'kyc_aml' module for that regime."
    ),
    "legal_disclaimer": "Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine Rechts- oder Compliance-Beratung dar. Die gewerbe- und geldwäscherechtlichen Anforderungen sind im Einzelfall durch qualifizierte Juristen zu validieren.",
    "legal_disclaimer_en": "This training material is provided for education and information purposes only and does not constitute legal or compliance advice. The trade-law and anti-money-laundering requirements must be validated in each individual case by qualified lawyers.",
    "topic_codes": {
        code: {"de": TOPICS[code], "en": TOPIC_LABELS_EN[code]} for code in TOPICS
    },
}


def main():
    ids = [x["id"] for x in Q]
    assert len(set(ids)) == len(ids), "duplicate question ids"
    for x in Q:
        assert x["correct"][0] in x["text"]["de"]["options"], x["id"]
        assert set(x["text"]["de"]["options"]) == set(x["text"]["en"]["options"]), x["id"]
        assert x["roles"], x["id"]
    dist = {}
    for x in Q:
        dist[x["topic_code"]] = dist.get(x["topic_code"], 0) + 1
    meta = dict(META)
    meta["total_questions"] = len(Q)
    meta["topic_distribution"] = dist
    json.dump({"meta": meta, "questions": Q},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {OUT}: {len(Q)} questions, distribution {dist}")


if __name__ == "__main__":
    main()
