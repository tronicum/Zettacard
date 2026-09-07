import json, re, sys

# Latin letters that look like Cyrillic
latin_lookalikes = set('aAeEoOcCpPxXyYkKmMtTHBn')  # broad set of visually similar latin letters
cyrillic_re = re.compile('[Ѐ-ӿ]')
latin_re = re.compile('[A-Za-z]')

def scan_word(word):
    # word contains at least one cyrillic char and at least one latin char that's a lookalike
    has_cyr = bool(cyrillic_re.search(word))
    if not has_cyr:
        return False
    # check each latin char in word
    for ch in word:
        if ch in latin_lookalikes:
            return True
    return False

def walk_strings(obj, path=""):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            results.extend(walk_strings(v, path + "." + str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            results.extend(walk_strings(v, path + f"[{i}]"))
    elif isinstance(obj, str):
        # only care about ru fields, so check path
        if ".ru" in path or path.endswith(".ru"):
            words = re.findall(r"\S+", obj)
            for w in words:
                if scan_word(w):
                    results.append((path, w, obj[:80]))
    return results

for fname in sys.argv[1:]:
    with open(fname, encoding='utf-8') as f:
        data = json.load(f)
    hits = walk_strings(data)
    print(f"=== {fname}: {len(hits)} suspicious words ===")
    for path, w, ctx in hits:
        print(f"  {path}: {w!r}")
