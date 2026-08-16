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
    # DN-44: per-question role-relevance tags ("all", "all_staff", "hr",
    # "it", "management") - only present on the 4 compliance modules so far;
    # `k in q` in split_module() below means every other module's questions
    # (which have no "roles" field at all) are unaffected.
    "roles",
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


def split_course(exam_type, locales):
    """2026-08-15: optional v1 "course" sidecar layer, see
    claude/modular-course-architecture-v1-2026-08-15.md (Opus design doc,
    scoped explicitly as authoring scaffolding, NOT the SQLite migration).
    A module with no <exam_type>_course.json in data/ produces byte-identical
    output to before this function existed - this is opt-in per module via
    the "hasCourse" flag on its modules_manifest.json entry, set by hand
    alongside adding the course file, same as "feature_flag" is set by hand.

    Folded into build_modules.py rather than a fourth build script on
    purpose - the design doc explicitly calls out not repeating the mistake
    that silently dropped primers/sign_reference/dora/nis2/sportboot output
    twice this same week because they lived in separate scripts nothing
    reminded you to re-run.

    Returns True/False so main() can print progress; return value is
    otherwise unused there since hasCourse is set on the manifest by hand,
    not derived here (keeps this function read-only w.r.t. modules_manifest.json).
    """
    src_path = os.path.join(HERE, f"{exam_type}_course.json")
    if not os.path.exists(src_path):
        return False

    src = json.load(open(src_path, encoding="utf-8"))
    module_dir = os.path.join(APP_DATA, exam_type)
    locales_dir = os.path.join(module_dir, "course_locales")
    os.makedirs(locales_dir, exist_ok=True)

    per_locale = {loc: {} for loc in locales}

    def pull(entity, entity_id, field, key_field=None):
        """Pop a {locale: text} object off entity[field], fan each locale's
        text out into per_locale[loc][entity_id][field], and leave
        `<field>_key` (or key_field) pointing at entity_id - same
        key-is-the-entity-id convention build_modules.py already uses for
        primers, so app.js resolves course text the same way it resolves
        primer text (Rule 1/§4 of the design doc)."""
        if field not in entity:
            return
        val = entity.pop(field)
        for loc in locales:
            text = val.get(loc)
            if text is None:
                continue
            per_locale[loc].setdefault(entity_id, {})[field] = text
        entity[key_field or f"{field}_key"] = entity_id

    for course in src.get("courses", []):
        cid = course["course_id"]
        pull(course, cid, "title")
        pull(course, cid, "description")

        for concept in course.get("concepts", []):
            pull(concept, concept["concept_id"], "label")

        for unit in course.get("units", []):
            pull(unit, unit["unit_id"], "title")

        for lesson in course.get("lessons", []):
            lid = lesson["lesson_id"]
            pull(lesson, lid, "title")
            for section in lesson.get("sections", []):
                sid = section["section_id"]
                pull(section, sid, "title")
                pull(section, sid, "body")
            for rel in lesson.get("related", []):
                nk = rel.get("note_key")
                if nk:
                    pull(rel, nk, "body", key_field="body_key")

    json.dump(src, open(os.path.join(module_dir, "course.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    for loc in locales:
        json.dump(per_locale[loc],
                  open(os.path.join(locales_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    return True


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

    # DN-48: full 12-locale coverage (2026-08-05) - angelschein/motorrad/lkw
    # and all 4 DN-44 compliance modules were DE/EN-only pilots; translated
    # into the same 10 additional languages fuehrerschein already carries,
    # so every module now has full-parity locale coverage app-wide. Uses the
    # same fs_locales list as fuehrerschein above (kept as a separate name
    # per module for clarity/history, not because the actual language list
    # differs - it doesn't, all modules are on the same 12 languages now).
    ang_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    ang_count, ang_missing = split_module(
        os.path.join(HERE, "angelschein_seed.json"), "angelschein", ang_locales)
    print(f"angelschein: {ang_count} questions, locale gaps: {ang_missing}")

    moto_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    moto_count, moto_missing = split_module(
        os.path.join(HERE, "motorrad_pilot.json"), "motorrad", moto_locales)
    print(f"motorrad: {moto_count} questions, locale gaps: {moto_missing}")

    lkw_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    lkw_count, lkw_missing = split_module(
        os.path.join(HERE, "lkw_pilot.json"), "lkw", lkw_locales)
    print(f"lkw: {lkw_count} questions, locale gaps: {lkw_missing}")

    # 2026-08-15 bugfix, same class as dora/nis2/sportboot below: this call
    # was also missing despite app/data/fuehrerschein_bus being committed
    # with full 12-locale output already.
    bus_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    bus_count, bus_missing = split_module(
        os.path.join(HERE, "fuehrerschein_bus_pilot.json"), "fuehrerschein_bus", bus_locales)
    print(f"fuehrerschein_bus: {bus_count} questions, locale gaps: {bus_missing}")

    # DN-44: 4 fully separate workplace-compliance modules. Originally a
    # 20-question/DE-EN-only pilot batch; DN-48 (2026-08-05) scaled each to
    # 40 questions (clearing the 30-question exam-mode threshold) and added
    # the same 10 additional languages every other module now has.
    compliance_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    dsg_count, dsg_missing = split_module(
        os.path.join(HERE, "datenschutz_pilot.json"), "datenschutz", compliance_locales)
    print(f"datenschutz: {dsg_count} questions, locale gaps: {dsg_missing}")
    if split_course("datenschutz", ["de", "en"]):
        print("datenschutz: course layer built (de, en)")

    asig_count, asig_missing = split_module(
        os.path.join(HERE, "arbeitssicherheit_pilot.json"), "arbeitssicherheit", compliance_locales)
    print(f"arbeitssicherheit: {asig_count} questions, locale gaps: {asig_missing}")
    if split_course("arbeitssicherheit", ["de", "en"]):
        print("arbeitssicherheit: course layer built (de, en)")

    kiact_count, kiact_missing = split_module(
        os.path.join(HERE, "ki_act_pilot.json"), "ki_act", compliance_locales)
    print(f"ki_act: {kiact_count} questions, locale gaps: {kiact_missing}")
    if split_course("ki_act", ["de", "en"]):
        print("ki_act: course layer built (de, en)")

    itsec_count, itsec_missing = split_module(
        os.path.join(HERE, "it_sicherheit_pilot.json"), "it_sicherheit", compliance_locales)
    print(f"it_sicherheit: {itsec_count} questions, locale gaps: {itsec_missing}")
    if split_course("it_sicherheit", ["de", "en"]):
        print("it_sicherheit: course layer built (de, en)")

    # 2026-08-16 recovery: hinweisgeberschutz/kyc_aml/kartellrecht (DN-50/
    # DN-53) were authored in a past session but only ever committed to a
    # stranded backup branch (origin/backup/cloud-session-46-2026-08-12),
    # never merged into main - modules_manifest.json still listed all 3 as
    # live modules even though neither their pilot source nor this script's
    # split_module() calls for them existed on this branch, so a build here
    # would have produced a manifest entry with no backing data (a picker
    # option that 404s). Pilot JSON + the smoke test script recovered
    # verbatim from that backup branch; build_modules.py calls re-added here
    # to match. LkSG (also in the manifest) has no pilot anywhere, including
    # that backup branch - not recoverable the same way, needs an actual
    # question-bank authored from scratch first.
    hgs_count, hgs_missing = split_module(
        os.path.join(HERE, "hinweisgeberschutz_pilot.json"), "hinweisgeberschutz", compliance_locales)
    print(f"hinweisgeberschutz: {hgs_count} questions, locale gaps: {hgs_missing}")

    kyc_count, kyc_missing = split_module(
        os.path.join(HERE, "kyc_aml_pilot.json"), "kyc_aml", ["de", "en"])
    print(f"kyc_aml: {kyc_count} questions, locale gaps: {kyc_missing}")

    kartell_count, kartell_missing = split_module(
        os.path.join(HERE, "kartellrecht_pilot.json"), "kartellrecht", ["de", "en"])
    print(f"kartellrecht: {kartell_count} questions, locale gaps: {kartell_missing}")

    # 2026-08-15 bugfix: dora/nis2 split_module() calls had gone missing from
    # this script even though app/data/dora and app/data/nis2 were already
    # committed (built by some earlier version of this file). Since main()
    # rmtree()s APP_DATA unconditionally at the top, running the script
    # as-checked-in would have silently deleted both live modules and never
    # regenerated them - caught while wiring up CKA below, restored here.
    dora_count, dora_missing = split_module(
        os.path.join(HERE, "dora_pilot.json"), "dora", ["de", "en"])
    print(f"dora: {dora_count} questions, locale gaps: {dora_missing}")
    if split_course("dora", ["de", "en"]):
        print("dora: course layer built (de, en)")

    nis2_count, nis2_missing = split_module(
        os.path.join(HERE, "nis2_pilot.json"), "nis2", ["de", "en"])
    print(f"nis2: {nis2_count} questions, locale gaps: {nis2_missing}")
    if split_course("nis2", ["de", "en"]):
        print("nis2: course layer built (de, en)")

    # 2026-08-15 bugfix, same class as dora/nis2 above: sportboot_binnen/
    # sportboot_see (this week's 515-question ELWIS import, DE/EN pilot)
    # were ALSO missing from this script despite being live/committed -
    # caught by actually running this script and watching app/data/
    # sportboot_binnen vanish after the rmtree() with nothing rebuilding it.
    sb_count, sb_missing = split_module(
        os.path.join(HERE, "sportboot_binnen_pilot.json"), "sportboot_binnen", ["de", "en"])
    print(f"sportboot_binnen: {sb_count} questions, locale gaps: {sb_missing}")

    ss_count, ss_missing = split_module(
        os.path.join(HERE, "sportboot_see_pilot.json"), "sportboot_see", ["de", "en"])
    print(f"sportboot_see: {ss_count} questions, locale gaps: {ss_missing}")

    # 2026-08-15: CKA (Certified Kubernetes Administrator) concept-check
    # pilot - first module authored via the zettacard-kb kb->JSON->staging
    # pipeline (see claude/cka-amateurfunk-kb-pipeline-mvp-2026-08-15.md),
    # first module with EN as canonical/source locale rather than DE, and
    # first with a minimal 4-locale set (en/de/ja/zh) rather than the full
    # 12 - deliberately scoped smaller for this alpha round, see
    # claude/cka-i18n-minimal-schema-and-translation-plan-2026-08-15.md.
    cka_count, cka_missing = split_module(
        os.path.join(HERE, "cka_pilot.json"), "cka", ["en", "de", "ja", "zh"])
    print(f"cka: {cka_count} questions, locale gaps: {cka_missing}")
    if split_course("cka", ["en", "de", "ja", "zh"]):
        print("cka: course layer built (en, de, ja, zh)")

    # Sanity: every core question must resolve in at least its canonical
    # locale, and every core question's scope field must be present -
    # otherwise the app would silently render a blank question.
    for exam_type in ("fuehrerschein", "angelschein", "motorrad", "lkw", "fuehrerschein_bus",
                       "datenschutz", "arbeitssicherheit", "ki_act", "it_sicherheit",
                       "hinweisgeberschutz", "kyc_aml", "kartellrecht",
                       "dora", "nis2", "sportboot_binnen", "sportboot_see", "cka"):
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
