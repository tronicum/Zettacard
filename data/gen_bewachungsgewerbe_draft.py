#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic generator for data/bewachungsgewerbe_pilot_DRAFT.json.

Module: bewachungsgewerbe -- "Bewachungsgewerbe - IHK-Sachkundepruefung (§ 34a GewO)"

DE is the canonical locale (this is a German state-administered trade exam);
EN is a full parallel translation, same launch pattern as aevo / fadp_ch /
kyc_aml / kartellrecht. German text is written with real Unicode umlauts and
eszett directly in this source file, same convention as
gen_makler_berufspflichten.py -- there is deliberately no ASCII
transliteration layer, because blanket digraph replacement corrupts genuine
German words ("Dauer", "neue", "Steuer").

SOURCING (see docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md):
  The exam's subject matter is fixed by legal instrument, not by any private
  catalogue. § 9 Abs. 2 BewachV: "Gegenstand der Sachkundepruefung sind die in
  § 7 in Verbindung mit Anlage 2 aufgefuehrten Sachgebiete". § 7 BewachV names
  seven Sachgebiete; Anlage 2 BewachV breaks them down to individually cited
  statutory provisions. German statutory text is an amtliches Werk under § 5
  UrhG and carries no copyright.

  Every question below is authored from the text of the provision named in its
  own `legal_basis` field, each of which was fetched and read directly from
  gesetze-im-internet.de on 2026-08-17 (GewO, BewachV incl. Anlage 2, BGB,
  StGB, StPO, WaffG, BDSG).

  NOT used as a source, directly or indirectly: any exam-prep vendor's question
  text, explanations, wording or structure (AGENTS.md constraint 1). The DIHK
  "Rahmenplan fuer die Sachkundepruefung im Bewachungsgewerbe" was read as a
  scope cross-check only and is NOT a content source -- it carries its own
  copyright notice (DIHK e.V.) and none of its wording, table structure,
  taxonomy assignments or "(S)" markers is reproduced here. See dossier § 4.1.

NOT wired into any build path. Not registered in build_modules.py or
modules_manifest.json. app.js untouched. Run manually:
    python3 data/gen_bewachungsgewerbe_draft.py
The script performs its own integrity + orthography checks and exits non-zero
on failure.
"""

import json
import os
import sys
import unicodedata

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "bewachungsgewerbe_pilot_DRAFT.json")

KEY_ORDER = ["id", "topic", "topic_code", "class_scope", "grundstoff",
             "legal_basis", "points", "high_stakes", "question_type",
             "image_ref", "correct", "text", "explanation"]

# The seven Sachgebiete of § 7 BewachV, 1:1, in the regulation's own order and
# wording.
TOPIC_DE = {
    "oeffentliche_sicherheit":
        "Recht der öffentlichen Sicherheit und Ordnung einschließlich Gewerberecht",
    "datenschutz": "Datenschutzrecht",
    "bgb": "Bürgerliches Gesetzbuch",
    "strafrecht_waffen": "Straf- und Verfahrensrecht, Umgang mit Waffen",
    "unfallverhuetung": "Unfallverhütungsvorschrift Wach- und Sicherungsdienste",
    "umgang_menschen": "Umgang mit Menschen, Deeskalation, interkulturelle Kompetenz",
    "sicherheitstechnik": "Grundzüge der Sicherheitstechnik",
}

QUESTIONS = []


def Q(qid, topic_code, legal_basis, points, high_stakes, correct,
      de_q, de_opts, de_expl, en_q, en_opts, en_expl, grundstoff=True):
    QUESTIONS.append({
        "id": "bewachung-%s-%s" % (topic_code, qid),
        "topic": TOPIC_DE[topic_code],
        "topic_code": topic_code,
        "class_scope": ["ALL"],
        "grundstoff": grundstoff,
        "legal_basis": legal_basis,
        "points": points,
        "high_stakes": high_stakes,
        "question_type": "single_choice",
        "image_ref": None,
        "correct": [correct],
        "text": {
            "de": {"question": de_q, "options": de_opts},
            "en": {"question": en_q, "options": en_opts},
        },
        "explanation": {"de": de_expl, "en": en_expl},
    })


# ---------------------------------------------------------------------------
# 1. Recht der öffentlichen Sicherheit und Ordnung einschließlich Gewerberecht
#    (§ 7 Nr. 1 BewachV / Anlage 2 Nr. 1) -- 5 questions
# ---------------------------------------------------------------------------

Q("01", "oeffentliche_sicherheit",
  "§ 34a Abs. 5 GewO", 5, True, "c",
  "Sie sind als Wachperson auf einem Firmengelände eingesetzt. Ein Mitarbeiter des Auftraggebers "
  "fordert Sie auf, einen Besucher zu durchsuchen, weil dieser sich verdächtig verhalte. Auf welche "
  "Befugnisse können Sie sich dabei berufen?",
  {"a": "Auf die Befugnisse der Polizei, weil Sie im Auftrag des Hausrechtsinhabers handeln",
   "b": "Auf eine allgemeine Kontrollbefugnis, die sich aus dem Bewachungsvertrag ergibt",
   "c": "Nur auf die Jedermannsrechte (Notwehr, Notstand, Selbsthilfe), auf vertraglich übertragene "
        "Selbsthilferechte und auf gegebenenfalls gesetzlich übertragene Befugnisse - stets unter "
        "Beachtung der Erforderlichkeit",
   "d": "Auf die Weisung des Auftraggebers, die als Rechtsgrundlage ausreicht"},
  "§ 34a Abs. 5 Satz 1 GewO ist abschließend: Gewerbetreibende und Beschäftigte dürfen gegenüber "
  "Dritten „nur die Rechte, die Jedermann im Falle einer Notwehr, eines Notstandes oder einer "
  "Selbsthilfe zustehen, die ihnen vom jeweiligen Auftraggeber vertraglich übertragenen "
  "Selbsthilferechte sowie die ihnen gegebenenfalls in Fällen gesetzlicher Übertragung zustehenden "
  "Befugnisse eigenverantwortlich ausüben“. Satz 2 stellt zusätzlich klar, dass dabei „der Grundsatz "
  "der Erforderlichkeit zu beachten“ ist. Eine Durchsuchungsbefugnis gehört nicht dazu; eine Durchsuchung "
  "kann allenfalls freiwillig geduldet werden. (a) ist falsch - private Bewachung erhält durch den "
  "Auftrag keine hoheitlichen Befugnisse; § 17 Abs. 1 Satz 2 BewachV verlangt sogar, dass die "
  "Dienstanweisung genau darauf hinweist. (b) und (d) sind falsch, weil weder Vertrag noch Weisung "
  "Befugnisse gegenüber Dritten schaffen können, die das Gesetz nicht vorsieht.",
  "You are deployed as a guard on company premises. An employee of the client asks you to search a "
  "visitor because the visitor is behaving suspiciously. Which powers can you rely on?",
  {"a": "Police powers, because you are acting on behalf of the holder of the domiciliary right",
   "b": "A general power of inspection arising from the guarding contract",
   "c": "Only the rights available to anyone (self-defence, necessity, self-help), self-help rights "
        "transferred by contract from the client, and any powers transferred by statute - always "
        "subject to the requirement of necessity",
   "d": "The client's instruction, which is sufficient as a legal basis"},
  "§ 34a(5) sentence 1 GewO is exhaustive: the trader and their staff may exercise, in relation to third "
  "parties, only the rights available to anyone in cases of self-defence, necessity or self-help, the "
  "self-help rights contractually transferred by the client, and any powers transferred by statute. "
  "Sentence 2 adds that the principle of necessity must be observed. A power to search is not among them; "
  "at most a search can be voluntarily tolerated. (a) is wrong - private guarding acquires no sovereign "
  "powers through the assignment, and § 17(1) sentence 2 BewachV actually requires the standing order to "
  "say so. (b) and (d) are wrong because neither a contract nor an instruction can create powers over "
  "third parties that the law does not provide.",
  )

Q("02", "oeffentliche_sicherheit",
  "§ 17 Abs. 1 und 2 BewachV", 3, False, "b",
  "Welche Angabe muss die Dienstanweisung eines Bewachungsunternehmens nach der Bewachungsverordnung "
  "zwingend enthalten?",
  {"a": "Die Höhe der Haftpflichtversicherungssumme des Unternehmens",
   "b": "Den Hinweis, dass die Wachperson nicht die Eigenschaft und die Befugnisse eines "
        "Polizeivollzugsbeamten oder eines sonstigen Behördenbediensteten besitzt",
   "c": "Die Bewacherregisteridentifikationsnummer jedes einzelnen Auftraggebers",
   "d": "Eine Auflistung der Straftatbestände, bei denen eine Festnahme zwingend vorzunehmen ist"},
  "§ 17 Abs. 1 Satz 2 BewachV: die Dienstanweisung „muss den Hinweis enthalten, dass die Wachperson "
  "nicht die Eigenschaft und die Befugnisse eines Polizeivollzugsbeamten, oder eines sonstigen "
  "Bediensteten einer Behörde besitzt“. Satz 3 verlangt zusätzlich die Regelung, dass Waffen nur mit "
  "Zustimmung des Gewerbetreibenden geführt werden dürfen und jeder Gebrauch unverzüglich anzuzeigen ist. "
  "Nach § 17 Abs. 2 BewachV ist der Wachperson vor der ersten Aufnahme der Bewachungstätigkeit ein "
  "Abdruck gegen Empfangsbescheinigung auszuhändigen. Die Versicherungssumme (§ 14 BewachV) und die "
  "Registeridentifikationsnummern (§ 18 Abs. 1 BewachV, Ausweis) sind an anderer Stelle geregelt; eine "
  "Festnahmepflicht kennt das Recht nicht - § 127 Abs. 1 StPO ist eine Befugnis, keine Pflicht.",
  "Which statement must a guarding company's standing order (Dienstanweisung) contain under the "
  "Bewachungsverordnung?",
  {"a": "The amount of the company's liability insurance cover",
   "b": "A statement that the guard has neither the status nor the powers of a police officer or any "
        "other public official",
   "c": "The guard-register identification number of every individual client",
   "d": "A list of the criminal offences for which an arrest must be made"},
  "§ 17(1) sentence 2 BewachV: the standing order must state that the guard has neither the status nor "
  "the powers of a police officer or any other public official. Sentence 3 additionally requires it to "
  "provide that weapons may be carried on duty only with the trader's consent and that every use must be "
  "reported without delay. Under § 17(2) BewachV a copy must be handed to the guard against a receipt "
  "before they first take up guarding duty. The insurance sum (§ 14 BewachV) and the register "
  "identification numbers (§ 18(1) BewachV, identity card) are dealt with elsewhere; and there is no duty "
  "to arrest - § 127(1) StPO confers a power, not an obligation.",
  )

Q("03", "oeffentliche_sicherheit",
  "§ 19 BewachV", 3, False, "d",
  "Ein Bewachungsunternehmen entwirft eine neue Dienstkleidung. Welche Vorgabe macht die "
  "Bewachungsverordnung dazu?",
  {"a": "Dienstkleidung ist für alle Wachpersonen in jedem Einsatz vorgeschrieben",
   "b": "Die Dienstkleidung muss in Schnitt und Farbe der Polizeiuniform des jeweiligen Landes "
        "entsprechen, damit sie erkennbar ist",
   "c": "Die Gestaltung der Dienstkleidung ist rechtlich vollständig frei",
   "d": "Sie muss sich deutlich von Uniformen der Streitkräfte und behördlicher Vollzugsorgane "
        "unterscheiden, und es dürfen keine Abzeichen verwendet werden, die Amtsabzeichen zum "
        "Verwechseln ähnlich sind"},
  "§ 19 Abs. 1 BewachV: bestimmt der Gewerbetreibende eine Dienstkleidung, so hat er dafür zu sorgen, "
  "„dass sie sich von Uniformen der Angehörigen von Streitkräften oder behördlichen Vollzugsorganen "
  "deutlich unterscheiden und dass keine Abzeichen verwendet werden, die Amtsabzeichen zum Verwechseln "
  "ähnlich sind“. Das ist die kleiderrechtliche Entsprechung zu § 34a Abs. 5 GewO: wer keine hoheitlichen "
  "Befugnisse hat, darf auch nicht so aussehen, als hätte er sie. (a) ist zu weit: nach § 19 Abs. 2 "
  "BewachV ist Dienstkleidung nur für Wachpersonen zwingend, die befriedetes Besitztum in Ausübung ihres "
  "Dienstes betreten sollen. (b) kehrt die Vorschrift ins Gegenteil um. (c) übersieht § 19 ganz.",
  "A guarding company is designing a new uniform. What does the Bewachungsverordnung require?",
  {"a": "A uniform is mandatory for every guard on every assignment",
   "b": "The uniform must match the cut and colour of the relevant state police uniform so that it is "
        "recognisable",
   "c": "The design of the uniform is legally entirely unrestricted",
   "d": "It must be clearly distinguishable from the uniforms of the armed forces and of public "
        "enforcement bodies, and no insignia confusingly similar to official insignia may be used"},
  "§ 19(1) BewachV: if the trader prescribes a uniform, they must ensure that it is clearly "
  "distinguishable from the uniforms of members of the armed forces or of public enforcement bodies and "
  "that no insignia confusingly similar to official insignia are used. This is the dress-code counterpart "
  "to § 34a(5) GewO: someone with no sovereign powers must not look as though they have them. (a) goes too "
  "far - under § 19(2) BewachV a uniform is mandatory only for guards who are to enter enclosed private "
  "property in the course of their duty. (b) inverts the rule. (c) ignores § 19 altogether.",
  )

Q("04", "oeffentliche_sicherheit",
  "§ 34a Abs. 1a Satz 1 Nr. 2 und Satz 2 GewO; § 6 BewachV", 5, True, "a",
  "Vier Wachpersonen sollen eingesetzt werden. Wer von ihnen benötigt nach § 34a Abs. 1a GewO zwingend "
  "die vor der Industrie- und Handelskammer abgelegte Sachkundeprüfung und nicht nur den "
  "Unterrichtungsnachweis?",
  {"a": "Die Wachperson, die als Ladendetektivin zum Schutz vor Ladendieben eingesetzt wird",
   "b": "Die Wachperson im Empfangsdienst einer Konzernzentrale",
   "c": "Die Wachperson im Objektschutz eines nicht öffentlich zugänglichen Betriebsgeländes",
   "d": "Die Wachperson, die bei einem zugangsgeschützten Stadionkonzert als einfache Ordnerin ohne "
        "Leitungsfunktion eingesetzt wird"},
  "§ 34a Abs. 1a Satz 2 GewO zählt die sachkundepflichtigen Tätigkeiten abschließend auf: "
  "1. Kontrollgänge im öffentlichen Verkehrsraum oder in Hausrechtsbereichen mit tatsächlich "
  "öffentlichem Verkehr, 2. Schutz vor Ladendieben, 3. Bewachungen im Einlassbereich von "
  "gastgewerblichen Diskotheken, 4. Bewachungen von Asyl-Aufnahmeeinrichtungen und "
  "Gemeinschaftsunterkünften „in leitender Funktion“, 5. Bewachungen von zugangsgeschützten "
  "Großveranstaltungen „in leitender Funktion“. (a) ist Nummer 2 und damit sachkundepflichtig. "
  "(b) und (c) stehen nicht auf der Liste: für sie genügt die Unterrichtung nach § 34a Abs. 1a Satz 1 "
  "Nr. 2 GewO, also 40 Unterrichtsstunden nach § 6 BewachV ohne Prüfung. (d) fällt unter Nummer 5, aber "
  "nur „in leitender Funktion“ - die einfache Ordnerin braucht die Prüfung gerade nicht. Merke: die "
  "Sachkundeprüfung tritt nach dem Wortlaut „zusätzlich zu den Anforderungen des Satzes 1 Nummer 1“ "
  "(Zuverlässigkeit) hinzu, nicht zu Nummer 2 - und § 8 Nr. 4 BewachV erklärt die "
  "Sachkundebescheinigung ausdrücklich zum Ersatz für den Unterrichtungsnachweis. Niemand braucht beides.",
  "Four guards are to be deployed. Which of them must, under § 34a(1a) GewO, hold the Sachkunde "
  "examination passed before the Chamber of Industry and Commerce, rather than merely the instruction "
  "certificate?",
  {"a": "The guard deployed as a store detective for protection against shoplifters",
   "b": "The guard on reception duty at a corporate headquarters",
   "c": "The guard on property protection at a business site that is not open to the public",
   "d": "The guard deployed as an ordinary steward, with no supervisory role, at a ticketed stadium "
        "concert"},
  "§ 34a(1a) sentence 2 GewO lists the activities requiring the Sachkunde examination exhaustively: "
  "1. patrols in public traffic space or in domiciliary areas with actual public traffic, 2. protection "
  "against shoplifters, 3. guarding at the entrance area of licensed discotheques, 4. guarding asylum "
  "reception facilities and shared accommodation 'in a supervisory role', 5. guarding access-controlled "
  "large events 'in a supervisory role'. (a) is number 2 and therefore requires the examination. (b) and "
  "(c) are not on the list: for them the instruction under § 34a(1a) sentence 1 no. 2 GewO suffices - 40 "
  "teaching hours under § 6 BewachV with no examination. (d) falls under number 5, but only 'in a "
  "supervisory role'; an ordinary steward specifically does not need the examination. Note the wording: "
  "the examination is required 'in addition to the requirements of sentence 1 number 1' (reliability), "
  "not number 2 - and § 8 no. 4 BewachV expressly treats the Sachkunde certificate as a substitute for the "
  "instruction certificate. Nobody needs both.",
  )

Q("05", "oeffentliche_sicherheit",
  "§ 18 Abs. 2 und 3 BewachV", 4, False, "b",
  "Für welche der folgenden Tätigkeiten schreibt § 18 Abs. 3 BewachV das sichtbare Tragen eines "
  "Schildes mit Namen oder Kennnummer und der Bezeichnung des Gewerbebetriebs gerade nicht vor?",
  {"a": "Kontrollgänge im öffentlichen Verkehrsraum",
   "b": "Schutz vor Ladendieben",
   "c": "Bewachung im Einlassbereich einer gastgewerblichen Diskothek",
   "d": "Bewachung einer zugangsgeschützten Großveranstaltung"},
  "§ 18 Abs. 3 Satz 1 BewachV verpflichtet zum sichtbaren Namens- oder Kennnummernschild jede Wachperson, "
  "die Tätigkeiten nach § 34a Abs. 1a Satz 2 „Nummer 1 und 3 bis 5“ ausübt. Nummer 2 - Schutz vor "
  "Ladendieben - ist bewusst ausgenommen: eine als solche erkennbare Ladendetektivin könnte ihre Aufgabe "
  "nicht erfüllen. Satz 2 erweitert die Pflicht für die Fälle der Nummern 4 und 5 auf Wachpersonen „in "
  "nicht leitender Funktion“, obwohl diese keine Sachkundeprüfung brauchen - Kennzeichnungspflicht und "
  "Qualifikationspflicht laufen also nicht parallel. Davon zu unterscheiden ist der Ausweis nach § 18 "
  "Abs. 1 und 2 BewachV: den muss jede Wachperson im Dienst mitführen und auf Verlangen vorzeigen, und er "
  "muss sich „deutlich von amtlichen Ausweisen“ unterscheiden.",
  "For which of the following activities does § 18(3) BewachV specifically NOT require a visibly worn "
  "badge showing a name or identification number and the name of the business?",
  {"a": "Patrols in public traffic space",
   "b": "Protection against shoplifters",
   "c": "Guarding at the entrance area of a licensed discotheque",
   "d": "Guarding an access-controlled large event"},
  "§ 18(3) sentence 1 BewachV requires a visible name or number badge of every guard carrying out "
  "activities under § 34a(1a) sentence 2 'numbers 1 and 3 to 5'. Number 2 - protection against "
  "shoplifters - is deliberately excluded: a store detective identifiable as such could not do the job. "
  "Sentence 2 extends the duty in the cases of numbers 4 and 5 to guards 'not in a supervisory role', even "
  "though those guards need no Sachkunde examination - so the badging duty and the qualification duty do "
  "not run in parallel. This is distinct from the identity card under § 18(1) and (2) BewachV, which every "
  "guard must carry on duty and show on demand, and which must be clearly distinguishable from official "
  "identity documents.",
  )

# ---------------------------------------------------------------------------
# 2. Datenschutzrecht (§ 7 Nr. 2 BewachV / Anlage 2 Nr. 2) -- 3 questions
# ---------------------------------------------------------------------------

Q("01", "datenschutz",
  "§ 4 Abs. 2 BDSG", 4, False, "c",
  "Ihr Auftraggeber betreibt eine Videoüberwachung im öffentlich zugänglichen Eingangsbereich eines "
  "Einkaufszentrums. Was verlangt § 4 Abs. 2 BDSG in Bezug auf die Kenntlichmachung?",
  {"a": "Es genügt, die Überwachung in der Hausordnung zu erwähnen",
   "b": "Ein Piktogramm allein reicht in jedem Fall aus, weitere Angaben sind nicht erforderlich",
   "c": "Der Umstand der Beobachtung sowie Name und Kontaktdaten des Verantwortlichen sind durch "
        "geeignete Maßnahmen zum frühestmöglichen Zeitpunkt erkennbar zu machen",
   "d": "Eine Kenntlichmachung ist entbehrlich, solange die Aufnahmen nicht gespeichert werden"},
  "§ 4 Abs. 2 BDSG: „Der Umstand der Beobachtung und der Name und die Kontaktdaten des Verantwortlichen "
  "sind durch geeignete Maßnahmen zum frühestmöglichen Zeitpunkt erkennbar zu machen.“ Es geht also um "
  "zwei Dinge zugleich - dass überwacht wird und wer dafür verantwortlich ist - und zwar so früh wie "
  "möglich, praktisch vor dem Betreten des überwachten Bereichs. Ein bloßer Hinweis in der Hausordnung "
  "(a) erreicht Passanten nicht rechtzeitig. Ein Kamerapiktogramm ohne Angabe des Verantwortlichen (b) "
  "erfüllt nur die halbe Anforderung. (d) ist falsch, weil bereits die Beobachtung eine Verarbeitung ist. "
  "Wichtig für die Praxis: die Wachperson bedient die Anlage regelmäßig nur; Verantwortlicher im "
  "datenschutzrechtlichen Sinne ist in aller Regel der Auftraggeber.",
  "Your client operates video surveillance in the publicly accessible entrance area of a shopping centre. "
  "What does § 4(2) BDSG require as regards making this recognisable?",
  {"a": "Mentioning the surveillance in the house rules is sufficient",
   "b": "A pictogram alone is always sufficient; no further details are needed",
   "c": "The fact of the monitoring and the name and contact details of the controller must be made "
        "recognisable by suitable means at the earliest possible time",
   "d": "No notice is needed as long as the footage is not stored"},
  "§ 4(2) BDSG requires that the fact of the monitoring and the name and contact details of the controller "
  "be made recognisable by suitable means at the earliest possible time. Two things at once, then - that "
  "monitoring takes place and who is responsible for it - and as early as possible, in practice before "
  "entering the monitored area. A mere note in the house rules (a) does not reach passers-by in time. A "
  "camera pictogram without identifying the controller (b) meets only half the requirement. (d) is wrong "
  "because the observation is itself processing. Practical point: the guard usually only operates the "
  "system; the controller in data-protection terms is normally the client.",
  )

Q("02", "datenschutz",
  "§ 4 Abs. 5 BDSG", 3, False, "a",
  "Wann sind durch Videoüberwachung erhobene Daten nach § 4 Abs. 5 BDSG zu löschen?",
  {"a": "Unverzüglich, wenn sie zur Erreichung des Zwecks nicht mehr erforderlich sind oder "
        "schutzwürdige Interessen der betroffenen Personen einer weiteren Speicherung entgegenstehen",
   "b": "Immer genau nach 72 Stunden, unabhängig vom Zweck",
   "c": "Erst nach Ablauf der dreijährigen Aufbewahrungsfrist des § 21 Abs. 4 BewachV",
   "d": "Nur auf ausdrücklichen Antrag einer betroffenen Person"},
  "§ 4 Abs. 5 BDSG: „Die Daten sind unverzüglich zu löschen, wenn sie zur Erreichung des Zwecks nicht "
  "mehr erforderlich sind oder schutzwürdige Interessen der betroffenen Personen einer weiteren "
  "Speicherung entgegenstehen.“ Es gibt also keine im Gesetz genannte Regelfrist; maßgeblich ist allein "
  "die Erforderlichkeit für den konkret festgelegten Zweck. Die häufig genannten 48 oder 72 Stunden sind "
  "Aufsichtspraxis und Faustregel, nicht Gesetzestext - deshalb ist (b) falsch. (c) verwechselt die "
  "datenschutzrechtliche Löschpflicht mit der gewerberechtlichen Aufbewahrungspflicht für "
  "Geschäftsunterlagen nach § 21 Abs. 4 BewachV; das sind verschiedene Regelungskreise. (d) ist falsch, "
  "weil die Löschpflicht von Amts wegen besteht und nicht von einem Antrag abhängt.",
  "When must data collected by video surveillance be erased under § 4(5) BDSG?",
  {"a": "Without undue delay, once they are no longer necessary to achieve the purpose or where "
        "interests of the data subjects worthy of protection preclude further storage",
   "b": "Always exactly after 72 hours, regardless of purpose",
   "c": "Only after the three-year retention period of § 21(4) BewachV has expired",
   "d": "Only on an express request by a data subject"},
  "§ 4(5) BDSG requires erasure without undue delay once the data are no longer necessary to achieve the "
  "purpose, or where interests of the data subjects worthy of protection preclude further storage. There "
  "is therefore no standard period in the statute; what matters is necessity for the specifically defined "
  "purpose. The frequently cited 48 or 72 hours are supervisory practice and a rule of thumb, not statutory "
  "text - hence (b) is wrong. (c) confuses the data-protection erasure duty with the trade-law retention "
  "duty for business records under § 21(4) BewachV; these are separate regimes. (d) is wrong because the "
  "erasure duty applies of its own motion and does not depend on a request.",
  )

Q("03", "datenschutz",
  "§ 4 Abs. 3 Satz 3 BDSG", 4, False, "d",
  "Der Auftraggeber möchte Videoaufnahmen, die zur Wahrnehmung des Hausrechts erhoben wurden, "
  "nachträglich für eine Auswertung der Kundenlaufwege im Marketing nutzen. Wie ist das nach § 4 Abs. 3 "
  "BDSG zu beurteilen?",
  {"a": "Zulässig, weil die Daten ohnehin bereits rechtmäßig erhoben wurden",
   "b": "Zulässig, sofern die Aufnahmen vorher anonymisiert wurden - eine Rechtsgrundlage ist dann nicht "
        "mehr nötig",
   "c": "Zulässig, wenn die Wachperson die Auswertung vornimmt und nicht das Marketing selbst",
   "d": "Unzulässig - eine Weiterverarbeitung für einen anderen Zweck ist nach § 4 Abs. 3 Satz 3 BDSG nur "
        "zulässig, soweit sie zur Abwehr von Gefahren für die staatliche und öffentliche Sicherheit sowie "
        "zur Verfolgung von Straftaten erforderlich ist"},
  "§ 4 Abs. 3 Satz 3 BDSG begrenzt die Zweckänderung eng: „Für einen anderen Zweck dürfen sie nur "
  "weiterverarbeitet werden, soweit dies zur Abwehr von Gefahren für die staatliche und öffentliche "
  "Sicherheit sowie zur Verfolgung von Straftaten erforderlich ist.“ Marketing-Analysen sind davon "
  "ersichtlich nicht gedeckt. (a) verkennt, dass die Rechtmäßigkeit der Erhebung nichts über die "
  "Zulässigkeit einer späteren Zweckänderung sagt - das ist der Kern des Grundsatzes der Zweckbindung. "
  "(b) trifft nur zu, wenn tatsächlich kein Personenbezug mehr herstellbar ist, was bei Laufwegen "
  "einzelner Kunden gerade fraglich ist; als pauschale Aussage ist sie falsch. (c) ist irrelevant: es "
  "kommt auf den Zweck an, nicht auf die ausführende Person.",
  "The client wants to use video footage collected for exercising the domiciliary right for a subsequent "
  "marketing analysis of customer movement patterns. How does § 4(3) BDSG treat this?",
  {"a": "Permitted, because the data were lawfully collected in any event",
   "b": "Permitted provided the footage is anonymised first - no legal basis is then needed",
   "c": "Permitted if the guard, rather than the marketing department, carries out the analysis",
   "d": "Not permitted - under § 4(3) sentence 3 BDSG further processing for another purpose is allowed "
        "only in so far as it is necessary to avert dangers to state and public security and to prosecute "
        "criminal offences"},
  "§ 4(3) sentence 3 BDSG narrowly limits any change of purpose: data may be further processed for another "
  "purpose only in so far as this is necessary to avert dangers to state and public security and to "
  "prosecute criminal offences. Marketing analysis is plainly not covered. (a) misses the point that the "
  "lawfulness of collection says nothing about the admissibility of a later change of purpose - that is the "
  "core of purpose limitation. (b) holds only if a personal reference genuinely can no longer be "
  "established, which is precisely doubtful for individual customers' movement paths; as a blanket "
  "statement it is wrong. (c) is irrelevant: what matters is the purpose, not who carries out the work.",
  )

# ---------------------------------------------------------------------------
# 3. Bürgerliches Gesetzbuch (§ 7 Nr. 3 BewachV / Anlage 2 Nr. 3) -- 5 questions
# ---------------------------------------------------------------------------

Q("01", "bgb",
  "§ 227 BGB; § 32 StGB", 5, True, "b",
  "Ein Angreifer schlägt auf Sie ein, lässt dann von Ihnen ab und läuft davon. Sie holen ihn nach "
  "wenigen Metern ein und schlagen zurück. Wie ist das zu bewerten?",
  {"a": "Als Notwehr, weil der Angriff kurz zuvor stattgefunden hat",
   "b": "Nicht als Notwehr - der Angriff war nicht mehr gegenwärtig; Ihre Handlung kann eine strafbare "
        "Körperverletzung und eine Schadensersatzpflicht auslösen",
   "c": "Als Selbsthilfe nach § 229 BGB, weil Sie Ihren Anspruch sichern",
   "d": "Als Nothilfe, weil Sie künftige Angriffe auf Dritte verhindern"},
  "§ 227 Abs. 2 BGB definiert Notwehr als „diejenige Verteidigung, welche erforderlich ist, um einen "
  "gegenwärtigen rechtswidrigen Angriff von sich oder einem anderen abzuwenden“; § 32 Abs. 2 StGB ist "
  "im Strafrecht wortgleich aufgebaut. Entscheidend ist das Merkmal „gegenwärtig“: der Angriff muss "
  "unmittelbar bevorstehen, gerade stattfinden oder noch andauern. Wer flieht, greift nicht mehr an - die "
  "Verteidigungslage endet, und was danach kommt, ist Vergeltung, nicht Notwehr. (c) ist falsch, weil "
  "§ 229 BGB die Sicherung eines zivilrechtlichen Anspruchs voraussetzt, nicht eine Bestrafung. (d) ist "
  "falsch, weil Nothilfe ebenfalls einen gegenwärtigen Angriff verlangt, hier auf einen Dritten - eine "
  "bloße Befürchtung genügt nicht. Für Wachpersonen ist das die praktisch wichtigste Grenze überhaupt, "
  "weil § 34a Abs. 5 GewO ihnen genau diese Jedermannsrechte und nichts darüber hinaus zuweist.",
  "An attacker hits you, then breaks off and runs away. You catch up with them after a few metres and hit "
  "back. How is this assessed?",
  {"a": "As self-defence, because the attack took place moments earlier",
   "b": "Not as self-defence - the attack was no longer present; your act may constitute a criminal "
        "assault and give rise to a liability in damages",
   "c": "As self-help under § 229 BGB, because you are securing your claim",
   "d": "As defence of another, because you are preventing future attacks on third parties"},
  "§ 227(2) BGB defines self-defence as the defence necessary to avert a present unlawful attack on "
  "oneself or another; § 32(2) StGB is built identically in criminal law. The decisive element is "
  "'present': the attack must be imminent, occurring, or still continuing. Someone fleeing is no longer "
  "attacking - the defensive situation ends, and what follows is retaliation, not self-defence. (c) is "
  "wrong because § 229 BGB presupposes securing a civil-law claim, not punishment. (d) is wrong because "
  "defence of another likewise requires a present attack, here on a third party; a mere apprehension is "
  "not enough. For guards this is the single most important practical limit, because § 34a(5) GewO assigns "
  "them exactly these general rights and nothing beyond them.",
  )

Q("02", "bgb",
  "§§ 229, 230 BGB", 5, True, "c",
  "Sie nehmen eine Person nach § 229 BGB im Wege der Selbsthilfe fest, weil sie der Flucht verdächtig "
  "ist und obrigkeitliche Hilfe nicht rechtzeitig zu erlangen war. Welche Folgepflicht sieht das BGB "
  "vor?",
  {"a": "Sie dürfen die Person bis zu 24 Stunden festhalten und dann selbst entscheiden",
   "b": "Sie müssen die Person zunächst zum Betriebssitz Ihres Arbeitgebers bringen",
   "c": "Sofern die Person nicht wieder in Freiheit gesetzt wird, ist der persönliche Sicherheitsarrest "
        "beim zuständigen Amtsgericht zu beantragen und die Person unverzüglich dem Gericht vorzuführen",
   "d": "Es bestehen keine weiteren Pflichten, sobald die Polizei verständigt wurde"},
  "§ 230 Abs. 3 BGB: „Im Falle der Festnahme des Verpflichteten ist, sofern er nicht wieder in Freiheit "
  "gesetzt wird, der persönliche Sicherheitsarrest bei dem Amtsgericht zu beantragen, in dessen Bezirk "
  "die Festnahme erfolgt ist; der Verpflichtete ist unverzüglich dem Gericht vorzuführen.“ Abs. 4 "
  "ergänzt: wird der Arrestantrag verzögert oder abgelehnt, hat die Freilassung unverzüglich zu erfolgen. "
  "Abs. 1 stellt ohnehin klar, dass die Selbsthilfe „nicht weiter gehen (darf), als zur Abwendung der "
  "Gefahr erforderlich ist“. Das längere Festhalten in (a) wäre Freiheitsberaubung nach § 239 StGB. (b) "
  "hat keine Grundlage. (d) verwechselt die zivilrechtliche Selbsthilfe des § 229 BGB mit der "
  "strafprozessualen Festnahme nach § 127 Abs. 1 StPO - zwei verschiedene Institute mit verschiedenen "
  "Voraussetzungen und Folgen.",
  "You detain a person by way of self-help under § 229 BGB because they are suspected of absconding and "
  "official assistance could not be obtained in time. What follow-up duty does the BGB impose?",
  {"a": "You may hold the person for up to 24 hours and then decide yourself",
   "b": "You must first take the person to your employer's business premises",
   "c": "Unless the person is released, personal security arrest must be applied for at the competent "
        "local court and the person must be brought before the court without undue delay",
   "d": "There are no further duties once the police have been notified"},
  "§ 230(3) BGB: in the case of detention of the obligor, unless they are released, personal security "
  "arrest must be applied for at the local court in whose district the detention took place, and the "
  "obligor must be brought before the court without undue delay. Subsection (4) adds that if the "
  "application is delayed or refused, release must follow without undue delay. Subsection (1) makes clear "
  "in any event that self-help may not go further than is necessary to avert the danger. Holding the "
  "person longer, as in (a), would be unlawful deprivation of liberty under § 239 StGB. (b) has no basis. "
  "(d) confuses civil-law self-help under § 229 BGB with the criminal-procedure arrest under § 127(1) "
  "StPO - two different institutions with different preconditions and consequences.",
  )

Q("03", "bgb",
  "§§ 855, 859 Abs. 2, 860 BGB", 4, False, "a",
  "Ein Dieb entreißt auf dem von Ihnen bewachten Betriebsgelände einem Mitarbeiter ein Notebook und "
  "läuft los. Sie verfolgen ihn und nehmen ihm das Gerät auf frischer Tat wieder ab. Welche "
  "zivilrechtliche Einordnung trifft zu?",
  {"a": "Besitzkehr nach § 859 Abs. 2 BGB, die Ihnen als Besitzdiener nach § 860 BGB in Verbindung mit "
        "§ 855 BGB zusteht",
   "b": "Eine hoheitliche Sicherstellung, weil Sie das Hausrecht ausüben",
   "c": "Ein Zurückbehaltungsrecht, weil das Notebook dem Auftraggeber gehört",
   "d": "Unzulässige verbotene Eigenmacht Ihrerseits nach § 858 BGB"},
  "§ 859 Abs. 2 BGB: wird eine bewegliche Sache dem Besitzer mittels verbotener Eigenmacht weggenommen, "
  "„so darf er sie dem auf frischer Tat betroffenen oder verfolgten Täter mit Gewalt wieder abnehmen“. "
  "§ 860 BGB erstreckt dieses Recht ausdrücklich auf denjenigen, „welcher die tatsächliche Gewalt nach "
  "§ 855 für den Besitzer ausübt“ - also den Besitzdiener, und genau das ist die Wachperson im fremden "
  "Objekt. Zeitlich ist das Recht eng: „auf frischer Tat betroffen oder verfolgt“, ohne Unterbrechung "
  "der Nacheile. (b) ist falsch, weil private Bewachung keine hoheitlichen Befugnisse hat (§ 34a Abs. 5 "
  "GewO). (c) verkennt, dass ein Zurückbehaltungsrecht ein bestehendes Schuldverhältnis voraussetzt. (d) "
  "kehrt die Rollen um: verbotene Eigenmacht nach § 858 BGB begeht der Dieb, nicht der Besitzdiener, der "
  "sie abwehrt.",
  "On the business site you are guarding, a thief snatches a laptop from an employee and runs off. You "
  "pursue and take the device back from them in the act. Which civil-law classification applies?",
  {"a": "Repossession under § 859(2) BGB, available to you as a servant in possession under § 860 BGB in "
        "conjunction with § 855 BGB",
   "b": "A sovereign seizure, because you are exercising the domiciliary right",
   "c": "A right of retention, because the laptop belongs to the client",
   "d": "Inadmissible unlawful interference with possession on your part under § 858 BGB"},
  "§ 859(2) BGB: where a movable thing is taken from the possessor by unlawful interference, the possessor "
  "may take it back by force from the perpetrator caught or pursued in the act. § 860 BGB expressly extends "
  "this right to a person who exercises actual control for the possessor under § 855 BGB - the servant in "
  "possession, which is exactly what a guard on someone else's site is. The right is narrow in time: caught "
  "or pursued in the act, with the pursuit uninterrupted. (b) is wrong because private guarding has no "
  "sovereign powers (§ 34a(5) GewO). (c) misunderstands that a right of retention presupposes an existing "
  "obligation. (d) reverses the roles: the unlawful interference under § 858 BGB is committed by the thief, "
  "not by the servant in possession repelling it.",
  )

Q("04", "bgb",
  "§ 858 BGB", 3, False, "d",
  "Was ist verbotene Eigenmacht im Sinne des § 858 Abs. 1 BGB?",
  {"a": "Jede Handlung, die dem Eigentümer wirtschaftlich schadet",
   "b": "Die Ausübung eines Rechts, die nur den Zweck haben kann, einem anderen Schaden zuzufügen",
   "c": "Jede Sachbeschädigung an fremdem Eigentum",
   "d": "Wer dem Besitzer ohne dessen Willen den Besitz entzieht oder ihn im Besitz stört, ohne dass das "
        "Gesetz dies gestattet"},
  "§ 858 Abs. 1 BGB: „Wer dem Besitzer ohne dessen Willen den Besitz entzieht oder ihn im Besitz stört, "
  "handelt, sofern nicht das Gesetz die Entziehung oder die Störung gestattet, widerrechtlich (verbotene "
  "Eigenmacht).“ Anknüpfungspunkt ist also der Besitz, nicht das Eigentum - deshalb ist (a) falsch, und "
  "deshalb kann auch der Nichteigentümer geschützt sein. Wichtig für die Praxis: die verbotene Eigenmacht "
  "ist der Auslöser für die Besitzwehr und die Besitzkehr nach § 859 BGB, die der Wachperson als "
  "Besitzdiener über § 860 BGB zustehen. (b) beschreibt das Schikaneverbot des § 226 BGB. (c) beschreibt "
  "die Sachbeschädigung, die strafrechtlich in § 303 StGB steht; sie kann verbotene Eigenmacht sein, ist "
  "es aber nicht zwingend.",
  "What is unlawful interference with possession within the meaning of § 858(1) BGB?",
  {"a": "Any act that causes the owner economic harm",
   "b": "The exercise of a right which can only have the purpose of causing harm to another",
   "c": "Any damage to another's property",
   "d": "Depriving the possessor of possession against their will, or disturbing them in their "
        "possession, where the law does not permit this"},
  "§ 858(1) BGB: a person who deprives the possessor of possession against their will, or disturbs them in "
  "their possession, acts unlawfully unless the law permits the deprivation or disturbance (unlawful "
  "interference with possession). The connecting factor is therefore possession, not ownership - which is "
  "why (a) is wrong and why a non-owner can also be protected. Practically important: unlawful interference "
  "is the trigger for the possessory defence and repossession rights under § 859 BGB, which are available "
  "to a guard as servant in possession via § 860 BGB. (b) describes the prohibition of chicanery in § 226 "
  "BGB. (c) describes criminal damage, which appears in § 303 StGB; it can amount to unlawful interference "
  "but need not.",
  )

Q("05", "bgb",
  "§ 823 Abs. 1 BGB; § 34a Abs. 5 Satz 2 GewO", 4, True, "b",
  "Sie setzen bei einer Auseinandersetzung deutlich mehr Kraft ein, als zur Abwehr nötig war, und "
  "verletzen die andere Person. Welche zivilrechtliche Folge kommt in Betracht?",
  {"a": "Keine - für Handlungen im Dienst haftet ausschließlich der Auftraggeber",
   "b": "Eine eigene Schadensersatzpflicht nach § 823 Abs. 1 BGB, weil Sie Körper und Gesundheit eines "
        "anderen widerrechtlich verletzt haben",
   "c": "Keine - die Haftpflichtversicherung nach § 14 BewachV schließt eine persönliche Haftung aus",
   "d": "Nur eine Ordnungswidrigkeit nach § 22 BewachV"},
  "§ 823 Abs. 1 BGB: „Wer vorsätzlich oder fahrlässig das Leben, den Körper, die Gesundheit, die "
  "Freiheit, das Eigentum oder ein sonstiges Recht eines anderen widerrechtlich verletzt, ist dem anderen "
  "zum Ersatz des daraus entstehenden Schadens verpflichtet.“ Wird die Grenze der Erforderlichkeit "
  "überschritten, entfällt die Rechtfertigung (§ 227 Abs. 2 BGB, § 32 Abs. 2 StGB) und die Handlung ist "
  "widerrechtlich - § 34a Abs. 5 Satz 2 GewO schreibt genau deshalb ausdrücklich vor, dass „der "
  "Grundsatz der Erforderlichkeit zu beachten“ ist. Die Haftung des Arbeitgebers nach § 831 BGB und die "
  "Haftpflichtversicherung nach § 14 BewachV treten daneben, sie ersetzen die eigene Haftung nicht - (a) "
  "und (c) sind daher falsch. (d) verkennt, dass § 22 BewachV nur bestimmte Verstöße gegen die BewachV "
  "erfasst, nicht die Körperverletzung; strafrechtlich käme zusätzlich § 223 StGB in Betracht.",
  "In an altercation you use considerably more force than was necessary for defence, and injure the other "
  "person. What civil-law consequence can arise?",
  {"a": "None - the client alone is liable for acts performed on duty",
   "b": "Your own liability in damages under § 823(1) BGB, because you unlawfully injured another "
        "person's body and health",
   "c": "None - the liability insurance under § 14 BewachV excludes personal liability",
   "d": "Only an administrative offence under § 22 BewachV"},
  "§ 823(1) BGB: a person who intentionally or negligently unlawfully injures the life, body, health, "
  "freedom, property or another right of another person is liable to compensate the resulting damage. If "
  "the limit of necessity is exceeded, the justification falls away (§ 227(2) BGB, § 32(2) StGB) and the "
  "act is unlawful - which is precisely why § 34a(5) sentence 2 GewO expressly prescribes that the "
  "principle of necessity must be observed. The employer's liability under § 831 BGB and the liability "
  "insurance under § 14 BewachV sit alongside this; they do not replace personal liability, so (a) and (c) "
  "are wrong. (d) misses that § 22 BewachV covers only certain breaches of the BewachV, not bodily injury; "
  "in criminal law § 223 StGB would additionally be in play.",
  )

# ---------------------------------------------------------------------------
# 4. Straf- und Verfahrensrecht, Umgang mit Waffen
#    (§ 7 Nr. 4 BewachV / Anlage 2 Nr. 4) -- 6 questions
# ---------------------------------------------------------------------------

Q("01", "strafrecht_waffen",
  "§ 127 Abs. 1 Satz 1 StPO", 5, True, "c",
  "Unter welchen Voraussetzungen darf jedermann - und damit auch eine Wachperson - eine Person nach "
  "§ 127 Abs. 1 Satz 1 StPO vorläufig festnehmen?",
  {"a": "Immer, wenn der Verdacht einer Straftat besteht",
   "b": "Nur bei Verbrechen im Sinne des § 12 Abs. 1 StGB",
   "c": "Wenn die Person auf frischer Tat betroffen oder verfolgt wird und sie entweder der Flucht "
        "verdächtig ist oder ihre Identität nicht sofort festgestellt werden kann",
   "d": "Wenn der Auftraggeber die Festnahme im Bewachungsvertrag angeordnet hat"},
  "§ 127 Abs. 1 Satz 1 StPO: „Wird jemand auf frischer Tat betroffen oder verfolgt, so ist, wenn er der "
  "Flucht verdächtig ist oder seine Identität nicht sofort festgestellt werden kann, jedermann befugt, "
  "ihn auch ohne richterliche Anordnung vorläufig festzunehmen.“ Es müssen also zwei Bedingungen "
  "zusammentreffen: die Tatnähe (auf frischer Tat betroffen oder verfolgt) und einer der beiden "
  "Festnahmegründe. Ein bloßer Verdacht ohne Tatnähe genügt nicht - (a) ist falsch. Eine Beschränkung "
  "auf Verbrechen enthält die Vorschrift nicht; § 127 Abs. 3 StPO erlaubt die Festnahme sogar bei "
  "Antragsdelikten, bevor ein Antrag gestellt ist - (b) ist falsch. (d) ist falsch, weil eine vertragliche "
  "Anordnung keine strafprozessuale Befugnis begründet. Wichtig: § 127 StPO ist eine Befugnis, keine "
  "Pflicht, und sie deckt nur die Festnahme selbst, nicht Durchsuchung oder Vernehmung.",
  "Under what conditions may anyone - and therefore also a guard - provisionally arrest a person under "
  "§ 127(1) sentence 1 StPO?",
  {"a": "Whenever there is a suspicion of a criminal offence",
   "b": "Only in the case of serious offences within the meaning of § 12(1) StGB",
   "c": "Where the person is caught or pursued in the act and is either suspected of absconding or their "
        "identity cannot be established immediately",
   "d": "Where the client has directed the arrest in the guarding contract"},
  "§ 127(1) sentence 1 StPO: if someone is caught or pursued in the act, then, where they are suspected of "
  "absconding or their identity cannot be established immediately, anyone is entitled to arrest them "
  "provisionally even without a judicial order. Two conditions must therefore coincide: proximity to the "
  "act (caught or pursued in the act) and one of the two grounds for arrest. Mere suspicion without "
  "proximity is not enough, so (a) is wrong. The provision contains no restriction to serious offences; "
  "§ 127(3) StPO even permits arrest for offences requiring a complaint before any complaint has been "
  "filed, so (b) is wrong. (d) is wrong because a contractual instruction cannot create a power under "
  "criminal procedure. Note: § 127 StPO confers a power, not a duty, and it covers only the arrest itself, "
  "not a search or an interrogation.",
  )

Q("02", "strafrecht_waffen",
  "§ 239 StGB", 5, True, "a",
  "Sie halten eine Person nach einer vermeintlichen Ladendiebstahlsbeobachtung im Büro fest, obwohl sich "
  "der Verdacht schon nach wenigen Minuten als unbegründet erwiesen hat, und lassen sie erst nach einer "
  "Stunde gehen. Welcher Straftatbestand kommt in Betracht?",
  {"a": "Freiheitsberaubung nach § 239 StGB, deren Versuch nach § 239 Abs. 2 StGB ebenfalls strafbar ist",
   "b": "Keiner, weil ein Anfangsverdacht bestanden hat",
   "c": "Nur Nötigung nach § 240 StGB, weil kein Einsperren vorlag",
   "d": "Keiner, weil das Hausrecht des Auftraggebers das Festhalten deckt"},
  "§ 239 Abs. 1 StGB: „Wer einen Menschen einsperrt oder auf andere Weise der Freiheit beraubt, wird mit "
  "Freiheitsstrafe bis zu fünf Jahren oder mit Geldstrafe bestraft.“ Abs. 2 stellt den Versuch unter "
  "Strafe. „Auf andere Weise“ erfasst gerade auch das Festhalten ohne Einsperren, weshalb (c) zu kurz "
  "greift. Die Rechtfertigung über § 127 Abs. 1 StPO entfällt, sobald deren Voraussetzungen nicht mehr "
  "vorliegen - ein zunächst bestehender Verdacht trägt das Festhalten nicht weiter, wenn er sich erledigt "
  "hat; (b) ist daher falsch. (d) ist falsch, weil das Hausrecht zum Verweisen berechtigt, nicht zum "
  "Festhalten. Bei längerer Dauer drohen zudem die Qualifikationen des § 239 Abs. 3 StGB.",
  "You detain a person in the office after a supposed observation of shoplifting, even though the "
  "suspicion proved unfounded within a few minutes, and let them go only after an hour. Which criminal "
  "offence is in play?",
  {"a": "Unlawful deprivation of liberty under § 239 StGB, the attempt of which is also punishable under "
        "§ 239(2) StGB",
   "b": "None, because there was an initial suspicion",
   "c": "Only coercion under § 240 StGB, because there was no locking up",
   "d": "None, because the client's domiciliary right covers the detention"},
  "§ 239(1) StGB: whoever locks up a person or otherwise deprives them of their liberty is liable to "
  "imprisonment of up to five years or a fine. Subsection (2) makes the attempt punishable. 'Otherwise' "
  "expressly covers holding someone without locking them up, which is why (c) falls short. Justification "
  "via § 127(1) StPO falls away as soon as its conditions cease to be met - an initially existing suspicion "
  "does not carry the detention further once it has been dispelled, so (b) is wrong. (d) is wrong because "
  "the domiciliary right permits ejection, not detention. With longer durations the aggravated forms in "
  "§ 239(3) StGB also come into play.",
  )

Q("03", "strafrecht_waffen",
  "§ 265a Abs. 1 StGB", 3, False, "b",
  "Ein Besucher verschafft sich ohne Ticket Zutritt zu einer kostenpflichtigen Veranstaltung, indem er "
  "sich an der Kontrolle vorbeidrängt, in der Absicht, das Entgelt nicht zu zahlen. Welcher "
  "Straftatbestand ist einschlägig?",
  {"a": "Diebstahl nach § 242 StGB",
   "b": "Erschleichen von Leistungen nach § 265a Abs. 1 StGB",
   "c": "Betrug nach § 263 StGB in jedem Fall",
   "d": "Sachbeschädigung nach § 303 StGB"},
  "§ 265a Abs. 1 StGB erfasst ausdrücklich, wer „den Zutritt zu einer Veranstaltung oder einer "
  "Einrichtung in der Absicht erschleicht, das Entgelt nicht zu entrichten“, mit Freiheitsstrafe bis zu "
  "einem Jahr oder Geldstrafe, „wenn die Tat nicht in anderen Vorschriften mit schwererer Strafe bedroht "
  "ist“. Der Versuch ist nach Abs. 2 strafbar. (a) passt nicht, weil § 242 StGB die Wegnahme einer "
  "fremden beweglichen Sache voraussetzt - der Zutritt ist keine Sache. (c) passt nur, wenn tatsächlich "
  "durch Täuschung ein Irrtum erregt wurde, etwa beim Vorzeigen einer Fälschung; das bloße Vorbeidrängen "
  "täuscht niemanden - „in jedem Fall“ ist deshalb falsch. (d) liegt neben der Sache, solange nichts "
  "beschädigt wird.",
  "A visitor gains entry to a paid event without a ticket by pushing past the check, intending not to pay "
  "the admission fee. Which offence applies?",
  {"a": "Theft under § 242 StGB",
   "b": "Obtaining services by deception under § 265a(1) StGB",
   "c": "Fraud under § 263 StGB in every case",
   "d": "Criminal damage under § 303 StGB"},
  "§ 265a(1) StGB expressly covers a person who surreptitiously obtains entry to an event or a facility "
  "intending not to pay the fee, with imprisonment of up to one year or a fine, where the act is not "
  "punishable more severely under other provisions. The attempt is punishable under subsection (2). (a) "
  "does not fit because § 242 StGB requires the taking of another's movable thing - entry is not a thing. "
  "(c) fits only where a deception actually caused an error, for example by presenting a forgery; merely "
  "pushing past deceives no one, so 'in every case' is wrong. (d) is beside the point as long as nothing "
  "is damaged.",
  )

Q("04", "strafrecht_waffen",
  "§ 252 StGB; § 249 StGB; § 12 Abs. 1 StGB", 5, True, "d",
  "Sie stellen einen Ladendieb unmittelbar nach der Tat. Er stößt Sie kräftig weg, um die gestohlene "
  "Ware behalten zu können. Wie ändert sich die strafrechtliche Bewertung seiner Tat?",
  {"a": "Sie ändert sich nicht; es bleibt beim Diebstahl nach § 242 StGB",
   "b": "Es liegt zusätzlich nur eine Ordnungswidrigkeit vor",
   "c": "Der Diebstahl entfällt, es bleibt allein die Körperverletzung",
   "d": "Es liegt räuberischer Diebstahl nach § 252 StGB vor; er ist gleich einem Räuber zu bestrafen, "
        "also nach dem Strafrahmen des § 249 StGB"},
  "§ 252 StGB: „Wer, bei einem Diebstahl auf frischer Tat betroffen, gegen eine Person Gewalt verübt "
  "oder Drohungen mit gegenwärtiger Gefahr für Leib oder Leben anwendet, um sich im Besitz des "
  "gestohlenen Gutes zu erhalten, ist gleich einem Räuber zu bestrafen.“ Der Verweis führt zu § 249 "
  "StGB - Freiheitsstrafe nicht unter einem Jahr, also ein Verbrechen im Sinne des § 12 Abs. 1 StGB. Das "
  "ist der Grund, weshalb die Situation „Zugriff nach dem Kassenbereich“ für Wachpersonen so heikel "
  "ist: die Reaktion des Täters kann die Tat von einem Vergehen zu einem Verbrechen hochstufen, und die "
  "Eigensicherung hat entsprechend Vorrang. (a) übersieht den Qualifikationssprung, (b) verkennt den "
  "Unterschied zwischen Straftat und Ordnungswidrigkeit, (c) ist falsch, weil der Diebstahl nicht "
  "entfällt, sondern gerade Anknüpfungspunkt des § 252 StGB ist.",
  "You confront a shoplifter immediately after the act. He shoves you hard in order to keep the stolen "
  "goods. How does the criminal assessment of his act change?",
  {"a": "It does not change; it remains theft under § 242 StGB",
   "b": "There is additionally only an administrative offence",
   "c": "The theft falls away and only the bodily injury remains",
   "d": "It becomes theft with violence under § 252 StGB; he is to be punished as a robber, that is under "
        "the sentencing range of § 249 StGB"},
  "§ 252 StGB: whoever, caught in the act of theft, uses force against a person or threats of present "
  "danger to life or limb in order to keep possession of the stolen goods is to be punished as a robber. "
  "The cross-reference leads to § 249 StGB - imprisonment of not less than one year, hence a serious "
  "offence within the meaning of § 12(1) StGB. This is why the 'intervention past the checkout' situation "
  "is so delicate for guards: the offender's reaction can escalate the act from a lesser offence to a "
  "serious one, and self-protection accordingly takes priority. (a) misses the escalation, (b) confuses a "
  "criminal offence with an administrative one, (c) is wrong because the theft does not fall away but is "
  "precisely the connecting factor for § 252 StGB.",
  )

Q("05", "strafrecht_waffen",
  "§ 42a WaffG; § 17 Abs. 1 Satz 3 BewachV", 4, True, "c",
  "Eine Wachperson möchte im Dienst ein feststehendes Messer mit 15 cm Klingenlänge führen. Was gilt "
  "nach § 42a WaffG?",
  {"a": "Das Führen ist ohne Weiteres erlaubt, weil es sich nicht um eine Schusswaffe handelt",
   "b": "Das Führen ist ausnahmslos verboten",
   "c": "Das Führen ist grundsätzlich verboten, das Verbot gilt aber nicht bei einem berechtigten "
        "Interesse, das insbesondere bei einem Zusammenhang mit der Berufsausübung vorliegen kann",
   "d": "Es kommt allein auf die Zustimmung des Auftraggebers an"},
  "§ 42a Abs. 1 Nr. 3 WaffG verbietet das Führen von „Messern mit einhändig feststellbarer Klinge "
  "(Einhandmesser) oder feststehende(n) Messer(n) mit einer Klingenlänge über 12 cm“. Nach Abs. 2 Satz 1 "
  "Nr. 3 gilt das Verbot nicht für die Gegenstände nach Abs. 1 Nr. 2 und 3, „sofern ein berechtigtes "
  "Interesse vorliegt“, und Abs. 3 nennt als Beispiel ausdrücklich, dass das Führen „im Zusammenhang "
  "mit der Berufsausübung erfolgt“. Ob das im Einzelfall trägt, ist eine Frage der konkreten Tätigkeit "
  "und keine pauschale Freistellung - deshalb ist (a) zu weit und (b) zu eng. Wichtig: die Ausnahme des "
  "Abs. 2 Satz 1 Nr. 3 gilt gerade nicht für Anscheinswaffen nach Abs. 1 Nr. 1. (d) ist falsch: die "
  "Zustimmung des Gewerbetreibenden ist nach § 17 Abs. 1 Satz 3 BewachV zusätzlich nötig, ersetzt aber "
  "das waffenrechtliche Erfordernis nicht.",
  "A guard wants to carry a fixed-blade knife with a 15 cm blade while on duty. What does § 42a WaffG "
  "provide?",
  {"a": "Carrying it is permitted without more, because it is not a firearm",
   "b": "Carrying it is prohibited without exception",
   "c": "Carrying it is prohibited in principle, but the prohibition does not apply where there is a "
        "legitimate interest, which may in particular exist in connection with the exercise of one's "
        "occupation",
   "d": "All that matters is the client's consent"},
  "§ 42a(1) no. 3 WaffG prohibits carrying knives with a blade lockable one-handed, or fixed-blade knives "
  "with a blade longer than 12 cm. Under subsection (2) sentence 1 no. 3 the prohibition does not apply to "
  "the objects in subsection (1) nos. 2 and 3 where a legitimate interest exists, and subsection (3) "
  "expressly gives as an example that the carrying takes place in connection with the exercise of one's "
  "occupation. Whether that holds in a given case depends on the specific activity and is not a blanket "
  "exemption - which is why (a) is too broad and (b) too narrow. Importantly, the exception in subsection "
  "(2) sentence 1 no. 3 specifically does not apply to imitation firearms under subsection (1) no. 1. (d) "
  "is wrong: the trader's consent is additionally required under § 17(1) sentence 3 BewachV, but it does "
  "not replace the weapons-law requirement.",
  )

Q("06", "strafrecht_waffen",
  "§ 28 Abs. 2 und 3 WaffG", 5, True, "b",
  "Ein Bewachungsunternehmen besitzt eine waffenrechtliche Erlaubnis für Schusswaffen. Was gilt für das "
  "Führen dieser Waffen durch Wachpersonal nach § 28 WaffG?",
  {"a": "Wachpersonal darf die Waffen jederzeit im Dienst führen, sobald das Unternehmen die Erlaubnis "
        "besitzt",
   "b": "Die Schusswaffe darf nur bei der tatsächlichen Durchführung eines konkreten Auftrages geführt "
        "werden, und die Überlassung an eine Wachperson darf erst erfolgen, wenn die zuständige Behörde "
        "zugestimmt hat",
   "c": "Es genügt, dass die Wachperson die Sachkundeprüfung nach § 34a GewO bestanden hat",
   "d": "Es genügt ein Kleiner Waffenschein"},
  "§ 28 Abs. 2 Satz 1 WaffG: „Die Schusswaffe darf nur bei der tatsächlichen Durchführung eines "
  "konkreten Auftrages nach Absatz 1 geführt werden.“ Satz 2 verpflichtet den Unternehmer, das auch bei "
  "seinem Bewachungspersonal in geeigneter Weise sicherzustellen. § 28 Abs. 3 WaffG verlangt, dass "
  "Wachpersonen der zuständigen Behörde zur Prüfung benannt werden und dass die Überlassung von "
  "Schusswaffen oder Munition „erst erfolgen (darf), wenn die zuständige Behörde zugestimmt hat“; die "
  "Zustimmung ist zu versagen, wenn die Wachperson die Voraussetzungen des § 4 Abs. 1 Nr. 1 bis 3 WaffG "
  "nicht erfüllt oder die Haftpflichtversicherung des Unternehmens das Waffenrisiko nicht umfasst. (a) "
  "übergeht beide Hürden. (c) verwechselt die gewerberechtliche Sachkunde mit der waffenrechtlichen "
  "Erlaubnis - das sind getrennte Verfahren. (d) ist falsch: der Kleine Waffenschein betrifft nicht das "
  "Führen scharfer Schusswaffen.",
  "A guarding company holds a weapons-law permit for firearms. What applies to guards carrying those "
  "firearms under § 28 WaffG?",
  {"a": "Guards may carry the firearms on duty at any time once the company holds the permit",
   "b": "The firearm may be carried only during the actual execution of a specific assignment, and it may "
        "be handed over to a guard only once the competent authority has given its consent",
   "c": "It is enough that the guard has passed the Sachkunde examination under § 34a GewO",
   "d": "A small firearms licence is sufficient"},
  "§ 28(2) sentence 1 WaffG: the firearm may be carried only during the actual execution of a specific "
  "assignment under subsection (1). Sentence 2 obliges the trader to ensure this in a suitable manner for "
  "their guarding staff as well. § 28(3) WaffG requires guards to be named to the competent authority for "
  "vetting and provides that firearms or ammunition may be handed over only once the competent authority "
  "has consented; consent must be refused where the guard does not meet the requirements of § 4(1) nos. 1 "
  "to 3 WaffG or where the company's liability insurance does not cover the firearms risk. (a) skips both "
  "hurdles. (c) confuses the trade-law Sachkunde with the weapons-law permit - separate procedures. (d) is "
  "wrong: the small firearms licence does not cover carrying live firearms.",
  )

# ---------------------------------------------------------------------------
# 5. Unfallverhütungsvorschrift Wach- und Sicherungsdienste
#    (§ 7 Nr. 5 BewachV / Anlage 2 Nr. 5) -- 3 questions
# ---------------------------------------------------------------------------

Q("01", "unfallverhuetung",
  "§ 17 Abs. 1 Satz 3 BewachV; § 20 Abs. 2 BewachV", 5, True, "a",
  "Was muss die Dienstanweisung nach § 17 Abs. 1 Satz 3 BewachV zum Führen von Waffen bestimmen?",
  {"a": "Dass die Wachperson während des Dienstes nur mit Zustimmung des Gewerbetreibenden eine "
        "Schusswaffe, Hieb- und Stoßwaffen sowie Reizstoffsprühgeräte führen darf und jeden Gebrauch "
        "dieser Waffen unverzüglich der zuständigen Polizeidienststelle und dem Gewerbetreibenden "
        "anzuzeigen hat",
   "b": "Dass das Führen von Reizstoffsprühgeräten generell ohne Zustimmung zulässig ist",
   "c": "Dass ein Waffengebrauch nur dann anzuzeigen ist, wenn eine Person verletzt wurde",
   "d": "Dass ausschließlich der Auftraggeber über das Führen von Waffen entscheidet"},
  "§ 17 Abs. 1 Satz 3 BewachV ist wortlautgenau zu kennen: die Dienstanweisung „muss ferner bestimmen, "
  "dass die Wachperson während des Dienstes nur mit Zustimmung des Gewerbetreibenden eine Schusswaffe, "
  "Hieb- und Stoßwaffen sowie Reizstoffsprühgeräte führen darf und jeden Gebrauch dieser Waffen "
  "unverzüglich der zuständigen Polizeidienststelle und dem Gewerbetreibenden anzuzeigen hat“. Zwei "
  "Punkte werden regelmäßig falsch erinnert: die Zustimmung gilt auch für Reizstoffsprühgeräte, nicht nur "
  "für Schusswaffen - (b) ist falsch -, und die Anzeigepflicht knüpft an den Gebrauch an, nicht an einen "
  "Verletzungserfolg - (c) ist falsch. (d) verkennt, dass die Verantwortung beim Gewerbetreibenden liegt, "
  "nicht beim Auftraggeber; § 20 Abs. 2 BewachV verpflichtet diesen zusätzlich zur Anzeige gegenüber der "
  "für § 34a GewO zuständigen Behörde.",
  "What must the standing order provide under § 17(1) sentence 3 BewachV regarding the carrying of "
  "weapons?",
  {"a": "That on duty the guard may carry a firearm, cutting and thrusting weapons and irritant sprays "
        "only with the trader's consent, and must report any use of such weapons without delay to the "
        "competent police station and to the trader",
   "b": "That carrying irritant sprays is generally permitted without consent",
   "c": "That a use of weapons need be reported only if a person was injured",
   "d": "That the client alone decides on the carrying of weapons"},
  "§ 17(1) sentence 3 BewachV should be known word for word: the standing order must further provide that "
  "on duty the guard may carry a firearm, cutting and thrusting weapons and irritant sprays only with the "
  "trader's consent, and must report any use of such weapons without delay to the competent police station "
  "and to the trader. Two points are regularly misremembered: the consent requirement also covers irritant "
  "sprays, not only firearms - so (b) is wrong - and the reporting duty attaches to the use, not to an "
  "injury resulting from it - so (c) is wrong. (d) misses that the responsibility lies with the trader, not "
  "with the client; § 20(2) BewachV additionally obliges the trader to report to the authority competent "
  "for § 34a GewO.",
  )

Q("02", "unfallverhuetung",
  "§ 20 BewachV; § 22 Abs. 1 Nr. 8 und 9 BewachV", 4, False, "b",
  "Welche Pflichten treffen den Gewerbetreibenden nach § 20 BewachV im Zusammenhang mit Waffen?",
  {"a": "Nur die Anzeige eines Waffengebrauchs; die Aufbewahrung ist Sache der Wachperson",
   "b": "Er ist für die sichere Aufbewahrung der Waffen und der Munition verantwortlich, hat die "
        "ordnungsgemäße Rückgabe nach Dienstende sicherzustellen und einen Waffengebrauch unverzüglich "
        "der zuständigen Behörde anzuzeigen",
   "c": "Er muss lediglich einmal jährlich einen Waffenbestand melden",
   "d": "Ihn treffen keine eigenen Pflichten, solange jede Wachperson einen Waffenschein besitzt"},
  "§ 20 Abs. 1 BewachV: „Der Gewerbetreibende ist für die sichere Aufbewahrung der Waffen und der "
  "Munition verantwortlich. Er hat die ordnungsgemäße Rückgabe der Waffen und der Munition nach "
  "Beendigung des Wachdienstes sicherzustellen.“ Abs. 2 verpflichtet ihn, einen Waffengebrauch "
  "unverzüglich der für den Vollzug des § 34a GewO zuständigen Behörde und - soweit noch keine Anzeige "
  "nach § 17 Abs. 1 Satz 3 erfolgt ist - der zuständigen Polizeidienststelle anzuzeigen. Die Verantwortung "
  "für die Aufbewahrung liegt also ausdrücklich beim Unternehmen und nicht bei der einzelnen Wachperson; "
  "(a) und (d) sind deshalb falsch. Ein Verstoß gegen § 20 Abs. 1 Satz 2 oder Abs. 2 ist nach § 22 Abs. 1 "
  "Nr. 8 und 9 BewachV bußgeldbewehrt. (c) ist frei erfunden.",
  "What duties does § 20 BewachV impose on the trader in connection with weapons?",
  {"a": "Only reporting a use of weapons; safekeeping is the guard's business",
   "b": "The trader is responsible for the safe storage of weapons and ammunition, must ensure their "
        "proper return at the end of duty, and must report any use of weapons without delay to the "
        "competent authority",
   "c": "The trader need only report a weapons inventory once a year",
   "d": "The trader has no duties of their own as long as every guard holds a firearms licence"},
  "§ 20(1) BewachV: the trader is responsible for the safe storage of the weapons and ammunition and must "
  "ensure their proper return after the guarding duty ends. Subsection (2) obliges the trader to report a "
  "use of weapons without delay to the authority competent for enforcing § 34a GewO and - where no report "
  "under § 17(1) sentence 3 has yet been made - to the competent police station. Responsibility for storage "
  "therefore lies expressly with the company and not with the individual guard, so (a) and (d) are wrong. A "
  "breach of § 20(1) sentence 2 or (2) carries a fine under § 22(1) nos. 8 and 9 BewachV. (c) is invented.",
  )

Q("03", "unfallverhuetung",
  "§ 17 Abs. 1 Satz 1 und Abs. 2 BewachV; § 21 Abs. 3 Nr. 3 BewachV", 3, False, "c",
  "Wann muss einer Wachperson ein Abdruck der Dienstanweisung ausgehändigt werden?",
  {"a": "Spätestens vier Wochen nach Beginn des Beschäftigungsverhältnisses",
   "b": "Nur auf ausdrückliches Verlangen der Wachperson",
   "c": "Vor der ersten Aufnahme der Bewachungstätigkeit, und zwar gegen Empfangsbescheinigung",
   "d": "Erst dann, wenn die Wachperson Waffen führen soll"},
  "§ 17 Abs. 2 BewachV: „Der Gewerbetreibende hat der Wachperson vor der ersten Aufnahme der "
  "Bewachungstätigkeit einen Abdruck der Dienstanweisung gegen Empfangsbescheinigung auszuhändigen.“ "
  "Zwei Elemente sind prüfungsrelevant: der Zeitpunkt (vor dem ersten Einsatz, nicht danach) und die Form "
  "(gegen Empfangsbescheinigung, also dokumentiert). Die Dienstanweisung selbst ist nach Abs. 1 Satz 1 "
  "verpflichtend - der Gewerbetreibende „hat den Wachdienst durch eine Dienstanweisung ... zu regeln“ - "
  "und ihr Fehlen oder ihre Unvollständigkeit ist nach § 22 Abs. 1 Nr. 2 BewachV bußgeldbewehrt. Nach "
  "§ 21 Abs. 3 Nr. 3 BewachV sind Dienstanweisung und Empfangsbescheinigung außerdem als Belege zu "
  "sammeln. Damit sind (a), (b) und (d) ausgeschlossen.",
  "When must a copy of the standing order be handed to a guard?",
  {"a": "At the latest four weeks after the employment begins",
   "b": "Only on the guard's express request",
   "c": "Before they first take up guarding duty, and against a receipt",
   "d": "Only once the guard is to carry weapons"},
  "§ 17(2) BewachV: the trader must hand the guard a copy of the standing order against a receipt before "
  "they first take up guarding duty. Two elements are examinable: the timing (before the first deployment, "
  "not after) and the form (against a receipt, hence documented). The standing order itself is mandatory "
  "under subsection (1) sentence 1 - the trader must regulate the guarding service by means of a standing "
  "order - and its absence or incompleteness carries a fine under § 22(1) no. 2 BewachV. Under § 21(3) "
  "no. 3 BewachV the standing order and the receipt must also be collected as records. That rules out (a), "
  "(b) and (d).",
  )

# ---------------------------------------------------------------------------
# 6. Umgang mit Menschen (§ 7 Nr. 6 BewachV / Anlage 2 Nr. 6) -- 3 questions
# ---------------------------------------------------------------------------

Q("01", "umgang_menschen",
  "§ 11 Abs. 1, 2, 4 und 6 BewachV", 3, False, "d",
  "Wie ist die Sachkundeprüfung nach § 11 BewachV aufgebaut, und worauf ist im mündlichen Teil ein "
  "Schwerpunkt zu legen?",
  {"a": "Sie besteht nur aus einem schriftlichen Teil; ein mündlicher Teil ist fakultativ",
   "b": "Sie besteht aus einem schriftlichen und einem praktischen Teil, Schwerpunkt ist die "
        "Sicherheitstechnik",
   "c": "Sie besteht aus drei Teilen, Schwerpunkt ist das Datenschutzrecht",
   "d": "Sie ist in einen mündlichen und einen schriftlichen Teil zu gliedern; im mündlichen Teil ist ein "
        "Schwerpunkt auf die Gebiete nach § 7 Nummer 1 und 6 BewachV zu legen"},
  "§ 11 Abs. 1 BewachV: „Die Sachkundeprüfung ist in einen mündlichen und einen schriftlichen Teil zu "
  "gliedern.“ Abs. 2: der mündliche Teil soll je Prüfling etwa 15 Minuten dauern, es können gleichzeitig "
  "bis zu fünf Prüflinge geprüft werden, und „im mündlichen Prüfungsteil ist ein Schwerpunkt auf die in "
  "§ 7 Nummer 1 und 6 genannten Gebiete zu legen“ - also auf das Recht der öffentlichen Sicherheit und "
  "Ordnung einschließlich Gewerberecht und auf den Umgang mit Menschen. Das ist inhaltlich schlüssig: "
  "beides lässt sich im Ankreuzverfahren nur begrenzt prüfen. Nach Abs. 4 ist die Prüfung bestanden, wenn "
  "die Leistungen im schriftlichen und im mündlichen Teil jeweils mindestens mit ausreichend bewertet "
  "wurden; nach Abs. 6 darf sie wiederholt werden. Einen praktischen Teil kennt die BewachV nicht - (b) "
  "ist deshalb falsch.",
  "How is the Sachkunde examination structured under § 11 BewachV, and where must the oral part place its "
  "emphasis?",
  {"a": "It consists of a written part only; an oral part is optional",
   "b": "It consists of a written and a practical part, with the emphasis on security technology",
   "c": "It consists of three parts, with the emphasis on data-protection law",
   "d": "It must be divided into an oral and a written part; in the oral part the emphasis must be placed "
        "on the areas under § 7 numbers 1 and 6 BewachV"},
  "§ 11(1) BewachV: the Sachkunde examination must be divided into an oral and a written part. Subsection "
  "(2): the oral part should last about 15 minutes per candidate, up to five candidates may be examined at "
  "once, and the oral part must place its emphasis on the areas named in § 7 numbers 1 and 6 - the law of "
  "public safety and order including trade-regulation law, and dealing with people. That is substantively "
  "coherent: both can only be tested to a limited extent by multiple choice. Under subsection (4) the "
  "examination is passed where the performance in the written part and in the oral part is each assessed as "
  "at least sufficient; under subsection (6) it may be repeated. The BewachV knows no practical part, so "
  "(b) is wrong.",
  )

Q("02", "umgang_menschen",
  "§ 34a Abs. 5 Satz 2 GewO; § 227 Abs. 2 BGB; § 127 Abs. 1 StPO", 4, True, "a",
  "Ein alkoholisierter Gast wird am Einlass laut und beleidigend, greift aber niemanden körperlich an. "
  "Welches Vorgehen entspricht der Rechtslage und dem Grundsatz der Erforderlichkeit?",
  {"a": "Ansprechen, Distanz wahren, deeskalierend führen und den Gast vom Hausrecht ausgehend des "
        "Bereichs verweisen; körperliche Einwirkung erst, wenn sie zur Abwehr eines Angriffs oder zur "
        "Durchsetzung des Hausrechts tatsächlich erforderlich wird",
   "b": "Sofortiger körperlicher Zugriff, weil Beleidigungen nach §§ 185 ff. StGB strafbar sind",
   "c": "Festnahme nach § 127 Abs. 1 StPO in jedem Fall, da eine Straftat vorliegt",
   "d": "Reizstoffsprühgerät einsetzen, um die Situation schnell zu beenden"},
  "§ 34a Abs. 5 Satz 2 GewO: „In den Fällen der Inanspruchnahme dieser Rechte und Befugnisse ist der "
  "Grundsatz der Erforderlichkeit zu beachten.“ Erforderlich ist stets das mildeste gleich geeignete "
  "Mittel - bei einer verbalen Eskalation ohne körperlichen Angriff sind das Ansprache, Distanz und "
  "Verweisung, nicht der Zugriff. (b) ist falsch, weil die Strafbarkeit einer Beleidigung keine Befugnis "
  "zum körperlichen Einschreiten schafft; Notwehr nach § 227 Abs. 2 BGB setzt einen gegenwärtigen Angriff "
  "voraus. (c) ist falsch, weil § 127 Abs. 1 StPO zusätzlich Fluchtverdacht oder eine nicht sofort "
  "feststellbare Identität verlangt und außerdem nur eine Befugnis, keine Pflicht ist. (d) ist falsch und "
  "zugleich waffenrechtlich heikel: der Einsatz wäre unverhältnismäßig, und das Führen eines "
  "Reizstoffsprühgeräts bedarf nach § 17 Abs. 1 Satz 3 BewachV ohnehin der Zustimmung des "
  "Gewerbetreibenden, jeder Gebrauch ist anzuzeigen.",
  "An intoxicated guest becomes loud and abusive at the entrance but does not physically attack anyone. "
  "Which course of action matches the legal position and the principle of necessity?",
  {"a": "Address them, keep your distance, manage the situation with de-escalation, and eject them from "
        "the area on the basis of the domiciliary right; physical intervention only once it actually "
        "becomes necessary to repel an attack or to enforce the domiciliary right",
   "b": "Immediate physical intervention, because insults are punishable under §§ 185 et seq. StGB",
   "c": "Arrest under § 127(1) StPO in any event, since a criminal offence has been committed",
   "d": "Use an irritant spray to end the situation quickly"},
  "§ 34a(5) sentence 2 GewO: where these rights and powers are relied on, the principle of necessity must "
  "be observed. What is necessary is always the mildest equally suitable means - in a verbal escalation "
  "without physical attack that means addressing, distance and ejection, not physical intervention. (b) is "
  "wrong because the punishability of an insult creates no power to intervene physically; self-defence "
  "under § 227(2) BGB requires a present attack. (c) is wrong because § 127(1) StPO additionally requires "
  "suspicion of absconding or an identity that cannot be established immediately, and in any event confers "
  "a power, not a duty. (d) is wrong and weapons-law sensitive: the use would be disproportionate, and "
  "carrying an irritant spray requires the trader's consent under § 17(1) sentence 3 BewachV in any case, "
  "with every use to be reported.",
  )

Q("03", "umgang_menschen",
  "Anlage 2 Nr. 6 BewachV; § 34a Abs. 1a Satz 2 Nr. 4 GewO", 3, False, "b",
  "Anlage 2 Nummer 6 BewachV nennt für das Sachgebiet Umgang mit Menschen ausdrücklich einen besonderen "
  "Personenkreis. Welchen?",
  {"a": "Beschäftigte des Auftraggebers in Leitungsfunktion",
   "b": "Besonders schutzbedürftige Geflüchtete, beispielsweise allein reisende Frauen, Homosexuelle, "
        "transgeschlechtliche Personen, Menschen mit Behinderung und Opfer schwerer Gewalt",
   "c": "Ausländische Geschäftsreisende",
   "d": "Mitglieder von Prüfungsausschüssen der Industrie- und Handelskammern"},
  "Anlage 2 Nummer 6 BewachV führt als Inhalt ausdrücklich den „Umgang mit und Schutz von besonders "
  "schutzbedürftigen Geflüchteten (wie beispielsweise allein reisende Frauen, Homosexuelle, "
  "transgeschlechtliche Personen, Menschen mit Behinderung, Opfer schwerer Gewalt)“ auf, eingebettet in "
  "„interkulturelle Kompetenz unter besonderer Beachtung von Diversität und gesellschaftlicher "
  "Vielfalt“. Mit etwa 11 der 40 Unterrichtsstunden ist Nummer 6 das mit Abstand größte Sachgebiet, und "
  "§ 11 Abs. 2 BewachV macht es zu einem Schwerpunkt des mündlichen Prüfungsteils. Der Zusammenhang ist "
  "offensichtlich: § 34a Abs. 1a Satz 2 Nr. 4 GewO macht gerade die Bewachung von "
  "Asyl-Aufnahmeeinrichtungen und Gemeinschaftsunterkünften in leitender Funktion sachkundepflichtig.",
  "Annex 2 number 6 BewachV expressly names a particular group of people for the subject area of dealing "
  "with people. Which one?",
  {"a": "Client employees in supervisory positions",
   "b": "Particularly vulnerable refugees, for example women travelling alone, homosexual people, "
        "transgender people, people with disabilities and victims of serious violence",
   "c": "Foreign business travellers",
   "d": "Members of the examination boards of the Chambers of Industry and Commerce"},
  "Annex 2 number 6 BewachV expressly lists as content the handling and protection of particularly "
  "vulnerable refugees (for example women travelling alone, homosexual people, transgender people, people "
  "with disabilities, victims of serious violence), embedded in intercultural competence with particular "
  "regard to diversity and social plurality. At roughly 11 of the 40 teaching hours, number 6 is by far the "
  "largest subject area, and § 11(2) BewachV makes it one of the focal points of the oral examination. The "
  "connection is plain: § 34a(1a) sentence 2 no. 4 GewO makes precisely the guarding of asylum reception "
  "facilities and shared accommodation in a supervisory role subject to the Sachkunde requirement.",
  )

# ---------------------------------------------------------------------------
# 7. Grundzüge der Sicherheitstechnik (§ 7 Nr. 7 BewachV / Anlage 2 Nr. 7)
#    -- 3 questions
# ---------------------------------------------------------------------------

Q("01", "sicherheitstechnik",
  "§ 34a Abs. 5 GewO; §§ 855, 859, 860 BGB; Anlage 2 Nr. 7 BewachV", 4, True, "c",
  "Eine Gefahrenmeldeanlage löst aus; Sie fahren im Rahmen der Alarmverfolgung zum Objekt und treffen "
  "dort eine unbekannte Person im Gebäude an. Welche Befugnisse haben Sie?",
  {"a": "Dieselben wie die Polizei, weil Sie im Rahmen eines Interventionsvertrages tätig werden",
   "b": "Eine Durchsuchungs- und Vernehmungsbefugnis, weil ein Alarm ausgelöst wurde",
   "c": "Nur die Jedermannsrechte nach § 34a Abs. 5 GewO sowie die als Besitzdiener zustehenden "
        "Besitzschutzrechte - die Anlage selbst schafft keine zusätzlichen Befugnisse",
   "d": "Keinerlei Befugnisse; Sie dürfen das Objekt nicht betreten"},
  "Die Auswertung einer Gefahrenmeldeanlage und die Alarmverfolgung sind Sachgebiet Nummer 7 der Anlage 2 "
  "BewachV, aber sie ändern nichts an der Befugnislage: § 34a Abs. 5 GewO weist Bewachungspersonal "
  "abschließend die Jedermannsrechte, vertraglich übertragene Selbsthilferechte und gegebenenfalls "
  "gesetzlich übertragene Befugnisse zu. Als Besitzdiener nach § 855 BGB stehen Ihnen über § 860 BGB die "
  "Besitzschutzrechte des § 859 BGB zu, und der Interventionsvertrag berechtigt zum Betreten - deshalb ist "
  "(d) falsch. Technik erweitert Befugnisse aber nie: (a) und (b) sind schon deshalb falsch, weil eine "
  "Durchsuchung oder Vernehmung selbst der Polizei nur unter engen gesetzlichen Voraussetzungen erlaubt "
  "ist. Praktisch heißt das: sichern, beobachten, Polizei verständigen - Eigensicherung hat Vorrang.",
  "An alarm system is triggered; you drive to the site as part of the alarm response and encounter an "
  "unknown person inside the building. What powers do you have?",
  {"a": "The same as the police, because you are acting under an intervention contract",
   "b": "A power to search and to question, because an alarm was triggered",
   "c": "Only the general rights under § 34a(5) GewO plus the possessory rights available to you as a "
        "servant in possession - the system itself creates no additional powers",
   "d": "No powers at all; you may not enter the site"},
  "Evaluating an alarm system and responding to alarms is subject area number 7 of Annex 2 BewachV, but it "
  "changes nothing about the position on powers: § 34a(5) GewO exhaustively assigns guarding staff the "
  "general rights available to anyone, self-help rights transferred by contract, and any powers transferred "
  "by statute. As a servant in possession under § 855 BGB you have the possessory rights of § 859 BGB via "
  "§ 860 BGB, and the intervention contract entitles you to enter - which is why (d) is wrong. But "
  "technology never extends powers: (a) and (b) are wrong if only because a search or an interrogation is "
  "permitted even to the police only under narrow statutory conditions. In practice: secure the scene, "
  "observe, call the police - your own safety comes first.",
  )

Q("02", "sicherheitstechnik",
  "§ 123 StGB; § 903 BGB", 4, False, "a",
  "Sie betreiben eine Zutrittskontrolle mit Vereinzelungsanlage. Eine Person gelangt regulär hinein, "
  "weigert sich aber nach Ihrer klaren Aufforderung, den Bereich zu verlassen. Wie ist das strafrechtlich "
  "einzuordnen?",
  {"a": "Als Hausfriedensbruch nach § 123 Abs. 1 StGB in der Variante des unbefugten Verweilens trotz "
        "Aufforderung des Berechtigten; die Tat wird nach § 123 Abs. 2 StGB nur auf Antrag verfolgt",
   "b": "Als Diebstahl nach § 242 StGB, weil die Person eine Leistung in Anspruch nimmt",
   "c": "Als Sachbeschädigung nach § 303 StGB an der Vereinzelungsanlage",
   "d": "Als bloße Ordnungswidrigkeit nach § 22 BewachV"},
  "§ 123 Abs. 1 StGB kennt zwei Varianten: das widerrechtliche Eindringen und - hier einschlägig - „wer, "
  "wenn er ohne Befugnis darin verweilt, auf die Aufforderung des Berechtigten sich nicht entfernt“. Wer "
  "also regulär eingelassen wurde, kann den Tatbestand dennoch durch Bleiben erfüllen. Wichtig für die "
  "Praxis ist § 123 Abs. 2 StGB: „Die Tat wird nur auf Antrag verfolgt“ - ohne Strafantrag des "
  "Berechtigten passiert nichts, weshalb die Dokumentation und die Verständigung des Hausrechtsinhabers "
  "zum Ablauf gehören. Das Hausrecht selbst folgt aus § 903 BGB beziehungsweise aus dem Besitz und wird "
  "von der Wachperson regelmäßig in übertragener Form ausgeübt. (b) und (c) passen tatbestandlich nicht, "
  "(d) verwechselt Straftat und Ordnungswidrigkeit.",
  "You operate an access control point with a turnstile. A person enters legitimately but refuses to leave "
  "the area after you have clearly asked them to. How is this classified in criminal law?",
  {"a": "As trespass under § 123(1) StGB in the variant of remaining without authorisation despite the "
        "entitled person's request; under § 123(2) StGB the offence is prosecuted only on complaint",
   "b": "As theft under § 242 StGB, because the person is using a service",
   "c": "As criminal damage under § 303 StGB to the turnstile",
   "d": "As a mere administrative offence under § 22 BewachV"},
  "§ 123(1) StGB has two variants: unlawful entry and - relevant here - failing to leave on the request of "
  "the entitled person while remaining without authorisation. Someone admitted legitimately can therefore "
  "still commit the offence by staying. Practically important is § 123(2) StGB: the offence is prosecuted "
  "only on complaint - without a criminal complaint by the entitled person nothing happens, which is why "
  "documenting the incident and notifying the holder of the domiciliary right are part of the procedure. "
  "The domiciliary right itself derives from § 903 BGB or from possession and is typically exercised by the "
  "guard on a delegated basis. (b) and (c) do not fit the elements of the offence; (d) confuses a criminal "
  "offence with an administrative one.",
  )

Q("03", "sicherheitstechnik",
  "§ 323c StGB; Anlage 2 Nr. 7 BewachV (Brandschutz)", 5, True, "b",
  "Sie entdecken bei einem Kontrollgang einen Entstehungsbrand und eine bewusstlose Person. Welche "
  "rechtliche Pflicht trifft Sie unmittelbar?",
  {"a": "Keine - Brandbekämpfung ist ausschließlich Aufgabe der Feuerwehr",
   "b": "Die Pflicht zur Hilfeleistung nach § 323c Abs. 1 StGB, soweit sie erforderlich und zumutbar ist, "
        "insbesondere ohne erhebliche eigene Gefahr und ohne Verletzung anderer wichtiger Pflichten "
        "möglich",
   "c": "Die Pflicht, den Brand in jedem Fall selbst zu löschen, auch unter erheblicher "
        "Eigengefährdung",
   "d": "Nur die Pflicht, den Vorfall nach § 21 BewachV aufzuzeichnen"},
  "§ 323c Abs. 1 StGB: „Wer bei Unglücksfällen oder gemeiner Gefahr oder Not nicht Hilfe leistet, obwohl "
  "dies erforderlich und ihm den Umständen nach zuzumuten, insbesondere ohne erhebliche eigene Gefahr und "
  "ohne Verletzung anderer wichtiger Pflichten möglich ist, wird mit Freiheitsstrafe bis zu einem Jahr "
  "oder mit Geldstrafe bestraft.“ Die Pflicht ist also durch Erforderlichkeit und Zumutbarkeit begrenzt - "
  "das schließt (c) aus, denn eine erhebliche Eigengefährdung wird gerade nicht verlangt. Regelmäßig "
  "geschuldet sind Notruf, Absicherung und die im Rahmen des Möglichen liegende Hilfe, etwa der Einsatz "
  "eines Handfeuerlöschers bei einem Entstehungsbrand. (a) ist falsch, weil die Hilfeleistungspflicht "
  "jedermann trifft. Abs. 2 stellt zudem unter Strafe, wer hilfeleistende Personen behindert. Die "
  "Aufzeichnungspflichten nach § 21 BewachV bestehen daneben, ersetzen die Hilfeleistung aber nicht - (d) "
  "ist deshalb falsch.",
  "During a patrol you discover an incipient fire and an unconscious person. What legal duty applies to "
  "you immediately?",
  {"a": "None - firefighting is exclusively the fire brigade's task",
   "b": "The duty to render assistance under § 323c(1) StGB, in so far as this is necessary and reasonable "
        "in the circumstances, in particular possible without significant danger to yourself and without "
        "breaching other important duties",
   "c": "The duty to extinguish the fire yourself in every case, even at significant risk to yourself",
   "d": "Only the duty to record the incident under § 21 BewachV"},
  "§ 323c(1) StGB: whoever fails to render assistance in the case of accidents, common danger or "
  "emergencies, although this is necessary and reasonable in the circumstances, in particular possible "
  "without significant danger to themselves and without breaching other important duties, is liable to "
  "imprisonment of up to one year or a fine. The duty is therefore limited by necessity and "
  "reasonableness - which rules out (c), since significant self-endangerment is precisely not required. "
  "What is normally owed is an emergency call, securing the scene, and such help as is possible, for "
  "example using a hand extinguisher on an incipient fire. (a) is wrong because the duty to render "
  "assistance applies to everyone. Subsection (2) additionally penalises obstructing people who are "
  "rendering assistance. The recording duties under § 21 BewachV exist alongside this but do not replace "
  "rendering assistance, so (d) is wrong.",
  )


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

DESCRIPTION = (
    "Original practice questions for the German IHK-Sachkundepruefung im "
    "Bewachungsgewerbe under § 34a Abs. 1 Satz 3 Nr. 3 and § 34a Abs. 1a Satz 2 "
    "GewO. Seven topics mapping 1:1 onto the seven Sachgebiete of § 7 BewachV, "
    "which § 9 Abs. 2 BewachV makes the legal subject matter of the examination: "
    "(1) Recht der oeffentlichen Sicherheit und Ordnung einschliesslich "
    "Gewerberecht, (2) Datenschutzrecht, (3) Buergerliches Gesetzbuch, (4) Straf- "
    "und Verfahrensrecht sowie Umgang mit Waffen, (5) Unfallverhuetungsvorschrift "
    "Wach- und Sicherungsdienste, (6) Umgang mit Menschen, (7) Grundzuege der "
    "Sicherheitstechnik. Questions are written in applied-situation style because "
    "§ 9 Abs. 1 BewachV defines the examination's purpose as proof of knowledge of "
    "the relevant rules and duties 'sowie deren praktische Anwendung'. "
    "SCOPE BOUNDARY, and the single most important fact in this module: the base "
    "guarding activity does NOT require this examination. A Wachperson needs only "
    "Zuverlaessigkeit plus an IHK Unterrichtungsbescheinigung (40 hours, "
    "attendance-based, no examination) under § 34a Abs. 1a Satz 1 Nr. 1 und 2 GewO "
    "in conjunction with § 6 BewachV. The full Sachkundepruefung is required only "
    "of the business owner / gesetzlicher Vertreter / Betriebsleiter as a condition "
    "of the Erlaubnis (§ 34a Abs. 1 Satz 3 Nr. 3 GewO), and of Wachpersonen "
    "performing one of the five activities exhaustively listed in § 34a Abs. 1a "
    "Satz 2 GewO. "
    "IMPORTANT - what this module is NOT: it is unofficial practice material. There "
    "is no official public question catalogue for this examination; the written "
    "Aufgabensaetze are bundeseinheitlich but not published. This pool therefore "
    "cannot and does not claim to reproduce, predict or fully cover the real "
    "examination, and passing every question here is not a guarantee of passing it. "
    "The oral part (§ 11 Abs. 1 und 2 BewachV), whose emphasis is on § 7 Nr. 1 and "
    "Nr. 6, is not testable by multiple choice at all."
)

SOURCES = {
    "tier_a_binding": [
        "Gewerbeordnung (GewO) §§ 6a, 32, 34a, 144, 159 - https://www.gesetze-im-internet.de/gewo/",
        "Bewachungsverordnung (BewachV) vom 3.5.2019, BGBl. I S. 692, zuletzt geaendert durch Art. 2 V. v. 24.6.2019 BGBl. I S. 882 - §§ 1, 4-12, 14, 16-23 und Anlage 2 - https://www.gesetze-im-internet.de/bewachv_2019/",
        "BewachV Anlage 2 (zu § 7), Fundstelle BGBl. I 2019, 701 - der gesetzliche Sachgebietskatalog, den § 9 Abs. 2 BewachV zum Gegenstand der Pruefung erklaert - https://www.gesetze-im-internet.de/bewachv_2019/anlage_2.html",
        "Buergerliches Gesetzbuch (BGB) §§ 226, 227, 228, 229, 230, 823, 833, 854, 855, 858, 859, 860, 903, 965 - https://www.gesetze-im-internet.de/bgb/",
        "Strafgesetzbuch (StGB) §§ 12, 32, 34, 123, 239, 240, 242, 249, 252, 263, 265a, 303, 323c - https://www.gesetze-im-internet.de/stgb/",
        "Strafprozessordnung (StPO) §§ 127, 163 - https://www.gesetze-im-internet.de/stpo/",
        "Waffengesetz (WaffG) §§ 10, 28, 42a - https://www.gesetze-im-internet.de/waffg_2002/",
        "Bundesdatenschutzgesetz (BDSG) § 4 - https://www.gesetze-im-internet.de/bdsg_2018/__4.html",
        "Gesetz zum Buerokratierueckbau in der Gewerbeordnung ..., G. v. 20.7.2026, BGBl. 2026 I Nr. 215, Art. 1 Nr. 1 und Art. 11 - Neufassung des § 6a Abs. 1 GewO mit ausdruecklicher Ausnahme fuer Verfahren nach § 34a Abs. 1, in Kraft seit 24.7.2026 - https://www.recht.bund.de/bgbl/1/2026/215/regelungstext.pdf",
    ],
    "tier_b_chamber_practice": [
        "DIHK, 'Bewachungsgewerbe - Rahmenplan fuer die Sachkundepruefung / Stoffsammlung fuer die Unterrichtung', Stand September 2019 - read as a SCOPE CROSS-CHECK ONLY. Not a content source: it carries its own copyright notice (DIHK e.V.) and none of its wording, table structure, taxonomy levels or (S) markers is reproduced in this module. See docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md section 4.1.",
        "IHK Frankfurt am Main, 'Sachkundepruefung im Bewachungsgewerbe nach § 34a GewO' (Nr. 5306328) - exam mechanics, fees, Zulassungsregel",
        "IHK Magdeburg, 'Sachkundepruefung Bewachung nach § 34a der GewO' (Nr. 3301986) - exam mechanics, Bewertungsmodell ab 1.7.2025",
        "IHK zu Essen, 'Rahmenplan fuer die Sachkundepruefung im Bewachungsgewerbe' (Nr. 2713376)",
    ],
    "note": (
        "No exam-prep vendor's question wording, explanations, structure or question "
        "compilation was read, opened, copied or paraphrased into this module "
        "(AGENTS.md constraint 1). Several such sites appeared in search results and "
        "were deliberately not fetched. The syllabus authority for this module is "
        "statutory - § 9 Abs. 2 BewachV in conjunction with § 7 and Anlage 2 BewachV - "
        "and German statutory text is an amtliches Werk under § 5 UrhG with no "
        "copyright. Every question is original synthesis from the text of the "
        "provision named in its own legal_basis field."
    ),
}


def main():
    doc = {"meta": {}, "questions": []}

    for q in QUESTIONS:
        doc["questions"].append({k: q[k] for k in KEY_ORDER if k in q})

    tdist = {}
    for q in QUESTIONS:
        tdist[q["topic_code"]] = tdist.get(q["topic_code"], 0) + 1

    doc["meta"] = {
        "app": "Zettacard / bewachungsgewerbe-lernmodul",
        "version": "0.1-draft",
        "generated": "2026-08-17",
        "generator": "authored:claude-opus/2026-08-17 (data/gen_bewachungsgewerbe_draft.py)",
        "description": DESCRIPTION,
        "class": "ALL",
        "locales": ["de", "en"],
        "canonical_locale": "de",
        "locale_note": (
            "DE ist kanonisch, EN ist eine vollstaendige Parallieluebersetzung - "
            "gleiches Startmuster wie aevo / fadp_ch / kyc_aml / kartellrecht. "
            "ABWEICHENDE EINSCHAETZUNG gegenueber jenen Modulen: dieses hier ist ein "
            "starker, kein schwacher Kandidat fuer alle 12 Sprachen. Die Belegschaft "
            "im Bewachungsgewerbe ist stark migrantisch gepraegt, § 6 Abs. 1 Satz 2 "
            "BewachV verlangt fuer die Unterrichtung ausdruecklich deutsche "
            "Sprachkenntnisse mindestens auf dem Niveau B1 des Gemeinsamen "
            "Europaeischen Referenzrahmens, und Anlage 2 Nr. 6 BewachV hat "
            "interkulturelle Kompetenz zum ausdruecklichen Gegenstand. Ein "
            "Produktivausbau sollte alle 12 Sprachen einplanen. UI-Strings shippen "
            "nach AGENTS.md Constraint 5 ohnehin in allen 12 Sprachen."
        ),
        "orthography_note": (
            "Deutsches Standarddeutsch mit echten Unicode-Umlauten und Eszett "
            "(ä/ö/ü/ß) - keine ASCII-Ersatzschreibung. Anders als beim Schweizer "
            "Modul fadp_ch, das bewusst 'ss' verwendet, weil der Schweizer "
            "Gesetzestext das tut. Deutsche Anfuehrungszeichen (Doppelchevrons "
            "unten/oben) werden in deutschen Zitaten verwendet, englische Felder "
            "nutzen einfache ASCII-Anfuehrungszeichen."
        ),
        "exam_format_note": (
            "§ 11 Abs. 1 BewachV: die Sachkundepruefung ist in einen muendlichen und "
            "einen schriftlichen Teil zu gliedern. § 11 Abs. 2: der muendliche Teil "
            "soll je Pruefling etwa 15 Minuten dauern, es koennen bis zu fuenf "
            "Prueflinge gleichzeitig geprueft werden, und der Schwerpunkt liegt auf "
            "den Gebieten nach § 7 Nr. 1 und Nr. 6. § 11 Abs. 4: bestanden, wenn die "
            "Leistungen im schriftlichen UND im muendlichen Teil jeweils mindestens "
            "mit ausreichend bewertet wurden. § 11 Abs. 6: die Pruefung darf "
            "wiederholt werden. § 11 Abs. 5: die Pruefung ist nicht oeffentlich. "
            "§ 10 Abs. 1: die Pruefung kann bei jeder IHK abgelegt werden, die sie "
            "anbietet - es gibt keine Bezirksbindung. § 11 Abs. 7: die IHK stellt "
            "eine Bescheinigung nach Anlage 3 BewachV aus. "
            "WICHTIG - was die BewachV gerade NICHT festlegt: Anzahl der Fragen, "
            "Dauer des schriftlichen Teils, Prozentschwelle fuer 'ausreichend' und "
            "ob der schriftliche Teil dem muendlichen vorgeschaltet ist. Das alles "
            "regeln die IHKs nach § 11 Abs. 8 BewachV in Verbindung mit § 32 Abs. 1 "
            "GewO durch Satzung, und es variiert. Zwei unabhaengig gepruefte Kammern "
            "(Frankfurt am Main, Magdeburg) nennen uebereinstimmend 120 Minuten fuer "
            "den schriftlichen Teil und lassen zum muendlichen Teil nur zu, wer den "
            "schriftlichen bestanden hat; das ist typische Kammerpraxis, nicht "
            "Bundesrecht, und darf nicht als solches dargestellt werden."
        ),
        "topic_weighting_note": (
            "Die sieben Topics entsprechen 1:1 den sieben Sachgebieten des § 7 "
            "BewachV. Die Gewichtung folgt naeherungsweise den Unterrichtsstunden, "
            "die Anlage 2 BewachV den Sachgebieten zuordnet (Nr. 1 und 2 zusammen "
            "etwa 6, Nr. 3 etwa 6, Nr. 4 etwa 6, Nr. 5 etwa 6, Nr. 6 etwa 11, Nr. 7 "
            "etwa 5 von insgesamt 40 Unterrichtsstunden), mit einer Untergrenze von "
            "3 Fragen je Sachgebiet, damit jedes Gebiet fuer themengefiltertes Ueben "
            "nutzbar bleibt. CAVEAT, klar gesagt: die Stundenangaben der Anlage 2 "
            "gelten formal dem UNTERRICHTUNGSverfahren; § 9 Abs. 2 BewachV uebernimmt "
            "die Sachgebiete fuer die Pruefung dem Gegenstand nach, nicht der "
            "Gewichtung nach. Keine Stelle veroeffentlicht eine Fragenverteilung fuer "
            "den schriftlichen Teil. Die Stundenverteilung als Naeherung fuer die "
            "Pruefungsgewichtung zu verwenden, ist eine begruendete eigene "
            "Entscheidung dieses Moduls und keine dokumentierte Tatsache ueber die "
            "echte Pruefung. Nr. 6 ist hier bewusst untergewichtet, weil sich "
            "Deeskalation und interkulturelle Kompetenz im Ankreuzverfahren nur "
            "begrenzt pruefen lassen - genau deshalb macht § 11 Abs. 2 BewachV sie "
            "zum Schwerpunkt des muendlichen Teils."
        ),
        "point_system": (
            "3-5 Punkte je Frage, wie in den uebrigen Modulen dieser App. 5 Punkte "
            "markieren die Fragen, bei denen ein Fehler in der Praxis eine Straftat, "
            "eine Ordnungswidrigkeit oder eine Befugnisueberschreitung bedeutet - "
            "also die Grenzen des § 34a Abs. 5 GewO, § 127 StPO, §§ 229/230 BGB, "
            "§ 239 StGB, § 252 StGB, das Waffenrecht und die Waffenpflichten der "
            "BewachV."
        ),
        "pass_rule_note": (
            "BEWUSST OFFEN GELASSEN - dieses Modul erfindet keine Bestehensregel. "
            "§ 11 Abs. 4 BewachV verlangt nur, dass der schriftliche und der "
            "muendliche Teil jeweils mindestens mit 'ausreichend' bewertet werden; "
            "eine Prozentschwelle, eine Fragenzahl und eine Pruefungsdauer nennt das "
            "Bundesrecht nicht. Diese Groessen regeln die IHKs nach § 11 Abs. 8 "
            "BewachV in Verbindung mit § 32 Abs. 1 Nr. 4, 5, 8 und 10 GewO durch "
            "Satzung. Hinzu kommt, dass mindestens eine Kammer (IHK Magdeburg) zum "
            "1.7.2025 vom 'Alles-oder-Nichts-Prinzip' auf eine Teilbewertung "
            "umgestellt hat; ob das bundesweit gilt, ist in diesem Rechercheschritt "
            "NICHT geklaert worden. Vor einer produktiven Nutzung ist die Satzung der "
            "jeweiligen IHK auszuwerten."
        ),
        "sources": SOURCES,
        "related_modules": [
            {
                "exam_type": "datenschutz",
                "relation": "see_also",
                "de": "Sachgebiet 2 des § 7 BewachV ist Datenschutzrecht. Dieses Modul behandelt es nur in dem für Bewachungsaufgaben typischen Ausschnitt (Videoüberwachung nach § 4 BDSG). Die allgemeinen Grundsätze der DS-GVO, die Betroffenenrechte und die Sanktionen behandelt das Modul 'Datenschutz' ausführlich.",
                "en": "Subject area 2 of § 7 BewachV is data-protection law. This module covers only the slice typical of guarding duties (video surveillance under § 4 BDSG). The general GDPR principles, data-subject rights and sanctions are covered in detail by the 'Datenschutz' module.",
            },
            {
                "exam_type": "waffensachkunde",
                "relation": "see_also",
                "de": "Sachgebiet 4 des § 7 BewachV umfasst den Umgang mit Waffen. Dieses Modul behandelt nur die bewachungsspezifischen Vorschriften (§ 28 WaffG, § 42a WaffG, §§ 17 und 20 BewachV). Die allgemeine Waffensachkunde nach § 7 WaffG ist Gegenstand eines eigenen Moduls und einer davon getrennten Prüfung.",
                "en": "Subject area 4 of § 7 BewachV covers the handling of weapons. This module covers only the guarding-specific provisions (§ 28 WaffG, § 42a WaffG, §§ 17 and 20 BewachV). The general weapons expertise under § 7 WaffG is the subject of a separate module and of a separate examination.",
            },
        ],
        "legal_review_status": (
            "NOT legally reviewed - AI-drafted from primary sources (GewO, BewachV "
            "incl. Anlage 2, BGB, StGB, StPO, WaffG, BDSG via "
            "gesetze-im-internet.de, retrieved 2026-08-17; BGBl. 2026 I Nr. 215 via "
            "recht.bund.de). Verify every citation and its currency before production "
            "or commercial use. No lawyer and no member of an IHK Pruefungsausschuss "
            "has reviewed this content. OPEN LEGAL POINT flagged for review: the "
            "applicability of § 4 Abs. 1 BDSG to non-public controllers is contested; "
            "the questions here deliberately rest only on § 4 Abs. 2, 3 und 5 BDSG and "
            "not on Abs. 1. See docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md "
            "sections 4.2 and 9.3."
        ),
        "renewal_months": None,
        "renewal_basis": "not_applicable",
        "renewal_note": (
            "Die Sachkundepruefung nach § 34a GewO ist ein einmaliger "
            "Eignungsnachweis; eine Wiederholungs- oder Auffrischungspflicht kennt "
            "weder die GewO noch die BewachV. Die Bescheinigung nach § 11 Abs. 7 "
            "BewachV in Verbindung mit Anlage 3 BewachV ist unbefristet. Davon zu "
            "unterscheiden ist die wiederkehrende Zuverlaessigkeitsueberpruefung: "
            "nach § 34a Abs. 1 Satz 10 GewO, auch in Verbindung mit Abs. 1a Satz 7, "
            "hat die zustaendige Behoerde die Zuverlaessigkeit in regelmaessigen "
            "Abstaenden, spaetestens jedoch nach Ablauf von fuenf Jahren, erneut zu "
            "pruefen. Das ist keine Wiederholung der Sachkundepruefung, sondern eine "
            "Zuverlaessigkeitsfrage."
        ),
        "draft_note": (
            "Not registered in data/build_modules.py, not in "
            "data/modules_manifest.json, app.js untouched, no build step run, nothing "
            "staged or committed. The _DRAFT filename suffix keeps this file out of "
            "the live build path by construction. First-round pilot: 28 questions, DE "
            "canonical + EN. See "
            "docs/bewachungsgewerbe-pre-review-dossier-2026-08-17.md for the sourcing "
            "analysis that unblocked this module (§ 9 Abs. 2 BewachV makes § 7 + "
            "Anlage 2 BewachV the exam's statutory subject matter) and for the open "
            "items the PO has to decide before it is wired in."
        ),
        "license": "CC BY-NC-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "license_note": (
            "Attribution-NonCommercial-ShareAlike: free to use, adapt, and "
            "redistribute for non-commercial training purposes, with credit and under "
            "the same license. Commercial reuse needs a separate arrangement."
        ),
        "total_questions": len(QUESTIONS),
        "topic_distribution": {k: tdist[k] for k in TOPIC_DE if k in tdist},
    }

    # ---------------------------- integrity checks -------------------------
    fails = []
    seen = set()
    for q in doc["questions"]:
        if q["id"] in seen:
            fails.append("duplicate id %s" % q["id"])
        seen.add(q["id"])
        if q["topic_code"] not in TOPIC_DE:
            fails.append("%s: unknown topic_code %s" % (q["id"], q["topic_code"]))
        if q["topic"] != TOPIC_DE[q["topic_code"]]:
            fails.append("%s: topic label does not match topic_code" % q["id"])
        if len(q["correct"]) != 1 or q["correct"][0] not in "abcd":
            fails.append("%s: bad correct %r" % (q["id"], q["correct"]))
        if q["points"] not in (3, 4, 5):
            fails.append("%s: points out of range" % q["id"])
        if not q["legal_basis"].strip():
            fails.append("%s: empty legal_basis" % q["id"])
        if q["question_type"] != "single_choice":
            fails.append("%s: unexpected question_type" % q["id"])
        for loc in ("de", "en"):
            t = q["text"][loc]
            if sorted(t["options"].keys()) != ["a", "b", "c", "d"]:
                fails.append("%s/%s: options must be exactly a-d" % (q["id"], loc))
            if q["correct"][0] not in t["options"]:
                fails.append("%s/%s: correct key missing from options" % (q["id"], loc))
            if not t["question"].strip():
                fails.append("%s/%s: empty question" % (q["id"], loc))
            if not q["explanation"][loc].strip():
                fails.append("%s/%s: empty explanation" % (q["id"], loc))
            if len(set(t["options"].values())) != 4:
                fails.append("%s/%s: duplicate option text" % (q["id"], loc))

    for tc in TOPIC_DE:
        if tdist.get(tc, 0) < 3:
            fails.append("topic %s has fewer than 3 questions (%d)"
                         % (tc, tdist.get(tc, 0)))

    dist = {}
    for q in doc["questions"]:
        dist[q["correct"][0]] = dist.get(q["correct"][0], 0) + 1
    for k in "abcd":
        if dist.get(k, 0) < 4:
            fails.append("answer key '%s' used only %d times (want >= 4)"
                         % (k, dist.get(k, 0)))

    # ---- orthography: DE carries umlauts, EN must not ----
    def collect(node, out):
        if isinstance(node, dict):
            for v in node.values():
                collect(v, out)
        elif isinstance(node, list):
            for v in node:
                collect(v, out)
        elif isinstance(node, str):
            out.append(node)

    de_strings, en_strings = [], []
    for q in doc["questions"]:
        collect(q["text"]["de"], de_strings)
        de_strings.append(q["explanation"]["de"])
        collect(q["text"]["en"], en_strings)
        en_strings.append(q["explanation"]["en"])

    umlauts = sum(s.count(c) for s in de_strings for c in "äöüÄÖÜß")
    if umlauts < 300:
        fails.append("suspiciously few German umlaut/eszett characters (%d)" % umlauts)

    en_with_umlauts = [s for s in en_strings if any(c in s for c in "äöüÄÖÜß")]
    if en_with_umlauts:
        fails.append("umlaut/eszett characters found in %d English string(s)"
                     % len(en_with_umlauts))

    # ASCII-transliteration residue in DE text: flag words containing ae/oe/ue
    # that are NOT legitimate German (legitimate: Dauer, neue, Steuer, Aufgabe...).
    LEGIT = ("auer", "aue", "eue", "reue", "oer", "uer", "auf", "aus")
    residue = set()
    for s in de_strings:
        for raw in s.split():
            w = raw.strip(".,;:()„“?!-–\"'")
            low = w.lower()
            for bad in ("ae", "oe", "ue"):
                if bad in low:
                    idx = low.find(bad)
                    ctx = low[max(0, idx - 1):idx + 3]
                    if not any(l in ctx for l in LEGIT):
                        residue.add(w)
    residue = sorted(residue)

    all_text = "\n".join(de_strings + en_strings)
    for bad, name in [("‘", "left single quote"), ("’", "right single quote"),
                      ("–", "en dash"), ("—", "em dash")]:
        if bad in all_text:
            fails.append("typographic character present (%s)" % name)
    for bad, name in [("„", "German low quote"), ("“", "German high quote")]:
        hits = [s for s in en_strings if bad in s]
        if hits:
            fails.append("German quotation mark (%s) present in %d EN string(s)"
                         % (name, len(hits)))
    for ch in set(all_text):
        if unicodedata.category(ch).startswith("C") and ch not in "\n\t":
            fails.append("control character %r present" % ch)

    # meta sanity
    m = doc["meta"]
    for required in ("license", "license_url", "legal_review_status", "draft_note",
                     "sources", "pass_rule_note", "description"):
        if not m.get(required):
            fails.append("meta.%s missing or empty" % required)
    if m["license"] != "CC BY-NC-SA 4.0":
        fails.append("meta.license is not CC BY-NC-SA 4.0")
    if m["total_questions"] != len(doc["questions"]):
        fails.append("meta.total_questions does not match question count")
    if sum(m["topic_distribution"].values()) != len(doc["questions"]):
        fails.append("meta.topic_distribution does not sum to question count")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    pd, hs, gs = {}, 0, 0
    for q in doc["questions"]:
        pd[q["points"]] = pd.get(q["points"], 0) + 1
        hs += 1 if q["high_stakes"] else 0
        gs += 1 if q["grundstoff"] else 0

    print("wrote %s (%d questions)" % (OUT, len(doc["questions"])))
    print("topic distribution:  %s" % dict(sorted(tdist.items())))
    print("answer key spread:   %s" % dict(sorted(dist.items())))
    print("points distribution: %s" % dict(sorted(pd.items())))
    print("high_stakes: %d   grundstoff: %d" % (hs, gs))
    print("German umlaut/eszett characters in DE text: %d" % umlauts)
    print("possible ASCII-transliteration residue (manual review): %s"
          % (residue if residue else "none"))

    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  - %s" % f)
        sys.exit(1)
    print("\nall integrity checks passed")


if __name__ == "__main__":
    main()
