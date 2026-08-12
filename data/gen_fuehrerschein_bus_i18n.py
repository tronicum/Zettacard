#!/usr/bin/env python3
"""i18n finalization script for the fuehrerschein_bus module.

Reads the DE+EN pilot authored earlier (data/fuehrerschein_bus_pilot.json),
merges in the 10 additional locale translations authored under
data/i18n_fuehrerschein_bus/<lang>.json, writes the merged 12-locale pilot
back to data/fuehrerschein_bus_pilot.json, and then produces the runtime
data files the app loads:

  - app/data/fuehrerschein_bus/core.json          (locale-independent fields)
  - app/data/fuehrerschein_bus/locales/<lang>.json (12 files)

Mirrors data/gen_amateurfunk_e_i18n.py, scoped to this module.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(HERE, "..", "app", "data")
I18N_DIR = os.path.join(HERE, "i18n_fuehrerschein_bus")

PILOT_PATH = os.path.join(HERE, "fuehrerschein_bus_pilot.json")

EXTRA_LOCALES = ["uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
ALL_LOCALES = ["de", "en"] + EXTRA_LOCALES


def build():
    pilot = json.load(open(PILOT_PATH, encoding="utf-8"))

    translations = {}
    for loc in EXTRA_LOCALES:
        translations[loc] = json.load(
            open(os.path.join(I18N_DIR, f"{loc}.json"), encoding="utf-8")
        )

    core_questions = []
    per_locale = {loc: {} for loc in ALL_LOCALES}

    for q in pilot["questions"]:
        qid = q["id"]
        for loc in EXTRA_LOCALES:
            entry = translations[loc][qid]
            q["text"][loc] = {
                "question": entry["question"],
                "options": entry["options"],
            }
            q["explanation"][loc] = entry["explanation"]

        base = dict(
            id=q["id"], topic=q["topic"], topic_code=q["topic_code"],
            class_scope=q["class_scope"], grundstoff=q["grundstoff"],
            legal_basis=q["legal_basis"], points=q["points"],
            high_stakes=q["high_stakes"], question_type=q["question_type"],
            image_ref=q["image_ref"], correct=q["correct"],
        )
        if "roles" in q:
            base["roles"] = q["roles"]
        core_questions.append(base)

        for loc in ALL_LOCALES:
            per_locale[loc][qid] = {
                "question": q["text"][loc]["question"],
                "options": q["text"][loc]["options"],
                "explanation": q["explanation"][loc],
            }

    # Update meta.locales to the full set of 12
    pilot["meta"]["locales"] = ALL_LOCALES

    # 1) Write back the merged 12-locale master pilot file
    json.dump(pilot, open(PILOT_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 2) app/data/fuehrerschein_bus/core.json + locales/<lang>.json
    module_dir = os.path.join(APP_DATA, "fuehrerschein_bus")
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    core_meta = dict(pilot["meta"])
    json.dump({"meta": core_meta, "questions": core_questions},
              open(os.path.join(module_dir, "core.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    for loc in ALL_LOCALES:
        json.dump(per_locale[loc],
                  open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    print(f"Wrote {len(pilot['questions'])} fuehrerschein_bus questions in {len(ALL_LOCALES)} locales.")
    topics = {}
    for q in pilot["questions"]:
        topics.setdefault(q["topic_code"], 0)
        topics[q["topic_code"]] += 1
    print(topics)


if __name__ == "__main__":
    build()
