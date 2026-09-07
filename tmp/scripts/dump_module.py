import json, sys

module_file = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

d = json.load(open(module_file))
qs = d['questions']
for q in qs[start:end]:
    qid = q['id']
    correct = q.get('correct')
    de = q.get('text',{}).get('de',{})
    tr = q.get('text',{}).get('tr',{})
    ede = q.get('explanation',{}).get('de','')
    etr = q.get('explanation',{}).get('tr','')
    print(f"=== ID {qid} correct={correct} ===")
    print(f"DE Q: {de.get('question')}")
    print(f"TR Q: {tr.get('question')}")
    for k in ['a','b','c','d']:
        if k in de.get('options',{}):
            print(f"  {k}) DE: {de['options'].get(k)}")
            print(f"     TR: {tr.get('options',{}).get(k)}")
    print(f"DE EXPL: {ede}")
    print(f"TR EXPL: {etr}")
    print()
