#!/usr/bin/env python3
"""
Batch B extension to generate_signs.py: StVO Anlage 2 Vorschriftzeichen
(prohibition/mandatory/regulatory signs), ~28-32 additional codes.

Import shape templates and icon helpers from generate_signs.py, add a
handful of new symB_*-prefixed icon helpers for symbols not already
covered, and expose BATCH_B_SIGNS = {code: svg_body, ...}.

Same minimalist original-pictogram style as the rest of the project - not
traced from any real sign-icon library.

Category verification notes (checked against independent sources, not
guessed):
  - 308 "Vorrang vor dem Gegenverkehr" is a blue SQUARE (Richtzeichen),
    NOT a blue circle - confirmed via multiple sources describing it as
    "ein blaues Quadrat" with a white arrow (priority direction) and a
    red arrow (yielding/oncoming direction) pointing opposite ways.
  - 224 (Haltestelle, used for Schulbushaltestelle context) and 229
    (Taxenstand) are blue rectangular/square Vorschriftzeichen plates
    (white symbol on blue), same square_blue family as e.g. 314 "P" and
    330 motorway signs - not a Verbotszeichen circle.
  - 241 (getrennter Rad- und Gehweg) and 242.1/242.2, 244.1/244.2, 245
    are all in the rectangular/square blue Vorschriftzeichen family
    (unlike 237/238/239/240 which are round blue Gebotszeichen) -
    confirmed via multiple sign-vendor listings describing 240-241,
    242.x, 244.x, 245 as "rechteckig".
  - 290.1/290.2 (Beginn/Ende eingeschraenktes Haltverbot fuer eine Zone)
    share the same blue-disc-with-red-ring family as 283/286, just for a
    zone - circle_stopping_ban, per the project's existing "end of..."
    grey-diagonal-overlay convention.
"""
from generate_signs import (
    svg, VB,
    triangle_warning, circle_prohibition, circle_mandatory, circle_no_entry,
    circle_stopping_ban, square_blue, diamond_yellow_border,
    rect_white_black_border, rect_yellow_black_border,
    sign_arrow_yellow, sign_arrow_blue, zusatzzeichen,
    sym_arrow_right, sym_arrow_left, sym_arrow_both,
    sym_bicycle, sym_car_silhouette, sym_motorcycle, sym_bus, sym_truck,
    sym_pedestrian, sym_horse_rider, sym_moped, sym_weight, sym_height,
    sym_width, sym_length, sym_snow_chain, sym_uturn_ban, sym_min_speed,
    sym_taxi_text,
)

# ---- new symB_* icon helpers (Batch B) --------------------------------

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
    # Zeichen 241 getrennter Rad- und Gehweg: bicycle pictogram over a
    # pedestrian pictogram, divided by a horizontal line - white on blue.
    return '''
  <circle cx="32" cy="40" r="9" fill="none" stroke="#fff" stroke-width="3.5"/>
  <circle cx="60" cy="40" r="9" fill="none" stroke="#fff" stroke-width="3.5"/>
  <path d="M32 40 L46 20 L60 40 M46 20 L42 40 M46 24 L54 24" stroke="#fff" stroke-width="3.5" fill="none" stroke-linejoin="round"/>
  <line x1="10" y1="50" x2="90" y2="50" stroke="#fff" stroke-width="3"/>
  <circle cx="50" cy="60" r="6" fill="#fff"/>
  <rect x="44" y="67" width="12" height="16" rx="4" fill="#fff"/>
  <path d="M44 83 L37 93 M56 83 L63 93" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
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

BATCH_B_SIGNS = {
    # -- mandatory-direction family (circle_mandatory) --
    "211": circle_mandatory(sym_arrow_right()),
    "214": circle_mandatory(sym_arrow_both()),
    "222": circle_mandatory(sym_arrow_right()),
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
    "242.1": square_blue(sym_pedestrian(color="#fff")),
    "242.2": square_blue(symB_pedestrian_end()),
    "244.1": square_blue(sym_bicycle()),
    "244.2": square_blue(symB_bicycle_end()),
    "245": square_blue(sym_bus(color="#fff")),
    "290.1": circle_stopping_ban('<line x1="26" y1="26" x2="74" y2="74" stroke="#c0272d" stroke-width="8"/>'),
    "290.2": circle_stopping_ban(
        '<line x1="26" y1="26" x2="74" y2="74" stroke="#c0272d" stroke-width="8"/>'
        '<line x1="74" y1="26" x2="26" y2="74" stroke="#8a8a8a" stroke-width="6"/>'
    ),
}

def main():
    import os
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "signs")
    os.makedirs(out_dir, exist_ok=True)
    for ref, body in BATCH_B_SIGNS.items():
        with open(os.path.join(out_dir, f"{ref}.svg"), "w", encoding="utf-8") as f:
            f.write(svg(body))
    print(f"Wrote {len(BATCH_B_SIGNS)} Batch B sign SVGs to {out_dir}")

if __name__ == "__main__":
    main()
