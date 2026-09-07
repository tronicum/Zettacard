import json, sys, os

base = os.environ["HOME"] + "/mnt/Zettacard/data"
mod = sys.argv[1]
fname = {
    "motorrad": "motorrad_pilot.json",
    "lkw": "lkw_pilot.json",
    "bus": "fuehrerschein_bus_pilot.json",
}[mod]

with open(os.path.join(base, fname), encoding="utf-8") as f:
    d = json.load(f)

qs = d["questions"]
lines = []
for q in qs:
    de = q["text"]["de"]
    ar = q["text"].get("ar", {})
    de_expl = q["explanation"].get("de", "")
    ar_expl = q["explanation"].get("ar", "")
    lines.append(f"=== ID {q['id']} correct={q['correct']} legal={q.get('legal_basis','')} ===")
    lines.append(f"DE Q: {de['question']}")
    lines.append(f"AR Q: {ar.get('question','')}")
    for k in ["a","b","c","d"]:
        de_o = de["options"].get(k, "")
        ar_o = ar.get("options", {}).get(k, "")
        lines.append(f"  {k}) DE: {de_o}")
        lines.append(f"     AR: {ar_o}")
    lines.append(f"DE EXPL: {de_expl}")
    lines.append(f"AR EXPL: {ar_expl}")
    lines.append("")

out = "\n".join(lines)
print(f"total questions: {len(qs)}")
with open(os.environ["HOME"] + f"/mnt/Zettacard/tmp/ar_dump_{mod}.txt", "w", encoding="utf-8") as f:
    f.write(out)
print("written")
