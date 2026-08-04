#!/usr/bin/env python3
"""
Pilot data generator for the Fuehrerschein (Klasse B) learning module.
Produces pilot_questions.json: 50 original MCQs (25 Vorfahrt, 25 Verkehrszeichen)
in the fact-layer / text-layer schema, DE + EN.

NOTE: Content is original phrasing derived from public StVO/StVZO rules and
standardized (non-copyrightable) sign shapes -- it deliberately does NOT copy
wording from the licensed amtlicher Fragenkatalog. Legal citations and point
values approximate real exam weighting and should get a final legal/subject
matter review before any public or commercial release.
"""
import json

def q(id_, topic, topic_code, legal_basis, points, high_stakes, qtype,
      image_ref, correct, de_q, de_opts, en_q, en_opts, de_expl, en_expl):
    return {
        "id": id_,
        "topic": topic,
        "topic_code": topic_code,
        "class_scope": ["B"],
        "grundstoff": True,
        "legal_basis": legal_basis,
        "points": points,
        "high_stakes": high_stakes,
        "question_type": qtype,  # "single_choice" | "multi_choice"
        "image_ref": image_ref,  # placeholder asset key, e.g. "signs/206"
        "correct": correct,      # list of option keys, e.g. ["b"]
        "text": {
            "de": {"question": de_q, "options": de_opts},
            "en": {"question": en_q, "options": en_opts},
        },
        "explanation": {"de": de_expl, "en": en_expl},
    }

questions = []

# ---------------------------------------------------------------------------
# TOPIC 1: VORFAHRT UND KREUZUNGEN (right-of-way & intersections) -- 25 items
# ---------------------------------------------------------------------------

questions.append(q(
    "vorfahrt-01", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 5, True,
    "single_choice", None, ["b"],
    "An einer Kreuzung ohne Verkehrszeichen und ohne Ampel nähern sich zwei Fahrzeuge gleichzeitig. Wer hat Vorfahrt?",
    {"a": "Das schnellere Fahrzeug", "b": "Das Fahrzeug von rechts", "c": "Das größere Fahrzeug", "d": "Wer zuerst hupt"},
    "At an intersection with no signs or traffic lights, two vehicles approach at the same time. Who has right of way?",
    {"a": "The faster vehicle", "b": "The vehicle coming from the right", "c": "The larger vehicle", "d": "Whoever honks first"},
    "Ohne abweichende Beschilderung gilt die Grundregel 'rechts vor links'.",
    "Without signs stating otherwise, the basic rule 'right before left' applies."
))

questions.append(q(
    "vorfahrt-02", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 205", 5, True,
    "single_choice", "signs/205", ["c"],
    "Sie sehen ein dreieckiges Schild mit der Spitze nach unten und rotem Rand (Zeichen 205). Was bedeutet es?",
    {"a": "Vorfahrtstraße", "b": "Verbot der Einfahrt", "c": "Vorfahrt gewähren", "d": "Halt, Stoppschild"},
    "You see a downward-pointing triangular sign with a red border (Zeichen 205). What does it mean?",
    {"a": "Priority road", "b": "No entry", "c": "Yield / give way", "d": "Stop"},
    "Zeichen 205 zwingt zum Vorfahrtgewähren, aber nicht zum vollständigen Anhalten, sofern die Sicht ausreicht.",
    "Zeichen 205 requires yielding right of way, but not a full stop, as long as visibility is sufficient."
))

questions.append(q(
    "vorfahrt-03", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 206", 5, True,
    "single_choice", "signs/206", ["a"],
    "An einem achteckigen roten Schild mit der Aufschrift 'STOP' (Zeichen 206) müssen Sie...",
    {"a": "immer vollständig anhalten, auch wenn kein anderes Fahrzeug zu sehen ist", "b": "nur anhalten, wenn ein anderes Fahrzeug kommt", "c": "die Geschwindigkeit nur verringern", "d": "nur bei Dunkelheit anhalten"},
    "At an octagonal red 'STOP' sign (Zeichen 206), you must...",
    {"a": "always come to a complete stop, even if no other vehicle is visible", "b": "stop only if another vehicle is approaching", "c": "only slow down", "d": "only stop at night"},
    "Das Stoppschild verlangt in jedem Fall ein vollständiges Anhalten, unabhängig vom übrigen Verkehr.",
    "The stop sign always requires a complete stop, regardless of other traffic."
))

questions.append(q(
    "vorfahrt-04", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 301", 4, False,
    "single_choice", "signs/301", ["b"],
    "Das gelbe, auf der Spitze stehende Schild mit weißem Rand (Zeichen 301) zeigt an, dass...",
    {"a": "die Straße endet", "b": "Sie an dieser Stelle Vorfahrt haben", "c": "ein Kreisverkehr folgt", "d": "Fußgänger Vorrang haben"},
    "The yellow diamond-shaped sign with a white border (Zeichen 301) indicates that...",
    {"a": "the road ends", "b": "you have right of way at this point", "c": "a roundabout follows", "d": "pedestrians have priority"},
    "Zeichen 301 markiert punktuell Vorfahrt gegenüber der kreuzenden Straße.",
    "Zeichen 301 marks priority at that single point relative to the crossing road."
))

questions.append(q(
    "vorfahrt-05", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 306/307", 4, False,
    "single_choice", "signs/306", ["a"],
    "Das rechteckige gelbe Schild mit weißem Rand, das auch Kurven der Straße darstellen kann (Zeichen 306), bedeutet:",
    {"a": "Vorfahrtstraße - Vorfahrt entlang des gesamten markierten Straßenverlaufs", "b": "Ende der Autobahn", "c": "Verbot für Kraftfahrzeuge", "d": "Fußgängerzone"},
    "The rectangular yellow sign with a white border, which can also show the road's curves (Zeichen 306), means:",
    {"a": "Priority road - right of way continues along the entire marked route", "b": "End of motorway", "c": "No motor vehicles", "d": "Pedestrian zone"},
    "Anders als Zeichen 301 gilt Zeichen 306 durchgehend entlang der gesamten Vorfahrtstraße, bis Zeichen 307 sie aufhebt.",
    "Unlike Zeichen 301, Zeichen 306 applies continuously along the entire priority road until Zeichen 307 ends it."
))

questions.append(q(
    "vorfahrt-06", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1a StVO", 5, True,
    "single_choice", "signs/215", ["b"],
    "Wie verhalten Sie sich bei der Einfahrt in einen Kreisverkehr (Zeichen 215), sofern keine Schilder etwas anderes vorschreiben?",
    {"a": "Fahrzeuge, die einfahren wollen, haben Vorfahrt", "b": "Fahrzeuge, die sich bereits im Kreisverkehr befinden, haben Vorfahrt", "c": "Es gilt rechts vor links", "d": "Der schnellere darf zuerst fahren"},
    "How do you behave when entering a roundabout (Zeichen 215), unless signs state otherwise?",
    {"a": "Vehicles entering the roundabout have priority", "b": "Vehicles already in the roundabout have priority", "c": "Right before left applies", "d": "Whoever is faster goes first"},
    "Im Kreisverkehr hat der fließende Verkehr im Kreis grundsätzlich Vorrang vor einfahrenden Fahrzeugen.",
    "In a roundabout, traffic already circulating generally has priority over vehicles entering."
))

questions.append(q(
    "vorfahrt-07", "Vorfahrt und Kreuzungen", "vorfahrt", "§9 Abs. 3 StVO", 5, True,
    "single_choice", None, ["c"],
    "Sie wollen an einer Kreuzung ohne Ampel nach links abbiegen. Entgegenkommender Verkehr fährt geradeaus. Wer hat Vorfahrt?",
    {"a": "Sie, weil Sie zuerst an der Kreuzung waren", "b": "Niemand, beide müssen warten", "c": "Der entgegenkommende, geradeausfahrende Verkehr", "d": "Der Linksabbieger, wenn er blinkt"},
    "You want to turn left at an unsignalled intersection. Oncoming traffic is going straight. Who has right of way?",
    {"a": "You, because you arrived at the intersection first", "b": "Neither, both must wait", "c": "The oncoming traffic going straight", "d": "The vehicle turning left, if it signals"},
    "Wer links abbiegt, muss entgegenkommenden, geradeausfahrenden oder rechtsabbiegenden Verkehr durchfahren lassen.",
    "A vehicle turning left must let oncoming traffic going straight or turning right pass first."
))

questions.append(q(
    "vorfahrt-08", "Vorfahrt und Kreuzungen", "vorfahrt", "§9 Abs. 3 StVO", 3, False,
    "single_choice", None, ["a"],
    "Zwei Fahrzeuge aus entgegengesetzter Richtung wollen an derselben Kreuzung gleichzeitig links abbiegen. Wie fahren sie üblicherweise?",
    {"a": "Sie fahren 'Kurve vor Kurve' (voreinander links abbiegend) an der Kreuzungsmitte vorbei", "b": "Der linke muss immer warten", "c": "Beide müssen vollständig anhalten und sich einigen", "d": "Der rechte muss immer warten"},
    "Two vehicles from opposite directions both want to turn left at the same intersection at the same time. How do they usually proceed?",
    {"a": "They pass each other 'nose to nose', each turning in front of the other around the intersection centre", "b": "The one on the left always has to wait", "c": "Both must stop completely and negotiate", "d": "The one on the right always has to wait"},
    "Beim gleichzeitigen Linksabbiegen fahren beide Fahrzeuge in der Regel voreinander vorbei (rechts an rechts).",
    "When both turn left simultaneously, they normally pass each other front-to-front (right side to right side)."
))

questions.append(q(
    "vorfahrt-09", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 5, True,
    "single_choice", None, ["b"],
    "Eine Straßenbahn nähert sich von rechts aus einer Nebenstraße. Wie verhalten Sie sich, wenn kein Schild etwas anderes vorschreibt?",
    {"a": "Sie haben Vorfahrt, da die Straßenbahn aus der Nebenstraße kommt", "b": "Die Straßenbahn hat grundsätzlich Vorfahrt", "c": "Es gilt rechts vor links wie bei Autos", "d": "Vorfahrt wird ausgelost"},
    "A tram is approaching from a side street on your right. How do you behave if no sign states otherwise?",
    {"a": "You have right of way because the tram is coming from a minor road", "b": "The tram generally has right of way", "c": "Right before left applies just like for cars", "d": "Right of way is decided randomly"},
    "Schienenfahrzeuge haben grundsätzlich Vorfahrt, unabhängig davon, aus welcher Richtung sie kommen.",
    "Rail vehicles generally have right of way, regardless of the direction they come from."
))

questions.append(q(
    "vorfahrt-10", "Vorfahrt und Kreuzungen", "vorfahrt", "§7 Abs. 4 StVO", 4, False,
    "single_choice", None, ["c"],
    "Ein Fahrstreifen endet und der Verkehr muss sich einordnen. Wie funktioniert das Reißverschlussverfahren?",
    {"a": "Wer zuerst da ist, darf zuerst fahren", "b": "Der linke Fahrstreifen hat immer Vorrang", "c": "Die Fahrzeuge beider Streifen wechseln sich beim Einfädeln ab", "d": "Nur Lkw dürfen sich einordnen"},
    "A lane ends and traffic must merge. How does the 'zip merge' (Reißverschlussverfahren) work?",
    {"a": "Whoever gets there first goes first", "b": "The left lane always has priority", "c": "Vehicles from both lanes take turns merging one after another", "d": "Only trucks are allowed to merge"},
    "Kurz vor der Verengung lässt man abwechselnd je ein Fahrzeug aus dem endenden Streifen einfädeln.",
    "Just before the lane narrows, vehicles from the ending lane are let in one at a time, alternating."
))

questions.append(q(
    "vorfahrt-11", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 2 StVO", 4, False,
    "single_choice", None, ["b"],
    "Sie fahren aus einem erkennbaren Feldweg auf eine normale Straße. Ein Fahrzeug nähert sich von rechts auf der Straße. Wer hat Vorfahrt?",
    {"a": "Sie, weil er von rechts kommt betrifft nur Straßen gleicher Bedeutung", "b": "Das Fahrzeug auf der Straße, der Feldweg gilt als untergeordnet", "c": "Rechts vor links gilt uneingeschränkt", "d": "Beide müssen gleichzeitig anhalten"},
    "You are driving from a clearly recognizable field/dirt track onto a normal road. A vehicle is approaching from the right on the road. Who has right of way?",
    {"a": "You, because 'right before left' only applies between roads of equal importance", "b": "The vehicle on the road; the field track counts as a minor road", "c": "Right before left applies without restriction", "d": "Both must stop at the same time"},
    "Erkennbar untergeordnete Wege (Feldwege, Grundstücksausfahrten) genießen keine Vorfahrt, selbst ohne Schild.",
    "Clearly minor routes (field tracks, driveways) have no right of way even without a sign."
))

questions.append(q(
    "vorfahrt-12", "Vorfahrt und Kreuzungen", "vorfahrt", "§10 StVO", 4, False,
    "single_choice", None, ["a"],
    "Sie fahren aus einer Grundstücksausfahrt auf die Straße. Welche Regel gilt?",
    {"a": "Sie müssen sich wie aus einer untergeordneten Straße verhalten und haben keine Vorfahrt", "b": "Rechts vor links gilt normal", "c": "Sie haben immer Vorfahrt gegenüber dem fließenden Verkehr", "d": "Nur bei Tageslicht müssen Sie warten"},
    "You are driving from a driveway onto the road. What rule applies?",
    {"a": "You must behave as if coming from a minor road and have no right of way", "b": "Right before left applies normally", "c": "You always have priority over moving traffic", "d": "You only have to wait during daylight"},
    "Wer aus einem Grundstück, einer Parklücke oder ähnlichem einfährt, muss sich besonders vorsichtig verhalten und hat keine Vorfahrt.",
    "Anyone entering traffic from a driveway, parking space, or similar must proceed with special caution and has no right of way."
))

questions.append(q(
    "vorfahrt-13", "Vorfahrt und Kreuzungen", "vorfahrt", "§36 StVO", 5, True,
    "single_choice", None, ["b"],
    "Ein Polizist gibt an einer Kreuzung Handzeichen, die im Widerspruch zur Ampel stehen. Was gilt?",
    {"a": "Die Ampel hat immer Vorrang", "b": "Die Zeichen des Polizisten haben Vorrang vor Ampeln und Verkehrszeichen", "c": "Man darf sich aussuchen, wem man folgt", "d": "Beide Regelungen gelten gleichzeitig"},
    "A police officer gives hand signals at an intersection that contradict the traffic light. What applies?",
    {"a": "The traffic light always takes precedence", "b": "The officer's signals take precedence over traffic lights and signs", "c": "You may choose which one to follow", "d": "Both regulations apply simultaneously"},
    "Zeichen und Weisungen von Polizeibeamten gehen Lichtzeichenanlagen und Verkehrszeichen immer vor.",
    "Signals and instructions from police officers always take precedence over traffic lights and signs."
))

questions.append(q(
    "vorfahrt-14", "Vorfahrt und Kreuzungen", "vorfahrt", "§37 Abs. 2 StVO, Zeichen 720", 3, False,
    "single_choice", "signs/720", ["c"],
    "An einer Ampel mit grünem Blinkpfeil nach rechts (Zeichen 720) dürfen Sie bei Rot rechts abbiegen. Was müssen Sie trotzdem tun?",
    {"a": "Nichts, Sie dürfen ungebremst durchfahren", "b": "Nur hupen zur Warnung", "c": "Zunächst anhalten und übrigen Verkehr sowie Fußgänger beachten", "d": "Nur bei Nacht anhalten"},
    "At a traffic light with a green arrow sign allowing right turns on red (Zeichen 720), you may turn right on red. What must you still do?",
    {"a": "Nothing, you may proceed without stopping", "b": "Only honk as a warning", "c": "Stop first and yield to other traffic and pedestrians", "d": "Only stop at night"},
    "Der Grünpfeil erlaubt das Rechtsabbiegen bei Rot nur nach vorherigem Halt und wenn niemand gefährdet wird.",
    "The green arrow only allows a right turn on red after coming to a full stop and if no one is endangered."
))

questions.append(q(
    "vorfahrt-15", "Vorfahrt und Kreuzungen", "vorfahrt", "§26 StVO, Zeichen 293", 5, True,
    "single_choice", "signs/293", ["a"],
    "Sie nähern sich einem Fußgängerüberweg (Zebrastreifen, Zeichen 293). Ein Fußgänger will die Straße überqueren. Wie verhalten Sie sich?",
    {"a": "Sie müssen warten und dem Fußgänger das Überqueren ermöglichen", "b": "Der Fußgänger muss warten, bis Sie durchgefahren sind", "c": "Nur bei Rot müssen Sie anhalten", "d": "Es gilt rechts vor links"},
    "You are approaching a pedestrian crossing (zebra crossing, Zeichen 293). A pedestrian wants to cross the road. How do you behave?",
    {"a": "You must wait and allow the pedestrian to cross", "b": "The pedestrian must wait until you have passed", "c": "You only need to stop at a red light", "d": "Right before left applies"},
    "An einem Zebrastreifen haben Fußgänger, die erkennbar die Fahrbahn überqueren wollen, Vorrang.",
    "At a zebra crossing, pedestrians who clearly intend to cross have priority."
))

questions.append(q(
    "vorfahrt-16", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 4, False,
    "single_choice", None, ["a"],
    "An einer Kreuzung ist die Ampel wegen eines Stromausfalls komplett ausgefallen und es gibt keine weiteren Schilder. Was gilt?",
    {"a": "Rechts vor links", "b": "Die Kreuzung darf nicht befahren werden", "c": "Wer zuerst kommt, fährt zuerst", "d": "Es gilt automatisch eine Vorfahrtstraße"},
    "At an intersection, the traffic light has completely failed due to a power outage and there are no other signs. What applies?",
    {"a": "Right before left", "b": "The intersection may not be entered at all", "c": "First to arrive goes first", "d": "A priority road automatically applies"},
    "Fällt die Ampel aus und fehlen andere Regelungen, gilt die Grundregel rechts vor links.",
    "If the traffic light fails and no other regulation applies, the basic right-before-left rule takes over."
))

questions.append(q(
    "vorfahrt-17", "Vorfahrt und Kreuzungen", "vorfahrt", "§9 Abs. 3 StVO (Novelle 2020)", 5, True,
    "single_choice", None, ["b"],
    "Sie biegen rechts ab und ein Radfahrer fährt geradeaus auf einem benutzungspflichtigen Radweg neben Ihnen. Wer hat Vorrang?",
    {"a": "Sie, weil Sie sich bereits zum Abbiegen eingeordnet haben", "b": "Der geradeausfahrende Radfahrer", "c": "Es wird ausgehandelt per Handzeichen", "d": "Der Radfahrer muss immer absteigen"},
    "You are turning right, and a cyclist is going straight on a mandatory cycle path next to you. Who has priority?",
    {"a": "You, because you have already positioned yourself to turn", "b": "The cyclist going straight", "c": "It is negotiated with hand signals", "d": "The cyclist must always dismount"},
    "Beim Abbiegen muss geradeausfahrenden Rad- und Fußverkehr Vorrang gewährt werden; im Zweifel Schrittgeschwindigkeit.",
    "When turning, priority must be given to cyclists and pedestrians going straight; when in doubt, proceed at walking pace."
))

questions.append(q(
    "vorfahrt-18", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 3, False,
    "single_choice", None, ["b"],
    "Sie haben sich bereits zum Abbiegen eingeordnet und den Blinker gesetzt. Was gilt bezüglich der Vorfahrt?",
    {"a": "Ihre Vorfahrtberechtigung erlischt automatisch", "b": "Ihre Vorfahrt gilt unverändert weiter, bis Sie abgebogen sind", "c": "Sie müssen in jedem Fall warten", "d": "Der Blinker gibt Ihnen automatisch Vorfahrt"},
    "You have already positioned yourself to turn and switched on the indicator. What applies regarding right of way?",
    {"a": "Your right of way automatically ends", "b": "Your right of way continues unchanged until you have turned", "c": "You must wait in every case", "d": "The indicator automatically grants you right of way"},
    "Einordnen und Blinken ändern nichts an einer bestehenden Vorfahrtberechtigung.",
    "Positioning and signalling do not change an existing right of way."
))

questions.append(q(
    "vorfahrt-19", "Vorfahrt und Kreuzungen", "vorfahrt", "§38 StVO", 5, True,
    "single_choice", None, ["a"],
    "Ein Einsatzfahrzeug nähert sich mit Blaulicht und Martinshorn von hinten. Was müssen Sie tun, auch wenn Sie eigentlich Vorfahrt hätten?",
    {"a": "Sofort freie Bahn schaffen, notfalls durch Bilden einer Rettungsgasse oder Ranfahren", "b": "Normal weiterfahren, da Sie Vorfahrt haben", "c": "Beschleunigen, um die Kreuzung zuerst zu erreichen", "d": "Nur hupen als Antwort"},
    "An emergency vehicle with blue lights and siren approaches from behind. What must you do, even if you would normally have right of way?",
    {"a": "Immediately clear a path, if necessary by forming an emergency corridor or pulling over", "b": "Continue driving normally, since you have right of way", "c": "Accelerate to reach the intersection first", "d": "Only honk in response"},
    "Sonderrechte von Einsatzfahrzeugen mit Blaulicht und Martinshorn gehen jeder sonstigen Vorfahrtregel vor.",
    "The special rights of emergency vehicles with blue lights and siren override every other right-of-way rule."
))

questions.append(q(
    "vorfahrt-20", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 102", 3, False,
    "single_choice", "signs/102", ["b"],
    "Ein dreieckiges Schild mit rotem Rand zeigt ein Kreuzsymbol (Zeichen 102, 'Kreuzung'). Was bedeutet es?",
    {"a": "Es regelt selbst die Vorfahrt an dieser Kreuzung neu", "b": "Es warnt lediglich vor einer Kreuzung; rechts vor links gilt weiterhin", "c": "Es zeigt eine Vorfahrtstraße an", "d": "Es verbietet das Kreuzen"},
    "A triangular sign with a red border shows a cross symbol (Zeichen 102, 'intersection'). What does it mean?",
    {"a": "It re-regulates right of way at this intersection", "b": "It merely warns of an upcoming intersection; right before left still applies", "c": "It indicates a priority road", "d": "It prohibits crossing"},
    "Gefahrzeichen wie 102 warnen nur; sie verändern nicht die geltende Vorfahrtregel.",
    "Warning signs like 102 only warn; they do not change the applicable right-of-way rule."
))

questions.append(q(
    "vorfahrt-21", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 5, True,
    "single_choice", None, ["b"],
    "Eine Vorfahrtstraße (Zeichen 306) kreuzt einen Bahnübergang ohne Schranke. Ein Zug nähert sich. Wer hat Vorrang?",
    {"a": "Die Vorfahrtstraße, da sie durch Zeichen 306 geschützt ist", "b": "Der Zug hat unabhängig von der Straßenbeschilderung immer Vorrang", "c": "Rechts vor links entscheidet", "d": "Der zuerst ankommende Verkehrsteilnehmer"},
    "A priority road (Zeichen 306) crosses a railway crossing without a barrier. A train is approaching. Who has priority?",
    {"a": "The priority road, since it is protected by Zeichen 306", "b": "The train always has priority regardless of road signage", "c": "Right before left decides", "d": "Whoever arrives first"},
    "Schienenfahrzeuge an Bahnübergängen haben immer Vorrang vor dem Straßenverkehr, unabhängig von sonstiger Beschilderung.",
    "Trains at level crossings always have priority over road traffic, regardless of other signage."
))

questions.append(q(
    "vorfahrt-22", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 3, False,
    "single_choice", None, ["a"],
    "Eine Straße wird durch eine Mittelinsel geteilt und kreuzt eine gleichrangige Straße ohne Schilder. Wie gilt die Vorfahrt?",
    {"a": "Rechts vor links gilt für die gesamte Straße einheitlich, unabhängig von der Mittelinsel", "b": "Jede Fahrbahnhälfte hat eine eigene Vorfahrtregel", "c": "Die Mittelinsel hebt jede Vorfahrtregelung auf", "d": "Es gilt automatisch eine Vorfahrtstraße"},
    "A road is divided by a central island and crosses a road of equal rank with no signs. How does right of way apply?",
    {"a": "Right before left applies uniformly to the whole road, regardless of the island", "b": "Each half of the carriageway has its own right-of-way rule", "c": "The central island cancels any right-of-way rule", "d": "A priority road automatically applies"},
    "Eine bauliche Teilung durch eine Mittelinsel ändert nichts an der grundsätzlichen Vorfahrtregelung der Straße.",
    "A structural division by a central island does not change the road's basic right-of-way rule."
))

questions.append(q(
    "vorfahrt-23", "Vorfahrt und Kreuzungen", "vorfahrt", "§8 Abs. 1 StVO", 3, False,
    "single_choice", None, ["b"],
    "Sie kommen aus einer Einbahnstraße ohne Vorfahrtsschilder und treffen auf eine gleichrangige Straße. Welche Regel gilt?",
    {"a": "Die Einbahnstraße hat automatisch Vorfahrt", "b": "Rechts vor links gilt wie an jeder anderen gleichrangigen Kreuzung", "c": "Der Gegenverkehr hat immer Vorfahrt", "d": "Es gibt keine Vorfahrtregel in Einbahnstraßen"},
    "You come out of a one-way street with no priority signs and meet a road of equal rank. What rule applies?",
    {"a": "The one-way street automatically has priority", "b": "Right before left applies as at any other intersection of equal-ranking roads", "c": "Oncoming traffic always has priority", "d": "There is no right-of-way rule in one-way streets"},
    "Eine Einbahnstraße ist für die Vorfahrt eine ganz normale Straße; ohne Schilder gilt rechts vor links.",
    "A one-way street is a perfectly normal road for right-of-way purposes; without signs, right before left applies."
))

questions.append(q(
    "vorfahrt-24", "Vorfahrt und Kreuzungen", "vorfahrt", "§6 StVO", 4, False,
    "single_choice", None, ["a"],
    "Auf Ihrer Fahrbahnseite steht ein Hindernis (z. B. parkende Fahrzeuge), sodass Sie auf die Gegenfahrbahn ausweichen müssen. Was gilt, unabhängig von Rechts-vor-links?",
    {"a": "Sie müssen dem Gegenverkehr Vorrang gewähren und dürfen ihn nicht behindern", "b": "Sie haben automatisch Vorfahrt, weil das Hindernis Sie zwingt auszuweichen", "c": "Der Gegenverkehr muss anhalten und warten", "d": "Es gilt rechts vor links wie an einer Kreuzung"},
    "There is an obstacle on your side of the road (e.g. parked vehicles), forcing you onto the opposite lane. What applies, regardless of right-before-left?",
    {"a": "You must give way to oncoming traffic and must not obstruct it", "b": "You automatically have priority because the obstacle forces you to swerve", "c": "Oncoming traffic must stop and wait", "d": "Right before left applies as at an intersection"},
    "Wer wegen eines Hindernisses die Gegenfahrbahn benutzen muss, hat dem Gegenverkehr Vorrang zu gewähren.",
    "Anyone who must use the opposite lane because of an obstacle must give way to oncoming traffic."
))

questions.append(q(
    "vorfahrt-25", "Vorfahrt und Kreuzungen", "vorfahrt", "§41 StVO, Zeichen 306/307", 3, False,
    "single_choice", "signs/307", ["c"],
    "Ein Schild wie Zeichen 306, jedoch grau/schwarz durchgestrichen (Zeichen 307), bedeutet:",
    {"a": "Beginn einer neuen Vorfahrtstraße", "b": "Verbot der Einfahrt in die Straße", "c": "Ende der Vorfahrtstraße", "d": "Autobahnende"},
    "A sign like Zeichen 306 but crossed out in grey/black (Zeichen 307) means:",
    {"a": "Start of a new priority road", "b": "No entry into the road", "c": "End of the priority road", "d": "End of the motorway"},
    "Zeichen 307 hebt die durch Zeichen 306 angeordnete durchgehende Vorfahrt wieder auf.",
    "Zeichen 307 cancels the continuous right of way established by Zeichen 306."
))

# ---------------------------------------------------------------------------
# TOPIC 2: VERKEHRSZEICHEN (traffic signs) -- 25 items
# ---------------------------------------------------------------------------

questions.append(q(
    "zeichen-01", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 274", 3, False,
    "single_choice", "signs/274", ["b"],
    "Ein weißes rundes Schild mit rotem Rand und einer schwarzen Zahl (z. B. '50') zeigt an:",
    {"a": "Empfohlene Mindestgeschwindigkeit", "b": "Zulässige Höchstgeschwindigkeit in km/h", "c": "Entfernung zur nächsten Stadt in km", "d": "Erlaubte Parkdauer in Minuten"},
    "A white round sign with a red border and a black number (e.g. '50') indicates:",
    {"a": "Recommended minimum speed", "b": "Maximum permitted speed in km/h", "c": "Distance to the next town in km", "d": "Permitted parking duration in minutes"},
    "Zeichen 274 legt die höchstzulässige Geschwindigkeit fest, die nicht überschritten werden darf.",
    "Zeichen 274 sets the maximum permitted speed, which must not be exceeded."
))

questions.append(q(
    "zeichen-02", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 278", 2, False,
    "single_choice", "signs/278", ["a"],
    "Das gleiche Schild wie die Geschwindigkeitsbegrenzung, aber grau durchgestrichen (Zeichen 278), bedeutet:",
    {"a": "Ende der zuvor angeordneten Geschwindigkeitsbegrenzung", "b": "Zusätzliche Geschwindigkeitsbegrenzung bei Nässe", "c": "Verbot des Überholens endet", "d": "Beginn eines Tempolimits"},
    "The same sign as the speed limit but crossed out in grey (Zeichen 278) means:",
    {"a": "End of the previously ordered speed limit", "b": "Additional speed limit in wet conditions", "c": "End of the overtaking ban", "d": "Start of a speed limit"},
    "Ein durchgestrichenes Zeichen hebt die zuvor geltende Anordnung auf.",
    "A crossed-out sign cancels the previously applicable order."
))

questions.append(q(
    "zeichen-03", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 267", 4, False,
    "single_choice", "signs/267", ["c"],
    "Ein rundes rotes Schild mit einem weißen waagerechten Balken (Zeichen 267) bedeutet:",
    {"a": "Halt, Vorfahrt gewähren", "b": "Durchfahrt für alle Fahrzeuge frei", "c": "Verbot der Einfahrt für Fahrzeuge aller Art", "d": "Einbahnstraße in Fahrtrichtung"},
    "A round red sign with a white horizontal bar (Zeichen 267) means:",
    {"a": "Stop, give way", "b": "Free passage for all vehicles", "c": "No entry for vehicles of any kind", "d": "One-way street in the direction of travel"},
    "Zeichen 267 verbietet die Einfahrt in diese Richtung, typisch am Ende einer Einbahnstraße.",
    "Zeichen 267 prohibits entry in that direction, typically at the end of a one-way street."
))

questions.append(q(
    "zeichen-04", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 133", 4, False,
    "single_choice", "signs/133", ["b"],
    "Ein dreieckiges Warnschild mit spielenden Kindern (Zeichen 133) weist auf hin auf:",
    {"a": "Eine Schule ohne besondere Vorsicht nötig", "b": "Mögliches plötzliches Auftauchen von Kindern auf der Fahrbahn", "c": "Ein Spielplatzverbot", "d": "Ein Tempolimit von 30 km/h zwingend"},
    "A triangular warning sign showing playing children (Zeichen 133) warns of:",
    {"a": "A school where no special caution is needed", "b": "Children possibly suddenly appearing on the road", "c": "A ban on playgrounds", "d": "A mandatory 30 km/h speed limit"},
    "Das Schild warnt vor Kindern in der Nähe der Fahrbahn, z. B. bei Schulen oder Spielplätzen; erhöhte Vorsicht und Bremsbereitschaft sind geboten.",
    "The sign warns of children near the road, e.g. near schools or playgrounds; increased caution and readiness to brake are required."
))

questions.append(q(
    "zeichen-05", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 101", 2, False,
    "single_choice", "signs/101", ["a"],
    "Ein dreieckiges Schild mit rotem Rand und einem Ausrufezeichen (Zeichen 101) bedeutet allgemein:",
    {"a": "Allgemeine Gefahrstelle - erhöhte Aufmerksamkeit erforderlich", "b": "Verbot jeglicher Fahrzeuge", "c": "Vorfahrtstraße beginnt", "d": "Ende aller Verbote"},
    "A triangular sign with a red border and an exclamation mark (Zeichen 101) generally means:",
    {"a": "General danger spot - increased attention required", "b": "Prohibition of all vehicles", "c": "Priority road begins", "d": "End of all prohibitions"},
    "Dieses Zeichen wird oft mit einem Zusatzschild kombiniert, das die konkrete Gefahr benennt.",
    "This sign is often combined with an additional plate specifying the concrete danger."
))

questions.append(q(
    "zeichen-06", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 120/121", 3, False,
    "single_choice", "signs/120", ["c"],
    "Ein dreieckiges Schild zeigt eine sich verengende Fahrbahn (Zeichen 120/121). Sie sollten:",
    {"a": "Beschleunigen, um die Engstelle schnell zu passieren", "b": "Ignorieren, wenn kein Gegenverkehr sichtbar ist", "c": "Geschwindigkeit anpassen und sich rechtzeitig einordnen", "d": "Auf dem Seitenstreifen anhalten"},
    "A triangular sign shows a narrowing road (Zeichen 120/121). You should:",
    {"a": "Accelerate to pass the narrow section quickly", "b": "Ignore it if no oncoming traffic is visible", "c": "Adjust speed and merge into the correct lane in good time", "d": "Stop on the hard shoulder"},
    "Bei Fahrbahnverengungen ist rechtzeitiges, vorausschauendes Einordnen und angepasste Geschwindigkeit wichtig.",
    "At road narrowings, merging early with foresight and adjusting speed is important."
))

questions.append(q(
    "zeichen-07", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 151/138", 5, True,
    "single_choice", "signs/151", ["b"],
    "Ein dreieckiges Warnschild mit einem Zugsymbol (z. B. Zeichen 151) kündigt an:",
    {"a": "Eine U-Bahn-Station in der Nähe", "b": "Einen Bahnübergang ohne Schranken oder Halbschranken", "c": "Eine Straßenbahnhaltestelle", "d": "Ein Museum für Eisenbahnen"},
    "A triangular warning sign with a train symbol (e.g. Zeichen 151) announces:",
    {"a": "A subway station nearby", "b": "A level crossing without full or half barriers", "c": "A tram stop", "d": "A railway museum"},
    "Solche Schilder kündigen unbeschrankte Bahnübergänge an, an denen besondere Vorsicht geboten ist.",
    "Such signs announce level crossings without barriers, where special caution is required."
))

questions.append(q(
    "zeichen-08", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 201", 5, True,
    "single_choice", "signs/201", ["a"],
    "Ein weißes Schild mit rotem Andreaskreuz (Zeichen 201) an einem eingleisigen Bahnübergang bedeutet:",
    {"a": "Bei einem herannahenden Schienenfahrzeug muss unbedingt angehalten werden", "b": "Es handelt sich nur um eine Deko-Markierung", "c": "Vorfahrt für die Straße gegenüber der Bahn", "d": "Die Bahnstrecke ist stillgelegt"},
    "A white sign with a red St. Andrew's cross (Zeichen 201) at a single-track level crossing means:",
    {"a": "You must always stop if a rail vehicle is approaching", "b": "It is merely a decorative marking", "c": "The road has priority over the railway", "d": "The rail line is out of service"},
    "Das Andreaskreuz markiert einen Bahnübergang; bei Annäherung eines Zuges muss zwingend angehalten werden.",
    "The St. Andrew's cross marks a level crossing; you must stop if a train is approaching."
))

questions.append(q(
    "zeichen-09", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 250", 4, False,
    "single_choice", "signs/250", ["b"],
    "Ein rundes weißes Schild mit rotem Rand ohne weitere Symbole (Zeichen 250) bedeutet:",
    {"a": "Verbot nur für Motorräder", "b": "Verbot für Fahrzeuge aller Art", "c": "Ende aller Verbote", "d": "Vorfahrt für Fußgänger"},
    "A round white sign with a red border and no further symbols (Zeichen 250) means:",
    {"a": "Prohibition for motorcycles only", "b": "Prohibition for vehicles of any kind", "c": "End of all prohibitions", "d": "Priority for pedestrians"},
    "Zeichen 250 sperrt die Strecke für sämtliche Fahrzeugarten, mit wenigen gesetzlichen Ausnahmen.",
    "Zeichen 250 closes the route to all types of vehicles, with a few statutory exceptions."
))

questions.append(q(
    "zeichen-10", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 260", 3, False,
    "single_choice", "signs/260", ["a"],
    "Ein rundes weißes Schild mit rotem Rand, das ein Auto und ein Motorrad zeigt (Zeichen 260), bedeutet:",
    {"a": "Verbot für Kraftfahrzeuge", "b": "Nur Kraftfahrzeuge erlaubt", "c": "Parkverbot für Kraftfahrzeuge", "d": "Tankstelle in der Nähe"},
    "A round white sign with a red border showing a car and a motorcycle (Zeichen 260) means:",
    {"a": "Prohibition for motor vehicles", "b": "Only motor vehicles allowed", "c": "No parking for motor vehicles", "d": "Petrol station nearby"},
    "Zeichen 260 verbietet motorisierten Fahrzeugen die Durchfahrt (mit definierten Ausnahmen, z. B. Mofas unter bestimmten Bedingungen).",
    "Zeichen 260 prohibits motorized vehicles from passing (with defined exceptions, e.g. mopeds under certain conditions)."
))

questions.append(q(
    "zeichen-11", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 237", 4, False,
    "single_choice", "signs/237", ["b"],
    "Ein blaues rundes Schild mit weißem Fahrrad-Symbol (Zeichen 237) bedeutet:",
    {"a": "Fahrräder sind hier verboten", "b": "Radweg mit Benutzungspflicht für Radfahrer", "c": "Fahrradverleih in der Nähe", "d": "Fahrradreparaturwerkstatt"},
    "A round blue sign with a white bicycle symbol (Zeichen 237) means:",
    {"a": "Bicycles are prohibited here", "b": "Cycle path with mandatory use for cyclists", "c": "Bicycle rental nearby", "d": "Bicycle repair workshop"},
    "Ist ein Radweg mit Zeichen 237 gekennzeichnet, müssen Radfahrer ihn benutzen, sofern er verkehrssicher ist.",
    "If a cycle path is marked with Zeichen 237, cyclists must use it, provided it is safe to use."
))

questions.append(q(
    "zeichen-12", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 240", 3, False,
    "single_choice", "signs/240", ["c"],
    "Ein blaues rundes Schild mit einem Fußgänger- und einem Fahrrad-Symbol übereinander (Zeichen 240) bedeutet:",
    {"a": "Getrennter Rad- und Gehweg", "b": "Fußgänger verboten", "c": "Gemeinsamer Geh- und Radweg", "d": "Fahrradverbot auf dem Gehweg"},
    "A round blue sign with a pedestrian symbol above a bicycle symbol (Zeichen 240) means:",
    {"a": "Separate cycle and footpath", "b": "Pedestrians prohibited", "c": "Shared pedestrian and cycle path", "d": "Bicycles prohibited on the footpath"},
    "Auf einem gemeinsamen Geh- und Radweg müssen sich Fußgänger und Radfahrer den Weg teilen und gegenseitig Rücksicht nehmen.",
    "On a shared pedestrian and cycle path, pedestrians and cyclists must share the space and show mutual consideration."
))

questions.append(q(
    "zeichen-13", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 220", 3, False,
    "single_choice", "signs/220", ["a"],
    "Ein blaues rechteckiges Schild mit weißem Pfeil nach oben und der Aufschrift 'Einbahnstraße' bzw. Zeichen 220 bedeutet:",
    {"a": "Die Straße darf nur in Pfeilrichtung befahren werden", "b": "Die Straße ist für alle Richtungen frei", "c": "Die Straße ist gesperrt", "d": "Nur Fußgänger dürfen die Straße nutzen"},
    "A blue rectangular sign with a white arrow pointing up, marking a one-way street (Zeichen 220) means:",
    {"a": "The road may only be driven in the direction of the arrow", "b": "The road is open in all directions", "c": "The road is closed", "d": "Only pedestrians may use the road"},
    "In einer Einbahnstraße ist das Fahren nur in der durch den Pfeil vorgegebenen Richtung erlaubt.",
    "On a one-way street, driving is only permitted in the direction indicated by the arrow."
))

questions.append(q(
    "zeichen-14", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 330.1", 3, False,
    "single_choice", "signs/330-1", ["b"],
    "Ein blaues Schild mit stilisierter Autobahnbrücke (Zeichen 330.1) zeigt an:",
    {"a": "Ende der Autobahn", "b": "Beginn der Autobahn", "c": "Rastplatz in 500 m", "d": "Baustelle auf der Autobahn"},
    "A blue sign with a stylised motorway bridge symbol (Zeichen 330.1) indicates:",
    {"a": "End of the motorway", "b": "Start of the motorway", "c": "Rest area in 500 m", "d": "Roadworks on the motorway"},
    "Ab diesem Schild gelten die besonderen Regeln für Autobahnen, z. B. Verbot für Fußgänger und langsame Fahrzeuge.",
    "From this sign onward, special motorway rules apply, e.g. prohibition of pedestrians and slow vehicles."
))

questions.append(q(
    "zeichen-15", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 330.2", 2, False,
    "single_choice", "signs/330-2", ["a"],
    "Das gleiche Symbol wie der Autobahnbeginn, jedoch grau durchgestrichen (Zeichen 330.2), zeigt an:",
    {"a": "Ende der Autobahn", "b": "Zusätzliche Autobahnauffahrt", "c": "Autobahnkreuz in Kürze", "d": "Erhöhtes Tempolimit"},
    "The same symbol as the motorway start, but crossed out in grey (Zeichen 330.2), indicates:",
    {"a": "End of the motorway", "b": "Additional motorway entrance", "c": "Motorway interchange coming up", "d": "Increased speed limit"},
    "Ab diesem Schild gelten wieder die normalen Straßenverkehrsregeln.",
    "From this sign onward, normal road traffic rules apply again."
))

questions.append(q(
    "zeichen-16", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 283", 3, False,
    "single_choice", "signs/283", ["b"],
    "Ein blaues rundes Schild mit rotem Rand und rotem Diagonalkreuz (Zeichen 283) bedeutet:",
    {"a": "Eingeschränktes Haltverbot", "b": "Absolutes Haltverbot", "c": "Parken erlaubt", "d": "Ladezone"},
    "A blue round sign with a red border and a red diagonal cross (Zeichen 283) means:",
    {"a": "Restricted no-stopping zone", "b": "Absolute no-stopping zone", "c": "Parking allowed", "d": "Loading zone"},
    "Beim absoluten Haltverbot darf zu keiner Zeit gehalten werden, auch nicht kurz zum Ein- oder Aussteigen.",
    "In an absolute no-stopping zone, stopping is never permitted, not even briefly to let someone in or out."
))

questions.append(q(
    "zeichen-17", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 286", 3, False,
    "single_choice", "signs/286", ["a"],
    "Ein blaues rundes Schild mit rotem Rand und einem einzelnen roten Diagonalstrich (Zeichen 286) bedeutet:",
    {"a": "Eingeschränktes Haltverbot - kurzes Halten zum Be- oder Entladen ist erlaubt", "b": "Absolutes Haltverbot ohne Ausnahme", "c": "Parken nur mit Parkschein", "d": "Vorfahrtstraße"},
    "A blue round sign with a red border and a single red diagonal stripe (Zeichen 286) means:",
    {"a": "Restricted no-stopping zone - brief stopping to load or unload is allowed", "b": "Absolute no-stopping zone with no exceptions", "c": "Parking only with a parking ticket", "d": "Priority road"},
    "Beim eingeschränkten Haltverbot ist kurzes Halten erlaubt, aber kein Parken (länger als 3 Minuten verlassen).",
    "In a restricted no-stopping zone, brief stopping is allowed but not parking (leaving the vehicle for more than 3 minutes)."
))

questions.append(q(
    "zeichen-18", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 314", 2, False,
    "single_choice", "signs/314", ["c"],
    "Ein blaues quadratisches Schild mit weißem 'P' (Zeichen 314) bedeutet:",
    {"a": "Parken verboten", "b": "Tankstelle", "c": "Parken erlaubt", "d": "Parkhaus voll"},
    "A blue square sign with a white 'P' (Zeichen 314) means:",
    {"a": "Parking prohibited", "b": "Petrol station", "c": "Parking allowed", "d": "Car park full"},
    "Zeichen 314 markiert einen Bereich, in dem das Parken ausdrücklich erlaubt ist.",
    "Zeichen 314 marks an area where parking is explicitly allowed."
))

questions.append(q(
    "zeichen-19", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 315", 3, False,
    "single_choice", "signs/315", ["b"],
    "Ein blaues Schild mit 'P' und einem Symbol, das teilweises Parken auf dem Gehweg zeigt (Zeichen 315), bedeutet:",
    {"a": "Parken auf dem Gehweg ist grundsätzlich verboten", "b": "Parken ist teilweise oder ganz auf dem Gehweg erlaubt, je nach Zusatzsymbol", "c": "Nur Fahrräder dürfen dort abgestellt werden", "d": "Der Gehweg ist für Fußgänger gesperrt"},
    "A blue sign with a 'P' and a symbol showing partial parking on the pavement (Zeichen 315) means:",
    {"a": "Parking on the pavement is generally prohibited", "b": "Parking is allowed partly or fully on the pavement, depending on the sub-symbol", "c": "Only bicycles may be parked there", "d": "The pavement is closed to pedestrians"},
    "Die genaue Art des erlaubten Gehwegparkens (ganz, halb, quer) wird durch das jeweilige Symbol festgelegt.",
    "The exact type of permitted pavement parking (full, half, perpendicular) is defined by the specific symbol."
))

questions.append(q(
    "zeichen-20", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 123", 4, False,
    "single_choice", "signs/123", ["a"],
    "Ein dreieckiges Warnschild mit einer Person und einer Schaufel (Zeichen 123) kündigt an:",
    {"a": "Eine Arbeitsstelle bzw. Baustelle", "b": "Ein Landwirtschaftsgebiet", "c": "Einen Spielplatz", "d": "Eine Mülldeponie"},
    "A triangular warning sign showing a person with a shovel (Zeichen 123) announces:",
    {"a": "A road works / construction site", "b": "An agricultural area", "c": "A playground", "d": "A landfill site"},
    "Das Schild warnt vor einer Arbeitsstelle; erhöhte Aufmerksamkeit und reduzierte Geschwindigkeit sind angebracht.",
    "The sign warns of a work site; increased attention and reduced speed are appropriate."
))

questions.append(q(
    "zeichen-21", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 350", 4, False,
    "single_choice", "signs/350", ["b"],
    "Ein blaues quadratisches Schild mit einem weißen Dreieck und einer Person darauf, die eine Straße überquert (Zeichen 350), markiert:",
    {"a": "Eine Bushaltestelle", "b": "Einen Fußgängerüberweg", "c": "Eine Fußgängerzone", "d": "Ein Überholverbot für Fußgänger"},
    "A blue square sign with a white triangle showing a person crossing (Zeichen 350) marks:",
    {"a": "A bus stop", "b": "A pedestrian crossing", "c": "A pedestrian zone", "d": "An overtaking ban for pedestrians"},
    "Dieses Schild kennzeichnet gemeinsam mit der Zebrastreifen-Markierung einen Fußgängerüberweg.",
    "This sign, together with the zebra-stripe road markings, indicates a pedestrian crossing."
))

questions.append(q(
    "zeichen-22", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 282", 2, False,
    "single_choice", "signs/282", ["a"],
    "Ein rundes weißes Schild mit fünf schrägen schwarzen Streifen (Zeichen 282) bedeutet:",
    {"a": "Ende sämtlicher zuvor angeordneter Streckenverbote/-beschränkungen", "b": "Beginn eines Überholverbots", "c": "Baustellenende", "d": "Erhöhte Vorfahrt"},
    "A round white sign with five diagonal black stripes (Zeichen 282) means:",
    {"a": "End of all previously ordered restrictions on that stretch of road", "b": "Start of an overtaking ban", "c": "End of roadworks", "d": "Increased right of way"},
    "Zeichen 282 hebt gebündelt alle vorher geltenden streckenbezogenen Verbote und Beschränkungen auf.",
    "Zeichen 282 collectively cancels all previously applicable stretch-related prohibitions and restrictions."
))

questions.append(q(
    "zeichen-23", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 276", 4, False,
    "single_choice", "signs/276", ["c"],
    "Ein rundes weißes Schild mit rotem Rand, das zwei Autos zeigt, eines schwarz und eines rot (Zeichen 276), bedeutet:",
    {"a": "Vorfahrt gegenüber Gegenverkehr", "b": "Kolonnenfahrt Pflicht", "c": "Überholverbot für Kraftfahrzeuge", "d": "Verbot der Einfahrt für zwei Fahrzeuge gleichzeitig"},
    "A round white sign with a red border showing two cars, one black and one red (Zeichen 276), means:",
    {"a": "Right of way over oncoming traffic", "b": "Mandatory convoy driving", "c": "No overtaking for motor vehicles", "d": "No entry for two vehicles at once"},
    "Zeichen 276 verbietet das Überholen von Kraftfahrzeugen; das Verbot endet i. d. R. mit Zeichen 280.",
    "Zeichen 276 prohibits overtaking motor vehicles; the prohibition usually ends with Zeichen 280."
))

questions.append(q(
    "zeichen-24", "Verkehrszeichen", "verkehrszeichen", "§41 StVO, Zeichen 209", 3, False,
    "single_choice", "signs/209", ["b"],
    "Ein blaues rundes Schild mit weißem Pfeil, der nach rechts zeigt (Zeichen 209), bedeutet:",
    {"a": "Empfehlung, nach rechts zu fahren", "b": "Vorgeschriebene Fahrtrichtung nach rechts", "c": "Rechtsabbiegen verboten", "d": "Rechts vorbeifahren an Hindernissen erlaubt"},
    "A round blue sign with a white arrow pointing right (Zeichen 209) means:",
    {"a": "Recommendation to go right", "b": "Mandatory direction of travel to the right", "c": "Turning right prohibited", "d": "Passing obstacles on the right is allowed"},
    "Vorgeschriebene Richtungspfeile (Zeichen 209ff.) zwingen zum Fahren in die angezeigte Richtung.",
    "Mandatory direction arrows (Zeichen 209 ff.) require driving in the indicated direction."
))

questions.append(q(
    "zeichen-25", "Verkehrszeichen", "verkehrszeichen", "§42 StVO, Zusatzzeichen", 2, False,
    "single_choice", "signs/zusatz", ["a"],
    "Unter einem Verkehrszeichen befindet sich ein kleines weißes Rechteck mit zusätzlichem Text oder Symbol. Was ist das?",
    {"a": "Ein Zusatzzeichen, das den Geltungsbereich oder die Bedeutung des Hauptschilds präzisiert", "b": "Ein rein dekoratives Element ohne rechtliche Bedeutung", "c": "Eine Werbetafel", "d": "Ein Hinweis auf eine Tankstelle"},
    "Below a traffic sign there is a small white rectangle with additional text or a symbol. What is that?",
    {"a": "An additional plate that specifies the scope or meaning of the main sign", "b": "A purely decorative element with no legal meaning", "c": "An advertisement", "d": "A reference to a petrol station"},
    "Zusatzzeichen können z. B. Geltungszeiten, Entfernungen oder Ausnahmen für bestimmte Fahrzeugarten angeben.",
    "Additional plates can specify, for example, validity times, distances, or exceptions for certain vehicle types."
))

# ---------------------------------------------------------------------------
# Assemble output
# ---------------------------------------------------------------------------

output = {
    "meta": {
        "app": "fluegel-angeln / fuehrerschein-lernmodul",
        "version": "0.1-pilot",
        "generated": "2026-08-04",
        "description": (
            "Pilot batch of 50 original MCQs for the German Klasse-B driving "
            "theory module, covering Vorfahrt und Kreuzungen and Verkehrszeichen. "
            "Content is independently phrased from public StVO/StVZO rules and "
            "standardised sign shapes, NOT copied from the licensed amtlicher "
            "Fragenkatalog. Locales: de (canonical), en (reviewed translation)."
        ),
        "class": "B",
        "locales": ["de", "en"],
        "canonical_locale": "de",
        "point_system": "2-5 points per question, matching real-exam weighting",
        "pass_rule_note": "Real exam Klasse B: max 10 error points overall; automatic fail on 2+ wrong high_stakes (Vorfahrt) questions",
        "legal_review_status": "NOT legally reviewed - verify citations and sign numbers before production/commercial use",
        "total_questions": len(questions),
        "license": "CC BY-NC-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "license_note": (
            "Attribution-NonCommercial-ShareAlike: free to use, adapt, and "
            "redistribute for non-commercial exam-prep purposes, with credit "
            "and under the same license. We don't care about owning the data, "
            "only about helping people pass -- so commercial reuse needs a "
            "separate arrangement, but non-commercial prep tools/forks are welcome."
        ),
    },
    "questions": questions,
}

with open("pilot_questions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(questions)} questions to pilot_questions.json")
