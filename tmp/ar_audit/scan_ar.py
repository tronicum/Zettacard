import json, re

files = ["datenschutz_pilot.json","arbeitssicherheit_pilot.json","ki_act_pilot.json","it_sicherheit_pilot.json"]

bad_ctrl = re.compile(r'[‎‏‪-‮⁦-⁩]')
latin_in_arabic = re.compile(r'[؀-ۿ][A-Za-z][؀-ۿ]')

for fname in files:
    d = json.load(open(fname))
    for q in d['questions']:
        texts = []
        ar = q['text'].get('ar', {})
        if ar.get('question'): texts.append(('question', ar['question']))
        for k,v in ar.get('options', {}).items():
            texts.append((f'option_{k}', v))
        expl = q.get('explanation',{}).get('ar')
        if expl: texts.append(('explanation', expl))
        for label, t in texts:
            if bad_ctrl.search(t):
                print(f"{fname} {q['id']} [{label}] CONTROL CHAR: {repr(t[:100])}")
            if latin_in_arabic.search(t):
                print(f"{fname} {q['id']} [{label}] LATIN-IN-ARABIC: {t}")
print("scan done")
