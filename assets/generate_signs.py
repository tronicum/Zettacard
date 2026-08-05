#!/usr/bin/env python3
"""
Generates simplified, original SVG renderings of German traffic signs,
based on the shape/color/category specification published in the StVO's
own annexes (Anlage 1-4) - i.e. the LEGAL SPEC (a triangle warning sign is
red-bordered white/yellow with a black symbol; a prohibition sign is a
red-ringed white circle; a mandatory sign is a blue circle; etc.), not any
third-party company's artwork. Icons inside each sign are original simple
geometric pictograms, not traced from any existing sign-icon library.

Output: one <ref>.svg per entry in SIGNS, written to ./signs/<ref>.svg
(relative to this script's directory).
"""
import os

VB = 100  # square viewBox 0 0 100 100

def svg(body, viewbox=f"0 0 {VB} {VB}"):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
        f'role="img">\n{body}\n</svg>\n'
    )

# ---- shape templates -------------------------------------------------

def triangle_warning(symbol=""):
    # StVO Gefahrzeichen: white/yellow triangle, thick red border, black symbol
    return f'''
  <polygon points="50,6 96,90 4,90" fill="#fff" stroke="#c0272d" stroke-width="7" stroke-linejoin="round"/>
  {symbol}
'''

def circle_prohibition(symbol=""):
    # StVO Verbotszeichen: white circle, thick red ring
    return f'''
  <circle cx="50" cy="50" r="44" fill="#fff" stroke="#c0272d" stroke-width="9"/>
  {symbol}
'''

def circle_mandatory(symbol=""):
    # StVO Gebotszeichen: solid blue circle, white symbol
    return f'''
  <circle cx="50" cy="50" r="46" fill="#0058a3"/>
  {symbol}
'''

def square_blue(symbol=""):
    # StVO Richtzeichen (info, parking, motorway, pedestrian crossing): blue square
    return f'''
  <rect x="6" y="6" width="88" height="88" rx="4" fill="#0058a3"/>
  {symbol}
'''

def circle_end_restriction(symbol=""):
    # 278/282 Ende-signs (speed/overtaking restriction lifted): real signs
    # are NOT a recolored prohibition ring - they use a visibly THIN grey
    # ring (not the thick 9px prohibition-ring width) with grey numbers/
    # stripes, since the restriction is being lifted rather than imposed
    # (catalog-audit finding 2026-08-05: previous version reused
    # circle_prohibition's thick ring via a string-replace color hack).
    return f'''
  <circle cx="50" cy="50" r="44" fill="#fff" stroke="#8a8a8a" stroke-width="3"/>
  {symbol}
'''

def circle_no_entry(symbol=""):
    # Zeichen 267 Verbot der Einfahrt: this is NOT a white circle with a red
    # ring like other Verbotszeichen - it's a solid red disc (thin white
    # edge) with a white bar, same family as the international "no entry"
    # sign.
    return f'''
  <circle cx="50" cy="50" r="46" fill="#c0272d" stroke="#fff" stroke-width="3"/>
  {symbol}
'''

def circle_stopping_ban(symbol=""):
    # Zeichen 283/286 Halt-/eingeschraenktes Haltverbot: blue disc like a
    # Gebotszeichen, but (unlike ordinary mandatory signs) it also carries a
    # thick red border ring, since it's functionally a prohibition sign.
    return f'''
  <circle cx="50" cy="50" r="46" fill="#0058a3" stroke="#c0272d" stroke-width="8"/>
  {symbol}
'''

def diamond_yellow_border():
    # Zeichen 301 Vorfahrt: yellow diamond, white border
    return '''
  <polygon points="50,4 96,50 50,96 4,50" fill="#fff"/>
  <polygon points="50,12 88,50 50,88 12,50" fill="#f5c400"/>
'''

def priority_road(crossed=False):
    # Zeichen 306/307 Vorfahrtstrasse / Ende der Vorfahrtstrasse: same diamond
    # ("auf der Spitze stehendes Quadrat") family as Zeichen 301, NOT an
    # upright square - yellow diamond with a white border, no black outline.
    # 307 (end of priority road) adds a diagonal grey line through it, matching
    # the "end of ..." convention used elsewhere in this file (see 278/282).
    body = '''
  <polygon points="50,4 96,50 50,96 4,50" fill="#fff"/>
  <polygon points="50,12 88,50 50,88 12,50" fill="#f5c400"/>
'''
    if crossed:
        # 307 Ende der Vorfahrtstrasse: the yellow diamond itself stays
        # yellow (WebSearch-verified 2026-08-05 - a prior render looked gray
        # overall, a real user-reported design flaw) - only a thick black
        # "cancellation" band crosses it corner-to-corner, with two thin
        # white pinstripes running down the middle of that band.
        body += '''
  <line x1="16" y1="84" x2="84" y2="16" stroke="#1a1a1a" stroke-width="11"/>
  <line x1="13.3" y1="81.3" x2="81.3" y2="13.3" stroke="#fff" stroke-width="1.6"/>
  <line x1="18.7" y1="86.7" x2="86.7" y2="18.7" stroke="#fff" stroke-width="1.6"/>
'''
    return body

def yield_sign():
    # Zeichen 205 Vorfahrt gewaehren: downward triangle, red border, blank white
    return '''
  <polygon points="8,10 92,10 50,94" fill="#fff" stroke="#c0272d" stroke-width="9" stroke-linejoin="round"/>
'''

def stop_octagon():
    pts = []
    import math
    for i in range(8):
        a = math.pi/8 + i * math.pi/4
        pts.append((50 + 44*math.cos(a), 50 + 44*math.sin(a)))
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'''
  <polygon points="{pts_str}" fill="#c0272d" stroke="#fff" stroke-width="3"/>
  <text x="50" y="59" font-family="Arial, sans-serif" font-size="24" font-weight="700"
        fill="#fff" text-anchor="middle">STOP</text>
'''

def andreaskreuz():
    # 201 Andreaskreuz: each of the 4 arms is physically half white (the
    # inner half, towards the center) / half red (the outer tip) - there is
    # no separate white background plate behind the X, the arms themselves
    # carry the two colors (WebSearch-verified against the official
    # dimensioned schematic, 2026-08-05 user-reported design flaw - previous
    # version painted the whole X red with only a thin white pinstripe down
    # the middle, not true half-white/half-red arms).
    # This app renders signs directly on a white page background with no
    # backing plate of their own - a white-colored arm half would be
    # invisible there (an earlier draft of this fix had exactly that bug:
    # the white inner halves vanished, leaving 4 disconnected floating red
    # marks). A thin dark outline under the full arm keeps the white half
    # visible while still matching the real half-white/half-red arm design.
    cx, cy = 50, 50
    ends = [(10, 20), (90, 80), (90, 20), (10, 80)]
    body = ""
    for ex, ey in ends:
        mx, my = (cx + ex) / 2, (cy + ey) / 2
        body += f'<line x1="{cx}" y1="{cy}" x2="{ex}" y2="{ey}" stroke="#333" stroke-width="14" stroke-linecap="round"/>'
    for ex, ey in ends:
        mx, my = (cx + ex) / 2, (cy + ey) / 2
        body += (
            f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
            f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{ex}" y2="{ey}" stroke="#c0272d" stroke-width="10" stroke-linecap="round"/>'
        )
    return body

def gruenpfeil():
    # "Grünpfeil" plate: black square plate, green right-turn arrow
    return '''
  <rect x="8" y="8" width="84" height="84" rx="6" fill="#fff" stroke="#000" stroke-width="4"/>
  <rect x="16" y="16" width="68" height="68" rx="4" fill="#000"/>
  <path d="M32 32 L68 50 L32 68 Z" fill="#1f9d5c"/>
'''

def zusatzzeichen(symbol=""):
    # Zeichen 1000-series Zusatzzeichen (supplementary plate): white
    # rectangle, black border - default body is two blank lines (a generic
    # "text plate" look) unless a specific symbol/text is passed in, which
    # replaces the blank lines.
    if symbol:
        return f'''
  <rect x="6" y="30" width="88" height="40" fill="#fff" stroke="#000" stroke-width="4"/>
  {symbol}
'''
    return '''
  <rect x="6" y="30" width="88" height="40" fill="#fff" stroke="#000" stroke-width="4"/>
  <line x1="18" y1="44" x2="82" y2="44" stroke="#000" stroke-width="4"/>
  <line x1="18" y1="56" x2="60" y2="56" stroke="#000" stroke-width="4"/>
'''

def rect_white_black_border(symbol="", w=88, h=88):
    # StVO Richtzeichen that are plain white-background plates rather than
    # blue info signs (e.g. Zeichen 357 Sackgasse) - white rectangle, black
    # border, black symbol.
    x = (100 - w) / 2
    y = (100 - h) / 2
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#000" stroke-width="4"/>
  {symbol}
'''

def rect_yellow_black_border(symbol="", w=88, h=60):
    # Ortstafel (310/311) and route-number shields (e.g. Bundesstrasse 401):
    # yellow rectangle, black border, black text/symbol - NOT blue like the
    # Richtzeichen info-sign family (square_blue), and not a Gefahrzeichen
    # triangle either - this is its own real-world color/shape combination.
    x = (100 - w) / 2
    y = (100 - h) / 2
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#f5c400" stroke="#000" stroke-width="4"/>
  {symbol}
'''

def sign_arrow_yellow(text=""):
    # Pfeilwegweiser on non-Autobahn roads (Zeichen 415/418/432/434/437-439):
    # yellow background, black border, black text, cut to a point on one end
    # to show direction - distinct from the blue Autobahn-destination family
    # (sign_arrow_blue) which uses the same pointed shape but blue/white.
    return f'''
  <polygon points="4,20 78,20 96,50 78,80 4,80" fill="#f5c400" stroke="#000" stroke-width="4" stroke-linejoin="round"/>
  {text}
'''

def sign_arrow_blue(text=""):
    # Pfeilwegweiser zur Autobahn / Autobahn destination signs (Zeichen
    # 430/440/441): same pointed-arrow plate shape as sign_arrow_yellow, but
    # blue background with white text/symbol, matching the blue Autobahn
    # sign family (330.1 etc) rather than the yellow ordinary-road family.
    return f'''
  <polygon points="4,20 78,20 96,50 78,80 4,80" fill="#0058a3" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>
  {text}
'''

# ---- simple original symbol pictograms (black, for use inside triangles) --

def sym_exclaim():
    return '<rect x="46" y="38" width="8" height="24" fill="#000"/><circle cx="50" cy="70" r="4.5" fill="#000"/>'

def sym_crossroads():
    return '<line x1="50" y1="34" x2="50" y2="78" stroke="#000" stroke-width="6"/><line x1="30" y1="56" x2="70" y2="56" stroke="#000" stroke-width="6"/>'

def sym_narrowing():
    # 120 Verengte Fahrbahn (both sides): the real pictogram is two bold
    # SOLID black road-edge silhouettes bending inward symmetrically, not
    # thin wireframe lines (WebSearch-verified 2026-08-05 user-reported
    # design flaw - too basic/thin previously).
    return '''<path d="M18 28 L18 58 L38 80" stroke="#000" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M82 28 L82 58 L62 80" stroke="#000" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

def sym_roadworks():
    return '''<line x1="38" y1="80" x2="62" y2="38" stroke="#000" stroke-width="6" stroke-linecap="round"/>
  <rect x="56" y="34" width="10" height="14" rx="2" fill="#000"/>
  <path d="M30 80 Q50 68 70 80" stroke="#000" stroke-width="5" fill="none"/>'''

def sym_children():
    # 136 Kinder: real sign shows two RUNNING children of clearly different
    # heights (WebSearch-verified against the official pictogram, ~2026-08-05
    # user-reported design flaw) - the shorter/left figure and taller/right
    # figure need a visible size difference plus kicked-leg running poses and
    # large round child-proportioned heads, not near-identical adult-style
    # stick figures with a plain rectangle torso.
    return '''
  <circle cx="30" cy="50" r="7" fill="#000"/>
  <rect x="24" y="58" width="12" height="14" rx="4" fill="#000"/>
  <path d="M24 70 L14 78 M36 70 L42 62 M28 58 L18 50 M32 58 L42 54" stroke="#000" stroke-width="4.5" stroke-linecap="round"/>
  <circle cx="64" cy="42" r="9" fill="#000"/>
  <rect x="56" y="52" width="16" height="20" rx="5" fill="#000"/>
  <path d="M56 72 L44 82 M72 72 L82 66 M60 52 L48 42 M68 52 L82 46" stroke="#000" stroke-width="5.5" stroke-linecap="round"/>'''

def sym_train():
    return '''<rect x="34" y="40" width="32" height="24" rx="6" fill="#000"/>
  <circle cx="42" cy="70" r="5" fill="#000"/><circle cx="58" cy="70" r="5" fill="#000"/>
  <line x1="50" y1="30" x2="50" y2="40" stroke="#000" stroke-width="4"/>'''

def sym_arrow_right(color="#fff"):
    return f'<path d="M32 30 L68 50 L32 70 Z" fill="{color}"/>'

def sym_roundabout():
    # 215 Kreisverkehr: the real sign shows 3 SEPARATE white crescent arrows
    # arranged ~120 degrees apart in a pinwheel (not one continuous circular
    # arrow), rotating counterclockwise - the right-hand-traffic convention
    # (WebSearch-verified against the official pictogram, 2026-08-05 user-
    # reported design flaw: previous version was a single thin arc, unclear
    # as a roundabout symbol).
    import math
    cx, cy, r = 50, 50, 23
    body = ""
    for i in range(3):
        a0 = math.radians(i * 120 - 20)
        a1 = math.radians(i * 120 + 70)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        # Tangent direction at the arc's leading (counterclockwise) end,
        # used to point the arrowhead.
        tx, ty = -math.sin(a1), math.cos(a1)
        px, py = math.cos(a1), math.sin(a1)
        hx, hy = x1 + tx * 10, y1 + ty * 10
        lx, ly = x1 + px * 6, y1 + py * 6
        rx, ry = x1 - px * 6, y1 - py * 6
        body += (
            f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f}" '
            f'fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
            f'<polygon points="{lx:.1f},{ly:.1f} {hx:.1f},{hy:.1f} {rx:.1f},{ry:.1f}" fill="#fff"/>'
        )
    return body

def sym_oneway_arrow():
    # 220 Einbahnstrasse: the real sign carries the word "Einbahnstraße" as
    # well as the arrow - a pure pictogram-only arrow is missing part of the
    # real design (WebSearch-verified 2026-08-05 user-reported design flaw:
    # text was missing entirely). Arrow direction matches this project's own
    # question content ("weisser Pfeil nach oben") - pointing up.
    text = '''<text x="50" y="20" font-family="Arial, sans-serif" font-size="10.5" font-weight="700"
        fill="#fff" text-anchor="middle">EINBAHN-</text>
  <text x="50" y="31" font-family="Arial, sans-serif" font-size="10.5" font-weight="700"
        fill="#fff" text-anchor="middle">STRASSE</text>'''
    arrow = '<path d="M50 40 L70 62 L58 62 L58 86 L42 86 L42 62 L30 62 Z" fill="#fff"/>'
    return text + arrow

def sym_bicycle():
    # 237 Radweg: needs a clear seat-tube apex with a saddle knob, and a
    # distinct curved handlebar rising from the front-wheel area with a
    # small forward hook - a plain triangle without these reads as an
    # abstract shape rather than a bicycle (WebSearch-verified 2026-08-05
    # user-reported design flaw).
    return '''<circle cx="34" cy="66" r="12" fill="none" stroke="#fff" stroke-width="4"/>
  <circle cx="66" cy="66" r="12" fill="none" stroke="#fff" stroke-width="4"/>
  <path d="M34 66 L48 40 L66 66 M48 40 L42 66" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="48" cy="37" r="3.5" fill="#fff"/>
  <path d="M66 66 L60 46 Q58 39 65 37" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>'''

def sym_ped_bike_stack():
    # 240 Gemeinsamer Fuss- und Radweg: pedestrian pictogram on top, bicycle
    # pictogram below, divided by a HORIZONTAL line (no vertical line - that
    # feature belongs to 241's side-by-side split, see symB_bike_ped_split;
    # WebSearch-verified 2026-08-05 user-reported design flaw - previously
    # had no divider line at all, which read as unfinished/ambiguous).
    return '''<circle cx="50" cy="24" r="6" fill="#fff"/><rect x="44" y="31" width="12" height="16" rx="3" fill="#fff"/>
  <line x1="14" y1="55" x2="86" y2="55" stroke="#fff" stroke-width="3"/>
  <circle cx="38" cy="74" r="8" fill="none" stroke="#fff" stroke-width="3.5"/>
  <circle cx="62" cy="74" r="8" fill="none" stroke="#fff" stroke-width="3.5"/>
  <path d="M38 74 L50 60 L62 74" stroke="#fff" stroke-width="3.5" fill="none"/>'''

def sym_car_silhouette(color="#000"):
    return f'<rect x="26" y="46" width="48" height="18" rx="6" fill="{color}"/><circle cx="36" cy="66" r="5" fill="{color}"/><circle cx="64" cy="66" r="5" fill="{color}"/>'

def sym_moto_and_car(color="#000"):
    # 260 Verbot fuer Kraftraeder ... sowie fuer Kraftwagen und sonstige
    # mehrspurige Kraftfahrzeuge: the real sign prohibits BOTH motorcycles
    # AND cars, and shows two vehicle pictograms stacked vertically
    # (motorcycle+helmeted rider on top, car below), not a single car
    # silhouette (WebSearch-verified 2026-08-05 user-reported design flaw -
    # previous version showed one car only, "not even a motorcycle").
    moto = (
        f'<circle cx="34" cy="38" r="9" fill="none" stroke="{color}" stroke-width="4"/>'
        f'<circle cx="66" cy="38" r="9" fill="none" stroke="{color}" stroke-width="4"/>'
        f'<path d="M34 38 L46 24 L66 38 M46 24 L54 38" stroke="{color}" stroke-width="4" '
        f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="50" cy="14" r="6" fill="{color}"/>'
    )
    line = f'<line x1="18" y1="50" x2="82" y2="50" stroke="{color}" stroke-width="3"/>'
    car = (
        f'<rect x="28" y="60" width="44" height="15" rx="5" fill="{color}"/>'
        f'<circle cx="37" cy="78" r="4.5" fill="{color}"/><circle cx="63" cy="78" r="4.5" fill="{color}"/>'
    )
    return moto + line + car

def sym_two_cars(c1="#000", c2="#c0272d"):
    return sym_car_silhouette(c1).replace('x="26"', 'x="14"') + sym_car_silhouette(c2).replace('x="26"', 'x="38"').replace('cx="36"','cx="48"').replace('cx="64"','cx="76"')

def sym_speed_number(n):
    return f'<text x="50" y="63" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'

def sym_speed_number_crossed(n):
    return sym_speed_number(n) + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="6"/>'

def sym_speed_number_grey(n):
    # 278 Ende der Geschwindigkeitsbegrenzung: number itself is grey (not
    # solid black) to match the restriction-lifted look of the thin grey
    # ring in circle_end_restriction() (catalog-audit finding 2026-08-05).
    return f'<text x="50" y="63" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#8a8a8a" text-anchor="middle">{n}</text>'

def sym_five_stripes():
    lines = "".join(
        f'<line x1="{x}" y1="82" x2="{x+18}" y2="18" stroke="#8a8a8a" stroke-width="5"/>'
        for x in (6, 22, 38, 54, 70)
    )
    return lines

def sym_P(x=50, y=68, size=46):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="700" fill="#fff" text-anchor="middle">P</text>'

def sym_P_pavement():
    return sym_P(x=42, y=52, size=34) + '<rect x="16" y="70" width="68" height="8" fill="#fff"/><circle cx="26" cy="82" r="4" fill="#fff"/><circle cx="74" cy="82" r="4" fill="#fff"/>'

def sym_ped_crossing():
    # 350 Fussgaengerueberweg: blue square, white triangle, black walking-
    # person silhouette standing over a few short black zebra-stripe bars at
    # his feet. Fixed the stripe color here while auditing 293 vs 350
    # (2026-08-05): they were filled the same blue as the square background,
    # making them invisible - should be black like the person silhouette.
    body = '<polygon points="50,14 88,82 12,82" fill="#fff"/>'
    body += '<circle cx="50" cy="52" r="6" fill="#000"/><rect x="43" y="60" width="14" height="18" rx="4" fill="#000"/>'
    for x in (24, 34, 44, 54, 64, 74):
        body += f'<rect x="{x}" y="83" width="6" height="7" fill="#000"/>'
    return body

def sym_zebra_marking():
    # 293 is NOT the same real-world thing as 350: it's the painted zebra-
    # stripe ROAD MARKING itself (Anlage 2 zu Section 42 StVO), not the blue
    # pedestrian-crossing warning/notice sign - a distinct icon is needed
    # (WebSearch-verified 2026-08-05 user-reported design flaw: 293 was
    # previously mapped to the exact same icon as 350). Depicted as
    # alternating white stripes on asphalt gray, viewed from above, not as
    # a blue Richtzeichen square.
    body = '<rect x="6" y="6" width="88" height="88" rx="4" fill="#58595b"/>'
    for x in (13, 28, 43, 58, 73):
        body += f'<rect x="{x}" y="16" width="11" height="68" fill="#fff"/>'
    return body

def sym_motorway_start():
    return '''<path d="M20 78 L44 34 L56 34 L80 78 Z" fill="none" stroke="#fff" stroke-width="5"/>
  <line x1="30" y1="78" x2="46" y2="46" stroke="#fff" stroke-width="4"/>
  <line x1="70" y1="78" x2="54" y2="46" stroke="#fff" stroke-width="4"/>'''

def sym_motorway_end():
    return sym_motorway_start() + '<line x1="14" y1="86" x2="86" y2="14" stroke="#c0272d" stroke-width="6"/>'

def sym_no_entry_bar():
    return '<rect x="18" y="42" width="64" height="16" rx="3" fill="#fff"/>'

# ---- shared icon helpers for the extended (DN-30) sign catalog -----------
# Same minimalist original-geometry style as the icons above - simple
# silhouettes/pictograms, not traced from any real sign-icon library. Colour
# defaults to black (for a white-background plate); pass color="#fff" for
# use inside a red/blue solid-fill sign.

def sym_motorcycle(color="#000"):
    return f'''<circle cx="30" cy="66" r="9" fill="none" stroke="{color}" stroke-width="4"/>
  <circle cx="70" cy="66" r="9" fill="none" stroke="{color}" stroke-width="4"/>
  <path d="M30 66 L48 40 L70 66 M48 40 L58 40" stroke="{color}" stroke-width="4" fill="none" stroke-linejoin="round"/>'''

def sym_bus(color="#000"):
    return f'<rect x="22" y="34" width="56" height="34" rx="6" fill="{color}"/><circle cx="34" cy="72" r="6" fill="{color}"/><circle cx="66" cy="72" r="6" fill="{color}"/>'

def sym_truck(color="#000"):
    return f'''<rect x="16" y="42" width="40" height="22" fill="{color}"/><rect x="56" y="48" width="22" height="16" fill="{color}"/>
  <circle cx="30" cy="70" r="6" fill="{color}"/><circle cx="66" cy="70" r="6" fill="{color}"/>'''

def sym_truck_trailer(color="#000"):
    return sym_truck(color) + f'<rect x="14" y="40" width="6" height="24" fill="{color}"/>'

def sym_pedestrian(color="#000"):
    return f'<circle cx="50" cy="30" r="8" fill="{color}"/><rect x="41" y="40" width="18" height="26" rx="5" fill="{color}"/><path d="M41 66 L34 84 M59 66 L66 84" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'

def sym_horse_rider(color="#000"):
    return f'''<circle cx="42" cy="30" r="7" fill="{color}"/><rect x="36" y="38" width="14" height="16" rx="4" fill="{color}"/>
  <path d="M30 68 Q50 50 78 68 L78 74 L30 74 Z" fill="{color}"/>'''

def sym_moped(color="#000"):
    return f'''<circle cx="32" cy="68" r="8" fill="none" stroke="{color}" stroke-width="4"/>
  <circle cx="68" cy="68" r="8" fill="none" stroke="{color}" stroke-width="4"/>
  <path d="M32 68 L50 52 L68 68 M50 52 L50 42 L62 42" stroke="{color}" stroke-width="4" fill="none"/>'''

def sym_caravan(color="#000"):
    return f'<rect x="18" y="40" width="52" height="26" rx="4" fill="{color}"/><circle cx="32" cy="70" r="6" fill="{color}"/><circle cx="58" cy="70" r="6" fill="{color}"/><rect x="70" y="52" width="10" height="8" fill="{color}"/>'

def sym_weight(n="7,5t"):
    return f'<text x="50" y="60" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'

def sym_height(n="3,5m"):
    return f'''<path d="M30 20 L30 80 M70 20 L70 80" stroke="#000" stroke-width="4"/>
  <path d="M22 20 L38 20 M22 80 L38 80" stroke="#000" stroke-width="4"/>
  <text x="50" y="58" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'''

def sym_width(n="2,2m"):
    return f'''<path d="M20 50 L80 50" stroke="#000" stroke-width="4"/>
  <path d="M20 42 L20 58 M80 42 L80 58" stroke="#000" stroke-width="4"/>
  <text x="50" y="35" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'''

def sym_length(n="10m"):
    return sym_width(n)

def sym_snow_chain():
    # 268 Schneekettenpflicht: real sign shows a single wheel/tyre with a
    # visible chain-link diamond net wrapped over it - two identical open
    # circles read as an abstract Venn diagram, not tyre chains
    # (catalog-audit finding 2026-08-05: "illegible, doesn't suggest tire
    # chains at all").
    tyre = '<circle cx="50" cy="50" r="24" fill="none" stroke="#fff" stroke-width="6"/>'
    links = ""
    import math
    for i in range(8):
        a = math.radians(i * 45)
        x1, y1 = 50 + 16 * math.cos(a), 50 + 16 * math.sin(a)
        x2, y2 = 50 + 24 * math.cos(a), 50 + 24 * math.sin(a)
        links += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="3"/>'
    net = '<circle cx="50" cy="50" r="16" fill="none" stroke="#fff" stroke-width="3"/>'
    return tyre + links + net

def sym_house_car():
    # Verkehrsberuhigter Bereich (325.1): simplified house + car + child
    # pictogram - kept intentionally minimal, not a literal scene.
    return '''<polygon points="24,42 24,60 42,60 42,42 33,32" fill="#fff"/>
  <rect x="52" y="48" width="30" height="14" rx="4" fill="#fff"/><circle cx="59" cy="64" r="4" fill="#0058a3"/><circle cx="75" cy="64" r="4" fill="#0058a3"/>'''

def sym_deadend():
    return '''<line x1="50" y1="22" x2="50" y2="62" stroke="#000" stroke-width="6"/>
  <line x1="26" y1="62" x2="74" y2="62" stroke="#000" stroke-width="6"/>'''

def sym_first_aid_cross():
    return '<rect x="42" y="24" width="16" height="52" fill="#fff"/><rect x="24" y="42" width="52" height="16" fill="#fff"/>'

def sym_police_star():
    import math
    pts = []
    for i in range(10):
        r = 26 if i % 2 == 0 else 12
        a = -math.pi/2 + i * math.pi/5
        pts.append((50 + r*math.cos(a), 50 + r*math.sin(a)))
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{pts_str}" fill="#fff"/>'

def sym_fuel_pump():
    return '''<rect x="30" y="30" width="26" height="44" rx="3" fill="#fff"/>
  <path d="M56 42 L68 42 L68 66 Q68 72 62 72" stroke="#fff" stroke-width="4" fill="none"/>'''

def sym_bed():
    return '<rect x="20" y="52" width="60" height="18" fill="#fff"/><rect x="24" y="40" width="18" height="14" fill="#fff"/>'

def sym_cutlery():
    return '''<line x1="34" y1="26" x2="34" y2="74" stroke="#fff" stroke-width="4"/>
  <line x1="26" y1="26" x2="26" y2="46" stroke="#fff" stroke-width="4"/>
  <line x1="42" y1="26" x2="42" y2="46" stroke="#fff" stroke-width="4"/>
  <circle cx="66" cy="34" r="10" fill="none" stroke="#fff" stroke-width="4"/>
  <line x1="66" y1="44" x2="66" y2="74" stroke="#fff" stroke-width="4"/>'''

def sym_toilet():
    return '<circle cx="38" cy="30" r="7" fill="#fff"/><rect x="30" y="40" width="16" height="24" fill="#fff"/><circle cx="64" cy="30" r="7" fill="#fff"/><path d="M56 40 L72 40 L72 64 L56 64 Z" fill="#fff"/>'

def sym_phone():
    return '<path d="M32 28 Q28 50 40 64 Q54 78 74 72 L70 58 L58 62 Q50 56 46 46 L50 34 Z" fill="#fff"/>'

def sym_camp_tent():
    return '<polygon points="50,26 78,74 22,74" fill="none" stroke="#fff" stroke-width="5"/><line x1="50" y1="26" x2="50" y2="74" stroke="#fff" stroke-width="3"/>'

def sym_ev_plug():
    return '<circle cx="50" cy="50" r="20" fill="none" stroke="#fff" stroke-width="5"/><line x1="42" y1="42" x2="42" y2="50" stroke="#fff" stroke-width="4"/><line x1="58" y1="42" x2="58" y2="50" stroke="#fff" stroke-width="4"/><line x1="50" y1="58" x2="50" y2="66" stroke="#fff" stroke-width="4"/>'

def sym_wheelchair():
    return '<circle cx="46" cy="30" r="7" fill="#fff"/><path d="M46 40 L46 56 L64 56 M46 48 L60 48" stroke="#fff" stroke-width="4" fill="none"/><path d="M46 56 Q46 74 30 74 Q18 74 18 62" stroke="#fff" stroke-width="4" fill="none"/>'

def sym_uturn_ban():
    # 272 Verbot des Wendens: real pictogram is a closed "U"-shaped arrow -
    # a straight segment down on the right, a full semicircular sweep across
    # the bottom, and a straight segment back up on the left ending in an
    # arrowhead pointing up - the previous geometry (a shallow top arc plus
    # a separate hook) read as "turn right" rather than a proper U-turn loop
    # (catalog-audit finding 2026-08-05).
    return '''<path d="M66 22 L66 54 A18 18 0 0 1 30 54 L30 32" stroke="#000" stroke-width="7" fill="none" stroke-linecap="round"/>
  <polygon points="20,40 30,22 40,40" fill="#000"/>
  <line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'''

def sym_min_speed(n="30"):
    return f'<text x="50" y="58" font-family="Arial, sans-serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">{n}</text><line x1="26" y1="70" x2="74" y2="70" stroke="#fff" stroke-width="4"/>'

def sym_arrow_straight(color="#fff"):
    return f'<path d="M50 22 L68 44 L58 44 L58 78 L42 78 L42 44 L32 44 Z" fill="{color}"/>'

def sym_arrow_left(color="#fff"):
    return sym_arrow_right(color).replace('M32 30 L68 50 L32 70', 'M68 30 L32 50 L68 70')

def sym_arrow_both(color="#fff"):
    return f'<path d="M22 50 L36 38 L36 46 L64 46 L64 38 L78 50 L64 62 L64 54 L36 54 L36 62 Z" fill="{color}"/>'

def sym_arrow_straight_and_right(color="#fff"):
    # 214 Vorgeschriebene Fahrtrichtung (geradeaus und rechts): real sign is
    # a straight-up arrow (tip at top, same shape as sym_arrow_straight) with
    # a second branch peeling off the shaft and curving right, ending in its
    # own arrowhead - NOT a left/right choice; fixes a wrong-meaning bug
    # where sym_arrow_both (a horizontal left-right double arrow) was reused
    # here (catalog-audit finding 2026-08-05).
    straight = f'<path d="M50 20 L66 40 L58 40 L58 78 L42 78 L42 40 L34 40 Z" fill="{color}"/>'
    branch = (
        f'<path d="M58 58 Q78 58 78 40" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        f'<path d="M69 32 L82 37 L73 48 Z" fill="{color}"/>'
    )
    return straight + branch

def sym_arrow_bypass_right(color="#fff"):
    # 222 Vorgeschriebene Vorbeifahrt: real sign shows traffic being routed
    # AROUND an obstacle (a bent/offset arrow), distinct from the plain
    # rightward arrow already used for 209/211 - reusing the same icon made
    # 222 visually indistinguishable from those two unrelated signs
    # (catalog-audit finding 2026-08-05).
    return f'''<path d="M26 26 L26 58 Q26 70 38 70 L58 70" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M48 58 L64 70 L48 82 Z" fill="{color}"/>'''

def sym_tunnel_shape():
    return '<path d="M20 74 L20 46 Q20 22 50 22 Q80 22 80 46 L80 74" fill="none" stroke="#fff" stroke-width="6"/>'

def sym_breakdown_h():
    return '<text x="50" y="66" font-family="Arial, sans-serif" font-size="40" font-weight="700" fill="#fff" text-anchor="middle">H</text>'

def sym_taxi_text():
    return '<text x="50" y="60" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">TAXI</text>'

def sym_bike_dismount():
    return sym_bicycle().replace('fill="none" stroke="#fff"', 'fill="none" stroke="#000"') + '<line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'

# ==== DN-30: extended sign-catalog batches (Gefahr/Vorschrift/Richt/Zusatz) ====

# ==== Batch A (Gefahrzeichen) icon helpers ====
def symA_curve():
    # 103 Kurve (rechts): simple curved road-band bending right
    return '<path d="M25 78 C25 40 45 24 82 24" stroke="#000" stroke-width="8" fill="none" stroke-linecap="round"/>'

def symA_double_curve():
    # 105 Doppelkurve (zunaechst links): S-curve, left then right
    return '<path d="M22 78 C22 55 45 55 50 50 C55 45 78 45 78 22" stroke="#000" stroke-width="7" fill="none" stroke-linecap="round"/>'

def symA_gefaelle(pct="10"):
    # 108 Gefaelle: schematic downward road-profile (flat top, vertical
    # drop, diagonal slope) with grade percentage
    return f'''<path d="M20 36 L80 36 L80 76" fill="none" stroke="#000" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="20" y1="36" x2="80" y2="76" stroke="#000" stroke-width="6" stroke-linecap="round"/>
  <text x="40" y="60" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#000" text-anchor="middle">{pct}%</text>'''

def symA_steigung(pct="10"):
    # 110 Steigung: mirror of symA_gefaelle, road profile rising to the right
    return f'''<path d="M20 76 L80 76 L80 36" fill="none" stroke="#000" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="20" y1="76" x2="80" y2="36" stroke="#000" stroke-width="6" stroke-linecap="round"/>
  <text x="60" y="66" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#000" text-anchor="middle">{pct}%</text>'''

def symA_uneven():
    # 112 Unebene Fahrbahn: simple wavy/bumpy road-surface line
    return '<path d="M22 66 Q32 46 42 66 Q52 86 62 66 Q72 46 78 60" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round"/>'

def symA_skid():
    # 114 Schleuder- oder Rutschgefahr: car silhouette with skid-mark curves
    return '''<rect x="34" y="46" width="34" height="14" rx="5" fill="#000"/><circle cx="42" cy="62" r="4" fill="#000"/><circle cx="60" cy="62" r="4" fill="#000"/>
  <path d="M20 76 Q40 62 60 76" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M30 82 Q50 70 70 82" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'''

def symA_crosswind():
    # 117 Seitenwind: pole with a pennant/windsock blown sideways
    return '''<line x1="30" y1="30" x2="30" y2="80" stroke="#000" stroke-width="5"/>
  <path d="M30 34 L74 42 L60 50 L74 58 L30 50 Z" fill="#000"/>'''

def symA_narrow_one_side():
    # 121 einseitig verengte Fahrbahn (rechts): left edge unaffected, right
    # edge angles inward - bold SOLID black road-edge silhouettes to match
    # 120's style, not thin wireframe lines (WebSearch-verified 2026-08-05
    # user-reported design flaw - too basic previously).
    return '''<line x1="28" y1="28" x2="28" y2="80" stroke="#000" stroke-width="11" stroke-linecap="round"/>
  <path d="M78 28 L78 56 L54 80" stroke="#000" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

def symA_stau():
    # 124 Stau: a few stacked car-rectangles, receding into the distance
    return '''<rect x="22" y="60" width="20" height="12" rx="2" fill="#000"/>
  <rect x="46" y="52" width="20" height="12" rx="2" fill="#000"/>
  <rect x="70" y="44" width="14" height="10" rx="2" fill="#000"/>
  <line x1="18" y1="76" x2="88" y2="76" stroke="#000" stroke-width="3"/>'''

def symA_oncoming():
    # 125 Gegenverkehr: two opposing vertical arrows
    return '''<path d="M30 78 L30 30 L22 40 M30 30 L38 40" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M70 30 L70 78 L62 68 M70 78 L78 68" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

def symA_traffic_light():
    # 131 Lichtzeichenanlage: schematic traffic-light column, 3 lights
    return '''<rect x="40" y="24" width="20" height="46" rx="4" fill="none" stroke="#000" stroke-width="5"/>
  <circle cx="50" cy="34" r="5" fill="#000"/>
  <circle cx="50" cy="47" r="5" fill="#000"/>
  <circle cx="50" cy="60" r="5" fill="#000"/>
  <line x1="50" y1="70" x2="50" y2="82" stroke="#000" stroke-width="5"/>'''

def symA_radverkehr():
    # 138 Radverkehr: reuse the existing sym_bicycle() pictogram, recolored
    # black (its default #fff stroke is meant for use on a blue/red fill)
    return sym_bicycle().replace('stroke="#fff"', 'stroke="#000"')

def symA_wildlife():
    # 142 Wildwechsel: simple leaping-deer silhouette (rotated body, legs,
    # small antler lines) - schematic, not photorealistic
    return '''<ellipse cx="46" cy="52" rx="20" ry="10" fill="#000" transform="rotate(-15 46 52)"/>
  <path d="M30 58 L20 78 M38 60 L32 80 M60 46 L72 30 M64 50 L78 40" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M64 40 L58 28 M64 40 L70 30" stroke="#000" stroke-width="4" fill="none" stroke-linecap="round"/>'''

def symA_ped_crossing_warn():
    # 101-21: warning-triangle version of the pedestrian-crossing pictogram
    # (pedestrian figure over zebra-stripe blocks), all black - distinct
    # from Zeichen 293/350 (blue square, white pictogram) which mark the
    # crossing itself rather than warn of one ahead
    return '''<circle cx="50" cy="40" r="6" fill="#000"/><rect x="43" y="48" width="14" height="18" rx="4" fill="#000"/>
  <rect x="20" y="74" width="8" height="10" fill="#000"/><rect x="34" y="74" width="8" height="10" fill="#000"/>
  <rect x="48" y="74" width="8" height="10" fill="#000"/><rect x="62" y="74" width="8" height="10" fill="#000"/>'''

def symA_falling_rocks():
    # 101-25 Steinschlag: cliff/slope wedge with rock fragments falling
    return '''<path d="M14 82 L14 40 L46 20 L46 82 Z" fill="#000"/>
  <path d="M64 30 L74 42 L66 50 L58 42 Z" fill="#000"/>
  <path d="M70 54 L76 62 L70 68 L64 62 Z" fill="#000"/>'''

def symA_bake3_body():
    # 156 Bahnuebergang mit Bake, 3-streifig: this is NOT a Gefahrzeichen
    # triangle - it's a distinct StVO sign family (Bake, Anlage 1 lfd. Nr.
    # under Zeichen 156), a narrow white rectangular post/plate with three
    # red diagonal stripes, placed ~240m before an unguarded railway
    # crossing (2-stripe/1-stripe Baken follow closer to the crossing).
    # Rendered as its own standalone SVG body, not via triangle_warning().
    return '''
  <rect x="30" y="4" width="40" height="92" fill="#fff" stroke="#000" stroke-width="2"/>
  <path d="M30 24 L70 8" stroke="#c0272d" stroke-width="9"/>
  <path d="M30 50 L70 34" stroke="#c0272d" stroke-width="9"/>
  <path d="M30 76 L70 60" stroke="#c0272d" stroke-width="9"/>
'''

# ---- registry: ref -> svg body --------------------------------------------

# ==== Batch B (Vorschriftzeichen) icon helpers ====
def symB_bicycle_black():
    # black-stroke variant of sym_bicycle, for use inside circle_prohibition
    return sym_bicycle().replace('stroke="#fff"', 'stroke="#000"')

def symB_priority_arrows():
    # Zeichen 308: white arrow (own direction has priority) pointing up,
    # red arrow (oncoming direction must yield) pointing down, side by
    # side - matches the sign's real white-arrow/red-arrow convention.
    return '''
  <path d="M32 74 L32 32 L23 43 M32 32 L41 43" stroke="#fff" stroke-width="7"
        fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M68 26 L68 68 L59 57 M68 68 L77 57" stroke="#c0272d" stroke-width="7"
        fill="none" stroke-linecap="round" stroke-linejoin="round"/>
'''

def symB_bike_ped_split():
    # Zeichen 241 getrennter Rad- und Gehweg: pedestrian pictogram on the
    # LEFT, bicycle pictogram on the RIGHT, divided by a VERTICAL line - this
    # is the feature that actually distinguishes 241 from 240 (which stacks
    # the same two icons top/bottom with a HORIZONTAL line instead, see
    # sym_ped_bike_stack). Previous version had this backwards - stacked
    # top/bottom with a horizontal line, indistinguishable from 240
    # (WebSearch-verified 2026-08-05 user-reported design flaw).
    return '''
  <circle cx="24" cy="34" r="6" fill="#fff"/>
  <rect x="18" y="41" width="12" height="17" rx="3" fill="#fff"/>
  <path d="M18 58 L12 74 M30 58 L36 74" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
  <line x1="50" y1="14" x2="50" y2="90" stroke="#fff" stroke-width="3"/>
  <circle cx="66" cy="66" r="8" fill="none" stroke="#fff" stroke-width="3.5"/>
  <circle cx="84" cy="66" r="8" fill="none" stroke="#fff" stroke-width="3.5"/>
  <path d="M66 66 L75 44 L84 66 M75 44 L71 66" stroke="#fff" stroke-width="3.5" fill="none" stroke-linejoin="round"/>
'''

def symB_min_distance(n="70m"):
    # Zeichen 273 Mindestabstand: two small truck rectangles with a gap
    # between them and the minimum distance text - original simplified
    # pictogram, not a literal truck drawing.
    return f'''
  <rect x="8" y="34" width="24" height="14" rx="2" fill="#000"/>
  <rect x="68" y="34" width="24" height="14" rx="2" fill="#000"/>
  <line x1="36" y1="60" x2="64" y2="60" stroke="#000" stroke-width="3" stroke-dasharray="5,4"/>
  <text x="50" y="82" font-family="Arial, sans-serif" font-size="18" font-weight="700"
        fill="#000" text-anchor="middle">{n}</text>
'''

_GREY_END_LINE = '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="6"/>'

def symB_pedestrian_end():
    return sym_pedestrian(color="#fff") + _GREY_END_LINE

def symB_bicycle_end():
    return sym_bicycle() + _GREY_END_LINE

# ---- registry: code -> svg body ---------------------------------------

# ==== Batch C (Richtzeichen) icon helpers + new template ====
def rect_green_white_border(symbol="", w=88, h=60):
    # Zeichen 410 Europastrassen route shield: GREEN rectangle, white
    # border, white text/symbol - verified real color (NOT the yellow used
    # by the domestic Bundesstrasse/Ortstafel family) since European route
    # numbers (E 40 etc.) use the international green E-road convention.
    x = (100 - w) / 2
    y = (100 - h) / 2
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#1f7a3d" stroke="#fff" stroke-width="4"/>
  {symbol}
'''

# ---- new symC_ icon helpers (original minimalist pictograms) -----------

def symC_park_ride():
    # 316 Parken und Reisen: P plus a simple rail-car icon.
    return sym_P(x=32, y=64, size=38) + '''
  <rect x="54" y="40" width="28" height="20" rx="5" fill="#fff"/>
  <circle cx="61" cy="66" r="4" fill="#fff"/><circle cx="75" cy="66" r="4" fill="#fff"/>
  <line x1="68" y1="30" x2="68" y2="40" stroke="#fff" stroke-width="3"/>
'''

def symC_hiker_park():
    # 317 Wandererparkplatz: P plus a simple tree icon.
    return sym_P(x=32, y=64, size=38) + '''
  <polygon points="68,26 80,52 56,52" fill="#fff"/>
  <polygon points="68,38 82,62 54,62" fill="#fff"/>
  <rect x="65" y="62" width="6" height="12" fill="#fff"/>
'''

def symC_house_car_end():
    # 325.2 Ende verkehrsberuhigter Bereich: same pictogram as 325.1's
    # sym_house_car. Real sign uses a RED diagonal line (matching this
    # project's own already-correct 330.2 Ende der Autobahn via
    # sym_motorway_end()) - was incorrectly using the grey "end" convention
    # that belongs to speed/overtaking-restriction signs instead
    # (catalog-audit finding 2026-08-05).
    return sym_house_car() + '<line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'

def symC_car_end():
    # 331.2 Ende Kraftfahrstrasse: same car silhouette as 331.1, plus the
    # RED diagonal "end" line (matching 330.2's already-correct convention -
    # catalog-audit finding 2026-08-05, same root cause as 325.2 above).
    return sym_car_silhouette("#fff") + '<line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'

def symC_waterdrop():
    # 354 Wasserschutzgebiet: simple original water-drop silhouette.
    # NOTE: superseded by symC_water_truck() below (catalog-audit finding
    # 2026-08-05: real sign shows a tanker truck over wavy water lines, not
    # a generic drop) - kept defined in case it's still referenced elsewhere.
    return '<path d="M50 22 C62 40 74 54 74 66 A24 24 0 1 1 26 66 C26 54 38 40 50 22 Z" fill="#fff"/>'

def symC_water_truck():
    # 354 Wasserschutzgebiet: real sign shows a tanker-truck silhouette over
    # wavy water lines (catalog-audit finding 2026-08-05).
    truck = '''<rect x="22" y="32" width="40" height="18" rx="3" fill="#fff"/>
  <rect x="62" y="36" width="14" height="14" rx="2" fill="#fff"/>
  <ellipse cx="42" cy="41" rx="16" ry="6" fill="#0058a3"/>
  <circle cx="34" cy="54" r="5" fill="#fff"/><circle cx="58" cy="54" r="5" fill="#fff"/><circle cx="70" cy="54" r="4" fill="#fff"/>'''
    water = '''<path d="M16 66 Q26 60 36 66 Q46 72 56 66 Q66 60 84 66" stroke="#fff" stroke-width="4" fill="none"/>
  <path d="M16 76 Q26 70 36 76 Q46 82 56 76 Q66 70 84 76" stroke="#fff" stroke-width="4" fill="none"/>'''
    return truck + water

def _inset(symbol, cx=50, cy=36, s=0.5):
    # Scales/repositions a full-100x100-viewbox pictogram (e.g. sym_pedestrian,
    # sym_bicycle - shared helpers also used at full scale elsewhere) to fit
    # inside sign_zone_plate()'s inset circle, without rewriting those shared
    # helpers.
    return f'<g transform="translate({cx},{cy}) scale({s}) translate(-50,-50)">{symbol}</g>'

def sign_zone_plate(symbol, label_lines, ended=False):
    # 242.x/244.x (Fussgaengerzone/Fahrradstrasse Beginn/Ende): real signs
    # are a white plate with a black border, a solid blue INSET CIRCLE
    # (not a full-square blue fill) carrying the pictogram, plus printed
    # text below the circle - the "Ende" variants add a diagonal
    # black-and-white hatch band across the plate (catalog-audit finding
    # 2026-08-05: previous version was just square_blue(pictogram), missing
    # the plate/inset-circle/text entirely).
    circle = f'<circle cx="50" cy="36" r="26" fill="#0058a3"/>{symbol}'
    text = "".join(
        f'<text x="50" y="{72 + i * 13}" font-family="Arial, sans-serif" '
        f'font-size="11" font-weight="700" fill="#000" text-anchor="middle">{line}</text>'
        for i, line in enumerate(label_lines)
    )
    hatch = ""
    if ended:
        hatch = (
            '<line x1="12" y1="88" x2="88" y2="12" stroke="#000" stroke-width="6"/>'
            '<line x1="12" y1="88" x2="88" y2="12" stroke="#fff" stroke-width="6" stroke-dasharray="8 8"/>'
        )
    return rect_white_black_border(circle + text + hatch)

def symC_guard():
    # 356 Verkehrshelfer: simple original figure holding a stop-paddle.
    return '''
  <circle cx="42" cy="28" r="7" fill="#fff"/>
  <rect x="35" y="36" width="14" height="24" rx="4" fill="#fff"/>
  <line x1="49" y1="42" x2="70" y2="30" stroke="#fff" stroke-width="4"/>
  <rect x="66" y="20" width="16" height="16" fill="#fff"/>
  <line x1="38" y1="60" x2="30" y2="80" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
  <line x1="46" y1="60" x2="52" y2="80" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
'''

def symC_autohof():
    # 448.1 Autohof: simple fuel pump plus a small bed rectangle.
    return '''
  <rect x="18" y="34" width="20" height="34" rx="3" fill="#fff"/>
  <path d="M38 44 L48 44 L48 62 Q48 66 44 66" stroke="#fff" stroke-width="3.5" fill="none"/>
  <rect x="58" y="52" width="26" height="10" fill="#fff"/>
  <rect x="61" y="44" width="10" height="8" fill="#fff"/>
'''

def symC_breakdown_bay():
    # 328 Nothalte- und Pannenbucht: road line with a rectangular bay
    # recess, and a simple white car silhouette sitting in the bay -
    # explicitly NOT a letter "H".
    return '''
  <path d="M10 34 L34 34 L34 52 L66 52 L66 34 L90 34" fill="none" stroke="#fff" stroke-width="5"/>
  <rect x="40" y="56" width="20" height="12" rx="3" fill="#fff"/>
  <circle cx="46" cy="70" r="4" fill="#fff"/><circle cx="56" cy="70" r="4" fill="#fff"/>
'''

def symC_text(t, x=50, y=60, size=20, color="#000", weight="700"):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="middle">{t}</text>'

def symC_town_name(name="MUSTERSTADT", color="#000"):
    return symC_text(name, size=15, color=color)

def symC_town_name_leaving(name="MUSTERSTADT"):
    # 311 Ortstafel Rueckseite: same plate as 310, with a diagonal red
    # line through the town name to indicate you're leaving (project's
    # diagonal-line "end/leaving" convention, red here per the real sign).
    return symC_town_name(name) + '<line x1="18" y1="78" x2="82" y2="42" stroke="#c0272d" stroke-width="5"/>'

def symC_route_number(t="B 1", color="#000", size=28):
    return symC_text(t, size=size, color=color)

def symC_distance_table():
    # 453 Entfernungstafel: 2-3 lines of placeholder town/distance text,
    # reusing the plain white/black-border plate look.
    return '''
  <text x="50" y="34" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#000" text-anchor="middle">Musterstadt 12</text>
  <text x="50" y="54" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#000" text-anchor="middle">Beispieldorf 27</text>
  <text x="50" y="74" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#000" text-anchor="middle">Musterhausen 45</text>
'''

# ---- registry: ref -> svg body -----------------------------------------

# ==== Batch D (Zusatzzeichen) icon helpers ====
def symD_text(text, size=22, y=58):
    return (f'<text x="50" y="{y}" font-family="Arial, sans-serif" font-size="{size}" '
            f'font-weight="700" fill="#000" text-anchor="middle">{text}</text>')

def symD_text_lines(lines, size=16, start_y=42, dy=18):
    tspans = "".join(
        f'<tspan x="50" dy="{0 if i == 0 else dy}">{line}</tspan>'
        for i, line in enumerate(lines)
    )
    return (f'<text y="{start_y}" font-family="Arial, sans-serif" font-size="{size}" '
            f'font-weight="700" fill="#000" text-anchor="middle">{tspans}</text>')

def symD_priority_route():
    # Zeichen 1002 Verlauf der Vorfahrtstrasse: thick black line showing the
    # shape the priority road takes through the junction (here: straight,
    # then bending), plus a thin line for the crossing minor road.
    return '''
  <path d="M10 40 L55 40 L55 85" stroke="#000" stroke-width="8" fill="none" stroke-linejoin="round"/>
  <line x1="20" y1="70" x2="92" y2="70" stroke="#000" stroke-width="3"/>
'''

def symD_caravan_skid():
    # Zeichen 1006 Schleudergefahr fuer Wohnwagengespanne: caravan silhouette
    # plus a couple of simple wavy skid-mark lines behind it.
    return sym_caravan(color="#000") + '''
  <path d="M14 78 Q22 72 30 78 T46 78" stroke="#000" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M54 78 Q62 72 70 78 T86 78" stroke="#000" stroke-width="3" fill="none" stroke-linecap="round"/>
'''

def symD_bicycle_black_v2():
    return '''<circle cx="36" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <circle cx="64" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <path d="M36 64 L50 40 L64 64 M50 40 L44 64 M50 48 L60 48" stroke="#000" stroke-width="4" fill="none" stroke-linejoin="round"/>'''

def symD_bike_end():
    # Zeichen 1012-31 Ende Radweg: bicycle icon with a grey diagonal line,
    # matching this project's existing "end of ..." convention (grey, not
    # red, since it marks a limit/end rather than a prohibition - see
    # sym_speed_number_crossed / priority_road(crossed=True) elsewhere in
    # generate_signs.py).
    return symD_bicycle_black_v2() + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="6"/>'

def symD_bike_dismount_walk():
    # Zeichen 1012-32 Radfahrer absteigen: bicycle icon next to a small
    # walking-figure pictogram (cyclist walking the bike, not riding it).
    bike = '''<circle cx="26" cy="70" r="9" fill="none" stroke="#000" stroke-width="3.5"/>
  <circle cx="50" cy="70" r="9" fill="none" stroke="#000" stroke-width="3.5"/>
  <path d="M26 70 L38 48 L50 70 M38 48 L34 70 M38 54 L46 54" stroke="#000" stroke-width="3.5" fill="none" stroke-linejoin="round"/>'''
    walker = '''<circle cx="76" cy="34" r="6" fill="#000"/>
  <rect x="69" y="42" width="14" height="18" rx="4" fill="#000"/>
  <path d="M69 60 L62 78 M83 60 L88 78" stroke="#000" stroke-width="4" stroke-linecap="round"/>'''
    return bike + walker

def symD_wheelchair_black():
    return ('<circle cx="46" cy="30" r="7" fill="#000"/>'
            '<path d="M46 40 L46 56 L64 56 M46 48 L60 48" stroke="#000" stroke-width="4" fill="none"/>'
            '<path d="M46 56 Q46 74 30 74 Q18 74 18 62" stroke="#000" stroke-width="4" fill="none"/>')

def symD_shoulder_crossed():
    # Zeichen 1013-50 Seitenstreifen nicht befahrbar: two lane-marking lines
    # (carriageway + hard shoulder) with the shoulder line struck through in
    # grey, matching the "not usable"/limitation convention used elsewhere
    # in this project (grey diagonal = restriction on the plate's referent,
    # not a full prohibition).
    return '''
  <line x1="14" y1="40" x2="86" y2="40" stroke="#000" stroke-width="5"/>
  <line x1="14" y1="60" x2="86" y2="60" stroke="#000" stroke-width="5"/>
  <line x1="20" y1="72" x2="80" y2="30" stroke="#8a8a8a" stroke-width="6"/>
'''

# ---- registry ---------------------------------------------------------

# ---- registry: ref -> svg body ---------------------------------------

SIGNS = {
    "101": triangle_warning(sym_exclaim()),
    "102": triangle_warning(sym_crossroads()),
    "120": triangle_warning(sym_narrowing()),
    "123": triangle_warning(sym_roadworks()),
    # Zeichen 133 "Fussgaenger" (a single adult figure) and Zeichen 136
    # "Kinder" (two smaller figures) are two DIFFERENT real signs - the
    # project originally shipped the two-children pictogram mislabeled as
    # 133 (it's actually 136); fixed while auditing the wider catalog.
    "133": triangle_warning(sym_pedestrian()),
    "136": triangle_warning(sym_children()),
    "151": triangle_warning(sym_train()),
    "201": andreaskreuz(),
    "205": yield_sign(),
    "206": stop_octagon(),
    "209": circle_mandatory(sym_arrow_right()),
    "215": circle_mandatory(sym_roundabout()),
    "220": square_blue(sym_oneway_arrow()),
    "237": circle_mandatory(sym_bicycle()),
    "240": circle_mandatory(sym_ped_bike_stack()),
    "250": circle_prohibition(""),
    "260": circle_prohibition(sym_moto_and_car("#000")),
    "267": circle_no_entry(sym_no_entry_bar()),
    "274": circle_prohibition(sym_speed_number("50")),
    "276": circle_prohibition(sym_two_cars()),
    "278": circle_end_restriction(sym_speed_number_grey("50")),
    "282": circle_end_restriction(sym_five_stripes()),
    "283": circle_stopping_ban('<line x1="24" y1="24" x2="76" y2="76" stroke="#c0272d" stroke-width="8"/><line x1="76" y1="24" x2="24" y2="76" stroke="#c0272d" stroke-width="8"/>'),
    "286": circle_stopping_ban('<line x1="26" y1="26" x2="74" y2="74" stroke="#c0272d" stroke-width="8"/>'),
    "293": sym_zebra_marking(),
    "301": diamond_yellow_border(),
    "306": priority_road(crossed=False),
    "307": priority_road(crossed=True),
    "314": square_blue(sym_P()),
    "315": square_blue(sym_P_pavement()),
    "330-1": square_blue(sym_motorway_start()),
    "330-2": square_blue(sym_motorway_end()),
    "350": square_blue(sym_ped_crossing()),
    "720": gruenpfeil(),
    "zusatz": zusatzzeichen(),
}

# ---- DN-30 batch registries, merged into SIGNS above -------------------
BATCH_A_SIGNS = {
    "103": triangle_warning(symA_curve()),
    "105": triangle_warning(symA_double_curve()),
    "108": triangle_warning(symA_gefaelle("10")),
    "110": triangle_warning(symA_steigung("10")),
    "112": triangle_warning(symA_uneven()),
    "114": triangle_warning(symA_skid()),
    "117": triangle_warning(symA_crosswind()),
    "121": triangle_warning(symA_narrow_one_side()),
    "124": triangle_warning(symA_stau()),
    "125": triangle_warning(symA_oncoming()),
    "131": triangle_warning(symA_traffic_light()),
    "138": triangle_warning(symA_radverkehr()),
    "142": triangle_warning(symA_wildlife()),
    "101-21": triangle_warning(symA_ped_crossing_warn()),
    "101-25": triangle_warning(symA_falling_rocks()),
    # 156 is a Bake, not a Gefahrzeichen triangle - see symA_bake3_body()
    # docstring above for why it doesn't use triangle_warning().
    "156": symA_bake3_body(),
}

BATCH_B_SIGNS = {
    # -- mandatory-direction family (circle_mandatory) --
    "211": circle_mandatory(sym_arrow_right()),
    "214": circle_mandatory(sym_arrow_straight_and_right()),
    "222": circle_mandatory(sym_arrow_bypass_right()),
    "238": circle_mandatory(sym_horse_rider(color="#fff")),
    "239": circle_mandatory(sym_pedestrian(color="#fff")),
    "268": circle_mandatory(sym_snow_chain()),
    "275": circle_mandatory(sym_min_speed("30")),
    # 308 verified as blue SQUARE (Richtzeichen), not a blue circle
    "308": square_blue(symB_priority_arrows()),

    # -- prohibition family (circle_prohibition) --
    "251": circle_prohibition(sym_car_silhouette("#000")),
    "253": circle_prohibition(sym_truck()),
    "254": circle_prohibition(symB_bicycle_black()),
    "255": circle_prohibition(sym_motorcycle()),
    "257-50": circle_prohibition(sym_moped()),
    "257-51": circle_prohibition(sym_horse_rider()),
    "257-54": circle_prohibition(sym_bus()),
    "259": circle_prohibition(sym_pedestrian()),
    "262": circle_prohibition(sym_weight()),
    "264": circle_prohibition(sym_width()),
    "265": circle_prohibition(sym_height()),
    "266": circle_prohibition(sym_length()),
    "272": circle_prohibition(sym_uturn_ban()),
    "273": circle_prohibition(symB_min_distance("70m")),

    # -- verified-independently regulatory signs --
    "224": square_blue(sym_bus(color="#fff")),
    "229": square_blue(sym_taxi_text()),
    "241": square_blue(symB_bike_ped_split()),
    "242.1": sign_zone_plate(_inset(sym_pedestrian(color="#fff")), ["ZONE"]),
    "242.2": sign_zone_plate(_inset(sym_pedestrian(color="#fff")), ["ZONE"], ended=True),
    "244.1": sign_zone_plate(_inset(sym_bicycle()), ["Fahrradstrasse"]),
    "244.2": sign_zone_plate(_inset(sym_bicycle()), ["Fahrradstrasse"], ended=True),
    "245": square_blue(sym_bus(color="#fff")),
    "290.1": circle_stopping_ban('<line x1="26" y1="26" x2="74" y2="74" stroke="#c0272d" stroke-width="8"/>'),
    "290.2": circle_stopping_ban(
        '<line x1="26" y1="26" x2="74" y2="74" stroke="#c0272d" stroke-width="8"/>'
        '<line x1="74" y1="26" x2="26" y2="74" stroke="#8a8a8a" stroke-width="6"/>'
    ),
}

BATCH_C_SIGNS = {
    # -- blue-square family (12) --
    "316": square_blue(symC_park_ride()),
    "317": square_blue(symC_hiker_park()),
    "325.1": square_blue(sym_house_car()),
    "325.2": square_blue(symC_house_car_end()),
    "327": square_blue(sym_tunnel_shape()),
    "331.1": square_blue(sym_car_silhouette("#fff")),
    "331.2": square_blue(symC_car_end()),
    "354": square_blue(symC_water_truck()),
    "356": square_blue(symC_guard()),
    "358": square_blue(sym_first_aid_cross()),
    "363": square_blue(symC_text("Polizei", size=17, color="#fff")),
    "448.1": square_blue(symC_autohof()),
    # -- service-facility signs (6), verified blue-square family --
    "365-fuel": square_blue(sym_fuel_pump()),
    "365-rest": square_blue(sym_cutlery()),
    "365-phone": square_blue(sym_phone()),
    "365-camp": square_blue(sym_camp_tent()),
    "365-ev": square_blue(sym_ev_plug()),
    "365-wc": square_blue(sym_toilet()),
    # -- breakdown bay --
    "328": square_blue(symC_breakdown_bay()),
    # -- yellow/other family (8), colors verified --
    "310": rect_yellow_black_border(symC_town_name("MUSTERSTADT")),
    "311": rect_yellow_black_border(symC_town_name_leaving("MUSTERSTADT")),
    "401": rect_yellow_black_border(symC_route_number("B 1")),
    "410": rect_green_white_border(symC_route_number("E 40", color="#fff")),
    "415": sign_arrow_yellow(symC_route_number("Musterdorf", size=15)),
    "430": sign_arrow_blue(symC_route_number("A 1", color="#fff")),
    "437": rect_white_black_border(symC_text("Musterstrasse", size=14)),
    "453": rect_white_black_border(symC_distance_table()),
}

BATCH_D_SIGNS = {
    "1000": zusatzzeichen(sym_arrow_right(color="#000")),
    "1001": zusatzzeichen(symD_text("300 m", size=30)),
    "1002": zusatzzeichen(symD_priority_route()),
    "1006": zusatzzeichen(symD_caravan_skid()),
    "1010-51": zusatzzeichen(symD_text("Radfahrer frei", size=16)),
    "1010-60": zusatzzeichen(symD_text("Anlieger frei", size=17)),
    "1010-53": zusatzzeichen(symD_text("Mofa frei", size=19)),
    "1012-31": zusatzzeichen(symD_bike_end()),
    "1012-32": zusatzzeichen(symD_bike_dismount_walk()),
    "1020-11": zusatzzeichen(symD_wheelchair_black()),
    "1020-30": zusatzzeichen(symD_text_lines(["mit Parkausweis", "Nr. ... frei"], size=14)),
    "1013-50": zusatzzeichen(symD_shoulder_crossed()),
}

SIGNS.update(BATCH_A_SIGNS)
SIGNS.update(BATCH_B_SIGNS)
SIGNS.update(BATCH_C_SIGNS)
SIGNS.update(BATCH_D_SIGNS)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # Write to BOTH this script's own signs/ (kept as the readable source-of-
    # truth location next to generate_signs.py) AND app/assets/signs/ (the
    # path actually served to users) in the same run. A real bug found
    # 2026-08-05: these two directories had drifted apart for years - fixes
    # made here (including an earlier session's DN-32 zeichen-68/214 redraw)
    # were verified against assets/signs/ but never copied to app/, so they
    # were never actually live. Writing both every run removes the
    # "someone forgot to copy" failure mode entirely.
    out_dirs = [
        os.path.join(here, "signs"),
        os.path.join(here, "..", "app", "assets", "signs"),
    ]
    for out_dir in out_dirs:
        os.makedirs(out_dir, exist_ok=True)
        for ref, body in SIGNS.items():
            with open(os.path.join(out_dir, f"{ref}.svg"), "w", encoding="utf-8") as f:
                f.write(svg(body))
        print(f"Wrote {len(SIGNS)} sign SVGs to {out_dir}")

if __name__ == "__main__":
    main()
