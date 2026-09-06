#!/usr/bin/env python3
"""CI-side receipt check: "does a current verdict exist?" - without running a model.

This is the piece that makes a local-only Tier 3 acceptable (ADR-llm-translation-qa
§6, ADR-ollama-setup §9). GitHub-hosted runners have no GPU and not enough RAM
for a 7B judge, and the content is not supposed to leave the developer's
machine anyway. So the Mac judges and commits receipts; CI verifies them.

A receipt counts as current when its source_hash equals today's German hash AND
its target_hash equals today's translation hash. Either side moving invalidates
it, which is the same rule Tier 0 uses for stamps - a re-translation must be
re-judged, and so must a German edit.

`--require` selects which cells must have one. Default `high_stakes`, because a
blanket requirement would fail the build for the ~16,000 cells that have never
been judged and turn the check into noise on day one.

    python3 scripts/i18n_qa/verify_receipts.py --require high_stakes
    python3 scripts/i18n_qa/verify_receipts.py --module fuehrerschein --require all --locales pl,tr
    python3 scripts/i18n_qa/verify_receipts.py --require none          # only integrity of what exists

Exit 1 if a required receipt is missing or stale, or if any receipt line is
corrupt. Verdicts themselves never fail the build: Tier 3 is advisory, and a
`fail` receipt is a review item that Tier 0/1 do not know about.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cells  # noqa: E402
import receipts  # noqa: E402


def check_module(module, require, locales, problems, stats):
    index = receipts.latest_index(module)
    _, broken = receipts.load(module)
    for lineno, err in broken:
        problems.append(f"[{module}] receipts line {lineno} is not valid JSON: {err}")
    for qid, question, locale in cells.iter_cells(module, locales=locales):
        needed = require == "all" or (require == "high_stakes" and question.get("high_stakes"))
        rec = index.get((qid, locale))
        if rec is None:
            if needed:
                stats["missing"] += 1
                problems.append(f"[{module}] {qid}/{locale}: no verdict receipt")
            continue
        src, tgt = cells.source_hash(question), cells.target_hash(question, locale)
        if rec.get("source_hash") != src or rec.get("target_hash") != tgt:
            stats["stale"] += 1
            if needed:
                problems.append(
                    f"[{module}] {qid}/{locale}: receipt is stale "
                    f"({'German' if rec.get('source_hash') != src else 'translation'} changed since "
                    f"{rec.get('at')}) - re-judge and commit a new receipt")
            continue
        stats["current"] += 1
        stats.setdefault("verdicts", {})
        stats["verdicts"][rec.get("verdict", "?")] = stats["verdicts"].get(rec.get("verdict", "?"), 0) + 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--module", help="one module; default all")
    ap.add_argument("--locales", help="comma-separated")
    ap.add_argument("--require", choices=["none", "high_stakes", "all"], default="high_stakes")
    args = ap.parse_args(argv)

    locales = [l.strip() for l in args.locales.split(",")] if args.locales else None
    modules = [args.module] if args.module else sorted(cells.MODULES)
    problems, stats = [], {"missing": 0, "stale": 0, "current": 0}
    for module in modules:
        if cells.load_master(module) is None:
            continue
        check_module(module, args.require, locales, problems, stats)

    print(f"receipts: {stats['current']} current, {stats['stale']} stale, "
          f"{stats['missing']} missing (requirement: {args.require})")
    if stats.get("verdicts"):
        print("  current verdicts: " + ", ".join(f"{k}={v}" for k, v in sorted(stats["verdicts"].items())))
    if problems:
        print(f"\nFAILED - {len(problems)} problem(s):")
        for p in problems[:100]:
            print("  " + p)
        if len(problems) > 100:
            print(f"  ... and {len(problems) - 100} more")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
