#!/usr/bin/env python3
"""ADR-app-0003 § 3: the exam version moves only when the answers could.

The PO's rule: questions can improve or change; if a change would alter the
exam questions' answers, the exam must be adjusted; if not, the material can
improve and diversify against the same exam.

That rule is worth exactly as much as this file. A split nobody verifies is
two hex strings that drift apart silently, and the failure is invisible - a
record keeps citing an exam version while the answers underneath it move.

    python3 scripts/test_module_versions.py
"""

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "data"))

from build_modules import module_versions  # noqa: E402

FAILURES = []


def check(name, before, after, expect_exam, expect_material):
    e0, m0 = module_versions(before)
    e1, m1 = module_versions(after)
    exam_moved, material_moved = e0 != e1, m0 != m1
    ok = (exam_moved == expect_exam) and (material_moved == expect_material)
    verdict = "ok  " if ok else "FAIL"
    print(f"  {verdict}: {name}\n        exam {'moved' if exam_moved else 'same '} "
          f"(expected {'moved' if expect_exam else 'same'}), "
          f"material {'moved' if material_moved else 'same '} "
          f"(expected {'moved' if expect_material else 'same'})")
    if not ok:
        FAILURES.append(name)


def main():
    src = json.load(open(os.path.join(ROOT, "data", "pilot_questions.json"), encoding="utf-8"))
    base = src["questions"]

    def mutate(fn):
        qs = copy.deepcopy(base)
        fn(qs)
        return qs

    # --- must NOT move the exam: the material improving -------------------
    def better_explanation(qs):
        qs[0]["explanation"]["de"] = qs[0]["explanation"]["de"] + " Zusätzliche Erläuterung."
    check("a German explanation is improved", base, mutate(better_explanation), False, True)

    def better_translation(qs):
        qs[0]["text"]["uk"]["question"] = "Покращений переклад питання."
    check("a translation is improved", base, mutate(better_translation), False, True)

    def new_locale(qs):
        qs[0]["text"]["xx"] = {"question": "?", "options": {"a": "1"}}
    check("a new locale is added", base, mutate(new_locale), False, True)

    # --- MUST move the exam: the answers could differ ---------------------
    def flip_answer(qs):
        qs[0]["correct"] = ["a"] if qs[0]["correct"] != ["a"] else ["b"]
    check("an answer key is changed", base, mutate(flip_answer), True, False)

    def reword_german(qs):
        qs[0]["text"]["de"]["question"] = "Völlig andere Frage?"
    check("the canonical German question is reworded", base, mutate(reword_german), True, False)

    def change_option(qs):
        qs[0]["text"]["de"]["options"]["a"] = "Ein anderer Antworttext"
    check("a German option is reworded", base, mutate(change_option), True, False)

    def change_high_stakes(qs):
        qs[0]["high_stakes"] = not qs[0].get("high_stakes")
    check("high_stakes is flipped (it changes the pass rule)", base, mutate(change_high_stakes), True, False)

    def change_points(qs):
        qs[0]["points"] = (qs[0].get("points") or 3) + 1
    check("points are changed (they change the pass rule)", base, mutate(change_points), True, False)

    def drop_question(qs):
        qs.pop()
    check("a question leaves the draw", base, mutate(drop_question), True, True)

    # --- and it must be stable -------------------------------------------
    check("rebuilding unchanged content", base, copy.deepcopy(base), False, False)

    print()
    if FAILURES:
        print(f"FAILURES: {len(FAILURES)} - {', '.join(FAILURES)}")
        return 1
    print("all module-version invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
