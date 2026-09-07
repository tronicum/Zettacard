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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CORE_PATH = os.path.join(ROOT, "app", "data", "fuehrerschein", "core.json")
LOCALE_DIR = os.path.join(ROOT, "app", "data", "fuehrerschein", "locales")
GEN_SIGNS_PATH = os.path.join(HERE, "generate_signs.py")
OUT_PATH = os.path.join(ROOT, "app", "data", "fuehrerschein", "sign_reference.json")

# The shape -> category mapping and the registry parser moved to
# assets/sign_categories.py so data/build_modules.py can assign question
# topic codes from the same grouping (roadmap 3.3). Re-exported here under
# their original names so the rest of this script is unchanged.
from sign_categories import (  # noqa: E402
    TEMPLATE_TO_CATEGORY,
    DEFAULT_CATEGORY,
    CATEGORY_ORDER,
    extract_dict_block,
    parse_ref_to_template,
)

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
