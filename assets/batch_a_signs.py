#!/usr/bin/env python3
"""
Batch A: Gefahrzeichen (StVO Anlage 1) extension for generate_signs.py.

New symA_* icon helpers + BATCH_A_SIGNS dict, following the exact style of
generate_signs.py (original simplified black-line pictograms, drawn inside
the existing triangle_warning() template). This file assumes triangle_warning,
sym_bicycle, svg(), etc. are already available (defined in generate_signs.py)
when merged - it is not meant to run standalone.
"""

# ---- symA_* icon helpers (original, simplified, black-on-white) ----------

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
    # 121 einseitig verengte Fahrbahn (rechts): left edge unaffected,
    # right edge angles inward
    return '''<line x1="30" y1="30" x2="30" y2="80" stroke="#000" stroke-width="6"/>
  <path d="M78 30 L54 62 L54 80" stroke="#000" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'''

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
