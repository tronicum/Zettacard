#!/usr/bin/env python3
"""One-off expansion script for the Motorrad (A1/A2/A) module (DN-65).

Adds ~48 new Zusatzstoff questions to the existing 90-question Motorrad
pilot, continuing the ID numbering scheme within 4 already-existing topics
(fahrphysik, schutzausruestung, verkehrsverhalten, fahrerlaubnis) rather than
introducing new topic codes - the same "extend existing topics, DE+EN only
for the new content" pattern used for tonight's LKW expansion
(lkw-ladungssicherung-31..45 / lkw-lenkzeiten-31..45).

Produces:
  - data/motorrad_pilot.json     (master source, updated IN PLACE - existing
                                   90 questions untouched, 48 new appended)
  - app/data/motorrad/core.json
  - app/data/motorrad/locales/<lang>.json for all 12 declared locales
    (new questions only carry de/en text; the other 10 locale files simply
    don't get entries for these new IDs yet, same as how build_modules.py's
    split_module() already tolerates partial locale coverage elsewhere)

Mirrors what data/build_modules.py's split_module() does, but scoped to just
this one module (like data/gen_lksg.py did for lksg) so the rest of
app/data is left untouched - build_modules.py itself rmtree()s the whole
app/data dir, which is too risky to run mid-review.

Sourcing: SS 6 FeV (license classes A1/A2/A - engine power, power-to-weight,
displacement thresholds), Anlage 7/7b FeV (Fahrerschulung structure for
Kraftrad classes), SS 21a Abs. 2 StVO (Schutzhelmpflicht), EU-VO 168/2013
(mandatory ABS >125cc, ABS-or-CBS choice <=125cc), general StVO/StVZO
provisions and established motorcycle-safety/riding-physics knowledge
(countersteering, weight transfer under braking, SEE/hazard-perception
technique, T-CLOCS-style pre-ride checks). All content independently
phrased from the underlying regulatory/physics facts - NOT copied from any
commercial driving-school question bank or the official amtlicher
Fragenkatalog.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(HERE, "..", "app", "data")
PILOT_PATH = os.path.join(HERE, "motorrad_pilot.json")

ALL_LOCALES = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]

NEW_QUESTIONS = [
    # =========================================================
    # fahrphysik (16-27): lean/countersteering physics & balance,
    # braking-distribution / ABS / CBS awareness
    # =========================================================
    dict(
        id="motorrad-fahrphysik-16", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht - sicheres Führen des Fahrzeugs)",
        points=4, high_stakes=True, correct=["c"],
        de=dict(
            q="Warum kippt ein Motorrad beim Gegenlenken (kurzer Druck auf das kurveninnere Lenkerende) tatsächlich in die gewünschte Richtung, obwohl der Impuls das Vorderrad zunächst leicht in die Gegenrichtung einschlagen lässt?",
            o={
                "a": "Weil der Fahrer dabei automatisch sein Körpergewicht verlagert",
                "b": "Weil sich dadurch der Reifendruck kurzzeitig verändert",
                "c": "Weil das kurzzeitige Gegeneinschlagen den Sturz des Kreiselmoments auslöst, wodurch das Motorrad um die eigene Längsachse in die gewünschte Richtung kippt",
                "d": "Weil dadurch automatisch die Hinterradbremse mit betätigt wird",
            },
            e="Die drehenden Räder eines Motorrads wirken als Kreisel. Ein kurzer Druck auf das kurveninnere Lenkerende bewirkt ein leichtes Gegeneinschlagen des Vorderrads; die daraus resultierende Kreiselpräzession lässt das Motorrad um seine Längsachse in genau die gewünschte Richtung kippen. Dieser physikalische Effekt, nicht reine Willenskraft oder Gewichtsverlagerung, ist die Grundlage des Gegenlenkens bei normaler bis hoher Geschwindigkeit.",
        ),
        en=dict(
            q="Why does a motorcycle actually lean into the intended direction during countersteering (a brief push on the inside handlebar grip), even though the initial impulse steers the front wheel slightly the other way?",
            o={
                "a": "Because the rider automatically shifts body weight at the same time",
                "b": "Because tyre pressure briefly changes as a result",
                "c": "Because the brief opposite steering input triggers gyroscopic precession, which tips the motorcycle around its longitudinal axis into the intended direction",
                "d": "Because the rear brake is automatically applied at the same time",
            },
            e="A motorcycle's spinning wheels behave like gyroscopes. A brief push on the inside handlebar grip briefly steers the front wheel slightly the other way; the resulting gyroscopic precession tips the bike around its longitudinal axis in exactly the intended direction. This physical effect - not willpower or weight shift alone - is the basis of countersteering at normal to higher speeds.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-17", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht - sicheres Führen des Fahrzeugs)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Bei sehr niedriger Geschwindigkeit (z. B. Rangieren im Schritttempo) funktioniert das Kurvenfahren mit dem Motorrad überwiegend anders als bei normalem Tempo. Wie?",
            o={
                "a": "Genauso wie bei normalem Tempo, nur langsamer ausgeführt",
                "b": "Überwiegend durch direktes Einlenken des Lenkers in die gewünschte Richtung (klassisches Lenken), da Gegenlenken bei sehr geringem Tempo kaum wirkt",
                "c": "Ausschließlich durch Gewichtsverlagerung, der Lenker bleibt starr geradeaus",
                "d": "Durch kurzes Antippen der Vorderradbremse in der Kurve",
            },
            e="Der Gegenlenkeffekt beruht auf Kreiselkräften, die von der Raddrehzahl abhängen. Bei sehr niedrigem Tempo (Schrittgeschwindigkeit, Rangieren) sind diese Kräfte zu schwach, damit funktioniert klassisches, direktes Einlenken des Lenkers in Kurvenrichtung deutlich besser als Gegenlenken.",
        ),
        en=dict(
            q="At very low speed (e.g. walking-pace manoeuvring), steering a motorcycle through a turn works largely differently than at normal speed. How?",
            o={
                "a": "Exactly the same as at normal speed, just performed more slowly",
                "b": "Mainly by turning the handlebars directly into the intended direction (classic steering), since countersteering barely works at very low speed",
                "c": "Purely by shifting body weight, with the handlebars held rigidly straight",
                "d": "By briefly tapping the front brake mid-turn",
            },
            e="The countersteering effect relies on gyroscopic forces that depend on wheel rotation speed. At very low speed (walking pace, manoeuvring) these forces are too weak, so classic, direct steering-input-into-the-turn works considerably better than countersteering.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-18", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht - sicheres Führen des Fahrzeugs)",
        points=4, high_stakes=True, correct=["a"],
        de=dict(
            q="Warum verlagert sich beim starken Bremsen eines Motorrads die Gewichtskraft deutlich auf das Vorderrad, sodass die Vorderradbremse einen wesentlich größeren Anteil der Bremsleistung übernehmen kann als die Hinterradbremse?",
            o={
                "a": "Durch die Verzögerung wirkt eine Trägheitskraft, die den Schwerpunkt nach vorn kippen lässt und das Vorderrad zusätzlich belastet, während das Hinterrad entlastet wird",
                "b": "Weil die Vorderradbremse serienmäßig immer stärker dimensioniert ist als die Hinterradbremse",
                "c": "Weil sich beim Bremsen automatisch mehr Kraftstoff nach vorn verlagert",
                "d": "Weil das Vorderrad beim Bremsen grundsätzlich einen größeren Durchmesser hat",
            },
            e="Beim Abbremsen wirkt Trägheit auf Fahrer und Motorrad: die Masse 'will' sich weiterhin nach vorn bewegen. Dadurch verlagert sich die dynamische Achslast nach vorn - das Vorderrad wird stärker belastet und kann mehr Bremskraft übertragen, das Hinterrad wird entlastet und neigt bei zu starkem Bremsen zum Blockieren. Deshalb übernimmt die Vorderradbremse bei einer Vollbremsung typischerweise 70-90 % der Verzögerung.",
        ),
        en=dict(
            q="Why does braking hard on a motorcycle shift weight noticeably onto the front wheel, allowing the front brake to provide a much larger share of the braking force than the rear brake?",
            o={
                "a": "Deceleration produces an inertial force that tips the centre of mass forward, loading the front wheel further while unloading the rear wheel",
                "b": "Because the front brake is always built stronger than the rear brake as standard",
                "c": "Because braking automatically shifts more fuel toward the front",
                "d": "Because the front wheel always has a larger diameter than the rear wheel",
            },
            e="During braking, inertia acts on rider and motorcycle: the mass 'wants' to keep moving forward. This shifts the dynamic axle load forward - the front wheel is loaded more heavily and can transmit more braking force, while the rear wheel is unloaded and prone to locking under hard braking. That is why the front brake typically provides 70-90% of stopping power in an emergency stop.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-19", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="EU-Verordnung (EU) Nr. 168/2013 (Genehmigung/Marktüberwachung von zwei-, drei- und vierrädrigen Fahrzeugen)",
        points=4, high_stakes=True, correct=["b"],
        de=dict(
            q="Seit wann ist ein Antiblockiersystem (ABS) für neu typgenehmigte Krafträder mit mehr als 125 cm³ Hubraum in der EU verpflichtend vorgeschrieben?",
            o={
                "a": "Es gab noch nie eine EU-weite ABS-Pflicht für Krafträder",
                "b": "Seit 1. Januar 2016 für neue Fahrzeugtypen (ab 1. Januar 2017 für alle Neuzulassungen), auf Basis der Verordnung (EU) Nr. 168/2013",
                "c": "Erst seit 2023, im Zuge der Euro-5-Abgasnorm",
                "d": "Nur für Krafträder der Klasse A1 (bis 125 cm³)",
            },
            e="Die Verordnung (EU) Nr. 168/2013 schreibt ABS für neu typgenehmigte Krafträder über 125 cm³ Hubraum und über 11 kW Leistung ab dem 1. Januar 2016 vor, für alle entsprechenden Neuzulassungen ab 1. Januar 2017 (mit Ausnahmen z. B. für Wettbewerbs-Enduros/Trial-Maschinen). Für Krafträder bis 125 cm³ genügt wahlweise ABS oder ein Kombibremssystem (CBS).",
        ),
        en=dict(
            q="Since when has an anti-lock braking system (ABS) been mandatory in the EU for newly type-approved motorcycles over 125cc?",
            o={
                "a": "There has never been an EU-wide ABS requirement for motorcycles",
                "b": "Since 1 January 2016 for new vehicle types (from 1 January 2017 for all first registrations), based on Regulation (EU) No. 168/2013",
                "c": "Only since 2023, as part of the Euro 5 emissions standard",
                "d": "Only for class A1 motorcycles (up to 125cc)",
            },
            e="Regulation (EU) No. 168/2013 requires ABS on newly type-approved motorcycles over 125cc and over 11 kW from 1 January 2016, and for all corresponding first registrations from 1 January 2017 (with exceptions, e.g. for competition enduro/trial machines). Motorcycles up to 125cc may instead be fitted with either ABS or a combined braking system (CBS).",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-20", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="EU-Verordnung (EU) Nr. 168/2013",
        points=3, high_stakes=False, correct=["c"],
        de=dict(
            q="Welche Aussage zur Bremsausrüstung von Leichtkrafträdern bis 125 cm³ nach EU-Recht trifft zu?",
            o={
                "a": "Sie dürfen grundsätzlich kein ABS haben",
                "b": "Sie benötigen zwingend sowohl ABS als auch ein Kombibremssystem gleichzeitig",
                "c": "Der Hersteller kann wählen: entweder ein ABS oder ein Kombibremssystem (CBS), das beim Betätigen eines Bremshebels beide Räder mitbremst",
                "d": "Für sie gelten überhaupt keine EU-Vorgaben zur Bremsausrüstung",
            },
            e="Nach Verordnung (EU) Nr. 168/2013 haben Hersteller bei Leichtkrafträdern bis 125 cm³ die Wahl zwischen ABS und einem Kombibremssystem (Combined Braking System, CBS), bei dem die Betätigung eines Bremshebels anteilig auch die jeweils andere Bremse mit aktiviert.",
        ),
        en=dict(
            q="Which statement about the braking equipment of light motorcycles up to 125cc under EU law is correct?",
            o={
                "a": "They may never be fitted with ABS",
                "b": "They must have both ABS and a combined braking system at the same time",
                "c": "The manufacturer can choose: either ABS or a combined braking system (CBS) that partially applies both brakes when one lever is operated",
                "d": "No EU requirements on braking equipment apply to them at all",
            },
            e="Under Regulation (EU) No. 168/2013, manufacturers of light motorcycles up to 125cc may choose between ABS and a combined braking system (CBS), where operating one brake lever also partially applies the other brake.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-21", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=True, correct=["d"],
        de=dict(
            q="Was ist eine der Hauptaufgaben von ABS am Motorrad im Vergleich zum Pkw-ABS?",
            o={
                "a": "Es verkürzt grundsätzlich den Bremsweg auf trockener Straße stärker als bei einem Pkw",
                "b": "Es ersetzt die Notwendigkeit, beide Bremsen zu benutzen",
                "c": "Es verhindert automatisch jede Schräglagenkorrektur in der Kurve",
                "d": "Es verhindert das Blockieren der Räder auch beim spontanen, kräftigen Bremsgriff in einer Gefahrensituation und hilft so, den kritischen Sturz durch ein blockierendes Vorderrad zu vermeiden",
            },
            e="Ein blockierendes Vorderrad ist bei Motorrädern besonders kritisch, da das Fahrzeug dabei sofort die Balance und Lenkfähigkeit verliert und stürzt. ABS verhindert dieses Blockieren auch bei abrupten, kräftigen Bremsgriffen in Schrecksituationen und reduziert dadurch nachweislich die Zahl der Sturz-Unfälle - ohne dabei per se auf jedem Untergrund den Bremsweg zu verkürzen.",
        ),
        en=dict(
            q="What is one of the main functions of ABS on a motorcycle compared with car ABS?",
            o={
                "a": "It always shortens stopping distance on dry roads more than car ABS does",
                "b": "It removes the need to use both brakes",
                "c": "It automatically prevents any lean-angle correction mid-corner",
                "d": "It prevents wheel lock even during a sudden, hard grab of the brake lever in an emergency, helping avoid the critical fall caused by a locked front wheel",
            },
            e="A locked front wheel is especially critical on a motorcycle, since the bike instantly loses balance and steering control and falls. ABS prevents this lockup even during abrupt, hard braking grabs triggered by panic, and has been shown to reduce fall-related crashes - though it does not automatically shorten stopping distance on every surface.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-22", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was passiert physikalisch, wenn ein Motorrad in Schräglage stärker bremst, als der aktuelle Kurvenradius und Reifengrip es zulassen?",
            o={
                "a": "Nichts, moderne Reifen kompensieren das automatisch",
                "b": "Der verfügbare Kraftschluss der Reifen wird zwischen Kurven- und Bremskräften aufgeteilt (Kammscher Kreis); übersteigt die Summe beider Kräfte den maximalen Grip, rutscht das Rad weg",
                "c": "Das Motorrad richtet sich dadurch automatisch stärker auf",
                "d": "Nur das Hinterrad kann in Schräglage überhaupt rutschen",
            },
            e="Der maximale Kraftschluss eines Reifens ist begrenzt (vereinfacht als 'Kammscher Kreis' modelliert) und muss sich Quer- (Kurvenfahrt) und Längskräfte (Bremsen/Beschleunigen) teilen. Wird in Schräglage zusätzlich stark gebremst, kann die Summe beider Kraftanteile den verfügbaren Grip überschreiten - das Rad verliert die Haftung und rutscht weg. Deshalb sollte eine Vollbremsung möglichst aufrecht erfolgen.",
        ),
        en=dict(
            q="What happens physically when a motorcycle leaned over in a corner brakes harder than the current cornering radius and tyre grip allow?",
            o={
                "a": "Nothing, modern tyres compensate for this automatically",
                "b": "The tyre's available grip is shared between cornering forces and braking forces (the 'friction circle'); if the combined demand exceeds maximum grip, the wheel slides out",
                "c": "The motorcycle automatically stands itself upright",
                "d": "Only the rear wheel can ever slide while leaned over",
            },
            e="A tyre's maximum grip is limited (simplified as the 'friction circle' or Kamm's circle) and must be shared between lateral forces (cornering) and longitudinal forces (braking/accelerating). Braking hard while leaned over can push the combined force demand past the available grip, causing the wheel to lose traction and slide out. That is why an emergency stop should, if at all possible, be performed upright.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-23", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Warum wird empfohlen, ein Motorrad vor einer Kurve möglichst noch aufrecht abzubremsen und die Bremse in der Kurve selbst deutlich zu reduzieren oder ganz zu lösen?",
            o={
                "a": "Weil der Reifen in aufrechter Position seinen vollen Kraftschluss für die Bremskraft nutzen kann, während in Schräglage ein Teil des Kraftschlusses bereits für die Kurvenkraft gebunden ist",
                "b": "Weil die Bremsen in Schräglage technisch nicht funktionieren",
                "c": "Weil es gesetzlich verboten ist, in Schräglage zu bremsen",
                "d": "Weil sich dadurch automatisch die Fahrgeschwindigkeit erhöht",
            },
            e="In aufrechter Position steht der gesamte verfügbare Kraftschluss des Reifens für Bremskraft zur Verfügung. In Schräglage ist bereits ein Teil davon durch die Kurvenkraft gebunden (siehe Kammscher Kreis), sodass für zusätzliches Bremsen weniger Reserve bleibt - starkes Bremsen in Schräglage erhöht daher das Rutschrisiko deutlich.",
        ),
        en=dict(
            q="Why is it recommended to complete most braking before a corner while still upright, and to significantly ease off or release the brakes once actually leaned over?",
            o={
                "a": "Because upright, the tyre can use its full available grip for braking force, whereas leaned over, part of that grip is already committed to cornering force",
                "b": "Because brakes technically do not work while leaned over",
                "c": "Because braking while leaned over is legally prohibited",
                "d": "Because it automatically increases riding speed",
            },
            e="Upright, the tyre's full available grip is free for braking. Leaned over, part of that grip is already committed to cornering force (see the friction-circle concept), leaving less reserve for additional braking - so hard braking while leaned over noticeably increases the risk of sliding out.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-24", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum ist eine Vollbremsung mit nur der Hinterradbremse auf einem Motorrad besonders riskant?",
            o={
                "a": "Weil die Hinterradbremse rechtlich gar nicht benutzt werden darf",
                "b": "Weil das Hinterrad durch die Gewichtsverlagerung nach vorn schnell entlastet wird und dadurch leicht blockiert und wegrutscht, was zu einem Highsider führen kann",
                "c": "Weil sie automatisch das Vorderrad blockiert",
                "d": "Weil sie den Bremsweg immer verlängert, egal wie stark gebremst wird",
            },
            e="Beim Bremsen verlagert sich die Last vom Hinter- auf das Vorderrad. Wird nur die Hinterradbremse (kräftig) benutzt, blockiert das entlastete Hinterrad leicht und rutscht seitlich weg; löst der Fahrer die Bremse in diesem Moment, kann das plötzlich wieder greifende Rad das Motorrad ruckartig aufrichten und den Fahrer abwerfen (Highsider).",
        ),
        en=dict(
            q="Why is an emergency stop using only the rear brake particularly risky on a motorcycle?",
            o={
                "a": "Because using the rear brake is not legally permitted at all",
                "b": "Because forward weight transfer quickly unloads the rear wheel, making it easy to lock and slide sideways, which can lead to a highside crash",
                "c": "Because it automatically locks the front wheel",
                "d": "Because it always lengthens stopping distance regardless of how hard it's applied",
            },
            e="Braking shifts load from the rear to the front wheel. Using only the rear brake (hard) easily locks the unloaded rear wheel, causing it to slide sideways; if the rider then releases the brake at that moment, the wheel can suddenly regain grip and violently right the bike, throwing the rider off (a highside).",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-25", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Was versteht man unter dem 'Blick in die Kurve' als Technik bei der Schräglagenfahrt?",
            o={
                "a": "Den Blick fest auf das Vorderrad zu richten, um die Schräglage zu kontrollieren",
                "b": "Den Blick möglichst weit nach unten auf die Fahrbahn direkt vor dem Vorderrad zu richten",
                "c": "Den Blick frühzeitig durch die Kurve zum Kurvenausgang zu richten, wodurch Kopf und Oberkörper die Fahrlinie unbewusst mitbestimmen und das Motorrad ruhiger und präziser gesteuert wird",
                "d": "Den Blick abwechselnd auf Tacho und Fahrbahn zu richten",
            },
            e="Wo der Blick hingeht, folgt unbewusst auch die Fahrlinie ('target fixation' im positiven Sinn). Wer frühzeitig durch die Kurve zum Ausgang blickt statt auf das unmittelbar Vorausliegende, fährt ruhiger, findet die richtige Linie leichter und reagiert schneller auf den weiteren Kurvenverlauf.",
        ),
        en=dict(
            q="What does the riding technique 'look through the corner' mean when leaned over?",
            o={
                "a": "Fixing your gaze on the front wheel to monitor lean angle",
                "b": "Looking as far down as possible at the road surface directly in front of the front wheel",
                "c": "Looking early through the corner toward the exit, since head and upper-body orientation unconsciously help steer the line, producing a smoother and more precise ride",
                "d": "Alternating your gaze between the speedometer and the road",
            },
            e="Where the eyes go, the riding line tends to follow (a positive form of target fixation). Looking early through a corner toward its exit, rather than at the immediate road surface, produces a smoother ride, makes finding the correct line easier, and speeds up reaction to how the corner continues.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-26", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=True, correct=["a"],
        de=dict(
            q="Warum ist eine unerwartete Fahrbahnunebenheit oder ein Schlagloch in Schräglage gefährlicher als bei aufrechter Fahrt?",
            o={
                "a": "Weil in Schräglage der Reifenaufstandspunkt seitlich versetzt liegt und schon geringe Grip-Reduzierung durch die Unebenheit den ohnehin reduzierten seitlichen Kraftschluss übersteigen kann",
                "b": "Weil Schlaglöcher in Schräglage optisch schwerer erkennbar sind, technisch aber keinen Unterschied machen",
                "c": "Weil das Motorrad in Schräglage grundsätzlich langsamer fährt und Unebenheiten deshalb härter spürbar sind",
                "d": "Weil in Schräglage automatisch das ABS deaktiviert wird",
            },
            e="In Schräglage trägt der Reifen bereits einen Teil des Kraftschlusses für die Kurvenkraft. Eine plötzliche Unebenheit kann die Aufstandsfläche kurzzeitig verkleinern oder den Grip reduzieren - reicht die verbleibende Haftung nicht mehr für die notwendige Seitenkraft, rutscht das Rad weg. Deshalb sind unbekannte Streckenabschnitte in Schräglage besonders vorsichtig zu befahren.",
        ),
        en=dict(
            q="Why is an unexpected road surface irregularity or pothole more dangerous while leaned over than while riding upright?",
            o={
                "a": "Because while leaned over the contact patch sits off to the side, so even a small grip reduction from the irregularity can exceed the already-reduced lateral grip reserve",
                "b": "Because potholes are visually harder to spot while leaned over, but make no technical difference otherwise",
                "c": "Because a motorcycle always rides slower while leaned over, so bumps are simply felt harder",
                "d": "Because ABS is automatically disabled while leaned over",
            },
            e="While leaned over, the tyre already commits part of its grip to cornering force. A sudden irregularity can briefly shrink the contact patch or reduce grip - if the remaining traction can no longer supply the needed lateral force, the wheel slides out. That is why unfamiliar stretches of road should be ridden with extra caution while leaned over.",
        ),
    ),
    dict(
        id="motorrad-fahrphysik-27", topic="Fahrphysik und Balance", topic_code="fahrphysik",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["d"],
        de=dict(
            q="Was bewirkt Beschleunigen (Gas geben) auf gerader Strecke in Bezug auf die Fahrstabilität eines Motorrads typischerweise?",
            o={
                "a": "Es macht das Motorrad grundsätzlich instabiler als Bremsen",
                "b": "Es hat keinerlei Einfluss auf die Radlastverteilung",
                "c": "Es verlagert die Last zusätzlich auf das Vorderrad",
                "d": "Es verlagert Last auf das Hinterrad und erhöht dadurch tendenziell dessen Grip, während das Vorderrad entlastet wird",
            },
            e="Beim Beschleunigen wirkt die Trägheit in die Gegenrichtung zum Bremsen: die Masse 'drückt' nach hinten, wodurch sich die dynamische Achslast auf das Hinterrad verlagert. Das erhöht tendenziell dessen Kraftschluss für den Antrieb, entlastet aber gleichzeitig das Vorderrad, was dessen Lenkpräzision verringern kann.",
        ),
        en=dict(
            q="What effect does accelerating (opening the throttle) on a straight typically have on a motorcycle's ride stability?",
            o={
                "a": "It always makes the motorcycle less stable than braking does",
                "b": "It has no effect at all on wheel load distribution",
                "c": "It shifts additional load onto the front wheel",
                "d": "It shifts load onto the rear wheel and tends to increase its grip, while the front wheel is unloaded",
            },
            e="Accelerating produces inertia acting opposite to braking: the mass 'pushes' rearward, shifting dynamic axle load onto the rear wheel. This tends to increase rear-wheel traction for drive power, but simultaneously unloads the front wheel, which can reduce steering precision.",
        ),
    ),

    # =========================================================
    # schutzausruestung (16-27): helmet standards, ATGATT
    # =========================================================
    dict(
        id="motorrad-schutzausruestung-16", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§21a Abs. 2 StVO (Schutzhelmpflicht)",
        points=4, high_stakes=True, correct=["c"],
        de=dict(
            q="Wer ist nach § 21a Abs. 2 StVO grundsätzlich verpflichtet, während der Fahrt einen geeigneten Schutzhelm zu tragen?",
            o={
                "a": "Nur der Fahrer, Beifahrer sind ausgenommen",
                "b": "Nur bei Fahrten außerorts, innerorts besteht keine Helmpflicht",
                "c": "Wer Krafträder oder offene drei- oder mehrrädrige Kraftfahrzeuge mit einer bauartbedingten Höchstgeschwindigkeit von über 20 km/h führt sowie darauf oder darin mitfährt",
                "d": "Nur Fahrer von Krafträdern über 125 cm³",
            },
            e="§ 21a Abs. 2 StVO verpflichtet alle Personen, die Krafträder oder offene drei-/vierrädrige Kraftfahrzeuge mit einer bauartbedingten Höchstgeschwindigkeit über 20 km/h führen oder darauf mitfahren, während der Fahrt einen geeigneten Schutzhelm zu tragen - das schließt Beifahrer ausdrücklich mit ein und gilt unabhängig von der Hubraumklasse und vom Streckentyp.",
        ),
        en=dict(
            q="Under § 21a(2) StVO, who is generally required to wear a suitable protective helmet while riding?",
            o={
                "a": "Only the rider; passengers are exempt",
                "b": "Only outside built-up areas; there is no helmet requirement within towns",
                "c": "Anyone riding or being carried on motorcycles or open three-/four-wheeled motor vehicles with a design top speed above 20 km/h",
                "d": "Only riders of motorcycles over 125cc",
            },
            e="§ 21a(2) StVO requires everyone riding or being carried on motorcycles or open three-/four-wheeled motor vehicles with a design top speed above 20 km/h to wear a suitable protective helmet while riding - this explicitly includes passengers and applies regardless of engine displacement class or road type.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-17", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§21a Abs. 2 StVO (Schutzhelmpflicht)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Ab welcher bauartbedingten Höchstgeschwindigkeit greift die Schutzhelmpflicht nach § 21a Abs. 2 StVO für offene drei- oder mehrrädrige Kraftfahrzeuge und Krafträder?",
            o={
                "a": "Über 20 km/h",
                "b": "Über 45 km/h",
                "c": "Über 50 km/h",
                "d": "Über 60 km/h",
            },
            e="Die Helmpflicht knüpft an eine bauartbedingte Höchstgeschwindigkeit von über 20 km/h an. Damit sind praktisch alle motorisierten Zweiräder, auch langsame Mofas über dieser Schwelle, erfasst - nicht erst ab 45 km/h, wo die versicherungskennzeichenpflichtige Klasse beginnt.",
        ),
        en=dict(
            q="At what design top speed does the helmet requirement under § 21a(2) StVO apply to open three-/four-wheeled motor vehicles and motorcycles?",
            o={
                "a": "Above 20 km/h",
                "b": "Above 45 km/h",
                "c": "Above 50 km/h",
                "d": "Above 60 km/h",
            },
            e="The helmet requirement is tied to a design top speed above 20 km/h. This covers practically all motorised two-wheelers above that threshold, including slower mopeds - not only from 45 km/h, which is where the insurance-plate-required class begins.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-18", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§21a Abs. 2 StVO i. V. m. anerkannten Prüfnormen für Schutzhelme",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Was bedeutet der Begriff 'ATGATT' als Grundprinzip der Motorradschutzausrüstung?",
            o={
                "a": "Ein technischer Standard für Helmschalen aus Karbon",
                "b": "'All The Gear, All The Time' - das Prinzip, bei jeder Fahrt, auch kurzen Strecken, immer die vollständige Schutzausrüstung (Helm, Jacke, Handschuhe, Hose, Stiefel) zu tragen",
                "c": "Eine gesetzliche Kennzeichnungspflicht für Motorradbekleidung nach StVZO",
                "d": "Eine Bezeichnung für die Kombination aus ABS und Traktionskontrolle",
            },
            e="ATGATT ('All The Gear, All The Time') ist kein gesetzlicher Begriff, sondern ein in der Motorradsicherheit etabliertes Verhaltensprinzip: vollständige Schutzausrüstung konsequent bei jeder Fahrt zu tragen, weil Stürze auch auf kurzen, vertrauten Strecken passieren und die meisten Verletzungen bei Stürzen ohne vollständige Schutzkleidung entstehen.",
        ),
        en=dict(
            q="What does the term 'ATGATT' mean as a core principle of motorcycle protective gear?",
            o={
                "a": "A technical standard for carbon-fibre helmet shells",
                "b": "'All The Gear, All The Time' - the principle of always wearing complete protective gear (helmet, jacket, gloves, trousers, boots) on every ride, even short ones",
                "c": "A statutory labelling requirement for motorcycle clothing under StVZO",
                "d": "A term for the combination of ABS and traction control",
            },
            e="ATGATT ('All The Gear, All The Time') is not a legal term but an established motorcycle-safety behavioural principle: consistently wearing full protective gear on every ride, since crashes also happen on short, familiar routes, and most crash injuries occur when full protective clothing is not worn.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-19", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§21a Abs. 2 StVO i. V. m. anerkannten Prüfnormen für Schutzhelme",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Was ist ein 'geeigneter Schutzhelm' im Sinne von § 21a Abs. 2 StVO im Regelfall NICHT?",
            o={
                "a": "Ein Integralhelm mit geschlossenem Kinnbügel",
                "b": "Ein Jethelm mit offenem Gesichtsfeld",
                "c": "Ein reiner Fahrradhelm oder eine Bau-/Schutzkappe ohne Prüfzeichen für den motorisierten Zweiradverkehr",
                "d": "Ein Klapphelm mit hochklappbarem Kinnteil",
            },
            e="Als 'geeignet' gelten grundsätzlich Helme mit anerkanntem Prüfzeichen für den Einsatz auf Krafträdern (z. B. entsprechend ECE-Regelung Nr. 22). Fahrradhelme oder Bauhelme sind für die im Straßenverkehr mit Krafträdern auftretenden Belastungen nicht ausgelegt und geprüft und erfüllen die Anforderung nicht.",
        ),
        en=dict(
            q="Which of the following is generally NOT a 'suitable protective helmet' within the meaning of § 21a(2) StVO?",
            o={
                "a": "A full-face helmet with a fixed chin bar",
                "b": "An open-face (jet) helmet",
                "c": "A plain bicycle helmet or a construction hard hat with no approval mark for motorised two-wheeler use",
                "d": "A flip-up (modular) helmet with a lift-up chin bar",
            },
            e="A 'suitable' helmet is generally one carrying a recognised approval mark for motorcycle use (e.g. under ECE Regulation No. 22). Bicycle helmets or construction hard hats are neither designed nor tested for the impact forces occurring in motorcycle road traffic and do not meet the requirement.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-20", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="anerkannte Prüfnormen für Schutzhelme (ECE-Regelung Nr. 22)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Wofür steht die ECE-Regelung Nr. 22 (in ihrer aktuellen Fassung 22.06) im Zusammenhang mit Motorradhelmen?",
            o={
                "a": "Für eine EU-Vorschrift zur maximalen Helmfarbe",
                "b": "Für einen international anerkannten Prüfstandard, den Schutzhelme für Kraftradfahrer bestehen müssen, um als straßenverkehrstauglich zu gelten",
                "c": "Für die maximale zulässige Geschwindigkeit, bei der ein Helm getragen werden muss",
                "d": "Für eine Herstellergarantiepflicht von zehn Jahren",
            },
            e="Die ECE-Regelung Nr. 22 ist ein international anerkannter technischer Prüfstandard für Kraftradhelme (Stoßdämpfung, Durchdringungsschutz, Kinnriemenfestigkeit, Sichtfeld u. a.). Helme mit gültigem ECE-22-Prüfzeichen gelten regelmäßig als 'geeignete' Schutzhelme im Sinne von § 21a Abs. 2 StVO.",
        ),
        en=dict(
            q="What is ECE Regulation No. 22 (currently in its 22.06 revision) in relation to motorcycle helmets?",
            o={
                "a": "An EU rule about the maximum permitted helmet colour",
                "b": "An internationally recognised technical approval standard that motorcycle helmets must pass to be considered road-legal",
                "c": "The maximum speed at which a helmet must be worn",
                "d": "A mandatory ten-year manufacturer warranty requirement",
            },
            e="ECE Regulation No. 22 is an internationally recognised technical test standard for motorcycle helmets (impact absorption, penetration resistance, chin-strap strength, field of vision, among others). Helmets carrying a valid ECE 22 approval mark are generally regarded as 'suitable' helmets within the meaning of § 21a(2) StVO.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-21", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht), Empfehlung nach anerkannten Sicherheitsstandards",
        points=2, high_stakes=False, correct=["a"],
        de=dict(
            q="Warum wird empfohlen, Motorradhandschuhe mit verstärktem Knöchel- und Handballenschutz zu tragen, auch wenn dafür keine ausdrückliche gesetzliche Pflicht besteht?",
            o={
                "a": "Weil bei Stürzen reflexartig die Hände zuerst aufkommen und Handverletzungen zu den häufigsten und oft folgenreichsten Sturzverletzungen bei Motorradfahrern zählen",
                "b": "Weil ohne Handschuhe der Kupplungshebel technisch nicht bedient werden kann",
                "c": "Weil Handschuhe gesetzlich vorgeschriebene Blinksignale ersetzen",
                "d": "Weil sie die Bremsleistung des Motorrads verbessern",
            },
            e="Bei einem Sturz stützen sich Fahrer reflexartig mit den Händen ab, wodurch Handflächen, Handballen und Fingerknöchel besonders sturzgefährdet sind. Auch ohne ausdrückliche gesetzliche Handschuhpflicht (anders als beim Helm) gehören Motorradhandschuhe mit Protektoren daher zur allgemein empfohlenen Schutzausrüstung.",
        ),
        en=dict(
            q="Why is it recommended to wear motorcycle gloves with reinforced knuckle and palm protection, even though there is no explicit statutory requirement to do so?",
            o={
                "a": "Because in a crash, riders instinctively brace with their hands first, making hand injuries among the most common and often most consequential crash injuries",
                "b": "Because the clutch lever cannot technically be operated without gloves",
                "c": "Because gloves legally replace turn-signal indicators",
                "d": "Because they improve the motorcycle's braking performance",
            },
            e="In a fall, riders instinctively brace themselves with their hands, making palms, the heel of the hand, and finger knuckles especially prone to injury. Even without an explicit statutory glove requirement (unlike the helmet), reinforced motorcycle gloves are therefore part of generally recommended protective gear.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-22", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Was ist der Hauptzweck von Protektoren (Schulter-, Ellbogen-, Rücken-, Knieprotektoren) in Motorradbekleidung?",
            o={
                "a": "Sie verbessern die Aerodynamik bei hohen Geschwindigkeiten",
                "b": "Sie ersetzen die Notwendigkeit eines Schutzhelms an diesen Körperstellen",
                "c": "Sie verteilen und dämpfen Aufprallenergie beim Sturz und Rutschen über Asphalt, um Prellungen, Knochenbrüche und Weichteilverletzungen an besonders belasteten Gelenken zu reduzieren",
                "d": "Sie dienen ausschließlich der besseren Sichtbarkeit bei Nacht",
            },
            e="Protektoren aus stoßdämpfendem Material verteilen die beim Aufprall und anschließenden Rutschen über den Asphalt entstehenden Kräfte auf eine größere Fläche und dämpfen Spitzenbelastungen ab, wodurch das Risiko von Brüchen, Prellungen und Abschürfungen an besonders exponierten Gelenken deutlich sinkt.",
        ),
        en=dict(
            q="What is the primary purpose of protectors (shoulder, elbow, back, knee protectors) in motorcycle clothing?",
            o={
                "a": "They improve aerodynamics at high speeds",
                "b": "They remove the need for a helmet at those body locations",
                "c": "They spread and cushion impact energy during a crash and subsequent slide across asphalt, reducing bruising, fractures, and soft-tissue injuries at particularly exposed joints",
                "d": "They serve solely to improve night-time visibility",
            },
            e="Impact-absorbing protectors spread the forces generated during impact and the subsequent slide across asphalt over a larger area and cushion peak loads, significantly reducing the risk of fractures, bruising, and abrasions at particularly exposed joints.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-23", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht - Sichtbarkeit im Verkehr)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum wird für Motorradfahrer helle oder retroreflektierende Kleidung besonders empfohlen, obwohl das Motorrad selbst tagsüber mit Licht fahren muss?",
            o={
                "a": "Weil dunkle Kleidung gesetzlich für Motorräder verboten ist",
                "b": "Weil ein Motorrad wegen seiner geringen Frontfläche für andere Verkehrsteilnehmer, insbesondere abbiegende Autofahrer, deutlich schwerer und später wahrzunehmen ist als ein Pkw - helle/reflektierende Kleidung erhöht die Erkennbarkeit zusätzlich zum Licht",
                "c": "Weil helle Kleidung die Bremsleistung verbessert",
                "d": "Weil reflektierende Kleidung offiziell den Schutzhelm ersetzen darf",
            },
            e="Ein Motorrad bietet aus der Fahrzeugfront gesehen eine viel kleinere Silhouette als ein Auto und wird deshalb von anderen Verkehrsteilnehmern - vor allem bei Abbiege- und Einfädelvorgängen - später oder gar nicht wahrgenommen ('Looked but failed to see'). Helle oder retroreflektierende Kleidung erhöht den Kontrast zur Umgebung und verbessert die Erkennbarkeit zusätzlich zum ohnehin vorgeschriebenen Tageslicht.",
        ),
        en=dict(
            q="Why is bright or retroreflective clothing especially recommended for motorcyclists, even though the motorcycle itself must run with its lights on during the day?",
            o={
                "a": "Because dark clothing is legally prohibited for motorcyclists",
                "b": "Because a motorcycle's small frontal silhouette makes it considerably harder and slower for other road users - especially turning drivers - to notice than a car; bright/reflective clothing improves conspicuity in addition to the running lights",
                "c": "Because bright clothing improves braking performance",
                "d": "Because reflective clothing may officially replace the protective helmet",
            },
            e="Seen head-on, a motorcycle presents a much smaller silhouette than a car and is therefore often noticed later or not at all by other road users - especially in turning and merging situations ('looked but failed to see'). Bright or retroreflective clothing increases contrast against the surroundings and improves conspicuity in addition to the already-mandatory daytime running lights.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-24", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§21a Abs. 2 StVO (Schutzhelmpflicht)",
        points=3, high_stakes=True, correct=["d"],
        de=dict(
            q="Ein Kinnriemen eines Integralhelms ist locker eingestellt, sodass sich der Helm mit der Hand deutlich nach vorn über die Stirn schieben lässt. Welche Aussage trifft zu?",
            o={
                "a": "Das ist unbedenklich, solange der Helm optisch korrekt sitzt",
                "b": "Das betrifft nur den Komfort, nicht die Schutzwirkung",
                "c": "Ein locker sitzender Helm erfüllt automatisch trotzdem die Anforderung von § 21a Abs. 2 StVO, solange irgendein Helm getragen wird",
                "d": "Ein zu locker sitzender Helm kann sich bei einem Sturz vom Kopf lösen oder verrutschen und damit seinen Schutzzweck verfehlen - er ist dann kein 'geeigneter' Schutzhelm im Sinne der Vorschrift mehr",
            },
            e="Die Schutzwirkung eines Helms hängt entscheidend vom korrekten Sitz und einem fest geschlossenen Kinnriemen ab. Ein zu locker eingestellter Helm kann sich beim Sturz lösen oder so verrutschen, dass er den Kopf nicht mehr wirksam schützt - er erfüllt dann die Anforderung an einen 'geeigneten' Schutzhelm faktisch nicht mehr, selbst wenn er formal getragen wird.",
        ),
        en=dict(
            q="A full-face helmet's chin strap is adjusted loosely enough that the helmet can be pushed forward off the forehead by hand. Which statement is correct?",
            o={
                "a": "This is harmless as long as the helmet visually appears to be worn correctly",
                "b": "This only affects comfort, not the protective effect",
                "c": "A loosely fitted helmet still automatically satisfies § 21a(2) StVO as long as some helmet is being worn",
                "d": "A helmet fitted too loosely can come off or shift during a crash and thereby fail its protective purpose - it effectively no longer counts as a 'suitable' helmet under the rule",
            },
            e="A helmet's protective effect crucially depends on a correct fit and a securely fastened chin strap. A helmet adjusted too loosely can come off or shift during a crash so that it no longer effectively protects the head - it then effectively fails to meet the requirement of being a 'suitable' helmet, even if it is nominally being worn.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-25", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["a"],
        de=dict(
            q="Warum ist geeignetes, robustes Schuhwerk (Motorradstiefel statt z. B. Sandalen) beim Motorradfahren wichtig?",
            o={
                "a": "Weil Füße und Knöchel bei einem Sturz oder Umkippen besonders exponiert sind und Motorradstiefel Knöchel, Schienbein und Fußballen zusätzlich vor Verbrennungen (heiße Auspuffteile) und mechanischen Verletzungen schützen",
                "b": "Weil Sandalen gesetzlich für alle Fahrzeugklassen verboten sind",
                "c": "Weil Stiefel die Motorleistung technisch beeinflussen",
                "d": "Weil offene Schuhe automatisch zum Verlust der Fahrerlaubnis führen",
            },
            e="Füße und Unterschenkel sind bei Stürzen, beim Abstützen an Kreuzungen oder beim Umfallen des Motorrads besonders gefährdet - zusätzlich drohen Verbrennungen an heißen Motor-/Auspuffteilen. Knöchelhohe, robuste Motorradstiefel bieten hier deutlich besseren Schutz als offenes oder niedriges Schuhwerk.",
        ),
        en=dict(
            q="Why is suitable, sturdy footwear (motorcycle boots rather than, e.g., sandals) important when riding?",
            o={
                "a": "Because feet and ankles are especially exposed in a crash or tip-over, and motorcycle boots additionally protect the ankle, shin, and forefoot from burns (hot exhaust parts) and mechanical injury",
                "b": "Because sandals are legally prohibited for all vehicle classes",
                "c": "Because boots technically affect engine power",
                "d": "Because open footwear automatically results in loss of the driving licence",
            },
            e="Feet and lower legs are especially at risk in crashes, when bracing at junctions, or if the motorcycle tips over - and there is an additional risk of burns from hot engine/exhaust parts. Sturdy, ankle-high motorcycle boots offer significantly better protection here than open or low-cut footwear.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-26", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Welche Aussage zur Lebensdauer/Ersatzpflicht eines Motorradhelms nach einem nennenswerten Sturz trifft zu?",
            o={
                "a": "Ein Helm hält technisch unbegrenzt und muss nie ersetzt werden",
                "b": "Ein Helm sollte nach einem nennenswerten Aufprall oder Sturz grundsätzlich ersetzt werden, da die stoßdämpfende Innenschale meist irreversibel komprimiert wird, auch wenn äußerlich keine Schäden sichtbar sind",
                "c": "Nur die Außenschale kann nach einem Sturz separat ausgetauscht werden, der Rest bleibt gleich",
                "d": "Ein Ersatz ist nur bei sichtbaren Rissen in der Außenschale nötig",
            },
            e="Die stoßdämpfende Innenschale (meist aus EPS-Hartschaum) vieler Helme ist für einen einzigen wirksamen Aufprall ausgelegt und wird dabei mikroskopisch komprimiert - oft ohne äußerlich sichtbare Schäden. Nach einem nennenswerten Sturz oder Stoß ist die Schutzwirkung deshalb in der Regel deutlich reduziert, weshalb Hersteller und Sicherheitsexperten einen Ersatz empfehlen.",
        ),
        en=dict(
            q="Which statement about a motorcycle helmet's lifespan/need for replacement after a significant impact is correct?",
            o={
                "a": "A helmet technically lasts indefinitely and never needs replacing",
                "b": "A helmet should generally be replaced after a significant impact or crash, since the energy-absorbing inner shell is usually compressed irreversibly, even if no external damage is visible",
                "c": "Only the outer shell can be swapped out separately after a crash, with the rest staying the same",
                "d": "Replacement is only necessary if visible cracks appear in the outer shell",
            },
            e="The energy-absorbing inner liner (typically hard EPS foam) in most helmets is designed to absorb a single significant impact effectively, and is microscopically compressed in doing so - often with no visible external damage. Its protective performance is therefore usually significantly reduced after a notable crash or impact, which is why manufacturers and safety experts recommend replacement.",
        ),
    ),
    dict(
        id="motorrad-schutzausruestung-27", topic="Schutzausrüstung und Sichtbarkeit", topic_code="schutzausruestung",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Warum ist stark abgefahrenes, poröses oder verkratztes Helmvisier ein Sicherheitsproblem, auch wenn der Helm selbst noch intakt ist?",
            o={
                "a": "Es hat keinen Einfluss auf die Sicherheit, nur auf die Optik",
                "b": "Es verringert ausschließlich den Wiederverkaufswert des Helms",
                "c": "Es kann die Sicht bei Blendung durch Gegenlicht (z. B. tiefstehende Sonne, entgegenkommende Scheinwerfer) erheblich verschlechtern und die Reaktionszeit auf Gefahren verlängern",
                "d": "Es macht den Kinnriemen automatisch unwirksam",
            },
            e="Ein zerkratztes oder trübes Visier streut einfallendes Licht stärker und kann bei Blendsituationen - etwa tiefstehende Sonne oder entgegenkommendes Fernlicht - die Sicht erheblich beeinträchtigen. Dadurch werden Gefahren später erkannt und die verfügbare Reaktionszeit verkürzt, weshalb ein beschädigtes Visier rechtzeitig ersetzt werden sollte.",
        ),
        en=dict(
            q="Why is a badly scratched, pitted, or hazy helmet visor a safety concern even if the helmet shell itself is still intact?",
            o={
                "a": "It has no effect on safety, only on appearance",
                "b": "It only reduces the helmet's resale value",
                "c": "It can significantly worsen visibility when glared by backlight (e.g. low sun, oncoming headlights) and lengthen reaction time to hazards",
                "d": "It automatically renders the chin strap ineffective",
            },
            e="A scratched or hazy visor scatters incoming light more strongly and can significantly impair vision in glare situations - such as low sun or oncoming high-beam headlights. This delays hazard recognition and shortens the available reaction time, which is why a damaged visor should be replaced promptly.",
        ),
    ),

    # =========================================================
    # verkehrsverhalten (16-27): hazard perception, filtering,
    # blind spots, group riding
    # =========================================================
    dict(
        id="motorrad-verkehrsverhalten-16", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Was ist mit 'Gefahrenlebrung' bzw. vorausschauender Gefahrenerkennung (Hazard Perception) im Motorradverkehr in erster Linie gemeint?",
            o={
                "a": "Nur das Erkennen von amtlichen Gefahrenzeichen nach StVO",
                "b": "Das aktive, kontinuierliche Absuchen der Verkehrssituation nach Anzeichen für mögliche Gefahren, bevor diese akut werden - etwa ein parkendes Auto mit besetztem Fahrersitz, aus dem gleich eine Tür geöffnet werden könnte",
                "c": "Das Abwarten, bis eine Gefahr bereits eingetreten ist, und erst dann zu reagieren",
                "d": "Eine Funktion moderner Motorrad-Assistenzsysteme, die der Fahrer nicht selbst ausführen muss",
            },
            e="Gefahrenerkennung bedeutet, die Verkehrsumgebung aktiv nach Frühwarnzeichen abzusuchen - z. B. Bremslichter weit voraus, eine sich öffnende Autotür, ein Kind am Straßenrand, spiegelndes Licht, das auf Nässe hindeutet - und die eigene Fahrweise (Tempo, Position, Blick) bereits anzupassen, bevor aus dem Anzeichen eine akute Gefahr wird. Diese Fähigkeit ist besonders für Motorradfahrer entscheidend, da sie ungeschützter und schwerer sichtbar sind.",
        ),
        en=dict(
            q="What does 'hazard perception' primarily mean in the context of motorcycle riding?",
            o={
                "a": "Only recognising official hazard warning signs under the StVO",
                "b": "Actively and continuously scanning the traffic situation for early signs of potential danger before they become acute - e.g. a parked car with someone in the driver's seat who might open the door",
                "c": "Waiting until a hazard has already occurred, and only reacting then",
                "d": "A function of modern motorcycle rider-assistance systems that the rider no longer needs to perform",
            },
            e="Hazard perception means actively scanning the traffic environment for early warning signs - e.g. brake lights far ahead, a car door starting to open, a child near the roadside, reflective glare suggesting a wet surface - and adjusting your own riding (speed, position, gaze) before a sign turns into an acute danger. This skill is especially critical for motorcyclists, who are more exposed and harder for others to see.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-17", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Warum sind Kreuzungen und Einmündungen für Motorradfahrer statistisch besonders unfallträchtig?",
            o={
                "a": "Weil dort grundsätzlich höhere Geschwindigkeiten gefahren werden dürfen",
                "b": "Weil Motorräder an Kreuzungen technisch schlechter bremsen können",
                "c": "Weil andere Verkehrsteilnehmer - vor allem abbiegende oder einfahrende Fahrzeugführer - ein Motorrad wegen seiner geringen Frontfläche und Geschwindigkeit oft übersehen oder dessen Geschwindigkeit falsch einschätzen ('looked but failed to see')",
                "d": "Weil an Kreuzungen grundsätzlich keine Vorfahrtsregeln gelten",
            },
            e="Ein häufiges Unfallmuster ist, dass ein wartepflichtiger Fahrzeugführer beim Abbiegen oder Einfahren in eine Straße den Verkehr zwar visuell absucht, ein herannahendes Motorrad aber wegen seiner schmalen Silhouette und der oft unterschätzten Annäherungsgeschwindigkeit übersieht oder zu spät erkennt. Motorradfahrer sollten sich an Kreuzungen deshalb möglichst sichtbar positionieren, Blickkontakt suchen und bremsbereit sein.",
        ),
        en=dict(
            q="Why are junctions and intersections statistically especially crash-prone for motorcyclists?",
            o={
                "a": "Because higher speeds are generally permitted there",
                "b": "Because motorcycles technically brake worse at junctions",
                "c": "Because other road users - especially drivers turning or entering the road - often overlook a motorcycle due to its small frontal profile and misjudge its speed ('looked but failed to see')",
                "d": "Because right-of-way rules generally do not apply at junctions",
            },
            e="A common crash pattern is that a yielding driver turning or entering a road visually scans traffic but overlooks or spots too late an approaching motorcycle, because of its narrow silhouette and an often-underestimated closing speed. Motorcyclists should therefore try to position themselves visibly at junctions, seek eye contact, and stay ready to brake.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-18", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO, §5 StVO (Überholen)",
        points=4, high_stakes=True, correct=["c"],
        de=dict(
            q="Ist es in Deutschland erlaubt, mit dem Motorrad zwischen stehenden oder langsam fahrenden Fahrzeugkolonnen 'durchzufahren' (Filtern/Lane-Splitting), wie es in manchen anderen Ländern zulässig ist?",
            o={
                "a": "Ja, uneingeschränkt, solange das Motorrad nicht schneller als 30 km/h fährt",
                "b": "Ja, aber nur auf Autobahnen",
                "c": "Nein, das deutsche Recht kennt kein generelles Filtern zwischen Fahrspuren; ein Vorbeifahren an einer Fahrzeugkolonne innerhalb derselben Fahrspur bzw. mit zu geringem Seitenabstand kann als unzulässiges Überholen oder als Verstoß gegen das Rechtsfahrgebot gewertet werden",
                "d": "Ja, weil Motorräder generell von der Fahrspurpflicht ausgenommen sind",
            },
            e="Anders als z. B. in einigen US-Bundesstaaten oder Frankreich gibt es in Deutschland keine gesetzliche Grundlage, die das reguläre Filtern zwischen Fahrspuren im Stau erlaubt. Ein Vorbeifahren innerhalb der Fahrspur mit zu geringem Sicherheitsabstand zu den Fahrzeugen kann als riskantes, unzulässiges Verhalten geahndet werden - erlaubt ist lediglich das reguläre Überholen unter Einhaltung der allgemeinen Überholvorschriften (Fahrspurwechsel, ausreichender Abstand, kein Überholen bei unklarer Verkehrslage).",
        ),
        en=dict(
            q="Is it legal in Germany to ride a motorcycle 'through' stopped or slow-moving lines of traffic between lanes (filtering/lane-splitting), as is permitted in some other countries?",
            o={
                "a": "Yes, without restriction, as long as the motorcycle stays under 30 km/h",
                "b": "Yes, but only on motorways",
                "c": "No, German law does not recognise general lane-filtering between traffic lanes; passing a line of vehicles within the same lane or with insufficient side clearance can be treated as unlawful overtaking or a violation of the keep-right rule",
                "d": "Yes, because motorcycles are generally exempt from the lane-discipline requirement",
            },
            e="Unlike, for example, some US states or France, German law has no legal basis permitting routine lane-filtering in traffic jams. Passing within a lane with insufficient safety clearance to the vehicles around you can be penalised as risky, unlawful conduct - only regular overtaking, following the general overtaking rules (lane change, adequate clearance, no overtaking in unclear traffic situations), is permitted.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-19", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO, §4 StVO (Abstand)",
        points=3, high_stakes=True, correct=["a"],
        de=dict(
            q="Warum sollten Motorradfahrer innerhalb ihrer eigenen Fahrspur bewusst eine seitlich versetzte Position wählen (z. B. links oder rechts in der Spur statt in der Mitte)?",
            o={
                "a": "Um besser in die Fahrzeuge vor ihnen hineinsehen zu können (bessere Sicht auf Gefahren voraus) und für nachfolgende sowie kreuzende Fahrzeuge besser sichtbar zu sein, während gleichzeitig ein Fluchtraum zur Seite erhalten bleibt",
                "b": "Weil das Fahren in der Fahrspurmitte gesetzlich verboten ist",
                "c": "Weil dadurch automatisch die zulässige Höchstgeschwindigkeit steigt",
                "d": "Nur aus optischen bzw. stilistischen Gründen, sicherheitsrelevant ist die Position nicht",
            },
            e="Eine leicht versetzte Position innerhalb der eigenen Fahrspur kann die Sichtlinie um vorausfahrende Fahrzeuge herum verbessern, erhöht die eigene Sichtbarkeit im Rückspiegel anderer Fahrzeuge und lässt seitlichen Ausweichraum. Die genaue Position sollte situativ (Fahrbahnzustand, Wind, Sichtverhältnisse, andere Verkehrsteilnehmer) gewählt werden, nicht starr in der Spurmitte gefahren werden.",
        ),
        en=dict(
            q="Why should motorcyclists deliberately choose an offset position within their own lane (e.g. toward the left or right rather than dead centre)?",
            o={
                "a": "To see further into and around the vehicles ahead (better view of hazards ahead) and to be more visible to following and crossing traffic, while keeping an escape space to the side",
                "b": "Because riding in the centre of the lane is legally prohibited",
                "c": "Because it automatically raises the permitted maximum speed",
                "d": "Purely for visual/stylistic reasons; lane position has no safety relevance",
            },
            e="A slightly offset position within your own lane can improve sightlines around vehicles ahead, increases your visibility in other drivers' mirrors, and leaves lateral escape space. The exact position should be chosen situationally (road surface, wind, visibility, other traffic) rather than always riding dead-centre in the lane.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-20", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Warum ist der 'tote Winkel' von Lkw und Bussen für Motorradfahrer besonders gefährlich?",
            o={
                "a": "Weil Motorräder in diesem Bereich technisch nicht bremsen können",
                "b": "Weil ein Motorrad wegen seiner geringen Größe im toten Winkel großer Fahrzeuge häufig vollständig unsichtbar für Spiegel und Kamerasysteme wird, obwohl der Fahrer des großen Fahrzeugs meint, ausreichend geschaut zu haben",
                "c": "Weil sich der tote Winkel bei Motorrädern grundsätzlich vergrößert",
                "d": "Weil der tote Winkel nur bei Nachtfahrten relevant ist",
            },
            e="Der tote Winkel bezeichnet Bereiche neben und hinter einem Fahrzeug, die weder direkt noch über die Spiegel eingesehen werden können. Ein vergleichsweise kleines Motorrad kann in diesem Bereich, insbesondere neben Lkw und Bussen, vollständig verschwinden - der Fahrer des großen Fahrzeugs sieht es also selbst bei sorgfältigem Blick in die Spiegel nicht. Motorradfahrer sollten sich deshalb möglichst nicht längere Zeit im toten Winkel großer Fahrzeuge aufhalten.",
        ),
        en=dict(
            q="Why is the 'blind spot' of trucks and buses especially dangerous for motorcyclists?",
            o={
                "a": "Because motorcycles technically cannot brake while in that zone",
                "b": "Because a motorcycle's small size means it can become completely invisible to a large vehicle's mirrors and camera systems within its blind spot, even though that driver believes they've looked carefully",
                "c": "Because the blind spot is always larger for motorcycles specifically",
                "d": "Because blind spots are only relevant at night",
            },
            e="The blind spot refers to areas beside and behind a vehicle that cannot be seen either directly or via the mirrors. A relatively small motorcycle can disappear entirely within that zone, especially alongside trucks and buses - the large vehicle's driver simply cannot see it, even when checking mirrors carefully. Motorcyclists should therefore avoid lingering in large vehicles' blind spots for extended periods.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-21", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Welche gefährliche Verhaltensweise vieler Autofahrer beim Abbiegen wird häufig als Erklärung für Kollisionen mit entgegenkommenden Motorrädern genannt?",
            o={
                "a": "Autofahrer fahren beim Linksabbiegen grundsätzlich zu langsam",
                "b": "Autofahrer schalten beim Abbiegen die Warnblinkanlage zu früh ein",
                "c": "Der Autofahrer schätzt die Annäherungsgeschwindigkeit des kleineren, schmaleren Motorrads falsch ein oder übersieht es zwischen anderen Fahrzeugen und biegt links ab, obwohl das Motorrad noch nicht durch ist",
                "d": "Autofahrer dürfen an Kreuzungen grundsätzlich nicht mehr links abbiegen",
            },
            e="Ein wiederkehrendes Unfallmuster ist das Linksabbiegen eines entgegenkommenden Autos vor einem sich nähernden Motorrad: Die geringere Silhouette und teils unterschätzte Annäherungsgeschwindigkeit von Motorrädern führen dazu, dass Autofahrer die verbleibende Zeitlücke falsch einschätzen oder das Motorrad zwischen anderen Fahrzeugen schlicht übersehen.",
        ),
        en=dict(
            q="Which dangerous behaviour by many drivers when turning is often cited as an explanation for collisions with oncoming motorcycles?",
            o={
                "a": "Drivers generally turn left too slowly",
                "b": "Drivers turn on their hazard lights too early when turning",
                "c": "The driver misjudges the closing speed of the smaller, narrower motorcycle or overlooks it among other vehicles, and turns left even though the motorcycle has not yet passed",
                "d": "Drivers are generally no longer allowed to turn left at intersections",
            },
            e="A recurring crash pattern is an oncoming car turning left in front of an approaching motorcycle: the motorcycle's smaller silhouette and its frequently underestimated closing speed lead drivers to misjudge the remaining time gap, or simply overlook the motorcycle among other traffic.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-22", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO, §4 StVO (Abstand)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Wie sollte bei gemeinsamem Fahren in einer Motorradgruppe der Sicherheitsabstand zwischen den Fahrern grundsätzlich gestaltet werden?",
            o={
                "a": "Jeder Fahrer hält selbst einen ausreichenden Abstand zum Vordermann ein, der genügend Reaktions- und Bremsweg lässt; ein versetztes Fahren (gestaffelte Formation) statt Fahren direkt hintereinander kann zusätzlich die Sicht nach vorn und die Sichtbarkeit für andere Verkehrsteilnehmer verbessern",
                "b": "Alle Fahrer der Gruppe müssen exakt im gleichen Abstand wie im Straßenverkehrsrecht für Lkw-Kolonnen hintereinanderfahren",
                "c": "Der Abstand ist irrelevant, solange die Gruppe insgesamt langsamer fährt als der übrige Verkehr",
                "d": "Nur der letzte Fahrer der Gruppe muss auf Abstand achten, die übrigen orientieren sich ausschließlich am Gruppenführer",
            },
            e="Auch in der Gruppe gilt für jeden Fahrer individuell die Pflicht zu ausreichendem Sicherheitsabstand entsprechend Tempo und Bedingungen. Eine gestaffelte, leicht versetzte Fahrformation statt strikt hintereinander verbessert oft die gegenseitige Sicht und die Sichtbarkeit für andere Verkehrsteilnehmer, ersetzt aber nicht den erforderlichen Bremswegabstand.",
        ),
        en=dict(
            q="How should the safety distance between riders generally be handled when riding together as a motorcycle group?",
            o={
                "a": "Each rider individually maintains sufficient distance to the rider ahead to allow adequate reaction and braking distance; riding in a staggered formation rather than directly in line can additionally improve forward visibility and conspicuity to other road users",
                "b": "All riders in the group must follow each other at the exact spacing prescribed by road traffic law for truck convoys",
                "c": "Spacing is irrelevant as long as the group as a whole rides slower than the surrounding traffic",
                "d": "Only the last rider in the group needs to watch spacing; the others rely entirely on the group leader",
            },
            e="Even within a group, each rider individually is required to maintain sufficient safety distance appropriate to speed and conditions. A staggered, slightly offset riding formation rather than strict single file often improves mutual visibility and conspicuity to other road users, but it does not replace the required braking-distance spacing.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-23", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum sollte man sich beim Fahren in einer Motorradgruppe nicht ausschließlich auf die Bremslichter des unmittelbaren Vordermanns verlassen?",
            o={
                "a": "Weil Bremslichter bei Motorrädern generell zu schwach sind, um überhaupt erkannt zu werden",
                "b": "Weil so eine Verzögerung des vorderen Fahrers erst spät wahrgenommen wird; ein Blick auch auf weiter vorausliegende Fahrzeuge und die Gesamtverkehrslage ermöglicht ein früheres, ruhigeres Reagieren als reines 'Draufstarren' auf ein einzelnes Rücklicht",
                "c": "Weil das gesetzlich verboten ist",
                "d": "Weil in Gruppen grundsätzlich keine Bremslichter benutzt werden dürfen",
            },
            e="Wer den Blick starr auf das Rücklicht des Vordermanns richtet, reagiert erst, wenn dieser bereits bremst - und damit relativ spät. Ein weiter vorausschauender Blick auf die gesamte Verkehrssituation vor der Gruppe erlaubt es, Bremsmanöver frühzeitig zu antizipieren und ruhiger, mit größerem Sicherheitsabstand zu reagieren.",
        ),
        en=dict(
            q="Why should you not rely solely on the brake light of the rider directly ahead when riding in a motorcycle group?",
            o={
                "a": "Because motorcycle brake lights are generally too dim to be noticed at all",
                "b": "Because that only reveals the rider ahead's deceleration relatively late; also scanning further ahead and the overall traffic situation allows earlier, calmer reactions than fixating on a single tail light",
                "c": "Because it is legally prohibited",
                "d": "Because brake lights may not be used at all when riding in groups",
            },
            e="Fixating on the rider ahead's tail light means you only react once that rider is already braking - relatively late. Looking further ahead at the overall traffic situation in front of the group makes it possible to anticipate braking manoeuvres earlier and react more calmly, with a larger safety margin.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-24", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=False, correct=["a"],
        de=dict(
            q="Was bedeutet die Fahrtechnik-Empfehlung, den Blick beim Fahren weit vorauszulegen, statt sich auf das unmittelbar Vorausliegende zu konzentrieren?",
            o={
                "a": "Frühzeitig weit voraus die Verkehrssituation, Fahrbahnzustand und mögliche Gefahrenquellen zu erfassen, damit genug Zeit bleibt, die Fahrweise rechtzeitig und ruhig anzupassen, statt erst im letzten Moment reagieren zu müssen",
                "b": "Ausschließlich geradeaus in die Ferne zu blicken und die nähere Umgebung zu ignorieren",
                "c": "Den Blick fest auf den eigenen Tacho zu richten, um die Geschwindigkeit exakt zu kontrollieren",
                "d": "Nur bei Nachtfahrten relevant, tagsüber spielt die Blickführung keine Rolle",
            },
            e="Ein weit vorausschauender Blick - kombiniert mit regelmäßigem Absuchen der näheren Umgebung und der Spiegel - verschafft mehr Zeit, um Gefahren frühzeitig zu erkennen und die Fahrweise (Tempo, Position, Bremsbereitschaft) rechtzeitig anzupassen, statt erst im letzten Moment abrupt reagieren zu müssen.",
        ),
        en=dict(
            q="What does the riding-technique recommendation to look far ahead, rather than focusing on the immediate road surface, actually mean?",
            o={
                "a": "Reading the traffic situation, road surface condition, and potential hazards early and far ahead, so there is enough time to adjust your riding calmly and in good time instead of reacting only at the last moment",
                "b": "Looking only straight into the distance and ignoring the nearby surroundings entirely",
                "c": "Fixing your gaze on the speedometer to control speed precisely",
                "d": "Only relevant at night; gaze direction plays no role during the day",
            },
            e="Looking far ahead - combined with regularly scanning the closer surroundings and mirrors - gives more time to spot hazards early and adjust your riding (speed, position, readiness to brake) in good time, instead of having to react abruptly at the last moment.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-25", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Welche Fahrbahnstellen bergen für Motorradfahrer ein erhöhtes Rutschrisiko, das Autofahrer oft kaum wahrnehmen?",
            o={
                "a": "Ausschließlich frisch geteerte Fahrbahnabschnitte",
                "b": "Nur Bereiche mit sichtbarem Schnee oder Eis",
                "c": "Fahrbahnmarkierungen, Kanaldeckel, Straßenbahnschienen und Splitt-/Ölspuren, insbesondere bei Nässe, da sie deutlich weniger Grip bieten als normaler Asphalt, für einen Autofahrer mit vier Reifen aber meist unbemerkt bleiben",
                "d": "Ausschließlich unbefestigte Feldwege",
            },
            e="Fahrbahnmarkierungen, Metalloberflächen wie Kanaldeckel oder Straßenbahnschienen sowie Splitt- oder Ölspuren bieten deutlich weniger Grip, besonders bei Nässe. Ein Auto mit vier Reifen kompensiert das meist unbemerkt, während ein Motorrad mit nur zwei, schmaleren Kontaktflächen dort leicht die Haftung verlieren kann - besonders kritisch in Schräglage.",
        ),
        en=dict(
            q="Which road surface features carry an elevated slip risk for motorcyclists that drivers of cars often barely notice?",
            o={
                "a": "Only freshly laid asphalt sections",
                "b": "Only areas with visible snow or ice",
                "c": "Road markings, manhole covers, tram rails, and patches of gravel or oil, especially when wet, since they offer significantly less grip than normal asphalt but usually go unnoticed by a driver on four tyres",
                "d": "Only unpaved farm tracks",
            },
            e="Road markings, metal surfaces such as manhole covers or tram rails, and patches of gravel or oil offer significantly less grip, especially when wet. A car on four tyres usually compensates for this unnoticed, whereas a motorcycle with only two, narrower contact patches can easily lose traction there - particularly critical while leaned over.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-26", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=3, high_stakes=False, correct=["b"],
        de=dict(
            q="Warum ist es sinnvoll, beim Herannahen an eine Kreuzung oder Einmündung regelmäßig auch in die Rückspiegel zu schauen, nicht nur nach vorn?",
            o={
                "a": "Weil die Straßenverkehrsordnung dies für jede Kreuzung ausdrücklich als Blinkpflicht vorschreibt",
                "b": "Um zu wissen, wie dicht nachfolgender Verkehr auffährt, damit man auf ein plötzliches, notwendiges Abbremsen vorbereitet ist und ggf. eine Vollbremsung angepasst dosieren oder ausweichen kann",
                "c": "Weil dadurch automatisch die Bremswirkung des Motorrads verbessert wird",
                "d": "Nur relevant bei Fahrten auf der Autobahn",
            },
            e="Wer weiß, wie dicht der nachfolgende Verkehr auffährt, kann eine notwendige Bremsung angepasst dosieren - etwa vorsichtiger einleiten, wenn ein dicht auffahrendes Fahrzeug sonst auffahren könnte - oder rechtzeitig nach einem Ausweichraum suchen. Der regelmäßige Blick in die Spiegel ist deshalb Teil der vorausschauenden Fahrweise, nicht nur eine reine Formalität.",
        ),
        en=dict(
            q="Why is it useful to regularly check the mirrors as well as looking ahead when approaching a junction or intersection?",
            o={
                "a": "Because the traffic regulations explicitly require checking mirrors as part of a signalling duty at every junction",
                "b": "To know how closely following traffic is riding, so you're prepared for a sudden, necessary braking manoeuvre and can dose a possible emergency stop appropriately or look for an escape route",
                "c": "Because it automatically improves the motorcycle's braking performance",
                "d": "Only relevant on motorways",
            },
            e="Knowing how closely following traffic is riding lets you dose a necessary braking manoeuvre appropriately - e.g. braking more gently at first if a tailgating vehicle might otherwise rear-end you - or find an escape route in time. Regularly checking the mirrors is therefore part of anticipatory riding, not just a formality.",
        ),
    ),
    dict(
        id="motorrad-verkehrsverhalten-27", topic="Verkehrsverhalten für Kraftradfahrer", topic_code="verkehrsverhalten",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht)",
        points=2, high_stakes=False, correct=["d"],
        de=dict(
            q="Ein parkendes Auto am Fahrbahnrand hat den Motor laufen und im Innenspiegel ist die Silhouette einer Person auf dem Fahrersitz zu erkennen. Wie sollte ein Motorradfahrer darauf im Sinne vorausschauender Gefahrenerkennung reagieren?",
            o={
                "a": "Ignorieren, solange sich die Fahrertür nicht bereits öffnet",
                "b": "Die Geschwindigkeit erhöhen, um den Bereich möglichst schnell zu passieren",
                "c": "Nur relevant, wenn das Auto ein Taxi ist",
                "d": "Das Fahrzeug als potenzielle Gefahrenquelle einstufen (plötzlich öffnende Tür, Anfahren in den Verkehr), rechtzeitig mehr seitlichen Abstand halten und die Geschwindigkeit leicht reduzieren, um Reaktionszeit zu gewinnen",
            },
            e="Anzeichen wie ein laufender Motor oder eine erkennbare Person im Fahrersitz eines parkenden Autos sind klassische Frühwarnzeichen für ein mögliches plötzliches Türöffnen oder Anfahren. Vorausschauendes Fahren bedeutet, solche Anzeichen frühzeitig zu erkennen und die eigene Position und Geschwindigkeit entsprechend anzupassen, statt erst zu reagieren, wenn die Gefahr bereits eingetreten ist.",
        ),
        en=dict(
            q="A parked car at the roadside has its engine running, and the silhouette of a person is visible in the driver's seat via the mirror. How should a motorcyclist respond, applying anticipatory hazard perception?",
            o={
                "a": "Ignore it, as long as the driver's door has not already opened",
                "b": "Increase speed to pass the area as quickly as possible",
                "c": "This is only relevant if the car is a taxi",
                "d": "Treat the vehicle as a potential hazard (sudden door opening, pulling out into traffic), allow extra lateral clearance in good time, and slightly reduce speed to gain reaction time",
            },
            e="Signs such as a running engine or a visible person in the driver's seat of a parked car are classic early-warning signs of a possible sudden door opening or pulling away. Anticipatory riding means recognising such signs early and adjusting your own position and speed accordingly, rather than reacting only once the hazard has already materialised.",
        ),
    ),

    # =========================================================
    # fahrerlaubnis (16-27): technical pre-ride checks
    # =========================================================
    dict(
        id="motorrad-fahrerlaubnis-16", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§1 StVO (allgemeine Sorgfaltspflicht), §23 StVZO (Zustand der Fahrzeuge)",
        points=3, high_stakes=True, correct=["c"],
        de=dict(
            q="Was ist der Sinn einer technischen Sichtprüfung des Motorrads vor Fahrtantritt, wie sie z. B. nach dem Prinzip 'Reifen, Kontrollen, Beleuchtung, Öl/Flüssigkeiten, Kette/Antrieb, Ständer' erfolgen kann?",
            o={
                "a": "Sie ist rein optional und dient ausschließlich der Motorpflege",
                "b": "Sie ersetzt die regelmäßige Hauptuntersuchung (HU) vollständig",
                "c": "Sie soll offensichtliche technische Mängel (z. B. platter Reifen, defektes Licht, lockere Kette, zu wenig Öl) erkennen, bevor sie während der Fahrt zu einer akuten Gefahr werden",
                "d": "Sie ist nur bei Motorrädern über 125 cm³ gesetzlich vorgeschrieben",
            },
            e="Ein systematischer Kurzcheck vor jeder Fahrt (häufig in Anlehnung an das aus dem angelsächsischen Raum bekannte 'T-CLOCS'-Schema: Tires, Controls, Lights, Oil, Chassis, Stands) soll offensichtliche technische Mängel frühzeitig erkennen, bevor sie unterwegs zu einer akuten Gefahrensituation werden - etwa ein zu geringer Reifendruck, ein Ausfall der Bremslichter oder eine zu lockere Antriebskette.",
        ),
        en=dict(
            q="What is the purpose of a technical visual check of a motorcycle before riding off, such as one following a 'tyres, controls, lights, oil/fluids, chain/drive, stands' checklist?",
            o={
                "a": "It is purely optional and serves only cosmetic engine maintenance",
                "b": "It completely replaces the regular periodic technical inspection (HU)",
                "c": "It is meant to catch obvious technical defects (e.g. a flat tyre, a broken light, a loose chain, low oil) before they become an acute danger while riding",
                "d": "It is legally required only for motorcycles over 125cc",
            },
            e="A systematic quick check before every ride (often following the widely known 'T-CLOCS' scheme: Tires, Controls, Lights, Oil, Chassis, Stands) is meant to catch obvious technical defects early, before they become an acute hazard on the road - for example, low tyre pressure, a failed brake light, or a chain that is too loose.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-17", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Warum ist die Kontrolle des Reifendrucks vor Fahrtantritt beim Motorrad besonders wichtig?",
            o={
                "a": "Weil der Reifendruck rein optisch von Auge zuverlässig geschätzt werden kann",
                "b": "Weil falscher Reifendruck (zu niedrig oder zu hoch) die Kontaktfläche des Reifens und damit Grip, Fahrstabilität und Bremsverhalten deutlich verschlechtern kann, und dies bei nur zwei Rädern viel unmittelbarer wirkt als bei einem vierrädrigen Fahrzeug",
                "c": "Weil Reifendruck ausschließlich die Höchstgeschwindigkeit begrenzt",
                "d": "Weil der Reifendruck keinen Einfluss auf die Fahrsicherheit hat, solange die Reifen nicht platt sind",
            },
            e="Der optimale Reifendruck ist entscheidend für Kontaktfläche, Grip und Wärmeentwicklung des Reifens. Bei einem Motorrad mit nur zwei, schmaleren Reifen wirkt sich eine Abweichung viel unmittelbarer auf Fahrstabilität, Kurvenverhalten und Bremsweg aus als bei einem Auto - der Reifendruck lässt sich zudem nicht zuverlässig durch bloßes Ansehen einschätzen und sollte vor der Fahrt mit einem Manometer geprüft werden.",
        ),
        en=dict(
            q="Why is checking tyre pressure before setting off especially important on a motorcycle?",
            o={
                "a": "Because tyre pressure can be reliably estimated just by looking at the tyre",
                "b": "Because incorrect tyre pressure (too low or too high) can significantly worsen the tyre's contact patch and thus grip, ride stability, and braking behaviour, and this effect is far more immediate with only two wheels than with a four-wheeled vehicle",
                "c": "Because tyre pressure only limits top speed",
                "d": "Because tyre pressure has no effect on riding safety as long as the tyres aren't flat",
            },
            e="Correct tyre pressure is crucial for contact patch size, grip, and heat build-up in the tyre. On a motorcycle with only two, narrower tyres, a deviation affects ride stability, cornering behaviour, and stopping distance far more directly than on a car - and pressure cannot be reliably judged by eye, so it should be checked with a gauge before riding.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-18", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Was sollte bei der Kontrolle der Antriebskette (bei kettengetriebenen Motorrädern) vor der Fahrt beachtet werden?",
            o={
                "a": "Die Kette muss immer straff durchgespannt sein, jegliches Spiel ist ein Defekt",
                "b": "Die Kette benötigt keinerlei Wartung, solange sie nicht sichtbar rostet",
                "c": "Ein angemessenes, herstellerseitig festgelegtes Spiel sowie ausreichende Schmierung sind wichtig; eine zu straffe oder zu lockere, trockene Kette kann zu erhöhtem Verschleiß, ruckartiger Kraftübertragung oder im Extremfall zum Abspringen der Kette führen",
                "d": "Kettenspiel ist ausschließlich für den Kraftstoffverbrauch relevant",
            },
            e="Antriebsketten benötigen ein herstellerseitig definiertes Spiel und regelmäßige Schmierung. Zu straff gespannte Ketten belasten Ritzel und Getriebe übermäßig, zu lockere oder trockene Ketten können ruckartige Kraftübertragung verursachen, schneller verschleißen oder sich im Extremfall lösen - mit direkter Auswirkung auf die Fahrsicherheit.",
        ),
        en=dict(
            q="What should be checked about a drive chain (on chain-driven motorcycles) before riding?",
            o={
                "a": "The chain must always be pulled taut; any slack at all indicates a defect",
                "b": "The chain needs no maintenance at all as long as it isn't visibly rusty",
                "c": "Appropriate, manufacturer-specified slack and adequate lubrication matter; a chain that is too tight or too loose and dry can cause increased wear, jerky power delivery, or in extreme cases the chain coming off",
                "d": "Chain slack is only relevant to fuel consumption",
            },
            e="Drive chains require a manufacturer-specified amount of slack and regular lubrication. Chains pulled too tight overstress the sprockets and gearbox, while chains that are too loose or dry can cause jerky power delivery, wear faster, or in extreme cases come off - directly affecting riding safety.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-19", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§17 StVO (Beleuchtung), §23 StVZO",
        points=2, high_stakes=False, correct=["a"],
        de=dict(
            q="Warum sollte vor Fahrtantritt geprüft werden, ob Brems-, Blink- und Rücklicht funktionieren?",
            o={
                "a": "Weil andere Verkehrsteilnehmer Bremsabsicht, Abbiegeabsicht und die Anwesenheit des Motorrads maßgeblich über diese Lichtsignale erkennen - ein Ausfall verzögert oder verhindert deren rechtzeitige Reaktion",
                "b": "Weil defekte Lichter die Motorleistung verringern",
                "c": "Weil die Lichtprüfung ausschließlich bei der Hauptuntersuchung relevant ist",
                "d": "Weil Blinker in Deutschland rein optional sind, solange Handzeichen gegeben werden",
            },
            e="Bremslicht, Blinker und Rücklicht sind für andere Verkehrsteilnehmer die zentralen Signale, um Bremsabsicht, Richtungsänderung und die Position des Motorrads - besonders bei Dämmerung oder Dunkelheit - zu erkennen. Ein defektes Licht kann dazu führen, dass nachfolgende oder kreuzende Fahrzeuge zu spät oder falsch reagieren.",
        ),
        en=dict(
            q="Why should you check before riding whether the brake light, turn signals, and tail light are working?",
            o={
                "a": "Because other road users primarily recognise braking intent, turning intent, and the motorcycle's presence through these light signals - a failure delays or prevents their timely reaction",
                "b": "Because faulty lights reduce engine power",
                "c": "Because light checks are only relevant during the periodic technical inspection",
                "d": "Because turn signals are purely optional in Germany as long as hand signals are given",
            },
            e="The brake light, turn signals, and tail light are the primary way other road users recognise braking intent, a change of direction, and the motorcycle's presence - especially at dusk or in the dark. A faulty light can cause following or crossing traffic to react too late or incorrectly.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-20", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=3, high_stakes=True, correct=["b"],
        de=dict(
            q="Wie prüft man vor der Fahrt grob, ob genügend Bremsflüssigkeit im Bremssystem vorhanden ist und die Bremse funktionsfähig erscheint?",
            o={
                "a": "Der Flüssigkeitsstand ist irrelevant, solange der Bremshebel sich überhaupt bewegen lässt",
                "b": "Sichtprüfung des Flüssigkeitsstands im Ausgleichsbehälter (zwischen Min-/Max-Markierung) sowie ein Prüfgriff des Bremshebels: er sollte einen spürbaren Druckpunkt haben und nicht bis zum Lenkergriff durchziehbar sein",
                "c": "Ausschließlich durch Hören eines Warntons beim Starten",
                "d": "Nur durch eine Probefahrt mit hoher Geschwindigkeit feststellbar",
            },
            e="Ein kurzer Blick auf den Flüssigkeitsstand im Ausgleichsbehälter der hydraulischen Bremse (sollte zwischen Min- und Max-Markierung liegen) und ein Prüfgriff am Bremshebel - er sollte spürbaren Widerstand mit klarem Druckpunkt bieten und sich nicht komplett bis zum Lenker durchziehen lassen - geben erste Hinweise auf die Funktionsfähigkeit der Bremse, ersetzen aber keine fachgerechte Wartung.",
        ),
        en=dict(
            q="How can you roughly check before riding whether there is enough brake fluid in the braking system and the brake feels functional?",
            o={
                "a": "The fluid level is irrelevant as long as the brake lever moves at all",
                "b": "A visual check of the fluid level in the reservoir (between the min/max marks) plus a test squeeze of the brake lever: it should have a firm, noticeable pressure point and not pull all the way back to the grip",
                "c": "Only by listening for a warning tone on start-up",
                "d": "Only by doing a high-speed test ride",
            },
            e="A quick look at the fluid level in the hydraulic brake's reservoir (should sit between the min and max marks) and a test squeeze of the brake lever - it should offer noticeable resistance with a clear pressure point and not pull all the way back to the handlebar - give an initial indication of brake function, but do not replace proper professional servicing.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-21", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Was ist bei der Sichtprüfung des Motorölstands vor Fahrtantritt zu beachten?",
            o={
                "a": "Der Ölstand ist nur bei Zweitaktmotoren relevant",
                "b": "Der Motor muss beim Prüfen des Ölstands immer laufen",
                "c": "Der Ölstand sollte im vom Hersteller angegebenen Bereich (z. B. am Schauglas oder Peilstab) liegen; zu wenig Öl kann zu unzureichender Schmierung und Motorschäden führen, zu viel Öl kann den Motor ebenfalls schädigen",
                "d": "Der Ölstand kann problemlos ignoriert werden, solange keine Warnlampe leuchtet",
            },
            e="Der Motorölstand sollte regelmäßig - meist am Schauglas oder Peilstab, je nach Herstellervorgabe bei kaltem oder betriebswarmem, meist stehendem Motor - kontrolliert werden. Sowohl zu wenig als auch zu viel Öl kann den Motor schädigen; ein korrekter Stand im angegebenen Bereich ist Voraussetzung für ausreichende Schmierung.",
        ),
        en=dict(
            q="What should be checked when visually inspecting the engine oil level before riding off?",
            o={
                "a": "The oil level is only relevant for two-stroke engines",
                "b": "The engine must always be running while checking the oil level",
                "c": "The oil level should sit within the manufacturer-specified range (e.g. on the sight glass or dipstick); too little oil can cause insufficient lubrication and engine damage, and too much oil can also damage the engine",
                "d": "The oil level can be safely ignored as long as no warning light is illuminated",
            },
            e="Engine oil level should be checked regularly - usually via the sight glass or dipstick, following the manufacturer's specification for cold or warm engine and whether the bike should be upright or on its stand. Both too little and too much oil can damage the engine; a correct level within the specified range is a prerequisite for adequate lubrication.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-22", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=3, high_stakes=True, correct=["d"],
        de=dict(
            q="Warum ist es wichtig, vor dem Losfahren zu prüfen, ob der Seiten- oder Hauptständer vollständig eingeklappt ist?",
            o={
                "a": "Weil ein ausgeklappter Ständer die Motorleistung drosselt",
                "b": "Weil ein ausgeklappter Ständer gesetzlich mit einem Bußgeld geahndet wird, auch ohne konkrete Gefahr",
                "c": "Weil ein ausgeklappter Ständer die Sicht auf den Tacho verdeckt",
                "d": "Weil ein nicht vollständig eingeklappter Seitenständer beim Einlenken in eine Kurve auf der jeweiligen Seite den Boden berühren und dadurch abrupt Grip verlieren bzw. das Hinterrad anheben kann, was zu einem plötzlichen Sturz führen kann",
            },
            e="Ein nicht vollständig eingeklappter Seitenständer kann bereits bei moderater Schräglage aufsetzen. Der dabei entstehende Hebel kann das Hinterrad kurzzeitig vom Boden abheben oder zu einem abrupten Blockieren/Wegrutschen führen - viele Motorräder verfügen deshalb über einen Seitenständerschalter, der die Zündung unterbricht, solange ein Gang eingelegt und der Ständer ausgeklappt ist.",
        ),
        en=dict(
            q="Why is it important to check before setting off that the side or centre stand is fully retracted?",
            o={
                "a": "Because an extended stand throttles engine power",
                "b": "Because an extended stand is legally subject to a fine even without any actual danger arising",
                "c": "Because an extended stand blocks the view of the speedometer",
                "d": "Because a not-fully-retracted side stand can touch the ground when leaning into a corner on that side, abruptly losing grip or lifting the rear wheel, which can cause a sudden crash",
            },
            e="A not-fully-retracted side stand can touch down even at moderate lean angles. The resulting leverage can briefly lift the rear wheel off the ground or cause it to abruptly lock/slide - which is why many motorcycles have a side-stand cut-off switch that interrupts ignition while a gear is engaged and the stand is extended.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-23", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Was sollte bei der Sichtprüfung des Reifenprofils vor der Fahrt beachtet werden?",
            o={
                "a": "Nur die Reifenfarbe ist relevant, das Profil spielt keine Rolle",
                "b": "Das Profil muss die gesetzliche Mindestprofiltiefe deutlich überschreiten, und es sollte auf gleichmäßigen Verschleiß, Fremdkörper (z. B. Nägel), Risse oder Ausbeulungen in der Reifenflanke geachtet werden - insbesondere Ausbeulungen deuten auf eine gefährliche Karkassenbeschädigung hin",
                "c": "Ein Reifen ist erst dann zu prüfen, wenn er sichtbar platt ist",
                "d": "Profiltiefe ist nur beim TÜV relevant, nicht für die tägliche Fahrt",
            },
            e="Neben ausreichender Profiltiefe (deutlich über der gesetzlichen Mindesttiefe, da Motorradreifen bei geringer Resttiefe besonders schnell an Grip verlieren) sollte auf gleichmäßigen Abrieb, eingefahrene Fremdkörper, Risse im Gummi und vor allem Ausbeulungen in der Reifenflanke geachtet werden - letztere deuten auf eine beschädigte, potenziell reißgefährdete Karkasse hin und erfordern sofortigen Reifenwechsel.",
        ),
        en=dict(
            q="What should be checked during a visual inspection of tyre tread before riding?",
            o={
                "a": "Only tyre colour matters; tread has no relevance",
                "b": "The tread should clearly exceed the legal minimum depth, and you should look for uneven wear, embedded foreign objects (e.g. nails), cracks, or bulges in the sidewall - bulges in particular indicate dangerous carcass damage",
                "c": "A tyre only needs checking once it is visibly flat",
                "d": "Tread depth is only relevant at the periodic inspection, not for everyday riding",
            },
            e="Besides adequate tread depth (well above the legal minimum, since motorcycle tyres lose grip especially quickly once tread runs low), you should check for uneven wear, embedded foreign objects, cracks in the rubber, and above all bulges in the sidewall - the latter indicate a damaged, potentially failing carcass and call for immediate tyre replacement.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-24", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=2, high_stakes=False, correct=["a"],
        de=dict(
            q="Warum sollten Lenker, Bremshebel und Kupplungshebel vor Fahrtantritt kurz auf festen Sitz und Leichtgängigkeit geprüft werden?",
            o={
                "a": "Weil ein lockerer Lenkerkopf, verbogene Hebel oder schwergängige Betätigungselemente die präzise Kontrolle über Lenkung, Bremsung und Kupplung im Fahrbetrieb beeinträchtigen können",
                "b": "Weil das gesetzlich für jede Fahrt zu Protokoll genommen werden muss",
                "c": "Weil dadurch die Höchstgeschwindigkeit des Motorrads bestimmt wird",
                "d": "Weil ein lockerer Lenker automatisch die Beleuchtung ausschaltet",
            },
            e="Lenkung, Bremshebel und Kupplungshebel sind zentrale Bedienelemente. Ein lockerer Lenkerkopf, verbogene oder klemmende Hebel oder ausgeschlagene Lager können die präzise, unmittelbare Kontrolle über Lenkung und Bremsung genau in dem Moment beeinträchtigen, in dem sie am wichtigsten ist - eine kurze Sichtprüfung mit Funktionsgriff vor der Fahrt kann solche Mängel frühzeitig aufdecken.",
        ),
        en=dict(
            q="Why should the handlebars, brake lever, and clutch lever be briefly checked for secure mounting and smooth operation before riding off?",
            o={
                "a": "Because a loose steering head, bent levers, or stiff controls can impair precise control over steering, braking, and clutch operation while riding",
                "b": "Because this must legally be logged in writing before every ride",
                "c": "Because this determines the motorcycle's top speed",
                "d": "Because a loose handlebar automatically switches off the lights",
            },
            e="Steering, brake lever, and clutch lever are core control elements. A loose steering head, bent or sticking levers, or worn bearings can impair precise, immediate control over steering and braking at exactly the moment it matters most - a brief visual and functional check before riding can catch such defects early.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-25", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge), §17 StVO",
        points=2, high_stakes=False, correct=["c"],
        de=dict(
            q="Warum sollten Spiegel vor Fahrtantritt korrekt eingestellt und auf festen Sitz geprüft werden, obwohl sie technisch nicht direkt zur Fortbewegung nötig sind?",
            o={
                "a": "Weil falsch eingestellte Spiegel automatisch ein Verkehrszeichen auslösen",
                "b": "Weil Spiegel ausschließlich der Kosmetik dienen und keine sicherheitsrelevante Funktion haben",
                "c": "Weil korrekt eingestellte, feste Spiegel die einzige praktikable Möglichkeit sind, den rückwärtigen und seitlichen Verkehr - insbesondere im toten Winkel relevante, sich annähernde Fahrzeuge - rechtzeitig wahrzunehmen, bevor ein Spurwechsel oder Abbiegen erfolgt",
                "d": "Weil sie bei jeder Fahrt neu am Lenker montiert werden müssen",
            },
            e="Da ein Motorradfahrer sich nur eingeschränkt umdrehen kann, sind gut eingestellte, fest sitzende Spiegel die wichtigste Informationsquelle über den rückwärtigen Verkehr. Verrutschte oder locker sitzende Spiegel liefern während der Fahrt ein unzuverlässiges oder falsches Bild und erhöhen das Risiko, ein herannahendes Fahrzeug zu übersehen.",
        ),
        en=dict(
            q="Why should mirrors be correctly adjusted and checked for a secure mount before riding off, even though they are not technically required for propulsion?",
            o={
                "a": "Because incorrectly adjusted mirrors automatically trigger a traffic sign",
                "b": "Because mirrors are purely cosmetic and have no safety-relevant function",
                "c": "Because correctly adjusted, securely mounted mirrors are the only practical way to notice traffic behind and to the side in time - including blind-spot-relevant approaching vehicles - before changing lanes or turning",
                "d": "Because they must be remounted on the handlebars before every ride",
            },
            e="Since a motorcyclist has only limited ability to turn and look back, well-adjusted, securely mounted mirrors are the primary source of information about traffic behind. Mirrors that have shifted or are loosely mounted give an unreliable or distorted picture while riding and increase the risk of overlooking an approaching vehicle.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-26", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=2, high_stakes=False, correct=["b"],
        de=dict(
            q="Was ist bei der Kontrolle des Kühlmittelstands vor der Fahrt bei einem flüssigkeitsgekühlten Motorrad zu beachten (falls vorhanden)?",
            o={
                "a": "Kühlmittelstand ist irrelevant, solange der Motor überhaupt anspringt",
                "b": "Der Stand sollte im Ausgleichsbehälter zwischen Min-/Max-Markierung liegen; ein zu niedriger Stand kann bei längerer Fahrt zu Überhitzung und Motorschäden führen",
                "c": "Kühlmittel muss vor jeder Fahrt komplett neu aufgefüllt werden",
                "d": "Ein niedriger Kühlmittelstand betrifft ausschließlich den Kraftstoffverbrauch",
            },
            e="Bei flüssigkeitsgekühlten Motoren sollte der Kühlmittelstand im Ausgleichsbehälter regelmäßig kontrolliert werden (üblicherweise zwischen Min- und Max-Markierung bei kaltem Motor). Ein zu niedriger Stand kann die Kühlleistung beeinträchtigen und bei längerer oder anstrengender Fahrt (z. B. im Stau, bei Hitze) zu Überhitzung und in der Folge zu Motorschäden führen.",
        ),
        en=dict(
            q="What should be checked about coolant level before riding a liquid-cooled motorcycle (where fitted)?",
            o={
                "a": "Coolant level is irrelevant as long as the engine starts at all",
                "b": "The level should sit between the min/max marks on the reservoir; too low a level can lead to overheating and engine damage on a longer ride",
                "c": "Coolant must be completely refilled before every single ride",
                "d": "A low coolant level only affects fuel consumption",
            },
            e="On liquid-cooled engines, the coolant level in the reservoir should be checked regularly (usually between the min and max marks with the engine cold). Too low a level can impair cooling performance and, during a longer or demanding ride (e.g. in traffic jams or hot weather), lead to overheating and consequent engine damage.",
        ),
    ),
    dict(
        id="motorrad-fahrerlaubnis-27", topic="Fahrerlaubnisklassen und technische Besonderheiten", topic_code="fahrerlaubnis",
        legal_basis="§23 StVZO (Zustand der Fahrzeuge)",
        points=3, high_stakes=False, correct=["d"],
        de=dict(
            q="Warum wird empfohlen, einen technischen Pre-Ride-Check nach einem festen Schema (z. B. immer in derselben Reihenfolge: Reifen, Bedienelemente, Licht, Flüssigkeiten, Fahrwerk/Rahmen, Ständer) durchzuführen, statt spontan und unsystematisch?",
            o={
                "a": "Weil ein festes Schema gesetzlich für jede einzelne Fahrt vorgeschrieben ist und dokumentiert werden muss",
                "b": "Weil ein festes Schema die Fahrzeit verkürzt",
                "c": "Weil nur ein festes Schema von der Zulassungsstelle anerkannt wird",
                "d": "Weil ein wiederkehrendes, systematisches Vorgehen die Wahrscheinlichkeit deutlich verringert, einen einzelnen wichtigen Prüfpunkt aus Gewohnheit oder Zeitdruck zu vergessen, verglichen mit einer jedes Mal unterschiedlichen, spontanen Kontrolle",
            },
            e="Ein systematisches, immer gleich ablaufendes Prüfschema (wie das bekannte T-CLOCS-Prinzip) nutzt den Vorteil von Routine: Wird jeder Punkt in derselben Reihenfolge abgearbeitet, sinkt die Wahrscheinlichkeit, unter Zeitdruck oder aus Gewohnheit einen sicherheitsrelevanten Punkt zu übersehen, deutlich gegenüber einer unsystematischen, spontanen Kontrolle.",
        ),
        en=dict(
            q="Why is it recommended to run a technical pre-ride check using a fixed sequence (e.g. always in the same order: tyres, controls, lights, fluids, chassis/frame, stands) rather than spontaneously and unsystematically?",
            o={
                "a": "Because a fixed sequence is legally required and must be documented before every single ride",
                "b": "Because a fixed sequence shortens ride time",
                "c": "Because only a fixed sequence is recognised by the vehicle registration authority",
                "d": "Because a recurring, systematic routine significantly reduces the chance of forgetting a single important check point out of habit or time pressure, compared with an unsystematic, spontaneous check that differs every time",
            },
            e="A systematic checklist run in the same order every time (like the well-known T-CLOCS principle) exploits the benefit of routine: working through each point in the same sequence significantly lowers the chance of overlooking a safety-relevant item under time pressure or out of habit, compared with an unsystematic, spontaneous check.",
        ),
    ),
]


def build():
    pilot = json.load(open(PILOT_PATH, encoding="utf-8"))
    existing_ids = {q["id"] for q in pilot["questions"]}

    new_pilot_questions = []
    per_locale_new = {"de": {}, "en": {}}

    for q in NEW_QUESTIONS:
        if q["id"] in existing_ids:
            raise SystemExit(f"Duplicate id detected, aborting: {q['id']}")
        pilot_q = dict(
            id=q["id"], topic=q["topic"], topic_code=q["topic_code"],
            class_scope=["A1", "A2", "A"], grundstoff=True, legal_basis=q["legal_basis"],
            points=q["points"], high_stakes=q["high_stakes"],
            question_type="single_choice", image_ref=None, correct=q["correct"],
        )
        pilot_q["text"] = {
            "de": {"question": q["de"]["q"], "options": q["de"]["o"]},
            "en": {"question": q["en"]["q"], "options": q["en"]["o"]},
        }
        pilot_q["explanation"] = {"de": q["de"]["e"], "en": q["en"]["e"]}
        new_pilot_questions.append(pilot_q)

        per_locale_new["de"][q["id"]] = {"question": q["de"]["q"], "options": q["de"]["o"], "explanation": q["de"]["e"]}
        per_locale_new["en"][q["id"]] = {"question": q["en"]["q"], "options": q["en"]["o"], "explanation": q["en"]["e"]}

    # 1) update master pilot file IN PLACE: append new questions, bump total_questions/generated
    pilot["questions"].extend(new_pilot_questions)
    pilot["meta"]["total_questions"] = len(pilot["questions"])
    pilot["meta"]["generated"] = "2026-08-12"
    pilot["meta"]["description"] = (
        pilot["meta"]["description"]
        + " DN-65 Zusatzstoff expansion (2026-08-12): +48 questions extending the existing "
          "fahrphysik/schutzausruestung/verkehrsverhalten/fahrerlaubnis topics with hazard "
          "perception, lean/countersteering physics, ABS/CBS braking-distribution awareness, "
          "helmet-standard/ATGATT protective-gear content, motorcycle-specific traffic scenarios "
          "(filtering legality, blind spots, group riding), and technical pre-ride checks. Sourced "
          "from SS 6 FeV (A1/A2/A class definitions), Anlage 7/7b FeV (Fahrerschulung structure), "
          "SS 21a Abs. 2 StVO (Schutzhelmpflicht), and EU-VO 168/2013 (ABS/CBS braking-equipment "
          "rules), plus established motorcycle-safety/riding-physics knowledge. New questions are "
          "DE/EN only for this round, same as the rest of this app's newest content."
    )
    json.dump(pilot, open(PILOT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 2) regenerate ONLY app/data/motorrad/ - core.json + locales/*.json for all
    #    declared locales, using the (now-updated) full pilot as source of truth.
    module_dir = os.path.join(APP_DATA, "motorrad")
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    CORE_FIELDS = [
        "id", "topic", "topic_code", "exam_type", "grundstoff", "legal_basis",
        "points", "high_stakes", "question_type", "image_ref", "correct", "roles",
    ]
    SCOPE_FIELDS = ["class_scope", "region_scope"]

    core_questions = []
    per_locale = {loc: {} for loc in ALL_LOCALES}
    missing_locale_count = {loc: 0 for loc in ALL_LOCALES}

    for q in pilot["questions"]:
        core = {k: q[k] for k in CORE_FIELDS if k in q}
        for sf in SCOPE_FIELDS:
            if sf in q:
                core[sf] = q[sf]
        core_questions.append(core)

        for loc in ALL_LOCALES:
            t = q["text"].get(loc)
            expl = q["explanation"].get(loc)
            if t is None or expl is None:
                missing_locale_count[loc] += 1
                continue
            per_locale[loc][q["id"]] = {
                "question": t["question"],
                "options": t["options"],
                "explanation": expl,
            }

    core_meta = dict(pilot["meta"])
    core_meta["locales"] = ALL_LOCALES
    core_meta["total_questions"] = len(core_questions)

    json.dump({"meta": core_meta, "questions": core_questions},
              open(os.path.join(module_dir, "core.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    for loc in ALL_LOCALES:
        json.dump(per_locale[loc], open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    print(f"Added {len(NEW_QUESTIONS)} new Motorrad questions.")
    print(f"New total: {len(pilot['questions'])} questions.")
    from collections import Counter
    print("Topic counts:", dict(Counter(q["topic_code"] for q in pilot["questions"])))
    print("Locale gaps (questions missing that locale):", missing_locale_count)

    ids = [q["id"] for q in pilot["questions"]]
    dupes = len(ids) - len(set(ids))
    print(f"Duplicate id count: {dupes}")


if __name__ == "__main__":
    build()
