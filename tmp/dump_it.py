import json, os

base = os.environ["HOME"] + "/mnt/Zettacard/app/data/fuehrerschein"
with open(base + "/locales/de.json", encoding="utf-8") as f:
    de = json.load(f)
with open(base + "/locales/it.json", encoding="utf-8") as f:
    it = json.load(f)
with open(base + "/core.json", encoding="utf-8") as f:
    core = json.load(f)
qs = core["questions"]

CHUNK = 30
outdir = os.environ["HOME"] + "/mnt/Zettacard/tmp/it_review_chunks"
os.makedirs(outdir, exist_ok=True)

for ci in range(0, len(qs), CHUNK):
    lines = []
    for i in range(ci, min(ci+CHUNK, len(qs))):
        q = qs[i]
        k = q["id"]
        correct = ",".join(q.get("correct", []))
        d = de[k]
        it_ = it[k]
        lines.append(f"=== [{i}] {k} correct={correct}")
        lines.append(f"DE-Q: {d['question']}")
        lines.append(f"IT-Q: {it_['question']}")
        for opt in ["a","b","c","d"]:
            if opt in d["options"]:
                lines.append(f"  {opt}) DE: {d['options'][opt]}")
                lines.append(f"  {opt}) IT: {it_['options'].get(opt,'<<MISSING>>')}")
        lines.append(f"DE-E: {d['explanation']}")
        lines.append(f"IT-E: {it_.get('explanation','<<MISSING>>')}")
        lines.append("")
    fname = f"{outdir}/chunk_{ci:03d}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(fname)
