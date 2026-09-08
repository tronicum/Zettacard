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
import hashlib
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DATA = os.path.normpath(os.path.join(HERE, "..", "app", "data"))
REPO_ROOT = os.path.normpath(os.path.join(HERE, ".."))
# Guard rail for main()'s cleanup rmtree()s below: APP_DATA must resolve to
# exactly <repo>/app/data, never the repo root or an ancestor of it. If a
# future refactor changes HERE/APP_DATA's derivation and widens that, this
# assertion fails loudly instead of silently deleting something else.
assert APP_DATA == os.path.join(REPO_ROOT, "app", "data"), (
    f"APP_DATA resolved to an unexpected path: {APP_DATA!r}")
assert os.path.commonpath([APP_DATA, REPO_ROOT]) == REPO_ROOT and APP_DATA != REPO_ROOT, (
    f"APP_DATA {APP_DATA!r} is not safely nested under repo root {REPO_ROOT!r}")

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

# Every module this script builds. Used both for the targeted cleanup in
# main() and for the sanity checks at the end of it, so the two can't drift
# apart. NOTE: app/data/ also contains module directories this script does
# NOT build (they have no *_pilot.json source in data/) - see main()'s
# cleanup comment.
# 2026-09-06: the four fun_translation modules (zettacard-kb module_kind
# "fun_translation" - another country's road rules as a comparison object, see
# data-rules.md § 3b in the KB). Their masters are data/<module>_fun.json, not
# _pilot.json, because they are deliberately NOT part of the German exam set.
#
# They live in their own tuple and are folded into BUILT_MODULES below, and
# main() builds them by iterating THIS SAME tuple. That is on purpose: this
# file's history contains two separate outages (dora/nis2 on 2026-08-15,
# sportboot_binnen/see the same day) caused by a module sitting in
# BUILT_MODULES with no split_module() call, so the cleanup pass deleted its
# built output and nothing rebuilt it. Driving both ends off one tuple makes
# that particular drift impossible for these four. All are DE/EN only.
FUN_TRANSLATION_MODULES = (
    "california_us", "uk_gb", "austria_at", "switzerland_ch",
)

# ADR-app-0002 § 5: per-locale question counts, collected by split_module()
# as it writes each locale file and folded into app/data/modules.json at the
# end of main(). {exam_type: {"total": int, "locales": {lang: int}}}.
#
# This script already computed the same information - missing_locale_count -
# and printed it for a human to read, then dropped it on the floor. Meanwhile
# the app told every user that every module was available in their language,
# because nothing in the runtime data said otherwise. Both halves of that were
# a choice made when there were two modules on two locales.
#
# It stays DERIVED and never hand-written into modules_manifest.json: a
# hand-maintained copy of a number that changes with every content round is
# exactly the failure mode this phase exists to fix, and it would go stale in
# the direction that lies to the learner (claiming coverage that was removed).
# A module with no split_module() call here therefore gets no coverage block at
# all, and app.js says nothing about its languages rather than guessing.
COVERAGE = {}
# exam_type -> {"exam": <digest>, "material": <digest>} (ADR-app-0003 § 3)
VERSIONS = {}

BUILT_MODULES = (
    "fuehrerschein", "angelschein", "angelschein_bayern", "angelschein_nrw",
    "motorrad", "lkw", "fuehrerschein_bus",
    "datenschutz", "fadp_ch", "arbeitssicherheit", "ki_act", "it_sicherheit",
    "hinweisgeberschutz", "kyc_aml", "kartellrecht",
    "dora", "nis2", "sportboot_binnen", "sportboot_see", "cka", "aevo",
) + FUN_TRANSLATION_MODULES


# Which master file each module was built from, recorded by split_module() as
# it runs so split_course() can find the questions a derived lesson is made of
# (roadmap 3.4) without a second hand-maintained module->filename map that
# could silently disagree with the calls in main().
MASTER_SOURCE_BY_MODULE = {}


# --- ADR-app-0003 § 3: exam version vs material version -------------------
#
# The PO's rule: the exam must be versioned and the test must match that
# version; questions can improve or change; if a change would alter the
# answers, the exam is adjusted; if not, the material may improve and
# diversify against the same exam.
#
# So two digests, and the split is the whole point. A single digest over the
# module would move on a typo fix, a new locale or a better explanation, and
# every record would then cite a version nobody else ever had.
#
# EXAM_SURFACE is deliberately NOT the KB's source_hash. That recipe includes
# the German explanation, which is right for translation staleness - a
# translator translates the explanation too - and wrong here, because
# rewriting an explanation cannot change which option is correct. Including it
# would bump the exam every time the teaching improved, which is the exact
# behaviour this split exists to prevent.
EXAM_SURFACE_FIELDS = ("correct", "points", "high_stakes")


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def module_versions(questions, canonical_locale="de"):
    """(exam_version, material_version) for one module's questions.

    exam: what could change the right answer - the id set of the draw, each
    question's key/points/high_stakes, and its canonical-locale question and
    option text, because rewording the German can change what is correct.

    material: everything else - explanations, every translation, and anything
    else carried per question.
    """
    exam_parts, material_parts = [], []
    for q in sorted(questions, key=lambda x: str(x.get("id"))):
        qid = str(q.get("id"))
        de = (q.get("text") or {}).get(canonical_locale) or {}
        exam_parts.append(_canonical({
            "id": qid,
            "question": de.get("question", ""),
            "options": de.get("options", {}),
            **{f: q.get(f) for f in EXAM_SURFACE_FIELDS},
        }))
        material_parts.append(_canonical({
            "id": qid,
            "explanation": q.get("explanation"),
            # every locale except the canonical one; the canonical text is
            # already accounted for on the exam side
            "text": {l: v for l, v in (q.get("text") or {}).items() if l != canonical_locale},
        }))
    exam = hashlib.sha256("\n".join(exam_parts).encode("utf-8")).hexdigest()
    material = hashlib.sha256("\n".join(material_parts).encode("utf-8")).hexdigest()
    return exam[:12], material[:12]


def split_module(src_path, exam_type, locales, out_meta_extra=None,
                 core_key_order="canonical"):
    """core_key_order controls the key order of the per-question objects
    written to core.json. "canonical" (default, and what every module built
    by this script has always used) emits CORE_FIELDS order first, then
    whichever SCOPE_FIELD the question carries, last. "source" instead
    preserves the order the keys appear in the source file itself.

    The "source" mode exists because angelschein_bayern/angelschein_nrw were
    originally built by a separate, now-lost per-module generator script (see
    BACKLOG.md's "2026-08 content expansion round 2" - build_modules.py was
    deliberately not run for those rounds) which filtered the source question
    dict in place rather than re-ordering it, so their live/committed
    core.json has class_scope sitting between topic_code and grundstoff. It
    is purely a key-ordering choice - the app reads these objects by key and
    is indifferent - but keeping it lets those two modules rebuild
    byte-identically to what is deployed, instead of producing a ~100-question
    reordering diff that would look like a content change in review. Do not
    reach for this mode for new modules; use the default.
    """
    src = json.load(open(src_path, encoding="utf-8"))
    questions = src["questions"]
    MASTER_SOURCE_BY_MODULE[exam_type] = src_path
    module_dir = os.path.join(APP_DATA, exam_type)
    locales_dir = os.path.join(module_dir, "locales")
    os.makedirs(locales_dir, exist_ok=True)

    core_questions = []
    per_locale = {loc: {} for loc in locales}
    missing_locale_count = {loc: 0 for loc in locales}

    for q in questions:
        if core_key_order == "source":
            core = {k: v for k, v in q.items() if k in CORE_FIELDS or k in SCOPE_FIELDS}
        else:
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

    # ADR-app-0002 § 5. Counted off per_locale, not off `locales` minus
    # missing_locale_count, so the number is literally "how many entries are
    # in the file that just got written" - if the two ever disagree the file
    # is what the app fetches, and the manifest must describe the file.
    exam_version, material_version = module_versions(questions)
    VERSIONS[exam_type] = {"exam": exam_version, "material": material_version}
    COVERAGE[exam_type] = {
        "total": len(core_questions),
        "locales": {loc: len(per_locale[loc]) for loc in locales},
    }

    return len(core_questions), missing_locale_count


# --- section_kind "media" (2026-08-17) ----------------------------------
# Generic media capability for the course layer: a lesson section may carry
# a `media` object alongside (or instead of) its prose body. Four types:
# youtube | video_mp4 | image | slideshow. Full schema + a worked example:
# docs/course-media-sections.md. Rendering: renderCourseMedia() in app/app.js.
#
# The fact/text split this file applies to every other content type applies
# here too, and the boundary is: URLs, types, licence identifiers and
# dimensions are FACTS (they do not change per language, so they stay in
# course.json), while alt_text and caption are DISPLAY TEXT (they do, so
# they are pulled out into course_locales/<lang>.json under the same
# "the key IS the entity id" convention as title/body). Getting this
# backwards would mean 12 copies of the same YouTube id.
MEDIA_TYPES = ("youtube", "video_mp4", "image", "slideshow")

# Youtube video ids are exactly 11 chars of [A-Za-z0-9_-]. Authors may paste
# any of the usual URL shapes; the id is what gets stored, so app.js only
# ever concatenates a validated id into the youtube-nocookie.com embed URL
# and never a whole author-supplied URL.
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
YOUTUBE_URL_RES = [
    re.compile(r"^https?://(?:www\.|m\.)?youtube(?:-nocookie)?\.com/watch\?(?:.*&)?v=([A-Za-z0-9_-]{11})"),
    re.compile(r"^https?://(?:www\.|m\.)?youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})"),
    re.compile(r"^https?://(?:www\.|m\.)?youtube(?:-nocookie)?\.com/shorts/([A-Za-z0-9_-]{11})"),
    re.compile(r"^https?://youtu\.be/([A-Za-z0-9_-]{11})"),
]


def normalize_youtube_id(raw, where):
    """Accept a bare id or any common YouTube URL shape, return the bare id.

    Normalising at BUILD time (not at render time) is deliberate: a typo in a
    pasted URL fails this build loudly, instead of shipping a section that
    renders an empty iframe for every learner in every locale.
    """
    raw = str(raw).strip()
    if YOUTUBE_ID_RE.match(raw):
        return raw
    for rx in YOUTUBE_URL_RES:
        m = rx.match(raw)
        if m:
            return m.group(1)
    raise ValueError(
        f"{where}: not a recognisable YouTube video id or URL: {raw!r}. "
        "Give either the bare 11-character id or a youtube.com/watch?v=.../"
        "youtu.be/.../youtube.com/embed/... URL."
    )


def check_media_src(url, where, require_remote=False):
    """Validate a media src/poster URL at build time.

    Allowed: an absolute https:// URL (externally hosted - the PO's own CDN
    for MP4, or a licensed image host), or a repo-relative path such as
    "assets/diagrams/foo.svg" for assets that genuinely live in this repo
    (the future Fuehrerschein PNG/SVG diagram case). Rejected: anything
    else, notably http:// (mixed content) and any scheme like javascript:
    or data: - app.js re-checks the same allow-list before it touches the
    DOM, but failing here means it can never reach a learner at all.

    require_remote=True is used for video_mp4: per PO decision 2026-08-17,
    MP4s are referenced from external hosting and are NEVER committed into
    this git repo, so a repo-relative MP4 path is a mistake worth failing.
    """
    url = str(url).strip()
    if url.startswith("https://"):
        return url
    if require_remote:
        raise ValueError(
            f"{where}: video_mp4 src must be an absolute https:// URL on external "
            f"hosting (PO decision 2026-08-17: MP4 files are never committed to "
            f"this repo), got {url!r}."
        )
    if url.startswith(("http://", "//")) or ":" in url.split("/")[0]:
        raise ValueError(f"{where}: unsupported media src {url!r} (https:// or a repo-relative path only).")
    if url.startswith("/") or url.startswith("../"):
        raise ValueError(f"{where}: media src must be relative to app/ (e.g. \"assets/...\"), got {url!r}.")
    return url


def _norm_media_facts(media, where):
    """Normalise + validate the locale-INDEPENDENT half of a media object,
    in place. The locale-dependent half (alt_text/caption) is handled by
    split_media_text() below, which needs split_course()'s pull() closure."""
    mtype = media.get("type")
    if mtype not in MEDIA_TYPES:
        raise ValueError(f"{where}: media.type must be one of {MEDIA_TYPES}, got {mtype!r}.")

    # Licence metadata sits inline on the media object rather than in a
    # separate ASSET entity (course-layer design doc §2.7 wanted the full
    # entity; PO scoped this round to inline fields, matching how
    # meta.license / meta.license_url / section.license_ref already sit
    # inline on sibling content records). `license` is required precisely so
    # nobody can add a third-party asset without saying what it is licensed
    # under - the gap the design doc flagged as a hard blocker.
    if not str(media.get("license", "")).strip():
        raise ValueError(
            f"{where}: media.license is required (e.g. \"CC BY 4.0\", "
            "\"Zettacard original\", \"YouTube Standard License\")."
        )

    if mtype == "youtube":
        raw = media.pop("youtube_id", None) or media.pop("src", None)
        if not raw:
            raise ValueError(f"{where}: youtube media needs youtube_id (id or URL).")
        media["youtube_id"] = normalize_youtube_id(raw, where)
    elif mtype == "video_mp4":
        if not media.get("src"):
            raise ValueError(f"{where}: video_mp4 media needs src (external https:// URL).")
        media["src"] = check_media_src(media["src"], f"{where}.src", require_remote=True)
        if media.get("poster"):
            media["poster"] = check_media_src(media["poster"], f"{where}.poster")
    elif mtype == "image":
        if not media.get("src"):
            raise ValueError(f"{where}: image media needs src.")
        media["src"] = check_media_src(media["src"], f"{where}.src")
    elif mtype == "slideshow":
        slides = media.get("slides") or []
        if len(slides) < 2:
            raise ValueError(f"{where}: slideshow media needs at least 2 slides (use type \"image\" for one).")
        for n, slide in enumerate(slides, start=1):
            if not slide.get("src"):
                raise ValueError(f"{where}.slides[{n}]: needs src.")
            slide["src"] = check_media_src(slide["src"], f"{where}.slides[{n}].src")





# --- Roadmap 3.4: derived topic lessons ---------------------------------
#
# The problem, in the roadmap's own words: course prose exists in de/en only,
# while questions exist in 18 locales, so a prose-first lesson serves nobody
# who needs it most. Fuehrerschein shipped three authored lessons covering ONE
# of its topics; a learner whose German is poor - the primary audience - had
# nothing to read in their own language at all.
#
# So these lessons are DERIVED, from material that is already translated: each
# one is a handful of solved worked examples taken from the topic's own
# questions. Question text, the correct option and the explanation all exist
# per locale in the master file, so a derived lesson is available in every
# locale the questions are, for free, the day a translation lands. Nothing
# here is authored and nothing here is content - every string comes from a
# question the KB already masters (see zettacard-kb; this is the presentation
# layer re-using content, not a second copy of it).
#
# Authored lessons always win: a topic that already has one is skipped, so
# fs-l1's hand-written right-of-way primer is untouched and `vorfahrt` gets no
# derived lesson.
DERIVED_EXAMPLES_PER_LESSON = 4
DERIVED_QUIZ_COUNT = 8
DERIVED_COMPLETION_RULE = "quiz_pass:0.7"
# Roughly a minute per worked example plus the quiz. Honest enough for a
# "14 min" style hint; not worth deriving anything cleverer.
DERIVED_MINUTES_PER_EXAMPLE = 2


def _topics_already_taught(course):
    """Topic codes an AUTHORED lesson already selects."""
    covered = set()
    for lesson in course.get("lessons", []):
        for code in ((lesson.get("select") or {}).get("topic_codes") or []):
            covered.add(code)
    return covered


def _worked_example_body(q, loc, correct_label):
    """One worked example, in one locale, from the question itself.

    Question, then the answer marked as such, then the explanation. Returns
    None when this locale has no text for the question, so a partially
    translated module simply yields a shorter lesson in that locale rather
    than one padded with German.
    """
    text = (q.get("text") or {}).get(loc)
    if not text or not text.get("question"):
        return None
    parts = [text["question"].strip()]
    options = text.get("options") or {}
    answers = [options[k] for k in (q.get("correct") or []) if k in options]
    if answers:
        parts.append(f"{correct_label}: " + " / ".join(a.strip() for a in answers))
    explanation = (q.get("explanation") or {}).get(loc)
    if explanation:
        parts.append(explanation.strip())
    return "\n\n".join(parts)


# "Correct answer" as a label, per locale. The one place this file needs a
# string of its own, because no question carries one. Kept to the locales the
# questions actually ship in; a locale missing here falls back to English,
# which is still better than a bare answer with no marker.
CORRECT_ANSWER_LABEL = {
    "de": "Richtige Antwort", "en": "Correct answer", "uk": "Правильна відповідь",
    "pl": "Prawidłowa odpowiedź", "ar": "الإجابة الصحيحة", "zh": "正确答案",
    "hi": "सही उत्तर", "tr": "Doğru cevap", "fr": "Bonne réponse",
    "ru": "Правильный ответ", "es": "Respuesta correcta", "it": "Risposta corretta",
    "ro": "Răspuns corect", "bar": "Richtige Antwort", "fa": "پاسخ درست",
    "el": "Σωστή απάντηση", "hr": "Točan odgovor", "pt": "Resposta correta",
}


def derive_topic_lessons(exam_type, questions, course, locales):
    """Append one derived lesson per topic that has no authored lesson."""
    covered = _topics_already_taught(course)

    order, by_topic = [], {}
    for q in questions:
        code = q.get("topic_code")
        if not code or code in covered:
            continue
        if code not in by_topic:
            by_topic[code] = []
            order.append(code)
        by_topic[code].append(q)
    if not order:
        return 0

    prefix = f"{exam_type}-derived"
    unit = {
        "unit_id": f"{prefix}-u",
        "unit_kind": "module",
        "order": len(course.get("units", [])),
        # No title object: app.js renders a derived unit's heading from its own
        # UI strings (see `derived_unit` in renderCourseView). Inventing a unit
        # title in 18 languages to say "Topics" would be 18 strings to
        # translate for a word the app already has.
        "derived_unit": True,
    }
    course.setdefault("units", []).append(unit)

    lessons = course.setdefault("lessons", [])
    made = 0
    for topic_index, code in enumerate(order):
        pool = by_topic[code]
        # Safety-critical questions first, then stable by id, so a rebuild
        # produces the same lesson and a review diff stays readable.
        pool = sorted(pool, key=lambda q: (not q.get("high_stakes"), str(q.get("id"))))
        examples = pool[:DERIVED_EXAMPLES_PER_LESSON]
        if not examples:
            continue

        lesson_id = f"{prefix}-{code}"
        sections = []
        for n, q in enumerate(examples):
            body = {}
            for loc in locales:
                text = _worked_example_body(q, loc, CORRECT_ANSWER_LABEL.get(loc, CORRECT_ANSWER_LABEL["en"]))
                if text:
                    body[loc] = text
            if not body:
                continue
            section = {
                "section_id": f"{lesson_id}-s{n + 1}",
                "order": len(sections),
                "section_kind": "prose",
                "license_ref": "CC-BY-NC-SA-4.0",
                # Not "draft": this is not a draft awaiting review, it is a
                # mechanical re-presentation of questions that already carry
                # their own review state. Saying "draft" would put a review
                # queue in front of text that is already reviewed elsewhere.
                "review_status": "derived",
                "generator": f"derived:build_modules/{exam_type}",
                "body": body,
            }
            if q.get("legal_basis"):
                section["legal_basis"] = q["legal_basis"]
            sections.append(section)
        if not sections:
            continue

        lessons.append({
            "lesson_id": lesson_id,
            "unit_ref": unit["unit_id"],
            "order": 1000 + topic_index,  # after every authored lesson
            "lesson_kind": "primer",
            "estimated_minutes": len(sections) * DERIVED_MINUTES_PER_EXAMPLE,
            "completion_rule": DERIVED_COMPLETION_RULE,
            "select": {"topic_codes": [code], "count": DERIVED_QUIZ_COUNT},
            "sections": sections,
            # app.js titles a derived lesson with the topic's own label
            # (getTopicLabel), so the 18-locale title problem is solved by the
            # labels that already exist rather than by new strings.
            "derived_topic_code": code,
        })
        made += 1
    return made


# --- Roadmap 3.7: UI strings, mastered in the KB -------------------------
#
# The app's *_STRINGS dictionaries are content - a {locale: string} map,
# translated and reviewable like everything else - and they lived in app.js
# only because that was convenient. They are mastered in
# zettacard-kb/content/_ui now and arrive here as data/ui_strings.json.
#
# Fanned out one file per locale, so a learner downloads their own language
# and not eighteen. Same key-is-the-entity-id convention the question and
# course locale bundles already use, so app.js resolves them the same way.
#
# A string missing in a locale is simply absent from that locale's file; the
# app falls back (its own literal today, English once the literals go). It is
# deliberately NOT padded with German, because a German string sitting in the
# Ukrainian bundle is indistinguishable at runtime from a real translation.
def split_ui_strings():
    src_path = os.path.join(HERE, "ui_strings.json")
    if not os.path.exists(src_path):
        return 0
    src = json.load(open(src_path, encoding="utf-8"))
    out_dir = os.path.join(APP_DATA, "ui")
    os.makedirs(out_dir, exist_ok=True)

    per_locale = {loc: {} for loc in src["locales"]}
    args_by_key = {}
    for key, entry in src["strings"].items():
        if entry.get("args"):
            args_by_key[key] = entry["args"]
        for loc, text in (entry.get("text") or {}).items():
            if loc in per_locale:
                per_locale[loc][key] = text

    for loc, block in per_locale.items():
        json.dump(block, open(os.path.join(out_dir, f"{loc}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, sort_keys=True)
    # The placeholder order is a property of the key, not of a language, so it
    # is written once rather than repeated in all 18 bundles.
    json.dump({"args": args_by_key},
              open(os.path.join(out_dir, "_args.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, sort_keys=True)

    short = sum(1 for e in src["strings"].values() if len(e.get("text") or {}) < len(src["locales"]))
    print(f"  ui strings: {len(src['strings'])} keys, {len(per_locale)} locales"
          + (f", {short} not in every locale" if short else ""))
    return len(src["strings"])


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
    # Roadmap 3.4: top the authored course up with one derived lesson per
    # otherwise-untaught topic, BEFORE the locale fan-out below, so derived
    # text goes through exactly the same pull()/course_locales path as
    # authored text and app.js needs no second way to read it.
    derived = 0
    master = MASTER_SOURCE_BY_MODULE.get(exam_type)
    if master and os.path.exists(master):
        questions = json.load(open(master, encoding="utf-8"))["questions"]
        for course in src.get("courses", []):
            derived += derive_topic_lessons(exam_type, questions, course, locales)
    if derived:
        print(f"  {exam_type}: {derived} derived topic lessons")
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

    def split_media(section, sid):
        """section_kind "media": validate/normalise the fact half in place,
        then pull alt_text/caption into the locale bundles via pull() above.

        Locale keys used (all under the same "key IS the entity id" scheme
        app.js already resolves title/body with):
          <section_id>            -> {"alt_text": ..., "caption": ...}
          <section_id>-m<n>       -> per-slide {"alt_text": ..., "caption": ...}
        A slide may set its own "slide_id" to override the derived key; the
        derived form is what the docs recommend, so authors never have to
        invent ids.
        """
        media = section.get("media")
        if media is None:
            if section.get("section_kind") == "media":
                raise ValueError(f"{exam_type}/{sid}: section_kind \"media\" needs a media object.")
            return
        if section.get("section_kind") != "media":
            raise ValueError(
                f"{exam_type}/{sid}: has a media object but section_kind is "
                f"{section.get('section_kind')!r} - set section_kind \"media\"."
            )
        where = f"{exam_type}/{sid}.media"
        _norm_media_facts(media, where)

        # alt_text is required on anything that renders an <img> the learner
        # is meant to read (an <img> with no alt is an accessibility bug) -
        # per-media for "image", per-slide for "slideshow" (checked in the
        # slide loop below). It stays optional for youtube/video_mp4, where
        # the section title plus the play button's own localized aria-label
        # already name the thing.
        if media["type"] == "image" and "alt_text" not in media:
            raise ValueError(f"{where}: image media needs alt_text (per-locale object).")
        pull(media, sid, "alt_text")
        pull(media, sid, "caption")
        for n, slide in enumerate(media.get("slides") or [], start=1):
            slide_id = slide.get("slide_id") or f"{sid}-m{n}"
            slide["slide_id"] = slide_id
            if "alt_text" not in slide:
                raise ValueError(f"{where}.slides[{n}]: needs alt_text (per-locale object).")
            pull(slide, slide_id, "alt_text")
            pull(slide, slide_id, "caption")

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
                split_media(section, sid)
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


def copy_kubectl_drills(exam_type):
    """2026-09-02: kubectl command-recall drill set (data/cka_kubectl_drills.json),
    authored separately from the question bank / course layer by a parallel
    content workstream (see data/cka_kubectl_drills_NOTES.md). Wired into the
    build here as its own small sidecar, same "opt-in per module, absent
    source file = no-op" shape as split_course() above, rather than folded
    into split_module() - the shape is fundamentally different (a `tasks`
    array of drill/grammar objects, not `questions` with `text`/`explanation`
    per-locale blocks) and doesn't need a fact/text split: unlike course.json
    (12-locale modules, split to avoid every visitor downloading all 12),
    this file already only carries the cka module's existing 4-locale set
    (en/de/ja/zh, see meta.locales) inline per task, and at ~50 short tasks
    the whole file is small enough (a few hundred KB) that a per-locale split
    would add real complexity (a new course_locales-style directory, a new
    fetchLocaleTextWithFallback-shaped fallback chain in app.js) for a
    download-size saving that doesn't matter at this size. Revisit if a
    future drill set grows enough per-locale bytes to matter, or if it moves
    to the module's full 12-locale set the way courses can.

    Copied through mostly verbatim - the one thing genuinely worth validating
    at build time (same "fail loudly here, not at runtime for a learner"
    principle check_media_src()/normalize_youtube_id() apply above) is that
    meta.task_count / meta.locales actually match the real `tasks` array, so
    a future hand-edit to the source file that drifts the two can't ship
    silently.
    """
    src_path = os.path.join(HERE, f"{exam_type}_kubectl_drills.json")
    if not os.path.exists(src_path):
        return False

    src = json.load(open(src_path, encoding="utf-8"))
    tasks = src.get("tasks") or []
    meta = src.get("meta") or {}

    declared_count = meta.get("task_count")
    if declared_count is not None and declared_count != len(tasks):
        raise ValueError(
            f"{exam_type}_kubectl_drills.json: meta.task_count ({declared_count}) "
            f"!= actual len(tasks) ({len(tasks)})."
        )

    locales = meta.get("locales") or []
    if not locales:
        raise ValueError(f"{exam_type}_kubectl_drills.json: meta.locales is empty.")
    seen_ids = set()
    for t in tasks:
        tid = t.get("id")
        if not tid:
            raise ValueError(f"{exam_type}_kubectl_drills.json: a task is missing 'id'.")
        if tid in seen_ids:
            raise ValueError(f"{exam_type}_kubectl_drills.json: duplicate task id {tid!r}.")
        seen_ids.add(tid)
        for field in ("prompt", "hint", "success_message", "explanation"):
            val = t.get(field) or {}
            missing = [loc for loc in locales if loc not in val]
            if missing:
                raise ValueError(
                    f"{exam_type}_kubectl_drills.json: task {tid} field {field!r} "
                    f"missing locale(s) {missing} declared in meta.locales."
                )
        if "accepted_grammar" not in t or "reference_command" not in t:
            raise ValueError(
                f"{exam_type}_kubectl_drills.json: task {tid} needs both "
                "reference_command and accepted_grammar."
            )

    module_dir = os.path.join(APP_DATA, exam_type)
    os.makedirs(module_dir, exist_ok=True)
    json.dump(src, open(os.path.join(module_dir, "kubectl_drills.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return True


def write_modules_json():
    """Copy modules_manifest.json out to app/data/modules.json, folding in the
    per-locale coverage COVERAGE collected during this build (ADR-app-0002 § 5).

    The manifest on disk in data/ stays hand-edited and coverage-free; the
    runtime copy is the derived one. Two things are checked here rather than
    left to be noticed by a learner:

      * every module named in COVERAGE must exist in the manifest - a module
        built but not listed is a module nobody can reach;
      * a module's `kind` must be one of the four the picker groups by, since
        an unknown kind would silently drop its row out of every group.

    A manifest module with NO coverage entry is allowed and left alone: those
    are the four modules (lksg, waffensachkunde, amateurfunk_a/_e) that sit in
    the manifest with no source file anywhere in data/ - see the recovery notes
    in main() below. app.js shows no language marker for them.
    """
    manifest = json.load(open(os.path.join(HERE, "modules_manifest.json"), encoding="utf-8"))
    by_type = {m["exam_type"]: m for m in manifest["modules"]}

    unknown = sorted(set(COVERAGE) - set(by_type))
    if unknown:
        raise AssertionError(
            f"built module(s) with no modules_manifest.json entry: {unknown}")
    for m in manifest["modules"]:
        kind = m.get("kind")
        if kind not in ("licence", "compliance", "cert", "compare"):
            raise AssertionError(
                f"{m['exam_type']}: kind is {kind!r}; must be one of "
                "licence/compliance/cert/compare (see the manifest's _comment).")

    for exam_type, cov in COVERAGE.items():
        by_type[exam_type]["coverage"] = cov
    # ADR-app-0003 § 3. Published so a completion record can name the exam it
    # was taken against, and so the app can tell an old record from a current
    # one without asking anyone to keep a number by hand.
    for exam_type, ver in VERSIONS.items():
        by_type[exam_type]["versions"] = ver

    json.dump(manifest, open(os.path.join(APP_DATA, "modules.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    uncovered = sorted(t for t in by_type if t not in COVERAGE)
    if uncovered:
        print("NOTE: manifest modules with no built content, so no locale "
              "coverage and no language marker in the picker: " + ", ".join(uncovered))


def main():
    # Cleanup used to be an unconditional shutil.rmtree(APP_DATA), which is
    # why BACKLOG.md's 2026-08 content-expansion rounds all record "build_
    # modules.py was again deliberately NOT run": running it deleted every
    # module directory this script has no split_module() call for (round 1/2/3's
    # new modules), and every sidecar artifact produced by a *different*
    # script (data/build_primers.py's primers.json/primers_locales/,
    # assets/build_sign_reference.py's sign_reference.json) - the exact
    # "silently dropped primers/sign_reference" failure split_course()'s
    # docstring above warns about.
    #
    # Cleanup is now scoped to the artifacts this script actually owns and
    # rewrites - core.json + locales/ from split_module(), course.json +
    # course_locales/ from split_course() - for the modules it actually
    # builds. Everything else under app/data/ is left alone, and any module
    # directory with no source here is named in a warning so it's visible
    # rather than silently deleted.
    os.makedirs(APP_DATA, exist_ok=True)
    for name in BUILT_MODULES:
        module_dir = os.path.join(APP_DATA, name)
        for owned in ("core.json", "locales", "course.json", "course_locales", "kubectl_drills.json"):
            p = os.path.normpath(os.path.join(module_dir, owned))
            # Belt-and-braces: never delete anything that isn't actually
            # inside APP_DATA (the generated app/data/ tree), no matter what
            # `name`/`owned` end up being after a future edit.
            assert os.path.commonpath([p, APP_DATA]) == APP_DATA, (
                f"refusing to delete {p!r}: outside APP_DATA {APP_DATA!r}")
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.isfile(p):
                os.remove(p)
    unbuilt = sorted(n for n in os.listdir(APP_DATA)
                     if os.path.isdir(os.path.join(APP_DATA, n)) and n not in BUILT_MODULES)
    if unbuilt:
        print("WARNING: app/data/ module directories with no source in data/ "
              "(left untouched, NOT rebuilt): " + ", ".join(unbuilt))

    # The manifest used to be copied out to app/data/modules.json right here,
    # before any module was built, because it was a pure copy and the ordering
    # made no difference. It does now: ADR-app-0002 § 5 has the emitted copy
    # carry each module's per-locale question counts, which only exist once
    # split_module() has actually written the locale files. The copy therefore
    # happens at the END of main(), in write_modules_json() below.

    # 2026-09-05: "bar" (Bavarian), "fa" (Persian) and "ro" (Romanian) added for
    # fuehrerschein. NOTE the rmtree() in main(): a locale that exists as a
    # generated app/data/<module>/locales/<lang>.json but is NOT listed here is
    # DELETED by the next build with nothing to rebuild it from. That nearly
    # destroyed the Romanian compliance locale on 2026-09-05. If you add a
    # locale to the master files, add it here in the same commit.
    # 2026-09-06: el, hr, pt added — official exam languages for the German
    # Theorieprüfung, drafted in the KB and now carried by the app. A locale
    # MUST be listed here or split_module() will not emit it, and rmtree()
    # above has already removed whatever was there.
    fs_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it",
                  "bar", "fa", "ro", "el", "hr", "pt"]
    split_ui_strings()

    fs_count, fs_missing = split_module(
        os.path.join(HERE, "pilot_questions.json"), "fuehrerschein", fs_locales)
    print(f"fuehrerschein: {fs_count} questions, locale gaps: {fs_missing}")
    # 2026-08-17: fuehrerschein gains a course layer (it had none before) -
    # data/fuehrerschein_course.json, six labelled right-of-way scenario
    # diagrams as section_kind "media" / media.type "image" sections, plus a
    # non-quizzed "guidance" lesson on the film-sequence tasks the real theory
    # exam has contained since 1 April 2014. First shipped content anywhere in
    # this repo to use the media capability (docs/course-media-sections.md).
    # DE/EN only, per the established pattern that a course/question bank may
    # launch DE+EN while UI strings must carry all 12 locales - the question
    # bank itself stays on its full 12 and is untouched by this.
    # fs_locales, not ["de", "en"]: the authored prose is de/en and stays that
    # way (pull() simply finds no text for the rest), but the DERIVED lessons
    # added by derive_topic_lessons() are built from question text that exists
    # in all 18 - and fanning them out is the entire point of roadmap 3.4.
    if split_course("fuehrerschein", fs_locales):
        print("fuehrerschein: course layer built (de, en)")

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

    # 2026-08-16 recovery, second half. angelschein_bayern (48Q, BayFiG/
    # AVBayFiG) and angelschein_nrw (56Q, LFischG NRW) were authored,
    # fact-checked and deployed in the 2026-08-12 "content expansion round 2"
    # session but never committed in any form - not their source, not their
    # built output, not a build_modules.py entry (that round built them with
    # a per-module generator script and skipped this one on purpose, see the
    # rmtree note in main()). Their built output was recovered from the live
    # site in the preceding commit; these two pilot sources were then
    # reverse-engineered from that output so the content is hand-editable
    # again and rebuilds from data/ like every other module. core_key_order=
    # "source" keeps the rebuild byte-identical to the deployed files - see
    # split_module()'s docstring.
    ang_state_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it"]
    angby_count, angby_missing = split_module(
        os.path.join(HERE, "angelschein_bayern_pilot.json"), "angelschein_bayern",
        ang_state_locales, core_key_order="source")
    print(f"angelschein_bayern: {angby_count} questions, locale gaps: {angby_missing}")

    angnrw_count, angnrw_missing = split_module(
        os.path.join(HERE, "angelschein_nrw_pilot.json"), "angelschein_nrw",
        ang_state_locales, core_key_order="source")
    print(f"angelschein_nrw: {angnrw_count} questions, locale gaps: {angnrw_missing}")

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
    # 2026-09-05: "ro" added. Romanian was created by a translation round that
    # wrote only the generated app/data/<module>/locales/ro.json files; the
    # masters had no `ro` text at all. Because main()'s cleanup rmtree()s each
    # built module's whole locales/ directory before regenerating it, a build
    # would have deleted all four ro.json files outright with nothing to
    # rebuild them from. The Romanian text has now been folded back into the
    # *_pilot.json masters, and listing it here is what keeps it alive.
    # 2026-09-06: "fa" added — the KB now carries Persian for every compliance
    # module. A locale MUST be in this list or split_module() will not emit it
    # (and rmtree() above has already removed whatever was there).
    compliance_locales = ["de", "en", "uk", "pl", "ar", "zh", "hi", "tr", "fr", "ru", "es", "it", "ro", "bar", "fa"]
    dsg_count, dsg_missing = split_module(
        os.path.join(HERE, "datenschutz_pilot.json"), "datenschutz", compliance_locales)
    print(f"datenschutz: {dsg_count} questions, locale gaps: {dsg_missing}")
    if split_course("datenschutz", ["de", "en"]):
        print("datenschutz: course layer built (de, en)")

    # 2026-08-17: fadp_ch - the revised Swiss Federal Act on Data Protection
    # (revDSG/nDSG, SR 235.1, in force 1.9.2023) + its implementing ordinance
    # (DSV, SR 235.11). Deliberately a SEPARATE module from datenschutz above,
    # not extra topics inside it (PO scope decision 2026-08-16): the Swiss and
    # the EU regimes are related but legally distinct, and the two modules
    # cross-link rather than merge. DE/EN 40-question pilot, same launch
    # pattern as dora/nis2/kyc_aml/kartellrecht - source authored by
    # data/gen_fadp_ch.py, which carries the full Fedlex source list.
    fadp_count, fadp_missing = split_module(
        os.path.join(HERE, "fadp_ch_pilot.json"), "fadp_ch", ["de", "en"])
    print(f"fadp_ch: {fadp_count} questions, locale gaps: {fadp_missing}")

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
    if split_course("hinweisgeberschutz", ["de", "en"]):
        print("hinweisgeberschutz: course layer built (de, en)")

    kyc_count, kyc_missing = split_module(
        os.path.join(HERE, "kyc_aml_pilot.json"), "kyc_aml", compliance_locales)
    print(f"kyc_aml: {kyc_count} questions, locale gaps: {kyc_missing}")
    if split_course("kyc_aml", ["de", "en"]):
        print("kyc_aml: course layer built (de, en)")

    kartell_count, kartell_missing = split_module(
        os.path.join(HERE, "kartellrecht_pilot.json"), "kartellrecht", compliance_locales)
    print(f"kartellrecht: {kartell_count} questions, locale gaps: {kartell_missing}")
    if split_course("kartellrecht", ["de", "en"]):
        print("kartellrecht: course layer built (de, en)")

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

    # 2026-09-02: kubectl command-recall drill set - see copy_kubectl_drills()
    # docstring above for why this is its own small sidecar rather than a
    # split_module()/split_course() call. Standalone frontend feature (a
    # terminal-look widget, not a course lesson), gated in app.js on
    # state.examType === "cka" directly, same as Sign Reference/Learn are
    # gated on state.examType === "fuehrerschein" - no modules_manifest.json
    # flag needed for it.
    if copy_kubectl_drills("cka"):
        print("cka: kubectl drill set built (en, de, ja, zh)")

    # 2026-08-17: aevo - the German IHK/HWK Ausbildereignungspruefung under the
    # Ausbilder-Eignungsverordnung (AusbEignV 2009). 76-question DE/EN pilot,
    # source authored by data/gen_aevo.py, which carries the full source list
    # (AEVO + BBiG + JArbSchG + BetrVG + AGG statutory text, plus the BIBB
    # Hauptausschuss Rahmenplan AEVO of 20.6.2023, BAnz AT 14.07.2023 S2).
    #
    # Unlike cka - deliberately a light concept check because the real CKA exam
    # is 100 % hands-on - this one is framed as real practice-exam prep: AEVO's
    # written part genuinely IS a 180-minute closed-form MCQ exam (§ 4 Abs. 2
    # AEVO), so the framing is honest here. Four topics mapping 1:1 onto the
    # four Handlungsfelder of § 2 AEVO, weighted per the 2023 Rahmenplan's
    # 15/20/50/15 % recommendation rather than evenly.
    #
    # The course layer carries the part the question bank deliberately does NOT
    # cover: the PRACTICAL exam part (§ 4 Abs. 3 AEVO), as written, non-quizzed
    # guidance (lesson_kind "guidance", completion_rule "read", no select
    # block) - a presentation/live-delivery-plus-Fachgespraech performance
    # cannot honestly be tested as multiple choice.
    aevo_count, aevo_missing = split_module(
        os.path.join(HERE, "aevo_pilot.json"), "aevo", ["de", "en"])
    print(f"aevo: {aevo_count} questions, locale gaps: {aevo_missing}")
    if split_course("aevo", ["de", "en"]):
        print("aevo: course layer built (de, en)")

    # 2026-09-06: the four fun_translation modules. 50 questions each, DE/EN
    # only (data-rules.md § 3b in zettacard-kb: these sit outside the 15-locale
    # set and must never be counted as locale-coverage gaps), authored from the
    # primary law of each jurisdiction and exported by
    # zettacard-kb/src/export_to_zettacard.py to data/<module>_fun.json.
    #
    # out_meta_extra carries the mandatory § 3b identification banner (DE+EN)
    # from the master's meta into app/data/<module>/core.json's meta, so the
    # app has the "this is a study aid, not a German licence, not that
    # country's official exam, confers nothing" text available at render time
    # in the same place it reads total_questions from. The manifest's intro
    # step states the same thing in the same words - both come from the KB
    # module.json's `identification` block, so there is one wording, not two.
    for fun_type in FUN_TRANSLATION_MODULES:
        fun_src = os.path.join(HERE, f"{fun_type}_fun.json")
        fun_meta = json.load(open(fun_src, encoding="utf-8"))["meta"]
        identification = fun_meta.get("identification")
        if not identification:
            raise AssertionError(
                f"{fun_type}: no identification banner in {fun_src}. It is "
                f"mandatory for fun_translation modules (data-rules.md § 3b); "
                f"refusing to build a module that cannot show it.")
        fun_count, fun_missing = split_module(
            fun_src, fun_type, ["de", "en"],
            out_meta_extra={"identification": identification})
        print(f"{fun_type}: {fun_count} questions, locale gaps: {fun_missing}")

    # Sanity: every core question must resolve in at least its canonical
    # locale, and every core question's scope field must be present -
    # otherwise the app would silently render a blank question.
    for exam_type in BUILT_MODULES:
        core = json.load(open(os.path.join(APP_DATA, exam_type, "core.json"), encoding="utf-8"))
        for q in core["questions"]:
            if not any(sf in q for sf in SCOPE_FIELDS):
                raise AssertionError(f"{exam_type}/{q['id']} has no scope field (class_scope/region_scope)")
        de = json.load(open(os.path.join(APP_DATA, exam_type, "locales", "de.json"), encoding="utf-8"))
        missing = [q["id"] for q in core["questions"] if q["id"] not in de]
        if missing:
            raise AssertionError(f"{exam_type}: {len(missing)} questions missing DE (canonical) text: {missing[:5]}")

    # ADR-app-0002 § 5: the coverage numbers are only worth writing if they
    # describe the files actually on disk, so check them against the files
    # rather than against per_locale's own bookkeeping.
    for exam_type, cov in COVERAGE.items():
        for loc, n in cov["locales"].items():
            path = os.path.join(APP_DATA, exam_type, "locales", f"{loc}.json")
            actual = len(json.load(open(path, encoding="utf-8")))
            if actual != n:
                raise AssertionError(
                    f"{exam_type}/{loc}: coverage says {n} but {path} holds {actual}")
            if n > cov["total"]:
                raise AssertionError(
                    f"{exam_type}/{loc}: coverage {n} exceeds total {cov['total']}")

    write_modules_json()
    print("Sanity checks passed.")


if __name__ == "__main__":
    main()
