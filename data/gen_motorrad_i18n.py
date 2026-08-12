#!/usr/bin/env python3
"""One-off script to add the 10 additional locale translations for the 48
newly-authored Motorrad questions (motorrad-<topic>-16..27, added by the
motorrad_scaleout expansion) and (re)generate the runtime data files the
app loads.

Mirrors data/gen_waffensachkunde_i18n.py's approach, but scoped only to the
48 new question ids in this module - the pre-existing 90 questions already
carry all 12 locales and are left untouched (merged straight through).

Inputs:
  - data/motorrad_pilot.json           (138 questions; 90 pre-existing with
                                         all 12 locales, 48 new DE+EN-only)
  - data/motorrad_i18n/<lang>.json     (translations for uk, pl, ar, zh, hi,
                                         tr, fr, ru, es, it, authored for the
                                         48 new question ids only; each is
                                         {question_id: {question, options,
                                         explanation}})

Outputs:
  - data/motorrad_pilot.json           (rewritten in place with all 138
                                         questions now carrying all 12 locales)
  - app/data/motorrad/core.json
  - app/data/motorrad/locales/<lang>.json   for all 12 locales
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(HERE, "..", "app", "data")
PILOT_PATH = os.path.join(HERE, "motorrad_pilot.json")
I18N_DIR = os.path.join(HERE, "motorrad_i18n")

NEW_LOCALES = ["uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
ALL_LOCALES = ["de", "en"] + NEW_LOCALES


def load_translations():
    translations = {}
    for loc in NEW_LOCALES:
        path = os.path.join(I18N_DIR, f"{loc}.json")
        with open(path, "r", encoding="utf-8") as f:
            translations[loc] = json.load(f)
    return translations


def build():
    with open(PILOT_PATH, "r", encoding="utf-8") as f:
        pilot = json.load(f)

    translations = load_translations()
    # ids these translation files are scoped to (the 48 new questions)
    target_ids = set(next(iter(translations.values())).keys())

    questions = pilot["questions"]
    ids_seen = set()
    newly_translated = set()
    for q in questions:
        qid = q["id"]
        ids_seen.add(qid)
        existing_locales = set(q["text"].keys())
        if existing_locales == set(ALL_LOCALES):
            continue  # pre-existing question, already fully translated
        if qid not in target_ids:
            raise SystemExit(
                f"Question {qid} is missing locales {set(ALL_LOCALES) - existing_locales} "
                f"but is not covered by the new translation files"
            )
        for loc in NEW_LOCALES:
            entry = translations[loc].get(qid)
            if entry is None:
                raise SystemExit(f"Missing {loc} translation for question id {qid}")
            missing_opts = set(q["text"]["de"]["options"].keys()) - set(entry["options"].keys())
            if missing_opts:
                raise SystemExit(f"{loc}/{qid} missing option keys: {missing_opts}")
            q["text"][loc] = {
                "question": entry["question"],
                "options": entry["options"],
            }
            q["explanation"][loc] = entry["explanation"]
        newly_translated.add(qid)

    # sanity: translation files should cover exactly the target new ids
    for loc in NEW_LOCALES:
        extra = set(translations[loc].keys()) - target_ids
        missing = target_ids - set(translations[loc].keys())
        if extra or missing:
            raise SystemExit(f"{loc}.json id mismatch — extra={extra} missing={missing}")

    missing_targets = target_ids - newly_translated
    if missing_targets:
        raise SystemExit(f"Translation files cover ids not found in pilot: {missing_targets}")

    pilot["meta"]["locales"] = ALL_LOCALES

    # 1) rewrite master pilot file with all 12 locales for every question
    with open(PILOT_PATH, "w", encoding="utf-8") as f:
        json.dump(pilot, f, ensure_ascii=False, indent=2)

    # 2) app/data/motorrad/core.json + locales/<lang>.json
    module_dir = os.path.join(APP_DATA, "motorrad")
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    core_questions = []
    per_locale = {loc: {} for loc in ALL_LOCALES}

    for q in questions:
        qid = q["id"]
        base = dict(
            id=qid,
            topic=q["topic"],
            topic_code=q["topic_code"],
            class_scope=q["class_scope"],
            grundstoff=q["grundstoff"],
            legal_basis=q["legal_basis"],
            points=q["points"],
            high_stakes=q["high_stakes"],
            question_type=q["question_type"],
            image_ref=q["image_ref"],
            correct=q["correct"],
        )
        core_questions.append(base)
        for loc in ALL_LOCALES:
            per_locale[loc][qid] = {
                "question": q["text"][loc]["question"],
                "options": q["text"][loc]["options"],
                "explanation": q["explanation"][loc],
            }

    core_meta = dict(pilot["meta"])
    with open(os.path.join(module_dir, "core.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": core_meta, "questions": core_questions}, f, ensure_ascii=False, indent=2)

    for loc in ALL_LOCALES:
        with open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8") as f:
            json.dump(per_locale[loc], f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(questions)} questions x {len(ALL_LOCALES)} locales.")
    print(f"Newly translated ids: {len(newly_translated)}")
    print("Locales:", ALL_LOCALES)


if __name__ == "__main__":
    build()
