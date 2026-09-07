import json, sys

name = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

d = json.load(open(f'{sys.argv[4]}/data/{name}.json', encoding='utf-8'))
qs = d['questions']
out = []
for q in qs[start:end]:
    qid = q['id']
    correct = q.get('correct')
    de = q['text'].get('de', {})
    uk = q['text'].get('uk', {})
    out.append(f"=== {qid} correct={correct} ===")
    out.append(f"DE Q: {de.get('question','')}")
    out.append(f"UK Q: {uk.get('question','')}")
    for k in ['a','b','c','d']:
        deo = de.get('options',{}).get(k,'')
        uko = uk.get('options',{}).get(k,'')
        out.append(f" [{k}] DE: {deo}")
        out.append(f" [{k}] UK: {uko}")
    de_exp = q.get('explanation',{}).get('de','')
    uk_exp = q.get('explanation',{}).get('uk','')
    out.append(f"DE EXP: {de_exp}")
    out.append(f"UK EXP: {uk_exp}")
    out.append("")

print("\n".join(out))
