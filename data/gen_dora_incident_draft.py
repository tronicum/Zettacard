#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for data/dora_incident_pilot_DRAFT.json (module `dora_incident`).

DRAFT ONLY - not wired into build_modules.py / modules_manifest.json.
Schema mirrors data/kartellrecht_pilot.json field-for-field and key-for-key.
All German text uses real umlauts (ae/oe/ue/ss transliteration is a defect here).
"""
import json
import os
import re
import sys

TOPICS = {
    "vorfallmanagement": "Vorfallmanagement und Erkennung",
    "klassifizierung": "Klassifizierung und Wesentlichkeitsschwellen",
    "meldefristen": "Meldefristen und Meldekaskade",
    "meldeinhalt": "Meldeinhalte, Vorlagen und Verfahren",
}

Q = []


def q(tc, n, legal, points, hs, grund, correct, de_q, de_o, en_q, en_o, de_x, en_x):
    Q.append({
        "id": "dora-incident-%s-%02d" % (tc, n),
        "topic": TOPICS[tc],
        "topic_code": tc,
        "class_scope": ["ALL"],
        "grundstoff": grund,
        "legal_basis": legal,
        "points": points,
        "high_stakes": hs,
        "question_type": "single_choice",
        "image_ref": None,
        "correct": [correct],
        "text": {
            "de": {"question": de_q, "options": de_o},
            "en": {"question": en_q, "options": en_o},
        },
        "explanation": {"de": de_x, "en": en_x},
        "roles": ["all"],
    })


# ---------------------------------------------------------------- Topic 1 ----
q("vorfallmanagement", 1,
  "Art. 17 Abs. 1 und 2 Verordnung (EU) 2022/2554",
  3, False, True, "c",
  "Welche IKT-Ereignisse muss ein Finanzunternehmen nach Art. 17 DORA erfassen?",
  {
    "a": "Nur Vorfaelle, die bereits als schwerwiegend eingestuft wurden",
    "b": "Nur Cyberangriffe durch externe Angreifer",
    "c": "Alle IKT-bezogenen Vorfaelle und alle erheblichen Cyberbedrohungen - unabhaengig davon, ob sie schwerwiegend sind",
    "d": "Nur Vorfaelle, bei denen Kundendaten abgeflossen sind",
  },
  "Which ICT events must a financial entity record under Art. 17 DORA?",
  {
    "a": "Only incidents already classified as major",
    "b": "Only cyber attacks by external threat actors",
    "c": "All ICT-related incidents and all significant cyber threats - regardless of whether they are major",
    "d": "Only incidents involving a leak of client data",
  },
  "Art. 17 Abs. 2 Satz 1 lautet im amtlichen deutschen Wortlaut: 'Finanzunternehmen erfassen alle IKT-bezogenen Vorfaelle und erheblichen Cyberbedrohungen.' Die Erfassungspflicht ist damit deutlich weiter als die Meldepflicht: gemeldet wird nach Art. 19 Abs. 1 nur der als schwerwiegend eingestufte Vorfall, erfasst wird jeder. Praktisch heisst das: das Vorfallregister ist die Grundlage, aus der spaeter die Klassifizierung nach Art. 18, die monatliche Pruefung wiederholter Vorfaelle nach Art. 8 Abs. 2 der Delegierten Verordnung (EU) 2024/1772 und die Ursachenanalyse gespeist werden. Wer nur schwerwiegende Vorfaelle dokumentiert, kann die Wiederholungspruefung strukturell nicht durchfuehren.",
  "Art. 17(2), first sentence, reads verbatim: 'Financial entities shall record all ICT-related incidents and significant cyber threats.' The recording duty is therefore considerably broader than the reporting duty: only an incident classified as major is reported under Art. 19(1), but every incident is recorded. In practice the incident register is the basis for later classification under Art. 18, for the monthly recurring-incident assessment under Art. 8(2) of Delegated Regulation (EU) 2024/1772, and for root-cause analysis. An entity that documents only major incidents structurally cannot perform the recurrence assessment.")

q("vorfallmanagement", 2,
  "Art. 17 Abs. 3 Buchst. a bis f Verordnung (EU) 2022/2554",
  3, False, False, "a",
  "Was muss der Prozess zur Behandlung IKT-bezogener Vorfaelle nach Art. 17 Abs. 3 DORA mindestens leisten?",
  {
    "a": "Fruehwarnindikatoren einsetzen, Verfahren zur Ermittlung, Nachverfolgung, Protokollierung, Kategorisierung und Klassifizierung nach den Kriterien des Art. 18 Abs. 1 einrichten sowie Funktionen und Zustaendigkeiten fuer die verschiedenen Vorfallarten zuweisen",
    "b": "Ausschliesslich eine Rufnummer fuer Stoerungsmeldungen bereitstellen",
    "c": "Ausschliesslich die technische Wiederherstellung des Dienstes regeln; Kommunikation und Eskalation sind nicht Teil des Prozesses",
    "d": "Zustaendigkeiten bewusst offenlassen, damit im Ernstfall flexibel entschieden werden kann",
  },
  "What must the ICT-related incident management process achieve as a minimum under Art. 17(3) DORA?",
  {
    "a": "Put in place early warning indicators, establish procedures to identify, track, log, categorise and classify incidents in accordance with the criteria in Art. 18(1), and assign roles and responsibilities for the different incident types",
    "b": "Merely provide a telephone number for reporting outages",
    "c": "Only govern technical service restoration; communication and escalation are not part of the process",
    "d": "Deliberately leave responsibilities open so that decisions can be taken flexibly in a crisis",
  },
  "Art. 17 Abs. 3 zaehlt sechs Bestandteile auf: Buchst. a Fruehwarnindikatoren; Buchst. b Verfahren zur Ermittlung, Nachverfolgung, Protokollierung, Kategorisierung und Klassifizierung 'entsprechend ihrer Prioritaet und Schwere und entsprechend der Kritikalitaet der betroffenen Dienste entsprechend den in Artikel 18 Absatz 1 genannten Kriterien'; Buchst. c Zuweisung von Funktionen und Zustaendigkeiten, 'die bei verschiedenen Arten von IKT-bezogenen Vorfaellen und -Szenarien aktiviert werden muessen'; Buchst. d Kommunikations- und Eskalationsplaene einschliesslich Kundenbenachrichtigung; Buchst. e Meldung an die hoehere Fuehrungsebene und Information der Geschaeftsleitung bei zumindest schwerwiegenden Vorfaellen; Buchst. f Reaktionsverfahren. Die Klassifizierungslogik ist also bereits im Prozess zu verankern - nicht erst im Ernstfall zu erfinden.",
  "Art. 17(3) enumerates six components: (a) early warning indicators; (b) procedures to identify, track, log, categorise and classify incidents 'according to their priority and severity and according to the criticality of the services impacted, in accordance with the criteria set out in Article 18(1)'; (c) assignment of roles and responsibilities 'that need to be activated for different ICT-related incident types and scenarios'; (d) communication and escalation plans including client notification; (e) reporting at least major incidents to relevant senior management and informing the management body; (f) incident response procedures. The classification logic must therefore be built into the process in advance - not improvised during the crisis.")

q("vorfallmanagement", 3,
  "Art. 17 Abs. 2 Verordnung (EU) 2022/2554",
  3, False, False, "b",
  "Ihr SOC stellt nach einem Ausfall den Dienst per Failover wieder her und schliesst das Ticket mit dem Vermerk 'Dienst wieder verfuegbar'. Genuegt das den Anforderungen des Art. 17 DORA?",
  {
    "a": "Ja - sobald der Dienst wieder laeuft, ist der Vorfall abgeschlossen",
    "b": "Nein - Art. 17 Abs. 2 verlangt zusaetzlich eine kohaerente und integrierte Weiterverfolgung, bei der Ursachen ermittelt, dokumentiert und angegangen werden, um erneutes Auftreten zu verhindern",
    "c": "Ja, sofern der Ausfall kuerzer als zwei Stunden gedauert hat",
    "d": "Nein, aber nur dann, wenn der Vorfall bereits an die Aufsicht gemeldet wurde",
  },
  "After an outage your SOC restores the service via failover and closes the ticket with the note 'service available again'. Does that satisfy Art. 17 DORA?",
  {
    "a": "Yes - once the service is running again the incident is closed",
    "b": "No - Art. 17(2) additionally requires consistent and integrated follow-up ensuring that root causes are identified, documented and addressed in order to prevent recurrence",
    "c": "Yes, provided the outage lasted less than two hours",
    "d": "No, but only where the incident has already been reported to the supervisor",
  },
  "Art. 17 Abs. 2 Satz 2 im amtlichen Wortlaut: 'Finanzunternehmen richten angemessene Verfahren und Prozesse ein, um die kohaerente und integrierte Ueberwachung, Handhabung und Weiterverfolgung IKT-bezogener Vorfaelle zu gewaehrleisten, um sicherzustellen, dass Ursachen ermittelt, dokumentiert und angegangen werden, um das Auftreten solcher Vorfaelle zu verhindern.' Wiederherstellung ist Reaktion, nicht Weiterverfolgung. Die Zwei-Stunden-Marke in Antwort c ist eine Wesentlichkeitsschwelle fuer die Klassifizierung (Art. 9 Abs. 3 Buchst. b der Delegierten Verordnung (EU) 2024/1772), keine Grenze fuer die Ursachenanalyse - und die Ursachenanalyse ist ausserdem Voraussetzung der Abschlussmeldung nach Art. 4 der Delegierten Verordnung (EU) 2025/301.",
  "Art. 17(2), second sentence, verbatim: 'Financial entities shall establish appropriate procedures and processes to ensure a consistent and integrated monitoring, handling and follow-up of ICT-related incidents, to ensure that root causes are identified, documented and addressed in order to prevent the occurrence of such incidents.' Restoration is response, not follow-up. The two-hour mark in option (c) is a materiality threshold for classification (Art. 9(3)(b) of Delegated Regulation (EU) 2024/1772), not a limit on root-cause work - and root-cause analysis is in any event the precondition for the final report under Art. 4 of Delegated Regulation (EU) 2025/301.")

q("vorfallmanagement", 4,
  "Art. 16 Abs. 1 Verordnung (EU) 2022/2554 i.V.m. Art. 8 Abs. 2 Delegierte Verordnung (EU) 2024/1772",
  4, False, False, "d",
  "Ein kleines, nicht verflochtenes Wertpapierdienstleistungsunternehmen faellt unter den vereinfachten IKT-Risikomanagementrahmen des Art. 16 DORA. Was folgt daraus fuer die Meldung von IKT-Vorfaellen (Kapitel III, Art. 17 bis 23)?",
  {
    "a": "Kapitel III gilt fuer dieses Unternehmen ueberhaupt nicht",
    "b": "Es gilt eine verlaengerte Erstmeldefrist von 72 Stunden",
    "c": "Es genuegt eine jaehrliche Sammelmeldung aller Vorfaelle",
    "d": "Kapitel III gilt unveraendert - Art. 16 Abs. 1 nimmt ausdruecklich nur die Artikel 5 bis 15 aus; die einzige ausdrueckliche Erleichterung in diesem Bereich betrifft die Zusammenfassung wiederholter Vorfaelle nach Art. 8 Abs. 2 der Delegierten Verordnung (EU) 2024/1772",
  },
  "A small and non-interconnected investment firm falls under the simplified ICT risk management framework in Art. 16 DORA. What follows for ICT incident reporting (Chapter III, Arts. 17-23)?",
  {
    "a": "Chapter III does not apply to that firm at all",
    "b": "An extended initial-notification deadline of 72 hours applies",
    "c": "An annual aggregated report of all incidents is sufficient",
    "d": "Chapter III applies unchanged - Art. 16(1) expressly disapplies only Articles 5 to 15; the only express relief in this area concerns the aggregation of recurring incidents under Art. 8(2) of Delegated Regulation (EU) 2024/1772",
  },
  "Art. 16 Abs. 1 Unterabs. 1 benennt die ausgenommenen Vorschriften abschliessend: 'Die Artikel 5 bis 15 dieser Verordnung gelten nicht fuer kleine und nicht verflochtene Wertpapierfirmen ...'. Kapitel III (Art. 17 bis 23) ist davon nicht erfasst - Erfassungs-, Klassifizierungs- und Meldepflichten gelten also in vollem Umfang, ebenso die Fristen der Delegierten Verordnung (EU) 2025/301. Die einzige textlich verankerte Erleichterung steht in Art. 8 Abs. 2 letzter Unterabsatz der Delegierten Verordnung (EU) 2024/1772: 'Dieser Absatz gilt nicht fuer Kleinstunternehmen und die in Artikel 16 Absatz 1 der Verordnung (EU) 2022/2554 genannten Finanzunternehmen.' Diese Ausnahme betrifft ausschliesslich die Zusammenfassung wiederholter Vorfaelle, nicht die Meldepflicht als solche. Anmerkung fuer die Rechtspruefung: Erwaegungsgrund 5 der Delegierten Verordnung (EU) 2025/301 nennt Verhaeltnismaessigkeit gegenueber Kleinstunternehmen als Motiv der Fristenregelung, setzt aber keine abweichende Frist.",
  "Art. 16(1), first subparagraph, lists the disapplied provisions exhaustively: 'Articles 5 to 15 of this Regulation shall not apply to small and non-interconnected investment firms ...'. Chapter III (Arts. 17-23) is not among them, so recording, classification and reporting duties apply in full, as do the time limits in Delegated Regulation (EU) 2025/301. The only relief anchored in the text is Art. 8(2), final subparagraph, of Delegated Regulation (EU) 2024/1772: 'This paragraph does not apply to microenterprises and to financial entities listed in Article 16(1) of Regulation (EU) 2022/2554.' That carve-out concerns only the aggregation of recurring incidents, not the reporting duty itself. Note for legal review: recital 5 of Delegated Regulation (EU) 2025/301 cites proportionality towards microenterprises as a motive for the timing rules but does not set a different deadline.")

q("vorfallmanagement", 5,
  "Art. 19 Abs. 3 Verordnung (EU) 2022/2554",
  4, True, False, "a",
  "Wann muessen Kunden ueber einen schwerwiegenden IKT-bezogenen Vorfall unterrichtet werden?",
  {
    "a": "Wenn der Vorfall Auswirkungen auf die finanziellen Interessen von Kunden hat - dann unverzueglich, sobald das Finanzunternehmen hiervon Kenntnis erlangt hat, und zwar ueber den Vorfall und die zur Minderung ergriffenen Massnahmen",
    "b": "Erst nachdem die Abschlussmeldung an die zustaendige Behoerde uebermittelt wurde",
    "c": "Nur wenn die zustaendige Behoerde die Kundeninformation anordnet",
    "d": "Bei jedem schwerwiegenden Vorfall, unabhaengig davon, ob finanzielle Interessen von Kunden beruehrt sind",
  },
  "When must clients be informed about a major ICT-related incident?",
  {
    "a": "Where the incident has an impact on the financial interests of clients - then without undue delay as soon as the financial entity becomes aware of it, informing them about the incident and about the mitigating measures taken",
    "b": "Only after the final report has been submitted to the competent authority",
    "c": "Only where the competent authority orders client notification",
    "d": "For every major incident, irrespective of whether clients' financial interests are affected",
  },
  "Art. 19 Abs. 3 Unterabs. 1 im amtlichen deutschen Wortlaut: 'Wenn ein schwerwiegender IKT-bezogener Vorfall auftritt und Auswirkungen auf die finanziellen Interessen von Kunden hat, unterrichten die Finanzunternehmen, sobald sie hiervon Kenntnis erlangt haben, ihre Kunden unverzueglich ueber den schwerwiegenden IKT-bezogenen Vorfall und die Massnahmen, die ergriffen wurden, um die nachteiligen Auswirkungen eines solchen Vorfalls zu mindern.' Zwei Punkte fuer die Praxis: erstens ist die Kundeninformation eine eigenstaendige Pflicht, die neben der Aufsichtsmeldung laeuft und nicht auf deren Freigabe wartet; zweitens hat sie einen eigenen Ausloeser - die Beruehrung finanzieller Kundeninteressen -, weshalb nicht jeder schwerwiegende Vorfall eine Kundeninformation nach sich zieht. Bei einer erheblichen Cyberbedrohung sind nach Unterabs. 2 gegebenenfalls potenziell betroffene Kunden ueber angemessene Schutzmassnahmen zu unterrichten.",
  "Art. 19(3), first subparagraph, verbatim: 'Where a major ICT-related incident occurs and has an impact on the financial interests of clients, financial entities shall, without undue delay as soon as they become aware of it, inform their clients about the major ICT-related incident and about the measures that have been taken to mitigate the adverse effects of such incident.' Two practical points: first, client information is a standalone duty that runs alongside the supervisory report and does not wait for supervisory clearance; second, it has its own trigger - impact on clients' financial interests - so not every major incident produces a client notification. For a significant cyber threat, the second subparagraph requires informing potentially affected clients, where applicable, of appropriate protection measures.")

# ---------------------------------------------------------------- Topic 2 ----
q("klassifizierung", 1,
  "Art. 8 Abs. 1 Delegierte Verordnung (EU) 2024/1772 i.V.m. Art. 18 Abs. 1 und Art. 19 Abs. 1 Verordnung (EU) 2022/2554",
  4, True, True, "c",
  "Nach welchem Test gilt ein IKT-bezogener Vorfall als schwerwiegend im Sinne des Art. 19 Abs. 1 DORA?",
  {
    "a": "Sobald zwei beliebige der sechs Kriterien des Art. 18 Abs. 1 DORA irgendwie beruehrt sind",
    "b": "Sobald mindestens drei Wesentlichkeitsschwellen erreicht sind",
    "c": "Wenn kritische Dienste im Sinne des Art. 6 der Delegierten Verordnung (EU) 2024/1772 beeintraechtigt sind und zusaetzlich entweder allein die Schwelle nach Art. 9 Abs. 5 Buchst. b oder aber zwei oder mehr der uebrigen Wesentlichkeitsschwellen erreicht sind",
    "d": "Wenn die Geschaeftsleitung den Vorfall nach eigenem Ermessen als schwerwiegend bezeichnet",
  },
  "Under what test does an ICT-related incident count as major for the purposes of Art. 19(1) DORA?",
  {
    "a": "As soon as any two of the six criteria in Art. 18(1) DORA are somehow touched",
    "b": "As soon as at least three materiality thresholds are met",
    "c": "Where critical services within the meaning of Art. 6 of Delegated Regulation (EU) 2024/1772 have been affected and, in addition, either the threshold in Art. 9(5)(b) alone is met or two or more of the other materiality thresholds are met",
    "d": "Where senior management decides at its own discretion to label the incident major",
  },
  "Art. 8 Abs. 1 der Delegierten Verordnung (EU) 2024/1772 im amtlichen deutschen Wortlaut: 'Ein Vorfall wird fuer die Zwecke von Artikel 19 Absatz 1 der Verordnung (EU) 2022/2554 als schwerwiegender Vorfall angesehen, wenn die in Artikel 6 genannten kritischen Dienste beeintraechtigt und eine der folgenden beiden Bedingungen erfuellt ist: a) Die in Artikel 9 Absatz 5 Buchstabe b genannte Wesentlichkeitsschwelle ist erreicht; b) zwei oder mehr der in Artikel 9 Absaetze 1 bis 6 genannten anderen Wesentlichkeitsschwellen sind erreicht.' Entscheidend ist die Struktur: die Beeintraechtigung kritischer Dienste ist ein vorgeschaltetes Eingangstor und zaehlt nicht als eine der zwei Schwellen mit. Art. 6 definiert 'kritische Dienste' dabei weiter als der Alltagssprachgebrauch - erfasst sind Buchst. a IKT-Dienste und Systeme zur Unterstuetzung kritischer oder wichtiger Funktionen, Buchst. b zulassungspflichtige oder beaufsichtigte Finanzdienstleistungen und Buchst. c ein erfolgreicher boeswilliger und unbefugter Zugriff auf Netzwerk- und Informationssysteme.",
  "Art. 8(1) of Delegated Regulation (EU) 2024/1772 verbatim: 'An incident shall be considered a major incident for the purposes of Article 19(1) of Regulation (EU) 2022/2554 where it has affected critical services as referred to in Article 6 and where either of the following conditions is fulfilled: (a) the materiality threshold referred to in Article 9(5), point (b), is met; (b) two or more of the other materiality thresholds referred to in Articles 9(1) to (6) are met.' The structure is what matters: the critical-services element is a gate that must be passed first and does not itself count as one of the two thresholds. Art. 6 defines 'critical services' more broadly than everyday usage - it covers (a) ICT services and systems supporting critical or important functions, (b) financial services requiring authorisation, registration or subject to supervision, and (c) a successful, malicious and unauthorised access to network and information systems.")

q("klassifizierung", 2,
  "Art. 9 Abs. 3 i.V.m. Art. 3 Delegierte Verordnung (EU) 2024/1772",
  3, False, False, "b",
  "Welche Zeitschwellen gelten fuer das Klassifizierungskriterium 'Dauer und Ausfallzeiten'?",
  {
    "a": "Dauer ueber 4 Stunden oder Ausfallzeit ueber 1 Stunde",
    "b": "Dauer des Vorfalls ueber 24 Stunden oder Ausfallzeit ueber 2 Stunden bei IKT-Diensten zur Unterstuetzung kritischer oder wichtiger Funktionen",
    "c": "Dauer ueber 2 Stunden oder Ausfallzeit ueber 24 Stunden",
    "d": "Es gibt keine festen Zeitschwellen; die Bewertung ist rein qualitativ",
  },
  "What time thresholds apply to the classification criterion 'duration and service downtime'?",
  {
    "a": "Duration over 4 hours or downtime over 1 hour",
    "b": "Incident duration longer than 24 hours, or service downtime longer than 2 hours for ICT services supporting critical or important functions",
    "c": "Duration over 2 hours or downtime over 24 hours",
    "d": "There are no fixed time thresholds; the assessment is purely qualitative",
  },
  "Art. 9 Abs. 3 der Delegierten Verordnung (EU) 2024/1772: 'a) Der Vorfall dauert mehr als 24 Stunden; b) die Ausfallzeiten bei IKT-Diensten zur Unterstuetzung kritischer oder wichtiger Funktionen betragen mehr als zwei Stunden.' Die beiden Groessen werden unterschiedlich gemessen (Art. 3): die Dauer laeuft vom Eintritt des Vorfalls bis zur Behebung - laesst sich der Eintritt nicht bestimmen, ab Feststellung, und bei nachtraeglich erkanntem frueherem Eintritt ab dem Zeitpunkt der Protokollierung in Logs oder anderen Datenquellen. Die Ausfallzeit laeuft ab dem Moment, in dem der Dienst fuer Kunden, Gegenparteien oder interne bzw. externe Nutzer ganz oder teilweise nicht verfuegbar ist, bis zur Wiederherstellung des vorherigen Serviceniveaus; verzoegert sich die Leistungserbringung darueber hinaus, laeuft sie bis zur vollstaendigen Erbringung. Ist die Behebung noch offen, sind Schaetzungen zu verwenden - Unsicherheit ist also kein Grund, die Klassifizierung aufzuschieben.",
  "Art. 9(3) of Delegated Regulation (EU) 2024/1772: '(a) the duration of the incident is longer than 24 hours; (b) the service downtime is longer than 2 hours for ICT services that support critical or important functions.' The two are measured differently (Art. 3): duration runs from the moment the incident occurs until it is resolved - where the moment of occurrence cannot be determined, from detection, and where the entity later becomes aware that the incident occurred earlier, from the moment it is recorded in network or system logs or other data sources. Downtime runs from the moment the service is fully or partially unavailable to clients, financial counterparts or other internal or external users, until the prior service level is restored; where a delay in service provision persists, it runs until that delayed service is fully provided. Where resolution is still open, estimates must be applied - uncertainty is therefore not a reason to defer classification.")

q("klassifizierung", 3,
  "Art. 9 Abs. 1 und 6 Delegierte Verordnung (EU) 2024/1772",
  3, False, False, "d",
  "Welche Werte nennt Art. 9 Abs. 1 der Delegierten Verordnung (EU) 2024/1772 fuer das Kriterium 'Kunden, finanzielle Gegenparteien und Transaktionen'?",
  {
    "a": "Mehr als 1 % der Kunden oder mehr als 1 000 betroffene Kunden",
    "b": "Mehr als 50 % der Kunden oder mehr als 1 Mio. betroffene Kunden",
    "c": "Ausschliesslich einen absoluten Wert von 10 000 betroffenen Kunden",
    "d": "Unter anderem mehr als 10 % aller Kunden der betroffenen Dienstleistung, mehr als 100 000 betroffene Kunden, mehr als 30 % der finanziellen Gegenparteien sowie mehr als 10 % der taeglichen durchschnittlichen Zahl oder des taeglichen Durchschnittswerts der Transaktionen",
  },
  "What figures does Art. 9(1) of Delegated Regulation (EU) 2024/1772 set for the criterion 'clients, financial counterparts and transactions'?",
  {
    "a": "More than 1 % of clients or more than 1,000 affected clients",
    "b": "More than 50 % of clients or more than 1 million affected clients",
    "c": "Only an absolute figure of 10,000 affected clients",
    "d": "Among others: more than 10 % of all clients using the affected service, more than 100,000 affected clients, more than 30 % of financial counterparts, and more than 10 % of the daily average number or daily average value of transactions",
  },
  "Art. 9 Abs. 1 nennt sechs alternative Bedingungen; eine genuegt, damit diese Schwelle als erreicht gilt: Buchst. a mehr als 10 % aller Kunden, die die betroffene Dienstleistung nutzen; Buchst. b mehr als 100 000 betroffene Kunden; Buchst. c mehr als 30 % der finanziellen Gegenparteien; Buchst. d mehr als 10 % der taeglichen durchschnittlichen Zahl der Transaktionen; Buchst. e mehr als 10 % des taeglichen Durchschnittswerts der Transaktionen; Buchst. f Betroffenheit von Kunden oder Gegenparteien, die nach Art. 1 Abs. 3 als relevant eingestuft wurden. Der Relativwert und der Absolutwert stehen nebeneinander - ein grosses Haus kann die 10-Prozent-Marke verfehlen und trotzdem ueber die 100 000 kommen. Laesst sich die tatsaechliche Zahl nicht bestimmen, ist sie auf Basis vergleichbarer Referenzzeitraeume zu schaetzen. Die wirtschaftliche Schwelle ist davon getrennt und liegt nach Art. 9 Abs. 6 bei Kosten und Verlusten, die 100 000 EUR uebersteigen oder wahrscheinlich uebersteigen werden.",
  "Art. 9(1) lists six alternative conditions; meeting one suffices for the threshold: (a) more than 10 % of all clients using the affected service; (b) more than 100,000 affected clients; (c) more than 30 % of financial counterparts; (d) more than 10 % of the daily average number of transactions; (e) more than 10 % of the daily average value of transactions; (f) clients or financial counterparts identified as relevant under Art. 1(3) have been affected. The relative and absolute figures sit side by side - a large institution may fall short of the 10 % mark and still exceed 100,000. Where the actual figure cannot be determined, it must be estimated from comparable reference periods. The economic threshold is separate and sits, under Art. 9(6), at costs and losses that have exceeded or are likely to exceed EUR 100,000.")

q("klassifizierung", 4,
  "Art. 6 Buchst. c i.V.m. Art. 8 Abs. 1 Buchst. a und Art. 9 Abs. 5 Buchst. b Delegierte Verordnung (EU) 2024/1772",
  4, True, False, "a",
  "Ein Angreifer hat sich erfolgreich und unbefugt Zugang zu einem Server verschafft, der eine kritische Funktion unterstuetzt; der Zugriff kann zu Datenverlusten fuehren. Der Dienst war zu keinem Zeitpunkt gestoert, Kunden sind nicht betroffen, die Kosten liegen deutlich unter 100 000 EUR. Kann der Vorfall trotzdem schwerwiegend sein?",
  {
    "a": "Ja - ein erfolgreicher boeswilliger und unbefugter Zugriff erfuellt zugleich das Eingangstor 'kritische Dienste' (Art. 6 Buchst. c) und die Schwelle nach Art. 9 Abs. 5 Buchst. b, die nach Art. 8 Abs. 1 Buchst. a allein ausreicht",
    "b": "Nein - ohne Ausfallzeit und ohne betroffene Kunden kann kein schwerwiegender Vorfall vorliegen",
    "c": "Nein - es fehlt an der wirtschaftlichen Schwelle von 100 000 EUR",
    "d": "Nur wenn zusaetzlich mindestens zwei weitere Wesentlichkeitsschwellen erreicht sind",
  },
  "An attacker has gained successful, unauthorised access to a server supporting a critical function; the access may result in data losses. The service was never disrupted, no clients were affected, and costs are well below EUR 100,000. Can the incident nevertheless be major?",
  {
    "a": "Yes - a successful, malicious and unauthorised access satisfies both the 'critical services' gate (Art. 6(c)) and the threshold in Art. 9(5)(b), which under Art. 8(1)(a) suffices on its own",
    "b": "No - without downtime and without affected clients there can be no major incident",
    "c": "No - the EUR 100,000 economic threshold is not met",
    "d": "Only if at least two further materiality thresholds are also met",
  },
  "Die Kette steht vollstaendig im Verordnungstext. Art. 6 Buchst. c: der Vorfall 'stellt einen erfolgreichen boeswilligen und unbefugten Zugriff auf die Netzwerk- und Informationssysteme des Finanzunternehmens dar oder stellte einen solchen dar'. Art. 9 Abs. 5 Buchst. b: die Schwelle 'Verluste von Daten' ist erreicht, wenn 'ein nicht unter Buchstabe a fallender erfolgreicher boeswilliger und unbefugter Zugriff auf Netzwerk- und Informationssysteme' stattfindet, 'sofern dieser Zugriff zu Verlusten von Daten fuehren kann'. Art. 8 Abs. 1 Buchst. a: allein diese Schwelle genuegt - eine zweite ist nicht erforderlich. Erwaegungsgrund 10 der Delegierten Verordnung (EU) 2024/1772 bestaetigt die Absicht: boeswilliger unbefugter Zugriff auf Systeme, die kritische oder wichtige Funktionen unterstuetzen, 'sollte immer als schwerwiegender Vorfall betrachtet werden'. Fuer SOC-Teams ist das die praktisch wichtigste Konsequenz: eine Intrusion ohne sichtbare Betriebsstoerung ist der Regelfall einer schwerwiegenden Meldung, nicht die Ausnahme.",
  "The whole chain sits in the enacting text. Art. 6(c): the incident 'constitutes or has constituted a successful, malicious and unauthorised access to the network and information systems of the financial entity'. Art. 9(5)(b): the 'data losses' threshold is met where 'any successful, malicious and unauthorised access not covered by point (a) occurs to network and information systems, where such access may result in data losses'. Art. 8(1)(a): that threshold alone suffices - no second threshold is required. Recital 10 of Delegated Regulation (EU) 2024/1772 confirms the intent: malicious, unauthorised access to systems supporting critical or important functions 'should always be considered as major incidents which are to be reported'. For SOC teams this is the most consequential point: an intrusion with no visible service disruption is the normal case for a major report, not the exception.")

q("klassifizierung", 5,
  "Art. 8 Abs. 2 Delegierte Verordnung (EU) 2024/1772 i.V.m. Art. 3 Durchfuehrungsverordnung (EU) 2025/302",
  3, False, False, "b",
  "Ihr Zahlungs-Gateway faellt seit Januar viermal wegen desselben Konfigurationsfehlers kurz aus. Kein einzelner Ausfall erreicht fuer sich die Wesentlichkeitsschwellen. Wie ist damit umzugehen?",
  {
    "a": "Solange kein Einzelvorfall die Schwellen erreicht, entsteht keine Meldepflicht",
    "b": "Wiederholte Vorfaelle gelten zusammengenommen als ein schwerwiegender Vorfall, wenn sie innerhalb von sechs Monaten mindestens zweimal aufgetreten sind, dieselbe offensichtliche Ursache haben und zusammengenommen die Kriterien erfuellen; die Pruefung ist monatlich vorzunehmen und die Meldung erfolgt in aggregierter Form",
    "c": "Wiederholte Vorfaelle sind einmal jaehrlich in einer Sammelmeldung zusammenzufassen",
    "d": "Wiederholte Vorfaelle sind nur bei Cyberangriffen zu betrachten",
  },
  "Your payment gateway has failed briefly four times since January because of the same configuration fault. No single outage meets the materiality thresholds on its own. How must this be handled?",
  {
    "a": "As long as no individual incident meets the thresholds, no reporting duty arises",
    "b": "Recurring incidents are treated collectively as one major incident where they have occurred at least twice within six months, have the same apparent root cause and collectively fulfil the criteria; the assessment must be performed monthly and the report is submitted in aggregated form",
    "c": "Recurring incidents must be summarised once a year in a collective report",
    "d": "Recurring incidents only need to be considered for cyber attacks",
  },
  "Art. 8 Abs. 2 der Delegierten Verordnung (EU) 2024/1772 nennt drei kumulative Bedingungen: Buchst. a mindestens zweimal innerhalb von sechs Monaten aufgetreten; Buchst. b dieselbe offensichtliche Ursache im Sinne von Art. 20 Abs. 1 Buchst. b DORA; Buchst. c zusammengenommen Erfuellung der Kriterien des Art. 8 Abs. 1. Ausdruecklich angeordnet ist ausserdem: 'Die Finanzunternehmen bewerten das Vorliegen wiederholter Vorfaelle monatlich.' Die Uebermittlung erfolgt nach Art. 3 der Durchfuehrungsverordnung (EU) 2025/302 'in aggregierter Form'. Der Absatz gilt nicht fuer Kleinstunternehmen und fuer Finanzunternehmen nach Art. 16 Abs. 1 DORA. Wichtig fuer die Fristenrechnung: Datenfeld 2.2 der Meldevorlage verlangt bei wiederholten Vorfaellen Datum und Uhrzeit der Feststellung des letzten dieser Vorfaelle.",
  "Art. 8(2) of Delegated Regulation (EU) 2024/1772 sets three cumulative conditions: (a) they have occurred at least twice within 6 months; (b) they have the same apparent root cause as referred to in Art. 20, first subparagraph, point (b), DORA; (c) they collectively fulfil the Art. 8(1) criteria. It also expressly orders: 'Financial entities shall assess the existence of recurring incidents on a monthly basis.' Submission is 'in an aggregated form' under Art. 3 of Implementing Regulation (EU) 2025/302. The paragraph does not apply to microenterprises or to financial entities listed in Art. 16(1) DORA. Relevant for the clock: template data field 2.2 requires, for recurring incidents, the date and time at which the last of those incidents was detected.")

# ---------------------------------------------------------------- Topic 3 ----
q("meldefristen", 1,
  "Art. 5 Abs. 1 Buchst. a Delegierte Verordnung (EU) 2025/301 i.V.m. Art. 19 Abs. 4 und Art. 20 Verordnung (EU) 2022/2554",
  4, True, True, "d",
  "Welche Frist gilt fuer die Erstmeldung eines schwerwiegenden IKT-bezogenen Vorfalls an die zustaendige Behoerde?",
  {
    "a": "Vier Stunden ab Entdeckung des Vorfalls",
    "b": "Vier Stunden ab Einstufung als schwerwiegend - eine weitere Frist besteht daneben nicht",
    "c": "24 Stunden ab Einstufung als schwerwiegend",
    "d": "So frueh wie moeglich, in jedem Fall aber innerhalb von vier Stunden nach der Einstufung als schwerwiegend und spaetestens 24 Stunden nach dem Zeitpunkt, zu dem das Finanzunternehmen Kenntnis von dem Vorfall erlangt hat",
  },
  "What deadline applies to the initial notification of a major ICT-related incident to the competent authority?",
  {
    "a": "Four hours from detection of the incident",
    "b": "Four hours from classification as major - no other time limit applies alongside it",
    "c": "24 hours from classification as major",
    "d": "As early as possible, but in any case within four hours from the classification of the incident as major and no later than 24 hours from the moment the financial entity became aware of the incident",
  },
  "Art. 5 Abs. 1 Buchst. a der Delegierten Verordnung (EU) 2025/301 im amtlichen deutschen Wortlaut: 'bei der Erstmeldung: so frueh wie moeglich, in jedem Fall aber innerhalb von vier Stunden nach Einstufung des IKT-bezogenen Vorfalls als schwerwiegend und spaetestens 24 Stunden nach dem Zeitpunkt, zu dem das Finanzunternehmen Kenntnis von dem IKT-bezogenen Vorfall erlangt hat'. Englisch: '... within four hours from the classification of the ICT-related incident as a major ICT-related incident and no later than 24 hours from the moment the financial entity has become aware of the ICT-related incident.' Es handelt sich um zwei nebeneinander stehende Fristen, verbunden durch 'und', nicht um eine Frist mit einem Anhaltspunkt: die frueher ablaufende ist massgeblich. Antwort a ist die klassische Fehlvorstellung ('Vier-Stunden-Regel ab Entdeckung'); Antwort b unterschlaegt die 24-Stunden-Aussengrenze. Zur Einordnung: die DORA-Grundverordnung selbst enthaelt keine einzige Stundenangabe zur Meldung - Art. 19 Abs. 4 verweist ausdruecklich auf die 'innerhalb der in Artikel 20 Absatz 1 Buchstabe a Ziffer ii festzulegenden Fristen', und diese Fristen stehen erst in der Delegierten Verordnung (EU) 2025/301.",
  "Art. 5(1)(a) of Delegated Regulation (EU) 2025/301 verbatim: 'for the initial report: as early as possible, but in any case, within four hours from the classification of the ICT-related incident as a major ICT-related incident and no later than 24 hours from the moment the financial entity has become aware of the ICT-related incident'. These are two time limits standing side by side, joined by 'and' - not one limit with a reference point: whichever expires first governs. Option (a) is the classic misconception ('four-hour rule from detection'); option (b) drops the 24-hour outer limit. For context: the DORA base Regulation contains no hour figure for reporting at all - Art. 19(4) expressly refers to 'the time limits to be laid down in accordance with Article 20, first paragraph, point (a), point (ii)', and those time limits appear only in Delegated Regulation (EU) 2025/301.")

q("meldefristen", 2,
  "Art. 5 Abs. 1 Buchst. a i.V.m. Art. 5 Abs. 2 Delegierte Verordnung (EU) 2025/301",
  4, True, False, "c",
  "Ihr SOC erlangt am Montag um 08:00 Uhr Kenntnis von einem Vorfall. Die formale Einstufung als schwerwiegend erfolgt am Dienstag um 06:00 Uhr. Wann laeuft die Frist fuer die Erstmeldung ab?",
  {
    "a": "Dienstag, 10:00 Uhr - vier Stunden nach der Einstufung",
    "b": "Dienstag, 12:00 Uhr",
    "c": "Dienstag, 08:00 Uhr - die 24-Stunden-Grenze ab Kenntniserlangung laeuft frueher ab als die Vier-Stunden-Frist ab Einstufung, und beide Fristen des Art. 5 Abs. 1 Buchst. a gelten nebeneinander",
    "d": "Mittwoch, 06:00 Uhr",
  },
  "Your SOC becomes aware of an incident at 08:00 on Monday. Formal classification as major happens at 06:00 on Tuesday. When does the initial-notification deadline expire?",
  {
    "a": "Tuesday 10:00 - four hours after classification",
    "b": "Tuesday 12:00",
    "c": "Tuesday 08:00 - the 24-hour limit from becoming aware expires earlier than the four-hour limit from classification, and both limbs of Art. 5(1)(a) apply side by side",
    "d": "Wednesday 06:00",
  },
  "Rechnung: vier Stunden ab Einstufung ergibt Dienstag 10:00 Uhr; 24 Stunden ab Kenntniserlangung ergibt Dienstag 08:00 Uhr. Da Art. 5 Abs. 1 Buchst. a beide Fristen mit 'und' verknuepft, ist die frueher endende massgeblich - im Beispiel bleiben also nach der Einstufung nur zwei Stunden. Bestaetigt wird diese Lesart durch Art. 5 Abs. 2: dieser Absatz stellt allein fuer den Fall, dass die Einstufung erst nach Ablauf der 24 Stunden erfolgt, wieder auf die Vier-Stunden-Frist ab - er waere ueberfluessig, wenn die 24-Stunden-Grenze ohnehin nachrangig waere. Betriebliche Konsequenz: die Vier-Stunden-Frist ist keine Planungsgroesse. Wer die Klassifizierung an das Ende des Kenntnistages legt, verkuerzt sich die eigene Meldefrist. PRUEFHINWEIS: die Verrechnung beider Fristen ist eine Auslegung des Wortlauts und im Dossier bewusst als Tier B gefuehrt.",
  "The arithmetic: four hours from classification gives Tuesday 10:00; 24 hours from becoming aware gives Tuesday 08:00. Because Art. 5(1)(a) joins the two with 'and', the one expiring earlier governs - in this example only two hours remain after classification. That reading is confirmed by Art. 5(2), which restores the four-hour limit only for the case where classification happens after the 24 hours have already run; it would be redundant if the 24-hour limb were subordinate anyway. Operational consequence: the four-hour limit is not a planning figure. Pushing classification to the end of the day on which you became aware shortens your own reporting window. REVIEW NOTE: the interaction of the two limbs is an interpretation of the wording and is deliberately recorded as Tier B in the dossier.")

q("meldefristen", 3,
  "Art. 5 Abs. 2 Delegierte Verordnung (EU) 2025/301",
  3, False, False, "a",
  "Ein Vorfall wird erst am vierten Tag nach Kenntniserlangung als schwerwiegend eingestuft, weil die Auswirkungen zunaechst nicht absehbar waren. Welche Frist gilt dann fuer die Erstmeldung?",
  {
    "a": "Vier Stunden ab der Einstufung als schwerwiegend - Art. 5 Abs. 2 der Delegierten Verordnung (EU) 2025/301 regelt genau diesen Fall ausdruecklich",
    "b": "Die Frist ist bereits abgelaufen; eine Erstmeldung ist nicht mehr vorgesehen",
    "c": "24 Stunden ab der Einstufung als schwerwiegend",
    "d": "Ein Monat ab Kenntniserlangung",
  },
  "An incident is only classified as major on the fourth day after the entity became aware of it, because the impact was not initially foreseeable. What deadline then applies to the initial notification?",
  {
    "a": "Four hours from classification as major - Art. 5(2) of Delegated Regulation (EU) 2025/301 expressly governs exactly this case",
    "b": "The deadline has already passed; no initial notification is provided for any more",
    "c": "24 hours from classification as major",
    "d": "One month from becoming aware",
  },
  "Art. 5 Abs. 2 im amtlichen deutschen Wortlaut: 'Hat das Finanzunternehmen einen IKT-bezogenen Vorfall nicht innerhalb von 24 Stunden nach dem Zeitpunkt, zu dem es Kenntnis von dem IKT-bezogenen Vorfall erlangt hat, sondern erst zu einem spaeteren Zeitpunkt als schwerwiegend eingestuft, uebermittelt es die Erstmeldung innerhalb von vier Stunden, nachdem es den IKT-bezogenen Vorfall als schwerwiegend eingestuft hat.' Die Meldepflicht entfaellt also nicht - sie knuepft dann allein an die Einstufung an. Das ist aber kein Freibrief fuer spaete Klassifizierung: Art. 17 Abs. 3 Buchst. b DORA verlangt eingerichtete Klassifizierungsverfahren, und die Meldevorlage nach der Durchfuehrungsverordnung (EU) 2025/302 verlangt in den Feldern 2.2 und 2.3 sowohl den Zeitpunkt der Kenntnisnahme als auch den der Einstufung. Ein grosser Abstand zwischen beiden Zeitstempeln ist fuer die Aufsicht unmittelbar sichtbar.",
  "Art. 5(2) verbatim: 'Where the financial entity has not classified an ICT-related incident as major within 24 hours from the moment the financial entity has become aware of the ICT-related incident but classifies that ICT-related incident as major at a later stage, the financial entity shall submit the initial notification within four hours from the classification of the ICT-related incident as a major incident.' The duty does not lapse - it simply attaches to classification alone. That is not a licence for late classification, though: Art. 17(3)(b) DORA requires established classification procedures, and the reporting template under Implementing Regulation (EU) 2025/302 requires, in fields 2.2 and 2.3, both the time of becoming aware and the time of classification. A wide gap between the two timestamps is immediately visible to the supervisor.")

q("meldefristen", 4,
  "Art. 5 Abs. 1 Buchst. b und c Delegierte Verordnung (EU) 2025/301 i.V.m. Art. 19 Abs. 4 Buchst. b und c Verordnung (EU) 2022/2554",
  4, True, False, "b",
  "Woran knuepfen die Fristen fuer Zwischen- und Abschlussmeldung an?",
  {
    "a": "Zwischenmeldung 72 Stunden nach der Einstufung als schwerwiegend, Abschlussmeldung einen Monat nach dem Vorfall",
    "b": "Zwischenmeldung spaetestens 72 Stunden nach Uebermittlung der Erstmeldung - auch dann, wenn sich Status oder Handhabung des Vorfalls nicht geaendert haben; Abschlussmeldung spaetestens einen Monat nach der Zwischenmeldung bzw. nach der letzten aktualisierten Zwischenmeldung",
    "c": "Beide Meldungen werden erst faellig, wenn die Ursachenanalyse abgeschlossen ist",
    "d": "Es bestehen keine Fristen; Zwischen- und Abschlussmeldung erfolgen nur auf Aufforderung der Behoerde",
  },
  "What are the intermediate and final report deadlines anchored to?",
  {
    "a": "Intermediate report 72 hours after classification as major; final report one month after the incident",
    "b": "Intermediate report at the latest within 72 hours from submission of the initial notification - even where the status or handling of the incident has not changed; final report no later than one month after the intermediate report or, where applicable, after the latest updated intermediate report",
    "c": "Both only fall due once root-cause analysis has been completed",
    "d": "There are no deadlines; intermediate and final reports are submitted only upon request of the authority",
  },
  "Art. 5 Abs. 1 Buchst. b der Delegierten Verordnung (EU) 2025/301: 'bei der Zwischenmeldung: spaetestens 72 Stunden nach Uebermittlung der Erstmeldung, auch wenn sich gemaess Artikel 19 Absatz 4 Buchstabe b der Verordnung (EU) 2022/2554 der Status oder die Handhabung des Vorfalls nicht geaendert hat. Die Finanzunternehmen uebermitteln unverzueglich etwaige aktualisierte Zwischenmeldungen, in jedem Fall aber, sobald der regulaere Geschaeftsbetrieb wiederaufgenommen wurde'. Buchst. c: 'bei der Abschlussmeldung: spaetestens einen Monat nach Uebermittlung der Zwischenmeldung oder gegebenenfalls nach der letzten aktualisierten Zwischenmeldung.' Zwei haeufige Fehler stecken in Antwort a: der Anker der 72 Stunden ist die Uebermittlung der Erstmeldung, nicht die Einstufung, und der Anker des Monats ist die Zwischenmeldung, nicht der Vorfall. Beachtenswert ist zudem das Verhaeltnis zur Grundverordnung: Art. 19 Abs. 4 Buchst. b DORA knuepft die Zwischenmeldung dem Wortlaut nach an eine erhebliche Statusaenderung - die Delegierte Verordnung stellt ausdruecklich klar, dass die 72-Stunden-Frist auch ohne jede Aenderung laeuft.",
  "Art. 5(1)(b) of Delegated Regulation (EU) 2025/301: 'for the intermediate report: at the latest within 72 hours from the submission of the initial notification, even where the status or the handling of the incident have not changed as referred to in Article 19(4), point (b), of Regulation (EU) 2022/2554. Financial entities shall submit an updated intermediate report without undue delay, and in any case when the regular activities have been recovered'. Point (c): 'for the final report: no later than one month after either the submission of the intermediate report, or, where applicable, after the latest updated intermediate report.' Option (a) contains two common errors: the 72-hour anchor is submission of the initial notification, not classification, and the one-month anchor is the intermediate report, not the incident. Note also the relationship to the base Regulation: on its wording, Art. 19(4)(b) DORA ties the intermediate report to a significant change of status - the Delegated Regulation expressly clarifies that the 72-hour clock runs even without any change.")

q("meldefristen", 5,
  "Art. 5 Abs. 4, 5 und 6 Delegierte Verordnung (EU) 2025/301",
  4, True, False, "d",
  "Die Frist fuer eine Erstmeldung faellt auf einen Sonntag. Wer kann sich auf die Wochenend- und Feiertagsregelung des Art. 5 Abs. 4 der Delegierten Verordnung (EU) 2025/301 berufen?",
  {
    "a": "Alle Finanzunternehmen ohne Ausnahme",
    "b": "Nur Kreditinstitute",
    "c": "Niemand - die Regelung betrifft ausschliesslich die Abschlussmeldung",
    "d": "Grundsaetzlich alle Finanzunternehmen; die Meldung darf dann bis 12.00 Uhr des darauffolgenden Arbeitstages erfolgen. Fuer Erst- und Zwischenmeldungen gilt sie jedoch nicht fuer Kreditinstitute, zentrale Gegenparteien, Betreiber von Handelsplaetzen und Finanzunternehmen, die nach Art. 3 der Richtlinie (EU) 2022/2555 als wesentliche oder wichtige Einrichtungen eingestuft sind",
  },
  "The deadline for an initial notification falls on a Sunday. Who can rely on the weekend and bank-holiday rule in Art. 5(4) of Delegated Regulation (EU) 2025/301?",
  {
    "a": "All financial entities without exception",
    "b": "Credit institutions only",
    "c": "Nobody - the rule concerns the final report only",
    "d": "In principle all financial entities; the report may then be submitted by noon of the next working day. For initial notifications and intermediate reports, however, it does not apply to credit institutions, central counterparties, operators of trading venues, or financial entities identified as essential or important entities pursuant to Art. 3 of Directive (EU) 2022/2555",
  },
  "Art. 5 Abs. 4: 'Faellt die Frist fuer die Uebermittlung der Erstmeldung, der Zwischenmeldung oder der Abschlussmeldung auf ein Wochenende oder einen Feiertag im Mitgliedstaat des meldenden Finanzunternehmens, so kann das Finanzunternehmen die ... Meldung bis 12.00 Uhr des darauffolgenden Arbeitstages uebermitteln.' Art. 5 Abs. 5 nimmt davon Erst- und Zwischenmeldungen der genannten Institutsgruppen aus - fuer sie gilt die Wochenendregelung also nur noch bei der Abschlussmeldung. Art. 5 Abs. 6 erlaubt den zustaendigen Behoerden zudem, Absatz 4 fuer weitere bedeutende oder systemrelevante Finanzunternehmen auszuschliessen; ein solcher Beschluss ist dem Unternehmen mitzuteilen und gilt nur fuer Vorfaelle nach der Mitteilung. Betrieblich heisst das: die Rufbereitschaft am Wochenende ist fuer Banken, CCPs, Handelsplatzbetreiber und NIS-2-Einrichtungen keine Option, sondern Voraussetzung der Fristenwahrung.",
  "Art. 5(4): 'Where the time limit for the submission of an initial notification, intermediate report, or a final report falls on a weekend day or a bank holiday in the Member State of the reporting financial entity, the financial entity may submit the ... report by noon of the next working day.' Art. 5(5) excludes initial notifications and intermediate reports by the listed groups - for them the weekend rule survives only for the final report. Art. 5(6) additionally lets competent authorities disapply paragraph 4 for other significant or systemically relevant financial entities; such a decision must be notified to the entity and applies only to incidents reported after that notification. Operationally: weekend on-call cover is not optional for banks, CCPs, trading venue operators and NIS2 entities - it is a precondition for meeting the deadline.")

# ---------------------------------------------------------------- Topic 4 ----
q("meldeinhalt", 1,
  "Art. 2 und Art. 4 Delegierte Verordnung (EU) 2025/301 i.V.m. Art. 1 Abs. 3 Durchfuehrungsverordnung (EU) 2025/302",
  4, True, True, "c",
  "Ihr Team hat einen Vorfall als schwerwiegend eingestuft, kennt aber die Ursache noch nicht und hat noch keine belastbaren Zahlen. Darf die Erstmeldung deshalb zurueckgestellt werden?",
  {
    "a": "Ja - ohne abgeschlossene Ursachenanalyse ist eine Meldung nicht moeglich",
    "b": "Ja, bis der Dienst wiederhergestellt ist und die tatsaechlichen Auswirkungen feststehen",
    "c": "Nein - Art. 2 der Delegierten Verordnung (EU) 2025/301 verlangt fuer die Erstmeldung gerade keine Ursachenanalyse; Angaben zu den Ursachen gehoeren nach Art. 4 in die Abschlussmeldung, und fehlende Werte sind nach Art. 1 Abs. 3 der Durchfuehrungsverordnung (EU) 2025/302 zu schaetzen",
    "d": "Nein, aber die Frist verlaengert sich in diesem Fall auf 72 Stunden",
  },
  "Your team has classified an incident as major but does not yet know the root cause and has no reliable figures. May the initial notification be deferred for that reason?",
  {
    "a": "Yes - no report is possible without a completed root-cause analysis",
    "b": "Yes, until the service is restored and the actual impact is known",
    "c": "No - Art. 2 of Delegated Regulation (EU) 2025/301 precisely does not require root-cause analysis for the initial notification; root causes belong in the final report under Art. 4, and missing values must be estimated under Art. 1(3) of Implementing Regulation (EU) 2025/302",
    "d": "No, but in that case the deadline is extended to 72 hours",
  },
  "Art. 2 der Delegierten Verordnung (EU) 2025/301 listet den Inhalt der Erstmeldung abschliessend: Referenzcode des Vorfalls; Datum und Uhrzeit der Feststellung sowie der Einstufung nach Art. 8 der Delegierten Verordnung (EU) 2024/1772; Beschreibung des Vorfalls; die herangezogenen Einstufungskriterien; betroffene Mitgliedstaaten; wie der Vorfall entdeckt wurde; sofern verfuegbar Angaben zum Ursprung; ob ein Notfallplan aktiviert wurde; gegebenenfalls Angaben zu einer Rueckstufung; sowie sonstige relevante Informationen, sofern verfuegbar. Ursachen ('information about the root causes') verlangt erst Art. 4 fuer die Abschlussmeldung, ebenso die Kosten- und Verlustangaben. Art. 1 Abs. 3 der Durchfuehrungsverordnung (EU) 2025/302 ordnet ausdruecklich an, dass fuer Erst- und Zwischenmeldung Schaetzwerte auf Grundlage anderer verfuegbarer Daten anzugeben sind, wenn genaue Daten zum Meldezeitpunkt nicht vorliegen. Erwaegungsgrund 2 der Delegierten Verordnung (EU) 2025/301 benennt dieselbe Absicht: der Inhalt der Erstmeldung soll bewusst auf die wichtigsten Informationen begrenzt sein, damit die Meldung die laufende Vorfallbearbeitung nicht behindert.",
  "Art. 2 of Delegated Regulation (EU) 2025/301 lists the content of the initial notification exhaustively: the incident reference code; the date and time of detection and of classification pursuant to Art. 8 of Delegated Regulation (EU) 2024/1772; a description of the incident; the criteria relied on for classifying it as major; the Member States impacted; how the incident was discovered; where available, information about its origin; whether a business continuity plan was activated; where applicable, information about reclassification; and, where available, any other relevant information. Root causes are required only by Art. 4, for the final report, as are cost and loss figures. Art. 1(3) of Implementing Regulation (EU) 2025/302 expressly requires estimated values based on other available data for the initial notification and the intermediate report where accurate data are not available at the time of reporting. Recital 2 of Delegated Regulation (EU) 2025/301 states the same intent: the content of the initial notification is deliberately limited to the most significant information so that reporting does not obstruct ongoing incident handling.")

q("meldeinhalt", 2,
  "Art. 5 Abs. 3 Delegierte Verordnung (EU) 2025/301 i.V.m. Art. 4 Durchfuehrungsverordnung (EU) 2025/302",
  4, False, False, "c",
  "Ihr Unternehmen kann eine Meldefrist absehbar nicht einhalten. Was ist zu tun?",
  {
    "a": "Nichts Besonderes - die Meldung wird einfach nachgeholt",
    "b": "Der Vorfall ist vorsorglich auf 'nicht schwerwiegend' zurueckzustufen",
    "c": "Die zustaendige Behoerde ist unverzueglich, spaetestens jedoch innerhalb der jeweiligen Frist zu unterrichten, und die Gruende fuer die Verzoegerung sind anzugeben",
    "d": "Die Meldung ist stattdessen unmittelbar an die zustaendige Europaeische Aufsichtsbehoerde zu richten",
  },
  "Your entity foresees that it will not be able to meet a reporting deadline. What must be done?",
  {
    "a": "Nothing in particular - the report is simply submitted late",
    "b": "The incident must be reclassified to 'non-major' as a precaution",
    "c": "The competent authority must be informed without undue delay and in any case no later than the respective deadline, stating the reasons for the delay",
    "d": "The report must instead be submitted directly to the relevant European Supervisory Authority",
  },
  "Art. 5 Abs. 3 der Delegierten Verordnung (EU) 2025/301: 'Finanzunternehmen, die nicht in der Lage sind, die Erstmeldung, die Zwischenmeldung oder die Abschlussmeldung innerhalb der in Absatz 1 genannten Fristen zu uebermitteln, teilen dies der zustaendigen Behoerde unverzueglich, spaetestens jedoch innerhalb der jeweiligen Fristen fuer die Uebermittlung der Meldung mit und geben die Gruende fuer die Verzoegerung an.' Die Unterrichtung ueber die Verzoegerung unterliegt also derselben Frist wie die Meldung selbst - Schweigen ist keine Option. Parallel dazu regelt Art. 4 der Durchfuehrungsverordnung (EU) 2025/302 den technischen Ausfall: grundsaetzlich sind die von der zustaendigen Behoerde bereitgestellten sicheren elektronischen Kanaele zu nutzen; ist das nicht moeglich, ist die Behoerde im Einvernehmen auf anderem sicheren Weg zu unterrichten und die Meldung auf Verlangen spaeter ueber den sicheren Kanal erneut zu uebermitteln. Auch Art. 19 Abs. 1 Unterabs. 4 DORA sieht fuer den Fall technischer Unmoeglichkeit die Meldung 'auf anderem Wege' vor. Adressat bleibt in allen Faellen die zustaendige nationale Behoerde; die Weiterleitung an EBA, ESMA, EIOPA und EZB erfolgt nach Art. 19 Abs. 6 DORA durch die Behoerde selbst.",
  "Art. 5(3) of Delegated Regulation (EU) 2025/301: 'Financial entities that are unable to submit the initial notification, intermediate report, or final report within the time limits set out in paragraph 1, shall inform the competent authority thereof without undue delay, but no later than the respective time limits for the submission of the notification or report, and shall explain the reasons for the delay.' The notification of delay is therefore subject to the same deadline as the report itself - silence is not an option. In parallel, Art. 4 of Implementing Regulation (EU) 2025/302 governs technical failure: secure electronic channels made available by the competent authority must be used in principle; where that is impossible, the authority must be informed through other secure means in agreement with it, and the report resubmitted through the secure channel on request. Art. 19(1), fourth subparagraph, DORA likewise provides for notification 'via alternative means' where technical impossibility prevents use of the template. The addressee remains the national competent authority in all cases; onward transmission to EBA, ESMA, EIOPA and the ECB is done by that authority under Art. 19(6) DORA.")

q("meldeinhalt", 3,
  "Anhang I und Anhang II (Datenfelder 2.2 und 2.3) Durchfuehrungsverordnung (EU) 2025/302",
  3, False, False, "d",
  "Welche Zeitangaben verlangt die Meldevorlage der Durchfuehrungsverordnung (EU) 2025/302 bereits in der Erstmeldung?",
  {
    "a": "Nur den Zeitpunkt der Einstufung als schwerwiegend",
    "b": "Nur den Zeitpunkt der Feststellung des Vorfalls",
    "c": "Nur den Zeitpunkt der Wiederherstellung des Regelbetriebs",
    "d": "Sowohl Datum und Uhrzeit der Feststellung - also der Kenntnisnahme durch das Finanzunternehmen - als auch Datum und Uhrzeit der Einstufung als schwerwiegend; beide Felder sind Pflichtangaben im ISO-8601-UTC-Format",
  },
  "Which timestamps does the reporting template under Implementing Regulation (EU) 2025/302 require already in the initial notification?",
  {
    "a": "Only the time of classification as major",
    "b": "Only the time of detection of the incident",
    "c": "Only the time at which regular operations were restored",
    "d": "Both the date and time of detection - i.e. of the financial entity becoming aware - and the date and time of classification as major; both fields are mandatory, in ISO 8601 UTC format",
  },
  "Anhang I fuehrt unter 'Inhalt der Erstmeldung' die Felder 2.2 'Datum und Uhrzeit der Feststellung des IKT-bezogenen Vorfalls' und 2.3 'Datum und Uhrzeit der Einstufung des Vorfalls als schwerwiegend'. Anhang II definiert Feld 2.2 als 'Datum und Uhrzeit der Kenntnisnahme des IKT-bezogenen Vorfalls durch das Finanzunternehmen' und Feld 2.3 als den Zeitpunkt der Einstufung nach den Kriterien der Delegierten Verordnung (EU) 2024/1772; beide sind fuer Erst-, Zwischen- und Abschlussmeldung mit 'Ja' als Pflichtfeld gekennzeichnet, Feldtyp 'ISO 8601 UTC-Format'. Genau diese Feldpaarung macht die zweigliedrige Frist des Art. 5 Abs. 1 Buchst. a der Delegierten Verordnung (EU) 2025/301 fuer die Aufsicht nachrechenbar: aus den beiden Zeitstempeln und dem Eingangszeitpunkt der Meldung ergibt sich unmittelbar, ob beide Fristen eingehalten wurden. Der Zeitpunkt der Wiederherstellung (Feld 3.3) und der Eintrittszeitpunkt (Feld 3.2) gehoeren dagegen erst in die Zwischenmeldung.",
  "Annex I lists, under 'Content of the initial notification', field 2.2 'Date and time of detection of the major ICT-related incident' and field 2.3 'Date and time of classification of the ICT-related incident as major'. Annex II defines field 2.2 as 'Date and time at which the financial entity has become aware of the ICT-related incident' and field 2.3 as the time of classification according to the criteria in Delegated Regulation (EU) 2024/1772; both are marked 'Yes' as mandatory for the initial notification and the intermediate and final reports, with field type 'ISO 8601 standard UTC'. This pair of fields is exactly what makes the two-limbed deadline in Art. 5(1)(a) of Delegated Regulation (EU) 2025/301 auditable: from the two timestamps and the time of receipt, the supervisor can compute directly whether both limits were met. The recovery timestamp (field 3.3) and the time of occurrence (field 3.2), by contrast, belong to the intermediate report.")

q("meldeinhalt", 4,
  "Art. 19 Abs. 5 Verordnung (EU) 2022/2554 i.V.m. Art. 6 und Art. 7 Durchfuehrungsverordnung (EU) 2025/302",
  4, True, False, "a",
  "Ihr Unternehmen lagert die Vorfallmeldung an einen Dienstleister aus. Was gilt?",
  {
    "a": "Die Auslagerung ist zulaessig, das Finanzunternehmen bleibt aber in vollem Umfang fuer die Erfuellung der Meldepflichten verantwortlich; die zustaendige Behoerde ist ueber die Auslagerungsvereinbarung zu unterrichten, sobald sie geschlossen wurde, spaetestens vor der ersten Meldung, unter Angabe von Name, Kontaktdaten und Identifikationscode des Dritten",
    "b": "Die Auslagerung ist unzulaessig; die Meldung muss stets durch das Finanzunternehmen selbst erfolgen",
    "c": "Mit der Auslagerung geht die Verantwortung fuer die Einhaltung der Meldepflichten auf den Dienstleister ueber",
    "d": "Die Auslagerung ist zulaessig und muss der Behoerde nicht angezeigt werden",
  },
  "Your entity outsources incident reporting to a service provider. What applies?",
  {
    "a": "Outsourcing is permitted, but the financial entity remains fully responsible for fulfilling the reporting requirements; the competent authority must be informed of the outsourcing arrangement as soon as it has been concluded and at the latest prior to the first report, stating the third party's name, contact details and identification code",
    "b": "Outsourcing is not permitted; the report must always be made by the financial entity itself",
    "c": "On outsourcing, responsibility for compliance with the reporting duties passes to the service provider",
    "d": "Outsourcing is permitted and need not be notified to the authority",
  },
  "Art. 19 Abs. 5 DORA im amtlichen deutschen Wortlaut: 'Finanzunternehmen duerfen im Einklang mit den sektorspezifischen Rechtsvorschriften der Union und der Mitgliedstaaten die Meldepflichten nach diesem Artikel an einen Drittdienstleister auslagern. Bei einer solchen Auslagerung bleibt das Finanzunternehmen in vollem Umfang fuer die Erfuellung der Anforderungen fuer die Meldung von Vorfaellen verantwortlich.' Art. 6 der Durchfuehrungsverordnung (EU) 2025/302 ergaenzt die Anzeigepflichten: Unterrichtung der Behoerde, sobald die Vereinbarung geschlossen wurde und spaetestens vor der ersten Meldung (Abs. 1), Angabe von Name, Kontaktdaten und Identifikationscode des Dritten (Abs. 2) sowie Unterrichtung, sobald nicht mehr ausgelagert wird (Abs. 3). Art. 7 erlaubt einem solchen Dienstleister unter fuenf kumulativen Voraussetzungen eine aggregierte Meldung fuer mehrere betroffene Finanzunternehmen - unter anderem muss der Vorfall bei jedem einzelnen Unternehmen als schwerwiegend eingestuft sein und die zustaendige Behoerde muss dies ausdruecklich gestattet haben. Bedeutende Kreditinstitute, Betreiber von Handelsplaetzen und zentrale Gegenparteien sind davon ausgenommen und melden stets einzeln.",
  "Art. 19(5) DORA verbatim: 'Financial entities may outsource, in accordance with Union and national sectoral law, the reporting obligations under this Article to a third-party service provider. In case of such outsourcing, the financial entity remains fully responsible for the fulfilment of the incident reporting requirements.' Art. 6 of Implementing Regulation (EU) 2025/302 adds the notification duties: inform the authority as soon as the arrangement has been concluded and at the latest prior to the first report (para. 1), provide the third party's name, contact details and identification code (para. 2), and inform the authority as soon as reporting is no longer outsourced (para. 3). Art. 7 allows such a provider, under five cumulative conditions, to submit an aggregated report covering several affected financial entities - among other things the incident must be classified as major by each of them and the competent authority must have explicitly permitted it. Credit institutions of significant relevance, operators of trading venues and central counterparties are excluded and always report individually.")

q("meldeinhalt", 5,
  "Art. 5 Durchfuehrungsverordnung (EU) 2025/302 i.V.m. Art. 2 Buchst. i Delegierte Verordnung (EU) 2025/301",
  4, True, False, "b",
  "Unter welcher Voraussetzung darf ein bereits als schwerwiegend gemeldeter Vorfall gegenueber der Behoerde auf 'nicht schwerwiegend' zurueckgestuft werden?",
  {
    "a": "Sobald der Dienst wiederhergestellt ist und keine weiteren Auswirkungen mehr eintreten",
    "b": "Nur wenn das Finanzunternehmen nach eingehender Pruefung zu dem Schluss kommt, dass der Vorfall zu keinem Zeitpunkt die Einstufungskriterien und Schwellenwerte des Art. 8 der Delegierten Verordnung (EU) 2024/1772 erfuellt hat",
    "c": "Wenn sich die zunaechst geschaetzten Kosten im Nachhinein als niedriger herausstellen als angenommen",
    "d": "Eine Rueckstufung ist in keinem Fall vorgesehen",
  },
  "Under what condition may an incident already reported as major be reclassified to 'non-major' vis-a-vis the authority?",
  {
    "a": "As soon as the service is restored and no further impact occurs",
    "b": "Only where the financial entity concludes, after further assessment, that the incident at no time fulfilled the classification criteria and thresholds set out in Art. 8 of Delegated Regulation (EU) 2024/1772",
    "c": "Where the initially estimated costs subsequently turn out to be lower than assumed",
    "d": "Reclassification is never provided for",
  },
  "Art. 5 der Durchfuehrungsverordnung (EU) 2025/302: 'Kommt das Finanzunternehmen nach eingehender Pruefung zu dem Schluss, dass der zuvor als schwerwiegend gemeldete IKT-bezogene Vorfall zu keinem Zeitpunkt die in Artikel 8 der Delegierten Verordnung (EU) 2024/1772 festgelegten Einstufungskriterien und Schwellenwerte erfuellte, so teilt es der zustaendigen Behoerde mit, dass es den IKT-bezogenen Vorfall von schwerwiegend auf nicht schwerwiegend zurueckgestuft hat', und macht die Angaben in den Feldern 'Art der Meldung' und 'Sonstige Informationen'. Massgeblich ist damit ein rueckblickender Test: nicht 'der Vorfall ist vorbei', sondern 'die Schwelle war nie erreicht'. Antwort c beschreibt den haeufigsten Irrtum - Schaetzwerte sind nach Art. 1 Abs. 3 der Durchfuehrungsverordnung ausdruecklich vorgesehen, und eine nachtraeglich niedrigere Zahl macht die urspruengliche Einstufung nicht unrichtig, solange andere Schwellen erfuellt waren. Die Auswahlliste im Feld 1.1 sieht die Rueckstufung als eigenen Meldungstyp vor; Art. 2 Buchst. i der Delegierten Verordnung (EU) 2025/301 nennt Angaben zur Rueckstufung ausserdem als Inhalt der Erstmeldung, sofern einschlaegig. REDAKTIONELLER HINWEIS FUER DIE PRUEFUNG: Art. 5 der Durchfuehrungsverordnung verweist im Wortlaut auf 'die Vorlage in Anhang II', waehrend die Meldevorlage in Anhang I steht und Anhang II das Datenglossar enthaelt; auf die Antwort wirkt sich das nicht aus.",
  "Art. 5 of Implementing Regulation (EU) 2025/302: 'Where after further assessment, the financial entity concludes that the ICT-related incident previously reported as major, at no time fulfilled the classification criteria and thresholds set out in Article 8 of Delegated Regulation (EU) 2024/1772, the financial entity shall notify to the competent authority that it has reclassified the ICT-related incident from major to non-major', providing the information in the 'type of report' and 'other information' fields. The test is therefore retrospective: not 'the incident is over' but 'the threshold was never met'. Option (c) describes the most common error - estimates are expressly provided for by Art. 1(3) of the Implementing Regulation, and a subsequently lower figure does not make the original classification wrong so long as other thresholds were met. The choice list in field 1.1 provides for reclassification as its own submission type; Art. 2(i) of Delegated Regulation (EU) 2025/301 additionally lists reclassification information as content of the initial notification, where applicable. EDITORIAL NOTE FOR REVIEW: Art. 5 of the Implementing Regulation refers on its face to 'the template laid down in Annex II', whereas the reporting template is in Annex I and Annex II contains the data glossary; this has no effect on the answer.")


# ------------------------------------------------------------------ meta ----
META = {
    "app": "Zettacard / dora-incident-lernmodul",
    "version": "0.1-draft",
    "generated": "2026-08-16",
    "description": (
        "DRAFT Pilot-Fragenkatalog fuer das Modul 'DORA Art. 17-20 - Meldung von IKT-Vorfaellen' "
        "(dora_incident, Modul 5 der B2B-DORA/CRA-Roadmap). Zielgruppe: IT-Betrieb, Helpdesk/SOC und "
        "Incident-Manager in EU-Finanzunternehmen, die Vorfaelle tatsaechlich klassifizieren und "
        "fristgerecht melden muessen - nicht die allgemeine Belegschaft und nicht das Leitungsorgan. "
        "Grundlage sind ausschliesslich die amtlichen Amtsblatt-Texte der Verordnung (EU) 2022/2554 "
        "(Art. 16-23), der Delegierten Verordnung (EU) 2024/1772 (RTS Klassifizierung), der Delegierten "
        "Verordnung (EU) 2025/301 (RTS Inhalt und Fristen) und der Durchfuehrungsverordnung (EU) 2025/302 "
        "(ITS Formulare, Vorlagen und Verfahren), jeweils in der englischen und der deutschen "
        "Sprachfassung gelesen. Kein Fragentext eines kommerziellen Anbieters uebernommen. "
        "Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine "
        "Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall "
        "durch qualifizierte Juristen oder Wirtschaftspruefer zu validieren."
    ),
    "legal_disclaimer": (
        "Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken und stellt keine "
        "Rechts- oder Compliance-Beratung dar. Die regulatorischen Anforderungen sind im Einzelfall "
        "durch qualifizierte Juristen oder Wirtschaftspruefer zu validieren."
    ),
    "class": "ALL",
    "locales": ["de", "en"],
    "canonical_locale": "de",
    "point_system": "3-4 points per question, matching this app's existing compliance-module style",
    "total_questions": 20,
    "legal_review_status": (
        "DRAFT - NOT legally reviewed. Primary-source verification performed 2026-08-16 against the "
        "Official Journal texts retrieved from the EU Publications Office Cellar repository "
        "(publications.europa.eu/resource/celex/<CELEX>, Accept: application/xhtml+xml, "
        "Accept-Language: eng / deu): Regulation (EU) 2022/2554 (CELEX 32022R2554, OJ L 333, 27.12.2022, "
        "p. 1); Commission Delegated Regulation (EU) 2024/1772 of 13 March 2024 (CELEX 32024R1772, "
        "OJ L, 2024/1772, 25.6.2024); Commission Delegated Regulation (EU) 2025/301 of 23 October 2024 "
        "(CELEX 32025R0301, OJ L, 2025/301, 20.2.2025); Commission Implementing Regulation (EU) 2025/302 "
        "of 23 October 2024 (CELEX 32025R0302, OJ L, 2025/302, 20.2.2025). No consolidated version exists "
        "for any of the three Level 2 instruments as at 2026-08-16, i.e. no amendment or corrigendum has "
        "been applied to them. See docs/dora-incident-pre-review-dossier-2026-08-16.md for the per-question "
        "confidence-tier ledger before any use."
    ),
    "renewal_months": None,
    "renewal_basis": "not_specified_in_statute",
    "renewal_note": (
        "Weder Art. 13 Abs. 6 DORA noch Kapitel III (Art. 17-23) noch eine der drei Level-2-Verordnungen "
        "schreiben ein Schulungsintervall vor. Die einzigen ausdruecklichen Wiederholungstakte in diesem "
        "Themenfeld sind die monatliche Bewertung wiederholter Vorfaelle nach Art. 8 Abs. 2 der Delegierten "
        "Verordnung (EU) 2024/1772 und die jaehrliche Berichterstattung der ESA nach Art. 22 Abs. 2 DORA - "
        "beides sind keine Schulungsfristen. Ein Wiederholungstakt waere eine Produktentscheidung."
    ),
    "pass_rule_note": (
        "Offen. Bewusst werden hier keine EXAM_QUESTION_COUNT_BY_TYPE / MAX_ERROR_POINTS_BY_TYPE / "
        "EXAM_TOPIC_DRAW-Werte vorgeschlagen; die 4x5-Themenaufteilung legt einen Zug nahe, der alle vier "
        "Themen beruehrt, das ist aber eine Produktentscheidung nach der Rechtspruefung."
    ),
    "draft_note": (
        "Nicht in data/build_modules.py registriert, nicht in data/modules_manifest.json, kein Build "
        "ausgefuehrt, nichts committet. Dateiname bewusst mit _DRAFT-Suffix, damit die Datei nicht in den "
        "Live-Build-Pfad geraet."
    ),
    "license": "CC BY-NC-SA 4.0",
    "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "license_note": (
        "Attribution-NonCommercial-ShareAlike: free to use, adapt, and redistribute for non-commercial "
        "exam-prep purposes, with credit and under the same license. Commercial reuse needs a separate "
        "arrangement; non-commercial prep tools/forks are welcome."
    ),
}


# ------------------------------------------------------- umlaut restoration ---
# The question/explanation text above is authored with ASCII digraphs so that this
# generator file stays diff-friendly; the emitted JSON must contain real umlauts.
# The map below is applied to every DE string (and to DE-language words that occur
# inside EN strings, of which there are none by construction).
UMLAUT_WORDS = [
    # (ascii, proper) - longest first, applied with word-boundary awareness
    ("Ausschliesslich", "Ausschließlich"), ("ausschliesslich", "ausschließlich"),
    ("Grundsaetzlich", "Grundsätzlich"), ("grundsaetzlich", "grundsätzlich"),
    ("Durchfuehrungsverordnung", "Durchführungsverordnung"),
    ("Wertpapierdienstleistungsunternehmen", "Wertpapierdienstleistungsunternehmen"),
    ("Wesentlichkeitsschwellen", "Wesentlichkeitsschwellen"),
]

# Generic, order-sensitive digraph map. Applied only to German-language fields.
DIGRAPHS = [
    ("Ae", "Ä"), ("Oe", "Ö"), ("Ue", "Ü"),
    ("ae", "ä"), ("oe", "ö"), ("ue", "ü"), ("ss", "ß"),
]

# Explicit whitelist: ASCII form -> proper German form. Safer than blind digraph
# substitution, which would wreck words like 'Prozesse', 'Duesseldorf', 'Muster'.
REPL = {
    "Vorfaelle": "Vorfälle", "Vorfaellen": "Vorfällen",
    "Faelle": "Fälle", "faellt": "fällt", "Faellen": "Fällen", "Faellt": "Fällt",
    "unabhaengig": "unabhängig",
    "Cyberangriffe": "Cyberangriffe",
    "Fruehwarnindikatoren": "Frühwarnindikatoren",
    "Zustaendigkeiten": "Zuständigkeiten", "Zustaendigkeit": "Zuständigkeit",
    "zustaendige": "zuständige", "zustaendigen": "zuständigen", "zustaendiger": "zuständiger",
    "Zustaendige": "Zuständige", "Zustaendigen": "Zuständigen",
    "Behoerde": "Behörde", "Behoerden": "Behörden", "Behoerdlich": "Behördlich",
    "Aufsichtsbehoerde": "Aufsichtsbehörde",
    "Rufnummer": "Rufnummer",
    "Stoerungsmeldungen": "Störungsmeldungen", "gestoert": "gestört",
    "Ausschliesslich": "Ausschließlich", "ausschliesslich": "ausschließlich",
    "Eskalation": "Eskalation",
    "moeglich": "möglich", "moeglichst": "möglichst", "Moeglichkeit": "Möglichkeit",
    "unmoeglich": "unmöglich", "Unmoeglichkeit": "Unmöglichkeit",
    "muessen": "müssen", "muss": "muss",
    "koennen": "können", "koennte": "könnte",
    "fuer": "für", "Fuer": "Für",
    "fuehrt": "führt", "fuehren": "führen", "gefuehrt": "geführt",
    "durchfuehren": "durchführen", "Durchfuehrung": "Durchführung",
    "Durchfuehrungsverordnung": "Durchführungsverordnung",
    "einfuehren": "einführen", "Einfuehrung": "Einführung",
    "Fuehrungsebene": "Führungsebene", "hoehere": "höhere", "hoeheren": "höheren",
    "Geschaeftsleitung": "Geschäftsleitung", "Geschaeftsbetrieb": "Geschäftsbetrieb",
    "Geschaeftsziele": "Geschäftsziele", "Geschaeftstaetigkeit": "Geschäftstätigkeit",
    "taeglichen": "täglichen", "taeglich": "täglich",
    "Erwaegungsgrund": "Erwägungsgrund", "Erwaegungsgruende": "Erwägungsgründe",
    "waere": "wäre", "waeren": "wären",
    "spaeter": "später", "spaetere": "spätere", "spaetestens": "spätestens", "spaeteren": "späteren",
    "frueher": "früher", "fruehere": "frühere", "frueh": "früh",
    "kuerzer": "kürzer", "verkuerzt": "verkürzt",
    "verfuegbar": "verfügbar", "Verfuegbarkeit": "Verfügbarkeit", "verfuegbare": "verfügbare",
    "Verzoegerung": "Verzögerung", "verzoegert": "verzögert",
    "zurueckgestellt": "zurückgestellt", "zurueckgestuft": "zurückgestuft",
    "zurueckzustufen": "zurückzustufen", "Rueckstufung": "Rückstufung",
    "unverzueglich": "unverzüglich",
    "beruehrt": "berührt", "Beruehrung": "Berührung",
    "eingefuehrt": "eingeführt",
    "Ueberwachung": "Überwachung", "ueber": "über", "Ueber": "Über",
    "uebersteigen": "übersteigen", "Uebermittlung": "Übermittlung",
    "uebermittelt": "übermittelt", "uebermitteln": "übermitteln",
    "uebernommen": "übernommen", "Uebertragung": "Übertragung",
    "ueberfluessig": "überflüssig", "Uebersicht": "Übersicht",
    "naechsten": "nächsten", "naechste": "nächste",
    "Erfuellung": "Erfüllung", "erfuellt": "erfüllt", "erfuellen": "erfüllen",
    "Erfuellungsgehilfe": "Erfüllungsgehilfe",
    "zulaessig": "zulässig", "unzulaessig": "unzulässig",
    "Zulassungsbedingungen": "Zulassungsbedingungen",
    "kohaerente": "kohärente", "kohaerent": "kohärent",
    "Kritikalitaet": "Kritikalität",
    "Prioritaet": "Priorität",
    "Verhaeltnismaessigkeit": "Verhältnismäßigkeit", "Verhaeltnis": "Verhältnis",
    "Groessen": "Größen", "Groesse": "Größe", "grosses": "großes", "gross": "groß",
    "massgeblich": "maßgeblich", "Massnahmen": "Maßnahmen", "Massnahme": "Maßnahme",
    "grosse": "große", "grossen": "großen",
    "Aussengrenze": "Außengrenze",
    "genuegt": "genügt", "genuegen": "genügen",
    "Pruefung": "Prüfung", "pruefen": "prüfen", "geprueft": "geprüft",
    "PRUEFHINWEIS": "PRÜFHINWEIS", "Pruefhinweis": "Prüfhinweis",
    "Wirtschaftspruefer": "Wirtschaftsprüfer",
    "Rechtspruefung": "Rechtsprüfung",
    "REDAKTIONELLER HINWEIS FUER DIE PRUEFUNG": "REDAKTIONELLER HINWEIS FÜR DIE PRÜFUNG",
    "Schaetzung": "Schätzung", "Schaetzungen": "Schätzungen", "Schaetzwerte": "Schätzwerte",
    "schaetzt": "schätzt", "geschaetzten": "geschätzten", "zu schaetzen": "zu schätzen",
    "Waehrung": "Währung", "waehrend": "während",
    "gemaess": "gemäß", "Gemaess": "Gemäß",
    "aeussern": "äußern",
    "Anhaltspunkt": "Anhaltspunkt",
    "haeufigsten": "häufigsten", "haeufige": "häufige", "haeufig": "häufig",
    "urspruengliche": "ursprüngliche", "urspruenglichen": "ursprünglichen",
    "nachtraeglich": "nachträglich",
    "Europaeische": "Europäische", "Europaeischen": "Europäischen",
    "Aufsichtsbehoerden": "Aufsichtsbehörden",
    "boeswilliger": "böswilliger", "boeswillige": "böswillige", "boeswilligen": "böswilligen",
    "unbefugter": "unbefugter",
    "vorgeschaltetes": "vorgeschaltetes",
    "Sprachfassung": "Sprachfassung",
    "eigenstaendige": "eigenständige", "eigenstaendig": "eigenständig",
    "Eigenstaendig": "Eigenständig",
    "Handelsplaetzen": "Handelsplätzen", "Handelsplaetze": "Handelsplätze",
    "Absaetzen": "Absätzen", "Absaetze": "Absätze",
    "Datenverlusten": "Datenverlusten",
    "Wiederherstellung": "Wiederherstellung",
    "Notfallplan": "Notfallplan",
    "regulaere": "reguläre", "regulaeren": "regulären",
    "Referenzzeitraeume": "Referenzzeiträume", "Referenzzeitraeumen": "Referenzzeiträumen",
    "abschliessend": "abschließend", "einschliesslich": "einschließlich",
    "Schliesslich": "Schließlich", "schliesslich": "schließlich",
    "schliesst": "schließt",
    "Vermerk": "Vermerk",
    "Zahlungs-Gateway": "Zahlungs-Gateway",
    "faellt auf": "fällt auf",
    "Feiertagsregelung": "Feiertagsregelung",
    "darauffolgenden": "darauffolgenden",
    "Rufbereitschaft": "Rufbereitschaft",
    "Voraussetzung": "Voraussetzung",
    "Fristenwahrung": "Fristenwahrung",
    "Fristenrechnung": "Fristenrechnung",
    "belastbaren": "belastbaren",
    "Auswahlliste": "Auswahlliste",
    "einschlaegig": "einschlägig",
    "nachrechenbar": "nachrechenbar",
    "Feldpaarung": "Feldpaarung",
    "Institutsgruppen": "Institutsgruppen",
    "systemrelevante": "systemrelevante",
    "Anzeigepflichten": "Anzeigepflichten",
    "kumulativen": "kumulativen",
    "Bedeutende": "Bedeutende",
    "Datenglossar": "Datenglossar",
    "Meldungstyp": "Meldungstyp",
    "Konfigurationsfehler": "Konfigurationsfehler",
    "aufgeschoben": "aufgeschoben", "aufzuschieben": "aufzuschieben",
    "Unsicherheit": "Unsicherheit",
    "Serviceniveaus": "Serviceniveaus",
    "Leistungserbringung": "Leistungserbringung",
    "vollstaendigen": "vollständigen", "vollstaendig": "vollständig",
    "Freibrief": "Freibrief",
    "Zeitstempel": "Zeitstempel", "Zeitstempeln": "Zeitstempeln",
    "Abstand": "Abstand",
    "Klassifizierungsverfahren": "Klassifizierungsverfahren",
    "aktualisierten": "aktualisierten", "aktualisierte": "aktualisierte",
    "Aenderung": "Änderung", "Statusaenderung": "Statusänderung",
    "geaendert": "geändert",
    "Planungsgroesse": "Planungsgröße",
    "Kenntnistages": "Kenntnistages",
    "Betriebliche": "Betriebliche", "betrieblich": "betrieblich",
    "Konsequenz": "Konsequenz",
    "Auslegung": "Auslegung",
    "Wortlauts": "Wortlauts", "Wortlaut": "Wortlaut",
    "Fehlvorstellung": "Fehlvorstellung",
    "unterschlaegt": "unterschlägt",
    "Einordnung": "Einordnung",
    "Stundenangabe": "Stundenangabe",
    "Grundverordnung": "Grundverordnung",
    "Kenntniserlangung": "Kenntniserlangung",
    "Kenntnisnahme": "Kenntnisnahme",
    "Betreiber": "Betreiber",
    "Gegenparteien": "Gegenparteien",
    "Sammelmeldung": "Sammelmeldung",
    "jaehrliche": "jährliche", "jaehrlich": "jährlich", "jaehrlichen": "jährlichen",
    "Wertpapierfirmen": "Wertpapierfirmen",
    "Erleichterung": "Erleichterung",
    "Kleinstunternehmen": "Kleinstunternehmen",
    "verflochtenes": "verflochtenes", "verflochtene": "verflochtene",
    "Meldevorlage": "Meldevorlage",
    "Ursachenanalyse": "Ursachenanalyse",
    "Vorfallregister": "Vorfallregister",
    "strukturell": "strukturell",
    "dokumentiert": "dokumentiert",
    "Wiederholungspruefung": "Wiederholungsprüfung",
    "Weiterverfolgung": "Weiterverfolgung",
    "Protokollierung": "Protokollierung",
    "Kategorisierung": "Kategorisierung",
    "Nachverfolgung": "Nachverfolgung",
    "Kundenbenachrichtigung": "Kundenbenachrichtigung",
    "Reaktionsverfahren": "Reaktionsverfahren",
    "Ernstfall": "Ernstfall",
    "Schutzmassnahmen": "Schutzmaßnahmen",
    "Minderung": "Minderung",
    "Aufsichtsmeldung": "Aufsichtsmeldung",
    "Freigabe": "Freigabe",
    "Ausloeser": "Auslöser",
    "Wortgleich": "Wortgleich",
    # --- second pass: caught by the digraph audit -------------------------
    "Ausdruecklich": "Ausdrücklich", "ausdruecklich": "ausdrücklich",
    "ausdrueckliche": "ausdrückliche", "ausdruecklichen": "ausdrücklichen",
    "Beeintraechtigung": "Beeinträchtigung", "beeintraechtigt": "beeinträchtigt",
    "Bestaetigt": "Bestätigt", "bestaetigt": "bestätigt",
    "Betriebsstoerung": "Betriebsstörung",
    "Eskalationsplaene": "Eskalationspläne",
    "Genuegt": "Genügt",
    "Gruende": "Gründe",
    "Grundsaetzlich": "Grundsätzlich", "grundsaetzlich": "grundsätzlich",
    "Kanaele": "Kanäle",
    "Laesst": "Lässt", "laesst": "lässt",
    "Massgeblich": "Maßgeblich",
    "Unterstuetzung": "Unterstützung",
    "unterstuetzen": "unterstützen", "unterstuetzt": "unterstützt",
    "ausserdem": "außerdem",
    "auszuschliessen": "auszuschließen",
    "duerfen": "dürfen",
    "enthaelt": "enthält",
    "ergaenzt": "ergänzt",
    "faellig": "fällig",
    "fuenf": "fünf",
    "gehoeren": "gehören",
    "geraet": "gerät",
    "gewaehrleisten": "gewährleisten",
    "heisst": "heißt",
    "knuepfen": "knüpfen", "knuepft": "knüpft", "verknuepft": "verknüpft",
    "laeuft": "läuft",
    "rueckblickender": "rückblickender",
    "spaete": "späte",
    "tatsaechlich": "tatsächlich", "tatsaechliche": "tatsächliche",
    "tatsaechlichen": "tatsächlichen",
    "uebrigen": "übrigen",
    "unveraendert": "unverändert",
    "verlaengert": "verlängert", "verlaengerte": "verlängerte",
    "zaehlt": "zählt",
    "zunaechst": "zunächst",
    "zusaetzlich": "zusätzlich",
}


def germanise(s):
    """Replace ASCII-transliterated German with proper orthography."""
    # longest keys first so that e.g. 'Durchfuehrungsverordnung' beats 'fuehr'
    for k in sorted(REPL, key=len, reverse=True):
        s = s.replace(k, REPL[k])
    return s


def walk_de(obj, path=()):
    """Apply germanise() to every German-language string."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = walk_de(v, path + (k,))
        return out
    if isinstance(obj, list):
        return [walk_de(v, path) for v in obj]
    if isinstance(obj, str):
        # German fields: anything under a 'de' key, plus meta prose fields
        if "de" in path or path and path[-1] in (
            "description", "legal_disclaimer", "renewal_note",
            "pass_rule_note", "draft_note",
        ):
            return germanise(obj)
        return obj
    return obj


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(root, "dora_incident_pilot_DRAFT.json")

    doc = {"meta": META, "questions": Q}
    doc = walk_de(doc)

    # --- integrity checks -------------------------------------------------
    ids = [q["id"] for q in doc["questions"]]
    assert len(ids) == 20, len(ids)
    assert len(set(ids)) == 20, "duplicate ids"
    from collections import Counter
    keyc = Counter(q["correct"][0] for q in doc["questions"])
    assert keyc == {"a": 5, "b": 5, "c": 5, "d": 5}, keyc
    tc = Counter(q["topic_code"] for q in doc["questions"])
    assert set(tc.values()) == {5}, tc
    ref = json.load(open(os.path.join(root, "kartellrecht_pilot.json"), encoding="utf-8"))
    ref_keys = list(ref["questions"][0].keys())
    for q_ in doc["questions"]:
        assert list(q_.keys()) == ref_keys, (q_["id"], list(q_.keys()))
        for loc in ("de", "en"):
            assert set(q_["text"][loc]["options"]) == {"a", "b", "c", "d"}
            assert q_["correct"][0] in q_["text"][loc]["options"]

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    blob = open(out_path, encoding="utf-8").read()
    umlauts = sum(blob.count(c) for c in "äöüÄÖÜß")
    residue = re.findall(
        r"\b\w*(?:fuer|ueber|muessen|koennen|waere|gefuehrt|ausschliesslich|faellt|"
        r"maessig|groesse|zustaendig|behoerde|moeglich|spaetest|unverzueglich|"
        r"gemaess|pruef|schaetz|vorfaelle|jaehrlich|massnahm|erfuell)\w*\b", blob, re.I)
    print("questions      :", len(doc["questions"]))
    print("answer key     :", dict(keyc))
    print("topics         :", dict(tc))
    print("points 4 / 3   :", sum(1 for x in doc["questions"] if x["points"] == 4),
          "/", sum(1 for x in doc["questions"] if x["points"] == 3))
    print("high_stakes    :", sum(1 for x in doc["questions"] if x["high_stakes"]))
    print("grundstoff     :", sum(1 for x in doc["questions"] if x["grundstoff"]))
    print("umlaut chars   :", umlauts)
    print("ASCII residue  :", sorted(set(residue)) or "NONE")
    print("wrote          :", out_path)
    return 0 if not residue else 1


if __name__ == "__main__":
    sys.exit(main())
