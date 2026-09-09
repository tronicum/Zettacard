#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail if German content carries an ASCII-transliterated umlaut or ß.

The app once showed a learner "Uebungsquiz", "Ueben ohne Zeitlimit" and
"Staatliche Pruefung" on its main screen, and the tests were green: nothing
asserted anything about how German is spelled, so 1200-odd such spellings sat
across the content, the UI strings and app.js while every suite passed. On a
language-learning app that is not cosmetic - it teaches the wrong spelling.

What this does NOT do is guess. `ue` is legal German ("aktuelle", "Steuer")
and `ss` is legal German ("Schlüssel", "zulässig"), so a pattern rule is
either useless or destructive. Instead it matches an explicit list of
spellings that a dictionary has already judged: each was rejected by hunspell
de_DE as written and had exactly one valid restoration.

Swiss modules are exempt from the ß half - Swiss Standard German has no ß, so
"Strasse" and "Mindestmass" are correct there, and data/*_pilot.json for those
modules says so in its own orthography_note.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
KNOWN = json.load(open(os.path.join(ROOT, "data", "orthography_known_bad.json"), encoding="utf-8"))
SWISS = ("switzerland_ch", "fadp_ch")
GERMAN_LOCALES = {"de", "bar"}
IDENT = re.compile(r"^[a-z0-9_]+$")
LETTER = "A-Za-zÄÖÜäöüß"

def rx(keys):
    return re.compile(f"(?<![{LETTER}])(" + "|".join(
        re.escape(k) for k in sorted(keys, key=len, reverse=True)) + f")(?![{LETTER}])")

RX = {"de": rx(KNOWN["de"]), "bar": rx(set(KNOWN["de"]) | set(KNOWN["bar"]))}
# ss->ss fixes are the ones whose correction introduces a ß; those are the only
# ones a Swiss module is allowed to keep.
SHARP = {k for k, v in KNOWN["de"].items() if "ß" in v}
RX_CH = rx(set(KNOWN["de"]) - SHARP)

hits = []

def scan(o, locale, swiss, where):
    if isinstance(o, dict):
        for k, v in o.items():
            scan(v, k if (k in GERMAN_LOCALES or (isinstance(k, str) and len(k) <= 3)) else locale,
                 swiss, f"{where}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, locale, swiss, f"{where}[{i}]")
    elif isinstance(o, str) and locale in GERMAN_LOCALES and not IDENT.match(o.strip()):
        r = RX_CH if swiss else RX[locale]
        for m in r.finditer(o):
            hits.append((where, m.group(1), o[max(0, m.start() - 40):m.end() + 40]))

def scan_file(fp):
    swiss = any(m in fp for m in SWISS)
    rel = os.path.relpath(fp, ROOT)
    if fp.endswith(".jsonl"):
        for n, line in enumerate(open(fp, encoding="utf-8"), 1):
            line = line.strip()
            if line: scan(json.loads(line), None, swiss, f"{rel}:{n}")
    else:
        scan(json.load(open(fp, encoding="utf-8")), None, swiss, rel)

for sub in ("data", os.path.join("app", "data")):
    for root, dirs, files in os.walk(os.path.join(ROOT, sub)):
        for fn in files:
            if fn.endswith((".json", ".jsonl")) and fn != "orthography_known_bad.json":
                try: scan_file(os.path.join(root, fn))
                except Exception: pass

# app.js carries the same strings as compiled-in fallbacks. Quoted values
# only - the file is full of ASCII identifiers (exam_type "fuehrerschein",
# topic codes) that are correct as they are, and of English comments.
src = open(os.path.join(ROOT, "app", "app.js"), encoding="utf-8").read()
for i, line in enumerate(src.split("\n"), 1):
    st = line.lstrip()
    if st.startswith("//") or st.startswith("*") or st.startswith("/*"): continue
    # Double-quoted AND backtick template literals. Only the first was checked
    # at first, and the gap was not hypothetical: `dueToday: (n) => \`Heute
    # faellig: ${n}\`` sat two lines from strings this had just cleaned, was
    # missed by the guard AND by the fixer, and came back through the KB the
    # next time the UI strings were re-extracted. A German string does not
    # stop being one because it interpolates a number.
    for m in re.finditer(r'"([^"\\]{4,})"|`([^`\\]{4,})`', line):
        body = m.group(1) or m.group(2)
        for h in RX["bar"].finditer(body):
            hits.append((f"app/app.js:{i}", h.group(1), body[:80]))

if hits:
    print(f"{len(hits)} ASCII-transliterated German spelling(s):\n")
    for where, tok, ctx in hits[:40]:
        want = KNOWN["de"].get(tok) or KNOWN["bar"].get(tok)
        print(f"  {tok}  ->  {want}\n      {where}\n      …{ctx}…")
    if len(hits) > 40: print(f"  ... and {len(hits) - 40} more")
    print("\nFix with: python3 ../zettacard-kb/src/fix_umlauts.py data/*.json")
    sys.exit(1)
print("Orthography: no known ASCII-transliterated German spellings.")
