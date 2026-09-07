import json, sys

fname = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = int(sys.argv[3]) if len(sys.argv) > 3 else 999

d = json.load(open(fname))
qs = d['questions']
for q in qs[start:end]:
    qid = q['id']
    de = q['text'].get('de', {})
    ar = q['text'].get('ar', {})
    print(f"===== ID {qid} correct={q.get('correct')} =====")
    print("DE Q:", de.get('question'))
    for k in sorted(de.get('options', {})):
        print(f"  DE {k}:", de['options'][k])
    print("AR Q:", ar.get('question'))
    for k in sorted(ar.get('options', {})):
        print(f"  AR {k}:", ar.get('options', {}).get(k))
    print("DE EXPL:", q.get('explanation', {}).get('de'))
    print("AR EXPL:", q.get('explanation', {}).get('ar'))
    print()
