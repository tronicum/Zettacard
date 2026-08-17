#!/usr/bin/env python3
"""
Original top-down "who has right of way" scenario diagrams for the
fuehrerschein COURSE layer (data/fuehrerschein_course.json), rendered as
section_kind "media" / media.type "image" sections - see
docs/course-media-sections.md.

Deliberately a SEPARATE script from assets/generate_signs.py and
assets/generate_diagrams.py: AGENTS.md's "Parallel vs. sequential work"
section flags generate_signs.py as a file that must never be edited
concurrently, and generate_diagrams.py owns the per-QUESTION diagrams
(vorfahrt-NN[-answer].svg) referenced from the question bank's image_ref.
These are course assets with their own naming space (kurs-vorfahrt-NN.svg),
so they get their own file and neither script needs touching.

House style is the one already used by assets/generate_diagrams.py and the
StVO sign icons: flat, schematic, high contrast, no gradients, no
photorealism - grey road bands, dashed lane markings, rounded-rectangle
cars with a triangular nose, and the project's own bicycle/pedestrian
pictograms (adapted from sym_bicycle()/sym_pedestrian() in
generate_signs.py, i.e. this project's own artwork). Every composition is
original: it depicts a GENERIC intersection geometry derived from the StVO
rules being taught, and is not traced from, modelled on, or a close
imitation of any official Fragenkatalog image, ADAC material or any
third-party driving-school illustration. No branding, no real street names.

Actor labels are single LATIN LETTERS (A/B/C/D) on purpose, not words: the
course ships de + en (and more later), and a baked-in German word inside an
SVG would be wrong in every other locale. The per-locale alt_text/caption in
data/fuehrerschein_course.json says which letter is which road user.

Output: assets/diagrams/kurs-vorfahrt-NN.svg AND app/assets/diagrams/... in
the same run (same two-target convention as generate_signs.py).
"""
import os

VB = 260

BG = "#eef1f8"
ROAD = "#8a93a8"
LANE = "#f5f7fb"
WALK = "#cfd6e6"        # footway / sidewalk band
BIKELANE = "#c98f68"    # Radweg / Radverkehrsfuehrung band (red-brown asphalt)
CAR_YOU = "#2f6fed"     # the learner's own vehicle
CAR_OTHER = "#4a5266"   # another motor vehicle
CAR_PARKED = "#7a8296"  # a parked, stationary vehicle (no arrow)
VRU = "#1f3a5f"         # cyclist / pedestrian pictograms
ZEBRA = "#f7f9fd"

# Lane centre lines for a 64 px road centred on 130 (two 32 px lanes,
# right-hand traffic).
C = 130
RW = 64
NB, SB = 146, 114       # vertical road: north-bound / south-bound lane centre
EB, WB = 146, 114       # horizontal road: east-bound / west-bound lane centre

_marker_n = [0]


def svg(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{VB}" height="{VB}" '
        f'viewBox="0 0 {VB} {VB}" role="img">\n'
        f'<rect width="{VB}" height="{VB}" fill="{BG}"/>\n{body}\n</svg>\n'
    )


def road_h(y=C, w=RW, dashes=True):
    out = f'<rect x="0" y="{y - w / 2}" width="{VB}" height="{w}" fill="{ROAD}"/>'
    if dashes:
        out += (f'<line x1="0" y1="{y}" x2="{VB}" y2="{y}" stroke="{LANE}" '
                f'stroke-width="2" stroke-dasharray="9,9"/>')
    return out


def road_v(x=C, w=RW, dashes=True):
    out = f'<rect x="{x - w / 2}" y="0" width="{w}" height="{VB}" fill="{ROAD}"/>'
    if dashes:
        out += (f'<line x1="{x}" y1="0" x2="{x}" y2="{VB}" stroke="{LANE}" '
                f'stroke-width="2" stroke-dasharray="9,9"/>')
    return out


def junction_clear(x=C, y=C, w=RW):
    """Repaint the junction box in plain road grey so the two centre-line
    dashes do not run through the intersection - centre lines stop at a
    junction in reality, and a cross of dashes reads as a marking that
    isn't there."""
    return (f'<rect x="{x - w / 2}" y="{y - w / 2}" width="{w}" height="{w}" '
            f'fill="{ROAD}"/>')


def walk_h(y, w=13):
    return f'<rect x="0" y="{y - w / 2}" width="{VB}" height="{w}" fill="{WALK}"/>'


def bike_band_v(x, w=24):
    """A cycle track alongside the carriageway, continuing across the
    junction (a Radverkehrsfuehrung in the sense of § 9 Abs. 2 Satz 3 StVO)."""
    return f'<rect x="{x - w / 2}" y="0" width="{w}" height="{VB}" fill="{BIKELANE}"/>'


def bike_band_junction(x, w=24, y=C, rw=RW):
    """The same cycle track WHERE IT CROSSES the junction box. Drawn after
    junction_clear(), which would otherwise paint plain road grey over it."""
    return (f'<rect x="{x - w / 2}" y="{y - rw / 2}" width="{w}" height="{rw}" '
            f'fill="{BIKELANE}"/>')


def zebra(x0, x1, y=C, w=RW, stripes=5):
    """Fussgaengerueberweg marking - Zeichen 293, i.e. the broad white bars
    across the carriageway (StVO Anlage 3). Drawn from the marking alone; no
    upright sign is depicted."""
    out = ""
    span = x1 - x0
    bw = span / (stripes * 2 - 1)
    for i in range(stripes):
        sx = x0 + i * 2 * bw
        out += (f'<rect x="{sx:.1f}" y="{y - w / 2 + 3}" width="{bw:.1f}" '
                f'height="{w - 6}" fill="{ZEBRA}"/>')
    return out


def car(cx, cy, angle, color, ego=False):
    """Rounded-rectangle car with a triangular nose marking the direction it
    faces (angle 0 = facing up / north). The learner's own car additionally
    carries a small white roof dot, so "which one am I" survives greyscale
    printing and colour-vision differences."""
    roof = f'<circle cx="0" cy="0" r="4.5" fill="#fff"/>' if ego else ""
    return f'''
  <g transform="translate({cx},{cy}) rotate({angle})">
    <rect x="-11" y="-18" width="22" height="36" rx="6" fill="{color}"/>
    <polygon points="0,-23 -7,-14 7,-14" fill="{color}"/>{roof}
  </g>'''


def bicycle(cx, cy, angle=0, color=VRU, scale=0.45):
    """Cyclist seen from above-behind, drawn from this project's own
    sym_bicycle() silhouette (assets/generate_signs.py) plus a rider dot.
    Native pictogram bbox is roughly x 19-83, y 59-81, so it is recentred
    on (0,0) before scaling."""
    glyph = f'''<circle cx="30" cy="70" r="11" fill="none" stroke="{color}" stroke-width="6"/>
    <circle cx="72" cy="70" r="11" fill="none" stroke="{color}" stroke-width="6"/>
    <path d="M30 70 L50 70 L46 46 L30 70 M50 70 L64 46 L46 46 M64 46 L72 70" stroke="{color}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M64 46 L74 40" stroke="{color}" stroke-width="6" stroke-linecap="round"/>
    <line x1="46" y1="46" x2="42" y2="40" stroke="{color}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="52" cy="30" r="12" fill="{color}"/>'''
    # rotate(angle-90): the pictogram is drawn facing right, the diagram
    # convention is angle 0 = facing up.
    return f'''
  <g transform="translate({cx},{cy}) rotate({angle - 90}) scale({scale}) translate(-51,-52)">
    {glyph}
  </g>'''


def pedestrian(cx, cy, color=VRU, scale=0.55, flip=False):
    """Walking pedestrian, from this project's own sym_pedestrian()
    silhouette (assets/generate_signs.py). Native bbox ~x 33-65, y 23-78."""
    glyph = f'''<circle cx="50" cy="30" r="8" fill="{color}"/>
    <rect x="43" y="38" width="14" height="21" rx="6" fill="{color}"/>
    <path d="M46 42 L33 51 M54 42 L65 35" stroke="{color}" stroke-width="6" stroke-linecap="round"/>
    <path d="M46 57 L35 78 M54 57 L63 74" stroke="{color}" stroke-width="6.5" stroke-linecap="round"/>'''
    sx = -scale if flip else scale
    return f'''
  <g transform="translate({cx},{cy}) scale({sx},{scale}) translate(-49,-50)">
    {glyph}
  </g>'''


def tag(cx, cy, letter, color):
    """Actor label: a white disc with a coloured ring and a bold letter.
    Readable on road grey, on the light background and on the cycle band
    alike, which a bare <text> is not."""
    return f'''
  <circle cx="{cx}" cy="{cy}" r="12" fill="#fff" stroke="{color}" stroke-width="2.5"/>
  <text x="{cx}" y="{cy + 5}" font-family="Arial, Helvetica, sans-serif" font-size="15"
        font-weight="700" fill="{color}" text-anchor="middle">{letter}</text>'''


def _marker(color):
    """markerUnits="userSpaceOnUse" is load-bearing: SVG's default is
    "strokeWidth", which multiplies the marker box by the line's stroke-width
    and produced arrowheads several times larger than the vehicles on the
    first render of these diagrams."""
    _marker_n[0] += 1
    mid = f"ah{_marker_n[0]}"
    return mid, (f'<defs><marker id="{mid}" markerUnits="userSpaceOnUse" '
                 f'markerWidth="11" markerHeight="11" refX="9.5" refY="5.5" '
                 f'orient="auto"><path d="M0,0.5 L10,5.5 L0,10.5 Z" '
                 f'fill="{color}"/></marker></defs>')


def arrow(x1, y1, x2, y2, color):
    mid, defs = _marker(color)
    return (f'{defs}<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="3.5" stroke-linecap="round" marker-end="url(#{mid})"/>')


def arrow_path(d, color):
    mid, defs = _marker(color)
    return (f'{defs}<path d="{d}" fill="none" stroke="{color}" stroke-width="3.5" '
            f'stroke-linecap="round" marker-end="url(#{mid})"/>')


SCENES = {}

# --------------------------------------------------------------------------
# kurs-vorfahrt-01 - plain rechts vor links, two cars, no signs.
# A (you) from the south going straight on; B from A's right going straight
# on. § 8 Abs. 1 Satz 1 StVO: B has priority.
# --------------------------------------------------------------------------
b = road_h() + road_v() + junction_clear()
b += car(NB, 222, 0, CAR_YOU, ego=True) + arrow(NB, 194, NB, 170, CAR_YOU)
b += tag(NB + 32, 224, "A", CAR_YOU)
b += car(226, WB, -90, CAR_OTHER) + arrow(198, WB, 172, WB, CAR_OTHER)
b += tag(226, WB - 32, "B", CAR_OTHER)
SCENES["kurs-vorfahrt-01"] = b

# --------------------------------------------------------------------------
# kurs-vorfahrt-02 - same unsigned crossroads, but the vehicle coming from
# the right is a BICYCLE on the carriageway (no cycle track present).
# § 8 Abs. 1 Satz 1 + § 2 Abs. 1 Satz 1 StVO: the cyclist has priority.
# --------------------------------------------------------------------------
b = road_h() + road_v() + junction_clear()
b += car(NB, 222, 0, CAR_YOU, ego=True) + arrow(NB, 194, NB, 170, CAR_YOU)
b += tag(NB + 32, 224, "A", CAR_YOU)
b += bicycle(218, WB, -90) + arrow(196, WB, 172, WB, VRU)
b += tag(222, WB - 32, "B", VRU)
SCENES["kurs-vorfahrt-02"] = b

# --------------------------------------------------------------------------
# kurs-vorfahrt-03 - § 9 Abs. 3 Satz 1: A turns right across a cycle track
# carrying a cyclist going STRAIGHT ON in the same direction. The cyclist
# goes first; this is a turning rule, not a Vorfahrt rule.
# --------------------------------------------------------------------------
BIKE_X = 174
b = road_h() + road_v() + bike_band_v(BIKE_X) + junction_clear()
b += bike_band_junction(BIKE_X)
b += car(NB, 214, 0, CAR_YOU, ego=True)
b += arrow_path(f"M{NB},188 Q{NB},{EB} 208,{EB}", CAR_YOU)
b += tag(NB - 36, 216, "A", CAR_YOU)
b += bicycle(BIKE_X, 212) + arrow(BIKE_X, 192, BIKE_X, 168, VRU)
b += tag(BIKE_X + 34, 214, "B", VRU)
SCENES["kurs-vorfahrt-03"] = b

# --------------------------------------------------------------------------
# kurs-vorfahrt-04 - NO Fussgaengerueberweg: a pedestrian steps off the kerb
# between parked cars, mid-block. § 25 Abs. 3 Satz 1 StVO puts the duty to
# watch the traffic on the pedestrian; § 26 does not apply at all. § 1 Abs. 2
# still binds the driver.
# --------------------------------------------------------------------------
b = road_h() + walk_h(C - RW / 2 - 6) + walk_h(C + RW / 2 + 6)
b += car(50, 140, 90, CAR_YOU, ego=True) + arrow(78, 140, 108, 140, CAR_YOU)
b += tag(50, 108, "A", CAR_YOU)
b += car(148, 156, 90, CAR_PARKED) + car(218, 156, 90, CAR_PARKED)
b += pedestrian(183, 158) + arrow(183, 138, 183, 108, VRU)
b += tag(183, 194, "B", VRU)
SCENES["kurs-vorfahrt-04"] = b

# --------------------------------------------------------------------------
# kurs-vorfahrt-05 - a marked Fussgaengerueberweg (Zeichen 293). Pedestrian B
# clearly wants to use it (§ 26 Abs. 1 StVO); cyclist C RIDES across it and is
# not among the road users § 26 Abs. 1 names.
# --------------------------------------------------------------------------
b = road_h() + walk_h(C - RW / 2 - 6) + walk_h(C + RW / 2 + 6)
b += zebra(138, 198)
b += car(46, EB, 90, CAR_YOU, ego=True) + arrow(74, EB, 104, EB, CAR_YOU)
b += tag(46, 112, "A", CAR_YOU)
b += pedestrian(150, 176) + arrow(150, 154, 150, 106, VRU)
b += tag(118, 190, "B", VRU)
b += bicycle(188, 104, 180) + arrow(188, 124, 188, 154, VRU)
b += tag(222, 96, "C", VRU)
SCENES["kurs-vorfahrt-05"] = b

# --------------------------------------------------------------------------
# kurs-vorfahrt-06 - the four-actor case: A turns right; B approaches from
# A's LEFT on the crossing road; C cycles straight on alongside A; D crosses
# the side road A is turning into, with no marked crossing.
# § 9 Abs. 3 Satz 1 (C) + Satz 3 (D), then § 8 Abs. 1 Satz 1 and
# § 8 Abs. 2 Satz 4 (B waits for A).
# --------------------------------------------------------------------------
b = road_h() + road_v() + bike_band_v(BIKE_X) + junction_clear()
b += bike_band_junction(BIKE_X)
b += car(NB, 224, 0, CAR_YOU, ego=True)
b += arrow_path(f"M{NB},198 Q{NB},{EB} 212,{EB}", CAR_YOU)
b += tag(NB - 36, 226, "A", CAR_YOU)
b += car(28, EB, 90, CAR_OTHER) + arrow(56, EB, 88, EB, CAR_OTHER)
b += tag(28, 184, "B", CAR_OTHER)
b += bicycle(BIKE_X, 220) + arrow(BIKE_X, 200, BIKE_X, 176, VRU)
b += tag(BIKE_X + 34, 222, "C", VRU)
b += pedestrian(236, 180, flip=True) + arrow(236, 158, 236, 104, VRU)
b += tag(238, 216, "D", VRU)
SCENES["kurs-vorfahrt-06"] = b


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    targets = [os.path.join(here, "diagrams"),
               os.path.join(repo, "app", "assets", "diagrams")]
    for t in targets:
        os.makedirs(t, exist_ok=True)
    for name, body in sorted(SCENES.items()):
        out = svg(body)
        for t in targets:
            with open(os.path.join(t, f"{name}.svg"), "w", encoding="utf-8") as f:
                f.write(out)
    print(f"Wrote {len(SCENES)} course scenario SVGs to:")
    for t in targets:
        print(f"  {t}")


if __name__ == "__main__":
    main()
