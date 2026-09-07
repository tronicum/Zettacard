import json, sys

path = sys.argv[1]
out = sys.argv[2]
with open(path, encoding='utf-8') as f:
    data = json.load(f)

lines = []
for q in data['questions']:
    qid = q['id']
    correct = q.get('correct')
    de = q['text'].get('de', {})
    ru = q['text'].get('ru', {})
    lines.append(f"=== ID {qid} | correct={correct} ===")
    lines.append(f"DE Q: {de.get('question','')}")
    lines.append(f"RU Q: {ru.get('question','')}")
    de_opts = de.get('options', {})
    ru_opts = ru.get('options', {})
    for k in sorted(de_opts.keys()):
        lines.append(f"  DE[{k}]: {de_opts.get(k,'')}")
        lines.append(f"  RU[{k}]: {ru_opts.get(k,'')}")
    de_exp = q.get('explanation', {}).get('de', '')
    ru_exp = q.get('explanation', {}).get('ru', '')
    lines.append(f"DE EXP: {de_exp}")
    lines.append(f"RU EXP: {ru_exp}")
    lines.append("")

with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("questions:", len(data['questions']))
