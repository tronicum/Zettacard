#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic generator for data/cra_supply_chain_pilot_DRAFT.json.

Module: cra_supply_chain -- "CRA - Secure Supply Chain & Vulnerability Handling"
Roadmap module 2A ("Secure Supply Chain Coding"), B2B DORA/CRA roadmap 2026-08-16.

EN is the canonical locale for this pilot (audience: DevSecOps / CTOs in the
Polish and Romanian tech-hub markets). DE is produced as a secondary locale.

All legal content is grounded in the Official Journal text of Regulation (EU)
2024/2847 (Cyber Resilience Act), CELEX 32024R2847, OJ L, 2024/2847, 20.11.2024,
**as corrected** -- see docs/cra-supply-chain-pre-review-dossier-2026-08-16.md.

NOT wired into any build path. Not registered in build_modules.py or
modules_manifest.json. Run manually:  python3 data/gen_cra_supply_chain_draft.py
The script performs its own integrity + German-orthography checks and exits
non-zero on failure.
"""

import json
import os
import re
import sys
import unicodedata

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "cra_supply_chain_pilot_DRAFT.json")
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "kartellrecht_pilot.json")

KEY_ORDER = ["id", "topic", "topic_code", "class_scope", "grundstoff",
             "legal_basis", "points", "high_stakes", "question_type",
             "image_ref", "correct", "text", "explanation", "roles"]

TOPICS = {
    "scope_dates": ("Scope, definitions and application dates",
                    "Anwendungsbereich, Begriffsbestimmungen und Geltungsbeginn"),
    "manufacturer_duties": ("Manufacturer obligations and support period",
                            "Herstellerpflichten und Unterstützungszeitraum"),
    "sbom_vulnerability": ("SBOM and vulnerability handling",
                           "Software-Stückliste und Behandlung von Schwachstellen"),
    "reporting": ("Reporting obligations under Article 14",
                  "Meldepflichten nach Artikel 14"),
}

DISCLAIMER_DE = ("Dieses Schulungsmaterial dient reinen Ausbildungs- und "
                 "Informationszwecken und stellt keine Rechts- oder "
                 "Compliance-Beratung dar. Die regulatorischen Anforderungen "
                 "sind im Einzelfall durch qualifizierte Juristen oder "
                 "Wirtschaftsprüfer zu validieren.")

DISCLAIMER_EN = ("This training material is provided for education and "
                 "information purposes only and does not constitute legal or "
                 "compliance advice. Regulatory requirements must be validated "
                 "case by case by qualified lawyers or auditors.")


def Q(qid, topic_code, grundstoff, legal_basis, points, high_stakes, correct,
      q_en, o_en, q_de, o_de, exp_en, exp_de):
    return {
        "id": qid,
        "topic": TOPICS[topic_code][0],
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
            "en": {"question": q_en, "options": o_en},
            "de": {"question": q_de, "options": o_de},
        },
        "explanation": {"en": exp_en, "de": exp_de},
        "roles": ["all"],
    }


QUESTIONS = [

    # ---------------------------------------------------------------- topic A
    Q("cra-scope_dates-01", "scope_dates", True,
      "Art. 2(1), Art. 3(1) Regulation (EU) 2024/2847 (CRA)", 3, False, "b",
      "Your team ships an embedded controller. It has no internet stack of its "
      "own; it only talks over a serial bus to a gateway that is itself network "
      "connected. Does the Cyber Resilience Act apply to your controller?",
      {
        "a": "No. The CRA only applies to products that connect directly to the internet or to a public network.",
        "b": "Yes. The CRA applies to products with digital elements whose intended purpose or reasonably foreseeable use includes a direct or indirect logical or physical data connection to a device or network.",
        "c": "No. The CRA only applies to standalone software products, not to hardware or firmware.",
        "d": "Only if the controller is sold separately for payment; components supplied inside a larger product are always out of scope.",
      },
      "Ihr Team liefert einen eingebetteten Controller aus. Er hat keinen "
      "eigenen Internet-Stack, sondern kommuniziert nur über einen seriellen "
      "Bus mit einem Gateway, das seinerseits netzverbunden ist. Gilt die "
      "Cyberresilienz-Verordnung für Ihren Controller?",
      {
        "a": "Nein. Die CRA gilt nur für Produkte, die sich unmittelbar mit dem Internet oder einem öffentlichen Netz verbinden.",
        "b": "Ja. Die CRA gilt für Produkte mit digitalen Elementen, deren bestimmungsgemäßer Zweck oder vernünftigerweise vorhersehbare Verwendung eine direkte oder indirekte logische oder physische Datenverbindung mit einem Gerät oder Netz einschließt.",
        "c": "Nein. Die CRA gilt nur für eigenständige Softwareprodukte, nicht für Hardware oder Firmware.",
        "d": "Nur wenn der Controller separat gegen Bezahlung verkauft wird; in ein größeres Produkt eingebaute Komponenten sind stets ausgenommen.",
      },
      "Art. 2(1) CRA: the Regulation \"applies to products with digital elements "
      "made available on the market, the intended purpose or reasonably "
      "foreseeable use of which includes a direct or indirect logical or "
      "physical data connection to a device or network\". The word \"indirect\" "
      "is what catches the serial-bus case. Art. 3(1) defines a \"product with "
      "digital elements\" as \"a software or hardware product and its remote "
      "data processing solutions, including software or hardware components "
      "being placed on the market separately\" - so hardware, firmware, software "
      "and separately marketed components are all covered. Free-of-charge supply "
      "does not remove a product from scope (Art. 3(22)). Note the express "
      "carve-outs that do exist: medical devices, in-vitro diagnostics and motor "
      "vehicles under Arts. 2(2)(a)-(c), certified aviation products (Art. 2(3)), "
      "marine equipment (Art. 2(4)), identical spare parts (Art. 2(6)) and "
      "products developed or modified exclusively for national security or "
      "defence purposes (Art. 2(7)).",
      "Art. 2 Abs. 1 CRA: \"Diese Verordnung gilt für auf dem Markt "
      "bereitgestellte Produkte mit digitalen Elementen, deren "
      "bestimmungsgemäßer Zweck oder vernünftigerweise vorhersehbare Verwendung "
      "eine direkte oder indirekte logische oder physische Datenverbindung mit "
      "einem Gerät oder Netz einschließt.\" Das Wort \"indirekte\" erfasst genau den Bus-Fall. "
      "Art. 3 Nr. 1 definiert ein \"Produkt mit digitalen Elementen\" als \"ein "
      "Software- oder Hardwareprodukt und dessen Datenfernverarbeitungslösungen, "
      "einschließlich Software- oder Hardwarekomponenten, die getrennt in den "
      "Verkehr gebracht werden\". Hardware, Firmware, Software und separat "
      "vermarktete Komponenten sind also gleichermaßen erfasst. Unentgeltliche "
      "Abgabe nimmt ein Produkt nicht aus dem Anwendungsbereich (Art. 3 Nr. 22). "
      "Ausdrückliche Ausnahmen bestehen dagegen u. a. für Medizinprodukte, "
      "In-vitro-Diagnostika und Kraftfahrzeuge (Art. 2 Abs. 2), zertifizierte "
      "Luftfahrtprodukte (Art. 2 Abs. 3), Schiffsausrüstung (Art. 2 Abs. 4), "
      "identische Ersatzteile (Art. 2 Abs. 6) sowie Produkte, die ausschließlich "
      "für Zwecke der nationalen Sicherheit oder der Verteidigung entwickelt oder "
      "geändert wurden (Art. 2 Abs. 7)."),

    Q("cra-scope_dates-02", "scope_dates", False,
      "Art. 3(13) Regulation (EU) 2024/2847 (CRA)", 3, True, "c",
      "A Warsaw scale-up does not write the firmware itself: it commissions an "
      "external development house, then ships the resulting device under its own "
      "trademark, and gives the companion mobile app away free of charge. Who is "
      "the \"manufacturer\" under the CRA?",
      {
        "a": "The external development house, because it wrote the code.",
        "b": "Nobody, for the mobile app: products supplied free of charge have no manufacturer under the CRA.",
        "c": "The Warsaw scale-up, for both the device and the free app: a manufacturer is a person who develops or manufactures products with digital elements, or has them designed, developed or manufactured, and markets them under its own name or trademark, whether for payment, monetisation or free of charge.",
        "d": "Only the entity that is established in the Union and holds the CE file; a manufacturer outside the Union cannot be a CRA manufacturer.",
      },
      "Ein Warschauer Scale-up schreibt die Firmware nicht selbst, sondern "
      "beauftragt ein externes Entwicklungshaus, vertreibt das fertige Gerät "
      "dann unter der eigenen Marke und gibt die zugehörige Mobil-App "
      "unentgeltlich ab. Wer ist \"Hersteller\" im Sinne der CRA?",
      {
        "a": "Das externe Entwicklungshaus, weil es den Code geschrieben hat.",
        "b": "Für die Mobil-App niemand: Unentgeltlich abgegebene Produkte haben nach der CRA keinen Hersteller.",
        "c": "Das Warschauer Scale-up, und zwar für Gerät und kostenlose App: Hersteller ist, wer Produkte mit digitalen Elementen entwickelt oder herstellt oder konzipieren, entwickeln oder herstellen lässt und sie unter eigenem Namen oder eigener Marke vermarktet, sei es gegen Bezahlung, zur Monetarisierung oder unentgeltlich.",
        "d": "Nur die in der Union niedergelassene Stelle, die die CE-Akte führt; ein Hersteller außerhalb der Union kann kein CRA-Hersteller sein.",
      },
      "Art. 3(13) CRA: \"'manufacturer' means a natural or legal person who "
      "develops or manufactures products with digital elements or has products "
      "with digital elements designed, developed or manufactured, and markets "
      "them under its name or trademark, whether for payment, monetisation or "
      "free of charge\". Three traps are closed by that single sentence: "
      "outsourcing development does not move the obligation; the trademark, not "
      "the keyboard, decides; and \"free of charge\" is expressly inside the "
      "definition. Establishment in the Union is irrelevant to the definition - "
      "a non-EU manufacturer is still the manufacturer, which is why Arts. 18 "
      "and 19 add an authorised representative and importer layer, and why "
      "Art. 14(7) provides a reporting-endpoint cascade for manufacturers with "
      "no main establishment in the Union.",
      "Art. 3 Nr. 13 CRA definiert den Hersteller als \"eine natürliche oder "
      "juristische Person, die Produkte mit digitalen Elementen entwickelt oder herstellt "
      "oder die Produkte mit digitalen Elementen konzipieren, entwickeln oder "
      "herstellen lässt und sie unter ihrem Namen oder ihrer Marke vermarktet, "
      "sei es gegen Bezahlung, zur Monetarisierung oder unentgeltlich\". Dieser "
      "eine Satz schließt drei Irrtümer aus: Auslagerung der Entwicklung "
      "verschiebt die Pflicht nicht, es entscheidet die Marke und nicht die "
      "Tastatur, und die Unentgeltlichkeit steht ausdrücklich in der Definition. "
      "Die Niederlassung in der Union spielt für die Definition keine Rolle - "
      "ein Hersteller aus einem Drittstaat bleibt Hersteller. Deshalb ergänzen "
      "Art. 18 und Art. 19 die Ebene des Bevollmächtigten und des Einführers, "
      "und deshalb enthält Art. 14 Abs. 7 eine Rangfolge für Hersteller ohne "
      "Hauptniederlassung in der Union."),

    Q("cra-scope_dates-03", "scope_dates", False,
      "Art. 71(2) Regulation (EU) 2024/2847 (CRA)", 4, True, "a",
      "Your CTO asks for the CRA milestone dates so the roadmap can be planned. "
      "What does Article 71(2) actually say?",
      {
        "a": "The Regulation applies from 11 December 2027; however, Article 14 (reporting obligations of manufacturers) applies from 11 September 2026 and Chapter IV (Articles 35 to 51) applies from 11 June 2026.",
        "b": "The whole Regulation applies from 11 September 2026, with a grace period for conformity assessment until 11 December 2027.",
        "c": "The Regulation applies from 11 December 2027 without exception; the September 2026 date is only an ENISA platform milestone with no legal effect on manufacturers.",
        "d": "The Regulation applies from 11 June 2026, with the SBOM requirement deferred to 11 December 2027.",
      },
      "Ihr CTO fragt nach den CRA-Stichtagen, um die Roadmap zu planen. Was "
      "steht tatsächlich in Artikel 71 Absatz 2?",
      {
        "a": "Die Verordnung gilt ab dem 11. Dezember 2027; Artikel 14 (Meldepflichten der Hersteller) gilt jedoch ab dem 11. September 2026 und Kapitel IV (Artikel 35 bis 51) ab dem 11. Juni 2026.",
        "b": "Die gesamte Verordnung gilt ab dem 11. September 2026, mit einer Übergangsfrist für die Konformitätsbewertung bis zum 11. Dezember 2027.",
        "c": "Die Verordnung gilt ausnahmslos ab dem 11. Dezember 2027; der September-2026-Termin ist nur ein ENISA-Plattformmeilenstein ohne Rechtswirkung für Hersteller.",
        "d": "Die Verordnung gilt ab dem 11. Juni 2026, wobei die Anforderung zur Software-Stückliste bis zum 11. Dezember 2027 aufgeschoben ist.",
      },
      "Art. 71(2) CRA, verbatim: \"This Regulation shall apply from 11 December "
      "2027. However, Article 14 shall apply from 11 September 2026 and Chapter "
      "IV (Articles 35 to 51) shall apply from 11 June 2026.\" Three dates, not "
      "two. 11 June 2026 (Chapter IV) is about notification of conformity "
      "assessment bodies and matters little to a product team; 11 September 2026 "
      "is the one that bites first, because from that day the Article 14 "
      "reporting duties are live even though the essential requirements in "
      "Annex I are not yet applicable; 11 December 2027 is when the rest - "
      "Annex I, CE marking, technical documentation, conformity assessment - "
      "starts to apply. Practical consequence: a manufacturer can be legally "
      "obliged to notify an actively exploited vulnerability in a product that "
      "is not yet required to meet a single essential cybersecurity requirement.",
      "Art. 71 Abs. 2 CRA im Wortlaut: \"Diese Verordnung gilt ab dem 11. "
      "Dezember 2027. Artikel 14 gilt jedoch ab dem 11. September 2026, und "
      "Kapitel IV (Artikel 35 bis 51) gilt ab dem 11. Juni 2026.\" Es sind drei "
      "Termine, nicht zwei. Der 11. Juni 2026 (Kapitel IV) betrifft die "
      "Notifizierung von Konformitätsbewertungsstellen und ist für ein "
      "Produktteam kaum relevant; der 11. September 2026 greift zuerst, weil ab "
      "diesem Tag die Meldepflichten des Art. 14 gelten, obwohl die "
      "grundlegenden Anforderungen des Anhangs I noch nicht anwendbar sind; ab "
      "dem 11. Dezember 2027 gilt der Rest - Anhang I, CE-Kennzeichnung, "
      "technische Dokumentation, Konformitätsbewertung. Praktische Folge: Ein "
      "Hersteller kann rechtlich verpflichtet sein, eine aktiv ausgenutzte "
      "Schwachstelle in einem Produkt zu melden, das noch keine einzige "
      "grundlegende Cybersicherheitsanforderung erfüllen muss."),

    Q("cra-scope_dates-04", "scope_dates", False,
      "Art. 69(2), (3) Regulation (EU) 2024/2847 (CRA)", 4, True, "d",
      "A product you placed on the EU market in 2025 is still supported but will "
      "receive no substantial modification after 11 December 2027. In January "
      "2028 you learn that a vulnerability in it is being actively exploited. "
      "What is your legal position?",
      {
        "a": "Nothing applies. Products placed on the market before 11 December 2027 are entirely outside the CRA unless substantially modified.",
        "b": "Everything applies. From 11 December 2027 the CRA applies to the full installed base regardless of when a product was placed on the market.",
        "c": "Nothing applies, because the reporting duty is switched off once a product has left the support period.",
        "d": "The Annex I requirements and CE/conformity duties do not apply to that legacy product absent a substantial modification - but the Article 14 reporting obligations do apply to it, by express derogation.",
      },
      "Ein Produkt, das Sie 2025 auf dem EU-Markt in Verkehr gebracht haben, wird "
      "weiter unterstützt, erfährt aber nach dem 11. Dezember 2027 keine "
      "wesentliche Änderung. Im Januar 2028 erfahren Sie, dass eine Schwachstelle "
      "darin aktiv ausgenutzt wird. Wie ist die Rechtslage?",
      {
        "a": "Nichts gilt. Vor dem 11. Dezember 2027 in Verkehr gebrachte Produkte stehen vollständig außerhalb der CRA, sofern sie nicht wesentlich geändert werden.",
        "b": "Alles gilt. Ab dem 11. Dezember 2027 erfasst die CRA den gesamten Bestand, unabhängig vom Zeitpunkt des Inverkehrbringens.",
        "c": "Nichts gilt, weil die Meldepflicht mit Ablauf des Unterstützungszeitraums entfällt.",
        "d": "Die Anforderungen des Anhangs I sowie die CE- und Konformitätspflichten gelten für dieses Bestandsprodukt ohne wesentliche Änderung nicht - die Meldepflichten des Artikels 14 gelten dafür aber kraft ausdrücklicher Abweichung sehr wohl.",
      },
      "Art. 69(2) CRA: \"Products with digital elements that have been placed on "
      "the market before 11 December 2027 shall be subject to the requirements "
      "set out in this Regulation only if, from that date, those products are "
      "subject to a substantial modification.\" Art. 69(3): \"By way of "
      "derogation from paragraph 2 of this Article, the obligations laid down in "
      "Article 14 shall apply to all products with digital elements that fall "
      "within the scope of this Regulation that have been placed on the market "
      "before 11 December 2027.\" So legacy products are grandfathered for "
      "everything except reporting. This is the single most commercially "
      "significant transitional rule for an established vendor: the installed "
      "base does not have to be re-engineered, but it does have to be watched, "
      "and an actively exploited vulnerability anywhere in it triggers the "
      "24-hour clock. The support period is irrelevant to Art. 69(3), which "
      "refers to products \"that fall within the scope of this Regulation\" "
      "without any support-period qualifier.",
      "Art. 69 Abs. 2 CRA: \"Produkte mit digitalen Elementen, die vor dem 11. "
      "Dezember 2027 in den Verkehr gebracht wurden, unterliegen den in dieser "
      "Verordnung festgelegten Anforderungen nur dann, wenn nach diesem "
      "Zeitpunkt diese Produkte einer wesentlichen Änderung unterliegen.\" "
      "Art. 69 Abs. 3: \"Abweichend von Absatz 2 des vorliegenden Artikels "
      "gelten die in Artikel 14 festgelegten Pflichten für alle Produkte mit "
      "digitalen Elementen, die in den Anwendungsbereich dieser Verordnung "
      "fallen und vor dem 11. Dezember 2027 in den Verkehr gebracht wurden.\" "
      "Bestandsprodukte genießen also Bestandsschutz für alles außer der "
      "Meldung. Das ist für einen etablierten Anbieter die wirtschaftlich "
      "wichtigste Übergangsregel: Der Bestand muss nicht neu entwickelt, aber "
      "beobachtet werden, und jede aktiv ausgenutzte Schwachstelle darin löst "
      "die 24-Stunden-Frist aus. Auf den Unterstützungszeitraum kommt es bei "
      "Art. 69 Abs. 3 nicht an; die Vorschrift stellt allein auf den "
      "Anwendungsbereich ab."),

    Q("cra-scope_dates-05", "scope_dates", False,
      "Art. 3(40), (41), (42) Regulation (EU) 2024/2847 (CRA)", 3, False, "a",
      "Which of these facts, on its own, makes a vulnerability an \"actively "
      "exploited vulnerability\" and therefore notifiable under Article 14(1)?",
      {
        "a": "There is reliable evidence that a malicious actor has exploited it in a system without the permission of the system owner.",
        "b": "A working proof-of-concept exploit has been published on a public repository.",
        "c": "It has a CVSS base score of 9.0 or higher.",
        "d": "A commercial scanner has flagged it as exploitable in your dependency tree.",
      },
      "Welche dieser Tatsachen macht eine Schwachstelle für sich genommen zu "
      "einer \"aktiv ausgenutzten Schwachstelle\" und damit nach Artikel 14 "
      "Absatz 1 meldepflichtig?",
      {
        "a": "Es liegen verlässliche Nachweise dafür vor, dass ein böswilliger Akteur sie in einem System ohne Zustimmung des Systemeigners ausgenutzt hat.",
        "b": "Ein funktionsfähiger Proof-of-Concept-Exploit wurde in einem öffentlichen Repository veröffentlicht.",
        "c": "Sie hat einen CVSS-Basiswert von 9,0 oder höher.",
        "d": "Ein kommerzieller Scanner hat sie in Ihrem Abhängigkeitsbaum als ausnutzbar markiert.",
      },
      "The CRA uses a three-step ladder and only the top step triggers Art. 14. "
      "Art. 3(40): a \"vulnerability\" is \"a weakness, susceptibility or flaw "
      "of a product with digital elements that can be exploited by a cyber "
      "threat\". Art. 3(41): an \"exploitable vulnerability\" is \"a "
      "vulnerability that has the potential to be effectively used by an "
      "adversary under practical operational conditions\". Art. 3(42): an "
      "\"actively exploited vulnerability\" is \"a vulnerability for which there "
      "is reliable evidence that a malicious actor has exploited it in a system "
      "without permission of the system owner\". A published PoC, a high CVSS "
      "score and a scanner finding all speak to exploitability, not to actual "
      "exploitation, and none of them appears anywhere in the CRA text. Note "
      "that \"a system\" is not \"your customer's system\" - evidence of "
      "exploitation anywhere is enough. Ordinary (non-actively-exploited) "
      "vulnerabilities are not notifiable under Art. 14 at all; they are handled "
      "under Annex I Part II and may be reported voluntarily under Art. 15.",
      "Die CRA arbeitet mit einer dreistufigen Leiter, und nur die oberste Stufe "
      "löst Art. 14 aus. Art. 3 Nr. 40: \"Schwachstelle\" ist \"eine Schwäche, "
      "Anfälligkeit oder Fehlfunktion eines Produkts mit digitalen Elementen, "
      "die bei einer Cyberbedrohung ausgenutzt werden kann\". Art. 3 Nr. 41: "
      "\"ausnutzbare Schwachstelle\" ist \"eine Schwachstelle, die von einem "
      "unbefugten Dritten unter praktischen Betriebsbedingungen wirksam genutzt "
      "werden kann\". Art. 3 Nr. 42: \"aktiv ausgenutzte Schwachstelle\" ist "
      "\"eine Schwachstelle, zu der verlässliche Nachweise dafür vorliegen, dass "
      "ein böswilliger Akteur sie in einem System ohne Zustimmung des "
      "Systemeigners ausgenutzt hat\". Veröffentlichter PoC, hoher CVSS-Wert und "
      "Scannerbefund betreffen die Ausnutzbarkeit, nicht die tatsächliche "
      "Ausnutzung, und keines dieser Kriterien kommt im CRA-Text vor. \"Ein "
      "System\" heißt nicht \"das System Ihres Kunden\" - Nachweise über eine "
      "Ausnutzung irgendwo genügen. Gewöhnliche, nicht aktiv ausgenutzte "
      "Schwachstellen sind nach Art. 14 gar nicht meldepflichtig; sie werden "
      "nach Anhang I Teil II behandelt und können nach Art. 15 freiwillig "
      "gemeldet werden."),

    # ---------------------------------------------------------------- topic B
    Q("cra-manufacturer_duties-01", "manufacturer_duties", True,
      "Art. 13(5) Regulation (EU) 2024/2847 (CRA)", 4, False, "b",
      "Your build pulls in an unmaintained MIT-licensed npm package that nobody "
      "sells and nobody supports. Under the CRA, whose problem is its security?",
      {
        "a": "The upstream project's. The CRA places obligations on whoever publishes a component, not on whoever consumes it.",
        "b": "Yours. Manufacturers must exercise due diligence when integrating components sourced from third parties so that those components do not compromise the product's cybersecurity - expressly including free and open-source software components that have not been made available on the market in the course of a commercial activity.",
        "c": "Nobody's, until the package is placed on the EU market commercially; unpaid open source is carved out of the CRA in its entirety.",
        "d": "Yours, but only if the component itself carries CE marking; uncertified components must simply be removed.",
      },
      "Ihr Build zieht ein nicht mehr gepflegtes, MIT-lizenziertes npm-Paket "
      "herein, das niemand verkauft und niemand betreut. Wessen Problem ist "
      "dessen Sicherheit nach der CRA?",
      {
        "a": "Das des Upstream-Projekts. Die CRA verpflichtet denjenigen, der eine Komponente veröffentlicht, nicht denjenigen, der sie verwendet.",
        "b": "Ihres. Hersteller müssen die gebotene Sorgfalt walten lassen, wenn sie von Dritten bezogene Komponenten integrieren, damit diese die Cybersicherheit des Produkts nicht beeinträchtigen - ausdrücklich auch bei freier und quelloffener Software, die nicht im Rahmen einer Geschäftstätigkeit auf dem Markt bereitgestellt wurde.",
        "c": "Niemandes, solange das Paket nicht gewerblich auf dem EU-Markt bereitgestellt wird; unentgeltliche quelloffene Software ist vollständig aus der CRA ausgenommen.",
        "d": "Ihres, aber nur wenn die Komponente selbst CE-gekennzeichnet ist; nicht zertifizierte Komponenten sind schlicht zu entfernen.",
      },
      "Art. 13(5) CRA: \"For the purpose of complying with paragraph 1, "
      "manufacturers shall exercise due diligence when integrating components "
      "sourced from third parties so that those components do not compromise the "
      "cybersecurity of the product with digital elements, including when "
      "integrating components of free and open-source software that have not "
      "been made available on the market in the course of a commercial "
      "activity.\" That closing clause is deliberate: the CRA does not regulate "
      "the hobbyist maintainer, it regulates you for shipping their code. The "
      "separate, lighter regime for \"open-source software stewards\" in "
      "Art. 24 applies to legal persons that systematically support development "
      "of FOSS intended for commercial activities - it does not shift your "
      "Art. 13(5) duty. Art. 25 empowers the Commission to establish voluntary "
      "security attestation programmes precisely to make this due-diligence duty "
      "workable; those are voluntary and, as at 2026-08-16, not adopted.",
      "Art. 13 Abs. 5 CRA: \"Für die Zwecke der Erfüllung der in Absatz 1 "
      "festgelegten Pflicht lassen die Hersteller die gebotene Sorgfalt walten, "
      "wenn sie von Dritten bezogene Komponenten in ihre Produkte mit digitalen "
      "Elementen integrieren, sodass solche Komponenten die Cybersicherheit des "
      "Produkts mit digitalen Elementen nicht beeinträchtigen, auch nicht bei "
      "der Integration von freier und quelloffener Software, die nicht im Rahmen "
      "einer Geschäftstätigkeit auf dem Markt bereitgestellt wurde.\" Der letzte "
      "Halbsatz ist bewusst gesetzt: Die CRA reguliert nicht den privaten "
      "Maintainer, sondern Sie, weil Sie dessen Code ausliefern. Das gesonderte, "
      "leichtere Regime für \"Verwalter quelloffener Software\" in Art. 24 gilt "
      "für juristische Personen, die die Entwicklung quelloffener, für "
      "Geschäftstätigkeiten bestimmter Produkte systematisch unterstützen - es "
      "verschiebt Ihre Pflicht aus Art. 13 Abs. 5 nicht. Art. 25 ermächtigt die "
      "Kommission, freiwillige Sicherheitsattestierungsprogramme einzuführen, "
      "gerade um diese Sorgfaltspflicht praktikabel zu machen; sie sind "
      "freiwillig und zum 16.08.2026 nicht erlassen."),

    Q("cra-manufacturer_duties-02", "manufacturer_duties", False,
      "Art. 13(6) Regulation (EU) 2024/2847 (CRA)", 4, True, "c",
      "You find a vulnerability in an open-source library embedded in your "
      "product. It is not known to be exploited anywhere. What does Article "
      "13(6) require you to do?",
      {
        "a": "Patch or replace the library in your own product and say nothing further; the upstream project is not your counterparty.",
        "b": "Notify the market surveillance authority of your Member State before shipping the fix.",
        "c": "Report the vulnerability to the person or entity manufacturing or maintaining the component, and address and remediate it in accordance with Annex I Part II - and, if you developed a software or hardware modification to fix it, share the relevant code or documentation with that person or entity, where appropriate in a machine-readable format.",
        "d": "Submit an early warning to the CSIRT designated as coordinator and to ENISA within 24 hours.",
      },
      "Sie finden eine Schwachstelle in einer quelloffenen Bibliothek, die in "
      "Ihrem Produkt eingebettet ist. Eine Ausnutzung ist nirgends bekannt. Was "
      "verlangt Artikel 13 Absatz 6?",
      {
        "a": "Die Bibliothek im eigenen Produkt patchen oder ersetzen und im Übrigen schweigen; das Upstream-Projekt ist kein Vertragspartner.",
        "b": "Vor Auslieferung des Fixes die Marktüberwachungsbehörde des eigenen Mitgliedstaats benachrichtigen.",
        "c": "Die Schwachstelle der Person oder Einrichtung melden, die die Komponente herstellt oder wartet, sie gemäß Anhang I Teil II behandeln und beheben - und, falls Sie eine Software- oder Hardware-Änderung zur Behebung entwickelt haben, den betreffenden Code oder die einschlägigen Unterlagen dieser Person oder Stelle mitteilen, gegebenenfalls in einem maschinenlesbaren Format.",
        "d": "Binnen 24 Stunden eine Frühwarnung an das als Koordinator benannte CSIRT und an die ENISA übermitteln.",
      },
      "Art. 13(6) CRA: \"Manufacturers shall, upon identifying a vulnerability in "
      "a component, including in an open source-component, which is integrated "
      "in the product with digital elements report the vulnerability to the "
      "person or entity manufacturing or maintaining the component, and address "
      "and remediate the vulnerability in accordance with the vulnerability "
      "handling requirements set out in Part II of Annex I. Where manufacturers "
      "have developed a software or hardware modification to address the "
      "vulnerability in that component, they shall share the relevant code or "
      "documentation with the person or entity manufacturing or maintaining the "
      "component, where appropriate in a machine-readable format.\" This is a "
      "genuine upstream give-back duty and it is easy to miss because it sits in "
      "Art. 13, not in Art. 14. Distractor (d) is the important one: Art. 14 "
      "reporting is triggered only by an *actively exploited* vulnerability "
      "(Art. 3(42)) or a *severe* incident, so a merely-known vulnerability "
      "creates an upstream duty, not a CSIRT/ENISA notification. Note also that "
      "the code-sharing limb is qualified by \"where appropriate\" as to format, "
      "not as to whether to share.",
      "Art. 13 Abs. 6 CRA: \"Sobald der Hersteller eine Schwachstelle in einer in "
      "das Produkt mit digitalen Elementen integrierten Komponente, "
      "einschließlich einer quelloffenen Komponente, feststellt, meldet er die "
      "Schwachstelle der Person oder Einrichtung, die diese Komponente herstellt "
      "oder wartet, und behandelt und behebt die Schwachstelle gemäß den in "
      "Anhang I Teil II festgelegten Anforderungen an die Behandlung von "
      "Schwachstellen. Haben Hersteller eine Software- oder Hardware-Änderung "
      "entwickelt, um die Schwachstelle in dieser Komponente zu beheben, teilen "
      "sie den betreffenden Code oder die einschlägigen Unterlagen der Person "
      "oder Stelle, die die Komponente herstellt oder wartet, gegebenenfalls in "
      "einem maschinenlesbaren Format mit.\" Das ist eine echte "
      "Rückgabepflicht an das Upstream-Projekt und wird leicht übersehen, weil "
      "sie in Art. 13 und nicht in Art. 14 steht. Wichtig ist Antwort (d): "
      "Art. 14 wird nur durch eine *aktiv ausgenutzte* Schwachstelle "
      "(Art. 3 Nr. 42) oder einen *schwerwiegenden* Sicherheitsvorfall "
      "ausgelöst; eine lediglich bekannte Schwachstelle begründet eine "
      "Upstream-Pflicht, keine Meldung an CSIRT und ENISA. Das \"gegebenenfalls\" "
      "bezieht sich auf das Format, nicht auf das Ob der Mitteilung."),

    Q("cra-manufacturer_duties-03", "manufacturer_duties", False,
      "Art. 13(8), (9) Regulation (EU) 2024/2847 (CRA)", 4, False, "d",
      "How long must a manufacturer handle vulnerabilities, and how long must "
      "security updates stay available?",
      {
        "a": "Both are fixed at five years from placing on the market.",
        "b": "Both are fixed at ten years from placing on the market.",
        "c": "The market surveillance authority sets the support period per product category; the manufacturer has no discretion.",
        "d": "The manufacturer determines the support period to reflect how long the product is expected to be in use; it must be at least five years, unless the product is expected to be in use for less, in which case it equals the expected use time. Separately, each security update made available during the support period must remain available for at least 10 years after it was issued, or for the remainder of the support period, whichever is longer.",
      },
      "Wie lange muss ein Hersteller Schwachstellen behandeln, und wie lange "
      "müssen Sicherheitsaktualisierungen verfügbar bleiben?",
      {
        "a": "Beides ist auf fünf Jahre ab Inverkehrbringen festgelegt.",
        "b": "Beides ist auf zehn Jahre ab Inverkehrbringen festgelegt.",
        "c": "Die Marktüberwachungsbehörde legt den Unterstützungszeitraum je Produktkategorie fest; der Hersteller hat keinen Spielraum.",
        "d": "Der Hersteller legt den Unterstützungszeitraum so fest, dass er die Dauer der voraussichtlichen Nutzung widerspiegelt; er beträgt mindestens fünf Jahre, es sei denn, das Produkt ist voraussichtlich kürzer im Betrieb - dann entspricht er der voraussichtlichen Nutzungsdauer. Davon getrennt muss jede während des Unterstützungszeitraums bereitgestellte Sicherheitsaktualisierung nach ihrer Bereitstellung mindestens zehn Jahre oder für die verbleibende Dauer des Unterstützungszeitraums verfügbar bleiben, je nachdem, welcher Zeitraum länger ist.",
      },
      "Two different periods, routinely conflated. Art. 13(8) CRA: manufacturers "
      "must ensure vulnerabilities are handled effectively \"when placing a "
      "product with digital elements on the market, and for the support period\"; "
      "they \"shall determine the support period so that it reflects the length "
      "of time during which the product is expected to be in use\", and "
      "\"[w]ithout prejudice to the second subparagraph, the support period shall "
      "be at least five years. Where the product with digital elements is "
      "expected to be in use for less than five years, the support period shall "
      "correspond to the expected use time.\" Art. 13(19) requires the end date "
      "of the support period (at least month and year) to be stated clearly at "
      "the time of purchase. Art. 13(9) is the separate archival duty: \"each "
      "security update ... which has been made available to users during the "
      "support period, remains available after it has been issued for a minimum "
      "of 10 years or for the remainder of the support period, whichever is "
      "longer.\" The five years is a floor set by the manufacturer's own "
      "assessment, not a ceiling and not a default; the Commission may under "
      "Art. 13(8) fifth subparagraph specify minimum support periods for "
      "specific categories by delegated act.",
      "Zwei verschiedene Zeiträume, die regelmäßig verwechselt werden. Art. 13 "
      "Abs. 8 CRA: Hersteller müssen die wirksame Behandlung von Schwachstellen "
      "sicherstellen, \"wenn sie ein Produkt mit digitalen Elementen in den "
      "Verkehr bringen und während des Unterstützungszeitraums\"; sie \"legen "
      "den Unterstützungszeitraum so fest, dass er die Dauer der "
      "voraussichtlichen Nutzung des Produkts widerspiegelt\", und "
      "\"[u]nbeschadet Unterabsatz 2 beträgt der Unterstützungszeitraum "
      "mindestens fünf Jahre. Wird davon ausgegangen, dass das Produkt mit "
      "digitalen Elementen weniger als fünf Jahre im Betrieb ist, muss der "
      "Unterstützungszeitraum der voraussichtlichen Nutzungsdauer entsprechen.\" "
      "Nach Art. 13 Abs. 19 ist das Enddatum des Unterstützungszeitraums "
      "(mindestens Monat und Jahr) beim Kauf klar anzugeben. Art. 13 Abs. 9 "
      "regelt getrennt die Archivpflicht: Jede den Nutzern während des "
      "Unterstützungszeitraums bereitgestellte Sicherheitsaktualisierung bleibt "
      "\"nach ihrer Bereitstellung für mindestens zehn Jahre oder für die "
      "verbleibende Dauer des Unterstützungszeitraums, je nachdem, welcher "
      "Zeitraum länger ist, verfügbar\". Die fünf Jahre sind eine vom Hersteller "
      "selbst zu bestimmende Untergrenze, keine Obergrenze und kein "
      "Regelwert; die Kommission kann nach Art. 13 Abs. 8 Unterabs. 5 durch "
      "delegierten Rechtsakt Mindestunterstützungszeiträume für bestimmte "
      "Kategorien festlegen. "
      "Hinweis: Die ursprüngliche deutsche Amtsblattfassung des Art. 13 Abs. 8 "
      "enthielt zusätzlich die Wendung \"der erwarteten Produktlebensdauer und\"; "
      "diese wurde durch Berichtigung (ABl. L, 2025/90555 vom 2.7.2025) "
      "gestrichen. Maßgeblich ist der berichtigte Wortlaut."),

    Q("cra-manufacturer_duties-04", "manufacturer_duties", False,
      "Art. 13(2), (3), (4), Annex VII Regulation (EU) 2024/2847 (CRA)", 3, False, "a",
      "What is the status of the cybersecurity risk assessment under the CRA?",
      {
        "a": "It must be documented and updated as appropriate during the support period, must be included in the technical documentation when the product is placed on the market, and where certain essential cybersecurity requirements are not applicable the manufacturer must include a clear justification to that effect in that technical documentation.",
        "b": "It is a one-off exercise completed before first release; later changes are covered by the substantial-modification rules instead.",
        "c": "It is required only for important products with digital elements listed in Annex III.",
        "d": "It must be published together with the EU declaration of conformity so that users can verify it.",
      },
      "Welchen Status hat die Bewertung der Cybersicherheitsrisiken nach der CRA?",
      {
        "a": "Sie ist zu dokumentieren und während des Unterstützungszeitraums gegebenenfalls zu aktualisieren, beim Inverkehrbringen in die technische Dokumentation aufzunehmen; sind bestimmte grundlegende Cybersicherheitsanforderungen nicht anwendbar, muss der Hersteller eine klare Begründung dafür in diese technische Dokumentation aufnehmen.",
        "b": "Sie ist eine einmalige Übung vor der Erstveröffentlichung; spätere Änderungen werden stattdessen über die Regeln zur wesentlichen Änderung erfasst.",
        "c": "Sie ist nur für wichtige Produkte mit digitalen Elementen nach Anhang III erforderlich.",
        "d": "Sie ist zusammen mit der EU-Konformitätserklärung zu veröffentlichen, damit Nutzer sie überprüfen können.",
      },
      "Art. 13(2) CRA requires the assessment and requires its outcome to be "
      "taken into account \"during the planning, design, development, "
      "production, delivery and maintenance phases\". Art. 13(3): \"The "
      "cybersecurity risk assessment shall be documented and updated as "
      "appropriate during a support period to be determined in accordance with "
      "paragraph 8 of this Article.\" It must indicate whether and how the "
      "Annex I Part I point (2) requirements apply and how the manufacturer "
      "applies Annex I Part I point (1) and the Part II vulnerability handling "
      "requirements. Art. 13(4): the assessment goes into the technical "
      "documentation required under Art. 31 and Annex VII, and \"[w]here certain "
      "essential cybersecurity requirements are not applicable to the product "
      "with digital elements, the manufacturer shall include a clear "
      "justification to that effect in that technical documentation.\" That "
      "justification requirement is the operative discipline behind the phrase "
      "\"where applicable\" in Annex I Part I point (2): you may disapply a "
      "requirement, but you must write down why. The technical documentation is "
      "kept at the disposal of market surveillance authorities for at least 10 "
      "years or the support period, whichever is longer (Art. 13(13)); it is not "
      "a published document.",
      "Art. 13 Abs. 2 CRA verlangt die Bewertung und deren Berücksichtigung \"in "
      "der Planungs-, Konzeptions-, Entwicklungs-, Herstellungs-, Liefer- und "
      "Wartungsphase des Produkts mit digitalen Elementen\". Art. 13 Abs. 3: \"Die Bewertung des "
      "Cybersicherheitsrisikos wird während eines gemäß Absatz 8 festzulegenden "
      "Unterstützungszeitraums dokumentiert und gegebenenfalls aktualisiert.\" "
      "Sie muss angeben, ob und wie die Anforderungen des Anhangs I Teil I "
      "Nummer 2 anwendbar sind und wie der Hersteller Anhang I Teil I Nummer 1 "
      "sowie die Anforderungen des Teils II an die Behandlung von Schwachstellen "
      "anwendet. Art. 13 Abs. 4: Die Bewertung ist in die nach Art. 31 und "
      "Anhang VII vorgeschriebene technische Dokumentation aufzunehmen; \"[s]ind "
      "bestimmte grundlegende Cybersicherheitsanforderungen nicht auf das "
      "Produkt mit digitalen Elementen anwendbar, so nimmt der Hersteller eine "
      "klare Begründung hierfür in diese technische Dokumentation auf.\" Diese "
      "Begründungspflicht ist die eigentliche Disziplin hinter dem "
      "\"gegebenenfalls\" in Anhang I Teil I Nummer 2: Man darf eine Anforderung "
      "abwählen, muss aber aufschreiben, warum. Die technische Dokumentation ist "
      "den Marktüberwachungsbehörden mindestens zehn Jahre oder für die Dauer "
      "des Unterstützungszeitraums bereitzuhalten, je nachdem, welcher Zeitraum "
      "länger ist (Art. 13 Abs. 13); sie ist kein Veröffentlichungsdokument."),

    Q("cra-manufacturer_duties-05", "manufacturer_duties", False,
      "Art. 64(2), (10) Regulation (EU) 2024/2847 (CRA)", 4, True, "a",
      "What is the maximum administrative fine for breaching the Annex I "
      "essential requirements or the Article 13 or 14 obligations, and is there "
      "any relief for small manufacturers?",
      {
        "a": "Up to EUR 15 000 000 or, if the offender is an undertaking, up to 2,5 % of its total worldwide annual turnover for the preceding financial year, whichever is higher - and manufacturers qualifying as microenterprises or small enterprises are exempted from those fines specifically for failing to meet the 24-hour early-warning deadline in Article 14(2)(a) or 14(4)(a).",
        "b": "Up to EUR 10 000 000 or 2 % of total worldwide annual turnover, whichever is higher, with no size-based relief of any kind.",
        "c": "Up to EUR 20 000 000 or 4 % of total worldwide annual turnover, mirroring the GDPR.",
        "d": "The CRA fixes no EU-level ceiling at all; the amount is left entirely to national law.",
      },
      "Wie hoch ist die höchstmögliche Geldbuße bei Verstößen gegen die "
      "grundlegenden Anforderungen des Anhangs I oder gegen die Pflichten der "
      "Artikel 13 und 14, und gibt es Erleichterungen für kleine Hersteller?",
      {
        "a": "Bis zu 15 000 000 EUR oder - im Falle von Unternehmen - bis zu 2,5 % des gesamten weltweiten Jahresumsatzes des vorangegangenen Geschäftsjahres, je nachdem, welcher Betrag höher ist. Hersteller, die als Kleinst- oder Kleinunternehmen gelten, sind von diesen Geldbußen ausgenommen, soweit es um die Nichteinhaltung der 24-Stunden-Frist für die Frühwarnung nach Art. 14 Abs. 2 Buchst. a oder Art. 14 Abs. 4 Buchst. a geht.",
        "b": "Bis zu 10 000 000 EUR oder 2 % des gesamten weltweiten Jahresumsatzes, je nachdem, welcher Betrag höher ist, ohne jede größenabhängige Erleichterung.",
        "c": "Bis zu 20 000 000 EUR oder 4 % des gesamten weltweiten Jahresumsatzes, entsprechend der DSGVO.",
        "d": "Die CRA setzt überhaupt keine unionsrechtliche Obergrenze; die Höhe bleibt vollständig dem nationalen Recht überlassen.",
      },
      "Art. 64(2) CRA: \"Non-compliance with the essential cybersecurity "
      "requirements set out in Annex I and the obligations set out in Articles "
      "13 and 14 shall be subject to administrative fines of up to EUR 15 000 "
      "000 or, if the offender is an undertaking, up to 2,5 % of the its total "
      "worldwide annual turnover for the preceding financial year, whichever is "
      "higher.\" (The stray \"the\" is in the OJ text.) A lower tier of EUR 10 "
      "000 000 / 2 % applies to the Art. 18-23 economic-operator duties and "
      "others under Art. 64(3); supplying incorrect, incomplete or misleading "
      "information to notified bodies or market surveillance authorities carries "
      "EUR 5 000 000 / 1 % under Art. 64(4). Art. 64(10) then carves out, \"[b]y "
      "way of derogation from paragraphs 2 to 9\", (a) micro and small "
      "manufacturers as regards \"any failure to meet the deadline referred to "
      "in Article 14(2), point (a), or Article 14(4), point (a)\" and (b) any "
      "infringement by open-source software stewards. IMPORTANT: the original OJ "
      "text of Art. 64(10) read \"paragraphs 3 to 9\", which would have left the "
      "carve-out inoperative for Art. 14 breaches (those sit in paragraph 2). "
      "This was corrected to \"paragraphs 2 to 9\" by corrigendum. The corrected "
      "text is the operative one, and the exemption is narrow: it covers the "
      "24-hour early-warning deadline only, not the 72-hour notification, not "
      "the final report, and not the substance of the duty.",
      "Art. 64 Abs. 2 CRA: \"Bei Nichteinhaltung der in Anhang I festgelegten "
      "grundlegenden Cybersicherheitsanforderungen oder Verstößen gegen die in "
      "den Artikeln 13 und 14 festgelegten Pflichten werden Geldbußen von bis zu "
      "15 000 000 EUR oder - im Falle von Unternehmen - von bis zu 2,5 % des "
      "gesamten weltweiten Jahresumsatzes des vorangegangenen Geschäftsjahres "
      "verhängt, je nachdem, welcher Betrag höher ist.\" Eine niedrigere Stufe "
      "von 10 000 000 EUR bzw. 2 % gilt nach Art. 64 Abs. 3 u. a. für die "
      "Pflichten der Wirtschaftsakteure nach Art. 18 bis 23; falsche, "
      "unvollständige oder irreführende Auskünfte gegenüber notifizierten "
      "Stellen und Marktüberwachungsbehörden werden nach Art. 64 Abs. 4 mit bis "
      "zu 5 000 000 EUR bzw. 1 % geahndet. Art. 64 Abs. 10 nimmt sodann "
      "\"[a]bweichend von den Absätzen 2 bis 9\" aus: a) Kleinst- und "
      "Kleinunternehmen \"in Bezug auf die Nichteinhaltung der in Artikel 14 "
      "Absatz 2 Buchstabe a oder Artikel 14 Absatz 4 Buchstabe a genannten "
      "Frist\" und b) Verwalter quelloffener Software bei jedem Verstoß. "
      "WICHTIG: Die ursprüngliche Amtsblattfassung lautete \"Absätzen 3 bis 9\", "
      "was die Ausnahme für Art.-14-Verstöße leerlaufen ließe, weil diese in "
      "Absatz 2 stehen. Dies wurde durch Berichtigung zu \"Absätzen 2 bis 9\" "
      "korrigiert. Maßgeblich ist die berichtigte Fassung, und die Ausnahme ist "
      "eng: Sie betrifft nur die 24-Stunden-Frist der Frühwarnung, nicht die "
      "72-Stunden-Meldung, nicht den Abschlussbericht und nicht die Pflicht "
      "selbst."),

    # ---------------------------------------------------------------- topic C
    Q("cra-sbom_vulnerability-01", "sbom_vulnerability", True,
      "Annex I Part II point (1), Art. 13(24), Art. 3(39) Regulation (EU) 2024/2847 (CRA)",
      4, True, "d",
      "Your tooling vendor tells you that \"the CRA requires CycloneDX\". Your "
      "auditor tells you it requires SPDX because SPDX is an ISO standard. What "
      "does the CRA actually require?",
      {
        "a": "CycloneDX, because it is the OWASP standard and is published as ECMA-424.",
        "b": "SPDX, because SPDX 2.2.1 is standardised as ISO/IEC 5962:2021.",
        "c": "Either CycloneDX or SPDX, but in both cases the complete transitive dependency tree.",
        "d": "Neither by name. Annex I Part II point (1) requires manufacturers to identify and document vulnerabilities and components \"including by drawing up a software bill of materials in a commonly used and machine-readable format covering at the very least the top-level dependencies of the products\". No format is named; the Commission may - not must - specify the format and elements by implementing act under Article 13(24).",
      },
      "Ihr Werkzeuganbieter sagt, \"die CRA verlangt CycloneDX\". Ihr Prüfer "
      "sagt, sie verlange SPDX, weil SPDX eine ISO-Norm sei. Was verlangt die "
      "CRA tatsächlich?",
      {
        "a": "CycloneDX, weil es der OWASP-Standard ist und als ECMA-424 veröffentlicht wurde.",
        "b": "SPDX, weil SPDX 2.2.1 als ISO/IEC 5962:2021 normiert ist.",
        "c": "Entweder CycloneDX oder SPDX, in beiden Fällen aber den vollständigen transitiven Abhängigkeitsbaum.",
        "d": "Keines von beiden namentlich. Anhang I Teil II Nummer 1 verlangt, Schwachstellen und Komponenten zu ermitteln und zu dokumentieren, \"u. a. durch Erstellung einer Software-Stückliste in einem gängigen maschinenlesbaren Format, aus der zumindest die obersten Abhängigkeiten der Produkte hervorgehen\". Kein Format wird genannt; die Kommission kann - nicht muss - Format und Elemente nach Art. 13 Abs. 24 durch Durchführungsrechtsakt festlegen.",
      },
      "This is the single most-repeated error in CRA vendor material. The CRA "
      "specifies three things about the SBOM and nothing else: it must be in a "
      "\"commonly used\" format, it must be \"machine-readable\", and it must "
      "cover \"at the very least the top-level dependencies\" (Annex I Part II "
      "point (1)). Art. 3(39) defines an SBOM as \"a formal record containing "
      "details and supply chain relationships of components included in the "
      "software elements of a product with digital elements\". Art. 13(24): "
      "\"The Commission MAY, by means of implementing acts taking into account "
      "European or international standards and best practices, specify the "
      "format and elements of the software bill of materials referred to in Part "
      "II, point (1), of Annex I.\" - a discretionary power that, as at "
      "2026-08-16, has not been exercised. What follows for a DevSecOps team: "
      "(i) CycloneDX (OWASP; published by Ecma International as ECMA-424) and "
      "SPDX (Linux Foundation; SPDX 2.2.1 standardised as ISO/IEC 5962:2021, "
      "SPDX 3.0 released April 2024) are both plausible ways to satisfy "
      "\"commonly used and machine-readable\", but that is a factual "
      "characterisation, not a legal designation; (ii) top-level dependencies "
      "are the legal floor, and going deeper is good engineering, not a "
      "statutory requirement; (iii) if the Commission does adopt an implementing "
      "act, format choice stops being yours. Build your pipeline so the format "
      "is a swappable output stage.",
      "Das ist der am häufigsten wiederholte Fehler in Anbietermaterial zur CRA. "
      "Die CRA legt zur Software-Stückliste genau drei Dinge fest und sonst "
      "nichts: ein \"gängiges\" Format, \"maschinenlesbar\", und \"zumindest die "
      "obersten Abhängigkeiten\" (Anhang I Teil II Nummer 1). Art. 3 Nr. 39 "
      "definiert die Software-Stückliste als \"eine formale Aufzeichnung der "
      "Einzelheiten und Lieferkettenbeziehungen der Komponenten, die in den "
      "Softwareelementen eines Produkts mit digitalen Elementen enthalten "
      "sind\". Art. 13 Abs. 24: \"Die Kommission KANN im Wege von "
      "Durchführungsrechtsakten unter Berücksichtigung europäischer oder "
      "internationaler Normen und bewährter Verfahren das Format und die "
      "Elemente der Software-Stückliste gemäß Anhang I Teil II Nummer 1 "
      "festlegen.\" - eine Ermessensbefugnis, die zum 16.08.2026 nicht ausgeübt "
      "wurde. Für ein DevSecOps-Team folgt daraus: (i) CycloneDX (OWASP; von "
      "Ecma International als ECMA-424 veröffentlicht) und SPDX (Linux "
      "Foundation; SPDX 2.2.1 als ISO/IEC 5962:2021 normiert, SPDX 3.0 im April "
      "2024 erschienen) sind beide plausible Wege, \"gängig und maschinenlesbar\" "
      "zu erfüllen - das ist eine tatsächliche Einschätzung, keine rechtliche "
      "Festlegung; (ii) die obersten Abhängigkeiten sind die rechtliche "
      "Untergrenze, mehr Tiefe ist gute Technik, keine gesetzliche Pflicht; "
      "(iii) erlässt die Kommission doch einen Durchführungsrechtsakt, ist die "
      "Formatwahl nicht mehr Ihre. Bauen Sie die Pipeline so, dass das Format "
      "eine austauschbare Ausgabestufe ist."),

    Q("cra-sbom_vulnerability-02", "sbom_vulnerability", False,
      "Annex II point 9, Annex VII points 2(b) and 8, Art. 13(25) Regulation (EU) 2024/2847 (CRA)",
      4, False, "c",
      "A large customer demands your full SBOM, citing \"the CRA transparency "
      "requirement\". What does the CRA actually oblige you to do with the SBOM?",
      {
        "a": "Publish it on your website for each product version.",
        "b": "Ship it with every product, in the box or in the download bundle.",
        "c": "Nothing towards the public. The SBOM belongs in the technical documentation; a market surveillance authority can obtain it further to a reasoned request where necessary to check compliance; and Annex II point 9 requires you to tell users where the SBOM can be accessed only \"[i]f the manufacturer decides to make available the software bill of materials to the user\".",
        "d": "Upload it to the ENISA single reporting platform together with each vulnerability notification.",
      },
      "Ein Großkunde verlangt Ihre vollständige Software-Stückliste und beruft "
      "sich auf die \"CRA-Transparenzpflicht\". Wozu verpflichtet die CRA Sie "
      "tatsächlich in Bezug auf die Software-Stückliste?",
      {
        "a": "Zur Veröffentlichung auf Ihrer Website für jede Produktversion.",
        "b": "Zur Beilage zu jedem Produkt, in der Verpackung oder im Download-Paket.",
        "c": "Zu nichts gegenüber der Öffentlichkeit. Die Software-Stückliste gehört in die technische Dokumentation; eine Marktüberwachungsbehörde kann sie auf begründetes Verlangen erhalten, soweit dies zur Prüfung der Einhaltung erforderlich ist; und Anhang II Nummer 9 verlangt die Angabe des Zugriffsorts nur \"für den Fall, dass der Hersteller dem Nutzer die Software-Stückliste zur Verfügung stellt\".",
        "d": "Zum Hochladen auf die einheitliche Meldeplattform der ENISA zusammen mit jeder Schwachstellenmeldung.",
      },
      "Three provisions, read together, dispose of the \"CRA transparency\" "
      "claim. Annex VII point 2(b) puts the SBOM inside the technical "
      "documentation as part of the vulnerability-handling process description. "
      "Annex VII point 8 adds it \"where applicable, ... further to a reasoned "
      "request from a market surveillance authority provided that it is "
      "necessary in order for that authority to be able to check compliance with "
      "the essential cybersecurity requirements set out in Annex I\". Annex II "
      "point 9 - the user-information annex - is expressly conditional: \"If the "
      "manufacturer decides to make available the software bill of materials to "
      "the user, information on where the software bill of materials can be "
      "accessed.\" Art. 13(25) is the only other route out: market surveillance "
      "authorities may request SBOMs for an ADCO Union-wide dependency "
      "assessment, and what reaches ADCO is anonymised and aggregated. Recital "
      "77 states the policy in terms - \"Manufacturers should not be obliged to "
      "make the SBOM public\" - but that is a recital and is cited here only as "
      "corroboration of the enacting text, not as its source. Commercially: "
      "handing an SBOM to a customer is a contract question, not a CRA question, "
      "and you can negotiate it.",
      "Drei Vorschriften erledigen im Zusammenspiel die Behauptung einer "
      "\"CRA-Transparenzpflicht\". Anhang VII Nummer 2 Buchst. b ordnet die "
      "Software-Stückliste als Teil der Beschreibung der Verfahren zur "
      "Behandlung von Schwachstellen in die technische Dokumentation ein. "
      "Anhang VII Nummer 8 nennt sie zusätzlich \"gegebenenfalls auf begründetes "
      "Verlangen der Marktüberwachungsbehörde ..., sofern dies erforderlich ist, "
      "damit diese Behörde die Einhaltung der grundlegenden "
      "Cybersicherheitsanforderungen in Anhang I überprüfen kann\". Anhang II "
      "Nummer 9 - der Anhang zu den Nutzerinformationen - ist ausdrücklich "
      "bedingt formuliert: \"für den Fall, dass der Hersteller dem Nutzer die "
      "Software-Stückliste zur Verfügung stellt, wo auf die Software-Stückliste "
      "zugegriffen werden kann.\" Der einzige weitere Weg ist Art. 13 Abs. 25: "
      "Marktüberwachungsbehörden können Software-Stücklisten für eine "
      "unionsweite Abhängigkeitsbewertung der ADCO anfordern; an die ADCO gehen "
      "nur anonymisierte und aggregierte Informationen. Erwägungsgrund 77 sagt "
      "die Politik ausdrücklich - \"Die Hersteller sollten nicht verpflichtet "
      "sein, die Software-Stückliste zu veröffentlichen\" -, ist aber ein "
      "Erwägungsgrund und wird hier nur als Bestätigung des verfügenden Teils "
      "angeführt, nicht als dessen Quelle. Wirtschaftlich: Die Herausgabe an "
      "einen Kunden ist eine Vertragsfrage, keine CRA-Frage, und verhandelbar."),

    Q("cra-sbom_vulnerability-03", "sbom_vulnerability", False,
      "Annex I Part II points (2), (7), (8) Regulation (EU) 2024/2847 (CRA)", 4, True, "b",
      "Your release process bundles security fixes into the next quarterly "
      "feature release, and security patches are available only to customers on "
      "a paid maintenance plan. Assess this against Annex I Part II.",
      {
        "a": "Compliant. The CRA prescribes no release cadence and leaves commercial terms for updates entirely to the manufacturer.",
        "b": "Non-compliant on both counts. Vulnerabilities must be addressed and remediated \"without delay\", and \"where technically feasible, new security updates shall be provided separately from functionality updates\"; and security updates must be \"disseminated without delay and, unless otherwise agreed between a manufacturer and a business user in relation to a tailor-made product with digital elements, free of charge\", accompanied by advisory messages.",
        "c": "Compliant, provided the quarterly cadence is disclosed in the user information under Annex II.",
        "d": "Non-compliant only for products listed as important in Annex III; for ordinary products the manufacturer may set its own patch policy.",
      },
      "Ihr Release-Prozess bündelt Sicherheitskorrekturen in das nächste "
      "quartalsweise Feature-Release, und Sicherheitspatches erhalten nur Kunden "
      "mit kostenpflichtigem Wartungsvertrag. Bewerten Sie dies anhand von "
      "Anhang I Teil II.",
      {
        "a": "Konform. Die CRA schreibt keinen Release-Takt vor und überlässt die kommerziellen Bedingungen für Aktualisierungen vollständig dem Hersteller.",
        "b": "In beiden Punkten nicht konform. Schwachstellen sind \"unverzüglich\" zu behandeln und zu beheben, und \"soweit technisch machbar, müssen neue Sicherheitsaktualisierungen getrennt von den Funktionsaktualisierungen bereitgestellt werden\"; Sicherheitsaktualisierungen müssen \"unverzüglich und - sofern zwischen dem Hersteller und dem gewerblichen Nutzer in Bezug auf ein maßgeschneidertes Produkt mit digitalen Elementen nichts anderes vereinbart wurde - kostenlos verbreitet werden\", zusammen mit Hinweisen.",
        "c": "Konform, sofern der Quartalstakt in den Nutzerinformationen nach Anhang II offengelegt wird.",
        "d": "Nicht konform nur bei den in Anhang III als wichtig eingestuften Produkten; bei gewöhnlichen Produkten darf der Hersteller seine eigene Patch-Politik festlegen.",
      },
      "Annex I Part II point (2): manufacturers shall \"in relation to the risks "
      "posed to products with digital elements, address and remediate "
      "vulnerabilities without delay, including by providing security updates; "
      "where technically feasible, new security updates shall be provided "
      "separately from functionality updates\". Point (8): manufacturers shall "
      "\"ensure that, where security updates are available to address identified "
      "security issues, they are disseminated without delay and, unless "
      "otherwise agreed between a manufacturer and a business user in relation "
      "to a tailor-made product with digital elements, free of charge, "
      "accompanied by advisory messages providing users with the relevant "
      "information, including on potential action to be taken\". Point (7) adds "
      "the requirement to provide mechanisms for the secure distribution of "
      "updates. The paid-plan model survives only in the narrow tailor-made / "
      "business-user carve-out in point (8) - it is not a general licence to "
      "monetise security patches. Note the related Annex I Part I point (2)(c) "
      "requirement that products ensure vulnerabilities can be addressed through "
      "security updates, where applicable automatically installed by default "
      "with a clear opt-out. These requirements apply to all products with "
      "digital elements; the Annex III importance classification changes the "
      "conformity assessment route, not the substantive requirements.",
      "Anhang I Teil II Nummer 2: Hersteller müssen \"im Hinblick auf die "
      "Risiken im Zusammenhang mit den Produkten mit digitalen Elementen "
      "unverzüglich Schwachstellen behandeln und beheben, unter anderem durch "
      "Bereitstellung von Sicherheitsaktualisierungen; soweit technisch machbar, "
      "müssen neue Sicherheitsaktualisierungen getrennt von den "
      "Funktionsaktualisierungen bereitgestellt werden\". Nummer 8: Hersteller "
      "müssen \"dafür sorgen, dass Sicherheitsaktualisierungen, die zur "
      "Bewältigung festgestellter Sicherheitsprobleme zur Verfügung stehen, "
      "unverzüglich und - sofern zwischen dem Hersteller und dem gewerblichen "
      "Nutzer in Bezug auf ein maßgeschneidertes Produkt mit digitalen Elementen "
      "nichts anderes vereinbart wurde - kostenlos verbreitet werden, zusammen "
      "mit Hinweisen und einschlägigen Informationen, auch über zu treffende "
      "mögliche Maßnahmen\". Nummer 7 verlangt ergänzend Mechanismen für die "
      "sichere Verbreitung von Aktualisierungen. Das Modell des "
      "kostenpflichtigen Wartungsvertrags überlebt nur in der engen Ausnahme für "
      "maßgeschneiderte Produkte gegenüber gewerblichen Nutzern nach Nummer 8 - "
      "es ist keine allgemeine Erlaubnis, Sicherheitspatches zu monetarisieren. "
      "Verwandt ist Anhang I Teil I Nummer 2 Buchst. c: Produkte müssen "
      "sicherstellen, dass Schwachstellen durch Sicherheitsaktualisierungen "
      "behoben werden können, gegebenenfalls standardmäßig automatisch "
      "installiert mit klarer Opt-out-Möglichkeit. Diese Anforderungen gelten "
      "für alle Produkte mit digitalen Elementen; die Einstufung nach Anhang III "
      "ändert den Weg der Konformitätsbewertung, nicht die materiellen "
      "Anforderungen."),

    Q("cra-sbom_vulnerability-04", "sbom_vulnerability", False,
      "Annex I Part II point (4) Regulation (EU) 2024/2847 (CRA)", 3, False, "c",
      "When must a manufacturer publicly disclose information about a "
      "vulnerability it has fixed?",
      {
        "a": "Never. Disclosing fixed vulnerabilities would create risk for users still running old versions, so the CRA prohibits it.",
        "b": "Immediately on discovery, before any patch exists, so that users can take defensive action.",
        "c": "Once a security update has been made available: the manufacturer must share and publicly disclose information about fixed vulnerabilities, including a description, information identifying the affected product, the impacts and severity, and clear information helping users remediate. In duly justified cases, where the manufacturer considers the security risks of publication to outweigh the security benefits, publication may be delayed until users have been given the possibility to apply the relevant patch.",
        "d": "Only to customers under a support contract; public disclosure is a matter for the CSIRT, not the manufacturer.",
      },
      "Wann muss ein Hersteller Informationen über eine von ihm behobene "
      "Schwachstelle veröffentlichen?",
      {
        "a": "Nie. Die Offenlegung behobener Schwachstellen würde Nutzer alter Versionen gefährden, deshalb untersagt die CRA sie.",
        "b": "Sofort bei Entdeckung, noch bevor ein Patch existiert, damit Nutzer Gegenmaßnahmen ergreifen können.",
        "c": "Sobald eine Sicherheitsaktualisierung bereitgestellt worden ist: Der Hersteller muss Informationen über beseitigte Schwachstellen teilen und veröffentlichen, einschließlich einer Beschreibung, Angaben zur Erkennung des betroffenen Produkts, der Auswirkungen und der Schwere sowie eindeutiger Hinweise zur Behebung. In hinreichend begründeten Fällen, in denen die Risiken der Veröffentlichung die Sicherheitsvorteile überwiegen, darf die Veröffentlichung aufgeschoben werden, bis den Nutzern die Möglichkeit gegeben wurde, den Patch anzuwenden.",
        "d": "Nur gegenüber Kunden mit Supportvertrag; die Veröffentlichung ist Sache des CSIRT, nicht des Herstellers.",
      },
      "Annex I Part II point (4) CRA: manufacturers shall \"once a security "
      "update has been made available, share and publicly disclose information "
      "about fixed vulnerabilities, including a description of the "
      "vulnerabilities, information allowing users to identify the product with "
      "digital elements affected, the impacts of the vulnerabilities, their "
      "severity and clear and accessible information helping users to remediate "
      "the vulnerabilities; in duly justified cases, where manufacturers "
      "consider the security risks of publication to outweigh the security "
      "benefits, they may delay making public information regarding a fixed "
      "vulnerability until after users have been given the possibility to apply "
      "the relevant patch\". Two things engineers get wrong here: the trigger is "
      "availability of the update, not discovery (so option (b) is the "
      "coordinated-disclosure failure mode), and the delay is an exception "
      "requiring a documented justification with a defined end point, not an "
      "open-ended right to stay silent. This publication duty is distinct from "
      "the Art. 14 notification duty (to CSIRT and ENISA), from the Art. 14(8) "
      "duty to inform users of an actively exploited vulnerability or severe "
      "incident, and from the Art. 17(5) mechanism by which ENISA, in agreement "
      "with the manufacturer, adds a publicly known notified vulnerability to "
      "the European vulnerability database.",
      "Anhang I Teil II Nummer 4 CRA: Hersteller müssen \"sobald eine "
      "Sicherheitsaktualisierung bereitgestellt worden ist, Informationen über "
      "beseitigte Schwachstellen teilen und veröffentlichen, einschließlich "
      "einer Beschreibung der Schwachstellen mit Angaben, anhand deren die "
      "Nutzer das betroffene Produkt mit digitalen Elementen, die Auswirkungen "
      "der Schwachstellen und ihre Schwere erkennen können, sowie eindeutige und "
      "verständliche Informationen, die den Nutzern helfen, die Schwachstellen "
      "zu beheben; in hinreichend begründeten Fällen, in denen die Hersteller "
      "der Auffassung sind, dass die Risiken der Veröffentlichung die Vorteile "
      "in Bezug auf die Sicherheit überwiegen, können sie die Veröffentlichung "
      "von Informationen über eine behobene Schwachstelle so lange aufschieben, "
      "bis den Nutzern die Möglichkeit gegeben wurde, den entsprechenden Patch "
      "anzuwenden\". Zwei typische Irrtümer: Auslöser ist die Verfügbarkeit der "
      "Aktualisierung, nicht die Entdeckung (Antwort b ist der klassische "
      "Fehlgriff bei koordinierter Offenlegung), und der Aufschub ist eine "
      "begründungsbedürftige Ausnahme mit definiertem Endpunkt, kein "
      "unbefristetes Schweigerecht. Diese Veröffentlichungspflicht ist zu "
      "unterscheiden von der Meldepflicht nach Art. 14 (an CSIRT und ENISA), von "
      "der Pflicht nach Art. 14 Abs. 8, Nutzer über eine aktiv ausgenutzte "
      "Schwachstelle oder einen schwerwiegenden Sicherheitsvorfall zu "
      "informieren, und von Art. 17 Abs. 5, wonach die ENISA im Einvernehmen mit "
      "dem Hersteller eine öffentlich bekannte gemeldete Schwachstelle in die "
      "europäische Schwachstellendatenbank aufnimmt."),

    Q("cra-sbom_vulnerability-05", "sbom_vulnerability", False,
      "Annex I Part II points (5), (6), Art. 13(17) Regulation (EU) 2024/2847 (CRA)",
      3, False, "d",
      "What does the CRA require of a manufacturer's vulnerability-reporting "
      "front door?",
      {
        "a": "A bug bounty programme with monetary rewards.",
        "b": "A security.txt file at a well-known URI on the manufacturer's website.",
        "c": "An automated web form is sufficient, provided it is reachable from the product documentation.",
        "d": "A coordinated vulnerability disclosure policy that is put in place AND enforced, measures facilitating information sharing about potential vulnerabilities including in third-party components, a contact address for reporting, and a single point of contact that is easily identifiable, listed in the Annex II user information, that lets users choose their preferred means of communication and is not limited to automated tools.",
      },
      "Was verlangt die CRA von der Anlaufstelle eines Herstellers für "
      "Schwachstellenmeldungen?",
      {
        "a": "Ein Bug-Bounty-Programm mit Geldprämien.",
        "b": "Eine security.txt-Datei unter einem well-known-URI auf der Website des Herstellers.",
        "c": "Ein automatisiertes Webformular genügt, sofern es aus der Produktdokumentation erreichbar ist.",
        "d": "Eine Strategie für die koordinierte Offenlegung von Schwachstellen, die aufgestellt UND umgesetzt wird, Maßnahmen zur Erleichterung des Informationsaustauschs über mögliche Schwachstellen auch in Komponenten Dritter, eine Kontaktadresse für Meldungen sowie eine zentrale Anlaufstelle, die von den Nutzern leicht ermittelt werden kann, in die Nutzerinformationen nach Anhang II aufgenommen wird, den Nutzern die Wahl ihres bevorzugten Kommunikationsmittels lässt und diese Mittel nicht auf automatisierte Instrumente beschränkt.",
      },
      "Annex I Part II point (5): manufacturers shall \"put in place and enforce "
      "a policy on coordinated vulnerability disclosure\". Point (6): they shall "
      "\"take measures to facilitate the sharing of information about potential "
      "vulnerabilities in their product with digital elements as well as in "
      "third-party components contained in that product, including by providing "
      "a contact address for the reporting of the vulnerabilities discovered in "
      "the product with digital elements\". Art. 13(17): \"manufacturers shall "
      "designate a single point of contact to enable users to communicate "
      "directly and rapidly with them, including in order to facilitate "
      "reporting on vulnerabilities\"; it must be easily identifiable and "
      "included in the Annex II user information; and \"[t]he single point of "
      "contact shall allow users to choose their preferred means of "
      "communication and shall not limit such means to automated tools.\" That "
      "last sentence is what disposes of the web-form-only answer. Bug bounties "
      "appear only in recital 76 as something manufacturers \"should be able to\" "
      "use inside a CVD policy - permissive, and a recital, so not a "
      "requirement. security.txt is industry convention, useful, and nowhere in "
      "the Regulation. Art. 13(6) is the mirror-image duty: reporting outward to "
      "the maintainers of components you consume.",
      "Anhang I Teil II Nummer 5: Hersteller müssen \"eine Strategie für die "
      "koordinierte Offenlegung von Schwachstellen aufstellen und umsetzen\". "
      "Nummer 6: Sie müssen \"Maßnahmen ergreifen, um den Austausch von "
      "Informationen über mögliche Schwachstellen in ihrem Produkt mit digitalen "
      "Elementen und darin enthaltenen Komponenten Dritter zu erleichtern, und "
      "dazu u. a. eine Kontaktadresse für die Meldung der in dem Produkt mit "
      "digitalen Elementen entdeckten Schwachstellen angeben\". Art. 13 Abs. 17: "
      "\"benennen die Hersteller eine zentrale Anlaufstelle, die es den Nutzern "
      "ermöglicht, direkt und schnell mit ihnen zu kommunizieren, auch um die "
      "Meldung von Schwachstellen des Produkts mit digitalen Elementen zu "
      "erleichtern\"; sie muss von den Nutzern leicht ermittelt werden können und "
      "in die Informationen und Anleitungen für die Nutzer gemäß Anhang II "
      "aufgenommen werden, und \"[d]ie zentrale Anlaufstelle ermöglicht es den "
      "Nutzern, ihr bevorzugtes Kommunikationsmittel zu wählen, wobei diese "
      "Mittel nicht auf automatisierte Instrumente beschränkt werden dürfen.\" "
      "(Anmerkung zur Terminologie: Die deutsche Fassung spricht in Art. 13 "
      "Abs. 17 von der \"zentralen Anlaufstelle\", in Anhang II Nummer 2 dagegen "
      "von der \"zentralen Kontaktstelle\"; die englische Fassung verwendet "
      "durchgehend \"single point of contact\". Gemeint ist dieselbe Stelle.) "
      "Dieser letzte Satz erledigt die "
      "Webformular-Antwort. Bug-Bounty-Programme kommen nur in Erwägungsgrund 76 "
      "vor, und zwar als etwas, das Hersteller im Rahmen ihrer Strategie nutzen "
      "können sollten - erlaubend, und ein Erwägungsgrund, also keine Pflicht. "
      "security.txt ist Branchenkonvention, nützlich und steht nirgends in der "
      "Verordnung. Art. 13 Abs. 6 ist die spiegelbildliche Pflicht: die Meldung "
      "nach außen an die Betreuer der von Ihnen verwendeten Komponenten."),

    # ---------------------------------------------------------------- topic D
    Q("cra-reporting-01", "reporting", True,
      "Art. 14(1), (2)(a), (b), (7), Art. 16(1) Regulation (EU) 2024/2847 (CRA)",
      4, True, "a",
      "At 09:00 on Tuesday your threat-intel team confirms reliable evidence "
      "that a vulnerability in your shipped product is being exploited in the "
      "wild. What must you do, by when, and to whom?",
      {
        "a": "An early warning notification without undue delay and in any event within 24 hours of becoming aware - so by 09:00 Wednesday - and a vulnerability notification without undue delay and in any event within 72 hours of becoming aware; both go simultaneously to the CSIRT designated as coordinator and to ENISA, submitted via the single reporting platform established under Article 16.",
        "b": "A single notification to the market surveillance authority of your Member State within 72 hours; ENISA and the CSIRTs are informed by that authority.",
        "c": "An early warning within 24 hours, after which the 72-hour clock for the fuller notification starts running from submission of that early warning.",
        "d": "A notification to ENISA alone within 24 hours; CSIRT involvement is triggered only if ENISA escalates.",
      },
      "Dienstag um 09:00 Uhr bestätigt Ihr Threat-Intel-Team verlässliche "
      "Nachweise dafür, dass eine Schwachstelle in Ihrem ausgelieferten Produkt "
      "aktiv ausgenutzt wird. Was müssen Sie bis wann und an wen tun?",
      {
        "a": "Eine Frühwarnung unverzüglich, in jedem Fall aber innerhalb von 24 Stunden nach Kenntniserlangung - also bis Mittwoch 09:00 Uhr - und eine Meldung der Schwachstelle unverzüglich, in jedem Fall aber innerhalb von 72 Stunden nach Kenntniserlangung; beide gehen gleichzeitig an das als Koordinator benannte CSIRT und an die ENISA, übermittelt über die nach Art. 16 eingerichtete einheitliche Meldeplattform.",
        "b": "Eine einzige Meldung an die Marktüberwachungsbehörde Ihres Mitgliedstaats innerhalb von 72 Stunden; ENISA und die CSIRTs werden von dieser Behörde unterrichtet.",
        "c": "Eine Frühwarnung innerhalb von 24 Stunden; danach läuft die 72-Stunden-Frist für die ausführlichere Meldung ab Übermittlung dieser Frühwarnung.",
        "d": "Eine Meldung allein an die ENISA innerhalb von 24 Stunden; das CSIRT wird nur eingeschaltet, wenn die ENISA eskaliert.",
      },
      "Art. 14(1) CRA: \"A manufacturer shall notify any actively exploited "
      "vulnerability contained in the product with digital elements that it "
      "becomes aware of simultaneously to the CSIRT designated as coordinator, "
      "in accordance with paragraph 7 of this Article, and to ENISA. The "
      "manufacturer shall notify that actively exploited vulnerability via the "
      "single reporting platform established pursuant to Article 16.\" "
      "Art. 14(2)(a): \"an early warning notification of an actively exploited "
      "vulnerability, without undue delay and in any event within 24 hours of "
      "the manufacturer becoming aware of it\". Art. 14(2)(b): \"a vulnerability "
      "notification, without undue delay and in any event within 72 hours of the "
      "manufacturer becoming aware of the actively exploited vulnerability\". "
      "Note carefully what the 72 hours runs from: BOTH clocks start at the same "
      "event - the manufacturer becoming aware - so the 72-hour deadline is 72 "
      "hours after awareness, not 72 hours after the early warning. That is the "
      "point of distractor (c), and it is the CRA's structural difference from "
      "the DORA incident cascade, where the intermediate report runs from "
      "submission of the initial notification. The addressee is not the market "
      "surveillance authority: under Art. 16(3) the CSIRTs pass the necessary "
      "information to the market surveillance authorities, not the other way "
      "round. Both limbs are also qualified by \"without undue delay\", so the "
      "hour figures are outer limits, not entitlements.",
      "Art. 14 Abs. 1 CRA: \"Ein Hersteller meldet jede aktiv ausgenutzte "
      "Schwachstelle, die in dem Produkt mit digitalen Elementen enthalten ist "
      "und von der er Kenntnis erlangt, gleichzeitig dem gemäß Absatz 7 als "
      "Koordinator benannten CSIRT und der ENISA. Der Hersteller meldet diese "
      "aktiv ausgenutzte Schwachstelle über die gemäß Artikel 16 eingerichtete "
      "einheitliche Meldeplattform.\" Art. 14 Abs. 2 Buchst. a: \"unverzüglich, "
      "in jedem Fall aber innerhalb von 24 Stunden, nachdem der Hersteller davon "
      "Kenntnis erlangt hat, eine Frühwarnung über eine aktiv ausgenutzte "
      "Schwachstelle\". Art. 14 Abs. 2 Buchst. b: \"unverzüglich, in jedem Fall "
      "aber innerhalb von 72 Stunden, nachdem der Hersteller Kenntnis von der "
      "aktiv ausgenutzten Schwachstelle erlangt hat, eine Meldung von "
      "Schwachstellen\". Entscheidend ist der Anknüpfungspunkt der 72 Stunden: "
      "BEIDE Fristen laufen ab demselben Ereignis - der Kenntniserlangung -, die "
      "72-Stunden-Frist also ab Kenntnis und nicht ab der Frühwarnung. Genau "
      "darauf zielt Antwort (c), und darin unterscheidet sich die CRA "
      "strukturell von der DORA-Meldekaskade, bei der der Zwischenbericht ab "
      "Übermittlung der Erstmeldung läuft. Adressat ist nicht die "
      "Marktüberwachungsbehörde: Nach Art. 16 Abs. 3 leiten die CSIRTs die "
      "erforderlichen Informationen an die Marktüberwachungsbehörden weiter, "
      "nicht umgekehrt. Beide Fristen stehen zudem unter \"unverzüglich\", die "
      "Stundenangaben sind also Höchstfristen, keine Ansprüche."),

    Q("cra-reporting-02", "reporting", False,
      "Art. 14(2)(c), (4)(c) Regulation (EU) 2024/2847 (CRA)", 4, True, "b",
      "The CRA requires a final report in both reporting tracks. From what event "
      "does each final-report deadline run?",
      {
        "a": "Both run one month from the manufacturer becoming aware.",
        "b": "They run from different events. For an actively exploited vulnerability, the final report is due no later than 14 days after a corrective or mitigating measure is available. For a severe incident, the final report is due within one month after the submission of the incident notification under Article 14(4)(b).",
        "c": "Both run 14 days from submission of the 72-hour notification.",
        "d": "Both run one month from submission of the early warning notification.",
      },
      "Die CRA verlangt in beiden Meldesträngen einen Abschlussbericht. Ab "
      "welchem Ereignis läuft die jeweilige Frist?",
      {
        "a": "Beide laufen einen Monat ab Kenntniserlangung des Herstellers.",
        "b": "Sie laufen ab unterschiedlichen Ereignissen. Bei einer aktiv ausgenutzten Schwachstelle ist der Abschlussbericht spätestens 14 Tage, nachdem eine Korrektur- oder Risikominderungsmaßnahme zur Verfügung steht, vorzulegen. Bei einem schwerwiegenden Sicherheitsvorfall ist er innerhalb eines Monats nach Übermittlung der Meldung des Sicherheitsvorfalls nach Art. 14 Abs. 4 Buchst. b vorzulegen.",
        "c": "Beide laufen 14 Tage ab Übermittlung der 72-Stunden-Meldung.",
        "d": "Beide laufen einen Monat ab Übermittlung der Frühwarnung.",
      },
      "This is the single most confusable point in Article 14, because the first "
      "two stages of the two tracks are symmetrical (24 hours and 72 hours from "
      "awareness in both) and the third stage is not. Art. 14(2)(c): \"unless "
      "the relevant information has already been provided, a final report, no "
      "later than 14 days after a corrective or mitigating measure is "
      "available\". Art. 14(4)(c): \"unless the relevant information has already "
      "been provided, a final report, within one month after the submission of "
      "the incident notification under point (b)\". The consequences are "
      "practical: in the vulnerability track the clock is engineering-driven and "
      "can start months after the notification, because it starts when a fix or "
      "mitigation exists; in the incident track the clock is calendar-driven and "
      "starts the moment you file the 72-hour notification, whether or not you "
      "have finished your analysis. Both are qualified by \"unless the relevant "
      "information has already been provided\", so a genuinely complete earlier "
      "submission can discharge the stage. Required minimum contents differ too: "
      "the vulnerability final report needs a description with severity and "
      "impact, information on any malicious actor where available, and details "
      "of the security update or other corrective measures; the incident final "
      "report needs a detailed description with severity and impact, the type of "
      "threat or likely root cause, and applied and ongoing mitigation measures.",
      "Das ist der am leichtesten zu verwechselnde Punkt des Artikels 14, weil "
      "die ersten beiden Stufen beider Stränge symmetrisch sind (jeweils 24 und "
      "72 Stunden ab Kenntnis), die dritte aber nicht. Art. 14 Abs. 2 Buchst. c: "
      "\"sofern die einschlägigen Informationen nicht bereits vorgelegt wurden, "
      "spätestens 14 Tage, nachdem eine Korrektur- oder "
      "Risikominderungsmaßnahme zur Verfügung steht, einen Abschlussbericht\". "
      "Art. 14 Abs. 4 Buchst. c: \"sofern die einschlägigen Informationen nicht "
      "bereits übermittelt wurden, innerhalb eines Monats nach Übermittlung der "
      "Meldung des Sicherheitsvorfalls gemäß Buchstabe b einen "
      "Abschlussbericht\". Die Folgen sind praktisch: Im Schwachstellenstrang "
      "wird die Frist durch die Technik ausgelöst und kann Monate nach der "
      "Meldung beginnen, weil sie an die Verfügbarkeit einer Abhilfe anknüpft; "
      "im Vorfallstrang läuft sie kalendarisch ab dem Zeitpunkt, zu dem Sie die "
      "72-Stunden-Meldung abgesetzt haben, unabhängig vom Stand Ihrer Analyse. "
      "Beide stehen unter dem Vorbehalt \"sofern die einschlägigen Informationen "
      "nicht bereits ... vorgelegt wurden\", eine wirklich vollständige frühere "
      "Übermittlung kann die Stufe also erledigen. Auch die Mindestinhalte "
      "unterscheiden sich: Der Schwachstellenbericht verlangt Beschreibung mit "
      "Schweregrad und Auswirkungen, falls verfügbar Angaben zum böswilligen "
      "Akteur sowie Angaben zur Sicherheitsaktualisierung oder anderen "
      "Korrekturmaßnahmen; der Vorfallbericht verlangt eine ausführliche "
      "Beschreibung mit Schweregrad und Auswirkungen, die Art der Bedrohung bzw. "
      "die zugrunde liegende Ursache und die angewandten und laufenden "
      "Risikominderungsmaßnahmen."),

    Q("cra-reporting-03", "reporting", False,
      "Art. 14(3), (5), Art. 3(43), (44) Regulation (EU) 2024/2847 (CRA)", 4, True, "c",
      "Which incidents must a manufacturer notify under Article 14(3)?",
      {
        "a": "Every incident having an impact on the security of the product with digital elements, and every near miss.",
        "b": "Only incidents where personal data has been confirmed lost or exfiltrated.",
        "c": "Only SEVERE incidents having an impact on the security of the product - and an incident is severe where it negatively affects or is capable of negatively affecting the product's ability to protect the availability, authenticity, integrity or confidentiality of sensitive or important data or functions, OR where it has led or is capable of leading to the introduction or execution of malicious code in the product or in the network and information systems of a user of the product.",
        "d": "Only incidents affecting more than a defined number of users, set by the CSIRT designated as coordinator.",
      },
      "Welche Sicherheitsvorfälle muss ein Hersteller nach Artikel 14 Absatz 3 "
      "melden?",
      {
        "a": "Jeden Sicherheitsvorfall mit Auswirkungen auf die Sicherheit des Produkts mit digitalen Elementen und jeden Beinahevorfall.",
        "b": "Nur Vorfälle, bei denen der Verlust oder Abfluss personenbezogener Daten bestätigt ist.",
        "c": "Nur SCHWERWIEGENDE Sicherheitsvorfälle mit Auswirkungen auf die Sicherheit des Produkts - und schwerwiegend ist ein Vorfall, wenn er sich negativ auf die Fähigkeit des Produkts auswirkt oder auswirken kann, die Verfügbarkeit, Authentizität, Integrität oder Vertraulichkeit von sensiblen oder wichtigen Daten oder Funktionen zu schützen, ODER wenn er zur Einführung oder Ausführung eines böswilligen Codes im Produkt oder im Netzwerk und Informationssystem eines Nutzers geführt hat oder dazu führen kann.",
        "d": "Nur Vorfälle oberhalb einer bestimmten Nutzerzahl, die das als Koordinator benannte CSIRT festlegt.",
      },
      "Art. 14(3) CRA limits the duty to \"any severe incident having an impact "
      "on the security of the product with digital elements\". Art. 3(44) "
      "defines the underlying category - \"an incident that negatively affects "
      "or is capable of negatively affecting the ability of a product with "
      "digital elements to protect the availability, authenticity, integrity or "
      "confidentiality of data or functions\" - and Art. 14(5) then supplies the "
      "severity filter with two alternative limbs: point (a) narrows Art. 3(44) "
      "to \"sensitive or important data or functions\", and point (b) covers an "
      "incident that \"has led or is capable of leading to the introduction or "
      "execution of malicious code in a product with digital elements or in the "
      "network and information systems of a user of the product with digital "
      "elements\". Note how far the \"is capable of\" wording reaches: a "
      "successful supply-chain implant in your build pipeline that has not yet "
      "executed anywhere is capable of leading to execution of malicious code in "
      "the product, and is therefore severe. Near misses are NOT notifiable "
      "under Art. 14 - Art. 15(2) makes them a voluntary channel only. Nothing "
      "in the CRA sets a user-count threshold, and personal data is a GDPR "
      "question, not the Art. 14 trigger.",
      "Art. 14 Abs. 3 CRA beschränkt die Pflicht auf \"jeden schwerwiegenden "
      "Sicherheitsvorfall, der sich auf die Sicherheit des Produkts mit "
      "digitalen Elementen auswirkt\". Art. 3 Nr. 44 definiert die Grundkategorie "
      "- einen Vorfall, \"der sich negativ auf die Fähigkeit eines Produkts mit "
      "digitalen Elementen auswirkt oder auswirken kann, die Verfügbarkeit, "
      "Authentizität, Integrität oder Vertraulichkeit von Daten oder Funktionen "
      "zu schützen\" -, und Art. 14 Abs. 5 fügt den Schwerefilter mit zwei "
      "Alternativen hinzu: Buchst. a verengt Art. 3 Nr. 44 auf \"sensiblen oder "
      "wichtigen Daten oder Funktionen\", Buchst. b erfasst Vorfälle, die \"zur "
      "Einführung oder Ausführung eines böswilligen Codes in einem Produkt mit "
      "digitalen Elementen oder im Netzwerk und Informationssystem eines Nutzers "
      "des Produkts mit digitalen Elementen geführt hat oder dazu führen kann\". "
      "Wie weit die Wendung \"oder dazu führen kann\" reicht, ist zu beachten: "
      "Ein erfolgreicher Lieferketten-Implantat in Ihrer Build-Pipeline, der noch "
      "nirgends ausgeführt wurde, kann zur Ausführung böswilligen Codes im "
      "Produkt führen und ist damit schwerwiegend. Beinahevorfälle sind nach "
      "Art. 14 NICHT meldepflichtig - Art. 15 Abs. 2 eröffnet dafür nur einen "
      "freiwilligen Kanal. Eine Nutzerzahlschwelle kennt die CRA nicht, und "
      "personenbezogene Daten sind eine Frage der DSGVO, nicht der Auslösung des "
      "Art. 14."),

    Q("cra-reporting-04", "reporting", False,
      "Art. 14(7) Regulation (EU) 2024/2847 (CRA)", 3, False, "b",
      "A US software vendor has no EU entity, but its engineering and security "
      "decisions for the product are made in its Romanian development centre, "
      "which is a subsidiary. Which CSIRT endpoint does it use for an Article 14 "
      "notification?",
      {
        "a": "Any CSIRT designated as coordinator it chooses; the platform routes the notification onwards, so the choice is immaterial.",
        "b": "The endpoint of the CSIRT designated as coordinator of the Member State of its main establishment in the Union - and for this Regulation the main establishment is the Member State where the decisions related to the cybersecurity of its products are predominantly taken, i.e. Romania on these facts.",
        "c": "The CSIRT of the Member State in which the vulnerability was first exploited.",
        "d": "The CSIRT of the Member State where the group's parent company is registered for tax purposes.",
      },
      "Ein US-Softwareanbieter hat keine EU-Gesellschaft, trifft die technischen "
      "und sicherheitsbezogenen Entscheidungen zum Produkt aber in seinem "
      "rumänischen Entwicklungszentrum, einer Tochtergesellschaft. Welchen "
      "CSIRT-Endpunkt nutzt er für eine Meldung nach Artikel 14?",
      {
        "a": "Ein beliebiges als Koordinator benanntes CSIRT; die Plattform leitet die Meldung ohnehin weiter, die Wahl ist also unerheblich.",
        "b": "Den Endpunkt des als Koordinator benannten CSIRT des Mitgliedstaats seiner Hauptniederlassung in der Union - und Hauptniederlassung ist für diese Verordnung der Mitgliedstaat, in dem die Entscheidungen im Zusammenhang mit der Cybersicherheit seiner Produkte überwiegend getroffen werden, hier also Rumänien.",
        "c": "Das CSIRT des Mitgliedstaats, in dem die Schwachstelle zuerst ausgenutzt wurde.",
        "d": "Das CSIRT des Mitgliedstaats, in dem die Konzernmutter steuerlich registriert ist.",
      },
      "Art. 14(7) CRA: the notification \"shall be submitted using the electronic "
      "notification end-point of the CSIRT designated as coordinator of the "
      "Member State where the manufacturers have their main establishment in the "
      "Union and shall be simultaneously accessible to ENISA. For the purposes "
      "of this Regulation, a manufacturer shall be considered to have its main "
      "establishment in the Union in the Member State where the decisions related "
      "to the cybersecurity of its products with digital elements are "
      "predominantly taken. If such a Member State cannot be determined, the "
      "main establishment shall be considered to be in the Member State where "
      "the manufacturer concerned has the establishment with the highest number "
      "of employees in the Union.\" The test is where cybersecurity decisions "
      "are taken - not corporate registration, not tax residence, not where the "
      "exploitation occurred. This matters commercially for exactly the Polish "
      "and Romanian nearshore development centres this module addresses: moving "
      "product security decision-making into a Member State moves the reporting "
      "endpoint there with it. Where a manufacturer genuinely has no main "
      "establishment in the Union, Art. 14(7) third subparagraph supplies a "
      "cascade in order: (a) the authorised representative's Member State for "
      "the highest number of products, then (b) the importer's, then (c) the "
      "distributor's, then (d) where the highest number of users are located. "
      "Under the fourth subparagraph, a manufacturer that landed on limb (d) may "
      "keep reporting subsequent cases to the same CSIRT it first reported to.",
      "Art. 14 Abs. 7 CRA: Die Meldung \"wird über den Endpunkt für die "
      "elektronische Meldung des CSIRT übermittelt, der als Koordinator des "
      "Mitgliedstaats benannt wurde, in dem die Hersteller ihre Hauptniederlassung "
      "in der Union haben, und ist gleichzeitig für die ENISA zugänglich. Für "
      "die Zwecke dieser Verordnung wird davon ausgegangen, dass ein Hersteller "
      "seine Hauptniederlassung in der Union in dem Mitgliedstaat hat, in dem die "
      "Entscheidungen im Zusammenhang mit der Cybersicherheit seiner Produkte "
      "mit digitalen Elementen überwiegend getroffen werden. Kann ein solcher "
      "Mitgliedstaat nicht bestimmt werden, so gilt als Mitgliedstaat der "
      "Hauptniederlassung der Mitgliedstaat, in dem der betreffende Hersteller "
      "die Niederlassung mit der höchsten Beschäftigtenzahl in der Union hat.\" "
      "Maßgeblich ist also, wo die Cybersicherheitsentscheidungen getroffen "
      "werden - nicht die gesellschaftsrechtliche Registrierung, nicht der "
      "steuerliche Sitz, nicht der Ort der Ausnutzung. Für genau die polnischen "
      "und rumänischen Nearshore-Entwicklungszentren, an die sich dieses Modul "
      "richtet, hat das wirtschaftliche Folgen: Wer die "
      "Produktsicherheitsentscheidungen in einen Mitgliedstaat verlagert, "
      "verlagert den Meldeendpunkt mit. Hat ein Hersteller tatsächlich keine "
      "Hauptniederlassung in der Union, sieht Art. 14 Abs. 7 Unterabs. 3 eine "
      "Rangfolge vor: a) der Mitgliedstaat des Bevollmächtigten mit der höchsten "
      "Produktzahl, dann b) der des Einführers, dann c) der des Händlers, dann "
      "d) der mit der höchsten Nutzerzahl. Nach Unterabs. 4 darf ein Hersteller, "
      "der über Buchstabe d zugeordnet wurde, spätere Fälle weiterhin demselben "
      "CSIRT melden."),

    Q("cra-reporting-05", "reporting", False,
      "Art. 14(6), (8) Regulation (EU) 2024/2847 (CRA)", 3, False, "d",
      "Between the 72-hour notification and the final report, what does the CRA "
      "require - and what does it require towards your users?",
      {
        "a": "An intermediate report is mandatory every 72 hours until the final report is filed.",
        "b": "Nothing at all until the final report; user communication is at the manufacturer's commercial discretion throughout.",
        "c": "Users must be informed only after the final report has been accepted, so that no unverified information circulates.",
        "d": "An intermediate report is not automatic: where necessary, the CSIRT designated as coordinator initially receiving the notification may request one on relevant status updates. Separately and independently, after becoming aware the manufacturer must inform impacted users - and where appropriate all users - of the vulnerability or incident and, where necessary, of risk mitigation and corrective measures they can deploy, where appropriate in a structured, machine-readable format that is easily automatically processable.",
      },
      "Was verlangt die CRA zwischen der 72-Stunden-Meldung und dem "
      "Abschlussbericht - und was verlangt sie gegenüber Ihren Nutzern?",
      {
        "a": "Ein Zwischenbericht ist alle 72 Stunden verpflichtend, bis der Abschlussbericht vorliegt.",
        "b": "Bis zum Abschlussbericht gar nichts; die Nutzerkommunikation liegt durchgehend im unternehmerischen Ermessen des Herstellers.",
        "c": "Nutzer dürfen erst nach Annahme des Abschlussberichts informiert werden, damit keine ungeprüften Informationen kursieren.",
        "d": "Ein Zwischenbericht erfolgt nicht automatisch: Erforderlichenfalls kann das als Koordinator benannte CSIRT, das die Meldung ursprünglich erhalten hat, einen Zwischenbericht über relevante Statusaktualisierungen anfordern. Davon getrennt und unabhängig muss der Hersteller nach Kenntniserlangung die betroffenen Nutzer - und gegebenenfalls alle Nutzer - über die Schwachstelle oder den Vorfall und erforderlichenfalls über Risikominderungs- und Korrekturmaßnahmen informieren, gegebenenfalls in einem strukturierten, maschinenlesbaren Format, das leicht automatisch zu verarbeiten ist.",
      },
      "Art. 14(6) CRA: \"Where necessary, the CSIRT designated as coordinator "
      "initially receiving the notification may request manufacturers to provide "
      "an intermediate report on relevant status updates about the actively "
      "exploited vulnerability or severe incident having an impact on the "
      "security of the product with digital elements.\" It is a supervisory "
      "power, not a standing obligation - the contrast with DORA, where the "
      "intermediate report is due on a fixed clock, is worth internalising if "
      "you work across both regimes. Art. 14(8): \"After becoming aware of an "
      "actively exploited vulnerability or a severe incident ... the manufacturer "
      "shall inform the impacted users of the product with digital elements, and "
      "where appropriate all users, of that vulnerability or incident and, where "
      "necessary, of any risk mitigation and corrective measures that the users "
      "can deploy ... where appropriate in a structured, machine-readable format "
      "that is easily automatically processable. Where the manufacturer fails to "
      "inform the users ... in a timely manner, the notified CSIRTs designated as "
      "coordinators may provide such information to the users when considered to "
      "be proportionate and necessary for preventing or mitigating the impact.\" "
      "So the user-facing duty is a legal obligation with a substitution "
      "mechanism attached, not a marketing choice - and the machine-readable "
      "phrasing is the CRA's only textual nod towards structured advisory "
      "formats such as CSAF or a VEX document, neither of which it names or "
      "requires.",
      "Art. 14 Abs. 6 CRA: Erforderlichenfalls kann das als Koordinator "
      "benannte CSIRT, das die Meldung ursprünglich erhält, die Hersteller "
      "auffordern, \"einen Zwischenbericht über relevante Statusaktualisierungen "
      "über die aktiv genutzte Schwachstelle oder den schwerwiegenden "
      "Sicherheitsvorfall, der sich auf die Sicherheit des Produkts mit "
      "digitalen Elementen auswirkt, vorzulegen\". (Die deutsche Fassung des "
      "Amtsblatts schreibt an dieser Stelle \"CSIRT, dass ursprünglich die "
      "Meldung erhält\"; gemeint ist ersichtlich der Relativsatz \"das\". Die "
      "englische Fassung lautet insoweit \"the CSIRT designated as coordinator "
      "initially receiving the notification\".) Das ist eine Befugnis der "
      "Aufsicht, keine laufende Pflicht - der Unterschied zu DORA, wo der "
      "Zwischenbericht fristgebunden geschuldet ist, sollte verinnerlicht "
      "werden, wenn Sie in beiden Regimen arbeiten. Art. 14 Abs. 8: \"Nachdem "
      "der Hersteller Kenntnis von einer aktiv ausgenutzten Schwachstelle oder "
      "einem schwerwiegenden Sicherheitsvorfall ... erlangt hat, informiert er "
      "die betroffenen Nutzer des Produkts mit digitalen Elementen und "
      "gegebenenfalls alle Nutzer über diese Schwachstelle oder diesen "
      "schwerwiegenden Sicherheitsvorfall und erforderlichenfalls über jegliche "
      "Risikominderungsmaßnahmen und Korrekturmaßnahmen, die die Nutzer ergreifen "
      "können ..., gegebenenfalls in einem strukturierten, maschinenlesbaren "
      "Format, das leicht automatisch zu verarbeiten ist. Versäumt es der "
      "Hersteller, die Nutzer des Produkts mit digitalen Elementen rechtzeitig "
      "zu informieren, können die als Koordinatoren benannten CSIRTs diese "
      "Informationen den Nutzern zur Verfügung stellen, wenn sie dies für "
      "verhältnismäßig und erforderlich halten, um die Auswirkungen dieser "
      "Schwachstellen oder Sicherheitsvorfälle zu verhindern oder abzumildern.\" "
      "Die Nutzerinformation "
      "ist also eine Rechtspflicht mit angehängtem Ersatzvornahmemechanismus, "
      "keine Marketingentscheidung - und die Wendung \"maschinenlesbar\" ist der "
      "einzige Textanker der CRA in Richtung strukturierter Advisory-Formate wie "
      "CSAF oder eines VEX-Dokuments, von denen die Verordnung keines benennt "
      "oder vorschreibt."),
]


META = {
    "app": "Zettacard / cra-supply-chain-lernmodul",
    "version": "0.1-draft",
    "generated": "2026-08-16",
    "description": (
        "DRAFT pilot question pool for the module 'CRA - Secure Supply Chain & "
        "Vulnerability Handling' (cra_supply_chain, module 2A of the B2B "
        "DORA/CRA roadmap). Audience: DevSecOps engineers, CTOs and software "
        "supply-chain / security engineering staff at manufacturers of products "
        "with digital elements. English is the canonical locale for this pilot "
        "(the roadmap targets EN/PL/RO for this module, i.e. the Polish and "
        "Romanian tech-hub markets); German is a secondary locale and is a "
        "deliberate deviation from the DE-canonical convention of the sibling "
        "DORA modules. All legal content is grounded exclusively in the Official "
        "Journal text of Regulation (EU) 2024/2847 (Cyber Resilience Act), CELEX "
        "32024R2847, read in full in the English and German language versions "
        "AND in the consolidated version incorporating the corrigenda published "
        "up to 17 October 2025. No question text was taken from any commercial "
        "provider. " + DISCLAIMER_EN
    ),
    "legal_disclaimer_en": DISCLAIMER_EN,
    "legal_disclaimer": DISCLAIMER_DE,
    "class": "ALL",
    "locales": ["en", "de"],
    "canonical_locale": "en",
    "canonical_locale_note": (
        "EN is canonical for this module by deliberate audience decision "
        "(DevSecOps/CTO readers in Poland and Romania), not by oversight. The "
        "German strings are a secondary translation and were checked against the "
        "German OJ language version of the CRA, not machine-translated from the "
        "English."
    ),
    "point_system": "3-4 points per question, matching this app's existing compliance-module style",
    "total_questions": 20,
    "legal_review_status": (
        "DRAFT - NOT legally reviewed. Primary-source verification performed "
        "2026-08-16 against the Official Journal text retrieved from the EU "
        "Publications Office Cellar repository "
        "(publications.europa.eu/resource/celex/<CELEX>, Accept: "
        "application/xhtml+xml, Accept-Language: eng / deu): Regulation (EU) "
        "2024/2847 (Cyber Resilience Act), CELEX 32024R2847, OJ L, 2024/2847, "
        "20.11.2024; and the consolidated version 02024R2847-20241120 (EN "
        "000.003), which incorporates three corrigenda in the EN version "
        "(OJ L, 2024/90780, 5.12.2024; OJ L, 2025/90555, 2.7.2025; OJ L, "
        "2025/90828, 17.10.2025) and two in the DE version (OJ L, 2025/90555, "
        "2.7.2025; OJ L, 2025/90828, 17.10.2025). Two corrections are material "
        "to this module and the questions follow the CORRECTED text: Art. 64(10) "
        "'paragraphs 3 to 9' -> 'paragraphs 2 to 9' (EN and DE), and the German "
        "Art. 13(8), from which the words 'der erwarteten Produktlebensdauer "
        "und' were deleted. Also read in full: Commission Delegated Regulation "
        "(EU) 2026/881 of 11 December 2025 (CELEX 32026R0881, OJ L, 2026/881, "
        "20.4.2026) on delaying dissemination of notifications - no answer key "
        "in this pilot depends on it. See "
        "docs/cra-supply-chain-pre-review-dossier-2026-08-16.md for the "
        "per-question confidence-tier ledger before any use."
    ),
    "renewal_months": None,
    "renewal_basis": "not_specified_in_statute",
    "renewal_note": (
        "Regulation (EU) 2024/2847 prescribes no training interval of any kind. "
        "The only express recurring duties in this subject area are the ENISA "
        "24-monthly technical report under Art. 17(3) and the Commission's "
        "four-yearly evaluation report under Art. 70(1) - neither is a training "
        "cadence. Art. 10 asks Member States to promote re-skilling and "
        "up-skilling for manufacturers' employees, but sets no frequency. A "
        "renewal interval would be a product decision, not a statutory one."
    ),
    "pass_rule_note": (
        "Open. No EXAM_QUESTION_COUNT_BY_TYPE / MAX_ERROR_POINTS_BY_TYPE / "
        "EXAM_TOPIC_DRAW values are proposed here; the 4x5 topic split suggests "
        "a draw touching all four topics, but that is a product decision after "
        "legal review."
    ),
    "draft_note": (
        "Not registered in data/build_modules.py, not in "
        "data/modules_manifest.json, app.js untouched, no build step run, "
        "nothing staged or committed. The _DRAFT filename suffix keeps this file "
        "out of the live build path by construction."
    ),
    "license": "CC BY-NC-SA 4.0",
    "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "license_note": (
        "Attribution-NonCommercial-ShareAlike: free to use, adapt, and "
        "redistribute for non-commercial exam-prep purposes, with credit and "
        "under the same license. Commercial reuse needs a separate arrangement; "
        "non-commercial prep tools/forks are welcome."
    ),
}


# --------------------------------------------------------------------------
# integrity checks
# --------------------------------------------------------------------------

ASCII_TRANSLIT_PATTERNS = [
    "fuer", "ueber", "muessen", "koennen", "waere", "gefuehrt",
    "ausschliesslich", "faellt", "maessig", "groesse", "zustaendig",
    "behoerde", "moeglich", "spaetest", "unverzueglich", "gemaess",
    "pruef", "schaetz", "vorfaelle", "jaehrlich", "massnahm", "erfuell",
    "haerte", "verstoesse", "regelmaessig", "gemaesse", "sicherheitsmaessig",
    "hersteller-stueckliste", "stueckliste", "abhaengigkeit", "geldbusse",
    "schliesslich", "grundsaetzlich", "vollstaendig", "naechste",
]

LEGIT_ASCII_DE_WORDS = {
    # words that legitimately contain ae/oe/ue/ss without needing an umlaut
    "dauer", "dauert", "gedauert", "datenquellen", "genaue", "genauer",
    "konsequenz", "konsequenzen", "prozess", "prozesse", "prozessen",
    "beschluss", "dass", "muss", "abgeschlossen", "quelloffene",
    "quelloffener", "quelloffenen", "quellen", "aktuell", "neue", "neuen",
    "neuer", "steuer", "steuerlich", "steuerlichen", "erneuerung",
    "auslieferung", "ausserdem", "eu", "user", "users",
    # further legitimate ASCII German words appearing in this file's DE strings
    "abfluss", "abschlussbericht", "abschlussberichts", "adressat",
    "amtsblattfassung", "auffassung", "bauen", "bestandsschutz", "betreuer",
    "bewusst", "cvss-basiswert", "cvss-wert", "dessen", "ereignissen",
    "erfasst", "erlassen", "ermessen", "ermessensbefugnis", "fassung",
    "hauptniederlassung", "informationssystem", "klassische", "kommission",
    "kontaktadresse", "lassen", "niedergelassene", "niederlassung",
    "nutzungsdauer", "produktlebensdauer", "quelle", "release-prozess",
    "sodass", "stattdessen", "steuerliche", "voraussichtlich",
    "voraussichtlichen", "warschauer", "wessen", "zuerst",
}


def de_strings(obj, acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "de" or k == "legal_disclaimer" or k.endswith("_de"):
                acc.extend(collect_strings(v))
            else:
                de_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            de_strings(v, acc)
    return acc


def collect_strings(obj, acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, str):
        acc.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            collect_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            collect_strings(v, acc)
    return acc


def en_strings(obj, acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "en":
                acc.extend(collect_strings(v))
            else:
                en_strings(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            en_strings(v, acc)
    return acc


def main():
    doc = {"meta": META, "questions": QUESTIONS}
    fails = []

    # 1. schema parity against kartellrecht_pilot.json
    with open(REF, encoding="utf-8") as fh:
        ref = json.load(fh)
    ref_keys = list(ref["questions"][0].keys())
    for q in QUESTIONS:
        if list(q.keys()) != ref_keys:
            fails.append("KEY ORDER mismatch on %s: %s" % (q["id"], list(q.keys())))
    if ref_keys != KEY_ORDER:
        fails.append("reference key order changed: %s" % ref_keys)

    # 2. count, ids, options, correct key
    if len(QUESTIONS) != 20:
        fails.append("expected 20 questions, got %d" % len(QUESTIONS))
    ids = [q["id"] for q in QUESTIONS]
    if len(set(ids)) != len(ids):
        fails.append("duplicate question ids")
    for q in QUESTIONS:
        for loc in ("en", "de"):
            opts = q["text"][loc]["options"]
            if set(opts.keys()) != {"a", "b", "c", "d"}:
                fails.append("%s/%s option keys != a,b,c,d" % (q["id"], loc))
            if q["correct"][0] not in opts:
                fails.append("%s/%s correct key missing" % (q["id"], loc))
            if not q["text"][loc]["question"].strip():
                fails.append("%s/%s empty question" % (q["id"], loc))
            if not q["explanation"][loc].strip():
                fails.append("%s/%s empty explanation" % (q["id"], loc))
        if q["topic_code"] not in TOPICS:
            fails.append("%s unknown topic_code" % q["id"])
        if q["topic"] != TOPICS[q["topic_code"]][0]:
            fails.append("%s topic label mismatch" % q["id"])

    # 3. answer-key distribution 5/5/5/5
    from collections import Counter
    dist = Counter(q["correct"][0] for q in QUESTIONS)
    if dict(dist) != {"a": 5, "b": 5, "c": 5, "d": 5}:
        fails.append("answer key distribution not 5/5/5/5: %s" % dict(dist))

    # 4. topic distribution 5/5/5/5
    tdist = Counter(q["topic_code"] for q in QUESTIONS)
    if set(tdist.values()) != {5}:
        fails.append("topic distribution not 5 per topic: %s" % dict(tdist))

    # 5. points 12x4 + 8x3
    pdist = Counter(q["points"] for q in QUESTIONS)
    if dict(pdist) != {4: 12, 3: 8}:
        fails.append("points distribution not 12x4 / 8x3: %s" % dict(pdist))

    # 6. high_stakes / grundstoff
    hs = sum(1 for q in QUESTIONS if q["high_stakes"])
    gs = sum(1 for q in QUESTIONS if q["grundstoff"])
    if hs != 10:
        fails.append("expected 10 high_stakes, got %d" % hs)
    if gs != 4:
        fails.append("expected 4 grundstoff, got %d" % gs)

    # 7. German orthography
    de_text = "\n".join(de_strings(doc))
    umlauts = sum(de_text.count(c) for c in "äöüÄÖÜß")
    low = de_text.lower()
    hits = [p for p in ASCII_TRANSLIT_PATTERNS if p in low]
    if hits:
        fails.append("ASCII transliteration residue in German text: %s" % hits)
    if umlauts < 200:
        fails.append("suspiciously few umlaut/eszett characters: %d" % umlauts)

    # 7b. exhaustive audit: German words containing ae/oe/ue/ss with no umlaut
    suspects = set()
    for w in re.findall(r"[A-Za-zÄÖÜäöüß-]+", de_text):
        wl = w.lower()
        if any(c in wl for c in "äöüß"):
            continue
        if ("ae" in wl or "oe" in wl or "ue" in wl or "ss" in wl):
            base = wl.strip("-")
            if base not in LEGIT_ASCII_DE_WORDS:
                suspects.add(base)

    # 8. no umlauts in English fields
    en_text = "\n".join(en_strings(doc))
    en_umlauts = [c for c in en_text if c in "äöüÄÖÜß"]
    if en_umlauts:
        fails.append("umlaut characters found in English fields: %r" % en_umlauts[:10])

    # 9. punctuation convention (kartellrecht_pilot.json: straight quotes, ASCII hyphens)
    all_text = "\n".join(collect_strings(doc))
    for bad, name in [("‘", "left single quote"), ("’", "right single quote"),
                      ("“", "left double quote"), ("”", "right double quote"),
                      ("–", "en dash"), ("—", "em dash")]:
        if bad in all_text:
            fails.append("typographic character present (%s)" % name)

    # 10. no non-Latin scripts / stray control chars
    for ch in set(all_text):
        if unicodedata.category(ch).startswith("C") and ch not in "\n\t":
            fails.append("control character %r present" % ch)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    print("wrote %s (%d questions)" % (OUT, len(QUESTIONS)))
    print("answer key distribution: %s" % dict(sorted(dist.items())))
    print("topic distribution:      %s" % dict(sorted(tdist.items())))
    print("points distribution:     %s" % dict(sorted(pdist.items())))
    print("high_stakes: %d   grundstoff: %d" % (hs, gs))
    print("German umlaut/eszett characters (ä ö ü Ä Ö Ü ß): %d" % umlauts)
    print("ASCII-transliteration residue hits: %d" % len(hits))
    print("ae/oe/ue/ss words in German text without an umlaut (manual review): %s"
          % (sorted(suspects) if suspects else "none"))
    print("umlauts in English fields: %d" % len(en_umlauts))

    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  - %s" % f)
        sys.exit(1)
    print("\nall integrity checks passed")


if __name__ == "__main__":
    main()
