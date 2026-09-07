import json, os

base = os.environ["HOME"] + "/mnt/Zettacard/app/data/fuehrerschein"

with open(base + "/locales/ar.json", "r", encoding="utf-8") as f:
    ar = json.load(f)
with open(base + "/locales/de.json", "r", encoding="utf-8") as f:
    de = json.load(f)
with open(base + "/core.json", "r", encoding="utf-8") as f:
    core = json.load(f)

core_ids = [q["id"] for q in core["questions"]]
print("valid JSON: OK")
print("core question count:", len(core_ids))
print("ar top-level key count:", len(ar))
print("ids match core (set equal):", set(ar.keys()) == set(core_ids))
print("no dup ids in core:", len(core_ids) == len(set(core_ids)))

mismatches = []
for qid in core_ids:
    if qid not in ar:
        mismatches.append((qid, "missing in ar"))
        continue
    if qid not in de:
        mismatches.append((qid, "missing in de"))
        continue
    de_keys = set(de[qid]["options"].keys())
    ar_keys = set(ar[qid]["options"].keys())
    if de_keys != ar_keys:
        mismatches.append((qid, f"option key mismatch de={de_keys} ar={ar_keys}"))

print("option-key mismatches:", len(mismatches))
for m in mismatches[:20]:
    print(" ", m)

# spot check the two fixed entries
print()
print("zeichen-04 question:", ar["zeichen-04"]["question"])
print("zeichen-68 options:", ar["zeichen-68"]["options"])
