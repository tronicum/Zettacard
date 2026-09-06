import json, re, sys

MODULES = [
    ("fuehrerschein", "data/pilot_questions.json"),
    ("motorrad", "data/motorrad_pilot.json"),
    ("lkw", "data/lkw_pilot.json"),
    ("fuehrerschein_bus", "data/fuehrerschein_bus_pilot.json"),
]

BASE = sys.argv[1] if len(sys.argv) > 1 else "."

de_chars = re.compile(r'[äöüÄÖÜß]')
num_re = re.compile(r'\d+[.,]?\d*')
sign_re_de = re.compile(r'[Zz]eichen\s*(\d+)')
sign_re_en = re.compile(r'[Ss]ign\s*(\d+)|[Zz]eichen\s*(\d+)')
placeholder_tokens = ['high_stakes', 'grundstoff', 'TODO', 'XXX', 'lorem ipsum', 'placeholder', 'FIXME', '{{', '}}', 'undefined']

def get_texts(q, lang):
    t = q.get('text', {}).get(lang, {})
    parts = [t.get('question','')]
    opts = t.get('options', {})
    for k in sorted(opts.keys()):
        parts.append(opts[k])
    expl = q.get('explanation', {}).get(lang, '')
    parts.append(expl)
    return parts, opts, t.get('question',''), expl

total_report = []

for modname, relpath in MODULES:
    path = f"{BASE}/{relpath}"
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    qs = data['questions']
    flags = []
    for q in qs:
        qid = q.get('id')
        de_parts, de_opts, de_q, de_expl = get_texts(q, 'de')
        en_parts, en_opts, en_q, en_expl = get_texts(q, 'en')
        en_all = ' '.join(en_parts)
        de_all = ' '.join(de_parts)

        reasons = []
        if de_chars.search(en_all):
            reasons.append('DE_CHARS_IN_EN')
        for tok in placeholder_tokens:
            if tok.lower() in en_all.lower():
                reasons.append(f'PLACEHOLDER:{tok}')
        de_signs = set(m for m in sign_re_de.findall(de_all))
        en_signs_raw = sign_re_en.findall(en_all)
        en_signs = set(a or b for a,b in en_signs_raw)
        if de_signs or en_signs:
            if de_signs != en_signs:
                reasons.append(f'SIGN_MISMATCH de={de_signs} en={en_signs}')
        if not en_q.strip() or not en_expl.strip():
            reasons.append('EMPTY_EN')
        if set(de_opts.keys()) != set(en_opts.keys()):
            reasons.append(f'OPTION_KEY_MISMATCH de={sorted(de_opts.keys())} en={sorted(en_opts.keys())}')
        de_nums = set(num_re.findall(de_q) + num_re.findall(de_expl))
        en_nums = set(num_re.findall(en_q) + num_re.findall(en_expl))
        def norm(s):
            return s.replace(',', '.')
        de_nums_n = set(norm(x) for x in de_nums)
        en_nums_n = set(norm(x) for x in en_nums)
        if de_nums_n != en_nums_n:
            reasons.append(f'NUM_MISMATCH de={sorted(de_nums_n)} en={sorted(en_nums_n)}')

        if reasons:
            flags.append((qid, reasons))
    total_report.append((modname, len(qs), flags))

for modname, count, flags in total_report:
    print(f"=== {modname}: {count} questions, {len(flags)} flagged ===")
    for qid, reasons in flags:
        print(f"  {qid}: {' | '.join(reasons)}")
