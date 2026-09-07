#!/usr/bin/env python3
"""
Refuse to deploy an app/ tree that is missing a module.

`app/data/` is only PARTLY a build artefact, and that asymmetry is what makes
this check necessary. `data/build_modules.py` owns `core.json` and `locales/`
for the modules listed in its `BUILT_MODULES` tuple and deliberately leaves
everything else alone - so `amateurfunk_a`, `amateurfunk_e`, `lksg` and
`waffensachkunde` live under `app/data/` with **no source anywhere in the build
path**. They exist only as committed output.

Consequences, both of which have very nearly happened:

  * A deploy assembled from a partial copy of `app/` - a tarball, a staged
    subset, a fresh checkout that never had them - silently drops four live
    modules. On 2026-09-06 this was one command away and was caught only by
    listing the directory first.
  * A module removed from `BUILT_MODULES`, or one whose `split_module()` call
    goes missing, disappears from the built tree with nothing objecting. The
    comments in build_modules.py record that happening to dora, nis2 and both
    sportboot modules already.

The expectation is derived from `data/modules_manifest.json` rather than from a
snapshot of a previous deploy. The manifest is what the app fetches to build its
picker, so a module listed there and absent from `app/data/` is not a warning -
it is a picker entry that leads nowhere. That makes the manifest the honest
source of truth for "what must be servable", and it needs no baseline file that
could itself go stale.

Exit codes: 0 all good; 1 something is missing or unreadable.

    python3 scripts/check_deploy_preflight.py
    python3 scripts/check_deploy_preflight.py --root . --quiet
"""
import argparse
import json
import os
import sys


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=here, help="repo root (default: parent of scripts/)")
    ap.add_argument("--quiet", action="store_true", help="only print problems")
    args = ap.parse_args()

    manifest_path = os.path.join(args.root, "data", "modules_manifest.json")
    app_data = os.path.join(args.root, "app", "data")

    problems, notes = [], []

    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except Exception as e:
        print(f"FATAL: cannot read {manifest_path}: {e}", file=sys.stderr)
        return 1

    expected = [m["exam_type"] for m in manifest.get("modules", [])]
    if not expected:
        print("FATAL: manifest lists no modules", file=sys.stderr)
        return 1

    for mod in expected:
        d = os.path.join(app_data, mod)
        core = os.path.join(d, "core.json")
        locales_dir = os.path.join(d, "locales")

        if not os.path.isdir(d):
            problems.append(f"{mod}: no directory at app/data/{mod} - the module "
                            f"is in the picker and has nothing to serve")
            continue
        if not os.path.isfile(core):
            problems.append(f"{mod}: no core.json")
            continue
        try:
            core_doc = json.load(open(core, encoding="utf-8"))
        except Exception as e:
            problems.append(f"{mod}: core.json is unreadable ({e})")
            continue

        questions = core_doc.get("questions") if isinstance(core_doc, dict) else core_doc
        if not questions:
            problems.append(f"{mod}: core.json holds no questions")
            continue

        if not os.path.isdir(locales_dir):
            problems.append(f"{mod}: no locales/ directory - every question would "
                            f"render empty")
            continue
        locale_files = sorted(f for f in os.listdir(locales_dir) if f.endswith(".json"))
        if not locale_files:
            problems.append(f"{mod}: locales/ is empty")
            continue

        # A locale file that does not cover every question is not fatal - the app
        # falls back per question - but a locale file covering NOTHING means the
        # split wrote an empty map, which renders as a module of blank cards.
        for lf in locale_files:
            p = os.path.join(locales_dir, lf)
            try:
                loc = json.load(open(p, encoding="utf-8"))
            except Exception as e:
                problems.append(f"{mod}/{lf}: unreadable ({e})")
                continue
            if not loc:
                problems.append(f"{mod}/{lf}: empty - every card would render blank")

        if not args.quiet:
            notes.append(f"  {mod:<22} {len(questions):>4} q   "
                         f"{len(locale_files):>2} locales")

    # A directory under app/data/ that no manifest entry claims is dead weight
    # being served. Not fatal - it may be mid-migration - but say so.
    if os.path.isdir(app_data):
        on_disk = {n for n in os.listdir(app_data)
                   if os.path.isdir(os.path.join(app_data, n))}
        orphans = sorted(on_disk - set(expected))
        if orphans:
            notes.append(f"  note: {len(orphans)} directory(ies) under app/data/ "
                         f"not in the manifest: {', '.join(orphans)}")

    if notes and not args.quiet:
        print(f"{len(expected)} modules in the manifest:")
        print("\n".join(notes))

    if problems:
        print(f"\nDEPLOY PREFLIGHT FAILED - {len(problems)} problem(s):",
              file=sys.stderr)
        for p in problems:
            print(f"  ! {p}", file=sys.stderr)
        print("\nRun `python3 data/build_modules.py` and check that every module "
              "in BUILT_MODULES also has a split_module() call.", file=sys.stderr)
        return 1

    print(f"\nDeploy preflight OK - all {len(expected)} manifest modules are "
          f"present and servable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
