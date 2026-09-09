#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail if user-facing copy claims an origin the records do not establish.

DEF-0003/0004/0005 (zettacard-kb/data/defects/_claims.jsonl). The catalogue
described its questions as "Original" in 22 module descriptions and on the
landing page in 12 languages. Two readings, both wrong: "authentic, from the
real exam" - impossible for a compliance module, where no official exam exists
at all - and "bespoke", which overstates how the sets were made. The PO's
position is that a learning package we assembled does not need to justify where
its questions came from, and does not elsewhere.

So the rule is narrow and mechanical: these words may not appear in copy a
learner reads. It does not try to judge whether any claim is TRUE - that
question is open for the four driving modules (Verkehrsblatt) and is settled
for the Sportboot pair only once the boating import carries its source licences
into the KB. It only stops the claim reappearing while that is unresolved.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
# Latin plus the scripts the landing page actually ships in. Written out rather
# than matched loosely: "original" is a normal word in several of these
# languages and only the origin-claim sense is at issue.
CLAIM = re.compile(
    r"\bOriginal\b|\boriginale?s?\b|\boriginali\b|Оригінальн|Оригинальн"
    r"|Oryginaln|أصلية|原创|मौलिक|[öÖ]zgün", re.I)

hits = []
p = os.path.join(ROOT, "app", "index.html")
for i, line in enumerate(open(p, encoding="utf-8"), 1):
    if line.lstrip().startswith("//") or line.lstrip().startswith("<!--"):
        continue
    for m in CLAIM.finditer(line):
        hits.append(("app/index.html", i, line[max(0, m.start()-45):m.end()+45].strip()))

for sub in ("data", os.path.join("app", "data")):
    for root, _, files in os.walk(os.path.join(ROOT, sub)):
        for fn in files:
            if not fn.endswith(".json"): continue
            fp = os.path.join(root, fn)
            try: d = json.load(open(fp, encoding="utf-8"))
            except Exception: continue
            meta = d.get("meta") if isinstance(d, dict) else None
            desc = meta.get("description") if isinstance(meta, dict) else None
            # Only the LEADING claim. "Original MCQs for ..." is the
            # positioning statement this defect is about; "REPLACES that
            # original ~30-question pool" and "the original 5 categories" are
            # ordinary English about an earlier version, and "Original
            # phrasing, AI-authored" (cka, amateurfunk) is an honest
            # disclosure that should survive, not be swept up. The first pass
            # of this check flagged all 13 of those and would have taught
            # whoever met it to ignore the check.
            if isinstance(desc, str) and CLAIM.match(desc.strip()):
                hits.append((os.path.relpath(fp, ROOT), 0, desc[:100]))

if hits:
    print(f"{len(hits)} origin claim(s) in learner-facing copy:\n")
    for where, line, ctx in hits[:30]:
        print(f"  {where}{':' + str(line) if line else ''}\n      …{ctx}…")
    print("\nSee zettacard-kb/data/defects/_claims.jsonl (DEF-0003/0004/0005).")
    sys.exit(1)
print("Claims: no unestablished origin claims in learner-facing copy.")
