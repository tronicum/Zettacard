#!/usr/bin/env python3
"""Tier 2 (OPTIONAL): embedding pre-filter that RANKS candidates for the judge.

READ THIS BEFORE USING IT
-------------------------
This tier is subordinate to Tiers 0 and 1 and is not allowed to fail a build.
Tier 0 (translation_ledger.py) catches source drift with zero false positives
and no model; Tier 1 (check_data_integrity.py) catches structure and leaked
tokens exactly. Everything here is a heuristic on top of those two, and its
only job is to put the ~16,000 unjudged cells in a sensible order so the
expensive Tier 3 judge is spent on the plausible 200 first.

What it can and cannot see (ADR-llm-translation-qa, option O3):
  CAN  - a cell that describes a different sign/situation than the German
         (the zeichen-68 class) lands far from its source in embedding space.
  CANNOT - polarity ("must" vs "must not" embed almost identically), a single
         wrong number, or a false friend. Never read a high similarity as
         "this translation is fine".

Only the stem and the correct option are embedded. Distractors are NEVER
embedded, because this project's distractors are deliberately not literal
translations (see judge.py); embedding them would rank correct localisation as
suspicious. The explanation is excluded too - it is long, freely worded, and
would dominate the cosine.

Thresholds are deliberately NOT hard-coded per locale. Cross-lingual similarity
for hi/ar/uk sits systematically lower than for es/fr even when the translation
is perfect, so a fixed number would either flag those three locales wholesale
or clear everything else. The tool therefore reports a ranked list plus each
locale's own distribution (median / p10), and only the "near-certainly wrong"
floor of 0.20 from the ADR is treated as more than advisory.

    python3 scripts/i18n_qa/embed_screen.py --module fuehrerschein --locales pl,tr --top 40
    python3 scripts/i18n_qa/embed_screen.py --module fuehrerschein --json tmp/tier2_candidates.json
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cells  # noqa: E402
from ollama_client import DEFAULT_HOST, OllamaClient, OllamaError, sha256_text  # noqa: E402

DEFAULT_EMBED_MODEL = "bge-m3"
HARD_FLOOR = 0.20  # ADR: below this the two texts are near-certainly about different things
CACHE_DIR = os.path.join(cells.REPO, "tmp", "embed_cache")


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)


def screen_text(view):
    """Stem + correct option only. The whole point of this tier's precision."""
    parts = [view["question"].strip()]
    for letter in sorted(view["correct"]):
        if letter in view["options"]:
            parts.append(view["options"][letter].strip())
    return " ".join(p for p in parts if p)


class EmbedCache:
    """Content-addressed on disk: an unchanged German cell is embedded once for all 11 locales."""

    def __init__(self, client, model, directory=CACHE_DIR):
        self.client, self.model, self.dir = client, model, directory
        os.makedirs(directory, exist_ok=True)

    def get(self, text):
        key = sha256_text(self.model + "\n" + text)
        path = os.path.join(self.dir, key + ".json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)["v"]
        vec = self.client.embed(self.model, [text])["vectors"][0]
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"model": self.model, "v": vec}, fh)
        return vec


def run(module, locales, ids, model, client, top, out_json):
    cache = EmbedCache(client, model)
    rows = []
    for qid, question, locale in cells.iter_cells(module, locales=locales, ids=ids):
        de = screen_text(cells.cell_view(question, cells.SOURCE_LOCALE))
        tgt = screen_text(cells.cell_view(question, locale))
        sim = cosine(cache.get(de), cache.get(tgt))
        rows.append({"module": module, "id": qid, "locale": locale,
                     "similarity": round(sim, 4),
                     "below_hard_floor": sim < HARD_FLOOR,
                     "source_hash": cells.source_hash(question),
                     "target_hash": cells.target_hash(question, locale)})
    rows.sort(key=lambda r: r["similarity"])

    by_locale = {}
    for r in rows:
        by_locale.setdefault(r["locale"], []).append(r["similarity"])
    print(f"{'locale':<8}{'n':>6}{'median':>9}{'p10':>9}{'min':>9}{'<floor':>8}")
    print("-" * 49)
    for loc in sorted(by_locale):
        s = sorted(by_locale[loc])
        med = s[len(s) // 2]
        p10 = s[max(0, int(len(s) * 0.10) - 1)]
        print(f"{loc:<8}{len(s):>6}{med:>9.3f}{p10:>9.3f}{s[0]:>9.3f}"
              f"{sum(1 for x in s if x < HARD_FLOOR):>8}")
    print(f"\nlowest {min(top, len(rows))} cell(s) - CANDIDATES for the judge, not failures:")
    for r in rows[:top]:
        print(f"  {r['similarity']:.3f}  {r['id']:<18}{r['locale']}"
              + ("   <- below hard floor" if r["below_hard_floor"] else ""))
    if out_json:
        os.makedirs(os.path.dirname(os.path.abspath(out_json)), exist_ok=True)
        with open(out_json, "w", encoding="utf-8") as fh:
            json.dump(rows[:top], fh, ensure_ascii=False, indent=2)
        print(f"\nwrote {min(top, len(rows))} candidate(s) to {out_json}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--module", required=True)
    ap.add_argument("--locales")
    ap.add_argument("--id", action="append", dest="ids")
    ap.add_argument("--model", default=DEFAULT_EMBED_MODEL)
    ap.add_argument("--ollama", default=DEFAULT_HOST)
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--json", dest="out_json", help="write the candidate list here")
    args = ap.parse_args(argv)
    locales = [l.strip() for l in args.locales.split(",")] if args.locales else None
    try:
        return run(args.module, locales, set(args.ids) if args.ids else None,
                   args.model, OllamaClient(host=args.ollama), args.top, args.out_json)
    except OllamaError as exc:
        print(f"ABORTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
