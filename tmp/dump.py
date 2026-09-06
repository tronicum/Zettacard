import json, sys

name = sys.argv[1]
path = f"{sys.argv[2]}/data/{name}.json"
d = json.load(open(path, encoding='utf-8'))
qs = d['questions']
out = []
for q in qs:
    qid = q['id']
    correct = q.get('correct')
    de = q['text'].get('de', {})
    es = q['text'].get('es', {})
    ede = q.get('explanation', {}).get('de', '')
    ees = q.get('explanation', {}).get('es', '')
    out.append(f"=== ID {qid} correct={correct} ===")
    out.append(f"DE Q: {de.get('question')}")
    out.append(f"ES Q: {es.get('question')}")
    for k in ['a','b','c','d']:
        dov = de.get('options',{}).get(k)
        esv = es.get('options',{}).get(k)
        if dov is None and esv is None:
            continue
        out.append(f"  {k}) DE: {dov}")
        out.append(f"  {k}) ES: {esv}")
    out.append(f"DE EXP: {ede}")
    out.append(f"ES EXP: {ees}")
    out.append("")

text = "\n".join(out)
with open(f"{sys.argv[2]}/tmp/{name}_dump.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("wrote", len(qs), "questions")
