#!/usr/bin/env python3
"""One-off authoring script for the fuehrerschein_bus module (D-family Zusatzstoff).

Hand-run once to produce:
  - data/fuehrerschein_bus_pilot.json   (master source, same shape as lksg_pilot.json /
                                          lkw_pilot.json)
  - app/data/fuehrerschein_bus/core.json         (locale-independent question fields)
  - app/data/fuehrerschein_bus/locales/de.json
  - app/data/fuehrerschein_bus/locales/en.json

Mirrors data/gen_lksg.py's build() shape, scoped to just this one module.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(HERE, "..", "app", "data")

# D-family classes covered by this Zusatzstoff module: D1, D1E, D, DE
# (§ 6 FeV: D1 = up to 16 passengers/max 8 m; D = more than 8 passengers;
#  D1E/DE = the respective tractor class combined with a trailer > 750 kg).
D_FAMILY = ["D1", "D1E", "D", "DE"]

QUESTIONS = [
    # =========================================================================
    # Topic 1: PBefG/BOKraft - Fahrgastverhalten und Sicherheit (12)
    # =========================================================================
    dict(
        id="bus-pbefg-01", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 1 BOKraft",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Woran müssen sich Fahrgäste nach § 14 Abs. 1 BOKraft grundsätzlich halten, wenn sie einen Linienbus benutzen?",
            o={
                "a": "An gar keine Vorgaben, das Verhalten der Fahrgäste ist gesetzlich nicht geregelt",
                "b": "An das, was die Sicherheit und Ordnung des Betriebs sowie die Rücksicht auf andere Personen erfordern, und an die Anweisungen des Betriebspersonals",
                "c": "Ausschließlich an eine vom Fahrgast selbst festgelegte Hausordnung",
                "d": "Nur an die Vorgaben der StVO, BOKraft gilt für Fahrgäste nicht",
            },
            e="§ 14 Abs. 1 BOKraft verpflichtet Fahrgäste, sich so zu verhalten, wie es die Sicherheit und Ordnung des Betriebs sowie die Rücksicht auf andere Personen erfordern, und den Anweisungen des Betriebspersonals (also insbesondere des Fahrers) Folge zu leisten.",
        ),
        en=dict(
            q="Under Sec. 14(1) BOKraft, what must passengers on a scheduled bus service generally comply with?",
            o={
                "a": "No requirements at all; passenger conduct is not regulated by law",
                "b": "Whatever the safety and orderly operation of the service and consideration for other persons require, and the instructions of the operating staff",
                "c": "Exclusively a house code the passenger sets for themselves",
                "d": "Only the StVO; BOKraft does not apply to passengers",
            },
            e="Sec. 14(1) BOKraft obliges passengers to conduct themselves as safety and orderly operation of the service, as well as consideration for other persons, require, and to follow the instructions of the operating staff (in particular the driver).",
        ),
    ),
    dict(
        id="bus-pbefg-02", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 2 BOKraft",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Welches der folgenden Verhaltensweisen ist Fahrgästen nach § 14 Abs. 2 BOKraft ausdrücklich untersagt?",
            o={
                "a": "Während der Fahrt ruhig auf einem Sitzplatz zu sitzen",
                "b": "Den Fahrer nach der Ankunftszeit an der Endhaltestelle zu fragen",
                "c": "Während der Fahrt auf- oder abzuspringen sowie sich während der Fahrt mit dem Fahrer zu unterhalten",
                "d": "Ein Ticket am Automaten zu kaufen",
            },
            e="§ 14 Abs. 2 BOKraft verbietet Fahrgästen unter anderem, sich während der Fahrt mit dem Fahrer zu unterhalten, Türen eigenmächtig zu öffnen, Sicherheitseinrichtungen zu missbrauchen, Gegenstände aus dem Fahrzeug zu werfen sowie während der Fahrt auf- oder abzuspringen - Verhaltensweisen, die die Verkehrssicherheit unmittelbar gefährden.",
        ),
        en=dict(
            q="Which of the following is explicitly prohibited for passengers under Sec. 14(2) BOKraft?",
            o={
                "a": "Sitting quietly in a seat while the vehicle is moving",
                "b": "Asking the driver about the arrival time at the terminus",
                "c": "Jumping on or off while the vehicle is moving, and talking to the driver while the vehicle is moving",
                "d": "Buying a ticket from a vending machine",
            },
            e="Sec. 14(2) BOKraft prohibits passengers from, among other things, talking to the driver while the vehicle is in motion, opening doors without authorization, misusing safety equipment, throwing objects from the vehicle, and jumping on or off a moving vehicle - conduct that directly endangers traffic safety.",
        ),
    ),
    dict(
        id="bus-pbefg-03", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 2 BOKraft",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Darf ein Fahrgast versuchen, in einen als 'besetzt' gekennzeichneten Bus einzusteigen oder noch einzusteigen bzw. auszusteigen, wenn die Türen bereits schließen oder die Abfahrt unmittelbar bevorsteht?",
            o={
                "a": "Ja, das ist immer erlaubt, solange keine Verletzungsgefahr besteht",
                "b": "Nein, § 14 Abs. 2 BOKraft verbietet dies ausdrücklich, weil dabei ein erhebliches Verletzungsrisiko besteht",
                "c": "Ja, aber nur wenn der Fahrgast eine Zeitkarte besitzt",
                "d": "Das ist nur bei Doppelstockbussen verboten",
            },
            e="§ 14 Abs. 2 BOKraft untersagt es Fahrgästen ausdrücklich, in als voll besetzt gekennzeichnete Fahrzeuge einzusteigen sowie ein- oder auszusteigen, wenn die Abfahrt unmittelbar bevorsteht oder die Türen bereits schließen - solche Situationen bergen ein hohes Risiko, beim Anfahren oder durch sich schließende Türen verletzt zu werden.",
        ),
        en=dict(
            q="May a passenger try to board a bus marked as 'full', or board/alight while the doors are already closing or departure is imminent?",
            o={
                "a": "Yes, this is always permitted as long as there is no risk of injury",
                "b": "No, Sec. 14(2) BOKraft expressly prohibits this because it carries a significant risk of injury",
                "c": "Yes, but only if the passenger holds a season ticket",
                "d": "This is only prohibited on double-decker buses",
            },
            e="Sec. 14(2) BOKraft expressly prohibits passengers from boarding a vehicle marked as fully occupied, and from boarding or alighting when departure is imminent or the doors are already closing - such situations carry a high risk of injury from the vehicle moving off or from closing doors.",
        ),
    ),
    dict(
        id="bus-pbefg-04", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 3 BOKraft",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Was verlangt § 14 Abs. 3 BOKraft von Fahrgästen im Linienverkehr zusätzlich, etwa beim Ein- und Aussteigen?",
            o={
                "a": "Fahrgäste dürfen nur an dafür bestimmten Haltestellen ein- und aussteigen, sollen die Türbereiche zügig freimachen, sich festhalten und Kinder beaufsichtigen, damit diese nicht auf Sitzen stehen oder knien",
                "b": "Fahrgäste müssen sich vor jeder Fahrt schriftlich beim Fahrer anmelden",
                "c": "Fahrgäste dürfen an jeder beliebigen Straßenstelle ein- und aussteigen, wenn der Fahrer zustimmt",
                "d": "Kinder dürfen ohne Aufsicht auf Sitzen stehen, solange sie angeschnallt sind",
            },
            e="§ 14 Abs. 3 BOKraft konkretisiert das Verhalten im Linienverkehr: Ein- und Aussteigen ist nur an den dafür bestimmten Haltestellen zulässig, der Türbereich soll zügig freigemacht werden, Fahrgäste sollen sich festen Halt verschaffen, und Kinder sind so zu beaufsichtigen, dass sie nicht auf Sitzen stehen oder knien.",
        ),
        en=dict(
            q="What does Sec. 14(3) BOKraft additionally require of passengers on scheduled bus services, e.g. when boarding and alighting?",
            o={
                "a": "Passengers may only board and alight at designated stops, should clear the door area promptly, should hold on securely, and must supervise children so they do not stand or kneel on seats",
                "b": "Passengers must register with the driver in writing before every trip",
                "c": "Passengers may board or alight at any point on the road, provided the driver agrees",
                "d": "Children may stand on seats unsupervised as long as they wear a seatbelt",
            },
            e="Sec. 14(3) BOKraft spells out conduct on scheduled services: boarding and alighting is only permitted at designated stops, the door area should be cleared promptly, passengers should hold on securely, and children must be supervised so they do not stand or kneel on seats.",
        ),
    ),
    dict(
        id="bus-pbefg-05", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 4 BOKraft",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Was darf das Unternehmen bzw. das Fahr- oder Betriebspersonal tun, wenn ein Fahrgast trotz Ermahnung wiederholt gegen die Verhaltenspflichten des § 14 BOKraft verstößt?",
            o={
                "a": "Nichts, ein Ausschluss von der Beförderung ist unter keinen Umständen zulässig",
                "b": "Sofort die Polizei rufen, ohne den Fahrgast vorher zu ermahnen",
                "c": "Den Fahrgast nach vorheriger Ermahnung von der Beförderung ausschließen (§ 14 Abs. 4 BOKraft)",
                "d": "Dem Fahrgast lebenslang die Nutzung sämtlicher Buslinien in Deutschland untersagen",
            },
            e="§ 14 Abs. 4 BOKraft erlaubt es dem Unternehmer bzw. dem Betriebspersonal, einen Fahrgast, der trotz Ermahnung gegen seine Verhaltenspflichten verstößt, von der Beförderung auszuschließen. Dies ist ein Hausrecht, kein pauschales bundesweites Beförderungsverbot.",
        ),
        en=dict(
            q="What may the company or its driving/operating staff do if a passenger repeatedly violates the conduct duties of Sec. 14 BOKraft despite a warning?",
            o={
                "a": "Nothing; excluding a passenger from carriage is never permissible",
                "b": "Immediately call the police without warning the passenger first",
                "c": "Exclude the passenger from carriage after a prior warning (Sec. 14(4) BOKraft)",
                "d": "Ban the passenger for life from using every bus line in Germany",
            },
            e="Sec. 14(4) BOKraft allows the operator or its staff to exclude a passenger from carriage, after a prior warning, if the passenger violates their conduct duties. This is a right of the operator over that particular service, not a blanket nationwide travel ban.",
        ),
    ),
    dict(
        id="bus-pbefg-06", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 22 PBefG",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was besagt die Beförderungspflicht nach § 22 PBefG für ein genehmigtes Busunternehmen?",
            o={
                "a": "Der Unternehmer darf Fahrgäste frei nach Sympathie auswählen",
                "b": "Der Unternehmer ist zur Beförderung verpflichtet, wenn die Beförderungsbedingungen eingehalten werden, die Beförderung mit den regelmäßig eingesetzten Mitteln möglich ist und keine unabwendbaren Hindernisse vorliegen",
                "c": "Eine Beförderungspflicht besteht nur für Fahrgäste mit Zeitkarten",
                "d": "Die Beförderungspflicht gilt ausschließlich für den Schülerverkehr",
            },
            e="§ 22 PBefG verpflichtet den genehmigten Unternehmer grundsätzlich zur Beförderung, sofern die Beförderungsbedingungen eingehalten werden, die Beförderung mit den regelmäßig eingesetzten Beförderungsmitteln möglich ist und sie nicht durch vom Unternehmer nicht abwendbare oder behebbare Umstände verhindert wird - ein Kontrahierungszwang im öffentlichen Interesse.",
        ),
        en=dict(
            q="What does the duty to carry under Sec. 22 PBefG mean for a licensed bus operator?",
            o={
                "a": "The operator may freely pick and choose passengers as they please",
                "b": "The operator is obliged to carry passengers if the conditions of carriage are complied with, carriage is possible with the vehicles regularly deployed, and no circumstances beyond the operator's control prevent it",
                "c": "A duty to carry exists only for passengers holding season tickets",
                "d": "The duty to carry applies exclusively to school transport services",
            },
            e="Sec. 22 PBefG generally obliges a licensed operator to carry passengers, provided the conditions of carriage are met, carriage is possible with the vehicles regularly deployed, and it is not prevented by circumstances the operator cannot avert or remedy - a public-interest contracting obligation.",
        ),
    ),
    dict(
        id="bus-pbefg-07", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="VO (EU) Nr. 181/2011 Art. 10(4), 13",
        points=4, high_stakes=True, correct=["c"],
        de=dict(
            q="Welche Pflicht ergibt sich aus der EU-Fahrgastrechteverordnung (VO (EU) Nr. 181/2011) gegenüber Personen mit Behinderungen oder eingeschränkter Mobilität im Busverkehr?",
            o={
                "a": "Personen mit eingeschränkter Mobilität dürfen von der Beförderung generell ausgeschlossen werden, wenn dies dem Fahrplan dient",
                "b": "Es besteht keinerlei besondere Unterstützungspflicht, jeder Fahrgast muss sich selbst um Hilfe kümmern",
                "c": "Diesen Personen ist unentgeltlich Hilfeleistung beim Ein- und Aussteigen sowie an dafür benannten Bushaltestellen/-bahnhöfen zu leisten; eine Begleitperson kann kostenlos mitfahren, wenn dies zur Erfüllung von Sicherheitsanforderungen erforderlich ist",
                "d": "Rollstuhlfahrer dürfen nur auf Linien mit weniger als 50 km Streckenlänge befördert werden",
            },
            e="Die VO (EU) Nr. 181/2011 verpflichtet Busunternehmen, Personen mit Behinderungen und eingeschränkter Mobilität unentgeltliche Hilfeleistung beim Ein- und Aussteigen sowie an benannten Terminals/Haltestellen zu gewähren; ist eine Begleitperson zur Erfüllung von Sicherheitsanforderungen oder zur Überwindung von Zugangsbarrieren erforderlich, wird diese kostenlos befördert. Eine Voranmeldung (üblicherweise bis 36 Stunden vorher) wird empfohlen, ist aber kein Ausschlussgrund für die Hilfeleistung selbst.",
        ),
        en=dict(
            q="What duty does the EU Bus Passenger Rights Regulation (Regulation (EU) No. 181/2011) impose regarding persons with disabilities or reduced mobility?",
            o={
                "a": "Persons with reduced mobility may generally be excluded from carriage if that serves the timetable",
                "b": "There is no special assistance duty at all; every passenger must arrange their own help",
                "c": "Such persons must be given free assistance boarding and alighting, and at designated bus terminals/stops; a companion may travel free of charge where necessary to meet safety requirements",
                "d": "Wheelchair users may only be carried on lines shorter than 50 km",
            },
            e="Regulation (EU) No. 181/2011 obliges bus operators to provide free assistance to persons with disabilities and reduced mobility when boarding and alighting and at designated terminals/stops; where a companion is necessary to meet safety requirements or overcome access barriers, that companion is carried free of charge. Advance notice (typically up to 36 hours) is recommended but is not a valid reason to withhold the assistance itself.",
        ),
    ),
    dict(
        id="bus-pbefg-08", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="VO (EU) Nr. 181/2011 Art. 17",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was sieht die EU-Fahrgastrechteverordnung vor, wenn ein Rollstuhl oder ein anderes Mobilitätshilfsmittel bei der Beförderung durch das Busunternehmen beschädigt wird?",
            o={
                "a": "Das Busunternehmen haftet grundsätzlich nicht, das Risiko trägt allein der Fahrgast",
                "b": "Der betroffene Fahrgast hat Anspruch auf Entschädigung; nach Möglichkeit ist ein vorübergehender Ersatz für das Hilfsmittel bereitzustellen",
                "c": "Eine Entschädigung ist nur bei vorsätzlicher Beschädigung durch den Fahrer möglich",
                "d": "Beschädigte Mobilitätshilfen werden ausschließlich durch die Krankenversicherung des Fahrgasts ersetzt",
            },
            e="Wird ein Rollstuhl oder ein anderes Mobilitätshilfsmittel bei der Beförderung beschädigt, sieht die VO (EU) Nr. 181/2011 einen Entschädigungsanspruch des Fahrgasts vor; soweit möglich ist ihm ein vorübergehender Ersatz zur Verfügung zu stellen, bis das eigene Hilfsmittel repariert oder ersetzt ist.",
        ),
        en=dict(
            q="What does the EU Bus Passenger Rights Regulation provide if a wheelchair or other mobility aid is damaged during carriage by the bus operator?",
            o={
                "a": "The bus operator is generally not liable; the passenger bears the risk alone",
                "b": "The affected passenger is entitled to compensation, and where possible must be given a temporary replacement for the aid",
                "c": "Compensation is only available if the driver damaged it intentionally",
                "d": "Damaged mobility aids are only replaced by the passenger's own health insurer",
            },
            e="If a wheelchair or other mobility aid is damaged during carriage, Regulation (EU) No. 181/2011 provides for a compensation claim by the passenger; where possible the passenger must be given a temporary replacement until the aid is repaired or replaced.",
        ),
    ),
    dict(
        id="bus-pbefg-09", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 BOKraft; allgemeine Deeskalationspflicht",
        points=4, high_stakes=True, correct=["b"],
        de=dict(
            q="Ein Fahrgast weigert sich, den Fahrpreis zu zahlen, und es kommt zu einer lauten Auseinandersetzung mit anderen Fahrgästen. Wie sollte sich der Busfahrer im Sinne der Sicherheit primär verhalten?",
            o={
                "a": "Sofort während der Fahrt den Streit mit eigenen Händen schlichten und dabei den Verkehr aus den Augen lassen",
                "b": "Die Fahrt sicher fortsetzen bzw. an geeigneter Stelle anhalten, deeskalierend wirken, den Streit nicht eskalieren lassen und bei Bedarf die Leitstelle oder Polizei informieren, statt den Konflikt eigenmächtig gewaltsam zu lösen",
                "c": "Den Fahrgast bei voller Fahrt aus dem fahrenden Bus drängen",
                "d": "Den Vorfall ignorieren und keinerlei Meldung machen, da Fahrpreisstreitigkeiten den Fahrer nichts angehen",
            },
            e="Die Verkehrssicherheit hat Vorrang: Der Fahrer darf sich durch einen Konflikt nicht vom Verkehrsgeschehen ablenken lassen. Richtig ist, ruhig und deeskalierend zu reagieren, notfalls an geeigneter, sicherer Stelle zu halten und die Leitstelle bzw. bei eskalierender Lage die Polizei einzuschalten - eigenmächtige körperliche Auseinandersetzungen sind zu vermeiden und bergen zusätzliche Haftungs- und Sicherheitsrisiken.",
        ),
        en=dict(
            q="A passenger refuses to pay the fare and a loud dispute breaks out with other passengers. What should the driver primarily do, with safety in mind?",
            o={
                "a": "Immediately intervene physically while driving, taking their eyes off traffic",
                "b": "Keep driving safely or stop at a suitable location, de-escalate, prevent the dispute from escalating further, and notify the control centre or police if needed, rather than resolving the conflict physically on their own",
                "c": "Push the passenger out of the moving bus",
                "d": "Ignore the incident entirely and file no report, since fare disputes are not the driver's concern",
            },
            e="Traffic safety takes priority: the driver must not let a conflict distract them from traffic. The correct response is to stay calm, de-escalate, stop at a suitable safe location if necessary, and involve the control centre or, if the situation escalates, the police - taking matters into one's own hands physically must be avoided and carries additional liability and safety risks.",
        ),
    ),
    dict(
        id="bus-pbefg-10", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 14 Abs. 2 BOKraft (Sicherheitseinrichtungen)",
        points=3, high_stakes=True, correct=["a"],
        de=dict(
            q="Was gilt nach § 14 Abs. 2 BOKraft für den Umgang der Fahrgäste mit Sicherheitseinrichtungen im Bus, etwa Notausstiegsfenstern oder Nothämmern?",
            o={
                "a": "Der Missbrauch von Sicherheitseinrichtungen ist ausdrücklich untersagt; sie dürfen nur im tatsächlichen Notfall benutzt werden",
                "b": "Fahrgäste dürfen Nothämmer jederzeit als Souvenir mitnehmen",
                "c": "Notausstiegsfenster dürfen während der Fahrt zur Belüftung geöffnet werden",
                "d": "Sicherheitseinrichtungen dürfen von Kindern zum Spielen benutzt werden, solange ein Erwachsener zusieht",
            },
            e="§ 14 Abs. 2 BOKraft verbietet den Missbrauch von Sicherheitseinrichtungen. Notausstiegsfenster, Nothämmer und Notbremseinrichtungen dienen ausschließlich der Gefahrenabwehr im echten Notfall; ihre zweckwidrige Nutzung gefährdet die Funktionsfähigkeit im Ernstfall und kann Ordnungswidrigkeiten- bzw. haftungsrechtliche Folgen haben.",
        ),
        en=dict(
            q="Under Sec. 14(2) BOKraft, what applies to how passengers may handle safety equipment on the bus, such as emergency-exit windows or emergency hammers?",
            o={
                "a": "Misusing safety equipment is expressly prohibited; it may only be used in an actual emergency",
                "b": "Passengers may take emergency hammers home as souvenirs at any time",
                "c": "Emergency-exit windows may be opened during the journey for ventilation",
                "d": "Safety equipment may be used by children for play as long as an adult is watching",
            },
            e="Sec. 14(2) BOKraft prohibits misuse of safety equipment. Emergency-exit windows, emergency hammers, and emergency braking devices are meant exclusively for hazard response in a genuine emergency; using them for other purposes can compromise their function when actually needed and can carry regulatory or liability consequences.",
        ),
    ),
    dict(
        id="bus-pbefg-11", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 15 BOKraft (Beförderung von Sachen)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Dürfen Fahrgäste nach BOKraft grundsätzlich beliebig große und schwere Gegenstände (z. B. sperrige Fahrräder oder große Kisten) im Fahrgastraum mitführen?",
            o={
                "a": "Ja, uneingeschränkt, solange ein Sitzplatz frei bleibt",
                "b": "Nein, die Mitnahme von Sachen ist im Linienbus generell vollständig verboten",
                "c": "Nein, die Mitnahme von Sachen ist nur zulässig, soweit dies ohne Gefährdung oder erhebliche Behinderung anderer Fahrgäste und ohne Beeinträchtigung der Betriebssicherheit möglich ist; das Betriebspersonal kann die Mitnahme einschränken oder ablehnen",
                "d": "Das entscheidet ausschließlich der jeweilige Fahrgast selbst",
            },
            e="Die Mitnahme von Sachen ist nach BOKraft an die Betriebssicherheit und die Rücksichtnahme auf andere Fahrgäste gebunden: Gegenstände dürfen andere nicht gefährden oder erheblich behindern und die Betriebssicherheit nicht beeinträchtigen; im Zweifel kann das Betriebspersonal die Mitnahme untersagen, etwa bei sperrigen oder gefährlichen Gegenständen im vollbesetzten Bus.",
        ),
        en=dict(
            q="Under BOKraft, may passengers generally bring items of any size and weight (e.g. bulky bicycles or large boxes) into the passenger compartment as they please?",
            o={
                "a": "Yes, without restriction as long as a seat remains free",
                "b": "No, bringing items on board a scheduled bus is completely prohibited under all circumstances",
                "c": "No, bringing items is only permitted as far as it does not endanger or significantly obstruct other passengers and does not impair operational safety; operating staff may restrict or refuse it",
                "d": "That is decided solely by each passenger themselves",
            },
            e="Under BOKraft, carrying items is tied to operational safety and consideration for other passengers: items must not endanger or significantly obstruct others and must not impair operational safety; where in doubt, operating staff may refuse carriage of an item, e.g. bulky or hazardous items on a full bus.",
        ),
    ),
    dict(
        id="bus-pbefg-12", topic="PBefG/BOKraft: Fahrgastverhalten und Sicherheit",
        topic_code="pbefg_verhalten", legal_basis="§ 22 PBefG i. V. m. Allgemeinen Beförderungsbedingungen",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Darf ein Fahrgast im Linienverkehr grundsätzlich von der Beförderung ausgeschlossen werden, wenn er offensichtlich erheblich alkoholisiert ist und andere Fahrgäste dadurch gefährdet oder erheblich belästigt?",
            o={
                "a": "Nein, die Beförderungspflicht nach § 22 PBefG gilt ausnahmslos für jeden Fahrgast",
                "b": "Ja, die Beförderungspflicht besteht nur, solange die Beförderungsbedingungen eingehalten werden; ein Fahrgast, der andere erheblich gefährdet oder stört, kann im Rahmen der Beförderungsbedingungen und des Hausrechts von der Beförderung ausgeschlossen werden",
                "c": "Ja, aber nur mit vorheriger richterlicher Genehmigung",
                "d": "Nein, Alkoholisierung ist rechtlich völlig irrelevant für die Beförderung",
            },
            e="Die Beförderungspflicht nach § 22 PBefG steht unter dem Vorbehalt, dass die Beförderungsbedingungen eingehalten werden. Gefährdet oder stört ein erheblich alkoholisierter Fahrgast andere erheblich, kann er im Rahmen der Beförderungsbedingungen und des Hausrechts des Unternehmens - vergleichbar dem Ausschluss nach § 14 Abs. 4 BOKraft - von der Beförderung ausgeschlossen werden.",
        ),
        en=dict(
            q="On a scheduled service, may a passenger generally be excluded from carriage if they are obviously significantly intoxicated and thereby endanger or seriously disturb other passengers?",
            o={
                "a": "No, the duty to carry under Sec. 22 PBefG applies to every passenger without exception",
                "b": "Yes, the duty to carry only applies as long as the conditions of carriage are complied with; a passenger who seriously endangers or disturbs others can be excluded from carriage under the conditions of carriage and the operator's house rules",
                "c": "Yes, but only with a prior court order",
                "d": "No, intoxication is legally entirely irrelevant to carriage",
            },
            e="The duty to carry under Sec. 22 PBefG is conditional on the conditions of carriage being complied with. If a significantly intoxicated passenger seriously endangers or disturbs others, they can be excluded from carriage under the conditions of carriage and the operator's house rules - comparable to exclusion under Sec. 14(4) BOKraft.",
        ),
    ),

    # =========================================================================
    # Topic 2: Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr (12)
    # =========================================================================
    dict(
        id="bus-lenkzeiten-01", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 3 Buchst. a",
        points=4, high_stakes=True, correct=["c"],
        de=dict(
            q="Welche bus-spezifische Ausnahme von den Lenk- und Ruhezeitvorschriften der EU-VO 561/2006 sieht Art. 3 Buchst. a der Verordnung vor?",
            o={
                "a": "Alle Reisebusse sind grundsätzlich von der Verordnung ausgenommen",
                "b": "Fahrzeuge mit mehr als 30 Sitzplätzen sind immer ausgenommen",
                "c": "Fahrzeuge, die im Personenverkehr im Linienverkehr eingesetzt werden, dessen Linienweg nicht mehr als 50 km beträgt, sind von der Verordnung ausgenommen",
                "d": "Busse sind nur in den Ferienmonaten ausgenommen",
            },
            e="Art. 3 Buchst. a der EU-VO 561/2006 nimmt Fahrzeuge, die für die Personenbeförderung im Linienverkehr eingesetzt werden, dessen Linienweg 50 km nicht überschreitet, ausdrücklich vom Anwendungsbereich der Verordnung aus - die sogenannte 50-km-Ausnahme für den örtlichen/regionalen Nahlinienverkehr. Für alle anderen Bus- und Reiseverkehre (z. B. Fernlinien, Gelegenheitsverkehr) gelten die allgemeinen Lenk- und Ruhezeiten unverändert.",
        ),
        en=dict(
            q="What bus-specific exemption from the EU Reg. 561/2006 driving and rest time rules does Article 3(a) of the Regulation provide?",
            o={
                "a": "All coaches are generally exempt from the Regulation",
                "b": "Vehicles with more than 30 seats are always exempt",
                "c": "Vehicles used for passenger transport on regular (scheduled) services where the route does not exceed 50 km are exempt from the Regulation",
                "d": "Buses are only exempt during the summer holiday months",
            },
            e="Article 3(a) of EU Reg. 561/2006 expressly exempts vehicles used for passenger transport on regular (scheduled) services where the route length does not exceed 50 km - the so-called 50 km exemption for local/regional scheduled bus services. All other bus and coach operations (e.g. long-distance scheduled services, occasional/charter services) remain fully subject to the general driving and rest time rules.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-02", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 3 Buchst. a; FPersG",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Ein Busfahrer fährt ausschließlich Linienverkehr innerhalb einer Stadt mit einer Linienlänge von 22 km. Gilt für ihn die EU-VO 561/2006 mit Fahrtenschreiberpflicht?",
            o={
                "a": "Ja, uneingeschränkt, da jeder Omnibus über 3,5 t immer erfasst ist",
                "b": "Nein, da der Linienweg 50 km nicht übersteigt, greift die Ausnahme nach Art. 3 Buchst. a EU-VO 561/2006 und die Verordnung ist nicht anwendbar",
                "c": "Nur an Werktagen, an Wochenenden gilt die Ausnahme nicht",
                "d": "Nur wenn der Fahrer weniger als 10 Jahre Berufserfahrung hat",
            },
            e="Da der Linienweg mit 22 km deutlich unter der 50-km-Grenze liegt, greift die Ausnahme des Art. 3 Buchst. a EU-VO 561/2006 - die Verordnung (und damit auch die grundsätzliche Fahrtenschreiberpflicht nach VO (EU) 165/2014) ist auf diesen Linienverkehr nicht anwendbar. National können dennoch andere Regelungen (z. B. Arbeitszeitgesetz, Tarifrecht) einschlägig sein.",
        ),
        en=dict(
            q="A bus driver operates exclusively on a scheduled city service with a route length of 22 km. Does EU Reg. 561/2006, including the tachograph requirement, apply to them?",
            o={
                "a": "Yes, without limitation, since every bus over 3.5 t is always covered",
                "b": "No, because the route does not exceed 50 km, the exemption under Article 3(a) EU Reg. 561/2006 applies and the Regulation does not apply",
                "c": "Only on weekdays; the exemption does not apply at weekends",
                "d": "Only if the driver has fewer than 10 years of professional experience",
            },
            e="Because the route length of 22 km is well under the 50 km threshold, the exemption under Article 3(a) EU Reg. 561/2006 applies - the Regulation (and hence the general tachograph obligation under Reg. (EU) 165/2014) does not apply to this scheduled service. Other national rules (e.g. working-time law, collective agreements) may still be relevant regardless.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-03", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="§ 18 FPersV",
        points=4, high_stakes=False, correct=["a"],
        de=dict(
            q="§ 18 FPersV enthält nationale deutsche Ausnahmen von der EU-VO 561/2006 und VO (EU) 165/2014. Welche der folgenden Aussagen zu einer dort genannten personenverkehrsbezogenen Ausnahme trifft zu?",
            o={
                "a": "Fahrzeuge mit 10 bis 17 Sitzplätzen, die ausschließlich zur nicht gewerblichen Personenbeförderung verwendet werden, sind nach § 18 FPersV von den EU-Vorschriften ausgenommen",
                "b": "§ 18 FPersV nimmt sämtliche Reisebusunternehmen generell von der EU-VO 561/2006 aus",
                "c": "§ 18 FPersV gilt nur für Fahrzeuge mit mehr als 50 Sitzplätzen",
                "d": "§ 18 FPersV betrifft ausschließlich den Güterverkehr, Personenverkehr ist dort nicht erwähnt",
            },
            e="§ 18 FPersV listet zahlreiche nationale Ausnahmetatbestände auf; darunter fallen unter anderem Fahrzeuge mit 10 bis 17 Sitzplätzen, die ausschließlich zur nicht gewerblichen Personenbeförderung eingesetzt werden. Kommerzielle Linien- oder Reisebusverkehre mit größeren Fahrzeugen fallen grundsätzlich nicht unter diese spezielle Ausnahme und unterliegen weiterhin der EU-VO 561/2006, soweit nicht die 50-km-Linienausnahme (Art. 3 Buchst. a) greift.",
        ),
        en=dict(
            q="Sec. 18 FPersV contains national German exemptions from EU Reg. 561/2006 and Reg. (EU) 165/2014. Which statement about a passenger-transport-related exemption listed there is correct?",
            o={
                "a": "Vehicles with 10 to 17 seats used exclusively for non-commercial passenger transport are exempt from the EU rules under Sec. 18 FPersV",
                "b": "Sec. 18 FPersV generally exempts all coach operators from EU Reg. 561/2006",
                "c": "Sec. 18 FPersV only applies to vehicles with more than 50 seats",
                "d": "Sec. 18 FPersV concerns only freight transport; passenger transport is not mentioned there",
            },
            e="Sec. 18 FPersV lists numerous national exemptions; these include vehicles with 10 to 17 seats used exclusively for non-commercial passenger transport. Commercial scheduled or coach services using larger vehicles are generally not covered by this specific exemption and remain subject to EU Reg. 561/2006, unless the 50 km scheduled-service exemption (Article 3(a)) applies.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-04", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 6",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Ein Reisebusfahrer im grenzüberschreitenden Fernlinienverkehr (kein Ausnahmefall) unterliegt der EU-VO 561/2006. Wie lange darf die tägliche Lenkzeit höchstens sein, und wie oft pro Woche darf sie ausnahmsweise verlängert werden?",
            o={
                "a": "Höchstens 8 Stunden täglich, niemals verlängerbar",
                "b": "Höchstens 9 Stunden täglich, zweimal pro Woche verlängerbar auf 10 Stunden",
                "c": "Höchstens 12 Stunden täglich, beliebig oft verlängerbar",
                "d": "Es gibt keine tägliche Höchstlenkzeit, nur eine wöchentliche",
            },
            e="Nach Art. 6 EU-VO 561/2006 beträgt die tägliche Lenkzeit grundsätzlich höchstens 9 Stunden; sie darf höchstens zweimal in der Woche auf bis zu 10 Stunden verlängert werden. Diese Grundregel gilt für Busfahrer im Fernlinien- oder Gelegenheitsverkehr genauso wie für Lkw-Fahrer, sofern keine bus-spezifische Ausnahme (z. B. 50-km-Linienausnahme) greift.",
        ),
        en=dict(
            q="A coach driver on a cross-border long-distance scheduled service (no exemption applies) is subject to EU Reg. 561/2006. What is the maximum daily driving time, and how often per week may it exceptionally be extended?",
            o={
                "a": "A maximum of 8 hours per day, never extendable",
                "b": "A maximum of 9 hours per day, extendable to 10 hours up to twice a week",
                "c": "A maximum of 12 hours per day, extendable as often as needed",
                "d": "There is no daily maximum driving time, only a weekly one",
            },
            e="Under Article 6 of EU Reg. 561/2006, daily driving time is generally limited to a maximum of 9 hours; it may be extended to up to 10 hours on no more than two days per week. This baseline rule applies to coach drivers on long-distance or occasional services just as it does to lorry drivers, unless a bus-specific exemption (e.g. the 50 km scheduled-service exemption) applies.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-05", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 7",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Nach spätestens 4,5 Stunden Lenkzeit muss ein Busfahrer im Fernlinien- oder Reiseverkehr (ohne Ausnahme) eine Fahrtunterbrechung einlegen. Wie lange muss diese mindestens sein, wenn sie nicht aufgeteilt wird?",
            o={
                "a": "Mindestens 45 zusammenhängende Minuten, sofern keine Ruhezeit eingelegt wird",
                "b": "Mindestens 10 Minuten",
                "c": "Mindestens 2 Stunden",
                "d": "Eine Unterbrechung ist bei Busfahrern gesetzlich nicht vorgesehen",
            },
            e="Nach Art. 7 EU-VO 561/2006 muss nach spätestens 4,5 Stunden Lenkzeit eine Fahrtunterbrechung von mindestens 45 zusammenhängenden Minuten erfolgen, sofern nicht bereits eine Ruhezeit angetreten wird. Alternativ kann diese Pause in eine erste Teilpause von mindestens 15 Minuten und eine zweite von mindestens 30 Minuten aufgeteilt werden, die jeweils in die Lenkzeit eingelegt werden.",
        ),
        en=dict(
            q="After at most 4.5 hours of driving, a coach driver on a long-distance or occasional service (no exemption) must take a break. If it is not split, how long must this break be at minimum?",
            o={
                "a": "At least 45 consecutive minutes, unless a rest period is taken instead",
                "b": "At least 10 minutes",
                "c": "At least 2 hours",
                "d": "The law does not require a break for coach drivers",
            },
            e="Under Article 7 of EU Reg. 561/2006, after at most 4.5 hours of driving a break of at least 45 consecutive minutes must be taken, unless a rest period is already being taken. Alternatively, this break can be split into a first part of at least 15 minutes and a second part of at least 30 minutes, each inserted into the driving time.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-06", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 8",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Was gilt für die regelmäßige tägliche Ruhezeit eines Busfahrers im nicht ausgenommenen Reiseverkehr grundsätzlich?",
            o={
                "a": "Sie muss mindestens 6 Stunden betragen",
                "b": "Es gibt keine tägliche Ruhezeit, nur eine wöchentliche",
                "c": "Sie muss mindestens 11 zusammenhängende Stunden innerhalb von 24 Stunden nach Ende der letzten Ruhezeit betragen (reduzierbar auf mindestens 9 Stunden an bis zu drei Tagen pro Woche)",
                "d": "Sie muss immer genau 8 Stunden betragen und darf nie verkürzt werden",
            },
            e="Nach Art. 8 EU-VO 561/2006 beträgt die regelmäßige tägliche Ruhezeit mindestens 11 zusammenhängende Stunden innerhalb von 24 Stunden nach dem Ende der vorherigen Ruhezeit. Sie kann auf mindestens 9 zusammenhängende Stunden reduziert werden, jedoch höchstens dreimal zwischen zwei wöchentlichen Ruhezeiten.",
        ),
        en=dict(
            q="What generally applies to the regular daily rest period of a coach driver on a non-exempt service?",
            o={
                "a": "It must be at least 6 hours",
                "b": "There is no daily rest period, only a weekly one",
                "c": "It must be at least 11 consecutive hours within 24 hours of the end of the previous rest period (reducible to at least 9 hours on up to three days per week)",
                "d": "It must always be exactly 8 hours and can never be shortened",
            },
            e="Under Article 8 of EU Reg. 561/2006, the regular daily rest period must be at least 11 consecutive hours within 24 hours of the end of the previous rest period. It can be reduced to at least 9 consecutive hours, but no more than three times between two weekly rest periods.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-07", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 8 Abs. 6a (Gelegenheitsverkehr, Sonderregel)",
        points=4, high_stakes=False, correct=["b"],
        de=dict(
            q="Welche bus-spezifische Sonderregel enthält die EU-VO 561/2006 für die wöchentliche Ruhezeit bei einer einzelnen internationalen Fahrt im gelegentlichen Personenverkehr (z. B. mehrtägige Reisebus-Rundreise)?",
            o={
                "a": "Es gibt für den Gelegenheitsverkehr keinerlei Sonderregeln, es gelten stets exakt dieselben Fristen wie im Güterfernverkehr",
                "b": "Für eine einzelne Fahrt im internationalen gelegentlichen Personenverkehr kann die wöchentliche Ruhezeit unter bestimmten Voraussetzungen um bis zu 12 aufeinanderfolgende 24-Stunden-Zeiträume aufgeschoben werden",
                "c": "Reisebusfahrer im Gelegenheitsverkehr müssen niemals eine wöchentliche Ruhezeit einlegen",
                "d": "Die Sonderregel gilt nur für Fahrten innerhalb eines einzigen Bundeslandes",
            },
            e="Die EU-VO 561/2006 sieht für Fahrer, die eine einzelne Fahrt im internationalen gelegentlichen Personenverkehr durchführen, eine Sonderregel vor: Unter bestimmten Voraussetzungen kann die wöchentliche Ruhezeit um bis zu 12 aufeinanderfolgende 24-Stunden-Zeiträume nach der vorangegangenen regelmäßigen wöchentlichen Ruhezeit aufgeschoben werden - eine Erleichterung, die die Besonderheiten mehrtägiger Reisebus-Rundfahrten (z. B. Kreuzfahrt- oder Ausflugsfahrten) berücksichtigt und im Güterverkehr keine Entsprechung hat.",
        ),
        en=dict(
            q="What bus-specific special rule does EU Reg. 561/2006 provide for the weekly rest period on a single international trip in occasional passenger transport (e.g. a multi-day coach tour)?",
            o={
                "a": "There are no special rules for occasional passenger transport at all; exactly the same deadlines as in long-distance freight transport always apply",
                "b": "For a single international occasional passenger transport trip, the weekly rest period can, under certain conditions, be postponed by up to 12 consecutive 24-hour periods",
                "c": "Coach drivers on occasional services never have to take a weekly rest period",
                "d": "The special rule only applies to trips within a single federal state",
            },
            e="EU Reg. 561/2006 provides a special rule for drivers carrying out a single international occasional passenger transport trip: under certain conditions the weekly rest period can be postponed by up to 12 consecutive 24-hour periods following the previous regular weekly rest period - an accommodation for the particulars of multi-day coach tours (e.g. cruise-connection or excursion trips) that has no equivalent in freight transport.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-08", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="VO (EU) Nr. 165/2014; EU-VO 561/2006 Art. 3 Buchst. a",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Muss ein Bus, der ausschließlich im Linienverkehr mit einer Streckenlänge von unter 50 km eingesetzt wird, mit einem Fahrtenschreiber gemäß VO (EU) Nr. 165/2014 ausgestattet und dieser genutzt werden?",
            o={
                "a": "Ja, ausnahmslos für jeden Omnibus über 3,5 t zulässige Gesamtmasse",
                "b": "Ja, aber nur wenn der Bus mehr als 30 Sitzplätze hat",
                "c": "Grundsätzlich nicht verpflichtend aus VO (EU) 165/2014, da bei Einsatz ausschließlich auf einer solchen Linie die Ausnahme nach Art. 3 Buchst. a EU-VO 561/2006 greift und damit auch die Fahrtenschreiberpflicht entfällt",
                "d": "Nur an Sonn- und Feiertagen erforderlich",
            },
            e="Da die Fahrtenschreiberpflicht der VO (EU) 165/2014 an die Anwendbarkeit der EU-VO 561/2006 anknüpft, entfällt sie für Fahrzeuge, die ausschließlich im Rahmen der 50-km-Linienausnahme nach Art. 3 Buchst. a EU-VO 561/2006 eingesetzt werden. Wird derselbe Bus jedoch auch auf längeren Linien oder im Gelegenheitsverkehr eingesetzt, greifen die allgemeinen Vorschriften einschließlich Fahrtenschreiberpflicht für diese Einsätze.",
        ),
        en=dict(
            q="Must a bus used exclusively on a scheduled service with a route length under 50 km be fitted with, and use, a tachograph under Reg. (EU) No. 165/2014?",
            o={
                "a": "Yes, without exception for every bus with a permissible gross weight over 3.5 t",
                "b": "Yes, but only if the bus has more than 30 seats",
                "c": "Generally not required under Reg. (EU) 165/2014, because when used exclusively on such a service the exemption under Article 3(a) EU Reg. 561/2006 applies and the tachograph requirement falls away with it",
                "d": "Only required on Sundays and public holidays",
            },
            e="Because the tachograph requirement under Reg. (EU) 165/2014 is tied to the applicability of EU Reg. 561/2006, it does not apply to vehicles used exclusively within the 50 km scheduled-service exemption under Article 3(a) EU Reg. 561/2006. If the same bus is also used on longer routes or for occasional services, the general rules including the tachograph requirement apply to those uses.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-09", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="§ 21a Abs. 4 ArbZG; EU-VO 561/2006 Art. 4",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was versteht die EU-VO 561/2006 unter 'Fahrtunterbrechung' (im Gegensatz zu Ruhezeit oder anderer Arbeit)?",
            o={
                "a": "Jede Tätigkeit, bei der der Fahrer weiterhin verantwortlich am Steuer bleibt",
                "b": "Einen Zeitraum, in dem der Fahrer keine Fahrtätigkeit ausübt und über den er frei verfügen kann, insbesondere um sich zu erholen",
                "c": "Die Zeit für das Reinigen des Busses während der Fahrgastpause",
                "d": "Ausschließlich die Zeit, die für Ticketkontrollen verwendet wird",
            },
            e="Art. 4 Buchst. d EU-VO 561/2006 definiert die Fahrtunterbrechung als einen Zeitraum, in dem der Fahrer keine Fahrtätigkeit ausübt und der ausschließlich zur Erholung dient - der Fahrer kann über diese Zeit frei verfügen. Andere Tätigkeiten wie Fahrgastbetreuung, Reinigung oder Beladung zählen in der Regel als 'andere Arbeit' und nicht als Fahrtunterbrechung.",
        ),
        en=dict(
            q="What does EU Reg. 561/2006 mean by a 'break' (as distinct from rest or other work)?",
            o={
                "a": "Any activity during which the driver remains responsible at the wheel",
                "b": "A period during which the driver may not carry out any driving activity and which is used exclusively for recreation, and over which they may freely dispose",
                "c": "The time spent cleaning the bus while passengers are on a break",
                "d": "Exclusively the time used for ticket checks",
            },
            e="Article 4(d) EU Reg. 561/2006 defines a 'break' as a period during which a driver may not carry out any driving or other work and which is used exclusively for recreation - the driver may freely dispose of this time. Other activities such as assisting passengers, cleaning, or loading generally count as 'other work', not as a break.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-10", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 6 Abs. 3",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Wie viele Stunden darf ein Busfahrer im Fernlinien- oder Reiseverkehr (ohne Ausnahme) höchstens innerhalb von zwei aufeinanderfolgenden Wochen lenken?",
            o={
                "a": "Höchstens 45 Stunden",
                "b": "Höchstens 90 Stunden",
                "c": "Höchstens 120 Stunden",
                "d": "Es gibt keine Zweiwochengrenze, nur eine tägliche",
            },
            e="Art. 6 Abs. 3 EU-VO 561/2006 begrenzt die Lenkzeit innerhalb von zwei aufeinanderfolgenden Wochen auf höchstens 90 Stunden. Diese Grenze gilt zusätzlich zur täglichen (9/10 Stunden) und wöchentlichen (56 Stunden) Höchstlenkzeit und soll eine übermäßige Kumulierung der Lenkzeit über mehrere Wochen verhindern.",
        ),
        en=dict(
            q="What is the maximum driving time a coach driver on a long-distance or occasional service (no exemption) may accumulate within any two consecutive weeks?",
            o={
                "a": "A maximum of 45 hours",
                "b": "A maximum of 90 hours",
                "c": "A maximum of 120 hours",
                "d": "There is no two-week limit, only a daily one",
            },
            e="Article 6(3) EU Reg. 561/2006 limits driving time within any two consecutive weeks to a maximum of 90 hours. This limit applies in addition to the daily (9/10 hours) and weekly (56 hours) maximum driving times and is meant to prevent excessive accumulation of driving time over several weeks.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-11", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 Art. 7 Unterabs. 2",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Bei einem Bus mit mehreren Fahrern (Doppelbesetzung) auf einer langen Reisebusfahrt: Darf die vorgeschriebene Fahrtunterbrechung eines Fahrers eingehalten werden, während der zweite Fahrer weiterfährt?",
            o={
                "a": "Ja, bei Mehrfahrerbesatzung kann die Fahrtunterbrechung eines Fahrers während der Fahrt eingelegt werden, solange der ruhende Fahrer neben dem fahrenden Fahrer keine Unterstützung leistet",
                "b": "Nein, bei Doppelbesetzung muss der Bus für jede Pause vollständig anhalten",
                "c": "Nein, Mehrfahrerbesatzung ist im Busverkehr gesetzlich verboten",
                "d": "Ja, aber nur wenn beide Fahrer gleichzeitig am Steuer sitzen",
            },
            e="Art. 7 Unterabs. 2 EU-VO 561/2006 erlaubt es bei Mehrfahrerbesatzung, dass ein Fahrer seine Fahrtunterbrechung nimmt, während ein anderer Fahrer das Fahrzeug lenkt - vorausgesetzt, der ruhende Fahrer leistet dem Fahrer keinerlei Unterstützung. Dies ist im Reisebusverkehr auf langen Strecken eine praktisch bedeutsame Regelung.",
        ),
        en=dict(
            q="On a coach with multiple drivers (multi-manning) on a long trip, can one driver's required break be taken while the other driver continues to drive?",
            o={
                "a": "Yes, with multi-manning, one driver's break can be taken while the vehicle is being driven, as long as the resting driver provides no assistance to the driver at the wheel",
                "b": "No, with multi-manning the coach must come to a complete stop for every break",
                "c": "No, multi-manning is legally prohibited for coach services",
                "d": "Yes, but only if both drivers sit at the controls at the same time",
            },
            e="Article 7(2) EU Reg. 561/2006 permits, in the case of multi-manning, that one driver takes a break while another driver drives the vehicle - provided that the resting driver does not assist the driver in any way. This is a practically significant rule for long-distance coach travel.",
        ),
    ),
    dict(
        id="bus-lenkzeiten-12", topic="Lenk- und Ruhezeiten sowie Fahrtenschreiber im Busverkehr",
        topic_code="lenkzeiten_bus", legal_basis="EU-VO 561/2006 (Sinn und Zweck); FPersG",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Warum sind die Lenk- und Ruhezeitvorschriften im Reisebusverkehr besonders sicherheitsrelevant?",
            o={
                "a": "Weil Busse grundsätzlich langsamer fahren als andere Fahrzeuge und deshalb kein Unfallrisiko besteht",
                "b": "Weil sie ausschließlich die Rentabilität der Busunternehmen sichern sollen",
                "c": "Weil ein übermüdeter Fahrer eines vollbesetzten Reisebusses bei einem Unfall potenziell eine sehr hohe Zahl an Fahrgästen gefährdet, sodass ausreichende Erholung besonders wichtig ist",
                "d": "Weil Reisebusse keine Bremsen benötigen",
            },
            e="Anders als bei Pkw kann ein übermüdeter Reisebusfahrer bei einem Unfall eine sehr große Zahl an Fahrgästen gleichzeitig gefährden. Die Lenk- und Ruhezeitvorschriften der EU-VO 561/2006 sollen sicherstellen, dass Busfahrer ausreichend erholt sind, um diese besondere Verantwortung sicher wahrzunehmen.",
        ),
        en=dict(
            q="Why are the driving and rest time rules particularly safety-relevant in coach transport?",
            o={
                "a": "Because buses generally drive more slowly than other vehicles, so there is no accident risk",
                "b": "Because they are meant solely to protect the profitability of bus companies",
                "c": "Because a fatigued driver of a fully occupied coach potentially endangers a very large number of passengers if an accident occurs, making adequate rest especially important",
                "d": "Because coaches do not require brakes",
            },
            e="Unlike a passenger car, a fatigued coach driver can potentially endanger a very large number of passengers at once if an accident occurs. The driving and rest time rules of EU Reg. 561/2006 are meant to ensure coach drivers are sufficiently rested to safely carry this particular responsibility.",
        ),
    ),

    # =========================================================================
    # Topic 3: Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen (12)
    # =========================================================================
    dict(
        id="bus-technik-01", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeine Fahrphysik/Fahrzeugtechnik (Grundwissen Gelenkbus)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Was ist eine besondere Gefahr beim Kurvenfahren mit einem Gelenkbus (Gelenkomnibus)?",
            o={
                "a": "Gelenkbusse können grundsätzlich nicht abbiegen",
                "b": "Durch die Fahrzeuggelenkung kann der Nachläufer beim Abbiegen einen deutlich engeren oder weiteren Radius als die Zugmaschine beschreiben ('Ausschwenken' bzw. 'Einschneiden'), was andere Verkehrsteilnehmer im Kurveninnen- oder -außenbereich gefährden kann",
                "c": "Der Nachläufer bewegt sich exakt auf derselben Spur wie das Zugteil, es gibt keinerlei Unterschied",
                "d": "Gelenkbusse haben grundsätzlich keine Heckpartie",
            },
            e="Beim Gelenkbus folgt der Nachläufer dem vorderen Fahrzeugteil über das Gelenk und kann je nach Lenkwinkel und Geschwindigkeit deutlich von dessen Spur abweichen - er kann beim Abbiegen enger einschneiden (Innenradius) oder weiter ausschwenken (Außenradius) als die Zugmaschine. Fahrer müssen dies beim Einschätzen von Kurven, insbesondere an Kreuzungen mit Fußgängern und Radfahrern, besonders berücksichtigen.",
        ),
        en=dict(
            q="What is a particular hazard when cornering with an articulated bus (bendy bus)?",
            o={
                "a": "Articulated buses generally cannot turn at all",
                "b": "Because of the articulation joint, the rear section can trace a noticeably tighter or wider radius than the front section when turning (cutting in or swinging out), which can endanger other road users on the inside or outside of the curve",
                "c": "The rear section moves exactly along the same track as the front section, with no difference whatsoever",
                "d": "Articulated buses generally have no rear section",
            },
            e="On an articulated bus, the rear section follows the front section via the articulation joint and, depending on steering angle and speed, can deviate noticeably from its path - it can cut in tighter (inner radius) or swing out wider (outer radius) than the front section when turning. Drivers must account for this particularly when judging turns, especially at intersections with pedestrians and cyclists.",
        ),
    ),
    dict(
        id="bus-technik-02", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnik-/Sicherheitswissen Omnibus",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Warum ist die systematische Kontrolle sämtlicher Spiegel (Weitwinkel-, Rampen-, Frontspiegel usw.) bei einem Kraftomnibus vor jeder Fahrt besonders wichtig?",
            o={
                "a": "Weil Busse grundsätzlich keine toten Winkel haben und die Spiegel nur der Optik dienen",
                "b": "Weil Spiegel bei Bussen gesetzlich verboten sind und stattdessen nur Kameras genutzt werden dürfen",
                "c": "Weil ein Kraftomnibus aufgrund seiner Länge, Höhe und Breite erheblich größere und mehr tote Winkel als ein Pkw hat, insbesondere im Nahbereich vor der Front, seitlich an der Einstiegstür und im Heckbereich, in denen sich Fußgänger, Radfahrer oder Kinder befinden können",
                "d": "Weil ausschließlich der Innenspiegel für die Fahrgastbeobachtung benötigt wird",
            },
            e="Die Abmessungen eines Kraftomnibusses (Länge, Höhe, Breite) erzeugen deutlich größere tote Winkel als bei einem Pkw - besonders unmittelbar vor der Fahrzeugfront, im Bereich der Einstiegstür sowie am Fahrzeugheck bei Gelenkbussen. Diese Bereiche müssen vor dem Anfahren und beim Rangieren systematisch mit allen vorhandenen Spiegeln (und ggf. Kamerasystemen) kontrolliert werden, um Fußgänger, Radfahrer und insbesondere Kinder nicht zu übersehen.",
        ),
        en=dict(
            q="Why is systematically checking all mirrors (wide-angle, kerb/ramp, front mirrors, etc.) on a bus before every journey especially important?",
            o={
                "a": "Because buses have no blind spots at all and the mirrors serve a purely cosmetic purpose",
                "b": "Because mirrors are legally prohibited on buses and only cameras may be used instead",
                "c": "Because a bus, due to its length, height, and width, has significantly larger and more blind spots than a car, especially directly in front of the vehicle, alongside the entrance door, and at the rear, where pedestrians, cyclists, or children may be present",
                "d": "Because only the interior mirror is needed to observe passengers",
            },
            e="A bus's dimensions (length, height, width) create significantly larger blind spots than a car - particularly directly in front of the vehicle, near the entrance door, and at the rear on articulated buses. These areas must be systematically checked with all available mirrors (and any camera systems) before moving off and while manoeuvring, so as not to overlook pedestrians, cyclists, and especially children.",
        ),
    ),
    dict(
        id="bus-technik-03", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Kneeling-System)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was bewirkt das sogenannte 'Kneeling'-System (Absenksystem) an modernen Niederflurbussen?",
            o={
                "a": "Es senkt ausschließlich den hinteren Teil des Busses ab, um Gepäck leichter zu verladen",
                "b": "Es senkt die Karosserie an der Einstiegsseite pneumatisch ab, um den Einstiegsspalt zu verringern und den Ein- und Ausstieg für Personen mit Gehbehinderung, ältere Fahrgäste, Kinderwagen oder Rollstuhlnutzer zu erleichtern",
                "c": "Es hebt den Bus während der Fahrt automatisch an, um die Bodenfreiheit zu erhöhen",
                "d": "Es dient ausschließlich der Kraftstoffeinsparung im Stand",
            },
            e="Beim Kneeling senkt der Fahrer über die Luftfederung gezielt die Karosserieseite an der Einstiegstür ab, um den Höhenunterschied zwischen Bordstein bzw. Fahrbahn und Einstieg zu verringern. Das erleichtert den barrierearmen Einstieg für mobilitätseingeschränkte Fahrgäste, ältere Menschen, Personen mit Kinderwagen und ist ein wichtiger Baustein der Barrierefreiheit im ÖPNV.",
        ),
        en=dict(
            q="What does the 'kneeling' (lowering) system on modern low-floor buses do?",
            o={
                "a": "It lowers only the rear section of the bus to make loading luggage easier",
                "b": "It pneumatically lowers the body on the boarding side to reduce the step gap and make boarding and alighting easier for people with reduced mobility, elderly passengers, prams, or wheelchair users",
                "c": "It automatically raises the bus while driving to increase ground clearance",
                "d": "It exists solely to save fuel while the bus is stationary",
            },
            e="With kneeling, the driver uses the air suspension to selectively lower the body on the side with the entrance door, reducing the height difference between the kerb or road surface and the entrance. This makes low-barrier boarding easier for passengers with reduced mobility, elderly people, and those with prams, and is an important accessibility feature in public transport.",
        ),
    ),
    dict(
        id="bus-technik-04", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnik-/Fahrdynamikwissen",
        points=4, high_stakes=True, correct=["a"],
        de=dict(
            q="Wie wirkt sich der hohe Schwerpunkt eines Kraftomnibusses, insbesondere im vollbesetzten oder als Doppeldecker ausgeführten Zustand, auf das Fahrverhalten in Kurven aus?",
            o={
                "a": "Ein hoher Schwerpunkt erhöht die Kippgefahr in schnell gefahrenen Kurven deutlich, weshalb Kurven mit angepasster, reduzierter Geschwindigkeit gefahren werden müssen",
                "b": "Der Schwerpunkt hat keinerlei Einfluss auf das Kurvenverhalten von Bussen",
                "c": "Ein hoher Schwerpunkt verringert grundsätzlich die Kippgefahr, weil das Fahrzeug dadurch stabiler wird",
                "d": "Der Schwerpunkt ist bei Doppeldeckerbussen niedriger als bei einstöckigen Bussen",
            },
            e="Kraftomnibusse, besonders Doppeldeckerbusse oder voll besetzte Fahrzeuge mit stehenden Fahrgästen im Oberdeck bzw. hoch liegender Fahrgastebene, haben einen vergleichsweise hohen Schwerpunkt. Das erhöht in schnell gefahrenen Kurven die Kippgefahr durch die einwirkende Fliehkraft deutlich. Kurven müssen deshalb mit angepasster, in der Regel reduzierter Geschwindigkeit gefahren werden, um ausreichende Fahrstabilität zu gewährleisten.",
        ),
        en=dict(
            q="How does a bus's high centre of gravity, particularly when fully occupied or configured as a double-decker, affect cornering behaviour?",
            o={
                "a": "A high centre of gravity significantly increases the risk of tipping over in fast-taken curves, which is why curves must be taken at an adjusted, reduced speed",
                "b": "The centre of gravity has no effect whatsoever on a bus's cornering behaviour",
                "c": "A high centre of gravity generally reduces the risk of tipping over because it makes the vehicle more stable",
                "d": "Double-decker buses have a lower centre of gravity than single-deck buses",
            },
            e="Buses, especially double-decker buses or fully occupied vehicles with standing passengers on an upper deck or elevated passenger level, have a comparatively high centre of gravity. This significantly increases the risk of tipping over in fast-taken curves due to the centrifugal force involved. Curves must therefore be taken at an adjusted, generally reduced speed to maintain adequate stability.",
        ),
    ),
    dict(
        id="bus-technik-05", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="§ 6 FeV (Klasseneinteilung D1/D)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Wie unterscheiden sich die Fahrerlaubnisklassen D1 und D im Wesentlichen hinsichtlich der Fahrgastkapazität und Fahrzeuglänge?",
            o={
                "a": "D1 erlaubt mehr Fahrgäste als D",
                "b": "Beide Klassen sind identisch definiert, es gibt keinen Unterschied",
                "c": "D1 umfasst Kraftfahrzeuge zur Beförderung von nicht mehr als 16 Personen außer dem Fahrzeugführer mit einer Länge von höchstens 8 m; D umfasst Kraftfahrzeuge zur Beförderung von mehr als acht Personen ohne diese Längenbegrenzung",
                "d": "D1 gilt nur für Fahrzeuge ohne Fahrgäste",
            },
            e="Nach § 6 FeV ist Klasse D1 auf Kraftfahrzeuge beschränkt, die zur Beförderung von nicht mehr als 16 Personen außer dem Fahrzeugführer bestimmt sind und höchstens 8 m lang sind - eine Zwischenklasse für kleinere Busse (Midibusse). Klasse D umfasst demgegenüber Kraftfahrzeuge zur Beförderung von mehr als acht Personen außer dem Fahrzeugführer ohne diese Längenbegrenzung, also auch große Linien- und Reisebusse.",
        ),
        en=dict(
            q="How do driving licence classes D1 and D essentially differ in terms of passenger capacity and vehicle length?",
            o={
                "a": "D1 permits more passengers than D",
                "b": "Both classes are defined identically; there is no difference",
                "c": "D1 covers motor vehicles for carrying no more than 16 persons other than the driver, with a length of no more than 8 m; D covers motor vehicles for carrying more than eight persons other than the driver without this length restriction",
                "d": "D1 applies only to vehicles carrying no passengers",
            },
            e="Under Sec. 6 FeV, Class D1 is limited to motor vehicles designed to carry no more than 16 persons other than the driver and no longer than 8 m - an intermediate class for smaller buses (midibuses). Class D, by contrast, covers motor vehicles for carrying more than eight persons other than the driver with no such length restriction, including large scheduled-service and coach buses.",
        ),
    ),
    dict(
        id="bus-technik-06", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Überhang/Ausschwenken)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Was ist beim Rechtsabbiegen mit einem langen Linienbus in Bezug auf den vorderen Überhang und das Fahrzeugheck besonders zu beachten?",
            o={
                "a": "Ein langer Bus verhält sich beim Abbiegen identisch wie ein Pkw, es gibt keine Besonderheiten",
                "b": "Der vordere Fahrzeugteil kann beim Einlenken zunächst nach links ausschwenken (Vorderüberhang), während das Heck weiter innen die Kurve schneidet - Radfahrer und Fußgänger im rechten toten Winkel und im Bereich des Vorderüberhangs sind besonders gefährdet",
                "c": "Das Heck eines Linienbusses kann sich beim Rechtsabbiegen niemals in den Gegenverkehr bewegen",
                "d": "Es besteht keine Gefahr für Radfahrer, da Busse grundsätzlich langsamer abbiegen als Fahrräder fahren",
            },
            e="Wegen des Radstands und des vorderen Überhangs schwenkt der vordere Busteil beim Einleiten eines Rechtsabbiegevorgangs zunächst leicht nach links aus, bevor das Fahrzeug die Kurve nimmt, während das Heck enger schneidet. In Kombination mit dem toten Winkel rechts neben und vor dem Bus entsteht eine erhebliche Gefahr für Radfahrer und Fußgänger, die sich in diesem Bereich befinden - eine sorgfältige Beobachtung vor und während des Abbiegevorgangs ist unerlässlich.",
        ),
        en=dict(
            q="What must be considered when a long scheduled-service bus turns right, regarding the front overhang and the rear of the vehicle?",
            o={
                "a": "A long bus behaves identically to a car when turning; there are no particular considerations",
                "b": "The front section can initially swing left as the driver turns in (front overhang), while the rear cuts the curve more tightly on the inside - cyclists and pedestrians in the right-hand blind spot and in the front overhang area are particularly at risk",
                "c": "The rear of a scheduled-service bus can never move into oncoming traffic",
                "d": "There is no danger to cyclists, since buses generally turn more slowly than bicycles travel",
            },
            e="Because of the wheelbase and front overhang, the front of the bus initially swings slightly to the left as a right turn is initiated, before the vehicle takes the curve, while the rear cuts the corner more tightly. Combined with the blind spot to the right and in front of the bus, this creates a significant hazard for cyclists and pedestrians in that area - careful observation before and during the turning manoeuvre is essential.",
        ),
    ),
    dict(
        id="bus-technik-07", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Höhe/lichte Höhe)",
        points=2, high_stakes=True, correct=["b"],
        de=dict(
            q="Warum muss ein Busfahrer vor Fahrtantritt insbesondere bei unbekannten Strecken die Fahrzeughöhe sowie Höhenbeschränkungen (z. B. Brücken, Unterführungen, Parkhäuser) besonders im Blick behalten?",
            o={
                "a": "Weil alle Straßen in Deutschland für beliebig hohe Fahrzeuge freigegeben sind",
                "b": "Weil ein Kraftomnibus deutlich höher ist als ein Pkw und bei Kollision mit einer zu niedrigen Brücke oder Unterführung das Fahrzeugdach, die Fahrgäste und die Bauwerksstruktur erheblich gefährdet werden können",
                "c": "Weil die Fahrzeughöhe keinen Einfluss auf die Verkehrssicherheit hat",
                "d": "Weil Busse grundsätzlich niedriger sind als alle anderen Nutzfahrzeuge",
            },
            e="Aufgrund ihrer beträchtlichen Bauhöhe (bei Doppeldeckern noch ausgeprägter) besteht bei Bussen ein reales Risiko einer Kollision mit zu niedrigen Brücken, Unterführungen oder Einfahrten. Solche Kollisionen können zu schweren Fahrgastverletzungen, Strukturschäden am Fahrzeug und am Bauwerk führen. Fahrer müssen die Streckenführung und bekannte Höhenbeschränkungen vorab prüfen, insbesondere bei Umleitungen oder unbekannten Routen.",
        ),
        en=dict(
            q="Why must a bus driver, especially on unfamiliar routes, pay particular attention to the vehicle's height and height restrictions (e.g. bridges, underpasses, car parks) before setting off?",
            o={
                "a": "Because all roads in Germany are cleared for vehicles of any height",
                "b": "Because a bus is significantly taller than a car, and a collision with a bridge or underpass that is too low can seriously endanger the roof, the passengers, and the structure of the building",
                "c": "Because vehicle height has no bearing on traffic safety",
                "d": "Because buses are generally lower than all other commercial vehicles",
            },
            e="Because of their considerable height (even more pronounced on double-deckers), buses face a real risk of colliding with bridges, underpasses, or entrances that are too low. Such collisions can cause serious passenger injuries and structural damage to both the vehicle and the structure. Drivers must check the planned route and any known height restrictions in advance, particularly on diversions or unfamiliar routes.",
        ),
    ),
    dict(
        id="bus-technik-08", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Bremsverhalten)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Wie wirkt sich eine hohe Fahrgastauslastung (vollbesetzter Bus inklusive stehender Fahrgäste) auf den Bremsweg und das Fahrverhalten aus?",
            o={
                "a": "Ein höheres Gesamtgewicht durch mehr Fahrgäste verlängert tendenziell den Bremsweg und verändert das Fahrverhalten, weshalb ein größerer Sicherheitsabstand und vorausschauendes, ruckfreies Bremsen besonders wichtig sind",
                "b": "Das Gewicht der Fahrgäste hat keinerlei Einfluss auf den Bremsweg eines modernen Busses",
                "c": "Ein voller Bus bremst grundsätzlich kürzer als ein leerer Bus",
                "d": "Nur das Leergewicht des Busses ist für den Bremsweg relevant, die Fahrgäste zählen nicht mit",
            },
            e="Mit zunehmender Fahrgastzahl steigt das Gesamtgewicht des Fahrzeugs, was den Bremsweg tendenziell verlängert und das Fahrverhalten (z. B. Kurvenverhalten, Bremsstabilität) beeinflusst. Zusätzlich sind bei stehenden Fahrgästen abrupte Brems- oder Ausweichmanöver besonders gefährlich, da sie stürzen können. Vorausschauendes Fahren, ausreichender Sicherheitsabstand und ruckfreies, dosiertes Bremsen sind deshalb besonders wichtig.",
        ),
        en=dict(
            q="How does a high passenger load (a fully occupied bus including standing passengers) affect braking distance and handling?",
            o={
                "a": "The additional weight from more passengers tends to lengthen braking distance and change handling, which is why a larger safety distance and smooth, anticipatory braking are especially important",
                "b": "The weight of the passengers has no effect whatsoever on a modern bus's braking distance",
                "c": "A full bus generally has a shorter braking distance than an empty bus",
                "d": "Only the bus's unladen weight is relevant for braking distance; passengers do not count",
            },
            e="As the number of passengers increases, so does the vehicle's total weight, which tends to lengthen braking distance and affects handling (e.g. cornering behaviour, braking stability). In addition, abrupt braking or evasive manoeuvres are especially dangerous for standing passengers, who can fall. Anticipatory driving, an adequate safety distance, and smooth, well-metered braking are therefore especially important.",
        ),
    ),
    dict(
        id="bus-technik-09", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Rangieren/Einweiser)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Was ist beim Rückwärtsrangieren eines langen Kraftomnibusses, etwa auf dem Betriebshof oder an einer engen Endhaltestelle, empfehlenswert?",
			o={
                "a": "Grundsätzlich mit hoher Geschwindigkeit rangieren, um Zeit zu sparen",
                "b": "Wenn möglich einen Einweiser hinzuziehen, alle verfügbaren Spiegel und Kamerasysteme systematisch nutzen und in sehr geringer Geschwindigkeit rangieren, um die großen toten Winkel im Heckbereich zu kompensieren",
                "c": "Auf Spiegel und Kameras verzichten, da sie beim Rangieren keinen Nutzen bringen",
                "d": "Rückwärtsrangieren ist bei Kraftomnibussen grundsätzlich technisch nicht möglich",
            },
            e="Aufgrund der Fahrzeuglänge und der eingeschränkten Sicht nach hinten bestehen beim Rückwärtsrangieren erhebliche tote Winkel. Empfehlenswert sind daher: wenn verfügbar einen Einweiser nutzen, alle Spiegel und ggf. Rückfahrkamerasysteme systematisch beobachten und in sehr geringer, gut kontrollierbarer Geschwindigkeit rangieren, um im Zweifel sofort anhalten zu können.",
        ),
        en=dict(
            q="What is advisable when reversing a long bus, for example in a depot or at a tight terminus?",
            o={
                "a": "Generally reverse at high speed to save time",
                "b": "Where possible, use a spotter/banksman, systematically use all available mirrors and camera systems, and reverse at very low speed to compensate for the large blind spots at the rear",
                "c": "Dispense with mirrors and cameras, since they provide no benefit when reversing",
                "d": "Reversing is generally not technically possible with buses",
            },
            e="Because of the vehicle's length and limited rearward visibility, considerable blind spots exist when reversing. It is therefore advisable to: use a spotter/banksman where available, systematically monitor all mirrors and any reversing camera systems, and reverse at very low, well-controlled speed so as to be able to stop immediately if needed.",
        ),
    ),
    dict(
        id="bus-technik-10", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Seitenwind)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Warum sind Kraftomnibusse besonders anfällig für Seitenwindeinflüsse, etwa auf Brücken oder in offenem Gelände?",
            o={
                "a": "Weil Busse grundsätzlich schwerer sind als Lkw und deshalb windunanfälliger",
                "b": "Seitenwind hat bei Bussen keinerlei praktische Bedeutung",
                "c": "Wegen ihrer großen seitlichen Angriffsfläche (Höhe und Länge) bei vergleichsweise geringem Gewicht im Verhältnis zur Fläche reagieren Busse empfindlicher auf Seitenwind, was besonders bei Doppeldeckern und Gelenkbussen die Fahrstabilität beeinträchtigen kann",
                "d": "Seitenwind betrifft ausschließlich Fahrzeuge mit offenem Verdeck",
            },
            e="Die große Höhe und Länge eines Kraftomnibusses bieten dem Wind eine erhebliche Angriffsfläche, während das Gewicht im Verhältnis dazu vergleichsweise gering ist. Bei starkem Seitenwind - etwa auf Brücken, in Waldschneisen oder bei Sturmwarnung - kann dies die Spurhaltung beeinträchtigen; bei Doppeldeckern und Gelenkbussen ist die Windempfindlichkeit besonders ausgeprägt. Angepasste, reduzierte Geschwindigkeit ist in solchen Situationen geboten.",
        ),
        en=dict(
            q="Why are buses particularly susceptible to crosswind effects, for example on bridges or in open terrain?",
            o={
                "a": "Because buses are generally heavier than lorries and therefore less affected by wind",
                "b": "Crosswind has no practical relevance for buses whatsoever",
                "c": "Because of their large side surface area (height and length) relative to comparatively modest weight, buses react more sensitively to crosswind, which can impair stability especially on double-deckers and articulated buses",
                "d": "Crosswind only affects vehicles with an open top",
            },
            e="A bus's considerable height and length present a large surface area to the wind, while its weight is comparatively modest relative to that area. In strong crosswinds - for example on bridges, through forest clearings, or during storm warnings - this can affect lane holding; double-deckers and articulated buses are particularly sensitive to wind. Adjusted, reduced speed is warranted in such situations.",
        ),
    ),
    dict(
        id="bus-technik-11", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="§ 6 FeV (Klasseneinteilung D1E/DE)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Wie unterscheiden sich die Fahrerlaubnisklassen D1E und DE hinsichtlich der zulässigen Anhängermasse von D1 bzw. D?",
            o={
                "a": "D1E und DE erlauben Fahrzeugkombinationen aus einem Zugfahrzeug der Klasse D1 bzw. D mit einem Anhänger, dessen zulässige Gesamtmasse 750 kg übersteigt - während D1 und D grundsätzlich nur Anhänger bis 750 kg zulässige Gesamtmasse einschließen",
                "b": "D1E und DE erlauben grundsätzlich keine Anhänger",
                "c": "D1E und DE unterscheiden sich nur in der Farbe des Führerscheins, inhaltlich sind sie identisch mit D1 und D",
                "d": "D1E gilt für Anhänger unter 250 kg, DE für Anhänger unter 500 kg",
            },
            e="Nach § 6 FeV bauen D1E und DE auf D1 bzw. D auf: Sie berechtigen zum Führen von Fahrzeugkombinationen aus einem Zugfahrzeug der jeweiligen Klasse (D1 bzw. D) und einem Anhänger, dessen zulässige Gesamtmasse 750 kg übersteigt. Die Grundklassen D1 und D selbst umfassen dagegen nur Anhänger bis zu einer zulässigen Gesamtmasse von 750 kg.",
        ),
        en=dict(
            q="How do driving licence classes D1E and DE differ from D1 and D respectively in terms of permitted trailer mass?",
            o={
                "a": "D1E and DE permit vehicle combinations consisting of a towing vehicle of class D1 or D respectively together with a trailer whose permissible gross mass exceeds 750 kg, whereas D1 and D generally only include trailers up to a permissible gross mass of 750 kg",
                "b": "D1E and DE generally do not permit trailers at all",
                "c": "D1E and DE differ from D1 and D only in the colour of the licence card; they are otherwise identical",
                "d": "D1E applies to trailers under 250 kg, DE to trailers under 500 kg",
            },
            e="Under Sec. 6 FeV, D1E and DE build on D1 and D respectively: they authorise driving vehicle combinations consisting of a towing vehicle of the respective class (D1 or D) and a trailer whose permissible gross mass exceeds 750 kg. The base classes D1 and D themselves only include trailers up to a permissible gross mass of 750 kg.",
        ),
    ),
    dict(
        id="bus-technik-12", topic="Fahrzeugtechnik und Fahrdynamik von Kraftomnibussen",
        topic_code="fahrzeugtechnik_bus", legal_basis="Allgemeines Fahrzeugtechnikwissen (Anfahrkontrolle)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Was gehört zu einer sorgfältigen Anfahrkontrolle eines Busfahrers, bevor er an einer Haltestelle wieder losfährt?",
            o={
                "a": "Ausschließlich das Prüfen, ob genug Kraftstoff vorhanden ist",
                "b": "Kontrolle, dass alle Türen vollständig geschlossen sind, kein Fahrgast noch ein- oder aussteigt oder sich in der Türnähe befindet, sowie Beobachtung der Spiegel/Kamerasysteme auf Fußgänger und Radfahrer im Nahbereich, bevor angefahren wird",
                "c": "Nur das Einschalten des Blinkers, alles Weitere ist nicht erforderlich",
                "d": "Das Warten auf ein Handzeichen der Fahrgäste im Bus",
            },
            e="Bevor ein Busfahrer an einer Haltestelle wieder anfährt, muss er sicherstellen, dass alle Türen vollständig geschlossen sind, kein Fahrgast mehr ein- oder aussteigt oder sich gefährlich nah an einer Tür befindet, und mit allen verfügbaren Spiegeln bzw. Kamerasystemen den Nahbereich - insbesondere vor der Fahrzeugfront und seitlich - auf Fußgänger und Radfahrer kontrollieren, bevor er losfährt.",
        ),
        en=dict(
            q="What does a careful pull-away check by a bus driver involve before setting off again from a stop?",
            o={
                "a": "Exclusively checking that there is enough fuel",
                "b": "Checking that all doors are fully closed, no passenger is still boarding or alighting or standing dangerously close to a door, and observing the mirrors/camera systems for pedestrians and cyclists in the immediate vicinity before pulling away",
                "c": "Only switching on the indicator; nothing further is required",
                "d": "Waiting for a hand signal from passengers inside the bus",
            },
            e="Before pulling away from a stop, a bus driver must ensure all doors are fully closed, no passenger is still boarding or alighting or standing dangerously close to a door, and must check the immediate surroundings - particularly in front of and alongside the vehicle - for pedestrians and cyclists using all available mirrors or camera systems before setting off.",
        ),
    ),

    # =========================================================================
    # Topic 4: Notfallmaßnahmen und Sicherheitsausrüstung (12)
    # =========================================================================
    dict(
        id="bus-notfall-01", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="§ 35g StVZO",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Wie viele Feuerlöscher schreibt § 35g StVZO für einen einstöckigen Kraftomnibus mindestens vor, und wo müssen sie angebracht sein?",
            o={
                "a": "Kein Feuerlöscher ist vorgeschrieben, es genügt ein Verbandkasten",
                "b": "Mindestens ein Feuerlöscher mit einem Löschmittelinhalt von mindestens 6 kg, in unmittelbarer Nähe des Fahrersitzes und für den Fahrer jederzeit erreichbar angebracht",
                "c": "Mindestens fünf Feuerlöscher, verteilt über den gesamten Fahrgastraum",
                "d": "Ein Feuerlöscher ist nur bei Fahrten über 100 km Pflicht",
            },
            e="§ 35g StVZO schreibt für einstöckige Kraftomnibusse mindestens einen Feuerlöscher mit einem Löschmittelinhalt (Füllmasse) von mindestens 6 kg vor, der in unmittelbarer Nähe des Fahrersitzes anzubringen und für den Fahrer jederzeit ohne Hindernisse erreichbar sein muss. Bei Doppelstockbussen ist je Fahrzeugebene ein Feuerlöscher vorgeschrieben, also insgesamt mindestens zwei.",
        ),
        en=dict(
            q="How many fire extinguishers does Sec. 35g StVZO require at minimum for a single-deck bus, and where must they be mounted?",
            o={
                "a": "No fire extinguisher is required; a first-aid kit is sufficient",
                "b": "At least one fire extinguisher with an extinguishing agent content of at least 6 kg, mounted in immediate proximity to the driver's seat and reachable by the driver at all times without obstruction",
                "c": "At least five fire extinguishers, distributed throughout the passenger compartment",
                "d": "A fire extinguisher is only required on trips over 100 km",
            },
            e="Sec. 35g StVZO requires single-deck buses to carry at least one fire extinguisher with an extinguishing agent content of at least 6 kg, mounted in immediate proximity to the driver's seat and reachable by the driver at all times without obstruction. Double-decker buses require one fire extinguisher per deck, i.e. at least two in total.",
        ),
    ),
    dict(
        id="bus-notfall-02", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="§ 35g StVZO",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Wie oft muss die Funktionsfähigkeit der Feuerlöscher in einem Kraftomnibus nach § 35g StVZO überprüft werden?",
            o={
                "a": "Nie, einmal eingebaute Feuerlöscher gelten dauerhaft als funktionsfähig",
                "b": "Nur bei der Hauptuntersuchung alle zwei Jahre",
                "c": "Mindestens einmal jährlich durch eine dazu befähigte Person oder Stelle",
                "d": "Nur nach jedem tatsächlichen Einsatz des Feuerlöschers",
            },
            e="Nach § 35g StVZO ist die Funktionsfähigkeit der vorgeschriebenen Feuerlöscher mindestens einmal jährlich von einer hierzu befähigten Person oder Stelle zu überprüfen. Der Nachweis dieser Prüfung wird üblicherweise durch eine Prüfplakette am Feuerlöscher dokumentiert. Ein Fehlen oder eine überfällige Prüfung kann als Mangel bei der Fahrzeugkontrolle gelten.",
        ),
        en=dict(
            q="Under Sec. 35g StVZO, how often must the functionality of fire extinguishers on a bus be checked?",
            o={
                "a": "Never; once installed, fire extinguishers are permanently deemed functional",
                "b": "Only at the periodic technical inspection every two years",
                "c": "At least once a year, by a suitably qualified person or body",
                "d": "Only after each actual use of the fire extinguisher",
            },
            e="Under Sec. 35g StVZO, the functionality of the required fire extinguishers must be checked at least once a year by a suitably qualified person or body. This inspection is usually documented with an inspection sticker on the extinguisher. A missing or overdue inspection can be treated as a defect during a vehicle check.",
        ),
    ),
    dict(
        id="bus-notfall-03", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Notausstiege)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Was gehört zu den Pflichten eines Busfahrers im Hinblick auf Notausstiege (Notausstiegsfenster, Dachluken, Nottüren) vor Fahrtantritt, insbesondere im Reiseverkehr?",
            o={
                "a": "Notausstiege müssen nicht überprüft werden, sie funktionieren immer automatisch",
                "b": "Der Fahrer sollte sich vor Fahrtantritt vergewissern, dass Notausstiege nicht blockiert (z. B. durch Gepäck) und frei zugänglich sind, und die Fahrgäste bei Bedarf (etwa im Reiseverkehr) kurz über deren Lage informieren",
                "c": "Notausstiege dürfen während der Fahrt grundsätzlich mit Gepäck zugestellt werden, da sie im Regelfall nicht gebraucht werden",
                "d": "Nur der Busunternehmer, nie der Fahrer, ist für Notausstiege verantwortlich",
            },
            e="Notausstiege müssen im Ernstfall sofort und ungehindert nutzbar sein. Ein sorgfältiger Fahrer kontrolliert vor Fahrtantritt, dass Notausstiegsfenster, Dachluken oder Nottüren frei zugänglich sind und nicht etwa durch Gepäckstücke verstellt wurden, und informiert die Fahrgäste - insbesondere bei längeren Reisebusfahrten - kurz über deren Lage und Bedienung, um im Ernstfall Zeit zu sparen.",
        ),
        en=dict(
            q="What are a bus driver's duties regarding emergency exits (emergency-exit windows, roof hatches, emergency doors) before setting off, particularly on coach trips?",
            o={
                "a": "Emergency exits do not need to be checked; they always function automatically",
                "b": "The driver should verify before departure that emergency exits are not blocked (e.g. by luggage) and are freely accessible, and should briefly inform passengers of their location where relevant, e.g. on coach trips",
                "c": "Emergency exits may generally be blocked with luggage while travelling, since they are normally not needed",
                "d": "Only the bus operator, never the driver, is responsible for emergency exits",
            },
            e="Emergency exits must be usable immediately and without obstruction in a genuine emergency. A careful driver checks before departure that emergency-exit windows, roof hatches, or emergency doors are freely accessible and not blocked by luggage, and briefly informs passengers - especially on longer coach trips - of their location and use, to save time in an actual emergency.",
        ),
    ),
    dict(
        id="bus-notfall-04", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Evakuierung)",
        points=4, high_stakes=True, correct=["a"],
        de=dict(
            q="Was ist bei einer Evakuierung eines vollbesetzten Reisebusses nach einem Unfall oder Brandausbruch grundsätzlich vorrangig zu beachten?",
            o={
                "a": "Ruhiges, systematisches Vorgehen ohne Panik: nächstgelegene, sichere Ausstiege (Türen und Notausstiege) nutzen, Fahrgäste gezielt anweisen, hilfsbedürftige Personen zuerst unterstützen und sich an einem sicheren Sammelpunkt abseits der Fahrbahn versammeln",
                "b": "Alle Fahrgäste sollen gleichzeitig durch dieselbe Tür flüchten, um Verwirrung zu vermeiden",
                "c": "Der Fahrer sollte den Bus zuerst verlassen, bevor er die Fahrgäste informiert",
                "d": "Eine Evakuierung ist bei Bussen aufgrund der stabilen Bauweise grundsätzlich nie erforderlich",
            },
            e="Bei einer Evakuierung ist ruhiges, koordiniertes Handeln entscheidend, um Panik und einen Fahrgaststau an einzelnen Ausgängen zu vermeiden. Alle verfügbaren, sicher erreichbaren Ausstiege - Türen und Notausstiege - sollten genutzt werden; Fahrgäste mit eingeschränkter Mobilität oder in Schockzustand benötigen gezielte Unterstützung. Nach dem Verlassen des Fahrzeugs sollten sich Fahrgäste an einem sicheren Sammelpunkt abseits der Fahrbahn und möglicher Gefahrenquellen (z. B. Kraftstoff, fließender Verkehr) versammeln.",
        ),
        en=dict(
            q="What is generally the priority when evacuating a fully occupied coach after an accident or a fire breaks out?",
            o={
                "a": "Calm, systematic action without panic: use the nearest safe exits (doors and emergency exits), give passengers clear instructions, assist those needing help first, and gather at a safe assembly point away from the roadway",
                "b": "All passengers should flee through the same door simultaneously to avoid confusion",
                "c": "The driver should leave the bus first, before informing the passengers",
                "d": "Evacuation is generally never necessary on buses because of their sturdy construction",
            },
            e="During an evacuation, calm, coordinated action is crucial to avoid panic and a bottleneck of passengers at a single exit. All available, safely reachable exits - doors and emergency exits - should be used; passengers with reduced mobility or in shock need targeted assistance. After leaving the vehicle, passengers should gather at a safe assembly point away from the roadway and any hazards (e.g. fuel, moving traffic).",
        ),
    ),
    dict(
        id="bus-notfall-05", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Nothammer)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Wofür ist der in vielen Bussen an den Fenstern angebrachte Nothammer bestimmt?",
            o={
                "a": "Zum Aufbrechen von Getränkeautomaten am Busbahnhof",
                "b": "Um im echten Notfall (z. B. wenn Türen blockiert sind) eine Fensterscheibe gezielt einzuschlagen und so einen zusätzlichen Fluchtweg zu schaffen",
                "c": "Zum routinemäßigen Öffnen der Fenster während der Fahrt zur Belüftung",
                "d": "Ausschließlich zur Dekoration, er hat keine praktische Funktion",
            },
            e="Der Nothammer dient dazu, in einem echten Notfall - etwa wenn reguläre Türen und Notausstiege blockiert oder unbenutzbar sind - eine Fensterscheibe gezielt an einer markierten Stelle einzuschlagen, um zusätzliche Fluchtwege zu schaffen. Er darf ausschließlich zu diesem Zweck verwendet werden und ist eine wichtige Ergänzung zu den regulären Notausstiegen.",
        ),
        en=dict(
            q="What is the emergency hammer mounted at many bus windows intended for?",
            o={
                "a": "To break open vending machines at bus stations",
                "b": "To deliberately smash a window in a genuine emergency (e.g. when doors are blocked), creating an additional escape route",
                "c": "To routinely open windows for ventilation during the journey",
                "d": "Purely for decoration; it has no practical function",
            },
            e="The emergency hammer is intended for use in a genuine emergency - for example when regular doors and emergency exits are blocked or unusable - to deliberately smash a window at a marked point, creating additional escape routes. It must only be used for this purpose and is an important supplement to the regular emergency exits.",
        ),
    ),
    dict(
        id="bus-notfall-06", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="§ 35h StVZO (Erste-Hilfe-Material)",
        points=2, high_stakes=False, correct=["a"],
        de=dict(
            q="Was schreibt § 35h StVZO sinngemäß in Bezug auf Erste-Hilfe-Material in Kraftomnibussen vor?",
            o={
                "a": "Kraftomnibusse müssen mit geeignetem Verbandmaterial (Erste-Hilfe-Ausstattung) ausgerüstet sein, das leicht zugänglich mitgeführt wird",
                "b": "Erste-Hilfe-Material ist bei Bussen gesetzlich ausdrücklich nicht vorgeschrieben",
                "c": "Erste-Hilfe-Material darf nur von Fahrgästen mit medizinischer Ausbildung mitgeführt werden",
                "d": "Ein Verbandkasten ist nur bei Fahrten außerhalb Deutschlands erforderlich",
            },
            e="§ 35h StVZO verlangt, dass Kraftomnibusse mit geeignetem Verbandmaterial ausgestattet sind, das leicht zugänglich mitgeführt wird, um im Verletzungsfall eine erste Versorgung von Fahrgästen zu ermöglichen, bis professionelle Hilfe eintrifft.",
        ),
        en=dict(
            q="What does Sec. 35h StVZO essentially require regarding first-aid material on buses?",
            o={
                "a": "Buses must be equipped with suitable first-aid/dressing material, carried so it is easily accessible",
                "b": "First-aid material is expressly not required by law on buses",
                "c": "First-aid material may only be carried by passengers with medical training",
                "d": "A first-aid kit is only required on trips outside Germany",
            },
            e="Sec. 35h StVZO requires buses to be equipped with suitable dressing/first-aid material, carried so it is easily accessible, to enable initial care for injured passengers until professional help arrives.",
        ),
    ),
    dict(
        id="bus-notfall-07", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Brandverhalten)",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Was sollte ein Busfahrer tun, wenn während der Fahrt Rauch oder Brandgeruch aus dem Motorraum wahrgenommen wird?",
            o={
                "a": "Die Geschwindigkeit erhöhen, um schneller den Zielort zu erreichen",
                "b": "Den Vorfall ignorieren, solange kein offenes Feuer sichtbar ist",
                "c": "Den Bus umgehend an einer sicheren Stelle anhalten, den Motor abstellen, die Fahrgäste zur zügigen, ruhigen Evakuierung auffordern und sich, sofern gefahrlos möglich, mit dem mitgeführten Feuerlöscher oder durch Alarmierung der Feuerwehr um die Brandbekämpfung kümmern",
                "d": "Weiterfahren bis zur nächsten Haltestelle, egal wie weit diese entfernt ist",
            },
            e="Rauch- oder Brandgeruch ist ein ernstzunehmendes Warnsignal. Der Fahrer sollte den Bus sofort an einer sicheren Stelle anhalten, den Motor abstellen, die Fahrgäste ruhig aber zügig zur Evakuierung auffordern, ausreichend Abstand zum Fahrzeug halten lassen und - sofern ohne Eigengefährdung möglich - mit dem vorgeschriebenen Feuerlöscher reagieren sowie die Feuerwehr alarmieren. Weiterfahren mit einem brennenden oder rauchenden Fahrzeug gefährdet alle Insassen erheblich.",
        ),
        en=dict(
            q="What should a bus driver do if smoke or a burning smell is noticed coming from the engine compartment while driving?",
            o={
                "a": "Increase speed to reach the destination faster",
                "b": "Ignore the incident as long as no open flame is visible",
                "c": "Stop the bus immediately at a safe location, switch off the engine, instruct passengers to evacuate promptly and calmly, and, if it can be done without personal danger, attempt to fight the fire with the on-board extinguisher or call the fire brigade",
                "d": "Continue driving to the next stop, regardless of how far away it is",
            },
            e="Smoke or a burning smell is a serious warning sign. The driver should immediately stop the bus at a safe location, switch off the engine, calmly but promptly have passengers evacuate, keep them at a safe distance from the vehicle, and - if it can be done without endangering themselves - respond with the required fire extinguisher and call the fire brigade. Continuing to drive a burning or smoking vehicle seriously endangers everyone on board.",
        ),
    ),
    dict(
        id="bus-notfall-08", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Absicherung Unfallstelle)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was gehört nach einem Unfall mit einem Kraftomnibus auf der Straße zu den ersten sicherheitsrelevanten Maßnahmen des Fahrers?",
            o={
                "a": "Sofort alle Fahrgäste zum Aussteigen auf die Fahrbahn auffordern, unabhängig von der Verkehrslage",
                "b": "Warnblinkanlage einschalten, wenn möglich die Unfallstelle mit Warndreieck absichern, für Eigen- und Fahrgastsicherheit sorgen und den Notruf absetzen bzw. absetzen lassen",
                "c": "Zunächst die Beschwerden der Fahrgäste zur Verspätung entgegennehmen, bevor Sicherheitsmaßnahmen ergriffen werden",
                "d": "Das Fahrzeug ohne weitere Maßnahmen sofort verlassen und allein zu Fuß Hilfe holen",
            },
            e="Nach einem Unfall sollte der Fahrer zunächst die Warnblinkanlage einschalten, die Unfallstelle nach Möglichkeit mit einem Warndreieck absichern (unter Beachtung der eigenen Sicherheit), die Lage einschätzen und den Notruf absetzen bzw. veranlassen. Erst danach - abhängig von der konkreten Gefährdungslage - sollte über eine geordnete Evakuierung der Fahrgäste entschieden werden, da unkontrolliertes Aussteigen auf eine befahrene Straße zusätzliche Risiken schafft.",
        ),
        en=dict(
            q="After a bus accident on the road, what should be among the driver's first safety-related actions?",
            o={
                "a": "Immediately have all passengers get off onto the carriageway, regardless of the traffic situation",
                "b": "Switch on the hazard warning lights, secure the accident site with a warning triangle where possible, ensure personal and passenger safety, and call or have someone call the emergency services",
                "c": "First deal with passenger complaints about the delay before taking any safety measures",
                "d": "Leave the vehicle immediately without any further measures and go for help alone on foot",
            },
            e="After an accident, the driver should first switch on the hazard warning lights, secure the accident site with a warning triangle where possible (while ensuring their own safety), assess the situation, and call or arrange for the emergency services to be called. Only after that - depending on the specific hazard situation - should an orderly evacuation of passengers be decided on, since uncontrolled disembarking onto a busy road creates additional risks.",
        ),
    ),
    dict(
        id="bus-notfall-09", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Rollstuhl-/Mobilitätshilfe-Sicherung)",
        points=3, high_stakes=True, correct=["a"],
        de=dict(
            q="Worauf muss ein Busfahrer besonders achten, wenn ein Fahrgast im Rollstuhl über die zugehörige Rampe oder den Rollstuhllift ein- oder aussteigt?",
            o={
                "a": "Ausreichend Zeit lassen, den Fahrgast bei Bedarf unterstützen, den Rollstuhl sicher in der vorgesehenen Rollstuhlstellfläche fixieren (Rückhaltesystem/Gurte) und erst danach weiterfahren",
                "b": "Die Rampe grundsätzlich möglichst schnell ausklappen und wieder einklappen, um Verspätungen zu vermeiden",
                "c": "Rollstuhlfahrer müssen sich immer selbst um die Sicherung ihres Rollstuhls kümmern, der Fahrer darf nicht helfen",
                "d": "Der Rollstuhl muss während der Fahrt nicht gesondert gesichert werden, da die Bremsen des Rollstuhls ausreichen",
            },
            e="Beim Ein- und Ausstieg über Rampe oder Lift sollte dem Fahrgast ausreichend Zeit gelassen und bei Bedarf Unterstützung angeboten werden. In der Rollstuhlstellfläche muss der Rollstuhl mit dem vorgesehenen Rückhaltesystem gesichert werden, bevor der Bus weiterfährt - ungesicherte Rollstühle können bei Bremsungen oder in Kurven erheblich verrutschen und den Fahrgast sowie andere gefährden.",
        ),
        en=dict(
            q="What must a bus driver pay particular attention to when a passenger in a wheelchair boards or alights via the ramp or wheelchair lift?",
            o={
                "a": "Allow sufficient time, assist the passenger if needed, secure the wheelchair firmly in the designated wheelchair space using the retention system/straps, and only continue driving afterward",
                "b": "Generally extend and retract the ramp as quickly as possible to avoid delays",
                "c": "Wheelchair users must always secure their own wheelchair themselves; the driver may not help",
                "d": "The wheelchair does not need separate securing during the journey, because the wheelchair's own brakes are sufficient",
            },
            e="When boarding or alighting via a ramp or lift, the passenger should be given sufficient time and offered assistance if needed. In the wheelchair space, the wheelchair must be secured with the designated retention system before the bus continues - an unsecured wheelchair can shift significantly under braking or in curves, endangering the passenger and others.",
        ),
    ),
    dict(
        id="bus-notfall-10", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Standplatzbereiche)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum ist die Anzahl zulässiger Stehplätze in einem Linienbus begrenzt und in bestimmten Bereichen (z. B. über der Vorderachse) reduziert oder ausgeschlossen?",
            o={
                "a": "Weil Stehplätze in Bussen grundsätzlich verboten sind",
                "b": "Weil eine übermäßige Anzahl stehender Fahrgäste bei Bremsungen, Ausweichmanövern oder in Kurven ein erhöhtes Sturz- und Verletzungsrisiko birgt und die Fahrstabilität sowie den Bremsweg beeinträchtigt; bestimmte Bereiche mit eingeschränkter Sicht oder Stabilität für den Fahrer sind deshalb besonders reguliert",
                "c": "Weil stehende Fahrgäste den Fahrgastfluss beim Ein- und Aussteigen beschleunigen",
                "d": "Weil Stehplätze ausschließlich aus ästhetischen Gründen begrenzt werden",
            },
            e="Stehende Fahrgäste sind bei abrupten Fahrmanövern - Notbremsung, Ausweichen, Kurvenfahrt - besonders sturzgefährdet, da sie keinen Sitz mit Rückhalt haben. Die zulässige Stehplatzzahl ist daher begrenzt, und in bestimmten Bereichen (etwa unmittelbar hinter der Fahrertür oder über Achsen mit eingeschränkter Sicht/Stabilität für den Fahrer) kann sie weiter eingeschränkt sein, um Sicherheit und Fahrstabilität zu gewährleisten.",
        ),
        en=dict(
            q="Why is the number of permitted standing places on a scheduled bus limited, and reduced or excluded in certain areas (e.g. above the front axle)?",
            o={
                "a": "Because standing places are generally prohibited on buses",
                "b": "Because an excessive number of standing passengers increases the risk of falls and injury during braking, evasive manoeuvres, or cornering, and impairs stability and braking distance; certain areas with limited visibility or stability for the driver are therefore specifically regulated",
                "c": "Because standing passengers speed up the flow of boarding and alighting",
                "d": "Because standing places are limited purely for aesthetic reasons",
            },
            e="Standing passengers are particularly at risk of falling during abrupt manoeuvres - emergency braking, evasive action, cornering - since they lack a seat with restraint. The permitted number of standing places is therefore limited, and in certain areas (e.g. immediately behind the driver's door, or above axles where the driver's visibility/stability is limited) it may be further restricted to ensure safety and stability.",
        ),
    ),
    dict(
        id="bus-notfall-11", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (medizinischer Notfall an Bord)",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Ein Fahrgast erleidet während einer längeren Reisebusfahrt auf der Autobahn plötzlich einen medizinischen Notfall. Wie sollte der Fahrer reagieren?",
            o={
                "a": "Die Fahrt bis zum geplanten Ziel unverändert fortsetzen, da ein Zwischenstopp den Fahrplan gefährden würde",
                "b": "Den Fahrgast ignorieren, da medizinische Hilfe nicht zu den Aufgaben des Fahrers gehört",
                "c": "So bald wie sicher möglich an geeigneter Stelle (z. B. Parkplatz, Nothaltebucht) anhalten, den Rettungsdienst alarmieren, Erste-Hilfe-Material bereitstellen und, soweit möglich, Erste Hilfe leisten oder leisten lassen, bis professionelle Hilfe eintrifft",
                "d": "Selbstständig eine medizinische Diagnose stellen und dem Fahrgast Medikamente aus dem Verbandkasten verabreichen",
            },
            e="Bei einem medizinischen Notfall an Bord hat die Sicherheit des betroffenen Fahrgasts Vorrang. Der Fahrer sollte so schnell wie sicher möglich an geeigneter Stelle anhalten, den Rettungsdienst alarmieren, das mitgeführte Erste-Hilfe-Material bereitstellen und im Rahmen seiner Möglichkeiten (bzw. durch andere Fahrgäste mit Erste-Hilfe-Kenntnissen) erste Hilfe leisten, ohne eine eigene medizinische Diagnose oder Medikamentengabe vorzunehmen.",
        ),
        en=dict(
            q="A passenger suffers a sudden medical emergency during a long coach trip on the motorway. How should the driver respond?",
            o={
                "a": "Continue the journey unchanged to the planned destination, since an intermediate stop would jeopardise the schedule",
                "b": "Ignore the passenger, since providing medical help is not part of the driver's duties",
                "c": "Stop as soon as safely possible at a suitable location (e.g. a car park or emergency lay-by), call emergency medical services, provide the on-board first-aid material, and give or arrange first aid as far as possible until professional help arrives",
                "d": "Independently make a medical diagnosis and administer medication from the first-aid kit to the passenger",
            },
            e="In a medical emergency on board, the affected passenger's safety takes priority. The driver should stop as soon as safely possible at a suitable location, call emergency medical services, provide the on-board first-aid material, and give first aid within their own competence (or via other passengers with first-aid training) without making their own medical diagnosis or administering medication.",
        ),
    ),
    dict(
        id="bus-notfall-12", topic="Notfallmaßnahmen und Sicherheitsausrüstung im Kraftomnibus",
        topic_code="notfall_bus", legal_basis="Allgemeines Sicherheitswissen (Fahrgastinformation Sicherheit)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum ist es insbesondere im Reisebus- und Fernlinienverkehr sinnvoll, Fahrgäste zu Beginn der Fahrt kurz auf Sicherheitseinrichtungen (Notausstiege, Nothammer, Sitzgurte) hinzuweisen?",
            o={
                "a": "Weil dies gesetzlich vollkommen bedeutungslos ist und nur der Unterhaltung dient",
                "b": "Weil Fahrgäste im Ernstfall dadurch schneller und sicherer reagieren können, was insbesondere bei Fahrten mit ungeübten Fahrgästen und ohne vertrautes Fahrzeugumfeld die Reaktionszeit im Notfall deutlich verkürzt",
                "c": "Weil dadurch die Lenkzeit des Fahrers verkürzt wird",
                "d": "Weil dies ausschließlich bei Fahrten ins Ausland vorgeschrieben ist",
            },
            e="Ein kurzer Sicherheitshinweis zu Beginn der Fahrt - vergleichbar der Sicherheitsunterweisung im Flugzeug - hilft Fahrgästen, sich mit Lage und Bedienung von Notausstiegen, Nothammer und Sitzgurten vertraut zu machen. Im Ernstfall verkürzt dieses Wissen die Reaktionszeit erheblich und kann entscheidend zu einer schnelleren, geordneten Evakuierung beitragen, besonders bei Fahrgästen, die das Fahrzeug nicht kennen.",
        ),
        en=dict(
            q="Why is it useful, especially on coach and long-distance scheduled services, to briefly brief passengers on safety equipment (emergency exits, emergency hammer, seatbelts) at the start of the journey?",
            o={
                "a": "Because it is legally completely meaningless and serves only as entertainment",
                "b": "Because it allows passengers to react faster and more safely in a genuine emergency, which noticeably shortens reaction time in an emergency especially for passengers unfamiliar with the vehicle",
                "c": "Because it shortens the driver's driving time",
                "d": "Because it is only required by law on trips abroad",
            },
            e="A brief safety briefing at the start of the journey - similar to the safety briefing on an aircraft - helps passengers familiarize themselves with the location and use of emergency exits, the emergency hammer, and seatbelts. In a genuine emergency, this knowledge significantly reduces reaction time and can be decisive for a faster, orderly evacuation, especially for passengers unfamiliar with the vehicle.",
        ),
    ),
]


def build():
    meta = {
        "app": "Zettacard / fuehrerschein-bus-lernmodul",
        "version": "0.1",
        "generated": "2026-08-12",
        "description": (
            "Original MCQs for the German bus/passenger-transport driving license Zusatzstoff "
            "module (Klassen D1/D1E/D/DE), covering: PBefG/BOKraft passenger-conduct and safety "
            "rules (boarding/alighting, standing-passenger conduct, driver authority/Hausrecht, "
            "fare disputes, misuse of safety equipment) plus EU Reg. (EU) 181/2011 bus passenger "
            "rights for accessibility/wheelchair and mobility-aid assistance duties; D-family "
            "driving/rest-time and tachograph specifics under EU Reg. 561/2006 and FPersG/FPersV, "
            "including the Art. 3(a) 50 km local scheduled-service exemption, the FPersV Sec. 18 "
            "10-17 seat non-commercial exemption, and the occasional-service weekly-rest deferral "
            "rule that has no equivalent in freight transport; bus-specific vehicle handling "
            "(articulated-bus dynamics, mirror/blind-spot checks for a long/tall/wide vehicle, "
            "kneeling-bus mechanisms, crosswind and high-centre-of-gravity effects); and emergency "
            "procedures (evacuation, StVZO Sec. 35g/35h fire-extinguisher and first-aid-kit rules, "
            "emergency hammer use, wheelchair securing, medical emergencies on board). Content is "
            "independently phrased from public FeV/PBefG/BOKraft/StVZO/EU-VO 561/2006/181/2011/"
            "FPersG/FPersV text (gesetze-im-internet.de and lxgesetze.de mirrors) and general "
            "commercial-passenger-vehicle safety knowledge, NOT copied from the licensed amtlicher "
            "Fragenkatalog. This is a fully independent exam module - separate content pool, "
            "separate exam simulation from every other module (Fuehrerschein Klasse B, Motorrad, "
            "LKW, Angelschein, etc.). DE (canonical) + EN only for this first round."
        ),
        "class": "D1/D1E/D/DE",
        "canonical_locale": "de",
        "point_system": "2-4 points per question, matching this app's existing style",
        "pass_rule_note": (
            "Provisional: same generic mechanics as Klasse B/LKW (30-question draw, max 10 error "
            "points, auto-fail on 2+ wrong high_stakes) used as a reasonable placeholder pending "
            "legal review of the actual Klasse D/D1/D1E/DE theory exam parameters - see "
            "legal_review_status."
        ),
        "legal_review_status": "NOT legally reviewed",
        "total_questions": len(QUESTIONS),
        "license": "CC BY-NC-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "license_note": (
            "Attribution-NonCommercial-ShareAlike: free to use, adapt, and redistribute for "
            "non-commercial exam-prep purposes, with credit and under the same license. Commercial "
            "reuse needs a separate arrangement; non-commercial prep tools/forks are welcome."
        ),
        "locales": ["de", "en"],
    }

    pilot_questions = []
    core_questions = []
    per_locale = {"de": {}, "en": {}}

    for q in QUESTIONS:
        base = dict(
            id=q["id"], topic=q["topic"], topic_code=q["topic_code"],
            class_scope=D_FAMILY, grundstoff=False, legal_basis=q["legal_basis"],
            points=q["points"], high_stakes=q["high_stakes"],
            question_type="single_choice", image_ref=None, correct=q["correct"],
            roles=["all"],
        )
        pilot_q = dict(base)
        pilot_q["text"] = {
            "de": {"question": q["de"]["q"], "options": q["de"]["o"]},
            "en": {"question": q["en"]["q"], "options": q["en"]["o"]},
        }
        pilot_q["explanation"] = {"de": q["de"]["e"], "en": q["en"]["e"]}
        pilot_questions.append(pilot_q)

        core_questions.append(base)
        per_locale["de"][q["id"]] = {"question": q["de"]["q"], "options": q["de"]["o"], "explanation": q["de"]["e"]}
        per_locale["en"][q["id"]] = {"question": q["en"]["q"], "options": q["en"]["o"], "explanation": q["en"]["e"]}

    # 1) master pilot file (source of truth, matches lksg_pilot.json / lkw_pilot.json shape)
    json.dump({"meta": meta, "questions": pilot_questions},
              open(os.path.join(HERE, "fuehrerschein_bus_pilot.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 2) app/data/fuehrerschein_bus/core.json + locales/{de,en}.json
    module_dir = os.path.join(APP_DATA, "fuehrerschein_bus")
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)
    core_meta = dict(meta)
    json.dump({"meta": core_meta, "questions": core_questions},
              open(os.path.join(module_dir, "core.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    for loc in ("de", "en"):
        json.dump(per_locale[loc], open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    print(f"Wrote {len(QUESTIONS)} fuehrerschein_bus questions.")
    topics = {}
    for q in QUESTIONS:
        topics.setdefault(q["topic_code"], 0)
        topics[q["topic_code"]] += 1
    print(topics)


if __name__ == "__main__":
    build()
