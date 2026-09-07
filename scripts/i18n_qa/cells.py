#!/usr/bin/env python3
"""Loading and hashing of one (module, question id, locale) translation cell.

WHY THIS MODULE EXISTS SEPARATELY
---------------------------------
judge.py, embed_screen.py, seed_eval.py and receipts.py all need the same three
things: "give me the German cell", "give me the target cell", "give me the
hashes that identify both". Putting that in one place is the only way to
guarantee the hash written into a receipt is the same hash Tier 0 computes -
which is the whole point of the receipt.

The German hash is NOT reimplemented here. It is `translation_ledger.source_hash`,
imported from scripts/translation_ledger.py, so a receipt and a ledger stamp can
never disagree about what "the source moved" means. The target hash reuses the
very same function by handing it a question whose German slot holds the target
locale's text - identical normalisation by construction, not by copy-paste.
(test_offline.py asserts `target_hash(q, "de") == source_hash(q)`.)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(SCRIPTS, ".."))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import translation_ledger as ledger  # noqa: E402  (path set up above)

SOURCE_LOCALE = ledger.SOURCE_LOCALE
MODULES = ledger.MODULES
DATA = ledger.DATA
source_hash = ledger.source_hash
load_master = ledger.load_master
load_ledger = ledger.load_ledger


class CellError(Exception):
    """A requested cell does not exist, or has no German to compare against."""


def target_hash(question, locale):
    """Hash of a *translation* cell, normalised exactly like the German one.

    Implemented by re-labelling the target locale as the source locale and
    calling translation_ledger.source_hash, so the two can never drift apart.
    `correct` is included for the same reason it is included in the German
    hash: if the answer key moves, the translation's meaning of "option a"
    moves with it.
    """
    text = question.get("text", {}).get(locale)
    expl = question.get("explanation", {}).get(locale)
    if text is None or expl is None:
        return None
    shim = {
        "text": {SOURCE_LOCALE: text},
        "explanation": {SOURCE_LOCALE: expl},
        "correct": question.get("correct"),
    }
    return source_hash(shim)


def load_questions(module):
    questions = load_master(module)
    if questions is None:
        raise CellError(
            f"unknown module {module!r} or missing master file; known modules: "
            + ", ".join(sorted(MODULES))
        )
    return {q["id"]: q for q in questions}


def cell_view(question, locale):
    """The learner-visible half of a question in one locale, plus the key.

    Returns a plain dict so it can be embedded verbatim in a prompt, a seed
    file or a test fixture without any further shaping.
    """
    text = question.get("text", {}).get(locale)
    expl = question.get("explanation", {}).get(locale)
    if text is None or expl is None:
        raise CellError(f"{question.get('id')}: no {locale} text/explanation")
    return {
        "question": text.get("question", ""),
        "options": dict(text.get("options", {})),
        "explanation": expl,
        "correct": list(question.get("correct") or []),
    }


def iter_cells(module, locales=None, ids=None):
    """Yield (qid, question, locale) for every translated cell in a module."""
    questions = load_questions(module)
    for qid in sorted(questions):
        if ids and qid not in ids:
            continue
        q = questions[qid]
        if source_hash(q) is None:
            continue
        for loc in sorted(q.get("text", {})):
            if loc == SOURCE_LOCALE:
                continue
            if locales and loc not in locales:
                continue
            if q.get("explanation", {}).get(loc) is None:
                continue
            yield qid, q, loc


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
