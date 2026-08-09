#!/usr/bin/env python3
"""Builds app/data/fuehrerschein/primers.json + app/data/fuehrerschein/primers_locales/*.json
from data/fuehrerschein_primers_source.json (the single source of truth for DN-52's
"kickstart learning journey" topic-primer content - see docs/kickstart-learning-journey-scoping.md).

Mirrors the split pattern build_modules.py already uses for question data (core
structural fields vs. per-locale text), so the primer content follows the same
discipline: edit the source file, re-run this script, never hand-edit the
generated app/data files directly.

Run from the data/ directory: `python3 build_primers.py`

NOTE (standing gotcha from this session): this script does NOT touch
assets/sign_reference.json or app/data/<module>/*.json for question content -
it only regenerates the fuehrerschein primer files. If you also ran
build_modules.py in the same session, remember that separately wipes and
rebuilds app/data/**, so re-run build_primers.py AFTER build_modules.py if
both need to run, or the primer files will be gone.
"""
import json
import os

LOCALES = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]

SOURCE_PATH = "fuehrerschein_primers_source.json"
OUT_DIR = "../app/data/fuehrerschein"


def main():
    with open(SOURCE_PATH, encoding="utf-8") as f:
        chunks = json.load(f)

    # Structural gap check before writing anything - fail loudly rather than
    # silently shipping a locale gap (AGENTS.md non-negotiable constraint 5).
    problems = []
    for c in chunks:
        for lang in LOCALES:
            entry = c.get(lang)
            if not entry or not entry.get("title") or not entry.get("body"):
                problems.append((c.get("id"), lang))
    if problems:
        raise SystemExit(f"Locale gaps found, aborting build: {problems}")

    core = {
        "meta": {
            "app": "fluegel-angeln / fuehrerschein-lernmodul",
            "version": "0.1",
            "generated": "2026-08-09",
            "description": (
                "DN-52 Phase 1 kickstart-learning-journey primers: short 5-10 "
                "minute topic-primer chunks that bridge a beginner to each "
                "Fuehrerschein exam topic before they start practicing real "
                "exam questions. Content is original, grounded in verified "
                "sample questions from pilot_questions.json plus well-established "
                "StVO/StVZO/StVG/StGB structure - NOT copied from the licensed "
                "amtlicher Fragenkatalog or commercial exam-prep material. See "
                "docs/kickstart-learning-journey-scoping.md for the full feature "
                "scoping."
            ),
            "locales": LOCALES,
        },
        "primers": [
            {"id": c["id"], "topic_code": c["topic_code"], "order": c["order"]}
            for c in chunks
        ],
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f"{OUT_DIR}/primers.json", "w", encoding="utf-8") as f:
        json.dump(core, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT_DIR}/primers.json with {len(core['primers'])} entries")

    os.makedirs(f"{OUT_DIR}/primers_locales", exist_ok=True)
    for lang in LOCALES:
        locale_data = {
            c["id"]: {"title": c[lang]["title"], "body": c[lang]["body"]}
            for c in chunks
        }
        with open(f"{OUT_DIR}/primers_locales/{lang}.json", "w", encoding="utf-8") as f:
            json.dump(locale_data, f, ensure_ascii=False, indent=2)
        print(f"Wrote {OUT_DIR}/primers_locales/{lang}.json with {len(locale_data)} entries")


if __name__ == "__main__":
    main()
