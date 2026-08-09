#!/usr/bin/env python3
"""One-off script (DN-XX, Sign Reference view) that assembles
app/data/fuehrerschein/sign_reference.json from ALREADY-VERIFIED content:
core.json's question -> image_ref/correct mapping, plus each of the 12
locale files' option text and explanation. This intentionally does NOT
invent any new factual claim about what a sign means - see
assets/generate_signs.py's many "verified" comments and BACKLOG.md's DN-32
entry for why that discipline matters in this project. Every name/description
below is lifted verbatim from an existing, already-reviewed question's
correct option text or explanation.

Categorization (StVO family) is derived from which SVG template function
assets/generate_signs.py used to draw each ref - not re-derived from
scratch - by locating the ref's dict entry in that file's SIGNS /
BATCH_A_SIGNS / BATCH_B_SIGNS / BATCH_C_SIGNS / BATCH_D_SIGNS registries and
mapping the outer template call name to a category. A few refs that exist as
shipped SVG files but have no registry entry at all (leftover from an older
generator run - see 1020-32/1022-10) can't be categorized this way and fall
back to "sonstige".

Run: python3 assets/build_sign_reference.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CORE_PATH = os.path.join(ROOT, "app", "data", "fuehrerschein", "core.json")
LOCALE_DIR = os.path.join(ROOT, "app", "data", "fuehrerschein", "locales")
GEN_SIGNS_PATH = os.path.join(HERE, "generate_signs.py")
OUT_PATH = os.path.join(ROOT, "app", "data", "fuehrerschein", "sign_reference.json")

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
    for dict_name in ["SIGNS", "BATCH_A_SIGNS", "BATCH_B_SIGNS", "BATCH_C_SIGNS", "BATCH_D_SIGNS"]:
        block = extract_dict_block(gen_text, dict_name)
        # Match lines like:  "205": yield_sign(),   or   "308": square_blue(...),
        for m in re.finditer(r'"([\w.\-]+)"\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(', block):
            ref, fn = m.group(1), m.group(2)
            ref_to_template[ref] = fn
    return ref_to_template


def category_for(ref, ref_to_template):
    fn = ref_to_template.get(ref)
    if fn is None:
        return DEFAULT_CATEGORY
    return TEMPLATE_TO_CATEGORY.get(fn, DEFAULT_CATEGORY)


def collect_refs_and_questions(core):
    """ref -> list of (qid, correct_letters) """
    ref_to_qids = {}
    qid_to_correct = {}
    for q in core["questions"]:
        ir = q.get("image_ref")
        qid_to_correct[q["id"]] = q.get("correct") or []
        if not ir:
            continue
        ref = ir.split("/", 1)[1]
        ref_to_qids.setdefault(ref, []).append(q["id"])
    return ref_to_qids, qid_to_correct


def build_entry_for_ref(ref, qids, qid_to_correct, locale):
    """Pick the best candidate question for this ref in one locale and
    return {"name": ..., "desc": ...}, or None if nothing usable is found."""
    candidates = []
    for qid in qids:
        loc = locale.get(qid)
        if not loc:
            continue
        letters = qid_to_correct.get(qid) or []
        if not letters:
            continue
        opts = loc.get("options", {})
        # Use the first correct letter's option text as the "name".
        letter = letters[0]
        name = opts.get(letter)
        if not name:
            continue
        desc = loc.get("explanation") or name
        candidates.append((name, desc))
    if not candidates:
        return None
    # Prefer the shortest, most canonical-sounding correct-option text as the
    # "name" (short names like "Vorfahrt gewaehren" read better as a sign
    # label than a full sentence) - per task guidance, eyeballed heuristic,
    # not a hard rule.
    candidates.sort(key=lambda t: len(t[0]))
    name, desc = candidates[0]
    return {"name": name, "desc": desc}


LOCALES = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]


def main():
    core = json.load(open(CORE_PATH, encoding="utf-8"))
    locales = {
        lang: json.load(open(os.path.join(LOCALE_DIR, f"{lang}.json"), encoding="utf-8"))
        for lang in LOCALES
    }
    gen_text = open(GEN_SIGNS_PATH, encoding="utf-8").read()

    ref_to_template = parse_ref_to_template(gen_text)
    ref_to_qids, qid_to_correct = collect_refs_and_questions(core)

    result = {cat: [] for cat in CATEGORY_ORDER}
    skipped = []

    for ref in sorted(ref_to_qids.keys()):
        qids = ref_to_qids[ref]
        entries_by_lang = {
            lang: build_entry_for_ref(ref, qids, qid_to_correct, locales[lang])
            for lang in LOCALES
        }
        # de/en gate whether this ref is usable at all (same standing as
        # before this change) - the other 10 locales fall back to en if a
        # given ref's question text happens to be missing/empty for them
        # (shouldn't happen given pilot_questions.json's own zero-locale-gap
        # guarantee, but fail soft here rather than dropping the whole ref).
        if not entries_by_lang["de"] or not entries_by_lang["en"]:
            skipped.append((ref, qids))
            continue
        entry = {"ref": ref}
        for lang in LOCALES:
            entry[lang] = entries_by_lang[lang] or entries_by_lang["en"]
        cat = category_for(ref, ref_to_template)
        result[cat].append(entry)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {OUT_PATH}")
    for cat in CATEGORY_ORDER:
        print(f"  {cat}: {len(result[cat])}")
    if skipped:
        print("Skipped (no usable locale text found):")
        for ref, qids in skipped:
            print(f"  {ref}: cited by {qids}")


if __name__ == "__main__":
    main()
