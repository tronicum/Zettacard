import json, os

base = os.environ["HOME"] + "/mnt/Zettacard/app/data/fuehrerschein"

with open(base + "/locales/it.json", "r", encoding="utf-8") as f:
    it = json.load(f)
with open(base + "/locales/de.json", "r", encoding="utf-8") as f:
    de = json.load(f)
with open(base + "/core.json", "r", encoding="utf-8") as f:
    core = json.load(f)

core_ids = [q["id"] for q in core["questions"]]
print("valid JSON: OK")
print("core question count:", len(core_ids))
print("it top-level key count:", len(it))
print("ids match core (set equal):", set(it.keys()) == set(core_ids))
print("no dup ids in core:", len(core_ids) == len(set(core_ids)))

mismatches = []
for qid in core_ids:
    if qid not in it:
        mismatches.append((qid, "missing in it"))
        continue
    if qid not in de:
        mismatches.append((qid, "missing in de"))
        continue
    de_keys = set(de[qid]["options"].keys())
    it_keys = set(it[qid]["options"].keys())
    if de_keys != it_keys:
        mismatches.append((qid, f"option key mismatch de={de_keys} it={it_keys}"))

print("option-key mismatches:", len(mismatches))
for m in mismatches[:20]:
    print(" ", m)

print()
print("zeichen-68:", json.dumps(it["zeichen-68"], ensure_ascii=False))
print("zeichen-132:", json.dumps(it["zeichen-132"], ensure_ascii=False))
print("zeichen-118 option c:", it["zeichen-118"]["options"]["c"])
