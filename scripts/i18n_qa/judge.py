#!/usr/bin/env python3
"""Tier 3: bilingual LLM judge for one translation cell (ADR-llm-translation-qa.md §5).

WHAT IT IS AND IS NOT
---------------------
It is the LAST tier and the only advisory one. Tier 0 (translation_ledger.py)
and Tier 1 (check_data_integrity.py) gate CI; this produces review items. A
`fail` here is a request for a human to look, never an automatic revert.

THE DESIGN CONSTRAINT THAT DECIDES WHETHER THIS TOOL IS USEFUL AT ALL
---------------------------------------------------------------------
Distractor options in this repo are deliberately NOT literal translations: a
translator may swap in a wrong answer that is more plausible for that language.
A judge that asks "is this a faithful translation" would therefore flag several
hundred perfectly good cells and be switched off within a day. So distractors
are judged on exactly one question - "is this still clearly wrong, and not a
restatement of the correct option?" - and on nothing else. Both ADRs say this;
the rubric in prompts/judge_v1.md says it in capitals; and
`derive_verdict` additionally *drops* any letter the model names that is in
fact a correct-key letter, because "the correct answer reads as correct" is not
a defect.

THE OTHER NON-NEGOTIABLE: the model does not decide.
The schema contains a `verdict` field only because models produce better
booleans when they are also allowed to conclude. That field is recorded as
`model_self_verdict` and never used as the answer. The verdict this tool
reports is computed by `derive_verdict()` from the booleans, in Python, and is
unit-tested over every boolean combination.

A reply that is not JSON, or that is missing a field, or whose fields have the
wrong type, produces verdict "error". It is never treated as a pass. Silence
and garbage must cost something, otherwise a broken model looks like a clean
sweep.

USAGE (on the Mac, with Ollama running - see README.md)
    python3 scripts/i18n_qa/judge.py --module fuehrerschein --id zeichen-68 --locale pl --explain
    python3 scripts/i18n_qa/judge.py --module fuehrerschein --locales pl,tr --high-stakes --model qwen2.5:7b-instruct
    python3 scripts/i18n_qa/judge.py --module fuehrerschein --dry-run --id zeichen-132 --locale ar   # prints the prompt, calls nothing
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cells  # noqa: E402
from ollama_client import (  # noqa: E402
    DEFAULT_HOST, OllamaClient, OllamaError, sha256_text,
)
import receipts  # noqa: E402

PROMPT_DIR = os.path.join(HERE, "prompts")
DEFAULT_PROMPT = "judge_v1.md"

# The schema is part of the receipt: its sha256 is folded into options_sha256,
# so a schema change is visible as a non-reproduction rather than a mystery.
VERDICT_SCHEMA = {
    "type": "object",
    "required": [
        "stem_equivalent", "correct_option_equivalent", "polarity_preserved",
        "numbers_preserved", "distractor_became_correct",
        "explanation_facts_preserved", "verdict", "confidence", "evidence",
    ],
    "properties": {
        "stem_equivalent": {"type": "boolean"},
        "correct_option_equivalent": {"type": "boolean"},
        "polarity_preserved": {"type": "boolean"},
        "numbers_preserved": {"type": "boolean"},
        "distractor_became_correct": {
            "type": "array",
            "items": {"type": "string", "enum": ["a", "b", "c", "d", "e"]},
        },
        "explanation_facts_preserved": {"type": "boolean"},
        "verdict": {"type": "string", "enum": ["pass", "fail", "unsure"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {"type": "string", "maxLength": 400},
    },
}

# False on any of these = the answer key is wrong for this locale = fail.
HARD_BOOLS = (
    "stem_equivalent", "correct_option_equivalent",
    "polarity_preserved", "numbers_preserved",
)
# ADR §5 lists the explanation separately and does NOT make it a hard fail: an
# explanation defect is a review item, not "this question is unanswerable".
SOFT_BOOLS = ("explanation_facts_preserved",)
BOOL_FIELDS = HARD_BOOLS + SOFT_BOOLS

# Per-locale judge defaults from ADR-llm-translation-qa §"Model policy".
# On the target machine (Apple Silicon, 36 GB unified memory) a 12-14B judge and
# bge-m3 fit resident together comfortably, and a 27B at Q4 (~17-20 GB) fits on
# its own with the browser closed - so the split below is affordable there. It
# is still a default, not a finding: seed_eval.py decides per locale.
JUDGE_MODEL_BY_LOCALE = {
    "hi": "aya-expanse:8b", "ar": "aya-expanse:8b", "uk": "aya-expanse:8b",
    "tr": "aya-expanse:8b", "ro": "aya-expanse:8b",
}
DEFAULT_JUDGE_MODEL = "qwen2.5:7b-instruct"
# Downgrade-only: a low-confidence pass becomes "unsure". It can never turn an
# unsure into a pass. The number is the ADR's, and is a self-report, not a
# calibrated probability - which is exactly why it may only ever weaken a pass.
CONFIDENCE_FLOOR = 0.7


class JudgeProtocolError(Exception):
    """The model's reply cannot be read as a verdict. Never a pass."""


def model_for_locale(locale, override=None):
    if override:
        return override
    return JUDGE_MODEL_BY_LOCALE.get(locale, DEFAULT_JUDGE_MODEL)


def load_prompt_template(name=DEFAULT_PROMPT):
    path = os.path.join(PROMPT_DIR, name)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def render_cell_block(view):
    """Deterministic rendering of one cell. Sorted keys, fixed labels, no JSON escaping noise."""
    lines = ["question: " + view["question"].strip()]
    for letter in sorted(view["options"]):
        mark = "  <- marked correct" if letter in view["correct"] else ""
        lines.append(f"option {letter}: {view['options'][letter].strip()}{mark}")
    lines.append("explanation: " + view["explanation"].strip())
    return "\n".join(lines)


def build_prompt(source_view, target_view, locale, template=None):
    """Pure function: same inputs -> byte-identical prompt. Tested in test_offline.py."""
    tpl = template if template is not None else load_prompt_template()
    correct = ", ".join(sorted(source_view["correct"])) or "(none recorded)"
    return (
        tpl.replace("{{SOURCE}}", render_cell_block(source_view))
           .replace("{{TARGET}}", render_cell_block(target_view))
           .replace("{{LOCALE}}", locale)
           .replace("{{CORRECT}}", correct)
    )


def validate_reply(parsed, option_letters=None):
    """Return a normalised verdict dict, or raise JudgeProtocolError.

    Strict on purpose: a model that cannot fill this schema cannot be trusted
    with a Hindi polarity call either, and 'unparseable' must be visible in the
    seed-eval numbers rather than absorbed as a pass.
    """
    if not isinstance(parsed, dict):
        raise JudgeProtocolError("reply is not a JSON object")
    out = {}
    for field in BOOL_FIELDS:
        if field not in parsed:
            raise JudgeProtocolError(f"missing required field {field!r}")
        val = parsed[field]
        if not isinstance(val, bool):
            raise JudgeProtocolError(f"field {field!r} is {type(val).__name__}, expected boolean")
        out[field] = val
    letters = parsed.get("distractor_became_correct", [])
    if not isinstance(letters, list) or any(not isinstance(x, str) for x in letters):
        raise JudgeProtocolError("distractor_became_correct must be a list of option letters")
    if option_letters is not None:
        unknown = [x for x in letters if x not in option_letters]
        if unknown:
            raise JudgeProtocolError(
                f"distractor_became_correct names option(s) {unknown} that do not exist"
            )
    out["distractor_became_correct"] = sorted(set(letters))
    conf = parsed.get("confidence", None)
    if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 <= conf <= 1:
        raise JudgeProtocolError("confidence must be a number in [0, 1]")
    out["confidence"] = float(conf)
    evidence = parsed.get("evidence", "")
    if not isinstance(evidence, str):
        raise JudgeProtocolError("evidence must be a string")
    out["evidence"] = evidence.strip()
    self_verdict = parsed.get("verdict", "")
    out["model_self_verdict"] = self_verdict if isinstance(self_verdict, str) else ""
    return out


def derive_verdict(reply, correct_letters=(), confidence_floor=CONFIDENCE_FLOOR):
    """THE verdict. Computed here, in Python, from the booleans. Never the model's.

    Returns (verdict, reasons) with verdict in {"pass", "fail", "unsure"}.

    Rules, in order:
      * A correct-key letter named in distractor_became_correct is DISCARDED.
        The model is saying "the right answer is right"; that is not a defect,
        and left in it would fire on every well-translated cell.
      * Any hard boolean false, or any surviving distractor letter -> fail.
      * explanation_facts_preserved false -> unsure (ADR §5 keeps the
        explanation out of the hard-fail list; it is still a review item).
      * A fail with no evidence quote -> downgraded to unsure. An accusation
        the reviewer cannot check is not actionable (ADR §5).
      * A clean sheet below the confidence floor -> unsure. Downgrade only.
    """
    reasons = []
    correct = set(correct_letters or ())
    letters = [x for x in reply.get("distractor_became_correct", []) if x not in correct]
    for field in HARD_BOOLS:
        if reply.get(field) is False:
            reasons.append(field)
    if letters:
        reasons.append("distractor_became_correct=" + ",".join(sorted(letters)))
    soft = [f for f in SOFT_BOOLS if reply.get(f) is False]
    if reasons:
        if not reply.get("evidence"):
            return "unsure", reasons + ["no_evidence_quote(downgraded_from_fail)"]
        return "fail", reasons
    if soft:
        if not reply.get("evidence"):
            return "unsure", soft + ["no_evidence_quote"]
        return "unsure", soft
    if reply.get("confidence", 1.0) < confidence_floor:
        return "unsure", ["low_confidence"]
    return "pass", []


def judge_cell(client, module, qid, question, locale, model, template=None,
               prompt_name=DEFAULT_PROMPT, options=None):
    """Judge one cell and return a receipt-shaped record. Raises nothing on a bad reply."""
    source_view = cells.cell_view(question, cells.SOURCE_LOCALE)
    target_view = cells.cell_view(question, locale)
    tpl = template if template is not None else load_prompt_template(prompt_name)
    prompt = build_prompt(source_view, target_view, locale, template=tpl)
    started = time.time()
    call = client.generate_json(model, prompt, VERDICT_SCHEMA, options=options)
    elapsed_ms = int((time.time() - started) * 1000)

    record = {
        "module": module,
        "id": qid,
        "locale": locale,
        "source_hash": cells.source_hash(question),
        "target_hash": cells.target_hash(question, locale),
        "model": call["model"],
        "model_digest": call["model_digest"],
        "ollama_version": call["ollama_version"],
        "prompt_file": prompt_name,
        "prompt_template_sha256": sha256_text(tpl),
        "prompt_sha256": call["prompt_sha256"],
        "options_sha256": call["options_sha256"],
        "options": call["options"],
        "elapsed_ms": elapsed_ms,
        "at": receipts.utcnow(),
    }
    if call["parse_error"] or call["parsed"] is None:
        record.update(verdict="error", reasons=["unparseable_reply"],
                      error=call["parse_error"] or "empty reply",
                      raw_excerpt=(call["raw"] or "")[:300])
        return record, prompt, call
    try:
        reply = validate_reply(call["parsed"], option_letters=set(target_view["options"]))
    except JudgeProtocolError as exc:
        record.update(verdict="error", reasons=["schema_violation"], error=str(exc),
                      raw_excerpt=(call["raw"] or "")[:300])
        return record, prompt, call
    verdict, reasons = derive_verdict(reply, correct_letters=target_view["correct"])
    record.update(
        verdict=verdict, reasons=reasons,
        booleans={f: reply[f] for f in BOOL_FIELDS},
        distractor_became_correct=reply["distractor_became_correct"],
        confidence=reply["confidence"], evidence=reply["evidence"],
        model_self_verdict=reply["model_self_verdict"],
    )
    return record, prompt, call


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("USAGE")[0].strip(),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--module", required=True)
    ap.add_argument("--id", action="append", dest="ids", help="repeatable question id")
    ap.add_argument("--locales", help="comma-separated; default: every translated locale")
    ap.add_argument("--model", help="override the per-locale default judge model")
    ap.add_argument("--high-stakes", action="store_true", help="only high_stakes questions")
    ap.add_argument("--limit", type=int, help="stop after N cells")
    ap.add_argument("--ollama", default=DEFAULT_HOST)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--no-receipts", action="store_true", help="do not append to the receipt file")
    ap.add_argument("--explain", action="store_true", help="print the prompt and the raw reply")
    ap.add_argument("--dry-run", action="store_true",
                    help="build prompts and print them; make no model call at all")
    args = ap.parse_args(argv)

    locales = [l.strip() for l in args.locales.split(",")] if args.locales else None
    ids = set(args.ids) if args.ids else None
    todo = []
    for qid, question, locale in cells.iter_cells(args.module, locales=locales, ids=ids):
        if args.high_stakes and not question.get("high_stakes"):
            continue
        todo.append((qid, question, locale))
        if args.limit and len(todo) >= args.limit:
            break
    if not todo:
        print("no matching cells")
        return 0

    template = load_prompt_template(args.prompt)
    if args.dry_run:
        for qid, question, locale in todo:
            prompt = build_prompt(cells.cell_view(question, cells.SOURCE_LOCALE),
                                  cells.cell_view(question, locale), locale, template=template)
            print(f"===== {args.module} {qid} {locale}  "
                  f"prompt_sha256={sha256_text(prompt)[:16]} chars={len(prompt)} "
                  f"model={model_for_locale(locale, args.model)}")
            if args.explain:
                print(prompt)
        print(f"\ndry run: {len(todo)} cell(s), 0 model calls")
        return 0

    client = OllamaClient(host=args.ollama, timeout=args.timeout)
    counts = {}
    try:
        for qid, question, locale in todo:
            model = model_for_locale(locale, args.model)
            record, prompt, call = judge_cell(client, args.module, qid, question, locale, model,
                                              template=template, prompt_name=args.prompt)
            counts[record["verdict"]] = counts.get(record["verdict"], 0) + 1
            if not args.no_receipts:
                receipts.append(args.module, record)
            print(f"{record['verdict']:<7} {qid:<16} {locale:<3} "
                  f"{','.join(record.get('reasons', [])) or '-'}  "
                  f"conf={record.get('confidence', '-')} {record['elapsed_ms']}ms")
            if record.get("evidence"):
                print(f"        evidence: {record['evidence'][:200]}")
            if args.explain:
                print("---- prompt ----\n" + prompt)
                print("---- raw reply ----\n" + (call["raw"] or "")[:2000])
    except OllamaError as exc:
        print(f"\nABORTED: {exc}", file=sys.stderr)
        return 2
    print("\n" + json.dumps(counts, sort_keys=True))
    # Exit 0 even on fails: Tier 3 opens review items, it does not gate. CI gating
    # is verify_receipts.py's job, and it needs no model.
    return 0


if __name__ == "__main__":
    sys.exit(main())
