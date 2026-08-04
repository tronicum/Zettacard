#!/usr/bin/env python3
"""
Batch C extension to generate_signs.py: StVO Anlage 3 Richtzeichen
(informational signs) not yet covered by the base catalog. Same minimalist,
original-pictogram style as generate_signs.py - reuses its shape templates
and icon helpers where possible, and adds a small number of new ones (all
prefixed symC_ to avoid collisions with any other parallel batch of new
signs, plus one new shape template, rect_green_white_border, for the green
Europastrasse route-shield family).

Colors were verified (not assumed) for the signs most likely to be
mis-colored:
  - 310/311 Ortstafel: YELLOW rectangle, black border, black text (NOT
    blue like the Richtzeichen info-sign family) - confirmed via
    bussgeldkatalog.org ("Die gelben Richtzeichen ... geschlossene
    Ortschaft") and de.wikipedia.org/wiki/Bundesstra%C3%9Fe, which
    describes the whole "kleine, schwarzumrandete, gelbe Tafeln" family
    that 310/311/401 belong to.
  - 401 Bundesstrassen: YELLOW rectangle, black border, black numerals -
    confirmed via de.wikipedia.org/wiki/Bundesstra%C3%9Fe ("gelbe Tafeln
    mit der Nummer in schwarzer Schrift").
  - 410 Europastrassen: GREEN background, WHITE text (NOT yellow) -
    confirmed via de.wikipedia.org/wiki/Europastra%C3%9Fe ("a white E
    with road number on green background"). Needed a brand-new template,
    rect_green_white_border, since no green-plate shape existed yet.
  - 365-series service/facility signs (Tankstelle, Raststaette, Telefon,
    Camping, Ladestation, WC) and 328 Nothalte-/Pannenbucht: confirmed
    part of the ordinary blue-square Richtzeichen family (600x600mm
    square plates per strassenausstatter.de product specs), so
    square_blue is correct for all of them - not a separate color family.

Output: same ./signs/<ref>.svg convention as generate_signs.py, written by
running this file directly (it imports and augments generate_signs.py's
own writer).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_signs import (
    svg, square_blue, rect_white_black_border, rect_yellow_black_border,
    sign_arrow_yellow, sign_arrow_blue, sym_P, sym_first_aid_cross,
    sym_police_star, sym_fuel_pump, sym_bed, sym_cutlery, sym_toilet,
    sym_phone, sym_camp_tent, sym_ev_plug, sym_tunnel_shape, sym_house_car,
    sym_car_silhouette,
)

# ---- new shape template ------------------------------------------------

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
    # sym_house_car, with the project's standard grey diagonal "end" line.
    return sym_house_car() + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="7"/>'

def symC_car_end():
    # 331.2 Ende Kraftfahrstrasse: same car silhouette as 331.1, plus the
    # grey diagonal "end" line convention.
    return sym_car_silhouette("#fff") + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="7"/>'

def symC_waterdrop():
    # 354 Wasserschutzgebiet: simple original water-drop silhouette.
    return '<path d="M50 22 C62 40 74 54 74 66 A24 24 0 1 1 26 66 C26 54 38 40 50 22 Z" fill="#fff"/>'

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

BATCH_C_SIGNS = {
    # -- blue-square family (12) --
    "316": square_blue(symC_park_ride()),
    "317": square_blue(symC_hiker_park()),
    "325.1": square_blue(sym_house_car()),
    "325.2": square_blue(symC_house_car_end()),
    "327": square_blue(sym_tunnel_shape()),
    "331.1": square_blue(sym_car_silhouette("#fff")),
    "331.2": square_blue(symC_car_end()),
    "354": square_blue(symC_waterdrop()),
    "356": square_blue(symC_guard()),
    "358": square_blue(sym_first_aid_cross()),
    "363": square_blue(sym_police_star()),
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

def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "signs")
    os.makedirs(out_dir, exist_ok=True)
    for ref, body in BATCH_C_SIGNS.items():
        with open(os.path.join(out_dir, f"{ref}.svg"), "w", encoding="utf-8") as f:
            f.write(svg(body))
    print(f"Wrote {len(BATCH_C_SIGNS)} sign SVGs to {out_dir}")

if __name__ == "__main__":
    main()
