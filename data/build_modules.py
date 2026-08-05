#!/usr/bin/env python3
"""
DN-39: build the modular runtime data layout the app actually loads, out of
the flat editable master files content is generated/edited in
(pilot_questions.json for Fuehrerschein, angelschein_seed.json for the new
Angelschein seed). This is intentionally a BUILD step, not a rewrite of how
content gets authored - batch-generation agents keep editing one flat JSON
file per module, which is easier for them to reason about and diff, and
this script derives the per-module / per-locale files app.js actually
fetches at runtime.

Combines two previously-separate restructurings that were going to touch
the same code either way (see BACKLOG.md DN-36 and DN-39): splitting by
LOCALE (so a user only downloads their own language, not all 12) and
splitting by MODULE (so a Fuehrerschein user never downloads Angelschein
content and vice versa - and future classes/regions can be added without
growing the file every existing user already has cached).

Output layout (all under app/data/, replacing the old single app/data.json):
  app/data/modules.json                     - manifest of modules/classes/regions
  app/data/<exam_type>/core.json            - locale-independent question fields
  app/data/<exam_type>/locales/<lang>.json  - {id: {question, options, explanation}}

Run from the data/ directory: `python3 build_modules.py`
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.join(HERE, "..", "app", "data")

CORE_FIELDS = [
    "id", "topic", "topic_code", "exam_type", "grundstoff", "legal_basis",
    "points", "high_stakes", "question_type", "image_ref", "correct",
]
# scope field name differs by module (class_scope for Fuehrerschein,
# region_scope for Angelschein) - included in CORE_FIELDS output as
# whichever one the question actually has, so core.json stays generic.
SCOPE_FIELDS = ["class_scope", "region_scope"]


def split_module(src_path, exam_type, locales, out_meta_extra=None):
    src = json.load(open(src_path, encoding="utf-8"))
    questions = src["questions"]
    module_dir = os.path.join(APP_DATA, exam_type)
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    core_questions = []
    per_locale = {loc: {} for loc in locales}
    missing_locale_count = {loc: 0 for loc in locales}

    for q in questions:
        core = {k: q[k] for k in CORE_FIELDS if k in q}
        for sf in SCOPE_FIELDS:
            if sf in q:
                core[sf] = q[sf]
        core_questions.append(core)

        for loc in locales:
            t = q["text"].get(loc)
            expl = q["explanation"].get(loc)
            if t is None or expl is None:
                missing_locale_count[loc] += 1
                continue
            per_locale[loc][q["id"]] = {
                "question": t["question"],
                "options": t["options"],
                "explanation": expl,
            }

    meta = {k: v for k, v in src["meta"].items() if k not in ("locales",)}
    meta["locales"] = locales
    meta["total_questions"] = len(core_questions)
    if out_meta_extra:
        meta.update(out_meta_extra)

    json.dump({"meta": meta, "questions": core_questions},
              open(os.path.join(module_dir, "core.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    for loc in locales:
        json.dump(per_locale[loc],
                  open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)

    return len(core_questions), missing_locale_count


def main():
    if os.path.exists(APP_DATA):
        shutil.rmtree(APP_DATA)
    os.makedirs(APP_DATA, exist_ok=True)

    manifest = json.load(open(os.path.join(HERE, "modules_manifest.json"), encoding="utf-8"))
    json.dump(manifest, open(os.path.join(APP_DATA, "modules.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    fs_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    fs_count, fs_missing = split_module(
        os.path.join(HERE, "pilot_questions.json"), "fuehrerschein", fs_locales)
    print(f"fuehrerschein: {fs_count} questions, locale gaps: {fs_missing}")

    ang_locales = ["de", "en"]
    ang_count, ang_missing = split_module(
        os.path.join(HERE, "angelschein_seed.json"), "angelschein", ang_locales)
    print(f"angelschein: {ang_count} questions, locale gaps: {ang_missing}")

    moto_locales = ["de", "en"]
    moto_count, moto_missing = split_module(
        os.path.join(HERE, "motorrad_pilot.json"), "motorrad", moto_locales)
    print(f"motorrad: {moto_count} questions, locale gaps: {moto_missing}")

    lkw_locales = ["de", "en"]
    lkw_count, lkw_missing = split_module(
        os.path.join(HERE, "lkw_pilot.json"), "lkw", lkw_locales)
    print(f"lkw: {lkw_count} questions, locale gaps: {lkw_missing}")

    # DN-44: 4 fully separate workplace-compliance modules, first pilot batch
    # (20 questions each, DE/EN) - infra-first per PO decision, content is
    # deliberately a first pilot batch like Angelschein's DN-11 was, not a
    # full-scale batch yet.
    compliance_locales = ["de", "en"]
    dsg_count, dsg_missing = split_module(
        os.path.join(HERE, "datenschutz_pilot.json"), "datenschutz", compliance_locales)
    print(f"datenschutz: {dsg_count} questions, locale gaps: {dsg_missing}")

    asig_count, asig_missing = split_module(
        os.path.join(HERE, "arbeitssicherheit_pilot.json"), "arbeitssicherheit", compliance_locales)
    print(f"arbeitssicherheit: {asig_count} questions, locale gaps: {asig_missing}")

    kiact_count, kiact_missing = split_module(
        os.path.join(HERE, "ki_act_pilot.json"), "ki_act", compliance_locales)
    print(f"ki_act: {kiact_count} questions, locale gaps: {kiact_missing}")

    itsec_count, itsec_missing = split_module(
        os.path.join(HERE, "it_sicherheit_pilot.json"), "it_sicherheit", compliance_locales)
    print(f"it_sicherheit: {itsec_count} questions, locale gaps: {itsec_missing}")

    # Sanity: every core question must resolve in at least its canonical
    # locale, and every core question's scope field must be present -
    # otherwise the app would silently render a blank question.
    for exam_type in ("fuehrerschein", "angelschein", "motorrad", "lkw",
                       "datenschutz", "arbeitssicherheit", "ki_act", "it_sicherheit"):
        core = json.load(open(os.path.join(APP_DATA, exam_type, "core.json"), encoding="utf-8"))
        for q in core["questions"]:
            if not any(sf in q for sf in SCOPE_FIELDS):
                raise AssertionError(f"{exam_type}/{q['id']} has no scope field (class_scope/region_scope)")
        de = json.load(open(os.path.join(APP_DATA, exam_type, "locales", "de.json"), encoding="utf-8"))
        missing = [q["id"] for q in core["questions"] if q["id"] not in de]
        if missing:
            raise AssertionError(f"{exam_type}: {len(missing)} questions missing DE (canonical) text: {missing[:5]}")
    print("Sanity checks passed.")


if __name__ == "__main__":
    main()
