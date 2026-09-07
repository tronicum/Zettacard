import json, sys

fname = sys.argv[1]
outprefix = sys.argv[2]
chunk_size = int(sys.argv[3]) if len(sys.argv) > 3 else 50

d = json.load(open(fname, encoding='utf-8'))
qs = d['questions']

def fmt(q):
    lines = []
    lines.append(f"=== ID: {q['id']}  correct={q.get('correct')} ===")
    de = q['text'].get('de', {})
    ru = q['text'].get('ru', {})
    lines.append(f"DE Q: {de.get('question')}")
    lines.append(f"RU Q: {ru.get('question')}")
    deopt = de.get('options', {})
    ruopt = ru.get('options', {})
    for k in sorted(deopt.keys()):
        lines.append(f"  [{k}] DE: {deopt.get(k)}")
        lines.append(f"  [{k}] RU: {ruopt.get(k)}")
    deexp = q.get('explanation', {}).get('de')
    ruexp = q.get('explanation', {}).get('ru')
    lines.append(f"DE EXPL: {deexp}")
    lines.append(f"RU EXPL: {ruexp}")
    lines.append("")
    return "\n".join(lines)

for i in range(0, len(qs), chunk_size):
    chunk = qs[i:i+chunk_size]
    text = "\n".join(fmt(q) for q in chunk)
    fn = f"{outprefix}_{i:03d}.txt"
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(text)
    print(fn, len(chunk))
