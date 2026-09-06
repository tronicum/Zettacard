#!/usr/bin/env python3
"""The viability experiment: is a local judge good enough to be worth running?

ADR-ollama-setup.md §6 makes this the gate on everything else in Tier 3, and it
asks one question per locale:

    PRECISION ON THE KNOWN-GOOD HALF DECIDES VIABILITY.
    A judge that flags everything catches every defect and is worthless,
    because nobody reads a review queue of 800 items.

Recall is the second number, not the first. The thresholds are the ADR's:

    false-positive rate on known-good <= 10 %  AND recall on known-bad >= 70 %
        -> the locale may be enabled (blocking-capable)
    FP <= 20 % but recall short of 70 %
        -> advisory only: report, do not queue
    FP > 20 %
        -> disabled for that locale, whatever the recall is

WHERE THE LABELLED DATA COMES FROM
----------------------------------
Not from synthetic corpora: from this repository's own documented defects, so
the measurement is about the content we actually ship.

  zeichen-68     translations described an obstacle-passing sign while the
                 German describes Zeichen 214 (mandatory straight-or-right).
                 Pre-fix text recovered from tmp/pilot_questions.backup-*.json
                 (10 locales; the German is byte-identical to today's, so this
                 is a pure translation defect).
  zeichen-132    translations described a "Mofa frei" moped-exemption plate
                 while the German describes the "Fussgaenger" supplementary
                 sign 1010-53. Same backup; also tmp/pilot.pre-z132fix.json.
  zeichen-04     sign number rendered 133 instead of 136.
  high_stakes    the editorial clause "... - daher als high_stakes markiert."
                 that leaked into explanations and was then translated into ten
                 languages, recovered from tmp/datenschutz_pilot.pre-highstakes.json.
                 Applied to the TARGET only, so the target says something the
                 German does not. This class is Tier 1's job (check_data_integrity
                 catches the token exactly); it is included as a control, to see
                 whether the judge notices content the source does not contain.
  synthetic      language-neutral, deterministic mutations of known-good cells:
                 the correct option swapped with a distractor (answer-key
                 breakage), the whole target cell replaced by another question's
                 target cell (the zeichen-68 class), and a digit flip in the
                 stem. No hand-written per-language negations: writing those
                 needs a native speaker for each of eleven languages, and a bad
                 hand-written "negation" would poison the very number we are
                 trying to measure.

The known-good half is an equal number of cells, per locale, that the ledger
currently records as reconciled against today's German (they are "presumed
good", not proven good - if the judge flags one and a human agrees, it moves to
the bad half and the measurement gets better).

Because the seed files embed the defective text verbatim, they keep working
after tmp/ is cleaned out. Build once, commit, re-run against any model.

USAGE
    python3 scripts/i18n_qa/seed_eval.py build-seed             # writes seed/known_{bad,good}.json
    python3 scripts/i18n_qa/seed_eval.py run --model qwen2.5:7b-instruct
    python3 scripts/i18n_qa/seed_eval.py run --model aya-expanse:8b --locales pl,tr,uk,ar,hi
    python3 scripts/i18n_qa/seed_eval.py run --dry-run          # build every prompt, call nothing
"""
import argparse
import copy
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cells  # noqa: E402
import judge  # noqa: E402
import receipts  # noqa: E402
from ollama_client import DEFAULT_HOST, OllamaClient, OllamaError  # noqa: E402

SEED_DIR = os.path.join(HERE, "seed")
KNOWN_BAD = os.path.join(SEED_DIR, "known_bad.json")
KNOWN_GOOD = os.path.join(SEED_DIR, "known_good.json")
TMP = os.path.join(cells.REPO, "tmp")

# Real pre-fix material, in the order it is searched.
BACKUPS = [
    ("fuehrerschein", "tmp/pilot_questions.backup-20260905-072649.json",
     ["zeichen-68", "zeichen-132", "zeichen-04"]),
    ("fuehrerschein", "tmp/pilot.pre-z132fix.json", ["zeichen-132"]),
    ("datenschutz", "tmp/datenschutz_pilot.pre-highstakes.json", None),  # None = scan for the leak
]
DEFECT_BY_ID = {
    "zeichen-68": "wrong_sign_obstacle_vs_214",
    "zeichen-132": "wrong_sign_mofa_vs_pedestrian",
    "zeichen-04": "wrong_number_133_vs_136",
}
LEAK_TOKEN = "high_stakes"
MAX_LEAK_CELLS = 12  # a control, not the bulk of the set


# --------------------------------------------------------------------------
# building the labelled set
# --------------------------------------------------------------------------
def _load_backup(relpath):
    path = os.path.join(cells.REPO, relpath)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return {q["id"]: q for q in json.load(fh)["questions"]}


def _override(question, locale):
    return {"question": question["text"][locale]["question"],
            "options": dict(question["text"][locale]["options"]),
            "explanation": question["explanation"][locale]}


def collect_real_bad(verbose=True):
    """Pre-fix cells whose German is unchanged - i.e. genuine translation defects."""
    found, seen = [], set()
    for module, relpath, ids in BACKUPS:
        old = _load_backup(relpath)
        if old is None:
            if verbose:
                print(f"  (skipped, not present: {relpath})")
            continue
        cur = cells.load_questions(module)
        target_ids = ids if ids is not None else sorted(old)
        for qid in target_ids:
            if qid not in old or qid not in cur:
                continue
            oq, cq = old[qid], cur[qid]
            de_same = (oq["text"].get("de") == cq["text"].get("de")
                       and oq["explanation"].get("de") == cq["explanation"].get("de"))
            for locale in sorted(oq.get("text", {})):
                if locale == "de" or locale not in cq.get("text", {}):
                    continue
                if (qid, locale) in seen:
                    continue
                old_view = _override(oq, locale)
                if old_view == _override(cq, locale):
                    continue  # this locale was already correct back then
                if ids is None:
                    # leak scan: only cells whose old explanation carries the token
                    if LEAK_TOKEN not in old_view["explanation"]:
                        continue
                    defect = "leaked_high_stakes_token_in_target"
                    if sum(1 for f in found if f["defect"] == defect) >= MAX_LEAK_CELLS:
                        continue
                elif not de_same:
                    continue  # German moved too: Tier 0 owns that case, not the judge
                else:
                    defect = DEFECT_BY_ID.get(qid, "pre_fix_translation")
                seen.add((qid, locale))
                found.append({"module": module, "id": qid, "locale": locale, "label": "bad",
                              "defect": defect, "origin": relpath, "target_override": old_view})
    return found


def _mutate(view, kind, other_view=None):
    """Deterministic, language-neutral mutations. Returns None when not applicable."""
    v = copy.deepcopy(view)
    if kind == "swapped_correct_option":
        correct = sorted(v["correct"])
        distractors = [k for k in sorted(v["options"]) if k not in correct]
        if len(correct) != 1 or not distractors:
            return None
        c, d = correct[0], distractors[0]
        v["options"][c], v["options"][d] = v["options"][d], v["options"][c]
        return v
    if kind == "foreign_cell":
        if other_view is None or set(other_view["options"]) != set(v["options"]):
            return None
        v["question"] = other_view["question"]
        v["options"] = dict(other_view["options"])
        v["explanation"] = other_view["explanation"]
        return v
    if kind == "digit_flip":
        digits = [ch for ch in v["question"] if ch.isdigit()]
        if not digits:
            return None
        target = digits[0]
        replacement = "8" if target != "8" else "3"
        v["question"] = v["question"].replace(target, replacement, 1)
        return v
    return None


def build_synthetic(donor_pool, per_locale=3):
    """Synthetic bad cells, deterministically mutated from DONOR cells.

    The donors must be disjoint from the known-good half: a cell that appears
    in both halves would be scored twice with opposite labels and quietly
    corrupt both precision and recall.
    """
    out = []
    by_locale = {}
    for entry in donor_pool:
        by_locale.setdefault(entry["locale"], []).append(entry)
    kinds = ["swapped_correct_option", "foreign_cell", "digit_flip"]
    for locale in sorted(by_locale):
        pool = sorted(by_locale[locale], key=lambda e: e["id"])
        made = 0
        for i, entry in enumerate(pool):
            if made >= per_locale:
                break
            # cycle through the kinds so every locale exercises every mutation
            kind = kinds[made % len(kinds)]
            questions = cells.load_questions(entry["module"])
            view = cells.cell_view(questions[entry["id"]], locale)
            other = None
            if kind == "foreign_cell":
                donor = pool[(i + 1) % len(pool)]
                if donor["id"] == entry["id"]:
                    continue
                other = cells.cell_view(questions[donor["id"]], locale)
            mutated = _mutate(view, kind, other)
            if mutated is None:
                continue
            out.append({"module": entry["module"], "id": entry["id"], "locale": locale,
                        "label": "bad", "defect": "synthetic_" + kind, "origin": "generated",
                        "target_override": {k: mutated[k] for k in ("question", "options", "explanation")}})
            made += 1
    return out


def pick_good(counts, exclude_ids):
    """Ledger-clean cells, `counts[(module, locale)]` of them, spread across the id list."""
    out = []
    for (module, locale), n in sorted(counts.items()):
        questions = cells.load_questions(module)
        ledger = cells.load_ledger(module)
        clean = []
        for qid in sorted(questions):
            if qid in exclude_ids:
                continue
            q = questions[qid]
            h = cells.source_hash(q)
            if h is None or q.get("text", {}).get(locale) is None:
                continue
            if ledger.get(qid, {}).get(locale) == h:
                clean.append(qid)
        if not clean:
            continue
        # even stride, so the sample is not all from one topic prefix
        stride = max(1, len(clean) // max(1, n))
        chosen = [clean[i * stride] for i in range(min(n, len(clean)))]
        for qid in chosen:
            out.append({"module": module, "id": qid, "locale": locale, "label": "good",
                        "defect": None, "origin": "ledger-clean", "target_override": None})
    return out


def cmd_build_seed(args):
    os.makedirs(SEED_DIR, exist_ok=True)
    print("collecting real pre-fix defects from backups:")
    bad = collect_real_bad()
    for defect in sorted({b["defect"] for b in bad}):
        n = sum(1 for b in bad if b["defect"] == defect)
        locs = sorted({b["locale"] for b in bad if b["defect"] == defect})
        print(f"  {defect:<38} {n:>3} cell(s)  {','.join(locs)}")

    # Every half is drawn from a disjoint set of question ids, in this order:
    #   real bad -> good (matching count per locale) -> synthetic donors -> good again.
    # Sharing an id between the halves would score one cell twice with opposite
    # labels; sharing it between real and synthetic bad would double-count a defect.
    used = {b["id"] for b in bad}
    counts = {}
    for b in bad:
        counts[(b["module"], b["locale"])] = counts.get((b["module"], b["locale"]), 0) + 1
    good = pick_good(counts, used)
    used |= {g["id"] for g in good}

    per_loc = args.synthetic_per_locale
    if per_loc:
        # ask for spare donors: some mutations do not apply to some cells
        donor_counts = {k: per_loc * 3 for k in {(g["module"], g["locale"]) for g in good}}
        donors = pick_good(donor_counts, used)
        synth = build_synthetic(donors, per_locale=per_loc)
        used |= {s["id"] for s in synth}
        bad += synth
        print(f"  {'synthetic (deterministic mutations)':<38} {len(synth):>3} cell(s)")
        extra = {}
        for s_ in synth:
            extra[(s_["module"], s_["locale"])] = extra.get((s_["module"], s_["locale"]), 0) + 1
        good += pick_good(extra, used)
        used |= {g["id"] for g in good}

    overlap = {(b["id"], b["locale"]) for b in bad} & {(g["id"], g["locale"]) for g in good}
    if overlap:
        raise SystemExit(f"BUG: {len(overlap)} cell(s) are in both halves: {sorted(overlap)[:5]}")

    with open(KNOWN_BAD, "w", encoding="utf-8") as fh:
        json.dump(bad, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    with open(KNOWN_GOOD, "w", encoding="utf-8") as fh:
        json.dump(good, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"\nwrote {len(bad)} known-bad and {len(good)} known-good cell(s) to {SEED_DIR}/")
    print("The bad file embeds the defective text verbatim, so it survives tmp/ being cleaned.")
    return 0


# --------------------------------------------------------------------------
# running the evaluation
# --------------------------------------------------------------------------
def materialise(entry):
    """The question dict as the judge should see it, with any defective text spliced in."""
    questions = cells.load_questions(entry["module"])
    q = copy.deepcopy(questions[entry["id"]])
    ov = entry.get("target_override")
    if ov:
        q["text"][entry["locale"]] = {"question": ov["question"], "options": dict(ov["options"])}
        q["explanation"][entry["locale"]] = ov["explanation"]
    return q


def load_seeds(locales=None):
    seeds = []
    for path in (KNOWN_BAD, KNOWN_GOOD):
        if not os.path.exists(path):
            raise SystemExit(f"{path} not found - run `seed_eval.py build-seed` first")
        with open(path, encoding="utf-8") as fh:
            seeds.extend(json.load(fh))
    if locales:
        seeds = [s for s in seeds if s["locale"] in locales]
    seeds.sort(key=lambda s: (s["locale"], s["label"], s["module"], s["id"], s.get("defect") or ""))
    return seeds


def decide(fp_rate, recall):
    """The ADR's per-locale gate. Precision on the good half comes first."""
    if fp_rate > 0.20:
        return "DISABLED (too many false positives to be readable)"
    if fp_rate <= 0.10 and recall >= 0.70:
        return "ENABLED (blocking-capable)"
    return "ADVISORY (report only, do not queue)"


def summarise(results, flag_set):
    """flag_set: which verdicts count as 'flagged'. Errors are counted apart, never as a catch."""
    per_locale = {}
    for r in results:
        s = per_locale.setdefault(r["locale"], {"tp": 0, "fn": 0, "fp": 0, "tn": 0,
                                                "err_bad": 0, "err_good": 0, "ms": []})
        if r.get("elapsed_ms"):
            s["ms"].append(r["elapsed_ms"])
        flagged = r["verdict"] in flag_set
        if r["verdict"] == "error":
            s["err_bad" if r["label"] == "bad" else "err_good"] += 1
            flagged = False
        if r["label"] == "bad":
            s["tp" if flagged else "fn"] += 1
        else:
            s["fp" if flagged else "tn"] += 1
    return per_locale


def render_report(per_locale, per_defect, model, digest, ollama_version, flag_label, n):
    lines = []
    lines.append(f"### Flag policy: {flag_label}\n")
    lines.append("| locale | n_bad | caught | recall | n_good | FP | FP rate | precision | errors | median s/cell | decision |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    tot = {"tp": 0, "fn": 0, "fp": 0, "tn": 0, "err": 0}
    for loc in sorted(per_locale):
        s = per_locale[loc]
        n_bad, n_good = s["tp"] + s["fn"], s["fp"] + s["tn"]
        recall = s["tp"] / n_bad if n_bad else float("nan")
        fp_rate = s["fp"] / n_good if n_good else float("nan")
        precision = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else float("nan")
        med = statistics.median(s["ms"]) / 1000 if s["ms"] else 0
        for k in ("tp", "fn", "fp", "tn"):
            tot[k] += s[k]
        tot["err"] += s["err_bad"] + s["err_good"]
        dec = decide(fp_rate if fp_rate == fp_rate else 1.0, recall if recall == recall else 0.0)
        lines.append(
            f"| {loc} | {n_bad} | {s['tp']} | {recall:.0%} | {n_good} | {s['fp']} | {fp_rate:.0%} "
            f"| {precision:.0%} | {s['err_bad'] + s['err_good']} | {med:.1f} | {dec} |")
    n_bad, n_good = tot["tp"] + tot["fn"], tot["fp"] + tot["tn"]
    recall = tot["tp"] / n_bad if n_bad else 0
    fp_rate = tot["fp"] / n_good if n_good else 0
    precision = tot["tp"] / (tot["tp"] + tot["fp"]) if (tot["tp"] + tot["fp"]) else 0
    lines.append(f"| **all** | {n_bad} | {tot['tp']} | {recall:.0%} | {n_good} | {tot['fp']} | "
                 f"{fp_rate:.0%} | {precision:.0%} | {tot['err']} | | {decide(fp_rate, recall)} |")
    lines.append("")
    lines.append("Recall by defect class (how many of each real defect the judge caught):\n")
    lines.append("| defect | n | caught | recall |")
    lines.append("|---|---|---|---|")
    for defect in sorted(per_defect):
        d = per_defect[defect]
        lines.append(f"| {defect} | {d['n']} | {d['caught']} | {d['caught'] / d['n']:.0%} |")
    lines.append("")
    return "\n".join(lines)


def run_eval(seeds, client, model_override=None, prompt_name=judge.DEFAULT_PROMPT,
             log_path=None, on_result=None):
    template = judge.load_prompt_template(prompt_name)
    results = []
    log = open(log_path, "a", encoding="utf-8") if log_path else None
    try:
        for entry in seeds:
            question = materialise(entry)
            model = judge.model_for_locale(entry["locale"], model_override)
            record, prompt, call = judge.judge_cell(
                client, entry["module"], entry["id"], question, entry["locale"], model,
                template=template, prompt_name=prompt_name)
            record["label"] = entry["label"]
            record["defect"] = entry.get("defect")
            results.append(record)
            if log:
                log.write(json.dumps({**record, "prompt": prompt, "raw": call.get("raw")},
                                     ensure_ascii=False) + "\n")
                log.flush()
            if on_result:
                on_result(record)
    finally:
        if log:
            log.close()
    return results


def cmd_run(args):
    locales = [l.strip() for l in args.locales.split(",")] if args.locales else None
    seeds = load_seeds(locales)
    if args.limit:
        seeds = seeds[:args.limit]
    print(f"{len(seeds)} labelled cell(s): "
          f"{sum(1 for s in seeds if s['label'] == 'bad')} bad, "
          f"{sum(1 for s in seeds if s['label'] == 'good')} good")

    if args.dry_run:
        template = judge.load_prompt_template()
        for entry in seeds:
            q = materialise(entry)
            prompt = judge.build_prompt(cells.cell_view(q, "de"),
                                        cells.cell_view(q, entry["locale"]),
                                        entry["locale"], template=template)
            print(f"  {entry['label']:<4} {entry['id']:<18}{entry['locale']:<3} "
                  f"{(entry.get('defect') or '-'): <42} chars={len(prompt)}")
        print("\ndry run: prompts built for every cell, 0 model calls, no metrics produced.")
        return 0

    client = OllamaClient(host=args.ollama, timeout=args.timeout)
    os.makedirs(TMP, exist_ok=True)
    log_path = os.path.join(TMP, "judge_seed_log.jsonl")

    def echo(rec):
        expect = "bad " if rec["label"] == "bad" else "good"
        print(f"  [{expect}] {rec['verdict']:<7} {rec['id']:<18}{rec['locale']:<3} "
              f"{','.join(rec.get('reasons', [])) or '-'}")

    try:
        results = run_eval(seeds, client, args.model, log_path=log_path, on_result=echo)
    except OllamaError as exc:
        print(f"\nABORTED: {exc}", file=sys.stderr)
        return 2

    report = build_report(results, args.model or "(per-locale defaults)")
    out = os.path.join(TMP, "judge_seed_report.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(report)
    print("\n" + report)
    print(f"report: {out}\nfull prompts and raw replies: {log_path}")
    return 0


def build_report(results, model_label):
    header = [
        "# Tier 3 judge - seeded viability report",
        "",
        f"- model: `{model_label}`",
        f"- digests: " + ", ".join(sorted({f"{r['model']}@{r.get('model_digest', '?')[:19]}" for r in results})),
        f"- ollama: " + ", ".join(sorted({str(r.get("ollama_version")) for r in results})),
        f"- prompt: " + ", ".join(sorted({f"{r.get('prompt_file')}@{r.get('prompt_template_sha256', '')[:12]}" for r in results})),
        f"- cells: {len(results)}",
        "",
        "## How to read this",
        "",
        "**Precision on the known-good half is what decides viability.** A judge that flags",
        "everything has perfect recall and is worthless: nobody reads a review queue of",
        "hundreds of items, and the tier gets switched off within a week. Read the FP-rate",
        "column first, the recall column second.",
        "",
        "Thresholds (ADR-llm-translation-qa / ADR-ollama-setup §6): FP rate on known-good",
        "<= 10 % **and** recall >= 70 % enables a locale; FP > 20 % disables it whatever the",
        "recall; anything in between is advisory - reported, never queued, never blocking.",
        "",
        "The known-good cells are *presumed* good (ledger-clean, not natively reviewed). A",
        "flag on one of them may be a real find; check before counting it as a false positive.",
        "",
    ]
    per_defect = {}
    for r in results:
        if r["label"] != "bad":
            continue
        d = per_defect.setdefault(r["defect"] or "?", {"n": 0, "caught": 0})
        d["n"] += 1
        if r["verdict"] == "fail":
            d["caught"] += 1
    body = [
        render_report(summarise(results, {"fail"}), per_defect, model_label, None, None,
                      "`fail` only (strict - what would block)", len(results)),
        render_report(summarise(results, {"fail", "unsure"}), per_defect, model_label, None, None,
                      "`fail` or `unsure` (the actual review-queue size)", len(results)),
    ]
    errors = [r for r in results if r["verdict"] == "error"]
    if errors:
        body.append(f"### {len(errors)} unusable repl(ies)\n")
        body.append("An unparseable or schema-violating reply is counted as an error, never as a")
        body.append("pass and never as a catch. A model that cannot fill a six-boolean schema")
        body.append("should not be trusted with a polarity call either.\n")
        for r in errors[:10]:
            body.append(f"- `{r['id']}/{r['locale']}`: {r.get('error')} - {r.get('raw_excerpt', '')[:120]!r}")
        body.append("")
    return "\n".join(header + body)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("USAGE")[0].strip(),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build-seed", help="rebuild seed/known_{bad,good}.json from repo backups")
    b.add_argument("--synthetic-per-locale", type=int, default=3,
               help="one of each mutation kind per locale by default")
    r = sub.add_parser("run", help="judge the labelled set and report precision/recall per locale")
    r.add_argument("--model", help="one model for every locale; default = per-locale defaults")
    r.add_argument("--locales")
    r.add_argument("--limit", type=int)
    r.add_argument("--ollama", default=DEFAULT_HOST)
    r.add_argument("--timeout", type=int, default=300)
    r.add_argument("--dry-run", action="store_true", help="build prompts, call no model")
    args = ap.parse_args(argv)
    return {"build-seed": cmd_build_seed, "run": cmd_run}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
