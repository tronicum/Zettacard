#!/usr/bin/env python3
"""
Original schematic diagrams for the "gefahr" (hazard / road-condition)
pilot round (backlog card DN-27) - 28 of the 40 gefahr-topic questions
that genuinely benefit from a spatial/visual illustration (braking
distance, black ice location, aquaplaning, following-distance rules,
blind spots, roadside hazards, wind/gradient physics, etc). The other
12 gefahr questions are purely definitional/behavioural (blood-alcohol
effects, microsleep warning signs, medication labels, touchscreen vs
knob controls...) and were deliberately left without a diagram - see
the pilot report for the full skip list.

Reuses the flat/schematic aesthetic, muted palette and helper functions
(svg(), road_h(), road_v(), car(), badge(), arrow()) from
generate_diagrams.py so all diagrams in the app share one visual
language. Adds several NEW helper "visual vocabularies" for concepts
that don't fit the birds-eye intersection style of the original 7
Vorfahrt diagrams: wet/dry braking-distance lanes, a reaction/following
distance timeline, a black-ice hotspot icon, an aquaplaning water-film
cross-section, a blind-spot wedge, roadside-hazard scenes, a parked-car
row, a transit-stop scene, a truck-convoy sightline, a tire-tread
cross-section, a low-sun geometry scene, a crosswind bridge scene, a
downhill-gradient scene and a loose-gravel scene.

Entirely original composition for every scene below - not modeled on,
traced from, or composed to resemble any commercial driving-school or
Fragenkatalog illustration (see AGENTS.md constraint 1). Diagrams were
kept deliberately simple/abstract; where a concept felt like it might
edge toward a "known" exam-prep visual metaphor, the scene was
simplified further rather than made more elaborate.

Output: ./diagrams/<question-id>.svg and ./diagrams/<question-id>-answer.svg
(main() also copies both dirs the same way generate_signs.py /
generate_diagrams.py do - see main() below).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_diagrams import (  # noqa: E402
    svg, road_h, road_v, car, badge, arrow, VB,
    ROAD, LANE, CAR_YOU, CAR_OTHER, GREEN, AMBER, RED,
)

# --- extra palette for hazard scenes (kept muted, consistent with the
# existing background #eef1f8 / ROAD #8a93a8 / CAR_YOU #2f6fed family) ---
WATER = "#3f7fbf"
WATER_LIGHT = "#bcd6ec"
ICE = "#cfe3f2"
LEAF = "#8a7a3a"
SUN = "#e8a33d"
DARK = "#2a2a2a"
BLIND = "#c7ceda"
GRAVEL = "#a99a7a"
FONT = "Arial, sans-serif"

DIAGRAMS = {}
DIAGRAM_HL = {}  # extra elements added only in the "-answer" variant


def label(x, y, text, color=CAR_OTHER, size=11, weight="700", anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{text}</text>')


def person(cx, cy, color, scale=1.0, label_txt=""):
    s = scale
    body = f'''
  <g transform="translate({cx},{cy}) scale({s})">
    <circle cx="0" cy="-14" r="5" fill="{color}"/>
    <rect x="-4" y="-9" width="8" height="14" rx="3" fill="{color}"/>
    <line x1="-4" y1="5" x2="-7" y2="15" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
    <line x1="4" y1="5" x2="7" y2="15" stroke="{color}" stroke-width="3" stroke-linecap="round"/>
  </g>'''
    if label_txt:
        body += label(cx, cy + 26 * s, label_txt, color, size=10)
    return body


def animal(cx, cy, color=CAR_OTHER, scale=1.0):
    s = scale
    return f'''
  <g transform="translate({cx},{cy}) scale({s})">
    <ellipse cx="0" cy="0" rx="12" ry="7" fill="{color}"/>
    <circle cx="13" cy="-3" r="5" fill="{color}"/>
    <line x1="-9" y1="6" x2="-9" y2="14" stroke="{color}" stroke-width="3"/>
    <line x1="7" y1="6" x2="7" y2="14" stroke="{color}" stroke-width="3"/>
  </g>'''


# ---------------------------------------------------------------------
# Vocabulary 1: braking-distance comparison (two horizontal lanes, one
# dry one wet, car at the left edge of each, a stop-mark further along
# in whichever lane brakes worse).
# ---------------------------------------------------------------------
def braking_lanes(dry_frac=0.35, wet_frac=0.62, dry_label="trocken", wet_label="nass"):
    y1, y2 = 62, 142
    body = f'<rect x="0" y="{y1-24}" width="{VB}" height="48" fill="{ROAD}"/>'
    body += f'<line x1="0" y1="{y1}" x2="{VB}" y2="{y1}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
    body += f'<rect x="0" y="{y2-24}" width="{VB}" height="48" fill="{ROAD}"/>'
    # wet texture: light diagonal water sheen lines
    for i in range(4):
        xx = 20 + i * 45
        body += f'<line x1="{xx}" y1="{y2-16}" x2="{xx+18}" y2="{y2+16}" stroke="{WATER_LIGHT}" stroke-width="4" opacity="0.55"/>'
    body += f'<line x1="0" y1="{y2}" x2="{VB}" y2="{y2}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
    body += car(24, y1, 90, CAR_YOU)
    body += car(24, y2, 90, CAR_YOU)
    body += label(24, y1 - 30, dry_label, CAR_OTHER, size=11)
    body += label(24, y2 - 30, wet_label, WATER, size=11)
    return body


def braking_lanes_hl(dry_frac=0.35, wet_frac=0.62):
    y1, y2 = 62, 142
    dry_x = 24 + dry_frac * (VB - 40)
    wet_x = 24 + wet_frac * (VB - 40)
    body = f'<rect x="24" y="{y1-10}" width="{dry_x-24}" height="20" fill="{GREEN}" opacity="0.35"/>'
    body += f'<line x1="{dry_x}" y1="{y1-14}" x2="{dry_x}" y2="{y1+14}" stroke="{GREEN}" stroke-width="3"/>'
    body += f'<rect x="24" y="{y2-10}" width="{wet_x-24}" height="20" fill="{AMBER}" opacity="0.35"/>'
    body += f'<line x1="{wet_x}" y1="{y2-14}" x2="{wet_x}" y2="{y2+14}" stroke="{AMBER}" stroke-width="3"/>'
    body += label(dry_x, y1 + 30, "kurz", GREEN, size=10)
    body += label(wet_x, y2 + 30, "länger", AMBER, size=10)
    return body


# gefahr-01: rain lengthens braking distance
DIAGRAMS["gefahr-01"] = braking_lanes(dry_label="trocken", wet_label="nass")
DIAGRAM_HL["gefahr-01"] = braking_lanes_hl(0.32, 0.60)

# gefahr-18: braking distance ~4x when speed doubles (use two speed labels)
DIAGRAMS["gefahr-18"] = braking_lanes(dry_label="v", wet_label="2×v")
DIAGRAM_HL["gefahr-18"] = braking_lanes_hl(0.20, 0.80)


# ---------------------------------------------------------------------
# Vocabulary 2: reaction / following distance timeline (car, dashed
# "thinking" gap, then a solid brake-mark segment). Used for reaction
# distance itself, the "halber Tacho" and "3-second" following rules,
# tunnels, sudden-braking-ahead following distance and headlight range.
# ---------------------------------------------------------------------
def timeline_scene(show_lead_car=False, tunnel=False):
    y = 100
    body = ""
    if tunnel:
        body += f'<rect x="0" y="{y-55}" width="{VB}" height="110" fill="{DARK}"/>'
        body += f'<rect x="10" y="{y-40}" width="{VB-20}" height="80" fill="#3a3f4d"/>'
    body += road_h(y, w=50) if not tunnel else (
        f'<rect x="0" y="{y-25}" width="{VB}" height="50" fill="{ROAD}"/>'
        f'<line x1="0" y1="{y}" x2="{VB}" y2="{y}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
    )
    body += car(30, y, 90, CAR_YOU, "Sie")
    if show_lead_car:
        body += car(150, y, 90, CAR_OTHER)
    return body


def timeline_hl(gap_start=45, think_end=85, brake_end=140, gap_color=CAR_OTHER, brake_color=AMBER, note=""):
    y = 100
    body = f'<line x1="{gap_start}" y1="{y-35}" x2="{think_end}" y2="{y-35}" stroke="{gap_color}" stroke-width="3" stroke-dasharray="4,5"/>'
    body += label((gap_start + think_end) / 2, y - 42, "Reaktion", gap_color, size=8)
    body += f'<line x1="{think_end}" y1="{y-35}" x2="{brake_end}" y2="{y-35}" stroke="{brake_color}" stroke-width="4"/>'
    body += label((think_end + brake_end) / 2 + 8, y - 42, "Bremsweg", brake_color, size=8)
    if note:
        body += label(VB / 2, 188, note, CAR_OTHER, size=9)
    return body


# gefahr-05: reaction distance at 80 km/h (~24m in ~130ms; shown purely schematically)
DIAGRAMS["gefahr-05"] = timeline_scene()
DIAGRAM_HL["gefahr-05"] = timeline_hl(45, 85, 140, note="Reaktionsweg ≈ 24 m bei 80 km/h")

# gefahr-06: "halber Tacho" following-distance rule (gap sized to speed/2)
DIAGRAMS["gefahr-06"] = timeline_scene(show_lead_car=True)
DIAGRAM_HL["gefahr-06"] = (
    f'<line x1="45" y1="115" x2="140" y2="115" stroke="{GREEN}" stroke-width="3"/>'
    f'{arrow(45, 115, 60, 115, GREEN)}{arrow(140, 115, 125, 115, GREEN)}'
    + label(VB / 2, 175, "Abstand (m) ≥ Tempo/2", GREEN, size=9)
)

# gefahr-07: three-second rule (fixed point + count seconds)
DIAGRAMS["gefahr-07"] = timeline_scene(show_lead_car=True) + (
    f'<line x1="115" y1="55" x2="115" y2="145" stroke="{CAR_OTHER}" stroke-width="3" stroke-dasharray="2,4"/>'
    + label(115, 50, "Fixpunkt", CAR_OTHER, size=9)
)
DIAGRAM_HL["gefahr-07"] = label(VB / 2, 175, "min. 3 Sek. bis zum Fixpunkt", GREEN, size=9)

# gefahr-27: dense fog, ~50m visibility -> slow down, increase gap
DIAGRAMS["gefahr-27"] = (
    f'<rect x="0" y="0" width="{VB}" height="{VB}" fill="#dfe4ec"/>'
    + road_h(100, w=50) + car(35, 100, 90, CAR_YOU, "Sie")
    + f'<rect x="90" y="0" width="{VB-90}" height="{VB}" fill="#dfe4ec" opacity="0.88"/>'
    + car(150, 100, 90, CAR_OTHER)
)
DIAGRAM_HL["gefahr-27"] = (
    f'<line x1="60" y1="122" x2="120" y2="122" stroke="{AMBER}" stroke-width="3"/>'
    + arrow(60, 122, 45, 122, AMBER) + arrow(120, 122, 135, 122, AMBER)
    + label(VB / 2, 175, "mehr Abstand, weniger Tempo", AMBER, size=9)
)

# gefahr-37: tunnel - keep extra distance because rescue/escape is harder
DIAGRAMS["gefahr-37"] = timeline_scene(show_lead_car=True, tunnel=True)
DIAGRAM_HL["gefahr-37"] = (
    f'<line x1="45" y1="122" x2="140" y2="122" stroke="{AMBER}" stroke-width="3"/>'
    + arrow(45, 122, 60, 122, AMBER) + arrow(140, 122, 125, 122, AMBER)
    + label(VB / 2, 175, "mehr Abstand im Tunnel", AMBER, size=9)
)

# gefahr-38: sudden braking ahead - adequate following distance protects you
DIAGRAMS["gefahr-38"] = timeline_scene(show_lead_car=True) + (
    f'<rect x="145" y="88" width="10" height="24" rx="2" fill="{RED}"/>'  # lead car's brake light
)
DIAGRAM_HL["gefahr-38"] = (
    f'<line x1="45" y1="122" x2="140" y2="122" stroke="{GREEN}" stroke-width="3"/>'
    + arrow(45, 122, 60, 122, GREEN) + arrow(140, 122, 125, 122, GREEN)
    + label(VB / 2, 175, "Abstand fängt Vollbremsung ab", GREEN, size=9)
)

# gefahr-36: night speed matched to low-beam range (beam cone vs stop point)
def headlight_scene():
    y = 100
    body = f'<rect x="0" y="0" width="{VB}" height="{VB}" fill="#1c2230"/>'
    body += f'<rect x="0" y="{y-25}" width="{VB}" height="50" fill="#33394a"/>'
    body += f'<line x1="0" y1="{y}" x2="{VB}" y2="{y}" stroke="#5a6178" stroke-width="2" stroke-dasharray="8,8"/>'
    body += f'<polygon points="30,{y-10} 150,{y-45} 150,{y+45} 30,{y+10}" fill="#f2d98a" opacity="0.35"/>'
    body += car(25, y, 90, CAR_YOU)
    return body


DIAGRAMS["gefahr-36"] = headlight_scene()
DIAGRAM_HL["gefahr-36"] = (
    f'<line x1="150" y1="55" x2="150" y2="145" stroke="{GREEN}" stroke-width="3" stroke-dasharray="4,4"/>'
    + label(150, 45, "hier muss der", GREEN, size=9)
    + label(150, 165, "Bremsweg enden", GREEN, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 3: black-ice hotspot (bridge / shaded tree) - a raised
# bridge deck and a roadside tree casting shade, each with a pale icy
# patch that stands out from the otherwise plain road.
# ---------------------------------------------------------------------
def blackice_scene():
    body = road_h(100, w=44)
    # bridge on the left: piers + deck rail
    body += f'<rect x="10" y="70" width="70" height="8" fill="{CAR_OTHER}"/>'
    body += f'<rect x="15" y="122" width="6" height="26" fill="{CAR_OTHER}"/>'
    body += f'<rect x="65" y="122" width="6" height="26" fill="{CAR_OTHER}"/>'
    body += label(45, 62, "Brücke", CAR_OTHER, size=10)
    # tree on the right, casting shade over the road
    body += f'<circle cx="165" cy="55" r="16" fill="{GREEN}" opacity="0.7"/>'
    body += f'<rect x="162" y="55" width="6" height="20" fill="#5a4326"/>'
    body += label(165, 40, "Schatten", CAR_OTHER, size=10)
    return body


DIAGRAMS["gefahr-04"] = blackice_scene()
DIAGRAM_HL["gefahr-04"] = (
    f'<ellipse cx="45" cy="100" rx="30" ry="14" fill="{ICE}" opacity="0.9"/>'
    f'<ellipse cx="165" cy="105" rx="22" ry="12" fill="{ICE}" opacity="0.9"/>'
    + label(45, 130, "Glatteis", "#2f6fed", size=9) + label(165, 130, "Glatteis", "#2f6fed", size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 4: aquaplaning / water-film cross-section - a wheel shown
# from the side with a wavy water layer between tire and road.
# ---------------------------------------------------------------------
def aquaplane_scene(lifted=False):
    body = f'<rect x="0" y="150" width="{VB}" height="30" fill="{ROAD}"/>'
    # water sheet on the road
    for i in range(8):
        xx = 10 + i * 24
        body += f'<path d="M{xx},150 q6,-5 12,0 q6,5 12,0" stroke="{WATER}" stroke-width="2" fill="none"/>'
    lift = 10 if lifted else 0
    body += f'<circle cx="100" cy="{150-22-lift}" r="26" fill="{CAR_OTHER}"/>'
    body += f'<circle cx="100" cy="{150-22-lift}" r="10" fill="{LANE}"/>'
    body += car(100, 150 - 46 - lift, 0, CAR_YOU, "")
    return body


DIAGRAMS["gefahr-02"] = aquaplane_scene(lifted=False)
DIAGRAM_HL["gefahr-02"] = (
    f'<line x1="55" y1="150" x2="145" y2="150" stroke="{RED}" stroke-width="3"/>'
    + label(100, 142, "Wasserfilm hebt Reifen ab", RED, size=9)
)

# gefahr-25: deep puddle looks shallow (hidden depth cross-section)
def puddle_scene():
    body = road_h(120, w=60)
    body += f'<ellipse cx="120" cy="120" rx="34" ry="12" fill="{WATER}" opacity="0.85"/>'
    body += car(35, 120, 90, CAR_YOU)
    return body


DIAGRAMS["gefahr-25"] = puddle_scene()
DIAGRAM_HL["gefahr-25"] = (
    f'<line x1="120" y1="120" x2="120" y2="160" stroke="{RED}" stroke-width="2" stroke-dasharray="3,3"/>'
    + label(120, 172, "tiefer als sie aussieht", RED, size=9)
    + arrow(60, 130, 45, 145, RED, dashed=True)
    + label(70, 105, "Lenkruck möglich", RED, size=9)
)

# gefahr-26: worn tire tread vs new tread (aquaplaning risk factor). Tread
# grooves drawn as thick notches cut into the tire ring so the depth
# difference between the two tires reads clearly even at small size.
def tire_pair_scene():
    import math

    def tire(cx, groove_depth):
        b = f'<circle cx="{cx}" cy="100" r="32" fill="{CAR_OTHER}"/>'
        b += f'<circle cx="{cx}" cy="100" r="15" fill="{LANE}"/>'
        for i in range(8):
            ang = i * 45
            x1 = cx + 15 * math.cos(math.radians(ang))
            y1 = 100 + 15 * math.sin(math.radians(ang))
            x2 = cx + (15 + groove_depth) * math.cos(math.radians(ang))
            y2 = 100 + (15 + groove_depth) * math.sin(math.radians(ang))
            b += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{LANE}" stroke-width="5" stroke-linecap="round"/>'
        return b
    body = tire(55, 16)   # deep grooves reaching almost to the outer edge
    body += tire(145, 3)  # grooves barely worn in - tread almost flat
    body += label(55, 148, "neuer Reifen", CAR_OTHER, size=10)
    body += label(145, 148, "abgefahren", CAR_OTHER, size=10)
    return body


DIAGRAMS["gefahr-26"] = tire_pair_scene()
DIAGRAM_HL["gefahr-26"] = (
    f'<circle cx="55" cy="100" r="38" fill="none" stroke="{GREEN}" stroke-width="3"/>'
    f'<circle cx="145" cy="100" r="38" fill="none" stroke="{RED}" stroke-width="3"/>'
    # water pooling under the worn tire instead of being channeled away
    + f'<path d="M126,138 q19,-8 38,0 q-6,8 -19,8 q-13,0 -19,-8 Z" fill="{WATER}" opacity="0.75"/>'
    + label(55, 172, "leitet Wasser ab", GREEN, size=9)
    + label(145, 185, "hohes Risiko", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 5: blind-spot wedge (birds eye "you" car/truck with a
# shaded triangular zone beside/behind where mirrors can't see).
# ---------------------------------------------------------------------
def blindspot_scene(truck=False):
    body = road_v(100, w=90)
    body += f'<line x1="70" y1="0" x2="70" y2="{VB}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
    if truck:
        body += f'''<g transform="translate(85,130)">
        <rect x="-13" y="-30" width="26" height="60" rx="4" fill="{CAR_YOU}"/>
        <rect x="-11" y="-28" width="22" height="16" fill="{LANE}" opacity="0.6"/>
      </g>'''
        body += label(85, 172, "Lkw", CAR_YOU, size=10)
    else:
        body += car(85, 130, 180, CAR_YOU, "Sie")
    # shaded blind-spot wedge along the right side
    body += f'<polygon points="98,90 150,60 150,140" fill="{BLIND}" opacity="0.75"/>'
    body += label(160, 40, "toter Winkel", CAR_OTHER, size=9)
    return body


DIAGRAMS["gefahr-10"] = blindspot_scene()
DIAGRAM_HL["gefahr-10"] = car(120, 100, -90, RED, "") + label(120, 175, "unsichtbar!", RED, size=9)

DIAGRAMS["gefahr-24"] = blindspot_scene(truck=True)
DIAGRAM_HL["gefahr-24"] = (
    f'''<g transform="translate(120,80)">
    <circle cx="-9" cy="8" r="6" fill="{RED}"/><circle cx="9" cy="8" r="6" fill="{RED}"/>
    <path d="M-9 8 L0 -6 L9 8 M0 -6 L-4 8" stroke="{RED}" stroke-width="3" fill="none"/>
  </g>''' + label(120, 62, "Radfahrer unsichtbar", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 6: roadside hazard (birds-eye road + shoulder, a ball or
# a child figure near the edge, optionally a faded second child hidden
# behind a parked car for the "ball" scenario).
# ---------------------------------------------------------------------
def roadside_scene(kind):
    body = road_h(120, w=50)
    body += f'<rect x="0" y="95" width="{VB}" height="12" fill="#d8dbe4"/>'  # sidewalk strip
    body += car(30, 120, 90, CAR_YOU, "Sie")
    if kind == "ball":
        body += f'<circle cx="140" cy="112" r="7" fill="{AMBER}"/>'
        body += arrow(133, 108, 118, 128, AMBER, dashed=True)
    elif kind == "child":
        body += person(160, 78, CAR_OTHER, label_txt="Kind")
    elif kind == "school":
        body += person(140, 78, CAR_OTHER)
        body += person(158, 80, CAR_OTHER)
        body += person(170, 76, CAR_OTHER)
        body += label(155, 62, "Schule 13 Uhr", CAR_OTHER, size=9)
    return body


DIAGRAMS["gefahr-08"] = roadside_scene("ball")
DIAGRAM_HL["gefahr-08"] = (
    person(150, 62, RED, scale=0.8) + label(150, 44, "Kind folgt Ball?", RED, size=9)
    + label(VB / 2, 178, "Tempo runter", GREEN, size=9)
)

DIAGRAMS["gefahr-20"] = roadside_scene("child")
DIAGRAM_HL["gefahr-20"] = (
    f'<rect x="0" y="95" width="{VB}" height="12" fill="{AMBER}" opacity="0.35"/>'
    + label(VB / 2, 178, "bremsbereit, unberechenbar", AMBER, size=9)
)

DIAGRAMS["gefahr-33"] = roadside_scene("school")
DIAGRAM_HL["gefahr-33"] = (
    f'<rect x="0" y="95" width="{VB}" height="12" fill="{RED}" opacity="0.3"/>'
    + label(VB / 2, 178, "langsam, bremsbereit", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 7: parked-car row (birds-eye) with a passing car and a
# pedestrian who may step out from between two parked cars.
# ---------------------------------------------------------------------
def parked_row_scene():
    body = road_h(110, w=70)
    for cx in (40, 90, 140):
        body += f'''<g transform="translate({cx},142)">
      <rect x="-14" y="-9" width="28" height="18" rx="4" fill="{CAR_OTHER}"/>
    </g>'''
    body += car(20, 78, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-16"] = parked_row_scene()
DIAGRAM_HL["gefahr-16"] = (
    person(115, 122, RED, scale=0.75) + label(115, 178, "verdeckt zwischen Autos", RED, size=9)
    + arrow(20, 55, 20, 42, GREEN) + label(70, 38, "mehr Seitenabstand", GREEN, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 8: transit-stop scene (bus/tram stopped, doors open,
# passengers, approaching car).
# ---------------------------------------------------------------------
def transit_stop_scene(kind="bus"):
    body = road_h(120, w=60)
    if kind == "tram":
        veh = f'''<g transform="translate(150,120)">
      <rect x="-14" y="-18" width="28" height="36" rx="3" fill="{CAR_OTHER}"/>
      <line x1="-14" y1="-6" x2="14" y2="-6" stroke="#fff" stroke-width="2"/>
    </g>'''
        body += veh + label(150, 155, "Tram", CAR_OTHER, size=10)
        body += person(120, 100, CAR_OTHER, scale=0.8)
    else:
        veh = f'''<g transform="translate(150,150)">
      <rect x="-16" y="-11" width="32" height="22" rx="4" fill="{CAR_OTHER}"/>
      <rect x="8" y="-9" width="6" height="8" fill="{LANE}"/>
    </g>'''
        body += veh + label(150, 172, "Bus", CAR_OTHER, size=10)
    body += car(30, 90, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-09"] = transit_stop_scene("bus")
DIAGRAM_HL["gefahr-09"] = (
    f'<rect x="100" y="130" width="70" height="40" fill="{AMBER}" opacity="0.3"/>'
    + label(VB / 2, 188, "Tempo für Bus-Einfädeln anpassen", AMBER, size=9)
)

DIAGRAMS["gefahr-22"] = transit_stop_scene("tram")
DIAGRAM_HL["gefahr-22"] = (
    person(120, 100, RED, scale=0.8) + label(120, 78, "quert zur Haltestelle", RED, size=9)
    + label(VB / 2, 188, "sehr langsam fahren", AMBER, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 9: truck-convoy sightline (side view - truck ahead blocks
# the view; the dashed sightline only reaches past the truck once the
# gap is opened up).
# ---------------------------------------------------------------------
def convoy_scene():
    body = road_h(130, w=40)
    body += f'''<g transform="translate(140,116)">
    <rect x="-18" y="-26" width="36" height="34" rx="3" fill="{CAR_OTHER}"/>
  </g>'''
    body += label(140, 165, "Lastwagen", CAR_OTHER, size=10)
    body += car(60, 130, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-19"] = convoy_scene()
DIAGRAM_HL["gefahr-19"] = (
    f'<line x1="75" y1="108" x2="118" y2="90" stroke="{RED}" stroke-width="2" stroke-dasharray="3,3"/>'
    + label(95, 78, "Sicht versperrt", RED, size=9)
    + arrow(60, 150, 45, 150, GREEN) + label(VB / 2, 178, "mehr Abstand = früher erkennen", GREEN, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 10: wet leaves on the road (autumn) - leaf icons scattered
# over a lane, with a skid/yaw arrow in the answer variant.
# ---------------------------------------------------------------------
def leaves_scene():
    body = road_h(110, w=50)
    import random
    random.seed(23)
    for _ in range(14):
        x = random.randint(15, VB - 15)
        y = random.randint(95, 125)
        r = random.choice([-20, 10, 40])
        body += f'<g transform="translate({x},{y}) rotate({r})"><path d="M0,-6 Q6,0 0,6 Q-6,0 0,-6 Z" fill="{LEAF}"/></g>'
    body += car(30, 110, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-23"] = leaves_scene()
DIAGRAM_HL["gefahr-23"] = (
    f'<path d="M50,110 q30,-10 60,4" stroke="{RED}" stroke-width="3" fill="none" stroke-dasharray="4,4"/>'
    + label(100, 90, "Grip fast wie bei Glätte", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 11: unfenced pasture along a rural road with a grazing
# animal that could step onto the road.
# ---------------------------------------------------------------------
def pasture_scene():
    body = road_h(130, w=36)
    body += f'<rect x="0" y="0" width="{VB}" height="94" fill="#dcead9"/>'
    body += animal(60, 60)
    body += animal(120, 45, scale=0.8)
    body += car(30, 130, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-32"] = pasture_scene()
DIAGRAM_HL["gefahr-32"] = (
    arrow(60, 68, 60, 108, RED, dashed=True) + label(60, 122, "kein Zaun!", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 12: low-sun glare geometry - a sun icon low on the
# horizon at one end of an east-west road, with morning/evening icons.
# ---------------------------------------------------------------------
def sun_glare_scene():
    body = road_h(140, w=40)
    body += f'<rect x="0" y="0" width="{VB}" height="120" fill="#dfe8f3"/>'
    body += f'<circle cx="170" cy="115" r="16" fill="{SUN}"/>'
    for ang in range(0, 360, 45):
        import math
        x1 = 170 + 20 * math.cos(math.radians(ang))
        y1 = 115 + 20 * math.sin(math.radians(ang))
        x2 = 170 + 27 * math.cos(math.radians(ang))
        y2 = 115 + 27 * math.sin(math.radians(ang))
        body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{SUN}" stroke-width="2"/>'
    body += label(30, 128, "W", CAR_OTHER, size=11) + label(170, 90, "O", CAR_OTHER, size=11)
    body += car(35, 140, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-29"] = sun_glare_scene()
DIAGRAM_HL["gefahr-29"] = (
    f'<line x1="35" y1="140" x2="170" y2="115" stroke="{SUN}" stroke-width="2" stroke-dasharray="4,4"/>'
    + label(VB / 2, 165, "kurz nach Sonnenauf-/", AMBER, size=9)
    + label(VB / 2, 178, "vor Sonnenuntergang", AMBER, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 13: crosswind bridge - side view of a raised bridge deck,
# a car on it, and horizontal wind arrows pushing sideways.
# ---------------------------------------------------------------------
def wind_bridge_scene():
    body = f'<rect x="10" y="120" width="{VB-20}" height="8" fill="{CAR_OTHER}"/>'
    body += f'<rect x="20" y="128" width="6" height="30" fill="{CAR_OTHER}"/>'
    body += f'<rect x="{VB-26}" y="128" width="6" height="30" fill="{CAR_OTHER}"/>'
    body += car(100, 110, 0, CAR_YOU)
    for y in (60, 80, 100):
        body += arrow(10, y, 40, y, "#7a9bd6")
    return body


DIAGRAMS["gefahr-35"] = wind_bridge_scene()
DIAGRAM_HL["gefahr-35"] = (
    arrow(100, 105, 130, 105, RED, dashed=True) + label(130, 92, "seitlich verweht", RED, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 14: downhill gradient - side view of a steep descent, a
# fully-loaded car, and either an overheating-brake icon (wrong) or a
# low-gear icon (correct, highlighted in the answer variant).
# ---------------------------------------------------------------------
def downhill_scene():
    # diagonal descending road band (slope ~48 deg), car centred on it
    # oriented to travel down-and-right, matching the slope direction.
    body = f'<polygon points="20,20 60,20 180,170 140,170" fill="{ROAD}"/>'
    body += f'<line x1="40" y1="20" x2="160" y2="170" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
    body += car(70, 65, 130, CAR_YOU)
    body += label(60, 45, "voll beladen", CAR_OTHER, size=9)
    body += arrow(130, 110, 150, 135, CAR_OTHER)
    return body


DIAGRAMS["gefahr-40"] = downhill_scene()
DIAGRAM_HL["gefahr-40"] = (
    f'<circle cx="95" cy="90" r="9" fill="{RED}" opacity="0.85"/>'
    + label(120, 88, "Bremsen überhitzen", RED, size=9)
    + label(VB / 2, 188, "früh in niedrigen Gang schalten", GREEN, size=9)
)


# ---------------------------------------------------------------------
# Vocabulary 15: loose gravel road - scattered stone dots over a road
# band, car with a slight fishtail/yaw arrow in the answer variant.
# ---------------------------------------------------------------------
def gravel_scene():
    body = road_h(110, w=54)
    import random
    random.seed(7)
    for _ in range(40):
        x = random.randint(10, VB - 10)
        y = random.randint(88, 132)
        body += f'<circle cx="{x}" cy="{y}" r="2" fill="{GRAVEL}"/>'
    body += car(35, 110, 90, CAR_YOU, "Sie")
    return body


DIAGRAMS["gefahr-34"] = gravel_scene()
DIAGRAM_HL["gefahr-34"] = (
    f'<path d="M60,110 q20,14 45,0" stroke="{AMBER}" stroke-width="3" fill="none" stroke-dasharray="4,4"/>'
    + label(VB / 2, 178, "lose Steine: Ausbrechgefahr", AMBER, size=9)
)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dirs = [
        os.path.join(here, "diagrams"),
        os.path.join(here, "..", "app", "assets", "diagrams"),
    ]
    for out_dir in out_dirs:
        os.makedirs(out_dir, exist_ok=True)
        for qid, body in DIAGRAMS.items():
            with open(os.path.join(out_dir, f"{qid}.svg"), "w", encoding="utf-8") as f:
                f.write(svg(body))
            with open(os.path.join(out_dir, f"{qid}-answer.svg"), "w", encoding="utf-8") as f:
                f.write(svg(body + DIAGRAM_HL[qid]))
        print(f"Wrote {len(DIAGRAMS) * 2} hazard diagram SVGs to {out_dir}")


if __name__ == "__main__":
    main()
