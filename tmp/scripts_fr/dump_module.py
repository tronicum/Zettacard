import json, sys

module = sys.argv[1]
path = f"/sessions/rcw-01dljkimnrnap8ldte7prwra/mnt/Zettacard/data/{module}.json"
d = json.load(open(path, encoding='utf-8'))
qs = d['questions']
start = int(sys.argv[2])
end = int(sys.argv[3])
out = []
for q in qs[start:end]:
    out.append(f"=== ID: {q['id']}  correct={q['correct']} ===")
    de = q['text']['de']
    fr = q['text']['fr']
    out.append(f"DE Q: {de['question']}")
    out.append(f"FR Q: {fr['question']}")
    for k in ['a','b','c','d']:
        if k in de['options']:
            out.append(f"  {k}) DE: {de['options'][k]}")
            out.append(f"  {k}) FR: {fr['options'].get(k,'<<MISSING>>')}")
    out.append(f"DE EXPL: {q['explanation']['de']}")
    out.append(f"FR EXPL: {q['explanation'].get('fr','<<MISSING>>')}")
    out.append("")
print("\n".join(out))
