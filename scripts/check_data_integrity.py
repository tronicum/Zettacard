#!/usr/bin/env python3
"""
DN-94: fast, browser-free integrity checks on generated question data.

Runs in about a second over every module and locale. This is the bottom of the
test pyramid described in docs/adr/ADR-exam-e2e-testing.md: it cannot tell you
a translation is *wrong* (see translation_ledger.py for staleness, and the LLM
QA ADR for meaning), but it catches every structural defect that has actually
occurred in this project, and it catches them before a browser is ever started.

Checks per module:
  1. Generated app/data/<m>/locales/<l>.json matches what the master in data/
     would produce. Catches the 2026-09-05 failure mode where translation fixes
     were written to generated files and would have been erased by the next
     build - and its mirror image, master edits that never reached the app.
  2. Every locale has exactly the question ids listed in core.json.
  3. Every question's option keys match the German original's, per locale.
  4. Every id in core.json has a `correct` answer, and every letter in it
     actually exists in that question's options in EVERY locale. A translation
     that drops or renames an option would make a question unanswerable.
  5. No empty question/option/explanation strings.
  6. No leaked authoring tokens in learner-visible prose (high_stakes,
     grundstoff, topic_code, TODO, FIXME, {{...}}). Nine real `high_stakes`
     leaks were found in datenschutz's German text.
  7. No text identical to the German in a non-German locale (untranslated
     leftovers), ignoring strings too short to be meaningful.

Usage:  python3 scripts/check_data_integrity.py [--module <name>]
Exit 1 on any failure.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "data")
APP_DATA = os.path.join(REPO, "app", "data")

MASTERS = {
    "fuehrerschein": "pilot_questions.json",
    "motorrad": "motorrad_pilot.json",
    "lkw": "lkw_pilot.json",
    "fuehrerschein_bus": "fuehrerschein_bus_pilot.json",
    "datenschutz": "datenschutz_pilot.json",
    "arbeitssicherheit": "arbeitssicherheit_pilot.json",
    "ki_act": "ki_act_pilot.json",
    "it_sicherheit": "it_sicherheit_pilot.json",
    "hinweisgeberschutz": "hinweisgeberschutz_pilot.json",
    "angelschein_bayern": "angelschein_bayern_pilot.json",
    "angelschein_nrw": "angelschein_nrw_pilot.json",
}

LEAK_PATTERNS = [
    re.compile(r"\bhigh_stakes\b"),
    re.compile(r"\bgrundstoff\b"),
    re.compile(r"\btopic_code\b"),
    # case-sensitive on purpose: authoring markers are always caps, and a
    # case-insensitive TODO matches the Spanish word "todo" ("all").
    re.compile(r"\b(TODO|FIXME|XXX|TBD)\b"),
    re.compile(r"\{\{.*?\}\}"),
]
MIN_UNTRANSLATED_LEN = 25


def walk_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


def check_module(module, failures):
    def fail(msg):
        failures.append(f"[{module}] {msg}")

    core_path = os.path.join(APP_DATA, module, "core.json")
    loc_dir = os.path.join(APP_DATA, module, "locales")
    if not os.path.exists(core_path) or not os.path.isdir(loc_dir):
        fail("missing core.json or locales/ - module not built?")
        return
    core = json.load(open(core_path, encoding="utf-8"))
    core_q = {q["id"]: q for q in core["questions"]}
    locales = sorted(f[:-5] for f in os.listdir(loc_dir) if f.endswith(".json"))
    if "de" not in locales:
        fail("no German locale - nothing to compare translations against")
        return
    de = json.load(open(os.path.join(loc_dir, "de.json"), encoding="utf-8"))

    # 1. generated vs master
    master_file = MASTERS.get(module)
    if master_file and os.path.exists(os.path.join(DATA, master_file)):
        mq = json.load(open(os.path.join(DATA, master_file), encoding="utf-8"))["questions"]
        for loc in locales:
            gen = json.load(open(os.path.join(loc_dir, f"{loc}.json"), encoding="utf-8"))
            rebuilt = {}
            for q in mq:
                t = q.get("text", {}).get(loc)
                e = q.get("explanation", {}).get(loc)
                if t is None or e is None:
                    continue
                rebuilt[q["id"]] = {
                    "question": t["question"], "options": t["options"], "explanation": e,
                }
            drift = [k for k in set(gen) | set(rebuilt) if gen.get(k) != rebuilt.get(k)]
            if drift:
                fail(f"{loc}: {len(drift)} question(s) differ between master and generated "
                     f"file - a build would change them: {sorted(drift)[:5]}")

    for loc in locales:
        data = json.load(open(os.path.join(loc_dir, f"{loc}.json"), encoding="utf-8"))
        # 2. id parity
        missing = [i for i in core_q if i not in data]
        extra = [i for i in data if i not in core_q]
        if missing:
            fail(f"{loc}: {len(missing)} id(s) in core.json missing from locale: {missing[:5]}")
        if extra:
            fail(f"{loc}: {len(extra)} id(s) not in core.json: {extra[:5]}")

        for qid, entry in data.items():
            if qid not in core_q:
                continue
            de_entry = de.get(qid, {})
            # 3. option-key parity with German
            if loc != "de" and de_entry:
                if set(entry.get("options", {})) != set(de_entry.get("options", {})):
                    fail(f"{loc}/{qid}: option keys differ from German "
                         f"({sorted(entry.get('options', {}))} vs {sorted(de_entry.get('options', {}))})")
            # 4. answer key resolvable
            correct = core_q[qid].get("correct")
            if not correct:
                fail(f"{qid}: no `correct` answer in core.json")
            else:
                for letter in correct:
                    if letter not in entry.get("options", {}):
                        fail(f"{loc}/{qid}: correct answer '{letter}' has no matching option "
                             f"- question is unanswerable in this language")
            # 5/6/7
            for path, s in walk_strings(entry, qid):
                if not s.strip():
                    fail(f"{loc}/{path}: empty string")
                for pat in LEAK_PATTERNS:
                    if pat.search(s):
                        fail(f"{loc}/{path}: leaked authoring token: {s.strip()[:80]!r}")
                        break
            if loc != "de" and de_entry:
                for field in ("question", "explanation"):
                    a, b = entry.get(field, ""), de_entry.get(field, "")
                    if a and a == b and len(a) >= MIN_UNTRANSLATED_LEN:
                        fail(f"{loc}/{qid}.{field}: identical to German - untranslated?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", help="check only this module")
    args = ap.parse_args()
    modules = sorted(d for d in os.listdir(APP_DATA)
                     if os.path.isdir(os.path.join(APP_DATA, d)))
    if args.module:
        modules = [args.module]
    failures = []
    checked = 0
    for m in modules:
        if not os.path.isdir(os.path.join(APP_DATA, m, "locales")):
            continue
        check_module(m, failures)
        checked += 1
    if failures:
        print(f"FAILED - {len(failures)} problem(s) across {checked} module(s):\n")
        for f in failures[:200]:
            print("  " + f)
        if len(failures) > 200:
            print(f"  ... and {len(failures) - 200} more")
        return 1
    print(f"OK - {checked} modules pass all data-integrity checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
