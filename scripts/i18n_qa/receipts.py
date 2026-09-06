#!/usr/bin/env python3
"""Append-only verdict receipts: data/translation_state/verdicts/<module>.jsonl.

WHY A SEPARATE FILE FROM THE LEDGER
-----------------------------------
scripts/translation_ledger.py is deliberately dumb - one hash per cell, no
model, no opinion - and it gates CI. Writing model verdicts into it would
couple the gate to the advisory tier and change a schema that is already
committed and relied upon. So receipts live beside it, one JSON object per
line, append-only: history is the point, and an append never rewrites a line
somebody already reviewed.

WHAT A RECEIPT IS FOR
---------------------
CI cannot run a 7B model (no GPU, not enough RAM, and content must stay on the
developer's machine). So the Mac produces receipts and commits them, and CI
checks the receipts: "every cell that requires a verdict has one, whose
source_hash still matches today's German and whose target_hash still matches
today's translation". That check needs no model and runs in a second - see
verify_receipts.py.

A receipt is only a receipt if it pins all of: model + full digest, Ollama
version, prompt template sha, rendered-prompt sha, options+schema sha, the
source and target hashes and a UTC timestamp (ADR-ollama-setup §7). Nothing
here invents those; they come from the client call that produced the verdict.
"""
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
VERDICT_DIR = os.path.join(REPO, "data", "translation_state", "verdicts")

REQUIRED_FIELDS = (
    "module", "id", "locale", "source_hash", "target_hash",
    "model", "model_digest", "prompt_sha256", "verdict", "at",
)


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def path_for(module, directory=None):
    return os.path.join(directory or VERDICT_DIR, f"{module}.jsonl")


def validate(record):
    missing = [f for f in REQUIRED_FIELDS if not record.get(f)]
    if missing:
        raise ValueError(f"receipt is missing required field(s): {', '.join(missing)}")
    return record


def append(module, record, directory=None):
    """Append one receipt. Never rewrites, never reorders, never dedupes."""
    validate(record)
    directory = directory or VERDICT_DIR
    os.makedirs(directory, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with open(path_for(module, directory), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return line


def load(module, directory=None):
    """All receipts for a module, oldest first. Unreadable lines are reported, not skipped silently."""
    path = path_for(module, directory)
    if not os.path.exists(path):
        return [], []
    out, broken = [], []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except ValueError as exc:
                broken.append((n, str(exc)))
    return out, broken


def latest_index(module, directory=None):
    """{(id, locale) -> most recent receipt}. Later lines win; that is what append-only means."""
    records, _ = load(module, directory)
    index = {}
    for rec in records:
        index[(rec.get("id"), rec.get("locale"))] = rec
    return index
