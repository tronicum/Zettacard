#!/usr/bin/env python3
"""
Batch D: Zusatzzeichen (StVO Anlage 4, Zeichen 1000-series supplementary
plates) - additions to the main generate_signs.py catalog.

Reuses the existing `zusatzzeichen()` template (white rectangle, black
border, black content) from generate_signs.py and its icon helpers where
they fit (sym_caravan, sym_wheelchair, sym_arrow_right, ...). New icon
helpers needed for this batch are prefixed `symD_` to avoid colliding with
any other parallel batch's helpers; nothing in generate_signs.py is
modified or redefined here.

Output: merge BATCH_D_SIGNS into SIGNS (or run standalone - see main()).
"""
import os
from generate_signs import svg, zusatzzeichen, sym_caravan, sym_wheelchair, sym_arrow_right

# ---- new original pictogram helpers (symD_ prefix) ------------------------

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

def symD_bicycle_black():
    return '''<circle cx="36" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <circle cx="64" cy="64" r="12" fill="none" stroke="#000" stroke-width="4"/>
  <path d="M36 64 L50 40 L64 64 M50 40 L44 64 M50 48 L60 48" stroke="#000" stroke-width="4" fill="none" stroke-linejoin="round"/>'''

def symD_bike_end():
    # Zeichen 1012-31 Ende Radweg: bicycle icon with a grey diagonal line,
    # matching this project's existing "end of ..." convention (grey, not
    # red, since it marks a limit/end rather than a prohibition - see
    # sym_speed_number_crossed / priority_road(crossed=True) elsewhere in
    # generate_signs.py).
    return symD_bicycle_black() + '<line x1="18" y1="82" x2="82" y2="18" stroke="#8a8a8a" stroke-width="6"/>'

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

def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "signs")
    os.makedirs(out_dir, exist_ok=True)
    for ref, body in BATCH_D_SIGNS.items():
        with open(os.path.join(out_dir, f"{ref}.svg"), "w", encoding="utf-8") as f:
            f.write(svg(body))
    print(f"Wrote {len(BATCH_D_SIGNS)} sign SVGs to {out_dir}")

if __name__ == "__main__":
    main()
