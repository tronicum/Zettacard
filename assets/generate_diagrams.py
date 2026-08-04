#!/usr/bin/env python3
"""
Original birds-eye scenario diagrams for the 7 high_stakes Vorfahrt questions
that have no sign to illustrate (the scenario itself, not a sign, is what
needs to be understood). Simple schematic style: grey road bands, dashed
lane markings, small rounded-rectangle "cars" with a direction arrow, a
green marker on whoever has the right of way, an amber marker on whoever
must yield. Entirely original composition - not modeled on any specific
exam-prep company's diagram style.

Output: ./diagrams/<question-id>.svg
"""
import os, math

VB = 200

def svg(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB} {VB}" role="img">\n'
        f'<rect width="{VB}" height="{VB}" fill="#eef1f8"/>\n{body}\n</svg>\n'
    )

ROAD = "#8a93a8"
LANE = "#f5f7fb"
CAR_YOU = "#2f6fed"
CAR_OTHER = "#4a5266"
GREEN = "#1f9d5c"
AMBER = "#b5790a"
RED = "#c0272d"

def road_h(y, w=40):
    return f'<rect x="0" y="{y-w/2}" width="{VB}" height="{w}" fill="{ROAD}"/>' \
           f'<line x1="0" y1="{y}" x2="{VB}" y2="{y}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'

def road_v(x, w=40):
    return f'<rect x="{x-w/2}" y="0" width="{w}" height="{VB}" fill="{ROAD}"/>' \
           f'<line x1="{x}" y1="0" x2="{x}" y2="{VB}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'

def car(cx, cy, angle, color, label=""):
    # simple rounded rectangle car with a small triangular "front" indicator, rotated
    body = f'''
  <g transform="translate({cx},{cy}) rotate({angle})">
    <rect x="-9" y="-15" width="18" height="30" rx="5" fill="{color}"/>
    <polygon points="0,-19 -6,-11 6,-11" fill="{color}"/>
  </g>'''
    if label:
        body += f'<text x="{cx}" y="{cy+34}" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{color}" text-anchor="middle">{label}</text>'
    return body

def badge(cx, cy, symbol, color):
    return f'''
  <circle cx="{cx}" cy="{cy}" r="11" fill="{color}"/>
  <text x="{cx}" y="{cy+4}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{symbol}</text>'''

def arrow(x1, y1, x2, y2, color, dashed=False):
    dash = ' stroke-dasharray="5,5"' if dashed else ''
    return f'''
  <defs><marker id="ah-{x1}-{y1}-{x2}-{y2}" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
    <path d="M0,0 L8,4 L0,8 Z" fill="{color}"/></marker></defs>
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"{dash}
        marker-end="url(#ah-{x1}-{y1}-{x2}-{y2})"/>'''

# DIAGRAMS holds the neutral scene (no answer given away). DIAGRAM_BADGES
# holds the "who has priority" markers separately, so the app can show the
# neutral version while the question is unanswered and only reveal the
# marked-up version after the user hits "reveal answer" - otherwise the
# illustration itself gives away the answer before the user even guesses,
# which defeats the point of asking the question at all.
DIAGRAMS = {}
DIAGRAM_BADGES = {}

# vorfahrt-01: equal 4-way crossing, no signs - "you" from south, other from your right (east side street) -> other has priority (rechts vor links)
body = road_h(100) + road_v(100)
body += car(100, 165, 0, CAR_YOU, "Sie")
body += arrow(100, 155, 100, 128, CAR_YOU)
body += car(165, 100, -90, CAR_OTHER, "")
body += arrow(155, 100, 128, 100, CAR_OTHER)
DIAGRAMS["vorfahrt-01"] = body
DIAGRAM_BADGES["vorfahrt-01"] = badge(140, 78, "1", GREEN) + badge(78, 140, "2", AMBER)

# vorfahrt-07: you turning left, oncoming traffic goes straight -> oncoming has priority
body = road_h(100) + road_v(100)
body += car(100, 165, 0, CAR_YOU, "Sie")
body += arrow(100, 150, 65, 108, CAR_YOU, dashed=True)  # curving left path (approx as diagonal)
body += car(100, 35, 180, CAR_OTHER, "")
body += arrow(100, 50, 100, 95, CAR_OTHER)
DIAGRAMS["vorfahrt-07"] = body
DIAGRAM_BADGES["vorfahrt-07"] = badge(120, 60, "1", GREEN) + badge(80, 150, "2", AMBER)

# vorfahrt-09: tram from the right on a side street, you on the main road -> tram has priority (rail exception)
body = road_h(100) + road_v(100, w=26)
body += car(100, 165, 0, CAR_YOU, "Sie")
body += arrow(100, 155, 100, 128, CAR_YOU)
tram = f'''
  <g transform="translate(165,100) rotate(-90)">
    <rect x="-11" y="-17" width="22" height="34" rx="3" fill="{CAR_OTHER}"/>
    <line x1="-11" y1="-6" x2="11" y2="-6" stroke="#fff" stroke-width="2"/>
    <line x1="0" y1="-17" x2="0" y2="-24" stroke="#fff" stroke-width="2"/>
  </g>'''
body += tram + f'<text x="165" y="134" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{CAR_OTHER}" text-anchor="middle">Tram</text>'
body += arrow(155, 100, 128, 100, CAR_OTHER)
DIAGRAMS["vorfahrt-09"] = body
DIAGRAM_BADGES["vorfahrt-09"] = badge(140, 78, "1", GREEN) + badge(78, 140, "2", AMBER)

# vorfahrt-13: intersection, traffic light contradicts a police officer's hand signal -> officer wins
body = road_h(100) + road_v(100)
# traffic light icon (top right) - neutral, just shows there IS a light, no "overridden" mark pre-reveal
body += '<rect x="150" y="20" width="14" height="34" rx="3" fill="#2a2a2a"/>'
body += f'<circle cx="157" cy="29" r="5" fill="{RED}"/><circle cx="157" cy="37" r="5" fill="#4a4a4a"/><circle cx="157" cy="45" r="5" fill="#4a4a4a"/>'
# officer icon (center) with raised arm - showing the officer is neutral fact, not the answer
body += f'''
  <g transform="translate(100,100)">
    <circle cx="0" cy="-10" r="6" fill="{CAR_OTHER}"/>
    <rect x="-5" y="-4" width="10" height="16" rx="3" fill="{CAR_OTHER}"/>
    <line x1="5" y1="-2" x2="16" y2="-14" stroke="{CAR_OTHER}" stroke-width="4" stroke-linecap="round"/>
  </g>'''
body += f'<text x="100" y="128" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{CAR_OTHER}" text-anchor="middle">Polizist</text>'
DIAGRAMS["vorfahrt-13"] = body
DIAGRAM_BADGES["vorfahrt-13"] = (
    f'<line x1="148" y1="18" x2="166" y2="56" stroke="{AMBER}" stroke-width="3"/>'
    + badge(122, 78, "1", GREEN) + badge(178, 20, "2", AMBER)
)

# vorfahrt-17: you turn right, cyclist on a marked lane goes straight alongside -> cyclist has priority
body = road_h(100, w=50)
body += f'<rect x="0" y="{100-26-6}" width="{VB}" height="6" fill="#0058a3"/>'  # cycle lane marking just above the road
body += car(140, 100, 0, CAR_YOU, "Sie")
body += arrow(155, 100, 175, 118, CAR_YOU, dashed=True)  # curving right
bike = f'''
  <g transform="translate(60,70)">
    <circle cx="-9" cy="8" r="7" fill="none" stroke="{CAR_OTHER}" stroke-width="3"/>
    <circle cx="9" cy="8" r="7" fill="none" stroke="{CAR_OTHER}" stroke-width="3"/>
    <path d="M-9 8 L0 -6 L9 8 M0 -6 L-4 8" stroke="{CAR_OTHER}" stroke-width="3" fill="none"/>
  </g>'''
body += bike + f'<text x="60" y="96" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{CAR_OTHER}" text-anchor="middle">Radfahrer</text>'
body += arrow(90, 70, 150, 70, CAR_OTHER)
DIAGRAMS["vorfahrt-17"] = body
DIAGRAM_BADGES["vorfahrt-17"] = badge(150, 55, "1", GREEN) + badge(180, 105, "2", AMBER)

# vorfahrt-19: emergency vehicle approaching from behind on a 2-lane road, other cars form a corridor
body = road_v(100, w=100)
body += f'<line x1="70" y1="0" x2="70" y2="{VB}" stroke="{LANE}" stroke-width="2" stroke-dasharray="8,8"/>'
body += car(65, 60, 180, CAR_OTHER, "")
body += car(135, 40, 180, CAR_OTHER, "")
body += car(65, 145, 180, CAR_YOU, "Sie")
amb = f'''
  <g transform="translate(135,165) rotate(180)">
    <rect x="-10" y="-16" width="20" height="32" rx="4" fill="#fff" stroke="{RED}" stroke-width="3"/>
    <circle cx="0" cy="-4" r="4" fill="{CAR_OTHER}"/>
  </g>'''
body += amb + f'<text x="135" y="188" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{RED}" text-anchor="middle">Einsatz-</text>'
body += f'<text x="135" y="198" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{RED}" text-anchor="middle">fahrzeug</text>'
body += arrow(135, 156, 135, 120, RED)
DIAGRAMS["vorfahrt-19"] = body
DIAGRAM_BADGES["vorfahrt-19"] = badge(157, 145, "1", GREEN)

# vorfahrt-21: priority road crosses an unguarded rail crossing, train approaching -> train always wins
body = road_h(100)
# rail track diagonal
body += f'<line x1="0" y1="0" x2="{VB}" y2="{VB}" stroke="#4a4a4a" stroke-width="10"/>'
body += f'<line x1="0" y1="0" x2="{VB}" y2="{VB}" stroke="#d7deec" stroke-width="2" stroke-dasharray="6,10"/>'
body += car(40, 100, 0, CAR_YOU, "Sie")
body += arrow(55, 100, 85, 100, CAR_YOU)
train = f'''
  <g transform="translate(150,150) rotate(-45)">
    <rect x="-13" y="-20" width="26" height="40" rx="4" fill="{CAR_OTHER}"/>
    <line x1="-13" y1="-6" x2="13" y2="-6" stroke="#fff" stroke-width="2"/>
  </g>'''
body += train + f'<text x="150" y="180" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{CAR_OTHER}" text-anchor="middle">Zug</text>'
body += arrow(140, 140, 118, 118, CAR_OTHER)
DIAGRAMS["vorfahrt-21"] = body
DIAGRAM_BADGES["vorfahrt-21"] = (
    badge(172, 128, "1", GREEN)   # next to the train - the train wins regardless of road priority
    + badge(40, 78, "2", AMBER)   # next to "Sie" - must yield despite being on the priority road
)

def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")
    os.makedirs(out_dir, exist_ok=True)
    for qid, body in DIAGRAMS.items():
        # Plain version - shown before the answer is revealed. No priority markers.
        with open(os.path.join(out_dir, f"{qid}.svg"), "w", encoding="utf-8") as f:
            f.write(svg(body))
        # Answer version - shown after "reveal answer". Same scene + priority markers.
        with open(os.path.join(out_dir, f"{qid}-answer.svg"), "w", encoding="utf-8") as f:
            f.write(svg(body + DIAGRAM_BADGES[qid]))
    print(f"Wrote {len(DIAGRAMS)*2} diagram SVGs (plain + answer variants) to {out_dir}")

if __name__ == "__main__":
    main()
