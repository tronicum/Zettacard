import json, sys

fname = sys.argv[1]
with open(fname, encoding='utf-8') as f:
    data = json.load(f)

qs = data['questions']
print(f"TOTAL: {len(qs)}")
for q in qs:
    qid = q.get('id')
    correct = q.get('correct')
    de = q.get('text', {}).get('de', {})
    tr = q.get('text', {}).get('tr', {})
    de_expl = q.get('explanation', {}).get('de', '')
    tr_expl = q.get('explanation', {}).get('tr', '')
    print(f"\n===== ID {qid} correct={correct} =====")
    print(f"DE-Q: {de.get('question')}")
    print(f"TR-Q: {tr.get('question')}")
    de_opts = de.get('options', {})
    tr_opts = tr.get('options', {})
    for k in sorted(de_opts.keys()):
        print(f"  DE[{k}]: {de_opts.get(k)}")
        print(f"  TR[{k}]: {tr_opts.get(k)}")
    print(f"DE-EXPL: {de_expl}")
    print(f"TR-EXPL: {tr_expl}")
