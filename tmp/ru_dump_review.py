import json, sys
import os
root = os.path.expanduser("~/mnt/Zettacard/app/data/fuehrerschein")
de = json.load(open(f"{root}/locales/de.json", encoding="utf-8"))
ru = json.load(open(f"{root}/locales/ru.json", encoding="utf-8"))
core = json.load(open(f"{root}/core.json", encoding="utf-8"))
correct = {q['id']: q['correct'] for q in core['questions']}
ids = list(de.keys())
start = int(sys.argv[1])
end = int(sys.argv[2])
for i in ids[start:end]:
    d = de[i]; r = ru[i]
    print(f"=== {i} | correct={correct.get(i)} ===")
    print(f"DE-Q: {d['question']}")
    print(f"RU-Q: {r['question']}")
    for k in ['a','b','c','d']:
        if k in d['options']:
            print(f"  {k}) DE: {d['options'][k]}")
            print(f"  {k}) RU: {r['options'].get(k,'MISSING')}")
    print(f"DE-EXPL: {d.get('explanation','')}")
    print(f"RU-EXPL: {r.get('explanation','')}")
    print()
