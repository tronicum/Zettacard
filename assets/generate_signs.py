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

def circle_haltestelle(letter="H"):
    # Zeichen 224 Haltestelle (Linienverkehr und Schulbusse): re-audited
    # 2026-08-09 against the official ADAC brochure (p.6) plus an
    # independent WebSearch confirmation - this is NOT a blue square with a
    # bus pictogram at all (that was a 2026-08-06 round's mistake, probably
    # confusing it with 245 Bussonderfahrstreifen, which correctly IS a
    # blue square). The real 224 is a round sign: YELLOW disc, GREEN ring
    # border, GREEN "H" letter (Haltestelle) in the middle - its own
    # distinct colour family shared with no other sign in this catalog.
    return f'''
  <circle cx="50" cy="50" r="46" fill="#f5c400" stroke="#1f9d5c" stroke-width="7"/>
  <text x="50" y="66" font-family="Arial, sans-serif" font-size="50" font-weight="700"
        fill="#1f9d5c" text-anchor="middle">{letter}</text>
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

def priority_diamond_plain():
    # Zeichen 301 Vorfahrt: reverted 2026-08-09 - an earlier fix this same
    # session (priority_triangle()/symA_priority_cross(), a red triangle
    # with a black crossroads cross) was a confirmed regression, not a
    # correction. That shape is actually Zeichen 102 (Kreuzung oder
    # Einmuendung, a Gefahrzeichen warning about an intersection), a
    # completely different sign. The real Zeichen 301 is a plain yellow
    # diamond ("auf der Spitze stehendes Quadrat"), white border, no
    # pictogram at all - this is well-established (every German "Vorfahrt"
    # sign looks like this) and matches this project's own 2026-08-06
    # DN-46/DN-47 finding, which this restores verbatim. See priority_road()
    # below for 306/307, the visually similar but legally distinct
    # "Vorfahrtstrasse" signs (306 additionally carries a white diamond
    # inset to stay visually distinguishable from 301, which has none).
    return '''
  <polygon points="50,4 96,50 50,96 4,50" fill="#fff"/>
  <polygon points="50,12 88,50 50,88 12,50" fill="#f5c400"/>
'''

def priority_road(crossed=False):
    # Zeichen 306/307 Vorfahrtstrasse / Ende der Vorfahrtstrasse: same outer
    # diamond ("auf der Spitze stehendes Quadrat") family as Zeichen 301 -
    # white border, yellow fill - but 306 additionally carries a SMALLER
    # white diamond inset (thin black border) centered inside the yellow
    # field. That inner white diamond is what makes 306 a real,
    # distinguishable sign from 301: 301 marks right-of-way at a single
    # junction only (plain white-frame + yellow-fill diamond, nothing else
    # inside - see diamond_yellow_border() above), while 306 marks a
    # priority ROAD that continues across multiple junctions until 307
    # cancels it (catalog-audit finding 2026-08-06: 301 and 306 previously
    # shared byte-for-byte identical artwork via this same polygon pair,
    # which is wrong since they are two different signs with two different
    # meanings).
    body = '''
  <polygon points="50,4 96,50 50,96 4,50" fill="#fff"/>
  <polygon points="50,12 88,50 50,88 12,50" fill="#f5c400"/>
  <polygon points="50,30 71,50 50,70 29,50" fill="#fff" stroke="#1a1a1a" stroke-width="2.5"/>
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
    # "Gruenpfeil" plate (Zeichen 720): re-audited 2026-08-09 against the
    # official ADAC brochure (p.18) - the real sign is a plain BLACK square
    # (no separate white outer frame) with a bold GREEN ARROW (a shaft plus
    # a triangular head, white-outlined for contrast) pointing right. The
    # previous version's bare filled triangle (no shaft) reads as a "play"
    # button/wedge rather than a directional arrow - the exact same failure
    # mode this file's own sym_arrow_right() comment already documented and
    # fixed for other signs, just not carried over to this one.
    return '''
  <rect x="8" y="8" width="84" height="84" rx="6" fill="#000"/>
  <path d="M22 50 L60 50" stroke="#fff" stroke-width="15" stroke-linecap="round"/>
  <path d="M22 50 L58 50" stroke="#1f9d5c" stroke-width="9" stroke-linecap="round"/>
  <polygon points="50,28 82,50 50,72" fill="#fff"/>
  <polygon points="53,34 76,50 53,66" fill="#1f9d5c"/>
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
    # 102 Kreuzung oder Einmuendung mit Vorfahrt von rechts: the real
    # pictogram is a diagonal "X" (two crossing diagonals), NOT an upright
    # "+" - ADAC-brochure audit finding 2026-08-06 (previous version was
    # rotated 45 degrees off from the real sign).
    return '<line x1="32" y1="38" x2="68" y2="74" stroke="#000" stroke-width="6"/><line x1="68" y1="38" x2="32" y2="74" stroke="#000" stroke-width="6"/>'

def sym_narrowing():
    # 120 Verengte Fahrbahn (both sides): the real pictogram shows the two
    # road edges pinching INWARD toward the centre (the road narrowing),
    # then flaring back out at top and bottom - NOT a "wishbone" that
    # diverges/widens outward near the apex (ADAC-brochure audit finding
    # 2026-08-06: previous geometry only widened going down and never
    # converged). Bold solid black road-edge silhouettes, not thin wireframe
    # lines (earlier WebSearch-verified 2026-08-05 fix, kept here).
    # Fixed 2026-08-09 (user-reported): both top ends (40,22)/(60,22) sat
    # outside the triangle's interior at that height, crossing the red
    # border - moved the top ends down to y=36 where the triangle is wide
    # enough to actually contain them.
    return '''<path d="M40 36 Q46 55 40 78" stroke="#000" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M60 36 Q54 55 60 78" stroke="#000" stroke-width="9" fill="none" stroke-linecap="round"/>'''

def sym_roadworks():
    # 123 Arbeitsstelle: a recognizable construction-worker-with-shovel
    # silhouette (bent-over digging pose, head, shovel handle+blade, small
    # spoil heap) - not an ambiguous abstract squiggle (ADAC-brochure audit
    # finding 2026-08-06).
    return '''<circle cx="40" cy="30" r="6" fill="#000"/>
  <path d="M40 36 Q34 44 38 50" stroke="#000" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M38 50 L32 78 M38 50 L46 76" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M40 38 L64 64" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M58 58 L72 66 L68 74 L54 66 Z" fill="#000"/>
  <path d="M20 82 Q40 70 62 82" stroke="#000" stroke-width="5" fill="none"/>'''

def sym_children():
    # 136 Kinder: real sign shows two RUNNING children of clearly different
    # heights (WebSearch-verified against the official pictogram, ~2026-08-05
    # user-reported design flaw) - the shorter/left figure and taller/right
    # figure need a visible size difference plus kicked-leg running poses and
    # large round child-proportioned heads, not near-identical adult-style
    # stick figures with a plain rectangle torso.
    # Fixed 2026-08-09 (user-reported): the taller right figure's head and
    # raised arm reached outside the triangle's interior at that height
    # (checked against the triangle's actual width at each y, not just
    # eyeballed) - whole figure shifted left, and the raised-arm reach
    # shortened separately since shifting alone wasn't enough to clear it.
    return '''
  <circle cx="34" cy="50" r="7" fill="#000"/>
  <rect x="28" y="58" width="12" height="14" rx="4" fill="#000"/>
  <path d="M28 70 L18 78 M40 70 L46 62 M32 58 L22 50 M36 58 L46 54" stroke="#000" stroke-width="4.5" stroke-linecap="round"/>
  <circle cx="56" cy="42" r="9" fill="#000"/>
  <rect x="48" y="52" width="16" height="20" rx="5" fill="#000"/>
  <path d="M48 72 L36 82 M64 72 L74 68 M52 52 L40 42 M60 52 L66 48" stroke="#000" stroke-width="5.5" stroke-linecap="round"/>'''

def sym_train():
    # 151 Bahnuebergang ohne Schranken: a recognizable train/locomotive
    # FRONT silhouette - long low body, a clearly sloped/rounded nose
    # (rather than a boxy van-like front), a cab window set back from the
    # nose, a raised roofline with a small pantograph stub, and a visible
    # wheel/underframe strip - not a plain van/trolley box (ADAC-brochure
    # audit finding 2026-08-06: an earlier same-day fix attempt still read
    # as boxy/van-like once actually rendered).
    return '''<path d="M18 76 L18 58 Q18 50 26 48 L34 44 Q40 40 50 40 L66 40 Q72 40 72 48 L72 76 Z" fill="#000"/>
  <path d="M40 46 Q34 48 30 52 L26 58 L40 58 Z" fill="#fff"/>
  <rect x="48" y="46" width="16" height="12" rx="2" fill="#fff"/>
  <rect x="14" y="70" width="62" height="6" rx="2" fill="#000"/>
  <circle cx="30" cy="80" r="5" fill="#000"/><circle cx="50" cy="80" r="5" fill="#000"/><circle cx="66" cy="80" r="5" fill="#000"/>
  <line x1="58" y1="32" x2="58" y2="40" stroke="#000" stroke-width="4"/>
  <line x1="52" y1="28" x2="64" y2="28" stroke="#000" stroke-width="4"/>'''

def sym_arrow_right(color="#fff"):
    # A proper arrow glyph - a line shaft plus a triangular arrowhead - not
    # a bare filled triangle on its own (catalog-audit finding 2026-08-06:
    # the previous version was just a triangle, which reads as a "play"
    # button/wedge rather than a directional arrow; used e.g. by the 1000
    # Zusatzzeichen "Pfeil zeigt Richtung/Bereich an").
    return (f'<line x1="16" y1="50" x2="60" y2="50" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
            f'<polygon points="52,32 86,50 52,68" fill="{color}"/>')

def sym_arrow_right_bold(color="#fff"):
    # 211/211-10/211-20 Vorgeschriebene Fahrtrichtung hier rechts: a bold
    # SHAFTED, perfectly horizontal arrow - not the bare triangle-only
    # sym_arrow_right() (that thin glyph is reused for small
    # additional-panel icons elsewhere and is too weak to read as the
    # sign's sole pictogram) - pointing straight in the mandated direction.
    # RE-AUDITED 2026-08-09 against the official ADAC brochure (p.6) plus an
    # independent WebSearch confirmation ("VZ 211 zeigt einen horizontalen,
    # nach rechts weisenden Pfeil"): this straight arrow is 211's real
    # pictogram, and the BENT arrow below (sym_arrow_bend_junction) is
    # actually 209's - a 2026-08-06 round had these two swapped (assigned
    # this straight arrow to 209 and the bent one to 211), which was
    # backwards. Fixed at the SIGNS registry call sites, not just here.
    return f'<path d="M82 50 L54 26 L54 38 L18 38 L18 62 L54 62 L54 74 Z" fill="{color}"/>'

def sym_arrow_bend_junction(color="#fff"):
    # 209/209-10/209-20/209-30 Vorgeschriebene Fahrtrichtung (hier: rechts,
    # at a point where the road itself bends): the real sign shows a bold
    # arrow that CHANGES heading (rises vertically from below, then curves
    # into a new direction) - WebSearch-confirmed 2026-08-09 ("VZ 209 zeigt
    # einen vertikalen, nach rechts oben gebogenen Pfeil"). See the
    # sym_arrow_right_bold() comment above for the 209/211 swap this
    # corrects (a 2026-08-06 round had this bent arrow assigned to 211 and
    # the straight one to 209 - backwards).
    shaft = (
        f'<path d="M30 84 L30 46 Q30 28 48 28 L58 28" stroke="{color}" '
        f'stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    head = f'<polygon points="54,14 82,28 54,42" fill="{color}"/>'
    return shaft + head

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

def sym_bicycle(color="#fff"):
    # 237/138/254 Radweg / Radverkehr / Verbot fuer Radverkehr: a
    # bicycle-SPECIFIC silhouette with a visible diamond frame triangle
    # (chain stay + seat tube + seat stay forming the rear triangle; top
    # tube + down tube + fork forming the front triangle), plus a short
    # handlebar and seat-post/saddle stub - not the same abstract
    # "wishbone" two-wheels-plus-one-bent-line shape previously shared
    # (almost identically) with the motorcycle/moped icons, which made
    # 254/255/257-50 hard to tell apart (ADAC-brochure audit finding
    # 2026-08-06). Colour is expressed only via stroke="{color}" (never
    # fill) so the existing .replace('stroke="#fff"', 'stroke="#000"')
    # recolour hooks used elsewhere in this file keep working unchanged.
    return f'''<circle cx="30" cy="70" r="11" fill="none" stroke="{color}" stroke-width="4"/>
  <circle cx="72" cy="70" r="11" fill="none" stroke="{color}" stroke-width="4"/>
  <path d="M30 70 L50 70 L46 46 L30 70 M50 70 L64 46 L46 46 M64 46 L72 70" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M64 46 L74 40" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
  <line x1="46" y1="46" x2="42" y2="40" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'''

def sym_ped_bike_stack():
    # 240 Gemeinsamer Geh- und Radweg: RE-AUDITED 2026-08-09 against the
    # official ADAC brochure (p.6) - the real sign stacks the adult+child
    # pedestrian pictogram ON TOP, a HORIZONTAL divider line in the middle,
    # and the bicycle pictogram BELOW (a 2026-08-06 round had this side by
    # side with no divider at all, and used a single pedestrian instead of
    # the adult+child pair - both wrong; the side-by-side/vertical-divider
    # layout actually belongs to 241, see symB_bike_ped_split() below).
    ped = f'<g transform="translate(9,-8) scale(0.42)">{sym_ped_child(color="#fff")}</g>'
    divider = '<line x1="14" y1="50" x2="86" y2="50" stroke="#fff" stroke-width="3"/>'
    bike = f'<g transform="translate(18,52) scale(0.62)">{sym_bicycle(color="#fff")}</g>'
    return ped + divider + bike

def sym_car_silhouette(color="#000"):
    # 251/331.1 etc: a recognizable front/side car silhouette (bonnet,
    # windshield, raised roofline, sloped rear) rather than a shapeless
    # rounded box on two wheels that could be any vehicle (ADAC-brochure
    # audit finding 2026-08-06: previous version was just a rounded rect).
    # Added a light windshield/window cutout 2026-08-09 (user-reported: the
    # silhouette read as an all-black blob with no internal definition,
    # e.g. on sign 260) - a white cabin-window shape over the roofline,
    # matching the cutout-window convention already used elsewhere in this
    # file (e.g. sym_train()) rather than a fully solid silhouette.
    window = '#fff' if color != '#fff' else '#000'
    return (
        f'<path d="M16 66 L20 54 Q24 46 34 46 L40 46 L46 36 Q49 32 55 32 '
        f'L66 32 Q71 32 74 37 L79 46 Q88 46 90 54 L90 66 Z" fill="{color}"/>'
        f'<path d="M48 46 L52 40 Q54 37 58 37 L63 37 Q66 37 68 40 L71 46 Z" fill="{window}"/>'
        f'<circle cx="30" cy="70" r="7" fill="{color}"/>'
        f'<circle cx="76" cy="70" r="7" fill="{color}"/>'
    )

def sym_moto_and_car(color="#000"):
    # 260 Verbot fuer Kraftraeder ... sowie fuer Kraftwagen und sonstige
    # mehrspurige Kraftfahrzeuge: the real sign prohibits BOTH motorcycles
    # AND cars, and shows two vehicle pictograms stacked vertically
    # (motorcycle+helmeted rider on top, car below), divided by a
    # horizontal line - reuses the dedicated sym_motorcycle() and
    # sym_car_silhouette() pictograms (rather than a bespoke thin
    # "wishbone" motorcycle sketch) so 260's top figure is unmistakably a
    # motorcycle, not a bicycle/cyclist (ADAC-brochure audit finding
    # 2026-08-06).
    # Transforms below are computed from each pictogram's actual rendered
    # bounding box (not guessed) so the motorcycle sits entirely ABOVE the
    # divider line and the car sits entirely BELOW it, with a clear gap on
    # each side - the previous transforms pushed the car's roofline up
    # past the divider line, producing a stray thick bar cutting straight
    # through the car silhouette (ADAC-brochure audit finding 2026-08-06).
    moto = f'<g transform="translate(21.4,-2.6) scale(0.561)">{sym_motorcycle(color)}</g>'
    line = f'<line x1="18" y1="50" x2="82" y2="50" stroke="{color}" stroke-width="3"/>'
    car = f'<g transform="translate(5.3,25) scale(0.844)">{sym_car_silhouette(color)}</g>'
    return moto + line + car

def sym_two_cars(c1="#000", c2="#c0272d"):
    # 276 Ueberholverbot fuer Kraftfahrzeuge aller Art: TWO PASSENGER CARS
    # (one red, one black) in an overtaking pose - built from the shared
    # sym_car_silhouette() pictogram (positioned/scaled via <g transform>)
    # rather than brittle string-replace hacks tied to a since-changed
    # rect-based car shape (ADAC-brochure audit finding 2026-08-06).
    car1 = f'<g transform="translate(-4,10) scale(0.56)">{sym_car_silhouette(c1)}</g>'
    car2 = f'<g transform="translate(22,-6) scale(0.56)">{sym_car_silhouette(c2)}</g>'
    return car1 + car2

def sym_speed_number(n):
    return f'<text x="50" y="63" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'

def sym_speed_number_crossed(n):
    return sym_speed_number(n) + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="6"/>'

def sym_speed_number_grey(n):
    # 278 Ende der Geschwindigkeitsbegrenzung: number itself is grey (not
    # solid black) to match the restriction-lifted look of the thin grey
    # ring in circle_end_restriction() (catalog-audit finding 2026-08-05).
    # ADAC-brochure audit finding 2026-08-06: the real 278 pictogram also
    # carries the same grey diagonal-stripe pattern used by 282
    # (sym_five_stripes()) laid OVER the number - reused here rather than
    # a bare number with no "end of restriction" stripe cue at all.
    text = f'<text x="50" y="63" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#8a8a8a" text-anchor="middle">{n}</text>'
    return text + sym_five_stripes()

def sym_five_stripes():
    lines = "".join(
        f'<line x1="{x}" y1="82" x2="{x+18}" y2="18" stroke="#8a8a8a" stroke-width="5"/>'
        for x in (6, 22, 38, 54, 70)
    )
    return lines

def sym_P(x=50, y=68, size=46):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="700" fill="#fff" text-anchor="middle">P</text>'

def sym_P_pavement():
    # 315 Parken teilweise/ganz auf Gehwegen: a small car silhouette tilted
    # up onto a raised kerb/sidewalk step (one wheel on the road, one wheel
    # up on the pavement), plus a small "P" - the previous version was just
    # a "P" over a plain flat bar with two dots, which read as a generic
    # parking sign rather than "parking (partly) on the pavement"
    # (catalog-audit finding 2026-08-06).
    p = sym_P(x=24, y=36, size=22)
    curb = (
        '<line x1="14" y1="80" x2="54" y2="80" stroke="#fff" stroke-width="4"/>'
        '<line x1="54" y1="80" x2="54" y2="70" stroke="#fff" stroke-width="4"/>'
        '<line x1="54" y1="70" x2="88" y2="70" stroke="#fff" stroke-width="4"/>'
    )
    car = (
        '<g transform="rotate(-6 60 60)">'
        '<path d="M40 66 L43 58 Q46 53 53 53 L60 53 L64 47 Q66 44 71 44 L78 44 '
        'Q82 44 84 48 L88 53 Q94 53 95 58 L95 66 Z" fill="#fff"/>'
        '<circle cx="49" cy="70" r="5.5" fill="#fff"/>'
        '<circle cx="86" cy="70" r="5.5" fill="#fff"/>'
        '</g>'
    )
    return p + curb + car

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
    # 255 Verbot fuer Kraftraeder: a bulky, low-slung motorcycle-with-rider
    # silhouette matching the real Zeichen 255 pictogram (WebSearch/Commons-
    # verified 2026-08-06) - thick wheel rings, a solid low body block that
    # fuses the front fork, tank/seat hump and engine block into ONE filled
    # shape sitting BETWEEN the wheels (not a thin wishbone arc with a small
    # rectangle "engine" stuck on), plus a forward-leaning helmeted rider
    # with an arm reaching down to the handlebar grip. This is deliberately
    # bulkier/lower and structurally different from sym_bicycle()'s thin
    # diamond-frame wireframe, so 254 vs 255 are distinguishable at a glance
    # (previous version still read as "a bicycle with a blob rider").
    # NOTE: the body path's lower corners are kept ABOVE each wheel's
    # center (y=64, not y=75) so it only overlaps the ring's OUTER stroke
    # band rather than dipping into the ring's hollow middle - dipping into
    # the middle left an uneven, hard-edged white wedge showing through
    # the open part of the wheel (a real rendering artifact found while
    # visually inspecting this icon 2026-08-06, not merely a style choice).
    return f'''<circle cx="27" cy="75" r="12" fill="none" stroke="{color}" stroke-width="6.5"/>
  <circle cx="75" cy="75" r="12" fill="none" stroke="{color}" stroke-width="6.5"/>
  <path d="M27 64 Q29 56 40 55 Q43 46 52 45 Q60 44 64 49 Q69 54 69 60 Q80 60 80 68 L80 64 L68 64 L68 62 Q68 59 62 59 L42 59 Q38 59 37 62 L34 64 Z" fill="{color}"/>
  <path d="M40 55 L35 42" stroke="{color}" stroke-width="5.5" stroke-linecap="round"/>
  <path d="M31 40 L39 40" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
  <circle cx="42" cy="30" r="7.5" fill="{color}"/>
  <path d="M46 35 Q56 40 58 50" stroke="{color}" stroke-width="8.5" fill="none" stroke-linecap="round"/>
  <path d="M40 36 L34 41" stroke="{color}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'''

def sym_bus(color="#000"):
    # 257-54 Verbot fuer Kraftomnibusse: adds a row of small passenger
    # windows so the box reads as a bus, not an undifferentiated
    # box-on-wheels indistinguishable from the truck pictogram
    # (ADAC-brochure audit finding 2026-08-06). Window fill contrasts with
    # the body colour (blue windows on a white bus body when used on a
    # white/red background, white windows when used white-on-blue).
    window_color = "#0058a3" if color == "#fff" else "#fff"
    windows = "".join(
        f'<rect x="{x}" y="40" width="8" height="10" rx="1" fill="{window_color}"/>'
        for x in (28, 40, 52, 64)
    )
    return (
        f'<rect x="22" y="34" width="56" height="34" rx="6" fill="{color}"/>'
        f'{windows}'
        f'<circle cx="34" cy="72" r="6" fill="{color}"/><circle cx="66" cy="72" r="6" fill="{color}"/>'
    )

def sym_truck(color="#000"):
    # 253 Verbot fuer Kraftfahrzeuge ueber 3,5t: adds a cab window so the
    # cab reads clearly as a truck cab rather than a plain second box
    # welded to the cargo box (ADAC-brochure audit finding 2026-08-06).
    return f'''<rect x="16" y="42" width="40" height="22" fill="{color}"/><rect x="56" y="48" width="22" height="16" fill="{color}"/>
  <rect x="60" y="51" width="9" height="8" rx="1" fill="#fff"/>
  <circle cx="30" cy="70" r="6" fill="{color}"/><circle cx="66" cy="70" r="6" fill="{color}"/>'''

def sym_truck_trailer(color="#000"):
    return sym_truck(color) + f'<rect x="14" y="40" width="6" height="24" fill="{color}"/>'

def sym_pedestrian(color="#000"):
    # 133 (Fussgaenger warning) and 259 (Verbot fuer Fussgaenger): a proper
    # walking pedestrian silhouette - swinging arms and a forward/back
    # stride - matching the pose convention this app already uses correctly
    # for 101-21 (symA_ped_crossing_warn), reused here instead of a static
    # torso-with-straight-legs blob with no arms (ADAC-brochure audit
    # finding 2026-08-06). NOT used for 239/240/241/242.x - re-audited
    # 2026-08-09: the whole "Sonderweg/Sonderflaeche Fussgaenger" mandatory-
    # path family (239, 240, 241, 242.1, 242.2) shows an ADULT+CHILD pair,
    # not a single walking figure - see sym_ped_child() below, which a
    # 2026-08-06 round should have used for those refs instead of this one.
    return f'''<circle cx="50" cy="30" r="7" fill="{color}"/>
  <rect x="44" y="38" width="12" height="20" rx="5" fill="{color}"/>
  <path d="M46 42 L34 50 M54 42 L64 36" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
  <path d="M46 56 L36 76 M54 56 L62 72" stroke="{color}" stroke-width="5.5" stroke-linecap="round"/>'''

def sym_ped_child(color="#000"):
    # 239 Sonderweg Fussgaenger / 240 gemeinsamer Geh- und Radweg / 241
    # getrennter Rad- und Gehweg / 242.1/242.2 Fussgaengerzone: the real
    # pictogram for this whole family is an ADULT holding a CHILD's hand,
    # not a single walking figure (WebSearch-confirmed 2026-08-09: "Das
    # runde Verkehrszeichen zeigt 2 Personen in Weiss, einen Erwachsenen und
    # ein Kind in Bewegung" - also directly visible in the official ADAC
    # brochure, p.6). Adult on the left (taller, skirt-like lower body to
    # read distinctly as the "adult" figure per the real pictogram's
    # convention), smaller child on the right holding hands.
    adult = f'''<circle cx="30" cy="26" r="7" fill="{color}"/>
  <path d="M24 36 L20 62 L28 62 L30 48 L32 62 L40 62 L36 36 Z" fill="{color}"/>
  <path d="M30 40 L42 46" stroke="{color}" stroke-width="4.5" stroke-linecap="round"/>'''
    child = f'''<circle cx="62" cy="46" r="5.5" fill="{color}"/>
  <rect x="57" y="53" width="11" height="14" rx="4" fill="{color}"/>
  <path d="M58 67 L52 80 M67 67 L73 80" stroke="{color}" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M58 57 L47 47" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'''
    return adult + child

def sym_horse_rider(color="#000"):
    # 257-51/238: a horse-and-rider silhouette, redrawn a FOURTH time
    # 2026-08-09 (BACKLOG's own history: earlier organic-curve attempts kept
    # reading as "a llama/table" or "a dog/donkey" even after their own
    # render checks - this project's standing lesson that curvy hand-tuned
    # bezier silhouettes are hard to get right without many render/inspect
    # cycles). This version deliberately uses simple, blocky, kid's-drawing
    # geometry instead: a rounded-rectangle barrel body, a STRAIGHT tapering
    # polygon wedge (not a multi-curve path) for the neck+head ending in a
    # clearly pointed nose, jagged mane teeth along the neck's top edge (a
    # concrete visual cue a "dog" silhouette lacks), 4 straight legs evenly
    # spaced directly under the body (kept simple rather than angled, since
    # angling was tried before and the head/neck shape - not the legs - was
    # the actual repeat failure point), and a distinctly separate rider
    # (round head clearly floating above the horse's back, short torso,
    # one leg) so the two silhouettes don't visually merge into one blob.
    body = f'<rect x="14" y="52" width="44" height="20" rx="10" fill="{color}"/>'
    # A SHORT, thick neck (a stroke, not a big filled wedge - an earlier
    # attempt's oversized wedge read as a paper airplane/flag; a longer
    # thin neck after that read as a giraffe) rising only slightly above
    # the body line to a small head - horses carry their head roughly
    # level with/just above the back, not high up like a giraffe.
    neck = f'<path d="M48 56 Q55 44 62 38" stroke="{color}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    head = f'<ellipse cx="67" cy="35" rx="8.5" ry="6.5" fill="{color}"/>'
    snout = f'<polygon points="73,33 86,36 73,40" fill="{color}"/>'
    ear = f'<path d="M64 30 L62 21 L70 26 Z" fill="{color}"/>'
    tail = f'<path d="M15 54 Q6 52 6 64 Q9 72 16 68" stroke="{color}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    legs = (
        f'<rect x="19" y="70" width="7" height="20" rx="2" fill="{color}"/>'
        f'<rect x="33" y="70" width="7" height="20" rx="2" fill="{color}"/>'
        f'<rect x="45" y="70" width="7" height="20" rx="2" fill="{color}"/>'
        f'<rect x="57" y="70" width="7" height="20" rx="2" fill="{color}"/>'
    )
    rider_head = f'<circle cx="32" cy="34" r="7.5" fill="{color}"/>'
    rider_torso = f'<rect x="27" y="41" width="11" height="16" rx="4" fill="{color}"/>'
    rider_leg = f'<path d="M29 55 Q24 62 26 70" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return body + neck + head + snout + ear + tail + legs + rider_head + rider_torso + rider_leg

def sym_moped(color="#000"):
    # 257-50 Verbot fuer Mofas: matches the real Zeichen 257-50 pictogram
    # (WebSearch/Commons-verified 2026-08-06) - a bare Mofa with NO rider
    # (unlike 255's motorcycle+rider), smaller/thinner wheel rings than the
    # motorcycle, a curved gooseneck frame rising to a low peak near the
    # front fork, and a small luggage rack/box sitting above the rear
    # wheel - structurally distinct from both the motorcycle's bulky
    # low body+rider silhouette and the bicycle's thin diamond frame
    # (previous version was a near-duplicate of the other two).
    return f'''<circle cx="27" cy="76" r="10.5" fill="none" stroke="{color}" stroke-width="5"/>
  <circle cx="73" cy="76" r="10.5" fill="none" stroke="{color}" stroke-width="5"/>
  <path d="M27 76 L34 62 Q38 52 46 50 Q40 62 44 66 L58 66 Q62 66 62 70 L62 76" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M46 50 L52 42" stroke="{color}" stroke-width="5" stroke-linecap="round"/>
  <rect x="58" y="54" width="16" height="9" rx="1.5" fill="{color}"/>'''

def sym_caravan(color="#000"):
    return f'<rect x="18" y="40" width="52" height="26" rx="4" fill="{color}"/><circle cx="32" cy="70" r="6" fill="{color}"/><circle cx="58" cy="70" r="6" fill="{color}"/><rect x="70" y="52" width="10" height="8" fill="{color}"/>'

def sym_weight(n="7,5t"):
    return f'<text x="50" y="60" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'

def sym_height(n="3,5m"):
    # 265 Verbot fuer zu hohe Fahrzeuge: real pictogram is a solid black
    # triangle pointing DOWN above the number and a solid black triangle
    # pointing UP below it (sandwiching the height value vertically) - not
    # the 264 "I-beam bar" convention rotated 90 degrees, and the number
    # must sit clear of both triangles instead of visually colliding with
    # a bar (ADAC-brochure audit finding 2026-08-06: previous version used
    # two full-height vertical bars with T-caps, with the number
    # overlapping the left bar).
    return f'''<polygon points="30,18 70,18 50,30" fill="#000"/>
  <polygon points="30,82 70,82 50,70" fill="#000"/>
  <text x="50" y="58" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'''

def sym_width(n="2,2m"):
    # 264 Verbot fuer zu breite Fahrzeuge: real pictogram uses solid black
    # TRIANGULAR pointers flanking the width value left/right (apex
    # pointing inward toward the number), not a plain "I-beam" bar with
    # flat end-caps (ADAC-brochure audit finding 2026-08-06).
    return f'''<polygon points="16,40 16,60 30,50" fill="#000"/>
  <polygon points="84,40 84,60 70,50" fill="#000"/>
  <text x="50" y="58" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'''

def sym_length(n="10m"):
    # 266 Verbot fuer zu lange Fahrzeuge: official sign shows a truck
    # pictogram ABOVE a "<-10m->" length arrow+value - not just a bare
    # ruler bar with no vehicle at all (ADAC-brochure audit finding
    # 2026-08-06).
    truck = f'<g transform="translate(10,-14) scale(0.85)">{sym_truck("#000")}</g>'
    # Fixed 2026-08-09 (user-reported text/arrow placement): the arrow at
    # y=84 spanning x=18-82 was wider than the circle's actual interior at
    # that height (a circle narrows fast near its bottom edge), and sat
    # right against the text above it - moved up and narrowed to fit, with
    # the text nudged up to keep a clear gap.
    arrow = '''<line x1="22" y1="79" x2="78" y2="79" stroke="#000" stroke-width="3.5"/>
  <polygon points="22,79 30,73 30,85" fill="#000"/>
  <polygon points="78,79 70,73 70,85" fill="#000"/>'''
    text = f'<text x="50" y="68" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#000" text-anchor="middle">{n}</text>'
    return truck + arrow + text

def sym_snow_chain():
    # 268 Schneekettenpflicht: real sign shows a plain tyre silhouette with a
    # diamond-lattice chain-link net draped across its face (two sets of
    # parallel diagonal lines crossing at ~45/135 degrees, clipped to the
    # tyre's circle) - NOT a life-preserver-style ring of radiating spokes
    # (ADAC-brochure audit finding 2026-08-05: previous geometry read as a
    # life-ring, not a tyre with chains).
    # Redrawn 2026-08-06: added an inner hub ring plus short radial tread
    # marks around the tyre's rim so the shape unambiguously reads as a
    # TYRE (outer rim + hub + tread), not a bare undetailed ring with a
    # chain mesh laid over it (catalog-audit finding 2026-08-06).
    import math
    r = 24
    tyre = f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="#fff" stroke-width="5"/>'
    hub = f'<circle cx="50" cy="50" r="8" fill="none" stroke="#fff" stroke-width="3"/>'
    tread = ""
    for i in range(8):
        a = math.radians(i * 45)
        x0, y0 = 50 + (r - 5) * math.cos(a), 50 + (r - 5) * math.sin(a)
        x1, y1 = 50 + (r + 4) * math.cos(a), 50 + (r + 4) * math.sin(a)
        tread += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#fff" stroke-width="3"/>'
    clip = (
        f'<clipPath id="tyreClip"><circle cx="50" cy="50" r="{r}"/></clipPath>'
    )
    mesh = ""
    offsets = [-32, -20, -8, 8, 20, 32]
    for o in offsets:
        # 45deg diagonals
        mesh += f'<line x1="{10+o}" y1="90" x2="{90+o}" y2="10" stroke="#fff" stroke-width="2.5"/>'
        # 135deg diagonals
        mesh += f'<line x1="{10+o}" y1="10" x2="{90+o}" y2="90" stroke="#fff" stroke-width="2.5"/>'
    return clip + tyre + hub + tread + f'<g clip-path="url(#tyreClip)">{mesh}</g>'

def sym_house_car():
    # Verkehrsberuhigter Bereich (325.1): house + car pictogram PLUS a
    # walking pedestrian figure - the real sign's meaning is "pedestrians
    # may use the whole street, cars must go at walking pace", which needs
    # a visible pedestrian alongside the car (catalog-audit finding
    # 2026-08-06: previous version omitted any pedestrian figure entirely).
    # RE-AUDITED 2026-08-09 against the official ADAC brochure (p.10):
    # confirmed the real pictogram ALSO includes a small child playing with
    # a ball at the bottom (this specific detail - children may play in the
    # street - is part of what "verkehrsberuhigt" actually permits, and was
    # still missing after the 2026-08-06 round). Added a small child+ball
    # glyph bottom-centre, and enlarged/repositioned the pedestrian to the
    # left edge to better match the real layout (pedestrian left, car top,
    # house top-right, child+ball bottom).
    house = '''<polygon points="66,20 66,36 84,36 84,20 75,10" fill="#fff"/>'''
    car = '''<rect x="38" y="26" width="28" height="13" rx="4" fill="#fff"/><circle cx="45" cy="41" r="3.5" fill="#0058a3"/><circle cx="59" cy="41" r="3.5" fill="#0058a3"/>'''
    ped = f'<g transform="translate(8,28) scale(0.46)">{sym_pedestrian(color="#fff")}</g>'
    child = f'<g transform="translate(46,54) scale(0.3)">{sym_pedestrian(color="#fff")}</g>'
    ball = '<circle cx="66" cy="82" r="4.5" fill="#fff"/>'
    return house + car + ped + child + ball

def sym_deadend():
    return '''<line x1="50" y1="22" x2="50" y2="62" stroke="#000" stroke-width="6"/>
  <line x1="26" y1="62" x2="74" y2="62" stroke="#000" stroke-width="6"/>'''

def sym_first_aid_cross():
    # 358 Erste Hilfe: the real sign is a RED cross on a WHITE inset panel
    # within the blue square border - not a white cross drawn straight onto
    # the blue background (ADAC-brochure audit finding 2026-08-05).
    panel = '<rect x="18" y="18" width="64" height="64" rx="3" fill="#fff"/>'
    cross = '<rect x="42" y="26" width="16" height="48" fill="#c0272d"/><rect x="26" y="42" width="48" height="16" fill="#c0272d"/>'
    return panel + cross

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
    # A clearer fuel-pump silhouette: a tall pump body with a small display
    # "window" cut into it, a nozzle/hose looping down to a pump-gun head -
    # redrawn 2026-08-06 because the previous body+hose shape read as a mug
    # (catalog-audit finding on 448.1, applies equally to 365-fuel which
    # shares this helper).
    body = '<rect x="28" y="26" width="24" height="48" rx="3" fill="#fff"/>'
    window = '<rect x="33" y="33" width="14" height="10" rx="1" fill="#0058a3"/>'
    hose = '<path d="M52 46 Q66 46 66 58 L66 68" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>'
    gun = '<path d="M66 68 L74 68 Q78 68 78 64" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>'
    base = '<rect x="24" y="74" width="32" height="4" rx="1" fill="#fff"/>'
    return body + window + hose + gun + base

def sym_bed():
    # A clearer bed silhouette (side view): a low headboard, a mattress
    # slab with a pillow bump, and short legs - redrawn 2026-08-06 because
    # the previous two-rectangle shape didn't read as a bed at the small
    # scale used on 448.1 (catalog-audit finding).
    headboard = '<rect x="18" y="34" width="6" height="30" rx="2" fill="#fff"/>'
    mattress = '<rect x="24" y="52" width="58" height="12" rx="2" fill="#fff"/>'
    pillow = '<rect x="27" y="46" width="16" height="8" rx="3" fill="#fff"/>'
    legs = '<rect x="22" y="64" width="4" height="8" fill="#fff"/><rect x="76" y="64" width="4" height="8" fill="#fff"/>'
    return headboard + mattress + pillow + legs

def sym_cutlery():
    return '''<line x1="34" y1="26" x2="34" y2="74" stroke="#fff" stroke-width="4"/>
  <line x1="26" y1="26" x2="26" y2="46" stroke="#fff" stroke-width="4"/>
  <line x1="42" y1="26" x2="42" y2="46" stroke="#fff" stroke-width="4"/>
  <circle cx="66" cy="34" r="10" fill="none" stroke="#fff" stroke-width="4"/>
  <line x1="66" y1="44" x2="66" y2="74" stroke="#fff" stroke-width="4"/>'''

def sym_toilet():
    # 365-58.2 oeffentliche Toilette: the real German sign uses the literal
    # "WC" lettering, not a generic two-person silhouette (catalog-audit
    # finding 2026-08-06).
    return symC_text("WC", x=50, y=64, size=34, color="#fff")

def sym_phone():
    return '<path d="M32 28 Q28 50 40 64 Q54 78 74 72 L70 58 L58 62 Q50 56 46 46 L50 34 Z" fill="#fff"/>'

def sym_camp_tent():
    # 365-58 Campingplatz: a small tent outline PLUS a caravan (travel-
    # trailer) silhouette side by side - the previous version drew only a
    # bare tent triangle with no caravan at all (catalog-audit finding
    # 2026-08-06).
    tent = ('<polygon points="34,30 50,64 18,64" fill="none" stroke="#fff" '
            'stroke-width="4"/><line x1="34" y1="30" x2="34" y2="64" stroke="#fff" stroke-width="2.5"/>')
    caravan = f'<g transform="translate(30,18) scale(0.72)">{sym_caravan(color="#fff")}</g>'
    return tent + caravan

def sym_ev_plug():
    return '<circle cx="50" cy="50" r="20" fill="none" stroke="#fff" stroke-width="5"/><line x1="42" y1="42" x2="42" y2="50" stroke="#fff" stroke-width="4"/><line x1="58" y1="42" x2="58" y2="50" stroke="#fff" stroke-width="4"/><line x1="50" y1="58" x2="50" y2="66" stroke="#fff" stroke-width="4"/>'

def sym_wheelchair():
    return '<circle cx="46" cy="30" r="7" fill="#fff"/><path d="M46 40 L46 56 L64 56 M46 48 L60 48" stroke="#fff" stroke-width="4" fill="none"/><path d="M46 56 Q46 74 30 74 Q18 74 18 62" stroke="#fff" stroke-width="4" fill="none"/>'

def sym_uturn_ban():
    # 272 Verbot des Wendens: real pictogram is an upside-down "U" / "∩"
    # shape - a semicircular arc across the TOP with both prongs hanging
    # DOWN, one of them ending in an arrowhead-flare - not an arc across
    # the bottom with prongs pointing up (mirror-flip fix, ADAC-brochure
    # audit finding 2026-08-05: previous geometry had the loop opening
    # upward instead of downward).
    return '''<path d="M66 78 L66 46 A18 18 0 0 0 30 46 L30 68" stroke="#000" stroke-width="7" fill="none" stroke-linecap="round"/>
  <polygon points="20,60 30,78 40,60" fill="#000"/>
  <line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'''

def sym_min_speed(n="30"):
    # 275 Mindestgeschwindigkeit: real sign is just the plain number on the
    # blue circle - removed a stray underline rule that had no basis in the
    # actual sign design (catalog-audit finding 2026-08-06).
    return f'<text x="50" y="58" font-family="Arial, sans-serif" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>'

def sym_arrow_straight(color="#fff"):
    return f'<path d="M50 22 L68 44 L58 44 L58 78 L42 78 L42 44 L32 44 Z" fill="{color}"/>'

def sym_arrow_left(color="#fff"):
    return sym_arrow_right(color).replace(
        'x1="16" y1="50" x2="60" y2="50"', 'x1="84" y1="50" x2="40" y2="50"'
    ).replace('points="52,32 86,50 52,68"', 'points="48,32 14,50 48,68"')

def sym_arrow_both(color="#fff"):
    return f'<path d="M22 50 L36 38 L36 46 L64 46 L64 38 L78 50 L64 62 L64 54 L36 54 L36 62 Z" fill="{color}"/>'

def sym_arrow_straight_and_right(color="#fff"):
    # 214 Vorgeschriebene Fahrtrichtung (geradeaus und rechts): a single
    # common shaft rising from the bottom then FORKING into two clearly
    # separated arms - one continuing straight up, one branching off
    # diagonally to the right - each ending in its own distinct triangular
    # arrowhead. Redrawn 2026-08-06: the previous version's right branch
    # curved back close alongside the main shaft and closed into a loop at
    # the top, so the whole glyph read as the letter "P" rather than a
    # forked arrow (catalog-audit finding 2026-08-06).
    stem = f'<path d="M50 86 L50 66" stroke="{color}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    left_arm = f'<path d="M50 66 L50 32" stroke="{color}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    left_head = f'<polygon points="50,16 36,36 64,36" fill="{color}"/>'
    right_arm = f'<path d="M50 66 L74 46" stroke="{color}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    right_head = f'<polygon points="85,37 77,55 65,42" fill="{color}"/>'
    return stem + left_arm + left_head + right_arm + right_head

def sym_arrow_bypass_right(color="#fff"):
    # 222 Vorgeschriebene Vorbeifahrt (Hindernis nur auf angezeigter Seite
    # vorbei): real sign shows a bold, perfectly STRAIGHT diagonal arrow
    # from upper-left to lower-right - re-audited 2026-08-09 against the
    # official ADAC brochure (p.6): the real pictogram's shaft has no
    # curve/bend at all, unlike the smooth curved sweep a 2026-08-06 round
    # drew (that round correctly fixed an earlier right-angle "L" bend, but
    # over-corrected into a curve instead of landing on the real sign's
    # plain straight diagonal).
    shaft = (
        f'<line x1="24" y1="22" x2="64" y2="68" stroke="{color}" stroke-width="10" '
        f'stroke-linecap="round"/>'
    )
    head = f'<polygon points="80,76 56,80 66,60" fill="{color}"/>'
    return shaft + head

def sym_tunnel_shape():
    # 327 Tunnel: re-audited 2026-08-09 against the official ADAC brochure
    # (p.10) - the real sign shows a SOLID black tunnel-arch silhouette
    # (an arched entrance shape, brick/arch texture implied by its solid
    # fill) sitting inside a white inset panel within the blue square
    # border - not a bare white outline arch directly on the blue
    # background (a previous version's outline-only arch didn't read as a
    # solid tunnel mouth).
    panel = '<rect x="14" y="14" width="72" height="72" rx="3" fill="#fff"/>'
    arch = '<path d="M24 78 L24 48 Q24 20 50 20 Q76 20 76 48 L76 78 Z" fill="#000"/>'
    return panel + arch

def sym_breakdown_h():
    return '<text x="50" y="66" font-family="Arial, sans-serif" font-size="40" font-weight="700" fill="#fff" text-anchor="middle">H</text>'

def sym_taxi_text():
    # 229 Taxenstand: re-audited 2026-08-09 against the official ADAC
    # brochure (p.6) - the real sign is NOT just white "TAXI" text on a
    # blue square. It carries the standard red "reserved, no parking for
    # others" ring-with-cross symbol (same family as 283/286's prohibition
    # rings) above the "TAXI" text, since the sign reserves the space for
    # taxis and prohibits everyone else from stopping there - a bare "TAXI"
    # label alone (this file's previous version) omits that defining
    # pictogram entirely.
    ring = '<circle cx="50" cy="34" r="18" fill="none" stroke="#c0272d" stroke-width="5"/>'
    cross = (
        '<line x1="39" y1="23" x2="61" y2="45" stroke="#c0272d" stroke-width="5" stroke-linecap="round"/>'
        '<line x1="61" y1="23" x2="39" y2="45" stroke="#c0272d" stroke-width="5" stroke-linecap="round"/>'
    )
    text = '<text x="50" y="76" font-family="Arial, sans-serif" font-size="19" font-weight="700" fill="#fff" text-anchor="middle">TAXI</text>'
    return ring + cross + text

def sym_bike_dismount():
    return sym_bicycle().replace('fill="none" stroke="#fff"', 'fill="none" stroke="#000"') + '<line x1="18" y1="82" x2="82" y2="18" stroke="#c0272d" stroke-width="7"/>'

# ==== DN-30: extended sign-catalog batches (Gefahr/Vorschrift/Richt/Zusatz) ====

# ==== Batch A (Gefahrzeichen) icon helpers ====
def symA_curve():
    # 103 Kurve (rechts): simple curved road-band bending right. Fixed
    # 2026-08-09 (user-reported): the curve's upper-right end (82,24) sat far
    # outside the triangle's actual interior at that height (the triangle
    # narrows sharply near its apex), so the black line visibly crossed the
    # red border - end point pulled in to stay inside at every height along
    # the curve, not just checked at the start.
    return '<path d="M25 78 C25 54 38 36 58 34" stroke="#000" stroke-width="8" fill="none" stroke-linecap="round"/>'

def symA_double_curve():
    # 105 Doppelkurve: the plain (un-suffixed) Zeichen 105 is officially
    # "Doppelkurve (zunaechst rechts)" per the ADAC brochure / StVO Anlage 1
    # (the -10/"zunaechst links" and -20/"zunaechst rechts" split into two
    # separate numbers only came later) - WebSearch/ADAC-brochure-verified
    # 2026-08-06 (this project's own sign_reference.json text currently says
    # "zunaechst nach links" for this ref, which looks like a genuine
    # content-data mismatch - flagged separately, not silently changed here).
    # Drawn as a single ribbon-like road-band with two distinct bends (first
    # right, then left - a real "S"/zigzag), not one smooth uninterrupted
    # diagonal sweep (ADAC-brochure audit finding 2026-08-06).
    # Fixed 2026-08-09 (user-reported): the top end (32,20) sat well outside
    # the triangle's interior at that height (too close to the narrow apex),
    # crossing the red border - pulled the top bend inward/lower to stay
    # clear of the border at every point.
    return '<path d="M32 80 C32 64 55 64 55 50 C55 38 46 33 46 28" stroke="#000" stroke-width="9" fill="none" stroke-linecap="round"/>'

def symA_gefaelle(pct="10"):
    # 108 Gefaelle: real pictogram is a SOLID filled black wedge - flat
    # bottom edge along the sign's base, diagonal slope descending from a
    # point on the upper-left down to the bottom-right corner - not just an
    # outline (ADAC-brochure audit finding 2026-08-06: previous version only
    # drew the outline, leaving the wedge unfilled/white).
    # Widened the margin from the border 2026-08-09 (user-reported): the
    # wedge's base corners sat only ~3 units from the triangle's actual
    # inner edge at that height - pulled in a bit more for a comfortable gap.
    return f'''<polygon points="22,74 78,74 32,48" fill="#000"/>
  <text x="58" y="38" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#000" text-anchor="middle">{pct}%</text>'''

def symA_steigung(pct="10"):
    # 110 Steigung: mirror of symA_gefaelle - solid filled black wedge with
    # a flat bottom and a diagonal rising from the bottom-left corner up to
    # a point on the upper-right (same solid-fill fix as 108 - ADAC-brochure
    # audit finding 2026-08-06). Margin widened 2026-08-09, same reason/fix
    # as symA_gefaelle above.
    return f'''<polygon points="22,74 78,74 68,48" fill="#000"/>
  <text x="42" y="38" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#000" text-anchor="middle">{pct}%</text>'''

def symA_uneven():
    # 112 Unebene Fahrbahn: re-audited 2026-08-09 against the official ADAC
    # brochure (p.4) - the real pictogram is a single continuous irregular
    # mound/ridge silhouette sitting directly on the triangle's own bottom
    # edge (a filled bumpy hill shape, not a separate straight baseline
    # stroke with two detached bump-arcs floating above it - a 2026-08-06
    # round's version still read as "two arches on a shelf" rather than one
    # uneven road surface).
    return '<path d="M18 82 L18 76 Q26 60 34 76 Q40 64 46 76 Q54 58 62 76 Q70 66 76 76 L82 76 L82 82 Z" fill="#000"/>'

def symA_skid():
    # 114 Schleuder- oder Rutschgefahr: re-audited 2026-08-09 against the
    # official ADAC brochure (p.4) - the real pictogram's single most
    # defining visual cue is that the CAR ITSELF is drawn skewed/rotated
    # (as if it has spun sideways), not sitting square and level - a
    # previous version's perfectly level, unrotated car silhouette lost
    # that cue entirely and could read as a generic "slippery road" icon
    # with no car-specific skid. Car silhouette + wheels now sit inside a
    # <g transform="rotate(...)"> so the whole car is visibly canted,
    # matching the real sign, with the same two skid-mark curves trailing
    # behind it.
    car = ('<g transform="rotate(-18 46 55)">'
           '<rect x="34" y="46" width="34" height="14" rx="5" fill="#000"/>'
           '<circle cx="42" cy="62" r="4" fill="#000"/><circle cx="60" cy="62" r="4" fill="#000"/>'
           '</g>')
    skids = ('<path d="M18 74 Q40 60 62 74" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'
             '<path d="M26 82 Q48 70 70 82" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return car + skids

def symA_crosswind():
    # 117 Seitenwind: RE-AUDITED 2026-08-09 against the official ADAC
    # brochure (p.4) - the real pictogram is a single continuous tapering
    # windsock CONE (wide where it attaches to the pole, narrowing smoothly
    # to a point, with a slight downward droop from gravity/wind), not a
    # row of disconnected shrinking triangle segments (a 2026-08-06 round's
    # version, which still didn't read as a windsock once rendered - it
    # looked like a torn flag). One continuous filled silhouette for the
    # outer shape, with two thin white gap-lines layered on top for the
    # classic banded-windsock texture cue, so the outline itself (the part
    # that actually has to read as "a windsock") stays a single smooth
    # taper.
    pole = '<line x1="28" y1="18" x2="28" y2="82" stroke="#000" stroke-width="5"/>'
    cone = '<path d="M28 26 C46 22 64 28 80 46 C64 44 46 46 28 40 Z" fill="#000"/>'
    bands = (
        '<line x1="38" y1="27.3" x2="41" y2="39.8" stroke="#fff" stroke-width="2"/>'
        '<line x1="54" y1="30.3" x2="56" y2="42.3" stroke="#fff" stroke-width="2"/>'
    )
    return pole + cone + bands

def symA_narrow_one_side():
    # 121 einseitig verengte Fahrbahn (rechts): left edge unaffected, right
    # edge angles inward - bold SOLID black road-edge silhouettes to match
    # 120's style, not thin wireframe lines (WebSearch-verified 2026-08-05
    # user-reported design flaw - too basic previously).
    # Fixed 2026-08-09 (user-reported): both top ends (28,28)/(78,28) sat
    # outside the triangle's interior at that height - moved down/inward.
    return '''<line x1="36" y1="44" x2="36" y2="80" stroke="#000" stroke-width="11" stroke-linecap="round"/>
  <path d="M64 44 L64 58 L48 80" stroke="#000" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

def symA_stau():
    # 124 Stau: THREE car-rear-view silhouettes (a wide low body with a
    # narrower, rounded-top cabin/roof merged flush on top - reads as a car,
    # not a floating blob), receding into the distance with a vertical/
    # perspective offset - the official pictogram shows a 3-car queue, not 2
    # (ADAC-brochure audit finding 2026-08-06). The stray full-width baseline
    # from the previous version (not part of the real pictogram) is removed.
    return '''<rect x="16" y="64" width="32" height="12" rx="3" fill="#000"/>
  <path d="M20 64 L20 58 Q20 52 26 52 L38 52 Q44 52 44 58 L44 64 Z" fill="#000"/>
  <circle cx="24" cy="76" r="4" fill="#000"/><circle cx="40" cy="76" r="4" fill="#000"/>
  <rect x="54" y="50" width="19" height="7" rx="2" fill="#000"/>
  <path d="M57 50 L57 46 Q57 43 60 43 L68 43 Q71 43 71 46 L71 50 Z" fill="#000"/>
  <circle cx="59" cy="57" r="2.5" fill="#000"/><circle cx="68" cy="57" r="2.5" fill="#000"/>
  <rect x="70" y="32" width="10" height="4" rx="1.3" fill="#000"/>
  <path d="M72 32 L72 29 Q72 27.5 73.3 27.5 L76.7 27.5 Q78 27.5 78 29 L78 32 Z" fill="#000"/>
  <circle cx="73" cy="36.3" r="1.4" fill="#000"/><circle cx="77" cy="36.3" r="1.4" fill="#000"/>'''

def symA_oncoming():
    # 125 Gegenverkehr: official pictogram is a DOWN arrow on the left and
    # an UP arrow on the right - the previous version had this backwards
    # (ADAC-brochure audit finding 2026-08-06).
    # Fixed 2026-08-09 (user-reported): both arrow tails (30,30)/(70,30) and
    # the right arrow's barb (78,40) sat outside the triangle's interior at
    # that height - shortened both arrows and pulled the barbs inward.
    return '''<path d="M38 42 L38 78 L30 68 M38 78 L46 68" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M62 78 L62 42 L54 52 M62 42 L68 52" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

def symA_traffic_light():
    # 131 Lichtzeichenanlage: schematic traffic-light column with the 3
    # lights in their real red/yellow/green colours, not all-black
    # (ADAC-brochure audit finding 2026-08-06).
    return '''<rect x="40" y="24" width="20" height="46" rx="4" fill="none" stroke="#000" stroke-width="5"/>
  <circle cx="50" cy="34" r="5" fill="#c0272d"/>
  <circle cx="50" cy="47" r="5" fill="#f5c400"/>
  <circle cx="50" cy="60" r="5" fill="#1f9d5c"/>
  <line x1="50" y1="70" x2="50" y2="82" stroke="#000" stroke-width="5"/>'''

def symA_radverkehr():
    # 138 Radverkehr: reuse the existing sym_bicycle() pictogram, recolored
    # black (its default #fff stroke is meant for use on a blue/red fill)
    return sym_bicycle().replace('stroke="#fff"', 'stroke="#000"')

def symA_wildlife():
    # 142 Wildwechsel: redrawn a FOURTH time 2026-08-09 (user-reported: "the
    # animal looks weird," independently confirmed - the 3rd attempt's legs
    # were straight lines splayed outward at odd angles, more spider-like
    # than deer-like, and the antlers read as a disconnected zigzag floating
    # above the head with no clear attachment). This version: a thicker
    # neck stroke (13, up from 11) that visibly overlaps both the body and
    # head ellipses so there's no visible seam/gap at the joins, a small
    # simplified two-prong antler tucked close against the head rather than
    # a tall zigzag, and legs bent at a "knee" (front legs bending forward,
    # back legs bending back) instead of straight diagonals, since a real
    # leaping animal's legs are never poker-straight.
    # 5th attempt, same session: switched the neck from a thin stroke (read
    # as giraffe-like/too long) to a filled tapering wedge merged directly
    # with the body via one path, antlers splayed outward in a V (a
    # straight-up pair read as bug antennae, not antlers), and straight
    # (not bent) legs at a running angle, since the bent-knee version's
    # extra joints read as broken/disjointed rather than animal-like.
    body = '<ellipse cx="38" cy="58" rx="20" ry="8" fill="#000"/>'
    neck = '<path d="M50 56 Q58 44 66 34 Q69 30 74 30 L74 37 Q67 43 58 55 Q54 59 48 59 Z" fill="#000"/>'
    head = '<ellipse cx="76" cy="28" rx="6" ry="5" fill="#000"/>'
    snout = '<polygon points="81,27 90,29 81,31" fill="#000"/>'
    antlers = (
        '<path d="M72 24 L65 16 M80 24 L87 17" '
        'stroke="#000" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
    )
    tail = '<path d="M18 53 L10 49" stroke="#000" stroke-width="5" stroke-linecap="round"/>'
    front_legs = (
        '<path d="M52 64 L60 78" stroke="#000" stroke-width="6" stroke-linecap="round"/>'
        '<path d="M60 63 L70 78" stroke="#000" stroke-width="6" stroke-linecap="round"/>'
    )
    back_legs = (
        '<path d="M24 64 L16 78" stroke="#000" stroke-width="6" stroke-linecap="round"/>'
        '<path d="M32 64 L26 79" stroke="#000" stroke-width="6" stroke-linecap="round"/>'
    )
    return body + neck + head + snout + antlers + tail + front_legs + back_legs

def symA_ped_crossing_warn():
    # 101-21: warning-triangle version of the pedestrian-crossing pictogram
    # (a walking figure - mid-stride, one leg forward one back, arms
    # swinging - over a set of angled zebra-stripe bars in perspective, not
    # a static blob over blocky squares), all black - distinct from Zeichen
    # 293/350 (blue square, white pictogram) which mark the crossing itself
    # rather than warn of one ahead (ADAC-brochure audit finding 2026-08-06).
    return '''<circle cx="50" cy="32" r="6.5" fill="#000"/>
  <rect x="44" y="40" width="12" height="18" rx="5" fill="#000"/>
  <path d="M46 44 L34 52 M54 44 L64 38" stroke="#000" stroke-width="5" stroke-linecap="round"/>
  <path d="M46 58 L36 76 M54 58 L62 72" stroke="#000" stroke-width="5.5" stroke-linecap="round"/>
  <path d="M20 88 L28 74 L38 74 L30 88 Z" fill="#000"/>
  <path d="M38 88 L46 74 L56 74 L48 88 Z" fill="#000"/>
  <path d="M56 88 L64 74 L74 74 L66 88 Z" fill="#000"/>'''

def symA_falling_rocks():
    # 101-25 Steinschlag: real pictogram has the cliff/rock-face on the
    # RIGHT with fragments falling to the LEFT (the previous version had
    # this mirrored) - the cliff face is a jagged, irregular rock silhouette
    # rather than a plain rectangle (ADAC-brochure audit finding 2026-08-06).
    return '''<path d="M82 82 L82 48 L75 42 L71 32 L64 36 L60 27 L53 34 L57 43 L49 47 L53 56 L46 60 L49 82 Z" fill="#000"/>
  <path d="M28 40 L38 52 L30 60 L22 52 Z" fill="#000"/>
  <path d="M22 64 L28 72 L22 78 L16 70 Z" fill="#000"/>'''

def symA_bake3_body():
    # 156 Bahnuebergang mit Bake, 3-streifig: a distinct StVO sign family
    # (Bake, Anlage 1) - a narrow white post with three red diagonal
    # stripes, placed ~240m before an unguarded railway crossing (2-stripe/
    # 1-stripe Baken follow closer to the crossing). RE-AUDITED 2026-08-09
    # against the official ADAC brochure (p.4): the real 156 also carries a
    # SMALL triangular warning-sign icon (the same train pictogram as 151)
    # mounted on top of the striped post - a previous version drew only the
    # bare striped post with no triangle at all, missing that defining
    # element (159/162, the closer 2-stripe/1-stripe Baken, correctly have
    # no triangle - only 156, the first one in the sequence, carries it).
    triangle = (
        '<polygon points="50,2 67,29 33,29" fill="#fff" stroke="#c0272d" '
        'stroke-width="4" stroke-linejoin="round"/>'
        # sym_train()'s own bbox is roughly x14-78 (center 46), y28-85
        # (center 56.5) - scaled by 0.26 and translated so that center
        # lands in the middle of the small triangle above (center 50,15.5).
        # An earlier attempt's translate math put this entirely off-canvas
        # above the triangle (negative y) - caught by re-rendering and
        # actually looking, not just trusting the transform arithmetic.
        f'<g transform="translate(38,1) scale(0.26)">{sym_train()}</g>'
    )
    post = '''
  <rect x="34" y="33" width="32" height="63" fill="#fff" stroke="#000" stroke-width="2"/>
  <path d="M34 47 L66 35" stroke="#c0272d" stroke-width="7"/>
  <path d="M34 67 L66 55" stroke="#c0272d" stroke-width="7"/>
  <path d="M34 87 L66 75" stroke="#c0272d" stroke-width="7"/>
'''
    return triangle + post

# ---- registry: ref -> svg body --------------------------------------------

# ==== Batch B (Vorschriftzeichen) icon helpers ====
def symB_bicycle_black():
    # black-stroke variant of sym_bicycle, for use inside circle_prohibition
    return sym_bicycle().replace('stroke="#fff"', 'stroke="#000"')

def symB_priority_arrows():
    # Zeichen 308 Vorrang vor dem Gegenverkehr: RE-AUDITED 2026-08-09
    # against the official ADAC brochure (p.6) - the real sign shows a RED
    # arrow pointing DOWN on the LEFT (oncoming traffic, which must yield)
    # and a WHITE arrow pointing UP on the RIGHT (your own, priority
    # direction), both roughly the same bold weight. A 2026-08-06 round's
    # "fix" got both the colour (used near-black "#1a1a1a" instead of white
    # for the own-direction arrow, which reads wrong against this sign's
    # blue background) and the left/right position backwards.
    return '''
  <path d="M32 24 L32 76 L20 62 M32 76 L44 62" stroke="#c0272d" stroke-width="8"
        fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M68 76 L68 24 L56 38 M68 24 L80 38" stroke="#fff" stroke-width="8"
        fill="none" stroke-linecap="round" stroke-linejoin="round"/>
'''

def symC_bus_lane():
    # 245 Bussonderfahrstreifen: a bus pictogram PLUS a dedicated-lane
    # direction arrow underneath, so it reads as "bus lane" rather than
    # just "bus stop" - distinguishes it from 224's bus-alone pictogram
    # (catalog-audit finding 2026-08-06: 224 and 245 previously shared the
    # exact same artwork).
    bus = f'<g transform="translate(6,-12) scale(0.7)">{sym_bus(color="#fff")}</g>'
    lane = ('<path d="M50 62 L50 90" stroke="#fff" stroke-width="6" fill="none" '
            'stroke-linecap="round"/>'
            '<polygon points="50,50 40,66 60,66" fill="#fff"/>')
    return bus + lane

def symB_bike_ped_split():
    # Zeichen 241 getrennter Rad- und Gehweg: RE-AUDITED 2026-08-09 against
    # the official ADAC brochure (p.6) - bicycle pictogram on the LEFT,
    # adult+child pedestrian pair on the RIGHT, divided by a VERTICAL line.
    # A 2026-08-05 round correctly identified that 241 needs a vertical
    # divider (as opposed to 240's horizontal one, see sym_ped_bike_stack)
    # but put a single pedestrian on the left / bicycle on the right - both
    # backwards versus the real sign, and using the wrong pedestrian
    # pictogram (single figure, not adult+child - same family-wide mistake
    # as 239/240/242.x, see sym_ped_child()).
    bike = f'<g transform="translate(-8,4) scale(0.5)">{sym_bicycle(color="#fff")}</g>'
    divider = '<line x1="50" y1="14" x2="50" y2="90" stroke="#fff" stroke-width="3"/>'
    ped = f'<g transform="translate(46,-4) scale(0.46)">{sym_ped_child(color="#fff")}</g>'
    return bike + divider + ped

def symB_min_distance(n="70m"):
    # Zeichen 273 Mindestabstand: two boxier truck (cab+trailer) silhouettes
    # with a central gap between them and the minimum-distance text ABOVE
    # the vehicles - original simplified pictogram, not a literal truck
    # drawing (catalog-audit DN-46 legibility polish, 2026-08-06).
    return f'''
  <text x="50" y="24" font-family="Arial, sans-serif" font-size="18" font-weight="700"
        fill="#000" text-anchor="middle">{n}</text>
  <rect x="8" y="42" width="20" height="16" rx="1" fill="#000"/>
  <rect x="28" y="46" width="8" height="12" rx="1" fill="#000"/>
  <circle cx="14" cy="60" r="3" fill="#000"/><circle cx="30" cy="60" r="3" fill="#000"/>
  <rect x="64" y="46" width="8" height="12" rx="1" fill="#000"/>
  <rect x="72" y="42" width="20" height="16" rx="1" fill="#000"/>
  <circle cx="70" cy="60" r="3" fill="#000"/><circle cx="86" cy="60" r="3" fill="#000"/>
  <line x1="36" y1="50" x2="64" y2="50" stroke="#000" stroke-width="3" stroke-dasharray="5,4"/>
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
    # 316 Parken und Reisen (Park & Ride): rendered as the literal "P+R"
    # lettering used on real Park&Ride signage, so it reads unambiguously
    # as a park-and-ride sign - the previous P+train-car composite's train
    # icon overpowered the small P and effectively read as train-only
    # (catalog-audit finding 2026-08-06).
    return symC_text("P+R", x=50, y=64, size=30, color="#fff")

def symC_hiker_park():
    # 317 Wandererparkplatz: P plus a hiking-figure pictogram (head, torso,
    # backpack, walking stick, striding legs) - the real sign shows a
    # hiker, not a pine tree (catalog-audit finding 2026-08-06: previous
    # version drew two stacked triangles for a tree). Re-audited 2026-08-09
    # against the official ADAC brochure (p.10): the real pictogram shows
    # TWO hikers side by side, not one - added a second, smaller figure
    # just behind/right of the first.
    p = sym_P(x=24, y=64, size=30)
    hiker = '''
  <circle cx="60" cy="26" r="6" fill="#fff"/>
  <rect x="55" y="33" width="11" height="18" rx="4" fill="#fff"/>
  <rect x="52" y="36" width="8" height="12" rx="2" fill="#fff"/>
  <path d="M55 37 L44 60" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M57 51 L51 70 M64 51 L70 68" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
'''
    hiker2 = '''
  <circle cx="78" cy="32" r="5" fill="#fff"/>
  <rect x="74" y="38" width="9" height="15" rx="3.5" fill="#fff"/>
  <path d="M74 41 L66 58" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
  <path d="M76 53 L71 70 M81 53 L86 68" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
'''
    return p + hiker2 + hiker

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
    # 354 Wasserschutzgebiet: real sign shows a tanker-truck pictogram plus
    # the literal printed label "Wasser-Schutzgebiet" underneath (as text,
    # matching this project's existing icon+text-label convention used for
    # 242.x/244.x's "ZONE"/"Fahrradstrasse" and 356's "Verkehrshelfer"
    # labels) - it does NOT show wavy water lines at all (ADAC-brochure
    # audit finding 2026-08-05). Truck nudged up slightly to leave room for
    # the two-line label below it.
    truck = '''<rect x="22" y="24" width="40" height="18" rx="3" fill="#fff"/>
  <rect x="62" y="28" width="14" height="14" rx="2" fill="#fff"/>
  <ellipse cx="42" cy="33" rx="16" ry="6" fill="#0058a3"/>
  <circle cx="34" cy="46" r="5" fill="#fff"/><circle cx="58" cy="46" r="5" fill="#fff"/><circle cx="70" cy="46" r="4" fill="#fff"/>'''
    label = symC_text("Wasser-", x=50, y=66, size=13, color="#fff") + \
        symC_text("Schutzgebiet", x=50, y=80, size=13, color="#fff")
    return truck + label

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
    # text below the circle. The "Ende" variants do NOT keep the circle
    # blue with a hatch band across the whole plate - instead the entire
    # inset circle (and its pictogram/text) turns GREY, with a single
    # clean solid diagonal line crossing just the circle (ADAC-brochure
    # audit finding 2026-08-05: previous "Ende" version kept the circle
    # blue and added a dashed hatch band across the full plate instead).
    # NOTE: circle and symbol/text use distinct grey shades (not the same
    # #8a8a8a for both) so the pictogram stays visible against the grey
    # circle instead of disappearing into it.
    circle_color = "#b0b0b0" if ended else "#0058a3"
    text_color = "#5a5a5a" if ended else "#000"
    circle = f'<circle cx="50" cy="36" r="26" fill="{circle_color}"/>{symbol}'
    text = "".join(
        f'<text x="50" y="{72 + i * 13}" font-family="Arial, sans-serif" '
        f'font-size="11" font-weight="700" fill="{text_color}" text-anchor="middle">{line}</text>'
        for i, line in enumerate(label_lines)
    )
    hatch = ""
    if ended:
        # single solid diagonal line crossing only the circle's bounding
        # area (circle center 50,36 r=26 -> bbox roughly x24-76, y10-62)
        hatch = '<line x1="24" y1="62" x2="76" y2="10" stroke="#5a5a5a" stroke-width="5"/>'
    return rect_white_black_border(circle + text + hatch)

def _zone_stop_ring(ended=False):
    # 290.1/290.2 (Beginn/Ende Zone eingeschraenktes Haltverbot): the
    # inset circle drawn by sign_zone_plate() needs the same red-ring
    # "eingeschraenktes Haltverbot" cue as Zeichen 286 (a red ring around
    # the disc, plus a single diagonal bar) layered on top of it - grey
    # instead of red for the "ended" variant, whose grey diagonal is
    # already supplied by sign_zone_plate(ended=True)'s own hatch line.
    color = "#5a5a5a" if ended else "#c0272d"
    ring = f'<circle cx="50" cy="36" r="26" fill="none" stroke="{color}" stroke-width="5"/>'
    if ended:
        return ring
    return ring + f'<line x1="34" y1="20" x2="66" y2="52" stroke="{color}" stroke-width="5"/>'

def symC_guard():
    # 356 Verkehrshelfer: figure holding a stop-paddle, plus the printed
    # "Verkehrshelfer" label underneath - the real sign always carries this
    # text label (matching the icon+text-label convention used for
    # 242.x/244.x and 354); the previous version rendered the icon alone
    # with no label at all (ADAC-brochure audit finding 2026-08-05). Figure
    # scaled/shifted up slightly to leave room for the two-line label.
    figure = '''
  <circle cx="42" cy="24" r="6" fill="#fff"/>
  <rect x="36" y="30" width="12" height="20" rx="4" fill="#fff"/>
  <line x1="48" y1="35" x2="66" y2="25" stroke="#fff" stroke-width="3.5"/>
  <rect x="63" y="17" width="14" height="14" fill="#fff"/>
  <line x1="39" y1="50" x2="32" y2="66" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="45" y1="50" x2="50" y2="66" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
'''
    label = symC_text("Verkehrs-", x=50, y=78, size=12, color="#fff") + \
        symC_text("helfer", x=50, y=90, size=12, color="#fff")
    return figure + label

def symC_police_panel():
    # 363 Polizei: the real sign has "Polizei" sitting inside a distinct
    # white inset rectangular panel within the blue square border, not white
    # text directly on the blue background - the panel needs black text
    # since it now sits on white (ADAC-brochure audit finding 2026-08-05).
    panel = '<rect x="14" y="36" width="72" height="28" rx="4" fill="#fff"/>'
    text = symC_text("Polizei", x=50, y=56, size=17, color="#000")
    return panel + text

def symC_autohof():
    # 448.1 Autohof: RE-AUDITED 2026-08-09 against the official ADAC
    # brochure (p.16) - this is a NAVIGATION sign (same "Wegweiser zur
    # Ausfahrt" family as 448 itself, just labelled "Autohof" instead of a
    # destination name), not an amenity-icon sign. The real pictogram is
    # the word "Autohof" plus a small motorway-junction arrow (main road
    # continuing, with a branch peeling off toward the exit) and a small
    # exit-number badge - fuel-pump/bed icons (a 2026-08-06 round's version)
    # belong to the completely separate 365-fuel/365-rest service-facility
    # signs, which this project already has correctly elsewhere and
    # shouldn't have been duplicated here.
    label = symC_text("Autohof", x=50, y=24, size=15, color="#fff")
    junction = (
        '<path d="M30 34 L30 66" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>'
        '<path d="M30 50 L52 66" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>'
        '<polygon points="58,70 44,68 50,58" fill="#fff"/>'
    )
    badge = (
        '<circle cx="72" cy="46" r="13" fill="#fff"/>'
        '<text x="72" y="51" font-family="Arial, sans-serif" font-size="14" font-weight="700" '
        'fill="#0058a3" text-anchor="middle">27</text>'
    )
    return label + junction + badge

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

def _fit_font_size(text, max_width, base_size):
    # Crude but effective text-fit estimate: bold Arial glyphs average
    # roughly 0.62x their font-size in rendered width. If the text at
    # base_size would run wider than max_width, shrink the font-size (down
    # to a legibility floor) so the string never overruns the sign's
    # boundary - used by 310/311/401/437/453 below (catalog-audit finding
    # 2026-08-06: those signs previously used a single fixed font-size with
    # no regard for the plate's width, so longer place/street names ran
    # past the sign's edges).
    if not text:
        return base_size
    avg_char_w = 0.62
    fitted = max_width / (len(text) * avg_char_w)
    return max(5, min(base_size, fitted))

def symC_text_fit(t, x=50, y=60, max_width=76, base_size=20, color="#000", weight="700"):
    size = _fit_font_size(t, max_width, base_size)
    return symC_text(t, x=x, y=y, size=size, color=color, weight=weight)

def symC_town_name(name="MUSTERSTADT", color="#000"):
    # 310 Ortstafel: font-size now scales down for longer names (via
    # symC_text_fit) so e.g. "Bad Muenstereifel-Nord" stays inside the
    # yellow plate instead of overflowing past its edges (catalog-audit
    # finding 2026-08-06).
    return symC_text_fit(name, max_width=78, base_size=15, color=color)

def symC_town_name_leaving(name="MUSTERSTADT"):
    # 311 Ortstafel Rueckseite: same plate as 310, with a diagonal red
    # line through the town name to indicate you're leaving (project's
    # diagonal-line "end/leaving" convention, red here per the real sign).
    return symC_town_name(name) + '<line x1="18" y1="78" x2="82" y2="42" stroke="#c0272d" stroke-width="5"/>'

def symC_route_number(t="1", color="#000", size=28):
    # NOTE: kept as a plain (non-fitted) text call, unchanged from before -
    # this helper is shared with 410/415 (not part of this fix), and route
    # numbers/plain destination words here are already short enough not to
    # overflow. 401's fix (removing the extraneous "B" prefix so only the
    # bare number is drawn) is applied at the SIGNS registry call site
    # below, not in this helper.
    return symC_text(t, size=size, color=color)

def symC_autobahn_wegweiser():
    # 430 Wegweiser zur Autobahn: a stylized motorway-overpass pictogram
    # (reusing the same arch/overpass shape as sym_motorway_start(), which
    # is the correct Autobahn-junction motif already used elsewhere in this
    # file for 330-1) plus the "Autobahn" label and a directional arrowhead
    # - not a plain route-number shield (catalog-audit finding 2026-08-06:
    # previous version showed "A 1" route-number text in a pointed
    # destination-plate shape, the wrong content type entirely for a real
    # Zeichen 430).
    bridge = f'<g transform="translate(0,-14) scale(0.68)">{sym_motorway_start()}</g>'
    label = symC_text("Autobahn", x=48, y=78, size=11, color="#fff")
    arrow = '<polygon points="88,50 74,42 74,58" fill="#fff"/>'
    return bridge + label + arrow

def rect_blue_white_border(symbol="", w=88, h=76):
    # 453 Entfernungstafel: real Autobahn distance-table signs use the same
    # blue/white informational colour scheme as other overhead Autobahn
    # signage (distinct from the plain white/black-border plate previously
    # used here, which read as an ordinary Richtzeichen plate rather than
    # an Autobahn distance table - catalog-audit finding 2026-08-06).
    x = (100 - w) / 2
    y = (100 - h) / 2
    return f'''
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#0058a3" stroke="#fff" stroke-width="4"/>
  {symbol}
'''

def symC_distance_table(lines=("Musterstadt 12", "Beispieldorf 27", "Musterhausen 45")):
    # 453 Entfernungstafel: 2-3 lines of placeholder town/distance text.
    # Each line is now run through symC_text_fit so longer town names
    # shrink to stay inside the plate's width instead of overrunning its
    # edges (catalog-audit finding 2026-08-06), and text/background now
    # use the blue-plate colour scheme (see rect_blue_white_border above).
    ys = (32, 54, 76)
    body = ""
    for line, y in zip(lines, ys):
        body += symC_text_fit(line, y=y, max_width=78, base_size=14, color="#fff")
    return body

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
    # Fixed 2026-08-09 (user-reported): the vertical stem ran to y=85, well
    # past the plate's own bottom border (the plate's visible interior only
    # goes to about y=68) - rescaled the whole pictogram to fit inside.
    return '''
  <path d="M10 42 L55 42 L55 62" stroke="#000" stroke-width="8" fill="none" stroke-linejoin="round"/>
  <line x1="20" y1="58" x2="85" y2="58" stroke="#000" stroke-width="3"/>
'''

def symD_caravan_skid():
    # Zeichen 1006 Schleudergefahr fuer Wohnwagengespanne: a "Gespann" is
    # specifically the CAR+trailer combination, so this needs a small car
    # silhouette actually towing the caravan (catalog-audit finding
    # 2026-08-06: a bare caravan on its own, with no towing vehicle, doesn't
    # read as a "Gespann"/combination at all) plus wavy skid-mark lines
    # trailing the wheels to show the fishtail/swerve risk this plate warns
    # about.
    car = '''<path d="M4 64 L8 52 Q11 46 18 46 L28 46 Q32 38 40 38 L44 46 L48 46 Q52 46 52 52 L52 64 Z" fill="#000"/>
  <circle cx="14" cy="68" r="5" fill="#000"/><circle cx="42" cy="68" r="5" fill="#000"/>'''
    hitch = '<line x1="52" y1="58" x2="58" y2="58" stroke="#000" stroke-width="3"/>'
    caravan = '''<rect x="58" y="40" width="34" height="26" rx="3" fill="#000"/>
  <circle cx="68" cy="68" r="5" fill="#000"/><circle cx="84" cy="68" r="5" fill="#000"/>'''
    skid = '''<path d="M56 80 Q64 74 72 80 T88 80" stroke="#000" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M6 82 Q14 76 22 82 T38 82" stroke="#000" stroke-width="2.5" fill="none" stroke-linecap="round"/>'''
    return car + hitch + caravan + skid

def symD_bicycle_black_v2():
    return '''<circle cx="36" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <circle cx="64" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <path d="M36 64 L50 40 L64 64 M50 40 L44 64 M50 48 L60 48" stroke="#000" stroke-width="4" fill="none" stroke-linejoin="round"/>'''

def symD_bike_end():
    # Zeichen 1012-31: re-audited 2026-08-09 against the official ADAC
    # brochure (p.20) - the real plate is simply the plain word "Ende" (a
    # generic "end of the previous restriction/dedication" qualifier, not
    # specifically about bicycles/Radweg) - no bicycle icon or diagonal
    # line at all. A previous round's crossed-bicycle icon was the wrong
    # content for this specific ref.
    return symD_text("Ende", size=22)

def symD_bike_dismount_walk():
    # Zeichen 1012-32 Radfahrer absteigen: re-audited 2026-08-09 against
    # the official ADAC brochure (p.20) - the real plate is plain two-line
    # text "Radfahrer" / "absteigen", not a bicycle+walking-figure icon
    # pair (a previous round's icon-based version was the wrong content
    # type for this ref - matches this file's own already-correct text-only
    # treatment of sibling plates like 1012-34 "Gruene Welle bei ... km/h").
    return symD_text_lines(["Radfahrer", "absteigen"], size=15, start_y=46, dy=17)

def symD_wheelchair_black():
    # Zeichen 1020-11 Parkverbot gilt nicht fuer Schwerbehinderte: the
    # standard, universally-recognised accessibility pictogram - a compact
    # seated figure (head + torso + forward arm) resting against a large
    # wheel, with a small front caster. RE-AUDITED 2026-08-09 against the
    # official ADAC brochure (p.20): the real plate is NOT the icon alone -
    # it's a SMALL icon in the upper-left corner plus the qualifying text
    # "mit Parkausweis ... frei" filling most of the plate, since the icon
    # by itself would read as generic disabled-parking signage rather than
    # this specific "exempted if you hold the permit" qualifier (a
    # 2026-08-06 round's icon-only version, oversized and centered, omitted
    # that essential text entirely).
    # icon bbox in its own native coordinates is roughly x31-69,y32-69
    # (center ~50,50) - scaled by 0.55 and translated so it lands fully
    # inside the plate's left third (an earlier attempt's translate math
    # pushed it up above the plate's top edge - caught by re-rendering and
    # looking, not just trusting the transform arithmetic).
    icon = f'<g transform="translate(-5,15) scale(0.55)">' + (
        '<circle cx="36" cy="37" r="5" fill="#000"/>'
        '<path d="M36 42 L37 50" stroke="#000" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M37 50 L54 50" stroke="#000" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M37 45 L49 55" stroke="#000" stroke-width="4" stroke-linecap="round"/>'
        '<circle cx="51" cy="58" r="11" fill="none" stroke="#000" stroke-width="4"/>'
        '<circle cx="51" cy="58" r="2" fill="#000"/>'
        '<circle cx="66" cy="64" r="3" fill="#000"/>'
        '<path d="M54 50 L66 64" stroke="#000" stroke-width="3" stroke-linecap="round"/>'
    ) + '</g>'
    # Fixed 2026-08-09 (user-reported text placement): the two lines sat
    # unevenly in the plate's vertical space ("mit Parkausweis" too close to
    # the icon's own midline, "frei" too close to the bottom border) -
    # rebalanced with more even spacing top and bottom.
    text = (
        symC_text_fit("mit Parkausweis", x=64, y=40, max_width=56, base_size=11) +
        '<text x="64" y="60" font-family="Arial, sans-serif" font-size="13" font-weight="700" '
        'fill="#000" text-anchor="middle">frei</text>'
    )
    return icon + text

def symD_shoulder_crossed():
    # Zeichen 1013-50 Seitenstreifen nicht befahrbar: a solid carriageway
    # line PLUS a separate, clearly-labelled hard-shoulder strip (thin
    # dashed line, offset below/beside the carriageway - matching real
    # road-marking convention for a shoulder lane), with a RED cross placed
    # specifically over that shoulder strip - a prohibitive red X (not a
    # neutral grey diagonal) since this plate means "do NOT use the
    # shoulder", the opposite of a permissive "shoulder may be used" sign
    # (catalog-audit finding 2026-08-06: an earlier version used a single
    # ambiguous grey diagonal crossing both lines at once, which read like
    # this project's neutral "end of ..." convention rather than an actual
    # prohibition, and didn't clearly identify which line was the
    # shoulder).
    road = '<line x1="10" y1="40" x2="90" y2="40" stroke="#000" stroke-width="7"/>'
    shoulder = '<line x1="10" y1="64" x2="90" y2="64" stroke="#000" stroke-width="4" stroke-dasharray="10,6"/>'
    red_x = ('<line x1="26" y1="80" x2="74" y2="50" stroke="#c0272d" stroke-width="7" stroke-linecap="round"/>'
             '<line x1="26" y1="50" x2="74" y2="80" stroke="#c0272d" stroke-width="7" stroke-linecap="round"/>')
    return road + shoulder + red_x

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
    "209": circle_mandatory(sym_arrow_bend_junction()),
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
    "301": priority_diamond_plain(),
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
    "211": circle_mandatory(sym_arrow_right_bold()),
    "214": circle_mandatory(sym_arrow_straight_and_right()),
    "222": circle_mandatory(sym_arrow_bypass_right()),
    "238": circle_mandatory(sym_horse_rider(color="#fff")),
    "239": circle_mandatory(sym_ped_child(color="#fff")),
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
    # 224 (bus/tram stop - bus pictogram alone) and 245 (dedicated bus lane
    # - bus pictogram PLUS a lane/direction arrow) previously called the
    # exact same sym_bus(color="#fff") and were byte-identical despite
    # being different signs (catalog-audit finding 2026-08-06) - see
    # symC_bus_lane() below for 245's differentiated artwork.
    "224": circle_haltestelle(),
    "229": square_blue(sym_taxi_text()),
    "241": square_blue(symB_bike_ped_split()),
    "242.1": sign_zone_plate(_inset(sym_ped_child(color="#fff"), s=0.42), ["ZONE"]),
    "242.2": sign_zone_plate(_inset(sym_ped_child(color="#5a5a5a"), s=0.42), ["ZONE"], ended=True),
    "244.1": sign_zone_plate(_inset(sym_bicycle()), ["Fahrradstrasse"]),
    "244.2": sign_zone_plate(_inset(sym_bicycle(color="#5a5a5a")), ["Fahrradstrasse"], ended=True),
    "245": square_blue(symC_bus_lane()),
    # 290.1/290.2 Beginn/Ende Zone eingeschraenktes Haltverbot: real signs
    # are a "Zone" plate (white rectangle, black border, inset circle,
    # "ZONE" text below), NOT a bare circle identical to 286
    # (ADAC-brochure audit finding 2026-08-06: previous version reused
    # circle_stopping_ban() directly, with no plate/text at all).
    "290.1": sign_zone_plate(_zone_stop_ring(False), ["ZONE"]),
    "290.2": sign_zone_plate(_zone_stop_ring(True), ["ZONE"], ended=True),
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
    "363": square_blue(symC_police_panel()),
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
    # 401 Nummer einer Bundesstrasse: real shield shows ONLY the plain
    # number (e.g. just "1"), not a literal "B" glyph baked into the icon -
    # the category/context already conveys it's a Bundesstrasse
    # (catalog-audit finding 2026-08-06: previous call passed "B 1").
    "401": rect_yellow_black_border(symC_route_number("1")),
    "410": rect_green_white_border(symC_route_number("E 40", color="#fff")),
    "415": sign_arrow_yellow(symC_route_number("Musterdorf", size=15)),
    # 430 Wegweiser zur Autobahn: a rectangular blue/white sign with a
    # stylized motorway-overpass pictogram, "Autobahn" label and a
    # directional arrow - the previous version reused the pointed
    # route-number-shield shape/content (sign_arrow_blue + "A 1" text),
    # which is actually 415/440-style destination signage, not a real
    # Zeichen 430 (catalog-audit finding 2026-08-06).
    "430": rect_blue_white_border(symC_autobahn_wegweiser(), h=68),
    "437": rect_white_black_border(symC_text_fit("Musterstrasse", max_width=78, base_size=14)),
    "453": rect_blue_white_border(symC_distance_table(), h=76),
}

BATCH_D_SIGNS = {
    "1000": zusatzzeichen(sym_arrow_right(color="#000")),
    # 1001-30 "Auf ... m": re-audited 2026-08-09 against the official ADAC
    # brochure (p.20) - the real plate flanks the distance text with a
    # small up-arrow on each side ("^800 m^"), which a previous version's
    # bare text omitted.
    "1001": zusatzzeichen(
        symD_text("300 m", size=19)
        + '<polygon points="10,60 15,49 20,60" fill="#000"/>'
        + '<polygon points="80,60 85,49 90,60" fill="#000"/>'
    ),
    "1002": zusatzzeichen(symD_priority_route()),
    "1006": zusatzzeichen(symD_caravan_skid()),
    # 1010-51 real meaning (WebSearch/ADAC-brochure-verified 2026-08-09,
    # p.20): "Kraftfahrzeuge mit einem zulaessigen Gesamtgewicht ueber
    # 3,5t... ausgenommen Personenkraftwagen und Kraftomnibusse" - a
    # weight-based vehicle-type qualifier. The real plate shows a bare
    # TRUCK icon with no text at all (confirmed directly in the brochure's
    # own pictogram) - a prior round's "Radfahrer frei" text was simply the
    # wrong content for this ref (that meaning belongs to 1022-10, which
    # already correctly shows a bicycle icon elsewhere in this registry).
    "1010-51": zusatzzeichen(_inset(sym_truck(color="#000"), cx=50, cy=52, s=0.68)),
    # Fixed 2026-08-09: plain symD_text() with a fixed font-size ran the
    # text past both edges of the plate once actually rendered (caught by
    # rendering and looking, not just reading the code) - switched to
    # symC_text_fit() like its sibling 1020-30 (identical wording) already
    # correctly does.
    "1010-60": zusatzzeichen(symC_text_fit("Anlieger frei", max_width=80, base_size=17)),
    # 1010-53 "gilt auch fuer Fussgaenger": a walking-pedestrian pictogram -
    # the previous version showed the literal text "Mofa frei" (a completely
    # different, unrelated plate's wording) instead of any pedestrian icon
    # (catalog-audit finding 2026-08-06).
    "1010-53": zusatzzeichen(_inset(sym_pedestrian(color="#000"), cx=50, cy=50, s=0.62)),
    "1012-31": zusatzzeichen(symD_bike_end()),
    "1012-32": zusatzzeichen(symD_bike_dismount_walk()),
    "1020-11": zusatzzeichen(symD_wheelchair_black()),
    # 1020-30 Anlieger frei: the previous version showed unrelated
    # "mit Parkausweis / Nr. ... frei" wording instead of the actual
    # "Anlieger frei" text this plate carries (catalog-audit finding
    # 2026-08-06) - text matches the 1010-60 rendering of the same wording.
    "1020-30": zusatzzeichen(symC_text_fit("Anlieger frei", max_width=80, base_size=17)),
    "1013-50": zusatzzeichen(symD_shoulder_crossed()),
    # 1020-32 Bewohnerparkausweis mit angegebener Nummer: placeholder
    # "Nr. ..." wording, distinct from the generic disabled/Anlieger plates
    # above (catalog-audit finding 2026-08-06: this ref existed only as a
    # hand-added file in app/assets/signs/, with no registry entry here, so
    # it was silently at risk of being lost/overwritten by this generator).
    "1020-32": zusatzzeichen(
        symC_text_fit("Nur mit Parkausweis", x=50, y=46, max_width=82, base_size=13)
        + symC_text_fit("Nr. ...", x=50, y=64, max_width=82, base_size=15)
    ),
    # 1022-10 "Radfahrer frei": reuses the shared sym_bicycle() pictogram
    # (same helper used by 237/138/254) rather than inventing a new bike
    # glyph, since this plate just exempts cyclists from the main sign's
    # prohibition (catalog-audit finding 2026-08-06: same missing-from-
    # registry file-hygiene issue as 1020-32 above). Re-audited 2026-08-09
    # against the official ADAC brochure (p.20): the real plate pairs the
    # bicycle icon with "frei" text underneath it - icon alone (this file's
    # previous version) was missing that text.
    # Fixed 2026-08-09 (user-reported text placement): "frei" sat right at
    # the plate's bottom border, crowding the bicycle icon above it - icon
    # nudged up, text nudged up off the border for a clear gap between them.
    "1022-10": zusatzzeichen(
        _inset(sym_bicycle(color="#000"), cx=50, cy=39, s=0.5)
        + '<text x="50" y="63" font-family="Arial, sans-serif" font-size="15" font-weight="700" '
          'fill="#000" text-anchor="middle">frei</text>'
    ),
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
