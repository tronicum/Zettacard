#!/usr/bin/env python3
"""
DN-94: translation staleness ledger.

WHY THIS EXISTS
---------------
On 2026-09-05 an entire class of defect was found in the fuehrerschein module:
the canonical German text for several questions had been revised, but only the
English translation was regenerated. Ten other languages silently kept their
pre-revision text. The result was structurally perfect JSON - correct ids,
correct option keys, valid answer keys - in which `zeichen-68` described an
obstacle-passing sign in ten languages while the German described Zeichen 214
(a mandatory-direction sign), and `zeichen-132` described a "Mofa frei" plate
where the German described the "Fussgaenger" supplementary sign.

No schema check, no JSON validation and no browser test can catch that: nothing
is malformed, the app renders it perfectly, and the wrong answer is still
"correct". It is only visible by comparing a translation against the German it
was made from - which is exactly what this script records.

HOW IT WORKS
------------
For every question, for every locale, we store a SHA-256 of the GERMAN source
cell (question + options + explanation + the `correct` key) that the translation
was last reconciled against. If the German is later edited, its hash changes and
every translation stamped against the old hash is reported STALE.

This is deliberately dumb: no model, no embeddings, no network, no judgement
calls, and therefore no false positives. It cannot tell you a translation is
*wrong* - only that the German moved underneath it and nobody re-checked. That
is precisely the defect that actually bit this project, and it runs in under a
second.

USAGE
    python3 scripts/translation_ledger.py check     # exit 1 if anything is stale
    python3 scripts/translation_ledger.py stamp     # record current state as reconciled
    python3 scripts/translation_ledger.py stamp --locale uk --module lkw
    python3 scripts/translation_ledger.py status    # human summary, always exit 0

`stamp` is an assertion by a human (or a reviewing agent) that the listed
translations have been checked against the current German. Stamping without
actually re-reading is how this tool gets defeated, so stamp narrowly: prefer
`--locale`/`--module`/`--id` over a blanket re-stamp.

The ledger lives in data/translation_state/<module>.json and is meant to be
committed, so staleness is visible in review as a diff.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "data")
LEDGER_DIR = os.path.join(DATA, "translation_state")
SOURCE_LOCALE = "de"

# module name -> master file in data/. Only modules whose questions carry
# per-locale `text`/`explanation` maps belong here.
MODULES = {
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
    "fadp_ch": "fadp_ch_pilot.json",
    "kartellrecht": "kartellrecht_pilot.json",
    "kyc_aml": "kyc_aml_pilot.json",
    "nis2": "nis2_pilot.json",
    "dora": "dora_pilot.json",
    "aevo": "aevo_pilot.json",
    "cka": "cka_pilot.json",
    "sportboot_binnen": "sportboot_binnen_pilot.json",
    "sportboot_see": "sportboot_see_pilot.json",
}


def source_hash(question):
    """Hash of everything a translator must be faithful to.

    Includes `correct`: if the answer key moves, existing translations may make
    the wrong option read as right, so that also invalidates a stamp.
    """
    de = question.get("text", {}).get(SOURCE_LOCALE)
    expl = question.get("explanation", {}).get(SOURCE_LOCALE)
    if de is None or expl is None:
        return None
    payload = {
        "question": de.get("question", ""),
        # sort_keys below makes option order irrelevant, but the mapping is not
        "options": de.get("options", {}),
        "explanation": expl,
        "correct": question.get("correct"),
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def load_master(module):
    path = os.path.join(DATA, MODULES[module])
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("questions", [])


def ledger_path(module):
    return os.path.join(LEDGER_DIR, f"{module}.json")


def load_ledger(module):
    p = ledger_path(module)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def save_ledger(module, ledger):
    os.makedirs(LEDGER_DIR, exist_ok=True)
    with open(ledger_path(module), "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def scan(module):
    """Return (stale, untracked, missing_source) for one module.

    stale          - German changed since the translation was stamped
    untracked      - a translation exists that was never stamped at all
    missing_source - question has no German; nothing can be verified against it
    """
    questions = load_master(module)
    if questions is None:
        return None
    ledger = load_ledger(module)
    stale, untracked, missing_source = [], [], []
    for q in questions:
        qid = q.get("id")
        h = source_hash(q)
        if h is None:
            missing_source.append(qid)
            continue
        recorded = ledger.get(qid, {})
        for loc in sorted(q.get("text", {})):
            if loc == SOURCE_LOCALE:
                continue
            if q.get("explanation", {}).get(loc) is None:
                continue
            was = recorded.get(loc)
            if was is None:
                untracked.append((qid, loc))
            elif was != h:
                stale.append((qid, loc))
    return stale, untracked, missing_source


def cmd_check(args):
    total_stale = total_untracked = 0
    for module in sorted(MODULES):
        res = scan(module)
        if res is None:
            continue
        stale, untracked, missing = res
        if stale or untracked:
            print(f"\n{module}:")
        if stale:
            total_stale += len(stale)
            by_loc = {}
            for qid, loc in stale:
                by_loc.setdefault(loc, []).append(qid)
            print(f"  STALE ({len(stale)}) - German changed since these were checked:")
            for loc in sorted(by_loc):
                ids = by_loc[loc]
                shown = ", ".join(ids[:6]) + (f" ... +{len(ids)-6} more" if len(ids) > 6 else "")
                print(f"    {loc}: {len(ids)} - {shown}")
        if untracked:
            total_untracked += len(untracked)
            locs = sorted({loc for _, loc in untracked})
            print(f"  UNTRACKED ({len(untracked)}) - never stamped: {', '.join(locs)}")
    if total_stale or total_untracked:
        print(f"\nFAIL: {total_stale} stale, {total_untracked} untracked translation(s).")
        print("Re-check the flagged translations against the current German, then:")
        print("  python3 scripts/translation_ledger.py stamp --module <m> --locale <l>")
        return 1
    print("OK: every translation is stamped against the current German source.")
    return 0


def cmd_stamp(args):
    stamped = 0
    for module in sorted(MODULES):
        if args.module and module != args.module:
            continue
        questions = load_master(module)
        if questions is None:
            continue
        ledger = load_ledger(module)
        touched = False
        for q in questions:
            qid = q.get("id")
            if args.id and qid != args.id:
                continue
            h = source_hash(q)
            if h is None:
                continue
            for loc in q.get("text", {}):
                if loc == SOURCE_LOCALE:
                    continue
                if args.locale and loc != args.locale:
                    continue
                if q.get("explanation", {}).get(loc) is None:
                    continue
                if ledger.setdefault(qid, {}).get(loc) != h:
                    ledger[qid][loc] = h
                    stamped += 1
                    touched = True
        if touched:
            save_ledger(module, ledger)
            print(f"{module}: ledger updated")
    print(f"stamped {stamped} translation(s) as reconciled against current German")
    return 0


def cmd_status(args):
    print(f"{'module':<22}{'questions':>10}{'locales':>9}{'stale':>8}{'untracked':>11}")
    print("-" * 60)
    for module in sorted(MODULES):
        res = scan(module)
        if res is None:
            print(f"{module:<22}{'(no master)':>10}")
            continue
        stale, untracked, _ = res
        questions = load_master(module)
        locales = sorted({l for q in questions for l in q.get("text", {}) if l != SOURCE_LOCALE})
        print(f"{module:<22}{len(questions):>10}{len(locales):>9}{len(stale):>8}{len(untracked):>11}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("USAGE")[0].strip())
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="fail if any translation is stale or untracked")
    s = sub.add_parser("stamp", help="record translations as reconciled against current German")
    s.add_argument("--module", help="limit to one module")
    s.add_argument("--locale", help="limit to one locale")
    s.add_argument("--id", help="limit to one question id")
    sub.add_parser("status", help="summary table, never fails")
    args = ap.parse_args()
    return {"check": cmd_check, "stamp": cmd_stamp, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
