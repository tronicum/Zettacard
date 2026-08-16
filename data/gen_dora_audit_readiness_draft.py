#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic generator for data/dora_audit_readiness_pilot_DRAFT.json.

Module:   dora_audit_readiness
Working title: "Surviving the DORA Audit: Testing, Evidence, and ISO 27001 Alignment"
Audience: internal audit functions, CISOs and audit-preparation staff at EU
          financial entities who must produce evidence for a DORA compliance
          audit (internal audit, Big 4 external audit, supervisory examination).

Canonical locale: de (matching the four DORA sibling draft modules), + en.

Primary sources, read 2026-08-16 in the OJ text (EN + DE) via the EU
Publications Office Cellar repository:
  - Regulation (EU) 2022/2554 (DORA), CELEX 32022R2554
  - Commission Delegated Regulation (EU) 2025/1190, CELEX 32025R1190
    (RTS on TLPT under the Art. 26(11) mandate, OJ L, 2025/1190, 18.6.2025)

NOT wired into any build path. Writes only the _DRAFT file.
Runs its own integrity, schema-parity and German-orthography checks and
exits non-zero on failure.
"""

import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dora_audit_readiness_pilot_DRAFT.json")
TEMPLATE = os.path.join(HERE, "kartellrecht_pilot.json")

DISCLAIMER_DE = (
    "Dieses Schulungsmaterial dient reinen Ausbildungs- und Informationszwecken "
    "und stellt keine Rechts- oder Compliance-Beratung dar. Die regulatorischen "
    "Anforderungen sind im Einzelfall durch qualifizierte Juristen oder "
    "Wirtschaftsprüfer zu validieren."
)

TOPICS = {
    "testprogramm": {
        "de": "Testprogramm und allgemeine Testanforderungen",
        "en": "Testing programme and general testing requirements",
    },
    "tlpt_scoping": {
        "de": "TLPT: Anwendungsbereich, Häufigkeit und Testumfang",
        "en": "TLPT: scope of application, frequency and test scope",
    },
    "tester_governance": {
        "de": "Tester, Unabhängigkeit und interne Revision",
        "en": "Testers, independence and internal audit",
    },
    "nachweise_audit": {
        "de": "Nachweise, Dokumentation und Auditvorbereitung",
        "en": "Evidence, documentation and audit preparation",
    },
}


def q(qid, topic_code, grundstoff, legal_basis, points, high_stakes, correct,
      de_q, de_opts, en_q, en_opts, de_exp, en_exp):
    return {
        "id": qid,
        "topic": TOPICS[topic_code]["de"],
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
        "explanation": {"de": de_exp, "en": en_exp},
        "roles": ["all"],
    }


QUESTIONS = []

# ---------------------------------------------------------------------------
# Topic 1 - testprogramm (Art. 24, 25, 11 DORA)
# ---------------------------------------------------------------------------

QUESTIONS.append(q(
    "dora-audit-testprogramm-01", "testprogramm", True,
    "Art. 24 Abs. 1 und 2 VO (EU) 2022/2554", 3, False, "b",
    "Ein Pruefer der Internen Revision fragt, welchen Status das Programm fuer das "
    "Testen der digitalen operationalen Resilienz nach Artikel 24 DORA hat. Welche "
    "Aussage trifft zu?".replace("Pruefer", "Prüfer").replace("fuer", "für"),
    {
        "a": "Es ist ein eigenstaendiges Projekt der IT-Sicherheit und vom "
             "IKT-Risikomanagementrahmen bewusst getrennt zu halten."
             .replace("eigenstaendiges", "eigenständiges"),
        "b": "Es ist integraler Bestandteil des IKT-Risikomanagementrahmens nach "
             "Artikel 6, wird erstellt, gepflegt und überprüft und umfasst eine Reihe "
             "von Bewertungen, Tests, Methoden, Verfahren und Tools nach den Artikeln 25 "
             "und 26.",
        "c": "Es besteht ausschließlich aus bedrohungsorientierten Penetrationstests "
             "(TLPT) und ist deshalb nur für die von der Aufsicht benannten Unternehmen "
             "relevant.",
        "d": "Es ist eine einmalige Bestandsaufnahme vor der Erstzulassung und muss "
             "danach nur bei wesentlichen Systemwechseln wiederholt werden.",
    },
    "An internal auditor asks what status the digital operational resilience testing "
    "programme under Article 24 DORA has. Which statement is correct?",
    {
        "a": "It is a stand-alone IT security project and should deliberately be kept "
             "separate from the ICT risk management framework.",
        "b": "It is an integral part of the ICT risk management framework referred to in "
             "Article 6, is established, maintained and reviewed, and includes a range of "
             "assessments, tests, methodologies, practices and tools to be applied in "
             "accordance with Articles 25 and 26.",
        "c": "It consists exclusively of threat-led penetration testing (TLPT) and is "
             "therefore relevant only to entities identified by the supervisor.",
        "d": "It is a one-off stocktake before initial authorisation and needs to be "
             "repeated only when systems change substantially.",
    },
    "Artikel 24 Absatz 1 DORA verlangt von Finanzunternehmen, die keine "
    "Kleinstunternehmen sind, ein solides und umfassendes Programm für das Testen der "
    "digitalen operationalen Resilienz zu erstellen, zu pflegen und zu überprüfen, und "
    "zwar ausdrücklich \"als integraler Bestandteil des in Artikel 6 genannten "
    "IKT-Risikomanagementrahmens\". Absatz 2 fügt hinzu: \"Das Programm für Tests der "
    "digitalen operationalen Resilienz umfasst eine Reihe von Bewertungen, Tests, "
    "Methoden, Verfahren und Tools, die gemäß den Artikeln 25 und 26 anzuwenden sind.\" "
    "Fuer die Auditvorbereitung folgt daraus zweierlei: das Testprogramm ist Teil des "
    "Rahmenwerks, das nach Artikel 6 Absatz 5 mindestens einmal jährlich dokumentiert und "
    "überprüft wird, und die Basistests nach Artikel 26 sind nicht optional, nur weil das "
    "Unternehmen nicht TLPT-pflichtig ist. Kleinstunternehmen sind vom Programm nach "
    "Artikel 24 ausgenommen, unterliegen aber Artikel 25 Absatz 3."
    .replace("Fuer", "Für"),
    "Article 24(1) DORA requires financial entities other than microenterprises to "
    "establish, maintain and review a sound and comprehensive digital operational "
    "resilience testing programme, expressly \"as an integral part of the ICT "
    "risk-management framework referred to in Article 6\". Paragraph 2 adds: \"The digital "
    "operational resilience testing programme shall include a range of assessments, tests, "
    "methodologies, practices and tools to be applied in accordance with Articles 25 and "
    "26.\" Two consequences for audit preparation: the testing programme is part of the "
    "framework that is documented and reviewed at least once a year under Article 6(5), "
    "and the baseline tests under Article 25 are not optional merely because the entity is "
    "not in scope for TLPT. Microenterprises are outside Article 24 but are addressed by "
    "Article 25(3).",
))

QUESTIONS.append(q(
    "dora-audit-testprogramm-02", "testprogramm", False,
    "Art. 24 Abs. 6 VO (EU) 2022/2554", 4, True, "a",
    "Ein Finanzunternehmen testet seine kritischen Kernbankanwendungen alle drei Jahre "
    "im Rahmen eines großen Testzyklus. In welchem Mindestrhythmus verlangt Artikel 24 "
    "Absatz 6 DORA Tests bei IKT-Systemen und -Anwendungen, die kritische oder wichtige "
    "Funktionen unterstützen?",
    {
        "a": "Mindestens einmal jährlich sind angemessene Tests bei allen IKT-Systemen und "
             "-Anwendungen durchzuführen, die kritische oder wichtige Funktionen "
             "unterstützen.",
        "b": "Mindestens alle drei Jahre, entsprechend dem TLPT-Zyklus nach Artikel 26 "
             "Absatz 1.",
        "c": "Nur anlassbezogen nach wesentlichen Änderungen oder schwerwiegenden "
             "IKT-bezogenen Vorfällen.",
        "d": "Nur bei denjenigen Systemen, bei denen ein früherer Test Schwächen "
             "aufgedeckt hat.",
    },
    "A financial entity tests its critical core banking applications every three years as "
    "part of a large test cycle. What minimum frequency does Article 24(6) DORA require "
    "for ICT systems and applications supporting critical or important functions?",
    {
        "a": "At least yearly, appropriate tests must be conducted on all ICT systems and "
             "applications supporting critical or important functions.",
        "b": "At least every three years, in line with the TLPT cycle under Article 26(1).",
        "c": "Only on an ad hoc basis after substantive changes or major ICT-related "
             "incidents.",
        "d": "Only on those systems where an earlier test revealed weaknesses.",
    },
    "Artikel 24 Absatz 6 DORA lautet: Finanzunternehmen, die keine Kleinstunternehmen "
    "sind, \"stellen sicher, dass bei allen IKT-Systemen und -Anwendungen, die kritische "
    "oder wichtige Funktionen unterstützen, mindestens einmal jährlich angemessene Tests "
    "durchgeführt werden\". Das ist eine eigenständige Jahresfrequenz und hat mit dem "
    "Dreijahreszyklus des TLPT nach Artikel 26 Absatz 1 nichts zu tun: TLPT ist die "
    "erweiterte Testform für einen kleinen Kreis benannter Unternehmen, Artikel 24 Absatz "
    "6 gilt für jedes Finanzunternehmen, das kein Kleinstunternehmen ist. Diese Verwechslung "
    "ist der häufigste Prüfungsbefund in diesem Bereich. Was \"angemessen\" ist, richtet "
    "sich nach dem risikobasierten Ansatz des Artikels 24 Absatz 3; eine bestimmte "
    "Testtiefe schreibt DORA nicht vor.",
    "Article 24(6) DORA reads: financial entities other than microenterprises \"shall "
    "ensure, at least yearly, that appropriate tests are conducted on all ICT systems and "
    "applications supporting critical or important functions\". This is a free-standing "
    "annual frequency and has nothing to do with the three-year TLPT cycle in Article "
    "26(1): TLPT is the advanced form of testing for a small identified population, whereas "
    "Article 24(6) binds every financial entity that is not a microenterprise. Conflating "
    "the two is the most common audit finding in this area. What counts as \"appropriate\" "
    "follows the risk-based approach in Article 24(3); DORA prescribes no particular test "
    "depth.",
))

QUESTIONS.append(q(
    "dora-audit-testprogramm-03", "testprogramm", False,
    "Art. 24 Abs. 5 VO (EU) 2022/2554", 4, True, "c",
    "Nach einem Penetrationstest legt das Sicherheitsteam einen Bericht vor, eröffnet "
    "für jeden Befund ein Ticket im Change-Management und schließt die Tickets nach "
    "Umsetzung der Fixes. Der Prüfer beanstandet die Vorgehensweise. Was fehlt nach "
    "Artikel 24 Absatz 5 DORA?",
    {
        "a": "Nichts. Ticketeröffnung und -schließung erfüllen die Anforderungen von "
             "Artikel 24 Absatz 5 vollständig.",
        "b": "Die Meldung der Testergebnisse an die zuständige Behörde innerhalb von "
             "72 Stunden.",
        "c": "Festgelegte Verfahren und Leitlinien zur Priorisierung, Klassifizierung und "
             "Behebung aller zutage getretenen Probleme sowie interne "
             "Validierungsmethoden, mit denen festgestellt wird, dass alle ermittelten "
             "Schwächen, Mängel oder Lücken vollständig angegangen werden.",
        "d": "Eine Bescheinigung eines externen Wirtschaftsprüfers über jeden einzelnen "
             "behobenen Befund.",
    },
    "After a penetration test the security team files a report, opens a change-management "
    "ticket for every finding and closes the tickets once the fixes are deployed. The "
    "auditor challenges this approach. What is missing under Article 24(5) DORA?",
    {
        "a": "Nothing. Opening and closing tickets fully satisfies Article 24(5).",
        "b": "Notification of the test results to the competent authority within 72 hours.",
        "c": "Established procedures and policies to prioritise, classify and remedy all "
             "issues revealed, plus internal validation methodologies to ascertain that all "
             "identified weaknesses, deficiencies or gaps are fully addressed.",
        "d": "An external auditor's attestation for each individual remediated finding.",
    },
    "Artikel 24 Absatz 5 DORA verlangt zwei getrennte Dinge. Erstens: Finanzunternehmen, "
    "die keine Kleinstunternehmen sind, \"legen Verfahren und Leitlinien zur Priorisierung, "
    "Klassifizierung und Behebung aller während der Durchführung der Tests zutage "
    "getretenen Probleme fest\". Zweitens, und das ist der Punkt, den ein Ticketsystem "
    "allein nicht abdeckt: sie \"legen interne Validierungsmethoden fest, um "
    "sicherzustellen, dass alle ermittelten Schwächen, Mängel oder Lücken vollständig "
    "angegangen werden\". Ein geschlossenes Ticket belegt, dass jemand etwas getan hat; "
    "die Validierungsmethode belegt, dass es gewirkt hat. In der Auditakte sind daher beide "
    "Artefakte nachzuweisen. Eine Meldepflicht an die Aufsicht für gewöhnliche "
    "Testergebnisse enthält Artikel 24 nicht; Meldepflichten regeln Artikel 17 bis 20 für "
    "Vorfälle und Artikel 26 Absatz 6 für TLPT.",
    "Article 24(5) DORA requires two separate things. First, financial entities other than "
    "microenterprises \"shall establish procedures and policies to prioritise, classify and "
    "remedy all issues revealed throughout the performance of the tests\". Second, and this "
    "is what a ticketing system alone does not deliver, they \"shall establish internal "
    "validation methodologies to ascertain that all identified weaknesses, deficiencies or "
    "gaps are fully addressed\". A closed ticket evidences that somebody did something; the "
    "validation methodology evidences that it worked. Both artefacts therefore belong in "
    "the audit file. Article 24 contains no duty to report ordinary test results to the "
    "supervisor; reporting duties sit in Articles 17 to 20 for incidents and in Article "
    "26(6) for TLPT.",
))

QUESTIONS.append(q(
    "dora-audit-testprogramm-04", "testprogramm", False,
    "Art. 25 Abs. 1 und 2 VO (EU) 2022/2554", 3, False, "d",
    "Welche Aussage über die in Artikel 25 DORA genannten Testarten trifft zu?",
    {
        "a": "Artikel 25 nennt ausschließlich automatisierte technische Verfahren; "
             "organisatorische Prüfungen sind nicht erfasst.",
        "b": "Artikel 25 nennt nur den Penetrationstest und den TLPT als zulässige "
             "Testarten.",
        "c": "Quellcodeprüfungen sind nach Artikel 25 ausnahmslos verpflichtend, "
             "Überprüfungen der physischen Sicherheit dagegen ausgeschlossen.",
        "d": "Die Aufzählung ist offen und umfasst unter anderem Überprüfungen der "
             "physischen Sicherheit, Fragebögen und Quellcodeprüfungen, letztere aber "
             "ausdrücklich nur \"soweit durchführbar\"; zusätzlich müssen Zentralverwahrer "
             "und zentrale Gegenparteien Schwachstellenbewertungen vor jedem Einsatz oder "
             "Wiedereinsatz durchführen.",
    },
    "Which statement about the types of test named in Article 25 DORA is correct?",
    {
        "a": "Article 25 names only automated technical procedures; organisational reviews "
             "are outside its scope.",
        "b": "Article 25 names only penetration testing and TLPT as permitted test types.",
        "c": "Source code reviews are mandatory without exception under Article 25, whereas "
             "physical security reviews are excluded.",
        "d": "The list is open-ended and includes, among others, physical security reviews, "
             "questionnaires and source code reviews, the latter expressly only \"where "
             "feasible\"; in addition, central securities depositories and central "
             "counterparties must perform vulnerability assessments before any deployment "
             "or redeployment.",
    },
    "Artikel 25 Absatz 1 DORA fuehrt die Testarten mit der Wendung \"wie etwa\" ein, die "
    "Aufzählung ist also nicht abschließend: \"Schwachstellenbewertung und -scans, "
    "Open-Source-Analysen, Netzwerksicherheitsbewertungen, Lückenanalysen, Überprüfungen "
    "der physischen Sicherheit, Fragebögen und Scans von Softwarelösungen, "
    "Quellcodeprüfungen soweit durchführbar, szenariobasierte Tests, Kompatibilitätstests, "
    "Leistungstests, End-to-End-Tests und Penetrationstests\". Zwei Punkte sind fuer die "
    "Auditvorbereitung wichtig: Überprüfungen der physischen Sicherheit und Fragebögen sind "
    "ausdrücklich genannt, das Testprogramm ist also nicht rein technisch; und die "
    "Quellcodeprüfung steht unter dem Vorbehalt \"soweit durchführbar\", was bei "
    "Standardsoftware Dritter praktisch relevant ist. Artikel 25 Absatz 2 richtet sich nur "
    "an Zentralverwahrer und zentrale Gegenparteien und verlangt von ihnen "
    "Schwachstellenbewertungen, \"bevor Anwendungen und Infrastrukturkomponenten sowie "
    "IKT-Dienstleistungen, die kritische oder wichtige Funktionen des Finanzunternehmens "
    "unterstützen, eingesetzt oder wieder eingesetzt werden\"."
    .replace("fuehrt", "führt").replace("fuer die", "für die"),
    "Article 25(1) DORA introduces the test types with the words \"such as\", so the list is "
    "not exhaustive: \"vulnerability assessments and scans, open source analyses, network "
    "security assessments, gap analyses, physical security reviews, questionnaires and "
    "scanning software solutions, source code reviews where feasible, scenario-based tests, "
    "compatibility testing, performance testing, end-to-end testing and penetration "
    "testing\". Two points matter for audit preparation: physical security reviews and "
    "questionnaires are expressly named, so the testing programme is not purely technical; "
    "and source code review carries the qualifier \"where feasible\", which is practically "
    "relevant for third-party off-the-shelf software. Article 25(2) is addressed only to "
    "central securities depositories and central counterparties and requires them to perform "
    "vulnerability assessments \"before any deployment or redeployment of new or existing "
    "applications and infrastructure components, and ICT services supporting critical or "
    "important functions of the financial entity\".",
))

QUESTIONS.append(q(
    "dora-audit-testprogramm-05", "testprogramm", False,
    "Art. 11 Abs. 3 und Abs. 6 VO (EU) 2022/2554", 3, False, "b",
    "Die Interne Revision prüft die Testabdeckung der IKT-Geschäftsfortführungspläne und "
    "der IKT-Reaktions- und Wiederherstellungspläne. Was verlangt Artikel 11 DORA?",
    {
        "a": "Diese Pläne sind vom Testprogramm ausgenommen, weil sie bereits vom "
             "Leitungsorgan genehmigt wurden.",
        "b": "Die Pläne sind bei IKT-Systemen, die alle Funktionen unterstützen, mindestens "
             "jährlich sowie bei jeder wesentlichen Änderung an IKT-Systemen für kritische "
             "oder wichtige Funktionen zu testen; Unternehmen, die keine Kleinstunternehmen "
             "sind, müssen dabei Szenarien für Cyberangriffe und Umschaltvorgänge auf "
             "Redundanzkapazitäten einbeziehen.",
        "c": "Ein Test alle drei Jahre genügt, sofern er im Rahmen eines TLPT stattfindet.",
        "d": "Es genügt ein Schreibtischtest der Dokumentation ohne technische Ausführung, "
             "sofern die Ergebnisse protokolliert werden.",
    },
    "Internal audit is reviewing the test coverage of the ICT business continuity plans and "
    "the ICT response and recovery plans. What does Article 11 DORA require?",
    {
        "a": "These plans are outside the testing programme because the management body has "
             "already approved them.",
        "b": "The plans must be tested at least yearly in relation to ICT systems supporting "
             "all functions, and on any substantive change to ICT systems supporting "
             "critical or important functions; entities other than microenterprises must "
             "include scenarios of cyber-attacks and switchovers to redundant capacity.",
        "c": "A test every three years is sufficient, provided it takes place within a TLPT.",
        "d": "A desktop walk-through of the documentation without technical execution is "
             "sufficient, provided the results are minuted.",
    },
    "Artikel 11 Absatz 6 Buchstabe a DORA verlangt: Finanzunternehmen \"testen bei "
    "IKT-Systemen, die alle Funktionen unterstützen, mindestens jährlich sowie im Falle "
    "jeglicher wesentlicher Änderungen an IKT-Systemen, die kritische oder wichtige "
    "Funktionen unterstützen, die IKT-Geschäftsfortführungspläne sowie die IKT-Reaktions- "
    "und Wiederherstellungspläne\". Unterabsatz 2 ergänzt, dass Finanzunternehmen, die keine "
    "Kleinstunternehmen sind, in die Testpläne Szenarien für Cyberangriffe und "
    "Umschaltvorgänge zwischen der primären IKT-Infrastruktur und den Redundanzkapazitäten, "
    "Backups und Ausweichanlagen aufnehmen. Ergänzend bestimmt Artikel 11 Absatz 3, dass die "
    "IKT-Reaktions- und Wiederherstellungspläne \"einer unabhängigen internen Revision zu "
    "unterziehen sind, sofern es sich bei dem Finanzunternehmen nicht um ein "
    "Kleinstunternehmen handelt\". Fuer die Auditakte heißt das: Testnachweis, "
    "Szenarioabdeckung und eine unabhaengige Revisionsfeststellung sind drei verschiedene "
    "Belege."
    .replace("Fuer", "Für").replace("unabhaengige", "unabhängige"),
    "Article 11(6)(a) DORA requires financial entities to \"test the ICT business continuity "
    "plans and the ICT response and recovery plans in relation to ICT systems supporting all "
    "functions at least yearly, as well as in the event of any substantive changes to ICT "
    "systems supporting critical or important functions\". The second subparagraph adds that "
    "entities other than microenterprises must include in the testing plans scenarios of "
    "cyber-attacks and switchovers between the primary ICT infrastructure and the redundant "
    "capacity, backups and redundant facilities. Article 11(3) separately provides that the "
    "ICT response and recovery plans \"shall be subject to independent internal audit "
    "reviews\" for entities other than microenterprises. For the audit file that means three "
    "distinct artefacts: the test evidence, the scenario coverage, and an independent "
    "internal audit finding.",
))

# ---------------------------------------------------------------------------
# Topic 2 - tlpt_scoping (Art. 26 DORA, Art. 2/9/11 RTS 2025/1190)
# ---------------------------------------------------------------------------

QUESTIONS.append(q(
    "dora-audit-tlpt_scoping-01", "tlpt_scoping", True,
    "Art. 26 Abs. 1 i.V.m. Abs. 8 UAbs. 3 und Art. 16 Abs. 1 VO (EU) 2022/2554", 4, True, "c",
    "Ein Vorstand fragt die Interne Revision, wann das Haus seinen ersten "
    "bedrohungsorientierten Penetrationstest (TLPT) durchführen muss. Welche Aussage gibt "
    "die Rechtslage nach Artikel 26 DORA korrekt wieder?",
    {
        "a": "Jedes Finanzunternehmen muss jährlich einen TLPT durchführen.",
        "b": "Jedes Finanzunternehmen, das kein Kleinstunternehmen ist, muss mindestens alle "
             "drei Jahre einen TLPT durchführen.",
        "c": "TLPT-pflichtig sind nur die von der zuständigen Behörde nach Artikel 26 Absatz "
             "8 Unterabsatz 3 ermittelten Finanzunternehmen; diese führen mindestens alle "
             "drei Jahre einen TLPT durch, wobei die Behörde die Häufigkeit verringern oder "
             "erhöhen kann. Unternehmen nach Artikel 16 Absatz 1 Unterabsatz 1 und "
             "Kleinstunternehmen sind ausgenommen.",
        "d": "TLPT ist durchgehend freiwillig und dient nur der Reifegradmessung.",
    },
    "A board member asks internal audit when the firm must carry out its first threat-led "
    "penetration test (TLPT). Which statement correctly reflects Article 26 DORA?",
    {
        "a": "Every financial entity must carry out a TLPT every year.",
        "b": "Every financial entity that is not a microenterprise must carry out a TLPT at "
             "least every three years.",
        "c": "Only financial entities identified by the competent authority under Article "
             "26(8), third subparagraph, are in scope; those entities carry out a TLPT at "
             "least every three years, and the authority may reduce or increase that "
             "frequency. Entities referred to in Article 16(1), first subparagraph, and "
             "microenterprises are excluded.",
        "d": "TLPT is voluntary throughout and serves only to measure maturity.",
    },
    "Artikel 26 Absatz 1 DORA lautet: \"Gemäß Absatz 8 Unterabsatz 3 des vorliegenden "
    "Artikels ermittelte Finanzunternehmen, bei denen es sich weder um die in Artikel 16 "
    "Absatz 1 Unterabsatz 1 genannten Unternehmen noch um Kleinstunternehmen handelt, führen "
    "mindestens alle drei Jahre anhand von TLPT erweiterte Tests durch. Auf der Grundlage "
    "des Risikoprofils des Finanzunternehmens und unter Berücksichtigung der betrieblichen "
    "Gegebenheiten kann die zuständige Behörde das Finanzunternehmen erforderlichenfalls "
    "auffordern, die Häufigkeit dieser Tests zu verringern oder zu erhöhen.\" Der Satz "
    "enthält drei Filter, die in der Praxis regelmäßig übersehen werden: eine positive "
    "Ermittlung durch die zuständige Behörde, den Ausschluss der in Artikel 16 Absatz 1 "
    "Unterabsatz 1 genannten Unternehmen (unter anderem kleine und nicht verflochtene "
    "Wertpapierfirmen, bestimmte ausgenommene Zahlungs- und E-Geld-Institute, kleine "
    "Einrichtungen der betrieblichen Altersversorgung) und den Ausschluss von "
    "Kleinstunternehmen im Sinne des Artikels 3 Nummer 60. TLPT ist also die Ausnahme, nicht "
    "die Regel. Die jährliche Testpflicht nach Artikel 24 Absatz 6 bleibt davon unberührt.",
    "Article 26(1) DORA reads: \"Financial entities, other than entities referred to in "
    "Article 16(1), first subparagraph, and other than microenterprises, which are identified "
    "in accordance with paragraph 8, third subparagraph, of this Article, shall carry out at "
    "least every 3 years advanced testing by means of TLPT. Based on the risk profile of the "
    "financial entity and taking into account operational circumstances, the competent "
    "authority may, where necessary, request the financial entity to reduce or increase this "
    "frequency.\" The sentence contains three filters that are regularly overlooked in "
    "practice: a positive identification by the competent authority, the exclusion of the "
    "entities listed in Article 16(1), first subparagraph (among others small and "
    "non-interconnected investment firms, certain exempted payment and electronic money "
    "institutions, small institutions for occupational retirement provision), and the "
    "exclusion of microenterprises within the meaning of Article 3(60). TLPT is therefore the "
    "exception, not the rule. The yearly testing duty under Article 24(6) is unaffected.",
))

QUESTIONS.append(q(
    "dora-audit-tlpt_scoping-02", "tlpt_scoping", False,
    "Art. 2 Abs. 1 und 2 Del. VO (EU) 2025/1190", 4, False, "a",
    "Nach welchem Mechanismus bestimmt die TLPT-Behörde, welche Finanzunternehmen einen "
    "TLPT durchführen müssen (Delegierte Verordnung (EU) 2025/1190)?",
    {
        "a": "Artikel 2 Absatz 1 nennt einen Katalog von Auswirkungs-, Systemrelevanz- und "
             "IKT-Risikofaktoren; Absatz 2 zählt zusätzlich Unternehmensgruppen auf, von "
             "denen die Behörde einen TLPT verlangt, es sei denn, die Bewertung nach Absatz "
             "1 ergibt, dass Auswirkungen, Finanzstabilitätsbedenken oder IKT-Risikoprofil "
             "einen TLPT nicht rechtfertigen.",
        "b": "Ausschlaggebend ist allein die Zahl der Beschäftigten und die Bilanzsumme.",
        "c": "Alle Kreditinstitute sind ohne weitere Prüfung TLPT-pflichtig.",
        "d": "Die Unternehmen melden sich selbst; eine behördliche Ermittlung findet nicht "
             "statt.",
    },
    "By what mechanism does the TLPT authority determine which financial entities must "
    "perform a TLPT (Delegated Regulation (EU) 2025/1190)?",
    {
        "a": "Article 2(1) sets out a catalogue of impact-related, systemic-character and "
             "ICT risk-related factors; Article 2(2) additionally lists categories of entity "
             "from which the authority shall require a TLPT, unless the assessment under "
             "paragraph 1 indicates that impact, financial stability concerns or the ICT risk "
             "profile do not justify a TLPT.",
        "b": "Headcount and balance-sheet total alone are decisive.",
        "c": "All credit institutions are in scope for TLPT without further assessment.",
        "d": "Entities self-declare; there is no identification by an authority.",
    },
    "Delegierte Verordnung (EU) 2025/1190 ist der nach Artikel 26 Absatz 11 DORA "
    "erlassene technische Regulierungsstandard; sie wurde am 13. Februar 2025 angenommen und "
    "im Amtsblatt L, 2025/1190 vom 18. Juni 2025 veröffentlicht. Artikel 2 Absatz 1 verlangt "
    "von den TLPT-Behörden eine Bewertung anhand eines zweiteiligen Kriterienkatalogs: "
    "Faktoren in Verbindung mit Auswirkungen und systemischem Charakter (unter anderem "
    "Größe, Verflechtung, Kritikalität, Substituierbarkeit, Komplexität des "
    "Geschäftsmodells) und IKT-risikobezogene Faktoren (unter anderem Risikoprofil, "
    "Bedrohungslage, Abhängigkeit kritischer Funktionen von IKT-Systemen, Reifegrad der "
    "Erkennungs- und Reaktionsmaßnahmen). Artikel 2 Absatz 2 fügt eine widerlegliche Regel "
    "hinzu: \"Die TLPT-Behörden verlangen von allen folgenden Finanzunternehmen die "
    "Durchführung von TLPT, es sei denn, die Bewertung eines Finanzunternehmens gemäß Absatz "
    "1 hat ergeben, dass seine Auswirkungen, Bedenken hinsichtlich der Finanzstabilität in "
    "Bezug auf das betreffende Finanzunternehmen oder sein IKT-Risikoprofil die Durchführung "
    "eines TLPT nicht rechtfertigen\" Erfasst sind unter anderem als global oder anderweitig "
    "systemrelevant eingestufte Kreditinstitute und ihre Teile, Zahlungsinstitute und "
    "E-Geld-Institute oberhalb bestimmter Transaktionsschwellen, Zentralverwahrer, zentrale "
    "Gegenparteien, bestimmte Handelsplätze sowie große Versicherungs- und "
    "Rückversicherungsunternehmen. Wichtig fuer die Auditvorbereitung: Auf der Liste zu "
    "stehen begründet keine automatische Pflicht, und nicht auf der Liste zu stehen "
    "begründet keine Freistellung, denn Absatz 1 gilt fuer jedes Finanzunternehmen."
    .replace("fuer die Auditvorbereitung", "für die Auditvorbereitung")
    .replace("fuer jedes", "für jedes"),
    "Delegated Regulation (EU) 2025/1190 is the regulatory technical standard adopted under "
    "the Article 26(11) DORA mandate; it was adopted on 13 February 2025 and published in "
    "OJ L, 2025/1190 of 18 June 2025. Article 2(1) requires TLPT authorities to assess "
    "entities against a two-part catalogue: impact-related and systemic-character factors "
    "(among others size, interconnectedness, criticality, substitutability, complexity of the "
    "business model) and ICT risk-related factors (among others risk profile, threat "
    "landscape, dependence of critical functions on ICT systems, maturity of detection and "
    "mitigation measures). Article 2(2) adds a rebuttable rule: \"TLPT authorities shall "
    "require all of the following financial entities to perform TLPT, unless the assessment "
    "referred to in paragraph 1 in respect of a financial entity indicates that its impact, "
    "the financial stability concerns relating to that financial entity, or its ICT risk "
    "profile, does not justify the performance of a TLPT\" The list covers, among others, "
    "credit institutions identified as globally or otherwise systemically important and parts "
    "of them, payment and electronic money institutions above stated transaction thresholds, "
    "central securities depositories, central counterparties, certain trading venues, and "
    "large insurance and reinsurance undertakings. Important for audit preparation: being on "
    "the list is not an automatic duty, and being off the list is not an exemption, because "
    "paragraph 1 applies to every financial entity.",
))

QUESTIONS.append(q(
    "dora-audit-tlpt_scoping-03", "tlpt_scoping", False,
    "Art. 26 Abs. 2 VO (EU) 2022/2554", 4, True, "d",
    "Ein Finanzunternehmen plant, den TLPT aus Risikogründen in einer vollständigen "
    "Spiegelumgebung der Produktion durchzuführen und den Testumfang eigenständig "
    "festzulegen. Wie ist das nach Artikel 26 Absatz 2 DORA zu bewerten?",
    {
        "a": "Zulässig, sofern die Spiegelumgebung technisch identisch ist.",
        "b": "Zulässig, denn DORA äußert sich zur Testumgebung nicht.",
        "c": "Unzulässig hinsichtlich der Umgebung, aber der Testumfang darf ohne Beteiligung "
             "der Aufsicht festgelegt werden.",
        "d": "In beiden Punkten unzulässig: Der TLPT wird an Live-Produktionssystemen "
             "durchgeführt, die mehrere oder alle kritischen oder wichtigen Funktionen "
             "unterstützen, und der genaue Umfang wird von den zuständigen Behörden "
             "validiert.",
    },
    "A financial entity plans, for risk reasons, to run its TLPT in a full mirror of the "
    "production environment and to set the test scope on its own. How does this stand under "
    "Article 26(2) DORA?",
    {
        "a": "Permissible, provided the mirror environment is technically identical.",
        "b": "Permissible, because DORA says nothing about the test environment.",
        "c": "Impermissible as to the environment, but the scope may be set without involving "
             "the supervisor.",
        "d": "Impermissible on both counts: the TLPT is performed on live production systems "
             "supporting several or all critical or important functions, and the precise "
             "scope is validated by the competent authorities.",
    },
    "Artikel 26 Absatz 2 Unterabsatz 1 DORA lautet: \"Jeder bedrohungsorientierte "
    "Penetrationstest schließt mehrere oder alle kritischen oder wichtigen Funktionen eines "
    "Finanzunternehmens ein und wird an Live-Produktionssystemen durchgeführt, die derartige "
    "Funktionen unterstützen.\" Unterabsatz 3 fügt hinzu: \"Finanzunternehmen bewerten, "
    "welche kritischen oder wichtigen Funktionen ein TLPT einschließen muss. Der genaue "
    "Umfang von TLPT ist vom Ergebnis dieser Bewertung abhängig und wird von den zuständigen "
    "Behörden validiert.\" Der Testumfang ist damit ein Vorschlag des Unternehmens und eine "
    "Entscheidung der Behörde. Nach Artikel 9 Absatz 6 der Delegierten Verordnung (EU) "
    "2025/1190 legt das Unternehmen innerhalb von sechs Monaten nach der Aufforderung ein "
    "Dokument zur Beschreibung des Testumfangs vor, und das Leitungsorgan genehmigt dieses "
    "Dokument. Die Risiken des Tests auf Produktivsystemen werden nicht durch Ausweichen in "
    "eine Testumgebung, sondern durch die Risikomanagementkontrollen nach Artikel 26 Absatz 5 "
    "und die Aussetzungs- und Purple-Teaming-Regeln des Artikels 11 Absatz 10 der Delegierten "
    "Verordnung aufgefangen.",
    "Article 26(2), first subparagraph, DORA reads: \"Each threat-led penetration test shall "
    "cover several or all critical or important functions of a financial entity, and shall be "
    "performed on live production systems supporting such functions.\" The third subparagraph "
    "adds: \"Financial entities shall assess which critical or important functions need to be "
    "covered by the TLPT. The result of this assessment shall determine the precise scope of "
    "TLPT and shall be validated by the competent authorities.\" The scope is therefore the "
    "entity's proposal and the authority's decision. Under Article 9(6) of Delegated "
    "Regulation (EU) 2025/1190 the entity submits a scope specification document within six "
    "months of the notification, and the management body approves that document. The risks of "
    "testing on production are addressed not by moving to a test environment but by the risk "
    "management controls in Article 26(5) DORA and by the suspension and limited "
    "purple-teaming rules in Article 11(10) of the Delegated Regulation.",
))

QUESTIONS.append(q(
    "dora-audit-tlpt_scoping-04", "tlpt_scoping", False,
    "Art. 26 Abs. 3 und 4 VO (EU) 2022/2554", 4, False, "b",
    "Ein Cloud-Anbieter, der eine kritische Funktion unterstützt, lehnt die Teilnahme an "
    "einem TLPT ab, weil andere Kunden außerhalb des DORA-Anwendungsbereichs beeinträchtigt "
    "würden. Was sieht Artikel 26 DORA vor?",
    {
        "a": "Der Anbieter kann nicht in den TLPT einbezogen werden; die betroffene Funktion "
             "fällt aus dem Testumfang heraus.",
        "b": "Das Finanzunternehmen und der IKT-Drittdienstleister können schriftlich "
             "vereinbaren, dass der Anbieter unmittelbar einen externen Tester beauftragt, "
             "um unter der Leitung eines benannten Finanzunternehmens einen gebündelten TLPT "
             "durchzuführen; dieser gilt als TLPT der beteiligten Finanzunternehmen.",
        "c": "Mit der Einbindung des Anbieters geht die Verantwortung für die Einhaltung von "
             "DORA insoweit auf den Anbieter über.",
        "d": "Die Einbeziehung von IKT-Drittdienstleistern in einen TLPT bedarf einer "
             "Einzelfallgenehmigung der Europäischen Kommission.",
    },
    "A cloud provider supporting a critical function refuses to take part in a TLPT because "
    "other customers outside the scope of DORA would be adversely affected. What does Article "
    "26 DORA provide?",
    {
        "a": "The provider cannot be included in the TLPT; the affected function drops out of "
             "the test scope.",
        "b": "The financial entity and the ICT third-party service provider may agree in "
             "writing that the provider contracts directly with an external tester in order "
             "to conduct, under the direction of one designated financial entity, a pooled "
             "TLPT; that pooled test counts as a TLPT carried out by the participating "
             "financial entities.",
        "c": "Including the provider transfers responsibility for compliance with DORA to the "
             "provider to that extent.",
        "d": "Including ICT third-party service providers in a TLPT requires case-by-case "
             "approval from the European Commission.",
    },
    "Artikel 26 Absatz 3 DORA stellt zunächst klar, dass das Finanzunternehmen bei "
    "Einbeziehung von IKT-Drittdienstleistern alle erforderlichen Maßnahmen und Vorkehrungen "
    "ergreift und \"jederzeit die volle Verantwortung für die Gewährleistung der Einhaltung "
    "dieser Verordnung\" trägt. Absatz 4 regelt genau den beschriebenen Konflikt: Ist "
    "vernünftigerweise davon auszugehen, dass sich die Einbindung nachteilig auf Qualität "
    "oder Sicherheit der Dienstleistungen für Kunden außerhalb des Anwendungsbereichs oder "
    "auf die Vertraulichkeit der zugehörigen Daten auswirkt, können Finanzunternehmen und "
    "Anbieter schriftlich einen gebündelten Test vereinbaren. Der Text bestimmt ausdrücklich: "
    "\"Die gebündelten Tests gelten als TLPT, die von den an den gebündelten Tests beteiligten "
    "Finanzunternehmen durchgeführt werden.\" Die Zahl der Beteiligten wird nach Komplexität "
    "und Art der Dienstleistungen angemessen austariert. Artikel 16 Absätze 4 und 5 der "
    "Delegierten Verordnung (EU) 2025/1190 regelt die Zusammenarbeit der TLPT-Behörden "
    "hierfür.",
    "Article 26(3) DORA first makes clear that where ICT third-party service providers are "
    "included, the financial entity takes the necessary measures and safeguards and \"shall "
    "retain at all times full responsibility for ensuring compliance with this Regulation\". "
    "Paragraph 4 governs exactly the conflict described: where the provider's participation "
    "is reasonably expected to have an adverse impact on the quality or security of services "
    "delivered to customers outside the scope of DORA, or on the confidentiality of the "
    "related data, the entity and the provider may agree in writing on a pooled test. The "
    "text expressly states: \"The pooled testing shall be considered TLPT carried out by the "
    "financial entities participating in the pooled testing.\" The number of participants is "
    "duly calibrated taking into account the complexity and types of services involved. "
    "Article 16(4) and (5) of Delegated Regulation (EU) 2025/1190 governs the cooperation "
    "between TLPT authorities for this purpose.",
))

QUESTIONS.append(q(
    "dora-audit-tlpt_scoping-05", "tlpt_scoping", False,
    "Art. 9 Abs. 2 und 6, Art. 11 Abs. 5 Del. VO (EU) 2025/1190", 3, False, "c",
    "Welche Fristen und Mindestdauern gelten nach der Delegierten Verordnung (EU) 2025/1190 "
    "für einen TLPT?",
    {
        "a": "Zwei Wochen aktive Red-Team-Testphase; das Scoping-Dokument genehmigt der CISO.",
        "b": "Vier Wochen aktive Red-Team-Testphase; ein Scoping-Dokument ist nicht "
             "vorgesehen.",
        "c": "Informationen zur Einleitung des TLPT innerhalb von drei Monaten und das vom "
             "Leitungsorgan genehmigte Dokument zur Beschreibung des Testumfangs innerhalb "
             "von sechs Monaten nach der Aufforderung; die aktive Red-Team-Testphase dauert "
             "in jedem Fall mindestens zwölf Wochen.",
        "d": "Es gibt weder eine Mindestdauer für die aktive Testphase noch Fristen für die "
             "Vorbereitungsdokumente.",
    },
    "What deadlines and minimum durations does Delegated Regulation (EU) 2025/1190 set for a "
    "TLPT?",
    {
        "a": "Two weeks of active red team testing; the scoping document is approved by the "
             "CISO.",
        "b": "Four weeks of active red team testing; no scoping document is required.",
        "c": "TLPT initiation information within three months and the scope specification "
             "document, approved by the management body, within six months of the "
             "notification; the active red team testing phase lasts in any case at least "
             "twelve weeks.",
        "d": "There is neither a minimum duration for the active testing phase nor any "
             "deadline for the preparatory documents.",
    },
    "Artikel 9 Absatz 2 der Delegierten Verordnung (EU) 2025/1190 bestimmt: \"Das "
    "Finanzunternehmen übermittelt den Testmanagern innerhalb von drei Monaten nach Erhalt "
    "der in Absatz 1 genannten Aufforderung alle folgenden Informationen über die Einleitung "
    "des TLPT\", darunter die Projektcharta, die Kontaktdaten des Leiters des Kontrollteams, "
    "Angaben zum beabsichtigten Einsatz interner oder externer Tester, die "
    "Kommunikationskanäle und den Codenamen. Artikel 9 Absatz 6 verlangt binnen sechs "
    "Monaten ein Dokument zur Beschreibung des Testumfangs und bestimmt ausdrücklich: \"Das "
    "Leitungsorgan des Finanzunternehmens genehmigt das Scoping-Dokument.\" Artikel 11 Absatz "
    "5 legt fest, dass die Dauer der aktiven Red-Team-Testphase im Verhältnis zu Umfang, "
    "Größe und Komplexität steht \"und beträgt in jedem Fall mindestens zwölf Wochen\". Die "
    "Mindestdauer ist ein harter Wert, der in die Kapazitäts- und Budgetplanung gehört; für "
    "die Auditakte ist der Genehmigungsbeschluss des Leitungsorgans zum Scoping-Dokument der "
    "am häufigsten fehlende Beleg.",
    "Article 9(2) of Delegated Regulation (EU) 2025/1190 provides: \"A financial entity shall, "
    "within 3 months from having received the notification referred to in paragraph 1, submit "
    "to the test managers all of the following TLPT initiation information\", including the "
    "project charter, the contact details of the control team lead, information on the "
    "intended use of internal or external testers, the communication channels and the code "
    "name. Article 9(6) requires a scope specification document within six months and states "
    "expressly: \"The management body of the financial entity shall approve the scope "
    "specification document.\" Article 11(5) provides that the duration of the active red team "
    "testing phase shall be proportionate to scope, scale and complexity \"and in any case "
    "shall last for at least 12 weeks\". The minimum duration is a hard figure that belongs in "
    "capacity and budget planning; for the audit file, the management body's approval decision "
    "on the scope specification document is the single most frequently missing artefact.",
))

# ---------------------------------------------------------------------------
# Topic 3 - tester_governance (Art. 24(4), 26(8), 27 DORA; Art. 6 DORA)
# ---------------------------------------------------------------------------

QUESTIONS.append(q(
    "dora-audit-tester_governance-01", "tester_governance", True,
    "Art. 24 Abs. 4 VO (EU) 2022/2554", 3, False, "a",
    "Wer darf die Tests des Testprogramms nach Artikel 24 DORA durchführen?",
    {
        "a": "Unabhängige Parteien, interne oder externe; bei internen Testern sind "
             "ausreichende Ressourcen bereitzustellen und Interessenkonflikte während der "
             "Konzeptions- und Durchführungsphase zu vermeiden.",
        "b": "Ausschließlich externe, von einer Akkreditierungsstelle zertifizierte "
             "Dienstleister.",
        "c": "Interne Teams nur dann, wenn die zuständige Behörde dies für jeden einzelnen "
             "Test vorab genehmigt.",
        "d": "Jede beliebige Stelle; ein Unabhängigkeitserfordernis besteht für die "
             "Basistests nicht.",
    },
    "Who may carry out the tests in the testing programme under Article 24 DORA?",
    {
        "a": "Independent parties, whether internal or external; where internal testers are "
             "used, sufficient resources must be dedicated and conflicts of interest avoided "
             "throughout the design and execution phases.",
        "b": "Exclusively external providers certified by an accreditation body.",
        "c": "Internal teams only where the competent authority approves each individual test "
             "in advance.",
        "d": "Any party at all; there is no independence requirement for baseline tests.",
    },
    "Artikel 24 Absatz 4 DORA lautet: \"Finanzunternehmen, die keine Kleinstunternehmen sind, "
    "stellen sicher, dass Tests von unabhängigen, internen oder externen Parteien "
    "durchgeführt werden. Werden die Tests von einem internen Tester durchgeführt, stellen "
    "die Finanzunternehmen ausreichende Ressourcen bereit und tragen dafür Sorge, dass "
    "während der Konzeptions- und Durchführungsphase der Prüfung keine Interessenkonflikte "
    "entstehen.\" Wichtig ist die Abgrenzung zum TLPT: Die aufsichtliche Vorabgenehmigung "
    "interner Tester und das Erfordernis eines externen Anbieters von Bedrohungsanalysen "
    "stehen in Artikel 27 Absatz 2 und gelten nur für TLPT, nicht für die Basistests nach "
    "Artikel 25. Wer diese beiden Regime vermischt, prüft entweder zu viel oder zu wenig.",
    "Article 24(4) DORA reads: \"Financial entities, other than microenterprises, shall ensure "
    "that tests are undertaken by independent parties, whether internal or external. Where "
    "tests are undertaken by an internal tester, financial entities shall dedicate sufficient "
    "resources and ensure that conflicts of interest are avoided throughout the design and "
    "execution phases of the test.\" The distinction from TLPT matters: supervisory prior "
    "approval of internal testers and the requirement of an external threat intelligence "
    "provider sit in Article 27(2) and apply only to TLPT, not to the baseline tests under "
    "Article 25. Conflating the two regimes leads either to over-testing or under-testing.",
))

QUESTIONS.append(q(
    "dora-audit-tester_governance-02", "tester_governance", False,
    "Art. 26 Abs. 8 UAbs. 1 und 2 VO (EU) 2022/2554", 4, True, "d",
    "Ein bedeutendes Kreditinstitut im Sinne des Artikels 6 Absatz 4 der Verordnung (EU) "
    "Nr. 1024/2013 plant, seinen TLPT mit einem internen Red Team durchzuführen. Was gilt?",
    {
        "a": "Zulässig, sofern jeder dritte Test extern beauftragt wird.",
        "b": "Zulässig, sofern die TLPT-Behörde den Einsatz interner Tester genehmigt.",
        "c": "Zulässig ohne Einschränkung, weil DORA interne Tester generell gleichstellt.",
        "d": "Unzulässig: Bedeutende Kreditinstitute ziehen nur externe Tester gemäß Artikel "
             "27 Absatz 1 Buchstaben a bis e heran. Die Regel \"für jeden dritten Test einen "
             "externen Tester\" gilt für die übrigen Unternehmen.",
    },
    "A credit institution classified as significant within the meaning of Article 6(4) of "
    "Regulation (EU) No 1024/2013 plans to run its TLPT with an internal red team. What "
    "applies?",
    {
        "a": "Permissible, provided every third test is contracted externally.",
        "b": "Permissible, provided the TLPT authority approves the use of internal testers.",
        "c": "Permissible without restriction, because DORA treats internal testers as equal "
             "throughout.",
        "d": "Not permissible: significant credit institutions shall only use external testers "
             "in accordance with Article 27(1), points (a) to (e). The \"external testers "
             "every three tests\" rule applies to the other entities.",
    },
    "Artikel 26 Absatz 8 DORA enthält zwei getrennte Regeln. Unterabsatz 1: \"Ziehen "
    "Finanzunternehmen für die Zwecke der Durchführung von TLPT interne Tester heran, so "
    "beauftragen sie für jeden dritten Test einen externen Tester.\" Unterabsatz 2: "
    "\"Kreditinstitute, die gemäß Artikel 6 Absatz 4 der Verordnung (EU) Nr. 1024/2013 als "
    "bedeutend eingestuft wurden, ziehen nur externe Tester gemäß Artikel 27 Absatz 1 "
    "Buchstaben a bis e heran.\" Für bedeutende Institute besteht damit keine "
    "Genehmigungsoption; der Ausschluss interner Tester ist absolut. Der Verweis auf Artikel "
    "27 Absatz 1 Buchstaben a bis e schließt zugleich aus, dass die Zusatzbedingungen des "
    "Artikels 27 Absatz 2 für interne Tester hier überhaupt zur Anwendung kommen könnten.",
    "Article 26(8) DORA contains two separate rules. First subparagraph: \"When financial "
    "entities use internal testers for the purposes of undertaking TLPT, they shall contract "
    "external testers every three tests.\" Second subparagraph: \"Credit institutions that are "
    "classified as significant in accordance with Article 6(4) of Regulation (EU) No 1024/2013, "
    "shall only use external testers in accordance with Article 27(1), points (a) to (e).\" For "
    "significant institutions there is therefore no approval route; the exclusion of internal "
    "testers is absolute. The reference to Article 27(1), points (a) to (e), also means that "
    "the additional internal-tester conditions in Article 27(2) cannot come into play here at "
    "all.",
))

QUESTIONS.append(q(
    "dora-audit-tester_governance-03", "tester_governance", False,
    "Art. 27 Abs. 2 VO (EU) 2022/2554", 4, True, "b",
    "Ein Finanzunternehmen möchte den TLPT mit internen Testern durchführen und die "
    "Bedrohungsanalyse von der eigenen Cyber Threat Intelligence-Einheit erstellen lassen. "
    "Welche Zusatzbedingungen des Artikels 27 Absatz 2 DORA sind zu beachten?",
    {
        "a": "Nur eine Anzeige an die zuständige Behörde; inhaltliche Bedingungen bestehen "
             "nicht.",
        "b": "Der Einsatz muss von der zuständigen Behörde oder der benannten einzigen "
             "staatlichen Behörde genehmigt sein, die Behörde muss ausreichende Ressourcen "
             "und die Vermeidung von Interessenkonflikten überprüft haben, und der Anbieter "
             "von Bedrohungsanalysen darf nicht dem Finanzunternehmen angehören.",
        "c": "Die interne Bedrohungsanalyse ist zulässig, sofern sie organisatorisch vom "
             "Red Team getrennt ist.",
        "d": "Es gelten dieselben Bedingungen wie für externe Tester; Zusatzbedingungen "
             "bestehen nicht.",
    },
    "A financial entity wants to run its TLPT with internal testers and have the threat "
    "intelligence produced by its own cyber threat intelligence unit. Which additional "
    "conditions in Article 27(2) DORA apply?",
    {
        "a": "Only a notification to the competent authority; there are no substantive "
             "conditions.",
        "b": "The use must be approved by the relevant competent authority or the designated "
             "single public authority, that authority must have verified sufficient dedicated "
             "resources and the avoidance of conflicts of interest, and the threat "
             "intelligence provider must be external to the financial entity.",
        "c": "Internal threat intelligence is permissible provided it is organisationally "
             "separated from the red team.",
        "d": "The same conditions apply as for external testers; there are no additional "
             "conditions.",
    },
    "Artikel 27 Absatz 2 DORA lautet: \"Beim Einsatz interner Tester gewährleisten "
    "Finanzunternehmen, dass neben den Anforderungen in Absatz 1 auch folgende Bedingungen "
    "erfüllt sind: a) der Einsatz wurde von der jeweils zuständigen Behörde oder von der "
    "gemäß Artikel 26 Absätze 9 und 10 benannten einzigen staatlichen Behörde genehmigt; b) "
    "die jeweils zuständige Behörde hat überprüft, dass das Finanzunternehmen über "
    "ausreichende Ressourcen verfügt und sichergestellt hat, dass während der Konzeptions- "
    "und Durchführungsphase der Tests keine Interessenkonflikte entstehen; und c) der "
    "Anbieter von Bedrohungsanalysen gehört nicht dem Finanzunternehmen an.\" Buchstabe c ist "
    "der Punkt, an dem die meisten internen Planungen scheitern: Interne Tester sind unter "
    "Bedingungen zulässig, ein interner Anbieter von Bedrohungsanalysen ist es nicht, und "
    "eine organisatorische Trennung heilt das nicht. Artikel 15 der Delegierten Verordnung "
    "(EU) 2025/1190 ergänzt die Vorkehrungen für interne Tester.",
    "Article 27(2) DORA reads: \"When using internal testers, financial entities shall ensure "
    "that, in addition to the requirements in paragraph 1, the following conditions are met: "
    "(a) such use has been approved by the relevant competent authority or by the single "
    "public authority designated in accordance with Article 26(9) and (10); (b) the relevant "
    "competent authority has verified that the financial entity has sufficient dedicated "
    "resources and ensured that conflicts of interest are avoided throughout the design and "
    "execution phases of the test; and (c) the threat intelligence provider is external to the "
    "financial entity.\" Point (c) is where most in-house plans fail: internal testers are "
    "permissible subject to conditions, an internal threat intelligence provider is not, and "
    "organisational separation does not cure this. Article 15 of Delegated Regulation (EU) "
    "2025/1190 supplements the arrangements for internal testers.",
))

QUESTIONS.append(q(
    "dora-audit-tester_governance-04", "tester_governance", False,
    "Art. 27 Abs. 1 VO (EU) 2022/2554", 3, False, "c",
    "Ein Anbieter bewirbt sich als externer TLPT-Tester und legt Zertifikate seiner "
    "Mitarbeitenden vor, ist aber selbst nicht von einer Akkreditierungsstelle zertifiziert. "
    "Wie ist das nach Artikel 27 Absatz 1 DORA zu beurteilen?",
    {
        "a": "Ausgeschlossen: Ohne Zertifizierung durch eine Akkreditierungsstelle in einem "
             "Mitgliedstaat ist der Einsatz unzulässig.",
        "b": "Unbeachtlich: Artikel 27 Absatz 1 stellt keine Anforderungen an die "
             "Qualifikation der Tester.",
        "c": "Möglich: Artikel 27 Absatz 1 Buchstabe c lässt als Alternative zur "
             "Zertifizierung durch eine Akkreditierungsstelle die Einhaltung formaler "
             "Verhaltenskodizes oder ethischer Rahmenregelungen zu. Die übrigen Anforderungen "
             "der Buchstaben a, b, d und e, darunter die Berufshaftpflichtversicherung, "
             "müssen jedoch erfüllt sein.",
        "d": "Möglich, sofern die Mitarbeitenden über eine namentlich in DORA genannte "
             "Zertifizierung wie CISA oder OSCP verfügen.",
    },
    "A provider applies as an external TLPT tester and produces certifications held by its "
    "staff, but is not itself certified by an accreditation body. How does this stand under "
    "Article 27(1) DORA?",
    {
        "a": "Ruled out: without certification by an accreditation body in a Member State the "
             "engagement is impermissible.",
        "b": "Irrelevant: Article 27(1) imposes no qualification requirements on testers.",
        "c": "Possible: Article 27(1)(c) allows adherence to formal codes of conduct or "
             "ethical frameworks as an alternative to certification by an accreditation body. "
             "The remaining requirements in points (a), (b), (d) and (e), including "
             "professional indemnity insurance, must nevertheless be met.",
        "d": "Possible, provided staff hold a certification named in DORA such as CISA or "
             "OSCP.",
    },
    "Artikel 27 Absatz 1 DORA nennt fünf kumulative Anforderungen an Tester: sie müssen \"von "
    "höchster Eignung und Ansehen\" sein (Buchstabe a), \"über technische und organisatorische "
    "Fähigkeiten verfügen und spezifisches Fachwissen in den Bereichen Bedrohungsanalyse, "
    "Penetrationstests und Red-Team-Tests nachweisen\" (Buchstabe b), \"von einer "
    "Akkreditierungsstelle in einem Mitgliedstaat zertifiziert wurden oder formale "
    "Verhaltenskodizes oder ethische Rahmenregelungen einhalten\" (Buchstabe c), eine "
    "unabhängige Gewähr oder einen Auditbericht vorlegen (Buchstabe d) und \"ordnungsgemäß "
    "und vollständig durch einschlägige Berufshaftpflichtversicherungen abgesichert sind, "
    "einschließlich einer Versicherung gegen das Risiko von Fehlverhalten und "
    "Fahrlässigkeit\" (Buchstabe e). Buchstabe c ist alternativ formuliert, nicht kumulativ. "
    "DORA nennt keine einzige Zertifizierung namentlich, weder CISA noch OSCP, CREST oder "
    "OSCE. Artikel 7 Absatz 1 der Delegierten Verordnung (EU) 2025/1190 konkretisiert "
    "zusätzlich Erfahrungsjahre und Referenzen, ohne ein bestimmtes Zertifikat zu verlangen.",
    "Article 27(1) DORA sets out five cumulative requirements for testers: they must be \"of "
    "the highest suitability and reputability\" (point (a)), \"possess technical and "
    "organisational capabilities and demonstrate specific expertise in threat intelligence, "
    "penetration testing and red team testing\" (point (b)), \"are certified by an "
    "accreditation body in a Member State or adhere to formal codes of conduct or ethical "
    "frameworks\" (point (c)), provide an independent assurance or an audit report (point (d)) "
    "and \"are duly and fully covered by relevant professional indemnity insurances, including "
    "against risks of misconduct and negligence\" (point (e)). Point (c) is framed as an "
    "alternative, not a cumulative requirement. DORA names no certification at all, neither "
    "CISA nor OSCP, CREST or OSCE. Article 7(1) of Delegated Regulation (EU) 2025/1190 adds "
    "concrete requirements on years of experience and references, again without requiring any "
    "particular certificate.",
))

QUESTIONS.append(q(
    "dora-audit-tester_governance-05", "tester_governance", False,
    "Art. 6 Abs. 4 und 6 VO (EU) 2022/2554", 3, False, "a",
    "Welche Anforderungen stellt Artikel 6 DORA an die organisatorische Aufstellung und an "
    "die Revisoren, die den IKT-Risikomanagementrahmen prüfen?",
    {
        "a": "Die Zuständigkeit für Management und Überwachung des IKT-Risikos liegt bei einer "
             "hinreichend unabhängigen Kontrollfunktion; IKT-Risikomanagement-, Kontroll- und "
             "interne Revisionsfunktionen sind nach dem Modell der drei Verteidigungslinien "
             "oder einem internen Modell für Risikomanagement und Kontrolle angemessen zu "
             "trennen; die Revisoren müssen über ausreichendes Wissen, Fähigkeiten und "
             "Fachkenntnisse im Bereich IKT-Risiken sowie über angemessene Unabhängigkeit "
             "verfügen.",
        "b": "Die interne Revision darf das IKT-Risikomanagement selbst verantworten, sofern "
             "sie darüber berichtet.",
        "c": "Die interne Revision kann vollständig durch einen externen "
             "Wirtschaftsprüfungsauftrag ersetzt werden.",
        "d": "DORA stellt keine Anforderungen an die Qualifikation der Revisoren; maßgeblich "
             "ist allein der Revisionsplan.",
    },
    "What does Article 6 DORA require as regards organisational set-up and the auditors who "
    "review the ICT risk management framework?",
    {
        "a": "Responsibility for managing and overseeing ICT risk sits with a control function "
             "having an appropriate level of independence; ICT risk management, control and "
             "internal audit functions must be appropriately segregated according to the three "
             "lines of defence model or an internal risk management and control model; and the "
             "auditors must possess sufficient knowledge, skills and expertise in ICT risk as "
             "well as appropriate independence.",
        "b": "Internal audit may itself own ICT risk management, provided it reports on it.",
        "c": "Internal audit may be replaced entirely by an external audit engagement.",
        "d": "DORA imposes no qualification requirements on auditors; only the audit plan "
             "matters.",
    },
    "Artikel 6 Absatz 4 DORA verlangt von Finanzunternehmen, die keine Kleinstunternehmen "
    "sind, die Zuständigkeit für Management und Überwachung des IKT-Risikos einer "
    "Kontrollfunktion zu übertragen und deren angemessene Unabhängigkeit sicherzustellen; "
    "weiter heißt es: \"Die Finanzunternehmen sorgen für eine angemessene Trennung und "
    "Unabhängigkeit von IKT-Risikomanagementfunktionen, Kontrollfunktionen und internen "
    "Revisionsfunktionen gemäß dem Modell der drei Verteidigungslinien oder einem internen "
    "Modell für Risikomanagement und Kontrolle.\" Artikel 6 Absatz 6 stellt Anforderungen an "
    "die Personen: \"Diese Revisoren verfügen über ausreichendes Wissen und ausreichende "
    "Fähigkeiten und Fachkenntnisse im Bereich IKT-Risiken sowie über eine angemessene "
    "Unabhängigkeit\"; Häufigkeit und Schwerpunkt der IKT-Revisionen sind den IKT-Risiken "
    "entsprechend angemessen. Abgrenzungshinweis: Die Genehmigung der IKT-Revisionspläne durch "
    "das Leitungsorgan nach Artikel 5 Absatz 2 Buchstabe f und das förmliche "
    "Follow-up-Verfahren nach Artikel 6 Absatz 7 sind Gegenstand des Moduls für "
    "Leitungsorgane und werden hier nicht erneut geprüft.",
    "Article 6(4) DORA requires financial entities other than microenterprises to assign "
    "responsibility for managing and overseeing ICT risk to a control function and to ensure an "
    "appropriate level of independence of that function; it continues: \"Financial entities "
    "shall ensure appropriate segregation and independence of ICT risk management functions, "
    "control functions, and internal audit functions, according to the three lines of defence "
    "model, or an internal risk management and control model.\" Article 6(6) sets requirements "
    "for the individuals: \"Those auditors shall possess sufficient knowledge, skills and "
    "expertise in ICT risk, as well as appropriate independence\"; the frequency and focus of "
    "ICT audits shall be commensurate to the ICT risk of the entity. Boundary note: the "
    "management body's approval of ICT internal audit plans under Article 5(2)(f) and the formal "
    "follow-up process under Article 6(7) belong to the executive module and are not re-tested "
    "here.",
))

# ---------------------------------------------------------------------------
# Topic 4 - nachweise_audit
# ---------------------------------------------------------------------------

QUESTIONS.append(q(
    "dora-audit-nachweise_audit-01", "nachweise_audit", True,
    "Art. 26 Abs. 6 und 7 VO (EU) 2022/2554", 4, True, "d",
    "Der TLPT ist abgeschlossen. Was ist der Behörde vorzulegen, und welche Wirkung hat die "
    "ausgestellte Bescheinigung?",
    {
        "a": "Der vollständige Red-Team-Testbericht einschließlich aller technischen "
             "Angriffsdetails; die Bescheinigung befreit von der weiteren Verantwortung für "
             "die Auswirkungen des Tests.",
        "b": "Nichts; die Ergebnisse verbleiben beim Unternehmen, und die Bescheinigung wird "
             "unaufgefordert von der Behörde ausgestellt.",
        "c": "Nur der Plan mit Abhilfemaßnahmen; die Bescheinigung gilt als Nachweis der "
             "vollständigen DORA-Konformität des Unternehmens.",
        "d": "Eine Zusammenfassung der maßgeblichen Ergebnisse, die Pläne mit Abhilfemaßnahmen "
             "und die Unterlagen, mit denen belegt wird, dass der TLPT anforderungsgemäß "
             "durchgeführt wurde; die Bescheinigung dient der gegenseitigen Anerkennung "
             "zwischen den zuständigen Behörden, und das Unternehmen bleibt jederzeit in "
             "vollem Umfang für die Auswirkungen der Tests verantwortlich.",
    },
    "The TLPT is complete. What must be provided to the authority, and what effect does the "
    "attestation have?",
    {
        "a": "The full red team test report including all technical attack detail; the "
             "attestation relieves the entity of further responsibility for the impact of the "
             "test.",
        "b": "Nothing; the results stay with the entity, and the attestation is issued by the "
             "authority unprompted.",
        "c": "Only the remediation plan; the attestation counts as proof of the entity's full "
             "compliance with DORA.",
        "d": "A summary of the relevant findings, the remediation plans and the documentation "
             "demonstrating that the TLPT has been conducted in accordance with the "
             "requirements; the attestation serves mutual recognition between competent "
             "authorities, and the entity remains at all times fully responsible for the impact "
             "of the tests.",
    },
    "Artikel 26 Absatz 6 DORA lautet: \"Nach Abschluss der Tests und der Ausarbeitung von "
    "Berichten und Plänen mit Abhilfemaßnahmen legen das Finanzunternehmen und gegebenenfalls "
    "die externen Tester der gemäß Absatz 9 oder 10 benannten Behörde eine Zusammenfassung der "
    "maßgeblichen Ergebnisse, die Pläne mit Abhilfemaßnahmen und die Unterlagen vor, mit denen "
    "belegt wird, dass der TLPT anforderungsgemäß durchgeführt wurden.\" Absatz 7: \"Die "
    "Behörden stellen Finanzunternehmen eine Bescheinigung aus, aus der hervorgeht, dass der "
    "Test [...] im Einklang mit den Anforderungen durchgeführt wurde, um die gegenseitige "
    "Anerkennung bedrohungsorientierter Penetrationstests zwischen den zuständigen Behörden zu "
    "ermöglichen\"; und weiter: \"Unbeschadet einer solchen Bescheinigung bleiben "
    "Finanzunternehmen jederzeit in vollem Umfang für die Auswirkungen der in Absatz 4 "
    "genannten Tests verantwortlich.\" Die Bescheinigung bestätigt also die "
    "Anforderungskonformität des Tests, nicht die DORA-Konformität des Unternehmens, und sie "
    "verlagert keine Verantwortung. Die Anforderungen an ihren Inhalt stehen in Artikel 14 und "
    "Anhang VIII der Delegierten Verordnung (EU) 2025/1190.",
    "Article 26(6) DORA reads: \"At the end of the testing, after reports and remediation plans "
    "have been agreed, the financial entity and, where applicable, the external testers shall "
    "provide to the authority, designated in accordance with paragraph 9 or 10, a summary of "
    "the relevant findings, the remediation plans and the documentation demonstrating that the "
    "TLPT has been conducted in accordance with the requirements.\" Paragraph 7: \"Authorities "
    "shall provide financial entities with an attestation confirming that the test was "
    "performed in accordance with the requirements as evidenced in the documentation in order "
    "to allow for mutual recognition of threat led penetration tests between competent "
    "authorities\"; and further: \"Without prejudice to such attestation, financial entities "
    "shall remain at all times fully responsible for the impact of the tests referred to in "
    "paragraph 4.\" The attestation therefore confirms that the test met the requirements, not "
    "that the entity complies with DORA, and it shifts no responsibility. The required content "
    "is set out in Article 14 and Annex VIII of Delegated Regulation (EU) 2025/1190.",
))

QUESTIONS.append(q(
    "dora-audit-nachweise_audit-02", "nachweise_audit", False,
    "Art. 13 Abs. 1 und 2 Del. VO (EU) 2025/1190", 4, True, "c",
    "Welche Angaben muss der Plan mit Abhilfemaßnahmen nach Artikel 13 der Delegierten "
    "Verordnung (EU) 2025/1190 für jedes Ergebnis des TLPT enthalten?",
    {
        "a": "Nur eine Beschreibung der festgestellten Mängel und ein Zieldatum.",
        "b": "Nur die vorgeschlagenen Abhilfemaßnahmen und deren Kostenschätzung.",
        "c": "Beschreibung der festgestellten Mängel; Beschreibung der vorgeschlagenen "
             "Abhilfemaßnahmen einschließlich Priorisierung und voraussichtlichem Abschluss; "
             "Ursachenanalyse; die verantwortlichen Mitarbeiter oder Funktionen; sowie die "
             "Risiken einer ausbleibenden Umsetzung und gegebenenfalls die mit der Umsetzung "
             "verbundenen Risiken.",
        "d": "Eine Bestätigung der externen Tester, dass alle Befunde behoben wurden.",
    },
    "What must the remediation plan under Article 13 of Delegated Regulation (EU) 2025/1190 "
    "contain for each TLPT finding?",
    {
        "a": "Only a description of the identified shortcomings and a target date.",
        "b": "Only the proposed remediation measures and a cost estimate.",
        "c": "A description of the identified shortcomings; a description of the proposed "
             "remediation measures including their prioritisation and expected completion; a "
             "root cause analysis; the staff or functions responsible; and the risks of not "
             "implementing the measures and, where relevant, the risks associated with "
             "implementing them.",
        "d": "A confirmation by the external testers that all findings have been remediated.",
    },
    "Artikel 13 Absatz 1 der Delegierten Verordnung (EU) 2025/1190 setzt die Frist: "
    "\"Innerhalb von acht Wochen nach der in Artikel 12 Absatz 7 der vorliegenden Verordnung "
    "genannten Unterrichtung\" legt das Finanzunternehmen der TLPT-Behörde und, sofern "
    "abweichend, der zuständigen Behörde die Pläne mit Abhilfemaßnahmen und die Unterlagen nach "
    "Artikel 26 Absatz 6 DORA vor. Absatz 2 zählt fünf Pflichtangaben je Ergebnis auf: "
    "\"Beschreibung der festgestellten Mängel\"; \"Beschreibung der vorgeschlagenen "
    "Abhilfemaßnahmen, ihrer Priorisierung und ihres voraussichtlichen Abschlusses, "
    "gegebenenfalls einschließlich Maßnahmen zur Verbesserung der Identifizierungs-, Schutz-, "
    "Erkennungs- und Reaktionsfähigkeiten\"; \"Ursachenanalyse\"; \"Mitarbeiter oder Funktionen "
    "des Finanzunternehmens, die für die Umsetzung der vorgeschlagenen Abhilfemaßnahmen oder "
    "Verbesserungen verantwortlich sind\"; und \"Risiken in Verbindung mit einer ausbleibenden "
    "Umsetzung der unter Buchstabe b genannten Maßnahmen und gegebenenfalls die mit der "
    "Umsetzung dieser Maßnahmen verbundenen Risiken\". Ursachenanalyse und namentliche "
    "Verantwortungszuordnung sind die beiden Angaben, die in gewachsenen Findings-Listen "
    "typischerweise fehlen und die ein Prüfer zuerst sucht.",
    "Article 13(1) of Delegated Regulation (EU) 2025/1190 sets the deadline: \"Within 8 weeks "
    "from the notification referred to in Article 12(7) of this Regulation\", the entity "
    "provides the remediation plans and the documentation referred to in Article 26(6) DORA to "
    "the TLPT authority and, where different, to its competent authority. Paragraph 2 lists "
    "five mandatory items per finding: \"a description of the identified shortcomings\"; \"a "
    "description of the proposed remediation measures and of their prioritisation and expected "
    "completion, including, where relevant, measures to improve the identification, protection, "
    "detection and response capabilities\"; \"a root cause analysis\"; \"the financial entity's "
    "staff or functions responsible for the implementation of the proposed remediation measures "
    "or improvements\"; and \"the risks associated to not implementing the measures referred to "
    "in point (b) and, where relevant, risks associated to the implementation of such "
    "measures\". Root cause analysis and named ownership are the two items typically missing "
    "from organically grown findings lists, and the two an auditor looks for first.",
))

QUESTIONS.append(q(
    "dora-audit-nachweise_audit-03", "nachweise_audit", False,
    "Art. 6, 24 bis 27 und Art. 40 Abs. 4 VO (EU) 2022/2554", 4, True, "a",
    "Ein nach ISO/IEC 27001 zertifiziertes Finanzunternehmen argumentiert gegenüber der "
    "Aufsicht, das Zertifikat belege die Erfüllung der DORA-Anforderungen an Testprogramm und "
    "IKT-Risikomanagement. Wie ist das zu bewerten?",
    {
        "a": "Unzutreffend: DORA enthält keine Regelung, wonach eine Zertifizierung die "
             "Einhaltung der Verordnung ersetzt oder vermutet. Die Pflichten der Artikel 6 und "
             "24 bis 27 sind unabhängig davon zu erfüllen und einzeln nachzuweisen; ein "
             "bestehendes Managementsystem kann die Nachweisführung erleichtern, ersetzt sie "
             "aber nicht.",
        "b": "Zutreffend: DORA erkennt die ISO/IEC 27001-Zertifizierung als Nachweis der "
             "Konformität mit Artikel 6 an.",
        "c": "Zutreffend, soweit es um TLPT geht: Zertifizierte Unternehmen sind von Artikel 26 "
             "befreit.",
        "d": "Zutreffend: DORA sieht wie das Produktsicherheitsrecht eine Konformitätsvermutung "
             "bei Anwendung harmonisierter Normen vor.",
    },
    "A financial entity certified to ISO/IEC 27001 argues to its supervisor that the "
    "certificate evidences compliance with DORA's requirements on the testing programme and ICT "
    "risk management. How does this stand?",
    {
        "a": "Incorrect: DORA contains no provision under which a certification substitutes for, "
             "or gives rise to a presumption of, compliance with the Regulation. The duties in "
             "Articles 6 and 24 to 27 must be met and evidenced independently; an existing "
             "management system can make evidencing easier but does not replace it.",
        "b": "Correct: DORA recognises ISO/IEC 27001 certification as evidence of conformity "
             "with Article 6.",
        "c": "Correct as regards TLPT: certified entities are exempt from Article 26.",
        "d": "Correct: like product safety law, DORA provides for a presumption of conformity "
             "where harmonised standards are applied.",
    },
    "Eine Volltextprüfung des Verordnungstextes in beiden Sprachfassungen ergibt: DORA nennt "
    "ISO/IEC 27001 an keiner Stelle und enthält keine Konformitätsvermutung und keine "
    "Gleichwertigkeitsregel für Zertifizierungen. Der Begriff der Zertifizierung kommt im "
    "verfügenden Teil nur an zwei Stellen vor, und beide betreffen nicht die eigene Compliance "
    "des Finanzunternehmens: Artikel 27 Absatz 1 Buchstabe c für die Eignung von TLPT-Testern "
    "und Artikel 40 Absatz 4 Unterabsatz 2, wonach die federführende Überwachungsbehörde \"alle "
    "einschlägigen Zertifizierungen Dritter und interne oder externe IKT-Prüfungsberichte "
    "Dritter berücksichtigen\" kann, die ein kritischer IKT-Drittdienstleister zur Verfügung "
    "stellt. Eine Konformitätsvermutung durch harmonisierte Normen ist ein Mechanismus des "
    "Produktrechts, etwa des Cyberresilienzgesetzes, und gerade nicht des DORA-Regimes. "
    "Praktisch bedeutet das: Wer bereits nach ISO/IEC 27001 zertifiziert ist, hat für einen "
    "Teil der von DORA verlangten Gegenstände bereits Strukturen, Belege und Prüfroutinen "
    "aufgebaut, die sich thematisch überschneiden. Der Nachweis gegenüber der Aufsicht muss "
    "aber an den DORA-Vorschriften selbst geführt werden, und für Gegenstände wie Artikel 24 "
    "Absatz 6, Artikel 26 und Artikel 27 besteht keine unmittelbare Entsprechung.",
    "A full-text check of the Regulation in both language versions shows: DORA nowhere mentions "
    "ISO/IEC 27001 and contains no presumption of conformity and no equivalence rule for "
    "certifications. The concept of certification appears in the enacting terms in only two "
    "places, and neither concerns the financial entity's own compliance: Article 27(1)(c) on the "
    "suitability of TLPT testers, and Article 40(4), second subparagraph, under which the Lead "
    "Overseer \"may take into consideration any relevant third-party certifications and ICT "
    "third-party internal or external audit reports made available by the critical ICT "
    "third-party service provider\". A presumption of conformity through harmonised standards is "
    "a product law mechanism, for instance under the Cyber Resilience Act, and precisely not part "
    "of the DORA regime. In practice: an entity already certified to ISO/IEC 27001 will have "
    "built structures, evidence and review routines that address related ground for part of what "
    "DORA requires. But the demonstration to the supervisor has to be made against DORA's own "
    "provisions, and for subjects such as Article 24(6), Article 26 and Article 27 there is no "
    "direct counterpart.",
))

QUESTIONS.append(q(
    "dora-audit-nachweise_audit-04", "nachweise_audit", False,
    "Art. 15 Abs. 1 und 3 Del. VO (EU) 2025/1190", 3, False, "b",
    "Ein Finanzunternehmen setzt für seinen TLPT interne Tester ein. Welche Nachweise verlangt "
    "Artikel 15 der Delegierten Verordnung (EU) 2025/1190 zusätzlich?",
    {
        "a": "Keine; die Genehmigung der TLPT-Behörde nach Artikel 27 Absatz 2 DORA genügt.",
        "b": "Eine dokumentierte und regelmäßig überprüfte Strategie für das Management "
             "interner Tester, die unter anderem ein Testteam aus einem Testleiter und "
             "mindestens zwei weiteren Mitgliedern sowie eine mindestens zwölfmonatige "
             "vorherige Beschäftigung aller Teammitglieder verlangt; zudem ist der Einsatz "
             "interner Tester in den Einleitungsinformationen, im Red-Team-Testbericht und im "
             "zusammenfassenden Ergebnisbericht auszuweisen.",
        "c": "Nur eine Erklärung des CISO, dass keine Interessenkonflikte bestehen.",
        "d": "Eine externe Zertifizierung jedes internen Testers durch eine Akkreditierungsstelle.",
    },
    "A financial entity uses internal testers for its TLPT. What additional evidence does "
    "Article 15 of Delegated Regulation (EU) 2025/1190 require?",
    {
        "a": "None; the TLPT authority's approval under Article 27(2) DORA suffices.",
        "b": "A documented and periodically reviewed policy for the management of internal "
             "testers requiring, among other things, a test team consisting of a test lead and "
             "at least two additional members and that all team members have been employed for "
             "the preceding 12 months; in addition, the use of internal testers must be stated "
             "in the initiation information, in the red team test report and in the summary "
             "findings report.",
        "c": "Only a statement by the CISO that no conflicts of interest exist.",
        "d": "External certification of every internal tester by an accreditation body.",
    },
    "Artikel 15 Absatz 1 der Delegierten Verordnung (EU) 2025/1190 verlangt drei Vorkehrungen: "
    "eine Strategie für das Management interner Tester, Maßnahmen zum Schutz der allgemeinen "
    "Verteidigungs- und Resilienzfähigkeiten während des Tests und Maßnahmen zur Sicherstellung "
    "ausreichender Ressourcen und Fähigkeiten. Die Strategie muss Kriterien für Eignung, "
    "Kompetenz und potenzielle Interessenkonflikte enthalten, die Zuständigkeiten der "
    "Geschäftsleitung festlegen, \"dokumentiert und regelmäßig überprüft werden\", ein Testteam "
    "aus einem Testleiter und mindestens zwei zusätzlichen Mitgliedern vorsehen, verlangen, "
    "\"dass alle Mitglieder des Testteams in den vorangegangenen zwölf Monaten bei dem "
    "Finanzunternehmen oder einem gruppeninternen IKT-Dienstleister beschäftigt waren\", und "
    "Regelungen zur Schulung enthalten. Absatz 3 ergänzt die Transparenzpflicht: Der Einsatz "
    "interner Tester ist in den Einleitungsinformationen nach Artikel 9, im Red-Team-Testbericht "
    "nach Artikel 12 Absatz 2 und im zusammenfassenden Bericht nach Artikel 26 Absatz 6 DORA zu "
    "erwähnen. Absatz 4 stellt klar, dass Tester eines gruppeninternen IKT-Dienstleisters als "
    "interne Tester gelten. Hinweis zur deutschen Fassung: Artikel 15 Absatz 1 verwendet für "
    "die Leitung des internen Testteams das Wort Testmanager, das in Artikel 3 für die "
    "Testmanager der Aufsichtsbehörde definiert ist; die englische Fassung unterscheidet hier "
    "test lead und test manager. Gemeint sind zwei verschiedene Rollen.",
    "Article 15(1) of Delegated Regulation (EU) 2025/1190 requires three arrangements: a policy "
    "for the management of internal testers in a TLPT, measures to ensure that their use does "
    "not negatively impact the entity's general defensive or resilience capabilities during the "
    "test, and measures to ensure internal testers have sufficient resources and capabilities. "
    "The policy must contain criteria to assess suitability, competence and potential conflicts "
    "of interest, specify management responsibilities, \"be documented and periodically "
    "reviewed\", \"provide that the internal testing team includes a test lead, and at least two "
    "additional members\", \"require that all members of the test team have been employed by the "
    "financial entity or by an ICT intra-group service provider for the preceding 12 months\", "
    "and include provisions on training. Paragraph 3 adds a transparency duty: the use of "
    "internal testers must be mentioned in the initiation information under Article 9, in the red "
    "team test report under Article 12(2) and in the summary report under Article 26(6) DORA. "
    "Paragraph 4 clarifies that testers employed by an ICT intra-group service provider count as "
    "internal testers.",
))

QUESTIONS.append(q(
    "dora-audit-nachweise_audit-05", "nachweise_audit", False,
    "Art. 26 Abs. 11 VO (EU) 2022/2554 i.V.m. Del. VO (EU) 2025/1190", 4, True, "d",
    "Ein externer Prüfer fragt, ob der TLPT des Hauses nach der TIBER-EU-Methodik durchgeführt "
    "werden muss. Welche Antwort ist rechtlich korrekt?",
    {
        "a": "Ja: TIBER-EU ist ein Rechtsakt der Union und für alle TLPT verbindlich.",
        "b": "Ja: DORA verweist in Artikel 26 Absatz 1 auf TIBER-EU als verbindliche "
             "Testmethodik.",
        "c": "Nein: TIBER-EU steht in keinem Zusammenhang mit DORA und darf für TLPT nicht "
             "herangezogen werden.",
        "d": "Nein: Verbindlich sind die Artikel 26 und 27 DORA und die Delegierte Verordnung "
             "(EU) 2025/1190. Artikel 26 Absatz 11 DORA verpflichtet die ESA, den technischen "
             "Regulierungsstandard im Einvernehmen mit der EZB im Einklang mit dem "
             "TIBER-EU-Rahmen auszuarbeiten; TIBER-EU selbst ist ein Rahmenwerk der Zentralbanken "
             "und kein Unionsrechtsakt, und die Delegierte Verordnung stellt seine Anwendung "
             "ausdrücklich frei, soweit sie mit den rechtlichen Anforderungen im Einklang steht.",
    },
    "An external auditor asks whether the firm's TLPT must be conducted according to the "
    "TIBER-EU methodology. Which answer is legally correct?",
    {
        "a": "Yes: TIBER-EU is a Union legal act and is binding for all TLPTs.",
        "b": "Yes: Article 26(1) DORA refers to TIBER-EU as the binding testing methodology.",
        "c": "No: TIBER-EU has no connection with DORA and may not be used for TLPT.",
        "d": "No: what binds are Articles 26 and 27 DORA and Delegated Regulation (EU) 2025/1190. "
             "Article 26(11) DORA obliges the ESAs to develop the regulatory technical standard "
             "in agreement with the ECB in accordance with the TIBER-EU framework; TIBER-EU "
             "itself is a central bank framework, not a Union legal act, and the Delegated "
             "Regulation expressly leaves its application optional, in as much as it is "
             "consistent with the legal requirements.",
    },
    "Der einzige Verweis auf TIBER-EU im verfügenden Teil von DORA steht in Artikel 26 Absatz "
    "11: \"Die ESA arbeiten im Einvernehmen mit der EZB im Einklang mit dem TIBER-EU-Rahmen "
    "gemeinsame Entwürfe technischer Regulierungsstandards aus\". Adressat dieser Vorgabe sind "
    "die Europäischen Aufsichtsbehörden bei der Rechtsetzung, nicht die Finanzunternehmen bei der "
    "Testdurchführung. Der daraufhin erlassene technische Regulierungsstandard, die Delegierte "
    "Verordnung (EU) 2025/1190, hält in Erwägungsgrund 1 fest: \"Diese Verordnung wurde im "
    "Einklang mit dem TIBER-EU-Rahmen ausgearbeitet und spiegelt die Methodik, das Verfahren und "
    "die Struktur bedrohungsorientierter Penetrationstests\" wider; und weiter: "
    "\"Finanzunternehmen, die zur Durchführung von TLPT verpflichtet sind, können sich auf den "
    "TIBER-EU-Rahmen oder eine seiner nationalen Umsetzungen beziehen und diesen Rahmen oder die "
    "nationale Umsetzung anwenden, sofern dieser Rahmen oder die Umsetzung mit den Anforderungen "
    "der Artikel 26 und 27 der Verordnung (EU) 2022/2554 und der vorliegenden Verordnung im "
    "Einklang steht.\" Das Wort ist \"können\", nicht \"müssen\". Hintergrundinformation, nicht "
    "Rechtsgrundlage: TIBER-EU wurde 2018 von der Europäischen Zentralbank veröffentlicht und "
    "vom Eurosystem 2025 an die TLPT-Anforderungen angepasst. Praktisch ist die Frage oft "
    "entschieden, bevor sie sich stellt, weil die nationale TLPT-Behörde eine nationale "
    "TIBER-Umsetzung anwendet; rechtlich bleibt der Prüfmaßstab aber die Delegierte Verordnung.",
    "The only reference to TIBER-EU in DORA's enacting terms is in Article 26(11): \"The ESAs "
    "shall, in agreement with the ECB, develop joint draft regulatory technical standards in "
    "accordance with the TIBER-EU framework\". That instruction is addressed to the European "
    "Supervisory Authorities in their rule-making, not to financial entities in their testing. "
    "The resulting regulatory technical standard, Delegated Regulation (EU) 2025/1190, states in "
    "recital 1: \"This Regulation has been drafted in accordance with the TIBER-EU framework and "
    "mirrors the methodology, process and structure of threat-led penetration testing (TLPT) as "
    "described in TIBER-EU. Financial entities subject to TLPT may refer to and apply the "
    "TIBER-EU framework, or one of its national implementations, in as much as that framework or "
    "implementation is consistent with the requirements set out in Articles 26 and 27 of "
    "Regulation (EU) 2022/2554 and this Regulation.\" The word is \"may\", not \"shall\". "
    "Background, not legal basis: TIBER-EU was published by the European Central Bank in 2018 and "
    "updated by the Eurosystem in 2025 to align with the TLPT requirements. In practice the "
    "question is often settled before it arises, because the national TLPT authority applies a "
    "national TIBER implementation; legally, however, the yardstick remains the Delegated "
    "Regulation.",
))


# ---------------------------------------------------------------------------
# Meta block
# ---------------------------------------------------------------------------

META = {
    "app": "Zettacard / dora-audit-readiness-lernmodul",
    "version": "0.1-DRAFT",
    "generated": "2026-08-16",
    "description": (
        "DRAFT pilot questions for a B2B DORA module aimed at internal audit functions, "
        "CISOs and audit-preparation staff at EU financial entities who must produce "
        "evidence for a DORA compliance audit (internal audit, Big 4 external audit or a "
        "supervisory examination). Working title: \"Surviving the DORA Audit: Testing, "
        "Evidence, and ISO 27001 Alignment\"; roadmap module 3A, which the roadmap calls "
        "\"Surviving the CISA Audit\". CISA here means the ISACA credential Certified "
        "Information Systems Auditor, i.e. the professional qualification typically held by "
        "the people in this audience - it does NOT refer to the US Cybersecurity and "
        "Infrastructure Security Agency, and it is not an EU term at all; see the pre-review "
        "dossier for why the module name should be changed before any learner-facing use. "
        "Subject matter: Chapter IV of Regulation (EU) 2022/2554 (digital operational "
        "resilience testing, Art. 24 to 27), the internal audit and independence provisions "
        "of Art. 6(4) and 6(6) and Art. 11(3)/(6), and Commission Delegated Regulation (EU) "
        "2025/1190, the regulatory technical standard on threat-led penetration testing "
        "adopted under the Art. 26(11) mandate. Every citation was read in the Official "
        "Journal text in both the English and the German language versions on 2026-08-16 via "
        "the EU Publications Office Cellar repository. Deliberately non-overlapping with the "
        "sibling draft modules: board governance including the Art. 5(2)(f) internal-audit-plan "
        "approval duty is covered by dora_executive; vendor audit rights under Art. 30 and "
        "exit-strategy documentation under Art. 30(3)(f) and Art. 28(8) are covered by "
        "dora_procurement; incident reporting under Art. 17 to 20 is covered by dora_incident. "
        "Exit-strategy documentation is expressly NOT re-tested here. No question asserts that "
        "any certification, including ISO/IEC 27001, substitutes for DORA compliance; no ISO "
        "control text is quoted or paraphrased anywhere in this file. NOT legal advice; "
        "attorney sign-off required before any commercial use."
    ),
    "class": "ALL",
    "locales": ["de", "en"],
    "canonical_locale": "de",
    "point_system": "3-4 points per question, matching this app's existing style",
    "pass_rule_note": (
        "DRAFT: no EXAM_QUESTION_COUNT_BY_TYPE / MAX_ERROR_POINTS_BY_TYPE / "
        "EXAM_TIME_LIMIT_MS_BY_TYPE / EXAM_TOPIC_DRAW values are proposed for this module. "
        "The 5/5/5/5 topic split would support a 4- or 5-question draw touching every topic, "
        "but that is a design decision to be taken after legal sign-off. This module is not "
        "registered in data/build_modules.py or data/modules_manifest.json and app.js is "
        "untouched."
    ),
    "legal_review_status": (
        "AI-prepared draft, 2026-08-16, NOT reviewed by a qualified lawyer. Primary sources "
        "read in full in the Official Journal text, EN + DE, via the EU Publications Office "
        "Cellar repository (publications.europa.eu/resource/celex/<CELEX>): Regulation (EU) "
        "2022/2554 (DORA), CELEX 32022R2554, OJ L 333, 27.12.2022, p. 1 - Art. 3(17), 3(60), "
        "4, 6, 11, 16(1), 24, 25, 26, 27 and 40(4) read verbatim; Commission Delegated "
        "Regulation (EU) 2025/1190 of 13 February 2025, CELEX 32025R1190, OJ L, 2025/1190, "
        "18.6.2025 - the regulatory technical standard on threat-led penetration testing "
        "adopted under the Art. 26(11) DORA mandate, recitals and Art. 1 to 17 and Annexes VII "
        "and VIII read. Adopted status confirmed from the instrument's own OJ header and "
        "closing formula. Consolidated-version probe run with a positive control "
        "(02024R2956-20241202 returns a consolidation; 02025R1190-20250701 and "
        "02025R1190-20250101 return 404), so no corrigendum or amendment to Delegated "
        "Regulation (EU) 2025/1190 was found as at 2026-08-16. Full-text negative checks: the "
        "string ISO does not occur anywhere in DORA or in the RTS; DORA contains no "
        "presumption-of-conformity or certification-equivalence provision. TIBER-EU is a "
        "European Central Bank / Eurosystem framework, not a Union legal act; it is cited in "
        "this module only as guidance and no answer key depends on it. See "
        "docs/dora-audit-readiness-pre-review-dossier-2026-08-16.md for the full citation "
        "ledger, confidence tiers, deliberate non-assertions and gap list."
    ),
    "renewal_months": None,
    "renewal_basis": "not_specified_in_statute",
    "renewal_note": (
        "DORA fixes no training interval for audit or CISO staff. The genuine recurring "
        "obligations in this area are of a different kind and must not be presented as a "
        "training cadence: tests on all ICT systems and applications supporting critical or "
        "important functions at least yearly (Art. 24(6)); testing of ICT business continuity "
        "and ICT response and recovery plans at least yearly and on substantive changes (Art. "
        "11(6)(a)); documentation and review of the ICT risk management framework at least "
        "once a year (Art. 6(5)); and advanced testing by means of TLPT at least every 3 years "
        "for identified entities, which the competent authority may reduce or increase (Art. "
        "26(1))."
    ),
    "legal_disclaimer": DISCLAIMER_DE,
    "legal_disclaimer_en": (
        "This training material is provided for education and information purposes only and "
        "does not constitute legal or compliance advice. The regulatory requirements must be "
        "validated in each individual case by qualified lawyers or auditors."
    ),
    "acronym_note": (
        "CISA is a genuinely ambiguous acronym and this module must not use it carelessly. In "
        "the roadmap's working title \"Surviving the CISA Audit\" it means the ISACA "
        "credential Certified Information Systems Auditor - the professional qualification "
        "held by many internal and external IT auditors, i.e. the audience of this module. It "
        "does not mean the United States Cybersecurity and Infrastructure Security Agency, "
        "which has no role under DORA. Neither reading is an EU legal term; the EU instrument "
        "on the resilience of critical entities is Directive (EU) 2022/2557, whose established "
        "short form is CER, not CISA. Recommendation recorded in the pre-review dossier: drop "
        "the acronym from the learner-facing module title."
    ),
    "topic_codes": {k: v for k, v in TOPICS.items()},
}


def build():
    return {"meta": META, "questions": QUESTIONS}


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

ASCII_RESIDUE_PATTERNS = [
    "fuer", "ueber", "muessen", "koennen", "waere", "gefuehrt", "ausschliesslich",
    "faellt", "maessig", "groesse", "zustaendig", "behoerde", "moeglich", "spaetest",
    "unverzueglich", "gemaess", "pruef", "schaetz", "vorfaelle", "jaehrlich",
    "massnahm", "erfuell", "haerte", "verstoesse", "regelmaessig", "abhaengigkeit",
    "geldbusse", "vollstaendig", "naechste", "grundsaetzlich", "durchfuehr",
    "beruecksichtig", "haeufigkeit", "unabhaengig", "maengel", "schwaech",
    "genehmig ung", "ueberprue", "aendrung", "aenderung", "loesung", "kuerzest",
    "auszufuehr", "ergaenz", "traeger", "waehrend", "nachtraeglich", "bericht erstatt",
]

GERMAN_ASCII_WHITELIST = {
    # legitimately ASCII German words containing ae/oe/ue/ss
    "dass", "muss", "prozess", "prozesse", "prozessen", "beschluss", "abschluss",
    "abschlusses", "abschlussbericht", "auffassung", "lassen", "sodass", "aussage",
    "aussagen", "voraussichtlich", "voraussichtlichen", "ausserdem", "dauer", "dauern",
    "dauert", "genaue", "genauen", "genauer", "aufsicht", "aufsichtlichen",
    "aufsichtliche", "aufsichtsbehoerde", "auswirkung", "auswirkungen", "aufsichts",
    "ausreichende", "ausreichendes", "ausreichenden", "ausreichend", "aufgebaut",
    "ausgeschlossen", "ausschluss", "schliesslich", "kommission", "aussetzungs",
    "neue", "neuen", "kaufen", "auf", "aus", "auch", "haus", "hauses", "blaue",
    "grosse", "reihe", "aufwand", "ausgenommen", "aufnehmen", "aufnahme",
    "interessenkonflikte", "interessenkonflikten", "vertraulichkeit", "grundlage",
    "aufzaehlung", "ausgewiesen", "auszuweisen", "ausweisen", "aufgestellt",
    # further legitimately-ASCII German words verified by hand in this file
    "abgeschlossen", "adressat", "akkreditierungsstelle", "angemessen", "angemessene",
    "angepasst", "anlassbezogen", "ausschlaggebend", "bewusst", "erfasst",
    "ergebnisse", "erlassene", "erstzulassung", "fachkenntnisse", "fachwissen",
    "fassung", "genehmigungsbeschluss", "geschlossenes", "jahresfrequenz",
    "klassifizierung", "mindestdauer", "mindestdauern", "produktionssystemen",
    "regulierungsstandard", "regulierungsstandards", "reifegradmessung", "ressourcen",
    "sprachfassungen", "testergebnisse", "transaktionsschwellen", "umfassendes",
    "umfasst", "verbesserung", "verbesserungen", "voraussichtlichem", "wissen",
    "zuerst", "zusammenfassenden", "zusammenfassung",
    # English loanwords deliberately used in the German text (RTS terminology)
    "business", "blue", "red", "team", "teams", "purple", "teaming", "cyber",
    "intelligence", "charter",
}


def check(data):
    errors = []
    qs = data["questions"]

    # 1. count
    if len(qs) != 20:
        errors.append("expected 20 questions, got %d" % len(qs))

    # 2. schema parity with kartellrecht_pilot.json
    with open(TEMPLATE, encoding="utf-8") as fh:
        tmpl = json.load(fh)
    tkeys = list(tmpl["questions"][0].keys())
    for item in qs:
        if list(item.keys()) != tkeys:
            errors.append("schema key order mismatch in %s: %s" % (item["id"], list(item.keys())))
            break

    # 3. ids unique
    ids = [x["id"] for x in qs]
    if len(set(ids)) != len(ids):
        errors.append("duplicate question ids")

    # 4. answer key distribution
    from collections import Counter
    dist = Counter(x["correct"][0] for x in qs)
    if sorted(dist.items()) != [("a", 5), ("b", 5), ("c", 5), ("d", 5)]:
        errors.append("answer key distribution not 5/5/5/5: %s" % dict(dist))

    # 5. option-set integrity in both locales + correct key exists
    for item in qs:
        for loc in ("de", "en"):
            opts = item["text"][loc]["options"]
            if set(opts.keys()) != {"a", "b", "c", "d"}:
                errors.append("%s/%s option keys wrong" % (item["id"], loc))
            for k, v in opts.items():
                if not isinstance(v, str) or not v.strip():
                    errors.append("%s/%s/%s empty option" % (item["id"], loc, k))
            if item["correct"][0] not in opts:
                errors.append("%s/%s correct key missing" % (item["id"], loc))
            if not item["text"][loc]["question"].strip():
                errors.append("%s/%s empty question" % (item["id"], loc))
        for loc in ("de", "en"):
            if not item["explanation"][loc].strip():
                errors.append("%s/%s empty explanation" % (item["id"], loc))

    # 6. points and flags
    pts = Counter(x["points"] for x in qs)
    if pts.get(4) != 12 or pts.get(3) != 8:
        errors.append("points distribution not 12x4 / 8x3: %s" % dict(pts))
    hs = sum(1 for x in qs if x["high_stakes"])
    if hs != 10:
        errors.append("high_stakes count is %d, expected 10" % hs)
    gs = sum(1 for x in qs if x["grundstoff"])
    if gs != 4:
        errors.append("grundstoff count is %d, expected 4" % gs)

    # 7. topic balance
    tc = Counter(x["topic_code"] for x in qs)
    if sorted(tc.values()) != [5, 5, 5, 5]:
        errors.append("topic balance not 5/5/5/5: %s" % dict(tc))
    for item in qs:
        if item["topic"] != TOPICS[item["topic_code"]]["de"]:
            errors.append("%s topic label mismatch" % item["id"])
        if item["class_scope"] != ["ALL"] or item["roles"] != ["all"]:
            errors.append("%s class_scope/roles mismatch" % item["id"])
        if item["question_type"] != "single_choice" or item["image_ref"] is not None:
            errors.append("%s question_type/image_ref mismatch" % item["id"])

    # 8. German orthography
    def german_strings(obj):
        out = []
        for item in qs:
            out.append(item["text"]["de"]["question"])
            out.extend(item["text"]["de"]["options"].values())
            out.append(item["explanation"]["de"])
            out.append(item["topic"])
        out.append(META["legal_disclaimer"])
        out.append(META["renewal_note"])
        for v in TOPICS.values():
            out.append(v["de"])
        return out

    de_blob = "\n".join(german_strings(data))
    umlauts = {c: de_blob.count(c) for c in "äöüÄÖÜß"}
    total_umlauts = sum(umlauts.values())
    if total_umlauts == 0:
        errors.append("no umlaut/eszett characters found in German text")

    low = de_blob.lower()
    residue_hits = sorted({p for p in ASCII_RESIDUE_PATTERNS if p in low})
    if residue_hits:
        errors.append("ASCII transliteration residue: %s" % residue_hits)

    # exhaustive token audit
    tokens = re.findall(r"[A-Za-zÄÖÜäöüß]+", de_blob)
    suspects = set()
    for t in tokens:
        tl = t.lower()
        if any(ch in tl for ch in "äöüß"):
            continue
        if ("ae" in tl or "oe" in tl or "ue" in tl or "ss" in tl) and tl not in GERMAN_ASCII_WHITELIST:
            suspects.add(tl)
    if suspects:
        errors.append("unwhitelisted ASCII-suspect German tokens: %s" % sorted(suspects))

    # 9. no umlauts in English text
    en_blob = []
    for item in qs:
        en_blob.append(item["text"]["en"]["question"])
        en_blob.extend(item["text"]["en"]["options"].values())
        en_blob.append(item["explanation"]["en"])
    en_blob = "\n".join(en_blob)
    en_umlauts = sum(en_blob.count(c) for c in "äöüÄÖÜß")
    if en_umlauts:
        errors.append("English text contains %d umlaut characters" % en_umlauts)

    # 10. punctuation convention: straight quotes, ASCII hyphens, no control chars
    blob = json.dumps(data, ensure_ascii=False)
    banned = {
        "“": "left double quote", "”": "right double quote",
        "„": "german low double quote", "‘": "left single quote",
        "’": "right single quote", "–": "en dash", "—": "em dash",
        " ": "nbsp", "…": "ellipsis",
    }
    for ch, name in banned.items():
        if ch in blob:
            errors.append("banned character present (%s): %d" % (name, blob.count(ch)))
    for ch in blob:
        if unicodedata.category(ch) == "Cc" and ch not in "\n\t":
            errors.append("control character present")
            break

    return errors, umlauts, total_umlauts


if __name__ == "__main__":
    data = build()
    errs, umlauts, total = check(data)
    if errs:
        for e in errs:
            print("FAIL:", e, file=sys.stderr)
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("OK  wrote %s" % OUT)
    print("    questions: %d" % len(data["questions"]))
    print("    umlaut/eszett characters in German text: %d  %s" % (total, umlauts))
