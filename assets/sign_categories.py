"""The one definition of which category a German traffic sign belongs to.

The category is not hand-written per sign: it is derived from the SVG
TEMPLATE the sign is drawn with in generate_signs.py / batch_*_signs.py -
that is, from the sign's actual shape and colour, which is exactly what the
StVO's own grouping means by Gefahr-/Verbots-/Gebots-/Richtzeichen. A red
triangle IS a Gefahrzeichen; there is no second fact to maintain.

Extracted from assets/build_sign_reference.py (which now imports from here)
so that data/build_modules.py can assign question topic codes from the same
grouping without a second, drifting copy of the mapping. See roadmap 3.3.
"""

import os
import re

TEMPLATE_TO_CATEGORY = {
    "triangle_warning": "gefahrzeichen",
    "circle_prohibition": "verbotszeichen",
    "circle_no_entry": "verbotszeichen",
    "circle_stopping_ban": "verbotszeichen",
    "circle_end_restriction": "verbotszeichen",
    "circle_mandatory": "gebotszeichen",
    "square_blue": "richtzeichen",
    "rect_white_black_border": "richtzeichen",
    "rect_yellow_black_border": "richtzeichen",
    "rect_green_white_border": "richtzeichen",
    "sign_arrow_yellow": "richtzeichen",
    "sign_arrow_blue": "richtzeichen",
    "sign_zone_plate": "richtzeichen",
}
# anything else (andreaskreuz, yield_sign, stop_octagon, sym_zebra_marking,
# priority_road, diamond_yellow_border, gruenpfeil, zusatzzeichen, or a ref
# with no registry entry at all) falls into "sonstige".
DEFAULT_CATEGORY = "sonstige"

CATEGORY_ORDER = ["gefahrzeichen", "verbotszeichen", "gebotszeichen", "richtzeichen", "sonstige"]

SIGN_REGISTRY_DICTS = ["SIGNS", "BATCH_A_SIGNS", "BATCH_B_SIGNS", "BATCH_C_SIGNS", "BATCH_D_SIGNS"]


def extract_dict_block(text, dict_name):
    """Return the raw source text of `dict_name = { ... }` (brace-matched)."""
    m = re.search(re.escape(dict_name) + r"\s*=\s*\{", text)
    if not m:
        return ""
    start = m.end() - 1  # position of the opening brace
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return text[start:]


def parse_ref_to_template(gen_text):
    """Map each sign ref (dict key) to the outer template function name used
    to build it, by scanning the top-level 'REF': template_fn(...) lines of
    each registry dict in generate_signs.py."""
    ref_to_template = {}
    for dict_name in SIGN_REGISTRY_DICTS:
        block = extract_dict_block(gen_text, dict_name)
        # Match lines like:  "205": yield_sign(),   or   "308": square_blue(...),
        for m in re.finditer(r'"([\w.\-]+)"\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(', block):
            ref, fn = m.group(1), m.group(2)
            ref_to_template[ref] = fn
    return ref_to_template


def category_for_ref(ref, ref_to_template):
    """The category for one sign ref, or None when the ref is unknown.

    Returns None rather than DEFAULT_CATEGORY for an unknown ref so callers
    can tell "this is a sign we know, and it is uncategorised" apart from
    "this is not a sign ref at all" - build_modules.py needs that
    distinction, build_sign_reference.py does not and defaults it away.
    """
    fn = ref_to_template.get(str(ref))
    if fn is None:
        return None
    return TEMPLATE_TO_CATEGORY.get(fn, DEFAULT_CATEGORY)


def load_ref_to_template(root):
    """Read the sign registry and return ref -> template fn.

    generate_signs.py is the only file read, deliberately: it is where every
    registry dict (including the BATCH_* ones) is assigned, and reading the
    batch_*_signs.py modules as well would pick up their internal helper
    definitions and shadow the real entries. Same single source
    build_sign_reference.py has always used.
    """
    with open(os.path.join(root, "assets", "generate_signs.py"), encoding="utf-8") as fh:
        return parse_ref_to_template(fh.read())
